from src.utils.snowflake_client import SnowflakeClient


def main():

    client = SnowflakeClient()

    result = client.execute(
        """
        SELECT
            CURRENT_ACCOUNT(),
            CURRENT_REGION(),
            CURRENT_WAREHOUSE(),
            CURRENT_TIMESTAMP()
        """
    )

    print(result)

    client.close()


if __name__ == "__main__":
    main()