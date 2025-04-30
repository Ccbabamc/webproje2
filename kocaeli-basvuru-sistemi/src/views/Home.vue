<template>
  <div class="home">
    <header class="hero">
      <h1>Kocaeli Üniversitesi</h1>
      <h2>Akademik Personel Başvuru Sistemi</h2>
      <p class="description">Akademik personel alım başvuruları için online başvuru platformu</p>
      <div class="actions">
        <router-link to="/login" class="btn btn-primary">Giriş Yap</router-link>
      </div>
    </header>

    <section class="announcements">
      <h2>Güncel İlanlar</h2>
      <div class="announcement-list">
        <div class="announcement-card" v-for="(item, index) in announcements" :key="index">
          <h3>{{ item.title }}</h3>
          <div class="meta">
            <span class="department">{{ item.department }}</span>
            <span class="position">{{ item.position }}</span>
          </div>
          <div class="dates">
            <span class="date">Başlangıç: {{ item.startDate }}</span>
            <span class="date">Bitiş: {{ item.endDate }}</span>
          </div>
          <router-link :to="'/announcement/' + item.id" class="btn btn-sm">Detayları Gör</router-link>
        </div>
      </div>
    </section>

    <section class="info">
      <h2>Başvuru Adımları</h2>
      <div class="steps">
        <div class="step">
          <div class="step-number">1</div>
          <h3>Giriş Yap</h3>
          <p>Admin tarafından verilen TC ve şifre ile sisteme giriş yapın</p>
        </div>
        <div class="step">
          <div class="step-number">2</div>
          <h3>İlan Seç</h3>
          <p>İlgilendiğiniz akademik pozisyon ilanını seçin</p>
        </div>
        <div class="step">
          <div class="step-number">3</div>
          <h3>Başvuruyu Tamamla</h3>
          <p>Gerekli bilgileri doldurun ve belgeleri yükleyin</p>
        </div>
        <div class="step">
          <div class="step-number">4</div>
          <h3>Takip Et</h3>
          <p>Başvurunuzun durumunu sistem üzerinden takip edin</p>
        </div>
      </div>
    </section>

    <footer>
      <p>&copy; 2025 Kocaeli Üniversitesi - Tüm Hakları Saklıdır</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      announcements: [
        {
          id: 1,
          title: 'Bilgisayar Mühendisliği - Dr. Öğretim Üyesi',
          department: 'Bilgisayar Mühendisliği',
          position: 'Dr. Öğretim Üyesi',
          startDate: '15 Nisan 2025',
          endDate: '15 Mayıs 2025'
        },
        {
          id: 2,
          title: 'İktisat Fakültesi - Doçent',
          department: 'İktisat',
          position: 'Doçent',
          startDate: '10 Nisan 2025',
          endDate: '10 Mayıs 2025'
        },
        {
          id: 3,
          title: 'Tıp Fakültesi - Profesör',
          department: 'Tıp',
          position: 'Profesör',
          startDate: '20 Nisan 2025',
          endDate: '20 Mayıs 2025'
        }
      ]
    }
  }
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.hero {
  text-align: center;
  padding: 60px 0;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 40px;
}

.hero h1 {
  font-size: 2.5rem;
  color: #0056b3;
  margin-bottom: 10px;
}

.hero h2 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 20px;
}

.description {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 30px;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.btn {
  padding: 12px 24px;
  border-radius: 4px;
  font-weight: bold;
  text-decoration: none;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #0056b3;
  color: white;
}

.btn-primary:hover {
  background-color: #003d82;
}

.btn-outline {
  border: 2px solid #0056b3;
  color: #0056b3;
}

.btn-outline:hover {
  background-color: #0056b3;
  color: white;
}

.btn-sm {
  padding: 8px 16px;
  font-size: 0.9rem;
}

.announcements, .info {
  margin-bottom: 50px;
}

h2 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.announcement-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.announcement-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.announcement-card h3 {
  color: #0056b3;
  margin-bottom: 10px;
}

.meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 0.9rem;
}

.dates {
  margin-bottom: 15px;
  font-size: 0.9rem;
}

.date {
  display: block;
  margin-bottom: 5px;
  color: #666;
}

.steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 30px;
  margin-top: 30px;
}

.step {
  text-align: center;
  padding: 20px;
  border-radius: 8px;
  background-color: #f8f9fa;
}

.step-number {
  width: 40px;
  height: 40px;
  background-color: #0056b3;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  font-weight: bold;
}

footer {
  text-align: center;
  padding: 20px 0;
  border-top: 1px solid #eee;
  color: #666;
}
</style> 