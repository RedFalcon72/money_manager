from fastapi import FastAPI
from tracker.database import get_summary, get_category_summary, get_transactions

app = FastAPI()

@app.get("/summary")
def summary(start_date: str, end_date: str):
    return get_summary(start_date, end_date)

@app.get("/summary/category")
def summary_category(start_date: str, end_date: str):
    return get_category_summary(start_date, end_date)

@app.get("/transactions")
def transactions(start_date: str, end_date: str):
    return get_transactions(start_date, end_date)