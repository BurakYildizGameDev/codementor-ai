setup:
	uv sync

lint:
	uv run ruff check .
	uv run ruff format --check .

typecheck:
	uv run mypy src/

test:
	uv run pytest -m "not live"

roslyn-check:
	dotnet build tools/roslyn-check -c Release -o tools/roslyn-check/out

test-compiler:
	uv run pytest -m compiler

schema:
	uv run codementor schema export --out schemas/

check: lint typecheck test

.PHONY: setup lint typecheck test roslyn-check test-compiler schema check
