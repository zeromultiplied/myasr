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
    <div class="welcome-bar">
      <h2 class="page-title">欢迎使用 MyASR</h2>
      <p class="page-sub">语音转写，AI 赋能。上传音频，获取结构化洞察。</p>
    </div>

    <!-- Stats -->
    <div v-if="loading" class="loading-hint">加载中...</div>
    <div v-else-if="stats" class="stats-row">
      <div class="stat-card">
        <div class="stat-num">{{ stats.total }}</div>
        <div class="stat-label">总任务</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">{{ stats.done }}</div>
        <div class="stat-label">已完成</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">{{ stats.this_month }}</div>
        <div class="stat-label">本月新增</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">{{ stats.materials_count }}</div>
        <div class="stat-label">我的资料</div>
      </div>
    </div>

    <!-- Quick actions -->
    <div class="section">
      <h3 class="section-title">快捷操作</h3>
      <div class="actions-row">
        <button class="action-card" @click="$emit('navigate', 'transcribe')">
          <span class="action-icon">🎤</span>
          <span class="action-title">开始转写</span>
          <span class="action-desc">上传音频文件，语音转文字</span>
        </button>
        <button class="action-card" @click="$emit('navigate', 'materials')">
          <span class="action-icon">📄</span>
          <span class="action-title">我的资料</span>
          <span class="action-desc">查看已保存的转写结果</span>
        </button>
        <button class="action-card" @click="$emit('navigate', 'transcribe')">
          <span class="action-icon">📋</span>
          <span class="action-title">任务列表</span>
          <span class="action-desc">查看进行中的转写任务</span>
        </button>
      </div>
    </div>

    <!-- Usage steps -->
    <div class="section">
      <h3 class="section-title">使用步骤</h3>
      <div class="steps-row">
        <div class="step-card">
          <div class="step-num">1</div>
          <div class="step-icon">🎤</div>
          <div class="step-title">上传音频</div>
          <div class="step-desc">支持 wav / flac / opus / m4a / mp3</div>
        </div>
        <div class="step-arrow">→</div>
        <div class="step-card">
          <div class="step-num">2</div>
          <div class="step-icon">⏳</div>
          <div class="step-title">等待转写</div>
          <div class="step-desc">讯飞语音引擎自动转录</div>
        </div>
        <div class="step-arrow">→</div>
        <div class="step-card">
          <div class="step-num">3</div>
          <div class="step-icon">✨</div>
          <div class="step-title">查看结果</div>
          <div class="step-desc">LLM 自动总结、润色、发散、提取行动项</div>
        </div>
      </div>
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
          <span class="activity-status">{{ statusLabels[item.status] || item.status }}</span>
          <span class="activity-time">{{ formatTime(item.created_at) }}</span>
        </div>
      </div>
      <div v-if="!stats.recent.length" class="empty-hint">暂无记录，开始你的第一次转写吧</div>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  max-width: 860px;
  margin: 0 auto;
  padding: 24px;
}

.welcome-bar {
  margin-bottom: var(--space-5);
}

.page-title {
  font-size: 1.375rem;
  font-weight: 600;
  color: var(--charcoal);
  margin: 0 0 4px 0;
  letter-spacing: -0.02em;
}

.page-sub {
  font-size: 0.875rem;
  color: var(--muted);
  margin: 0;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-3);
  margin-bottom: var(--space-5);
}

.stat-card {
  background: var(--cream);
  border-radius: var(--radius-card);
  padding: var(--space-4);
  text-align: center;
  border: 1px solid var(--border-light);
}

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

.actions-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-3);
}

.action-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: var(--space-4) 12px;
  background: var(--charcoal-3);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-card);
  cursor: pointer;
  transition: background 0.15s;
  text-align: center;
}

.action-card:hover {
  background: var(--charcoal-4);
}

.action-icon {
  font-size: 1.5rem;
}

.action-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--charcoal);
}

.action-desc {
  font-size: 0.75rem;
  color: var(--muted);
  line-height: 1.4;
}

.steps-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
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
  font-size: 0.75rem;
  color: var(--muted);
  margin-right: 16px;
  flex-shrink: 0;
}

.activity-time {
  color: var(--muted);
  font-size: 0.75rem;
  flex-shrink: 0;
}

.empty-hint {
  text-align: center;
  color: var(--muted);
  font-size: 0.813rem;
  padding: var(--space-3) 0;
}

@media (max-width: 768px) {
  .stats-row { grid-template-columns: repeat(2, 1fr); }
  .actions-row { grid-template-columns: 1fr; }
  .steps-row { flex-direction: column; }
  .step-arrow { transform: rotate(90deg); }
}
</style>
