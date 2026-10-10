from pathlib import Path
from datetime import datetime

from src.utils.snowflake_client import SnowflakeClient
from src.utils.slack_client import SlackClient


class GoldLoader:

    SQL_SCRIPTS = [
        "sql/04_gold/load_dim_city.sql",
        "sql/04_gold/load_dim_group.sql",
        "sql/04_gold/load_dim_venue.sql",
        "sql/04_gold/load_dim_date.sql",
        "sql/04_gold/load_fact_events.sql"
    ]

    TABLES = [
        "DIM_CITY",
        "DIM_GROUP",
        "DIM_VENUE",
        "DIM_DATE",
        "FACT_EVENTS"
    ]

    def __init__(self):

        self.snowflake = SnowflakeClient()

        self.pipeline_run_id = (
            datetime.now()
            .strftime("%Y%m%d_%H%M%S")
        )

    def execute_loads(self):

        for script in self.SQL_SCRIPTS:

            print(
                f"[Gold Loader] Ejecutando {script}"
            )

            sql = Path(
                script
            ).read_text(
                encoding="utf-8"
            )

            sql = sql.replace(
                "{pipeline_run_id}",
                self.pipeline_run_id
            )

            self.snowflake.execute_multi_statement(
                sql
            )

    def get_counts(self):

        counts = {}

        for table in self.TABLES:

            result = self.snowflake.execute(
                f"""
                SELECT COUNT(*)
                FROM GOLD.{table}
                """
            )

            counts[table] = result[0][0]

        return counts

    def notify(self, counts):

        message = (
            "Gold Load Completed\n\n"
            f"Pipeline Run Id: "
            f"{self.pipeline_run_id}\n\n"
        )

        for table, count in counts.items():

            message += (
                f"{table}: {count}\n"
            )

        SlackClient().send_message(
            message
        )

    def run(self):

        self.execute_loads()

        counts = self.get_counts()

        self.notify(counts)

        return counts