<template>
  <div class="not-found">
    <div class="content">
      <span class="icon">🚧</span>
      <h1>404 - Sayfa Bulunamadı</h1>
      <p>Aradığınız sayfa maalesef bulunamadı.</p>
      <p>Ana sayfaya dönebilir veya farklı bir sayfa aramayı deneyebilirsiniz.</p>
      <router-link to="/" class="home-button">Ana Sayfaya Dön</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound'
}
</script>

<style scoped>
.not-found {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
  text-align: center;
  padding: 20px;
}

.content {
  background-color: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.icon {
  font-size: 4rem;
  display: block;
  margin-bottom: 20px;
}

h1 {
  color: #0056b3;
  margin-bottom: 15px;
}

p {
  color: #666;
  margin-bottom: 10px;
}

.home-button {
  display: inline-block;
  margin-top: 20px;
  padding: 12px 25px;
  background-color: #0056b3;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: bold;
  transition: background-color 0.3s;
}

.home-button:hover {
  background-color: #003d82;
}
</style> 