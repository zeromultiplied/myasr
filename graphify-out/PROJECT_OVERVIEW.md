# MyASR 项目概述

## 项目简介

**MyASR** 是一款私有化部署的语音处理工具，支持将音频文件转写为文字，并通过大语言模型（LLM）进行智能文本处理。

## 核心功能

| 功能 | 说明 |
|------|------|
| 语音转写 | 基于科大讯飞非实时转写 API（v2），支持 mp3、wav、flac、opus、m4a 等格式，最长 5 小时音频 |
| 文本总结 | 自动提炼语音内容的核心要点 |
| 内容发散 | 基于原文进行延伸思考和扩展 |
| 文本润色 | 优化文字表达，提升可读性 |
| 行动项提取 | 从会议/对话中提取待办事项 |
| 多 LLM 支持 | 支持 OpenAI（含兼容 API）、Anthropic Claude、Ollama 本地模型 |
| 任务管理 | 异步任务队列，支持重试、重新分析、结果导出 |

## 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                         前端 (Vue 3)                         │
│   HomePage / TranscribePage / AudioUpload / TaskList        │
└─────────────────────────────────────────────────────────────┘
                              │
                         FastAPI
                              │
┌─────────────────────────────────────────────────────────────┐
│                        路由层 (routes)                       │
│   process.py: /api/v1/submit, /tasks, /retry, /reanalyze    │
│   health.py: /api/v1/health                                 │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                       服务层 (services)                      │
│   pipeline.py: ASR→LLM 编排                                │
└─────────────────────────────────────────────────────────────┘
                              │
┌──────────────────┐    ┌──────────────────────────────────────┐
│   ASR 层 (asr/)  │    │           LLM 层 (llm/)             │
│   xfyun.py       │    │  openai / anthropic / ollama        │
└──────────────────┘    └──────────────────────────────────────┘
```

## 项目结构

```
myasr/
├── main.py                    # FastAPI 应用入口
├── app/
│   ├── config.py              # pydantic-settings 配置管理
│   ├── models.py              # Pydantic 数据模型
│   ├── db.py                  # SQLite 数据层 (WAL mode)
│   ├── db_postgres.py         # Postgres 数据层 (Vercel 部署)
│   ├── routes/
│   │   ├── process.py         # 核心 API 路由 (提交/查询/重试/导出)
│   │   └── health.py          # 健康检查
│   ├── asr/
│   │   ├── base.py            # ASR 抽象基类
│   │   ├── factory.py         # ASR Provider 工厂
│   │   └── xfyun.py           # 科大讯飞实现
│   ├── llm/
│   │   ├── base.py            # LLM 抽象基类
│   │   ├── factory.py         # LLM Provider 工厂
│   │   ├── openai_provider.py # OpenAI GPT 实现
│   │   ├── anthropic_provider.py # Claude 实现
│   │   └── ollama_provider.py # Ollama 本地模型实现
│   └── tasks/
│       └── prompts.py         # LLM Prompt 模板 (4种任务)
├── frontend/                  # Vue 3 前端
│   └── src/components/        # 组件目录
├── data/                      # SQLite 数据库
├── output/                    # 导出结果文件
└── .env.example               # 环境变量示例
```

## 数据模型

### TaskType (任务类型枚举)

```
summarize    → 文本总结
expand       → 内容发散
polish       → 文本润色
action_items → 行动项提取
```

### 任务状态流转

```
uploading → transcribing → llm_processing → done / failed
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/submit` | 提交音频文件进行转写 |
| GET | `/api/v1/tasks` | 获取任务列表 |
| GET | `/api/v1/tasks/{id}` | 获取任务详情 |
| DELETE | `/api/v1/tasks/{id}` | 删除任务 |
| POST | `/api/v1/tasks/{id}/retry` | 重试失败任务 |
| POST | `/api/v1/tasks/{id}/reanalyze` | 重新运行 LLM 分析 |
| GET | `/api/v1/stats` | 获取统计数据 |
| POST | `/api/v1/save` | 保存结果到服务器 |
| GET | `/api/v1/health` | 健康检查 |

## LLM Prompt 设计

### 文本总结 (summarize)
- 提取核心要点，按重要性排列
- 保留关键数据、人名、时间等重要信息
- 先给出一句话概要，再列出分条要点

### 内容发散 (expand)
- 围绕核心主题，提出 3-5 个延伸方向
- 每个方向给出具体思路和建议
- 鼓励创新性思考，保持与原文相关性

### 文本润色 (polish)
- 修正语音识别的错别字和语法错误
- 优化口语化表达，使其更书面化
- 保留原文核心意思，不增删内容

### 行动项提取 (action_items)
- 识别所有待办事项、决策、承诺
- 包含具体内容、负责人、截止时间
- 使用清单格式输出（- [ ] 格式）

## 配置项

### ASR (科大讯飞)
```
XFYUN_APP_ID=        # 讯飞应用 ID
XFYUN_SECRET_KEY=   # 讯飞密钥
```

### LLM Provider
```
DEFAULT_LLM_PROVIDER=openai|anthropic|ollama

# OpenAI
OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o

# Anthropic
ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=claude-sonnet-4-20250514

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

### 应用配置
```
LOG_LEVEL=INFO
MAX_AUDIO_SIZE_MB=500
ASR_POLL_INTERVAL_SEC=3
ASR_POLL_TIMEOUT_SEC=120
```

## 处理流程

```
用户上传音频
     ↓
提交到 /api/v1/submit，返回 task_id
     ↓
后台异步处理:
  1. 上传到科大讯飞 ASR
  2. 轮询获取转写结果
  3. 调用 LLM 执行选定任务
     ↓
任务完成，用户查询 /api/v1/tasks/{id} 获取结果
     ↓
可选择保存到 /api/v1/save (JSON + Markdown)
```

## 部署方式

### 本地部署
```bash
python3.12 main.py
# 服务运行在 http://localhost:8000
```

### Vercel 部署
- 自动切换到 Postgres 数据库
- 使用 `api/` 目录下的 Serverless Functions
- 前端构建后静态托管

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3.12 / FastAPI / Uvicorn / httpx |
| 前端 | Vue 3 / TypeScript / Vite |
| ASR | 科大讯飞非实时转写 v2 API |
| LLM | OpenAI / Anthropic Claude / Ollama |
| 数据库 | SQLite (WAL mode) / Postgres |
