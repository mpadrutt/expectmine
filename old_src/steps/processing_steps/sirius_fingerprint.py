import subprocess
from logging import Logger
from pathlib import Path

from InquirerPy import inquirer

from pipeline import PersistentStorage, VolatileStorage
from steps import BaseStep


class SiriusFingerprint(BaseStep):
    name = "SiriusFingerprint"

    @classmethod
    def can_run(cls, input_files: list[str]) -> bool:
        """
        Checks if the step can run on the given input files. Should return a boolean indicating if the step can
        run on the given input files.

        Args:
            input_files (list[Path]): A list of input files.

        Returns:
            bool: True if the step can run on the given input files, False otherwise.
        """
        return (
            all([file.lower() == ".mgf" for file in input_files])
            and len(input_files) > 0
        )

    def output_filetypes(self, input_files: list[Path]) -> list[Path]:
        """
        Returns a list of output filetypes that the step will produce. This is used to check if the output filetypes
        are valid for the next step.

        Args:
            input_files (list[Path]): A list of input files.

        Returns:
            list[Path]: A list of output filetypes that the step will produce.
        """
        return []

    def setup(
        self,
        persistent_storage_object: PersistentStorage,
        io_object,
    ) -> None:
        """
        Is called when the step is created and added to the pipeline. Setup is used to get all
        static config values from the persistent storage_object. If the values are not yet found
        in the storage_object they should be queried by the io_object and then stored in the storage.

        Args:
            persistent_storage_object (Storage): The storage object used to store and retrieve persistent config values.
            io_object (IO): The io object used to query the user for config values. It is a consistant interface for GUI and CLI.

        Returns:
            None
        """
        if not persistent_storage_object.get("executable_path"):
            path = inquirer.filepath(
                message="Please select the Sirius executable",
                only_directories=False,
            ).execute()

            persistent_storage_object.store_object("executable_path", path)

    def configure(
        self,
        volatile_storage_object: VolatileStorage,
        io_object,
    ) -> None:
        """
        Is called after setup and is used to get all volatile config values from the user such as config files that are used
        as input for the step. The values should only be used for this exact step such as input dependent config values.

        Args:
            volatile_storage_object (Storage): The storage object used to store and retrieve volatile config values.
            io_object (IO): The io object used to query the user for config values. It is a consistant interface for GUI and CLI.

        Returns:
            None
        """
        pass

    def run(
        self,
        input_files: list[Path],
        output_path: Path,
        persitant_storage_object: PersistentStorage,
        volatile_storage_object: VolatileStorage,
        logger: Logger,
    ) -> list[Path]:
        """
        The main function of the step. It can access all config values from previous steps. It should return a list of output files.
        Some utility functions are provided by the base class such as logging.

        Args:
            input_files (list[Path]): A list of input files.
            output_path (Path): The output path of the step.
            persitant_storage_object (Storage): The storage object used to store and retrieve persistent config values.
            volatile_storage_object (Storage): The storage object used to store and retrieve volatile config values.
            logger (Logger): The logger object used to log messages and errors.

        Returns:
            list[Path]: A list of output files.
        """
        cmd = [
            str(persitant_storage_object.get("executable_path")),
            "--input",
            input_files[0],
            "--output",
            output_path,
            "formula -p orbitrap fingerprint structure compound-classes write-summaries --output",
            output_path,
        ]
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        stdout, stderr = process.communicate()

        logger.info(stdout)
        logger.info(stderr)

        return []

    def metadata(
        self,
        persitant_storage_object: PersistentStorage,
        volatile_storage_object: VolatileStorage,
    ) -> dict:
        """
        The metadata function is used to return a dictionary of metadata values. The metadata values are used to
        add additional information of the step setup in the pipeline. For example the metadata can contain the
        version of java.

        Args:
            persitant_storage_object (Storage): The storage object used to store and retrieve persistent config values.
            volatile_storage_object (Storage): The storage object used to store and retrieve volatile config values.

        Returns:
            dict: A dictionary of metadata values.
        """
        metadata = {}

        cmd = [str(persitant_storage_object.get("executable_path")), "--version"]
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        stdout, _ = process.communicate()

        output_lines = stdout.splitlines()
        for line in output_lines[:100]:
            if "SIRIUS lib:" in line:
                metadata["sirius_lib"] = line.split(" ")[-1]
            elif "CSI:FingerID lib:" in line:
                metadata["csifingerid_lib"] = line.split(" ")[-1]
            elif "SIRIUS" in line:
                metadata["sirius_version"] = line.split(" ")[-1]

        return metadata
