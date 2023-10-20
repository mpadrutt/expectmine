from pathlib import Path
from typing import Type

from src.steps import BaseStep
from src.io import BaseIo
from src.logger import BaseLoggerAdapter
from src.storage import BaseStorageAdapter


def validate_init(
    persistent_adapter: BaseStorageAdapter,
    volatile_adapter: BaseStorageAdapter,
    logger_adapter: BaseLoggerAdapter,
):
    """
    Validates the adapters to be valid when initializing the pipeline class.


    :param persistent_adapter: Persistent storage adapter to the pipeline
    :type persistent_adapter: BaseStorageAdapter
    :param volatile_adapter: Volatile storage adapter to the pipeline
    :type volatile_adapter: BaseStorageAdapter
    :param logger_adapter: Logging adapter to the pipeline
    :type logger_adapter: BaseLoggerAdapter

    :Example:

    >>> validate_init(StoageAdapter(...), StorageAdapter(...), LoggingAdapter(...))


    >>> validate_init()
    TypeError("Persistent adapter needs to be an instance of BaseStorageAdapter.")


    :raises TypeError: If the arguments have the wrong type.
    """
    if not isinstance(persistent_adapter, BaseStorageAdapter):
        raise TypeError(
            "Persistent adapter needs to be an instance of BaseStorageAdapter."
        )
    if not isinstance(volatile_adapter, BaseStorageAdapter):
        raise TypeError(
            "Volatile adapter needs to be an instance of BaseStorageAdapter."
        )
    if not isinstance(logger_adapter, BaseLoggerAdapter):
        raise TypeError(
            "Logging adapter needs to be an instance of BaseStorageAdapter."
        )


def validate_input_files(input_files: list[Path], current_input_filetypes: list[str]):
    """
    Validates the input files to the pipeline. The list can only contain
    Path objects and those must point to files.


    :param input_files: List of input_files to the pipeline
    :type input_files: list[Path]
    :param current_input_filetypes: List of the current input filetypes.
    :type current_input_filetypes: list[str]

    :Example:

    >>> validate_input_files([Path("text.txt"), Path("test.xml")])


    >>> validate_input_files()
    TypeError("input_files need to be of type list[Path].")

    >>> validate_input_files([Path("/directory")])
    ValueError("input_files need to exclusively contain files.")


    :raises TypeError: If the arguments have the wrong type.
    :raises ValueError: If not all elements are files or if the input filetype
            gets changed while reassigning input_files.
    """
    if not isinstance(input_files, list):
        raise TypeError("input_files need to be of type list[Path].")

    if not all(isinstance(file, Path) for file in input_files):
        raise TypeError("input_files need to be of type list[Path].")

    if not all(file.is_file() for file in input_files):
        raise ValueError("input_files need to exclusively contain files.")

    if not all(file.suffix in current_input_filetypes for file in input_files):
        raise ValueError(
            "input_files are forbidden to change input type of the pipeline."
        )


def validate_add_step(step: Type[BaseStep], io: BaseIo):
    """
    Validates the adapter init parameters.


    :param step: Step that should be added to the pipeline
    :type step: Type[BaseStep]
    :param io: Io object that will configure the step
    :type io: BaseIo

    :Example:

    >>> validate_add_step(Step(...), Io(...))


    >>> validate_init()
    TypeError("Step needs to be of type BaseStep")


    :raises TypeError: If the arguments have the wrong type.
    """
    if not issubclass(step, BaseStep):
        raise TypeError("Step needs to be of type BaseStep")
    if not isinstance(io, BaseIo):
        raise TypeError("Io needs to be of type BaseIo")


def validate_step_can_run(step: Type[BaseStep], input_filetypes: list[str] | None):
    """
    Validates that a step can actually run on a given input. Throws an
    error otherwise.


    :param step: Step that should be added to the pipeline
    :type step: Type[BaseStep]
    :param input_filetypes: Current input where step needs to run on.
    :type input_filetypes: list[str] | None

    :Example:

    >>> validate_add_step(Step(...), [".txt"])


    >>> validate_add_step(Step(...), None)
    TypeError("Step needs to be of type BaseStep")


    :raises ValueError: If the step can not run on previous output or if
        no input has been given to the pipeline yet.
    """
    if not input_filetypes:
        raise ValueError("No input given to the pipeline before adding step.")

    if not step.can_run(input_filetypes):
        raise ValueError(f"Step {step.step_name()} can not run on the given input.")
