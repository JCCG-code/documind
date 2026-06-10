interface QueryRequest {
  text: string
  model?: string
}

interface QueryResponse {
  answer: string
  sources: string[]
  confidence: number
  chunks_used: number
}
