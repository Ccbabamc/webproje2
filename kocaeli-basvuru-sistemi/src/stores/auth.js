import { defineStore } from 'pinia'
import apiClient from '../api/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
    isLoading: false,
    error: null,
    initialized: false
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    userRole: (state) => {
      if (!state.user) return null
      
      // Kullanıcı nesnesinde role alanının farklı formatlarını kontrol et
      if (state.user.role) return state.user.role
      if (state.user.groups && state.user.groups.length > 0) return state.user.groups[0]
      if (state.user.is_superuser) return 'SUPERADMIN'
      if (state.user.is_staff) return 'ADMIN'
      
      // Varsayılan rol - kullanıcı rolü yoksa aday olarak kabul et
      // Bu varsayım projenin mantığına göre değişebilir.
      // Eğer tanımsız rol olmamalıysa null döndürmek daha doğru olabilir.
      return 'CANDIDATE' 
    },
    
    // Belirli roller için yardımcı metodlar
    isAdmin: (state) => {
      const role = state.user?.role?.toUpperCase() || 
                  (state.user?.groups && state.user.groups.length > 0 
                    ? state.user.groups[0].toUpperCase() : null)
      // is_staff veya is_superuser kontrolü de ekleyelim
      return role === 'ADMIN' || role === 'SUPERADMIN' || 
             state.user?.is_staff || state.user?.is_superuser
    },
    
    isCandidate: (state) => {
      const role = state.user?.role?.toUpperCase() || 
                  (state.user?.groups && state.user.groups.length > 0 
                    ? state.user.groups[0].toUpperCase() : null)
      // Sadece 'ADAY' rolüne sahipse veya rol tanımlı değilse aday kabul edelim (varsayılan)
      return role === 'ADAY' // userRole getter'ındaki varsayıma göre güncellendi
    }
  },
  
  actions: {
    async initialize() {
      if (this.initialized) return
      console.log('Auth store initializing...');
      
      // Eğer token varsa kullanıcı bilgilerini getir
      if (this.token) {
        console.log('Token found, attempting to fetch user...');
        try {
          await this.fetchUser()
        } catch (error) {
          // fetchUser zaten 401 durumunda refresh deniyor ve başarısızsa logout yapıyor.
          // Bu yüzden burada ek bir refresh/logout mantığına gerek yok.
          console.error('Initialization failed during fetchUser:', error);
          // Eğer fetchUser sonrası hala token yoksa (logout yapıldıysa)
          if (!this.token) {
             console.log('Token invalid after fetchUser attempt, user logged out.');
          }
        }
      } else {
        console.log('No token found during initialization.');
      }
      
      this.initialized = true
      console.log('Auth store initialized.');
    },
    
    async login(credentials) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await apiClient.post('/api/auth/login/', credentials)
        console.log('Login response:', response.data)
        
        this.token = response.data.token || response.data.access
        this.refreshToken = response.data.refresh
        
        // User bilgisi response içinde varsa kaydet
        if (response.data.user) {
          this.user = response.data.user
          console.log('User data from login response stored:', this.user)
        } else {
          // User bilgisi yoksa ayrıca getir (Başarılı login sonrası yapılmalı)
          console.log('User data not in login response, fetching separately...');
          await this.fetchUser() 
        }
        
        // Token'ları yerel depolamaya kaydet
        localStorage.setItem('token', this.token)
        if (this.refreshToken) {
          localStorage.setItem('refreshToken', this.refreshToken)
        }
        console.log('Tokens stored after login.');
        
        return true
      } catch (error) {
        console.error('Login store error:', error)
        this.error = error.response?.data?.detail || 
                    error.response?.data?.message ||
                    error.response?.data?.error ||
                    'Giriş başarısız'
        // Başarısız girişte token'ları temizle
        this.logout(); 
        return false
      } finally {
        this.isLoading = false
      }
    },
    
    async register(userData) {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await apiClient.post('/api/auth/register/', userData)
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 
                   (error.response?.data?.errors ? Object.values(error.response.data.errors).join(', ') : 'Kayıt başarısız')
        return false
      } finally {
        this.isLoading = false
      }
    },
    
    async logout() {
      console.log('Logging out...');
      // Backend'e logout isteği gönderme (isteğe bağlı, token blacklist yoksa çok kritik değil)
      // if (this.token && this.refreshToken) {
      //   try {
      //     await apiClient.post('/api/auth/logout/', {
      //       refresh: this.refreshToken
      //     })
      //   } catch (error) {
      //     console.error('Logout API call failed:', error)
      //   }
      // }
      
      // Yerel durumu temizle
      this.user = null
      this.token = null
      this.refreshToken = null
      this.error = null
      this.initialized = false; // Re-initialize on next load
      
      // Yerel depolamayı temizle
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
      console.log('Local state and storage cleared.');
    },
    
    async fetchUser() {
      if (!this.token) {
        console.log('fetchUser called but no token exists.');
        return; // Token yoksa işlem yapma
      }
      
      this.isLoading = true
      console.log('Attempting to fetch user data with current token...');
      
      try {
        const response = await apiClient.get('/api/users/me/') // Sadece bu endpoint'i kullan
        console.log('User data fetched successfully:', response.data);
        this.user = response.data
      } catch (error) {
        console.error('Error fetching user data:', error.response?.status, error.message);
        // Token geçersizse (401), interceptor zaten yenilemeyi deneyecek.
        // Başarısız olursa interceptor logout yapacak veya hatayı iletecek.
        // Bu yüzden burada tekrar refresh/logout mantığına gerek yok,
        // sadece hatayı yukarıya fırlatmak yeterli olabilir.
        // Ancak initialize içinde yakalanması için hatayı fırlatmak önemli.
        this.user = null; // Kullanıcı alınamadıysa state'i temizle
        throw error; // Propagate the error for initialize() to handle
      } finally {
        this.isLoading = false
      }
    },
    
    // Token yenileme işlemi (axios interceptor tarafından kullanılır)
    async refreshAuthToken() {
      console.log('Attempting to refresh token...');
      if (!this.refreshToken) {
        console.log('No refresh token available.');
        return false;
      }
      
      try {
        const response = await apiClient.post('/api/auth/token/refresh/', {
          refresh: this.refreshToken
        })
        
        console.log('Token refresh successful:', response.data);
        
        // Yeni access token'ı kaydet
        this.token = response.data.access
        
        // Eğer yeni refresh token varsa onu da kaydet (ROTATE_REFRESH_TOKENS=True ise gelir)
        if (response.data.refresh) {
          this.refreshToken = response.data.refresh
          localStorage.setItem('refreshToken', this.refreshToken)
          console.log('New refresh token stored.');
        }
        
        localStorage.setItem('token', this.token)
        console.log('Auth Store: New access token set in state and localStorage.');
        
        return true
      } catch (error) {
        console.error('Token refresh failed:', error.response?.status, error.message);
        // Yenileme başarısızsa logout yap
        this.logout(); 
        return false
      }
    },
    
    // Token'ın geçerliliğini kontrol et (Artık çok gerekli olmayabilir)
    async checkAuth() {
      console.warn('checkAuth action is likely redundant, consider removing.');
      if (!this.token) return false
      
      try {
        await apiClient.get('/api/users/me/') // Use /me endpoint for verification
        return true
      } catch (error) {
        if (error.response?.status === 401 && this.refreshToken) {
          console.log('checkAuth failed with 401, attempting refresh...');
          return await this.refreshAuthToken()
        }
        // Diğer hatalarda veya refresh token yoksa logout
        this.logout()
        return false
      }
    },
    
    // Kullanıcı bilgilerini güncelle
    async updateUserData(userData) {
      if (!this.token || !this.user) return false
      
      this.isLoading = true
      
      try {
        // Endpoint düzeltildi: /api/users/users/me/ -> /api/users/me/
        const response = await apiClient.patch('/api/users/me/', userData) 
        this.user = response.data
        console.log('User data updated successfully.');
        return true
      } catch (error) {
        console.error('User update failed:', error);
        // Hata detayını kullanıcıya göstermek için error state'i güncellenebilir
        this.error = error.response?.data || 'Kullanıcı güncelleme hatası';
        return false
      } finally {
        this.isLoading = false
      }
    }
  }
})
