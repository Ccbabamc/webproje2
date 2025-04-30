<template>
  <div class="login-container">
    <div class="login-content">
      <div class="login-logo">
        <img src="../assets/koü-logo.png" alt="KOÜ Logo" class="logo-image">
        <h2>Kocaeli Üniversitesi</h2>
        <p>Akademik Başvuru Sistemi</p>
      </div>
      
      <div class="login-card">
        <h1>Giriş Yap</h1>
        <div class="login-card-tabs">
          <button 
            :class="['tab-btn', { active: loginMethod === 'tc' }]" 
            @click="switchMethod('tc')"
          >
            TC Kimlik ile Giriş
          </button>
          <button 
            :class="['tab-btn', { active: loginMethod === 'edevlet' }]" 
            @click="switchMethod('edevlet')"
          >
            e-Devlet ile Giriş
          </button>
        </div>

        <div v-if="loginMethod === 'tc'" class="fade-enter-active">
          <form @submit.prevent="handleSubmit" class="login-form" novalidate>
            <div class="form-group">
              <label for="tcno">TC Kimlik Numarası</label>
              <div class="input-wrapper" :class="{ 'has-error': errors.tcno }">
                <input 
                  type="text" 
                  id="tcno" 
                  v-model="form.tcno" 
                  @input="validateTCNo"
                  @blur="validateTCNo"
                  placeholder="TC Kimlik Numaranızı Giriniz"
                  maxlength="11"
                  :class="{ 'error': errors.tcno }"
                  autocomplete="username"
                >
                <span v-if="errors.tcno" class="error-text">{{ errors.tcno }}</span>
              </div>
            </div>
            
            <div class="form-group">
              <label for="password">Şifre</label>
              <div class="input-wrapper" :class="{ 'has-error': errors.password }">
                <div class="password-input-container">
                  <input 
                    :type="showPassword ? 'text' : 'password'" 
                    id="password" 
                    v-model="form.password"
                    @input="validatePassword"
                    @blur="validatePassword"
                    placeholder="Şifrenizi Giriniz"
                    :class="{ 'error': errors.password }"
                    autocomplete="current-password"
                  >
                  <button 
                    type="button" 
                    class="toggle-password-btn" 
                    @click="togglePassword"
                    :aria-label="showPassword ? 'Şifreyi gizle' : 'Şifreyi göster'"
                  >
                    {{ showPassword ? '👁️' : '👁️' }}
                  </button>
                </div>
                <span v-if="errors.password" class="error-text">{{ errors.password }}</span>
              </div>
            </div>
            
            <div class="form-actions">
              <div class="remember-me">
                <input type="checkbox" id="remember" v-model="form.remember">
                <label for="remember">Beni Hatırla</label>
              </div>
              <a href="#" class="forgot-password" @click.prevent="handleForgotPassword">
                Şifremi Unuttum
              </a>
            </div>
            
            <button 
              type="submit" 
              class="login-btn" 
              :disabled="isLoading || !isFormValid"
            >
              <div v-if="isLoading" class="spinner"></div>
              <span v-if="isLoading">Giriş Yapılıyor...</span>
              <span v-else>Giriş Yap</span>
            </button>
            
            <transition name="fade">
              <div v-if="error" class="error-message">
                <span class="error-icon">⚠️</span>
                {{ error }}
              </div>
            </transition>
          </form>
        </div>
        
        <div v-else class="edevlet-login fade-enter-active">
          <div class="edevlet-info">
            <p>e-Devlet üzerinden güvenli giriş yapmak için aşağıdaki butona tıklayınız.</p>
            <div class="edevlet-note">
              <span class="info-icon">ℹ️</span>
              <p>e-Devlet şifreniz ile giriş yaparak sistem üzerindeki işlemlerinizi gerçekleştirebilirsiniz.</p>
            </div>
          </div>
          <button 
            class="edevlet-btn" 
            @click="loginWithEdevlet"
            :disabled="isLoading"
          >
            <div v-if="isLoading" class="spinner"></div>
            <span v-else class="edevlet-icon">🔒</span>
            {{ isLoading ? 'Yönlendiriliyor...' : 'e-Devlet ile Giriş Yap' }}
          </button>
        </div>
        
        <div class="need-help">
          <p>
            Giriş yaparken sorun mu yaşıyorsunuz? 
            <a href="mailto:destek@kocaeli.edu.tr" class="support-link">
              Destek Hattı
            </a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { ref, computed } from 'vue'
import { onLoadingStateChange } from '../api/axios'

export default {
  name: 'LoginView',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    const showPassword = ref(false)
    const loginMethod = ref('tc')
    const form = ref({
      tcno: '',
      password: '',
      remember: false
    })
    const errors = ref({
      tcno: '',
      password: ''
    })
    const error = ref(null)
    const isLoading = ref(false)

    // Form doğrulama fonksiyonları
    const validateTCNo = () => {
      const tcno = form.value.tcno
      errors.value.tcno = ''
      
      if (!tcno) {
        errors.value.tcno = 'TC Kimlik Numarası zorunludur'
        return false
      }
      
      if (!/^\d{11}$/.test(tcno)) {
        errors.value.tcno = 'TC Kimlik Numarası 11 haneli olmalıdır'
        return false
      }
      
      // Simplified validation - ensure it starts with non-zero
      if (tcno[0] === '0') {
        errors.value.tcno = 'Geçersiz TC Kimlik Numarası'
        return false
      }
      
      return true
    }

    const validatePassword = () => {
      const password = form.value.password
      errors.value.password = ''
      
      if (!password) {
        errors.value.password = 'Şifre zorunludur'
        return false
      }
      
      if (password.length < 6) {
        errors.value.password = 'Şifre en az 6 karakter olmalıdır'
        return false
      }
      
      return true
    }

    const isFormValid = computed(() => {
      return validateTCNo() && validatePassword()
    })

    // Form gönderme
    const handleSubmit = async () => {
      if (!isFormValid.value) return
      
      error.value = null
      isLoading.value = true
      
      try {
        const success = await authStore.login({
          username: form.value.tcno,
          password: form.value.password
        })
        
        if (!success) {
          error.value = authStore.error || 'Giriş başarısız'
          return
        }
        
        const role = authStore.userRole?.toUpperCase()
        const redirectPath = (role === 'ADMIN' || role === 'SUPERADMIN') 
          ? '/admin/dashboard' 
          : '/candidate/dashboard'
        
        await router.push(redirectPath)
      } catch (err) {
        error.value = err.userMessage || 'Giriş yapılırken bir hata oluştu'
      } finally {
        isLoading.value = false
      }
    }

    // e-Devlet ile giriş
    const loginWithEdevlet = () => {
      isLoading.value = true
      const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
      window.location.href = `${baseUrl}/api/auth/edevlet-login/`
    }

    // Yardımcı fonksiyonlar
    const switchMethod = (method) => {
      loginMethod.value = method
      error.value = null
      errors.value = { tcno: '', password: '' }
    }

    const togglePassword = () => {
      showPassword.value = !showPassword.value
    }

    const handleForgotPassword = () => {
      // Şifre sıfırlama sayfasına yönlendir veya modal göster
      alert('Şifre sıfırlama özelliği yakında aktif olacaktır.')
    }

    // Global loading state'i dinle
    onLoadingStateChange((loading) => {
      isLoading.value = loading
    })

    return {
      form,
      errors,
      error,
      isLoading,
      showPassword,
      loginMethod,
      isFormValid,
      handleSubmit,
      validateTCNo,
      validatePassword,
      loginWithEdevlet,
      switchMethod,
      togglePassword,
      handleForgotPassword
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
  background-color: var(--light-color);
  background-image: linear-gradient(135deg, rgba(29, 131, 72, 0.05) 0%, rgba(29, 131, 72, 0.1) 100%);
}

.login-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 1000px;
}

.login-logo {
  text-align: center;
  margin-bottom: 30px;
}

.login-logo .logo-image {
  height: 80px;
  margin-bottom: 10px;
  border-radius: 8px;
  padding: 5px;
  background: white;
  box-shadow: var(--shadow-sm);
}

.login-logo h2 {
  font-size: 1.8rem;
  color: var(--primary-color);
  margin: 0;
  font-weight: 600;
}

.login-logo p {
  font-size: 1.1rem;
  color: var(--dark-color);
  margin: 5px 0 0;
  opacity: 0.8;
}

.login-card {
  background-color: white;
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  padding: 35px;
  width: 100%;
  max-width: 450px;
}

h1 {
  text-align: center;
  color: var(--primary-color);
  margin-bottom: 25px;
  font-size: 2rem;
  font-weight: 600;
}

.login-card-tabs {
  display: flex;
  margin-bottom: 25px;
  border-bottom: 1px solid var(--border-color);
}

.tab-btn {
  flex: 1;
  padding: 12px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  color: var(--dark-color);
  transition: all 0.3s ease;
  position: relative;
}

.tab-btn.active {
  color: var(--primary-color);
  font-weight: 600;
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: var(--primary-color);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.input-wrapper.has-error input {
  border-color: var(--danger-color);
}

label {
  font-weight: 500;
  color: var(--dark-color);
  font-size: 0.95rem;
}

input[type="text"],
input[type="password"] {
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  font-size: 1rem;
  transition: all 0.3s ease;
}

input[type="text"]:focus,
input[type="password"]:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(29, 131, 72, 0.1);
  outline: none;
}

.password-input-container {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}

.password-input-container input {
  width: 100%;
}

.toggle-password-btn {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  padding: 5px;
  font-size: 1.1rem;
  cursor: pointer;
  color: var(--dark-color);
  opacity: 0.6;
  transition: opacity 0.3s ease;
}

.toggle-password-btn:hover {
  opacity: 1;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 8px;
}

.remember-me input[type="checkbox"] {
  width: 16px;
  height: 16px;
  border: 2px solid var(--border-color);
  border-radius: 3px;
}

.forgot-password {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.forgot-password:hover {
  color: var(--dark-color);
}

.login-btn,
.edevlet-btn {
  padding: 14px;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius-sm);
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.login-btn:hover:not(:disabled),
.edevlet-btn:hover:not(:disabled) {
  background-color: var(--dark-color);
  transform: translateY(-1px);
}

.login-btn:disabled,
.edevlet-btn:disabled {
  background-color: var(--gray-color);
  cursor: not-allowed;
  transform: none;
}

.error-message {
  color: var(--danger-color);
  background-color: #fff5f5;
  padding: 12px;
  border-radius: var(--border-radius-sm);
  text-align: center;
  border: 1px solid #ffcccc;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.error-text {
  color: var(--danger-color);
  font-size: 0.85rem;
  margin-top: 4px;
}

.edevlet-login {
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.edevlet-info {
  margin-bottom: 10px;
}

.edevlet-note {
  background-color: var(--border-color);
  padding: 15px;
  border-radius: var(--border-radius-sm);
  margin-top: 15px;
  font-size: 0.9rem;
  color: var(--dark-color);
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.info-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.edevlet-btn {
  background-color: #9c0404;
  padding: 16px;
}

.edevlet-btn:hover:not(:disabled) {
  background-color: #7a0000;
}

.need-help {
  margin-top: 25px;
  text-align: center;
  font-size: 0.9rem;
  color: var(--gray-color);
}

.support-link {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.support-link:hover {
  color: var(--dark-color);
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.fade-enter-active {
  animation: fade-in 0.3s ease-out;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Tablet için responsive düzenlemeler */
@media (max-width: 768px) {
  .login-card {
    padding: 25px;
  }
  
  h1 {
    font-size: 1.8rem;
  }
  
  .login-logo .logo-image {
    height: 60px;
  }
  
  .login-logo h2 {
    font-size: 1.5rem;
  }
}

/* Mobil için responsive düzenlemeler */
@media (max-width: 480px) {
  .login-container {
    padding: 15px;
  }
  
  .login-card {
    padding: 20px;
  }
  
  h1 {
    font-size: 1.5rem;
    margin-bottom: 20px;
  }
  
  .tab-btn {
    padding: 10px 5px;
    font-size: 0.9rem;
  }
  
  .form-actions {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .login-logo .logo-image {
    height: 50px;
  }
  
  .login-logo h2 {
    font-size: 1.3rem;
  }
  
  .login-logo p {
    font-size: 0.9rem;
  }

  .login-btn,
  .edevlet-btn {
    padding: 12px;
  }
}
</style>
