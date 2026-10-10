from src.extractors.synthetic_generator import (
    SyntheticGenerator
)
from src.loaders.bronze_loader import BronzeLoader
from src.loaders.silver_loader import SilverLoader
from src.loaders.gold_loader import GoldLoader
from src.loaders.export_loader import ExportLoader


def main():

    print(
        "\n=== Generating Synthetic Data ===\n"
    )

    synthetic_result = (
        SyntheticGenerator().run()
    )

    print(
        f"Generated: "
        f"{synthetic_result['records']} records"
    )

    print(
        "\n=== Bronze Load ===\n"
    )

    bronze_counts = (
        BronzeLoader().run()
    )

    print(
        "\n=== Silver Load ===\n"
    )

    silver_counts = (
        SilverLoader().run()
    )

    print(
        "\n=== Gold Load ===\n"
    )

    gold_counts = (
        GoldLoader().run()
    )

    print(
        "\n=== Export Gold To S3 ===\n"
    )

    ExportLoader().run()

    print(
        "\n=== Pipeline Completed Successfully ===\n"
    )

    print(
        "\nBronze Counts\n"
    )

    for table, count in bronze_counts.items():

        print(
            f"{table}: {count}"
        )

    print(
        "\nSilver Counts\n"
    )

    for table, count in silver_counts.items():

        print(
            f"{table}: {count}"
        )

    print(
        "\nGold Counts\n"
    )

    for table, count in gold_counts.items():

        print(
            f"{table}: {count}"
        )


if __name__ == "__main__":
    main()