from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path


class LogLevel(Enum):
    """
    LogLevels for the logger. The levels include:
    ALL, DEBUG, INFO, WARN and ERROR.
    Each logger which implements the BaseLogger also needs
    to have these 5 log levels.
    """

    ALL = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARNING"
    ERROR = "ERROR"


class BaseLogger(ABC):
    @abstractmethod
    def __init__(self, log_level: LogLevel, write_logfile: bool, path: Path | None, **kwargs):
        """
        Produces a scoped instance of type BaseLogger.


        :param log_level: The loglevel of the instance
        :type log_level: LogLevel
        :param write_logfile: Boolean indicating weather logs are written to files.
        :type write_logfile: bool
        :param path: Path to the directory where logs are written to.
        :type path: Path | None

        :return: A scoped logger instance.
        :rtype: BaseLogger

        :Example:

        >>> BaseLogger(LogLevel.ERROR, true, Path('foo'))
        BaseLogger

        >>> BaseLogger(LogLevel.ERROR, true)
        ValueError("Path can not be empty if write has been set to true.")

        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If path is empty in case write was set to true. Or
            the path is invalid.
        """
        raise NotImplementedError

    @abstractmethod
    def log(self, message: str | Exception):
        """
        Writes a message to the log.


        :param message: Message to be logged.
        :type message: str | Exception

        :raises TypeError: If the arguments have the wrong type.
        """
        raise NotImplementedError

    @abstractmethod
    def debug(self, message: str | Exception):
        """
        Writes debug info to the log.


        :param message: Message to be logged.
        :type message: str | Exception

        :raises TypeError: If the arguments have the wrong type.
        """
        raise NotImplementedError

    @abstractmethod
    def info(self, message: str | Exception):
        """
        Writes info to the log.


        :param message: Message to be logged.
        :type message: str | Exception

        :raises TypeError: If the arguments have the wrong type.
        """
        raise NotImplementedError

    @abstractmethod
    def warn(self, message: str | Exception):
        """
        Writes a warning to the log.


        :param message: Message to be logged.
        :type message: str | Exception

        :raises TypeError: If the arguments have the wrong type.
        """
        raise NotImplementedError

    @abstractmethod
    def error(self, message: str | Exception):
        """
        Writes an error to the log.


        :param message: Message to be logged.
        :type message: str | Exception

        :raises TypeError: If the arguments have the wrong type.
        """
        raise NotImplementedError
