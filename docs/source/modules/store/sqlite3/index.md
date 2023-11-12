# Sqlite3

Basic sqlite3 database implementation for persisting data. Creates a `.db`
file where it then manages connections and inserts config objects to. Built 
to be a very versatile store that can also be accessed by many other systems.

## Usage
Go create a new `Sqlite3Store` you need to provide the store with two 
arguments:
- `persistent_path`: Used as a base path to find the database or create a 
  new one if it does not exist. *NOTE: This does not point to the database 
  itself, only to the path.*
- `working_directory`: If a file is requested from the store, here is where 
  it will be recreated and then linked to.

```python
from pathlib import Path

from src.storage.stores.sqlite3_store import Sqlite3Store
from src.storage.adapters.sqlite3_adapter import Sqlite3StoreAdapter

database_path = Path("output")
temp_directory = Path("output/temp")

store = Sqlite3Store(database_path, temp_directory)
adapter = Sqlite3StoreAdapter(database_path, temp_directory)
```

## Further Info
```{toctree}
---
maxdepth: 3
---
sqlite3
sqlite3_adapter
```