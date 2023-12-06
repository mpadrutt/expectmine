# Sirius Fingerprint
**Processes:** {bdg-primary}`.mgf`

**Returns:** {bdg-info}`CSI:FingerID (.tsv)`

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

## Data processing
```{note}
*All step descriptions are directly copied from the SIRIUS CLI `--help` command*
```
This step imports all provided `.mgf` files. It then does the following 
steps:
1. Compound Tool: Identify molecular formulas for each compound individually 
   using fragmentation trees and isotope patterns.
2. Compound Tool: Predict molecular fingerprints from MS/MS and 
   fragmentation trees for each compound individually using CSI: FingerID 
   fingerprint prediction.
3. Compound Tool: Search in molecular structure db for each compound 
   individually using CSI: FingerID structure database search.
4. Write summary files from a given project space into the given project 
   space or a custom location.


## Default paths
The default mzmine3_path is depending on the operating system you use:
- Windows: -
- Mac: /Applications/sirius.app/Contents/MacOS/sirius
- Linux: /home/{username}/sirius/bin/sirius

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
