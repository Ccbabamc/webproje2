import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    redirect: to => {
      const authStore = useAuthStore()
      if (authStore.isAuthenticated) {
        // Use isAdmin getter for role check
        return authStore.isAdmin ? '/admin/dashboard' : '/candidate/dashboard' 
      }
      return '/login'
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { 
      guestOnly: true,
      title: 'Giriş Yap'
    }
  },
  {
    path: '/admin',
    name: 'AdminLayout',
    component: () => import('../layouts/AdminLayout.vue'),
    meta: { 
      requiresAuth: true,
      role: 'ADMIN', // Use uppercase to match backend/store
      title: 'Yönetici Paneli'
    },
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('../views/admin/Dashboard.vue'),
        meta: {
          title: 'Gösterge Paneli'
        }
      },
      {
        path: 'announcements',
        name: 'AdminAnnouncements',
        component: () => import('../views/admin/Announcements.vue'),
        meta: {
          title: 'İlan Yönetimi'
        }
      },
      {
        path: 'announcements/create',
        name: 'AdminAnnouncementCreate',
        component: () => import('../views/admin/AnnouncementForm.vue'),
        meta: {
          title: 'Yeni İlan Oluştur'
        }
      },
      {
        path: 'announcements/edit/:id',
        name: 'AdminAnnouncementEdit',
        component: () => import('../views/admin/AnnouncementForm.vue'),
        props: true,
        meta: {
          title: 'İlan Düzenle'
        }
      },
      {
        path: 'announcements/:id',
        name: 'AdminAnnouncementDetail',
        component: () => import('../views/admin/AnnouncementDetail.vue'),
        props: true,
        meta: {
          title: 'İlan Detayı'
        }
      },
      {
        path: 'users',
        name: 'AdminUserManagement',
        component: () => import('../views/admin/UserManagement.vue'),
        meta: {
          title: 'Kullanıcı Yönetimi',
          role: 'SUPERADMIN' // Only Super Admins can access
        }
      },
      {
        path: 'applications',
        name: 'AdminApplications',
        component: () => import('../views/admin/ApplicationReviews.vue'),
        meta: {
          title: 'Başvuru İncelemeleri'
        }
      },
      {
        path: 'applications/:id',
        name: 'AdminApplicationDetail',
        component: () => import('../views/admin/ApplicationDetail.vue'),
        props: true,
        meta: {
          title: 'Başvuru Detayı'
        }
      }
      // Add other admin routes here
    ]
  },
  {
    path: '/candidate',
    name: 'CandidateLayout',
    component: () => import('../layouts/CandidateLayout.vue'),
    meta: { 
      requiresAuth: true,
      role: 'ADAY', // Match backend/store role name (uppercase)
      title: 'Aday Paneli'
    },
    children: [
      {
        path: 'dashboard',
        name: 'CandidateDashboard',
        // Ensure correct path to component
        component: () => import('../views/candidate/Dashboard.vue'), 
        meta: {
          title: 'Gösterge Paneli'
        }
      },
      {
        path: 'applications',
        name: 'CandidateApplications',
         // Ensure correct path to component
        component: () => import('../views/candidate/Applications.vue'),
        meta: {
          title: 'Başvurularım'
        }
      },
      // Removed route for creating new application directly
      {
        path: 'applications/edit/:id',
        name: 'CandidateApplicationEdit',
         // Ensure correct path to component
        component: () => import('../views/candidate/ApplicationForm.vue'),
        props: true,
        meta: {
          title: 'Başvuru Düzenle'
        }
      },
      {
        path: 'applications/:id',
        name: 'CandidateApplicationDetail',
         // Ensure correct path to component
        component: () => import('../views/candidate/ApplicationDetail.vue'),
        props: true,
        meta: {
          title: 'Başvuru Detayı'
        }
      },
      {
        path: 'announcements',
        name: 'CandidateAnnouncements',
        component: () => import('../views/candidate/Announcements.vue'),
        meta: {
          title: 'Aktif İlanlar'
        }
      },
      {
        path: 'announcements/:id',
        name: 'CandidateAnnouncementDetail',
        component: () => import('../views/candidate/AnnouncementDetail.vue'),
        props: true,
        meta: {
          title: 'İlan Detayı'
        }
      },
      // Removed profile route
      { 
        path: 'documents',
        name: 'CandidateDocuments',
        component: () => import('../views/candidate/Documents.vue'),
        meta: {
          title: 'Belgelerim'
        }
      }
    ]
  },
  {
    path: '/unauthorized',
    name: 'Unauthorized',
    component: () => import('../views/Unauthorized.vue'),
    meta: {
      title: 'Yetkisiz Erişim'
    }
  },
  {
    path: '/:catchAll(.*)',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
    meta: {
      title: 'Sayfa Bulunamadı'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    return { top: 0 }
  }
})

// Sayfa başlığını güncelle
const updateTitle = (to) => {
  const baseTitle = 'KOÜ Akademik Başvuru Sistemi'
  const pageTitle = to.meta.title
  document.title = pageTitle ? `${pageTitle} - ${baseTitle}` : baseTitle
}

// Global navigation guard
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  try {
    // Store başlatılmamışsa başlat
    if (!authStore.initialized) {
      await authStore.initialize()
    }
    
    const isAuthenticated = authStore.isAuthenticated
    // Get role directly from getter, already handles uppercase and defaults
    const userRole = authStore.userRole 
    const requiredRole = to.meta.role // Get required role (should be uppercase now)
    
    // Debug bilgileri
    console.log('Route:', to.fullPath)
    console.log('Auth Status:', isAuthenticated ? 'Authenticated' : 'Not Authenticated')
    console.log('User Role:', userRole)
    console.log('Required Role:', requiredRole)
    
    // Misafir sayfaları kontrolü (login gibi)
    if (to.meta.guestOnly && isAuthenticated) {
      console.log('Authenticated user trying to access guest page, redirecting...')
      // Use isAdmin getter for redirection logic
      return next(authStore.isAdmin ? '/admin/dashboard' : '/candidate/dashboard') 
    }
    
    // Yetkilendirme kontrolü
    if (to.meta.requiresAuth) {
      if (!isAuthenticated) {
        console.log('Authentication required, redirecting to login...')
        return next({ path: '/login', query: { redirect: to.fullPath }})
      }
      
      // Rol kontrolü
      if (requiredRole) {
        // Corrected logic: Compare directly with userRole from store
        // SUPERADMIN should be able to access ADMIN routes too
        if (userRole !== requiredRole) { 
          // Special case: If required role is ADMIN, also allow SUPERADMIN
          if (!(requiredRole === 'ADMIN' && userRole === 'SUPERADMIN')) {
             console.log(`Role mismatch: User role '${userRole}' does not match required role '${requiredRole}'. Redirecting to unauthorized...`)
             return next('/unauthorized')
          }
        }
      }
    }
    
    // Sayfa başlığını güncelle
    updateTitle(to)
    
    // Her şey yolunda, devam et
    console.log('Access granted.');
    return next()
  } catch (error) {
    console.error('Navigation guard error:', error)
    // Hata durumunda oturumu kapat ve login sayfasına yönlendir
    if (authStore.isAuthenticated) { // Avoid logging out if already logged out
        authStore.logout()
    }
    return next('/login')
  }
})

export default router
