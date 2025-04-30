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
        <button 
          class="btn btn-primary" 
          @click="applyToAnnouncement"
          :disabled="!canApply"
        >
          <span class="btn-icon">📝</span> Başvur
        </button>
      </div>
    </div>

    <div v-if="isLoading" class="loading-container">
      <div class="spinner"></div>
      <p>İlan detayları yükleniyor...</p>
    </div>

    <template v-else>
      <div class="announcement-info card">
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
      </div>
    </template>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import apiClient from '../../api/axios'

export default {
  name: 'CandidateAnnouncementDetail',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const isLoading = ref(false)
    const announcement = ref({})

    onMounted(async () => {
      await loadAnnouncement()
    })

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

    const canApply = computed(() => {
      if (!announcement.value.end_date) return false
      const endDate = new Date(announcement.value.end_date)
      const today = new Date()
      return announcement.value.status === 'active' && endDate >= today
    })

    const applyToAnnouncement = () => {
      router.push({ path: '/candidate/applications/new', query: { announcementId: route.params.id } })
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

    return {
      announcement,
      isLoading,
      canApply,
      getPositionText,
      formatDate,
      applyToAnnouncement
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
}

.announcement-title {
  font-size: 1.5rem;
  color: var(--dark-color);
  margin: 0 0 24px 0;
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

.document-icon {
  font-size: 1.2rem;
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

.btn {
  padding: 10px 16px;
  border-radius: var(--border-radius-sm);
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
  border: none;
}

.btn-primary:hover {
  background: var(--dark-color);
}

.btn-primary:disabled {
  background: var(--gray-color);
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
}
</style>
