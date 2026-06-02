import sqlite3
from pathlib import Path
from tracker.models import Transaction

DB_PATH = Path("data/processed/money.db")

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,   
                date        TEXT NOT NULL,                         -- "YYYY-MM-DD"形式で保存
                amount      INTEGER NOT NULL,                      -- 収入(+)、支出(-)
                description TEXT NOT NULL,                         -- 摘要・店名
                source      TEXT NOT NULL,                         -- どのCSVから来たか
                category    TEXT NOT NULL DEFAULT '未分類',         -- カテゴリ（後で分析して付ける）
                UNIQUE(date, amount, description, source)          -- 重複防止
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