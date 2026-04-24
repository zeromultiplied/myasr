<script setup lang="ts">
import { ref } from 'vue'
import { login, register, setToken } from '../api'

const emit = defineEmits<{
  authenticated: [user: { id: number; username: string }]
}>()

const mode = ref<'login' | 'register'>('login')
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function onSubmit() {
  error.value = ''
  if (!username.value || !password.value) {
    error.value = '请填写用户名和密码'
    return
  }
  loading.value = true
  try {
    const fn = mode.value === 'login' ? login : register
    const res = await fn(username.value, password.value)
    setToken(res.token)
    emit('authenticated', res.user)
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

function switchMode() {
  mode.value = mode.value === 'login' ? 'register' : 'login'
  error.value = ''
}
</script>

<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-header">
        <h1>MyASR</h1>
        <p>语音转写与智能分析</p>
      </div>

      <form class="login-form" @submit.prevent="onSubmit">
        <label class="field">
          <span>用户名</span>
          <input
            v-model="username"
            type="text"
            placeholder="请输入用户名"
            autocomplete="username"
          />
        </label>

        <label class="field">
          <span>密码</span>
          <input
            v-model="password"
            type="password"
            placeholder="请输入密码"
            autocomplete="current-password"
          />
        </label>

        <div v-if="error" class="login-error">{{ error }}</div>

        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? '处理中...' : (mode === 'login' ? '登录' : '注册') }}
        </button>
      </form>

      <div class="login-switch">
        <span v-if="mode === 'login'">还没有账号？</span>
        <span v-else>已有账号？</span>
        <button class="btn-switch" @click="switchMode">
          {{ mode === 'login' ? '立即注册' : '去登录' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: var(--cream);
}

.login-card {
  width: 380px;
  max-width: 90vw;
  background: var(--cream);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-card);
  padding: var(--space-8) var(--space-6);
}

.login-header {
  text-align: center;
  margin-bottom: var(--space-6);
}

.login-header h1 {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--charcoal);
  margin: 0 0 4px 0;
  letter-spacing: -0.02em;
}

.login-header p {
  font-size: 0.875rem;
  color: var(--muted);
  margin: 0;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.field span {
  font-size: 0.813rem;
  font-weight: 500;
  color: var(--charcoal);
}

.field input {
  padding: 10px 12px;
  font-size: 0.875rem;
}

.login-error {
  padding: 8px 12px;
  background: var(--charcoal-3);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-std);
  color: var(--charcoal-83);
  font-size: 0.813rem;
}

.btn-primary {
  margin-top: var(--space-1);
  padding: 10px 16px;
  background: var(--charcoal);
  color: var(--off-white);
  border: none;
  border-radius: var(--radius-std);
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: var(--btn-inset);
  transition: opacity 0.15s;
}

.btn-primary:hover { opacity: 0.85; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }

.login-switch {
  margin-top: var(--space-4);
  text-align: center;
  font-size: 0.813rem;
  color: var(--muted);
}

.btn-switch {
  border: none;
  background: none;
  color: var(--charcoal);
  font-size: 0.813rem;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
  padding: 0 4px;
}

.btn-switch:hover { opacity: 0.7; }
</style>
