format:
	poetry run ruff format *.py
	poetry run ruff --fix *.py

lint:
	poetry run mypy --ignore-missing-imports *.py
	poetry run ruff main.py
	poetry run ruff format --check *.py

test:
	poetry run pytest
