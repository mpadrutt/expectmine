from abc import ABC, abstractmethod
from typing import Any, Dict

from .base_io import BaseIo


class BaseIoAdapter(ABC):
    @abstractmethod
    def __init__(self, **kwargs: Dict[Any, Any]):
        """
        Creates a factory for producing scoped io.
        """
        raise NotImplementedError

    @abstractmethod
    def get_instance(self, step_name: str, **kwargs: Dict[Any, Any]) -> "BaseIo":
        """
        Produces a scoped instance of type BaseIo.


        :param step_name: The scope of the instance
        :type step_name: str

        :return: A scoped instance of io.
        :rtype: BaseIo

        :Example:

        >>> get_instance("Instance 1")
        BaseStore

        >>> get_instance("")
        ValueError("Step name can not be empty.")


        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If step name is too long or empty.
        """
        raise NotImplementedError
