---
type: API Endpoint
title: GET /v1/orders/{order_id}
description: Public REST endpoint returning a single order, its customer, and line items.
resource: http://localhost:8000/v1/orders/{order_id}
tags: [ecommerce, api, orders]
timestamp: 2026-07-05T00:00:00Z
---

# Schema
Returns `order_id`, `customer_id`, `customer_name`, `customer_email`, `status`,
`created_at`, `total_usd`, and an `items` array of
`{product_id, name, quantity, unit_price_usd, line_total_usd}` —
joins [orders](/tables/orders_table.md), [customers](/tables/customers_table.md),
[order_items](/tables/order_items_table.md), and [products](/tables/products_table.md).

Related read-only endpoints on the same server: `GET /v1/orders` (list, with `total_usd`
but no `items`), `GET /v1/customers`, `GET /v1/customers/{id}`, `GET /v1/products`,
`GET /v1/products/{id}`.

# Examples
```
GET /v1/orders/ord_001
-> {
  "order_id": "ord_001", "customer_id": "cust_1", "customer_name": "Alice Nguyen",
  "customer_email": "alice@example.com", "status": "completed",
  "created_at": "2026-07-01T10:00:00Z", "total_usd": 33.5,
  "items": [
    {"product_id": "prod_1", "name": "Wireless Mouse", "quantity": 1, "unit_price_usd": 25.0, "line_total_usd": 25.0},
    {"product_id": "prod_5", "name": "Notebook", "quantity": 2, "unit_price_usd": 4.25, "line_total_usd": 8.5}
  ]
}
```

# Citations
Backed by [orders table](/tables/orders_table.md), [order_items](/tables/order_items_table.md),
[products](/tables/products_table.md), and [customers](/tables/customers_table.md).
