import logging
import pickle
from abc import ABC, abstractmethod
from logging import Logger
from pathlib import Path

from pipeline import BaseIo, PersistentStorage, VolatileStorage


class BaseStep(ABC):
    name: str = "BaseStep"

    @classmethod
    def load_instance(cls, filepath: Path):
        with open(filepath, "rb") as file:
            return pickle.load(file)

    @classmethod
    @abstractmethod
    def can_run(cls, input_files: list[str]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def output_filetypes(self, input_files: list[str]) -> list[str]:
        raise NotImplementedError

    def __init__(self, **kwargs: object):
        self.kwargs = kwargs

    @abstractmethod
    def setup(
        self, persistent_storage_object: PersistentStorage, io_object: BaseIo
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def configure(
        self, volatile_storage_object: VolatileStorage, io_object: BaseIo
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def run(
        self,
        input_files: list[Path],
        output_path: Path,
        persitant_storage_object: PersistentStorage,
        volatile_storage_object: VolatileStorage,
        logger: Logger,
    ) -> list[Path]:
        raise NotImplementedError

    @abstractmethod
    def metadata(
        self,
        persitant_storage_object: PersistentStorage,
        volatile_storage_object: VolatileStorage,
    ) -> dict[str, object]:
        raise NotImplementedError

    def dump_instance(self, output_path: Path):
        with open(output_path / "dump.pkl", "wb") as file:
            pickle.dump(self, file)

    def get_persistent_storage(self, step_name: str):
        if not hasattr(self, "persistent_storage") or not self.persistent_storage:
            self.persistent_storage = PersistentStorage(step_name)

        return self.persistent_storage

    def get_volatile_storage(self, step_name: str):
        if not hasattr(self, "volatile_storage") or not self.volatile_storage:
            self.volatile_storage = VolatileStorage(step_name)

        return self.volatile_storage

    def get_logger(self, step_name: str):
        if not hasattr(self, "logger") or not self.logger:
            self.logger = logging.getLogger(step_name)

        return self.logger
