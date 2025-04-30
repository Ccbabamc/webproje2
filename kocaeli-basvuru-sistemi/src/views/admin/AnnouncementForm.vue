<template>
  <div class="announcement-form-container">
    <h2>{{ isEditing ? 'İlan Düzenle' : 'Yeni İlan Ekle' }}</h2>
    
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="title">İlan Başlığı</label>
        <input
          type="text"
          id="title"
          v-model="form.title"
          :class="{ 'is-invalid': errors.title }"
        />
        <div v-if="errors.title" class="invalid-feedback">
          {{ errors.title }}
        </div>
      </div>

      <div class="form-group">
        <label for="description">Açıklama</label>
        <textarea
          id="description"
          v-model="form.description"
          :class="{ 'is-invalid': errors.description }"
        ></textarea>
        <div v-if="errors.description" class="invalid-feedback">
          {{ errors.description }}
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="faculty">Fakülte</label>
          <select
            id="faculty"
            v-model="selectedFaculty"
            @change="handleFacultyChange"
          >
            <option value="">Fakülte Seçin</option>
            <option
              v-for="faculty in faculties"
              :key="faculty.id"
              :value="faculty.id"
            >
              {{ faculty.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="department">Bölüm</label>
          <select
            id="department"
            v-model="form.department"
            :disabled="!selectedFaculty"
            :class="{ 'is-invalid': errors.department }"
          >
            <option value="">Bölüm Seçin</option>
            <option
              v-for="dept in filteredDepartments"
              :key="dept.id"
              :value="dept.id"
            >
              {{ dept.name }}
            </option>
          </select>
          <div v-if="errors.department" class="invalid-feedback">
            {{ errors.department }}
          </div>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="start_date">Başlangıç Tarihi</label>
          <input
            type="date"
            id="start_date"
            v-model="form.start_date"
            :min="today"
            :class="{ 'is-invalid': errors.start_date }"
          />
          <div v-if="errors.start_date" class="invalid-feedback">
            {{ errors.start_date }}
          </div>
        </div>

        <div class="form-group">
          <label for="end_date">Bitiş Tarihi</label>
          <input
            type="date"
            id="end_date"
            v-model="form.end_date"
            :min="form.start_date || today"
            :class="{ 'is-invalid': errors.end_date }"
          />
          <div v-if="errors.end_date" class="invalid-feedback">
            {{ errors.end_date }}
          </div>
        </div>
      </div>

      <div class="form-group">
        <label>Gerekli Belgeler</label>
        <div
          v-for="(doc, index) in form.required_documents"
          :key="index"
          class="document-item"
        >
          <input
            type="text"
            v-model="form.required_documents[index]"
          />
          <button
            type="button"
            class="remove-btn"
            @click="removeDocument(index)"
          >
            Kaldır
          </button>
        </div>
        <button
          type="button"
          class="add-btn"
          @click="addDocument"
        >
          Belge Ekle
        </button>
      </div>

      <div class="form-group">
        <label>Değerlendirme Kriterleri</label>
        <div
          v-for="(criterion, index) in form.criteria"
          :key="index"
          class="criterion-item"
        >
          <div class="criterion-row">
            <input
              type="text"
              v-model="criterion.name"
              placeholder="Kriter Adı"
              :class="{ 'is-invalid': errors[`criteria[${index}].name`] }"
            />
            <input
              type="number"
              v-model.number="criterion.min_score"
              placeholder="Min Puan"
              :class="{ 'is-invalid': errors[`criteria[${index}].min_score`] }"
            />
            <input
              type="number"
              v-model.number="criterion.max_score"
              placeholder="Max Puan"
              :class="{ 'is-invalid': errors[`criteria[${index}].max_score`] }"
            />
            <button
              type="button"
              class="remove-btn"
              @click="removeCriterion(index)"
            >
              Kaldır
            </button>
          </div>
          <div v-if="errors[`criteria[${index}].name`]" class="invalid-feedback">
            {{ errors[`criteria[${index}].name`] }}
          </div>
          <div v-if="errors[`criteria[${index}].min_score`]" class="invalid-feedback">
            {{ errors[`criteria[${index}].min_score`] }}
          </div>
          <div v-if="errors[`criteria[${index}].max_score`]" class="invalid-feedback">
            {{ errors[`criteria[${index}].max_score`] }}
          </div>
        </div>
        <button
          type="button"
          class="add-btn"
          @click="addCriterion"
        >
          Kriter Ekle
        </button>
      </div>

      <div class="form-group">
        <label for="status">Durum</label>
        <select id="status" v-model="form.status">
          <option value="active">Aktif</option>
          <option value="inactive">Pasif</option>
        </select>
      </div>

      <div v-if="generalError" class="alert error">
        {{ generalError }}
      </div>

      <button type="submit" :disabled="isLoading">
        {{ isLoading ? 'Kaydediliyor...' : 'Kaydet' }}
      </button>
    </form>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import apiClient from '../../api/axios'

export default {
  name: 'AnnouncementForm',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const isLoading = ref(false)
    const isEditing = computed(() => !!route.params.id)
    const errors = ref({})
    const generalError = ref('')
    const faculties = ref([])
    const departments = ref([])
    const selectedFaculty = ref('')

const form = ref({
  title: '',
  description: '',
  department: '',
  start_date: '',
  end_date: '',
  required_documents: [],
  criteria: [],
  status: 'inactive'
})

    const today = computed(() => {
      return new Date().toISOString().split('T')[0]
    })

    const filteredDepartments = computed(() => {
      return departments.value
    })

onMounted(async () => {
  try {
    await loadFaculties()

    if (isEditing.value) {
      await loadAnnouncement()
    }
  } catch (error) {
    console.error('Form yüklenirken hata:', error)
  }
})

const loadFaculties = async () => {
  try {
    const response = await apiClient.get('/api/ilan/fakulteler/')
    faculties.value = response.data
  } catch (error) {
    console.error('Fakülteler yüklenirken hata:', error)
    faculties.value = []
  }
}

const loadDepartments = async () => {
  if (!selectedFaculty.value) {
    departments.value = [];
    return;
  }
  
  try {
    const response = await apiClient.get('/api/ilan/bolumler/', {
      params: {
        faculty: selectedFaculty.value
      }
    });
    departments.value = response.data;
  } catch (error) {
    console.error('Bölümler yüklenirken hata:', error)
    departments.value = []
  }
}

const handleFacultyChange = async () => {
  form.value.department = ''  // Reset department selection
  departments.value = []      // Clear departments list
  if (selectedFaculty.value) {
    await loadDepartments()
  }
}

    const loadAnnouncement = async () => {
      try {
        const response = await apiClient.get(`/api/announcements/${route.params.id}/`)
        const announcement = response.data
        
        form.value = {
          ...announcement,
          required_documents: Array.isArray(announcement.required_documents) ? announcement.required_documents : [],
          criteria: Array.isArray(announcement.criteria) ? announcement.criteria : []
        };

        const relatedDepartment = departments.value.find(
          dept => dept.id === announcement.department
        );

        if (relatedDepartment) {
          selectedFaculty.value = relatedDepartment.faculty;
        } else if (announcement.department) {
           console.warn(`İlanın bölümü (${announcement.department}) yüklenen bölümler listesinde bulunamadı.`);
        }
        
      } catch (error) {
        console.error('İlan yüklenirken hata:', error);
      }
    }

    const validate = () => {
      errors.value = {}
      generalError.value = ''
      let isValid = true

      if (!form.value.title?.trim()) {
        errors.value.title = 'İlan başlığı zorunludur'
        isValid = false
      }


      if (!form.value.department) {
        errors.value.department = 'Bölüm seçimi zorunludur'
        isValid = false
      }

      if (!form.value.start_date) {
        errors.value.start_date = 'Başlangıç tarihi zorunludur'
        isValid = false
      }

      if (!form.value.end_date) {
        errors.value.end_date = 'Bitiş tarihi zorunludur'
        isValid = false
      }
      
      if (!form.value.description?.trim()) {
        errors.value.description = 'İlan açıklaması zorunludur'
        isValid = false
      }

      form.value.criteria.forEach((criterion, index) => {
        let criterionPrefix = `criteria[${index}]`;
        if (!criterion.name?.trim()) {
          errors.value[`${criterionPrefix}.name`] = `Kriter #${index + 1} adı zorunludur`
          isValid = false
        }
        if (criterion.min_score == null || criterion.min_score < 0) {
           errors.value[`${criterionPrefix}.min_score`] = `Kriter #${index + 1} min puanı geçerli değil`
           isValid = false
        }
         if (criterion.max_score == null || criterion.max_score < 0) {
           errors.value[`${criterionPrefix}.max_score`] = `Kriter #${index + 1} max puanı geçerli değil`
           isValid = false
        }
        if (criterion.min_score != null && criterion.max_score != null && criterion.min_score > criterion.max_score) {
          errors.value[`${criterionPrefix}.scores`] = `Kriter #${index + 1} min puanı max puanından büyük olamaz`
          isValid = false
        }
      });

      if (form.value.start_date && form.value.end_date && 
          new Date(form.value.start_date) >= new Date(form.value.end_date)) {
        errors.value.end_date = 'Bitiş tarihi başlangıç tarihinden sonra olmalıdır'
        isValid = false
      }

      return isValid
    }

    const handleSubmit = async () => {
      if (!validate()) return

      isLoading.value = true
      try {
        const method = isEditing.value ? 'put' : 'post'
        const url = isEditing.value 
          ? `/api/announcements/${route.params.id}/` // Assuming this endpoint uses the FrontendIlanCreateSerializer for PUT as well
          : '/api/announcements/' // Assuming this endpoint uses the FrontendIlanCreateSerializer for POST

// Construct payload matching the backend's FrontendIlanCreateSerializer expectations
const payload = {
  title: form.value.title,
  description: form.value.description,
  bolum: form.value.department, // Send department ID as 'bolum'
  deadline: form.value.end_date, // Send end_date as 'deadline'
  status: form.value.status
  // start_date is not sent
  // required_documents are not sent to this endpoint
  // criteria are not sent to this endpoint
}
        console.log("Sending payload:", payload); // Debugging: Log the payload before sending

        await apiClient[method](url, payload)
        router.push('/admin/announcements')
      } catch (error) {
        console.error('İlan kaydedilirken hata:', error)
        if (error.response) {
          if (error.response.status === 400 && error.response.data) {
            // Handle validation errors
            errors.value = error.response.data;
            generalError.value = 'Lütfen formdaki hataları düzeltin.';
          } else if (error.response.status === 401) {
            generalError.value = 'Oturum süreniz doldu. Lütfen tekrar giriş yapın.';
          } else if (error.response.status === 403) {
            generalError.value = 'Bu işlemi yapmaya yetkiniz yok.';
          } else if (error.response.status === 404) {
            generalError.value = 'İlan bulunamadı.';
          } else {
            generalError.value = 'İlan kaydedilirken beklenmedik bir hata oluştu. Lütfen tekrar deneyin veya sistem yöneticisiyle iletişime geçin.';
          }
        } else if (error.request) {
          generalError.value = 'Sunucuya ulaşılamıyor. Lütfen internet bağlantınızı kontrol edin.';
        } else {
          generalError.value = 'İşlem sırasında bir hata oluştu. Lütfen tekrar deneyin.';
        }
      } finally {
        isLoading.value = false
      }
    }


    const addDocument = () => {
      form.value.required_documents.push('')
    }

    const removeDocument = (index) => {
      form.value.required_documents.splice(index, 1)
    }

    const addCriterion = () => {
      form.value.criteria.push({
        name: '',
        min_score: 0,
        max_score: 100
      })
    }

    const removeCriterion = (index) => {
      form.value.criteria.splice(index, 1)
    }

    return {
      form,
      errors,
      isLoading,
      isEditing,
      faculties,
      selectedFaculty,
      filteredDepartments,
      today,
      generalError,
      handleSubmit,
      handleFacultyChange,
      addDocument,
      removeDocument,
      addCriterion,
      removeCriterion
    }
  }
}
</script>

<style scoped>
.announcement-form-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

h2 {
  color: #2e7d32;
  margin-bottom: 2rem;
  text-align: center;
  font-size: 1.8rem;
  font-weight: 600;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-row {
  display: flex;
  gap: 1rem;
}

.form-row .form-group {
  flex: 1;
}

label {
  font-weight: 500;
  color: #2c3e50;
}

input, textarea, select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input:focus, textarea:focus, select:focus {
  outline: none;
  border-color: #3498db;
}

.is-invalid {
  border-color: #e74c3c;
}

.invalid-feedback {
  color: #e74c3c;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.document-item, .criterion-item {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  margin-bottom: 0.5rem;
}

.criterion-row {
  display: flex;
  gap: 0.5rem;
  width: 100%;
}

.criterion-row input {
  flex: 1;
}

.add-btn, .remove-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.add-btn {
  background-color: #388e3c;
  color: white;
  border: 1px solid #2e7d32;
}

.add-btn:hover {
  background-color: #2e7d32;
}

.remove-btn {
  background-color: #d32f2f;
  color: white;
  border: 1px solid #b71c1c;
}

.remove-btn:hover {
  background-color: #b71c1c;
}

button[type="submit"] {
  background-color: #4caf50;
  color: white;
  padding: 1rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

button[type="submit"]:hover {
  background-color: #43a047;
}

button[type="submit"]:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.alert.error {
  background-color: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}
</style>
