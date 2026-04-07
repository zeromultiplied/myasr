<script setup lang="ts">
import type { TaskRecord } from '../api'
import { deleteTask } from '../api'

const props = defineProps<{
  tasks: TaskRecord[]
  activeId: number | null
}>()

const emit = defineEmits<{
  select: [task: TaskRecord]
  refresh: []
}>()

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

function formatTime(iso: string): string {
  const d = new Date(iso)
  return d.toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

async function onDelete(e: Event, taskId: number) {
  e.stopPropagation()
  if (!confirm('确定删除该任务？')) return
  await deleteTask(taskId)
  emit('refresh')
}
</script>

<template>
  <div class="task-list">
    <div class="list-header">
      <h3>录音任务</h3>
      <button class="btn-refresh" @click="$emit('refresh')" title="刷新">↻</button>
    </div>

    <div v-if="!tasks.length" class="empty">暂无任务</div>

    <div
      v-for="t in tasks"
      :key="t.id"
      class="task-item"
      :class="{ active: activeId === t.id }"
      @click="$emit('select', t)"
    >
      <div class="task-top">
        <span class="task-name" :title="t.filename">{{ t.filename }}</span>
        <button class="btn-del" @click="onDelete($event, t.id)" title="删除">✕</button>
      </div>
      <div class="task-bottom">
        <span
          class="task-status"
          :style="{ color: statusColors[t.status] || '#667085' }"
        >
          <span
            v-if="t.status !== 'done' && t.status !== 'failed'"
            class="dot-ani"
            :style="{ background: statusColors[t.status] }"
          ></span>
          {{ statusLabels[t.status] || t.status }}
        </span>
        <span class="task-time">{{ formatTime(t.created_at) }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.task-list {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 16px 12px;
  border-bottom: 1px solid #eaecf0;
}

.list-header h3 {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: #1d2939;
}

.btn-refresh {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
  color: #667085;
  padding: 4px;
  border-radius: 4px;
}

.btn-refresh:hover {
  background: #f2f4f7;
  color: #4f46e5;
}

.empty {
  padding: 32px 16px;
  text-align: center;
  color: #98a2b3;
  font-size: 14px;
}

.task-item {
  padding: 12px 16px;
  cursor: pointer;
  border-bottom: 1px solid #f2f4f7;
  transition: background 0.15s;
}

.task-item:hover {
  background: #f9fafb;
}

.task-item.active {
  background: #f0f0ff;
  border-left: 3px solid #4f46e5;
}

.task-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
}

.task-name {
  font-size: 13px;
  font-weight: 500;
  color: #344054;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 180px;
}

.btn-del {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 12px;
  color: #d0d5dd;
  padding: 2px 4px;
  border-radius: 3px;
  opacity: 0;
  transition: opacity 0.15s;
}

.task-item:hover .btn-del {
  opacity: 1;
}

.btn-del:hover {
  color: #ef4444;
  background: #fef3f2;
}

.task-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.task-status {
  font-size: 12px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

.dot-ani {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  animation: pulse 1.2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}

.task-time {
  font-size: 11px;
  color: #98a2b3;
}
</style>
