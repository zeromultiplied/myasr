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

    # Main tasks table
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
            kb_collection_id INTEGER,
            kb_document_id INTEGER,
            kb_processed BOOLEAN NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    # Configuration profiles
    conn.execute("""
        CREATE TABLE IF NOT EXISTS config_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            is_default BOOLEAN NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)

    # Provider configurations
    conn.execute("""
        CREATE TABLE IF NOT EXISTS provider_configs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER NOT NULL,
            provider_type TEXT NOT NULL,
            provider_name TEXT NOT NULL,
            api_key TEXT,
            base_url TEXT,
            model_name TEXT,
            priority INTEGER DEFAULT 1,
            is_active BOOLEAN NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (profile_id) REFERENCES config_profiles(id) ON DELETE CASCADE,
            UNIQUE(profile_id, provider_type, provider_name)
        )
    """)

    # Knowledge base collections
    conn.execute("""
        CREATE TABLE IF NOT EXISTS kb_collections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            slug TEXT UNIQUE NOT NULL,
            is_public BOOLEAN NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)

    # Knowledge base documents
    conn.execute("""
        CREATE TABLE IF NOT EXISTS kb_documents (
           极id INTEGER PRIMARY KEY AUTOINCREMENT,
            collection_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            content_type TEXT NOT NULL DEFAULT 'markdown',
            summary TEXT,
            tags_json TEXT,
            parent_id INTEGER,
            is_published BOOLEAN NOT NULL DEFAULT 1,
            version INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT极NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (collection_id) REFERENCES kb_collections(id) ON DELETE CASCADE,
            FOREIGN KEY (parent_id) REFERENCES kb_documents(id) ON DELETE SET NULL
        )
    """)

    # Q&A sessions
    conn.execute("""
        CREATE TABLE IF NOT EXISTS qa_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            collection_id INTEGER NOT NULL,
            session_name TEXT,
            session_type TEXT NOT NULL DEFAULT 'interactive',
            model_used TEXT,
            profile_used INTEGER,
            total_questions INTEGER DEFAULT 0,
            total_tokens INTEGER DEFAULT 0,
            started_at TEXT NOT NULL DEFAULT (datetime('now')),
            ended_at TEXT,
            metadata_json TEXT,
            FOREIGN KEY (collection_id) REFERENCES kb_collections(id) ON DELETE CASCADE,
            FOREIGN KEY (profile_used) REFERENCES config_profiles(id) ON DELETE SET NULL
        )
    """)

    # Migration for existing tables
    try:
        conn.execute("ALTER TABLE tasks ADD COLUMN asr_raw_result TEXT")
    except Exception:
        pass  # column already exists

    try:
        conn.execute("ALTER TABLE tasks ADD COLUMN kb_collection_id INTEGER")
    except Exception:
        pass  # column already exists

    try:
        conn.execute("ALTER TABLE tasks ADD COLUMN kb_document_id INTEGER")
    except Exception:
        pass  # column already exists

    try:
        conn.execute("ALTER TABLE tasks ADD COLUMN kb_processed BOOLEAN NOT NULL DEFAULT 0")
    except Exception:
        pass  # column already exists

    # Ensure there's a default profile
    try:
        from app.config import settings
        conn.execute(
            "INSERT OR IGNORE INTO config_profiles (name, description, is_default) VALUES (?, ?, ?)",
            ("default", "Default configuration profile", 1)
        )
    except Exception:
        pass  # Settings may not be available yet

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
