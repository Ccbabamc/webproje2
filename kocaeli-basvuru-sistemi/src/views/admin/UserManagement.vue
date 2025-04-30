<template>
  <div class="user-management">
    <Toast />
    <ConfirmDialog />

    <!-- Page Header -->
    <div class="page-header">
      <h1>Kullanıcı Yönetimi</h1>
      <Button label="Yeni Kullanıcı Ekle" icon="pi pi-plus" @click="openNewUserDialog" />
    </div>

    <!-- Data Table -->
    <DataTable 
      :value="users" 
      :loading="loading"
      loadingMode="icon"
      paginator 
      :rows="10" 
      :rowsPerPageOptions="[10, 20, 50]"
      dataKey="id"
      filterDisplay="row"
      v-model:filters="filters"
      :globalFilterFields="['first_name', 'last_name', 'email', 'tc_kimlik_no', 'role']"  
      class="p-datatable-sm"
      responsiveLayout="scroll" 
    >
      <template #header>
        <div class="table-header">
          <span class="p-input-icon-left">
            <i class="pi pi-search" />
            <InputText v-model="filters['global'].value" placeholder="Genel Arama" id="globalSearch" name="globalSearch" />
          </span>
        </div>
      </template>
      
      <template #empty> Kullanıcı bulunamadı. </template>
      <template #loading> Kullanıcılar yükleniyor... </template>
      
      <Column field="tc_kimlik_no" header="TC Kimlik No" sortable filterMatchMode="contains" style="min-width: 10rem;"> 
        <template #filter="{ filterModel, filterCallback }">
          <InputText v-model="filterModel.value" @input="filterCallback()" placeholder="TC No ile ara" class="p-column-filter" />
        </template>
      </Column>
      <Column field="first_name" header="Ad" sortable filterMatchMode="contains" style="min-width: 10rem;">
        <template #filter="{ filterModel, filterCallback }">
          <InputText v-model="filterModel.value" @input="filterCallback()" placeholder="Ada göre ara" class="p-column-filter" />
        </template>
      </Column>
      <Column field="last_name" header="Soyad" sortable filterMatchMode="contains" style="min-width: 10rem;">
        <template #filter="{ filterModel, filterCallback }">
          <InputText v-model="filterModel.value" @input="filterCallback()" placeholder="Soyada göre ara" class="p-column-filter" />
        </template>
      </Column>
      <Column field="email" header="E-posta" sortable filterMatchMode="contains" style="min-width: 12rem;">
         <template #filter="{ filterModel, filterCallback }">
          <InputText v-model="filterModel.value" @input="filterCallback()" placeholder="E-postaya göre ara" class="p-column-filter" />
        </template>
      </Column>
      <Column field="role" header="Rol" sortable filterMatchMode="equals" style="min-width: 10rem;">
        <template #filter="{ filterModel, filterCallback }">
          <Dropdown 
            v-model="filterModel.value" 
            :options="roles" 
            optionLabel="name"
            optionValue="code"
            placeholder="Rol Seçin" 
            class="p-column-filter" 
            showClear
            @change="filterCallback()"
          />
        </template>
         <template #body="slotProps">
          <Tag :value="getRoleName(slotProps.data.role)" :severity="getRoleSeverity(slotProps.data.role)" />
        </template>
      </Column>
      <Column header="İşlemler" style="min-width: 8rem; text-align: center;" frozen alignFrozen="right"> 
        <template #body="slotProps">
          <Button icon="pi pi-pencil" class="p-button-rounded p-button-success mr-2" @click="openEditUserDialog(slotProps.data)" />
          <Button icon="pi pi-trash" class="p-button-rounded p-button-danger" @click="confirmDeleteUser(slotProps.data)" />
        </template>
      </Column>
    </DataTable>

    <!-- Yeni/Düzenle Kullanıcı Dialog -->
    <Dialog 
      v-model:visible="userDialogVisible" 
      :header="dialogHeader" 
      :modal="true" 
      class="p-fluid user-dialog"
      @hide="hideDialog"
      :breakpoints="{'960px': '75vw', '640px': '95vw'}" 
      style="width: 50vw;" 
    >
      <form @submit.prevent="saveUser"> <!-- Add form tag -->
        <div class="formgrid grid">
          <div class="field col-12 md:col-6">
            <label for="tcno">TC Kimlik Numarası</label>
          <InputText 
            id="tcno" 
            name="tcno"
            v-model.trim="currentUser.tcno" 
            required 
            autofocus 
            maxlength="11"
            :class="{'p-invalid': submitted && (!currentUser.tcno || errors.tcno)}" 
            :disabled="isEditMode"
            autocomplete="off"
          />
          <small class="p-error" v-if="submitted && !currentUser.tcno">TC Kimlik No zorunludur.</small>
          <small class="p-error" v-if="errors.tcno">{{ errors.tcno }}</small>
        </div>
        <div class="field col-12 md:col-6">
          <label for="role">Rol</label>
          <Dropdown 
            id="role" 
            name="role"
            v-model="currentUser.role" 
            :options="roles" 
            optionLabel="name"
            optionValue="code"
            placeholder="Rol Seçin"
            required
            :class="{'p-invalid': submitted && errors.role}" 
          />
           <small class="p-error" v-if="submitted && errors.role">{{ errors.role }}</small>
        </div>
        <div class="field col-12 md:col-6">
          <label for="firstName">Ad</label>
          <InputText id="firstName" name="firstName" v-model.trim="currentUser.first_name" required :class="{'p-invalid': submitted && errors.first_name}" autocomplete="given-name"/>
          <small class="p-error" v-if="submitted && errors.first_name">{{ errors.first_name }}</small>
        </div>
        <div class="field col-12 md:col-6">
          <label for="lastName">Soyad</label>
          <InputText id="lastName" name="lastName" v-model.trim="currentUser.last_name" required :class="{'p-invalid': submitted && errors.last_name}" autocomplete="family-name"/>
          <small class="p-error" v-if="submitted && errors.last_name">{{ errors.last_name }}</small>
        </div>
        <div class="field col-12">
          <label for="email">E-posta</label>
          <InputText id="email" name="email" v-model.trim="currentUser.email" required type="email" :class="{'p-invalid': submitted && errors.email}" autocomplete="email"/>
          <small class="p-error" v-if="submitted && errors.email">{{ errors.email }}</small>
        </div>
        <div class="field col-12 md:col-6">
          <label for="password">Şifre {{ isEditMode ? '(Değiştirmek istemiyorsanız boş bırakın)' : '' }}</label>
          <Password 
            id="password" 
            name="password"
            v-model="currentUser.password" 
            :feedback="!isEditMode" 
            toggleMask
            :required="!isEditMode"
            :class="{'p-invalid': submitted && errors.password}"
            autocomplete="new-password"
          />
           <small class="p-error" v-if="submitted && !isEditMode && !currentUser.password">Şifre zorunludur.</small>
           <small class="p-error" v-if="submitted && !isEditMode && !currentUser.password">Şifre zorunludur.</small>
           <small class="p-error" v-if="errors.password">{{ errors.password }}</small>
          </div>
        </div>
      </form> <!-- Close form tag -->

      <template #footer>
        <div class="dialog-footer-buttons"> 
          <Button label="İptal" icon="pi pi-times" class="p-button-text" @click="hideDialog"/>
          <!-- Change button type to submit to potentially help with form context -->
          <Button :label="saveButtonLabel" icon="pi pi-check" type="submit" @click="saveUser" :loading="saving"/> 
        </div>
      </template>
    </Dialog>

  </div>
</template>

<script setup>
import { ref, onMounted, reactive, computed, nextTick } from 'vue'; // Import nextTick
import apiClient, { invalidateCacheEntry } from '../../api/axios'; // apiClient ve invalidateCacheEntry'yi import et
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Password from 'primevue/password';
import Dialog from 'primevue/dialog';
import Tag from 'primevue/tag';
import Toast from 'primevue/toast';
import ConfirmDialog from 'primevue/confirmdialog';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import { FilterMatchMode } from 'primevue/api';

const toast = useToast();
const confirm = useConfirm();

const users = ref([]);
const loading = ref(true);
const saving = ref(false);
const userDialogVisible = ref(false);
const isEditMode = ref(false);
const submitted = ref(false);
const currentUser = reactive({});
const errors = reactive({}); // Form validasyon/API hataları

// Roller (Backend modeline göre güncellendi)
const roles = ref([
    { name: 'Admin', code: 'ADMIN' }, // Uppercase
    { name: 'Jüri Üyesi', code: 'JURI_UYESI' }, // Uppercase and match backend
    { name: 'Yönetici', code: 'YONETICI' }, // Uppercase and match backend
    { name: 'Aday', code: 'ADAY' } // Uppercase
    // SUPERADMIN eklenmedi, genellikle doğrudan atanmaz.
]);

// DataTable filtreleri
const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    tc_kimlik_no: { value: null, matchMode: FilterMatchMode.CONTAINS }, // Changed filter key to tc_kimlik_no
    first_name: { value: null, matchMode: FilterMatchMode.CONTAINS },
    last_name: { value: null, matchMode: FilterMatchMode.CONTAINS },
    email: { value: null, matchMode: FilterMatchMode.CONTAINS },
    role: { value: null, matchMode: FilterMatchMode.EQUALS },
});

// Rol adını ve tag rengini almak için yardımcı fonksiyonlar
const getRoleName = (roleCode) => {
    const role = roles.value.find(r => r.code === roleCode);
    return role ? role.name : roleCode;
};

const getRoleSeverity = (roleCode) => {
    // Use uppercase codes matching the updated roles array
    if (roleCode === 'ADMIN') return 'danger';
    if (roleCode === 'JURI_UYESI') return 'warning';
    if (roleCode === 'YONETICI') return 'help'; // Changed from manager_candidate
    if (roleCode === 'ADAY') return 'info';
    if (roleCode === 'SUPERADMIN') return 'primary'; // Add SUPERADMIN if needed
    return 'secondary';
};

// Kullanıcıları API'den çekme
const fetchUsers = async () => {
    loading.value = true;
    try {
        // noCache: true ekleyerek cache'i bypass etmeyi deneyebiliriz, 
        // ancak invalidate daha doğru bir yaklaşım.
        const response = await apiClient.get('/api/users/'); 
        users.value = response.data.results || response.data; // API hem {results:[]} hem de direkt array dönebilir
    } catch (error) {
        console.error("Kullanıcılar yüklenirken hata oluştu:", error);
        nextTick(() => { // Wrap toast in nextTick
            toast.add({ severity: 'error', summary: 'Hata', detail: 'Kullanıcılar yüklenemedi.', life: 3000 });
        });
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    fetchUsers();
});

// Dialog işlemleri
const openNewUserDialog = () => {
    Object.keys(currentUser).forEach(key => delete currentUser[key]); // Obje içeriğini temizle
    Object.keys(errors).forEach(key => delete errors[key]); // Hataları temizle
    isEditMode.value = false;
    submitted.value = false;
    userDialogVisible.value = true;
};

const openEditUserDialog = (user) => {
    // Create a deep copy to avoid modifying the original user object in the table directly
    const userCopy = JSON.parse(JSON.stringify(user));
    // Ensure tcno is mapped correctly if backend sends tc_kimlik_no
    currentUser.tcno = userCopy.tc_kimlik_no || userCopy.tcno; 
    Object.assign(currentUser, { ...userCopy, password: '' }); // Şifreyi düzenleme formunda gösterme
    Object.keys(errors).forEach(key => delete errors[key]);
    isEditMode.value = true;
    submitted.value = false;
    userDialogVisible.value = true;
};

const hideDialog = () => {
    userDialogVisible.value = false;
    submitted.value = false;
};

// Dialog başlığı ve kaydet butonu etiketi
const dialogHeader = computed(() => isEditMode.value ? 'Kullanıcı Düzenle' : 'Yeni Kullanıcı');
const saveButtonLabel = computed(() => isEditMode.value ? 'Güncelle' : 'Kaydet');

// Form validasyonu
const validate = () => {
    let isValid = true;
    Object.keys(errors).forEach(key => delete errors[key]); // Eski hataları temizle

    // TC No validasyonu
    if (!currentUser.tcno) {
        errors.tcno = 'TC Kimlik No zorunludur.';
        isValid = false;
    } else if (currentUser.tcno.length !== 11 || !/^[1-9][0-9]{10}$/.test(currentUser.tcno)) {
        errors.tcno = 'Geçerli 11 haneli TC Kimlik No giriniz.';
        isValid = false;
    }

    // Ad validasyonu
    if (!currentUser.first_name) {
        errors.first_name = 'Ad zorunludur.';
        isValid = false;
    } else if (currentUser.first_name.length < 2) {
        errors.first_name = 'Ad en az 2 karakter olmalıdır.';
        isValid = false;
    }

    // Soyad validasyonu
    if (!currentUser.last_name) {
        errors.last_name = 'Soyad zorunludur.';
        isValid = false;
    } else if (currentUser.last_name.length < 2) {
        errors.last_name = 'Soyad en az 2 karakter olmalıdır.';
        isValid = false;
    }

    // Email validasyonu
    if (!currentUser.email) {
        errors.email = 'E-posta zorunludur.';
        isValid = false;
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(currentUser.email)) {
        errors.email = 'Geçerli bir e-posta adresi giriniz.';
        isValid = false;
    }

    // Rol validasyonu
    if (!currentUser.role) {
        errors.role = 'Rol seçimi zorunludur.';
        isValid = false;
    }

    // Şifre validasyonu
    if (!isEditMode.value && !currentUser.password) {
        errors.password = 'Şifre zorunludur.';
        isValid = false;
    } else if (currentUser.password && currentUser.password.length < 8) {
        errors.password = 'Şifre en az 8 karakter olmalıdır.';
        isValid = false;
    } else if (currentUser.password && !/(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}/.test(currentUser.password)) {
        errors.password = 'Şifre en az 1 büyük harf, 1 küçük harf ve 1 rakam içermelidir.';
        isValid = false;
    }
    
    return isValid;
};

// Kullanıcı kaydetme veya güncelleme
const saveUser = async () => {
    submitted.value = true;
    if (!validate()) {
        nextTick(() => { // Wrap toast in nextTick
            toast.add({ severity: 'warn', summary: 'Uyarı', detail: 'Lütfen gerekli alanları kontrol edin.', life: 3000 });
        });
        return;
    }

    saving.value = true;
    // Clear previous errors before making the API call
    Object.keys(errors).forEach(key => delete errors[key]); 

    // Construct payload with expected backend field names based on UserCreateSerializer
    const userData = {
        tc_kimlik_no: currentUser.tcno, // Ensure this matches backend serializer
        // username: currentUser.tcno, // REMOVED: Let backend serializer handle username derivation from tc_kimlik_no
        first_name: currentUser.first_name,
        last_name: currentUser.last_name,
        email: currentUser.email,
        role: currentUser.role,
    };

    // Add password only if creating or if it's provided during edit
    if (!isEditMode.value || (isEditMode.value && currentUser.password)) {
        userData.password = currentUser.password;
    }

    try {
        let response;
        if (isEditMode.value) {
            // Güncelleme - Use PATCH for partial updates
            // Construct payload specifically for update, excluding read-only fields
            const updateData = {
                first_name: currentUser.first_name,
                last_name: currentUser.last_name,
                email: currentUser.email,
                role: currentUser.role,
                // Include other updatable fields from UserUpdateSerializer if they exist in currentUser
                ...(currentUser.faculty && { faculty: currentUser.faculty }), 
                ...(currentUser.department && { department: currentUser.department }),
                ...(currentUser.phone && { phone: currentUser.phone }),
            };
             // Add password only if it was provided in the edit form
            if (currentUser.password) {
                 updateData.password = currentUser.password;
            }

            response = await apiClient.patch(`/api/users/${currentUser.id}/`, updateData);
            nextTick(() => { // Wrap toast in nextTick
                toast.add({ severity: 'success', summary: 'Başarılı', detail: 'Kullanıcı güncellendi.', life: 3000 });
            });
        } else {
            // Ekleme - Payload already includes necessary fields (tc_kimlik_no, etc.)
            // Add potentially missing fields required by UserCreateSerializer, using '' instead of null
            userData.faculty = ''; // Send empty string instead of null
            userData.department = ''; // Send empty string instead of null
            userData.phone = ''; // Send empty string instead of null
            // Ensure password is included for creation
            if (!userData.password) {
                 // This case should ideally be caught by frontend validation, but as a safeguard:
                 console.error("Password missing for user creation!");
                 throw new Error("Şifre oluşturma için zorunludur.");
            }
            response = await apiClient.post('/api/users/', userData);
            nextTick(() => { // Wrap toast in nextTick
                toast.add({ severity: 'success', summary: 'Başarılı', detail: 'Kullanıcı eklendi.', life: 3000 });
            });
        }
        userDialogVisible.value = false;
        
        // Başarılı işlem sonrası kullanıcı listesi cache'ini temizle
        invalidateCacheEntry('get', '/api/users/'); 
        
        fetchUsers(); // Always fetch users after successful save/update
    } catch (error) {
        console.error("Kullanıcı kaydedilirken hata oluştu:", error.response?.data || error.message);
        let errorMessage = 'İşlem sırasında bir bilinmeyen hata oluştu.'; // Default generic error
        let hasSpecificError = false;

        if (error.response?.data) {
            const backendData = error.response.data;
            const errorString = backendData.error || (typeof backendData === 'string' ? backendData : ''); // Get potential error string

            // Check for specific duplicate key error patterns
            if (errorString.includes('duplicate key value') && errorString.includes('email')) {
                errors.email = 'Bu e-posta adresi zaten kullanılıyor.';
                hasSpecificError = true;
            }
            else if (errorString.includes('duplicate key value') && errorString.includes('tc_kimlik_no')) {
                 errors.tcno = 'Bu TC Kimlik Numarası zaten kullanılıyor.'; // Use tcno for form error display
                 hasSpecificError = true;
            }
            // Fallback to existing parsing logic for other structured errors
            else {
                const fieldErrors = backendData.details || (typeof backendData === 'object' && !Array.isArray(backendData) ? backendData : null); 

                if (fieldErrors) {
                    Object.keys(fieldErrors).forEach(key => {
                        // Map backend key to frontend key (tc_kimlik_no -> tcno for form)
                        const frontendKey = key === 'tc_kimlik_no' ? 'tcno' : key; 
                        if (Object.prototype.hasOwnProperty.call(currentUser, frontendKey) || ['password', 'tcno', 'role', 'email', 'first_name', 'last_name'].includes(frontendKey)) { 
                            errors[frontendKey] = Array.isArray(fieldErrors[key]) ? fieldErrors[key].join(' ') : String(fieldErrors[key]);
                            hasSpecificError = true;
                        } else {
                            if (errorMessage === 'İşlem sırasında bir bilinmeyen hata oluştu.') errorMessage = ''; 
                            errorMessage += `${key}: ${Array.isArray(fieldErrors[key]) ? fieldErrors[key].join(' ') : String(fieldErrors[key])} `;
                        }
                    });
                } 
                // Use the raw error string if no specific parsing worked
                else if (errorString) {
                    errorMessage = errorString;
                }
            }
        } else {
            // Network error or other non-response errors
            errorMessage = error.message || 'Ağ hatası veya sunucuya ulaşılamıyor.';
        }

        // Display appropriate toast message
        if (hasSpecificError) {
             nextTick(() => { // Wrap toast in nextTick
                toast.add({ severity: 'warn', summary: 'Doğrulama Hatası', detail: 'Lütfen formdaki işaretli hataları düzeltin.', life: 4000 });
             });
        } else {
             nextTick(() => { // Wrap toast in nextTick
                toast.add({ severity: 'error', summary: 'Hata', detail: errorMessage.trim(), life: 5000 });
             });
        }
    } finally { 
        saving.value = false;
    }
};


// Kullanıcı silme onayı
const confirmDeleteUser = (user) => {
    confirm.require({
        message: `${user.first_name} ${user.last_name} kullanıcısını silmek istediğinize emin misiniz?`,
        header: 'Silme Onayı',
        icon: 'pi pi-exclamation-triangle',
        acceptLabel: 'Evet',
        rejectLabel: 'Hayır',
        accept: async () => {
            try {
                await apiClient.delete(`/api/users/${user.id}/`);
                
                // Başarılı silme sonrası kullanıcı listesi cache'ini temizle
                invalidateCacheEntry('get', '/api/users/');

                nextTick(() => { // Wrap toast in nextTick
                    toast.add({ severity: 'success', summary: 'Başarılı', detail: 'Kullanıcı silindi.', life: 3000 });
                });
                // Fetch users in the next tick after the toast
                nextTick(() => { 
                    fetchUsers(); 
                });
            } catch (error) {
                console.error("Kullanıcı silinirken hata:", error);
                nextTick(() => { // Wrap toast in nextTick
                    toast.add({ severity: 'error', summary: 'Hata', detail: 'Kullanıcı silinemedi.', life: 3000 });
                });
            }
        }
    });
};

</script>

<style scoped>
.user-management {
  padding: 1.5rem;
  background-color: #f8f9fa;
  min-height: calc(100vh - 60px); /* Adjust based on header height */
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding: 1rem 1.5rem; 
  background: white;
  border-radius: 8px; 
  box-shadow: 0 2px 5px rgba(0,0,0,0.06); 
}

.table-header {
  display: flex;
  justify-content: flex-start; /* Align search to the left */
  align-items: center;
  padding: 0.5rem 0 1rem 0; 
}

/* --- Paginator Styles (Keep existing fixes) --- */
:deep(.p-paginator) { 
    display: flex;
    align-items: center;
    justify-content: center; 
    flex-wrap: wrap; 
    gap: 0.5rem;
    padding: 1rem 0; 
    background-color: transparent; 
    border: none; 
}

:deep(.p-paginator .p-paginator-first),
:deep(.p-paginator .p-paginator-prev),
:deep(.p-paginator .p-paginator-next),
:deep(.p-paginator .p-paginator-last),
:deep(.p-paginator .p-paginator-pages .p-paginator-page) {
    min-width: 2.5rem;
    height: 2.5rem;
    margin: 0 0.2rem; 
    border-radius: 4px; 
}

:deep(.p-paginator .p-dropdown) {
    height: 2.5rem; 
}
/* --- End Paginator Styles --- */


.p-datatable-sm .p-datatable-tbody > tr > td {
    padding: 0.75rem 1rem;
}

.p-column-filter {
    width: 100%;
}

.mr-2 {
  margin-right: 0.5rem;
}


/* --- Dialog Styles --- */
/* Keep width adjustments from previous attempt */
.user-dialog {
    /* width: 55vw; */ /* Let PrimeVue handle width with style/breakpoints */
    max-width: 700px; 
    min-width: 450px; 
}

.user-dialog :deep(.p-dialog-content) { 
    padding: 2rem 2.5rem; 
}

.user-dialog .formgrid.grid {
    margin: 0 -0.75rem; 
}

.user-dialog .field {
    padding: 0 0.75rem; 
    margin-bottom: 1.8rem; /* Keep increased vertical spacing */
}

.user-dialog .field label {
    display: block;
    margin-bottom: 0.75rem; /* Keep increased space below label */
    font-weight: 500;
    color: #495057; 
}

.user-dialog input[type="text"],
.user-dialog input[type="email"],
.user-dialog :deep(.p-dropdown), 
.user-dialog :deep(.p-password) { 
    width: 100%; 
}

.user-dialog .p-error {
    display: block;
    margin-top: 0.4rem; 
    font-size: 0.875rem;
}

/* --- Dialog Footer --- */
.user-dialog :deep(.p-dialog-footer) { 
    padding: 1.5rem 2.5rem 2rem 2.5rem; 
    border-top: 1px solid #dee2e6; 
    margin-top: 1rem; 
}

.dialog-footer-buttons { /* Wrapper for buttons */
    display: flex;
    justify-content: flex-end; 
    gap: 1rem; /* Keep increased space */
}

.user-dialog .p-button {
    min-width: 110px; 
    padding: 0.65rem 1rem; 
}
/* --- End Dialog Styles --- */


/* Responsive Adjustments (Keep existing) */
@media screen and (max-width: 960px) {
    .user-dialog {
        /* width: 75vw; */ /* Let PrimeVue handle */
        min-width: 400px;
    }
     .user-dialog :deep(.p-dialog-content) {
        padding: 1.5rem 2rem;
    }
     .user-dialog :deep(.p-dialog-footer) {
        padding: 1rem 2rem 1.5rem 2rem;
    }
}

@media screen and (max-width: 640px) {
    .user-management {
        padding: 1rem; 
    }
    .page-header {
        padding: 0.8rem 1rem;
        margin-bottom: 1rem;
    }
    .user-dialog {
        /* width: 95vw; */ /* Let PrimeVue handle */
        min-width: unset;
    }
    .user-dialog .formgrid.grid {
        margin: 0 -0.5rem;
    }
    .user-dialog .field {
        padding: 0 0.5rem;
        margin-bottom: 1.2rem;
    }
    .user-dialog :deep(.p-dialog-content) {
        padding: 1.2rem 1.5rem;
    }
     .user-dialog :deep(.p-dialog-footer) {
        padding: 1rem 1.5rem 1.5rem 1.5rem;
    }
    .dialog-footer-buttons {
        gap: 0.5rem; /* Reduce gap on small screens */
    }
    .user-dialog .p-button {
        min-width: 90px;
        padding: 0.6rem 0.8rem;
    }
    .user-dialog .formgrid.grid .field.col-12.md\:col-6 {
        width: 100%; /* Stack fields */
    }
}
</style>






















