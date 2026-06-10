<template>
  <div class="chat-empty">
    <div class="empty-glyph">
      <svg
        width="32"
        height="32"
        viewBox="0 0 24 24"
        fill="none"
        aria-hidden="true"
      >
        <path
          d="M12 2L2 7l10 5 10-5-10-5z"
          stroke="currentColor"
          stroke-width="1.5"
          stroke-linejoin="round"
          stroke-linecap="round"
        />
        <path
          d="M2 17l10 5 10-5"
          stroke="currentColor"
          stroke-width="1.5"
          stroke-linejoin="round"
          stroke-linecap="round"
        />
        <path
          d="M2 12l10 5 10-5"
          stroke="currentColor"
          stroke-width="1.5"
          stroke-linejoin="round"
          stroke-linecap="round"
        />
      </svg>
    </div>

    <h1 class="empty-title">Documind</h1>
    <p class="empty-sub">Ask questions about your indexed documents</p>

    <div class="empty-chips">
      <button
        v-for="s in SUGGESTIONS"
        :key="s"
        class="chip"
        @click="$emit('pick', s)"
      >
        {{ s }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineEmits<{ pick: [text: string] }>()

const SUGGESTIONS = [
  'Summarize the key topics in my documents',
  'What are the main conclusions?',
  'List the most important facts',
  'Compare the documents I have indexed',
]
</script>

<style scoped lang="scss">
@use '@/assets/styles/scss/variables' as *;
@use '@/assets/styles/scss/mixins' as *;

.chat-empty {
  flex: 1;
  @include flex-col;
  @include flex-center;
  text-align: center;
  padding: 48px 24px;
  gap: 12px;
}

.empty-glyph {
  @include icon-box($c-accent, 56px, 14px);
  background: linear-gradient(135deg, $c-accent 0%, $c-accent-hi 100%);
  border-color: transparent;
  color: #fff;
  box-shadow: 0 4px 20px $c-accent-gl;
  margin-bottom: 4px;
}

.empty-title {
  @include display-font;
  font-size: 2.2rem;
  color: $c-text-1;
}

.empty-sub {
  font-size: 14px;
  color: $c-text-3;
  max-width: 360px;
  line-height: 1.5;
}

.empty-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-top: 12px;
  max-width: 560px;
}

.chip {
  padding: 7px 14px;
  border-radius: 20px;
  border: 1px solid $c-border;
  background: $c-surface;
  color: $c-text-2;
  font-size: 13px;
  font-family: $font-body;
  cursor: pointer;
  transition:
    border-color 0.15s ease,
    color 0.15s ease,
    background 0.15s ease;

  &:hover {
    border-color: $c-accent;
    color: $c-text-1;
    background: $c-accent-lo;
  }
}
</style>
