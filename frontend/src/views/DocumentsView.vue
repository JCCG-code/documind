<template>
  <div class="docs-page">
    <!-- Header -->
    <div class="docs-header">
      <div class="docs-header__left">
        <h1 class="docs-title">Documents</h1>
        <span class="docs-count">{{ store.documents.length }} indexed</span>
      </div>
      <FileUpload
        mode="basic"
        custom-upload
        @select="onSelect"
        choose-label="Ingest file"
        accept=".pdf,.txt,.md"
        class="upload-btn-wrap"
      />
    </div>

    <!-- Content -->
    <div class="docs-content">
      <!-- Empty state -->
      <div v-if="store.documents.length === 0 && !store.loading" class="docs-empty">
        <div class="empty-icon">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
          </svg>
        </div>
        <p class="empty-title">No documents yet</p>
        <p class="empty-sub">Upload a PDF, TXT or Markdown file to get started</p>
      </div>

      <!-- Cards -->
      <div v-else class="docs-grid">
        <DocCard v-if="store.loading" :loading="true" />
        <DocCard v-for="doc in store.documents" :key="doc.hash" :doc="doc" />
      </div>
    </div>

    <AppFooter />
    <Toast position="bottom-right" />
  </div>
</template>

<script setup lang="ts">
import AppFooter from '@/components/AppFooter.vue'
import DocCard from '@/components/documents/DocCard.vue'
import * as documentService from '@/services/document.service'
import { useDocumentsStore } from '@/stores/documents'
import FileUpload from 'primevue/fileupload'
import Toast from 'primevue/toast'
import { useToast } from 'primevue/usetoast'
import { onMounted } from 'vue'

const store = useDocumentsStore()
const toast = useToast()

onMounted(async () => {
  if (!store.hydrated) {
    store.documents = await loadDocuments()
    store.hydrated = true
  }
})

const onSelect = async (event: { files: File[] }) => {
  store.loading = true
  const file = event.files[0] as File
  const res = await documentService.ingestDocument(file)
  if (res.detail) {
    toast.add({ severity: 'error', summary: 'Error', detail: res.detail, life: 5000 })
  }
  store.documents = await loadDocuments()
  store.loading = false
}

const loadDocuments = async (): Promise<Document[]> => {
  const res = await documentService.getAllDocuments()
  res.forEach((doc) => { doc.size = Number((doc.size / 1024).toFixed(2)) })
  return res
}
</script>

<style scoped lang="scss">
@use '@/assets/styles/scss/variables' as *;
@use '@/assets/styles/scss/mixins' as *;

.docs-page {
  @include page-root;
}

// ─── Header ──────────────────────────────────────────────────────────────────

.docs-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px 16px;
  border-bottom: 1px solid $c-border-s;
  flex-shrink: 0;

  &__left {
    display: flex;
    align-items: baseline;
    gap: 10px;
  }
}

.docs-title {
  @include display-font;
  font-size: 1.35rem;
  color: $c-text-1;
}

.docs-count {
  font-size: 12px;
  color: $c-text-3;
  @include mono-font;
}

// PrimeVue FileUpload override
.upload-btn-wrap {
  :deep(.p-fileupload-choose) {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 7px 14px;
    border-radius: $r-md;
    background: $c-accent-hi;
    border: none;
    color: #fff;
    font-size: 13px;
    font-family: $font-body;
    font-weight: 500;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba($c-accent-hi, 0.3);
    transition: background 0.15s ease, box-shadow 0.15s ease;

    &:hover {
      background: $c-accent;
      box-shadow: 0 4px 14px rgba($c-accent-hi, 0.45);
    }
  }
}

// ─── Content ─────────────────────────────────────────────────────────────────

.docs-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px;
}

// ─── Empty state ─────────────────────────────────────────────────────────────

.docs-empty {
  @include flex-col;
  @include flex-center;
  height: 100%;
  gap: 10px;
  text-align: center;
  padding: 48px 24px;
}

.empty-icon {
  @include icon-box($c-text-3, 52px, 12px);
  background: $c-raised;
  margin-bottom: 4px;
}

.empty-title {
  font-size: 15px;
  font-weight: 500;
  color: $c-text-2;
}

.empty-sub {
  font-size: 13px;
  color: $c-text-3;
  max-width: 280px;
  line-height: 1.5;
}

// ─── Grid ────────────────────────────────────────────────────────────────────

.docs-grid {
  @include flex-col;
  gap: 6px;
  max-width: 720px;
}
</style>
