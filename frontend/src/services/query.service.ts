import axios from 'axios'

export const streamQuery = (
  query: string,
  onChunk: (chunk: string) => void,
  onDone: () => void,
  onError: (error: string) => void,
  model: string = 'qwen3:8b',
): AbortController => {
  const controller = new AbortController()
  const data: QueryRequest = { text: query, model }

  fetch(`${axios.defaults.baseURL}query/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
    signal: controller.signal,
  })
    .then(async (response) => {
      if (!response.ok) {
        const detail = await response.text()
        onError(`HTTP ${response.status}: ${detail}`)
        return
      }

      const reader = response.body?.getReader()
      if (!reader) {
        onError('No response body')
        return
      }

      const decoder = new TextDecoder()
      let buffer = ''
      let finished = false

      const read = () => {
        reader
          .read()
          .then(({ done, value }) => {
            if (done) {
              if (!finished) onDone()
              return
            }

            buffer += decoder.decode(value, { stream: true })

            const events = buffer.split('\n\n')
            buffer = events.pop() || ''

            for (const event of events) {
              if (!event.startsWith('data: ')) continue
              const payload = event.slice(6)

              if (payload === '[DONE]') {
                finished = true
                onDone()
                reader.cancel()
                return
              }

              try {
                onChunk(JSON.parse(payload))
              } catch {
                onChunk(payload)
              }
            }

            if (!finished) read()
          })
          .catch((err) => {
            if (err.name !== 'AbortError') onError(err.message)
          })
      }

      read()
    })
    .catch((error) => {
      if (error.name !== 'AbortError') onError(error.message)
    })

  return controller
}

export const query = async (
  queryText: string,
  model: string = 'qwen3:8b',
): Promise<QueryResponse> => {
  const data: QueryRequest = { text: queryText, model }
  const res = await axios.post<QueryResponse>('/query', data)
  return res.data
}
