---
type: Policy
title: Refund Policy
description: Rules for when and how a customer order can be refunded.
tags: [ecommerce, policy, refunds]
timestamp: 2026-07-05T00:00:00Z
---

# Rules
1. Orders can be refunded in full within 14 days of `created_at`.
2. Orders over $100 require a manager approval before refunding.
3. Refunds are issued to the original payment method only.
4. A refunded order gets `status = 'refunded'` in the [orders table](/tables/orders_table.md)
   and is excluded from [daily_revenue](/metrics/daily_revenue.md).

# Examples
An order from [orders table](/tables/orders_table.md) placed on 2026-07-01 is refundable
until 2026-07-15. `ord_004` in the sample data is `refunded` for exactly this reason.

# Citations
Applies to rows in [orders table](/tables/orders_table.md); referenced by the
[investigate revenue drop playbook](/playbooks/investigate_revenue_drop.md).
