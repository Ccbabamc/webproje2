<template>
  <div class="announcements-container">
    <div class="page-header">
      <div class="header-left">
        <h1>İlan Yönetimi</h1>
        <div class="announcement-stats">
          <div class="stat-item">
            <span class="stat-label">Toplam İlan:</span>
            <span class="stat-value">{{ totalAnnouncements }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Aktif İlan:</span>
            <span class="stat-value">{{ activeAnnouncements }}</span>
          </div>
        </div>
      </div>
      <button class="btn btn-primary" @click="createAnnouncement">
        <span class="btn-icon">+</span> Yeni İlan Ekle
      </button>
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

        <div class="filter-group">
          <label for="status">Durum</label>
          <select id="status" v-model="filters.status">
            <option value="">Tümü</option>
            <option value="active">Aktif</option>
            <option value="inactive">Pasif</option>
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
      <div class="empty-icon">📋</div>
      <h3>İlan Bulunamadı</h3>
      <p>Arama kriterlerinize uygun ilan bulunmamaktadır.</p>
      <!-- Buton kaldırıldı -->
    </div>

    <div v-else class="announcements-grid">
      <div v-for="announcement in announcements" 
           :key="announcement.id" 
           class="announcement-card card"
      >
        <div class="announcement-header">
          <div class="announcement-status" 
               :class="announcement.status">
            {{ announcement.status === 'active' ? 'Aktif' : 'Pasif' }}
          </div>
          <div class="announcement-actions">
            <button class="action-btn edit" 
                    @click="editAnnouncement(announcement.id)"
                    title="Düzenle"
            >
              ✎
            </button>
            <button class="action-btn" 
                    :class="announcement.status === 'active' ? 'deactivate' : 'activate'"
                    @click="toggleAnnouncementStatus(announcement)"
                    :title="announcement.status === 'active' ? 'Pasife Al' : 'Aktifleştir'"
            >
              {{ announcement.status === 'active' ? '◉' : '○' }}
            </button>
            <button class="action-btn delete" 
                    @click="deleteAnnouncement(announcement)"
                    title="Sil"
            >
              ×
            </button>
          </div>
        </div>

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
            {{ formatDate(announcement.start_date) }} - {{ formatDate(announcement.end_date) }}
          </div>
        </div>

        <div class="announcement-footer">
          <router-link 
            :to="`/admin/announcements/${announcement.id}`"
            class="btn btn-outline btn-sm"
          >
            Detayları Görüntüle
          </router-link>
          <div class="footer-stats">
            <span class="stat" title="Başvuru Sayısı">
              📝 {{ announcement.application_count || 0 }}
            </span>
            <span class="stat" title="Görüntülenme">
              👁 {{ announcement.view_count || 0 }}
            </span>
          </div>
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

    <!-- Silme onay modalı -->
    <div v-if="showDeleteModal" class="modal-overlay">
      <div class="modal-content card">
        <h3>İlanı Sil</h3>
        <p>
          <strong>{{ selectedAnnouncement?.title }}</strong> ilanını silmek istediğinize emin misiniz?
          <br>
          Bu işlem geri alınamaz.
        </p>
        <div class="modal-actions">
          <button class="btn btn-outline" @click="showDeleteModal = false">
            İptal
          </button>
          <button class="btn btn-danger" 
                  @click="confirmDelete"
                  :disabled="isDeletingAnnouncement"
          >
            <div v-if="isDeletingAnnouncement" class="spinner"></div>
            <span v-if="isDeletingAnnouncement">Siliniyor...</span>
            <span v-else>Sil</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../../api/axios'

export default {
  name: 'Announcements',
  setup() {
    const router = useRouter()
    const isLoading = ref(false)
    const isLoadingMore = ref(false)
    const isDeletingAnnouncement = ref(false)
    const announcements = ref([])
    const faculties = ref([])
    const departments = ref([])
    const page = ref(1)
    const hasNextPage = ref(false)
    const showDeleteModal = ref(false)
    const selectedAnnouncement = ref(null)

    const filters = ref({
      search: '',
      faculty: '',
      department: '',
      position_type: '',
      status: ''
    })

    const totalAnnouncements = computed(() => announcements.value.length)
    const activeAnnouncements = computed(() => 
      announcements.value.filter(a => a.status === 'active').length
    )

    const filteredDepartments = computed(() => {
      if (!filters.value.faculty) return departments.value
      return departments.value.filter(dept => dept.faculty === filters.value.faculty)
    })

    // İlk yükleme
    onMounted(async () => {
      await Promise.all([
        loadFaculties(),
        loadDepartments(),
        loadAnnouncements()
      ])
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
        faculties.value = response.data.results || response.data || []
      } catch (error) {
        console.error('Fakülteler yüklenirken hata:', error)
      }
    }

    const loadDepartments = async () => {
      try {
        const response = await apiClient.get('/api/announcements/departments/')
        departments.value = response.data.results || response.data || []
      } catch (error) {
        console.error('Bölümler yüklenirken hata:', error)
      }
    }

    const loadAnnouncements = async () => {
      if (isLoading.value) return

      isLoading.value = true
      try {
        const params = {
          page: page.value,
          ...filters.value
        }

        const response = await apiClient.get('/api/announcements/', { params })
        const results = response.data.results || response.data || []
        
        if (page.value === 1) {
          announcements.value = results
        } else {
          announcements.value = [...announcements.value, ...results]
        }

        hasNextPage.value = response.data.next ? true : false
      } catch (error) {
        console.error('İlanlar yüklenirken hata:', error)
      } finally {
        isLoading.value = false
      }
    }

    const loadMore = async () => {
      if (isLoadingMore.value) return

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
        status: ''
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

    const createAnnouncement = () => {
      router.push('/admin/announcements/create')
    }

    const editAnnouncement = (id) => {
      router.push(`/admin/announcements/edit/${id}`)
    }

    const toggleAnnouncementStatus = async (announcement) => {
      try {
        const newStatus = announcement.status === 'active' ? 'inactive' : 'active'
        await apiClient.put(`/api/announcements/${announcement.id}/`, {
          ...announcement,
          status: newStatus
        })
        announcement.status = newStatus
      } catch (error) {
        console.error('İlan durumu değiştirilirken hata:', error)
      }
    }

    const deleteAnnouncement = (announcement) => {
      selectedAnnouncement.value = announcement
      showDeleteModal.value = true
    }

    const confirmDelete = async () => {
      if (!selectedAnnouncement.value || isDeletingAnnouncement.value) return

      isDeletingAnnouncement.value = true
      try {
        await apiClient.delete(`/api/announcements/${selectedAnnouncement.value.id}/`)
        announcements.value = announcements.value.filter(
          a => a.id !== selectedAnnouncement.value.id
        )
        showDeleteModal.value = false
      } catch (error) {
        console.error('İlan silinirken hata:', error)
      } finally {
        isDeletingAnnouncement.value = false
      }
    }

    return {
      isLoading,
      isLoadingMore,
      isDeletingAnnouncement,
      announcements,
      faculties,
      filters,
      filteredDepartments,
      hasNextPage,
      totalAnnouncements,
      activeAnnouncements,
      showDeleteModal,
      selectedAnnouncement,
      getPositionText,
      formatDate,
      loadMore,
      handleFacultyChange,
      resetFilters,
      createAnnouncement,
      editAnnouncement,
      toggleAnnouncementStatus,
      deleteAnnouncement,
      confirmDelete
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

.announcement-stats {
  display: flex;
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

.announcement-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.announcement-status {
  padding: 4px 8px;
  border-radius: var(--border-radius-sm);
  font-size: 0.85rem;
  font-weight: 500;
}

.announcement-status.active {
  background-color: #e6f7ee;
  color: var(--primary-color);
}

.announcement-status.inactive {
  background-color: #fef2f2;
  color: #dc2626;
}

.announcement-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 6px;
  min-width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  transition: all 0.2s;
}

.action-btn.edit {
  color: var(--primary-color);
}

.action-btn.activate {
  color: var(--primary-color);
}

.action-btn.deactivate {
  color: #dc2626;
}

.action-btn.delete {
  color: #dc2626;
}

.action-btn:hover {
  background: rgba(0, 0, 0, 0.1);
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
}

.footer-stats {
  display: flex;
  gap: 12px;
}

.stat {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.9rem;
  color: var(--gray-color);
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

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 24px;
  border-radius: var(--border-radius-lg);
  max-width: 400px;
  width: 100%;
}

.modal-content h3 {
  margin: 0;
  margin-bottom: 16px;
  color: var(--dark-color);
}

.modal-content p {
  margin: 0;
  margin-bottom: 24px;
  color: var(--gray-color);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .announcements-container {
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

  .announcements-grid {
    grid-template-columns: 1fr;
  }
}
</style>
