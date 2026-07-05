---
type: Policy
title: Shipping Policy
description: Rules for how and when orders ship once placed.
tags: [ecommerce, policy, shipping]
timestamp: 2026-07-05T00:00:00Z
---

# Rules
1. Orders ship within 2 business days of `status` becoming `completed`.
2. `pending` orders have not been charged yet and do not ship.
3. Orders over $75 ship free; otherwise a flat $5 shipping fee applies (not modeled
   in [order_items](/tables/order_items_table.md) in this sample).

# Examples
`ord_008` in the sample data is `pending`, so it has not shipped yet.

# Citations
Applies to rows in [orders table](/tables/orders_table.md) once `status = 'completed'`.
