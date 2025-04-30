import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice' // Bildirim servisi
import ConfirmationService from 'primevue/confirmationservice' // Onay dialogu servisi

// PrimeVue tema ve CSS (Güncellenmiş tema yolu)
import 'primevue/resources/themes/lara-light-indigo/theme.css'; // Doğru tema yolu
import 'primevue/resources/primevue.min.css';         // Core CSS
import 'primeicons/primeicons.css';                   // İkonlar

// Uygulamanın kendi CSS'i
import './style.css'

import App from './App.vue'
import router from './router'
import apiClient from './api/axios' // Axios interceptorları

const app = createApp(App)

// Pinia store
const pinia = createPinia()
app.use(pinia)

// Vue Router
app.use(router)

// PrimeVue
app.use(PrimeVue)
app.use(ToastService) // Toast servisini ekle
app.use(ConfirmationService) // Confirm servisini ekle

// Axios'u global olarak tanımla (opsiyonel, interceptor zaten çalışacak)
// app.config.globalProperties.$axios = apiClient

app.mount('#app')
