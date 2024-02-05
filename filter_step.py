from pathlib import Path

from expectmine.pipeline.pipeline import Pipeline
from expectmine.pipeline.utils import get_quickstart_config
from expectmine.steps.steps import FilterMgf


pipeline = Pipeline(*get_quickstart_config(output_path=Path("output")))

pipeline.set_input([Path("./examples/sirius_output.mgf")])

pipeline.add_step(
    FilterMgf,
    {
        "discard_pepmass": False,
        "discard_filepath": None,
        "error": 5,
        "should_stop": True,
        "filter_missing_ms": True,
        "should_filter_filename": False,
        "filter_filename": None,
    },
)


pipeline.run()
