import boto3

from botocore.exceptions import ClientError

from config.settings import settings


bucket_name = settings.s3_bucket_name

s3 = boto3.client(
    "s3",
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.aws_region
)

try:

    s3.head_bucket(
        Bucket=bucket_name
    )

    print(
        f"Bucket already exists: {bucket_name}"
    )

except ClientError:

    print(
        f"Creating bucket: {bucket_name}"
    )

    if settings.aws_region == "us-east-1":

        s3.create_bucket(
            Bucket=bucket_name
        )

    else:

        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                "LocationConstraint":
                    settings.aws_region
            }
        )

    print("Bucket created successfully")