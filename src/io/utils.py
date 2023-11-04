from pathlib import Path
from typing import TypeVar

K = TypeVar("K")


def validate_arguments(key: str, message: str):
    """
    Validates that the arguments are valid. Throws an error if not.

    :param key: Key used to identify the user input.
    :type key: str
    :param message: Message displayed to the user when asked the question.
    :type message: str

    :Example:

    >>> validate_arguments("hello", "world")


    >>> validate_arguments("")
    ValueError("Key can not be empty")

    :raises TypeError: If the arguments have the wrong type.
    :raises ValueError: If the key is empty.
    """
    if not isinstance(key, str) or not isinstance(message, str):
        raise TypeError("Key and message should be of type string.")

    if len(key) < 1:
        raise ValueError("Key can not be empty.")


def validate_choice(options: list[tuple[str, K]]):
    if not isinstance(options, list):
        raise TypeError("Options need to be of type list.")


def validate_step_name(step_name: str):
    if not isinstance(step_name, str):
        raise TypeError("Step_name should be of type string.")

    if len(step_name) > 255:
        raise ValueError("Step name is too long.")

    if len(step_name) < 1:
        raise ValueError("Step name can not be empty.")


def parse_number(number: str) -> int | float:
    """
    Parses the returned value into an int or float.

    :param number: Number to parses.
    :type number: str

    :Example:

    >>> parse_number("12.3")
    12.3

    >>> parse_number("1")
    1
    """
    try:
        return int(number)
    except ValueError:
        return float(number)


def parse_path(path: str):
    """
    Parses the returned value into a Path object.

    :param path: Number to parses.
    :type path: str

    :Example:

    >>> parse_path("foo.txt")
    Path("foo.txt")
    """
    return Path(path)
