import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from contextlib import contextmanager

# 数据库连接配置
DATABASE_URL = os.environ.get('POSTGRES_URL') or os.environ.get('DATABASE_URL')

@contextmanager
def get_conn():
    """获取数据库连接上下文管理器"""
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """初始化数据库表结构"""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    filename TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'uploading',
                    order_id TEXT,
                    task_types TEXT NOT NULL,
                    llm_provider TEXT,
                    llm_model TEXT,
                    transcription TEXT,
                    asr_raw_result TEXT,
                    results TEXT,
                    error TEXT,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
                )
            """)
            conn.commit()

def create_task(
    filename: str,
    task_types: list[str],
    llm_provider: str | None = None,
    llm_model: str | None = None,
) -> int:
    """创建新任务"""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO tasks (filename, status, task_types, llm_provider, llm_model, created_at, updated_at)
                VALUES (%s, 'uploading', %s, %s, %s, NOW(), NOW())
                RETURNING id
            """, (filename, json.dumps(task_types), llm_provider, llm_model))
            task_id = cur.fetchone()['id']
            conn.commit()
            return task_id

def update_task(task_id: int, **kwargs):
    """更新任务信息"""
    if not kwargs:
        return

    set_clauses = []
    values = []

    for key, value in kwargs.items():
        set_clauses.append(f"{key} = %s")
        values.append(value)

    set_clauses.append("updated_at = NOW()")
    values.append(task_id)

    with get_conn() as conn:
        with conn.cursor() as cur:
            query = f"UPDATE tasks SET {', '.join(set_clauses)} WHERE id = %s"
            cur.execute(query, values)
            conn.commit()

def get_task(task_id: int) -> dict | None:
    """获取任务详情"""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
            row = cur.fetchone()
            if row is None:
                return None

            # 转换为字典并处理 JSON 字段
            result = dict(row)
            if result.get('task_types'):
                result['task_types'] = json.loads(result['task_types'])
            if result.get('results'):
                result['results'] = json.loads(result['results'])

            return result

def list_tasks(limit: int = 50) -> list[dict]:
    """获取任务列表"""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks ORDER BY created_at DESC LIMIT %s", (limit,))
            rows = cur.fetchall()

            results = []
            for row in rows:
                result = dict(row)
                if result.get('task_types'):
                    result['task_types'] = json.loads(result['task_types'])
                if result.get('results'):
                    result['results'] = json.loads(result['results'])
                results.append(result)

            return results