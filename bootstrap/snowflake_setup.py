from pathlib import Path

from bootstrap.logger import get_logger
from src.utils.snowflake_client import SnowflakeClient
from config import settings


logger = get_logger("snowflake_setup")


SETUP_FILES = [

    "sql/01_setup/01_databases_schemas.sql",
    "sql/01_setup/02_storage_integration.sql",
    "sql/01_setup/03_stages_file_formats.sql",
    "sql/01_setup/05_control_tables.sql",
    "sql/02_bronze/create_bronze_tables.sql",
    "sql/03_silver/create_silver_tables.sql",
    "sql/03_silver/create_quarentine_tables.sql",
    "sql/04_gold/create_gold_tables.sql"
]


def storage_integration_exists(
    client: SnowflakeClient
) -> bool:

    result = client.execute(
        """
        SHOW STORAGE INTEGRATIONS
        LIKE 'MEETUP_S3_INT'
        """
    )

    return len(result) > 0


def setup_snowflake():

    client = SnowflakeClient()

    for script in SETUP_FILES:

        if (
            script.endswith(
                "02_storage_integration.sql"
            )
            and storage_integration_exists(
                client
            )
        ):

            logger.info(
                "Storage Integration "
                "MEETUP_S3_INT already exists. "
                "Skipping creation."
            )

            continue

        logger.info(
            f"Executing script: {script}"
        )

        sql = Path(
            script
        ).read_text(
            encoding="utf-8"
        )

        sql = sql.format(
            aws_role_arn=settings.aws_role_arn,
            bucket_name=settings.s3_bucket_name
        )

        client.execute_multi_statement(
            sql
        )

        logger.info(
            f"Completed script: {script}"
        )