from abc import ABC, abstractmethod
from pathlib import Path

from src.io import BaseIo
from src.logger import BaseLogger
from src.storage import BaseStore


class BaseStep(ABC):
    """
    Base class for processing steps the pipeline can use.
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @classmethod
    @abstractmethod
    def step_name(cls) -> str:
        """
        Returns the name of the step instance.

        :Example:

        >>> step_name()
        "BaseStep"
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def can_run(cls, input_files: list[str]) -> bool:
        """
        Indicates weather the step can run on a given list of inputs. This
        method is used for the autosuggestion of possible next steps.

        :param input_files: List of input files for the step
        :type input_files: list[str]

        :Example:

        >>> can_run(["test.mzml", "test2.mzml", "data.txt"])
        False

        >>> can_run(["test.mzml", "test2.mzml"])
        True
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def output_filetypes(cls, input_files: list[str]) -> list[str]:
        """
        Returns a list of possible output file-extensions.

        *NOTE: This method currently under development and can return an
        over or under-defined set of file extensions. Also, we currently
        do not rely on internal state to narrow the list of possible
        output file formats*

        :param input_files: List of input files for the step
        :type input_files: list[str]

        :return: A list of output files for the step.
        :rtype: list[str]

        :Example:

        >>> output_filetypes(["test.mzml", "test2.mzml"])
        ["test.txt", "test2.txt"]
        """
        raise NotImplementedError

    @abstractmethod
    def install(self, persistent_store: BaseStore, io: BaseIo, logger: BaseLogger):
        """
        Verifies that all necessary prerequisites to the method have been
        properly installed. If not the method can take action and install the
        files, methods or executables on its own.

        :param persistent_store: Persistent store which saves all step necessary
            parameters. The data stored will be available to all executions
            of the same step.
        :type persistent_store: BaseStore
        :param io: Gives the step access to query data from the user.
        :type io: BaseIo
        :param logger: Gives the step access to log information about its execution.
        :type logger: BaseLogger

        :Example:

        >>> install(Store(...), Io(...), Logger(...))
        """
        raise NotImplementedError

    @abstractmethod
    def setup(self, volatile_store: BaseStore, io: BaseIo, logger: BaseLogger):
        """
        Sets the step up to run with a specific configuration only available to
        this step instance. Purpose of this method is to set parameters for the
        step to correctly process the input data.

        :param volatile_store: Volatile store which saves all step necessary
            execution parameters. The data stored will only be available to
            this instance of the step.
        :type volatile_store: BaseStore
        :param io: Gives the step access to query data from the user.
        :type io: BaseIo
        :param logger: Gives the step access to log information about its execution.
        :type logger: BaseLogger

        :Example:

        >>> setup(Store(...), Io(...), Logger(...))
        """
        raise NotImplementedError

    @abstractmethod
    def run(
        self,
        input_files: list[Path],
        output_path: Path,
        persistent_store: BaseStore,
        volatile_store: BaseStore,
        logger: BaseLogger,
    ) -> list[Path]:
        """
        Processes the input_files given the parameters set in install and
        setup. The step will write to output_path.


        :param input_files: List of input files for the step.
        :type input_files: list[Path]
        :param output_path: Scoped folder where step will write to.
        :type output_path: Path
        :param persistent_store: Persistent store which saves all step necessary
            parameters. The data stored will be available to all executions
            of the same step.
        :param volatile_store: Volatile store which saves all step necessary
            execution parameters. The data stored will only be available to
            this instance of the step.
        :type volatile_store: BaseStore
        :param logger: Gives the step access to log information about its execution.
        :type logger: BaseLogger

        :return: List of all files produced.
        :rtype: list[Path]

        :Example:

        >>> run(["foo.txt, bar.txt"], Path(), Store(...), Store(...), Logger(...))
        """
        raise NotImplementedError

    @abstractmethod
    def metadata(
        self,
        persistent_store: BaseStore,
        volatile_store: BaseStore,
    ) -> dict[str, object]:
        """
        Produces metadata about the past run.

        :param persistent_store: Persistent store which saves all step necessary
            parameters. The data stored will be available to all executions
            of the same step.
        :param volatile_store: Volatile store which saves all step necessary
            execution parameters. The data stored will only be available to
            this instance of the step.
        :type volatile_store: BaseStore

        :return: Dict with all metadata in it.
        :rtype: dict[str, object]

        :Example:

        >>> metadata(Store(...), Store(...))
        { "python": 3.10 }
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def citation_and_disclaimer(cls) -> str:
        """
        Generates all necessary citations and disclaimers.

        :return: A multiline string with necessary citation and disclaimers.
        :rtype: string
        """
        raise NotImplementedError
