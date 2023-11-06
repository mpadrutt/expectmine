from pathlib import Path

from src.io.io.dict_io import DictIo
from src.logger.base_logger import LogLevel
from src.logger.loggers.cli_logger import CliLogger
from src.steps.steps import SiriusFingerprint
from src.storage.stores.in_memory_store import InMemoryStore

from dotenv import load_dotenv

load_dotenv()


path = Path("testdata/sirius")

ps = InMemoryStore("Sirius", path, path)
vs = InMemoryStore("Sirius", path, path)
io = DictIo(
    {
        "sirius_path": Path(
            "/Applications/sirius.app/Contents/MacOS/sirius", absolute=True
        ),
        "set_max_mz": False,
        "instrument": "orbitrap",
    }
)
lg = CliLogger(LogLevel.ALL, write_logfile=True, path=path)

step = SiriusFingerprint()
step.install(ps, io, lg)
step.setup(vs, io, lg)
step.run(
    [Path("testdata/laudanosine.mgf"), Path("testdata/laudanosine1.mgf")],
    path,
    ps,
    vs,
    lg,
)
