import { defineStore } from 'pinia'
import { reactive, ref } from 'vue'

export interface Message {
  role: 'user' | 'assistant'
  content: string
  loading?: boolean
}

export const useChatStore = defineStore('chat', () => {
  const messages = ref<Message[]>([])
  const input = ref('')
  const loading = ref(false)

  const pushMessage = (
    msg: Omit<Message, 'loading'> & { loading?: boolean },
  ): Message => {
    const m = reactive<Message>({ ...msg })
    messages.value.push(m)
    return m
  }

  return { messages, input, loading, pushMessage }
})
