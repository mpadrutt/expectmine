from src.io import BaseIo, BaseIoAdapter
from src.io.io import CliIo


class CliIoAdapter(BaseIoAdapter):
    """
    CliIo adapter to produce CliIo instances.
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def get_instance(self, step_name: str, **kwargs) -> "BaseIo":
        return CliIo(**kwargs)
