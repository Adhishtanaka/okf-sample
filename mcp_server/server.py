#!/usr/bin/env python3
"""MCP server exposing the OKF bundle's knowledge plus live order data."""

import sqlite3
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
from bundle_lib import load_bundle  # noqa: E402

BUNDLE_ROOT = ROOT / "bundle"
DB_PATH = ROOT / "ecom.db"

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
    """Look up a real order from the live SQLite orders table (ecom.db)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM orders WHERE order_id = ?", (order_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else {"error": f"no order with id {order_id}"}


if __name__ == "__main__":
    mcp.run()
