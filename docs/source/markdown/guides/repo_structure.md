# Repo structure

The repository is divided into the following parts:
- `docs/` Contains the sphinx documentation
  - `build/` Contains the html output of the generated documentation
  - `source/` Used to build the documentation
- `scripts/` Contains all scripts used for code generation
- `expectmine/` Contains the entire pipeline
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
