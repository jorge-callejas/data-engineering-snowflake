from pathlib import Path
from datetime import datetime

from src.utils.snowflake_client import SnowflakeClient
from src.utils.slack_client import SlackClient


class SilverLoader:

    SQL_SCRIPTS = [
        "sql/03_silver/load_categories.sql",
        "sql/03_silver/load_cities.sql",
        "sql/03_silver/load_topics.sql",
        "sql/03_silver/load_groups_topics.sql",
        "sql/03_silver/load_members_topics.sql",
        "sql/03_silver/load_members.sql",
        "sql/03_silver/load_venues.sql",
        "sql/03_silver/load_groups.sql",
        "sql/03_silver/load_events.sql"
    ]

    TABLES = [
        "CATEGORIES_SILVER",
        "CITIES_SILVER",
        "TOPICS_SILVER",
        "GROUPS_TOPICS_SILVER",
        "MEMBERS_TOPICS_SILVER",
        "MEMBERS_SILVER",
        "VENUES_SILVER",
        "GROUPS_SILVER",
        "EVENTS_SILVER"
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
                f"[Silver Loader] Ejecutando {script}"
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
                FROM SILVER.{table}
                """
            )

            counts[table] = result[0][0]

        return counts

    def notify(self, counts):

        message = (
            "Silver Load Completed\n\n"
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