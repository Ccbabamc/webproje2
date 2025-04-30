<template>
  <div class="application-detail-container">
    <div class="page-header">
      <div class="header-left">
        <button class="btn btn-outline" @click="$router.back()">
          <span class="btn-icon">←</span> Geri Dön
        </button>
        <h1>Başvuru Detayları</h1>
      </div>
      <div class="header-actions">
        <button 
          v-if="canEditApplication"
          class="btn btn-outline" 
          @click="editApplication"
        >
          <span class="btn-icon">✎</span> Düzenle
        </button>
        <button class="btn btn-outline" @click="printApplication">
          <span class="btn-icon">🖨️</span> Yazdır
        </button>
      </div>
    </div>

    <div v-if="isLoading" class="loading-container">
      <div class="spinner"></div>
      <p>Başvuru detayları yükleniyor...</p>
    </div>

    <template v-else>
      <div class="application-content">
        <div class="application-sidebar">
          <div class="application-status card">
            <h3>Başvuru Durumu</h3>
            <div class="status-badge" :class="getStatusClass(application.status)">
              {{ getStatusText(application.status) }}
            </div>
            <p class="status-description">
              {{ getStatusDescription(application.status) }}
            </p>
          </div>

          <div class="announcement-summary card">
            <h3>İlan Bilgileri</h3>
            <div class="info-item">
              <span class="info-label">Başlık</span>
              <span class="info-value">{{ application.announcement?.title }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Pozisyon</span>
              <span class="info-value">
                {{ getPositionText(application.announcement?.position_type) }}
              </span>
            </div>
            <div class="info-item">
              <span class="info-label">Bölüm</span>
              <span class="info-value">
                {{ application.announcement?.department?.name }}
              </span>
            </div>
            <router-link 
              :to="`/candidate/announcements/${application.announcement?.id}`"
              class="btn btn-sm btn-outline"
            >
              İlan Detayına Git
            </router-link>
          </div>
        </div>

        <div class="application-main">
          <div class="candidate-info card">
            <h3>Kişisel Bilgiler</h3>
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">Ad Soyad</span>
                <span class="info-value">
                  {{ application.candidate?.full_name || 
                     `${application.candidate?.first_name} ${application.candidate?.last_name}` }}
                </span>
              </div>
              <div class="info-item">
                <span class="info-label">TC Kimlik No</span>
                <span class="info-value">{{ application.candidate?.tcno }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">E-posta</span>
                <span class="info-value">{{ application.candidate?.email }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Telefon</span>
                <span class="info-value">{{ application.candidate?.phone_number }}</span>
              </div>
              <div class="info-item full-width">
                <span class="info-label">Adres</span>
                <span class="info-value">{{ application.candidate?.address }}</span>
              </div>
            </div>
          </div>

          <div class="education-section card">
            <h3>Eğitim Bilgileri</h3>
            <div v-if="application.education?.length" class="education-list">
              <div v-for="(edu, index) in application.education" :key="index" class="education-item">
                <p><strong>Üniversite:</strong> {{ edu.university }}</p>
                <p><strong>Derece:</strong> {{ edu.degree }}</p>
                <p><strong>Alan:</strong> {{ edu.field_of_study }}</p>
                <p><strong>Mezuniyet Yılı:</strong> {{ edu.graduation_year }}</p>
              </div>
            </div>
            <p v-else class="empty-text">Eğitim bilgisi bulunmamaktadır.</p>
          </div>

          <div class="table5-section card">
            <h3>Akademik Çalışmalar (Tablo 5)</h3>
            <div v-if="application.table5_entries?.length" class="table5-list">
              <div v-for="entry in application.table5_entries" :key="entry.id" class="table5-item">
                <span class="entry-type">{{ entry.entry_type }}</span>
                <span class="entry-description">{{ entry.description }}</span>
                <span class="entry-score">Puan: {{ entry.score }}</span>
              </div>
            </div>
            <p v-else class="empty-text">Tablo 5 bilgisi bulunmamaktadır.</p>
          </div>

          <div class="documents-section card">
            <h3>Yüklenen Belgeler</h3>
            <div v-if="application.documents?.length" class="document-list">
              <div v-for="doc in application.documents" :key="doc.id" class="document-item">
                <span class="document-icon">📄</span>
                <a :href="doc.file" target="_blank" class="document-link">
                  {{ doc.name || 'Belge' }}
                </a>
                <span class="document-date">
                  ({{ formatDate(doc.uploaded_at) }})
                </span>
              </div>
            </div>
            <p v-else class="empty-text">Yüklenen belge bulunmamaktadır.</p>
          </div>
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
  name: 'CandidateApplicationDetail',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const isLoading = ref(false)
    const application = ref({})

    onMounted(async () => {
      await loadApplication()
    })

    const loadApplication = async () => {
      isLoading.value = true
      try {
        // Aday kendi başvurusunu /api/applications/my/{id}/ endpointinden almalı
        // Ancak API listesinde böyle bir endpoint yok, genel endpointi kullanıyoruz
        // Güvenlik backend tarafında sağlanmalı
        const response = await apiClient.get(`/api/applications/applications/${route.params.id}/`)
        application.value = response.data
      } catch (error) {
        console.error('Başvuru detayları yüklenirken hata:', error)
        // Hata durumunda kullanıcıyı bilgilendir veya yönlendir
      } finally {
        isLoading.value = false
      }
    }

    const canEditApplication = computed(() => {
      return application.value.status === 'pending'
    })

    const editApplication = () => {
      router.push(`/candidate/applications/edit/${route.params.id}`)
    }

    const printApplication = () => {
      window.print()
    }

    const getPositionText = (positionType) => {
      const positions = {
        'dr': 'Dr. Öğretim Üyesi',
        'doc': 'Doçent',
        'prof': 'Profesör'
      }
      return positions[positionType] || positionType
    }

    const getStatusClass = (status) => {
      const statusClasses = {
        'pending': 'pending',
        'reviewing': 'reviewing',
        'approved': 'approved',
        'rejected': 'rejected'
      }
      return statusClasses[status] || ''
    }

    const getStatusText = (status) => {
      const statuses = {
        'pending': 'Beklemede',
        'reviewing': 'İncelemede',
        'approved': 'Onaylandı',
        'rejected': 'Reddedildi'
      }
      return statuses[status] || 'Bilinmiyor'
    }

    const getStatusDescription = (status) => {
      const descriptions = {
        'pending': 'Başvurunuz alındı ve değerlendirme için bekliyor.',
        'reviewing': 'Başvurunuz ilgili komisyon tarafından inceleniyor.',
        'approved': 'Tebrikler! Başvurunuz onaylandı.',
        'rejected': 'Üzgünüz, başvurunuz reddedildi.'
      }
      return descriptions[status] || ''
    }

    const formatDate = (dateString) => {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleDateString('tr-TR')
    }

    return {
      application,
      isLoading,
      canEditApplication,
      getPositionText,
      getStatusClass,
      getStatusText,
      getStatusDescription,
      formatDate,
      editApplication,
      printApplication
    }
  }
}
</script>

<style scoped>
.application-detail-container {
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

.application-content {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 24px;
}

.application-sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.application-status,
.announcement-summary {
  background: white;
  border-radius: var(--border-radius-lg);
  padding: 20px;
}

h3 {
  font-size: 1.2rem;
  color: var(--dark-color);
  margin: 0 0 16px 0;
}

.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: var(--border-radius-sm);
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 12px;
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

.status-description {
  font-size: 0.95rem;
  color: var(--gray-color);
  margin: 0;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 12px;
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

.application-main {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.candidate-info,
.education-section,
.table5-section,
.documents-section {
  background: white;
  border-radius: var(--border-radius-lg);
  padding: 20px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.info-item.full-width {
  grid-column: 1 / -1;
}

.education-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.education-item {
  padding-bottom: 16px;
  border-bottom: 1px dashed var(--border-color);
}
.education-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.education-item p {
  margin: 4px 0;
  font-size: 0.95rem;
}

.table5-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.table5-item {
  padding: 12px 16px;
  background: var(--border-color);
  border-radius: var(--border-radius-sm);
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 16px;
  align-items: center;
}

.entry-type {
  font-weight: 500;
}

.entry-description {
  color: var(--gray-color);
  font-size: 0.9rem;
}

.entry-score {
  font-weight: 600;
  color: var(--primary-color);
}

.document-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 12px;
}

.document-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--border-color);
  border-radius: var(--border-radius-sm);
}

.document-icon {
  font-size: 1.2rem;
}

.document-link {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 500;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.document-link:hover {
  text-decoration: underline;
}

.document-date {
  font-size: 0.85rem;
  color: var(--gray-color);
}

.empty-text {
  color: var(--gray-color);
  margin: 0;
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

@media (max-width: 992px) {
  .application-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .application-detail-container {
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
