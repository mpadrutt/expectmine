from pathlib import Path
from InquirerPy import inquirer
from typing import List, Tuple, TypedDict, NotRequired, Set

from expectmine.io.base_io import BaseIo
from expectmine.logger.base_logger import BaseLogger
from expectmine.steps.base_step import BaseStep
from expectmine.storage.base_storage import BaseStore


class Compound(TypedDict):
    id: NotRequired[int]
    lines: NotRequired[List[str]]
    mslevel: NotRequired[int]
    pepmass: NotRequired[float]
    filename: NotRequired[str]
    origin: NotRequired[str]


class FilterMgf(BaseStep):
    """
    Allows you to filter ions based on a set of crtiterias that have been set.
    Filter either by filename, pepmass or featureId. Consider only ions where both MSLEVEL
    1 and 2 are present.
    """

    @classmethod
    def step_name(cls) -> str:
        return "FilterMgf"

    @classmethod
    def can_run(cls, input_files: list[str]) -> bool:
        return (
            all([file.lower() == ".mgf" for file in input_files])
            and len(input_files) > 0
        )

    @classmethod
    def output_filetypes(cls, input_files: list[str]) -> list[str]:
        return [".mgf" for _ in input_files]

    def install(self, persistent_store: BaseStore, io: BaseIo, logger: BaseLogger):
        pass

    def setup(self, volatile_store: BaseStore, io: BaseIo, logger: BaseLogger):
        should_discard_by_pepmass = io.boolean(
            "discard_pepmass", "Sould any pepmass be discarded?"
        )
        logger.info(f"Filter out by pepmass is set to: {should_discard_by_pepmass}")
        if should_discard_by_pepmass:
            discard_filepath = io.filepath(
                "discard_filepath",
                "Enter a filepath which contains all pepmasses that should be kept.",
            )
            error = io.number("error", "Enter the error in ppm.")
            volatile_store.put("discard_filepath", discard_filepath)
            volatile_store.put("error", error)
            logger.info(
                f"Pepmass input filepath is set to {discard_filepath.absolute()}"
            )
            logger.info(f"Error is set to {error}ppm")

        should_stop = io.boolean("should_stop", "Should stop to ask for compound.")
        volatile_store.put("should_stop", should_stop)

        filter_missing_ms = io.boolean(
            "filter_missing_ms",
            "Should ions be removed where either MS1 or MS2 is missing?",
        )
        volatile_store.put("filter_missing_ms", filter_missing_ms)

        if should_stop:
            logger.info("Step will stop once it recieves input.")

        should_filter_filename = io.boolean(
            "should_filter_filename", "Should only a set of files be analyzed."
        )
        logger.info(f"Filter by filename is set to: {should_filter_filename}")
        if should_filter_filename:
            filter_filename = io.filepath(
                "filter_filename",
                "Enter a filepath which contains all mzML files which should be considered.",
            )
            volatile_store.put("filename_filter", filter_filename)
            logger.info(
                f"Filepath for files which should be filtered is set to {filter_filename.absolute()}"
            )

    def run(
        self,
        input_files: list[Path],
        output_path: Path,
        persistent_store: BaseStore,
        volatile_store: BaseStore,
        logger: BaseLogger,
    ) -> list[Path]:
        discard_filepath = volatile_store.get("discard_filepath", Path)
        error = volatile_store.get("error", float)
        should_stop = volatile_store.get("should_stop", bool)
        filter_missing_ms = volatile_store.get("filter_missing_ms", bool)
        filename_filter = volatile_store.get("filename_filter", Path)

        compound_list: List[Compound] = []

        compound: Compound = {}

        for file in input_files:
            compound: Compound = {}

            with open(file, "r") as f:
                for line in f:
                    compound["lines"].append(line)

                    if "FEATURE_ID" in line.upper():
                        compound["id"] = int(line.split("=")[-1].strip())
                    elif "MSLEVEL" in line.upper():
                        compound["mslevel"] = int(line.split("=")[-1].strip())
                    elif "PEPMASS" in line.upper():
                        compound["pepmass"] = float(line.split("=")[-1].strip())
                    elif "FILENAME" in line.upper():
                        compound["filename"] = line.split("=")[-1].strip()

                    elif "END IONS" in line:
                        compound["origin"] = file.name
                        compound_list.append(compound)
                        compound = {}

            compound_list.sort(key=lambda x: x["id"])  # type: ignore

        if should_stop:
            compound_id = inquirer.number(  # type: ignore
                "Enter the compound id you would like to look at.",
                float_allowed=False,
            ).execute()

            compounds: List[Compound] = [
                c for c in compound_list if "id" in c and c["id"] == compound_id
            ]

            return_files: Set[Path] = set()

            for compound in compounds:
                if "origin" not in compound:
                    continue

                with open(output_path / compound["origin"], "a") as f:
                    f.writelines(compound["lines"])
                    f.write("\n")

                return_files.add(output_path / compound["origin"])

            return list(return_files)

        if discard_filepath and error:
            pepmass_intervals: List[Tuple[float, float]] = []

            with open(discard_filepath, "r") as f:
                exact_error = error / 1_000_000
                for line in f.readlines():
                    pepmass_intervals.append(
                        (float(line) - exact_error, float(line) + exact_error)
                    )

            for i, compound in enumerate(compound_list):
                if "pepmass" not in compound or not any(
                    compound["pepmass"] > low and compound["pepmass"] < high
                    for (low, high) in pepmass_intervals
                ):
                    del compound_list[i]

        if filter_missing_ms:
            for i, compound in enumerate(compound_list):
                if "mslevel" not in compound:
                    del compound_list[i]

                found = False

                for c in compound_list:
                    if "mslevel" in c and c["mslevel"] == 3 - compound["mslevel"]:  # type: ignore
                        found = True
                        break

                if not found:
                    del compound_list[i]

        if not compounds_per_file:
            raise ValueError(
                "The compounds_per_file variable is not set in the volatile store."
            )

        output_paths: list[Path] = []

        for file in input_files:
            num_compounds = 0
            new_lines: list[str] = []
            with open(file, "r") as f:
                while num_compounds < compounds_per_file:
                    line = next(f)
                    new_lines.append(line)
                    if "END IONS" in line:
                        num_compounds += 1

            with open(output_path / file.name, "w") as f:
                f.writelines(new_lines)

            output_paths.append(output_path / file.name)

        return output_paths

    def metadata(
        self, persistent_store: BaseStore, volatile_store: BaseStore
    ) -> dict[str, object]:
        return {}

    @classmethod
    def citation_and_disclaimer(cls) -> str:
        return """
            This step was created for debugging and development.
        """
