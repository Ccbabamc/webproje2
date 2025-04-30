<template>
  <div class="unauthorized-container">
    <div class="error-card">
      <div class="error-icon">🔒</div>
      <h1>Yetkisiz Erişim</h1>
      <p>Bu sayfaya erişim yetkiniz bulunmamaktadır.</p>
      <div class="actions">
        <button @click="goBack" class="btn-back">Geri Dön</button>
        <button @click="goHome" class="btn-home">Ana Sayfa</button>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'; // Import Pinia store

export default {
  name: 'UnauthorizedView',
  methods: {
    goBack() {
      this.$router.go(-1)
    },
    goHome() {
      const authStore = useAuthStore(); // Use Pinia store instance
      // Access role via getter, handle potential null user
      const role = authStore.userRole ? authStore.userRole.toUpperCase() : null; 
      
      // Use normalized roles for redirection logic
      const isAdmin = role === 'ADMIN' || role === 'SUPERADMIN';
      const isCandidate = role === 'CANDIDATE'; // Assuming CANDIDATE is the role name

      if (isAdmin) {
        this.$router.push('/admin/dashboard');
      } else if (isCandidate) {
        // Redirect candidates to their dashboard or a default page
        this.$router.push('/candidate/dashboard'); 
      } else {
        // Fallback for other roles or if role is null after failed auth
        this.$router.push('/'); 
      }
    }
  }
}
</script>

<style scoped>
.unauthorized-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f8f9fa;
  padding: 20px;
}

.error-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 40px;
  max-width: 500px;
  width: 100%;
  text-align: center;
}

.error-icon {
  font-size: 5rem;
  margin-bottom: 20px;
}

h1 {
  color: #dc3545;
  margin-bottom: 15px;
  font-size: 2rem;
}

p {
  color: #666;
  margin-bottom: 30px;
  font-size: 1.1rem;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.btn-back, .btn-home {
  padding: 10px 20px;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.btn-back {
  background-color: #6c757d;
  color: white;
}

.btn-home {
  background-color: #0056b3;
  color: white;
}

.btn-back:hover {
  background-color: #5a6268;
}

.btn-home:hover {
  background-color: #004494;
}
</style>
