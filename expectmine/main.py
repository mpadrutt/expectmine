import argparse

parser = argparse.ArgumentParser(
    prog="ProgramName",
    description="What the program does",
    epilog="Text at the bottom of help",
)

parser.add_argument("--create", action="store_true", help="Call the create step flow.")


def main():
    args = parser.parse_args()

    if args.create:
        print("Create")
        return

    print("Normal")
