# Your first pipeline

## Initializing a simple pipeline
Creating a pipeline to execute in python directly is super easy, just import 
the `get_quickstart_config` method and initialize a pipeline directly from it.


```python
from pathlib import Path

from expectmine.pipeline.pipeline import Pipeline
from expectmine.pipeline.utils import get_quickstart_config

pipeline = Pipeline(*get_quickstart_config(output_path=Path("pipeline_output")))
```

## Adding input files
To add input files to the pipeline, just give it an array of paths to the 
individual files. The files you provide will serve as input to the first step.

```python
pipeline.set_input([Path('file1.mzml')])
```

## Adding steps
To add a step, just provide the type of step you want to add and an io 
object, which is used to configure the step.

```python
pipeline.add_step(
    MZmine3,
    {
        "mzmine3_path": Path(
            "/Applications/MZmine.app/Contents/MacOS/MZmine", absolute=True
        ),
        "batchfile": Path("batchfile.xml"),
    }
)
```

## Run the pipeline
After calling run the pipeline will then run and output files for each step 
in the directory you provided as `output_path`.

```python
pipeline.run()
```

## Summary
```python
from pathlib import Path

from expectmine.pipeline.pipeline import Pipeline
from expectmine.pipeline.utils import get_quickstart_config
from expectmine.steps.steps import SiriusFingerprint
from expectmine.steps.steps.mzmine3.mzmine3 import MZmine3

pipeline = Pipeline(*get_quickstart_config(output_path=Path("pipeline_output")))

pipeline.set_input([Path("file1.mzml"), Path("file2.mzml")])

pipeline.add_step(
    MZmine3,
    {
        "mzmine3_path": Path(
            "/Applications/MZmine.app/Contents/MacOS/MZmine", absolute=True
        ),
        "batchfile": Path("batchfile.xml"),
    }
)

pipeline.add_step(
    SiriusFingerprint,
    {
        "sirius_path": Path(
            "/Applications/sirius.app/Contents/MacOS/sirius", absolute=True
        ),
        "set_max_mz": False,
        "instrument": "orbitrap",
    }
)

pipeline.run()
```
