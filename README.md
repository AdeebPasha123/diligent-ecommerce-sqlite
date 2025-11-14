# E-commerce Analytics Mini Project

A small, self-contained project that generates synthetic e-commerce datasets, loads them into a local SQLite database, and provides example SQL analytics queries. It's ideal for learning SQL analytics workflows, testing query ideas, or teaching data ingestion from CSV to SQLite.

## Project Structure
- `data/`: synthetic CSV datasets and generated `ecommerce.db`
- `scripts/`: automation scripts (`generate_data.py`, `ingest_sqlite.py`, `show_query_example.py`)
- `sql/`: schema definition and analytics queries

## How to Reproduce
1. `python scripts/generate_data.py`
2. `python scripts/ingest_sqlite.py`
3. (Optional) `python scripts/show_query_example.py`

## GitHub Setup
```
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo>.git
git push -u origin main
```
