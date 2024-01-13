# In Memory

Basic KV-Store abstraction on top of a dictionary. Does not much special, 
but can get a pipeline working very quickly as it does not require much setup.

After the program terminates, the stored data is lost.

## Usage
Go create a new `InMemoryStore` you need to provide the store with two 
arguments:
- `persistent_path`: Mainly used for compatibility issues, you can point it 
  to wherever you want, it has no effect.
- `working_directory`: If a file is requested from the store, here is where 
  it will be recreated and then linked to.

```python
from pathlib import Path

from expectmine.storage.stores.in_memory_store import InMemoryStore
from expectmine.storage.adapters.in_memory_adapter import InMemoryStoreAdapter

output_directory = Path("output")
temp_directory = Path("output/temp")

store = InMemoryStore(output_directory, temp_directory)
adapter = InMemoryStoreAdapter(output_directory, temp_directory)
```
## Further Info
```{toctree}
---
maxdepth: 3
---
in_memory
in_memory_adapter
```
