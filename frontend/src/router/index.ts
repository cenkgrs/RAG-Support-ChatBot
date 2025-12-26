import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '@/views/LoginView.vue'
import DashboardView from '@/views/DashboardView.vue'
import ChatTestView from '@/views/ChatTestView.vue'
import ChatView from '@/views/ChatView.vue'
import ChatSettingsView from '@/views/ChatSettingsView.vue'
import DocumentsView from '@/views/DocumentsView.vue'
import AnalysisView from '@/views/AnalysisView.vue'
import ThemeSettingsView from '@/views/ThemeSettingsView.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },

  // Dashboard Pages
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/chat',
    name: '/chat',
    component: ChatView,
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/test-arayuzu',
    name: 'test',
    component: ChatTestView,
    meta: { requiresAuth: true }
  },
  {
    path: '/chatbot-ayar',
    name: 'chatbot',
    component: ChatSettingsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/icerik-dokuman',
    name: 'icerik',
    component: DocumentsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/analiz',
    name: 'analiz',
    component: AnalysisView,
    meta: { requiresAuth: true }
  },
  {
    path: '/tema-ayar',
    name: 'tema',
    component: ThemeSettingsView,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const raw = localStorage.getItem('user')

  if (!raw) {
    if (to.meta.requiresAuth) return next('/login')
    return next()
  }

  const data = JSON.parse(raw)

  if (data.expires < Date.now()) {
    localStorage.removeItem('user')
    return next('/login')
  }

  next()
})

export default router
