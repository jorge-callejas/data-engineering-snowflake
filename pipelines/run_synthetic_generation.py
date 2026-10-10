from src.extractors.synthetic_generator import (
    SyntheticGenerator
)


def main():

    result = SyntheticGenerator().run()

    print("\nSynthetic Generation Completed\n")

    print(
        f"Records Generated: "
        f"{result['records']}"
    )

    print(
        f"S3 Key: "
        f"{result['s3_key']}"
    )


if __name__ == "__main__":
    main()