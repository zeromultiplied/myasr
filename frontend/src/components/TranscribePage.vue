<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import AudioUpload from './AudioUpload.vue'
import TaskListVue from './TaskList.vue'
import ResultView from './ResultView.vue'
import {
  submitAudio,
  fetchTasks,
  fetchTask,
  retryTask,
  reanalyzeTask,
  type TaskRecord,
} from '../api'

const tasks = ref<TaskRecord[]>([])
const activeTask = ref<TaskRecord | null>(null)
const activeId = ref<number | null>(null)
const submitting = ref(false)
const error = ref('')

let detailPollTimer: number | null = null

onMounted(() => {
  refreshTaskList()
})

onUnmounted(() => {
  stopDetailPoll()
})

async function refreshTaskList() {
  try {
    tasks.value = await fetchTasks()
  } catch (e: any) {
    console.error('Failed to refresh tasks:', e)
  }
}

function startDetailPoll(taskId: number) {
  stopDetailPoll()
  detailPollTimer = window.setInterval(async () => {
    try {
      const t = await fetchTask(taskId)
      activeTask.value = t
      // Update in list too
      const idx = tasks.value.findIndex(x => x.id === taskId)
      if (idx >= 0) tasks.value[idx] = t
      // Stop if terminal
      if (t.status === 'done' || t.status === 'failed') {
        stopDetailPoll()
      }
    } catch {
      // ignore
    }
  }, 5000)
}

function stopDetailPoll() {
  if (detailPollTimer) {
    clearInterval(detailPollTimer)
    detailPollTimer = null
  }
}

async function onSelect(task: TaskRecord) {
  activeId.value = task.id
  stopDetailPoll()
  try {
    activeTask.value = await fetchTask(task.id)
  } catch {
    activeTask.value = task
  }
  // Start polling if still processing
  if (activeTask.value && activeTask.value.status !== 'done' && activeTask.value.status !== 'failed') {
    startDetailPoll(task.id)
  }
}

async function onSubmit(payload: {
  file: File
  tasks: string[]
  llmProvider: string
  llmModel: string
}) {
  submitting.value = true
  error.value = ''
  try {
    const res = await submitAudio(
      payload.file,
      payload.tasks,
      payload.llmProvider || undefined,
      payload.llmModel || undefined,
    )
    await refreshTaskList()
    const newTask = tasks.value.find(t => t.id === res.task_id)
    if (newTask) {
      activeId.value = newTask.id
      activeTask.value = newTask
      startDetailPoll(newTask.id)
    }
  } catch (e: any) {
    error.value = e.message
  } finally {
    submitting.value = false
  }
}

async function onRetry(taskId: number) {
  error.value = ''
  try {
    await retryTask(taskId)
    await refreshTaskList()
    const t = tasks.value.find(x => x.id === taskId)
    if (t) {
      activeTask.value = t
      startDetailPoll(taskId)
    }
  } catch (e: any) {
    error.value = e.message
  }
}

async function onReanalyze(payload: {
  taskId: number
  tasks: string[]
  llmProvider?: string
  llmModel?: string
}) {
  error.value = ''
  try {
    await reanalyzeTask(payload.taskId, payload.tasks, payload.llmProvider, payload.llmModel)
    await refreshTaskList()
    const t = tasks.value.find(x => x.id === payload.taskId)
    if (t) {
      activeTask.value = t
      startDetailPoll(payload.taskId)
    }
  } catch (e: any) {
    error.value = e.message
  }
}

async function onRefresh() {
  await refreshTaskList()
  if (activeId.value) {
    const updated = tasks.value.find(t => t.id === activeId.value)
    if (updated) activeTask.value = updated
  }
}
</script>

<template>
  <div class="transcribe-page">
    <div class="transcribe-sidebar">
      <TaskListVue
        :tasks="tasks"
        :active-id="activeId"
        @select="onSelect"
        @refresh="onRefresh"
      />
    </div>
    <div class="transcribe-main">
      <AudioUpload :loading="submitting" @submit="onSubmit" />

      <div v-if="error" class="error-bar">{{ error }}</div>

      <ResultView
        :task="activeTask"
        @retry="onRetry"
        @reanalyze="onReanalyze"
      />
    </div>
  </div>
</template>

<style scoped>
.transcribe-page {
  display: flex;
  height: 100%;
  gap: 0;
  background: var(--cream);
}

.transcribe-sidebar {
  width: 260px;
  min-width: 260px;
  background: var(--cream);
  border-right: 1px solid var(--border-light);
  overflow-y: auto;
}

.transcribe-main {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
  background: var(--cream);
}

.error-bar {
  padding: 10px 14px;
  background: var(--cream);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-std);
  color: var(--charcoal-83);
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .transcribe-page { flex-direction: column; }
  .transcribe-sidebar { width: 100%; min-width: 0; max-height: 200px; border-right: none; border-bottom: 1px solid var(--border-light); }
}
</style>
