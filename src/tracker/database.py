import sqlite3
from pathlib import Path
from tracker.models import Transaction

PROJECT_ROOT = Path(__file__).resolve().parents[2] # プロジェクトのルートディレクトリを取得
DB_PATH = PROJECT_ROOT / "data" / "processed" / "money.db"

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

def update_category(transaction_id: int, category: str) -> None:
    """指定IDのカテゴリを更新し、同じdescriptionの未分類も更新する"""
    with get_connection() as conn:
        # 該当の取引のdescriptionを取得
        cursor = conn.execute(
            "SELECT description FROM transactions WHERE id = ?", (transaction_id,)
        )
        row = cursor.fetchone()
        if not row:
            return
        description = row[0]

        # 同じdescriptionの未分類を一括更新
        conn.execute(
            "UPDATE transactions SET category = ? WHERE description = ? AND category = '未分類'",
            (category, description)
        )

def get_category_mapping() -> dict[str, str]:
    """過去に分類済みのdescription→categoryの対応表を取得"""
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT DISTINCT description, category FROM transactions WHERE category != '未分類'"
        )
        return {row[0]: row[1] for row in cursor.fetchall()}