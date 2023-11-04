from pathlib import Path

from .base_logger import LogLevel


def validate_init(log_level: LogLevel, write: bool, path: Path | None):
    """
    Validates the init parameters.


    :param log_level: The minimal logging priority that should be logged.
    :type log_level: LogLevel
    :param write: Boolean indicating weather logs should be written
        to a file.
    :type write: bool
    :param path: If write is set to true, logger will log to this path.
    :type path: Path | None

    :Example:

    >>> validate_init(LogLevel.DEBUG, true)
    BaseAdapter

    >>> validate_init()
    TypeError("LogLevel needs to be of type LogLevel.")


    :raises TypeError: If the arguments have the wrong type.
    :raises ValueError: If the LogLevel is not valid. Or path is
        None while write is set to true.
    """
    if not isinstance(log_level, LogLevel):
        raise TypeError("LogLevel needs to be of type LogLevel.")

    if not isinstance(write, bool):
        raise TypeError("Write needs to be of type bool.")

    if not isinstance(path, Path | None):
        raise TypeError("Path needs to be of type Path or None.")

    if write and not path:
        raise ValueError("Path can not be empty if write has been set to true.")

    if log_level not in LogLevel:
        raise ValueError("Invalid LogLevel.")


def validate_adapter_init(log_level: LogLevel, write_logfile: bool):
    """
    Validates the adapter init parameters.


    :param log_level: The minimal logging priority that should be logged.
    :type log_level: LogLevel
    :param write_logfile: Boolean indicating weather logs should be written
        to a file.
    :type write_logfile: bool

    :Example:

    >>> validate_init(LogLevel.DEBUG, true)
    BaseAdapter

    >>> validate_init()
    TypeError("LogLevel needs to be of type LogLevel.")


    :raises TypeError: If the arguments have the wrong type.
    :raises ValueError: If the LogLevel is not valid.
    """
    if not isinstance(log_level, LogLevel):
        raise TypeError("LogLevel needs to be of type LogLevel.")

    if not isinstance(write_logfile, bool):
        raise TypeError("Write needs to be of type bool.")

    if log_level not in LogLevel:
        raise ValueError("Invalid LogLevel.")
