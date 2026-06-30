# Money Manager

A backend tool that imports household budget CSVs into SQLite and provides income/expense summaries and category breakdowns via API.

## Features

- Import CSVs from various banks/cards (automatic column detection, multi-encoding support)
- Save to SQLite with duplicate prevention
- Manual category classification, automatically applied to future imports
- Get income/expense summary for a given date range
- Get category breakdown for a given date range
- Get transaction list for a given date range
- REST API powered by FastAPI

## Tech Stack

- Python 3.11+
- pandas (CSV reading and data processing)
- SQLite (data storage)
- FastAPI / Uvicorn (API)

## Project Structure

src/tracker/
├── models.py # Transaction dataclass
├── loader.py # CSV reading and column auto-detection
├── database.py # SQLite read/write and aggregation
├── logger.py # Logging
├── api/
│ └── main.py # FastAPI endpoints
└── main.py # CLI entry point

## Setup

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
pip install -e .
```

## Usage

### Import a CSV

```bash
python -m tracker import data/raw/your_file.csv
```

### Start the API server

```bash
uvicorn tracker.api.main:app --reload
```

API docs available at `http://127.0.0.1:8000/docs`.

### API Endpoints

| Method | Path              | Description                             |
| ------ | ----------------- | --------------------------------------- |
| GET    | /summary          | Income/expense summary for a date range |
| GET    | /summary/category | Category breakdown for a date range     |
| GET    | /transactions     | Transaction list for a date range       |

Query parameters: `start_date`, `end_date` (format: `YYYY-MM-DD`)

## License

MIT License
