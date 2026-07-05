# Ecommerce Knowledge Bundle

A sample [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)
bundle describing a fictional storefront's customer/product/order data.

## Datasets
- [ecommerce](/datasets/orders.md) — the SQLite database holding all storefront data

## Tables
- [customers](/tables/customers_table.md) — one row per customer
- [products](/tables/products_table.md) — the product catalog
- [orders](/tables/orders_table.md) — one row per order (header)
- [order_items](/tables/order_items_table.md) — one row per line item

## Metrics
- [daily_revenue](/metrics/daily_revenue.md) — daily revenue KPI (completed orders only)

## APIs
- [GET /v1/orders/{order_id}](/apis/orders_api.md) — order detail, plus list/customers/products endpoints

## Policies
- [Refund Policy](/policies/refund_policy.md)
- [Shipping Policy](/policies/shipping_policy.md)

## Playbooks
- [Investigate a daily_revenue drop](/playbooks/investigate_revenue_drop.md)

See [log.md](/log.md) for the bundle's change history.
