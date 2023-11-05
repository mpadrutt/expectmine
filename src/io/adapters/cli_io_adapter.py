from typing import Any, Dict

from src.io.base_io import BaseIo
from src.io.base_io_adapter import BaseIoAdapter
from src.io.io.cli_io import CliIo


class CliIoAdapter(BaseIoAdapter):
    """
    CliIo adapter to produce CliIo instances.
    """

    def __init__(self, **kwargs: Dict[Any, Any]):
        self.kwargs = kwargs

    def get_instance(self, step_name: str, **kwargs: Dict[Any, Any]) -> "BaseIo":
        return CliIo(**kwargs)
