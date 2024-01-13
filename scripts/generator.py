from pathlib import Path
import os

from inflection import camelize, underscore
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator, PathValidator
from jinja2 import Environment, FileSystemLoader


ROOT_PATH = Path(".")
IO_PATH = Path("./expectmine/io")
LOGGER_PATH = Path("./expectmine/logger")
PIPELINE_PATH = Path("./expectmine/pipeline")
STEPS_PATH = Path("./expectmine/steps")
STORAGE_PATH = Path("./expectmine/storage")

TEMPLATES_PATH = Path("./scripts/templates")


# initialize jinja environment
environment = Environment(loader=FileSystemLoader(TEMPLATES_PATH), trim_blocks=True)
environment.globals["camelize"] = camelize
environment.globals["underscore"] = underscore


def generate_step():
    """
    Generates an empty step in steps/steps. Used as a good starting point as
    the generated file contains todos with information about what needs to be
    done to get the step running.
    """
    step_name = inquirer.text(
        message="Enter the name of the step:",
        validate=EmptyInputValidator("Input should not be empty."),
    ).execute()

    step_path = inquirer.filepath(
        message="Where do you want to create the step?",
        validate=PathValidator("Input should be a valid directory.", is_dir=True),
    ).execute()

    step_template = environment.get_template("step.tmpl")

    generated_code = step_template.render(step_name=step_name)

    with open(Path(step_path) / f"{underscore(step_name)}.py", "w") as handle:
        handle.write(generated_code)


def generate_env():
    """
    Generates an empty environment template. If the .env file already exists
    moves the current .env file to old.env.
    """
    env_template = environment.get_template(".env.tmpl")

    generated_code = env_template.render()

    if (ROOT_PATH / ".env").exists():
        os.rename(ROOT_PATH / ".env", ROOT_PATH / "old.env")
        print("Renamed existing .env file to old.env")

    with open(ROOT_PATH / ".env", "w") as handle:
        handle.write(generated_code)
