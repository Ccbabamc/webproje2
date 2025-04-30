<template>
  <div class="documents-container">
    <h1>Belgelerim</h1>

    <!-- Removed Upload Section -->
    <!-- 
    <div class="upload-section card">
      <h2>Yeni Belge Yükle</h2>
      ... (upload form and selected files list code removed) ...
    </div> 
    -->

    <div class="documents-list-section card">
      <h2>Yüklenmiş Belgeler</h2>
      <p class="info-text">Burada, farklı başvurularınız için yüklediğiniz tüm belgeleri görebilirsiniz.</p>
      
      <div v-if="isLoading" class="loading-container">
        <div class="spinner"></div>
        <p>Belgeler yükleniyor...</p>
      </div>

      <div v-else-if="documents.length === 0" class="empty-state">
        <div class="empty-icon">📄</div>
        <p>Henüz yüklenmiş belgeniz bulunmamaktadır.</p>
         <p>Belgelerinizi ilgili ilana başvuru yaparken yükleyebilirsiniz.</p>
      </div>

      <div v-else class="documents-grid">
        <div v-for="doc in documents" :key="doc.id" class="document-card">
          <div class="doc-icon">
            {{ getFileIcon(doc.file) }}
          </div>
          <div class="doc-info">
            <a :href="doc.file" target="_blank" class="doc-name" :title="doc.name || 'Belge'">
              {{ doc.name || 'Belge' }}
            </a>
            <span class="doc-date">Yüklenme: {{ formatDate(doc.uploaded_at) }}</span>
             <!-- İlişkili Başvuruyu Göster (Opsiyonel) -->
             <span v-if="doc.basvuru_ilan_title" class="doc-application">
               İlan: {{ doc.basvuru_ilan_title }} (ID: {{ doc.basvuru_id }})
             </span>
          </div>
          <div class="doc-actions">
            <button class="action-btn download" @click="downloadDocument(doc.file, doc.name)" title="İndir">
              ⬇️
            </button>
            <!-- Silme işlevi genellikle başvuru üzerinden yönetilir, buradan kaldırılabilir -->
            <!-- 
            <button class="action-btn delete" @click="deleteDocument(doc)" title="Sil">
              🗑️
            </button> 
            -->
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
    </div>

    <!-- Silme onay modalı kaldırıldı -->
    <!-- 
    <div v-if="showDeleteModal" class="modal-overlay">
      ... (modal content removed) ...
    </div> 
    -->
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import apiClient from '../../api/axios'

export default {
  name: 'CandidateDocuments',
  setup() {
    const isLoading = ref(false)
    const isLoadingMore = ref(false)
    // Removed upload/delete related refs
    // const isUploading = ref(false) 
    // const isDeleting = ref(false)
    // const selectedFiles = ref([])
    // const showDeleteModal = ref(false)
    // const selectedDocument = ref(null)
    const documents = ref([])
    const page = ref(1)
    const hasNextPage = ref(false)


    onMounted(async () => {
      await loadDocuments()
    })

    const loadDocuments = async () => {
      if (isLoading.value && page.value > 1) return // Prevent concurrent loads
      if (page.value === 1) isLoading.value = true;

      try {
        const params = { page: page.value }
        // Endpoint'i kontrol et, muhtemelen /api/documents/my/ veya benzeri olmalı
        // Backend view'ına göre ayarla
        const response = await apiClient.get('/api/documents/my/', { params }) 
        
        // Backend'den gelen veriyi işle (ilişkili başvuru bilgisi eklenmiş olabilir)
        const processedDocs = response.data.results.map(doc => ({
          ...doc,
          // Backend serializer'ı bu bilgileri sağlıyorsa:
          basvuru_id: doc.basvuru?.id, 
          basvuru_ilan_title: doc.basvuru?.ilan?.baslik 
        }));

        if (page.value === 1) {
          documents.value = processedDocs;
        } else {
          documents.value = [...documents.value, ...processedDocs];
        }

        hasNextPage.value = !!response.data.next
      } catch (error) {
        console.error('Belgeler yüklenirken hata:', error)
      } finally {
         if (page.value === 1) isLoading.value = false;
      }
    }

    const loadMore = async () => {
      if (isLoadingMore.value || !hasNextPage.value) return

      page.value++
      isLoadingMore.value = true
      try {
        await loadDocuments()
      } finally {
        isLoadingMore.value = false
      }
    }

    // Removed upload/delete related methods
    // handleFileSelect, removeSelectedFile, uploadSelectedFiles, deleteDocument, confirmDelete

    const downloadDocument = (fileUrl, fileName) => {
      if (!fileUrl) return;
      const link = document.createElement('a')
      link.href = fileUrl
      link.target = '_blank' // Yeni sekmede açmak için
      link.download = fileName || 'belge' // İndirilen dosya adı
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }

    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    const formatDate = (dateString) => {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleDateString('tr-TR', { 
        year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' 
      })
    }

    const getFileIcon = (filePath) => {
      if (!filePath) return '❓'
      const extension = filePath.split('.').pop().toLowerCase()
      if (extension === 'pdf') return '📄'
      if (['doc', 'docx'].includes(extension)) return '📝'
      if (['jpg', 'jpeg', 'png', 'gif'].includes(extension)) return '🖼️'
      return '📁'
    }

    return {
      isLoading,
      isLoadingMore,
      // Removed upload/delete related refs
      documents,
      hasNextPage,
      downloadDocument,
      formatFileSize,
      formatDate,
      getFileIcon,
      loadMore
    }
  }
}
</script>

<style scoped>
.documents-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

h1 {
  font-size: 1.8rem;
  color: var(--primary-color);
  margin-bottom: 24px;
}

.card {
  background: white;
  border-radius: var(--border-radius-lg);
  padding: 24px;
  margin-bottom: 24px;
}

h2 {
  font-size: 1.4rem;
  color: var(--dark-color);
  margin: 0 0 20px 0;
}

.info-text {
  color: var(--gray-color);
  margin-bottom: 20px;
  font-size: 0.95rem;
}




.documents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.document-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  transition: box-shadow 0.3s ease;
}

.document-card:hover {
  box-shadow: var(--shadow-sm);
}

.doc-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.doc-info {
  flex-grow: 1;
  overflow: hidden;
}

.doc-name {
  display: block;
  font-weight: 500;
  color: var(--primary-color);
  text-decoration: none;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 4px;
}

.doc-name:hover {
  text-decoration: underline;
}

.doc-date {
  font-size: 0.85rem;
  color: var(--gray-color);
  display: block; /* Ensure it takes its own line */
}
.doc-application {
  font-size: 0.85rem;
  color: var(--gray-color);
  display: block; /* Ensure it takes its own line */
  margin-top: 4px;
}


.doc-actions {
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

.action-btn.download {
  color: var(--primary-color);
}





.action-btn:hover {
  background: rgba(0, 0, 0, 0.1);
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

.btn-outline {
  background: none;
  border: 1px solid var(--primary-color);
  color: var(--primary-color);
}

.btn-outline:hover {
  background: var(--border-color);
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.empty-state {
  text-align: center;
  padding: 48px 24px;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 16px;
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
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white; /* Spinner for buttons */
  animation: spin 1s linear infinite;
}

.loading-container .spinner { /* Spinner for loading container */
   border-top-color: var(--primary-color); 
}


.btn-outline .spinner {
  border-top-color: var(--primary-color);
}

.load-more {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .documents-container {
    padding: 16px;
  }

  .documents-grid {
    grid-template-columns: 1fr;
  }
}
</style>
