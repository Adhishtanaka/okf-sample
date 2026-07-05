# Log

## 2026-07-05 (2)
**Update:** Redesigned the schema to be a real relational model: split the flat
`orders.amount_usd` into `products` + `order_items` tables (orders are now headers only,
with a `status` of `completed`/`refunded`/`pending`), added a `customers` table, and added
`policies/refund_policy.md` + `policies/shipping_policy.md`. `daily_revenue` now sums
`order_items` for `completed` orders only. Added `tables/products_table.md` and
`tables/order_items_table.md`. Introduced `api/queries.py` as the shared query layer for
both the REST API and the MCP server.

## 2026-07-05 (1)
**Update:** Moved from documented-only concepts to a real running system: `orders`
now lives in a local SQLite database (`ecom.db`), served by a read-only REST API and
an MCP server that exposes this bundle plus live order lookups to MCP clients.
Updated `datasets/orders.md`, `tables/orders_table.md`, and `apis/orders_api.md`
`type`/`resource` fields from placeholder BigQuery values to the real SQLite/HTTP ones.

## 2026-07-01
**Update:** Added `orders_api.md` endpoint doc and linked it from the orders table and playbook.

## 2026-06-25
**Creation:** Added `investigate_revenue_drop.md` playbook.

## 2026-06-20
**Creation:** Added `daily_revenue.md` metric.

## 2026-06-15
**Creation:** Initial bundle — `datasets/orders.md` and `tables/orders_table.md`.
