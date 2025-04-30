<template>
  <div class="jury-assignment-container">
    <h1>Jüri Atamaları</h1>
    
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Başvurular yükleniyor...</p>
    </div>
    
    <div v-else>
      <!-- Filtreler -->
      <div class="filters-panel">
        <div class="search-box">
          <input 
            type="text" 
            v-model="filters.search" 
            placeholder="Aday adı, ilan başlığı, fakülte veya bölüm ara..."
            @input="debounceSearch"
          >
        </div>
        
        <div class="filter-options">
          <div class="filter-group">
            <label for="facultyFilter">Fakülte:</label>
            <select id="facultyFilter" v-model="filters.faculty" @change="onFacultyChange">
              <option value="">Tümü</option>
              <option v-for="faculty in faculties" :key="faculty.id" :value="faculty.id">{{ faculty.name }}</option>
            </select>
          </div>
          
          <div class="filter-group">
            <label for="departmentFilter">Bölüm:</label>
            <select id="departmentFilter" v-model="filters.department">
              <option value="">Tümü</option>
              <option v-for="dept in filteredDepartments" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
            </select>
          </div>
          
          <div class="filter-group">
            <label for="statusFilter">Jüri Durumu:</label>
            <select id="statusFilter" v-model="filters.jury_status">
              <option value="">Tümü</option>
              <option value="pending">Jüri Atanmamış</option>
              <option value="assigned">Jüri Atanmış</option>
            </select>
          </div>
          
          <button class="btn btn-outline" @click="resetFilters">Filtreleri Temizle</button>
        </div>
      </div>
      
      <!-- Tablo Görünümü -->
      <div class="table-container">
        <table class="applications-table">
          <thead>
            <tr>
              <th>Aday</th>
              <th>İlan</th>
              <th>Fakülte/Bölüm</th>
              <th>Başvuru Tarihi</th>
              <th>Jüri Durumu</th>
              <th>İşlemler</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="app in filteredApplications" :key="app.id">
              <td>{{ app.first_name }} {{ app.last_name }}</td>
              <td>{{ getAnnouncementTitle(app.announcement) }}</td>
              <td>
                {{ getAnnouncementFaculty(app.announcement) }} / 
                {{ getAnnouncementDepartment(app.announcement) }}
              </td>
              <td>{{ formatDate(app.created_at) }}</td>
              <td>
                <span 
                  class="status-badge" 
                  :class="app.jury_assigned ? 'assigned' : 'pending'"
                >
                  {{ app.jury_assigned ? 'Jüri Atanmış' : 'Jüri Atanmamış' }}
                </span>
              </td>
              <td>
                <button 
                  class="btn-sm btn-primary" 
                  @click="openAssignModal(app)"
                >
                  {{ app.jury_assigned ? 'Jüriyi Düzenle' : 'Jüri Ata' }}
                </button>
                <button 
                  class="btn-sm btn-outline" 
                  @click="viewApplication(app.id)"
                >
                  Detaylar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        
        <div v-if="filteredApplications.length === 0" class="empty-state">
          <p>Belirtilen kriterlere uygun başvuru bulunamadı.</p>
        </div>
      </div>
      
      <!-- Pagination -->
      <div class="pagination" v-if="totalPages > 1">
        <button 
          class="btn-page" 
          :disabled="currentPage === 1"
          @click="changePage(currentPage - 1)"
        >
          &laquo; Önceki
        </button>
        
        <button 
          v-for="page in paginationItems" 
          :key="page"
          class="btn-page"
          :class="{ active: page === currentPage }"
          @click="changePage(page)"
        >
          {{ page }}
        </button>
        
        <button 
          class="btn-page" 
          :disabled="currentPage === totalPages"
          @click="changePage(currentPage + 1)"
        >
          Sonraki &raquo;
        </button>
      </div>
    </div>
    
    <!-- Jüri Atama Modal -->
    <div class="modal-overlay" v-if="showAssignModal" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Jüri Atama</h2>
          <button class="btn-close" @click="closeModal">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="application-info">
            <h3>Başvuru Bilgileri</h3>
            <div class="info-row">
              <div class="info-item">
                <span class="info-label">Aday:</span>
                <span class="info-value">{{ selectedApplication.first_name }} {{ selectedApplication.last_name }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">İlan:</span>
                <span class="info-value">{{ getAnnouncementTitle(selectedApplication.announcement) }}</span>
              </div>
            </div>
          </div>
          
          <div class="jury-form">
            <h3>Jüri Üyeleri</h3>
            <p class="form-info">Başvuruyu değerlendirecek jüri üyelerini ekleyin. En az 3 jüri üyesi belirtilmelidir.</p>
            
            <div v-for="(member, index) in juryMembers" :key="index" class="jury-member">
              <div class="member-header">
                <h4>Jüri Üyesi {{ index + 1 }}</h4>
                <button 
                  v-if="index > 0" 
                  type="button" 
                  class="btn-remove" 
                  @click="removeJuryMember(index)"
                >
                  Kaldır
                </button>
              </div>
              
              <div class="form-row">
                <div class="form-group">
                  <label :for="`name_${index}`">Ad Soyad *</label>
                  <input 
                    :id="`name_${index}`" 
                    type="text" 
                    v-model="member.name"
                    required
                  >
                </div>
                
                <div class="form-group">
                  <label :for="`title_${index}`">Akademik Ünvan *</label>
                  <select 
                    :id="`title_${index}`" 
                    v-model="member.title"
                    required
                  >
                    <option value="">Seçiniz</option>
                    <option value="prof">Prof. Dr.</option>
                    <option value="doc">Doç. Dr.</option>
                    <option value="dr">Dr. Öğr. Üyesi</option>
                  </select>
                </div>
              </div>
              
              <div class="form-row">
                <div class="form-group">
                  <label :for="`institution_${index}`">Kurum *</label>
                  <input 
                    :id="`institution_${index}`" 
                    type="text" 
                    v-model="member.institution"
                    required
                  >
                </div>
                
                <div class="form-group">
                  <label :for="`field_${index}`">Uzmanlık Alanı</label>
                  <input 
                    :id="`field_${index}`" 
                    type="text" 
                    v-model="member.field"
                  >
                </div>
              </div>
              
              <div class="form-row">
                <div class="form-group">
                  <label :for="`email_${index}`">E-posta *</label>
                  <input 
                    :id="`email_${index}`" 
                    type="email" 
                    v-model="member.email"
                    required
                  >
                </div>
                
                <div class="form-group">
                  <label :for="`phone_${index}`">Telefon</label>
                  <input 
                    :id="`phone_${index}`" 
                    type="text" 
                    v-model="member.phone"
                  >
                </div>
              </div>
              
              <div class="form-group">
                <label :for="`notes_${index}`">Notlar</label>
                <textarea 
                  :id="`notes_${index}`" 
                  v-model="member.notes"
                  rows="2"
                ></textarea>
              </div>
            </div>
            
            <div class="jury-actions">
              <button type="button" class="btn btn-secondary" @click="addJuryMember">
                + Jüri Üyesi Ekle
              </button>
            </div>
            
            <div class="form-group">
              <label for="meeting_date">Değerlendirme Tarihi</label>
              <input 
                id="meeting_date" 
                type="date" 
                v-model="juryData.meeting_date"
              >
            </div>
            
            <div class="form-group">
              <label for="jury_notes">Ekstra Notlar</label>
              <textarea 
                id="jury_notes" 
                v-model="juryData.notes"
                rows="3"
                placeholder="Jüri ataması ile ilgili ekstra notlar..."
              ></textarea>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="closeModal">İptal</button>
          <button 
            class="btn btn-primary" 
            @click="saveJuryAssignment"
            :disabled="saving || juryMembers.length < 3 || !validateJuryForm()"
          >
            <span v-if="saving" class="spinner-sm"></span>
            {{ selectedApplication.jury_assigned ? 'Jüriyi Güncelle' : 'Jüriyi Ata' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../../api/axios'

export default {
  name: 'JuryAssignment',
  setup() {
    const router = useRouter()
    
    // State variables
    const loading = ref(true)
    const saving = ref(false)
    const applications = ref([])
    const faculties = ref([])
    const departments = ref([])
    const announcements = ref({}) // Id bazlı önbellek
    const showAssignModal = ref(false)
    const selectedApplication = ref({})
    
    // Pagination
    const currentPage = ref(1)
    const pageSize = ref(10)
    const totalPages = ref(1)
    const totalItems = ref(0)
    
    // Filters
    const filters = reactive({
      search: '',
      faculty: '',
      department: '',
      jury_status: ''
    })
    
    // Jüri form data
    const juryMembers = ref([])
    const juryData = reactive({
      meeting_date: '',
      notes: ''
    })
    
    // Fetch data
    const fetchApplications = async () => {
      loading.value = true
      try {
        const response = await apiClient.get('/api/applications/applications/', {
          params: {
            status: 'approved', // Sadece onaylanmış başvurular
            page: currentPage.value,
            page_size: pageSize.value,
            search: filters.search,
            faculty: filters.faculty,
            department: filters.department,
            jury_status: filters.jury_status
          }
        })
        
        applications.value = response.data.results || []
        totalItems.value = response.data.count || 0
        totalPages.value = Math.ceil(totalItems.value / pageSize.value)
        
        // Announcement bilgilerini ön belleğe al
        for (const app of applications.value) {
          if (app.announcement && !announcements.value[app.announcement]) {
            await fetchAnnouncementDetails(app.announcement)
          }
        }
      } catch (error) {
        console.error('Başvurular yüklenirken hata oluştu:', error)
      } finally {
        loading.value = false
      }
    }
    
    const fetchFaculties = async () => {
      try {
        const response = await apiClient.get('/api/announcements/faculties/')
        faculties.value = response.data || []
      } catch (error) {
        console.error('Fakülteler yüklenirken hata oluştu:', error)
      }
    }
    
    const fetchDepartments = async () => {
      try {
        const response = await apiClient.get('/api/announcements/departments/')
        departments.value = response.data || []
      } catch (error) {
        console.error('Bölümler yüklenirken hata oluştu:', error)
      }
    }
    
    const fetchAnnouncementDetails = async (announcementId) => {
      try {
        const response = await apiClient.get(`/api/announcements/${announcementId}/`)
        announcements.value[announcementId] = response.data
      } catch (error) {
        console.error(`İlan (${announcementId}) bilgileri yüklenirken hata oluştu:`, error)
      }
    }
    
    const fetchJuryMembers = async (applicationId) => {
      try {
        const response = await apiClient.get(`/api/jury/members/`, {
          params: { application_id: applicationId }
        })
        
        if (response.data && response.data.length > 0) {
          juryMembers.value = response.data.map(member => ({
            id: member.id,
            name: member.name,
            title: member.title,
            institution: member.institution,
            field: member.field || '',
            email: member.email,
            phone: member.phone || '',
            notes: member.notes || ''
          }))
          
          // Jüri toplantı bilgilerini getir
          const juryResponse = await apiClient.get(`/api/jury/assignments/`, {
            params: { application_id: applicationId }
          })
          
          if (juryResponse.data && juryResponse.data.length > 0) {
            juryData.meeting_date = juryResponse.data[0].meeting_date || ''
            juryData.notes = juryResponse.data[0].notes || ''
          }
        } else {
          resetJuryForm()
        }
      } catch (error) {
        console.error('Jüri üyeleri yüklenirken hata oluştu:', error)
        resetJuryForm()
      }
    }
    
    // Actions
    const onFacultyChange = () => {
      filters.department = '' // Fakülte değiştiğinde bölüm filtresini sıfırla
    }
    
    const resetFilters = () => {
      filters.search = ''
      filters.faculty = ''
      filters.department = ''
      filters.jury_status = ''
      currentPage.value = 1
      fetchApplications()
    }
    
    const changePage = (page) => {
      currentPage.value = page
      fetchApplications()
    }
    
    // Debounce search
    let searchTimeout = null
    const debounceSearch = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        currentPage.value = 1 // Arama yapıldığında ilk sayfaya dön
        fetchApplications()
      }, 500)
    }
    
    // View application details
    const viewApplication = (applicationId) => {
      router.push(`/admin/applications/${applicationId}`)
    }
    
    // Jury assignment modal
    const openAssignModal = async (application) => {
      selectedApplication.value = application
      showAssignModal.value = true
      
      // Eğer daha önce jüri atanmışsa, mevcut jüri üyelerini getir
      if (application.jury_assigned) {
        await fetchJuryMembers(application.id)
      } else {
        resetJuryForm()
      }
    }
    
    const closeModal = () => {
      showAssignModal.value = false
      selectedApplication.value = {}
      resetJuryForm()
    }
    
    const resetJuryForm = () => {
      // Varsayılan olarak 3 boş jüri üyesi başlat
      juryMembers.value = [
        createEmptyJuryMember(),
        createEmptyJuryMember(),
        createEmptyJuryMember()
      ]
      juryData.meeting_date = ''
      juryData.notes = ''
    }
    
    const createEmptyJuryMember = () => {
      return {
        name: '',
        title: '',
        institution: '',
        field: '',
        email: '',
        phone: '',
        notes: ''
      }
    }
    
    const addJuryMember = () => {
      juryMembers.value.push(createEmptyJuryMember())
    }
    
    const removeJuryMember = (index) => {
      juryMembers.value.splice(index, 1)
    }
    
    const validateJuryForm = () => {
      // Minimum 3 jüri üyesi ve zorunlu alanların kontrolü
      if (juryMembers.value.length < 3) return false
      
      for (const member of juryMembers.value) {
        if (!member.name.trim() || !member.title || !member.institution.trim() || !member.email.trim()) {
          return false
        }
      }
      
      return true
    }
    
    const saveJuryAssignment = async () => {
      if (!validateJuryForm()) {
        alert('Lütfen tüm zorunlu alanları doldurun.')
        return
      }
      
      saving.value = true
      
      try {
        // Jüri atama kaydı oluştur veya güncelle
        const assignmentData = {
          application: selectedApplication.value.id,
          meeting_date: juryData.meeting_date,
          notes: juryData.notes
        }
        
        // API isteği
        let assignmentResponse
        if (selectedApplication.value.jury_assigned) {
          // Güncelleme
          assignmentResponse = await apiClient.put(
            `/api/jury/assignments/${selectedApplication.value.id}/`,
            assignmentData
          )
        } else {
          // Yeni oluşturma
          assignmentResponse = await apiClient.post('/api/jury/assignments/', assignmentData)
        }
        
        // Jüri üyelerini kaydet
        for (const member of juryMembers.value) {
          const memberData = {
            ...member,
            application: selectedApplication.value.id
          }
          
          if (member.id) {
            // Mevcut üyeyi güncelle
            await apiClient.put(`/api/jury/members/${member.id}/`, memberData)
          } else {
            // Yeni üye ekle
            await apiClient.post('/api/jury/members/', memberData)
          }
        }
        
        // Başarılı ise listeyi güncelle
        fetchApplications()
        
        // Modal kapat
        closeModal()
        
        alert('Jüri ataması başarıyla kaydedildi.')
      } catch (error) {
        console.error('Jüri ataması yapılırken hata oluştu:', error)
        alert('Jüri ataması yapılırken bir hata oluştu. Lütfen daha sonra tekrar deneyin.')
      } finally {
        saving.value = false
      }
    }
    
    // Helper functions
    const getAnnouncementTitle = (announcementId) => {
      return announcements.value[announcementId]?.title || '-'
    }
    
    const getAnnouncementFaculty = (announcementId) => {
      return announcements.value[announcementId]?.faculty?.name || '-'
    }
    
    const getAnnouncementDepartment = (announcementId) => {
      return announcements.value[announcementId]?.department?.name || '-'
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return '-'
      const date = new Date(dateString)
      return date.toLocaleDateString('tr-TR')
    }
    
    // Computed properties
    const filteredDepartments = computed(() => {
      if (!filters.faculty) return departments.value
      return departments.value.filter(dept => dept.faculty === parseInt(filters.faculty))
    })
    
    const filteredApplications = computed(() => {
      return applications.value
    })
    
    const paginationItems = computed(() => {
      const items = []
      const maxVisiblePages = 5
      
      if (totalPages.value <= maxVisiblePages) {
        // Tüm sayfaları göster
        for (let i = 1; i <= totalPages.value; i++) {
          items.push(i)
        }
      } else {
        // Maksimum 5 sayfa göster
        let startPage = Math.max(1, currentPage.value - 2)
        let endPage = Math.min(totalPages.value, startPage + maxVisiblePages - 1)
        
        // Başlangıç ve bitiş sayfalarını ayarla
        if (endPage - startPage < maxVisiblePages - 1) {
          startPage = Math.max(1, endPage - maxVisiblePages + 1)
        }
        
        for (let i = startPage; i <= endPage; i++) {
          items.push(i)
        }
      }
      
      return items
    })
    
    // Lifecycle hooks
    onMounted(async () => {
      await Promise.all([
        fetchFaculties(),
        fetchDepartments()
      ])
      
      fetchApplications()
    })
    
    return {
      loading,
      saving,
      applications,
      faculties,
      filters,
      currentPage,
      totalPages,
      showAssignModal,
      selectedApplication,
      juryMembers,
      juryData,
      filteredApplications,
      filteredDepartments,
      paginationItems,
      onFacultyChange,
      resetFilters,
      debounceSearch,
      changePage,
      viewApplication,
      openAssignModal,
      closeModal,
      addJuryMember,
      removeJuryMember,
      validateJuryForm,
      saveJuryAssignment,
      getAnnouncementTitle,
      getAnnouncementFaculty,
      getAnnouncementDepartment,
      formatDate
    }
  }
}
</script>

<style scoped>
.jury-assignment-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  color: #0056b3;
  margin-bottom: 25px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px 0;
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

/* Filters */
.filters-panel {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  padding: 20px;
  margin-bottom: 25px;
}

.search-box {
  margin-bottom: 15px;
}

.search-box input {
  width: 100%;
  padding: 10px 15px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 1rem;
}

.filter-options {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  align-items: flex-end;
}

.filter-group {
  flex: 1;
  min-width: 200px;
}

.filter-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #495057;
}

.filter-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 1rem;
}

/* Table */
.table-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  padding: 20px;
  margin-bottom: 25px;
  overflow-x: auto;
}

.applications-table {
  width: 100%;
  border-collapse: collapse;
}

.applications-table th,
.applications-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.applications-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #495057;
}

.applications-table tr:hover {
  background-color: #f8f9fa;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.85rem;
}

.status-badge.pending {
  background-color: #fff3cd;
  color: #856404;
}

.status-badge.assigned {
  background-color: #d4edda;
  color: #155724;
}

.empty-state {
  padding: 30px;
  text-align: center;
  color: #6c757d;
  font-style: italic;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  gap: 5px;
  margin-top: 25px;
}

.btn-page {
  padding: 8px 12px;
  border: 1px solid #dee2e6;
  background-color: white;
  color: #0056b3;
  cursor: pointer;
  border-radius: 4px;
}

.btn-page.active {
  background-color: #0056b3;
  color: white;
  border-color: #0056b3;
}

.btn-page:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #dee2e6;
}

.modal-header h2 {
  margin: 0;
  color: #0056b3;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6c757d;
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  padding: 15px 20px;
  border-top: 1px solid #dee2e6;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* Application Info in Modal */
.application-info {
  background-color: #f8f9fa;
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 20px;
}

.application-info h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #495057;
  font-size: 1.1rem;
}

.info-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.info-item {
  flex: 1;
  min-width: 200px;
}

.info-label {
  font-weight: 500;
  color: #666;
  margin-right: 5px;
}

/* Jury Form */
.jury-form h3 {
  margin-top: 0;
  margin-bottom: 5px;
  color: #0056b3;
}

.form-info {
  color: #6c757d;
  margin-bottom: 20px;
}

.jury-member {
  background-color: #f8f9fa;
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 20px;
}

.member-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.member-header h4 {
  margin: 0;
  color: #495057;
}

.btn-remove {
  background-color: #f8d7da;
  color: #dc3545;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.form-row {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
}

.form-group {
  flex: 1;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #495057;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 1rem;
}

.jury-actions {
  margin-bottom: 20px;
}

/* Buttons */
.btn {
  padding: 10px 20px;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-primary {
  background-color: #0056b3;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-outline {
  background-color: transparent;
  color: #0056b3;
  border: 1px solid #0056b3;
}

.btn-sm {
  padding: 5px 10px;
  font-size: 0.875rem;
  margin-right: 5px;
}

.btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
  .filter-options {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-group {
    width: 100%;
  }
  
  .form-row {
    flex-direction: column;
  }
  
  .info-row {
    flex-direction: column;
  }
  
  .btn-sm {
    margin-bottom: 5px;
  }
}
</style>