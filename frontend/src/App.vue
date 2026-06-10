<template>
  <div class="app-shell">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar__brand">
        <div class="brand-glyph">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
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
        <span class="brand-name">documind</span>
      </div>

      <nav class="sidebar__nav">
        <RouterLink
          to="/"
          exact-active-class="nav-link--active"
          class="nav-link"
        >
          <svg
            class="nav-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path
              d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
            />
          </svg>
          <span>Chat</span>
        </RouterLink>

        <RouterLink
          to="/documents"
          active-class="nav-link--active"
          class="nav-link"
        >
          <svg
            class="nav-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path
              d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"
            />
          </svg>
          <span>Documents</span>
        </RouterLink>
      </nav>

      <div class="sidebar__footer">
        <div class="model-tag">
          <span class="model-dot" />
          <span class="model-label">qwen3:8b</span>
        </div>
      </div>
    </aside>

    <!-- Main area -->
    <main class="main-pane">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts"></script>

<style lang="scss">
@use '@/assets/styles/scss/variables' as *;

// ─── Shell layout ────────────────────────────────────────────────────────────

.app-shell {
  display: flex;
  height: 100%;
  overflow: hidden;
}

.main-pane {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  overflow: hidden;
  background: #09090b;
}

// ─── Sidebar ─────────────────────────────────────────────────────────────────

.sidebar {
  width: 240px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  background: #111113;
  border-right: 1px solid #1c1c1f;
  padding: 16px 10px 16px;

  &__brand {
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 4px 8px 18px;
    border-bottom: 1px solid #1c1c1f;
    margin-bottom: 10px;
  }

  &__nav {
    display: flex;
    flex-direction: column;
    gap: 2px;
    flex: 1;
  }

  &__footer {
    padding-top: 14px;
    border-top: 1px solid #1c1c1f;
  }
}

.brand-glyph {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 7px;
  background: linear-gradient(135deg, #818cf8 0%, #6366f1 100%);
  color: #fff;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.35);
}

.brand-name {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 1.15rem;
  font-weight: 500;
  letter-spacing: 0.03em;
  color: #fafafa;
}

// ─── Nav links ───────────────────────────────────────────────────────────────

.nav-link {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 7px 10px;
  border-radius: 7px;
  color: #71717a;
  font-size: 13.5px;
  font-weight: 400;
  transition:
    color 0.12s ease,
    background 0.12s ease;
  text-decoration: none;

  .nav-icon {
    width: 15px;
    height: 15px;
    flex-shrink: 0;
    transition: color 0.12s ease;
  }

  &:hover {
    color: #e4e4e7;
    background: #18181b;
  }

  &--active {
    color: #e4e4e7;
    background: #18181b;

    .nav-icon {
      color: #818cf8;
    }
  }
}

// ─── Model badge ─────────────────────────────────────────────────────────────

.model-tag {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 6px 10px;
  border-radius: 6px;
  background: #18181b;
  border: 1px solid #27272a;
}

.model-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #4ade80;
  flex-shrink: 0;
  box-shadow: 0 0 6px rgba(74, 222, 128, 0.5);
  animation: model-pulse 2.4s ease-in-out infinite;
}

.model-label {
  font-size: 11.5px;
  color: #71717a;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.02em;
}

@keyframes model-pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.45;
  }
}
</style>
