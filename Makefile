PYTHON := python3
VENV := .venv

all: help

help:
	@echo "Makefile commands:"
	@echo "  make venv         # create virtualenv"
	@echo "  make install      # install package and dev dependencies"
	@echo "  make test         # run pytest"

$(VENV)/bin/activate:
	$(PYTHON) -m venv $(VENV)

venv: $(VENV)/bin/activate
	@echo "Virtualenv ready in $(VENV)"

install: venv
	$(VENV)/bin/pip install --upgrade pip setuptools wheel
	$(VENV)/bin/pip install -e .[dev]

test: install
	$(VENV)/bin/pytest -v
