PYTHON ?= python3
VENV := .venv
BIN := $(VENV)/bin
INSTALL_STAMP := $(VENV)/.installed
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

setup: $(INSTALL_STAMP)

$(INSTALL_STAMP): pyproject.toml
	$(PYTHON) -m venv $(VENV)
	$(BIN)/python -m pip install --upgrade pip
	$(BIN)/python -m pip install -e ".[dev]"
	touch $(INSTALL_STAMP)

html: $(INSTALL_STAMP)
	$(RESUME_GENERATOR) --format html

docx: $(INSTALL_STAMP)
	$(RESUME_GENERATOR) --format docx

docx-no-pdf: $(INSTALL_STAMP)
	$(RESUME_GENERATOR) --format docx --no-pdf

build: $(INSTALL_STAMP)
	$(RESUME_GENERATOR)

docs: $(INSTALL_STAMP)
	$(BIN)/python scripts/build_api_docs.py

test: $(INSTALL_STAMP)
	$(BIN)/pytest

lint: $(INSTALL_STAMP)
	$(BIN)/ruff check .

check: test lint
