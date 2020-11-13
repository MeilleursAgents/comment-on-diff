format:
	poetry run black *.py
	poetry run isort *.py

lint:
	poetry run black --check *.py
	poetry run mypy --ignore-missing-imports *.py
	poetry run flake8 main.py

test:
	poetry run pytest
