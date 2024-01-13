import pytest
from expectmine.storage.adapters.in_memory_adapter import InMemoryStoreAdapter
from expectmine.storage.adapters.sqlite3_adapter import Sqlite3StoreAdapter
from expectmine.storage.stores.in_memory_store import InMemoryStore
from expectmine.storage.stores.sqlite3_store import Sqlite3Store

from .utils import PERSISTENT_PATH, WORKING_DIRECTORY, with_directory


@with_directory
def test_initialize_in_memory_adapter():
    adapter = InMemoryStoreAdapter(PERSISTENT_PATH, WORKING_DIRECTORY)
    store = adapter.get_instance("test")

    assert isinstance(adapter, InMemoryStoreAdapter)
    assert isinstance(store, InMemoryStore)


def test_in_memory_adapter_bad_init():
    with pytest.raises(TypeError):
        adapter = InMemoryStoreAdapter()


@with_directory
def test_initialize_sqlite3_adapter():
    adapter = Sqlite3StoreAdapter(PERSISTENT_PATH, WORKING_DIRECTORY)
    store = adapter.get_instance("test")

    assert isinstance(adapter, Sqlite3StoreAdapter)
    assert isinstance(store, Sqlite3Store)


def test_sqlite3_adapter_bad_init():
    with pytest.raises(TypeError):
        adapter = Sqlite3StoreAdapter()
