from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional

from src.io import BaseIo
from src.steps import BaseStep


class BasePipelineStore(ABC):
    @abstractmethod
    def __init__(self, persistent_path: Path, **kwargs: Dict[Any, Any]):
        """
        Creates an instance of a pipeline store. It requires a path to the
        persistant directory where data can be stored.

        :param persistent_path: The path which the storage can use to persist
            data.
        :type persistent_path: Path

        :Example:

        >>> BasePipelineStore(Path("path2"))
        BaseStore

        >>> validate_pipeline_store_init()
        TypeError("Persistent path needs to be of type Path")


        :raises TypeError: If the arguments have the wrong type.
        """
        raise NotImplementedError

    @abstractmethod
    def store_pipeline(
        self,
        key: str,
        steps: list[BaseStep],
        io: list[BaseIo],
        input_files: list[Path],
    ) -> None:
        """
        Saves the given key-pipeline pair to the store.

        :param key: The key to associate with the pipeline. A key cannot be
            empty. Keys have a maximum length of 255 characters.
        :type key: str
        :param steps: List of BaseSteps that make up the pipeline.
        :type steps: list[BaseStep]
        :param io: List of all Io objects used to configure the steps.
        :type io: list[BaseIo]
        :param input_files: List of input files to the pipeline.
        :type input_files: list[Path]

        :Example:

        >>> store_pipeline(Store(...), "Hello", [Step(...)], [Store(...)], [Path('text.txt')])


        >>> store_pipeline("A", "B")
        TypeError("Store needs to be of type BaseStore.")

        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If the key is empty or longer than 255 characters. If Steps
            and volatile_stores do not match in length or input files are not files
            but contain directories.
        """
        raise NotImplementedError

    @abstractmethod
    def list_pipelines(self) -> list[str]:
        """
        Returns a list of keys of all currently stored pipelines.

        :Example:

        >>> list_pipelines()
        list["Pipeline_1", "Pipeline_2", "Pipeline_3"]
        """
        raise NotImplementedError

    @abstractmethod
    def load_pipeline(
        self, key: str
    ) -> Optional[tuple[list[tuple[str, BaseIo]], list[str]]]:
        """
        For a given key, loads the given pipeline from store and returns a list of
        io objects to configure the steps.

        *Make sure you know what you are loading. The loading step relies on unpickle
        which can execute data!*

        :return: A tuple with consisting of a list of step-tuples of the following
            structure: ("step_name", step_io), and a list of input filetypes. If the
            pipeline key is not found, returns None.
        :rtype: Optional[tuple[list[tuple[str, BaseIo]], list[str]]]

        :Example:

        >>> load_pipeline("Pipeline1")
        (list[("Step1", Io()), ("Step2", Io())], list[".xml", ".xml"])

        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If the key is empty or too long.
        :raises: RuntimeError: If the pickle version does not match with the stored data.
        """
        raise NotImplementedError
