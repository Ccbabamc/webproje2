<template>
  <div class="announcement-detail-container">
    <div class="page-header">
      <div class="header-left">
        <button class="btn btn-outline" @click="$router.back()">
          <span class="btn-icon">←</span> Geri Dön
        </button>
        <h1>İlan Detayları</h1>
      </div>
      <div class="header-actions">
        <button class="btn btn-outline" @click="editAnnouncement">
          <span class="btn-icon">✎</span> Düzenle
        </button>
        <button 
          class="btn"
          :class="[announcement.status === 'active' ? 'btn-danger' : 'btn-success']"
          @click="toggleStatus"
          :disabled="isUpdatingStatus"
        >
          <div v-if="isUpdatingStatus" class="spinner"></div>
          <span v-else class="btn-icon">{{ announcement.status === 'active' ? '◉' : '○' }}</span>
          {{ announcement.status === 'active' ? 'Pasife Al' : 'Aktifleştir' }}
        </button>
      </div>
    </div>

    <div v-if="isLoading" class="loading-container">
      <div class="spinner"></div>
      <p>İlan detayları yükleniyor...</p>
    </div>

    <template v-else>
      <div class="announcement-info card">
        <div class="status-badge" :class="announcement.status">
          {{ announcement.status === 'active' ? 'Aktif' : 'Pasif' }}
        </div>

        <h2 class="announcement-title">{{ announcement.title }}</h2>

        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">Fakülte</span>
            <span class="info-value">
              {{ announcement.department?.faculty?.name || 'Belirtilmemiş' }}
            </span>
          </div>
          <div class="info-item">
            <span class="info-label">Bölüm</span>
            <span class="info-value">
              {{ announcement.department?.name || 'Belirtilmemiş' }}
            </span>
          </div>
          <div class="info-item">
            <span class="info-label">Pozisyon</span>
            <span class="info-value">
              {{ getPositionText(announcement.position_type) }}
            </span>
          </div>
          <div class="info-item">
            <span class="info-label">Başvuru Tarihleri</span>
            <span class="info-value">
              {{ formatDate(announcement.start_date) }} - {{ formatDate(announcement.end_date) }}
            </span>
          </div>
          <div class="info-item full-width">
            <span class="info-label">Açıklama</span>
            <p class="info-value description">{{ announcement.description }}</p>
          </div>
        </div>

        <div class="documents-section">
          <h3>Gerekli Belgeler</h3>
          <ul class="document-list" v-if="announcement.required_documents?.length">
            <li v-for="(doc, index) in announcement.required_documents" 
                :key="index" 
                class="document-item"
            >
              <span class="document-icon">📄</span>
              {{ doc }}
            </li>
          </ul>
          <p v-else class="empty-text">Belirtilen belge bulunmamaktadır.</p>
        </div>

        <div class="criteria-section">
          <h3>Değerlendirme Kriterleri</h3>
          <div class="criteria-list" v-if="announcement.criteria?.length">
            <div v-for="criterion in announcement.criteria" 
                 :key="criterion.id" 
                 class="criterion-item"
            >
              <div class="criterion-name">{{ criterion.name }}</div>
              <div class="criterion-scores">
                <span class="score">Min: {{ criterion.min_score }}</span>
                <span class="score">Max: {{ criterion.max_score }}</span>
              </div>
            </div>
          </div>
          <p v-else class="empty-text">Belirtilen kriter bulunmamaktadır.</p>
        </div>

        <div class="stats-section">
          <div class="stat-card">
            <span class="stat-value">{{ announcement.application_count || 0 }}</span>
            <span class="stat-label">Toplam Başvuru</span>
          </div>
          <div class="stat-card">
            <span class="stat-value">{{ announcement.view_count || 0 }}</span>
            <span class="stat-label">Görüntülenme</span>
          </div>
          <div class="stat-card">
            <span class="stat-value">{{ getPendingApplicationCount() }}</span>
            <span class="stat-label">Bekleyen Başvuru</span>
          </div>
        </div>
      </div>

      <div class="applications-section card">
        <div class="section-header">
          <h2>Başvurular</h2>
          <div class="header-filters">
            <div class="filter-group">
              <label for="status-filter">Durum</label>
              <select id="status-filter" v-model="applicationFilters.status">
                <option value="">Tümü</option>
                <option value="pending">Beklemede</option>
                <option value="reviewing">İncelemede</option>
                <option value="approved">Onaylandı</option>
                <option value="rejected">Reddedildi</option>
              </select>
            </div>
            <div class="filter-group">
              <label for="sort">Sıralama</label>
              <select id="sort" v-model="applicationFilters.sort">
                <option value="-created_at">En Yeni</option>
                <option value="created_at">En Eski</option>
                <option value="candidate__last_name">İsme Göre (A-Z)</option>
                <option value="-candidate__last_name">İsme Göre (Z-A)</option>
              </select>
            </div>
          </div>
        </div>

        <div v-if="isLoadingApplications" class="loading-container">
          <div class="spinner"></div>
          <p>Başvurular yükleniyor...</p>
        </div>

        <div v-else-if="applications.length === 0" class="empty-state">
          <div class="empty-icon">📮</div>
          <h3>Başvuru Bulunmadı</h3>
          <p>Bu ilana henüz başvuru yapılmamış.</p>
        </div>

        <div v-else class="applications-table">
          <table>
            <thead>
              <tr>
                <th>Başvuru No</th>
                <th>Aday</th>
                <th>TC Kimlik</th>
                <th>Başvuru Tarihi</th>
                <th>Durum</th>
                <th>İşlemler</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="application in applications" :key="application.id">
                <td>#{{ application.id }}</td>
                <td class="candidate-cell">
                  {{ application.candidate.full_name || 
                     `${application.candidate.first_name} ${application.candidate.last_name}` }}
                </td>
                <td>{{ maskTCKN(application.candidate.tcno) }}</td>
                <td>{{ formatDate(application.created_at) }}</td>
                <td>
                  <span class="status-badge" :class="application.status">
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

          <div v-if="hasMoreApplications" class="load-more">
            <button 
              class="btn btn-outline"
              @click="loadMoreApplications"
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
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import apiClient from '../../api/axios'

export default {
  name: 'AnnouncementDetail',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const isLoading = ref(false)
    const isLoadingApplications = ref(false)
    const isLoadingMore = ref(false)
    const isUpdatingStatus = ref(false)
    const announcement = ref({})
    const applications = ref([])
    const page = ref(1)
    const hasMoreApplications = ref(false)

    const applicationFilters = ref({
      status: '',
      sort: '-created_at'
    })

    onMounted(async () => {
      await Promise.all([
        loadAnnouncement(),
        loadApplications()
      ])
    })

    watch(applicationFilters, () => {
      page.value = 1
      applications.value = []
      loadApplications()
    }, { deep: true })

    const loadAnnouncement = async () => {
      isLoading.value = true
      try {
        const response = await apiClient.get(`/api/announcements/${route.params.id}/`)
        announcement.value = response.data
      } catch (error) {
        console.error('İlan detayları yüklenirken hata:', error)
      } finally {
        isLoading.value = false
      }
    }

    const loadApplications = async () => {
      if (isLoadingApplications.value) return

      isLoadingApplications.value = true
      try {
        const params = {
          announcement: route.params.id,
          page: page.value,
          ...applicationFilters.value
        }

        const response = await apiClient.get('/api/applications/applications/', { params })
        
        if (page.value === 1) {
          applications.value = response.data.results
        } else {
          applications.value = [...applications.value, ...response.data.results]
        }

        hasMoreApplications.value = !!response.data.next
      } catch (error) {
        console.error('Başvurular yüklenirken hata:', error)
      } finally {
        isLoadingApplications.value = false
      }
    }

    const loadMoreApplications = async () => {
      if (isLoadingMore.value) return

      page.value++
      isLoadingMore.value = true
      try {
        await loadApplications()
      } finally {
        isLoadingMore.value = false
      }
    }

    const toggleStatus = async () => {
      if (isUpdatingStatus.value) return

      isUpdatingStatus.value = true
      try {
        const newStatus = announcement.value.status === 'active' ? 'inactive' : 'active'
        await apiClient.put(`/api/announcements/${route.params.id}/`, {
          ...announcement.value,
          status: newStatus
        })
        announcement.value.status = newStatus
      } catch (error) {
        console.error('İlan durumu güncellenirken hata:', error)
      } finally {
        isUpdatingStatus.value = false
      }
    }

    const editAnnouncement = () => {
      router.push(`/admin/announcements/edit/${route.params.id}`)
    }

    const viewApplication = (id) => {
      router.push(`/admin/applications/${id}`)
    }

    const getPositionText = (positionType) => {
      const positions = {
        'dr': 'Dr. Öğretim Üyesi',
        'doc': 'Doçent',
        'prof': 'Profesör'
      }
      return positions[positionType] || positionType
    }

    const getStatusText = (status) => {
      const statuses = {
        'pending': 'Beklemede',
        'reviewing': 'İncelemede',
        'approved': 'Onaylandı',
        'rejected': 'Reddedildi'
      }
      return statuses[status] || status
    }

    const formatDate = (dateString) => {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleDateString('tr-TR')
    }

    const maskTCKN = (tcno) => {
      if (!tcno) return '***********'
      return tcno.substring(0, 5) + '*****' + tcno.substring(9, 11)
    }

    const getPendingApplicationCount = () => {
      return applications.value.filter(
        app => app.status === 'pending' || app.status === 'reviewing'
      ).length
    }

    return {
      announcement,
      applications,
      isLoading,
      isLoadingApplications,
      isLoadingMore,
      isUpdatingStatus,
      applicationFilters,
      hasMoreApplications,
      getPositionText,
      getStatusText,
      formatDate,
      maskTCKN,
      getPendingApplicationCount,
      toggleStatus,
      editAnnouncement,
      viewApplication,
      loadMoreApplications
    }
  }
}
</script>

<style scoped>
.announcement-detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

h1 {
  font-size: 1.8rem;
  color: var(--primary-color);
  margin: 0;
}

.announcement-info {
  background: white;
  border-radius: var(--border-radius-lg);
  padding: 24px;
  margin-bottom: 24px;
  position: relative;
}

.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: var(--border-radius-sm);
  font-size: 0.9rem;
  font-weight: 500;
  position: absolute;
  top: 24px;
  right: 24px;
}

.status-badge.active {
  background-color: #e6f7ee;
  color: var(--primary-color);
}

.status-badge.inactive {
  background-color: #fef2f2;
  color: #dc2626;
}

.status-badge.pending {
  background-color: #fff7ed;
  color: #c2410c;
}

.status-badge.reviewing {
  background-color: #eff6ff;
  color: #1d4ed8;
}

.status-badge.approved {
  background-color: #e6f7ee;
  color: var(--primary-color);
}

.status-badge.rejected {
  background-color: #fef2f2;
  color: #dc2626;
}

.announcement-title {
  font-size: 1.5rem;
  color: var(--dark-color);
  margin: 0 0 24px 0;
  padding-right: 100px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-item.full-width {
  grid-column: 1 / -1;
}

.info-label {
  font-size: 0.9rem;
  color: var(--gray-color);
}

.info-value {
  font-size: 1rem;
  color: var(--dark-color);
  font-weight: 500;
}

.description {
  font-weight: normal;
  line-height: 1.6;
  white-space: pre-line;
}

.documents-section,
.criteria-section {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid var(--border-color);
}

h3 {
  font-size: 1.2rem;
  color: var(--dark-color);
  margin: 0 0 16px 0;
}

.document-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}

.document-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--border-color);
  border-radius: var(--border-radius-sm);
  font-size: 0.95rem;
}

.criteria-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.criterion-item {
  padding: 12px 16px;
  background: var(--border-color);
  border-radius: var(--border-radius-sm);
}

.criterion-name {
  font-weight: 500;
  margin-bottom: 8px;
}

.criterion-scores {
  display: flex;
  gap: 16px;
  font-size: 0.9rem;
  color: var(--gray-color);
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid var(--border-color);
}

.stat-card {
  text-align: center;
  padding: 16px;
  background: var(--border-color);
  border-radius: var(--border-radius-sm);
}

.stat-value {
  display: block;
  font-size: 1.8rem;
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.9rem;
  color: var(--gray-color);
}

.applications-section {
  background: white;
  border-radius: var(--border-radius-lg);
  padding: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header-filters {
  display: flex;
  gap: 16px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.filter-group label {
  font-size: 0.9rem;
  color: var(--gray-color);
}

.filter-group select {
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  font-size: 0.95rem;
  min-width: 150px;
}

.applications-table {
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

.candidate-cell {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
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
  padding: 6px 12px;
  font-size: 0.9rem;
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

.btn-success {
  background: var(--primary-color);
  color: white;
  border: none;
}

.btn-success:hover {
  background: var(--dark-color);
}

.btn-danger {
  background: #dc2626;
  color: white;
  border: none;
}

.btn-danger:hover {
  background: #b91c1c;
}

.empty-state {
  text-align: center;
  padding: 48px 24px;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.empty-state h3 {
  margin: 0 0 8px 0;
}

.empty-text {
  color: var(--gray-color);
  margin: 0;
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
  .announcement-detail-container {
    padding: 16px;
  }

  .page-header {
    flex-direction: column;
    gap: 16px;
  }

  .header-left {
    width: 100%;
  }

  .header-actions {
    width: 100%;
  }

  .header-actions .btn {
    flex: 1;
  }

  .section-header {
    flex-direction: column;
    gap: 16px;
  }

  .header-filters {
    width: 100%;
  }

  .filter-group {
    flex: 1;
  }

  .filter-group select {
    width: 100%;
  }

  .stats-section {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
