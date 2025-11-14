PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS shipping;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    loyalty_tier TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    unit_price REAL NOT NULL,
    stock_qty INTEGER,
    active TEXT DEFAULT 'true'
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    order_status TEXT,
    total_amount REAL NOT NULL,
    primary_product_id INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (primary_product_id) REFERENCES products(product_id)
);

CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    payment_date TEXT NOT NULL,
    payment_method TEXT,
    amount REAL NOT NULL,
    currency TEXT NOT NULL,
    payment_status TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE shipping (
    shipment_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    shipped_date TEXT,
    delivery_date TEXT,
    carrier TEXT,
    tracking_number TEXT,
    shipping_cost REAL,
    destination_state TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
