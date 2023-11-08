from pathlib import Path

from src.steps.base_step import BaseStep

from src.io.base_io import BaseIo
from src.logger.base_logger import BaseLogger
from src.storage.base_storage import BaseStore


class ExampleStep(BaseStep):
    """
    This step generates a single output file (input.txt) containing all
    absolute paths of input files provided to this step.
    """

    @classmethod
    def step_name(cls) -> str:
        return "ExampleStep"

    @classmethod
    def can_run(cls, input_files: list[str]) -> bool:
        # We return true as this step can run on any kind of files.
        return True

    @classmethod
    def output_filetypes(cls, input_files: list[str]) -> list[str]:
        # We just return '.txt' as the only file returned from our step has this type.
        return [".txt"]

    def install(self, persistent_store: BaseStore, io: BaseIo, logger: BaseLogger):
        # Nothing to do here, here you would normally register executable paths or similar.
        logger.log("Nothing to do here as we do not have any external executables.")

    def setup(self, volatile_store: BaseStore, io: BaseIo, logger: BaseLogger):
        logger.log("Asking the user for his secret message with key 'message'")

        # Asking the user to ender a string using the io class.
        message = io.string("message", "Enter the secret message:")
        logger.log(f"Message entered was: {message}")

        # Adding the value to the key-value store.
        volatile_store.put("secret_message", message)

    def run(
        self,
        input_files: list[Path],
        output_path: Path,
        persistent_store: BaseStore,
        volatile_store: BaseStore,
        logger: BaseLogger,
    ) -> list[Path]:
        # We get the absolute path for every input_file to the step
        lines = [str(file.absolute()) for file in input_files]

        # We get the message back from the store NOTE: The value can be None!
        secret_message = volatile_store.get("secret_message", str)

        if not secret_message:
            logger.error("No secret message was found during execution.")
        else:
            lines.append(secret_message)

        with open(output_path / "input.txt", "w") as output_file:
            output_file.writelines(lines)

        # Return the path to our output back to the caller such that the next
        # step knows where to access the previous data.
        return [output_path / "input.txt"]

    def metadata(
        self, persistent_store: BaseStore, volatile_store: BaseStore
    ) -> dict[str, object]:
        # Return a dict of metadata that belongs to the step such as version numbers.
        return {
            "secret_number": 42,
        }

    @classmethod
    def citation_and_disclaimer(cls) -> str:
        # Add your relevant citation or disclaimer here for other users to see.
        return """When using this step, please cite noone.
        """
