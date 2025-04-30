import axios from 'axios'
import { useRouter } from 'vue-router'

// Cache mekanizması için basit bir Map
const cache = new Map()
const cacheTimeout = 5 * 60 * 1000 // 5 dakika cache süresi

// Temel axios yapılandırması
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  timeout: 15000
})

// Aktif istekleri takip etmek için
const pendingRequests = new Map()

// Global loading durumu
let globalLoadingTimeout = null
const loadingDelay = 300 // ms

// Loading durumunu yönetmek için event
const loadingEvent = new EventTarget()

// Loading durumunu değiştir
const setLoading = (loading) => {
  if (loading) {
    if (!globalLoadingTimeout) {
      globalLoadingTimeout = setTimeout(() => {
        loadingEvent.dispatchEvent(new CustomEvent('loading', { detail: true }))
      }, loadingDelay)
    }
  } else {
    if (globalLoadingTimeout) {
      clearTimeout(globalLoadingTimeout)
      globalLoadingTimeout = null
    }
    loadingEvent.dispatchEvent(new CustomEvent('loading', { detail: false }))
  }
}

// Cache kontrolü
const getCachedData = (key) => {
  const cached = cache.get(key)
  if (cached && Date.now() - cached.timestamp < cacheTimeout) {
    return cached.data
  }
  cache.delete(key) // Expired cache entry removed
  return null
}

const setCachedData = (key, data) => {
  cache.set(key, {
    data,
    timestamp: Date.now()
  })
}

// İstek anahtarı oluştur (internal usage)
const getRequestKey = (config) => {
  // Ensure consistent key generation, especially for params
  const paramsString = config.params ? JSON.stringify(config.params, Object.keys(config.params).sort()) : '{}';
  return `${config.method?.toLowerCase()}:${config.url}:${paramsString}`;
}

// Retry mekanizması için yapılandırma
const retryConfig = {
  retries: 2,
  retryDelay: 1000,
  retryCondition: (error) => {
    // Only retry network errors or 5xx server errors, not 4xx client errors (except 401 handled separately)
    return axios.isCancel(error) || !error.response || error.response.status >= 500
  }
}

// İstek interceptor'ı
apiClient.interceptors.request.use(
  async config => {
    // Cache kontrolü (sadece GET istekleri için)
    if (config.method === 'get' && !config.noCache) {
      const key = getRequestKey(config)
      const cachedData = getCachedData(key)
      if (cachedData) {
        console.log(`Cache hit for ${key}`)
        // Reject with a special flag to indicate cache hit
        return Promise.reject({ __CACHE_HIT__: true, data: cachedData, config: config })
      }
    }
    
    // Token kontrolü - Use token from auth store if available
    // Dynamically import store to avoid circular dependencies at module load time
    try {
        const { useAuthStore } = await import('../stores/auth');
        const authStore = useAuthStore();
        if (authStore.token) {
            config.headers.Authorization = `Bearer ${authStore.token}`;
            // console.log(`Setting Authorization header: Bearer ${authStore.token.substring(0, 15)}...`); // Reduce logging noise
        }
    } catch (e) {
        console.error("Could not import auth store in request interceptor:", e);
        // Fallback to localStorage if store import fails? Or handle error appropriately.
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
            // console.log(`Setting Authorization header (fallback): Bearer ${token.substring(0, 15)}...`);
        }
    }
    
    // İstek takibi
    const requestId = Math.random().toString(36).substring(7)
    config.requestId = requestId
    pendingRequests.set(requestId, config)
    
    // Loading durumunu güncelle
    if (pendingRequests.size === 1) {
      setLoading(true)
    }
    
    return config
  },
  error => {
    // Handle cache hit rejection
    if (error.__CACHE_HIT__) {
        // console.log(`Returning cached data for ${getRequestKey(error.config)}`); // Reduce logging noise
        return Promise.resolve({ data: error.data, __fromCache: true });
    }
    console.error('API isteği gönderilirken hata oluştu:', error)
    return Promise.reject(error)
  }
)

// Token yenileme için gerekli değişkenler
let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token) // Resolve with the new token
    }
  })
  failedQueue = []
}

// Yanıt interceptor'ı
apiClient.interceptors.response.use(
  response => {
    // İstek takibini kaldır
    if (response.config.requestId) {
      pendingRequests.delete(response.config.requestId)
    }
    
    // Loading durumunu güncelle
    if (pendingRequests.size === 0) {
      setLoading(false)
    }
    
    // GET isteklerini cache'le (if not from cache already)
    if (response.config.method === 'get' && !response.config.noCache && !response.__fromCache) {
      const key = getRequestKey(response.config)
      setCachedData(key, response.data)
      // console.log(`Cached data for ${key}`); // Reduce logging noise
    }
    
    return response
  },
  async error => {
    // Handle cache hit rejection passed from request interceptor
     if (error.__CACHE_HIT__) {
        // console.log(`Response interceptor: Returning cached data for ${getRequestKey(error.config)}`); // Reduce logging noise
        return Promise.resolve({ data: error.data, __fromCache: true });
     }

    const originalRequest = error.config
    
    // İstek takibini kaldır (eğer varsa)
    if (originalRequest?.requestId) {
      pendingRequests.delete(originalRequest.requestId)
    }
    
    // Loading durumunu güncelle
    if (pendingRequests.size === 0) {
      setLoading(false)
    }
    
    // Token yenileme kontrolü (Sadece 401 ve retry edilmemişse)
    if (error.response?.status === 401 && !originalRequest._retry) {
      
      if (isRefreshing) {
        // Eğer zaten token yenileme işlemi varsa, isteği sıraya ekle
        try {
          console.log('Token refresh in progress, queuing request:', originalRequest.url);
          const token = await new Promise((resolve, reject) => {
            failedQueue.push({ resolve, reject })
          })
          console.log('Retrying queued request with new token:', originalRequest.url);
          // Ensure the header is applied for the retry
          const newConfig = { ...originalRequest, headers: { ...originalRequest.headers, 'Authorization': `Bearer ${token}` }, _retry: true };
          return apiClient(newConfig); // Retry with a potentially cleaner config
        } catch (err) {
          console.error('Queued request failed after token refresh attempt:', err);
          return Promise.reject(err) // Propagate the error from the queue
        }
      }

      // İlk defa 401 alınıyor, yenileme işlemini başlat
      originalRequest._retry = true // Mark that we are attempting a retry
      isRefreshing = true
      console.log('Received 401, attempting token refresh...');

      try {
        const { useAuthStore } = await import('../stores/auth')
        const authStore = useAuthStore()
        const refreshed = await authStore.refreshAuthToken() // Yenilemeyi dene
        
        if (refreshed) {
          console.log('Token refresh successful.');
          const newToken = authStore.token // Store'dan YENİ token'ı al
          processQueue(null, newToken) // Sıradaki istekleri yeni token ile çöz
          
          console.log('Retrying original request with new token:', originalRequest.url);
          // Ensure the header is applied for the retry
          const newConfig = { ...originalRequest, headers: { ...originalRequest.headers, 'Authorization': `Bearer ${newToken}` }, _retry: true };
          return apiClient(newConfig); // Orijinal isteği YENİ TOKEN ve temiz config ile tekrar dene
        } else {
          // Yenileme başarısız oldu (refresh token geçersiz vs.)
          console.error('Token refresh failed, logging out.');
          processQueue(new Error('Token yenileme başarısız'), null) // Sıradaki istekleri hatayla reddet
          // authStore.logout() // refreshAuthToken already calls logout on failure
          return Promise.reject(error) // Orijinal 401 hatasını döndür
        }
      } catch (refreshError) {
        // Token yenileme sırasında beklenmedik bir hata oluştu
        console.error('Critical error during token refresh:', refreshError)
        processQueue(refreshError, null) // Sıradaki istekleri hatayla reddet
         try {
             const { useAuthStore } = await import('../stores/auth');
             const authStore = useAuthStore();
             if (authStore.isAuthenticated) { // Only logout if still authenticated
                authStore.logout(); // Kullanıcıyı sistemden at
             }
         } catch (logoutError) {
             console.error("Error logging out after refresh failure:", logoutError);
         }
        return Promise.reject(refreshError) // Yenileme hatasını döndür
      } finally {
        isRefreshing = false // Yenileme işlemi bitti
      }
    }
    
    // Retry mekanizması (401 dışındaki hatalar için)
    if (!originalRequest._retryCount) {
      originalRequest._retryCount = 0
    }
    
    if (originalRequest._retryCount < retryConfig.retries && 
        retryConfig.retryCondition(error)) {
      originalRequest._retryCount++
      console.log(`Retrying request (${originalRequest._retryCount}/${retryConfig.retries}): ${originalRequest.url}`);
      
      return new Promise(resolve => {
        setTimeout(() => {
          resolve(apiClient(originalRequest))
        }, retryConfig.retryDelay * originalRequest._retryCount)
      })
    }
    
    // Hata mesajlarını formatla (Eğer retry veya 401 değilse)
    let errorMessage = 'Bir hata oluştu'
    
    if (!error.response) {
      errorMessage = 'Sunucuya bağlanılamıyor. Lütfen internet bağlantınızı kontrol edin.'
      error.isNetworkError = true
    } else if (error.response.status === 0) {
      errorMessage = 'API erişim hatası. Güvenlik kısıtlamaları veya bağlantı sorunu olabilir.'
      error.isCorsError = true
    } else if (error.response.data) {
       // Daha detaylı hata mesajı çıkarmaya çalış
       const data = error.response.data;
       if (typeof data === 'string') {
           errorMessage = data;
       } else if (data.detail) {
           errorMessage = data.detail;
       } else if (data.message) {
           errorMessage = data.message;
       } else if (data.error) {
           errorMessage = data.error;
       } else if (data.non_field_errors) {
           errorMessage = data.non_field_errors.join(' ');
       } else if (typeof data === 'object') {
           // Try to extract field errors
           const fieldErrors = Object.entries(data)
               .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
               .join('; ');
           if (fieldErrors) {
               errorMessage = fieldErrors;
           } else {
               errorMessage = error.message; // Fallback
           }
       } else {
           errorMessage = error.message; // Fallback
       }

       if (data.errors) { // For validation errors specifically under 'errors' key
           error.validationErrors = data.errors;
           // Optionally append validation errors to the main message or handle separately
           const validationSummary = Object.entries(data.errors)
              .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
              .join('; ');
           errorMessage = `Doğrulama Hatası: ${validationSummary}`;
       }
    } else {
       errorMessage = error.message; // Fallback if no response data
    }
    
    error.userMessage = errorMessage.trim(); // Ensure no leading/trailing whitespace
    console.error(`API Error: ${error.response?.status} ${originalRequest?.method?.toUpperCase()} ${originalRequest?.url} - Message: ${error.userMessage}`);
    return Promise.reject(error)
  }
)

// Loading durumu için subscribe fonksiyonu
export const onLoadingStateChange = (callback) => {
  const handler = (event) => callback(event.detail)
  loadingEvent.addEventListener('loading', handler)
  return () => loadingEvent.removeEventListener('loading', handler)
}

// Cache temizleme fonksiyonu (tüm cache)
export const clearCache = () => {
  cache.clear()
  console.log('API cache cleared.');
}

// Belirli bir cache girdisini temizleme fonksiyonu
export const invalidateCacheEntry = (method, url, params = {}) => {
  const key = getRequestKey({ method, url, params });
  if (cache.has(key)) {
    cache.delete(key);
    console.log(`Cache invalidated for ${key}`);
    return true;
  }
  return false;
}

// Aktif istekleri iptal etme fonksiyonu
export const cancelPendingRequests = () => {
  pendingRequests.forEach((config, requestId) => {
    // Axios cancel tokens are usually attached to the config
    // This part depends on how cancel tokens are being generated and attached
    // Assuming a standard setup where a cancel token source might be on the config:
    if (config.cancelTokenSource) { 
      config.cancelTokenSource.cancel('İstek kullanıcı tarafından iptal edildi.');
      console.log(`Cancelled request: ${requestId}`);
    }
  });
  pendingRequests.clear();
}

export default apiClient
