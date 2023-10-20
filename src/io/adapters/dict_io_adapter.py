from .. import BaseIo, BaseIoAdapter
from ..io import DictIo


class DictIoAdapter(BaseIoAdapter):
    """
    Adapter to DictIo which takes a dict of dicts as argument (namely a dict
    for each step) and creates instances with config values for each step instance.
    If configuration values exist for each step instance,
    it will create instances accordingly; otherwise, it will raise an error.
    """

    def __init__(self, answers: dict[str, dict[str, object]], **kwargs):
        self.answers = answers
        self.kwargs = kwargs

    def get_instance(self, step_name: str, **kwargs) -> "BaseIo":
        if step_name not in self.answers:
            raise ValueError("Step name not found in DictIoAdapter")
        if not isinstance(self.answers.get(step_name), dict):
            raise ValueError("Value associated with step_name is not a dict.")

        return DictIo(self.answers.get(step_name), **self.kwargs, **kwargs)
