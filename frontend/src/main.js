import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import TestList from './views/TestList.vue'
import TestInterface from './views/TestInterface.vue'
import TestResult from './views/TestResult.vue'
import AdminDashboard from './views/AdminDashboard.vue'
import TestManager from './views/TestManager.vue'

const routes = [
  { path: '/', component: TestList },
  { path: '/test/:id', component: TestInterface },
  { path: '/result/:id', component: TestResult },
  { path: '/admin', component: AdminDashboard },
  { path: '/manage', component: TestManager }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

createApp(App).use(router).mount('#app')