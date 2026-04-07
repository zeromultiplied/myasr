import json
import logging
import time
from collections.abc import AsyncIterator

from app.asr.factory import get_asr_provider
from app.llm.factory import get_llm_provider
from app.models import ProcessResponse, TaskResult, TaskType
from app.tasks.prompts import TASK_PROMPTS

logger = logging.getLogger(__name__)


async def run_pipeline(
    audio_data: bytes,
    filename: str,
    tasks: list[TaskType],
    llm_provider: str | None = None,
    llm_model: str | None = None,
) -> ProcessResponse:
    metadata = {}

    # Step 1: ASR
    t0 = time.time()
    asr = get_asr_provider()
    transcription = await asr.transcribe(audio_data, filename)
    metadata["asr_duration_sec"] = round(time.time() - t0, 2)
    metadata["asr_provider"] = "xfyun"
    logger.info("ASR completed in %.2fs, text length=%d", metadata["asr_duration_sec"], len(transcription))

    # Step 2: LLM tasks
    t1 = time.time()
    llm = get_llm_provider(llm_provider, llm_model)
    metadata["llm_provider"] = llm_provider or "default"
    metadata["llm_model"] = llm_model or "default"

    results = []
    for task in tasks:
        prompt = TASK_PROMPTS[task]
        result_text = await llm.generate(prompt, transcription)
        results.append(TaskResult(task=task, result=result_text))
        logger.info("LLM task '%s' completed", task.value)

    metadata["llm_duration_sec"] = round(time.time() - t1, 2)

    return ProcessResponse(
        transcription=transcription,
        results=results,
        metadata=metadata,
    )


async def run_pipeline_stream(
    audio_data: bytes,
    filename: str,
    tasks: list[TaskType],
    llm_provider: str | None = None,
    llm_model: str | None = None,
) -> AsyncIterator[str]:
    """Yield SSE-formatted events for the streaming endpoint."""

    # Step 1: ASR (non-streaming — it's a batch operation)
    asr = get_asr_provider()
    transcription = await asr.transcribe(audio_data, filename)

    yield _sse_event("transcription", {"text": transcription})

    # Step 2: Stream LLM tasks one by one
    llm = get_llm_provider(llm_provider, llm_model)

    for task in tasks:
        prompt = TASK_PROMPTS[task]
        yield _sse_event("task_start", {"task": task.value})

        async for chunk in llm.generate_stream(prompt, transcription):
            yield _sse_event("task_chunk", {"task": task.value, "chunk": chunk})

        yield _sse_event("task_done", {"task": task.value})

    yield _sse_event("done", {})


def _sse_event(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"
