CREATE INDEX idx_transactions_metadata_gin
ON performance_lab.transactions
USING GIN (metadata);