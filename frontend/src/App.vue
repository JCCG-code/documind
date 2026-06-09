<template>
  <div class="main-wrap-app">
    <RouterView />
  </div>
</template>

<script setup lang="ts"></script>

<style lang="scss">
@import '@/assets/styles/css/reset.css';
@import '@/assets/styles/css/init.css';

.app-main-wrap {
  display: flex;
  flex-direction: column;

  min-width: 100vw;
  min-height: 100vh;
}
</style>
