PYTHON ?= python3
VENV := .venv
BIN := $(VENV)/bin
INSTALL_STAMP := $(VENV)/.installed
VENV_MARKER := $(VENV)/.project-root
PROJECT_ROOT := $(abspath .)
RESUME_GENERATOR := $(BIN)/resume-generator

.DEFAULT_GOAL := help

.PHONY: help setup html docx docx-no-pdf build docs test lint check

help:
	@printf "Resume generator commands:\n"
	@printf "  make setup       Create .venv and install the project\n"
	@printf "  make html        Build docs/index.html\n"
	@printf "  make docx        Build local DOCX/PDF files\n"
	@printf "  make docx-no-pdf Build local DOCX files only\n"
	@printf "  make build       Build HTML and local DOCX/PDF files\n"
	@printf "  make docs        Build pydoc API documentation\n"
	@printf "  make test        Run pytest\n"
	@printf "  make lint        Run ruff\n"
	@printf "  make check       Run tests and linting\n"

setup:
	@if [ -d "$(VENV)" ] && [ "$$(cat "$(VENV_MARKER)" 2>/dev/null)" != "$(PROJECT_ROOT)" ]; then \
		printf "Removing stale virtual environment for copied project path: $(VENV)\n"; \
		rm -rf "$(VENV)"; \
	fi
	@if [ ! -f "$(INSTALL_STAMP)" ] || [ pyproject.toml -nt "$(INSTALL_STAMP)" ] || [ Makefile -nt "$(INSTALL_STAMP)" ]; then \
		set -e; \
		$(PYTHON) -m venv "$(VENV)"; \
		"$(BIN)/python" -m pip install --upgrade pip; \
		"$(BIN)/python" -m pip install -e ".[dev]"; \
		printf "%s\n" "$(PROJECT_ROOT)" > "$(VENV_MARKER)"; \
		touch "$(INSTALL_STAMP)"; \
	fi

html: setup
	$(RESUME_GENERATOR) --format html

docx: setup
	$(RESUME_GENERATOR) --format docx

docx-no-pdf: setup
	$(RESUME_GENERATOR) --format docx --no-pdf

build: setup
	$(RESUME_GENERATOR)

docs: setup
	$(BIN)/python scripts/build_api_docs.py

test: setup
	$(BIN)/pytest

lint: setup
	$(BIN)/ruff check .

check: test lint
