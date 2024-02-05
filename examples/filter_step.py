from pathlib import Path

from expectmine.pipeline.pipeline import Pipeline
from expectmine.pipeline.utils import get_quickstart_config
from expectmine.steps.steps import FilterMgf


pipeline = Pipeline(*get_quickstart_config(output_path=Path("output")))

pipeline.set_input([Path("sirius_output.mgf")])

pipeline.add_step(FilterMgf, {})

pipeline.run()
