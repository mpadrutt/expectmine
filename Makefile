# System python interpreter. Used only to create virtual environment
PY = python3
VENV = env
BIN = $(VENV)/bin
OPEN_BROWSER = open

# Make it work on Windows too
ifeq ($(OS),Windows_NT)
	BIN = $(VENV)/Scripts
	PY = python
	OPEN_BROWSER = start
endif

ifeq ($(OS), Linux)
	OPEN_BROWSER = xdg-open
endif

# Check if venv does not exist and call deps if needed
$(VENV):
	@if [ ! -d "$(VENV)" ]; then \
		$(MAKE) deps; \
	fi

deps: requirements.txt
	$(PY) -m venv $(VENV)
	$(BIN)/pip install --upgrade -r requirements.txt

.PHONY: test
test: $(VENV)
	cd tests && ../$(BIN)/pytest -rA --cov=src .

.PHONY: lint
lint: $(VENV)
	$(BIN)/flake8 src
	$(BIN)/pyright src

.PHONY: format
format: $(VENV)
	$(BIN)/isort src
	$(BIN)/black src

.PHONY: clean
clean:
	rm -rf env
	rm -rf .pytest_cache

# Code generation
.PHONY: step
step: $(VENV)
	$(BIN)/python -c "from scripts.generator import generate_step; generate_step()"

.PHONY: env-vars
env-vars: $(VENV)
	$(BIN)/python -c "from scripts.generator import generate_env; generate_env()"

readme: $(VENV)
	$(BIN)/python -c "from scripts.markdown import process_markdown; process_markdown()"

docs-html: $(VENV)
	$(BIN)/sphinx-build -M html docs/source docs/build

.PHONY: docs-start
docs-start: $(VENV)
	$(BIN)/sphinx-autobuild docs/source docs/build

.PHONY: open-docs
open-docs:
	$(OPEN_BROWSER) docs/build/html/index.html