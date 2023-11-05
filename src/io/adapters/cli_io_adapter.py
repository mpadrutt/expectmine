from typing import Dict, Any

from src.io import BaseIo, BaseIoAdapter
from src.io.io import CliIo


class CliIoAdapter(BaseIoAdapter):
    """
    CliIo adapter to produce CliIo instances.
    """

    def __init__(self, **kwargs: Dict[Any, Any]):
        self.kwargs = kwargs

    def get_instance(self, step_name: str, **kwargs: Dict[Any, Any]) -> "BaseIo":
        return CliIo(**kwargs)
