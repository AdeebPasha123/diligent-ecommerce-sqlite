"""Synthetic data generator for e-commerce datasets."""
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

NUM_CUSTOMERS = 15
NUM_PRODUCTS = 12
NUM_ORDERS = 30

FIRST_NAMES = ["Avery", "Jordan", "Taylor", "Riley", "Quinn", "Morgan", "Casey", "Kai", "Emery", "Hayden"]
LAST_NAMES = ["Reed", "Patel", "Nguyen", "Garcia", "Kim", "Thompson", "Lewis", "Singh", "Wright", "Lopez"]
CATEGORIES = ["Electronics", "Home", "Outdoors", "Beauty", "Fitness", "Toys"]
LOYALTY_TIERS = ["Bronze", "Silver", "Gold", "Platinum"]
ORDER_STATUSES = ["processing", "fulfilled", "cancelled", "returned"]
PAYMENT_METHODS = ["credit_card", "paypal", "apple_pay", "google_pay"]
PAYMENT_STATUS = ["captured", "refunded", "pending"]
CARRIERS = ["UPS", "FedEx", "USPS", "DHL"]
STATES = ["CA", "NY", "TX", "WA", "IL", "FL", "MA", "GA"]

start_date = datetime(2024, 1, 1)


def random_date(start: datetime, days: int = 365) -> datetime:
    return start + timedelta(days=random.randint(0, days), hours=random.randint(0, 23))


def build_customers():
    customers = []
    for cid in range(1, NUM_CUSTOMERS + 1):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        created = random_date(start_date)
        customers.append(
            {
                "customer_id": cid,
                "first_name": first,
                "last_name": last,
                "email": f"{first.lower()}.{last.lower()}{cid}@example.com",
                "phone": f"+1-555-{random.randint(100, 999):03d}-{random.randint(1000, 9999):04d}",
                "loyalty_tier": random.choice(LOYALTY_TIERS),
                "created_at": created.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
    return customers


def build_products():
    products = []
    for pid in range(1, NUM_PRODUCTS + 1):
        category = random.choice(CATEGORIES)
        base_price = random.uniform(10, 300)
        products.append(
            {
                "product_id": pid,
                "product_name": f"{category} Item {pid}",
                "category": category,
                "unit_price": round(base_price, 2),
                "stock_qty": random.randint(15, 300),
                "active": random.choice(["true", "true", "false"]),
            }
        )
    return products


customers = build_customers()
products = build_products()

product_price_map = {p["product_id"]: p["unit_price"] for p in products}

orders = []
payments = []
shipping = []

for oid in range(1, NUM_ORDERS + 1):
    customer = random.choice(customers)
    order_date = random_date(start_date)
    num_items = random.randint(1, 4)
    product_ids = random.sample(list(product_price_map.keys()), num_items)
    subtotal = sum(product_price_map[pid] * random.randint(1, 3) for pid in product_ids)
    primary_product_id = product_ids[0]
    order_status = random.choices(ORDER_STATUSES, weights=[0.6, 0.25, 0.1, 0.05])[0]

    orders.append(
        {
            "order_id": oid,
            "customer_id": customer["customer_id"],
            "order_date": order_date.strftime("%Y-%m-%d %H:%M:%S"),
            "order_status": order_status,
            "total_amount": round(subtotal, 2),
            "primary_product_id": primary_product_id,
        }
    )

    payment_status = random.choices(PAYMENT_STATUS, weights=[0.7, 0.1, 0.2])[0]
    payments.append(
        {
            "payment_id": oid,
            "order_id": oid,
            "payment_date": (order_date + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
            "payment_method": random.choice(PAYMENT_METHODS),
            "amount": round(subtotal, 2),
            "currency": "USD",
            "payment_status": payment_status,
        }
    )

    shipment_date = order_date + timedelta(days=random.randint(0, 3))
    delivery_date = shipment_date + timedelta(days=random.randint(2, 7))
    shipping.append(
        {
            "shipment_id": oid,
            "order_id": oid,
            "shipped_date": shipment_date.strftime("%Y-%m-%d"),
            "delivery_date": delivery_date.strftime("%Y-%m-%d"),
            "carrier": random.choice(CARRIERS),
            "tracking_number": f"TRK{oid:05d}{random.randint(100,999)}",
            "shipping_cost": round(random.uniform(4.99, 19.99), 2),
            "destination_state": random.choice(STATES),
        }
    )


def write_csv(filename: str, fieldnames, rows):
    with open(DATA_DIR / filename, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


write_csv(
    "customers.csv",
    ["customer_id", "first_name", "last_name", "email", "phone", "loyalty_tier", "created_at"],
    customers,
)
write_csv(
    "products.csv",
    ["product_id", "product_name", "category", "unit_price", "stock_qty", "active"],
    products,
)
write_csv(
    "orders.csv",
    ["order_id", "customer_id", "order_date", "order_status", "total_amount", "primary_product_id"],
    orders,
)
write_csv(
    "payments.csv",
    ["payment_id", "order_id", "payment_date", "payment_method", "amount", "currency", "payment_status"],
    payments,
)
write_csv(
    "shipping.csv",
    ["shipment_id", "order_id", "shipped_date", "delivery_date", "carrier", "tracking_number", "shipping_cost", "destination_state"],
    shipping,
)

print(f"Datasets generated in {DATA_DIR}")
