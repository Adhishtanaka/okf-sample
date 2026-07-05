---
type: SQLite Table
title: orders
description: One row per customer order (header only); line items live in order_items.
resource: sqlite:///ecom.db#orders
tags: [ecommerce, orders, core]
timestamp: 2026-07-05T00:00:00Z
---

# Schema
| column | type | description |
|---|---|---|
| order_id | TEXT | Primary key |
| customer_id | TEXT | FK to customers |
| status | TEXT | `completed`, `refunded`, or `pending` |
| created_at | TEXT | Order creation time (ISO 8601) |

An order's total is not stored here — it's computed by summing
[order_items](/tables/order_items_table.md) rows for that `order_id`.

# Examples
See [daily_revenue metric](/metrics/daily_revenue.md) for a query built on this table,
and the [orders API](/apis/orders_api.md) for how it's served to clients.

# Citations
Part of [ecommerce dataset](/datasets/orders.md). Refund eligibility governed by the
[refund policy](/policies/refund_policy.md).
