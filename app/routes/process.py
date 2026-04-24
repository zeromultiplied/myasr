import asyncio
import json
import logging
import re
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from app.asr.xfyun import XfyunASRProvider
from app.config import settings
from app.db import create_task, get_task, list_tasks, update_task, create_saved_result
from app.llm.factory import get_llm_provider
from app.middleware.auth import get_current_user
from app.models import TaskType
from app.tasks.prompts import TASK_PROMPTS

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1")

ALLOWED_AUDIO_EXTENSIONS = {".wav", ".flac", ".opus", ".m4a", ".mp3"}


def _validate_audio_format(filename: str) -> None:
    if not filename:
        raise HTTPException(400, "Filename is required")
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(
            400,
            f"Unsupported audio format: '{ext}'. "
            f"Supported: {', '.join(sorted(ALLOWED_AUDIO_EXTENSIONS))}",
        )


def _parse_tasks(tasks_str: str) -> list[str]:
    task_list = []
    for t in tasks_str.split(","):
        t = t.strip()
        if not t:
            continue
        try:
            TaskType(t)
            task_list.append(t)
        except ValueError:
            valid = [e.value for e in TaskType]
            raise HTTPException(400, f"Unknown task: '{t}'. Valid tasks: {valid}")
    if not task_list:
        raise HTTPException(400, "At least one task is required")
    return task_list


# ==================== Task-based workflow ====================


@router.post("/submit")
async def submit_task(
    file: UploadFile = File(...),
    tasks: str = Form(...),
    llm_provider: str | None = Form(None),
    llm_model: str | None = Form(None),
    user: dict = Depends(get_current_user),
):
    """Submit an audio file for processing. Returns task_id immediately."""
    _validate_audio_format(file.filename)
    task_list = _parse_tasks(tasks)

    audio_data = await file.read()
    max_size = settings.max_audio_size_mb * 1024 * 1024
    if len(audio_data) > max_size:
        raise HTTPException(400, f"Audio file too large (max {settings.max_audio_size_mb}MB)")

    # Create DB task
    task_id = create_task(
        filename=file.filename,
        task_types=task_list,
        llm_provider=llm_provider,
        llm_model=llm_model,
        user_id=user["id"],
    )

    # Start background processing
    asyncio.create_task(_process_task(task_id, audio_data, file.filename, task_list, llm_provider, llm_model))

    logger.info("Task %d submitted: file=%s tasks=%s user=%d", task_id, file.filename, tasks, user["id"])
    return {"task_id": task_id, "status": "uploading"}


@router.get("/tasks")
async def get_tasks(user: dict = Depends(get_current_user)):
    """List all tasks for the current user."""
    return list_tasks(user_id=user["id"])


@router.get("/tasks/{task_id}")
async def get_task_detail(task_id: int, user: dict = Depends(get_current_user)):
    """Get task detail by id."""
    task = get_task(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    if task.get("user_id") is not None and task["user_id"] != user["id"]:
        raise HTTPException(404, "Task not found")
    return task


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, user: dict = Depends(get_current_user)):
    """Delete a task."""
    task = get_task(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    if task.get("user_id") is not None and task["user_id"] != user["id"]:
        raise HTTPException(404, "Task not found")
    from app.db import _get_conn
    conn = _get_conn()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return {"ok": True}


@router.post("/tasks/{task_id}/retry")
async def retry_task(task_id: int, user: dict = Depends(get_current_user)):
    """Retry a failed task that has an order_id — re-query iFlytek and recover."""
    task = get_task(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    if task.get("user_id") is not None and task["user_id"] != user["id"]:
        raise HTTPException(404, "Task not found")
    if task["status"] != "failed":
        raise HTTPException(400, "Only failed tasks can be retried")
    if not task.get("order_id"):
        raise HTTPException(400, "Task has no order_id, cannot retry")

    # Fire background recovery
    asyncio.create_task(_retry_task(
        task_id,
        task["order_id"],
        task["task_types"],
        task.get("llm_provider"),
        task.get("llm_model"),
    ))
    update_task(task_id, status="transcribing", error=None)
    return {"task_id": task_id, "status": "transcribing"}


class ReanalyzeRequest(BaseModel):
    tasks: str
    llm_provider: str | None = None
    llm_model: str | None = None


@router.post("/tasks/{task_id}/reanalyze")
async def reanalyze_task(task_id: int, req: ReanalyzeRequest, user: dict = Depends(get_current_user)):
    """Re-run LLM analysis on an already-transcribed task."""
    task = get_task(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    if task.get("user_id") is not None and task["user_id"] != user["id"]:
        raise HTTPException(404, "Task not found")
    if not task.get("transcription"):
        raise HTTPException(400, "Task has no transcription to analyze")

    task_list = _parse_tasks(req.tasks)
    asyncio.create_task(_reanalyze_task(
        task_id,
        task["transcription"],
        task_list,
        req.llm_provider,
        req.llm_model,
    ))
    update_task(task_id, status="llm_processing", error=None,
                task_types=json.dumps(task_list))
    return {"task_id": task_id, "status": "llm_processing"}


@router.get("/stats")
async def get_stats(user: dict = Depends(get_current_user)):
    """Return task statistics for the current user."""
    from app.db import _get_conn
    conn = _get_conn()
    uid = user["id"]
    row = conn.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN status = 'done' THEN 1 ELSE 0 END) as done,
            SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
            SUM(CASE WHEN status NOT IN ('done', 'failed') THEN 1 ELSE 0 END) as processing
        FROM tasks WHERE user_id = ?
    """, (uid,)).fetchone()
    # This month count
    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat()
    month_row = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE user_id = ? AND created_at >= ?",
        (uid, month_start),
    ).fetchone()
    # Materials count
    materials_row = conn.execute(
        "SELECT COUNT(*) FROM saved_results WHERE user_id = ?", (uid,)
    ).fetchone()
    recent = conn.execute(
        "SELECT id, filename, status, created_at, updated_at FROM tasks WHERE user_id = ? ORDER BY updated_at DESC LIMIT 10",
        (uid,),
    ).fetchall()
    conn.close()
    return {
        "total": row[0],
        "done": row[1],
        "failed": row[2],
        "processing": row[3],
        "this_month": month_row[0] if month_row else 0,
        "materials_count": materials_row[0] if materials_row else 0,
        "recent": [dict(r) for r in recent],
    }


# ==================== Background processing ====================


async def _process_task(
    task_id: int,
    audio_data: bytes,
    filename: str,
    task_types: list[str],
    llm_provider: str | None,
    llm_model: str | None,
):
    """Background: upload → poll ASR → run LLM tasks → save results."""
    try:
        asr = XfyunASRProvider()

        # Step 1: Upload to iFlytek
        update_task(task_id, status="uploading")
        order_id = await asr.upload(audio_data, filename)
        update_task(task_id, status="transcribing", order_id=order_id)
        logger.info("Task %d: uploaded, orderId=%s", task_id, order_id)

        # Step 2: Poll for ASR result
        timeout = settings.asr_poll_timeout_sec
        interval = settings.asr_poll_interval_sec
        elapsed = 0

        while elapsed < timeout:
            result = await asr.get_result(order_id)

            if result["status"] == "done":
                transcription = asr._parse_transcription(result["data"])
                update_task(task_id, status="llm_processing", transcription=transcription,
                            asr_raw_result=result["data"] if isinstance(result["data"], str) else json.dumps(result["data"], ensure_ascii=False))
                logger.info("Task %d: transcription done, len=%d", task_id, len(transcription))
                break
            elif result["status"] == "failed":
                update_task(task_id, status="failed", error="ASR transcription failed")
                logger.error("Task %d: ASR failed", task_id)
                return

            await asyncio.sleep(interval)
            elapsed += interval
        else:
            update_task(task_id, status="failed", error=f"ASR timed out after {timeout}s")
            return

        # Step 3: Run LLM tasks
        task = get_task(task_id)
        transcription = task["transcription"]

        llm = get_llm_provider(llm_provider, llm_model)
        results = []
        for t in task_types:
            task_type = TaskType(t)
            prompt = TASK_PROMPTS[task_type]
            try:
                result_text = await llm.generate(prompt, transcription)
                results.append({"task": t, "result": result_text})
                logger.info("Task %d: LLM task '%s' done", task_id, t)
            except Exception as e:
                results.append({"task": t, "result": f"[Error: {e}]"})
                logger.error("Task %d: LLM task '%s' failed: %s", task_id, t, e)

        update_task(task_id, status="done", results=json.dumps(results, ensure_ascii=False))
        logger.info("Task %d: all done", task_id)

    except Exception as e:
        logger.exception("Task %d: processing error", task_id)
        update_task(task_id, status="failed", error=str(e))


async def _retry_task(
    task_id: int,
    order_id: str,
    task_types: list[str],
    llm_provider: str | None,
    llm_model: str | None,
):
    """Background: re-query iFlytek for a previously timed-out task and recover."""
    try:
        asr = XfyunASRProvider()
        result = await asr.get_result(order_id)

        if result["status"] == "done":
            transcription = asr._parse_transcription(result["data"])
            raw = result["data"] if isinstance(result["data"], str) else json.dumps(result["data"], ensure_ascii=False)
            update_task(task_id, status="llm_processing", transcription=transcription, asr_raw_result=raw)
            logger.info("Task %d retry: transcription recovered, len=%d", task_id, len(transcription))
        elif result["status"] == "processing":
            # Still processing — poll for a while
            timeout = settings.asr_poll_timeout_sec
            interval = settings.asr_poll_interval_sec
            elapsed = 0
            while elapsed < timeout:
                await asyncio.sleep(interval)
                elapsed += interval
                result = await asr.get_result(order_id)
                if result["status"] == "done":
                    transcription = asr._parse_transcription(result["data"])
                    raw = result["data"] if isinstance(result["data"], str) else json.dumps(result["data"], ensure_ascii=False)
                    update_task(task_id, status="llm_processing", transcription=transcription, asr_raw_result=raw)
                    logger.info("Task %d retry: transcription done after %ds", task_id, elapsed)
                    break
                elif result["status"] == "failed":
                    update_task(task_id, status="failed", error="ASR transcription failed on retry")
                    return
            else:
                update_task(task_id, status="failed", error=f"ASR still not ready after retry ({timeout}s)")
                return
        else:
            update_task(task_id, status="failed", error="ASR transcription failed on retry")
            return

        # Run LLM tasks
        task = get_task(task_id)
        transcription = task["transcription"]
        llm = get_llm_provider(llm_provider, llm_model)
        results = []
        for t in task_types:
            task_type = TaskType(t)
            prompt = TASK_PROMPTS[task_type]
            try:
                result_text = await llm.generate(prompt, transcription)
                results.append({"task": t, "result": result_text})
            except Exception as e:
                results.append({"task": t, "result": f"[Error: {e}]"})
                logger.error("Task %d retry: LLM task '%s' failed: %s", task_id, t, e)

        update_task(task_id, status="done", results=json.dumps(results, ensure_ascii=False))
        logger.info("Task %d retry: all done", task_id)

    except Exception as e:
        logger.exception("Task %d retry error", task_id)
        update_task(task_id, status="failed", error=str(e))


async def _reanalyze_task(
    task_id: int,
    transcription: str,
    task_types: list[str],
    llm_provider: str | None,
    llm_model: str | None,
):
    """Background: re-run LLM analysis on existing transcription."""
    try:
        llm = get_llm_provider(llm_provider, llm_model)
        results = []
        for t in task_types:
            task_type = TaskType(t)
            prompt = TASK_PROMPTS[task_type]
            try:
                result_text = await llm.generate(prompt, transcription)
                results.append({"task": t, "result": result_text})
                logger.info("Task %d reanalyze: LLM task '%s' done", task_id, t)
            except Exception as e:
                results.append({"task": t, "result": f"[Error: {e}]"})
                logger.error("Task %d reanalyze: LLM task '%s' failed: %s", task_id, t, e)

        update_task(task_id, status="done", results=json.dumps(results, ensure_ascii=False))
        logger.info("Task %d reanalyze: all done", task_id)

    except Exception as e:
        logger.exception("Task %d reanalyze error", task_id)
        update_task(task_id, status="failed", error=str(e))


# ==================== Save endpoint ====================

OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "output"

TASK_NAMES = {
    "summarize": "文本总结",
    "expand": "内容发散",
    "polish": "文本润色",
    "action_items": "行动项提取",
}


class SaveResultItem(BaseModel):
    task: str
    result: str


class SaveRequest(BaseModel):
    transcription: str
    results: list[SaveResultItem]
    filename: str


@router.post("/save")
async def save_result(req: SaveRequest, user: dict = Depends(get_current_user)):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    stem = re.sub(r'[^\w\u4e00-\u9fff.-]', '_', req.filename.rsplit('.', 1)[0])
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"{stem}_{ts}"

    # Save JSON
    json_path = OUTPUT_DIR / f"{base_name}.json"
    json_data = {
        "filename": req.filename,
        "transcription": req.transcription,
        "results": [r.model_dump() for r in req.results],
        "saved_at": datetime.now().isoformat(),
    }
    json_path.write_text(json.dumps(json_data, ensure_ascii=False, indent=2), encoding="utf-8")

    # Save Markdown
    md_path = OUTPUT_DIR / f"{base_name}.md"
    md = f"# {req.filename} - 语音处理结果\n\n"
    md += f"## 原始转写\n\n{req.transcription}\n\n"
    for r in req.results:
        title = TASK_NAMES.get(r.task, r.task)
        md += f"## {title}\n\n{r.result}\n\n"
    md_path.write_text(md, encoding="utf-8")

    # Also persist to saved_results table
    create_saved_result(
        user_id=user["id"],
        filename=req.filename,
        transcription=req.transcription,
        results=json.dumps([r.model_dump() for r in req.results], ensure_ascii=False),
        file_path=str(md_path),
    )

    logger.info("Results saved to %s", OUTPUT_DIR / base_name)
    return {"path": str(md_path), "json_path": str(json_path)}
