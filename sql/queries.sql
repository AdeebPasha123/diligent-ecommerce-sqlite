-- Useful multi-table analytics queries

-- 1. Lifetime value and order mix per customer
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.loyalty_tier,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(SUM(p.amount), 2) AS lifetime_value,
    MAX(o.order_date) AS last_order_date
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN payments p ON p.order_id = o.order_id
GROUP BY c.customer_id
ORDER BY lifetime_value DESC;

-- 2. Top selling products by captured payments
SELECT
    pr.product_id,
    pr.product_name,
    pr.category,
    COUNT(o.order_id) AS orders_with_product,
    ROUND(SUM(p.amount), 2) AS revenue_contribution
FROM products pr
JOIN orders o ON o.primary_product_id = pr.product_id
JOIN payments p ON p.order_id = o.order_id AND p.payment_status = 'captured'
GROUP BY pr.product_id, pr.product_name, pr.category
ORDER BY revenue_contribution DESC
LIMIT 5;
