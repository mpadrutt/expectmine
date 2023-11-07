from pathlib import Path
import os

from inflection import camelize, underscore
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
from jinja2 import Environment, FileSystemLoader

os.chdir("./scripts")

ROOT_PATH = Path("..")
IO_PATH = Path("../src/io")
LOGGER_PATH = Path("../src/logger")
PIPELINE_PATH = Path("../src/pipeline")
STEPS_PATH = Path("../src/steps")
STORAGE_PATH = Path("../src/storage")

TEMPLATES_PATH = Path("templates")


def custom_camelize(string: str):
    return camelize("".join(map(lambda x: x.capitalize(), string.split("-"))))


# initialize jinja environment
environment = Environment(loader=FileSystemLoader(TEMPLATES_PATH), trim_blocks=True)
environment.globals["camelize"] = custom_camelize
environment.globals["underscore"] = underscore


def generate_step():
    """
    Generates an empty step in steps/steps. Used as a good starting point as
    the generated file contains todos with information about what needs to be
    done to get the step running.
    """
    step_name = inquirer.text(
        message="Enter the name of the step",
        validate=EmptyInputValidator("Input should not be empty"),
    ).execute()

    step_template = environment.get_template("step.tmpl")

    generated_code = step_template.render(step_name=step_name)

    with open(STEPS_PATH / "steps" / f"{underscore(step_name)}.py", "w") as handle:
        handle.write(generated_code)


def generate_env():
    env_template = environment.get_template(".env.tmpl")

    generated_code = env_template.render()

    if (ROOT_PATH / ".env").exists():
        os.rename(ROOT_PATH / ".env", ROOT_PATH / "old.env")
        print("Renamed existing .env file to old.env")

    with open(ROOT_PATH / ".env", "w") as handle:
        handle.write(generated_code)
