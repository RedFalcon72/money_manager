from fastapi import FastAPI, UploadFile, File
from typing import Optional
import tempfile
from pathlib import Path
from tracker.database import (
    get_summary,
    get_category_summary,
    get_transactions,
    get_category_mapping,
    update_category,
    init_db,
)
from tracker.loader import load_csv
from tracker.database import save_transactions
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/summary")
def summary(start_date: str, end_date: str):
    return get_summary(start_date, end_date)

@app.get("/summary/category")
def summary_category(start_date: str, end_date: str):
    return get_category_summary(start_date, end_date)

@app.get("/transactions")
def transactions(start_date: str, end_date: str, category: Optional[str] = None):
    result = get_transactions(start_date, end_date)
    if category:
        result = [t for t in result if t["category"] == category]
    return result

@app.post("/import")
async def import_csv(file: UploadFile = File(...)):
    init_db()
    category_mapping = get_category_mapping()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = Path(tmp.name)
    transactions = load_csv(tmp_path, category_mapping)
    saved = save_transactions(transactions)
    tmp_path.unlink()
    return {"imported": len(transactions), "saved": saved}

@app.put("/transactions/{transaction_id}/category")
def update_transaction_category(transaction_id: int, category: str):
    update_category(transaction_id, category)
    return {"message": "updated"}