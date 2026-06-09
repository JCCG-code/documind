import * as documentChecker from '@/utils/checkers/document.checker'
import axios from 'axios'

/**
 * Allows to get all documents from API
 * @returns Array of Documents
 */
export const getAllDocuments = async (): Promise<Document[]> => {
  // Call API
  const res = await axios.get('/documents')
  // Check data exists
  if (!res.data) {
    return []
    // Check Document[] type
  } else if (!documentChecker.isArrayDocument(res.data)) {
    return []
  }
  // Return statement
  return res.data
}

export const ingestDocument = async (document: File) => {
  const formData = new FormData()
  formData.append('file', document)
  // Call API
  try {
    const res = await axios.post('/documents/ingest', formData)
    if (res.data.points) {
      return res
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      // El detail de tu HTTPException está aquí
      return error.response?.data
    }
  }
}
