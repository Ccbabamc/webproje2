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
        <button class="btn btn-outline" @click="printApplication">
          <span class="btn-icon">🖨️</span> Yazdır
        </button>
        <button 
          class="btn"
          :class="[application.status === 'approved' ? 'btn-danger' : 'btn-success']"
          @click="updateStatus(application.status === 'approved' ? 'rejected' : 'approved')"
          :disabled="isUpdatingStatus"
        >
          <div v-if="isUpdatingStatus && targetStatus === (application.status === 'approved' ? 'rejected' : 'approved')" class="spinner"></div>
          <span v-else class="btn-icon">{{ application.status === 'approved' ? '✕' : '✓' }}</span>
          {{ application.status === 'approved' ? 'Reddet' : 'Onayla' }}
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
          <div class="candidate-info card">
            <h3>Aday Bilgileri</h3>
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
          </div>

          <div class="application-status card">
            <h3>Başvuru Durumu</h3>
            <div class="status-badge" :class="application.status">
              {{ getStatusText(application.status) }}
            </div>
            <div class="status-actions">
              <label for="status-update">Durumu Güncelle:</label>
              <select id="status-update" v-model="newStatus">
                <option value="pending">Beklemede</option>
                <option value="reviewing">İncelemede</option>
                <option value="approved">Onaylandı</option>
                <option value="rejected">Reddedildi</option>
              </select>
              <button 
                class="btn btn-sm btn-primary" 
                @click="updateStatus(newStatus)"
                :disabled="isUpdatingStatus || newStatus === application.status"
              >
                <div v-if="isUpdatingStatus && targetStatus === newStatus" class="spinner"></div>
                <span v-else>Güncelle</span>
              </button>
            </div>
          </div>
        </div>

        <div class="application-main">
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
            <p v-else class="empty-text">Aday tarafından yüklenen belge bulunmamaktadır.</p>
          </div>

          <div class="table5-section card">
            <h3>Tablo 5 Bilgileri</h3>
            <div v-if="application.table5_entries?.length" class="table5-list">
              <div v-for="entry in application.table5_entries" :key="entry.id" class="table5-item">
                <span class="entry-type">{{ entry.entry_type }}</span>
                <span class="entry-description">{{ entry.description }}</span>
                <span class="entry-score">Puan: {{ entry.score }}</span>
              </div>
            </div>
            <p v-else class="empty-text">Tablo 5 bilgisi bulunmamaktadır.</p>
          </div>

          <div class="notes-section card">
            <h3>İnceleme Notları</h3>
            <textarea 
              v-model="reviewNotes" 
              placeholder="Başvuru ile ilgili notlarınızı buraya ekleyebilirsiniz..."
              rows="4"
            ></textarea>
            <button 
              class="btn btn-sm btn-outline" 
              @click="saveNotes"
              :disabled="isSavingNotes"
            >
              <div v-if="isSavingNotes" class="spinner"></div>
              <span v-else>Notları Kaydet</span>
            </button>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import apiClient from '../../api/axios'

export default {
  name: 'ApplicationDetailAdmin',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const isLoading = ref(false)
    const isUpdatingStatus = ref(false)
    const isSavingNotes = ref(false)
    const application = ref({})
    const newStatus = ref('')
    const targetStatus = ref('')
    const reviewNotes = ref('')

    onMounted(async () => {
      await loadApplication()
    })

    const loadApplication = async () => {
      isLoading.value = true
      try {
        const response = await apiClient.get(`/api/applications/applications/${route.params.id}/`)
        application.value = response.data
        newStatus.value = application.value.status
        reviewNotes.value = application.value.review_notes || ''
      } catch (error) {
        console.error('Başvuru detayları yüklenirken hata:', error)
      } finally {
        isLoading.value = false
      }
    }

    const updateStatus = async (status) => {
      if (isUpdatingStatus.value) return

      targetStatus.value = status
      isUpdatingStatus.value = true
      try {
        await apiClient.put(`/api/applications/applications/${route.params.id}/`, {
          ...application.value,
          status: status
        })
        application.value.status = status
        newStatus.value = status
      } catch (error) {
        console.error('Başvuru durumu güncellenirken hata:', error)
      } finally {
        isUpdatingStatus.value = false
        targetStatus.value = ''
      }
    }

    const saveNotes = async () => {
      if (isSavingNotes.value) return

      isSavingNotes.value = true
      try {
        await apiClient.patch(`/api/applications/applications/${route.params.id}/`, {
          review_notes: reviewNotes.value
        })
        // Başarı mesajı gösterilebilir
      } catch (error) {
        console.error('Notlar kaydedilirken hata:', error)
      } finally {
        isSavingNotes.value = false
      }
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

    return {
      application,
      isLoading,
      isUpdatingStatus,
      isSavingNotes,
      newStatus,
      targetStatus,
      reviewNotes,
      getPositionText,
      getStatusText,
      formatDate,
      updateStatus,
      saveNotes,
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

.candidate-info,
.application-status {
  background: white;
  border-radius: var(--border-radius-lg);
  padding: 20px;
}

h3 {
  font-size: 1.2rem;
  color: var(--dark-color);
  margin: 0 0 16px 0;
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

.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: var(--border-radius-sm);
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 16px;
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

.status-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.status-actions label {
  font-size: 0.9rem;
  color: var(--gray-color);
}

.status-actions select {
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  font-size: 0.95rem;
}

.application-main {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.announcement-summary,
.documents-section,
.table5-section,
.notes-section {
  background: white;
  border-radius: var(--border-radius-lg);
  padding: 20px;
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

.notes-section textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  font-size: 1rem;
  margin-bottom: 12px;
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

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
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
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
}

.btn-outline .spinner {
  border-top-color: var(--primary-color);
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
