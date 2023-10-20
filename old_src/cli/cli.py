# from datetime import datetime
# import json
# import os
from pathlib import Path

from pipeline import build_pipeline as bp
from pipeline import run_pipeline as rp

# import typer
# from InquirerPy import inquirer
# from typing_extensions import Annotated
from pipeline.io.cli_io import CliIo

# from shutil import copy
# from typing import Optional
# from uuid import UUID, uuid4


# from steps import Input as InputStep
# from steps import steps


# all_steps = [step for step in steps]


# def get_possible_steps(input: list[str]):
#     return [step for step in all_steps if step.can_call(input)]


# def get_all_files_in_folder(folder: str):
#     return [
#         os.path.join(folder, file)
#         for file in os.listdir(folder)
#         if os.path.isfile(os.path.join(folder, file))
#     ]


# def build_pipeline(filepaths: list[str]):
#     pipeline = [InputStep().get_instance()]

#     TESTDATA = Path("testdata")

#     current_output = [file for file in TESTDATA.iterdir() if file.is_file()]

#     while True:
#         possible_steps = get_possible_steps(current_output)
#         if not possible_steps:
#             break

#         selected_step = inquirer.select(
#             message="Select a step",
#             choices=[step.name for step in possible_steps]
#             + ["Finish building pipeline"],
#             multiselect=False,
#         ).execute()

#         if selected_step == "Finish building pipeline":
#             break

#         step = [step for step in possible_steps if step.name == selected_step][0]

#         step = next((step for step in all_steps if step.name == selected_step), None)

#         current_output = step.output_type()

#         pipeline.append(step())

#         if step.requires_config():
#             config_path = inquirer.filepath(
#                 message="Enter config for this step",
#             ).execute()

#             pipeline[-1].set_config(config_path)

#     return pipeline


# def run_pipeline(pipeline, input: list[str], uuid: UUID):
#     output = input

#     OUTPUT_PATH = Path("output")

#     for i, step in enumerate(pipeline):
#         output_folder = f"./output/{uuid}/s{i}_{step.name}"
#         output_folder = OUTPUT_PATH / str(uuid) / f"s{i}_{step.name}"

#         os.makedirs(output_folder, exist_ok=True)
#         output_folder.mkdir(parents=True, exist_ok=True)

#         with open(output_folder / "metadata.json", "w") as file:
#             file.write(json.dumps(step.get_metadata(), indent=4))

#         if step.requires_config():
#             copy(step.config, f"{output_folder}/{step.config.split('/')[-1]}")

#         step.set_output_folder(output_folder)
#         output = step(output)


# def main():
#     uuid = uuid4()
#     date_string = str(datetime.now())
#     files = get_all_files_in_folder("./testdata")

#     selected_files = inquirer.select(
#         message="Select files",
#         choices=files,
#         multiselect=True,
#     ).execute()

#     pipeline = build_pipeline(selected_files)
#     run_pipeline(pipeline, selected_files, uuid)


def start_cli():
    # typer.run(main)
    pipeline = bp(CliIo())
    rp(pipeline, Path("generated"))
