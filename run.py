from pathlib import Path
from typing import Type

from src.io import BaseIo
from src.logger import LogLevel
from src.pipeline import Pipeline

from src.logger.adapters import CliLoggerAdapter
from src.steps import BaseStep
from src.storage.adapters import InMemoryStorageAdapter

from src.steps.steps import Foobar

#
# pipe = Pipeline(
#     persistent_adapter=InMemoryStorageAdapter(Path(), Path("/temp")),
#     volatile_adapter=InMemoryStorageAdapter(Path(), Path("/temp")),
#     logger_adapter=CliLoggerAdapter(LogLevel.INFO, write_logfile=False),
# )

print(issubclass(Foobar(), BaseStep))
# def validate(p: Path) -> bool:
#     return p.suffix == ".md"
#
#
# base_path = inquirer.filepath(
#     f"{message} (First select base path)",
#     only_directories=True,
# ).execute()
#
# response: list[Path] = inquirer.checkbox(
#     f"{message} (Now select the desired files)",
#     choices=[
#         Choice(name=file.name, value=file)
#         for file in Path(base_path).iterdir()
#         if file.is_file() and validate(file)
#     ],
# ).execute()

# print(response)
# s = Sqlite3Store("Hello", Path("config.db"), Path())
# s.put("1", 1)
# s.put("2", 2.2)
# s.put("3", "2.2")
# s.put("4", False)
# s.put("5", [1, 2, 3])
# s.put("6", Path("README.md"))
#
# print(s.get("1", int))
# print(s.get("2", float))
# print(s.get("3", str))
# print(s.get("4", bool))
# print(s.get("5", object))
# print(s.get("6", Path))
