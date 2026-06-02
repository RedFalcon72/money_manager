import pandas as pd
from pathlib import Path
from datetime import date
from tracker.models import Transaction
from tracker.logger import get_logger

logger = get_logger(__name__)

DATE_PATTERNS = ["日付", "取引日", "取引年月日", "年月日", "date"]
DESC_PATTERNS = ["摘要", "内容", "取引内容", "店名", "description"]
EXPENSE_PATTERNS = ["出金金額", "出金額", "支出", "引き落とし"]
INCOME_PATTERNS = ["入金金額", "入金額", "収入", "振込"]

def detect_columns(df: pd.DataFrame) -> dict[str, str]:
    """列名を自動検出してマッピングを返す"""
    mapping = {}
    cols = df.columns.tolist()

    for col in cols:
        if any(p in col for p in DATE_PATTERNS):
            mapping["date"] = col
        elif any(p in col for p in DESC_PATTERNS):
            mapping["description"] = col
        elif any(p in col for p in EXPENSE_PATTERNS):
            mapping["expense"] = col
        elif any(p in col for p in INCOME_PATTERNS):
            mapping["income"] = col

    return mapping

def load_csv(filepath: Path) -> list[Transaction]:
    """CSVを読み込んでTransactionのリストを返す"""
    logger.info(f"読み込み開始: {filepath.name}")

    for encoding in ["utf-8-sig", "utf-8", "shift-jis", "cp932"]:
        try:
            df = pd.read_csv(filepath, encoding=encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        logger.error(f"エンコーディング検出失敗: {filepath.name}")
        return []

    mapping = detect_columns(df)
    logger.debug(f"列マッピング: {mapping}")

    if "date" not in mapping or "description" not in mapping:
        logger.error(f"必要な列が見つかりません: {filepath.name}")
        return []

    transactions = []
    for _, row in df.iterrows():
        try:
            expense = row.get(mapping.get("expense", ""), 0)
            income = row.get(mapping.get("income", ""), 0)

            expense = int(float(str(expense).replace(",", "").strip())) if pd.notna(expense) else 0
            income = int(float(str(income).replace(",", "").strip())) if pd.notna(income) else 0

            amount = income - expense

            t = Transaction(
                date=pd.to_datetime(row[mapping["date"]]).date(),
                amount=amount,
                description=str(row[mapping["description"]]).strip(),
                source=filepath.name,
            )
            transactions.append(t)
        except Exception as e:
            logger.warning(f"行スキップ: {e}")
            continue

    logger.info(f"{len(transactions)}件読み込み完了: {filepath.name}")
    return transactions




