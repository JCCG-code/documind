<template>
  <div class="msg-row" :class="`msg-row--${message.role}`">
    <!-- User bubble -->
    <div v-if="message.role === 'user'" class="bubble bubble--user">
      {{ message.content }}
    </div>

    <!-- Assistant bubble -->
    <div v-else class="bubble bubble--assistant">
      <div class="assistant-avatar" aria-hidden="true">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none">
          <path
            d="M12 2L2 7l10 5 10-5-10-5z"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linejoin="round"
          />
          <path
            d="M2 17l10 5 10-5"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linejoin="round"
          />
          <path
            d="M2 12l10 5 10-5"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linejoin="round"
          />
        </svg>
      </div>
      <div class="assistant-body">
        <span
          v-if="message.loading && !message.content"
          class="skeleton-line"
        />
        <div
          v-if="message.content"
          class="markdown-body"
          v-html="renderMarkdown(message.content)"
        />
        <span v-if="message.loading" class="typing-cursor" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Message } from '@/stores/chat'
import { renderMarkdown } from '@/utils/markdown'
import 'highlight.js/styles/github-dark.css'

defineProps<{ message: Message }>()
</script>

<style scoped lang="scss">
@use '@/assets/styles/scss/variables' as *;
@use '@/assets/styles/scss/mixins' as *;

.msg-row {
  display: flex;
  width: 100%;

  &--user {
    justify-content: flex-end;
    padding-top: 12px;
  }
  &--assistant {
    justify-content: flex-start;
    padding-top: 16px;
  }
}

// ─── Bubbles ────────────────────────────────────────────────────────────────

.bubble {
  &--user {
    max-width: 72%;
    padding: 10px 16px;
    border-radius: 18px 18px 4px 18px;
    background: $c-raised;
    border: 1px solid $c-border;
    color: $c-text-1;
    font-size: 14px;
    line-height: 1.55;
    word-break: break-word;
  }

  &--assistant {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    max-width: 100%;
  }
}

.assistant-avatar {
  @include icon-box($c-accent, 26px, 7px);
  background: linear-gradient(135deg, $c-accent 0%, $c-accent-hi 100%);
  border-color: transparent;
  color: #fff;
  margin-top: 2px;
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
}

.assistant-body {
  flex: 1;
  min-width: 0;
  padding-top: 2px;
}

// ─── Loading states ──────────────────────────────────────────────────────────

.typing-cursor {
  display: inline-block;
  width: 2px;
  height: 1em;
  background: $c-accent;
  margin-left: 2px;
  vertical-align: text-bottom;
  border-radius: 1px;
  animation: blink 0.9s step-end infinite;
}

.skeleton-line {
  display: block;
  height: 14px;
  width: 180px;
  border-radius: 4px;
  background: linear-gradient(
    90deg,
    $c-raised 25%,
    $c-hover 50%,
    $c-raised 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
}

// ─── Markdown ────────────────────────────────────────────────────────────────

.markdown-body {
  color: $c-text-1;
  font-size: 14px;
  line-height: 1.7;

  &:deep(strong) {
    font-weight: 600;
  }
  &:deep(em) {
    font-style: italic;
    color: $c-text-2;
  }
  &:deep(a) {
    color: $c-accent;
    text-decoration: underline;
    text-underline-offset: 2px;
  }
  &:deep(hr) {
    border: none;
    border-top: 1px solid $c-border;
    margin: 16px 0;
  }
  &:deep(blockquote) {
    border-left: 3px solid $c-accent;
    padding-left: 14px;
    margin: 12px 0;
    color: $c-text-2;
    font-style: italic;
  }

  &:deep(h1),
  &:deep(h2),
  &:deep(h3) {
    font-weight: 600;
    margin: 20px 0 8px;
    color: $c-text-1;
    line-height: 1.3;
  }
  &:deep(h1) {
    font-size: 1.25rem;
  }
  &:deep(h2) {
    font-size: 1.1rem;
  }
  &:deep(h3) {
    font-size: 1rem;
  }

  &:deep(p) {
    margin: 0 0 10px;
    &:last-child {
      margin-bottom: 0;
    }
  }

  &:deep(ul),
  &:deep(ol) {
    margin: 8px 0 10px 20px;
    display: block;
  }
  &:deep(ul) {
    list-style: disc;
  }
  &:deep(ol) {
    list-style: decimal;
  }
  &:deep(li) {
    margin: 3px 0;
    display: list-item;
  }

  &:deep(pre) {
    border: 1px solid $c-border;
    padding: 14px 16px;
    border-radius: $r-md;
    overflow-x: auto;
    margin: 12px 0;
    @include mono-font;
    font-size: 13px;
  }

  &:deep(code:not(pre code)) {
    @include mono-font;
    font-size: 12.5px;
    background: $c-raised;
    border: 1px solid $c-border;
    padding: 2px 6px;
    border-radius: 4px;
    color: $c-accent;
  }
}
</style>
