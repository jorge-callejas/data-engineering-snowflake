from src.loaders.silver_loader import SilverLoader


def main():

    counts = SilverLoader().run()

    print("\nSilver Load Completed\n")

    for table, count in counts.items():

        print(
            f"{table}: {count}"
        )


if __name__ == "__main__":
    main()