<template>
  <div class="admin-dashboard">
    <h1>Gösterge Paneli</h1>
    
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Veriler yükleniyor...</p>
    </div>
    
    <template v-else>
      <div class="stats-cards">
        <div class="stats-card total-announcements">
          <div class="card-icon">📢</div>
          <div class="card-info">
            <div class="card-value">{{ stats.totalAnnouncements }}</div>
            <div class="card-title">Toplam İlan</div>
          </div>
        </div>
        <div class="stats-card active-announcements">
          <div class="card-icon">✓</div>
          <div class="card-info">
            <div class="card-value">{{ stats.activeAnnouncements }}</div>
            <div class="card-title">Aktif İlan</div>
          </div>
        </div>
        <div class="stats-card total-applications">
          <div class="card-icon">📝</div>
          <div class="card-info">
            <div class="card-value">{{ stats.totalApplications }}</div>
            <div class="card-title">Toplam Başvuru</div>
          </div>
        </div>
        <div class="stats-card pending-applications">
          <div class="card-icon">⏳</div>
          <div class="card-info">
            <div class="card-value">{{ stats.pendingApplications }}</div>
            <div class="card-title">Bekleyen Başvuru</div>
          </div>
        </div>
      </div>
      
      <div class="content-section">
        <div class="section-header">
          <h2>Son Eklenen İlanlar</h2>
          <button class="btn btn-outline" @click="createAnnouncement">
            <span class="btn-icon">+</span> Yeni İlan Ekle
          </button>
        </div>
        
        <div v-if="recentAnnouncements.length === 0" class="empty-state">
          <div class="empty-icon">📋</div>
          <p>Henüz ilan bulunmamaktadır.</p>
          <!-- Buton kaldırıldı -->
        </div>
        
        <div v-else class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>İlan No</th>
                <th>Başlık</th>
                <th>Fakülte/Bölüm</th>
                <th>Pozisyon</th>
                <th>Yayınlanma</th>
                <th>Bitiş</th>
                <th>Durum</th>
                <th>İşlemler</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in recentAnnouncements" :key="item.id">
                <td>#{{ item.id }}</td>
                <td class="title-cell">{{ item.title }}</td>
                <td>{{ item.department?.name || 'Belirtilmemiş' }}</td>
                <td>{{ getPositionText(item.position_type) }}</td>
                <td>{{ formatDate(item.start_date) }}</td>
                <td>{{ formatDate(item.end_date) }}</td>
                <td>
                  <span :class="['status-badge', item.status === 'active' ? 'active' : 'inactive']">
                    {{ item.status === 'active' ? 'Aktif' : 'Pasif' }}
                  </span>
                </td>
                <td class="actions-cell">
                  <button class="action-btn edit" @click="editAnnouncement(item.id)" title="Düzenle">
                    <span class="btn-icon">✎</span>
                  </button>
                  <button class="action-btn" 
                    :class="item.status === 'active' ? 'deactivate' : 'activate'"
                    @click="toggleAnnouncementStatus(item.id)"
                    :title="item.status === 'active' ? 'Pasife Al' : 'Aktifleştir'">
                    <span class="btn-icon">{{ item.status === 'active' ? '◉' : '○' }}</span>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          <div class="table-footer">
            <button class="btn btn-outline" @click="viewAllAnnouncements">Tüm İlanları Görüntüle</button>
          </div>
        </div>
      </div>
      
      <div class="content-section">
        <div class="section-header">
          <h2>Son Başvurular</h2>
        </div>
        
        <div v-if="recentApplications.length === 0" class="empty-state">
          <div class="empty-icon">📮</div>
          <p>Henüz başvuru bulunmamaktadır.</p>
        </div>
        
        <div v-else class="table-container">
          <table class="data-table">
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
              <tr v-for="item in recentApplications" :key="item.id">
                <td>#{{ item.id }}</td>
                <td>{{ item.candidate.full_name || `${item.candidate.first_name} ${item.candidate.last_name}` }}</td>
                <td>{{ maskTCKN(item.candidate.tcno) }}</td>
                <td class="title-cell">{{ item.announcement.title }}</td>
                <td>{{ formatDate(item.created_at) }}</td>
                <td>
                  <span :class="['status-badge', getStatusClass(item.status)]">
                    {{ getStatusText(item.status) }}
                  </span>
                </td>
                <td>
                  <button class="action-btn view" @click="viewApplication(item.id)" title="İncele">
                    <span class="btn-icon">👁</span>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          <div class="table-footer">
            <button class="btn btn-outline" @click="viewAllApplications">Tüm Başvuruları Görüntüle</button>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import apiClient from '../../api/axios'

export default {
  name: 'AdminDashboard',
  data() {
    return {
      stats: {
        totalAnnouncements: 0,
        activeAnnouncements: 0,
        totalApplications: 0,
        pendingApplications: 0
      },
      recentAnnouncements: [],
      recentApplications: [],
      loading: true
    }
  },
  created() {
    this.fetchDashboardData()
  },
  methods: {
    async fetchDashboardData() {
      this.loading = true
      try {
        await Promise.all([
          this.fetchStats(),
          this.fetchRecentAnnouncements(),
          this.fetchRecentApplications()
        ])
      } catch (error) {
        console.error('Dashboard verileri yüklenirken hata oluştu:', error)
        this.stats = {
          totalAnnouncements: 0,
          activeAnnouncements: 0,
          totalApplications: 0,
          pendingApplications: 0
        }
        this.recentAnnouncements = []
        this.recentApplications = []
      } finally {
        this.loading = false
      }
    },
    
    async fetchStats() {
      try {
        const [announcementsResponse, applicationsResponse] = await Promise.all([
          apiClient.get('/api/announcements/'),
          apiClient.get('/api/applications/applications/')
        ])
        
        const announcements = announcementsResponse.data.results || announcementsResponse.data || []
        const applications = applicationsResponse.data.results || applicationsResponse.data || []
        
        this.stats.totalAnnouncements = announcements.length || 0
        this.stats.activeAnnouncements = announcements.filter(item => item.status === 'active').length || 0
        this.stats.totalApplications = applications.length || 0
        this.stats.pendingApplications = applications.filter(item => 
          item.status === 'pending' || item.status === 'reviewing'
        ).length || 0
      } catch (error) {
        console.error('İstatistikler yüklenirken hata oluştu:', error)
      }
    },
    
    async fetchRecentAnnouncements() {
      try {
        const response = await apiClient.get('/api/announcements/', {
          params: { limit: 5, ordering: '-created_at' }
        })
        const announcements = response.data.results || response.data || []
        this.recentAnnouncements = announcements.slice(0, 5)
      } catch (error) {
        console.error('Son ilanlar yüklenirken hata oluştu:', error)
      }
    },
    
    async fetchRecentApplications() {
      try {
        const response = await apiClient.get('/api/applications/applications/', {
          params: { limit: 5, ordering: '-created_at' }
        })
        const applications = response.data.results || response.data || []
        this.recentApplications = applications.slice(0, 5)
      } catch (error) {
        console.error('Son başvurular yüklenirken hata oluştu:', error)
      }
    },
    
    getPositionText(positionType) {
      const positions = {
        'dr': 'Dr. Öğretim Üyesi',
        'doc': 'Doçent',
        'prof': 'Profesör'
      }
      return positions[positionType] || positionType
    },
    
    formatDate(dateString) {
      if (!dateString) return '-'
      const date = new Date(dateString)
      return date.toLocaleDateString('tr-TR')
    },
    
    maskTCKN(tcno) {
      if (!tcno) return '***********'
      return tcno.substring(0, 5) + '*****' + tcno.substring(9, 11)
    },
    
    getStatusClass(status) {
      const statusClasses = {
        'pending': 'pending',
        'reviewing': 'reviewing',
        'approved': 'completed',
        'rejected': 'rejected'
      }
      return statusClasses[status] || ''
    },
    
    getStatusText(status) {
      const statusTexts = {
        'pending': 'Beklemede',
        'reviewing': 'İncelemede',
        'approved': 'Tamamlandı',
        'rejected': 'Reddedildi'
      }
      return statusTexts[status] || 'Bilinmiyor'
    },
    
    async toggleAnnouncementStatus(id) {
      try {
        const announcement = this.recentAnnouncements.find(a => a.id === id)
        if (!announcement) return
        
        const newStatus = announcement.status === 'active' ? 'inactive' : 'active'
        await apiClient.put(`/api/announcements/${id}/`, {
          ...announcement,
          status: newStatus
        })
        
        announcement.status = newStatus
        await this.fetchStats() // İstatistikleri güncelle
      } catch (error) {
        console.error('İlan durumu değiştirilirken hata oluştu:', error)
      }
    },
    
    createAnnouncement() {
      this.$router.push('/admin/announcements/create')
    },
    
    editAnnouncement(id) {
      this.$router.push(`/admin/announcements/edit/${id}`)
    },
    
    viewApplication(id) {
      this.$router.push(`/admin/applications/${id}`)
    },
    
    viewAllAnnouncements() {
      this.$router.push('/admin/announcements')
    },
    
    viewAllApplications() {
      this.$router.push('/admin/applications')
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
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

.status-badge.active,
.status-badge.completed {
  background-color: #e6f7ee;
  color: var(--primary-color);
}

.status-badge.inactive,
.status-badge.rejected {
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

.action-btn.deactivate {
  color: #dc2626;
}

.action-btn.activate {
  color: var(--primary-color);
}

.action-btn:hover {
  background-color: var(--border-color);
  transform: scale(1.1);
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

.btn-icon {
  margin-right: 0.5rem;
  font-size: 1.1em;
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

.table-footer {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
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
  .admin-dashboard {
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
