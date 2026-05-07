from dataclasses import dataclass
from datetime import date

@dataclass
class Transaction:
    """1件の取引データを表すクラス"""
    date: date         # 日付
    description: str          # 店名・内容
    amount: int        # 金額（収入は正、支出は負）
    source: str        # どのCSVファイルから来たか
    category: str = "未分類"