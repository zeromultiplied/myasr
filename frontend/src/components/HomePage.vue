<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchStats, type StatsData } from '../api'

const emit = defineEmits<{
  navigate: [page: string]
}>()

const stats = ref<StatsData | null>(null)
const loading = ref(true)

const statusLabels: Record<string, string> = {
  uploading: '上传中',
  transcribing: '转写中',
  llm_processing: 'LLM处理中',
  done: '已完成',
  failed: '失败',
}

const statusColors: Record<string, string> = {
  uploading: '#f59e0b',
  transcribing: '#3b82f6',
  llm_processing: '#8b5cf6',
  done: '#10b981',
  failed: '#ef4444',
}

onMounted(async () => {
  try {
    stats.value = await fetchStats()
  } catch (e) {
    console.error('Failed to load stats:', e)
  } finally {
    loading.value = false
  }
})

function formatTime(iso: string): string {
  const d = new Date(iso)
  return d.toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<template>
  <div class="home-page">
    <h2 class="page-title">欢迎使用 MyASR</h2>

    <!-- Stats cards -->
    <div class="stats-row" v-if="stats">
      <div class="stat-card">
        <div class="stat-num">{{ stats.total }}</div>
        <div class="stat-label">总任务数</div>
      </div>
      <div class="stat-card done">
        <div class="stat-num">{{ stats.done }}</div>
        <div class="stat-label">已完成</div>
      </div>
      <div class="stat-card processing">
        <div class="stat-num">{{ stats.processing }}</div>
        <div class="stat-label">处理中</div>
      </div>
      <div class="stat-card failed">
        <div class="stat-num">{{ stats.failed }}</div>
        <div class="stat-label">失败</div>
      </div>
    </div>
    <div v-else-if="loading" class="loading-hint">加载中...</div>

    <!-- Usage steps -->
    <div class="section">
      <h3 class="section-title">使用步骤</h3>
      <div class="steps-row">
        <div class="step-card">
          <div class="step-num">1</div>
          <div class="step-icon">🎤</div>
          <div class="step-title">上传音频</div>
          <div class="step-desc">支持 wav / flac / opus / m4a / mp3 格式</div>
        </div>
        <div class="step-arrow">→</div>
        <div class="step-card">
          <div class="step-num">2</div>
          <div class="step-icon">⏳</div>
          <div class="step-title">等待转写</div>
          <div class="step-desc">讯飞语音引擎自动转录，支持中英文</div>
        </div>
        <div class="step-arrow">→</div>
        <div class="step-card">
          <div class="step-num">3</div>
          <div class="step-icon">✨</div>
          <div class="step-title">查看结果</div>
          <div class="step-desc">LLM 自动总结、润色、发散、提取行动项</div>
        </div>
      </div>
      <button class="btn-start" @click="$emit('navigate', 'transcribe')">开始使用</button>
    </div>

    <!-- Recent activity -->
    <div class="section" v-if="stats?.recent?.length">
      <h3 class="section-title">最近动态</h3>
      <div class="activity-list">
        <div
          v-for="item in stats.recent"
          :key="item.id"
          class="activity-item"
        >
          <span class="activity-name" :title="item.filename">{{ item.filename }}</span>
          <span
            class="activity-status"
            :style="{ color: statusColors[item.status] || '#667085' }"
          >{{ statusLabels[item.status] || item.status }}</span>
          <span class="activity-time">{{ formatTime(item.updated_at) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  max-width: 860px;
  margin: 0 auto;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: #1d2939;
  margin: 0 0 24px 0;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  border-left: 4px solid #4f46e5;
}

.stat-card.done { border-left-color: #10b981; }
.stat-card.processing { border-left-color: #3b82f6; }
.stat-card.failed { border-left-color: #ef4444; }

.stat-num {
  font-size: 28px;
  font-weight: 700;
  color: #1d2939;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 13px;
  color: #667085;
}

.loading-hint {
  text-align: center;
  color: #98a2b3;
  padding: 40px 0;
}

.section {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  margin-bottom: 24px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #1d2939;
  margin: 0 0 20px 0;
}

.steps-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 20px;
}

.step-card {
  flex: 1;
  text-align: center;
  padding: 20px 12px;
  background: #f9fafb;
  border-radius: 10px;
  position: relative;
}

.step-num {
  position: absolute;
  top: 10px;
  left: 14px;
  width: 22px;
  height: 22px;
  background: #4f46e5;
  color: #fff;
  border-radius: 50%;
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.step-icon { font-size: 28px; margin-bottom: 8px; }
.step-title { font-size: 14px; font-weight: 600; color: #1d2939; margin-bottom: 4px; }
.step-desc { font-size: 12px; color: #667085; line-height: 1.5; }

.step-arrow {
  font-size: 20px;
  color: #c7d2fe;
  font-weight: 700;
  flex-shrink: 0;
}

.btn-start {
  display: block;
  margin: 0 auto;
  padding: 10px 32px;
  background: #4f46e5;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-start:hover { background: #4338ca; }

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.activity-item {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  border-radius: 6px;
  font-size: 13px;
  transition: background 0.15s;
}

.activity-item:hover { background: #f9fafb; }

.activity-name {
  flex: 1;
  color: #344054;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-right: 12px;
}

.activity-status {
  font-weight: 500;
  margin-right: 16px;
  flex-shrink: 0;
}

.activity-time {
  color: #98a2b3;
  font-size: 12px;
  flex-shrink: 0;
}

@media (max-width: 768px) {
  .stats-row { grid-template-columns: repeat(2, 1fr); }
  .steps-row { flex-direction: column; }
  .step-arrow { transform: rotate(90deg); }
}
</style>
