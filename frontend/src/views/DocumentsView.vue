<template>
  <h1>Documents</h1>
  <!-- Ingest new document -->
  <FileUpload
    mode="basic"
    custom-upload
    @select="onSelect"
    choose-label="Ingest document"
  />
  <!-- List of documents -->
  <div class="document__list">
    <div v-if="data.documents.length === 0">No documents ingested</div>
    <div v-else>
      <!-- Documents already ingested -->
      <div v-for="(document, index) in data.documents" :key="document.hash">
        <Accordion :value="index">
          <AccordionPanel :value="index">
            <AccordionHeader>{{ document.filename }}</AccordionHeader>
            <AccordionContent>
              <div class="document__content__info">
                <p>{{ document.content_type }}</p>
                |
                <p>{{ document.size }} kb</p>
              </div>
            </AccordionContent>
          </AccordionPanel>
        </Accordion>
      </div>
      <!-- Accordion document loading -->
      <Accordion v-if="data.loading">
        <AccordionPanel value="loading">
          <AccordionHeader>
            Ingesting new file... <i class="pi pi-spin pi-spinner"></i>
          </AccordionHeader>
        </AccordionPanel>
      </Accordion>
    </div>
    <Toast />
  </div>
</template>

<script setup lang="ts">
import * as documentService from '@/services/document.service'
import Accordion from 'primevue/accordion'
import AccordionContent from 'primevue/accordioncontent'
import AccordionHeader from 'primevue/accordionheader'
import AccordionPanel from 'primevue/accordionpanel'
import FileUpload from 'primevue/fileupload'
import Toast from 'primevue/toast'
import { useToast } from 'primevue/usetoast'
import { onMounted, reactive } from 'vue'

// Initializations
const toast = useToast()

// Reactive data
const data = reactive({
  documents: [] as Document[],
  loading: false,
  document_size: 0,
})

onMounted(async () => {
  data.documents = await loadDocuments()
})

const onSelect = async (event: { files: File[] }) => {
  // Loading
  data.loading = true
  // Extract file to index
  const file = event.files[0] as File
  const res = await documentService.ingestDocument(file)
  // Check response
  if (res.detail) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: res.detail,
      life: 5000,
    })
  }
  console.log(res)
  // Refresh document list
  data.documents = await loadDocuments()
  data.loading = false
}

const loadDocuments = async (): Promise<Document[]> => {
  const res = await documentService.getAllDocuments()
  // Transform size attribute to kb
  res.forEach((doc) => {
    doc.size = Number((doc.size /= 1024).toFixed(2))
  })
  return res
}
</script>

<style lang="scss" scoped>
.document__content__info {
  display: flex;
  gap: 10px;
}
</style>
