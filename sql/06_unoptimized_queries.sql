EXPLAIN ANALYZE
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    SUM(t.amount) AS total_amount
FROM performance_lab.customers c
JOIN performance_lab.accounts a
    ON c.customer_id = a.customer_id
JOIN performance_lab.transactions t
    ON a.account_id = t.account_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name;