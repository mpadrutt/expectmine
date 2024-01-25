from pathlib import Path
import os

from inflection import camelize, underscore, sna
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator, PathValidator
from jinja2 import Environment, FileSystemLoader

script_path = Path(__file__).resolve().parent

TEMPLATES_PATH = script_path / "templates"

CURRENT_WORKING_DIRECTORY = Path.cwd()


def new_camelize(string: str):
    return camelize(underscore(string))


# initialize jinja environment
environment = Environment(loader=FileSystemLoader(TEMPLATES_PATH), trim_blocks=True)
environment.globals["camelize"] = new_camelize
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


def generate_small_step():
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

    if (CURRENT_WORKING_DIRECTORY / ".env").exists():
        os.rename(
            CURRENT_WORKING_DIRECTORY / ".env", CURRENT_WORKING_DIRECTORY / "old.env"
        )
        print("Renamed existing .env file to old.env")

    with open(CURRENT_WORKING_DIRECTORY / ".env", "w") as handle:
        handle.write(generated_code)


def create():
    action = inquirer.select(
        message="Select an action:",
        choices=[
            "Regular Step",
            "Small Step",
            "Env File",
        ],
        default=None,
    ).execute()

    if action == "Regular Step":
        generate_step()

    elif action == "Small Step":
        generate_small_step()

    elif action == "Env File":
        generate_env()
