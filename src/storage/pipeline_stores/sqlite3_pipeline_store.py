import atexit
import json
import pickle
import sys
import sqlite3
from pathlib import Path
from typing import Any, Dict, Optional

from src.io import BaseIo
from src.io.io import DictIo
from src.steps import BaseStep
from src.storage import BasePipelineStore
from src.storage.utils import (
    validate_pipeline_store_init,
    validate_pipeline,
    validate_key,
)


class Sqlite3PipelineStore(BasePipelineStore):
    def __init__(self, persistent_path: Path, **kwargs: Dict[Any, Any]):
        validate_pipeline_store_init(persistent_path)

        self.persistent_path = persistent_path
        self.kwargs = kwargs

        self.conn = sqlite3.connect(persistent_path / "sqlite.db", isolation_level=None)

        self._setup()
        atexit.register(self._cleanup)

    def store_pipeline(
        self,
        key: str,
        steps: list[BaseStep],
        io: list[BaseIo],
        input_files: list[Path],
    ) -> None:
        validate_pipeline(key, steps, io, input_files)

        cur = self.conn.cursor()

        cur.execute(
            """
            DELETE FROM pipeline_table WHERE name == ?
            """,
            (key,),
        )
        res = cur.execute(
            """
            INSERT INTO pipeline_table (name, input_filetypes) VALUES (?, ?) RETURNING id
            """,
            (key, json.dumps([file.suffix for file in input_files])),
        )

        pipeline_id = next(res)[0]
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        pickle_version: str = pickle.format_version  # type: ignore

        data = [
            (
                pipeline_id,
                d[0].step_name(),
                index,
                python_version,
                pickle_version if isinstance(pickle_version, str) else "0.0",
                pickle.dumps(d[1].all_answers()),
            )
            for index, d in enumerate(zip(steps, io))
        ]

        cur.executemany(
            """
            INSERT INTO pipeline_step (stepid, step_name, step_number, python_version, pickle_version, blob_value)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            data,
        )

    def list_pipelines(self) -> list[str]:
        cur = self.conn.cursor()

        res = cur.execute(
            """
            SELECT name FROM pipeline_table
            """
        )

        return [k[0] for k in res]

    def load_pipeline(
        self, key: str
    ) -> Optional[tuple[list[tuple[str, BaseIo]], list[str]]]:
        validate_key(key)

        cur = self.conn.cursor()

        res = cur.execute(
            """
            SELECT input_filetypes
            FROM pipeline_table
            WHERE name = ?;
            """,
            (key,),
        )

        input_filetypes = next(res)[0]

        res = cur.execute(
            """
            SELECT pipeline_step.stepid, pipeline_step.step_name, pipeline_step.step_number,
            pipeline_step.python_version, pipeline_step.pickle_version,
            pipeline_step.blob_value
            FROM pipeline_step
            INNER JOIN pipeline_table ON pipeline_step.stepid = pipeline_table.id
            WHERE pipeline_table.name = ?
            ORDER BY pipeline_step.step_number;
            """,
            (key,),
        )

        steps: list[tuple[str, BaseIo]] = list()

        for step in res:
            if step[4] != pickle.format_version:  # type: ignore
                raise RuntimeError(
                    "Pickle version mismatch in store and execution environment."
                )

            step_name: str = step[1]
            step_io_dict: dict[str, object] = step[5]

            if (
                not isinstance(step_name, str)
                or not isinstance(step_io_dict, dict)
                or not all(isinstance(k, str) for k in step_io_dict.keys())
                or not all(isinstance(v, object) for v in step_io_dict.values())
            ):
                raise RuntimeError("Step loaded is not valid.")

            steps.append((step_name, DictIo(step_io_dict)))

        return steps, input_filetypes

    def _setup(self):
        """
        Sets up the database, creates the necessary tables (if they don't exist).
        """
        cur = self.conn.cursor()
        cur.executescript(
            """
            BEGIN;
            PRAGMA foreign_keys = ON;
            CREATE TABLE IF NOT EXISTS pipeline_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                input_filetypes TEXT
            );
            CREATE TABLE IF NOT EXISTS pipeline_step (
                stepid INTEGER,
                step_name TEXT NOT NULL,
                step_number INTEGER NOT NULL,
                python_version TEXT NOT NULL,
                pickle_version TEXT NOT NULL,
                blob_value BLOB,
                PRIMARY KEY (stepid, step_number),
                FOREIGN KEY (stepid) REFERENCES pipeline_table(id) ON DELETE CASCADE
            );
            COMMIT;
            """
        )

    def _cleanup(self):
        """
        On exit, closes the sqlite3 connection.
        """
        self.conn.close()
