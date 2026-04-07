<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  submit: [payload: {
    file: File
    tasks: string[]
    llmProvider: string
    llmModel: string
  }]
}>()

const props = defineProps<{ loading: boolean }>()

const file = ref<File | null>(null)
const isDragOver = ref(false)
const llmProvider = ref('')
const llmModel = ref('')

const tasks = ref([
  { key: 'summarize', label: '文本总结', checked: true },
  { key: 'expand', label: '内容发散', checked: false },
  { key: 'polish', label: '文本润色', checked: false },
  { key: 'action_items', label: '行动项提取', checked: false },
])

const allowedExts = ['.wav', '.flac', '.opus', '.m4a', '.mp3']

function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  if (input.files?.length) {
    validateAndSet(input.files[0])
  }
}

function onDrop(e: DragEvent) {
  isDragOver.value = false
  const f = e.dataTransfer?.files[0]
  if (f) validateAndSet(f)
}

function validateAndSet(f: File) {
  const ext = '.' + f.name.split('.').pop()?.toLowerCase()
  if (!allowedExts.includes(ext)) {
    alert(`不支持的格式: ${ext}\n支持: ${allowedExts.join(', ')}`)
    return
  }
  file.value = f
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

function submit() {
  if (!file.value) return
  const selected = tasks.value.filter(t => t.checked).map(t => t.key)
  if (!selected.length) {
    alert('请至少选择一个处理任务')
    return
  }
  emit('submit', {
    file: file.value,
    tasks: selected,
    llmProvider: llmProvider.value,
    llmModel: llmModel.value,
  })
  file.value = null
}
</script>

<template>
  <div class="upload-card">
    <div
      class="drop-zone"
      :class="{ 'drag-over': isDragOver, 'has-file': file }"
      @dragover.prevent="isDragOver = true"
      @dragleave="isDragOver = false"
      @drop.prevent="onDrop"
      @click="($refs.fileInput as HTMLInputElement).click()"
    >
      <input
        ref="fileInput"
        type="file"
        :accept="allowedExts.join(',')"
        hidden
        @change="onFileChange"
      />
      <div v-if="!file" class="drop-hint">
        <div class="drop-icon">🎤</div>
        <p>拖拽音频文件到此处，或点击选择</p>
        <p class="drop-sub">支持 wav / flac / opus / m4a / mp3</p>
      </div>
      <div v-else class="file-info">
        <span class="file-name">{{ file.name }}</span>
        <span class="file-size">{{ formatSize(file.size) }}</span>
        <button class="btn-clear" @click.stop="file = null">✕</button>
      </div>
    </div>

    <div class="options">
      <div class="option-group">
        <label class="group-label">处理任务</label>
        <div class="checkbox-row">
          <label v-for="t in tasks" :key="t.key" class="checkbox-item">
            <input type="checkbox" v-model="t.checked" />
            {{ t.label }}
          </label>
        </div>
      </div>

      <div class="option-row">
        <div class="option-group">
          <label class="group-label">LLM Provider</label>
          <select v-model="llmProvider">
            <option value="">默认</option>
            <option value="openai">OpenAI</option>
            <option value="anthropic">Anthropic</option>
            <option value="ollama">Ollama</option>
          </select>
        </div>
        <div class="option-group">
          <label class="group-label">Model</label>
          <input type="text" v-model="llmModel" placeholder="默认模型" />
        </div>
      </div>
    </div>

    <button
      class="btn-submit"
      :disabled="!file || loading"
      @click="submit"
    >
      {{ loading ? '提交中...' : '提交任务' }}
    </button>
  </div>
</template>

<style scoped>
.upload-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.drop-zone {
  border: 2px dashed #d0d5dd;
  border-radius: 8px;
  padding: 32px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.drop-zone:hover,
.drop-zone.drag-over {
  border-color: #4f46e5;
  background: #f0f0ff;
}

.drop-zone.has-file {
  border-style: solid;
  border-color: #4f46e5;
  padding: 16px 20px;
}

.drop-icon { font-size: 32px; margin-bottom: 6px; }
.drop-hint p { margin: 4px 0; color: #667085; font-size: 14px; }
.drop-sub { font-size: 12px !important; color: #98a2b3 !important; }

.file-info { display: flex; align-items: center; gap: 12px; }
.file-name { font-weight: 600; color: #1d2939; font-size: 14px; }
.file-size { color: #98a2b3; font-size: 13px; }

.btn-clear {
  margin-left: auto; background: none; border: none;
  cursor: pointer; font-size: 16px; color: #98a2b3;
  padding: 4px 8px; border-radius: 4px;
}
.btn-clear:hover { background: #f2f4f7; color: #667085; }

.options { margin-top: 16px; }
.option-group { margin-bottom: 10px; }

.group-label {
  display: block; font-size: 13px; font-weight: 600;
  color: #344054; margin-bottom: 6px;
}

.checkbox-row { display: flex; flex-wrap: wrap; gap: 12px; }

.checkbox-item {
  display: flex; align-items: center; gap: 5px;
  font-size: 13px; color: #475467; cursor: pointer;
}

.option-row { display: flex; gap: 12px; align-items: end; }

.option-row select, .option-row input[type="text"] {
  padding: 5px 8px; border: 1px solid #d0d5dd;
  border-radius: 6px; font-size: 13px; outline: none;
}

.option-row select:focus, .option-row input[type="text"]:focus {
  border-color: #4f46e5;
}

.btn-submit {
  margin-top: 16px; width: 100%; padding: 10px;
  background: #4f46e5; color: #fff; border: none;
  border-radius: 8px; font-size: 14px; font-weight: 600;
  cursor: pointer; transition: background 0.2s;
}

.btn-submit:hover:not(:disabled) { background: #4338ca; }
.btn-submit:disabled { background: #c7d2fe; cursor: not-allowed; }
</style>
