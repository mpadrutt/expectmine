# Expectmine pipeline

It is recommended to visit the [documentation](https://mpadrutt.github.io/expectmine/)

## Project setup

To get started, we first create a virtual environment and install the
necessary dependencies. We can then use the makefile commands to navigate in
the project.

### Linux or macOS

```bash
python -m venv env
source env/bin/activate
make deps
make env-vars
```

### Windows

```bat
python -m venv env
.\env\Scripts\activate
make deps
make env-vars
```

## Commands

```{note}
As this step relies on Make, you either have to install [Make for Windows](https://gnuwin32.sourceforge.net/packages/make.htm)
or do the steps manually.
```

Every necessary step in the repo can be executed through a command in the 
Makefile. The commands can be grouped in the following groups:

### Project scripts
- `make deps`: Installs all necessary dependencies in the virtual environment.
- `make clean`: Removes the environment and pytest_cache.
- `make lint`: Lints the project using flake8 and pyright.
- `make format`: Formats code and imports using isort and black.
- `make test`: Runs tests and calculates test coverage using pytest.

### Code generation
- `make step`: Starts the workflow of creating a new step.
- `make readme`: Updates the `README.md` using the sphinx documentation.
- `make env-vars`: Generates an empty .env file with all necessary 
  environment variables.
- `make docs-html`: Generates the html documentation using .md and .rst files.

### Documentation
- `make docs-start`: Starts hot reloading of the sphinx documentation to 
  easily work on it.
- `make open-docs`: Opens the local documentation in the browser.
## Repo structure

The repository is divided into the following parts:
- `docs/` Contains the sphinx documentation
  - `build/` Contains the html output of the generated documentation
  - `source/` Used to build the documentation
- `scripts/` Contains all scripts used for code generation
- `src/` Contains the entire pipeline
  - `io/` All Io logic, concerned with getting user input to the pipeline and 
    steps.
  - `logger/` Contains all loggers
  - `pipeline/` Contains the pipeline code
  - `steps/` Contains all steps used by the pipeline
  - `storage/` Contains all storage logic
  - `utils/` Util functions used by all modules
- `tests/` Used for testing
- `Makefile` Used for running commands
- `pyproject.toml` Configures pyright isort and flake8
- `README.md` Auto generated readme
- `requirements.txt` Requirements used by the project
## Your first pipeline

### Initializing a simple pipeline
Creating a pipeline to execute in python directly is super easy, just import 
the `get_quickstart_config` method and initialize a pipeline directly from it.


```python
from pathlib import Path

from src.pipeline.pipeline import Pipeline
from src.pipeline.utils import get_quickstart_config

pipeline = Pipeline(*get_quickstart_config(output_path=Path("pipeline_output")))
```

### Adding input files
To add input files to the pipeline, just give it an array of paths to the 
individual files. The files you provide will serve as input to the first step.

```python
pipeline.set_input([Path('file1.mzml')])
```

### Adding steps
To add a step, just provide the type of step you want to add and an io 
object, which is used to configure the step.

```python
pipeline.add_step(
    MZmine3,
    {
        "mzmine3_path": Path(
            "/Applications/MZmine.app/Contents/MacOS/MZmine", absolute=True
        ),
        "batchfile": Path("batchfile.xml"),
    }
)
```

### Run the pipeline
After calling run the pipeline will then run and output files for each step 
in the directory you provided as `output_path`.

```python
pipeline.run()
```

### Summary
```python
from pathlib import Path

from src.pipeline.pipeline import Pipeline
from src.pipeline.utils import get_quickstart_config
from src.steps.steps import SiriusFingerprint
from src.steps.steps.mzmine3.mzmine3 import MZmine3

pipeline = Pipeline(*get_quickstart_config(output_path=Path("pipeline_output")))

pipeline.set_input([Path("file1.mzml"), Path("file2.mzml")])

pipeline.add_step(
    MZmine3,
    {
        "mzmine3_path": Path(
            "/Applications/MZmine.app/Contents/MacOS/MZmine", absolute=True
        ),
        "batchfile": Path("batchfile.xml"),
    }
)

pipeline.add_step(
    SiriusFingerprint,
    {
        "sirius_path": Path(
            "/Applications/sirius.app/Contents/MacOS/sirius", absolute=True
        ),
        "set_max_mz": False,
        "instrument": "orbitrap",
    }
)

pipeline.run()
```
