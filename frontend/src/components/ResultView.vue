<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { saveToServer, downloadAsMarkdown, type TaskRecord } from '../api'

const props = defineProps<{ task: TaskRecord | null }>()

const emit = defineEmits<{
  retry: [taskId: number]
  reanalyze: [payload: {
    taskId: number
    tasks: string[]
    llmProvider?: string
    llmModel?: string
  }]
}>()

const taskNames: Record<string, string> = {
  summarize: '文本总结',
  expand: '内容发散',
  polish: '文本润色',
  action_items: '行动项提取',
}

const statusLabels: Record<string, string> = {
  uploading: '正在上传音频到讯飞...',
  transcribing: '讯飞正在转写中，请稍候...',
  llm_processing: 'LLM 正在处理文本...',
  done: '处理完成',
  failed: '处理失败',
}

const activeTab = ref('')
const saving = ref(false)
const saveMsg = ref('')
const showReanalyze = ref(false)

const reanalyzeTasks = ref([
  { key: 'summarize', label: '文本总结', checked: true },
  { key: 'expand', label: '内容发散', checked: false },
  { key: 'polish', label: '文本润色', checked: false },
  { key: 'action_items', label: '行动项提取', checked: false },
])

const results = computed(() => props.task?.results || [])

watch(() => props.task, (t) => {
  if (t?.results?.length && !activeTab.value) {
    activeTab.value = t.results[0].task
  }
}, { immediate: true })

watch(results, (r) => {
  if (r.length && !r.find(x => x.task === activeTab.value)) {
    activeTab.value = r[0].task
  }
})

const activeResult = computed(() => {
  return results.value.find(r => r.task === activeTab.value)
})

async function onSaveServer() {
  if (!props.task?.transcription) return
  saving.value = true
  saveMsg.value = ''
  try {
    const res = await saveToServer({
      transcription: props.task.transcription,
      results: results.value,
      filename: props.task.filename,
    })
    saveMsg.value = `已保存到: ${res.path}`
  } catch (e: any) {
    saveMsg.value = `保存失败: ${e.message}`
  } finally {
    saving.value = false
  }
}

function onDownload() {
  if (!props.task?.transcription) return
  downloadAsMarkdown(props.task.transcription, results.value, props.task.filename)
}

function onRetry() {
  if (!props.task) return
  emit('retry', props.task.id)
}

function onReanalyze() {
  if (!props.task) return
  const selected = reanalyzeTasks.value.filter(t => t.checked).map(t => t.key)
  if (!selected.length) {
    alert('请至少选择一个处理任务')
    return
  }
  emit('reanalyze', {
    taskId: props.task.id,
    tasks: selected,
  })
  showReanalyze.value = false
}
</script>

<template>
  <div class="result-card" v-if="task">
    <div class="result-header">
      <h3>{{ task.filename }}</h3>
      <span
        class="status-badge"
        :class="task.status"
      >{{ statusLabels[task.status] || task.status }}</span>
    </div>

    <div v-if="task.error" class="error-bar">
      {{ task.error }}
      <button
        v-if="task.status === 'failed' && task.order_id"
        class="btn btn-retry"
        @click="onRetry"
      >重新查询转写结果</button>
    </div>

    <div v-if="task.status === 'uploading' || task.status === 'transcribing' || task.status === 'llm_processing'" class="loading-bar">
      <span class="loading-dot"></span>
      {{ statusLabels[task.status] }}
    </div>

    <div v-if="task.transcription" class="result-layout">
      <div class="result-left">
        <h4>原始转写</h4>
        <div class="text-box">{{ task.transcription }}</div>
      </div>

      <div class="result-right" v-if="results.length">
        <h4>处理结果</h4>
        <div class="tabs">
          <button
            v-for="r in results"
            :key="r.task"
            class="tab"
            :class="{ active: activeTab === r.task }"
            @click="activeTab = r.task"
          >{{ taskNames[r.task] || r.task }}</button>
        </div>
        <div class="text-box" v-if="activeResult">
          <pre>{{ activeResult.result }}</pre>
        </div>
      </div>
    </div>

    <div class="actions" v-if="task.status === 'done'">
      <button class="btn btn-primary" @click="onSaveServer" :disabled="saving">
        {{ saving ? '保存中...' : '保存到服务器' }}
      </button>
      <button class="btn btn-secondary" @click="onDownload">下载 Markdown</button>
      <button class="btn btn-secondary" @click="showReanalyze = !showReanalyze">
        {{ showReanalyze ? '取消' : '重新分析' }}
      </button>
      <span v-if="saveMsg" class="save-msg">{{ saveMsg }}</span>
    </div>

    <div v-if="showReanalyze && task.status === 'done'" class="reanalyze-panel">
      <div class="reanalyze-label">选择要重新执行的分析任务：</div>
      <div class="checkbox-row">
        <label v-for="t in reanalyzeTasks" :key="t.key" class="checkbox-item">
          <input type="checkbox" v-model="t.checked" />
          {{ t.label }}
        </label>
      </div>
      <button class="btn btn-primary" @click="onReanalyze">开始分析</button>
    </div>
  </div>

  <div v-else class="empty-state">
    <p>选择左侧任务查看详情，或提交新的音频文件</p>
  </div>
</template>

<style scoped>
.result-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.result-header h3 { margin: 0; font-size: 16px; color: #1d2939; }

.status-badge {
  font-size: 12px; font-weight: 500; padding: 3px 10px;
  border-radius: 12px;
}
.status-badge.done { background: #ecfdf5; color: #059669; }
.status-badge.failed { background: #fef3f2; color: #dc2626; }
.status-badge.uploading, .status-badge.transcribing, .status-badge.llm_processing {
  background: #f0f0ff; color: #4f46e5;
}

.error-bar {
  padding: 10px 14px; background: #fef3f2;
  border: 1px solid #fecdca; border-radius: 8px;
  color: #b42318; font-size: 13px; margin-bottom: 16px;
}

.loading-bar {
  display: flex; align-items: center; gap: 8px;
  padding: 14px 16px; background: #f0f0ff;
  border: 1px solid #c7d2fe; border-radius: 8px;
  color: #4f46e5; font-size: 14px;
}

.loading-dot {
  width: 8px; height: 8px; background: #4f46e5;
  border-radius: 50%; animation: pulse 1s infinite;
}

@keyframes pulse { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }

.result-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 16px;
}

@media (max-width: 768px) {
  .result-layout { grid-template-columns: 1fr; }
}

h4 { font-size: 14px; font-weight: 600; color: #1d2939; margin: 0 0 10px 0; }

.text-box {
  background: #f9fafb; border: 1px solid #eaecf0;
  border-radius: 8px; padding: 14px;
  min-height: 180px; max-height: 450px;
  overflow-y: auto; white-space: pre-wrap;
  line-height: 1.7; font-size: 13px; color: #344054;
}

.text-box pre {
  margin: 0; white-space: pre-wrap; font-family: inherit;
  line-height: 1.7; font-size: 13px; color: #344054;
}

.tabs {
  display: flex; gap: 2px; margin-bottom: 10px;
  border-bottom: 1px solid #eaecf0;
}

.tab {
  padding: 6px 14px; background: none; border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer; font-size: 13px; color: #667085; transition: all 0.2s;
}
.tab:hover { color: #4f46e5; }
.tab.active { color: #4f46e5; border-bottom-color: #4f46e5; font-weight: 600; }

.actions {
  display: flex; align-items: center; gap: 10px;
  margin-top: 18px; padding-top: 14px;
  border-top: 1px solid #eaecf0;
}

.btn {
  padding: 7px 18px; border-radius: 8px;
  font-size: 13px; font-weight: 600; cursor: pointer;
  border: none; transition: all 0.2s;
}
.btn-primary { background: #4f46e5; color: #fff; }
.btn-primary:hover:not(:disabled) { background: #4338ca; }
.btn-primary:disabled { background: #c7d2fe; cursor: not-allowed; }
.btn-secondary { background: #f2f4f7; color: #344054; border: 1px solid #d0d5dd; }
.btn-secondary:hover { background: #eaecf0; }

.save-msg { font-size: 12px; color: #667085; }

.btn-retry {
  margin-left: 12px;
  padding: 4px 12px;
  background: #4f46e5;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}
.btn-retry:hover { background: #4338ca; }

.reanalyze-panel {
  margin-top: 14px;
  padding: 16px;
  background: #f9fafb;
  border: 1px solid #eaecf0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.reanalyze-label {
  font-size: 13px;
  font-weight: 600;
  color: #344054;
}

.checkbox-row { display: flex; flex-wrap: wrap; gap: 12px; }

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 13px;
  color: #475467;
  cursor: pointer;
}

.reanalyze-panel .btn { align-self: flex-start; }

.empty-state {
  display: flex; align-items: center; justify-content: center;
  min-height: 300px; color: #98a2b3; font-size: 14px;
}
</style>
