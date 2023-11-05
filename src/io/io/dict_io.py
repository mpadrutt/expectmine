from pathlib import Path
from typing import Any, Callable, Dict

from src.io.base_io import BaseIo, K, T


class DictIo(BaseIo):
    """
    Simple dict that serves as IO to configure a step directly from config dict.

    :raises ValueError: If the key is not found in the dict, there
        is a type mismatch or validation fails.
    """

    def __init__(self, answers: dict[str, object], **kwargs: Dict[Any, Any]):
        self.answers = answers
        self.kwargs = kwargs

    def string(
        self, key: str, message: str, validate: Callable[[str], bool] = lambda _: True
    ) -> str:
        if key not in self.answers:
            raise ValueError("Key not found.")

        temp_result = self.answers.get(key)

        if not isinstance(temp_result, str):
            raise ValueError("Value is not of type string.")

        if not validate(temp_result):
            raise ValueError("Validation failed for value.")

        return temp_result

    def number(
        self,
        key: str,
        message: str,
        validate: Callable[[int | float], bool] = lambda _: True,
    ) -> int | float:
        if key not in self.answers:
            raise ValueError("Key not found.")

        temp_result = self.answers.get(key)

        if not isinstance(temp_result, int | float):
            raise ValueError("Value is not of type int or float.")

        if not validate(temp_result):
            raise ValueError("Validation failed for value.")

        return temp_result

    def boolean(self, key: str, message: str) -> bool:
        if key not in self.answers:
            raise ValueError("Key not found.")

        temp_result = self.answers.get(key)

        if not isinstance(temp_result, bool):
            raise ValueError("Value is not of type boolean.")

        return temp_result

    def filepath(
        self, key: str, message: str, validate: Callable[[Path], bool] = lambda _: True
    ) -> Path:
        if key not in self.answers:
            raise ValueError("Key not found.")

        temp_result = self.answers.get(key)

        if not isinstance(temp_result, Path):
            raise ValueError("Value is not of type Path.")

        if not validate(temp_result):
            raise ValueError("Validation failed for value.")

        return temp_result

    def filepaths(
        self,
        key: str,
        message: str,
        file_validate: Callable[[Path], bool] = lambda _: True,
        list_validate: Callable[[list[Path] | None], bool] = lambda _: True,
    ) -> list[Path]:
        if key not in self.answers:
            raise ValueError("Key not found.")

        temp_result: list[Path] = self.answers.get(key)  # type: ignore

        if not isinstance(temp_result, list):
            raise ValueError("Value is not of type list.")

        if not all(isinstance(file, Path) for file in temp_result):
            raise ValueError("List elements are not of type Path.")

        if not list_validate(temp_result):
            raise ValueError("Returned list not valid.")

        if all(isinstance(file, Path) and file_validate(file) for file in temp_result):
            raise ValueError("Returned list elements are not valid.")

        return temp_result

    def single_choice(self, key: str, message: str, options: list[tuple[str, K]]) -> K:
        if key not in self.answers:
            raise ValueError("Key not found.")

        temp_result = self.answers.get(key)

        for option in options:
            if temp_result == option[1]:
                return temp_result  # type: ignore

        raise ValueError("Result not found in options.")

    def multiple_choice(
        self,
        key: str,
        message: str,
        options: list[tuple[str, T]],
        allow_no_choice: bool = False,
    ) -> list[T] | None:
        if key not in self.answers:
            raise ValueError("Key not found.")

        temp_result = self.answers.get(key)

        for option in options:
            if temp_result == option[1]:
                return temp_result  # type: ignore

        if temp_result is None and allow_no_choice:
            return None

        raise ValueError("Result not found in options.")

    def all_answers(self) -> dict[str, object]:
        return self.answers
