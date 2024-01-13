# Store Module

## Functionality
The store serves as a temporary or persistent storage interface to each step.
This helps to abstract away the runtime environment or the mode the pipeline 
is executed in. To achieve that each store module is built like a 
[KV-Database](https://en.wikipedia.org/wiki/Key–value_database).

## Base types
The currently supported datatypes are:
- Boolean
- String
- Integer
- Float
- File (Stored as Blob)
- Object (Pickled and also stored as a blob)

## Current Adapters
Currently, there are two adapters. One which is tasked with persisting data 
and one only saves data temporary.

| Adapter                                                | Functionality                                      | When to use                                                                                                                                                   |
|--------------------------------------------------------|----------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [In Memory Store](../../modules/store/in_memory/index) | Stores files temporarily in local memory.          | Good for volatile storage. Can also be used for persistent storage, if you dont care about persisting data (e.g. running python code and not running the cli) |
| [Sqlite3 Store](../../modules/store/sqlite3/index)     | Uses a local sqlite3 database to store the values. | Good for persisting data. Should be used for the persistent storage in the Cli.                                                                               |


## Example
```{note}
The `get_quickstart_config` already configures the storage for a pipeline.
If you want to keep it simple, stick to the config. The following example is 
for a more fine grained setup.
```
Let's assume we want to add Sqlite3 as a persistent store to the pipeline and 
not use the  default config. This requires us to initialize the pipeline 
manually, which  implies that we also need to choose adapters logging.

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
from expectmine.storage.adapters.sqlite3_adapter import Sqlite3StoreAdapter

from expectmine.logger.adapters.cli_logger_adapter import CliLoggerAdapter
from expectmine.logger.base_logger import LogLevel

output_directory = Path("output")
temp_directory = Path("output/temp")
db_directory = Path()

pipeline = Pipeline(
    persistent_adapter=Sqlite3StoreAdapter(db_directory, temp_directory),
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
../../modules/store/base_store
../../modules/store/base_store_adapter
../../modules/store/utils

../../modules/store/in_memory/index
../../modules/store/sqlite3/index
```
