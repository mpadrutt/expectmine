# Shrink-Mgf
**Processes:** {bdg-primary}`.mgf`

**Returns:** {bdg-info}`.mgf`

This step is mainly for debugging purposes. It reduces the amount of 
compounds in the provided `.mgf` files. This reduces calculation time 
downstream.

## Requirements
*There is no external requirement for this step.*

## Arguments
To step requires the following arguments (if combined with DictIO):
- `compounds_per_file`: Number of compounds per file.

## Data processing
The step reads through all provided files and only returns the first 
`BEGIN IONS` to `END IONS` blocks.

## Usage
::::{tab-set}

:::{tab-item} Using Dict
:sync: key1
```python
from expectmine.steps.steps.shrink_mgf import ShrinkMgf

pipeline.add_step(ShrinkMgf, {"compounds_per_file": 5})
```
:::

:::{tab-item} Using DictIo
:sync: key2

```python
from expectmine.steps.steps.shrink_mgf import ShrinkMgf
from expectmine.io.io.dict_io import DictIo

pipeline.add_step(ShrinkMgf, DictIo({"compounds_per_file": 5}))
```
:::

:::{tab-item} Using CliIo
:sync: key3

```python
from expectmine.steps.steps.shrink_mgf import ShrinkMgf
from expectmine.io.io.cli_io import CliIo

pipeline.add_step(
    ShrinkMgf,
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
shrink_mgf.rst
```
