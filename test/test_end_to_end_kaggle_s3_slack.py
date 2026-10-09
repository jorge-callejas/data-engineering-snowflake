import os

from pathlib import Path

import boto3

from kaggle.api.kaggle_api_extended import KaggleApi

from config.settings import settings

from src.utils.slack_client import SlackClient


DATASET = "megelon/meetup"

LOCAL_PATH = "tmp/kaggle"

FILE_NAME = "categories.csv"


def download_from_kaggle():

    print("Downloading from Kaggle...")

    os.environ["KAGGLE_USERNAME"] = (
        settings.kaggle_username
    )

    os.environ["KAGGLE_KEY"] = (
        settings.kaggle_key
    )

    Path(LOCAL_PATH).mkdir(
        parents=True,
        exist_ok=True
    )

    api = KaggleApi()

    api.authenticate()

    api.dataset_download_files(
        DATASET,
        path=LOCAL_PATH,
        unzip=True
    )

    print("Download successful")


def upload_to_s3():

    print("Uploading to S3...")

    local_file = (
        f"{LOCAL_PATH}/{FILE_NAME}"
    )

    s3_key = (
        f"raw/meetup/initial/{FILE_NAME}"
    )

    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region
    )

    s3.upload_file(
        local_file,
        settings.s3_bucket_name,
        s3_key
    )

    print("Upload successful")

    return s3_key


def send_slack_notification(s3_key):

    slack = SlackClient()

    message = f"""
Meetup Smoke Test Successful

Dataset: {DATASET}

File Downloaded:
{FILE_NAME}

Bucket:
{settings.s3_bucket_name}

S3 Key:
{s3_key}

Environment:
DEV
"""

    slack.send_message(message)

    print("Slack notification sent")


def main():

    download_from_kaggle()

    s3_key = upload_to_s3()

    send_slack_notification(
        s3_key
    )

    print(
        "\nEnd-to-End test completed successfully"
    )


if __name__ == "__main__":

    main()