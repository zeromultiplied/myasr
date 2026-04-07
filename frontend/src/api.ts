export interface TaskResult {
  task: string
  result: string
}

export interface TaskRecord {
  id: number
  filename: string
  status: string
  order_id: string | null
  task_types: string[]
  llm_provider: string | null
  llm_model: string | null
  transcription: string | null
  asr_raw_result: string | null
  results: TaskResult[] | null
  error: string | null
  created_at: string
  updated_at: string
}

export async function submitAudio(
  file: File,
  tasks: string[],
  llmProvider?: string,
  llmModel?: string,
): Promise<{ task_id: number; status: string }> {
  const form = new FormData()
  form.append('file', file)
  form.append('tasks', tasks.join(','))
  if (llmProvider) form.append('llm_provider', llmProvider)
  if (llmModel) form.append('llm_model', llmModel)

  const resp = await fetch('/api/v1/submit', { method: 'POST', body: form })
  if (!resp.ok) {
    const err = await resp.json().catch(() => ({ detail: resp.statusText }))
    throw new Error(err.detail || '提交失败')
  }
  return resp.json()
}

export async function fetchTasks(): Promise<TaskRecord[]> {
  const resp = await fetch('/api/v1/tasks')
  if (!resp.ok) throw new Error('获取任务列表失败')
  return resp.json()
}

export async function fetchTask(taskId: number): Promise<TaskRecord> {
  const resp = await fetch(`/api/v1/tasks/${taskId}`)
  if (!resp.ok) throw new Error('获取任务详情失败')
  return resp.json()
}

export async function deleteTask(taskId: number): Promise<void> {
  const resp = await fetch(`/api/v1/tasks/${taskId}`, { method: 'DELETE' })
  if (!resp.ok) throw new Error('删除失败')
}

export async function retryTask(taskId: number): Promise<{ task_id: number; status: string }> {
  const resp = await fetch(`/api/v1/tasks/${taskId}/retry`, { method: 'POST' })
  if (!resp.ok) {
    const err = await resp.json().catch(() => ({ detail: resp.statusText }))
    throw new Error(err.detail || '重试失败')
  }
  return resp.json()
}

export async function reanalyzeTask(
  taskId: number,
  tasks: string[],
  llmProvider?: string,
  llmModel?: string,
): Promise<{ task_id: number; status: string }> {
  const resp = await fetch(`/api/v1/tasks/${taskId}/reanalyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      tasks: tasks.join(','),
      llm_provider: llmProvider || null,
      llm_model: llmModel || null,
    }),
  })
  if (!resp.ok) {
    const err = await resp.json().catch(() => ({ detail: resp.statusText }))
    throw new Error(err.detail || '重新分析失败')
  }
  return resp.json()
}

export interface StatsData {
  total: number
  done: number
  failed: number
  processing: number
  recent: { id: number; filename: string; status: string; created_at: string; updated_at: string }[]
}

export async function fetchStats(): Promise<StatsData> {
  const resp = await fetch('/api/v1/stats')
  if (!resp.ok) throw new Error('获取统计数据失败')
  return resp.json()
}

export async function saveToServer(data: {
  transcription: string
  results: TaskResult[]
  filename: string
}): Promise<{ path: string }> {
  const resp = await fetch('/api/v1/save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!resp.ok) {
    const err = await resp.json().catch(() => ({ detail: resp.statusText }))
    throw new Error(err.detail || '保存失败')
  }
  return resp.json()
}

export function downloadAsMarkdown(
  transcription: string,
  results: TaskResult[],
  filename: string,
) {
  const taskNames: Record<string, string> = {
    summarize: '文本总结',
    expand: '内容发散',
    polish: '文本润色',
    action_items: '行动项提取',
  }

  let md = `# ${filename} - 语音处理结果\n\n`
  md += `## 原始转写\n\n${transcription}\n\n`
  for (const r of results) {
    md += `## ${taskNames[r.task] || r.task}\n\n${r.result}\n\n`
  }

  const blob = new Blob([md], { type: 'text/markdown;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${filename.replace(/\.[^.]+$/, '')}_result.md`
  a.click()
  URL.revokeObjectURL(url)
}
