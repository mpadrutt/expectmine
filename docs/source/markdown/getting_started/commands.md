# Commands

```{note}
As this step relies on Make, you either have to install [Make for Windows](https://gnuwin32.sourceforge.net/packages/make.htm)
or do the steps manually.
```

Every necessary step in the repo can be executed through a command in the 
Makefile. The commands can be grouped in the following groups:

## Project scripts
- `make deps`: Installs all necessary dependencies in the virtual environment.
- `make clean`: Removes the environment and pytest_cache.
- `make lint`: Lints the project using flake8 and pyright.
- `make format`: Formats code and imports using isort and black.
- `make test`: Runs tests and calculates test coverage using pytest.

## Code generation
- `make step`: Starts the workflow of creating a new step.
- `make readme`: Updates the `README.md` using the sphinx documentation.
- `make env-vars`: Generates an empty .env file with all necessary 
  environment variables.
- `make docs-html`: Generates the html documentation using .md and .rst files.

## Documentation
- `make docs-start`: Starts hot reloading of the sphinx documentation to 
  easily work on it.
- `make open-docs`: Opens the local documentation in the browser.