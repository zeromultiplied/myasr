<script setup lang="ts">
import { ref } from 'vue'
import HomePage from './components/HomePage.vue'
import TranscribePage from './components/TranscribePage.vue'

const currentPage = ref<'home' | 'transcribe'>('home')

function navigate(page: string) {
  if (page === 'home' || page === 'transcribe') {
    currentPage.value = page
  }
}
</script>

<template>
  <div class="layout">
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
      </nav>
    </aside>

    <main class="content">
      <HomePage
        v-if="currentPage === 'home'"
        @navigate="navigate"
      />
      <TranscribePage
        v-else-if="currentPage === 'transcribe'"
      />
    </main>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
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

.content {
  flex: 1;
  padding: 0;
  overflow-y: auto;
  background: var(--cream);
}
</style>
