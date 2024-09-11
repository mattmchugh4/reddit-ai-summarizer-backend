# Makefile for a Python project

# Define the lint target
lint:
	@echo "Running isort, black, and flake8..."
	isort .  # Organize imports
	black .  # Format code
	flake8 . # Lint code

# Define additional targets here, e.g., for testing, formatting, etc.
# test:
#	pytest

# clean:
#	rm -rf __pycache__ *.pyc *.pyo