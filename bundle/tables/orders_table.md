---
type: SQLite Table
title: orders
description: One row per customer order, stored in the local ecom.db SQLite file.
resource: sqlite:///ecom.db#orders
tags: [ecommerce, orders, core]
timestamp: 2026-07-05T00:00:00Z
---

# Schema
| column | type | description |
|---|---|---|
| order_id | TEXT | Primary key |
| customer_id | TEXT | FK to customers |
| amount_usd | REAL | Order total |
| created_at | TEXT | Order creation time (ISO 8601) |

# Examples
See [daily_revenue metric](/metrics/daily_revenue.md) for a query built on this table,
and the [orders API](/apis/orders_api.md) for how it's served to clients.

# Citations
Part of [orders dataset](/datasets/orders.md).
