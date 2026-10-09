from src.loaders.bronze_loader import BronzeLoader


def main():

    counts = BronzeLoader().run()

    print("\nBronze Load Completed\n")

    for table, count in counts.items():

        print(
            f"{table}: {count}"
        )


if __name__ == "__main__":
    main()