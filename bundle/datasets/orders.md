---
type: SQLite Database
title: ecommerce
description: Database holding customers, products, orders, and order_items for the storefront.
resource: sqlite:///ecom.db
tags: [ecommerce, core]
timestamp: 2026-07-05T00:00:00Z
---

# Schema
Four tables: [customers](/tables/customers_table.md), [products](/tables/products_table.md),
[orders](/tables/orders_table.md) (headers), and
[order_items](/tables/order_items_table.md) (line items, joining orders to products).

# Citations
Owned by the Storefront Data team.
