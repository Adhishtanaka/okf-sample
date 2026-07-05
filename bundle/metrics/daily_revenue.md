---
type: Metric
title: daily_revenue
description: Sum of completed order line-item totals, grouped by day, used on the exec dashboard.
resource: sqlite:///ecom.db#daily_revenue
tags: [ecommerce, revenue, kpi]
timestamp: 2026-07-05T00:00:00Z
---

# Schema
```sql
SELECT substr(orders.created_at, 1, 10) AS day,
       ROUND(SUM(order_items.quantity * order_items.unit_price_usd), 2) AS revenue_usd
FROM orders JOIN order_items ON orders.order_id = order_items.order_id
WHERE orders.status = 'completed'
GROUP BY day ORDER BY day
```
Served live at `GET /v1/metrics/daily_revenue` (see [orders API](/apis/orders_api.md)).
`refunded`/`pending` orders are excluded per the [refund policy](/policies/refund_policy.md).

# Examples
A sudden drop in this metric triggers the
[investigate revenue drop playbook](/playbooks/investigate_revenue_drop.md).

# Citations
Built on [orders](/tables/orders_table.md) joined with [order_items](/tables/order_items_table.md).
