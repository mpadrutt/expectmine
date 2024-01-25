from pathlib import Path
import os

from inflection import camelize, underscore
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
    Generates an empty step. Used as a good starting point as
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
    Generates an empty small step. Used as a good starting point as
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

    step_template = environment.get_template("small_step.tmpl")

    generated_code = step_template.render(step_name=step_name)

    with open(Path(step_path) / f"{underscore(step_name)}.py", "w") as handle:
        handle.write(generated_code)


def generate_pipeline():
    """
    Generates a example pipeline.
    """
    while True:
        pipeline_file_name = inquirer.text(
            message="How should the generated file be called?",
            validate=EmptyInputValidator("Input should not be empty."),
        ).execute()

        pipeline_path = inquirer.filepath(
            message="Where do you want to create the pipeline?",
            validate=PathValidator("Input should be a valid directory.", is_dir=True),
        ).execute()

        file_name_with_extension = (
            f"{pipeline_file_name}.py"
            if not pipeline_file_name.endswith(".py")
            else pipeline_file_name
        )

        file_path = Path(pipeline_path) / file_name_with_extension

        if not file_path.exists():
            break
        else:
            print(
                f"The file '{file_path}' already exists. Please choose a different name."
            )

    pipeline_template = environment.get_template("pipeline.tmpl")
    generated_code = pipeline_template.render()

    with open(file_path, "w") as handle:
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
            "Starter Pipeline",
            "Env File",
        ],
        default=None,
    ).execute()

    if action == "Regular Step":
        generate_step()

    elif action == "Small Step":
        generate_small_step()

    elif action == "Starter Pipeline":
        generate_pipeline()

    elif action == "Env File":
        generate_env()
