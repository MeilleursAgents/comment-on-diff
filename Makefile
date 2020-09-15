format:
	poetry run black main.py
	poetry run isort main.py

lint:
	poetry run black --check main.py
	poetry run mypy --ignore-missing-imports main.py
	poetry run flake8 .

test:
	poetry run pytest
