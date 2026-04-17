# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

MyASR — 语音转文字 + LLM文本处理 API。上传音频文件，通过科大讯飞ASR转写为文本，再经LLM进行总结/发散/润色/行动项提取。

## Build & Run

```bash
# 安装 uv (如未安装)
pip install uv

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入讯飞和LLM的API密钥

# 使用 uv 启动服务 (自动安装依赖)
uv run python main.py
# 服务运行在 http://localhost:8000

# 或手动安装依赖后启动
uv pip install -r requirements.txt
uv run python main.py
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

## Coding
### 1. 编码前先思考

**不要臆测。不要隐瞒困惑。明确权衡取舍。**

在着手实现之前：

- 明确陈述你的假设。如有不确定之处，请提问。
- 如果存在多种解读方式，请将其列出——不要默不作声地自行选择其一。
- 如果存在更简单的解决方案，请直言不讳。在必要时，应提出异议或反建议。
- 如果遇到任何不明确之处，请立即停下。明确指出困惑点所在，并提出疑问。

### 2. 简单至上

**仅编写解决问题所需的最低限度代码。杜绝任何臆测性的代码。**

- 不添加任何超出需求范围的功能特性。
- 不为仅供单次使用的代码强行引入抽象层。
- 不添加任何未经明确要求的“灵活性”或“可配置性”设计。
- 不为那些在逻辑上绝无可能发生的场景编写错误处理代码。
- 如果你写了 200 行代码，而实际上 50 行就能搞定，请毫不犹豫地重写。

问问自己：“一位资深工程师会认为这段代码过于复杂吗？”如果答案是肯定的，请将其简化。

### 3. 精准修改（Surgical Changes）

**只修改必须修改的部分。只清理你自己制造的“烂摊子”。**

在修改现有代码时：

- 不要顺手“优化”相邻的代码、注释或格式排版。
- 不要重构那些本身并未损坏或出错的代码。
- 保持与现有代码风格的一致，即使你个人偏好另一种风格。
- 如果你发现了一些与当前任务无关的“死代码”（无用代码），请在备注中提及，但不要将其删除。

当你的修改导致代码中出现“孤儿”（无引用代码）时：

- 删除那些因**你的**修改而变得不再被引用的导入、变量或函数。
- 除非被明确要求，否则不要删除那些在你的修改之前就已经存在的“死代码”。

检验标准：代码中修改的每一行，都应当能直接追溯到用户的具体需求或请求。

### 4. 目标导向的执行

**明确定义成功的标准。** **循环迭代，直至通过验证。**

将任务转化为可验证的目标：

- “添加验证” → “针对无效输入编写测试，然后确保测试通过”
- “修复 Bug” → “编写一个能重现该 Bug 的测试，然后确保测试通过”
- “重构 X” → “确保重构前后所有测试均能通过”

对于包含多个步骤的任务，请拟定一份简要的计划：

```
1. [步骤] → 验证方式：[检查项]
2. [步骤] → 验证方式：[检查项]
3. [步骤] → 验证方式：[检查项]
```

明确且强有力的成功标准，能让你独立自主地进行迭代工作；而模糊且薄弱的标准（例如“让它能跑起来就行”），则往往需要你反复寻求澄清。

---

**若出现以下迹象，则表明这些准则正在发挥实效：**代码变更对比（Diffs）中不再包含冗余的修改；因过度复杂化而导致的返工重写现象显著减少；且所有需要澄清的疑问都能在实际编码实现之前得到解答，而非等到犯错之后才去追问。

## UI DESIGN
按照`DESIGN.md`的UI设计规范开发前端页面


