import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "myasr.db"


def _get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = _get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    # Add asr_raw_result column if missing (migration for existing DBs)
    try:
        conn.execute("ALTER TABLE tasks ADD COLUMN asr_raw_result TEXT")
        conn.commit()
    except Exception:
        pass  # column already exists
    conn.commit()
    conn.close()


def create_task(
    filename: str,
    task_types: list[str],
    llm_provider: str | None = None,
    llm_model: str | None = None,
) -> int:
    now = datetime.now().isoformat()
    conn = _get_conn()
    cursor = conn.execute(
        """INSERT INTO tasks (filename, status, task_types, llm_provider, llm_model, created_at, updated_at)
           VALUES (?, 'uploading', ?, ?, ?, ?, ?)""",
        (filename, json.dumps(task_types), llm_provider, llm_model, now, now),
    )
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id


def update_task(task_id: int, **kwargs):
    conn = _get_conn()
    kwargs["updated_at"] = datetime.now().isoformat()
    sets = ", ".join(f"{k} = ?" for k in kwargs)
    values = list(kwargs.values())
    values.append(task_id)
    conn.execute(f"UPDATE tasks SET {sets} WHERE id = ?", values)
    conn.commit()
    conn.close()


def get_task(task_id: int) -> dict | None:
    conn = _get_conn()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    if row is None:
        return None
    return _row_to_dict(row)


def list_tasks(limit: int = 50) -> list[dict]:
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM tasks ORDER BY created_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [_row_to_dict(r) for r in rows]


def _row_to_dict(row: sqlite3.Row) -> dict:
    d = dict(row)
    # Parse JSON fields
    if d.get("task_types"):
        d["task_types"] = json.loads(d["task_types"])
    if d.get("results"):
        d["results"] = json.loads(d["results"])
    return d
