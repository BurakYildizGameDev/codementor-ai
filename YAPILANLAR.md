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

**Commit'ler:** `60d0cae` Big-O ayrıştırıcı · `43c5708` veri modelleri · `719dc3b` schema export · `d83833e` dokümanlar · `806f3cf` bigo refactor

---

## Faz 2 — Soru Bankası ve Kontrol Listeleri ✅

**Dal:** `faz/2-soru-bankasi` · **Mimari:** §7, §8.3, §12

### Modeller (`models/questions.py`)
- `QuestionPublic` — API ve CLI'ın gördüğü soru: yalnızca problem tanımı. Referans çözüm yolu, ipuçları, kavram etiketleri ve soruya özgü kontrol maddeleri **yok**.
- `Question` — `QuestionPublic` + mentorluk verisi (`concept_tags`, `checklist_extra`, `hint_ladder`) + `reference_solution_path` (yalnızca `private/` altında göreli bir dosya).
- `ExpectedComplexity` — işlem → Big-O (`parse_bigo` ile doğrulanır, `1*` amortize).
- `ChecklistFile`, `ChecklistItem`, `AppliesTo` — kontrol listesi dosya formatı.

### Yükleyiciler (`questions/`)
- `QuestionBank.load(dir)`, `get(id)`, `public(id)`, `filter(language, engine, difficulty)`.
- `Checklists.load(dir)`, `select_items(language, engine, concept_tags, limit=12)`.
- Hata mesajları Türkçe ve dosya + alan yolu içerir; yinelenen kimlik, id/dosya adı uyuşmazlığı, YAML sözdizimi hataları yakalanır.

### İçerik (`data/`)
- **14 soru** (§7.2 matrisi): C ×4, C++ ×3, C# ×2, Unity ×3, Unreal ×2. Her birinde prompt, kısıtlar, beklenen karmaşıklık, kavram etiketleri, soruya özgü kontrol maddeleri ve 3 seviyeli ipucu merdiveni.
- **5 kontrol listesi** (c, cpp, csharp, unity, unreal), toplam 50 madde; §8.2'deki LLM tespitli kurallar dahil.
- Soru metinleri problemi tanımlar, yöntemi söylemez (testle korunuyor).

### CLI ve yapılandırma
- `codementor questions list [--language] [--engine] [--difficulty] [--dir]`
- `codementor questions show <id> [--dir]` — ipuçlarını ve referans yolunu göstermez.
- `codementor.toml` → `[data] questions_dir`, `checklists_dir`. Bağımlılık: `pyyaml`.

- Çıkış kodları: 1 soru bulunamadı, 3 bozuk yapılandırma veya veri dosyası (stderr'e, traceback'siz).

### Kod denetimi (`kod-denetci` alt ajanı)
- Yüksek önemde bulgu yok; 5 kabul kriterinin hepsi karşılanıyor.
- **Orta ×2, düzeltildi:** Public modelde mentorluk verisi (ipuçları API'den sızabilirdi) → modelden çıkarıldı; bozuk config'te traceback ve yanlış çıkış kodu → Türkçe mesaj + kod 3.
- **Düşük ×9, düzeltildi:** referans yolu doğrulaması sıkılaştırıldı, enum karşılaştırmaları `==`, YAML'da yinelenen anahtar reddi, tamamen Türkçe hata mesajları, boş işlem adı ve yinelenen etiket reddi, `.YAML` uzantısı, aynı dosyada yinelenen madde mesajı, soru içeriği düzeltmeleri (tanımsız `k`, dolaylı yöntem sızıntısı, yönteme bağlı ipucu).

### Testler (358 test, hepsi geçiyor)
- `test_question_bank.py`, `test_checklists.py`, `test_question_data.py`, `test_cli_questions.py`.

**Commit'ler:** `b079c87` modeller ve yükleyiciler · `663002e` 14 soru ve 5 kontrol listesi · `859602c` CLI komutları · `1ab14bc` dokümanlar

---

## Faz 3 — Normalizasyon ve Tier 0 Ön Doğrulama ✅

**Dal:** `faz/3-tier0` · **Mimari:** §5.1, §5.2.1, §5.2.4, §12

### Normalizasyon (`ingest/normalize.py`)
- UTF-8'e çözme, BOM atma; çözülemeyen bayt, NUL ve geçersiz Unicode reddi (API'de 422).
- CRLF ve tek CR → LF; sekmeler korunur; satırlar yalnızca `\n` ile bölünür (tree-sitter ile aynı numaralar).
- Satır/bayt sınırları config'den (600 satır / 40 KB) → `CodeTooLargeError` (413).
- LLM'e giden sağa hizalı numaralı görünüm (`  9 | kod`); görünmez satır ayırıcılar kaçışlanır.
- SHA-256 (önbellek anahtarı için).

### Dil ve motor tespiti (`ingest/detect.py`)
- Unity (`using UnityEngine`, `MonoBehaviour` ...) ve Unreal (`UCLASS`, `GENERATED_BODY`, `CoreMinimal.h` ...) önce; sonra C / C++ / C#.
- Sinyaller yorum ve metin içerikleri maskelenmiş kodda aranır (`printf("=>")` C#'a benzemez).
- Yalnızca C başlığı kullanan "C tarzı C++" tree-sitter dilbilgisiyle doğrulanıp C++'a düzeltilir; Java reddedilir.
- Kullanıcının verdiği dil/motor her zaman kazanır; belirsiz kod 422 ile kullanıcıya sorulur.

### tree-sitter katmanı (`analysis/`)
- `parsers.py`: iş parçacığı başına önbelleklenmiş ayrıştırıcılar; `TreeCursor` ile güvenli gezinti.
- Unreal makroları (`UCLASS(...)`, `UPROPERTY(...)`, `*_API` ...) ayrıştırmadan önce aynı uzunlukta boşlukla nötrleştirilir; satır/kolon kaymaz.
- `lexical.py`: tek geçişli (doğrusal süre) yorum/metin maskeleme ve parantez eşleme.

### Tier 0 ön doğrulama (`validation/`)
- `tier0.py`: ERROR/MISSING düğümleri → Türkçe mesajlı tanı; 1 tabanlı satır, karakter cinsinden kolon.
- Eksik `;` doğru satırda; dosya sonunda kapanmamış blok için "Satır N ile başlayan blok kapanmamış" mesajı.
- `policy.py`: sözdizimi hatası → `FAILED` ve erken çıkış; temiz → devam.
- 600 satırlık dosyada 1–4 ms (sınır 50 ms).

### Önemli olaylar
- **tree-sitter 0.26.0 çöküyordu:** hatalı büyük dosyalarda Windows'ta bellek ihlali ve heap bozulması. Sürüm `<0.26` sabitlendi; alt süreçte çalışan regresyon testi eklendi.
- **Kod denetimi (`kod-denetci`):** Yüksek ×2 (makro nötrleştirmede DoS, yorumdan önce eksik `;`un yanlış satırda raporlanması), Orta ×6, Düşük ×10 bulgu düzeltildi.

### Testler (573 test, hepsi geçiyor)
- 30 fixture: `tests/fixtures/tier0/{c,cpp,csharp}/{valid,invalid}/` (2 Unity, 3 Unreal dahil).
- `test_normalize.py`, `test_detect.py`, `test_lexical.py`, `test_parsers.py`, `test_tier0.py`, `test_policy.py`.

**Commit'ler:** `27a7874` tree-sitter ve makro nötrleştirme · `8360805` normalizasyon ve dil tespiti · `78d1824` Tier 0 ve politika · `525b41d` dokümanlar

---

## Mimari karar — Docker zorunluluğu kaldırıldı (ADR-0009) ✅

**Dal:** `adr/0009-docker-yok`

- **Karar:** Docker hiçbir yerde zorunlu değil. Tier 1 derleyici denetimi, makinede kuruluysa gcc/clang ve `dotnet` (Roslyn) ile doğrudan çalışır; kurulu değilse `SKIPPED` olur ve sistem Tier 0 ile devam eder. Docker yalnızca opsiyonel dağıtım paketlemesi olarak kaldı.
- **Güvenlik:** Konteyner yerine süreç düzeyi önlemler — kod yalnızca stdin ile, tehlikeli `#include`'lar derleyiciden önce engellenir, boş geçici çalışma dizini, temizlenmiş ortam, zaman aşımı, çıktı ve bellek sınırları. Kullanıcı kodu hâlâ hiç çalıştırılmıyor.
- **Güncellenenler:**
  - `docs/adr/0009-docker-yerine-yerel-derleyici.md` (yeni)
  - `docs/mimari.md`: Tier 1 tasarımı, güvenlik tablosu, test stratejisi, dizin yapısı, config, dağıtım, ADR listesi
  - `docs/UYGULAMA_PLANI.md`: kurulum gereksinimleri, komutlar, **Faz 4 yeniden yazıldı** ("Tier 1 Yerel Derleyici"), Faz 13, zaman çizelgesi
  - Test işareti `sandbox` → `compiler`; `make test-compiler`; CI ve AGENTS.md komutları; config'ten `sandbox_image` kaldırıldı
- **Durum:** Yalnızca karar ve dokümanlar; Faz 4'ün kodu henüz yazılmadı.
