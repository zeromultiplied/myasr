# Graph Report - /data/claude/myasr  (2026-04-16)

## Corpus Check
- Corpus is ~15,095 words - fits in a single context window. You may not need a graph.

## Summary
- 294 nodes · 464 edges · 54 communities detected
- Extraction: 69% EXTRACTED · 31% INFERRED · 0% AMBIGUOUS · INFERRED: 145 edges (avg confidence: 0.72)
- Token cost: 15,300 input · 2,950 output

## Community Hubs (Navigation)
- [[_COMMUNITY_PostgreSQL Data Layer|PostgreSQL Data Layer]]
- [[_COMMUNITY_SQLite Core App|SQLite Core App]]
- [[_COMMUNITY_Provider Pipeline|Provider Pipeline]]
- [[_COMMUNITY_Config Abstractions|Config Abstractions]]
- [[_COMMUNITY_Core Interfaces|Core Interfaces]]
- [[_COMMUNITY_Vue Frontend UI|Vue Frontend UI]]
- [[_COMMUNITY_ASR Demo Reference|ASR Demo Reference]]
- [[_COMMUNITY_Docs & Branding|Docs & Branding]]
- [[_COMMUNITY_Cloud LLM Providers|Cloud LLM Providers]]
- [[_COMMUNITY_Frontend API Client|Frontend API Client]]
- [[_COMMUNITY_Social Icons|Social Icons]]
- [[_COMMUNITY_Config Utils|Config Utils]]
- [[_COMMUNITY_Vue Docs Reference|Vue Docs Reference]]
- [[_COMMUNITY_Health Routes|Health Routes]]
- [[_COMMUNITY_Vue Main Entry|Vue Main Entry]]
- [[_COMMUNITY_OpenAI Methods|OpenAI Methods]]
- [[_COMMUNITY_Anthropic Methods|Anthropic Methods]]
- [[_COMMUNITY_Ollama Methods|Ollama Methods]]
- [[_COMMUNITY_Stats Interfaces|Stats Interfaces]]
- [[_COMMUNITY_Minor Cluster 19|Minor Cluster 19]]
- [[_COMMUNITY_Minor Cluster 20|Minor Cluster 20]]
- [[_COMMUNITY_Minor Cluster 21|Minor Cluster 21]]
- [[_COMMUNITY_Minor Cluster 22|Minor Cluster 22]]
- [[_COMMUNITY_Minor Cluster 23|Minor Cluster 23]]
- [[_COMMUNITY_Minor Cluster 24|Minor Cluster 24]]
- [[_COMMUNITY_Minor Cluster 25|Minor Cluster 25]]
- [[_COMMUNITY_Minor Cluster 26|Minor Cluster 26]]
- [[_COMMUNITY_Minor Cluster 27|Minor Cluster 27]]
- [[_COMMUNITY_Minor Cluster 28|Minor Cluster 28]]
- [[_COMMUNITY_Minor Cluster 29|Minor Cluster 29]]
- [[_COMMUNITY_Minor Cluster 30|Minor Cluster 30]]
- [[_COMMUNITY_Minor Cluster 31|Minor Cluster 31]]
- [[_COMMUNITY_Minor Cluster 32|Minor Cluster 32]]
- [[_COMMUNITY_Minor Cluster 33|Minor Cluster 33]]
- [[_COMMUNITY_Minor Cluster 34|Minor Cluster 34]]
- [[_COMMUNITY_Minor Cluster 35|Minor Cluster 35]]
- [[_COMMUNITY_Minor Cluster 36|Minor Cluster 36]]
- [[_COMMUNITY_Minor Cluster 37|Minor Cluster 37]]
- [[_COMMUNITY_Minor Cluster 38|Minor Cluster 38]]
- [[_COMMUNITY_Minor Cluster 39|Minor Cluster 39]]
- [[_COMMUNITY_Minor Cluster 40|Minor Cluster 40]]
- [[_COMMUNITY_Minor Cluster 41|Minor Cluster 41]]
- [[_COMMUNITY_Minor Cluster 42|Minor Cluster 42]]
- [[_COMMUNITY_Minor Cluster 43|Minor Cluster 43]]
- [[_COMMUNITY_Minor Cluster 44|Minor Cluster 44]]
- [[_COMMUNITY_Minor Cluster 45|Minor Cluster 45]]
- [[_COMMUNITY_Minor Cluster 46|Minor Cluster 46]]
- [[_COMMUNITY_Minor Cluster 47|Minor Cluster 47]]
- [[_COMMUNITY_Minor Cluster 48|Minor Cluster 48]]
- [[_COMMUNITY_Minor Cluster 49|Minor Cluster 49]]
- [[_COMMUNITY_Minor Cluster 50|Minor Cluster 50]]
- [[_COMMUNITY_Minor Cluster 51|Minor Cluster 51]]
- [[_COMMUNITY_Minor Cluster 52|Minor Cluster 52]]
- [[_COMMUNITY_Minor Cluster 53|Minor Cluster 53]]

## God Nodes (most connected - your core abstractions)
1. `TaskType` - 24 edges
2. `XfyunASRProvider` - 22 edges
3. `_get_conn()` - 21 edges
4. `retry_task()` - 13 edges
5. `_process_task()` - 13 edges
6. `RequestApi` - 11 edges
7. `reanalyze_task()` - 11 edges
8. `TranscribePage Component` - 11 edges
9. `Settings` - 10 edges
10. `ASRProvider` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Lightning Bolt Icon` --represents--> `MyASR Project`  [INFERRED]
  frontend/public/favicon.svg → CLAUDE.md
- `RequestApi` --reference_implementation--> `XfyunASRProvider Class`  [INFERRED]
  Ifasr_new.py → app/asr/xfyun.py
- `Main Application Entry` --calls_alternative--> `init_db()`  [INFERRED]
  main.py → app/db_postgres.py
- `WebLFASR RequestApi Class` --alternative_reference--> `XfyunASRProvider Class`  [INFERRED]
  weblfasr_python3_demo.py → app/asr/xfyun.py
- `Hero Banner Image` --used_in--> `TranscribePage Component`  [INFERRED]
  frontend/src/assets/hero.png → frontend/src/components/TranscribePage.vue

## Hyperedges (group relationships)
- **ASR-LLM Processing Pipeline** —  [EXTRACTED 1.00]
- **Background Task Async Flow** —  [EXTRACTED 1.00]
- **Provider Factory Pattern** —  [EXTRACTED 1.00]
- **Dual Database Backend Strategy** —  [INFERRED 0.85]
- **LLM Streaming vs Non-streaming Pattern** —  [INFERRED 0.80]
- **TaskType Enum Binding to Prompts and Names** —  [EXTRACTED 1.00]
- **SSE Streaming Output Pattern** —  [EXTRACTED 1.00]
- **Layered Config Fallback Pattern** —  [INFERRED 0.85]
- **Pipeline Orchestration Flow** — pipeline_pipeline, base_asrprovider, base_llmprovider, prompts_taskprompts, tasktype, processresponse, taskresult [EXTRACTED 1.00]

## Communities

### Community 0 - "PostgreSQL Data Layer"
Cohesion: 0.11
Nodes (32): BaseModel, create_task(), get_conn(), get_task(), init_db(), list_tasks(), update_task(), Enum (+24 more)

### Community 1 - "SQLite Core App"
Cohesion: 0.1
Nodes (31): Mangum Handler, ConfigService, create_profile(), delete_profile(), delete_provider_config(), get_active_config(), get_default_profile(), get_profile() (+23 more)

### Community 2 - "Provider Pipeline"
Cohesion: 0.14
Nodes (15): ASRProvider, get_asr_provider(), get_llm_provider(), OllamaProvider, run_pipeline(), run_pipeline_stream(), _sse_event(), _process_task() (+7 more)

### Community 3 - "Config Abstractions"
Cohesion: 0.14
Nodes (25): ASRProvider Abstract Class, ASR Factory Function, XFyun Get Result Method, Parse Transcription Helper, XFyun Transcribe Method, XFyun Upload Method, XfyunASRProvider Class, BaseSettings (+17 more)

### Community 4 - "Core Interfaces"
Cohesion: 0.11
Nodes (20): ABC, AnthropicLLMProvider, ASR Factory, ASRProvider, LLMProvider, LLM Factory, OllamaLLMProvider, OpenAILLMProvider (+12 more)

### Community 5 - "Vue Frontend UI"
Cohesion: 0.14
Nodes (24): API Module, App Root Component, AudioUpload Component, Backend API Server, deleteTask Function, downloadAsMarkdown Function, fetchStats Function, fetchTask Function (+16 more)

### Community 6 - "ASR Demo Reference"
Cohesion: 0.19
Nodes (5): RequestApi, object, str, RequestApi, SliceIdGenerator

### Community 7 - "Docs & Branding"
Cohesion: 0.11
Nodes (19): ASR Provider Pattern, LLM Provider Pattern, MyASR Project, ASR-LLM Pipeline, SSE Streaming, Anthropic Configuration, Ollama Configuration, OpenAI Configuration (+11 more)

### Community 8 - "Cloud LLM Providers"
Cohesion: 0.18
Nodes (3): AnthropicProvider, LLMProvider, OpenAIProvider

### Community 9 - "Frontend API Client"
Cohesion: 0.2
Nodes (0): 

### Community 10 - "Social Icons"
Cohesion: 0.48
Nodes (7): Bluesky Icon, Discord Icon, Documentation Icon, GitHub Icon, Social Icon, SVG Icon Sprite, X (Twitter) Icon

### Community 11 - "Config Utils"
Cohesion: 0.67
Nodes (3): _get_conn, ConfigService, Settings

### Community 12 - "Vue Docs Reference"
Cohesion: 0.67
Nodes (3): Vue Script Setup Docs, Vue 3 + TypeScript + Vite, Vue TypeScript Guide

### Community 13 - "Health Routes"
Cohesion: 1.0
Nodes (0): 

### Community 14 - "Vue Main Entry"
Cohesion: 1.0
Nodes (0): 

### Community 15 - "OpenAI Methods"
Cohesion: 1.0
Nodes (2): OpenAI Generate Method, OpenAI Generate Stream Method

### Community 16 - "Anthropic Methods"
Cohesion: 1.0
Nodes (2): Anthropic Generate Method, Anthropic Generate Stream Method

### Community 17 - "Ollama Methods"
Cohesion: 1.0
Nodes (2): Ollama Generate Method, Ollama Generate Stream Method

### Community 18 - "Stats Interfaces"
Cohesion: 1.0
Nodes (2): StatsData Data Structure, StatsData Interface

### Community 19 - "Minor Cluster 19"
Cohesion: 1.0
Nodes (0): 

### Community 20 - "Minor Cluster 20"
Cohesion: 1.0
Nodes (0): 

### Community 21 - "Minor Cluster 21"
Cohesion: 1.0
Nodes (0): 

### Community 22 - "Minor Cluster 22"
Cohesion: 1.0
Nodes (0): 

### Community 23 - "Minor Cluster 23"
Cohesion: 1.0
Nodes (1): Transcribe audio bytes to text.

### Community 24 - "Minor Cluster 24"
Cohesion: 1.0
Nodes (0): 

### Community 25 - "Minor Cluster 25"
Cohesion: 1.0
Nodes (1): Generate a complete response.

### Community 26 - "Minor Cluster 26"
Cohesion: 1.0
Nodes (1): Yield response text chunks as they arrive.

### Community 27 - "Minor Cluster 27"
Cohesion: 1.0
Nodes (0): 

### Community 28 - "Minor Cluster 28"
Cohesion: 1.0
Nodes (0): 

### Community 29 - "Minor Cluster 29"
Cohesion: 1.0
Nodes (0): 

### Community 30 - "Minor Cluster 30"
Cohesion: 1.0
Nodes (1): Create a new configuration profile.

### Community 31 - "Minor Cluster 31"
Cohesion: 1.0
Nodes (1): Get a configuration profile by ID.

### Community 32 - "Minor Cluster 32"
Cohesion: 1.0
Nodes (1): List all configuration profiles.

### Community 33 - "Minor Cluster 33"
Cohesion: 1.0
Nodes (1): Update a configuration profile.

### Community 34 - "Minor Cluster 34"
Cohesion: 1.0
Nodes (1): Delete a configuration profile.

### Community 35 - "Minor Cluster 35"
Cohesion: 1.0
Nodes (1): Set a profile as the default configuration.

### Community 36 - "Minor Cluster 36"
Cohesion: 1.0
Nodes (1): Get the default configuration profile.

### Community 37 - "Minor Cluster 37"
Cohesion: 1.0
Nodes (1): Save provider configuration for a profile.

### Community 38 - "Minor Cluster 38"
Cohesion: 1.0
Nodes (1): Get provider configuration for a profile.

### Community 39 - "Minor Cluster 39"
Cohesion: 1.0
Nodes (1): List provider configurations for a profile.

### Community 40 - "Minor Cluster 40"
Cohesion: 1.0
Nodes (1): Delete a provider configuration.

### Community 41 - "Minor Cluster 41"
Cohesion: 1.0
Nodes (1): Get the active configuration (combines database and .env settings).

### Community 42 - "Minor Cluster 42"
Cohesion: 1.0
Nodes (0): 

### Community 43 - "Minor Cluster 43"
Cohesion: 1.0
Nodes (0): 

### Community 44 - "Minor Cluster 44"
Cohesion: 1.0
Nodes (0): 

### Community 45 - "Minor Cluster 45"
Cohesion: 1.0
Nodes (0): 

### Community 46 - "Minor Cluster 46"
Cohesion: 1.0
Nodes (0): 

### Community 47 - "Minor Cluster 47"
Cohesion: 1.0
Nodes (0): 

### Community 48 - "Minor Cluster 48"
Cohesion: 1.0
Nodes (0): 

### Community 49 - "Minor Cluster 49"
Cohesion: 1.0
Nodes (1): SliceIdGenerator Class

### Community 50 - "Minor Cluster 50"
Cohesion: 1.0
Nodes (1): saveToServer Call

### Community 51 - "Minor Cluster 51"
Cohesion: 1.0
Nodes (1): downloadAsMarkdown Call

### Community 52 - "Minor Cluster 52"
Cohesion: 1.0
Nodes (1): deleteTask Call

### Community 53 - "Minor Cluster 53"
Cohesion: 1.0
Nodes (1): Vite Framework Logo/Icon

## Knowledge Gaps
- **58 isolated node(s):** `Transcribe audio bytes to text.`, `Parse the orderResult JSON to extract transcription text.`, `Generate a complete response.`, `Yield response text chunks as they arrive.`, `Service for managing system configuration with profile support.` (+53 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Health Routes`** (2 nodes): `health.py`, `health()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vue Main Entry`** (2 nodes): `App.vue`, `main.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `OpenAI Methods`** (2 nodes): `OpenAI Generate Method`, `OpenAI Generate Stream Method`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Anthropic Methods`** (2 nodes): `Anthropic Generate Method`, `Anthropic Generate Stream Method`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ollama Methods`** (2 nodes): `Ollama Generate Method`, `Ollama Generate Stream Method`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Stats Interfaces`** (2 nodes): `StatsData Data Structure`, `StatsData Interface`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 19`** (1 nodes): `main.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 20`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 21`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 22`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 23`** (1 nodes): `Transcribe audio bytes to text.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 24`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 25`** (1 nodes): `Generate a complete response.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 26`** (1 nodes): `Yield response text chunks as they arrive.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 27`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 28`** (1 nodes): `prompts.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 29`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 30`** (1 nodes): `Create a new configuration profile.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 31`** (1 nodes): `Get a configuration profile by ID.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 32`** (1 nodes): `List all configuration profiles.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 33`** (1 nodes): `Update a configuration profile.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 34`** (1 nodes): `Delete a configuration profile.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 35`** (1 nodes): `Set a profile as the default configuration.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 36`** (1 nodes): `Get the default configuration profile.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 37`** (1 nodes): `Save provider configuration for a profile.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 38`** (1 nodes): `Get provider configuration for a profile.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 39`** (1 nodes): `List provider configurations for a profile.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 40`** (1 nodes): `Delete a provider configuration.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 41`** (1 nodes): `Get the active configuration (combines database and .env settings).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 42`** (1 nodes): `vite.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 43`** (1 nodes): `AudioUpload.vue`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 44`** (1 nodes): `ResultView.vue`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 45`** (1 nodes): `TaskList.vue`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 46`** (1 nodes): `HomePage.vue`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 47`** (1 nodes): `TranscribePage.vue`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 48`** (1 nodes): `main.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 49`** (1 nodes): `SliceIdGenerator Class`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 50`** (1 nodes): `saveToServer Call`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 51`** (1 nodes): `downloadAsMarkdown Call`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 52`** (1 nodes): `deleteTask Call`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Minor Cluster 53`** (1 nodes): `Vite Framework Logo/Icon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TaskType` connect `PostgreSQL Data Layer` to `SQLite Core App`, `Provider Pipeline`, `Config Abstractions`, `ASR Demo Reference`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Why does `_get_conn()` connect `SQLite Core App` to `PostgreSQL Data Layer`, `Config Abstractions`, `ASR Demo Reference`?**
  _High betweenness centrality (0.090) - this node is a cross-community bridge._
- **Why does `XfyunASRProvider` connect `Provider Pipeline` to `PostgreSQL Data Layer`, `Core Interfaces`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `TaskType` (e.g. with `ReanalyzeRequest` and `SaveResultItem`) actually correct?**
  _`TaskType` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `XfyunASRProvider` (e.g. with `ReanalyzeRequest` and `SaveResultItem`) actually correct?**
  _`XfyunASRProvider` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `_get_conn()` (e.g. with `str` and `delete_task()`) actually correct?**
  _`_get_conn()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `str` (e.g. with `.gene_params()` and `.gene_request()`) actually correct?**
  _`str` has 14 INFERRED edges - model-reasoned connections that need verification._