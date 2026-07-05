#!/usr/bin/env python3
"""Create and seed ecom.db: customers, products, orders, order_items.

Matches the schemas documented in bundle/tables/*.md.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "ecom.db"

SEED_CUSTOMERS = [
    ("cust_1", "Alice Nguyen", "alice@example.com"),
    ("cust_2", "Bilal Khan", "bilal@example.com"),
    ("cust_3", "Chidi Okafor", "chidi@example.com"),
    ("cust_4", "Dana Silva", "dana@example.com"),
    ("cust_5", "Eve Larsson", "eve@example.com"),
]

SEED_PRODUCTS = [
    ("prod_1", "Wireless Mouse", "electronics", 25.00, 100),
    ("prod_2", "Mechanical Keyboard", "electronics", 75.00, 50),
    ("prod_3", "USB-C Cable", "electronics", 9.99, 200),
    ("prod_4", "Coffee Mug", "home", 12.50, 150),
    ("prod_5", "Notebook", "office", 4.25, 300),
    ("prod_6", "Desk Lamp", "home", 34.00, 40),
    ("prod_7", "Backpack", "accessories", 55.00, 60),
    ("prod_8", "Water Bottle", "accessories", 18.00, 120),
]

# (order_id, customer_id, status, created_at)
SEED_ORDERS = [
    ("ord_001", "cust_1", "completed", "2026-07-01T10:00:00Z"),
    ("ord_002", "cust_2", "completed", "2026-07-01T14:30:00Z"),
    ("ord_003", "cust_1", "completed", "2026-07-02T09:15:00Z"),
    ("ord_004", "cust_3", "refunded", "2026-07-02T11:45:00Z"),
    ("ord_005", "cust_4", "completed", "2026-07-02T20:05:00Z"),
    ("ord_006", "cust_2", "completed", "2026-07-03T08:00:00Z"),
    ("ord_007", "cust_5", "completed", "2026-07-03T16:20:00Z"),
    ("ord_008", "cust_3", "pending", "2026-07-04T13:10:00Z"),
]

# (order_id, product_id, quantity, unit_price_usd) -- price snapshot at order time
SEED_ORDER_ITEMS = [
    ("ord_001", "prod_1", 1, 25.00),
    ("ord_001", "prod_5", 2, 4.25),
    ("ord_002", "prod_4", 1, 12.50),
    ("ord_002", "prod_3", 1, 9.99),
    ("ord_003", "prod_2", 1, 75.00),
    ("ord_004", "prod_5", 3, 4.25),
    ("ord_005", "prod_7", 1, 55.00),
    ("ord_005", "prod_8", 1, 18.00),
    ("ord_006", "prod_6", 1, 34.00),
    ("ord_007", "prod_2", 1, 75.00),
    ("ord_007", "prod_1", 1, 25.00),
    ("ord_007", "prod_8", 1, 18.00),
    ("ord_008", "prod_4", 2, 12.50),
]

SCHEMA = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price_usd REAL NOT NULL,
    stock_qty INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL REFERENCES customers(customer_id),
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS order_items (
    order_id TEXT NOT NULL REFERENCES orders(order_id),
    product_id TEXT NOT NULL REFERENCES products(product_id),
    quantity INTEGER NOT NULL,
    unit_price_usd REAL NOT NULL,
    PRIMARY KEY (order_id, product_id)
);
"""


def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    seeds = [
        ("customers", SEED_CUSTOMERS),
        ("products", SEED_PRODUCTS),
        ("orders", SEED_ORDERS),
        ("order_items", SEED_ORDER_ITEMS),
    ]
    for table, rows in seeds:
        if conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] == 0:
            placeholders = ", ".join("?" * len(rows[0]))
            conn.executemany(f"INSERT INTO {table} VALUES ({placeholders})", rows)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"ready: {DB_PATH}")
