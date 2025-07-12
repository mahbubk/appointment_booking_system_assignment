# Makefile for automating Django Rest Framework tasks
# pytest --cov=utils
# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
MANAGE := $(PYTHON) manage.py

# Create a virtual environment (venv) if it doesn't exist and install project dependencies.
# If a dev_requirements.txt file exists, it installs the dependencies specified in it.
# Otherwise, it installs common dependencies used for Django Rest Framework projects.
.PHONY: venv
venv:
	@if [ ! -d "venv" ]; then \
		virtualenv venv; \
	fi
	@echo "Activating virtual environment..."
	@. venv/bin/activate; \
	if [ -f "dev_requirements.txt" ]; then \
		$(PIP) install -r requirements.txt; \
	else \
		$(PIP) install djangorestframework markdown django-filter; \
	fi

# Install project dependencies from dev_requirements.txt
.PHONY: requirements
requirements:
	@if [ -f "requirements.txt" ]; then \
		$(PIP) install -r requirements.txt; \
	else \
		echo "Error: requirements.txt not found."; \
	fi

# Apply database migrations
.PHONY: migrate
migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

# Run tests using pytest
# Check test coverage for specific directory
# pytest --cov=utils
.PHONY: pytest
pytest:
	pytest

# Run py tests coverage index
.PHONY: cov
cov:
	 pytest --cov

# Run py tests coverage index
.PHONY: cov_report
cov_report:
	coverage report

# Run py tests coverage index
.PHONY: cov_index
cov_index:
	coverage html && open htmlcov/index.html

# Format the Python code using black
.PHONY: format
format:
	isort .
	black .

# Run the flake8 linter to check for code style and potential errors
.PHONY: flake8
flake8:
	flake8 .

# Run the flake8 linter to check for code style and potential errors
.PHONY: accuracy
accuracy:
	python ./auth_app/management/commands/coding-accuracy.py

# Run the main.py script of the package
.PHONY: run
run:
	$(PYTHON) ./current/mypackage/main.py

# Run the Django development server
.PHONY: runserver
runserver:
	$(MANAGE) runserver

# Build the Python package distribution using setup.py
.PHONY: build
build:
	python ./current/setup.py build bdist_wheel

# Clean up temporary and generated files
.PHONY: clean
clean:
	rm -rf ./test_project/__pycache__
	rm -rf ./dist
	rm -rf ./htmlcov
	rm -rf ./build
	rm -rf ./test.egg-info
	rm -rf ./.pytest_cache
	# find . -name "*.pyc" -exec rm -f {} \;

.PHONY: all
all: venv migrate runserver

# Run pre-commit checks on all files
.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files
