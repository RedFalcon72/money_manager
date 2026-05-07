import sqlite3
from pathlib import Path
from models import Transaction

DB_PATH = Path("data/processed/money.db")

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                date        TEXT NOT NULL,
                amount      INTEGER NOT NULL,
                description TEXT NOT NULL,
                source      TEXT NOT NULL,
                category    TEXT NOT NULL DEFAULT '未分類',
                UNIQUE(date, amount, description, source)
            )
        """)

def save_transactions(transactions: list[Transaction]) -> int:
    """保存した件数を返す"""
    saved = 0
    with get_connection() as conn:
        for t in transactions:
            cursor = conn.execute(
                "INSERT OR IGNORE INTO transactions (date, amount, description, source, category) VALUES (?, ?, ?, ?, ?)",
                (str(t.date), t.amount, t.description, t.source, t.category)
            )
            saved += cursor.rowcount
    return saved