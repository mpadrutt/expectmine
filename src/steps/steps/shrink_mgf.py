from pathlib import Path
from typing import Type, Union

from ...io import BaseIo
from ...logger import BaseLogger
from ...storage import BaseStore
from .. import BaseStep


class ShrinkMgf(BaseStep):
    """
    Only takes the first n compounds of each given .mgf file. Good for debugging.
    """

    @classmethod
    def step_name(cls) -> str:
        return "ShrinkMgf"

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
        number_of_compounds = io.number(
            "compounds_per_file",
            "How many compounds should be in each file?",
        )

        logger.info(f"Compounds per file is set to: {number_of_compounds}")

        volatile_store.put("compounds_per_file", number_of_compounds)

    def run(
        self,
        input_files: list[Path],
        output_path: Path,
        persistent_store: BaseStore,
        volatile_store: BaseStore,
        logger: BaseLogger,
    ) -> list[Path]:
        compounds_per_file = int(volatile_store.get("compounds_per_file", float))
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
        pass

    @classmethod
    def citation_and_disclaimer(cls) -> str:
        return """
            This step was created for debugging and development.
        """
