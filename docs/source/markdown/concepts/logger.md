# Logger Module

## Functionality
The Logger module is tasked with creating a uniform `log.log` file for each 
step. The primary goal is to have each step execute as transparent as possible.
Each logfile is scoped to each individual step, so if you look into logfile 
of step A, you will only find information about step A.

## Current Adapters
Currently, there are is one available logging adapter.

| Adapter                                             | Functionality                             |
|-----------------------------------------------------|-------------------------------------------|
| [Cli Logger](../../modules/logger/cli_logger/index) | Logs to the console and writes a logfile. |

## Example
```{note}
The `get_quickstart_config` already configures the Cli Logger for a pipeline.
If you want to keep it simple, stick to the config. The following example is 
for a more fine grained setup.
```
Let's assume we want to add Cli Logger to the pipeline and not use the 
default config. This requires us to initialize the pipeline manually, which 
implies that we also need to choose adapters for storage.

::::{tab-set}

:::{tab-item} Using `get_quickstart_config`
:sync: key1
```python
from pathlib import Path

from expectmine.pipeline.pipeline import Pipeline
from expectmine.pipeline.utils import get_quickstart_config

pipeline = Pipeline(*get_quickstart_config(output_path=Path("output/")))
```
:::

:::{tab-item} Using Adapters
:sync: key2

```python
from pathlib import Path

from expectmine.pipeline.pipeline import Pipeline

from expectmine.storage.adapters.in_memory_adapter import InMemoryStoreAdapter

from expectmine.logger.adapters.cli_logger_adapter import CliLoggerAdapter
from expectmine.logger.base_logger import LogLevel

output_directory = Path("output")
temp_directory = Path("output/temp")

pipeline = Pipeline(
    persistent_adapter=InMemoryStoreAdapter(output_directory, temp_directory),
    volatile_adapter=InMemoryStoreAdapter(output_directory, temp_directory),
    logger_adapter=CliLoggerAdapter(LogLevel.ALL, True),
    output_directory=output_directory
)
```
:::
::::

## Further reading
```{toctree}
---
maxdepth: 1
---
../../modules/logger/base_logger
../../modules/logger/base_logger_adapter
../../modules/logger/utils

../../modules/logger/cli_logger/index
```
