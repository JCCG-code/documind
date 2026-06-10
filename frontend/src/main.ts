// Packages
import Lara from '@primeuix/themes/lara'
import axios from 'axios'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'
import { createApp } from 'vue'
import VueAxios from 'vue-axios'

// Global styles
import '@/assets/styles/css/reset.css'
import '@/assets/styles/scss/init.scss'

// Local files
import App from './App.vue'
import router from './router'

// Initializations
const app = createApp(App)
const pinia = createPinia()

// Axios default base url of API
axios.defaults.baseURL = 'http://localhost:8000/'

// Middlewares
app.use(pinia)
app.use(router)
app.use(VueAxios, axios)
app.use(PrimeVue, { theme: { preset: Lara } })
app.use(ToastService)

// Provide axios because of composition API
app.provide('axios', app.config.globalProperties.axios)

// App is mounted
app.mount('#app')
