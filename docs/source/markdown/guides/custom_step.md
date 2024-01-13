# How to write a custom step

In this example we write a custom step for the following function:

> For all input files, generate a single input.txt where each line contains
> the absolute path of one input file. At the last line, output the secret
> message provided to the step when configuring it.

This example is rather simple, but it highlights all necessary steps to
create any kind of step.

## 1. Generating the step

For this, we can use the `make step` command from our Makefile.

```bash
(env) ➜  expectmine git:(main) ✗ make step
env/bin/python -c "from scripts.generator import generate_step; generate_step()"
? Enter the name of the step: ExampleStep
? Where do you want to create the step? .
```

After answering the questions of the CLI, our new step `example_step.py` is
generated at the root of the project.

## 2. Fill in the blanks

```{note}
This does not serve as an in depth explanation of the lifecycle of each step,
to get a more in-depth look at a Step, please consider looking into the
"Concepts" part of the documentation.
```

Now, we can inspect the file and fill out every `TODO:` in it. **Before**
shows you the automatically generated code by `make step`, while **After**
shows the filled out code which solves the previously stated task.

::::{tab-set}

:::{tab-item} After

```python
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

```

:::

:::{tab-item} Before

```python
from pathlib import Path

from src.steps.base_step import BaseStep

from src.io.base_io import BaseIo
from src.logger.base_logger import BaseLogger
from src.storage.base_storage import BaseStore


class ExampleStep(BaseStep):
    """
    TODO: Write a good description about what the step does.
    """

    @classmethod
    def step_name(cls) -> str:
        return "ExampleStep"

    @classmethod
    def can_run(cls, input_files: list[str]) -> bool:
        """
        TODO:   Given a list of input files (or file endings), indicate
                if your step can run these files.
        """
        raise NotImplementedError

    @classmethod
    def output_filetypes(cls, input_files: list[str]) -> list[str]:
        """
        TODO:   Given a list of input files (or file endings), indicate
                what type of output files your step creates.
        """
        raise NotImplementedError

    def install(self, persistent_store: BaseStore, io: BaseIo, logger: BaseLogger):
        """
        TODO:   Check if all the necessary parameters are already available in
                the (persistent_store) if not set them up correctly. You can use
                (io) to interact with the user and use (logger) to log important
                messages.
        """
        raise NotImplementedError

    def setup(self, volatile_store: BaseStore, io: BaseIo, logger: BaseLogger):
        """
        TODO:   Check if all the necessary parameters for a specific run of your
                step are set in (volatile_store) if not set them up correctly. You
                can use (io) to interact with the user and (logger) to log
                important messages.
        """
        raise NotImplementedError

    def run(
        self,
        input_files: list[Path],
        output_path: Path,
        persistent_store: BaseStore,
        volatile_store: BaseStore,
        logger: BaseLogger,
    ) -> list[Path]:
        """
        TODO:   With the previously set stores (persistent_store, volatile_store) run
                run your step now on the (input_files). You should write your output
                to the output_path. If necessary you can use the (logger) to log
                important messages.
        """
        raise NotImplementedError

    def metadata(
        self, persistent_store: BaseStore, volatile_store: BaseStore
    ) -> dict[str, object]:
        """
        TODO:   Return all relevant metadata from the step back to the pipeline.
                This can help reproducibility and make your execution more
                transparent. For this you can access both stores
                (persistent_store, volatile_store).
        """
        raise NotImplementedError

    @classmethod
    def citation_and_disclaimer(cls) -> str:
        """
        TODO:   Write all necessary disclaimers and citation requirements in here.
                They will be presented on each execution of the step and
                additionally exported with the output files.
        """
        raise NotImplementedError
```

:::

::::

## 3. Using the step

To use the step we now have three possible options depending on where the step
should be used:

### Option 1: Quickly add to pipeline.

If you want to quickly import the step and use it in your existing pipeline
you can just import it and add it similarly to how you would import an other
step:

```python
from pathlib import Path

from src.pipeline.pipeline import Pipeline
from src.pipeline.utils import get_quickstart_config
from example_step import ExampleStep

pipeline = Pipeline(*get_quickstart_config(output_path=Path(f"output")))

pipeline.set_input([Path("testdata/1.mzML"), Path("testdata/2.mzML")])

# We add the new step here, with the value required in "Setup"
pipeline.add_step(ExampleStep, {"message": "Hello world"})

pipeline.run()
```

### Option 2: Make the step available to the CLI or GUI

If you use a managed workflow of the pipeline, you might want to register
the step such that it gets returned by `pipeline.get_registered_steps()`.

To do this, the process is even easier:

```python
from pathlib import Path

from src.pipeline.pipeline import Pipeline
from src.pipeline.utils import get_quickstart_config
from example_step import ExampleStep

pipeline = Pipeline(*get_quickstart_config(output_path=Path(f"output")))

pipeline.register_step(ExampleStep)
```

### Option 3: Save the step as a default step

For this, you just need to move your generated step to `src/steps/steps` and
include the step in `src/steps/steps/__init__.py`, the step then gets
automatically registered to the pipeline.
