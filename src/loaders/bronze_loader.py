import boto3

from config.settings import settings
from src.utils.snowflake_client import SnowflakeClient
from src.utils.slack_client import SlackClient


class BronzeLoader:

    INITIAL_COPY_SCRIPT = (
        "sql/02_bronze/copy_into_bronze.sql"
    )

    INCREMENTAL_COPY_SCRIPT = (
        "sql/02_bronze/copy_incremental_events.sql"
    )

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

    INCREMENTAL_PREFIX = (
        "raw/meetup/incremental/events/"
    )

    def __init__(self):

        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )

        self.snowflake = SnowflakeClient()

    def validate_initial_load(self):

        self.s3.head_object(
            Bucket=settings.s3_bucket_name,
            Key=settings.s3_initial_marker
        )

    def execute_script(
        self,
        script_path: str,
        **kwargs
    ):

        with open(
            script_path,
            "r",
            encoding="utf-8"
        ) as file:

            sql = file.read()

        if kwargs:

            sql = sql.format(
                **kwargs
            )

        self.snowflake.execute_multi_statement(
            sql
        )

    def get_incremental_files(self):

        response = self.s3.list_objects_v2(
            Bucket=settings.s3_bucket_name,
            Prefix=self.INCREMENTAL_PREFIX
        )

        if "Contents" not in response:

            return []

        files = []

        for obj in response["Contents"]:

            key = obj["Key"]

            if key.endswith("/"):
                continue

            files.append(key)

        return files

    def file_already_processed(
        self,
        file_name: str
    ):

        result = self.snowflake.execute(
            f"""
            SELECT COUNT(*)
            FROM CONTROL.PROCESSED_FILES
            WHERE FILE_NAME = '{file_name}'
            """
        )

        return result[0][0] > 0

    def get_pending_incremental_files(self):

        pending_files = []

        files = self.get_incremental_files()

        for file_path in files:

            file_name = file_path.split("/")[-1]

            if not self.file_already_processed(
                file_name
            ):

                pending_files.append(
                    {
                        "file_name": file_name,
                        "file_path": file_path
                    }
                )

        return pending_files

    def register_processed_file(
        self,
        file_name: str,
        file_path: str
    ):

        self.snowflake.execute(
            f"""
            INSERT INTO CONTROL.PROCESSED_FILES
            (
                FILE_NAME,
                FILE_PATH,
                FILE_TYPE
           )
            VALUES
            (
                '{file_name}',
                '{file_path}',
                'EVENTS_INCREMENTAL'
            )
            """
        )

    def execute_initial_load(self):

        print(
            "[Bronze Loader] Running initial load"
        )

        self.execute_script(
            self.INITIAL_COPY_SCRIPT
        )

    def execute_incremental_load(self):

        pending_files = (
            self.get_pending_incremental_files()
        )

        if not pending_files:

            print(
                "[Bronze Loader] No pending incremental files"
            )

            return

        for file in pending_files:

            print(
                f"[Bronze Loader] Processing "
                f"{file['file_name']}"
            )

            self.execute_script(
                self.INCREMENTAL_COPY_SCRIPT,
                incremental_file=file["file_path"]
            )

            self.register_processed_file(
                file_name=file["file_name"],
                file_path=file["file_path"]
            )

    def execute_copy(self):

        self.execute_initial_load()

        self.execute_incremental_load()

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

    def notify(
        self,
        counts
    ):

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

        self.notify(
            counts
        )

        return counts