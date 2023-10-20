import subprocess
from logging import Logger
from pathlib import Path
from shutil import copy

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

from pipeline import PersistentStorage, VolatileStorage
from pipeline.io.base_io import BaseIo
from steps import BaseStep
from utils import install_zip_to_path

DEFAULT_MZMINE_PATH = Path(
    "/Applications/MZmine.app/Contents/MacOS/MZmine", absolute=True
)
DEFAULT_INSTALL_PATH = Path("/Applications", absolute=True)


class Mzmine3BatchMode(BaseStep):
    name = "Mzmine3"

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
            all([file.lower() == ".mzml" for file in input_files])
            and len(input_files) > 0
        )

    def output_filetypes(self, input_files: list[str]) -> list[str]:
        """
        Returns a list of output filetypes that the step will produce. This is used to check if the output filetypes
        are valid for the next step.

        Args:
            input_files (list[Path]): A list of input files.

        Returns:
            list[Path]: A list of output filetypes that the step will produce.
        """
        return [".mgf" for _ in input_files]

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
            persistent_storage_object (Storage): The storage object used to
            store and retrieve persistent config values.
            io_object (IO): The io object used to query the user for config
            values. It is a consistant interface for GUI and CLI.

        Returns:
            None
        """
        if persistent_storage_object.get("executable_path"):
            # TODO: Check for updates
            return

        if DEFAULT_MZMINE_PATH.exists() and False:
            persistent_storage_object.store_object(
                "executable_path", DEFAULT_MZMINE_PATH
            )
            # TODO: Check for updates
            return

        if not inquirer.confirm(
            message="MZmine3 is not installed. Do you want to install it now?",
        ).execute():
            # TODO: Smart way of exiting here
            exit()

        while True:
            version = inquirer.select(
                message="Please select the MZmine3 version",
                choices=[
                    Choice(name=release["version"], value=release)
                    for release in get_releases("mzmine/mzmine3")
                    if any([r["name"].endswith(".zip") for r in release["assets"]])
                ]
                + [Separator(), Choice(name="Exit", value=False)],
            ).execute()

            if not version:
                exit()

            download = inquirer.select(
                message="Please select the MZmine3 download",
                choices=[
                    Choice(name=asset["name"], value=asset["browser_download_url"])
                    for asset in version["assets"]
                    if asset["name"].endswith(".zip")
                ]
                + [Separator(), Choice(name="Back", value=False)],
            ).execute()

            if download:
                break

        install_zip_to_path(download, DEFAULT_INSTALL_PATH)
        persistent_storage_object.store_object("executable_path", DEFAULT_MZMINE_PATH)

    def configure(
        self,
        volatile_storage_object: VolatileStorage,
        io_object: BaseIo,
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
        files = [
            Choice(name=file.name, value=file)
            for file in Path("testdata").iterdir()
            if file.is_file()
        ]

        selected_files = inquirer.select(
            message="Please select the MZmine3 batchfile",
            choices=files,
            multiselect=False,
        ).execute()

        volatile_storage_object.store_object("batchfile", selected_files)

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

        cmd = f"{str(persitant_storage_object.get('executable_path'))} -b {volatile_storage_object.get('batchfile')}"
        logger.info(f"Running command: {cmd}")

        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )

        stdout = result.stdout.decode("utf-8")
        stderr = result.stderr.decode("utf-8")

        logger.info(stdout)
        logger.info(stderr)

        if result.returncode != 0:
            return []

        logger.info(
            f"Finished running MZmine3BatchMode with exit code {result.returncode}"
        )

        copy(Path("generated") / "temp/temp_mzmine.mgf", output_path / "output.mgf")

        return [output_path / "output.mgf"]

    def metadata(
        self,
        persitant_storage_object: PersistentStorage,
        volatile_storage_object: VolatileStorage,
    ) -> dict[str, object]:
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

        _, stderr = process.communicate()

        output_lines = stderr.splitlines()
        for line in output_lines[:100]:
            if "io.github.mzmine.main.MZmineCore main Starting MZmine" in line:
                metadata["mzmine_version"] = line.split(" ")[-1]
            elif "openjdk version" in line:
                metadata["java_version"] = line.split(" ")[2].strip('"')
            elif "OpenJDK Runtime Environment" in line:
                metadata["java_runtime"] = " ".join(line.split(" ")[3:]).strip('"')
            elif "OpenJDK 64-Bit Server" in line:
                metadata["java_server"] = " ".join(line.split(" ")[3:]).strip('"')

        return metadata  # type: ignore
