import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    # =====================================================
    # AWS
    # =====================================================

    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")

    aws_secret_access_key = os.getenv(
        "AWS_SECRET_ACCESS_KEY"
    )

    aws_region = os.getenv(
        "AWS_REGION",
        "us-east-1"
    )

    s3_bucket_name = os.getenv(
        "S3_BUCKET_NAME"
    )


    s3_raw_prefix = os.getenv(
        "S3_RAW_PREFIX"
    )

    s3_incremental_prefix = os.getenv(
        "S3_INCREMENTAL_PREFIX"
    )

    s3_export_prefix = os.getenv(
        "S3_EXPORT_PREFIX"
    )

    s3_initial_marker = os.getenv(
        "S3_INITIAL_MARKER"
)
    # =====================================================
    # SNOWFLAKE
    # =====================================================

    snowflake_account = os.getenv(
        "SNOWFLAKE_ACCOUNT"
    )

    snowflake_user = os.getenv(
        "SNOWFLAKE_USER"
    )

    snowflake_password = os.getenv(
        "SNOWFLAKE_PASSWORD"
    )

    snowflake_warehouse = os.getenv(
        "SNOWFLAKE_WAREHOUSE",
        "MEETUP_WH"
    )

    snowflake_database = os.getenv(
        "SNOWFLAKE_DATABASE",
        "MEETUP_DB"
    )

    snowflake_schema = os.getenv(
        "SNOWFLAKE_SCHEMA",
        "BRONZE"
    )

    snowflake_role = os.getenv(
        "SNOWFLAKE_ROLE",
        "ACCOUNTADMIN"
    )

    # =====================================================
    # KAGGLE
    # =====================================================

    kaggle_username = os.getenv(
        "KAGGLE_USERNAME"
    )

    kaggle_key = os.getenv(
        "KAGGLE_KEY"
    )

    kaggle_dataset_handle = os.getenv(
    "KAGGLE_DATASET_HANDLE"
    )

    local_tmp_dir = os.getenv(
        "LOCAL_TMP_DIR",
        "tmp/meetup"
    )

    # =====================================================
    # SLACK
    # =====================================================

    slack_webhook_url = os.getenv(
        "SLACK_WEBHOOK_URL"
    )

    aws_role_arn = os.getenv(
        "AWS_ROLE_ARN"
    )

settings = Settings()