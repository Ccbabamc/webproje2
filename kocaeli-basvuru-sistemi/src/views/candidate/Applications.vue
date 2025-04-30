<template>
  <div class="applications-container">
    <div class="page-header">
      <h1>Başvurularım</h1>
      <!-- Removed "Yeni Başvuru Yap" button -->
    </div>

    <div class="filter-section card">
      <div class="filter-grid">
        <div class="filter-group">
          <label for="search">Arama</label>
          <input 
            type="text" 
            id="search" 
            v-model="filters.search"
            placeholder="İlan başlığı ara..."
          >
        </div>

        <div class="filter-group">
          <label for="status">Durum</label>
          <select id="status" v-model="filters.status">
            <option value="">Tümü</option>
            <!-- Backend modelindeki değerleri kullan -->
            <option value="TASLAK">Taslak</option>
            <option value="GONDERILDI">Gönderildi</option>
            <option value="DEGERLENDIRILDI">Değerlendirildi</option>
            <option value="KABUL_EDILDI">Kabul Edildi</option>
            <option value="RED_EDILDI">Red Edildi</option>
          </select>
        </div>

        <div class="filter-group">
          <label for="sort">Sıralama</label>
          <select id="sort" v-model="filters.ordering">
            <option value="-created_at">En Yeni</option>
            <option value="created_at">En Eski</option>
            <option value="announcement__title">İlan Adı (A-Z)</option>
            <option value="-announcement__title">İlan Adı (Z-A)</option>
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
      <p>Başvurularınız yükleniyor...</p>
    </div>

    <div v-else-if="applications.length === 0" class="empty-state card">
      <div class="empty-icon">📮</div>
      <h3>Başvuru Bulunamadı</h3>
      <p>Henüz herhangi bir ilana başvuru yapmadınız.</p>
      <button class="btn btn-primary" @click="goToAnnouncements">
        Aktif İlanları Görüntüle
      </button>
    </div>

    <div v-else class="table-container card">
      <table>
        <thead>
          <tr>
            <th>Başvuru No</th>
            <th>İlan</th>
            <th>Başvuru Tarihi</th>
            <th>Durum</th>
            <th>İşlemler</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="application in applications" :key="application.id">
            <td>#{{ application.id }}</td>
            <td class="announcement-cell">
              {{ application.announcement.title }}
            </td>
            <td>{{ formatDate(application.created_at) }}</td>
            <td>
              <span class="status-badge" :class="getStatusClass(application.status)">
                {{ getStatusText(application.status) }}
              </span>
            </td>
            <td>
              <button 
                class="btn btn-sm btn-outline"
                @click="viewApplication(application.id)"
              >
                Detay
              </button>
              <button 
                v-if="canEditApplication(application.status)"
                class="btn btn-sm btn-outline edit"
                @click="editApplication(application.id)"
              >
                Düzenle
              </button>
            </td>
          </tr>
        </tbody>
      </table>

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
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../../api/axios'

export default {
  name: 'CandidateApplications',
  setup() {
    const router = useRouter()
    const isLoading = ref(false)
    const isLoadingMore = ref(false)
    const applications = ref([])
    const page = ref(1)
    const hasNextPage = ref(false)

    const filters = ref({
      search: '',
      status: '',
      ordering: '-created_at'
    })

    // İlk yükleme
    onMounted(async () => {
      await loadApplications()
    })

    // Filtre değişikliklerini izle
    watch(filters, () => {
      page.value = 1
      applications.value = []
      loadApplications()
    }, { deep: true })

    const loadApplications = async () => {
      // Prevent concurrent loads when loading more
      if (isLoadingMore.value) return; 
      if (page.value === 1) isLoading.value = true;

      try {
        const params = {
          page: page.value,
          // Send only non-empty filters
          ...(filters.value.search && { search: filters.value.search }),
          ...(filters.value.status && { status: filters.value.status }),
          ...(filters.value.ordering && { ordering: filters.value.ordering }),
        }

        const response = await apiClient.get('/api/applications/my/', { params })
        
        if (page.value === 1) {
          applications.value = response.data.results
        } else {
          applications.value = [...applications.value, ...response.data.results]
        }

        hasNextPage.value = !!response.data.next
      } catch (error) {
        console.error('Başvurular yüklenirken hata:', error)
      } finally {
         if (page.value === 1) isLoading.value = false;
      }
    }

    const loadMore = async () => {
      if (isLoadingMore.value || !hasNextPage.value) return

      page.value++
      isLoadingMore.value = true
      try {
        await loadApplications()
      } finally {
        isLoadingMore.value = false
      }
    }

    const resetFilters = () => {
      filters.value = {
        search: '',
        status: '',
        ordering: '-created_at'
      }
    }

    const getStatusClass = (status) => {
      // Backend modelindeki değerlere göre class ata
      const statusClasses = {
        'TASLAK': 'draft', // Taslak için bir class ekleyebiliriz
        'GONDERILDI': 'pending', // Gönderildi -> Beklemede gibi
        'DEGERLENDIRILDI': 'reviewing',
        'KABUL_EDILDI': 'approved',
        'RED_EDILDI': 'rejected'
      }
      return statusClasses[status] || ''
    }

    const getStatusText = (status) => {
      // Backend modelindeki değerlere göre metin döndür
      const statuses = {
        'TASLAK': 'Taslak',
        'GONDERILDI': 'Gönderildi',
        'DEGERLENDIRILDI': 'Değerlendirildi',
        'KABUL_EDILDI': 'Kabul Edildi',
        'RED_EDILDI': 'Red Edildi'
      }
      return statuses[status] || 'Bilinmiyor'
    }

    const formatDate = (dateString) => {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleDateString('tr-TR')
    }

    const canEditApplication = (status) => {
      // Sadece 'TASLAK' durumundaki başvurular düzenlenebilir
      return status === 'TASLAK' 
    }

    const viewApplication = (id) => {
      router.push(`/candidate/applications/${id}`)
    }

    const editApplication = (id) => {
      router.push(`/candidate/applications/edit/${id}`)
    }

    const goToNewApplication = () => {
      router.push('/candidate/applications/new')
    }

    const goToAnnouncements = () => {
      router.push('/candidate/announcements')
    }

    return {
      isLoading,
      isLoadingMore,
      applications,
      filters,
      hasNextPage,
      getStatusClass,
      getStatusText,
      formatDate,
      canEditApplication,
      loadMore,
      resetFilters,
      viewApplication,
      editApplication,
      goToNewApplication,
      goToAnnouncements
    }
  }
}
</script>

<style scoped>
.applications-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.table-container {
  background: white;
  border-radius: var(--border-radius-lg);
  padding: 24px;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

th {
  background: var(--border-color);
  padding: 12px 16px;
  text-align: left;
  font-weight: 500;
  color: var(--dark-color);
  white-space: nowrap;
}

th:first-child {
  border-top-left-radius: var(--border-radius-sm);
}

th:last-child {
  border-top-right-radius: var(--border-radius-sm);
}

td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-color);
  color: var(--dark-color);
}

.announcement-cell {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: var(--border-radius-sm);
  font-size: 0.85rem;
  font-weight: 500;
}

/* Updated status classes */
.status-badge.draft { /* TASLAK */
  background-color: #f3f4f6; 
  color: #4b5563;
}
.status-badge.pending { /* GONDERILDI */
  background-color: #fffbeb; 
  color: #b45309;
}
.status-badge.reviewing { /* DEGERLENDIRILDI */
  background-color: #eff6ff;
  color: #1d4ed8;
}
.status-badge.approved { /* KABUL_EDILDI */
  background-color: #e6f7ee;
  color: var(--primary-color);
}
.status-badge.rejected { /* RED_EDILDI */
  background-color: #fef2f2;
  color: #dc2626;
}

.btn {
  padding: 10px 16px;
  border-radius: var(--border-radius-sm);
  font-weight: 500;
  cursor: pointer;
  display: inline-flex; /* Changed from flex */
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  text-decoration: none; /* Added for router-link consistency */
}

.btn-sm {
  padding: 6px 12px;
  font-size: 0.9rem;
  margin-right: 8px;
}
.btn-sm:last-child {
  margin-right: 0;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
  border: none;
}

.btn-primary:hover {
  background: var(--dark-color);
}

.btn-outline {
  background: none;
  border: 1px solid var(--primary-color);
  color: var(--primary-color);
}

.btn-outline:hover {
  background: var(--border-color);
}

.btn-outline.edit {
  border-color: #6b7280;
  color: #6b7280;
}
.btn-outline.edit:hover {
  background: #f3f4f6;
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
  .applications-container {
    padding: 16px;
  }

  .page-header {
    flex-direction: column;
    gap: 16px;
  }

  .filter-section {
    padding: 16px;
  }

  .filter-grid {
    grid-template-columns: 1fr;
  }
}
</style>
