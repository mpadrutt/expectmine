# Preprocessing pipeline
It is recommended to open the documentation in your 
browser. To open run:
- `start docs/build/html/index.html` on Windows
- `open docs/build/html/index.html` on macOS
- `xdg-open docs/build/html/index.html` on Linux

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

![[@docs/getting_started/commands.md]]

![[@docs/guides/repo_structure.md]]

![[@docs/getting_started/first_pipeline.md]]



