import sys
from pathlib import Path
from tracker.analyzer import load_csv
from tracker.database import init_db, save_transactions, get_category_mapping
from tracker.logger import get_logger



logger = get_logger(__name__)

def main():
    if len(sys.argv) < 3 or sys.argv[1] != "import":
        print("使い方: python -m tracker import <CSVファイルパス>")
        sys.exit(1)

    filepath = Path(sys.argv[2])
    if not filepath.exists():
        logger.error(f"ファイルが見つかりません: {filepath}")
        sys.exit(1)

    init_db()
    category_mapping = get_category_mapping()
    transactions = load_csv(filepath, category_mapping)
    saved = save_transactions(transactions)
    print(f"{saved}件保存しました（スキップ: {len(transactions) - saved}件）")

if __name__ == "__main__":
    main()