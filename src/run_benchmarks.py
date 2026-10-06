from pathlib import Path

from database import get_connection


BASE_DIR = Path(__file__).parent.parent

BASELINE_FILE = BASE_DIR / "sql" / "02_baseline_queries.sql"
DROP_INDEXES_FILE = BASE_DIR / "sql" / "03_drop_indexes.sql"
CREATE_INDEXES_FILE = BASE_DIR / "sql" / "04_create_indexes.sql"
UNOPTIMIZED_FILE = BASE_DIR / "sql" / "06_unoptimized_queries.sql"
OPTIMIZED_FILE = BASE_DIR / "sql" / "05_optimized_queries.sql"
JSONB_BASELINE_FILE = BASE_DIR / "sql" / "07_jsonb_baseline.sql"
DROP_JSONB_INDEX_FILE = BASE_DIR / "sql" / "08_drop_jsonb_index.sql"
CREATE_JSONB_INDEX_FILE = BASE_DIR / "sql" / "09_create_jsonb_index.sql"


def read_sql(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def run_benchmark(cursor, query, label):
    cursor.execute(query)
    results = cursor.fetchall()

    print(f"\n{label}")
    print("-" * 60)

    for row in results:
        print(row[0])


baseline_sql = read_sql(BASELINE_FILE)
drop_indexes_sql = read_sql(DROP_INDEXES_FILE)
create_indexes_sql = read_sql(CREATE_INDEXES_FILE)
unoptimized_sql = read_sql(UNOPTIMIZED_FILE)
optimized_sql = read_sql(OPTIMIZED_FILE)
jsonb_baseline_sql = read_sql(JSONB_BASELINE_FILE)
drop_jsonb_index_sql = read_sql(DROP_JSONB_INDEX_FILE)
create_jsonb_index_sql = read_sql(CREATE_JSONB_INDEX_FILE)

with get_connection() as connection:
    with connection.cursor() as cursor:

        # Test 1: Index impact
        cursor.execute(drop_indexes_sql)

        run_benchmark(
            cursor,
            baseline_sql,
            "Baseline - Without Performance Indexes"
        )

        cursor.execute(create_indexes_sql)

        run_benchmark(
            cursor,
            baseline_sql,
            "Baseline - With Performance Indexes"
        )

        # Test 2: Query rewrite impact
        run_benchmark(
            cursor,
            unoptimized_sql,
            "Unoptimized Query"
        )

        run_benchmark(
            cursor,
            optimized_sql,
            "Optimized Query"
        )
        # Test 3: JSONB index impact

        cursor.execute(drop_jsonb_index_sql)

        run_benchmark(
            cursor,
            jsonb_baseline_sql,
            "JSONB - Without GIN Index"
        )

        cursor.execute(create_jsonb_index_sql)

        run_benchmark(
            cursor,
            jsonb_baseline_sql,
            "JSONB - With GIN Index"
        )