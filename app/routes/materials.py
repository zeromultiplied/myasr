import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse

from app.db import (
    count_saved_results,
    delete_saved_result,
    get_saved_result,
    list_saved_results,
)
from app.middleware.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1")

TASK_NAMES = {
    "summarize": "文本总结",
    "expand": "内容发散",
    "polish": "文本润色",
    "action_items": "行动项提取",
}


def _build_markdown(item: dict) -> str:
    md = f"# {item['filename']} - 语音处理结果\n\n"
    md += f"## 原始转写\n\n{item['transcription']}\n\n"
    results = item.get("results", [])
    if isinstance(results, str):
        import json
        results = json.loads(results)
    for r in results:
        title = TASK_NAMES.get(r.get("task", ""), r.get("task", ""))
        md += f"## {title}\n\n{r.get('result', '')}\n\n"
    return md


@router.get("/materials")
async def list_materials(
    search: str | None = Query(None, description="Search keyword"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user: dict = Depends(get_current_user),
):
    items = list_saved_results(user["id"], search=search, limit=limit, offset=offset)
    total = count_saved_results(user["id"], search=search)
    # Truncate transcription for list view
    for item in items:
        t = item.get("transcription", "")
        if len(t) > 200:
            item["transcription_preview"] = t[:200] + "..."
        else:
            item["transcription_preview"] = t
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/materials/{material_id}")
async def get_material(material_id: int, user: dict = Depends(get_current_user)):
    item = get_saved_result(material_id)
    if not item or item["user_id"] != user["id"]:
        raise HTTPException(404, "Material not found")
    return item


@router.delete("/materials/{material_id}")
async def delete_material(material_id: int, user: dict = Depends(get_current_user)):
    item = get_saved_result(material_id)
    if not item or item["user_id"] != user["id"]:
        raise HTTPException(404, "Material not found")
    delete_saved_result(material_id)
    return {"ok": True}


@router.get("/materials/{material_id}/download")
async def download_material(material_id: int, user: dict = Depends(get_current_user)):
    item = get_saved_result(material_id)
    if not item or item["user_id"] != user["id"]:
        raise HTTPException(404, "Material not found")
    md = _build_markdown(item)
    filename = item["filename"].rsplit(".", 1)[0] + "_result.md"
    return PlainTextResponse(md, media_type="text/markdown; charset=utf-8", headers={
        "Content-Disposition": f"attachment; filename*=UTF-8''{filename}"
    })
