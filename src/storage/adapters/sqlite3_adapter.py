from pathlib import Path

from ..base_storage import BaseStore
from ..base_storage_adapter import BaseStorageAdapter
from ..stores.sqlite3_store import Sqlite3Store
from ..utils import validate_adapter_init, validate_step_name


class Sqlite3StorageAdapter(BaseStorageAdapter):
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
