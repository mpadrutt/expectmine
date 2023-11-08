from pathlib import Path

from src.pipeline.pipeline import Pipeline
from src.pipeline.utils import get_quickstart_config
from example_step import ExampleStep
from src.steps.steps import SiriusFingerprint, ShrinkMgf
from src.steps.steps.mzmine3.mzmine3 import MZmine3


pipeline = Pipeline(*get_quickstart_config(output_path=Path(f"output")))

pipeline.set_input([Path("testdata/1.mzML"), Path("testdata/2.mzML")])

# We add the new step here, with the value required in "Setup"
pipeline.add_step(ExampleStep, {"message": "Hello world"})

pipeline.run()


# pipeline.add_step(
#     MZmine3,
#     {
#         "mzmine3_path": Path(
#             "/Applications/MZmine.app/Contents/MacOS/MZmine", absolute=True
#         ),
#         "batchfile": Path("testdata/2.xml"),
#     },
# )
#
# pipeline.add_step(ShrinkMgf, {"compounds_per_file": 5})
#
# pipeline.add_step(
#     SiriusFingerprint,
#     {
#         "sirius_path": Path(
#             "/Applications/sirius.app/Contents/MacOS/sirius", absolute=True
#         ),
#         "set_max_mz": False,
#         "instrument": "orbitrap",
#     },
# )
