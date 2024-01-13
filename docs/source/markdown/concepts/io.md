# IO Module

## Functionality
The IO module serves as a communication layer between the user and the 
pipeline. It standardizes the input through a base class which makes the 
reasoning about input easier when implementing steps.

## Current Adapters
Currently, there are two adapters available. Cli and Dict input.

| Adapter                                  | Functionality                                        |
|------------------------------------------|------------------------------------------------------|
| [DictIo](../../modules/io/dict_io/index) | Configures the step from a provided dict.            |
| [CliIo](../../modules/io/cli_io/index)   | Configures the step using user input in the console. |

## Example
Let's assume we want to add a step to the pipeline and configure it through 
inputs in the CLI.
```python
from pathlib import Path

from expectmine.io.io.cli_io import CliIo
from expectmine.pipeline.pipeline import Pipeline
from expectmine.pipeline.utils import get_quickstart_config

from expectmine.steps.steps import MZmine3

pipeline = Pipeline(*get_quickstart_config(output_path=Path("output/")))

pipeline.set_input([Path("File1.mzML")])

"""
Here we add the CliIo instance as second argument, the Step is then 
initialized using input from the Cli
"""
pipeline.add_step(MZmine3, CliIo())
```

## Further reading
```{toctree}
---
maxdepth: 1
---
../../modules/io/base_io
../../modules/io/base_io_adapter
../../modules/io/utils

../../modules/io/cli_io/index
../../modules/io/dict_io/index
```
