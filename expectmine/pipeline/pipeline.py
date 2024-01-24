import json
import os
from pathlib import Path
from typing import Any, Dict, Type

from dotenv import load_dotenv

from expectmine.io.base_io import BaseIo
from expectmine.io.io.dict_io import DictIo
from expectmine.logger.base_logger import BaseLogger
from expectmine.logger.base_logger_adapter import BaseLoggerAdapter
from expectmine.pipeline.utils import (
    validate_add_step,
    validate_init,
    validate_input_files,
    validate_output_directory,
    validate_step_can_run,
)
from expectmine.steps.base_step import BaseStep
from expectmine.steps.small_base_step import SmallBaseStep
from expectmine.steps.utils import get_registered_steps
from expectmine.storage.base_storage import BaseStore
from expectmine.storage.base_storage_adapter import BaseStoreAdapter

load_dotenv()


class Pipeline:
    _registered_steps: list[Type[BaseStep | SmallBaseStep]] = [
        step[1] for step in get_registered_steps()
    ]

    def __init__(
        self,
        persistent_adapter: BaseStoreAdapter,
        volatile_adapter: BaseStoreAdapter,
        logger_adapter: BaseLoggerAdapter,
        output_directory: Path,
        **kwargs: Dict[Any, Any],
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
        validate_output_directory(output_directory)

        self.persistent_adapter = persistent_adapter
        self.volatile_adapter = volatile_adapter
        self.logger_adapter = logger_adapter
        self._output_directory = output_directory
        self.kwargs = kwargs

        self._steps: list[
            tuple[BaseStep | SmallBaseStep, BaseStore, BaseStore, BaseLogger, BaseIo]
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

    def add_step(
        self, step: Type[BaseStep | SmallBaseStep], io: BaseIo | Dict[str, object]
    ):
        """
        Adds a step to the current pipeline but takes into consideration the
        output of the previous step. The io object is used to configure the
        base step.

        :param step: Step that should be added to the pipeline
        :type step: Type[BaseStep | SmallBaseStep]
        :param io: Io object or dict that will configure the step
        :type io: BaseIo | Dict[str, str]

        :Example:

        >>> add_step(Step(...), Io(...))

        >>> add_step()
        TypeError("Step needs to be of type BaseStep")


        :raises TypeError: If the arguments have the wrong type.
        :raises ValueError: If the step can not run on previous output or if
            no input has been given to the pipeline yet.
        """
        if issubclass(step, SmallBaseStep):
            temp_step = step()

            temp_logger_directory = (
                self._output_directory / f"{len(self._steps)}_{temp_step.step_name()}"
            )
            os.makedirs(temp_logger_directory, exist_ok=True)
            temp_logger = self.logger_adapter.get_instance(
                self._output_directory / f"{len(self._steps)}_{temp_step.step_name()}"
            )

            self._current_output_filetypes = temp_step.output_filetypes(
                self._current_output_filetypes  # type: ignore
            )

            self._steps.append(
                (  # type: ignore
                    temp_step,
                    None,
                    None,
                    temp_logger,
                    io,
                )
            )

            return

        if isinstance(io, dict):
            if all(
                isinstance(key, str) and isinstance(value, object)
                for key, value in io.items()
            ):
                io = DictIo(io)
            else:
                raise ValueError("All values of the config dict need to be strings.")

        validate_add_step(step, io)
        validate_step_can_run(step, self._current_output_filetypes)

        temp_step = step()
        temp_persistent_store = self.persistent_adapter.get_instance(
            temp_step.step_name()
        )

        temp_volatile_store = self.volatile_adapter.get_instance(temp_step.step_name())

        temp_logger_directory = (
            self._output_directory / f"{len(self._steps)}_{temp_step.step_name()}"
        )
        os.makedirs(temp_logger_directory, exist_ok=True)
        temp_logger = self.logger_adapter.get_instance(
            self._output_directory / f"{len(self._steps)}_{temp_step.step_name()}"
        )

        temp_step.install(temp_persistent_store, io, temp_logger)
        temp_step.setup(temp_volatile_store, io, temp_logger)

        self._current_output_filetypes = temp_step.output_filetypes(
            self._current_output_filetypes  # type: ignore
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

    def run(self) -> list[Path]:
        """
        Runs the previously added steps in the pipeline and returns the output of the last step.


        :return: Filepaths of output of last step.
        :rtype: list[Path]

        """
        current_files = self._input_files

        for i, step in enumerate(self._steps):
            temp_step = step[0]
            temp_persistent_store = step[1]
            temp_volatile_store = step[2]
            temp_logger = step[3]

            if isinstance(temp_step, SmallBaseStep):
                current_files = temp_step.run(
                    current_files,
                    self._output_directory / f"{i}_{temp_step.step_name()}",
                    temp_logger,
                )
            else:
                current_files = temp_step.run(
                    current_files,
                    self._output_directory / f"{i}_{temp_step.step_name()}",
                    temp_persistent_store,
                    temp_volatile_store,
                    temp_logger,
                )

                with open(
                    self._output_directory
                    / f"{i}_{temp_step.step_name()}"
                    / "metadata.json",
                    "w",
                ) as metadata:
                    json_object = json.dumps(
                        temp_step.metadata(temp_persistent_store, temp_volatile_store),
                        indent=4,
                    )
                    metadata.write(json_object)

        return current_files

    def get_possible_steps(self) -> list[Type[BaseStep | SmallBaseStep]]:
        """
        Returns a list of all possible steps that can run on the current
        output of the pipeline.

        :return: All steps that can be added to the pipeline in its current
            state.
        :rtype: list[Type[BaseStep | SmallBaseStep]]

        :Example:

        >>> get_possible_steps()
        [Step1, Step3]
        """

        if not self._current_output_filetypes:
            return [step for step in self._registered_steps if step.can_run([])]

        return [
            step
            for step in self._registered_steps
            if step.can_run(self._current_output_filetypes)
        ]

    def get_registered_steps(self) -> list[Type[BaseStep | SmallBaseStep]]:
        """
        Returns a list of all steps registered with the pipeline.

        :return: A list of all registered steps.
        :rtype: list[Type[BaseStep | SmallBaseSteps]]

        :Example:

        >>> get_registered_steps()
        [Step1, Step2, Step3]
        """
        return self._registered_steps

    def register_step(self, step: Type[BaseStep | SmallBaseStep]):
        """
        Registers a new step to the pipeline which will then be available
        through get_steps().

        :param step: Step that should be added to the pipeline
        :type step: Type[BaseStep | SmallBaseStep]

        :Example:

        >>> register_step(Step)


        >>> register_step(InvalidStep)
        TypeError("Step is not valid subclass of BaseStep")

        :raises TypeError: If the arguments have the wrong type.
        """
        if not issubclass(step, BaseStep):
            raise TypeError("Step is not valid subclass of BaseStep")

        self._registered_steps.append(step)

    def clear(self):
        """
        Clears all files produced by the step.
        """
        os.rmdir(self._output_directory)
