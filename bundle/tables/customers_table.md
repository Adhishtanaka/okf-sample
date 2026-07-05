---
type: SQLite Table
title: customers
description: One row per customer — name and email, referenced by orders.customer_id.
resource: sqlite:///ecom.db#customers
tags: [ecommerce, customers, core]
timestamp: 2026-07-05T00:00:00Z
---

# Schema
| column | type | description |
|---|---|---|
| customer_id | TEXT | Primary key |
| name | TEXT | Customer's full name |
| email | TEXT | Customer's email address |

# Examples
Joined into [orders API](/apis/orders_api.md) responses and the
[orders table](/tables/orders_table.md)'s `customer_id` foreign key.

# Citations
Part of [ecommerce dataset](/datasets/orders.md).
