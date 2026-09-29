setup:
	uv sync

lint:
	uv run ruff check .
	uv run ruff format --check .

typecheck:
	uv run mypy src/

test:
	uv run pytest -m "not live"

test-compiler:
	uv run pytest -m compiler

schema:
	uv run codementor schema export --out schemas/

check: lint typecheck test

.PHONY: setup lint typecheck test test-compiler schema check
