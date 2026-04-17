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
  background: var(--cream);
  border-radius: var(--radius-card);
  padding: var(--space-5);
  border: 1px solid var(--border-light);
}

.drop-zone {
  border: 2px dashed var(--charcoal-40);
  border-radius: var(--radius-std);
  padding: 32px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  background: var(--cream);
}

.drop-zone:hover,
.drop-zone.drag-over {
  border-color: var(--charcoal-40);
  background: var(--charcoal-3);
}

.drop-zone.has-file {
  border-style: solid;
  border-color: var(--charcoal-40);
  padding: 16px 20px;
}

.drop-icon { font-size: 2rem; margin-bottom: 6px; }
.drop-hint p { margin: 4px 0; color: var(--muted); font-size: 0.875rem; }
.drop-sub { font-size: 0.75rem !important; color: var(--charcoal-40) !important; }

.file-info { display: flex; align-items: center; gap: 12px; }
.file-name { font-weight: 600; color: var(--charcoal); font-size: 0.875rem; }
.file-size { color: var(--muted); font-size: 0.813rem; }

.btn-clear {
  margin-left: auto;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  color: var(--muted);
  padding: 4px 8px;
  border-radius: var(--radius-micro);
}
.btn-clear:hover { background: var(--charcoal-4); color: var(--charcoal); }

.options { margin-top: var(--space-3); }
.option-group { margin-bottom: 10px; }

.group-label {
  display: block;
  font-size: 0.813rem;
  font-weight: 600;
  color: var(--charcoal);
  margin-bottom: 6px;
}

.checkbox-row { display: flex; flex-wrap: wrap; gap: 12px; }

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.813rem;
  color: var(--charcoal-82);
  cursor: pointer;
}

.option-row { display: flex; gap: 12px; align-items: end; }

.option-row select, .option-row input[type="text"] {
  padding: 6px 10px;
  border: 1px solid var(--border-light);
  border-radius: var(--radius-std);
  font-size: 0.875rem;
  outline: none;
  background: var(--cream);
  color: var(--charcoal);
}

.option-row select:focus, .option-row input[type="text"]:focus {
  border-color: var(--charcoal-40);
  box-shadow: 0 0 0 3px var(--ring-blue);
}

.btn-submit {
  margin-top: var(--space-3);
  width: 100%;
  padding: 10px;
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

.btn-submit:hover:not(:disabled) { opacity: 0.85; }
.btn-submit:disabled { opacity: 0.4; cursor: not-allowed; }
</style>
