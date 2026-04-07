# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

MyASR — 语音转文字 + LLM文本处理 API。上传音频文件，通过科大讯飞ASR转写为文本，再经LLM进行总结/发散/润色/行动项提取。

## Build & Run

```bash
# 安装依赖 (需要 Python 3.12+)
python3.12 -m pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入讯飞和LLM的API密钥

# 启动服务
python3.12 main.py
# 服务运行在 http://localhost:8000
```

## Architecture

```
main.py                → FastAPI 入口
app/config.py          → pydantic-settings 配置 (.env)
app/models.py          → 请求/响应 Pydantic 模型
app/routes/process.py  → POST /api/v1/process, /process/stream
app/routes/health.py   → GET /api/v1/health
app/asr/               → ASR Provider 模式 (讯飞实现)
app/llm/               → LLM Provider 模式 (OpenAI/Claude/Ollama)
app/tasks/prompts.py   → 4种任务的 Prompt 模板
app/services/pipeline.py → ASR→LLM 编排
```

Key patterns:
- Provider 抽象基类 + 工厂函数 (ASR, LLM)
- 异步全链路 (httpx + async SDK)
- SSE 流式输出
