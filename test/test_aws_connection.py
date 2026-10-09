import boto3

from config import settings

settings = settings   


def test_connection():

    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region
    )

    response = s3.list_buckets()

    print("\nConnection successful\n")

    for bucket in response["Buckets"]:
        print(bucket["Name"])


if __name__ == "__main__":
    test_connection()