EXPLAIN ANALYZE
WITH account_totals AS (
    SELECT
        account_id,
        SUM(amount) AS total_amount
    FROM performance_lab.transactions
    GROUP BY account_id
)
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    SUM(at.total_amount) AS total_amount
FROM performance_lab.customers c
JOIN performance_lab.accounts a
    ON c.customer_id = a.customer_id
JOIN account_totals at
    ON a.account_id = at.account_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name;