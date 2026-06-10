<template>
  <!-- Loading card -->
  <div v-if="loading" class="doc-card doc-card--loading">
    <div class="doc-card__icon doc-card__icon--neutral">
      <svg
        class="spin"
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
      >
        <path d="M21 12a9 9 0 1 1-6.219-8.56" />
      </svg>
    </div>
    <div class="doc-card__info">
      <span class="doc-card__name">Ingesting file…</span>
      <span class="doc-card__meta">Processing &amp; indexing</span>
    </div>
    <span class="doc-badge doc-badge--pending">pending</span>
  </div>

  <!-- Document card -->
  <div v-else-if="doc" class="doc-card">
    <div class="doc-card__icon" :class="`doc-card__icon--${fileType}`">
      <svg
        width="17"
        height="17"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="1.5"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <line v-if="fileType === 'pdf'" x1="8" y1="13" x2="16" y2="13" />
        <line v-else x1="8" y1="13" x2="16" y2="13" />
        <line v-if="fileType === 'md'" x1="8" y1="17" x2="16" y2="17" />
        <line v-else x1="8" y1="17" x2="13" y2="17" />
      </svg>
    </div>
    <div class="doc-card__info">
      <span class="doc-card__name" :title="doc.filename">{{
        doc.filename
      }}</span>
      <span class="doc-card__meta">{{ doc.size }} KB</span>
    </div>
    <span class="doc-badge" :class="`doc-badge--${fileType}`">{{
      fileLabel
    }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  doc?: Document
  loading?: boolean
}>()

const fileType = computed(() => {
  const ct = props.doc?.content_type ?? ''
  if (ct.includes('pdf')) return 'pdf'
  if (ct.includes('markdown') || ct.includes('md')) return 'md'
  return 'txt'
})

const fileLabel = computed(() => fileType.value.toUpperCase())
</script>

<style scoped lang="scss">
@use '@/assets/styles/scss/variables' as *;
@use '@/assets/styles/scss/mixins' as *;

.doc-card {
  @include card-surface;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;

  &--loading {
    animation: pulse-fade 1.5s ease-in-out infinite;
    pointer-events: none;
  }

  &__icon {
    @include icon-box($c-accent);

    &--pdf {
      @include icon-box(#f87171);
    }
    &--txt {
      @include icon-box($c-accent);
    }
    &--md {
      @include icon-box($c-success);
    }
    &--neutral {
      @include icon-box($c-text-3);
    }
  }

  &__info {
    flex: 1;
    min-width: 0;
    @include flex-col;
    gap: 2px;
  }

  &__name {
    font-size: 13.5px;
    font-weight: 500;
    color: $c-text-1;
    @include truncate;
  }

  &__meta {
    font-size: 12px;
    color: $c-text-3;
    @include mono-font;
  }
}

.doc-badge {
  font-size: 10.5px;
  font-weight: 600;
  @include mono-font;
  letter-spacing: 0.05em;
  padding: 3px 8px;
  border-radius: 4px;
  flex-shrink: 0;
  text-transform: uppercase;

  &--pdf {
    @include badge-color(#f87171);
  }
  &--txt {
    @include badge-color($c-accent);
  }
  &--md {
    @include badge-color($c-success);
  }
  &--pending {
    @include badge-color($c-warn);
  }
}

.spin {
  @include spin-animation;
}
</style>
