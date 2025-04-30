<template>
  <div class="announcements-container">
    <div class="page-header">
      <h1>Aktif İlanlar</h1>
    </div>

    <div class="filter-section card">
      <div class="filter-grid">
        <div class="filter-group">
          <label for="search">Arama</label>
          <input 
            type="text" 
            id="search" 
            v-model="filters.search"
            placeholder="İlan başlığı veya içeriği ara..."
          >
        </div>

        <div class="filter-group">
          <label for="faculty">Fakülte</label>
          <select id="faculty" v-model="filters.faculty" @change="handleFacultyChange">
            <option value="">Tümü</option>
            <option v-for="faculty in faculties" 
                    :key="faculty.id" 
                    :value="faculty.id"
            >
              {{ faculty.name }}
            </option>
          </select>
        </div>

        <div class="filter-group">
          <label for="department">Bölüm</label>
          <select id="department" 
                  v-model="filters.department"
                  :disabled="!filters.faculty"
          >
            <option value="">Tümü</option>
            <option v-for="dept in filteredDepartments" 
                    :key="dept.id" 
                    :value="dept.id"
            >
              {{ dept.name }}
            </option>
          </select>
        </div>

        <div class="filter-group">
          <label for="position">Pozisyon</label>
          <select id="position" v-model="filters.position_type">
            <option value="">Tümü</option>
            <option value="dr">Dr. Öğretim Üyesi</option>
            <option value="doc">Doçent</option>
            <option value="prof">Profesör</option>
          </select>
        </div>
      </div>

      <div class="filter-actions">
        <button class="btn btn-outline" @click="resetFilters">
          Filtreleri Temizle
        </button>
      </div>
    </div>

    <div v-if="isLoading" class="loading-container">
      <div class="spinner"></div>
      <p>İlanlar yükleniyor...</p>
    </div>

    <div v-else-if="announcements.length === 0" class="empty-state card">
      <div class="empty-icon">📢</div>
      <h3>Aktif İlan Bulunamadı</h3>
      <p>Arama kriterlerinize uygun aktif ilan bulunmamaktadır.</p>
    </div>

    <div v-else class="announcements-grid">
      <div v-for="announcement in announcements" 
           :key="announcement.id" 
           class="announcement-card card"
      >
        <h3 class="announcement-title">{{ announcement.title }}</h3>

        <div class="announcement-details">
          <div class="detail-item">
            <span class="detail-icon">🏢</span>
            {{ announcement.department?.faculty?.name || 'Fakülte bilgisi yok' }}
          </div>
          <div class="detail-item">
            <span class="detail-icon">📍</span>
            {{ announcement.department?.name || 'Bölüm bilgisi yok' }}
          </div>
          <div class="detail-item">
            <span class="detail-icon">👨‍🏫</span>
            {{ getPositionText(announcement.position_type) }}
          </div>
          <div class="detail-item date">
            <span class="detail-icon">📅</span>
            Bitiş: {{ formatDate(announcement.end_date) }}
          </div>
        </div>

        <div class="announcement-footer">
          <button 
            class="btn btn-primary btn-sm" 
            @click="applyToAnnouncement(announcement.id)"
            :disabled="hasApplied(announcement.id)" <!-- Butonu pasif yap -->
          >
            {{ hasApplied(announcement.id) ? 'Başvuruldu' : 'Başvur' }}
          </button>
          <router-link 
            :to="`/candidate/announcements/${announcement.id}`"
            class="btn btn-outline btn-sm"
          >
            Detayları Görüntüle
          </router-link>
        </div>
      </div>
    </div>

    <div v-if="hasNextPage" class="load-more">
      <button 
        class="btn btn-outline"
        @click="loadMore"
        :disabled="isLoadingMore"
      >
        <div v-if="isLoadingMore" class="spinner"></div>
        <span v-if="isLoadingMore">Yükleniyor...</span>
        <span v-else>Daha Fazla Göster</span>
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../../api/axios'

export default {
  name: 'CandidateAnnouncements',
  setup() {
    const router = useRouter()
    const isLoading = ref(false)
    const isLoadingMore = ref(false)
    const announcements = ref([])
    const faculties = ref([])
    const departments = ref([])
    const myApplicationIds = ref(new Set()) // Başvurulan ilan ID'lerini tutmak için Set
    const page = ref(1)
    const hasNextPage = ref(false)

    const filters = ref({
      search: '',
      faculty: '',
      department: '',
      position_type: '',
      status: 'AKTIF' // Backend modeline uygun büyük harf
    })

    const filteredDepartments = computed(() => {
      if (!filters.value.faculty) return departments.value
      return departments.value.filter(dept => dept.faculty === filters.value.faculty)
    })

    // İlk yükleme
    onMounted(async () => {
      isLoading.value = true; // Set loading true initially
      await Promise.all([
        loadFaculties(),
        loadDepartments(),
        loadMyApplications(), // Önce başvuruları yükle
        loadAnnouncements() // Sonra ilanları yükle
      ]);
      isLoading.value = false; // Set loading false after all loads
    })

    // Filtre değişikliklerini izle
    watch(filters, () => {
      page.value = 1
      announcements.value = []
      loadAnnouncements()
    }, { deep: true })

    const loadFaculties = async () => {
      try {
        const response = await apiClient.get('/api/announcements/faculties/')
        faculties.value = response.data
      } catch (error) {
        console.error('Fakülteler yüklenirken hata:', error)
      }
    }

    const loadDepartments = async () => {
      try {
        const response = await apiClient.get('/api/announcements/departments/')
        departments.value = response.data
      } catch (error) {
        console.error('Bölümler yüklenirken hata:', error)
      }
    }

    // Adayın başvurduğu ilanların ID'lerini yükle
    const loadMyApplications = async () => {
       try {
         // Tüm başvuruları çekmek için limit olmadan istek yapabiliriz
         // veya backend'den sadece ilan ID'lerini döndüren bir endpoint isteyebiliriz.
         // Şimdilik tüm başvuruları çekip ID'leri alalım.
         const response = await apiClient.get('/api/applications/my/', { params: { page_size: 1000 } }); // Yüksek bir limit
         myApplicationIds.value = new Set(response.data.results.map(app => app.announcement.id));
       } catch (error) {
         console.error('Başvurular yüklenirken hata:', error);
       }
    }

    const loadAnnouncements = async () => {
      // Prevent concurrent loads when loading more
      if (isLoadingMore.value) return; 
      if (page.value === 1 && !isLoading.value) isLoading.value = true; // Only set main loading for first page if not already loading

      try {
        const params = {
          page: page.value,
          ...filters.value
        }
        // Ensure status is always sent correctly
        if (!params.status) params.status = 'AKTIF'; 

        const response = await apiClient.get('/api/announcements/', { params })
        
        if (page.value === 1) {
          announcements.value = response.data.results
        } else {
          announcements.value = [...announcements.value, ...response.data.results]
        }

        hasNextPage.value = !!response.data.next
      } catch (error) {
        console.error('İlanlar yüklenirken hata:', error)
      } finally {
         if (page.value === 1) isLoading.value = false;
      }
    }

    const loadMore = async () => {
      if (isLoadingMore.value || !hasNextPage.value) return

      page.value++
      isLoadingMore.value = true
      try {
        await loadAnnouncements()
      } finally {
        isLoadingMore.value = false
      }
    }

    const handleFacultyChange = () => {
      filters.value.department = ''
    }

    const resetFilters = () => {
      filters.value = {
        search: '',
        faculty: '',
        department: '',
        position_type: '',
        status: 'AKTIF' // Resetlerken de backend'e uygun kalsın
      }
    }

    const getPositionText = (positionType) => {
      const positions = {
        'dr': 'Dr. Öğretim Üyesi',
        'doc': 'Doçent',
        'prof': 'Profesör'
      }
      return positions[positionType] || positionType
    }

    const formatDate = (dateString) => {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleDateString('tr-TR')
    }

    const applyToAnnouncement = (id) => {
       if (hasApplied(id)) return; // Zaten başvurulmuşsa bir şey yapma
      router.push({ path: '/candidate/applications/new', query: { announcementId: id } })
    }

    // İlana başvurulup başvurulmadığını kontrol et
    const hasApplied = (announcementId) => {
      return myApplicationIds.value.has(announcementId);
    }

    return {
      isLoading,
      isLoadingMore,
      announcements,
      faculties,
      filters,
      filteredDepartments,
      hasNextPage,
      getPositionText,
      formatDate,
      loadMore,
      handleFacultyChange,
      resetFilters,
      applyToAnnouncement,
      hasApplied // Template'de kullanmak için return et
    }
  }
}
</script>

<style scoped>
.announcements-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
}

.page-header {
  margin-bottom: 24px;
}

h1 {
  font-size: 1.8rem;
  color: var(--primary-color);
  margin: 0;
}

.filter-section {
  background: white;
  border-radius: var(--border-radius-lg);
  padding: 24px;
  margin-bottom: 24px;
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group label {
  font-weight: 500;
  color: var(--dark-color);
  font-size: 0.9rem;
}

.filter-group input,
.filter-group select {
  padding: 10px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.filter-group input:focus,
.filter-group select:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(29, 131, 72, 0.1);
  outline: none;
}

.filter-actions {
  display: flex;
  justify-content: flex-end;
}

.announcements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.announcement-card {
  background: white;
  border-radius: var(--border-radius-lg);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  transition: all 0.3s ease;
}

.announcement-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.announcement-title {
  font-size: 1.1rem;
  color: var(--dark-color);
  margin: 0;
  line-height: 1.4;
}

.announcement-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  color: var(--gray-color);
}

.detail-icon {
  font-size: 1.1rem;
}

.announcement-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
  padding-top: 16px;
  border-top: 1px solid var(--border-color);
}

.btn {
  padding: 10px 16px;
  border-radius: var(--border-radius-sm);
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.btn-sm {
  padding: 8px 12px;
  font-size: 0.9rem;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
  border: none;
}

.btn-primary:hover:not(:disabled) {
  background: var(--dark-color);
}

.btn-primary:disabled {
  background-color: var(--gray-color);
  cursor: not-allowed;
}


.btn-outline {
  background: none;
  border: 1px solid var(--primary-color);
  color: var(--primary-color);
}

.btn-outline:hover {
  background: var(--border-color);
}

.empty-state {
  text-align: center;
  padding: 48px 24px;
  background: white;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.empty-state h3 {
  margin: 0;
  margin-bottom: 8px;
  color: var(--dark-color);
}

.empty-state p {
  color: var(--gray-color);
  margin-bottom: 24px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 0;
  gap: 16px;
  color: var(--gray-color);
}

.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.load-more {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .announcements-container {
    padding: 16px;
  }

  .filter-section {
    padding: 16px;
  }

  .filter-grid {
    grid-template-columns: 1fr;
  }

  .announcements-grid {
    grid-template-columns: 1fr;
  }
}
</style>
