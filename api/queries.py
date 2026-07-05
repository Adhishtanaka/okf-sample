"""Shared SQLite queries over ecom.db, used by both api/server.py and mcp_server/server.py."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "ecom.db"


def _all(sql: str, params: tuple = ()) -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = [dict(row) for row in conn.execute(sql, params).fetchall()]
    conn.close()
    return rows


def _one(sql: str, params: tuple = ()) -> dict | None:
    rows = _all(sql, params)
    return rows[0] if rows else None


def list_customers() -> list[dict]:
    return _all("SELECT * FROM customers ORDER BY customer_id")


def get_customer(customer_id: str) -> dict | None:
    return _one("SELECT * FROM customers WHERE customer_id = ?", (customer_id,))


def list_products() -> list[dict]:
    return _all("SELECT * FROM products ORDER BY product_id")


def get_product(product_id: str) -> dict | None:
    return _one("SELECT * FROM products WHERE product_id = ?", (product_id,))


def list_orders() -> list[dict]:
    return _all(
        """
        SELECT orders.order_id, orders.customer_id, customers.name AS customer_name,
               orders.status, orders.created_at,
               ROUND(SUM(order_items.quantity * order_items.unit_price_usd), 2) AS total_usd
        FROM orders
        JOIN customers ON orders.customer_id = customers.customer_id
        JOIN order_items ON orders.order_id = order_items.order_id
        GROUP BY orders.order_id
        ORDER BY orders.created_at
        """
    )


def get_order(order_id: str) -> dict | None:
    header = _one(
        """
        SELECT orders.order_id, orders.customer_id, customers.name AS customer_name,
               customers.email AS customer_email, orders.status, orders.created_at
        FROM orders JOIN customers ON orders.customer_id = customers.customer_id
        WHERE orders.order_id = ?
        """,
        (order_id,),
    )
    if header is None:
        return None
    items = _all(
        """
        SELECT order_items.product_id, products.name, order_items.quantity,
               order_items.unit_price_usd,
               ROUND(order_items.quantity * order_items.unit_price_usd, 2) AS line_total_usd
        FROM order_items JOIN products ON order_items.product_id = products.product_id
        WHERE order_items.order_id = ?
        """,
        (order_id,),
    )
    header["items"] = items
    header["total_usd"] = round(sum(item["line_total_usd"] for item in items), 2)
    return header


def daily_revenue() -> list[dict]:
    """Revenue by day, completed orders only (refunded/pending don't count)."""
    return _all(
        """
        SELECT substr(orders.created_at, 1, 10) AS day,
               ROUND(SUM(order_items.quantity * order_items.unit_price_usd), 2) AS revenue_usd
        FROM orders JOIN order_items ON orders.order_id = order_items.order_id
        WHERE orders.status = 'completed'
        GROUP BY day ORDER BY day
        """
    )
