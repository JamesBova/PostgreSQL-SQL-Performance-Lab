# PostgreSQL SQL Performance Lab

This project demonstrates PostgreSQL query-performance analysis using a reproducible synthetic dataset.

The lab focuses on:

- measuring baseline query performance with `EXPLAIN ANALYZE`
- evaluating the effect of indexes
- comparing unoptimized vs optimized SQL
- benchmarking JSONB queries with and without a GIN index

## Technologies

- PostgreSQL
- Python
- psycopg
- Faker
- CSV
- JSONB
- Git

## Project Flow

Create schema  
→ Generate synthetic data  
→ Load data into PostgreSQL  
→ Remove performance indexes  
→ Run baseline benchmarks  
→ Create indexes  
→ Rerun benchmarks  
→ Compare query rewrites  
→ Benchmark JSONB with and without GIN indexing

## Dataset

The generated dataset currently contains approximately:

- 1,000 customers
- 2,000 accounts
- 100 merchants
- 100,000 transactions

Synthetic data is generated with Python and Faker using deterministic random seeds so benchmark runs can be reproduced.

Generated CSV files are not stored in Git. They can be recreated by running:

    python src\generate_data.py

## Benchmark Results

### Account Lookup: Index Impact

The first benchmark retrieves transactions for a single account.

Without a performance index:

    Seq Scan on transactions
    Rows Removed by Filter: 99,957
    Execution Time: 7.536 ms

After creating an index on `transactions(account_id)`:

    Bitmap Heap Scan on transactions
    Bitmap Index Scan on idx_transactions_account_id
    Execution Time: 0.081 ms

The indexed query was approximately **93x faster** in this test.

The execution plan changed from scanning the entire transaction table to using the index to locate matching rows.

### Query Rewrite Comparison

The unoptimized query joined all 100,000 transaction rows to the account and customer tables before performing aggregation.

Unoptimized query:

    Rows processed through join: 100,000
    Execution Time: 39.033 ms

The optimized version aggregated transaction data by account before joining to the smaller account and customer datasets.

Optimized query:

    Rows passed into later joins: approximately 2,000
    Execution Time: 17.440 ms

The rewritten query was approximately **2.2x faster**.

This demonstrates how reducing the number of rows participating in later joins can improve query execution time.

### JSONB GIN Index Benchmark

The JSONB benchmark searches transaction metadata for:

    {"fraud_review": true}

Without a GIN index:

    Seq Scan on transactions
    Rows Removed by Filter: 95,041
    Execution Time: 11.141 ms

With a GIN index:

    Bitmap Heap Scan on transactions
    Bitmap Index Scan on idx_transactions_metadata_gin
    Execution Time: 2.510 ms

The GIN-indexed query was approximately **4.4x faster**.

This demonstrates how PostgreSQL GIN indexes can improve containment searches against JSONB columns.

## Key Findings

The benchmark results demonstrate several PostgreSQL performance principles:

- indexes can dramatically improve highly selective queries
- PostgreSQL may use bitmap index scans when retrieving multiple matching rows
- reducing rows before joins can improve aggregation-heavy queries
- JSONB containment queries can benefit substantially from GIN indexing
- query plans should be measured rather than assuming a rewrite or index will improve performance

## Running the Project

Initialize the schema:

    python src\initialize_database.py

Generate synthetic data:

    python src\generate_data.py

Load the data:

    python src\load_data.py

Run the benchmarks:

    python src\run_benchmarks.py

## Project Structure

    sql/
        01_create_schema.sql
        02_baseline_queries.sql
        03_drop_indexes.sql
        04_create_indexes.sql
        05_unoptimized_queries.sql
        06_optimized_queries.sql
        07_jsonb_baseline.sql
        08_drop_jsonb_index.sql
        09_create_jsonb_index.sql

    src/
        database.py
        initialize_database.py
        generate_data.py
        load_data.py
        run_benchmarks.py