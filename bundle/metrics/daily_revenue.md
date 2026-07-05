---
type: Metric
title: daily_revenue
description: Sum of amount_usd from orders, grouped by day, used on the exec dashboard.
resource: sqlite:///ecom.db#daily_revenue
tags: [ecommerce, revenue, kpi]
timestamp: 2026-07-05T00:00:00Z
---

# Schema
```sql
SELECT substr(created_at, 1, 10) AS day, SUM(amount_usd) AS revenue_usd
FROM orders GROUP BY day ORDER BY day
```
Served live at `GET /v1/metrics/daily_revenue` (see [orders API](/apis/orders_api.md)).

# Examples
A sudden drop in this metric triggers the
[investigate revenue drop playbook](/playbooks/investigate_revenue_drop.md).

# Citations
Built on the [orders table](/tables/orders_table.md).
