import snowflake.connector

from config.settings import settings


class SnowflakeClient:

    def __init__(self):

        self.connection = snowflake.connector.connect(
            account=settings.snowflake_account,
            user=settings.snowflake_user,
            password=settings.snowflake_password,
            role=settings.snowflake_role,
            warehouse=settings.snowflake_warehouse,
            database=settings.snowflake_database,
            schema=settings.snowflake_schema
        )

    def execute(self, query: str):

        with self.connection.cursor() as cursor:

            cursor.execute(query)

            return cursor.fetchall()

    def execute_multi_statement(self, sql: str):

        statements = [
            stmt.strip()
            for stmt in sql.split(";")
            if stmt.strip()
        ]

        for statement in statements:
            self.execute(statement)

    def close(self):

        self.connection.close()