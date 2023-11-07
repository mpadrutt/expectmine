import logging
from pathlib import Path

from src.logger.base_logger import BaseLogger, LogLevel
from src.logger.utils import validate_init


class CliLogger(BaseLogger):
    """
    Cli logger which prints messages and optionally logs them to a file.
    """

    def __init__(
        self,
        log_level: LogLevel,
        write_logfile: bool,
        path: Path | None,
    ):
        validate_init(log_level, write_logfile, path)

        self.log_level = log_level.value
        self.write_logfile = write_logfile
        self.path = path

        self.logger = logging.Logger(str(path.absolute()))
        self.logger.setLevel(self.log_level)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        if self.write_logfile and self.path:
            file_handler = logging.FileHandler(
                self.path / "log.log", encoding="utf-8", mode="w"
            )
            file_handler.setLevel(self.log_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def log(self, message: str | Exception):
        self.logger.log(0, message)

    def debug(self, message: str | Exception):
        self.logger.debug(message)

    def info(self, message: str | Exception):
        self.logger.info(message)

    def warn(self, message: str | Exception):
        self.logger.warning(message)

    def error(self, message: str | Exception):
        self.logger.error(message)
