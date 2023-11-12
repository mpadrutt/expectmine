from pathlib import Path

from src.io.io.dict_io import DictIo
from src.logger.base_logger import LogLevel
from src.logger.loggers.cli_logger import CliLogger
from src.steps.steps.sirius_fingerprint import SiriusFingerprint
from src.storage.stores.in_memory_store import InMemoryStore
from .utils import PERSISTENT_PATH, WORKING_DIRECTORY, with_directory


def test_init_sirius_fingerprint():
    step = SiriusFingerprint()

    assert isinstance(step, SiriusFingerprint)


@with_directory
def test_install_sirius_fingerprint():
    store = InMemoryStore("SiriusFingerprint", PERSISTENT_PATH, WORKING_DIRECTORY)
    logger = CliLogger(LogLevel.ERROR, write_logfile=False, path=None)
    io = DictIo(
        {
            "sirius_path": Path(
                "/Applications/sirius.app/Contents/MacOS/sirius", absolute=True
            ),
            "set_max_mz": False,
            "instrument": "orbitrap",
        }
    )

    step = SiriusFingerprint()

    step.install(
        store,
        io,
        logger,
    )


@with_directory
def test_setup_sirius_fingerprint():
    store = InMemoryStore("SiriusFingerprint", PERSISTENT_PATH, WORKING_DIRECTORY)
    logger = CliLogger(LogLevel.ERROR, write_logfile=False, path=None)
    io = DictIo(
        {
            "sirius_path": Path(
                "/Applications/sirius.app/Contents/MacOS/sirius", absolute=True
            ),
            "set_max_mz": False,
            "instrument": "orbitrap",
        }
    )

    step = SiriusFingerprint()

    step.setup(
        store,
        io,
        logger,
    )


def test_metadata_sirius_fingerprint():
    store = InMemoryStore("SiriusFingerprint", PERSISTENT_PATH, WORKING_DIRECTORY)
    logger = CliLogger(LogLevel.ERROR, write_logfile=False, path=None)
    io = DictIo(
        {
            "sirius_path": Path(
                "/Applications/sirius.app/Contents/MacOS/sirius", absolute=True
            ),
            "set_max_mz": False,
            "instrument": "orbitrap",
        }
    )

    step = SiriusFingerprint()
    step.install(store, io, logger)
    step.setup(store, io, logger)

    assert isinstance(step.metadata(store, store), dict)


def test_disclaimer_sirius_fingerprint():
    assert isinstance(SiriusFingerprint.citation_and_disclaimer(), str)
