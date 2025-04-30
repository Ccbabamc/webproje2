<template>
  <div class="application-form-container">
    <div class="page-header">
      <h1>{{ isEditing ? 'Başvuru Düzenle' : 'Yeni Başvuru' }}</h1>
      <button class="btn btn-outline" @click="$router.back()">
        <span class="btn-icon">←</span> Geri Dön
      </button>
    </div>

    <div class="form-wrapper card">
      <div class="stepper">
        <div v-for="(step, index) in steps" 
             :key="index" 
             class="step" 
             :class="{ active: currentStep === index, completed: index < currentStep }"
             @click="goToStep(index)"
        >
          <div class="step-number">{{ index + 1 }}</div>
          <div class="step-label">{{ step.label }}</div>
        </div>
      </div>

      <form @submit.prevent="handleSubmit" class="application-form">
        <!-- Step 1: Kişisel Bilgiler -->
        <div v-if="currentStep === 0" class="form-step">
          <h2>Kişisel Bilgiler</h2>
          <div class="form-grid">
            <div class="form-group">
              <label for="first_name">Ad</label>
              <input type="text" id="first_name" v-model="formData.candidate.first_name" disabled>
            </div>
            <div class="form-group">
              <label for="last_name">Soyad</label>
              <input type="text" id="last_name" v-model="formData.candidate.last_name" disabled>
            </div>
            <div class="form-group">
              <label for="tcno">TC Kimlik No</label>
              <input type="text" id="tcno" v-model="formData.candidate.tcno" disabled>
            </div>
            <div class="form-group">
              <label for="email">E-posta</label>
              <input type="email" id="email" v-model="formData.candidate.email" disabled>
            </div>
            <div class="form-group">
              <label for="phone_number">Telefon Numarası</label>
              <input type="tel" id="phone_number" v-model="formData.candidate.phone_number">
            </div>
            <div class="form-group full-width">
              <label for="address">Adres</label>
              <textarea id="address" v-model="formData.candidate.address" rows="3"></textarea>
            </div>
          </div>
        </div>

        <!-- Step 2: Eğitim Bilgileri -->
        <div v-if="currentStep === 1" class="form-step">
          <h2>Eğitim Bilgileri</h2>
          <div v-for="(edu, index) in formData.education" :key="index" class="education-item">
            <div class="item-header">
              <h3>Eğitim #{{ index + 1 }}</h3>
              <button type="button" class="btn-icon" @click="removeEducation(index)">✕</button>
            </div>
            <div class="form-grid">
              <div class="form-group">
                <label :for="'university-' + index">Üniversite</label>
                <input type="text" :id="'university-' + index" v-model="edu.university">
              </div>
              <div class="form-group">
                <label :for="'degree-' + index">Derece</label>
                <input type="text" :id="'degree-' + index" v-model="edu.degree">
              </div>
              <div class="form-group">
                <label :for="'field_of_study-' + index">Alan</label>
                <input type="text" :id="'field_of_study-' + index" v-model="edu.field_of_study">
              </div>
              <div class="form-group">
                <label :for="'graduation_year-' + index">Mezuniyet Yılı</label>
                <input type="number" :id="'graduation_year-' + index" v-model="edu.graduation_year">
              </div>
            </div>
          </div>
          <button type="button" class="btn btn-outline" @click="addEducation">
            + Eğitim Ekle
          </button>
        </div>

        <!-- Step 3: Akademik Çalışmalar (Tablo 5) -->
        <div v-if="currentStep === 2" class="form-step">
          <h2>Akademik Çalışmalar (Tablo 5)</h2>
          <div v-for="(entry, index) in formData.table5_entries" :key="index" class="table5-item">
            <div class="item-header">
              <h3>Çalışma #{{ index + 1 }}</h3>
              <button type="button" class="btn-icon" @click="removeTable5Entry(index)">✕</button>
            </div>
            <div class="form-grid">
              <div class="form-group">
                <label :for="'entry_type-' + index">Çalışma Türü</label>
                <select :id="'entry_type-' + index" v-model="entry.entry_type">
                  <option value="">Tür Seçiniz</option>
                  <option value="publication">Yayın</option>
                  <option value="citation">Atıf</option>
                  <option value="conference">Konferans</option>
                  <option value="project">Proje</option>
                  <option value="patent">Patent</option>
                  <option value="other">Diğer</option>
                </select>
              </div>
              <div class="form-group full-width">
                <label :for="'description-' + index">Açıklama</label>
                <textarea :id="'description-' + index" v-model="entry.description" rows="2"></textarea>
              </div>
              <div class="form-group">
                <label :for="'score-' + index">Puan</label>
                <input type="number" :id="'score-' + index" v-model="entry.score" min="0">
              </div>
            </div>
          </div>
          <button type="button" class="btn btn-outline" @click="addTable5Entry">
            + Çalışma Ekle
          </button>
        </div>

        <!-- Step 4: Belgeler -->
        <div v-if="currentStep === 3" class="form-step">
          <h2>Belgeler</h2>
          <div class="form-group">
            <label>Gerekli Belgeler</label>
            <ul class="required-docs-list">
              <li v-for="(doc, index) in announcement.required_documents" :key="index">
                {{ doc }}
              </li>
            </ul>
          </div>
          <div class="form-group">
            <label for="documents">Belgeleri Yükle</label>
            <input 
              type="file" 
              id="documents" 
              multiple 
              @change="handleFileUpload"
              accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
            >
            <div v-if="uploadedFiles.length > 0" class="uploaded-files-list">
              <h4>Yüklenen Dosyalar:</h4>
              <ul>
                <li v-for="(file, index) in uploadedFiles" :key="index">
                  {{ file.name }} ({{ formatFileSize(file.size) }})
                  <button type="button" class="btn-icon" @click="removeFile(index)">✕</button>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Step 5: Önizleme -->
        <div v-if="currentStep === 4" class="form-step preview-step">
          <h2>Başvuru Önizleme</h2>
          <div class="preview-section">
            <h3>Kişisel Bilgiler</h3>
            <p><strong>Ad Soyad:</strong> {{ formData.candidate.first_name }} {{ formData.candidate.last_name }}</p>
            <p><strong>TC Kimlik No:</strong> {{ formData.candidate.tcno }}</p>
            <p><strong>E-posta:</strong> {{ formData.candidate.email }}</p>
            <p><strong>Telefon:</strong> {{ formData.candidate.phone_number }}</p>
            <p><strong>Adres:</strong> {{ formData.candidate.address }}</p>
          </div>
          <div class="preview-section">
            <h3>Eğitim Bilgileri</h3>
            <div v-for="(edu, index) in formData.education" :key="index" class="preview-item">
              <p><strong>Üniversite:</strong> {{ edu.university }}</p>
              <p><strong>Derece:</strong> {{ edu.degree }}</p>
              <p><strong>Alan:</strong> {{ edu.field_of_study }}</p>
              <p><strong>Mezuniyet Yılı:</strong> {{ edu.graduation_year }}</p>
            </div>
          </div>
          <div class="preview-section">
            <h3>Akademik Çalışmalar</h3>
            <div v-for="(entry, index) in formData.table5_entries" :key="index" class="preview-item">
              <p><strong>Tür:</strong> {{ entry.entry_type }}</p>
              <p><strong>Açıklama:</strong> {{ entry.description }}</p>
              <p><strong>Puan:</strong> {{ entry.score }}</p>
            </div>
          </div>
          <div class="preview-section">
            <h3>Yüklenen Belgeler</h3>
            <ul>
              <li v-for="(file, index) in uploadedFiles" :key="index">{{ file.name }}</li>
            </ul>
          </div>
        </div>

        <div class="form-navigation">
          <button 
            type="button" 
            class="btn btn-outline" 
            @click="prevStep" 
            :disabled="currentStep === 0"
          >
            Geri
          </button>
          <button 
            type="button" 
            class="btn btn-primary" 
            @click="nextStep" 
            v-if="currentStep < steps.length - 1"
          >
            İleri
          </button>
          <button 
            type="submit" 
            class="btn btn-success" 
            v-if="currentStep === steps.length - 1"
            :disabled="isLoading"
          >
            <div v-if="isLoading" class="spinner"></div>
            <span v-else>{{ isEditing ? 'Güncelle' : 'Başvuruyu Tamamla' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import apiClient from '../../api/axios'

export default {
  name: 'ApplicationForm',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()
    const isLoading = ref(false)
    const isEditing = computed(() => !!route.params.id)
    const currentStep = ref(0)
    const announcement = ref({})
    const uploadedFiles = ref([])

    const steps = [
      { label: 'Kişisel Bilgiler' },
      { label: 'Eğitim Bilgileri' },
      { label: 'Akademik Çalışmalar' },
      { label: 'Belgeler' },
      { label: 'Önizleme' }
    ]

    const formData = ref({
      announcement: route.query.announcementId || null,
      candidate: { ...authStore.user }, // Kullanıcı bilgilerini başlangıçta al
      education: [],
      table5_entries: [],
      documents: [] // Yüklenecek dosyaların ID'lerini tutacak
    })

    onMounted(async () => {
      if (!formData.value.candidate) {
        await authStore.fetchUser()
        formData.value.candidate = { ...authStore.user }
      }

      if (formData.value.announcement) {
        await loadAnnouncementDetails(formData.value.announcement)
      }

      if (isEditing.value) {
        await loadApplicationData()
      }
    })

    const loadAnnouncementDetails = async (id) => {
      try {
        const response = await apiClient.get(`/api/announcements/${id}/`)
        announcement.value = response.data
      } catch (error) {
        console.error('İlan detayları yüklenirken hata:', error)
      }
    }

    const loadApplicationData = async () => {
      isLoading.value = true
      try {
        const response = await apiClient.get(`/api/applications/applications/${route.params.id}/`)
        const appData = response.data
        formData.value = {
          ...appData,
          candidate: appData.candidate || { ...authStore.user },
          education: appData.education || [],
          table5_entries: appData.table5_entries || [],
          documents: appData.documents?.map(doc => doc.id) || [] // Mevcut belge ID'leri
        }
        // Mevcut belgeleri de göstermek için yüklenebilir
        // uploadedFiles.value = appData.documents?.map(doc => ({ name: doc.name, size: 0, id: doc.id })) || []
        if (appData.announcement) {
          formData.value.announcement = appData.announcement.id
          await loadAnnouncementDetails(appData.announcement.id)
        }
      } catch (error) {
        console.error('Başvuru verileri yüklenirken hata:', error)
      } finally {
        isLoading.value = false
      }
    }

    const nextStep = () => {
      if (currentStep.value < steps.length - 1) {
        currentStep.value++
      }
    }

    const prevStep = () => {
      if (currentStep.value > 0) {
        currentStep.value--
      }
    }

    const goToStep = (index) => {
      // Sadece önceki adımlara veya mevcut adıma tıklanabilir
      if (index <= currentStep.value) {
        currentStep.value = index
      }
    }

    const addEducation = () => {
      formData.value.education.push({ university: '', degree: '', field_of_study: '', graduation_year: '' })
    }

    const removeEducation = (index) => {
      formData.value.education.splice(index, 1)
    }

    const addTable5Entry = () => {
      formData.value.table5_entries.push({ entry_type: '', description: '', score: 0 })
    }

    const removeTable5Entry = (index) => {
      formData.value.table5_entries.splice(index, 1)
    }

    const handleFileUpload = (event) => {
      uploadedFiles.value = [...uploadedFiles.value, ...Array.from(event.target.files)]
    }

    const removeFile = (index) => {
      uploadedFiles.value.splice(index, 1)
    }

    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    const uploadDocuments = async () => {
      const uploadedDocumentIds = []
      for (const file of uploadedFiles.value) {
        // Eğer dosya zaten yüklenmişse (düzenleme modunda), ID'sini ekle
        if (file.id) {
          uploadedDocumentIds.push(file.id)
          continue
        }
        
        const docFormData = new FormData()
        docFormData.append('file', file)
        docFormData.append('name', file.name) // İsteğe bağlı: dosya adı
        
        try {
          const response = await apiClient.post('/api/applications/documents/upload/', docFormData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
          uploadedDocumentIds.push(response.data.id)
        } catch (error) {
          console.error(`${file.name} yüklenirken hata:`, error)
          // Hata yönetimi - kullanıcıya bilgi verilebilir
          throw new Error('Belge yükleme sırasında hata oluştu.')
        }
      }
      return uploadedDocumentIds
    }

    const handleSubmit = async () => {
      isLoading.value = true
      try {
        // 1. Belgeleri yükle
        const documentIds = await uploadDocuments()
        
        // 2. Başvuru verilerini hazırla
        const submissionData = {
          ...formData.value,
          documents: documentIds,
          candidate: formData.value.candidate.id // Sadece candidate ID'sini gönder
        }
        
        // 3. Başvuruyu gönder
        const method = isEditing.value ? 'put' : 'post'
        const url = isEditing.value 
          ? `/api/applications/applications/${route.params.id}/`
          : '/api/applications/applications/'
          
        await apiClient[method](url, submissionData)
        
        router.push('/candidate/applications')
      } catch (error) {
        console.error('Başvuru gönderilirken hata:', error)
        // Kullanıcıya hata mesajı göster
      } finally {
        isLoading.value = false
      }
    }

    return {
      isLoading,
      isEditing,
      currentStep,
      steps,
      formData,
      announcement,
      uploadedFiles,
      nextStep,
      prevStep,
      goToStep,
      addEducation,
      removeEducation,
      addTable5Entry,
      removeTable5Entry,
      handleFileUpload,
      removeFile,
      formatFileSize,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.application-form-container {
  max-width: 1000px;
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

.form-wrapper {
  background: white;
  border-radius: var(--border-radius-lg);
  padding: 30px;
}

.stepper {
  display: flex;
  justify-content: space-between;
  margin-bottom: 32px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-color);
}

.step {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.3s ease;
}

.step.active,
.step.completed {
  opacity: 1;
}

.step-number {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: var(--border-color);
  color: var(--gray-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  transition: all 0.3s ease;
}

.step.active .step-number {
  background-color: var(--primary-color);
  color: white;
}

.step.completed .step-number {
  background-color: var(--dark-color);
  color: white;
}

.step-label {
  font-weight: 500;
  color: var(--dark-color);
}

.form-step {
  animation: fade-in 0.5s ease;
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

h2 {
  font-size: 1.4rem;
  color: var(--dark-color);
  margin-bottom: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

label {
  font-weight: 500;
  color: var(--dark-color);
}

input[type="text"],
input[type="email"],
input[type="tel"],
input[type="number"],
input[type="file"],
select,
textarea {
  padding: 10px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  font-size: 1rem;
  transition: all 0.3s ease;
}

input:focus,
select:focus,
textarea:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(29, 131, 72, 0.1);
  outline: none;
}

input:disabled {
  background-color: var(--border-color);
  cursor: not-allowed;
}

.education-item,
.table5-item {
  background: var(--light-color);
  padding: 16px;
  border-radius: var(--border-radius-sm);
  margin-bottom: 16px;
  border: 1px solid var(--border-color);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.item-header h3 {
  font-size: 1.1rem;
  margin: 0;
}

.required-docs-list {
  list-style: disc;
  padding-left: 20px;
  margin: 0;
}

.uploaded-files-list {
  margin-top: 16px;
}

.uploaded-files-list h4 {
  font-size: 1rem;
  margin-bottom: 8px;
}

.uploaded-files-list ul {
  list-style: none;
  padding: 0;
}

.uploaded-files-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px dashed var(--border-color);
}

.preview-step h3 {
  font-size: 1.2rem;
  color: var(--primary-color);
  margin-top: 24px;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-color);
}

.preview-section {
  margin-bottom: 24px;
}

.preview-item {
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px dashed var(--border-color);
}
.preview-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.preview-section p {
  margin: 4px 0;
}

.form-navigation {
  display: flex;
  justify-content: space-between;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--border-color);
}

.btn {
  padding: 12px 24px;
  border-radius: var(--border-radius-sm);
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
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

.btn-outline {
  background: none;
  border: 1px solid var(--primary-color);
  color: var(--primary-color);
}

.btn-outline:hover {
  background: var(--border-color);
}

.btn-success {
  background: #10B981; /* Yeşil tonu */
  color: white;
  border: none;
}

.btn-success:hover {
  background: #059669;
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-icon {
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
  color: var(--dark-color);
  transition: all 0.2s;
}

.btn-icon:hover {
  background: rgba(0, 0, 0, 0.1);
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .application-form-container {
    padding: 16px;
  }

  .form-wrapper {
    padding: 20px;
  }

  .stepper {
    flex-wrap: wrap;
    gap: 16px;
  }

  .step-label {
    display: none; /* Mobilde sadece numaraları göster */
  }
}
</style>
