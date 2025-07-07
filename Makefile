# Makefile

.PHONY: setup format lint security pre-commit-all

# Setup Python tools and Git pre-commit hooks
setup:
	pip3 install --upgrade pip
	pip3 install -r requirements.txt
	pip3 install pre-commit
	python3 -m pre_commit install

# Format code using Black
format:
	python3 -m black infrabox.py cli/

# Run lint checks
lint:
	python3 -m ruff check infrabox.py cli/ --show-files --fix

# Run security scan
security:
	python3 -m bandit -r infrabox.py cli/

# Run full check
check: format lint security

# Run all pre-commit hooks against the entire codebase
pre-commit-all:
	python3 -m pre_commit run --all-files
