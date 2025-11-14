"""Utility script to print sample analytics output."""
import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "ecommerce.db"

QUERY = """
SELECT
    pr.product_id,
    pr.product_name,
    pr.category,
    COUNT(o.order_id) AS orders_with_product,
    ROUND(SUM(p.amount), 2) AS revenue_contribution
FROM products pr
JOIN orders o ON o.primary_product_id = pr.product_id
JOIN payments p ON p.order_id = o.order_id AND p.payment_status = 'captured'
GROUP BY pr.product_id, pr.product_name, pr.category
ORDER BY revenue_contribution DESC
LIMIT 5;
"""

with sqlite3.connect(DB_PATH) as conn:
    conn.row_factory = sqlite3.Row
    rows = conn.execute(QUERY).fetchall()

print(json.dumps([dict(r) for r in rows], indent=2))
