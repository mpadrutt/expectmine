from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional, Type, TypeVar

T = TypeVar("T", bound=object)


class BaseStore(ABC):
    @abstractmethod
    def __init__(
        self,
        step_name: str,
        persistent_path: Path,
        working_directory: Path,
        **kwargs: Dict[Any, Any]
    ):
        """
        Creates an instance of the scoped storage. Each storage instance is
        scoped to an individual step.

        :param step_name: Step name to which the storage should be scoped
        :type step_name: str
        :param persistent_path: The path which the storage can use to persist
            data.
        :type persistent_path: Path
        :param working_directory: The path which the storage can use to create
            temporary files in for the user or pipeline to access.
        :type working_directory: Path

        :Example:

        >>> BaseStore("hello", Path("path1"), Path("path2"))
        BaseStore

        >>> BaseStore("", Path("path1"), Path("path2"))
        ValueError("Step name can not be empty.")


        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If either step name or any of the
            paths are empty.
        """
        raise NotImplementedError

    @abstractmethod
    def put(self, key: str, value: object | Path) -> None:
        """
        Inserts the key value pair into the store. If it does already exist,
        the previous value is overwritten, when the new value is inserted.
        The put method can handle both objects and filepaths.

        :param key: The key to associate with the value. A key cannot be
            empty. Keys have a maximum length of 255 characters.
        :type key: str
        :param value: The value (object or file) to store. The maximum size
            of an object is 25 MiB. The object needs to be Pickled. In case
            of a filepath the maximum size of the file is 100MiB.
        :type value: object | Path

        :Example:

        >>> put("hello", "World")

        >>> put("file", Path("hello.txt"))

        >>> put("", "World")
        ValueError("Key can not be empty")


        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If either the key is empty or too long, the
            value is not pickleable or too big.
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, key: str, returning: Type[T]) -> Optional[T]:
        """
        Returns the value for a given key. If the key is not found it
        returns None instead. In case of a file, a path to the file
        is returned instead.

        :param key: The key to associate with the value. A key cannot be
            empty. Keys have a maximum length of 255 characters.
        :type key: str
        :param returning: The type of the returned object.
        :type returning: T

        :return: The object of the given key, None if the key does not exist.
        :rtype: T | None

        :Example:

        >>> get("hello", string)
        "World"

        >>> get("list", list[int | str])
        [1,2, "Hello"]

        >>> get("file", Path)
        Path("hello.txt")

        >>> get("unknown_key", dict)
        None

        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If there is a type mismatch between returning
            and the returned value, or if the key is empty or too long.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str) -> None:
        """
        Deletes the value associated to the given key.

        :param key: The key to associate with the value. A key cannot be
            empty. Keys have a maximum length of 255 characters.
        :type key: str

        :Example:

        >>> delete("hello")
        True

        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If the key is empty or too long.
        """
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[str]:
        """
        Returns a list with all the keys that live the given keyspace.

        :return: A list of all keys.
        :rtype: list[str]

        :Example:

        >>> list()
        []

        >>> list()
        ["hello", "world"]
        """
        raise NotImplementedError

    @abstractmethod
    def exists(self, key: str) -> bool:
        """
        Returns a boolean indicating if a given key exists.

        :param key: The key to associate with the value. A key cannot be
            empty. Keys have a maximum length of 255 characters.
        :type key: str

        :return: A boolean indicating if the key exists.
        :rtype: bool

        :Example:

        >>> exists("hello")
        True

        >>> exists("unknown_key")
        False

        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If the key is empty or too long.
        """
        raise NotImplementedError
