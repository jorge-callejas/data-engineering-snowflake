import os

from kaggle.api.kaggle_api_extended import KaggleApi

from config.settings import settings


def main():

    os.environ["KAGGLE_USERNAME"] = (
        settings.kaggle_username
    )

    os.environ["KAGGLE_KEY"] = (
        settings.kaggle_key
    )

    api = KaggleApi()

    api.authenticate()

    print(
        "Kaggle authentication successful"
    )

    datasets = api.dataset_list(
        search="meetup"
    )

    print(
        f"Datasets encontrados: {len(datasets)}"
    )

    for dataset in datasets[:5]:

        print(dataset.ref)


if __name__ == "__main__":
    main()