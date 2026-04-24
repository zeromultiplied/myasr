// ====== Token management ======

let token: string | null = localStorage.getItem('myasr_token')

export function getToken(): string | null {
  return token
}

export function setToken(t: string) {
  token = t
  localStorage.setItem('myasr_token', t)
}

export function clearToken() {
  token = null
  localStorage.removeItem('myasr_token')
}

// ====== Auth headers ======

function authHeaders(): Record<string, string> {
  const h: Record<string, string> = {}
  if (token) h['Authorization'] = `Bearer ${token}`
  return h
}

// ====== Types ======

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
  user_id: number | null
  created_at: string
  updated_at: string
}

export interface StatsData {
  total: number
  done: number
  failed: number
  processing: number
  this_month: number
  materials_count: number
  recent: { id: number; filename: string; status: string; created_at: string; updated_at: string }[]
}

export interface MaterialItem {
  id: number
  user_id: number
  task_id: number | null
  filename: string
  transcription: string
  transcription_preview: string
  file_path: string | null
  created_at: string
}

export interface MaterialsData {
  items: MaterialItem[]
  total: number
  limit: number
  offset: number
}

export interface UserInfo {
  id: number
  username: string
  email?: string
}

// ====== Auth API ======

export async function register(username: string, password: string): Promise<{ token: string; user: UserInfo }> {
  const resp = await fetch('/api/v1/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })
  if (!resp.ok) {
    const err = await resp.json().catch(() => ({ detail: resp.statusText }))
    throw new Error(err.detail || '注册失败')
  }
  return resp.json()
}

export async function login(username: string, password: string): Promise<{ token: string; user: UserInfo }> {
  const resp = await fetch('/api/v1/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })
  if (!resp.ok) {
    const err = await resp.json().catch(() => ({ detail: resp.statusText }))
    throw new Error(err.detail || '登录失败')
  }
  return resp.json()
}

export async function fetchMe(): Promise<UserInfo> {
  const resp = await fetch('/api/v1/auth/me', { headers: authHeaders() })
  if (!resp.ok) throw new Error('获取用户信息失败')
  return resp.json()
}

export async function updateMe(data: {
  username?: string
  email?: string
  password?: string
}): Promise<UserInfo> {
  const resp = await fetch('/api/v1/auth/me', {
    method: 'PUT',
    headers: { ...authHeaders(), 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!resp.ok) {
    const err = await resp.json().catch(() => ({ detail: resp.statusText }))
    throw new Error(err.detail || '更新失败')
  }
  return resp.json()
}

// ====== Task API ======

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

  const resp = await fetch('/api/v1/submit', {
    method: 'POST',
    headers: authHeaders(),
    body: form,
  })
  if (!resp.ok) {
    const err = await resp.json().catch(() => ({ detail: resp.statusText }))
    throw new Error(err.detail || '提交失败')
  }
  return resp.json()
}

export async function fetchTasks(): Promise<TaskRecord[]> {
  const resp = await fetch('/api/v1/tasks', { headers: authHeaders() })
  if (!resp.ok) throw new Error('获取任务列表失败')
  return resp.json()
}

export async function fetchTask(taskId: number): Promise<TaskRecord> {
  const resp = await fetch(`/api/v1/tasks/${taskId}`, { headers: authHeaders() })
  if (!resp.ok) throw new Error('获取任务详情失败')
  return resp.json()
}

export async function deleteTask(taskId: number): Promise<void> {
  const resp = await fetch(`/api/v1/tasks/${taskId}`, {
    method: 'DELETE',
    headers: authHeaders(),
  })
  if (!resp.ok) throw new Error('删除失败')
}

export async function retryTask(taskId: number): Promise<{ task_id: number; status: string }> {
  const resp = await fetch(`/api/v1/tasks/${taskId}/retry`, {
    method: 'POST',
    headers: authHeaders(),
  })
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
    headers: { ...authHeaders(), 'Content-Type': 'application/json' },
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

export async function fetchStats(): Promise<StatsData> {
  const resp = await fetch('/api/v1/stats', { headers: authHeaders() })
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
    headers: { ...authHeaders(), 'Content-Type': 'application/json' },
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

// ====== Materials API ======

export async function fetchMaterials(
  search?: string,
  limit = 20,
  offset = 0,
): Promise<MaterialsData> {
  const params = new URLSearchParams()
  if (search) params.set('search', search)
  params.set('limit', String(limit))
  params.set('offset', String(offset))

  const resp = await fetch(`/api/v1/materials?${params}`, { headers: authHeaders() })
  if (!resp.ok) throw new Error('获取资料列表失败')
  return resp.json()
}

export async function fetchMaterial(id: number): Promise<MaterialItem> {
  const resp = await fetch(`/api/v1/materials/${id}`, { headers: authHeaders() })
  if (!resp.ok) throw new Error('获取资料详情失败')
  return resp.json()
}

export async function deleteMaterial(id: number): Promise<void> {
  const resp = await fetch(`/api/v1/materials/${id}`, {
    method: 'DELETE',
    headers: authHeaders(),
  })
  if (!resp.ok) throw new Error('删除失败')
}

export async function downloadMaterial(id: number, filename: string): Promise<void> {
  const resp = await fetch(`/api/v1/materials/${id}/download`, { headers: authHeaders() })
  if (!resp.ok) throw new Error('下载失败')
  const text = await resp.text()
  const blob = new Blob([text], { type: 'text/markdown;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename.replace(/\.[^.]+$/, '') + '_result.md'
  a.click()
  URL.revokeObjectURL(url)
}
