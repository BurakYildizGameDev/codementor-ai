# Yapılanlar

Fazlara göre tamamlanan işlerin özeti. Ayrıntılı kararlar ve açık sorular: [PROGRESS.md](PROGRESS.md).

---

## Faz 0 — Repo İskeleti ve Araç Zinciri ✅

**Dal:** `faz/0-iskelet` · **Commit:** `8e642c3 chore(faz-0): proje iskeleti, araç zinciri ve CI`

- **Proje yapılandırması:** `pyproject.toml` (uv, hatchling), Python 3.12, `uv.lock`.
- **Araç zinciri:** ruff (lint + format), mypy `--strict` (pydantic eklentisi), pytest işaretleri `live` / `sandbox` / `slow`.
- **Yapılandırma (`config.py`):** pydantic-settings; öncelik CLI > ortam değişkeni > `codementor.toml` > varsayılan. TOML yolu `CODEMENTOR_CONFIG_FILE` ile değiştirilebilir.
- **CLI:** `codementor --version`.
- **Makefile:** `setup`, `lint`, `typecheck`, `test`, `test-sandbox`, `schema`, `check`.
- **CI:** `.github/workflows/ci.yml`.
- **Ajan dosyaları:** `AGENTS.md`, `CLAUDE.md`, `.claude/` (izinler, format hook'u, `/faz` komutu, `kod-denetci` alt ajanı), `.agents/` (Antigravity kuralı, iş akışı, denetim becerisi).
- **Dokümanlar:** `docs/mimari.md`, `docs/UYGULAMA_PLANI.md`, `PROGRESS.md`.
- **Testler:** `test_config.py`, `test_smoke.py`.

---

## Faz 1 — Veri Modelleri ve Big-O Ayrıştırıcı ✅

**Dal:** `faz/1-modeller` · **Mimari:** §6, §5.6, §5.3.1

### Veri modelleri (`src/codementor/models/`)
| Dosya | İçerik |
|---|---|
| `_base.py` | `StrictModel` — bilinmeyen alanları reddeder (`extra="forbid"`) |
| `enums.py` | §6.2 enum'ları + `PipelineMode`, `LoopBound`, `AllocationKind`, `DeallocationKind` |
| `llm_output.py` | `LLMFinding`, `LLMComplexity`, `LLMAnalysisOutput`, `LLMSocraticOutput` (§6.3) |
| `findings.py` | `Diagnostic`, `CompilationBlock`, `Finding` |
| `report.py` | `ComplexityResult`, `SocraticResult`, `ReportMeta`, `AnalysisReport` (§6.4) |
| `request.py` | `AnalysisRequest`, `AnalysisOptions` (§9 istek örneği) |
| `facts.py` | §5.3.1 olguları (`FunctionFact`, `LoopFact`, `RecursionFact`, `CallFact`, `AllocationFact`, `DeallocationFact`, `EngineSymbols`, `CodeFacts`) + `ComplexityHint` |
| `schemas.py` | JSON Schema üretimi |

- LLM şemaları ile rapor şeması ayrı modüllerde (§6.1); LLM şemalarında sistem alanı yok.
- Tüm şemalarda `additionalProperties: false`.

### Big-O ayrıştırıcı (`models/bigo.py`, `_bigo_algebra.py`, `_bigo_parser.py`)
- Regex yığını yerine tokenizer + özyinelemeli ayrıştırıcı.
- `parse_bigo(str) -> BigO`; `BigO.canonical` (`n^2`), `BigO.display` (`O(n²)`), `same_class()`, `<`, `<=`, `>`, `>=`.
- Desteklenen yazımlar: `O(...)`, büyük/küçük harf, üst simgeler (`²`, `¹⁰`, `ⁿ`), `* · × ⋅` ve bitişik çarpım (`nlogn`), `log` / `lg` / `ln`, log tabanları (`log2`, `log_2`, `log₂`), `log^k n`, `sqrt`, kesirli üs, `c^n`, `n!`, sabite bölme, toplam.
- Sabit katsayılar ve baskılanan terimler atılır (`O(3n^2 + n)` → `n^2`).
- Tek değişkenli ifadelerde toplam sıralama; çok değişkenlide `BigOComparisonError`.
- Sağlamlık sınırları: en fazla 200 karakter, üs en fazla 100.

### CLI
- `codementor schema export --out schemas/` → `report.schema.json`, `llm_analysis.schema.json`, `llm_socratic.schema.json`.

### Testler (234 test, hepsi geçiyor)
- `tests/unit/test_bigo.py` — birim testleri + 7 hypothesis özellik testi (geçişlilik, üçlü ayrım, gidiş-dönüş, değişmezlik, toplam = max, çarpım monotonluğu, çökme yok).
- `tests/unit/test_models.py` — alan eşleşmesi, sınırlar, fazladan alan reddi, modül ayrımı.
- `tests/unit/test_schema_export.py` — 3 dosya, deterministik çıktı, commit edilen şemaların güncelliği.
- `tests/golden/` — §6.5 örnek raporu doğrulama ve gidiş-dönüş.

### Refactor
- `bigo.py` 400 satır sınırı için bölündü: `bigo.py` (dışa açık API), `_bigo_algebra.py` (terim cebiri + biçim), `_bigo_parser.py` (tokenizer + ayrıştırıcı).
