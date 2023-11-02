from pathlib import Path

from src.storage.pipeline_stores import Sqlite3PipelineStore

s = Sqlite3PipelineStore(Path())
s.store_pipeline("Foo", [], [], [Path("foo.py"), Path("pyproject.toml")])
