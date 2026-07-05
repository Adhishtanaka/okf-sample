#!/usr/bin/env python3
"""Read-only REST API for orders/customers/products, matching bundle/apis/orders_api.md."""

import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import queries
from db import init_db

ORDER_PATH = re.compile(r"^/v1/orders/([^/]+)$")
CUSTOMER_PATH = re.compile(r"^/v1/customers/([^/]+)$")
PRODUCT_PATH = re.compile(r"^/v1/products/([^/]+)$")


class Handler(BaseHTTPRequestHandler):
    def _json(self, status: int, payload) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _one_or_404(self, row, not_found: str) -> None:
        self._json(200, row) if row else self._json(404, {"error": not_found})

    def do_GET(self) -> None:
        if self.path == "/v1/orders":
            self._json(200, queries.list_orders())
        elif self.path == "/v1/customers":
            self._json(200, queries.list_customers())
        elif self.path == "/v1/products":
            self._json(200, queries.list_products())
        elif self.path == "/v1/metrics/daily_revenue":
            self._json(200, queries.daily_revenue())
        elif match := ORDER_PATH.match(self.path):
            self._one_or_404(queries.get_order(match.group(1)), "order not found")
        elif match := CUSTOMER_PATH.match(self.path):
            self._one_or_404(queries.get_customer(match.group(1)), "customer not found")
        elif match := PRODUCT_PATH.match(self.path):
            self._one_or_404(queries.get_product(match.group(1)), "product not found")
        else:
            self._json(404, {"error": "not found"})

    def log_message(self, fmt, *args) -> None:
        pass  # ponytail: quiet by default, re-enable if you need request logs


if __name__ == "__main__":
    init_db()
    server = ThreadingHTTPServer(("localhost", 8000), Handler)
    print("serving on http://localhost:8000")
    server.serve_forever()
