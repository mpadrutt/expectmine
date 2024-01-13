from typing import Any, Dict

from expectmine.io.base_io import BaseIo
from expectmine.io.base_io_adapter import BaseIoAdapter
from expectmine.io.io.cli_io import CliIo


class CliIoAdapter(BaseIoAdapter):
    """
    CliIo adapter to produce CliIo instances.
    """

    def __init__(self, **kwargs: Dict[Any, Any]):
        self.kwargs = kwargs

    def get_instance(self, step_name: str, **kwargs: Dict[Any, Any]) -> "BaseIo":
        return CliIo(**kwargs)
