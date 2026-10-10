from src.loaders.gold_loader import GoldLoader


def main():

    counts = GoldLoader().run()

    print("\nGold Load Completed\n")

    for table, count in counts.items():

        print(
            f"{table}: {count}"
        )


if __name__ == "__main__":
    main()