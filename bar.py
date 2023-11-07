from pathlib import Path

from src.io.io.dict_io import DictIo
from src.pipeline.pipeline import Pipeline
from src.pipeline.utils import get_quickstart_config
from src.steps.steps import SiriusFingerprint, ShrinkMgf
from src.steps.steps.mzmine3.mzmine3 import MZmine3

from dotenv import load_dotenv

load_dotenv()


pipeline = Pipeline(*get_quickstart_config(output_path=Path(f"output")))

pipeline.set_input([Path("testdata/1.mzML"), Path("testdata/2.mzML")])

pipeline.add_step(
    MZmine3,
    DictIo(
        {
            "mzmine3_path": Path(
                "/Applications/MZmine.app/Contents/MacOS/MZmine", absolute=True
            ),
            "batchfile": Path("testdata/2.xml"),
        }
    ),
)

pipeline.add_step(ShrinkMgf, DictIo({"compounds_per_file": 5}))

pipeline.add_step(
    SiriusFingerprint,
    DictIo(
        {
            "sirius_path": Path(
                "/Applications/sirius.app/Contents/MacOS/sirius", absolute=True
            ),
            "set_max_mz": False,
            "instrument": "orbitrap",
        }
    ),
)

pipeline.run()
