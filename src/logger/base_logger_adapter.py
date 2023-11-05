from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict

from .base_logger import BaseLogger, LogLevel


class BaseLoggerAdapter(ABC):
    @abstractmethod
    def __init__(
        self, log_level: LogLevel, write_logfile: bool, **kwargs: Dict[Any, Any]
    ):
        """
        Creates a factory for producing scoped loggers.


        :param log_level: The minimal logging priority that should be logged.
        :type log_level: LogLevel
        :param write_logfile: Boolean indicating weather logs should be written
            to a file.
        :type write_logfile: bool

        :Example:

        >>> BaseLoggingAdapter(LogLevel.DEBUG, true)
        BaseAdapter

        >>> BaseAdapter()
        TypeError("LogLevel needs to be of type LogLevel.")


        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If the LogLevel is not valid.
        """
        raise NotImplementedError

    @abstractmethod
    def get_instance(self, path: Path | None) -> "BaseLogger":
        """
        Produces a scoped instance of type BaseLogger.


        :param path: The scope of the instance
        :type path: Path | None

        :return: A scoped logger instance.
        :rtype: BaseLogger

        :Example:

        >>> get_instance(Path('foo'))
        BaseLogger

        >>> get_instance()
        ValueError("Path can not be empty of write was set to true.")


        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If path is None while write is set to true.
        """
        raise NotImplementedError
