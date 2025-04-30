<template>
  <div class="candidate-layout">
    <header class="header">
      <div class="logo">
        <router-link to="/candidate/dashboard">
          <img src="../assets/koü-logo.png" alt="KOÜ Logo" class="logo-image" />
          <span class="logo-text">KOÜ Akademik Başvuru Sistemi</span>
        </router-link>
      </div>
      <div class="user-menu">
        <div class="user-info">
          <span class="user-name">{{ userName }}</span>
          <span class="user-role">{{ userRoleText }}</span>
        </div>
        <div class="dropdown-menu">
          <!-- Removed Profile Link -->
          <button @click="logout" class="logout-btn">
            <span class="dropdown-icon">🚪</span>
            Çıkış Yap
          </button>
        </div>
      </div>
    </header>
    
    <div class="layout-container">
      <button @click="toggleSidebar" class="mobile-menu-toggle">
        <span class="menu-icon-bar"></span>
        <span class="menu-icon-bar"></span>
        <span class="menu-icon-bar"></span>
      </button>
      
      <nav class="sidebar" :class="{ 'sidebar-open': sidebarOpen }">
        <ul class="menu">
          <li class="menu-item">
            <router-link to="/candidate/dashboard" class="menu-link" @click="closeSidebarOnMobile">
              <i class="menu-icon">📊</i>
              <span class="menu-text">Gösterge Paneli</span>
            </router-link>
          </li>
          <li class="menu-item">
            <router-link to="/candidate/announcements" class="menu-link" @click="closeSidebarOnMobile">
              <i class="menu-icon">📢</i>
              <span class="menu-text">Aktif İlanlar</span>
            </router-link>
          </li>
          <li class="menu-item">
            <router-link to="/candidate/applications" class="menu-link" @click="closeSidebarOnMobile">
              <i class="menu-icon">📝</i>
              <span class="menu-text">Başvurularım</span>
            </router-link>
          </li>
          <!-- Removed "Yeni Başvuru" link from sidebar -->
          <li class="menu-item">
            <router-link to="/candidate/documents" class="menu-link" @click="closeSidebarOnMobile">
              <i class="menu-icon">📄</i>
              <span class="menu-text">Belgelerim</span>
            </router-link>
          </li>
        </ul>
      </nav>
      
      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

export default {
  name: 'CandidateLayout',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    const sidebarOpen = ref(false)
    
    const userName = computed(() => {
      if (authStore.user) {
        if (authStore.user.first_name || authStore.user.last_name) {
          return `${authStore.user.first_name || ''} ${authStore.user.last_name || ''}`.trim()
        }
        return authStore.user.username || 'Aday Kullanıcı'
      }
      return 'Aday Kullanıcı'
    })
    
    const userRoleText = computed(() => {
      return 'Aday'
    })
    
    onMounted(() => {
      if (authStore.isAuthenticated && !authStore.user) {
        authStore.fetchUser()
      }
    })
    
    const logout = async () => {
      try {
        await authStore.logout()
        router.push('/login')
      } catch (error) {
        console.error('Çıkış yapılırken hata oluştu:', error)
        router.push('/login')
      }
    }
    
    const toggleSidebar = () => {
      sidebarOpen.value = !sidebarOpen.value
    }
    
    const closeSidebarOnMobile = () => {
      if (window.innerWidth <= 768) {
        sidebarOpen.value = false
      }
    }
    
    return {
      userName,
      userRoleText,
      logout,
      sidebarOpen,
      toggleSidebar,
      closeSidebarOnMobile
    }
  }
}
</script>

<style scoped>
.candidate-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--light-color);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 70px;
  background-color: var(--primary-color);
  color: white;
  box-shadow: var(--shadow-md);
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo a {
  display: flex;
  align-items: center;
  color: white;
  text-decoration: none;
}

.logo-image {
  height: 45px;
  margin-right: 12px;
  border-radius: 4px;
  background-color: white;
  padding: 2px;
}

.logo-text {
  font-size: 1.3rem;
  font-weight: bold;
  letter-spacing: 0.5px;
}

.user-menu {
  position: relative;
  display: flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: var(--border-radius-sm);
  transition: background-color 0.2s;
}

.user-menu:hover {
  background-color: var(--dark-color);
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  margin-right: 10px;
}

.user-name {
  font-weight: bold;
  font-size: 0.95rem;
  letter-spacing: 0.3px;
}

.user-role {
  font-size: 0.8rem;
  opacity: 0.9;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  min-width: 180px;
  background-color: white;
  border-radius: var(--border-radius-sm);
  box-shadow: var(--shadow-lg);
  padding: 8px 0;
  /* margin-top: 8px; */ /* Kaldırıldı - Fare geçiş sorununu çözmek için */
  display: none;
  z-index: 1000;
  border: 1px solid var(--border-color);
}

.user-menu:hover .dropdown-menu {
  display: block;
}

.dropdown-item,
.logout-btn {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 10px 16px;
  color: var(--dark-color);
  text-decoration: none;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 0.95rem;
  transition: all 0.2s;
}

.dropdown-item:hover,
.logout-btn:hover {
  background-color: var(--border-color);
  color: var(--primary-color);
}

.dropdown-icon {
  margin-right: 8px;
  font-size: 1.1rem;
}

.layout-container {
  display: flex;
  flex: 1;
  position: relative;
  background-color: var(--light-color);
}

.mobile-menu-toggle {
  display: none;
  position: fixed;
  top: 80px;
  left: 15px;
  z-index: 100;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background-color: var(--primary-color);
  border: none;
  box-shadow: var(--shadow-md);
  justify-content: center;
  align-items: center;
  flex-direction: column;
  padding: 10px;
}

.menu-icon-bar {
  display: block;
  width: 24px;
  height: 2px;
  background-color: white;
  margin-bottom: 5px;
  border-radius: 2px;
  transition: transform 0.3s;
}

.menu-icon-bar:last-child {
  margin-bottom: 0;
}

.sidebar {
  width: 260px;
  background-color: white;
  box-shadow: var(--shadow-sm);
  padding: 24px 0;
  transition: all 0.3s ease;
  z-index: 90;
  border-right: 1px solid var(--border-color);
  height: calc(100vh - 70px);
  position: sticky;
  top: 70px;
  overflow-y: auto;
}

.menu {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.menu-item {
  margin: 4px 12px;
}

.menu-link {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  color: var(--dark-color);
  text-decoration: none;
  border-radius: var(--border-radius-sm);
  transition: all 0.2s;
  font-weight: 500;
}

.menu-link:hover {
  background-color: var(--border-color);
  color: var(--primary-color);
  transform: translateX(4px);
}

.menu-link.router-link-active {
  background-color: var(--border-color);
  color: var(--primary-color);
  font-weight: 600;
  border-right: 3px solid var(--primary-color);
  transform: translateX(4px);
}

.menu-icon {
  margin-right: 12px;
  font-size: 1.2rem;
  min-width: 24px;
  text-align: center;
}

.content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  background-color: var(--light-color);
  min-height: calc(100vh - 70px);
}

@media (max-width: 768px) {
  .header {
    padding: 0 16px;
    height: 60px;
  }
  
  .logo-text {
    font-size: 1.1rem;
  }
  
  .logo-image {
    height: 35px;
  }
  
  .mobile-menu-toggle {
    display: flex;
    top: 70px;
  }
  
  .sidebar {
    position: fixed;
    left: 0;
    top: 60px;
    height: calc(100vh - 60px);
    transform: translateX(-100%);
    width: 280px;
  }
  
  .sidebar-open {
    transform: translateX(0);
  }
  
  .content {
    padding: 20px 16px;
    margin-top: 0;
  }
  
  .user-name {
    font-size: 0.9rem;
  }
  
  .user-role {
    font-size: 0.75rem;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .sidebar {
    width: 240px;
  }
  
  .content {
    padding: 20px;
  }
  
  .menu-item {
    margin: 4px 8px;
  }
  
  .menu-link {
    padding: 10px 14px;
  }
}

/* Karanlık tema desteği için */
@media (prefers-color-scheme: dark) {
  .candidate-layout {
    background-color: var(--dark-color);
    color: var(--light-color);
  }
  
  .sidebar {
    background-color: rgba(255, 255, 255, 0.05);
    border-right-color: rgba(255, 255, 255, 0.1);
  }
  
  .menu-link {
    color: var(--light-color);
  }
  
  .menu-link:hover,
  .menu-link.router-link-active {
    background-color: rgba(255, 255, 255, 0.1);
    color: var(--light-color);
  }
  
  .content {
    background-color: var(--dark-color);
  }
  
  .dropdown-menu {
    background-color: var(--dark-color);
    border-color: rgba(255, 255, 255, 0.1);
  }
  
  .dropdown-item,
  .logout-btn {
    color: var(--light-color);
  }
  
  .dropdown-item:hover,
  .logout-btn:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
}
</style>
