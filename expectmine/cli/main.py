import argparse

from .run_cli import run_cli
from .create import create

parser = argparse.ArgumentParser(
    prog="ProgramName",
    description="What the program does",
    epilog="Text at the bottom of help",
)

parser.add_argument(
    "--create", "-c", action="store_true", help="Call the create step flow."
)


def main():
    args = parser.parse_args()

    if args.create:
        create()

    else:
        run_cli()
