from pathlib import Path

from src.io.io.dict_io import DictIo
from src.io.adapters.dict_io_adapter import DictIoAdapter

io_object = DictIo({"foo": "bar", "answer": 31})
adapter = DictIoAdapter(
    {
        "StepName1": {"foo": "bar", "answer": 31},
        "StepName2": {"hello": "World"},
        "StepName3": {"executable": Path("path.exe")},
    }
)
