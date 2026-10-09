import boto3

from config.settings import settings 
from src.utils.snowflake_client import SnowflakeClient
from src.utils.slack_client import SlackClient


class BronzeLoader:

    COPY_SCRIPT = "sql/02_bronze/copy_into_bronze.sql"

    TABLES = [
        "CATEGORIES_RAW",
        "CITIES_RAW",
        "TOPICS_RAW",
        "GROUPS_TOPICS_RAW",
        "MEMBERS_TOPICS_RAW",
        "MEMBERS_RAW",
        "VENUES_RAW",
        "GROUPS_RAW",
        "EVENTS_RAW"
    ]

    def __init__(self):

        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key    ,
            region_name=settings.aws_region 
        )

        self.snowflake = SnowflakeClient()

    def validate_initial_load(self):

        self.s3.head_object(
            Bucket=settings.s3_bucket_name ,
            Key=settings.s3_initial_marker
        )

    def execute_copy(self):

        with open(
            self.COPY_SCRIPT,
            "r",
            encoding="utf-8"
        ) as file:

            sql = file.read()

        self.snowflake.execute_multi_statement(
            sql
        )

    def get_counts(self):

        counts = {}

        for table in self.TABLES:

            result = self.snowflake.execute(
                f"""
                SELECT COUNT(*)
                FROM BRONZE.{table}
                """
            )

            counts[table] = result[0][0]

        return counts

    def notify(self, counts):

        message = (
            "Bronze Load Completed\n\n"
        )

        for table, count in counts.items():

            message += (
                f"{table}: {count}\n"
            )

        SlackClient().send_message(
            message
        )

    def run(self):

        self.validate_initial_load()

        self.execute_copy()

        counts = self.get_counts()

        self.notify(counts)

        return counts