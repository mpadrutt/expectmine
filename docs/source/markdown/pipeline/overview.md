# Overview

## What is the expectmine-pipeline?
The Expectmine-Pipeline aims to create a simple interface for researchers 
to build processing pipelines for their workflows. It is built with reducing 
the interface overhead from the start which tries to the process of integrating 
new steps or adding library support as easy as possible.

## In action
Creating a pipeline to execute in python directly is super easy, just import 
the `get_quickstart_config` method and initialize a pipeline directly from it.


```python
from pathlib import Path

from expectmine.pipeline.pipeline import Pipeline
from expectmine.pipeline.utils import get_quickstart_config

pipeline = Pipeline(*get_quickstart_config(output_path=Path("pipeline_output")))
```

You can make it more specialized if you want. But the following code snippet 
shows the simplest pipeline in its entirety.

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
