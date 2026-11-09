import os
import sqlite3
from pathlib import Path
from .models import HomeworkStatus

DATA_DIR = Path(os.environ.get("LOCALAPPDATA", Path.home() / ".local")) / "Horizon"
DB_PATH = DATA_DIR / "horizon.db"

def connection() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialise() -> None:
    with connection() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS homework_state (homework_id TEXT PRIMARY KEY, status TEXT NOT NULL)")

def homework_status(homework_id: str) -> HomeworkStatus:
    with connection() as conn:
        row = conn.execute("SELECT status FROM homework_state WHERE homework_id = ?", (homework_id,)).fetchone()
    return HomeworkStatus(row["status"]) if row else HomeworkStatus.TODO

def update_homework_status(homework_id: str, status: HomeworkStatus) -> None:
    with connection() as conn:
        conn.execute("INSERT INTO homework_state(homework_id,status) VALUES (?,?) ON CONFLICT(homework_id) DO UPDATE SET status=excluded.status", (homework_id, status.value))
