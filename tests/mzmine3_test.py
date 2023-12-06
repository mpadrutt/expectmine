from pathlib import Path

from src.io.io.dict_io import DictIo
from src.logger.base_logger import LogLevel
from src.logger.loggers.cli_logger import CliLogger
from src.steps.steps.mzmine3.mzmine3 import MZmine3
from src.storage.stores.in_memory_store import InMemoryStore
from .utils import PERSISTENT_PATH, WORKING_DIRECTORY, with_directory


def test_init_mzmine3():
    step = MZmine3()

    assert isinstance(step, MZmine3)


@with_directory
def test_install_mzmine3():
    store = InMemoryStore("Mzmine3", PERSISTENT_PATH, WORKING_DIRECTORY)
    logger = CliLogger(LogLevel.ERROR, write_logfile=False, path=None)

    step = MZmine3()

    step.install(
        store,
        DictIo(
            {
                "mzmine3_path": Path(
                    "/Applications/MZmine.app/Contents/MacOS/MZmine", absolute=True
                ),
            }
        ),
        logger,
    )


@with_directory
def test_setup_mzmine3():
    store = InMemoryStore("Mzmine3", PERSISTENT_PATH, WORKING_DIRECTORY)
    logger = CliLogger(LogLevel.ERROR, write_logfile=False, path=None)

    step = MZmine3()

    step.setup(
        store,
        DictIo(
            {
                "batchfile": Path("../testdata/2.xml"),
            }
        ),
        logger,
    )


def test_metadata_mzmine3():
    store = InMemoryStore("Mzmine3", PERSISTENT_PATH, WORKING_DIRECTORY)
    logger = CliLogger(LogLevel.ERROR, write_logfile=False, path=None)
    io = DictIo(
        {
            "mzmine3_path": Path(
                "/Applications/MZmine.app/Contents/MacOS/MZmine", absolute=True
            ),
            "batchfile": Path("../testdata/2.xml"),
        }
    )

    step = MZmine3()
    step.install(store, io, logger)
    step.setup(store, io, logger)

    assert isinstance(step.metadata(store, store), dict)


def test_disclaimer_mzmine3():
    assert isinstance(MZmine3.citation_and_disclaimer(), str)
