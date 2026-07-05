---
type: API Endpoint
title: GET /v1/orders/{order_id}
description: Public REST endpoint returning a single order by id.
resource: http://localhost:8000/v1/orders/{order_id}
tags: [ecommerce, api, orders]
timestamp: 2026-06-20T00:00:00Z
---

# Schema
Returns JSON with `order_id`, `customer_id`, `amount_usd`, `created_at` —
mirrors the [orders table](/tables/orders_table.md) row shape.

# Examples
```
GET /v1/orders/abc123
-> {"order_id": "abc123", "customer_id": "cust_9", "amount_usd": 42.50, "created_at": "2026-07-01T10:00:00Z"}
```

# Citations
Backed by [orders table](/tables/orders_table.md).
