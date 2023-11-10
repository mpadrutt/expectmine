# Dict IO

The DictIo is a wrapper around a basic dict to make a very simple adapter and io class
to quickly configure steps on the run.

## Usage
To create a new DictIo instance, simply provide a dict which contains all keys and
values of the step you want to configure to the constructor.

For the adapter it is a bit more complex, provide a dict containing all step-names as keys,
where the value is a dict containing all key-value pairs of config values you need
to provide to the individual step.

```python
from pathlib import Path

from src.io.io.dict_io import DictIo
from src.io.adapters.dict_io_adapter import DictIoAdapter

io_object = DictIo({"foo": "bar", "answer": 31})
adapter = DictIoAdapter(
    {
        "StepName1": {"foo": "bar", "answer": 31},
        "StepName2": {"hello": "World"},
        "StepName3": {"executable": Path("path.exe")},
    }
)
```   

## Further Info
```{toctree}
---
maxdepth: 3
---
dict_io
dict_io_adapter
```