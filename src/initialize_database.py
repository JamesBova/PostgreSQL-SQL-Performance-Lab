from pathlib import Path
from database import get_connection

sql_file = Path(__file__).parent.parent / "sql" / "01_create_schema.sql"

with open(sql_file, "r") as file:
    sql = file.read()

with get_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute(sql)