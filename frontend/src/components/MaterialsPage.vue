<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  fetchMaterials,
  fetchMaterial,
  deleteMaterial,
  downloadMaterial,
  type MaterialItem,
  type MaterialsData,
} from '../api'

const items = ref<MaterialItem[]>([])
const total = ref(0)
const loading = ref(true)
const search = ref('')
const limit = 20
const offset = ref(0)
const detail = ref<MaterialItem | null>(null)
const showDetail = ref(false)

onMounted(() => loadData())

async function loadData() {
  loading.value = true
  try {
    const data: MaterialsData = await fetchMaterials(search.value || undefined, limit, offset.value)
    items.value = data.items
    total.value = data.total
  } catch (e) {
    console.error('Failed to load materials:', e)
  } finally {
    loading.value = false
  }
}

function onSearch() {
  offset.value = 0
  loadData()
}

function onClear() {
  search.value = ''
  offset.value = 0
  loadData()
}

async function onDelete(id: number) {
  if (!confirm('确定删除该资料？')) return
  try {
    await deleteMaterial(id)
    if (detail.value?.id === id) {
      detail.value = null
      showDetail.value = false
    }
    loadData()
  } catch (e: any) {
    alert(e.message)
  }
}

async function onView(id: number) {
  try {
    detail.value = await fetchMaterial(id)
    showDetail.value = true
  } catch (e: any) {
    alert(e.message)
  }
}

function onDownload(id: number, filename: string) {
  downloadMaterial(id, filename)
}

function closeDetail() {
  showDetail.value = false
  detail.value = null
}

function prevPage() {
  if (offset.value >= limit) {
    offset.value -= limit
    loadData()
  }
}

function nextPage() {
  if (offset.value + limit < total.value) {
    offset.value += limit
    loadData()
  }
}

function formatTime(iso: string): string {
  const d = new Date(iso)
  return d.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function truncate(text: string, max = 80): string {
  if (text.length <= max) return text
  return text.slice(0, max) + '...'
}
</script>

<template>
  <div class="materials-page">
    <h2 class="page-title">资料管理</h2>

    <!-- Search -->
    <div class="search-bar">
      <input
        v-model="search"
        type="text"
        placeholder="搜索文件名或内容..."
        @keyup.enter="onSearch"
      />
      <button class="btn-search" @click="onSearch">搜索</button>
      <button v-if="search" class="btn-clear" @click="onClear">清除</button>
    </div>

    <!-- Stats -->
    <div class="total-bar">
      共 <strong>{{ total }}</strong> 条资料
    </div>

    <!-- List -->
    <div v-if="loading" class="loading-hint">加载中...</div>
    <div v-else-if="!items.length" class="empty-hint">暂无保存的资料</div>

    <div v-else class="materials-list">
      <div
        v-for="item in items"
        :key="item.id"
        class="material-item"
      >
        <div class="item-main" @click="onView(item.id)">
          <div class="item-name">{{ item.filename }}</div>
          <div class="item-preview">{{ truncate(item.transcription_preview) }}</div>
          <div class="item-time">{{ formatTime(item.created_at) }}</div>
        </div>
        <div class="item-actions">
          <button class="btn-dl" @click.stop="onDownload(item.id, item.filename)" title="下载">⬇</button>
          <button class="btn-del" @click.stop="onDelete(item.id)" title="删除">✕</button>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="total > limit" class="pagination">
      <button :disabled="offset === 0" @click="prevPage">上一页</button>
      <span>{{ Math.floor(offset / limit) + 1 }} / {{ Math.ceil(total / limit) }}</span>
      <button :disabled="offset + limit >= total" @click="nextPage">下一页</button>
    </div>

    <!-- Detail modal -->
    <div v-if="showDetail && detail" class="modal-overlay" @click.self="closeDetail">
      <div class="modal-card">
        <div class="modal-header">
          <h3>{{ detail.filename }}</h3>
          <button class="btn-close" @click="closeDetail">✕</button>
        </div>
        <div class="modal-body">
          <pre class="detail-text">{{ detail.transcription }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.materials-page {
  max-width: 860px;
  margin: 0 auto;
  padding: 24px;
}

.page-title {
  font-size: 1.375rem;
  font-weight: 600;
  color: var(--charcoal);
  margin: 0 0 var(--space-4) 0;
  letter-spacing: -0.02em;
}

.search-bar {
  display: flex;
  gap: 8px;
  margin-bottom: var(--space-3);
}

.search-bar input {
  flex: 1;
  padding: 8px 12px;
  font-size: 0.875rem;
}

.btn-search {
  padding: 8px 16px;
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

.btn-search:hover { opacity: 0.85; }

.btn-clear {
  padding: 8px 12px;
  background: none;
  border: 1px solid var(--border-light);
  border-radius: var(--radius-std);
  font-size: 0.813rem;
  color: var(--muted);
  cursor: pointer;
}

.btn-clear:hover {
  background: var(--charcoal-4);
}

.total-bar {
  font-size: 0.813rem;
  color: var(--muted);
  margin-bottom: var(--space-3);
}

.loading-hint, .empty-hint {
  text-align: center;
  color: var(--muted);
  font-size: 0.875rem;
  padding: 40px 0;
}

.materials-list {
  display: flex;
  flex-direction: column;
  gap: 1px;
  background: var(--border-light);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-card);
  overflow: hidden;
}

.material-item {
  display: flex;
  align-items: center;
  background: var(--cream);
  padding: 12px 16px;
  gap: 12px;
}

.item-main {
  flex: 1;
  cursor: pointer;
  border-radius: var(--radius-micro);
  min-width: 0;
}

.item-main:hover .item-name {
  opacity: 0.7;
}

.item-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--charcoal);
  margin-bottom: 2px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-preview {
  font-size: 0.75rem;
  color: var(--muted);
  margin-bottom: 2px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-time {
  font-size: 0.688rem;
  color: var(--charcoal-40);
}

.item-actions {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
}

.btn-dl, .btn-del {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.813rem;
  padding: 4px 6px;
  border-radius: var(--radius-micro);
  color: var(--charcoal-40);
  transition: background 0.15s, color 0.15s;
}

.btn-dl:hover { background: var(--charcoal-4); color: var(--charcoal); }
.btn-del:hover { background: var(--charcoal-4); color: var(--charcoal-83); }

/* Pagination */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: var(--space-4);
  font-size: 0.813rem;
  color: var(--muted);
}

.pagination button {
  padding: 6px 14px;
  border: 1px solid var(--border-light);
  border-radius: var(--radius-std);
  background: var(--cream);
  font-size: 0.813rem;
  cursor: pointer;
  color: var(--charcoal);
  transition: background 0.15s;
}

.pagination button:hover:not(:disabled) { background: var(--charcoal-4); }
.pagination button:disabled { opacity: 0.4; cursor: not-allowed; }

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(28, 28, 28, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal-card {
  background: var(--cream);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-card);
  width: 700px;
  max-width: 90vw;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-light);
}

.modal-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.btn-close {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  color: var(--muted);
  padding: 4px 8px;
  border-radius: var(--radius-micro);
}

.btn-close:hover { background: var(--charcoal-4); color: var(--charcoal); }

.modal-body {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.detail-text {
  font-family: inherit;
  font-size: 0.875rem;
  line-height: 1.7;
  color: var(--charcoal-82);
  white-space: pre-wrap;
  word-break: break-word;
  margin: 0;
}

@media (max-width: 768px) {
  .material-item { flex-direction: column; align-items: stretch; }
  .item-actions { justify-content: flex-end; }
}
</style>
