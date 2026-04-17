# Graph Report - .  (2026-04-17)

## Corpus Check
- Corpus is ~17,889 words - fits in a single context window. You may not need a graph.

## Summary
- 159 nodes · 264 edges · 30 communities detected
- Extraction: 54% EXTRACTED · 46% INFERRED · 0% AMBIGUOUS · INFERRED: 121 edges (avg confidence: 0.62)
- Token cost: 10,006 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Frontend UI|Frontend UI]]
- [[_COMMUNITY_Backend API & Data|Backend API & Data]]
- [[_COMMUNITY_LLM Integration|LLM Integration]]
- [[_COMMUNITY_Documentation & Assets|Documentation & Assets]]
- [[_COMMUNITY_ASR & Pipeline|ASR & Pipeline]]
- [[_COMMUNITY_Pipeline Orchestration|Pipeline Orchestration]]
- [[_COMMUNITY_API Entry Points|API Entry Points]]
- [[_COMMUNITY_ASR Implementation|ASR Implementation]]
- [[_COMMUNITY_Configuration|Configuration]]
- [[_COMMUNITY_Frontend Docs|Frontend Docs]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]

## God Nodes (most connected - your core abstractions)
1. `TaskType` - 20 edges
2. `TranscribePage Component` - 18 edges
3. `TASK_PROMPTS` - 17 edges
4. `XfyunASRProvider` - 15 edges
5. `LLMProvider` - 15 edges
6. `Background Process Task` - 13 edges
7. `Process API Router` - 12 edges
8. `Background Retry Task` - 12 edges
9. `LLM Factory Function` - 10 edges
10. `TaskList Component` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Lightning Bolt Icon` --represents--> `MyASR Project`  [INFERRED]
  frontend/public/favicon.svg → CLAUDE.md
- `WebLFASR RequestApi Class` --alternative_reference--> `XfyunASRProvider Class`  [INFERRED]
  weblfasr_python3_demo.py → app/asr/xfyun.py
- `RequestApi Demo Class` --reference_implementation--> `XfyunASRProvider Class`  [INFERRED]
  Ifasr_new.py → app/asr/xfyun.py
- `Hero Banner Image` --used_in--> `TranscribePage Component`  [INFERRED]
  frontend/src/assets/hero.png → frontend/src/components/TranscribePage.vue
- `AI Integration Patterns` --relates_to--> `LLM Provider Pattern`  [INFERRED]
  output/agent_认知分享_20260407_044938.md → CLAUDE.md

## Hyperedges (group relationships)
- **Dual Database Backend Strategy** —  [INFERRED 0.85]
- **ASR-LLM Processing Pipeline** —  [EXTRACTED 1.00]
- **Background Task Async Flow** —  [EXTRACTED 1.00]
- **Provider Factory Pattern** —  [EXTRACTED 1.00]
- **LLM Streaming vs Non-streaming Pattern** —  [INFERRED 0.80]
- **TaskType Enum Binding to Prompts and Names** —  [EXTRACTED 1.00]
- **SSE Streaming Output Pattern** —  [EXTRACTED 1.00]
- **Pipeline Orchestration Flow** — pipeline_pipeline, base_asrprovider, base_llmprovider, prompts_taskprompts, tasktype, processresponse, taskresult [EXTRACTED 1.00]
- **Layered Config Fallback Pattern** —  [INFERRED 0.85]
- **Transcription pipeline orchestration** — pipeline_run_pipeline, pipeline_run_pipeline_stream, prompts_task_prompts, pipeline_sse_event [EXTRACTED 0.90]
- **Task list sidebar components** — tasklist_vue, tasklist_status_labels, tasklist_status_colors, tasklist_format_time, tasklist_on_delete [EXTRACTED 0.85]
- **TranscribePage state and polling** — transcribepage_refresh_task_list, transcribepage_start_detail_poll, transcribepage_stop_detail_poll, transcribepage_on_select [EXTRACTED 0.80]

## Communities

### Community 0 - "Frontend UI"
Cohesion: 0.09
Nodes (35): API Module, App Root Component, AudioUpload Component, Backend API Server, deleteTask Function, downloadAsMarkdown Function, fetchStats Function, fetchTask Function (+27 more)

### Community 1 - "Backend API & Data"
Cohesion: 0.21
Nodes (27): Create Task Function, Get Task Function, List Tasks Function, PostgreSQL Create Task, PostgreSQL Get Task, PostgreSQL List Tasks, PostgreSQL Update Task, Update Task Function (+19 more)

### Community 2 - "LLM Integration"
Cohesion: 0.18
Nodes (20): AnthropicLLMProvider, ASR Factory, LLMProvider, Settings Singleton, AnthropicProvider Class, Anthropic Generate Method, Anthropic Generate Stream Method, LLMProvider Abstract Class (+12 more)

### Community 3 - "Documentation & Assets"
Cohesion: 0.11
Nodes (19): ASR Provider Pattern, LLM Provider Pattern, MyASR Project, ASR-LLM Pipeline, SSE Streaming, Anthropic Configuration, Ollama Configuration, OpenAI Configuration (+11 more)

### Community 4 - "ASR & Pipeline"
Cohesion: 0.24
Nodes (12): ASRProvider Abstract Class, ASR Factory Function, XfyunASRProvider Class, RequestApi Demo Class, ProcessResponse Model, TaskResult Model, ProcessResponse, Run Pipeline Function (+4 more)

### Community 5 - "Pipeline Orchestration"
Cohesion: 0.57
Nodes (8): run_pipeline function, run_pipeline_stream function, _sse_event helper, Action items task prompt, Expand task prompt, Polish task prompt, Summarize task prompt, TASK_PROMPTS dictionary

### Community 6 - "API Entry Points"
Cohesion: 0.33
Nodes (6): Mangum Handler, SQLite Init DB, PostgreSQL Init DB, FastAPI App Instance, Main Application Entry, Health API Router

### Community 7 - "ASR Implementation"
Cohesion: 0.8
Nodes (5): XFyun Get Result Method, Parse Transcription Helper, XFyun Transcribe Method, XFyun Upload Method, ASRProvider

### Community 8 - "Configuration"
Cohesion: 0.67
Nodes (3): _get_conn, ConfigService, Settings

### Community 9 - "Frontend Docs"
Cohesion: 0.67
Nodes (3): Vue Script Setup Docs, Vue 3 + TypeScript + Vite, Vue TypeScript Guide

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (2): StatsData Data Structure, StatsData Interface

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (1): SliceIdGenerator Class

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (0): 

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (0): 

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (0): 

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (0): 

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (0): 

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (0): 

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (1): saveToServer Call

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (1): downloadAsMarkdown Call

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (1): deleteTask Call

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (1): SVG Icon Sprite

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (1): Bluesky Icon

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (1): Discord Icon

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (1): Documentation Icon

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): GitHub Icon

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (1): Social Icon

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (1): X (Twitter) Icon

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (1): Vite Framework Logo/Icon

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (1): TASK_NAMES dictionary

## Knowledge Gaps
- **53 isolated node(s):** `WebLFASR RequestApi Class`, `SliceIdGenerator Class`, `RequestApi Demo Class`, `Settings`, `_get_conn` (+48 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 10`** (2 nodes): `StatsData Data Structure`, `StatsData Interface`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (1 nodes): `SliceIdGenerator Class`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (1 nodes): `saveToServer Call`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (1 nodes): `downloadAsMarkdown Call`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `deleteTask Call`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `SVG Icon Sprite`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (1 nodes): `Bluesky Icon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (1 nodes): `Discord Icon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (1 nodes): `Documentation Icon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (1 nodes): `GitHub Icon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (1 nodes): `Social Icon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `X (Twitter) Icon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `Vite Framework Logo/Icon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `TASK_NAMES dictionary`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLM Factory Function` connect `LLM Integration` to `Backend API & Data`, `ASR & Pipeline`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `TaskType` connect `Backend API & Data` to `LLM Integration`, `ASR & Pipeline`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `TaskType` (e.g. with `Process API Router` and `Submit Task Endpoint`) actually correct?**
  _`TaskType` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `TranscribePage Component` (e.g. with `App Root Component` and `AudioUpload Component`) actually correct?**
  _`TranscribePage Component` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `TASK_PROMPTS` (e.g. with `Process API Router` and `Submit Task Endpoint`) actually correct?**
  _`TASK_PROMPTS` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `XfyunASRProvider` (e.g. with `Process API Router` and `Submit Task Endpoint`) actually correct?**
  _`XfyunASRProvider` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `LLMProvider` (e.g. with `OpenAIProvider Class` and `OpenAI Generate Method`) actually correct?**
  _`LLMProvider` has 11 INFERRED edges - model-reasoned connections that need verification._