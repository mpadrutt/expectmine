import shutil
from pathlib import Path

PERSISTENT_PATH = Path("output")
WORKING_DIRECTORY = PERSISTENT_PATH / "temp"


def with_directory(func):
    def wrapper():
        shutil.rmtree(PERSISTENT_PATH, ignore_errors=True)
        func()
        shutil.rmtree(PERSISTENT_PATH, ignore_errors=True)

    return wrapper
