import os
import sys
from pathlib import Path
from xml.etree import ElementTree

from src.io.base_io import BaseIo
from src.logger.base_logger import BaseLogger
from src.steps.base_step import BaseStep
from src.storage.base_storage import BaseStore
from src.utils.cmd import run_cmd

from .utils import EXPORT_STEPS, IMPORT_STEPS, batchfile_has_spectral_library_files


class MZmine3(BaseStep):
    """
    MZmine3 Batch step. The idea is the following: provide the step with a batchfile,
    give the step some input data in form of .mzml files and pipe the output to the
    next step.

    *Important: It is best to not provide the step with input and output steps.
    If input is provided, the step just changes all input paths to the provided
    paths of the step. in output, it works a bit differently. There only the sirius
    output step is rewritten, the rest is left untouched.*
    """

    @classmethod
    def step_name(cls) -> str:
        return "MZmine3"

    @classmethod
    def can_run(cls, input_files: list[str]) -> bool:
        return (
            all([file.lower() == ".mzml" for file in input_files])
            and len(input_files) > 0
        )

    @classmethod
    def output_filetypes(cls, input_files: list[str]) -> list[str]:
        return [".mgf" for _ in input_files]

    def install(self, persistent_store: BaseStore, io: BaseIo, logger: BaseLogger):
        logger.info("Running install step of MZmine3.")
        if not persistent_store.exists("mzmine3_path"):
            logger.info(
                "MZmine3 executable path was not found in persistent_store. Asking user for path."
            )
            temp_path = io.filepath(
                "mzmine3_path", "Enter the executable path for MZmine3:"
            )
            persistent_store.put("mzmine3_path", str(temp_path.absolute()))
        logger.info("Install step finished.")

    def setup(self, volatile_store: BaseStore, io: BaseIo, logger: BaseLogger):
        logger.info("Running setup step of MZmine3.")

        def validate_batchfile(path: Path) -> bool:
            return path.suffix == ".xml"

        batchfile = io.filepath(
            "batchfile", "Please select the MZmine3 batchfile:", validate_batchfile
        )

        if batchfile_has_spectral_library_files(batchfile):
            spectral_library_files = io.filepaths(
                "spectral_library_files",
                "You included spectral library files, please specify the paths to the files you want to include.",
            )

            volatile_store.put("spectral_library_files", spectral_library_files)

        volatile_store.put("batchfile", batchfile)

        logger.info("Setup step finished.")

    def run(
        self,
        input_files: list[Path],
        output_path: Path,
        persistent_store: BaseStore,
        volatile_store: BaseStore,
        logger: BaseLogger,
    ) -> list[Path]:
        """
        INFO: The following step should work as following:

        1. Check if it has no import if no, monkeypatch import.
        2. Check if ms2 import is used, if yes, update files.
        3. Update files in import step.
        4. Update files in export step -> change current_file

        6. Run step with batchfile
        """

        tree = ElementTree.parse(volatile_store.get("batchfile", Path))
        root = tree.getroot()

        input_steps = []

        for element in IMPORT_STEPS:
            for child in root.findall(f".//batchstep[@method='{element}']"):
                input_steps.append(child)

        if len(input_steps) > 1:
            logger.warn("More than one input step detected.")
            logger.warn("The same input will be provided to each input step.")

        if not input_steps:
            logger.warn("No input step detected, adding default input step.")
            input_tree = ElementTree.parse(
                Path(os.path.dirname(__file__)) / "default_input_step.xml"
            )
            input_root = input_tree.getroot()
            root.insert(0, input_root)
            input_steps.append(input_root)

        for input_step in input_steps:
            for parameter in input_step.findall(".//parameter[@name='File names']"):
                for files in parameter.findall(".//file"):
                    parameter.remove(files)
                for input_file in input_files:
                    file = ElementTree.SubElement(parameter, "file")
                    file.text = str(input_file.absolute())

        if volatile_store.exists("spectral_library_files"):
            logger.info("Changing spectral library files to provided path.")
            for child in root.findall(
                ".//batchstep[@method='io.github.mzmine.modules.io.import_rawdata_all.AllSpectralDataImportModule']"
            ):
                for parameter in child.findall(
                    ".//parameter[@name='Spectral library files']"
                ):
                    for files in parameter.findall(".//file"):
                        parameter.remove(files)
                    for input_file in volatile_store.get(
                        "spectral_library_files", list
                    ):
                        file = ElementTree.SubElement(parameter, "file")
                        file.text = str(input_file.absolute())

        has_output = False

        for output_step in EXPORT_STEPS:
            if root.findall(f".//batchstep[@method='{output_step}']"):
                if has_output:
                    logger.warn(
                        "Multiple output steps detected, only rewriting SiriusExportModule. If you have any other "
                        "steps, make sure they export to valid paths."
                    )
                has_output = True

        sirius_steps = root.findall(
            ".//batchstep[@method='io.github.mzmine.modules.io.export_features_sirius.SiriusExportModule']"
        )

        if not sirius_steps:
            logger.info("Appending sirius output step")
            output_tree = ElementTree.parse(
                Path(os.path.dirname(__file__)) / "sirius_export_step.xml"
            )
            output_root = output_tree.getroot()
            root.append(output_root)
            sirius_steps.append(output_root)

        for step in sirius_steps:
            for parameter in step.findall(".//parameter[@name='Filename']"):
                for file in parameter.findall(".//current_file"):
                    parameter.remove(file)
                file = ElementTree.SubElement(parameter, "current_file")
                file.text = str((output_path / "sirius_output.mgf").absolute())

        tree.write(output_path / "modified_batchfile.xml")

        logger.info(
            f"Running {persistent_store.get('mzmine3_path', str)} with batchfile "
            f"{str((output_path / 'modified_batchfile.xml').absolute())}"
        )
        status, out, err = run_cmd(
            persistent_store.get("mzmine3_path", str),
            [("-b", str((output_path / "modified_batchfile.xml").absolute()))],
        )
        logger.info(out)
        logger.error(err)
        logger.info(f"Finished running cmd with status code {status}.")

        logger.info(f"For citation:\n {self.citation_and_disclaimer()}")

        logger.info(
            f"Returning path {str((output_path / 'sirius_output.mgf').absolute())} for next step."
        )

        return [(output_path / "sirius_output.mgf")]

    def metadata(
        self, persistent_store: BaseStore, volatile_store: BaseStore
    ) -> dict[str, object]:
        metadata = {}

        status, out, err = run_cmd(
            persistent_store.get("mzmine3_path", str),
            ["--version"],
        )

        for line in err.splitlines():
            if "io.github.mzmine.main.MZmineCore main Starting MZmine" in line:
                metadata["mzmine_version"] = line.split(" ")[-1]
            elif "openjdk version" in line:
                metadata["java_version"] = line.split(" ")[2].strip('"')
            elif "OpenJDK Runtime Environment" in line:
                metadata["java_runtime"] = " ".join(line.split(" ")[3:]).strip('"')
            elif "OpenJDK 64-Bit Server" in line:
                metadata["java_server"] = " ".join(line.split(" ")[3:]).strip('"')

        metadata["python_version"] = sys.version

        return metadata

    @classmethod
    def citation_and_disclaimer(cls) -> str:
        return """
        Please cite the following publication if you use MZmine to analyze your data:

        Schmid, R., Heuckeroth, S., Korf, A. et al. Integrative analysis of multimodal mass spectrometry
        data in MZmine 3. Nature Biotechnology (2023). https://doi.org/10.1038/s41587-023-01690-2
        """
