from pathlib import Path

from src.storage import BaseStore
from src.storage import BaseStoreAdapter
from src.storage.stores import Sqlite3Store
from src.storage import validate_adapter_init, validate_step_name


class Sqlite3StoreAdapter(BaseStoreAdapter):
    """
    Pipeline storage adapter for Sqlite3Storage.
    """

    def __init__(self, persistent_path: Path, working_directory: Path, **kwargs):
        validate_adapter_init(persistent_path, working_directory)
        self.persistent_path = persistent_path
        self.working_directory = working_directory
        self.kwargs = kwargs

    def get_instance(self, step_name: str, *args, **kwargs) -> BaseStore:
        validate_step_name(step_name)
        return Sqlite3Store(
            step_name, self.persistent_path, self.working_directory, **self.kwargs
        )
