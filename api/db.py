#!/usr/bin/env python3
"""Create and seed ecom.db, matching the schema in bundle/tables/orders_table.md."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "ecom.db"

SEED_ORDERS = [
    ("ord_001", "cust_1", 42.50, "2026-07-01T10:00:00Z"),
    ("ord_002", "cust_2", 18.00, "2026-07-01T14:30:00Z"),
    ("ord_003", "cust_1", 99.99, "2026-07-02T09:15:00Z"),
    ("ord_004", "cust_3", 15.25, "2026-07-02T11:45:00Z"),
    ("ord_005", "cust_4", 60.00, "2026-07-02T20:05:00Z"),
    ("ord_006", "cust_2", 33.10, "2026-07-03T08:00:00Z"),
    ("ord_007", "cust_5", 120.00, "2026-07-03T16:20:00Z"),
    ("ord_008", "cust_3", 27.75, "2026-07-04T13:10:00Z"),
]


def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            amount_usd REAL NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    if conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO orders VALUES (?, ?, ?, ?)", SEED_ORDERS
        )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"ready: {DB_PATH}")
