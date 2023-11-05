from pathlib import Path
from typing import Optional, Type

from src.storage.base_storage import BaseStore, T
from src.storage import validate_key, validate_storage_init, validate_value


class InMemoryStore(BaseStore):
    """
    Scoped system based store: Each instance of this store is
    associated with a specific namespace. In this context, a namespace
    corresponds to a step, meaning that each step can maintain its
    distinct set of keys. The KV-store is implemented in-memory.
    """

    def __init__(
        self, step_name: str, persistent_path: Path, working_directory: Path, **kwargs
    ):
        validate_storage_init(step_name, persistent_path, working_directory)
        self.step_name = step_name
        self.persistent_path = persistent_path
        self.working_directory = working_directory
        self.storage: dict[str, object] = dict()

    def put(self, key: str, value: object | Path):
        validate_key(key)
        validate_value(value)

        self.storage[key] = value

    def get(self, key: str, returning: Type[T]) -> Optional[T]:
        validate_key(key)

        return_object = self.storage.get(key)

        if not isinstance(return_object, returning | None):
            raise ValueError("Value and return type do not match.")

        return return_object

    def delete(self, key: str):
        validate_key(key)
        self.storage.pop(key, None)

    def list(self) -> list[str]:
        return list(self.storage.keys())

    def exists(self, key: str) -> bool:
        validate_key(key)
        return key in self.storage
