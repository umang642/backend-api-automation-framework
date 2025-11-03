.PHONY: install test test-smoke run-mock lint format

install:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

test:
	pytest -q

test-smoke:
	pytest -m smoke -q

run-mock:
	uvicorn mock.server:app --reload --port 8000

lint:
	ruff check .

format:
	black . && isort .
