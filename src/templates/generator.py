from pathlib import Path

from inflection import camelize, underscore
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
from jinja2 import Environment, FileSystemLoader

IO_PATH = Path("../io")
LOGGER_PATH = Path("../logger")
PIPELINE_PATH = Path("../pipeline")
STEPS_PATH = Path("../steps")
STORAGE_PATH = Path("../storage")
TEMPLATES_PATH = Path()


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
