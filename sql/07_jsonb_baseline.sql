EXPLAIN ANALYZE
SELECT *
FROM performance_lab.transactions
WHERE metadata @> '{"fraud_review": true}';