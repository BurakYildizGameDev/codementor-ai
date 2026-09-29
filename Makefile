setup:
	uv sync

lint:
	uv run ruff check .
	uv run ruff format --check .

typecheck:
	uv run mypy src/

test:
	uv run pytest -m "not live and not sandbox"

test-sandbox:
	uv run pytest -m sandbox

schema:
	uv run codementor schema export --out schemas/

check: lint typecheck test

.PHONY: setup lint typecheck test test-sandbox schema check
