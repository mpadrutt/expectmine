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
