from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List

from src.storage.base_storage import BaseStore


class BaseStoreAdapter(ABC):
    @abstractmethod
    def __init__(
        self, persistent_path: Path, working_directory: Path, **kwargs: Dict[Any, Any]
    ):
        """
        Creates a factory for producing scoped storages.


        :param persistent_path: The path which the storage can use to persist
            data.
        :type persistent_path: Path
        :param working_directory: The path which the storage can use to create
            temporary files in for the user or pipeline to access.
        :type working_directory: Path

        :Example:

        >>> BaseAdapter(Path("path1"), Path("path2"))
        BaseAdapter

        >>> BaseAdapter(Path("path2"))
        ValueError("Storage paths can not be empty.")


        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If either step name or any of the
            paths are empty.
        """
        raise NotImplementedError

    @abstractmethod
    def get_instance(
        self, step_name: str, *args: List[Any], **kwargs: Dict[Any, Any]
    ) -> BaseStore:
        """
        Produces a scoped instance of type BaseStorage.


        :param step_name: The scope of the instance
        :type step_name: str

        :return: A scoped instance of a store.
        :rtype: BaseStore

        :Example:

        >>> get_instance("Instance 1")
        BaseStore

        >>> get_instance("")
        ValueError("Step name can not be empty.")


        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If step name is too long or empty.
        """
        raise NotImplementedError
