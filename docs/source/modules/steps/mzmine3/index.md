# MZmine3
This step serves as a python interface to the batch process of the MZmine3 CLI.
The general functionality of the step is simple; The step takes a batchfile (XML)
adds the input of the previous step of the pipeline, applies the batchfile to it and
exports the data as .mgf for Sirius to use.

## Requirements
To be able to use MZmine3 you need to have MZmine3 installed and know where the
executable is stored. If you are unsure where to find it, take a look at the
[documentation of MZmine3](https://mzmine.github.io/mzmine_documentation/commandline_tool.html).

[Download MZmine3](http://mzmine.github.io/download.html)

```{note}
If you dont include input or output steps in your batchfile, default steps are
atomatically added to your batchfile.
```
To find out how you can create a batchfile, check out the following link:
[Batch mode](https://mzmine.github.io/mzmine_documentation/workflows/batch_processing/batch-processing.html)

## Arguments
To step requires the following arguments (if combined with DictIO):
- `mzmine3_path`: Python `Path` containing the absolute path to the MZmine3 
  executable
- `batchfile`: Python `Path` containing the path to the batchfile which 
  should be used.
- (Optional) `spectral_library_files`: Python list of `Path` If spectral 
  library files where included in the batchfile, provide paths to the files
  used.

## Usage

::::{tab-set}

:::{tab-item} Using Dict
:sync: key1
```python
from src.steps.steps.mzmine3.mzmine3 import MZmine3

pipeline.add_step(
    MZmine3,
    {
        "mzmine3_path": Path(
            "/Applications/MZmine.app/Contents/MacOS/MZmine", absolute=True
        ),
        "batchfile": Path("testdata/2.xml"),
    },
)
```
:::

:::{tab-item} Using DictIo
:sync: key2

```python
from src.steps.steps.mzmine3.mzmine3 import MZmine3
from src.io.io.dict_io import DictIo

pipeline.add_step(
    MZmine3,
    DictIo({
        "mzmine3_path": Path(
            "/Applications/MZmine.app/Contents/MacOS/MZmine", absolute=True
        ),
        "batchfile": Path("testdata/2.xml"),
    }),
)
```
:::

:::{tab-item} Using CliIo
:sync: key3

```python
from src.steps.steps.mzmine3.mzmine3 import MZmine3
from src.io.io.cli_io import CliIo

pipeline.add_step(
    MZmine3,
    CliIo()
)
```
:::
::::


## Known Issues
- When using `peak finder (multithreaded)` the export to sirius module can 
break. It is therefore recommended using the regular peak finder.
- Using any other output step other than `Export for SIRIUS` can break the 
  sirius export.

## Further Info
```{toctree}
---
maxdepth: 3
---
mzmine3.rst
```