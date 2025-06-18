# Makefile for dbt project management

# Variables
VENV_NAME = .venv
PYTHON = $(VENV_NAME)/bin/python
PIP = $(VENV_NAME)/bin/pip
PIP_COMPILE = $(VENV_NAME)/bin/pip-compile
PIP_SYNC = $(VENV_NAME)/bin/pip-sync

# Create venv if it doesn't exist
create:
	python3 -m venv $(VENV_NAME)
	$(PIP) install --upgrade pip
	$(PIP) install pip-tools

# Compile requirements.txt from requirements.in
compile:
	$(PIP_COMPILE) requirements.in

# Sync the virtual environment with requirements.txt
sync:
	$(PIP_SYNC) requirements.txt

# Shortcut for full environment setup
install: create compile sync

# Remove the environment
clean:
	rm -rf $(VENV_NAME)

# Recreate the environment from scratch using requirements.txt
rebuild: clean create sync

