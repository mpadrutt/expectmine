from pathlib import Path
from typing import Any, Callable, Dict

from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from expectmine.io.base_io import BaseIo, K, T
from expectmine.io.utils import parse_number, parse_path


class CliIo(BaseIo):
    """
    CLI based io. Interacts with the user directly from the CLI interface.
    """

    def __init__(self, **kwargs: Dict[Any, Any]):
        self.kwargs = kwargs
        self.answers: dict[str, object] = dict()

    def string(
        self, key: str, message: str, validate: Callable[[str], bool] = lambda _: True
    ) -> str:
        if key in self.answers:
            temp_result = self.answers.get(key)

            if isinstance(temp_result, str) and validate(temp_result):
                return temp_result

        response = inquirer.text(message, validate=validate).execute()  # type: ignore

        self.answers[key] = response
        return response

    def number(
        self,
        key: str,
        message: str,
        validate: Callable[[int | float], bool] = lambda _: True,
    ) -> int | float:
        if key in self.answers:
            temp_result = self.answers.get(key)

            if isinstance(temp_result, int | float) and validate(temp_result):
                return temp_result

        response = inquirer.number(  # type: ignore
            message, float_allowed=True, validate=lambda x: validate(parse_number(x))
        ).execute()

        self.answers[key] = response
        return response

    def boolean(self, key: str, message: str) -> bool:
        if key in self.answers:
            temp_result = self.answers.get(key)

            if isinstance(temp_result, bool):
                return temp_result

        response = inquirer.confirm(message).execute()  # type: ignore

        self.answers[key] = response
        return response

    def filepath(
        self, key: str, message: str, validate: Callable[[Path], bool] = lambda _: True
    ) -> Path:
        if key in self.answers:
            temp_result = self.answers.get(key)

            if isinstance(temp_result, Path) and validate(temp_result):
                return temp_result

        response = inquirer.filepath(  # type: ignore
            message, validate=lambda x: validate(parse_path(x))
        ).execute()
        self.answers[key] = response
        return response

    def filepaths(
        self,
        key: str,
        message: str,
        file_validate: Callable[[Path], bool] = lambda _: True,
        list_validate: Callable[[list[Path] | None], bool] = lambda _: True,
    ) -> list[Path]:
        if key in self.answers:
            temp_result: list[Path] = self.answers.get(key)  # type: ignore

            if (
                isinstance(temp_result, list)
                and all(isinstance(x, Path) for x in temp_result)
                and all(file_validate(path) for path in temp_result)
                and list_validate(temp_result)
            ):
                return temp_result

        response: list[Path] = []

        while True:
            base_path = inquirer.filepath(  # type: ignore
                f"{message} (First select base path)",
                validate=lambda x: parse_path(x).is_dir(),
                only_directories=True,
            ).execute()

            response = inquirer.checkbox(  # type: ignore
                f"{message} (Now select the desired files)",
                choices=[
                    Choice(name=file.name, value=file)
                    for file in Path(base_path).iterdir()
                    if file.is_file() and file_validate(file)
                ],
            ).execute()

            if list_validate(response):
                break

            print("Choice of files not valid.")

        self.answers[key] = response
        return response

    def single_choice(self, key: str, message: str, options: list[tuple[str, K]]) -> K:
        if key in self.answers:
            temp_result = self.answers.get(key)

            for option in options:
                if temp_result == option[1]:
                    return temp_result  # type: ignore

        response = inquirer.select(  # type: ignore
            message,
            [Choice(option[1], option[0]) for option in options],
        ).execute()

        self.answers[key] = response
        return response

    def multiple_choice(
        self,
        key: str,
        message: str,
        options: list[tuple[str, T]],
        allow_no_choice: bool = False,
    ) -> list[T] | None:
        if key in self.answers:
            temp_result = self.answers.get(key)

            for option in options:
                if temp_result == option[1]:
                    return temp_result  # type: ignore

            if temp_result is None:
                return None

        response: list[T] = []

        while True:
            response = inquirer.checkbox(  # type: ignore
                f"{message} (Use space to select values)",
                [Choice(option[1], option[0]) for option in options],
            ).execute()

            if allow_no_choice:
                break
            if not allow_no_choice and len(response) > 0:
                break

            print("Select at least one file.")

    def all_answers(self) -> dict[str, object]:
        return self.answers
