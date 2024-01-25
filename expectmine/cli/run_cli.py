import os
import uuid
from pathlib import Path
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from expectmine.pipeline.pipeline import Pipeline
from expectmine.storage.adapters.in_memory_adapter import InMemoryStoreAdapter
from expectmine.logger.adapters.cli_logger_adapter import CliLoggerAdapter
from expectmine.io.io.cli_io import CliIo
from expectmine.logger.base_logger import LogLevel

CURRENT_WORKING_DIRECTORY = Path.cwd()


def list_files():
    current_directory = os.getcwd()
    files = [
        f
        for f in os.listdir(current_directory)
        if os.path.isfile(os.path.join(current_directory, f))
    ]
    return files


def run_cli():
    file_choices = list_files()

    input_files = inquirer.checkbox(
        message="Select files to process",
        choices=[Choice(Path(file_name), name=file_name) for file_name in file_choices],
    ).execute()

    pipeline_path = CURRENT_WORKING_DIRECTORY / str(uuid.uuid4())

    ps = InMemoryStoreAdapter(pipeline_path, pipeline_path)
    vs = InMemoryStoreAdapter(pipeline_path, pipeline_path)
    la = CliLoggerAdapter(log_level=LogLevel.INFO, write_logfile=True)

    pipeline = Pipeline(ps, vs, la, pipeline_path)
    pipeline.set_input(input_files)

    while True:
        possible_steps = pipeline.get_possible_steps()

        if not possible_steps:
            break

        next_step = inquirer.select(
            message="Select your next step",
            choices=[Choice(step, name=step.step_name()) for step in possible_steps]
            + [Choice(None, name="Finish...")],
        ).execute()

        if not next_step:
            break

        pipeline.add_step(next_step, CliIo())

    pipeline.run()
