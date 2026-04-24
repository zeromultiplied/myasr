<script setup lang="ts">
import { ref, onMounted } from 'vue'
import LoginPage from './components/LoginPage.vue'
import HomePage from './components/HomePage.vue'
import TranscribePage from './components/TranscribePage.vue'
import MaterialsPage from './components/MaterialsPage.vue'
import { getToken, clearToken, fetchMe, type UserInfo } from './api'

const currentPage = ref<'home' | 'transcribe' | 'materials'>('home')
const isAuthenticated = ref(false)
const user = ref<UserInfo | null>(null)
const authLoading = ref(true)

onMounted(async () => {
  if (getToken()) {
    try {
      user.value = await fetchMe()
      isAuthenticated.value = true
    } catch {
      clearToken()
    }
  }
  authLoading.value = false
})

function onAuthenticated(u: { id: number; username: string }) {
  user.value = u
  isAuthenticated.value = true
}

function onLogout() {
  clearToken()
  isAuthenticated.value = false
  user.value = null
  currentPage.value = 'home'
}
</script>

<template>
  <!-- Auth gate -->
  <LoginPage
    v-if="!authLoading && !isAuthenticated"
    @authenticated="onAuthenticated"
  />

  <!-- Loading -->
  <div v-else-if="authLoading" class="loading-screen">加载中...</div>

  <!-- Main app -->
  <div v-else class="layout">
    <aside class="sidebar">
      <div class="sidebar-top">
        <h2>MyASR</h2>
        <p class="sidebar-sub">语音转写与智能分析</p>
      </div>
      <nav class="nav">
        <button
          class="nav-item"
          :class="{ active: currentPage === 'home' }"
          @click="currentPage = 'home'"
        >
          <span class="nav-icon">🏠</span>
          <span>首页</span>
        </button>
        <button
          class="nav-item"
          :class="{ active: currentPage === 'transcribe' }"
          @click="currentPage = 'transcribe'"
        >
          <span class="nav-icon">🎤</span>
          <span>语音转写</span>
        </button>
        <button
          class="nav-item"
          :class="{ active: currentPage === 'materials' }"
          @click="currentPage = 'materials'"
        >
          <span class="nav-icon">📄</span>
          <span>资料管理</span>
        </button>
      </nav>

      <div class="sidebar-footer">
        <div class="user-info">
          <span class="user-avatar">👤</span>
          <span class="user-name">{{ user?.username || '用户' }}</span>
        </div>
        <button class="btn-logout" @click="onLogout">退出</button>
      </div>
    </aside>

    <main class="content">
      <HomePage
        v-if="currentPage === 'home'"
        @navigate="(p: string) => currentPage = p as any"
      />
      <TranscribePage v-else-if="currentPage === 'transcribe'" />
      <MaterialsPage v-else-if="currentPage === 'materials'" />
    </main>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.loading-screen {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  color: var(--muted);
  font-size: 0.875rem;
  background: var(--cream);
}

.sidebar {
  width: 220px;
  min-width: 220px;
  background: var(--cream);
  border-right: 1px solid var(--border-light);
  display: flex;
  flex-direction: column;
}

.sidebar-top {
  padding: 20px 16px 16px;
  border-bottom: 1px solid var(--border-light);
}

.sidebar-top h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--charcoal);
  letter-spacing: -0.02em;
}

.sidebar-sub {
  margin: 4px 0 0 0;
  font-size: 0.875rem;
  color: var(--muted);
}

.nav {
  display: flex;
  flex-direction: column;
  padding: 8px;
  gap: 4px;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border: none;
  background: none;
  border-radius: var(--radius-std);
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 400;
  color: var(--charcoal);
  text-align: left;
  transition: background 0.15s;
}

.nav-item:hover {
  background: var(--charcoal-4);
}

.nav-item.active {
  background: var(--charcoal-3);
  font-weight: 600;
}

.nav-icon {
  font-size: 1rem;
  width: 20px;
  text-align: center;
}

/* Sidebar footer */
.sidebar-footer {
  padding: 12px 16px;
  border-top: 1px solid var(--border-light);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.user-avatar {
  font-size: 1.125rem;
  flex-shrink: 0;
}

.user-name {
  font-size: 0.813rem;
  font-weight: 500;
  color: var(--charcoal);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.btn-logout {
  border: none;
  background: none;
  color: var(--muted);
  font-size: 0.75rem;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: var(--radius-micro);
  transition: color 0.15s, background 0.15s;
  flex-shrink: 0;
}

.btn-logout:hover {
  color: var(--charcoal-83);
  background: var(--charcoal-4);
}

.content {
  flex: 1;
  padding: 0;
  overflow-y: auto;
  background: var(--cream);
}
</style>
