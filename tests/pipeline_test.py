from pathlib import Path

import pytest
from src.logger.adapters.cli_logger_adapter import CliLoggerAdapter
from src.logger.base_logger import LogLevel
from src.pipeline.pipeline import Pipeline
from src.pipeline.utils import get_quickstart_config
from src.storage.adapters.in_memory_adapter import InMemoryStoreAdapter
from src.storage.adapters.sqlite3_adapter import Sqlite3StoreAdapter

from .utils import PERSISTENT_PATH, WORKING_DIRECTORY, with_directory


@with_directory
def test_pipeline_quickstart_config():
    pipeline = Pipeline(*get_quickstart_config(output_path=Path(PERSISTENT_PATH)))
    assert isinstance(pipeline, Pipeline)


@with_directory
def test_pipeline_custom_adapters_1():
    pipeline = Pipeline(
        persistent_adapter=InMemoryStoreAdapter(PERSISTENT_PATH, WORKING_DIRECTORY),
        volatile_adapter=InMemoryStoreAdapter(PERSISTENT_PATH, WORKING_DIRECTORY),
        logger_adapter=CliLoggerAdapter(LogLevel.ALL, True),
        output_directory=PERSISTENT_PATH,
    )
    assert isinstance(pipeline, Pipeline)


@with_directory
def test_pipeline_custom_adapters_2():
    pipeline = Pipeline(
        persistent_adapter=Sqlite3StoreAdapter(PERSISTENT_PATH, WORKING_DIRECTORY),
        volatile_adapter=InMemoryStoreAdapter(PERSISTENT_PATH, WORKING_DIRECTORY),
        logger_adapter=CliLoggerAdapter(LogLevel.ALL, True),
        output_directory=PERSISTENT_PATH,
    )
    assert isinstance(pipeline, Pipeline)


def test_pipeline_no_adapter():
    with pytest.raises(TypeError):
        pipeline = Pipeline()
