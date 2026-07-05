---
type: SQLite Table
title: order_items
description: Line items — one row per (order, product) pair, with quantity and price snapshot.
resource: sqlite:///ecom.db#order_items
tags: [ecommerce, orders, products, core]
timestamp: 2026-07-05T00:00:00Z
---

# Schema
| column | type | description |
|---|---|---|
| order_id | TEXT | FK to orders |
| product_id | TEXT | FK to products |
| quantity | INTEGER | Units purchased |
| unit_price_usd | REAL | Price at the time of purchase (snapshot, not live catalog price) |

Primary key is `(order_id, product_id)`.

# Examples
An order's total is `SUM(quantity * unit_price_usd)` grouped by `order_id` — see
[daily_revenue metric](/metrics/daily_revenue.md) for the same pattern applied across
all orders.

# Citations
Joins [orders](/tables/orders_table.md) to [products](/tables/products_table.md).
