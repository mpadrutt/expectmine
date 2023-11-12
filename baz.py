# from pathlib import Path
#
# from src.io.io.dict_io import DictIo
# from src.io.adapters.dict_io_adapter import DictIoAdapter
#
# io_object = DictIo({"foo": "bar", "answer": 31})
# adapter = DictIoAdapter(
#     {
#         "StepName1": {"foo": "bar", "answer": 31},
#         "StepName2": {"hello": "World"},
#         "StepName3": {"executable": Path("path.exe")},
#     }
# )
from pathlib import Path

from src.logger.adapters.cli_logger_adapter import CliLoggerAdapter
from src.logger.base_logger import LogLevel
from src.pipeline.pipeline import Pipeline
from src.storage.adapters.in_memory_adapter import InMemoryStoreAdapter

pipeline = Pipeline(
    persistent_adapter=InMemoryStoreAdapter(Path("output"), Path("output/temp")),
    volatile_adapter=InMemoryStoreAdapter(Path("output"), Path("output/temp")),
    logger_adapter=CliLoggerAdapter(LogLevel.ALL, True),
)
