import os

from pathlib import Path

from kaggle.api.kaggle_api_extended import KaggleApi

from config.settings import settings


def main():

    os.environ["KAGGLE_USERNAME"] = settings.kaggle_username
    os.environ["KAGGLE_KEY"] = settings.kaggle_key

    download_path = "tmp/kaggle"

    Path(download_path).mkdir(
        parents=True,
        exist_ok=True
    )

    api = KaggleApi()

    api.authenticate()

    api.dataset_download_files(
        "megelon/meetup",
        path=download_path,
        unzip=True
    )

    print("Download completed")


if __name__ == "__main__":
    main()
