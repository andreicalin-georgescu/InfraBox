# Makefile

.PHONY: help setup format lint security pre-commit-all

# Show help for each target
help:
	@echo ""
	@echo "InfraBox Makefile Commands:"
	@echo "---------------------------"
	@echo "setup           Install Python tools and Git pre-commit hooks"
	@echo "format          Format code using Black"
	@echo "lint            Run static code analysis using Ruff"
	@echo "security        Scan for security issues using Bandit"
	@echo "check           Run format, lint, and security checks (all-in-one)"
	@echo "pre-commit-all  Run all configured pre-commit hooks across the codebase"
	@echo ""

# Setup Python tools and Git pre-commit hooks
setup:
	pip3 install --upgrade pip
	pip3 install -r requirements.txt
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
