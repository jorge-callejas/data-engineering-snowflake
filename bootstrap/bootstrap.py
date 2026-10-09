from bootstrap.aws_setup import setup_s3
from bootstrap.snowflake_setup import setup_snowflake
from bootstrap.logger import get_logger

logger = get_logger("bootstrap")


def main():

    try:

        logger.info("Starting infrastructure provisioning")

        logger.info("Provisioning AWS resources")
        setup_s3()

        logger.info("Provisioning Snowflake resources")
        setup_snowflake()

        logger.info("Infrastructure provisioning completed")

    except Exception as ex:

        logger.exception(
            f"Infrastructure provisioning failed: {ex}"
        )

        raise


if __name__ == "__main__":
    main()