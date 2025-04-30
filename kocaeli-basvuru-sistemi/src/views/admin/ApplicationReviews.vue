<template>
  <div class="application-reviews-container">
    <div class="page-header">
      <div class="header-left">
        <h1>Başvuru İncelemeleri</h1>
        <div class="review-stats">
          <div class="stat-item">
            <span class="stat-label">Toplam Başvuru:</span>
            <span class="stat-value">{{ totalApplications }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Bekleyen:</span>
            <span class="stat-value pending">{{ pendingApplications }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">İncelenen:</span>
            <span class="stat-value reviewed">{{ reviewedApplications }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="filter-section card">
      <div class="filter-grid">
        <div class="filter-group">
          <label for="search">Arama</label>
          <input 
            type="text" 
            id="search" 
            v-model="filters.search"
            placeholder="TC Kimlik No veya Ad Soyad..."
          >
        </div>

        <div class="filter-group">
          <label for="announcement">İlan</label>
          <select id="announcement" v-model="filters.announcement">
            <option value="">Tümü</option>
            <option v-for="announcement in announcements" 
                    :key="announcement.id" 
                    :value="announcement.id"
            >
              <!-- Use optional chaining for safety -->
              {{ announcement?.title || 'İlan bilgisi yok' }} 
            </option>
          </select>
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
          <label for="status">Durum</label>
          <select id="status" v-model="filters.status">
            <option value="">Tümü</option>
             <!-- Use backend status values -->
            <option value="TASLAK">Taslak</option>
            <option value="GONDERILDI">Gönderildi</option>
            <option value="DEGERLENDIRILDI">Değerlendirildi</option>
            <option value="KABUL_EDILDI">Kabul Edildi</option>
            <option value="RED_EDILDI">Red Edildi</option>
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
      <p>Başvurular yükleniyor...</p>
    </div>

    <div v-else-if="applications.length === 0" class="empty-state card">
      <div class="empty-icon">📝</div>
      <h3>Başvuru Bulunamadı</h3>
      <p>Arama kriterlerinize uygun başvuru bulunmamaktadır.</p>
    </div>

    <div v-else class="table-container card">
      <table>
        <thead>
          <tr>
            <th>Başvuru No</th>
            <th>Aday</th>
            <th>TC Kimlik</th>
            <th>İlan</th>
            <th>Başvuru Tarihi</th>
            <th>Durum</th>
            <th>İşlemler</th>
          </tr>
        </thead>
        <tbody>
          <!-- Use optional chaining (?.) for safe access -->
          <tr v-for="application in applications" :key="application.id">
            <td>#{{ application.id }}</td>
            <td class="candidate-cell">
              {{ application.candidate?.full_name || 
                 `${application.candidate?.first_name || ''} ${application.candidate?.last_name || ''}`.trim() || 
                 'Aday Bilgisi Yok' }}
            </td>
            <td>{{ maskTCKN(application.candidate?.tcno) }}</td>
            <td class="announcement-cell">
              {{ application.announcement?.title || 'İlan Bilgisi Yok' }}
            </td>
            <td>{{ formatDate(application.created_at) }}</td>
            <td>
              <!-- Use backend status values for class and text -->
              <span class="status-badge" :class="getStatusClass(application.status)">
                {{ getStatusText(application.status) }}
              </span>
            </td>
            <td>
              <button 
                class="btn btn-sm btn-outline"
                @click="viewApplication(application.id)"
              >
                İncele
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
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../../api/axios'

export default {
  name: 'ApplicationReviews',
  setup() {
    const router = useRouter()
    const isLoading = ref(false)
    const isLoadingMore = ref(false)
    const applications = ref([])
    const announcements = ref([])
    const faculties = ref([])
    const departments = ref([])
    const page = ref(1)
    const hasNextPage = ref(false)
    const totalApplicationsCount = ref(0); // To store total count from API

    const filters = ref({
      search: '',
      announcement: '',
      faculty: '',
      department: '',
      status: '' // Default to empty, backend should handle default filtering if needed
    })

    // Computed properties for stats based on the fetched applications array
    const totalApplications = computed(() => totalApplicationsCount.value); // Use count from API
    const pendingApplications = computed(() => 
      applications.value.filter(a => a.status === 'GONDERILDI' || a.status === 'DEGERLENDIRILDI').length // Use backend values
    )
    const reviewedApplications = computed(() => 
      applications.value.filter(a => a.status === 'KABUL_EDILDI' || a.status === 'RED_EDILDI').length // Use backend values
    )

    const filteredDepartments = computed(() => {
      if (!filters.value.faculty) return departments.value
      // Ensure dept.faculty exists before comparison
      return departments.value.filter(dept => dept.faculty && dept.faculty === filters.value.faculty) 
    })

    // İlk yükleme
    onMounted(async () => {
      await Promise.all([
        loadAnnouncements(),
        loadFaculties(),
        loadDepartments(),
        loadApplications() // Load initial applications
      ])
    })

    // Filtre değişikliklerini izle
    watch(filters, () => {
      page.value = 1 // Reset page on filter change
      applications.value = [] // Clear current applications
      loadApplications()
    }, { deep: true })

    const loadAnnouncements = async () => {
      try {
        // Fetch all announcements for the filter dropdown
        const response = await apiClient.get('/api/announcements/', { params: { page_size: 1000 } }) 
        announcements.value = response.data.results || response.data; // Handle potential direct array response
      } catch (error) {
        console.error('İlanlar yüklenirken hata:', error)
      }
    }

    const loadFaculties = async () => {
      try {
        const response = await apiClient.get('/api/announcements/faculties/') // Assuming this endpoint exists
        faculties.value = response.data
      } catch (error) {
        console.error('Fakülteler yüklenirken hata:', error)
      }
    }

    const loadDepartments = async () => {
      try {
        const response = await apiClient.get('/api/announcements/departments/') // Assuming this endpoint exists
        departments.value = response.data
      } catch (error) {
        console.error('Bölümler yüklenirken hata:', error)
      }
    }

    const loadApplications = async () => {
      if (isLoadingMore.value) return; // Prevent concurrent loads when loading more
      if (page.value === 1) isLoading.value = true;

      try {
        const params = {
          page: page.value,
          // Send only non-empty filters
          ...(filters.value.search && { search: filters.value.search }),
          ...(filters.value.announcement && { ilan: filters.value.announcement }), // Use 'ilan' if that's the backend filter name
          ...(filters.value.faculty && { ilan__bolum__fakulte: filters.value.faculty }), // Adjust filter name based on backend
          ...(filters.value.department && { ilan__bolum: filters.value.department }), // Adjust filter name based on backend
          ...(filters.value.status && { status: filters.value.status }),
        }

        // Use the correct endpoint for listing all applications (for admin/manager)
        const response = await apiClient.get('/api/applications/applications/', { params }) 
        
        if (page.value === 1) {
          applications.value = response.data.results || []
        } else {
          applications.value = [...applications.value, ...(response.data.results || [])]
        }
        totalApplicationsCount.value = response.data.count || 0; // Store total count
        hasNextPage.value = !!response.data.next
      } catch (error) {
        console.error('Başvurular yüklenirken hata:', error)
         applications.value = []; // Clear applications on error
         totalApplicationsCount.value = 0;
         hasNextPage.value = false;
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

    const handleFacultyChange = () => {
      filters.value.department = '' // Reset department when faculty changes
    }

    const resetFilters = () => {
      filters.value = {
        search: '',
        announcement: '',
        faculty: '',
        department: '',
        status: ''
      }
      // No need to manually trigger watch, changing filters ref will do it
    }

    const getStatusText = (status) => {
      // Use backend status values
      const statuses = {
        'TASLAK': 'Taslak',
        'GONDERILDI': 'Gönderildi',
        'DEGERLENDIRILDI': 'Değerlendirildi',
        'KABUL_EDILDI': 'Kabul Edildi',
        'RED_EDILDI': 'Red Edildi'
      }
      return statuses[status] || status || 'Bilinmiyor'
    }
    
    const getStatusClass = (status) => {
      // Use backend status values
      const statusClasses = {
        'TASLAK': 'draft', 
        'GONDERILDI': 'pending', 
        'DEGERLENDIRILDI': 'reviewing',
        'KABUL_EDILDI': 'approved',
        'RED_EDILDI': 'rejected'
      }
      return statusClasses[status] || ''
    }


    const formatDate = (dateString) => {
      if (!dateString) return '-'
      // Use created_at for application date
      return new Date(dateString).toLocaleDateString('tr-TR') 
    }

    const maskTCKN = (tcno) => {
      if (!tcno || tcno.length !== 11) return '***********'
      // Masking logic seems fine
      return tcno.substring(0, 2) + '*******' + tcno.substring(9, 11); 
    }

    const viewApplication = (id) => {
      router.push(`/admin/applications/${id}`)
    }

    return {
      isLoading,
      isLoadingMore,
      applications,
      announcements,
      faculties,
      filters,
      filteredDepartments,
      hasNextPage,
      totalApplications,
      pendingApplications,
      reviewedApplications,
      getStatusText,
      getStatusClass, // Add this
      formatDate,
      maskTCKN,
      loadMore,
      handleFacultyChange,
      resetFilters,
      viewApplication
    }
  }
}
</script>

<style scoped>
.application-reviews-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

h1 {
  font-size: 1.8rem;
  color: var(--primary-color);
  margin: 0;
}

.review-stats {
  display: flex;
  flex-wrap: wrap; /* Allow wrapping on smaller screens */
  gap: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stat-label {
  color: var(--gray-color);
  font-size: 0.9rem;
}

.stat-value {
  font-weight: 600;
  color: var(--dark-color);
}

.stat-value.pending { /* Corresponds to GONDERILDI/DEGERLENDIRILDI */
  color: #b45309; /* Amber/Orange */
}

.stat-value.reviewed { /* Corresponds to KABUL_EDILDI/RED_EDILDI */
  color: var(--primary-color); /* Or differentiate between approved/rejected */
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
  vertical-align: middle; /* Align cell content vertically */
}

.candidate-cell,
.announcement-cell {
  max-width: 200px;
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
  white-space: nowrap;
}

/* Updated status classes based on backend model */
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
  display: inline-flex; /* Changed */
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  text-decoration: none; /* Added */
}

.btn-sm {
  padding: 6px 12px;
  font-size: 0.9rem;
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
  .application-reviews-container {
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
