import atexit
import os
import pickle
import sqlite3
from pathlib import Path
from typing import Any, Dict, Optional, Type

from src.storage.base_storage import BaseStore, T
from src.storage.utils import validate_key, validate_storage_init, validate_value


class Sqlite3Store(BaseStore):
    def __init__(
        self,
        step_name: str,
        persistent_path: Path,
        working_directory: Path,
        **kwargs: Dict[Any, Any],
    ):
        validate_storage_init(step_name, persistent_path, working_directory)

        self.step_name = step_name
        self.persistent_path = persistent_path
        self.working_directory = working_directory
        self.kwargs = kwargs

        os.makedirs(persistent_path, exist_ok=True)
        self.conn = sqlite3.connect(persistent_path / "sqlite.db", isolation_level=None)

        self._setup()
        atexit.register(self._cleanup)

    def put(self, key: str, value: object | Path):
        validate_key(key)
        validate_value(value)

        cur = self.conn.cursor()

        match value:
            case bool():
                value_type = "boolean"
            case str():
                value_type = "string"
            case int():
                value_type = "int"
            case float():
                value_type = "float"
            case Path():
                value_type = "file"
            case _:
                value_type = "blob"

        cur.execute(
            """
            INSERT OR REPLACE INTO kv_table
            (stepid, key, type, boolean_value, string_value, int_value, float_value, blob_value)
            SELECT step.id, ?, ?, ?, ?, ?, ?, ?
            FROM steps_table step
            WHERE step.name = ?;
            """,
            (
                key,
                value_type,
                value if value_type == "boolean" else None,
                value
                if value_type == "string"
                else (value.suffix if isinstance(value, Path) else None),
                value if value_type == "int" else None,
                value if value_type == "float" else None,
                pickle.dumps(value)
                if value_type == "blob"
                else (value.read_bytes() if isinstance(value, Path) else None),
                self.step_name,
            ),
        )

    def get(self, key: str, returning: Type[T]) -> Optional[T]:
        validate_key(key)

        cur = self.conn.cursor()

        res = cur.execute(
            """
            SELECT type, int_value, float_value, string_value, boolean_value, blob_value
            FROM step_table
            JOIN kv_table ON step_table.id = kv_table.stepid
            WHERE step_table.name = ? AND kv_table.key = ?;
            """,
            (self.step_name, key),
        ).fetchone()

        if res is None:
            return None

        match res[0]:
            case "int":
                return_object = int(res[1])
            case "float":
                return_object = float(res[2])
            case "string":
                return_object = str(res[3])
            case "boolean":
                return_object = bool(res[4])
            case "file":
                return_object = (
                    self.working_directory / f"{self.step_name}-{key}{res[3]}"
                )
                with open(return_object, "wb") as f:
                    f.write(res[5])
            case "blob":
                return_object = pickle.loads(bytes(res[5]))
            case _:
                raise ValueError("Value and return type do not match.")

        if not isinstance(return_object, returning | None):
            print(type(return_object), return_object)
            print(type(returning), returning)
            raise ValueError("Value and return type do not match.")

        return return_object

    def delete(self, key: str):
        validate_key(key)

        cur = self.conn.cursor()

        cur.execute(
            """
            DELETE FROM kv_table
            WHERE key = ? AND stepid IN (SELECT id FROM step_table WHERE name = ?);
            """,
            (key, self.step_name),
        )

    def list(self) -> list[str]:
        cur = self.conn.cursor()

        res = cur.execute(
            """
            SELECT key
            FROM kv_table
            WHERE stepid IN (SELECT id FROM step_table WHERE name = ?);
            """,
            (self.step_name,),
        )

        return [k[0] for k in res]

    def exists(self, key: str) -> bool:
        cur = self.conn.cursor()

        res = cur.execute(
            """
            SELECT 1
            FROM kv_table
            WHERE key = ? AND stepid IN (SELECT id from step_table WHERE name = ?)
            """,
            (key, self.step_name),
        ).fetchone()

        return res is not None

    def _setup(self):
        """
        Sets up the database, creates the necessary tables (if they don't exist)
        and checks that the necessary namespace (given by the step) exists.
        """
        cur = self.conn.cursor()
        cur.executescript(
            """
            BEGIN;
            PRAGMA foreign_keys = ON;
            CREATE TABLE IF NOT EXISTS step_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            );
            CREATE TABLE IF NOT EXISTS kv_table (
                stepid INTEGER,
                key TEXT NOT NULL,
                type TEXT NOT NULL CHECK (type IN ('int', 'float', 'string', 'boolean', 'blob', 'file')),
                int_value INTEGER,
                float_value REAL,
                string_value TEXT,
                boolean_value BOOLEAN,
                blob_value BLOB,
                PRIMARY KEY (stepid, key),
                FOREIGN KEY (stepid) REFERENCES step_table(id)
            );
            COMMIT;
            """
        )

        cur.execute(
            """
            INSERT OR IGNORE INTO step_table(name) VALUES (?);
            """,
            (self.step_name,),
        )

    def _cleanup(self):
        """
        On exit, closes the sqlite3 connection.
        """
        self.conn.close()
