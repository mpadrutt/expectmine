import json
import logging
import pickle
from datetime import datetime
from pathlib import Path

from tqdm import tqdm

from pipeline.io.base_io import BaseIo
from steps import steps
from steps.base_classes.base_step import BaseStep

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class Pipeline:
    @classmethod
    def load_instance(cls, filepath: Path):
        with open(filepath, "rb") as file:
            return pickle.load(file)

    def __init__(self, name: str, *args, **kwargs):
        self._name: str = name
        self._steps: list[BaseStep] = []
        self._input_files: list[Path] = []
        self._output_path: Path | None = None
        self._output_filetypes: list[list[str]] = []
        self.args = args
        self.kwargs = kwargs

    def add_step(self, step: BaseStep, io_object: BaseIo):
        if not step.can_run(self._output_filetypes[-1]):
            raise Exception("Step cannot run with current output files")

        step = step()  # type: ignore
        step_output_filetypes = step.output_filetypes(self._output_filetypes[-1])

        step.setup(step.get_persistent_storage(step.name), io_object)
        step.configure(step.get_volatile_storage(step.name), io_object)

        self._steps.append(step)
        self._output_filetypes.append(step_output_filetypes)

    def get_input_files(self):
        return self._input_files

    def set_input_files(self, input_files: list[Path]):
        self._input_files = input_files
        if not self._output_filetypes:
            self._output_filetypes = [[file.suffix for file in input_files]]

    def get_input_filetypes(self) -> list[str]:
        return self._output_filetypes[0]

    def get_next_steps(self) -> list[BaseStep]:
        return [step for step in steps if step.can_run(self._output_filetypes[-1])]

    def set_output_path(self, output_path: Path) -> None:
        self._output_path = output_path

    def __call__(self, *args, **kwargs) -> list[Path]:
        self._validate_before_run()

        folder_name = str(datetime.now())

        current_input = self._input_files

        for i, step in tqdm(enumerate(self._steps)):
            step_path = self._output_path / folder_name / f"{i}_{step.name}"  # type: ignore
            step_path.mkdir(parents=True, exist_ok=True)

            logger = step.get_logger(step.name)
            persistent_storage = step.get_persistent_storage(step.name)
            volatile_storage = step.get_volatile_storage(step.name)

            file_handler = logging.FileHandler(step_path / "log.log")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.setLevel(logging.INFO)

            logger.info(f"Starting step {step.name} at {datetime.now()}")
            logger.info(f"Step path: {step_path}")
            logger.info(f"Dumping instance to {step_path}/dump.pkl")
            step.dump_instance(step_path)
            logger.info(f"Successfully dumped instance to {step_path}/dump.pkl")

            logger.info(f"Input: {current_input}")
            current_input = step.run(
                current_input,
                step_path,
                persistent_storage,
                volatile_storage,
                logger,
            )
            logger.info(f"Output: {current_input}")

            logger.info(f"Dumping metadata to {step_path}/metadata.json")
            with open(step_path / "metadata.json", "w") as file:
                json_object = json.dumps(
                    step.metadata(
                        step.get_persistent_storage(step.name),
                        step.get_volatile_storage(step.name),
                    ),
                    indent=4,
                )
                file.write(json_object)

            logger.info(f"Successfully dumped metadata to {step_path}/metadata.json")
            logger.info(f"Finished step {step.name} at {datetime.now()}")

        return current_input

    def __len__(self) -> int:
        return len(self._steps)

    def __str__(self) -> str:
        return self._name

    def dump_class(self, output_path: Path):
        with open(output_path / "dump.pkl", "wb") as file:
            pickle.dump(self, file)

    def _validate_before_run(self):
        if not self._steps:
            raise Exception("Pipeline has no steps")

        if not self._input_files:
            raise Exception("Pipeline has no input files")

        if not self._output_path:
            raise Exception("Pipeline has no output path")

        if len(self._steps) + 1 != len(self._output_filetypes):
            raise Exception("Pipeline has not been configured correctly")

        for step, input_data in zip(self._steps, self._output_filetypes):
            if not step.can_run(input_data):
                raise Exception("Pipeline has not been configured correctly2")


# boolean
# string
# integer

# single_choice
# multiple_choice

# filepath
