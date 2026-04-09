import logging
import os

import uvicorn
from fastapi import FastAPI

from app.config import settings
from app.routes.health import router as health_router
from app.routes.process import router as process_router

# 根据环境选择数据库初始化
if os.environ.get('VERCEL') or os.environ.get('POSTGRES_URL'):
    # Vercel 环境使用 Postgres
    from app.db_postgres import init_db
else:
    # 本地环境使用 SQLite
    from app.db import init_db

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

init_db()

app = FastAPI(title="MyASR", description="语音转文字 + LLM文本处理 API")

app.include_router(health_router)
app.include_router(process_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
