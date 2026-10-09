import boto3
from botocore.exceptions import ClientError

from config.settings import settings
from bootstrap.logger import get_logger

logger = get_logger("aws_setup")


def setup_s3():
    bucket = settings.s3_bucket_name

    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region
    )

    try:
        s3.head_bucket(Bucket=bucket)
        logger.info(f"Bucket already exists: {bucket}")
    except ClientError:
        logger.info(f"Creating bucket: {bucket}")
        
        # En regiones distintas a us-east-1, AWS requiere el LocationConstraint
        if settings.aws_region == "us-east-1":
            s3.create_bucket(Bucket=bucket)
        else:
            s3.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={
                    'LocationConstraint': settings.aws_region
                }
            )
            
        logger.info(f"Bucket created successfully: {bucket}")

    folders = [
        "raw/meetup/initial/",
        "raw/meetup/incremental/",
        "exports/gold/",
        "control/"
    ]

    for folder in folders:
        s3.put_object(
            Bucket=bucket,
            Key=folder
        )
        logger.info(f"Folder created: {folder}")

    # Crear el marcador inicial
    s3.put_object(
        Bucket=bucket,
        Key=settings.s3_initial_marker,
        Body=b"INITIAL_LOAD_SUCCESSFUL"
    )
    logger.info(f"Marker created: {settings.s3_initial_marker}")