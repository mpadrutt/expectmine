from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, TypeVar, Dict, Any

K = TypeVar("K")
T = TypeVar("T")


class BaseIo(ABC):
    @abstractmethod
    def __init__(self, **kwargs: Dict[Any, Any]):
        """
        Creates an instance of the scoped io. Each io instance is
        scoped to an individual step.
        """
        raise NotImplementedError

    @abstractmethod
    def string(
        self, key: str, message: str, validate: Callable[[str], bool] = lambda _: True
    ) -> str:
        """
        Presents the user with a message and returns the inputted string. Can
        also validate the user input. For each key/step combination, the first
        entered value by the user for this question is always returned.

        :param key: Key used to identify the user input.
        :type key: str
        :param message: Message displayed to the user when asked the question.
        :type message: str
        :param validate: Validator which validates the user input.
        :type validate: Callable[[str], bool] | None

        :return: The value entered by the user.
        :rtype: str

        :Example:

        >>> string("hello", "world")
        "User input"

        >>> string("hello", "world", lambda x: True)
        "User input"

        >>> string()
        TypeError("Key and message should be of type string.")

        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If the key is empty.
        """
        raise NotImplementedError

    @abstractmethod
    def number(
        self,
        key: str,
        message: str,
        validate: Callable[[int | float], bool] = lambda _: True,
    ) -> int | float:
        """
        Presents the user with a message and returns the inputted number. Can
        also validate the user input. For each key/step combination, the first
        entered value by the user for this question is always returned.

        :param key: Key used to identify the user input.
        :type key: str
        :param message: Message displayed to the user when asked the question.
        :type message: str
        :param validate: Validator which validates the user input.
        :type validate: Callable[[int | float], bool] | None

        :return: The value entered by the user.
        :rtype: int | float

        :Example:

        >>> number("hello", "world")
        123

        >>> number("hello", "world", lambda x: True)
        123

        >>> number()
        TypeError("Key and message should be of type string.")

        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If the key is empty.
        """
        raise NotImplementedError

    @abstractmethod
    def boolean(self, key: str, message: str) -> bool:
        """
        Presents the user with a message and returns the inputted boolean. Can
        also validate the user input. For each key/step combination, the first
        entered value by the user for this question is always returned.

        :param key: Key used to identify the user input.
        :type key: str
        :param message: Message displayed to the user when asked the question.
        :type message: str

        :return: The value entered by the user.
        :rtype: bool

        :Example:

        >>> boolean("hello", "world")
        True

        >>> boolean()
        TypeError("Key and message should be of type string.")

        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If the key is empty.
        """
        raise NotImplementedError

    @abstractmethod
    def filepath(
        self, key: str, message: str, validate: Callable[[Path], bool] = lambda _: True
    ) -> Path:
        """
        Presents the user with a message and returns the inputted filepath. Can
        also validate the user input. For each key/step combination, the first
        entered value by the user for this question is always returned.

        :param key: Key used to identify the user input.
        :type key: str
        :param message: Message displayed to the user when asked the question.
        :type message: str
        :param validate: Validator which validates the user input.
        :type validate: Callable[[Path], bool] | None

        :return: The value entered by the user.
        :rtype: Path

        :Example:

        >>> filepath("hello", "world")
        Path()

        >>> filepath("hello", "world", lambda x: True)
        Path()

        >>> filepath()
        TypeError("Key and message should be of type string.")

        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If the key is empty.
        """
        raise NotImplementedError

    @abstractmethod
    def filepaths(
        self,
        key: str,
        message: str,
        file_validate: Callable[[Path], bool] = lambda _: True,
        list_validate: Callable[[list[Path] | None], bool] = lambda _: True,
    ) -> list[Path]:
        """
        Presents the user with a message and returns the inputted filepaths. Can
        also validate the user input. For each key/step combination, the first
        entered value by the user for this question is always returned.

        :param key: Key used to identify the user input.
        :type key: str
        :param message: Message displayed to the user when asked the question.
        :type message: str
        :param file_validate: Validator which validates the inputted files.
        :type file_validate: Callable[[Path], bool] | None
        :param list_validate: Validator which validates the inputted list of files.
        :type list_validate: Callable[[list], bool] | None

        :return: The value entered by the user.
        :rtype: list[Path]

        :Example:

        >>> filepaths("hello", "world")
        [Path(), Path()]

        >>> filepaths("hello", "world", lambda x: True)
        [Path(), Path()]

        >>> filepath()
        TypeError("Key and message should be of type string.")

        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If the key is empty.
        """
        raise NotImplementedError

    @abstractmethod
    def single_choice(self, key: str, message: str, options: list[tuple[str, K]]) -> K:
        """
        Presents the user with a message and options and returns the user choice.
        Can also validate the user input. For each key/step combination, the
        first entered value by the user for this question is always returned.

        :param key: Key used to identify the user input.
        :type key: str
        :param message: Message displayed to the user when asked the question.
        :type message: str
        :param options: Options from which the user can choose.
        :type options: list[tuple[str, K]]

        :return: The value chosen by the user.
        :rtype: K

        :Example:

        >>> single_choice("hello", "world", [("choice a", "a"), ("choice b", "b")])
        "a"

        >>> single_choice("A", "B")
        TypeError("Options need to be of type list.")

        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If the key is empty.
        """
        raise NotImplementedError

    @abstractmethod
    def multiple_choice(
        self,
        key: str,
        message: str,
        options: list[tuple[str, T]],
        allow_no_choice: bool = False,
    ) -> list[T] | None:
        """
        Presents the user with a message and options and returns the user choice.
        Can also validate the user input. For each key/step combination, the
        first entered value by the user for this question is always returned.

        :param key: Key used to identify the user input.
        :type key: str
        :param message: Message displayed to the user when asked the question.
        :type message: str
        :param options: Options from which the user can choose.
        :type options: list[tuple[str, K]]
        :param allow_no_choice: Optional argument to allow no selection by the user.
        :type allow_no_choice: bool | None

        :return: The value chosen by the user.
        :rtype: K

        :Example:

        >>> multiple_choice("hello", "world", [("choice a", "a"), ("choice b", "b")])
        ["a"]

        >>> multiple_choice("hello", "world", [("choice a", "a"), ("choice b", "b")], allow_no_choice=True)
        None

        >>> multiple_choice("A", "B")
        TypeError("Options need to be of type list.")

        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If the key is empty.
        """
        raise NotImplementedError

    @abstractmethod
    def all_answers(self) -> dict[str, object]:
        """
        Returns all previous questions together with the given answers.

        :return: All previously answered questions.
        :rtype: dict[str, object]

        :Example:

        >>> export_answers()
        { "foo" : "bar", "hello": 12, "world": True }
        """
        raise NotImplementedError
