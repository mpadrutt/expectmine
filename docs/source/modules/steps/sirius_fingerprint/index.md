# Sirius Fingerprint
This step serves as a python interface to the Cli mode of Sirius. The 
general functionality of the step is simple; The step takes a list of .mgf 
files and creates `CSI:FingerID` for all compounds.

## Requirements
To be able to use Sirius Fingerprint you need to have Sirius installed and 
know where the executable is stored. If you are unsure where to find it, take
a look at the [documentation of Sirius](https://boecker-lab.github.io/docs.sirius.github.io/install/).

[Download Sirius](https://bio.informatik.uni-jena.de/software/sirius/)
## Arguments
To step requires the following arguments (if combined with DictIO):
- `sirius_path`: Python `Path` containing the absolute path to the Sirius 
  executable
- `instrument`: Indicate what instrument was used. Possible values are 
  `orbitrap`, `qtof` and `fticr`
- `set_max_mz`: Boolean, indicating weather maxmz should be used. When set 
  to true Only consider compounds with a precursor m/z lower or equal `max_mz`. 
  All other compounds in the input will be skipped.
- (Optional) `max_mz`: If `set_max_mz` is True, this value is considered 
  (and required!). Otherwise, the value is skipped. When set only consider 
  compounds with a precursor m/z lower or equal `max_mz`. All other 
  compounds in the input will be skipped. Default value is `Infinity`

## Usage
::::{tab-set}

:::{tab-item} Using Dict
:sync: key1
```python
from src.steps.steps.sirius_fingerprint import SiriusFingerprint

pipeline.add_step(
    SiriusFingerprint,
    {
        "sirius_path": Path(
            "/Applications/sirius.app/Contents/MacOS/sirius", absolute=True
        ),
        "set_max_mz": False,
        "instrument": "orbitrap",
    },
)
```
:::

:::{tab-item} Using DictIo
:sync: key2

```python
from src.steps.steps.sirius_fingerprint import SiriusFingerprint
from src.io.io.dict_io import DictIo

pipeline.add_step(
    SiriusFingerprint,
    DictIo({
        "sirius_path": Path(
            "/Applications/sirius.app/Contents/MacOS/sirius", absolute=True
        ),
        "set_max_mz": False,
        "instrument": "orbitrap",
    }),
)
```
:::

:::{tab-item} Using CliIo
:sync: key3

```python
from src.steps.steps.sirius_fingerprint import SiriusFingerprint
from src.io.io.cli_io import CliIo

pipeline.add_step(
    SiriusFingerprint,
    CliIo()
)
```
:::
::::

## Further Info
```{toctree}
---
maxdepth: 3
---
sirius_fingerprint.rst
```