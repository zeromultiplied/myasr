# MyASR - 语音转写与智能分析

MyASR 是一款私有化部署的语音处理工具，支持将音频文件转写为文字，并通过大语言模型（LLM）进行智能文本处理。

## 功能特性

- **语音转写** — 基于科大讯飞非实时转写 API（v2），支持 mp3、wav、flac、opus、m4a 等格式，最长 5 小时音频
- **文本总结** — 自动提炼语音内容的核心要点
- **内容发散** — 基于原文进行延伸思考和扩展
- **文本润色** — 优化文字表达，提升可读性
- **行动项提取** — 从会议/对话中提取待办事项
- **多 LLM 支持** — 支持 OpenAI（含兼容 API）、Anthropic Claude、Ollama 本地模型
- **任务管理** — 异步任务队列，支持重试、重新分析、结果导出

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3.12 / FastAPI / Uvicorn |
| 前端 | Vue 3 / TypeScript / Vite |
| ASR | 科大讯飞非实时转写 v2 API |
| LLM | OpenAI / Anthropic / Ollama |
| 数据库 | SQLite (WAL mode) |

## 快速开始

### 环境要求

- Python 3.12+
- Node.js 18+（前端开发时需要）

### 安装

```bash
# 克隆项目
git clone <repo-url> myasr
cd myasr

# 安装 Python 依赖
python3.12 -m pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入讯飞 APP_ID/SECRET_KEY 和 LLM API 密钥
```

### 配置

编辑 `.env` 文件，至少需要配置：

```env
# 科大讯飞 ASR（必填）
XFYUN_APP_ID=your_app_id
XFYUN_SECRET_KEY=your_secret_key

# LLM Provider（三选一）
DEFAULT_LLM_PROVIDER=openai
OPENAI_API_KEY=sk-xxx
OPENAI_MODEL=gpt-4o
```

完整配置项参见 [.env.example](.env.example)。

### 启动

```bash
# 启动后端（默认端口 8000）
python3.12 main.py
```

访问 `http://localhost:8000` 即可使用 Web 界面。

### 前端开发

```bash
cd frontend
npm install
npm run dev    # 开发服务器（端口 5173，自动代理到后端）
npm run build  # 构建生产版本
```

## 项目结构

```
myasr/
├── main.py                    # 应用入口
├── app/
│   ├── config.py              # 配置管理 (pydantic-settings)
│   ├── models.py              # 数据模型
│   ├── db.py                  # SQLite 数据层
│   ├── routes/
│   │   ├── process.py         # 核心 API 路由
│   │   └── health.py          # 健康检查
│   ├── asr/
│   │   ├── base.py            # ASR 抽象基类
│   │   └── xfyun.py           # 科大讯飞实现
│   ├── llm/
│   │   ├── base.py            # LLM 抽象基类
│   │   ├── factory.py         # Provider 工厂
│   │   ├── openai_provider.py # OpenAI 实现
│   │   ├── anthropic_provider.py # Claude 实现
│   │   └── ollama_provider.py # Ollama 实现
│   └── tasks/
│       └── prompts.py         # LLM Prompt 模板
├── frontend/                  # Vue 3 前端
│   ├── src/
│   │   ├── App.vue            # 主布局（侧边栏导航）
│   │   ├── api.ts             # API 客户端
│   │   └── components/
│   │       ├── HomePage.vue       # 首页统计
│   │       ├── TranscribePage.vue # 转写页面
│   │       ├── AudioUpload.vue    # 音频上传
│   │       ├── TaskList.vue       # 任务列表
│   │       └── ResultView.vue     # 结果展示
│   └── vite.config.ts
├── data/                      # SQLite 数据库（自动创建）
├── output/                    # 导出结果文件
├── requirements.txt
└── .env.example
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

## 处理流程

```
上传音频 → 科大讯飞 ASR 转写 → LLM 文本处理 → 返回结果
                                  ├── 文本总结
                                  ├── 内容发散
                                  ├── 文本润色
                                  └── 行动项提取
```

任务状态流转：`uploading → transcribing → llm_processing → done / failed`

## License

[Apache License 2.0](LICENSE)
