from pathlib import Path

import src.io
import src.logger
import src.steps
import src.storage
import src.pipeline
import src.utils
from src.logger import LogLevel

from src.steps.steps import MZmine3
from src.io.io import DictIo
from src.storage.stores import InMemoryStore
from src.logger.loggers import CliLogger

step = MZmine3()
logger = CliLogger(LogLevel.ALL, True, Path("testdata/output"))
persistent_storage = InMemoryStore(
    "MZmine3", Path("testdata/output"), Path("testdata/output/temp")
)
volatile_storage = InMemoryStore(
    "MZmine3", Path("testdata/output"), Path("testdata/output/temp")
)

step.install(
    persistent_storage,
    DictIo(
        {
            "mzmine3_path": Path(
                "/Applications/MZmine.app/Contents/MacOS/MZmine", absolute=True
            )
        }
    ),
    logger,
)
step.setup(
    volatile_storage,
<<<<<<< HEAD
    DictIo(
        {
            "batchfile": Path("testdata/2.xml"),
            # "spectral_library_files": [Path("foo.bar")],
        }
    ),
    logger,
)
# step.run(
#     [Path("testdata/1.mzML")],
#     Path("testdata/output"),
#     persistent_storage,
#     volatile_storage,
#     logger,
# )

print(step.metadata(persistent_storage, volatile_storage))
=======
    DictIo({"batchfile": Path("testdata/2.xml")}),
    logger,
)
step.run(
    [Path("testdata/1.mzML"), Path("testdata/2.mzML"), Path("testdata/3.mzML")],
    Path("testdata/output"),
    persistent_storage,
    volatile_storage,
    logger,
)
>>>>>>> 4299879 (Upgradinng Mzmine3 step)
