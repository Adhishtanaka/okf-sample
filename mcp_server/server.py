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
    """List OKF bundle concepts (path, type, title), optionally filtered by `type`."""
    return [
        {"path": path, "type": meta["type"], "title": meta.get("title")}
        for path, meta in _concepts.items()
        if type is None or meta["type"] == type
    ]


@mcp.tool()
def get_order(order_id: str) -> dict:
    """Look up a real order (customer, status, line items, total) from ecom.db."""
    return queries.get_order(order_id) or {"error": f"no order with id {order_id}"}


@mcp.tool()
def get_customer(customer_id: str) -> dict:
    """Look up a real customer from the live customers table (ecom.db)."""
    return queries.get_customer(customer_id) or {"error": f"no customer with id {customer_id}"}


@mcp.tool()
def get_product(product_id: str) -> dict:
    """Look up a real product from the live products table (ecom.db)."""
    return queries.get_product(product_id) or {"error": f"no product with id {product_id}"}


if __name__ == "__main__":
    mcp.run()
