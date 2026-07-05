#!/usr/bin/env python3
"""MCP server exposing the OKF bundle's knowledge plus live ecom.db data."""

import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "api"))
from bundle_lib import load_bundle  # noqa: E402
import queries  # noqa: E402

BUNDLE_ROOT = ROOT / "bundle"

mcp = FastMCP("okf-sample")
_concepts = load_bundle(BUNDLE_ROOT)


def _make_reader(path: Path):
    def _read() -> str:
        return path.read_text()

    return _read


for _rel_path, _meta in _concepts.items():
    mcp.resource(
        f"okf://{_rel_path.lstrip('/')}",
        name=_meta.get("title", _rel_path),
        description=_meta.get("description"),
        mime_type="text/markdown",
    )(_make_reader(BUNDLE_ROOT / _rel_path.lstrip("/")))


@mcp.tool()
def list_concepts(type: str | None = None) -> list[dict]:
    """List OKF bundle concepts, optionally filtered by `type`.

    Each entry's `resource_uri` is the exact string to pass to a resource read
    (e.g. "okf://tables/orders_table.md") — use it as-is, don't guess a path.
    """
    return [
        {
            "path": path,
            "resource_uri": f"okf://{path.lstrip('/')}",
            "type": meta["type"],
            "title": meta.get("title"),
        }
        for path, meta in _concepts.items()
        if type is None or meta["type"] == type
    ]


@mcp.tool()
def read_concept(path: str) -> str:
    """Read one bundle concept's raw markdown by path — forgiving of format:
    accepts "tables/orders_table.md", "/tables/orders_table.md", or
    "okf://tables/orders_table.md" alike. Prefer this over guessing a resource URI.
    """
    key = "/" + path.removeprefix("okf://").lstrip("/")
    if key not in _concepts:
        return f"error: no concept at {path!r}. Call list_concepts() to see valid paths."
    return (BUNDLE_ROOT / key.lstrip("/")).read_text()


@mcp.tool()
def list_orders() -> list[dict]:
    """List all orders (customer, status, total) from the live ecom.db."""
    return queries.list_orders()


@mcp.tool()
def get_order(order_id: str) -> dict:
    """Look up a real order (customer, status, line items, total) from ecom.db."""
    return queries.get_order(order_id) or {"error": f"no order with id {order_id}"}


@mcp.tool()
def list_customers() -> list[dict]:
    """List all customers from the live customers table (ecom.db)."""
    return queries.list_customers()


@mcp.tool()
def get_customer(customer_id: str) -> dict:
    """Look up a real customer from the live customers table (ecom.db)."""
    return queries.get_customer(customer_id) or {"error": f"no customer with id {customer_id}"}


@mcp.tool()
def list_products() -> list[dict]:
    """List all products in the catalog from the live products table (ecom.db)."""
    return queries.list_products()


@mcp.tool()
def get_product(product_id: str) -> dict:
    """Look up a real product from the live products table (ecom.db)."""
    return queries.get_product(product_id) or {"error": f"no product with id {product_id}"}


if __name__ == "__main__":
    mcp.run()
