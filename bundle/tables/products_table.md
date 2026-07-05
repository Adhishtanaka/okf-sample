---
type: SQLite Table
title: products
description: Product catalog — name, category, current price, and stock level.
resource: sqlite:///ecom.db#products
tags: [ecommerce, products, core]
timestamp: 2026-07-05T00:00:00Z
---

# Schema
| column | type | description |
|---|---|---|
| product_id | TEXT | Primary key |
| name | TEXT | Product name |
| category | TEXT | e.g. `electronics`, `home`, `office`, `accessories` |
| price_usd | REAL | Current catalog price |
| stock_qty | INTEGER | Units in stock |

# Examples
Referenced by [order_items](/tables/order_items_table.md), which snapshots
`unit_price_usd` at order time so catalog price changes don't rewrite history.

# Citations
Part of [ecommerce dataset](/datasets/orders.md).
