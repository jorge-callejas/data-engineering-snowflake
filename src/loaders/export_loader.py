from pathlib import Path

from src.utils.snowflake_client import SnowflakeClient
from src.utils.slack_client import SlackClient


class ExportLoader:

    EXPORT_SCRIPT = (
        "sql/04_gold/export_gold_to_s3.sql"
    )

    def __init__(self):

        self.snowflake = SnowflakeClient()

    def execute_export(self):

        sql = Path(
            self.EXPORT_SCRIPT
        ).read_text(
            encoding="utf-8"
        )

        self.snowflake.execute_multi_statement(
            sql
        )

    def notify(self):

        SlackClient().send_message(
            "Gold Export To S3 Completed"
        )

    def run(self):

        self.execute_export()

        self.notify()