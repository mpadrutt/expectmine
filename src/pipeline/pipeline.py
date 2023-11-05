from pathlib import Path
from typing import Type

from .utils import (
    validate_init,
    validate_input_files,
    validate_add_step,
    validate_step_can_run,
)

from src.io import BaseIo
from src.steps import BaseStep, get_registered_steps
from src.storage import BaseStoreAdapter, BaseStore
from src.logger import BaseLoggerAdapter, BaseLogger


class Pipeline:
    _registered_steps: list[Type[BaseStep]] = [
        step[1] for step in get_registered_steps()
    ]

    def __init__(
        self,
        persistent_adapter: BaseStoreAdapter,
        volatile_adapter: BaseStoreAdapter,
        logger_adapter: BaseLoggerAdapter,
        output_directory: Path,
        **kwargs,
    ):
        """
        Initializes the pipeline. Needs 3 adapters to work.

        :param persistent_adapter: Persistent storage adapter to the pipeline
        :type persistent_adapter: BaseStoreAdapter
        :param volatile_adapter: Volatile storage adapter to the pipeline
        :type volatile_adapter: BaseStoreAdapter
        :param logger_adapter: Logging adapter to the pipeline
        :type logger_adapter: BaseLoggerAdapter
        :param output_directory: Path to where the pipeline should output to.
        :type output_directory: Path

        :Example:

        >>> __init__(StoageAdapter(...), StorageAdapter(...), LoggingAdapter(...), Path())


        >>> __init__()
        TypeError("Persistent adapter needs to be an instance of BaseStorageAdapter.")


        :raises TypeError: If the arguments have the wrong type.
        """
        validate_init(persistent_adapter, volatile_adapter, logger_adapter)

        self.persistent_adapter = persistent_adapter
        self.volatile_adapter = volatile_adapter
        self.logger_adapter = logger_adapter
        self._output_directory = output_directory
        self.kwargs = kwargs

        self._steps: list[
            tuple[BaseStep, BaseStore, BaseStore, BaseLogger, BaseIo]
        ] = list()
        self._input_files: list[Path] = list()
        self._current_input_filetypes: list[str] | None = None
        self._current_output_filetypes: list[str] | None = None

    def set_input(self, input_files: list[Path]):
        """
        Assigns input files to the pipeline

        :param input_files: File list to set as input
        :type input_files: list[Path]

        :Example:

        >>> set_input([Path("text.txt"), Path("input.xml")])


        >>> set_input()
        ValueError("input_files need to exclusively contain files.")


        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If not all elements are files or if the input filetype
            gets changed while reassigning input_files.
        """
        validate_input_files(input_files, self._current_input_filetypes)

        self._input_files = input_files
        self._current_input_filetypes = [file.suffix for file in self._input_files]

        if not self._current_output_filetypes:
            self._current_output_filetypes = [file.suffix for file in self._input_files]

    def add_step(self, step: Type[BaseStep], io: BaseIo):
        """
        Adds a step to the current pipeline but takes into consideration the
        output of the previous step. The io object is used to configure the
        base step.

        :param step: Step that should be added to the pipeline
        :type step: Type[BaseStep]
        :param io: Io object that will configure the step
        :type io: BaseIo

        :Example:

        >>> add_step(Step(...), Io(...))

        >>> add_step()
        TypeError("Step needs to be of type BaseStep")


        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If the step can not run on previous output or if
            no input has been given to the pipeline yet.
        """
        validate_add_step(step, io)
        validate_step_can_run(step, self._current_output_filetypes)

        temp_step = step()
        temp_persistent_store = self.persistent_adapter.get_instance(
            temp_step.step_name()
        )
        temp_volatile_store = self.volatile_adapter.get_instance(temp_step.step_name())
        temp_logger = self.logger_adapter.get_instance(
            self._output_directory / f"{len(self._steps)}{temp_step.step_name()}"
        )

        temp_step.install(temp_persistent_store, io, temp_logger)
        temp_step.setup(temp_volatile_store, io, temp_logger)

        self._current_output_filetypes = temp_step.output_filetypes(
            self._current_output_filetypes
        )

        self._steps.append(
            (
                temp_step,
                temp_persistent_store,
                temp_volatile_store,
                temp_logger,
                io,
            )
        )

    def run(self):
        """
        Runs the previously added steps in the pipeline.
        """
        current_files = self._input_files

        for i, step in enumerate(self._steps):
            temp_step = step[0]
            temp_persistent_store = step[1]
            temp_volatile_store = step[2]
            temp_logger = step[3]

            current_files = temp_step.run(
                current_files,
                self._output_directory / f"{i}_{temp_step.step_name()}",
                temp_persistent_store,
                temp_volatile_store,
                temp_logger,
            )

    def get_possible_steps(self) -> list[Type[BaseStep]]:
        """
        Returns a list of all possible steps that can run on the current
        output of the pipeline.

        :return: All steps that can be added to the pipeline in its current
            state.
        :rtype: list[Type[BaseStep]]

        :Example:

        >>> get_possible_steps()
        [Step1, Step3]
        """
        return [
            step
            for step in self._registered_steps
            if step.can_run(self._current_output_filetypes)
        ]

    def get_registered_steps(self) -> list[Type[BaseStep]]:
        """
        Returns a list of all steps registered with the pipeline.

        :return: A list of all registered steps.
        :rtype: list[Type[BaseStep]]

        :Example:

        >>> get_registered_steps()
        [Step1, Step2, Step3]
        """
        return self._registered_steps

    def register_step(self, step: Type[BaseStep]):
        """
        Registers a new step to the pipeline which will then be available
        through get_steps().

        :param step: Step that should be added to the pipeline
        :type step: Type[BaseStep]

        :Example:

        >>> register_step(Step)


        >>> register_step(InvalidStep)
        TypeError("Step is not valid subclass of BaseStep")

        :raises TypeError: If the arguments have the wrong type.
        """
        if not issubclass(step, BaseStep):
            raise TypeError("Step is not valid subclass of BaseStep")

        self._registered_steps.append(step)


# Regular workflow in code
"""
Pipeline.get_stored(store) -> list[key]
Pipeline.load(store, key) -> Pipeline
Pipeline.store(store, key)
"""
