from pathlib import Path

from src.io.base_io import BaseIo
from src.logger.base_logger import BaseLogger
from src.steps.base_step import BaseStep
from src.storage.base_storage import BaseStore
from src.utils.cmd import run_cmd


class SiriusFingerprint(BaseStep):
    """
    Step which takes .mgf as input and creates CSI:FingerID as output.

    *IMPORTANT: This step requires the env variables SIRIUS_USERNAME
    and SIRIUS_PASSWORD to be set before execution.*
    """

    @classmethod
    def step_name(cls) -> str:
        return "SiriusFingerprint"

    @classmethod
    def can_run(cls, input_files: list[str]) -> bool:
        return (
            all([file.lower() == ".mgf" for file in input_files])
            and len(input_files) > 0
        )

    @classmethod
    def output_filetypes(cls, input_files: list[str]) -> list[str]:
        return ["*/*.tsv"]

    def install(self, persistent_store: BaseStore, io: BaseIo, logger: BaseLogger):
        logger.info("Running install step of SiriusFingerprint.")
        if not persistent_store.exists("sirius_path"):
            logger.info(
                "Sirius executable path was not found in persistent_store. Asking user for path."
            )
            temp_path = io.filepath(
                "sirius_path", "Enter the executable path for Sirius:"
            )
            persistent_store.put("sirius_path", str(temp_path.absolute()))

        logger.info("Install step finished.")

    def setup(self, volatile_store: BaseStore, io: BaseIo, logger: BaseLogger):
        logger.info("Running setup step of SiriusFingerprint.")
        set_max_mz = io.boolean(
            "set_max_mz",
            "Do you want to set a mz to only consider compounds with mz lower than it.",
        )

        def validate_mz(num: int | float):
            return num > 0

        if set_max_mz:
            max_mz = io.number("max_mz", "Set the mz to limit compounds.", validate_mz)
            max_mz = int(max_mz)
            logger.info(f"Limiting the compounds to mz < {max_mz}")
            volatile_store.put("max_mz", max_mz)

        instrument = io.single_choice(
            "instrument",
            "Which instrument was used?",
            [("Q-TOF", "qtof"), ("Orbitrap", "orbitrap"), ("FT-ICR", "fticr")],
        )

        volatile_store.put("instrument", instrument)

        logger.info("Setup step finished.")

    def run(
        self,
        input_files: list[Path],
        output_path: Path,
        persistent_store: BaseStore,
        volatile_store: BaseStore,
        logger: BaseLogger,
    ) -> list[Path]:
        logger.info(f"Running {persistent_store.get('sirius_path', str)}")

        max_mz = volatile_store.get("max_mz", int)

        input_files_string = [f"-i {str(file.absolute())}" for file in input_files]

        login = (
            f"{persistent_store.get('sirius_path', str)} login --user-env=SIRIUS_USERNAME "
            "--password-env=SIRIUS_PASSWORD"
        )
        run_file = (
            f"{persistent_store.get('sirius_path', str)} {str(max_mz) if max_mz else ''} "
            f"{' '.join(input_files_string)} "
            f"-o {str((output_path / 'output').absolute())}"
        )

        sirius_command_pipeline = (
            f"sirius -p {volatile_store.get('instrument', str)} "
            "fingerprint "
            "structure -d ALL "
            "write-summaries"
        )

        status, out, err = run_cmd(f"{login} && {run_file} {sirius_command_pipeline}")

        logger.info(out)
        logger.error(err)
        logger.info(f"Finished running cmd with status code {status}.")
        logger.info(
            f"Returning path {str((output_path / 'output').absolute())} "
            "for next step."
        )

        return [output_path / "output"]

    def metadata(
        self, persistent_store: BaseStore, volatile_store: BaseStore
    ) -> dict[str, object]:
        metadata: dict[str, object] = {}

        status, out, err = run_cmd(
            persistent_store.get("sirius_path", str),
            ["--version"],
        )

        for line in out.split("\n"):
            if "SIRIUS lib:" in line:
                metadata["sirius_lib"] = line.split(" ")[-1]
            elif "CSI:FingerID lib:" in line:
                metadata["csifingerid_lib"] = line.split(" ")[-1]
            elif "SIRIUS" in line:
                metadata["sirius_version"] = line.split(" ")[-1]

        return metadata

    @classmethod
    def citation_and_disclaimer(cls) -> str:
        return """
        Please cite the following publications when using our tool:

        When using the SIRIUS Software please cite the following paper:

        Kai Dührkop, Markus Fleischauer, Marcus Ludwig, Alexander A. Aksenov, Alexey V. Melnik, Marvin Meusel,
        Pieter C. Dorrestein, Juho Rousu and Sebastian Böcker
        SIRIUS4: a rapid tool for turning tandem mass spectra into metabolite structure information
        Nat Methods, 16, 2019.  https://doi.org/10.1038/s41592-019-0344-8

        Depending on the tools you have used please also cite:

        Kai Dührkop, Louis-Félix Nothias, Markus Fleischauer, Raphael Reher, Marcus Ludwig, Martin A. Hoffmann,
        Daniel Petras, William H. Gerwick, Juho Rousu, Pieter C. Dorrestein and Sebastian Böcker
        Systematic classification of unknown metabolites using high-resolution fragmentation mass spectra
        Nature Biotechnology, 2020.  https://doi.org/10.1038/s41587-020-0740-8
        (Cite if you are using: CANOPUS)

        Yannick Djoumbou Feunang, Roman Eisner, Craig Knox, Leonid Chepelev, Janna Hastings, Gareth Owen, Eoin Fahy,
        Christoph Steinbeck, Shankar Subramanian, Evan Bolton, Russell Greiner, David S. Wishart
        ClassyFire: automated chemical classification with a comprehensive, computable taxonomy
        J Cheminf, 8, 2016.  https://doi.org/10.1186/s13321-016-0174-y
        (Cite if you are using: CANOPUS)

        Kim, Hyun Woo and Wang, Mingxun and Leber, Christopher A. and Nothias, Louis-Félix and Reher,
        Raphael and Kang,Kyo Bin and van der Hooft, Justin J. J. and Dorrestein, Pieter C. and Gerwick,
        William H. and Cottrell, Garrison W.
        NPClassifier: A Deep Neural Network-Based Structural Classification Tool for Natural Products
        Journal of Natural Products, 84, 2021.  https://doi.org/10.1021/acs.jnatprod.1c00399
        (Cite if you are using: CANOPUS)

        Kai Dührkop, Huibin Shen, Marvin Meusel, Juho Rousu and Sebastian Böcker
        Searching molecular structure databases with tandem mass spectra using CSI:FingerID
        Proc Natl Acad Sci U S A, 112, 2015.  https://doi.org/10.1073/pnas.1509788112
        (Cite if you are using: CSI:FingerID)

        Martin A. Hoffmann and Louis-Félix Nothias and Marcus Ludwig and Markus Fleischauer and Emily C. Gentry
        and Michael Witting and Pieter C. Dorrestein and Kai Dührkop and Sebastian Böcker
        Assigning confidence to structural annotations from mass spectra with COSMIC
        bioRxiv, 2021.  https://doi.org/10.1101/2021.03.18.435634
        (Cite if you are using: CSI:FingerID, COSMIC)

        Sebastian Böcker and Kai Dührkop
        Fragmentation trees reloaded
        J Cheminform, 8, 2016.  https://doi.org/10.1186/s13321-016-0116-8
        (Cite if you are using: Fragmentation Trees)

        Sebastian Böcker, Matthias Letzel, Zsuzsanna Lipták and Anton Pervukhin
        SIRIUS: Decomposing isotope patterns for metabolite identification
        Bioinformatics, 25, 2009.  https://doi.org/10.1093/bioinformatics/btn603
        (Cite if you are using: Isotope Pattern analysis)

        Marcus Ludwig, Louis-Félix Nothias, Kai Dührkop, Irina Koester, Markus Fleischauer, Martin A. Hoffmann,
        Daniel Petras, Fernando Vargas, Mustafa Morsy, Lihini Aluwihare, Pieter C. Dorrestein, Sebastian Böcker
        ZODIAC: database-independent molecular formula annotation using Gibbs sampling reveals unknown small molecules
        bioRxiv, 2019.  https://doi.org/10.1101/842740
        (Cite if you are using: ZODIAC)
        """
