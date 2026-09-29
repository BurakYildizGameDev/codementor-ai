# İlerleme Günlüğü

## Durum
| Faz | Durum | Dal | Tarih | Araç (uygulayan / denetleyen) |
|---|---|---|---|---|
| 0 | ✅ | faz/0-iskelet | 2026-09-29 | Claude Code / — |
| 1 | ✅ | faz/1-modeller | 2026-09-29 | Claude Code / — |
| 2 | ⏳ | | | |

## Faz 0 — Notlar
**Yapılanlar:** pyproject (uv, ruff, mypy strict, pytest işaretleri live/sandbox/slow), config (pydantic-settings; CLI > env > TOML > varsayılan), `codementor --version`, Makefile, CI, ajan dosyaları (Bölüm 4).
**Alınan kararlar (ve neden):**
- TOML dosya yolu `CODEMENTOR_CONFIG_FILE` ile değiştirilebilir (varsayılan `./codementor.toml`); testlerin geçici dosya kullanabilmesi için.
- CLI bayrakları `load_settings(**overrides)` init argümanı olarak verilir → en yüksek öncelik.
- ruff `allowed-confusables = ["ı"]`: Türkçe docstring/yorumlar RUF001-003 uyarısı vermesin.
**Mimariden sapmalar (ADR linki):** yok
**Açık sorular:**
- Windows geliştirme makinesinde `make` yok; komutlar `uv run ...` ile doğrudan çalıştırıldı. (Git Bash için `choco install make` / `winget install GnuWin32.Make` önerilir.)
- CI henüz GitHub'da çalıştırılmadı (uzak repo yok).
**Bu fazda öğrendiğim:**

## Faz 1 — Notlar
**Yapılanlar:**
- `models/`: `enums`, `request`, `facts`, `findings`, `llm_output`, `report` (§6.2–6.4 alan adları birebir), ortak `_base.StrictModel` (`extra="forbid"`).
- `models/bigo.py`: tokenizer + özyinelemeli ayrıştırıcı (regex yığını değil). Desteklenen: `O(...)`/`o(...)`, büyük/küçük harf, üst simgeler (`²`, `¹⁰`, `ⁿ`), `* · × ⋅` ve bitişik çarpım (`nlogn`, `nm`), `log/lg/ln`, log tabanı (`log2`, `log_2`, `log₂`), `log^k n`, `sqrt`, kesirli üs (`n^1.5`), `c^n`, `n!`, sabite bölme (`n/2`), toplam. Katsayılar ve baskılanan terimler atılır.
- Sıralama: `_Factor` alanları (faktöriyel, üstel taban, polinom, log) sözlüksel karşılaştırılır → tek değişkende toplam sıralama. Çok değişkenlide `BigOComparisonError`; sabit her şeyle karşılaştırılabilir. `same_class()` çok değişkenlide de çalışır.
- `models/schemas.py` + `codementor schema export --out` → `schemas/{report,llm_analysis,llm_socratic}.schema.json` (deterministik, `sort_keys`).
- Testler: `test_bigo.py` (7 hypothesis özelliği: geçişlilik, üçlü ayrım, kanonik/display gidiş-dönüş, katsayı/sarmalayıcı değişmezliği, toplam=max, çarpım monotonluğu, çökme yok), `test_models.py`, `test_schema_export.py`, `tests/golden/` (§6.5 örneği + gidiş-dönüş). 234 test.
**Alınan kararlar (ve neden):**
- `CompilationBlock = {status: CompilationStatus, diagnostics: list[Diagnostic]}` (§6.4 yalnızca "status + diagnostics" diyordu).
- `AnalysisRequest` §9 istek örneğinden; `options.*` varsayılanı `None` → config değeri geçerli. `NormalizedCode`/`LanguageHint` Faz 3'te eklenecek.
- §5.3.1 olgu alan adları tablodan türetildi (`FunctionFact`, `LoopFact`, ... `CodeFacts`); `ComplexityHint.value` doğrulayıcıda `parse_bigo` ile kanonikleşir; `EXPONENTIAL_SUSPECT` → `exponential_suspect: bool`.
- `extra="forbid"` tüm modellerde: LLM'in uydurduğu alanlar reddedilir, şemada `additionalProperties: false` (katı yapılandırılmış çıktı modları için gerekli).
- Değişkenler küçük harfe çevrilir (`O(N^2)` = `n^2` şartı) → `O(V+E)` kanonik `e + v`. Terimler kanonik metne göre sıralanır; farklı değişken grupları `*` ile birleşir (`m*n`, `e*log v`).
- Kanonik çarpan sırası: polinom, log, üstel, faktöriyel (`n^2 log n`, `n^2 2^n`). `display` yalnızca tam sayı üsleri üst simgeye çevirir (`n^1.5`, `2^n` olduğu gibi kalır).
- Güvenlik/sağlamlık sınırları: girdi ≤ 200 karakter, üs ≤ 100, üstel taban ≤ 10^100; 3+ ardışık tek harf (`size`, `foo`) "tanımsız sözcük" hatası.
- `schemas/` commit edilir (Web UI tipleri bundan üretilecek); `test_committed_schemas_up_to_date` model–şema kaymasını yakalar.
**Mimariden sapmalar (ADR linki):** yok. (`models/_base.py` ve `models/schemas.py` §16'da listelenmeyen yardımcı modüller.)
**Açık sorular:**
- ~~`bigo.py` 582 satır (>400)~~ → çözüldü: `bigo.py` (API, 155) + `_bigo_algebra.py` (terim cebiri/biçim, 177) + `_bigo_parser.py` (tokenizer/ayrıştırıcı, 291). Dışa açık API değişmedi.
- `make` hâlâ yok (Faz 0'dan); kontroller `uv run ...` ile çalıştırıldı.
- Windows konsolunda (cp1254) `O(n²)` çıktısı bozuk görünüyor; yalnızca görüntü sorunu (`PYTHONIOENCODING=utf-8` ile düzelir).
**Bu fazda öğrendiğim:**
- Asimptotik baskınlık, değişken başına `(faktöriyel, taban, üs, log üssü)` demetinin sözlüksel sırasıyla ifade edilebiliyor; çok değişkenlide "her değişkende ≥" kısmi sıra olarak kalıyor.

## Sonraya (kapsam dışı fikirler)
- Faz 5: `call_costs.yaml` içindeki amortize `1*` gösterimi `parse_bigo`'ya verilmeden önce `*` ayıklanmalı (ya da `BigO`'ya `amortized` bayrağı).
- `parse_bigo` şu an `log log n`, `n^n`, `Θ(...)`/`Ω(...)`, `max(n,m)` ve `k` gibi değişken üsleri desteklemiyor; eval'de LLM çıktılarında görülürse eklenebilir.
- `AnalysisReport.analysis_id` için ULID biçim doğrulaması (şu an serbest `str`, §6.4 böyle).
