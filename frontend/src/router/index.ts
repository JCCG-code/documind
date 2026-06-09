import { createRouter, createWebHistory } from 'vue-router'

// Local pages
import DocumentsView from '@/views/DocumentsView.vue'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomeView',
      component: HomeView,
    },
    {
      path: '/documents',
      name: 'DocumentView',
      component: DocumentsView,
    },
  ],
})

export default router
