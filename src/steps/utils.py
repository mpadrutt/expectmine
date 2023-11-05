import inspect
from typing import Type

from src.steps import steps

from src.steps.base_step import BaseStep


def get_registered_steps() -> list[tuple[str, Type[BaseStep]]]:
    """
    Validates the adapter init parameters.

    :returns: A list of tuples of all registered steps in src.steps.steps
    :rtype: list[tuple[str, BaseStep]]
    """
    members = inspect.getmembers(steps)

    return [member for member in members if inspect.isclass(member[1])]
