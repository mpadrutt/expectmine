from pathlib import Path

from expectmine.io.io.dict_io import DictIo
from expectmine.logger.base_logger import LogLevel
from expectmine.logger.loggers.cli_logger import CliLogger
from expectmine.steps.steps import SiriusFingerprint
from expectmine.storage.stores.in_memory_store import InMemoryStore

from dotenv import load_dotenv

load_dotenv()


path = Path("testdata/sirius")

persistent_storage = InMemoryStore("Sirius", path, path)
volatile_storage = InMemoryStore("Sirius", path, path)
io = DictIo(
    {
        "sirius_path": Path(
            "/Applications/sirius.app/Contents/MacOS/sirius", absolute=True
        ),
        "set_max_mz": False,
        "instrument": "orbitrap",
    }
)

logger = CliLogger(LogLevel.ALL, write_logfile=True, path=path)

step = SiriusFingerprint()
step.install(persistent_storage, io, logger)
step.setup(volatile_storage, io, logger)
step.run(
    [Path("testdata/laudanosine.mgf"), Path("testdata/laudanosine1.mgf")],
    path,
    persistent_storage,
    volatile_storage,
    logger,
)
print(step.metadata(persistent_storage, volatile_storage))
