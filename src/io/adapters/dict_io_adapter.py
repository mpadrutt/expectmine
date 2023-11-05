from typing import Dict, Any

from src.io import BaseIo, BaseIoAdapter
from src.io.io import DictIo


class DictIoAdapter(BaseIoAdapter):
    """
    Adapter to DictIo which takes a dict of dicts as argument (namely a dict
    for each step) and creates instances with config values for each step instance.
    If configuration values exist for each step instance,
    it will create instances accordingly; otherwise, it will raise an error.
    """

    def __init__(self, answers: dict[str, dict[str, object]], **kwargs: Dict[Any, Any]):
        self.answers = answers
        self.kwargs = kwargs

    def get_instance(self, step_name: str, **kwargs: Dict[Any, Any]) -> "BaseIo":
        if step_name not in self.answers:
            raise ValueError("Step name not found in DictIoAdapter")

        step_dict = self.answers.get(step_name)

        if not isinstance(step_dict, dict):
            raise ValueError("Value associated with step_name is not a dict.")

        return DictIo(step_dict, **self.kwargs, **kwargs)
