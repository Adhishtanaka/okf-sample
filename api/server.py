#!/usr/bin/env python3
"""Read-only REST API for the orders table, matching bundle/apis/orders_api.md."""

import json
import re
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from db import DB_PATH, init_db

ORDER_PATH = re.compile(r"^/v1/orders/([^/]+)$")


def query(sql: str, params: tuple = ()) -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


class Handler(BaseHTTPRequestHandler):
    def _json(self, status: int, payload) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/v1/orders":
            self._json(200, query("SELECT * FROM orders ORDER BY created_at"))
        elif self.path == "/v1/metrics/daily_revenue":
            rows = query(
                """
                SELECT substr(created_at, 1, 10) AS day, SUM(amount_usd) AS revenue_usd
                FROM orders GROUP BY day ORDER BY day
                """
            )
            self._json(200, rows)
        elif match := ORDER_PATH.match(self.path):
            rows = query("SELECT * FROM orders WHERE order_id = ?", (match.group(1),))
            if rows:
                self._json(200, rows[0])
            else:
                self._json(404, {"error": "order not found"})
        else:
            self._json(404, {"error": "not found"})

    def log_message(self, fmt, *args) -> None:
        pass  # ponytail: quiet by default, re-enable if you need request logs


if __name__ == "__main__":
    init_db()
    server = ThreadingHTTPServer(("localhost", 8000), Handler)
    print("serving on http://localhost:8000")
    server.serve_forever()
