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
  uploading: 'var(--charcoal-82)',
  transcribing: 'var(--charcoal-82)',
  llm_processing: 'var(--charcoal-82)',
  done: 'var(--charcoal-83)',
  failed: 'var(--charcoal-83)',
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
  padding: 24px;
}

.page-title {
  font-size: 1.375rem;
  font-weight: 600;
  color: var(--charcoal);
  margin: 0 0 var(--space-5) 0;
  letter-spacing: -0.02em;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-3);
  margin-bottom: var(--space-6);
}

.stat-card {
  background: var(--cream);
  border-radius: var(--radius-card);
  padding: var(--space-4);
  text-align: center;
  border: 1px solid var(--border-light);
  border-left: 4px solid var(--charcoal-40);
}

.stat-card.done { border-left-color: var(--charcoal-40); }
.stat-card.processing { border-left-color: var(--charcoal-40); }
.stat-card.failed { border-left-color: var(--charcoal-40); }

.stat-num {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--charcoal);
  margin-bottom: 4px;
  letter-spacing: -0.02em;
}

.stat-label {
  font-size: 0.813rem;
  color: var(--muted);
}

.loading-hint {
  text-align: center;
  color: var(--muted);
  padding: 40px 0;
}

.section {
  background: var(--cream);
  border-radius: var(--radius-card);
  padding: var(--space-5);
  border: 1px solid var(--border-light);
  margin-bottom: var(--space-4);
}

.section-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--charcoal);
  margin: 0 0 var(--space-4) 0;
}

.steps-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: var(--space-4);
}

.step-card {
  flex: 1;
  text-align: center;
  padding: var(--space-4) 12px;
  background: var(--charcoal-3);
  border-radius: var(--radius-compact);
  position: relative;
}

.step-num {
  position: absolute;
  top: 10px;
  left: 14px;
  width: 22px;
  height: 22px;
  background: var(--charcoal);
  color: var(--off-white);
  border-radius: 50%;
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
}

.step-icon { font-size: 1.75rem; margin-bottom: 8px; }
.step-title { font-size: 0.875rem; font-weight: 600; color: var(--charcoal); margin-bottom: 4px; }
.step-desc { font-size: 0.75rem; color: var(--muted); line-height: 1.5; }

.step-arrow {
  font-size: 1.25rem;
  color: var(--charcoal-40);
  font-weight: 600;
  flex-shrink: 0;
}

.btn-start {
  display: block;
  margin: 0 auto;
  padding: 10px 32px;
  background: var(--charcoal);
  color: var(--off-white);
  border: none;
  border-radius: var(--radius-std);
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.15s;
  box-shadow: var(--btn-inset);
}

.btn-start:hover { opacity: 0.85; }

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.activity-item {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  border-radius: var(--radius-micro);
  font-size: 0.813rem;
  transition: background 0.15s;
}

.activity-item:hover { background: var(--charcoal-4); }

.activity-name {
  flex: 1;
  color: var(--charcoal);
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
  color: var(--muted);
  font-size: 0.75rem;
  flex-shrink: 0;
}

@media (max-width: 768px) {
  .stats-row { grid-template-columns: repeat(2, 1fr); }
  .steps-row { flex-direction: column; }
  .step-arrow { transform: rotate(90deg); }
}
</style>
