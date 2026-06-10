<template>
  <div class="chat-page">
    <!-- Messages area -->
    <div class="chat-messages" ref="messagesEl">
      <Transition name="fade-up">
        <ChatEmpty
          v-if="store.messages.length === 0"
          @pick="store.input = $event"
        />
      </Transition>

      <TransitionGroup name="msg" tag="div" class="messages-list">
        <MessageBubble
          v-for="(msg, i) in store.messages"
          :key="i"
          :message="msg"
        />
      </TransitionGroup>
    </div>

    <!-- Input bar -->
    <div class="input-area">
      <div class="input-box" :class="{ 'input-box--focused': isFocused }">
        <input
          type="text"
          class="input-field"
          v-model="store.input"
          placeholder="Ask about your documents…"
          :disabled="store.loading"
          @keyup.enter="sendMessage"
          @focus="isFocused = true"
          @blur="isFocused = false"
        />
        <button
          class="send-btn"
          :class="{ 'send-btn--active': store.input.trim() && !store.loading }"
          :disabled="store.loading || !store.input.trim()"
          @click="sendMessage"
          aria-label="Send"
        >
          <svg
            v-if="!store.loading"
            width="15"
            height="15"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <line x1="22" y1="2" x2="11" y2="13" />
            <polygon points="22 2 15 22 11 13 2 9 22 2" />
          </svg>
          <svg
            v-else
            class="spin"
            width="15"
            height="15"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
          >
            <path d="M21 12a9 9 0 1 1-6.219-8.56" />
          </svg>
        </button>
      </div>
    </div>

    <AppFooter />
    <Toast position="bottom-right" />
  </div>
</template>

<script setup lang="ts">
import AppFooter from '@/components/AppFooter.vue'
import ChatEmpty from '@/components/chat/ChatEmpty.vue'
import MessageBubble from '@/components/chat/MessageBubble.vue'
import * as queryService from '@/services/query.service'
import { useChatStore } from '@/stores/chat'
import Toast from 'primevue/toast'
import { useToast } from 'primevue/usetoast'
import { nextTick, reactive, ref, watch } from 'vue'

const store = useChatStore()
const toast = useToast()
const messagesEl = ref<HTMLElement | null>(null)
const isFocused = ref(false)
let currentStream: AbortController | null = null

const scrollToBottom = async () => {
  await nextTick()
  if (messagesEl.value)
    messagesEl.value.scrollTop = messagesEl.value.scrollHeight
}

watch(() => store.messages.length, scrollToBottom)
watch(() => store.messages[store.messages.length - 1]?.content, scrollToBottom)

const sendMessage = () => {
  const text = store.input.trim()
  if (!text || store.loading) return

  currentStream?.abort()
  store.messages.push({ role: 'user', content: text })
  store.input = ''

  const assistantMsg = reactive({
    role: 'assistant' as const,
    content: '',
    loading: true,
  })
  store.messages.push(assistantMsg)
  store.loading = true

  currentStream = queryService.streamQuery(
    text,
    (chunk) => {
      assistantMsg.content += chunk
    },
    () => {
      assistantMsg.loading = false
      store.loading = false
    },
    (error) => {
      assistantMsg.content = `Error: ${error}`
      assistantMsg.loading = false
      store.loading = false
      toast.add({
        severity: 'error',
        summary: 'Error',
        detail: error,
        life: 5000,
      })
    },
  )
}
</script>

<style scoped lang="scss">
@use '@/assets/styles/scss/variables' as *;
@use '@/assets/styles/scss/mixins' as *;

.chat-page {
  @include page-root;
}

// ─── Messages ────────────────────────────────────────────────────────────────

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 0 24px 16px;
  display: flex;
  flex-direction: column;
}

.messages-list {
  @include flex-col;
  gap: 6px;
  width: 100%;
  max-width: 760px;
  margin: 0 auto;
}

// ─── Input ───────────────────────────────────────────────────────────────────

.input-area {
  padding: 12px 24px 14px;
  display: flex;
  justify-content: center;
  border-top: 1px solid $c-border-s;
}

.input-box {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  max-width: 760px;
  padding: 10px 12px 10px 16px;
  border-radius: $r-xl;
  background: $c-surface;
  border: 1px solid $c-border;
  transition:
    border-color 0.18s ease,
    box-shadow 0.18s ease;

  &--focused {
    border-color: rgba($c-accent, 0.45);
    box-shadow: 0 0 0 3px rgba($c-accent-hi, 0.08);
  }
}

.input-field {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: $c-text-1;
  font-size: 14px;
  font-family: $font-body;
  line-height: 1.5;

  &::placeholder {
    color: $c-text-3;
  }
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.send-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  @include flex-center;
  background: $c-raised;
  border: 1px solid $c-border;
  color: $c-text-3;
  flex-shrink: 0;
  transition: all 0.15s ease;
  cursor: not-allowed;

  &--active {
    background: $c-accent-hi;
    border-color: $c-accent-hi;
    color: #fff;
    cursor: pointer;
    box-shadow: 0 2px 10px rgba($c-accent-hi, 0.4);

    &:hover {
      background: $c-accent;
      transform: scale(1.05);
    }
  }
}

.spin {
  animation: spin 0.8s linear infinite;
}

// ─── Transitions ─────────────────────────────────────────────────────────────

.msg-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.msg-enter-active {
  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
}
.fade-up-enter-from {
  opacity: 0;
  transform: translateY(16px);
}
.fade-up-enter-active {
  transition:
    opacity 0.3s ease,
    transform 0.3s ease;
}
</style>
