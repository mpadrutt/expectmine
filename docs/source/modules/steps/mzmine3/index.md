# MZmine3
This step serves as a python interface to the batch process of the MZmine3 CLI.
The general functionality of the step is simple; The step takes a batchfile (XML)
adds the input of the previous step of the pipeline, applies the batchfile to it and
exports the data as .mgf for Sirius to use.

## Requirements
To be able to use MZmine3 you need to have MZmine3 installed and know where the
executable is stored. If you are unsure where to find it, take a look at the
[documentation of MZmine3](https://mzmine.github.io/mzmine_documentation/commandline_tool.html>).

## Arguments
To step requires the following arguments (if combined with DictIO):
- `mzmine3_path`

## Usage
To create a new CliIo instance, simply import the Class and create an instance.
Same holds true for the CliIoAdapter.

```python
from src.io.io.cli_io import CliIo
from src.io.adapters.cli_io_adapter import CliIoAdapter

io_object = CliIo()
adapter = CliIoAdapter()
```

## Known Issues

## Further Info
```{toctree}
---
maxdepth: 3
---
../../../modules/steps/mzmine3
```