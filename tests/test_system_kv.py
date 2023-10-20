from src.storage import SystemKV
from pathlib import Path
import os
import pytest

TEST_DB_PATH = Path("test_system_kv.db")


@pytest.fixture(scope="class", autouse=False)
def hello():
    print("Hello")


def setup(func):
    def wrapper(*args, **kwargs):
        if TEST_DB_PATH.exists():
            os.remove(TEST_DB_PATH)
        result = func(*args, **kwargs)
        if TEST_DB_PATH.exists():
            os.remove(TEST_DB_PATH)
        return result

    return wrapper


@setup
def test_setup():
    a = SystemKV("A", TEST_DB_PATH)
    b = SystemKV("B", TEST_DB_PATH)

    with pytest.raises(ValueError):
        SystemKV("", TEST_DB_PATH)

    with pytest.raises(ValueError):
        SystemKV("A", None)

    assert isinstance(a, SystemKV)
    assert isinstance(b, SystemKV)


@setup
def test_put_primitives():
    a = SystemKV("A", TEST_DB_PATH)
    a.put("int", 1)
    a.put("string", "hello world")
    a.put("float", 1.234)
    a.put("boolean", True)


print("hello world")
