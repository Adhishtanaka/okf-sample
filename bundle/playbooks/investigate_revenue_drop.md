---
type: Playbook
title: Investigate a daily_revenue drop
description: Steps for on-call to triage a sudden drop in the daily_revenue metric.
tags: [ecommerce, incident, revenue]
timestamp: 2026-06-25T00:00:00Z
---

# Steps
1. Check [daily_revenue metric](/metrics/daily_revenue.md) for the affected day.
2. Query the [orders table](/tables/orders_table.md) directly to rule out a pipeline delay.
3. Check whether an unusual number of orders flipped to `status = 'refunded'` — per the
   [refund policy](/policies/refund_policy.md), refunded orders are excluded from revenue.
4. Check the [orders API](/apis/orders_api.md) error rate — a client-side outage looks
   identical to a real revenue drop.

# Citations
References [daily_revenue](/metrics/daily_revenue.md), [orders table](/tables/orders_table.md),
[orders API](/apis/orders_api.md), and the [refund policy](/policies/refund_policy.md).
