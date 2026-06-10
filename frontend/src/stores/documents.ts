import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useDocumentsStore = defineStore('documents', () => {
  const documents = ref<Document[]>([])
  const loading = ref(false)
  const hydrated = ref(false)

  return { documents, loading, hydrated }
})
