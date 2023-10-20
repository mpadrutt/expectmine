## 👋 Quick Start

After cloning into this repository, set up a venv environment and install the python requirements using the following commands (on Windows, the commands to initialize the venv environment might look slightly different):

```
python3.10 -m venv env
source env/bin/activate
make init
```

## 📁 Repo structure

This repo is divided into three distinct folders that have their own README and their own set of commands:

- `scripts`: contains all necessary codegen scripts to generate new pipeline steps.
- `src/cli`: contains the CLI code.
- `src/steps`: contains all pipeline steps.
- `src/utils`: contains utility functions.
