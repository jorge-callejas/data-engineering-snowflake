from src.extractors.kaggle_extractor import (
    run_kaggle_initial_extraction
)


def main():

    print(
        "\nStarting Initial Load...\n"
    )

    run_kaggle_initial_extraction()

    print(
        "\nInitial Load Completed\n"
    )


if __name__ == "__main__":
    main()
