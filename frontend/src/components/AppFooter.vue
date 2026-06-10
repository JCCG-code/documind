<template>
  <footer class="app-footer">
    <p class="footer-disclaimer">
      <svg
        width="12"
        height="12"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        aria-hidden="true"
      >
        <circle cx="12" cy="12" r="10" />
        <line x1="12" y1="8" x2="12" y2="12" />
        <line x1="12" y1="16" x2="12.01" y2="16" />
      </svg>
      Answers are based solely on your indexed documents
    </p>
    <p class="footer-attribution">
      Built by
      <a
        href="https://github.com/JCCG-code/documind"
        target="_blank"
        rel="noopener noreferrer"
        title="Documind on GitHub"
        >@JCCG-Code</a
      >
      ·
      <a
        href="https://www.linkedin.com/in/juan-carlos-cuadrado-gracia/"
        target="_blank"
        rel="noopener noreferrer"
        title="LinkedIn"
        >LinkedIn</a
      >
    </p>
  </footer>
</template>

<style scoped lang="scss">
@use '@/assets/styles/scss/variables' as *;
@use '@/assets/styles/scss/mixins' as *;

.app-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 6px;
  padding: 8px 24px 12px;
  border-top: 1px solid $c-border-s;
}

.footer-disclaimer {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11.5px;
  color: $c-text-3;
  line-height: 1.4;

  svg {
    flex-shrink: 0;
    opacity: 0.7;
  }
}

.footer-attribution {
  font-size: 11.5px;
  color: $c-text-3;

  a {
    color: $c-text-2;
    text-decoration: none;
    transition: color 0.12s ease;

    &:hover {
      color: $c-accent;
    }
  }
}
</style>
