import argparse


parser = argparse.ArgumentParser(
    "multiduplex",
)
parser.add_argument("-s", "--server", action="store_true")
parser.add_argument("-c", "--client", action="store_true")

if __name__ == "__main__":
    args = parser.parse_args()

    print("Starting with: ", args)
