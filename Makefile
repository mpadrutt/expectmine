# System python interpreter. Used only to create virtual environment
PY = python3
VENV = env
BIN = $(VENV)/bin

# Make it work on Windows too
ifeq ($(OS),Windows_NT)
	BIN = $(VENV)/Scripts
	PY = python
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
	$(BIN)/pytest -rA --cov=src/storage/persistent tests/

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
step: $(VENV)
	cd src/templates && python -c "from generator import generate_step; generate_step()"