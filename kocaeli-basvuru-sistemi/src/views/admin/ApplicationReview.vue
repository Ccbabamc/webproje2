<template>
  <div class="application-review-container">
    <div class="page-header">
      <button class="btn-back" @click="goBack">
        <span>←</span> Geri
      </button>
      <h1>Başvuru Değerlendirme</h1>
    </div>
    
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Başvuru bilgileri yükleniyor...</p>
    </div>
    
    <div v-else-if="!application.id" class="error-container">
      <div class="error-icon">!</div>
      <h2>Başvuru bulunamadı</h2>
      <p>İstenilen başvuru kaydı bulunamadı veya erişim hakkınız bulunmuyor.</p>
      <button class="btn btn-primary" @click="goToApplications">Başvurulara Dön</button>
    </div>
    
    <template v-else>
      <!-- Değerlendirme Paneli -->
      <div class="review-panel">
        <div class="status-section">
          <div class="status-header">
            <h3>Başvuru Durumu</h3>
            <div class="status-badge" :class="application.status">
              {{ getStatusText(application.status) }}
            </div>
          </div>
          
          <div class="review-actions">
            <label for="status">Durumu Değiştir:</label>
            <select 
              id="status" 
              v-model="newStatus"
              :disabled="updating"
            >
              <option value="pending">Beklemede</option>
              <option value="reviewing">İncelemede</option>
              <option value="approved">Onayla</option>
              <option value="rejected">Reddet</option>
            </select>
            
            <div class="rejection-reason" v-if="newStatus === 'rejected'">
              <label for="rejectionReason">Red Sebebi:</label>
              <textarea 
                id="rejectionReason" 
                v-model="rejectionReason"
                placeholder="Başvurunun reddedilme sebebini belirtiniz"
                rows="3"
              ></textarea>
            </div>
            
            <div class="action-buttons">
              <button 
                class="btn btn-primary" 
                @click="updateStatus"
                :disabled="updating || !statusChanged"
              >
                <span v-if="updating" class="spinner-sm"></span>
                Durumu Güncelle
              </button>
            </div>
          </div>
        </div>
        
        <div class="notes-section">
          <h3>Notlar</h3>
          
          <div class="notes-list">
            <div class="note-item" v-for="(note, index) in reviewNotes" :key="index">
              <div class="note-header">
                <span class="note-author">{{ note.author }}</span>
                <span class="note-date">{{ formatDate(note.created_at) }}</span>
              </div>
              <div class="note-content">{{ note.content }}</div>
            </div>
            
            <div class="empty-notes" v-if="reviewNotes.length === 0">
              Henüz not eklenmemiş
            </div>
          </div>
          
          <div class="add-note">
            <textarea 
              v-model="newNote" 
              placeholder="Bu başvuru hakkında not ekleyin..."
              rows="3"
            ></textarea>
            
            <button 
              class="btn btn-outline" 
              @click="addNote"
              :disabled="!newNote.trim() || addingNote"
            >
              <span v-if="addingNote" class="spinner-sm"></span>
              Not Ekle
            </button>
          </div>
        </div>
      </div>
      
      <!-- Aday ve İlan Bilgileri -->
      <div class="info-cards">
        <div class="card candidate-card">
          <h3>Aday Bilgileri</h3>
          
          <div class="card-content">
            <div class="candidate-name">{{ application.first_name }} {{ application.last_name }}</div>
            
            <div class="detail-item">
              <span class="detail-label">TC Kimlik No:</span>
              <span>{{ application.tcno }}</span>
            </div>
            
            <div class="detail-item">
              <span class="detail-label">E-posta:</span>
              <span>{{ application.email }}</span>
            </div>
            
            <div class="detail-item">
              <span class="detail-label">Telefon:</span>
              <span>{{ application.phone }}</span>
            </div>
            
            <div class="detail-item">
              <span class="detail-label">Eğitim Seviyesi:</span>
              <span>{{ getEducationLevelText(application.education_level) }}</span>
            </div>
            
            <div class="detail-item">
              <span class="detail-label">Üniversite:</span>
              <span>{{ application.university }}</span>
            </div>
          </div>
        </div>
        
        <div class="card announcement-card">
          <h3>İlan Bilgileri</h3>
          
          <div class="card-content" v-if="announcement">
            <div class="announcement-title">{{ announcement.title }}</div>
            
            <div class="detail-item">
              <span class="detail-label">Fakülte:</span>
              <span>{{ announcement.faculty?.name || '-' }}</span>
            </div>
            
            <div class="detail-item">
              <span class="detail-label">Bölüm:</span>
              <span>{{ announcement.department?.name || '-' }}</span>
            </div>
            
            <div class="detail-item">
              <span class="detail-label">Pozisyon:</span>
              <span>{{ getPositionText(announcement.position_type) }}</span>
            </div>
            
            <div class="detail-item">
              <span class="detail-label">Son Başvuru:</span>
              <span>{{ formatDate(announcement.end_date) }}</span>
            </div>
          </div>
          
          <div class="action-buttons">
            <button class="btn btn-outline" @click="viewAnnouncement">İlanı Görüntüle</button>
          </div>
        </div>
      </div>
      
      <!-- Başvuru Detayları -->
      <div class="application-details">
        <h3>Başvuru Detayları</h3>
        
        <div class="application-tabs">
          <button 
            class="tab-button" 
            :class="{ active: activeTab === 'personal' }"
            @click="activeTab = 'personal'"
          >
            Kişisel Bilgiler
          </button>
          
          <button 
            class="tab-button" 
            :class="{ active: activeTab === 'education' }"
            @click="activeTab = 'education'"
          >
            Eğitim Bilgileri
          </button>
          
          <button 
            class="tab-button" 
            :class="{ active: activeTab === 'documents' }"
            @click="activeTab = 'documents'"
          >
            Belgeler
          </button>
        </div>
        
        <div class="tab-content">
          <!-- Kişisel Bilgiler Tab -->
          <div v-if="activeTab === 'personal'" class="tab-pane">
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">Ad:</span>
                <span>{{ application.first_name }}</span>
              </div>
              
              <div class="detail-item">
                <span class="detail-label">Soyad:</span>
                <span>{{ application.last_name }}</span>
              </div>
              
              <div class="detail-item">
                <span class="detail-label">TC Kimlik No:</span>
                <span>{{ application.tcno }}</span>
              </div>
              
              <div class="detail-item">
                <span class="detail-label">Doğum Tarihi:</span>
                <span>{{ formatDate(application.birth_date) }}</span>
              </div>
              
              <div class="detail-item">
                <span class="detail-label">E-posta:</span>
                <span>{{ application.email }}</span>
              </div>
              
              <div class="detail-item">
                <span class="detail-label">Telefon:</span>
                <span>{{ application.phone }}</span>
              </div>
              
              <div class="detail-item full-width">
                <span class="detail-label">Adres:</span>
                <span>{{ application.address }}</span>
              </div>
            </div>
          </div>
          
          <!-- Eğitim Bilgileri Tab -->
          <div v-if="activeTab === 'education'" class="tab-pane">
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">Eğitim Seviyesi:</span>
                <span>{{ getEducationLevelText(application.education_level) }}</span>
              </div>
              
              <div class="detail-item">
                <span class="detail-label">Üniversite:</span>
                <span>{{ application.university }}</span>
              </div>
              
              <div class="detail-item">
                <span class="detail-label">Bölüm:</span>
                <span>{{ application.department }}</span>
              </div>
              
              <div class="detail-item">
                <span class="detail-label">Mezuniyet Yılı:</span>
                <span>{{ application.graduation_year }}</span>
              </div>
              
              <div class="detail-item full-width" v-if="application.experience">
                <span class="detail-label">Akademik/İş Deneyimi:</span>
                <div class="text-content">{{ application.experience }}</div>
              </div>
            </div>
          </div>
          
          <!-- Belgeler Tab -->
          <div v-if="activeTab === 'documents'" class="tab-pane">
            <div class="documents-grid">
              <div class="document-item">
                <h4>Diploma</h4>
                <div class="document-preview" v-if="application.diploma">
                  <a :href="application.diploma" target="_blank" class="document-link">
                    <span class="document-icon">📄</span>
                    <span>Diplomayı Görüntüle</span>
                  </a>
                </div>
                <div class="no-document" v-else>
                  Diploma yüklenmemiş
                </div>
              </div>
              
              <div class="document-item">
                <h4>Özgeçmiş (CV)</h4>
                <div class="document-preview" v-if="application.cv">
                  <a :href="application.cv" target="_blank" class="document-link">
                    <span class="document-icon">📄</span>
                    <span>Özgeçmişi Görüntüle</span>
                  </a>
                </div>
                <div class="no-document" v-else>
                  Özgeçmiş yüklenmemiş
                </div>
              </div>
              
              <div class="document-item">
                <h4>Yayınlar</h4>
                <div class="document-preview" v-if="application.publications">
                  <a :href="application.publications" target="_blank" class="document-link">
                    <span class="document-icon">📄</span>
                    <span>Yayınları Görüntüle</span>
                  </a>
                </div>
                <div class="no-document" v-else>
                  Yayın dosyası yüklenmemiş
                </div>
              </div>
              
              <div class="document-item">
                <h4>Ek Belgeler</h4>
                <div class="document-preview" v-if="application.additional_documents">
                  <a :href="application.additional_documents" target="_blank" class="document-link">
                    <span class="document-icon">📄</span>
                    <span>Ek Belgeleri Görüntüle</span>
                  </a>
                </div>
                <div class="no-document" v-else>
                  Ek belge yüklenmemiş
                </div>
              </div>
            </div>
            
            <div class="application-notes" v-if="application.notes">
              <h4>Aday Notları</h4>
              <div class="text-content">{{ application.notes }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Başvuru Zaman Çizelgesi -->
      <div class="timeline-section">
        <h3>İşlem Geçmişi</h3>
        
        <div class="timeline">
          <div class="timeline-item">
            <div class="timeline-marker"></div>
            <div class="timeline-content">
              <div class="timeline-date">{{ formatDate(application.created_at) }}</div>
              <div class="timeline-title">Başvuru Oluşturuldu</div>
            </div>
          </div>
          
          <div class="timeline-item" v-for="(log, index) in statusLogs" :key="index">
            <div class="timeline-marker"></div>
            <div class="timeline-content">
              <div class="timeline-date">{{ formatDate(log.created_at) }}</div>
              <div class="timeline-title">
                Durum değiştirildi: <span class="status-text" :class="log.status">{{ getStatusText(log.status) }}</span>
              </div>
              <div class="timeline-description" v-if="log.reason">
                {{ log.reason }}
              </div>
              <div class="timeline-author" v-if="log.user">
                {{ log.user }}
              </div>
            </div>
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
  name: 'ApplicationReview',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const applicationId = route.params.id
    
    // State tanımlamaları
    const loading = ref(true)
    const updating = ref(false)
    const addingNote = ref(false)
    const application = ref({})
    const announcement = ref(null)
    const reviewNotes = ref([])
    const statusLogs = ref([])
    
    // Form State
    const newStatus = ref('')
    const rejectionReason = ref('')
    const newNote = ref('')
    const activeTab = ref('personal')
    
    // Başvuru bilgilerini getir
    const fetchApplicationDetails = async () => {
      loading.value = true
      try {
        const response = await apiClient.get(`/api/applications/applications/${applicationId}/`)
        application.value = response.data
        newStatus.value = application.value.status // Mevcut durumu formda göster
        
        // İlan bilgilerini getir
        if (application.value.announcement) {
          await fetchAnnouncementDetails(application.value.announcement)
        }
        
        // Not ve durum değişikliği geçmişini getir
        await fetchReviewNotes()
        await fetchStatusLogs()
      } catch (error) {
        console.error('Başvuru detayları yüklenirken hata oluştu:', error)
      } finally {
        loading.value = false
      }
    }
    
    // İlan bilgilerini getir
    const fetchAnnouncementDetails = async (announcementId) => {
      try {
        const response = await apiClient.get(`/api/announcements/${announcementId}/`)
        announcement.value = response.data
      } catch (error) {
        console.error('İlan bilgileri yüklenirken hata oluştu:', error)
      }
    }
    
    // Değerlendirme notlarını getir
    const fetchReviewNotes = async () => {
      try {
        const response = await apiClient.get(`/api/applications/notes/`, {
          params: { application_id: applicationId }
        })
        reviewNotes.value = response.data || []
      } catch (error) {
        console.error('Değerlendirme notları yüklenirken hata oluştu:', error)
      }
    }
    
    // Durum değişiklik geçmişini getir
    const fetchStatusLogs = async () => {
      try {
        const response = await apiClient.get(`/api/applications/status-logs/`, {
          params: { application_id: applicationId }
        })
        statusLogs.value = response.data || []
      } catch (error) {
        console.error('Durum değişiklik geçmişi yüklenirken hata oluştu:', error)
      }
    }
    
    // Durumu güncelle
    const updateStatus = async () => {
      if (!statusChanged.value) return
      
      updating.value = true
      try {
        const data = {
          status: newStatus.value
        }
        
        // Reddedilme durumunda sebep ekle
        if (newStatus.value === 'rejected' && rejectionReason.value.trim()) {
          data.rejection_reason = rejectionReason.value.trim()
        }
        
        // API isteği
        await apiClient.patch(`/api/applications/applications/${applicationId}/`, data)
        
        // Başarılı ise yenile
        application.value.status = newStatus.value
        if (newStatus.value === 'rejected') {
          application.value.rejection_reason = rejectionReason.value.trim()
        }
        
        // Log bilgilerini güncelle
        await fetchStatusLogs()
        
        alert('Başvuru durumu başarıyla güncellendi.')
      } catch (error) {
        console.error('Durum güncellenirken hata oluştu:', error)
        alert('Durum güncellenirken bir hata oluştu. Lütfen daha sonra tekrar deneyin.')
      } finally {
        updating.value = false
      }
    }
    
    // Not ekle
    const addNote = async () => {
      if (!newNote.value.trim()) return
      
      addingNote.value = true
      try {
        const noteData = {
          application: applicationId,
          content: newNote.value.trim()
        }
        
        // API isteği
        await apiClient.post('/api/applications/notes/', noteData)
        
        // Başarılı ise yenile ve formu temizle
        await fetchReviewNotes()
        newNote.value = ''
      } catch (error) {
        console.error('Not eklenirken hata oluştu:', error)
        alert('Not eklenirken bir hata oluştu. Lütfen daha sonra tekrar deneyin.')
      } finally {
        addingNote.value = false
      }
    }
    
    // İlanı görüntüle
    const viewAnnouncement = () => {
      if (announcement.value && announcement.value.id) {
        router.push(`/admin/announcements/${announcement.value.id}`)
      }
    }
    
    // Yönlendirmeler
    const goBack = () => {
      router.go(-1)
    }
    
    const goToApplications = () => {
      router.push('/admin/applications')
    }
    
    // Hesaplanmış Özellikler
    
    // Durum değişti mi?
    const statusChanged = computed(() => {
      return newStatus.value !== application.value.status
    })
    
    // Helper Fonksiyonlar
    const getStatusText = (status) => {
      switch(status) {
        case 'pending': return 'Beklemede'
        case 'reviewing': return 'İncelemede'
        case 'approved': return 'Onaylandı'
        case 'rejected': return 'Reddedildi'
        case 'withdrawn': return 'Geri Çekildi'
        default: return 'Bilinmiyor'
      }
    }
    
    const getPositionText = (positionType) => {
      switch(positionType) {
        case 'dr': return 'Dr. Öğretim Üyesi'
        case 'doc': return 'Doçent'
        case 'prof': return 'Profesör'
        default: return positionType
      }
    }
    
    const getEducationLevelText = (level) => {
      switch(level) {
        case 'associate': return 'Ön Lisans'
        case 'bachelor': return 'Lisans'
        case 'master': return 'Yüksek Lisans'
        case 'phd': return 'Doktora'
        default: return level
      }
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return '-'
      const date = new Date(dateString)
      return date.toLocaleDateString('tr-TR')
    }
    
    onMounted(() => {
      fetchApplicationDetails()
    })
    
    return {
      application,
      announcement,
      loading,
      updating,
      addingNote,
      newStatus,
      rejectionReason,
      newNote,
      reviewNotes,
      statusLogs,
      activeTab,
      statusChanged,
      updateStatus,
      addNote,
      viewAnnouncement,
      goBack,
      goToApplications,
      getStatusText,
      getPositionText,
      getEducationLevelText,
      formatDate
    }
  }
}
</script>

<style scoped>
.application-review-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
}

.btn-back {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 8px 15px;
  background-color: #f0f0f0;
  border: none;
  border-radius: 4px;
  color: #333;
  cursor: pointer;
  font-weight: 500;
}

h1 {
  color: #0056b3;
  margin: 0;
}

.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px 0;
  text-align: center;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid #0056b3;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

.spinner-sm {
  display: inline-block;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top: 2px solid #fff;
  width: 16px;
  height: 16px;
  animation: spin 1s linear infinite;
  margin-right: 8px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  background-color: #f8d7da;
  color: #dc3545;
  border-radius: 50%;
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 15px;
}

/* Review Panel */
.review-panel {
  display: flex;
  gap: 25px;
  margin-bottom: 30px;
}

.status-section,
.notes-section {
  flex: 1;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  padding: 20px;
}

.status-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.status-header h3 {
  margin: 0;
}

.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: 500;
  font-size: 0.9rem;
}

.status-badge.pending {
  background-color: #fff9eb;
  color: #b45309;
}

.status-badge.reviewing {
  background-color: #e6f0f9;
  color: #0369a1;
}

.status-badge.approved {
  background-color: #e6f7ee;
  color: #0d9488;
}

.status-badge.rejected {
  background-color: #fee;
  color: #e11d48;
}

.status-badge.withdrawn {
  background-color: #f1f1f1;
  color: #6c757d;
}

.review-actions {
  margin-top: 15px;
}

.review-actions label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #495057;
}

.review-actions select,
.review-actions textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 1rem;
  margin-bottom: 15px;
}

.rejection-reason {
  margin-top: 15px;
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 15px;
}

/* Notes Section */
.notes-section h3 {
  margin-top: 0;
  margin-bottom: 20px;
}

.notes-list {
  max-height: 250px;
  overflow-y: auto;
  margin-bottom: 20px;
  border: 1px solid #e9ecef;
  border-radius: 4px;
}

.note-item {
  padding: 15px;
  border-bottom: 1px solid #e9ecef;
}

.note-item:last-child {
  border-bottom: none;
}

.note-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.note-author {
  font-weight: 500;
  color: #495057;
}

.note-date {
  color: #6c757d;
}

.note-content {
  white-space: pre-line;
}

.empty-notes {
  padding: 20px;
  text-align: center;
  color: #6c757d;
  font-style: italic;
}

.add-note textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  margin-bottom: 10px;
  resize: vertical;
}

/* Info Cards */
.info-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 25px;
  margin-bottom: 30px;
}

.card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  padding: 20px;
}

.card h3 {
  color: #333;
  margin-top: 0;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.card-content {
  margin-bottom: 20px;
}

.candidate-name, 
.announcement-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #0056b3;
  margin-bottom: 15px;
}

.detail-item {
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
}

.detail-label {
  font-weight: 500;
  color: #666;
  margin-bottom: 3px;
}

/* Application Details */
.application-details {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  padding: 20px;
  margin-bottom: 30px;
}

.application-details h3 {
  color: #333;
  margin-top: 0;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.application-tabs {
  display: flex;
  border-bottom: 1px solid #dee2e6;
  margin-bottom: 20px;
}

.tab-button {
  padding: 10px 20px;
  background: none;
  border: none;
  cursor: pointer;
  font-weight: 500;
  color: #6c757d;
  border-bottom: 2px solid transparent;
}

.tab-button.active {
  color: #0056b3;
  border-bottom-color: #0056b3;
}

.tab-pane {
  padding: 15px 0;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.detail-item.full-width {
  grid-column: span 2;
}

.text-content {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
  white-space: pre-line;
}

/* Documents */
.documents-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.document-item {
  border: 1px solid #e9ecef;
  border-radius: 6px;
  padding: 15px;
}

.document-item h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #495057;
}

.document-preview {
  margin-top: 10px;
}

.document-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #0056b3;
  padding: 10px;
  background-color: #e7f5ff;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.document-link:hover {
  background-color: #d1e7ff;
}

.document-icon {
  font-size: 1.5rem;
  margin-right: 10px;
}

.no-document {
  padding: 10px;
  color: #6c757d;
  font-style: italic;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.application-notes {
  margin-top: 30px;
}

.application-notes h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #495057;
}

/* Timeline */
.timeline-section {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  padding: 20px;
  margin-bottom: 30px;
}

.timeline-section h3 {
  color: #333;
  margin-top: 0;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.timeline {
  position: relative;
  padding-left: 40px;
}

.timeline:before {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  left: 15px;
  width: 2px;
  background-color: #e9ecef;
}

.timeline-item {
  position: relative;
  margin-bottom: 30px;
}

.timeline-item:last-child {
  margin-bottom: 0;
}

.timeline-marker {
  position: absolute;
  top: 5px;
  left: -40px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #0056b3;
  border: 2px solid white;
  z-index: 1;
}

.timeline-content {
  padding-bottom: 15px;
}

.timeline-date {
  font-size: 0.85rem;
  color: #6c757d;
  margin-bottom: 5px;
}

.timeline-title {
  font-weight: 500;
  margin-bottom: 5px;
}

.timeline-description {
  margin-top: 5px;
  white-space: pre-line;
}

.timeline-author {
  font-size: 0.85rem;
  color: #6c757d;
  margin-top: 5px;
  font-style: italic;
}

.status-text {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
}

.status-text.pending {
  background-color: #fff9eb;
  color: #b45309;
}

.status-text.reviewing {
  background-color: #e6f0f9;
  color: #0369a1;
}

.status-text.approved {
  background-color: #e6f7ee;
  color: #0d9488;
}

.status-text.rejected {
  background-color: #fee;
  color: #e11d48;
}

.status-text.withdrawn {
  background-color: #f1f1f1;
  color: #6c757d;
}

/* Buttons */
.btn {
  padding: 10px 20px;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-primary {
  background-color: #0056b3;
  color: white;
  border: none;
}

.btn-outline {
  background-color: transparent;
  color: #0056b3;
  border: 1px solid #0056b3;
}

.btn-outline-danger {
  background-color: transparent;
  color: #dc3545;
  border: 1px solid #dc3545;
}

.btn:hover {
  opacity: 0.9;
}

.btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 992px) {
  .review-panel,
  .info-cards {
    flex-direction: column;
    display: block;
  }
  
  .status-section,
  .notes-section,
  .card {
    margin-bottom: 20px;
  }
  
  .documents-grid,
  .detail-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .application-tabs {
    flex-wrap: wrap;
  }
  
  .tab-button {
    flex: 1 0 auto;
    text-align: center;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 10px;
  }
  
  .btn {
    width: 100%;
  }
}
</style> 