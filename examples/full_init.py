from pathlib import Path

from expectmine.logger.adapters.cli_logger_adapter import CliLoggerAdapter
from expectmine.logger.base_logger import LogLevel
from expectmine.pipeline.pipeline import Pipeline
from expectmine.storage.adapters.in_memory_adapter import InMemoryStoreAdapter

pipeline = Pipeline(
    persistent_adapter=InMemoryStoreAdapter(Path("output"), Path("output/temp")),
    volatile_adapter=InMemoryStoreAdapter(Path("output"), Path("output/temp")),
    logger_adapter=CliLoggerAdapter(LogLevel.ALL, True),
)
