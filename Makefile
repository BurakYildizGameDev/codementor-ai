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

# Faz 29: dotnet gerektirmeyen tek dosya (trimmed, ~15 MB); exe paketine gömülür
roslyn-check-sc:
	dotnet publish tools/roslyn-check -c Release --use-current-runtime --self-contained true -p:PublishSingleFile=true -p:PublishTrimmed=true -o tools/roslyn-check/sc

test-compiler:
	uv run pytest -m compiler

schema:
	uv run codementor schema export --out schemas/

rules-doc:
	uv run codementor rules doc --out docs/rules-catalog.md

serve:
	uv run codementor serve

# Web UI (Faz 13): tipler schemas/'tan üretilir, elle yazılmaz
web-install:
	cd web && npm install

web-types: schema
	cd web && npm run gen:types

web:
	cd web && npm run dev

web-test:
	cd web && npm run typecheck && npm test && npm run build

web-e2e:
	cd web && npx playwright install chromium && npm run e2e

# Masaüstü uygulaması (Faz 14, ADR-0013)
desktop:
	uv run python -m codementor.desktop

desktop-assets:
	uv run python tools/make_desktop_assets.py

exe:
	uv run python build_exe.py --both

check: lint typecheck test

.PHONY: setup lint typecheck test roslyn-check roslyn-check-sc test-compiler schema rules-doc check serve web-install web-types web web-test web-e2e desktop desktop-assets exe
