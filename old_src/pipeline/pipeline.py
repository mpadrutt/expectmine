import json
import logging
from datetime import datetime
from pathlib import Path

from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from pipeline import BaseIo
from pipeline.storage.persistent_storage import PersistentStorage
from steps import BaseStep, steps


def get_possible_steps(input: list[str]):
    return [step for step in steps if step.can_run(input)]


def build_pipeline(io_object: BaseIo):
    pipeline: list[BaseStep] = []
    output_files = []
    next_steps = get_possible_steps(output_files)

    step_number = 0

    while True:
        if not next_steps:
            break

        selected_step = inquirer.select(
            message="Select a step",
            choices=[Choice(name=step.name, value=step) for step in next_steps]
            + [Choice(name="Exit", value=None)],
            multiselect=False,
        ).execute()

        if not selected_step:
            break

        selected_step = selected_step()

        selected_step.setup(
            selected_step.get_persistent_storage(selected_step.name),
            io_object,
        )
        selected_step.configure(
            selected_step.get_volatile_storage(selected_step.name),
            io_object,
        )

        output_files = selected_step.output_filetypes(output_files)
        next_steps = get_possible_steps(output_files)

        pipeline.append(selected_step)

        step_number += 1

    return pipeline


def run_pipeline(pipeline: list[BaseStep], pipeline_folder: Path):
    folder_name = str(datetime.now())

    current_input = []

    for i, step in enumerate(pipeline):
        step_path = pipeline_folder / folder_name / f"{i}_{step.name}"
        step_path.mkdir(parents=True, exist_ok=True)

        logger = step.get_logger(step.name)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

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
            step.get_persistent_storage(step.name),
            step.get_volatile_storage(step.name),
            step.get_logger(step.name),
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


def _build_pipeline(io_object: BaseIo) -> list[BaseStep]:
    return []


def _store_pipeline(pipeline: list[BaseStep], pipeline_name: str) -> bool:
    return False


def _run_pipeline(pipeline: list[BaseStep], output_directory: Path) -> list[Path]:
    return []


def _load_pipeline(pipeline_name: str) -> list[BaseStep]:
    return []


def _list_pipelines() -> list[str]:
    return []


def _delete_pipeline(pipeline_name: str) -> bool:
    return False


def _run_step(step: BaseStep, input: list[Path], output_directory: Path) -> list[Path]:
    return []
