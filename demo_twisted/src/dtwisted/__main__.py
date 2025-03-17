import argparse


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("echo-server", action="store_true", default=False)

    args = parser.parse_args()


if __name__ == "__main__":
    main()
