from pathlib import Path

from database import get_connection


DATA_DIR = Path(__file__).parent.parent / "data"


def load_csv(cursor, table_name, columns, filename):
    file_path = DATA_DIR / filename

    column_list = ", ".join(columns)

    copy_sql = f"""
        COPY performance_lab.{table_name} ({column_list})
        FROM STDIN
        WITH (
            FORMAT CSV,
            HEADER TRUE
        )
    """

    with open(file_path, "r", encoding="utf-8") as file:
        with cursor.copy(copy_sql) as copy:
            while data := file.read(8192):
                copy.write(data)

    print(f"Loaded {filename}")


with get_connection() as connection:
    with connection.cursor() as cursor:

        load_csv(
            cursor,
            "customers",
            [
                "customer_id",
                "first_name",
                "last_name",
                "email",
                "created_at"
            ],
            "customers.csv"
        )

        load_csv(
            cursor,
            "accounts",
            [
                "account_id",
                "customer_id",
                "account_type",
                "status",
                "opened_date"
            ],
            "accounts.csv"
        )

        load_csv(
            cursor,
            "merchants",
            [
                "merchant_id",
                "merchant_name",
                "merchant_category"
            ],
            "merchants.csv"
        )

        load_csv(
            cursor,
            "transactions",
            [
                "transaction_id",
                "account_id",
                "merchant_id",
                "transaction_date",
                "amount",
                "transaction_type",
                "description",
                "metadata"
            ],
            "transactions.csv"
        )

print("Data load complete.")