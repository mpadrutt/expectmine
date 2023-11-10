# Pipeline Module

## Function
The pipeline serves as the core element of the library. It creates a simple 
interface to add input, steps and config to run a specific set of tasks.

## Example
```python
from pathlib import Path

from src.pipeline.pipeline import Pipeline
from src.pipeline.utils import get_quickstart_config
from src.steps.steps import SiriusFingerprint
from src.steps.steps.mzmine3.mzmine3 import MZmine3

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

## Further reading
```{toctree}
---
maxdepth: 1
---
../../modules/pipeline/pipeline
../../modules/pipeline/utils
```