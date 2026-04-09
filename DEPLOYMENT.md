# MyASR 部署到 Vercel 指南

## 环境变量配置

在 Vercel 控制台中配置以下环境变量：

### ASR 配置 (科大讯飞)
- `XFYUN_APP_ID`: 讯飞应用 ID
- `XFYUN_SECRET_KEY`: 讯飞密钥

### LLM 提供商配置 (至少配置一个)

#### OpenAI
- `OPENAI_API_KEY`: OpenAI API 密钥
- `OPENAI_BASE_URL`: OpenAI API 地址 (默认: https://api.openai.com/v1)
- `OPENAI_MODEL`: 使用的模型 (默认: gpt-4o)

#### Anthropic
- `ANTHROPIC_API_KEY`: Anthropic API 密钥
- `ANTHROPIC_MODEL`: 使用的模型 (默认: claude-sonnet-4-20250514)

#### Ollama
- `OLLAMA_BASE_URL`: Ollama 服务地址 (默认: http://localhost:11434)
- `OLLAMA_MODEL`: 使用的模型 (默认: llama3)

### 默认 LLM 提供商
- `DEFAULT_LLM_PROVIDER`: 默认提供商 (openai | anthropic | ollama)

### 应用配置
- `LOG_LEVEL`: 日志级别 (默认: INFO)
- `MAX_AUDIO_SIZE_MB`: 最大音频文件大小 (默认: 500MB)
- `ASR_POLL_INTERVAL_SEC`: ASR 轮询间隔 (默认: 3秒)
- `ASR_POLL_TIMEOUT_SEC`: ASR 轮询超时 (默认: 120秒)

### 数据库配置 (Vercel Postgres)
- `POSTGRES_URL`: Vercel Postgres 连接字符串 (自动提供)
- 或 `DATABASE_URL`: 备用数据库连接字符串

## 部署步骤

1. **连接 Vercel Postgres**
   - 在 Vercel 控制台创建 Postgres 数据库
   - 数据库连接字符串会自动注入为 `POSTGRES_URL`

2. **配置环境变量**
   - 在 Vercel 项目设置中添加所有必需的 API 密钥

3. **部署项目**
   ```bash
   # 安装 Vercel CLI
   npm i -g vercel
   
   # 登录并部署
   vercel login
   vercel --prod
   ```

4. **验证部署**
   - 访问健康检查端点: `/api/v1/health`
   - 测试语音处理功能

## 本地开发

对于本地开发，使用 SQLite 数据库：

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

## 故障排除

### 数据库连接问题
- 确保 Vercel Postgres 已正确配置
- 检查 `POSTGRES_URL` 环境变量

### API 密钥问题
- 确认所有必需的 API 密钥都已配置
- 检查密钥权限和配额

### 文件上传限制
- Vercel 有 4.5MB 的请求体限制
- 大文件需要考虑分片上传或外部存储