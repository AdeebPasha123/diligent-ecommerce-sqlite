"""Ingest synthetic CSV datasets into an SQLite database."""
import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
SQL_DIR = ROOT / "sql"
DB_PATH = DATA_DIR / "ecommerce.db"
SCHEMA_PATH = SQL_DIR / "schema.sql"

TABLE_CONFIG = {
    "customers": [
        ("customer_id", int),
        ("first_name", str),
        ("last_name", str),
        ("email", str),
        ("phone", str),
        ("loyalty_tier", str),
        ("created_at", str),
    ],
    "products": [
        ("product_id", int),
        ("product_name", str),
        ("category", str),
        ("unit_price", float),
        ("stock_qty", int),
        ("active", str),
    ],
    "orders": [
        ("order_id", int),
        ("customer_id", int),
        ("order_date", str),
        ("order_status", str),
        ("total_amount", float),
        ("primary_product_id", int),
    ],
    "payments": [
        ("payment_id", int),
        ("order_id", int),
        ("payment_date", str),
        ("payment_method", str),
        ("amount", float),
        ("currency", str),
        ("payment_status", str),
    ],
    "shipping": [
        ("shipment_id", int),
        ("order_id", int),
        ("shipped_date", str),
        ("delivery_date", str),
        ("carrier", str),
        ("tracking_number", str),
        ("shipping_cost", float),
        ("destination_state", str),
    ],
}


def load_rows(table_name: str):
    csv_path = DATA_DIR / f"{table_name}.csv"
    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            yield tuple(caster(row[column]) for column, caster in TABLE_CONFIG[table_name])


def main():
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Missing schema at {SCHEMA_PATH}")

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
        conn.executescript(schema_sql)

        for table in TABLE_CONFIG:
            rows = list(load_rows(table))
            placeholders = ",".join(["?"] * len(TABLE_CONFIG[table]))
            columns = ",".join(col for col, _ in TABLE_CONFIG[table])
            conn.executemany(
                f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
                rows,
            )
            conn.commit()
            print(f"Loaded {len(rows)} rows into {table}")

    print(f"SQLite database ready at {DB_PATH}")


if __name__ == "__main__":
    main()
