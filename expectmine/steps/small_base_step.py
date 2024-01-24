from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict

from expectmine.logger.base_logger import BaseLogger


class SmallBaseStep(ABC):
    """
    Base class for small processing steps the pipeline can use.
    Can be used as an alternative to the regular step.
    """

    def __init__(self, **kwargs: Dict[Any, Any]):
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
    def run(
        self,
        input_files: list[Path],
        output_path: Path,
        logger: BaseLogger,
    ) -> list[Path]:
        """
        Processes the input_files given the parameters set in install and
        setup. The step will write to output_path.


        :param input_files: List of input files for the step.
        :type input_files: list[Path]
        :param output_path: Scoped folder where step will write to.
        :type output_path: Path
        :param logger: Gives the step access to log information about its execution.
        :type logger: BaseLogger

        :return: List of all files produced.
        :rtype: list[Path]

        :Example:

        >>> run(["foo.txt, bar.txt"], Path(), Logger(...))
        """
        raise NotImplementedError
