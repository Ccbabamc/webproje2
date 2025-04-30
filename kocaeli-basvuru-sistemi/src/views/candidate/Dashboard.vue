<template>
  <div class="candidate-dashboard">
    <h1>Aday Gösterge Paneli</h1>
    
    <div v-if="isLoading" class="loading-container">
      <div class="spinner"></div>
      <p>Veriler yükleniyor...</p>
    </div>
    
    <template v-else>
      <div class="stats-cards">
        <div class="stats-card active-announcements">
          <div class="card-icon">📢</div>
          <div class="card-info">
            <div class="card-value">{{ stats.activeAnnouncements }}</div>
            <div class="card-title">Aktif İlan</div>
          </div>
        </div>
        <div class="stats-card my-applications">
          <div class="card-icon">📝</div>
          <div class="card-info">
            <div class="card-value">{{ stats.myApplications }}</div>
            <div class="card-title">Başvurularım</div>
          </div>
        </div>
        <div class="stats-card pending-applications">
          <div class="card-icon">⏳</div>
          <div class="card-info">
            <div class="card-value">{{ stats.pendingApplications }}</div>
            <div class="card-title">Bekleyen Başvuru</div>
          </div>
        </div>
        <div class="stats-card completed-applications">
          <div class="card-icon">✓</div>
          <div class="card-info">
            <div class="card-value">{{ stats.completedApplications }}</div>
            <div class="card-title">Tamamlanan Başvuru</div>
          </div>
        </div>
      </div>
      
      <div class="content-section">
        <div class="section-header">
          <h2>Son Başvurularım</h2>
          <button class="btn btn-outline" @click="viewAllApplications">
            Tüm Başvurularım
          </button>
        </div>
        
        <div v-if="recentApplications.length === 0" class="empty-state">
          <div class="empty-icon">📮</div>
          <p>Henüz başvuru yapmadınız.</p>
          <button class="btn btn-primary" @click="viewAnnouncements">
            İlanları Görüntüle
          </button>
        </div>
        
        <div v-else class="table-container">
          <table class="data-table">
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
              <tr v-for="item in recentApplications" :key="item.id">
                <td>#{{ item.id }}</td>
                <td class="title-cell">{{ item.announcement.title }}</td>
                <td>{{ formatDate(item.created_at) }}</td>
                <td>
                  <span :class="['status-badge', getStatusClass(item.status)]">
                    {{ getStatusText(item.status) }}
                  </span>
                </td>
                <td>
                  <button class="action-btn view" @click="viewApplication(item.id)" title="Detay">
                    <span class="btn-icon">👁</span>
                  </button>
                  <button 
                    v-if="canEditApplication(item.status)"
                    class="action-btn edit" 
                    @click="editApplication(item.id)" 
                    title="Düzenle"
                  >
                    <span class="btn-icon">✎</span>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="content-section">
        <div class="section-header">
          <h2>Aktif İlanlar</h2>
          <button class="btn btn-outline" @click="viewAnnouncements">
            Tüm İlanlar
          </button>
        </div>
        
        <div v-if="activeAnnouncementsList.length === 0" class="empty-state">
          <div class="empty-icon">📢</div>
          <p>Şu anda aktif ilan bulunmamaktadır.</p>
        </div>
        
        <div v-else class="announcements-grid">
          <div v-for="announcement in activeAnnouncementsList" 
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
              >
                Başvur
              </button>
              <router-link 
                :to="`/candidate/announcements/${announcement.id}`"
                class="btn btn-outline btn-sm"
              >
                Detay
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../../api/axios'

export default {
  name: 'CandidateDashboard',
  setup() {
    const router = useRouter()
    const isLoading = ref(true)
    const stats = ref({
      activeAnnouncements: 0,
      myApplications: 0,
      pendingApplications: 0,
      completedApplications: 0
    })
    const recentApplications = ref([])
    const activeAnnouncementsList = ref([])

    onMounted(async () => {
      await fetchDashboardData()
    })

    const fetchDashboardData = async () => {
      isLoading.value = true
      try {
        await Promise.all([
          fetchStats(),
          fetchRecentApplications(),
          fetchActiveAnnouncements()
        ])
      } catch (error) {
        console.error('Dashboard verileri yüklenirken hata:', error)
      } finally {
        isLoading.value = false
      }
    }

    const fetchStats = async () => {
      try {
        const [announcementsResponse, applicationsResponse] = await Promise.all([
          apiClient.get('/api/announcements/', { params: { status: 'AKTIF' } }), // Use 'AKTIF'
          apiClient.get('/api/applications/my/')
        ])
        
        stats.value.activeAnnouncements = announcementsResponse.data.count || 0
        stats.value.myApplications = applicationsResponse.data.count || 0
        // Status names might need adjustment based on Application model
        stats.value.pendingApplications = applicationsResponse.data.results?.filter(
          app => app.status === 'BEKLEMEDE' || app.status === 'INCELEMEDE' // Adjust if needed
        ).length || 0
        stats.value.completedApplications = applicationsResponse.data.results?.filter(
          app => app.status === 'ONAYLANDI' || app.status === 'REDDEDILDI' // Adjust if needed
        ).length || 0
      } catch (error) {
        console.error('İstatistikler yüklenirken hata:', error)
      }
    }

    const fetchRecentApplications = async () => {
      try {
        const response = await apiClient.get('/api/applications/my/', {
          params: { limit: 5, ordering: '-created_at' }
        })
        recentApplications.value = response.data.results || []
      } catch (error) {
        console.error('Son başvurular yüklenirken hata:', error)
      }
    }

    const fetchActiveAnnouncements = async () => {
      try {
        const response = await apiClient.get('/api/announcements/', {
          params: { status: 'AKTIF', limit: 3, ordering: '-created_at' } // Use 'AKTIF'
        })
        activeAnnouncementsList.value = response.data.results || []
      } catch (error) {
        console.error('Aktif ilanlar yüklenirken hata:', error)
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

    const getStatusClass = (status) => {
      // Adjust keys if Application model uses different status values
      const statusClasses = {
        'BEKLEMEDE': 'pending', 
        'INCELEMEDE': 'reviewing',
        'ONAYLANDI': 'approved',
        'REDDEDILDI': 'rejected'
      }
      return statusClasses[status] || ''
    }

    const getStatusText = (status) => {
       // Adjust keys if Application model uses different status values
      const statusTexts = {
        'BEKLEMEDE': 'Beklemede',
        'INCELEMEDE': 'İncelemede',
        'ONAYLANDI': 'Onaylandı',
        'REDDEDILDI': 'Reddedildi'
      }
      return statusTexts[status] || 'Bilinmiyor'
    }

    const canEditApplication = (status) => {
      // Adjust if Application model uses different status value for pending
      return status === 'BEKLEMEDE' 
    }

    const viewApplication = (id) => {
      router.push(`/candidate/applications/${id}`)
    }

    const editApplication = (id) => {
      router.push(`/candidate/applications/edit/${id}`)
    }

    const viewAllApplications = () => {
      router.push('/candidate/applications')
    }

    const viewAnnouncements = () => {
      router.push('/candidate/announcements')
    }

    const applyToAnnouncement = (id) => {
      // Yeni başvuru sayfasına yönlendir, ilan ID'sini query param olarak ekle
      router.push({ path: '/candidate/applications/new', query: { announcementId: id } })
    }

    return {
      isLoading,
      stats,
      recentApplications,
      activeAnnouncementsList,
      getPositionText,
      formatDate,
      getStatusClass,
      getStatusText,
      canEditApplication,
      viewApplication,
      editApplication,
      viewAllApplications,
      viewAnnouncements,
      applyToAnnouncement
    }
  }
}
</script>

<style scoped>
.candidate-dashboard {
  max-width: 1400px;
  margin: 0 auto;
}

h1 {
  color: var(--primary-color);
  font-size: 2rem;
  margin-bottom: 2rem;
  font-weight: 600;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.stats-card {
  background-color: white;
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stats-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg);
}

.card-icon {
  font-size: 2rem;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-md);
  background-color: var(--border-color);
}

.card-info {
  flex: 1;
}

.card-value {
  font-size: 2rem;
  font-weight: bold;
  color: var(--primary-color);
  line-height: 1.2;
}

.card-title {
  font-size: 1rem;
  color: var(--dark-color);
  opacity: 0.8;
}

.content-section {
  background-color: white;
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
  margin-bottom: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  font-size: 1.5rem;
  color: var(--dark-color);
  margin: 0;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--gray-color);
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.table-container {
  overflow-x: auto;
  margin: 0 -1.5rem;
  padding: 0 1.5rem;
}

.data-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-bottom: 1rem;
}

.data-table th {
  background-color: var(--border-color);
  color: var(--dark-color);
  font-weight: 600;
  padding: 1rem;
  text-align: left;
  white-space: nowrap;
}

.data-table td {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
  color: var(--dark-color);
}

.title-cell {
  max-width: 250px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.status-badge {
  display: inline-block;
  padding: 0.4rem 0.8rem;
  border-radius: var(--border-radius-sm);
  font-size: 0.875rem;
  font-weight: 500;
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

.action-btn {
  padding: 0.5rem;
  border: none;
  background: none;
  cursor: pointer;
  border-radius: var(--border-radius-sm);
  transition: all 0.2s;
  margin-right: 0.5rem;
}

.action-btn:last-child {
  margin-right: 0;
}

.action-btn.edit {
  color: var(--primary-color);
}

.action-btn.view {
  color: var(--primary-color);
}

.action-btn:hover {
  background-color: var(--border-color);
  transform: scale(1.1);
}

.announcements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.announcement-card {
  background: white;
  border-radius: var(--border-radius-lg);
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
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
  gap: 0.5rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
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
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

.btn {
  display: inline-flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  border-radius: var(--border-radius-sm);
  font-weight: 500;
  transition: all 0.2s;
  cursor: pointer;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
  border: none;
}

.btn-primary:hover {
  background-color: var(--dark-color);
}

.btn-outline {
  background-color: transparent;
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
}

.btn-outline:hover {
  background-color: var(--border-color);
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid var(--border-color);
  border-top: 4px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .candidate-dashboard {
    padding: 1rem;
  }
  
  .stats-cards {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .content-section {
    padding: 1rem;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .table-container {
    margin: 0 -1rem;
    padding: 0 1rem;
  }
  
  .data-table th,
  .data-table td {
    padding: 0.75rem;
    font-size: 0.875rem;
  }
  
  .title-cell {
    max-width: 150px;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
  
  .announcement-footer .btn {
    width: auto;
  }
}

@media (max-width: 480px) {
  h1 {
    font-size: 1.75rem;
  }
  
  .section-header h2 {
    font-size: 1.25rem;
  }
  
  .card-value {
    font-size: 1.75rem;
  }
}
</style>
