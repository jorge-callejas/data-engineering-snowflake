from pathlib import Path

from src.utils.snowflake_client import SnowflakeClient

client = SnowflakeClient()

sql = Path(
    "sql/01_setup/01_databases_schemas.sql"
).read_text()

for statement in sql.split(";"):

    statement = statement.strip()

    if statement:

        print(
            f"Executing: {statement[:60]}"
        )

        client.execute(statement)

print("Setup executed successfully")

client.close()