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

---

## Faz 4 — Tier 1 Yerel Derleyici (Docker'sız) ✅

**Dal:** `faz/4-tier1` · **Mimari:** §5.2.2–5.2.4, §12 · **ADR:** 0009, 0010

### Araç keşfi (`validation/toolchain.py`)
- `PATH`'te gcc/g++/clang/clang++ ve `dotnet` + derlenmiş Roslyn aracı aranır; mutlak yolla çağrılır.
- Tercih: C gcc→clang, C++ g++→clang++, Unreal clang++→g++. Sonuç önbelleklenir; `/health/ready` için `summary()`.

### Güvenli çalıştırma (`validation/runner.py`, `_winjob.py`)
- Kod yalnızca stdin ile; kabuk yok; boş geçici çalışma dizini; izin listesiyle ortam (`LC_ALL=C`).
- Zaman aşımı; süreç ağacı her durumda öldürülür; stdout/stderr 64 KB sınırı.
- Windows: askıda başlatma → Job Object (bellek + 8 süreç) → devam; kurulamazsa çalıştırılmaz.
- POSIX: `RLIMIT_CPU/CORE/FSIZE/AS` exec öncesi başlatıcıda; süreç grubu (ADR-0010).

### Include koruması (`validation/include_guard.py`)
- Mutlak yol, `..`, sürücü, `:`, `\`, Windows aygıt adları, `#include MACRO`, `#import`, `#include_next`, `#embed`, `__has_*`, `_Pragma`, `#pragma ... dependency`, trigraph, `##` → derleyici hiç çağrılmaz, `SKIPPED`.
- Fail-closed: tehlikeli yollar yorum/metin içinde bile reddedilir (maskeleyici derleyiciyle her sözcük ayrımında aynı fikirde olmayabilir).

### Tier 1 ve politika (`validation/tier1.py`, `diagnostics.py`, `policy.py`)
- gcc/clang `<stdin>:satır:kolon: önem: mesaj` ayrıştırıcısı ve Roslyn JSON ayrıştırıcısı (en çok 20 tanı).
- Unreal: `data/stubs/ue_stubs.h` + Tier 0 makro nötrleştirme + yerel include'ların boşaltılması; hatalar `WARNING`'e düşer.
- Bulunamayan başlık `WARNING`; araç yok / zaman aşımı / koruma → `SKIPPED`; kesin hata → `FAILED` + erken çıkış.

### Roslyn aracı (`tools/roslyn-check/`)
- .NET 10 konsol uygulaması; yalnızca `CSharpSyntaxTree.ParseText`; stdin → JSON. `make roslyn-check` ile derlenir.

### Önemli olaylar
- **Güvenlik denetimi (`kod-denetci`):** Yüksek ×4 (include koruması; boşluklu satır birleştirme, `\f`/`\v`, maskeleyici–derleyici uyuşmazlığı ve Unreal dönüşümüyle atlatılabiliyordu), Orta ×3 (tanı regex'inde ReDoS — 60 KB satırda 118 s; token yapıştırma; `preexec_fn`), Düşük ×6. Hepsi düzeltildi ve testlendi.
- Stub, gerçek clang'a (`zig c++`) karşı iki Unreal fixture'ıyla denendi; yalnızca stub'da olmayan üyeler hata veriyor (uyarıya düşüyor).

### Testler (774 test + derleyici testleri)
- `test_include_guard.py`, `test_diagnostics.py`, `test_runner.py`, `test_toolchain.py`, `test_tier1.py`, `test_policy.py`, `test_ue_stubs.py`, `test_no_docker.py`.
- `tests/compiler/`: bu makinede Roslyn testleri çalışıyor; gcc/clang testleri araç olmadığı için atlanıyor.

---

## Faz 5 — Statik Olgu Çıkarımı ve Karmaşıklık İpucu ✅

**Dal:** `faz/5-olgular` · **Mimari:** §5.3.1, §5.3.2

### Olgu çıkarımı (`analysis/extractor.py` + yardımcılar)
- tree-sitter sorguları `analysis/queries/{c,cpp,csharp}/*.scm` dosyalarında: fonksiyonlar, döngüler, çağrılar, tahsisler, alanlar.
- Her fonksiyon için: ad, satırlar, parametreler, motor yaşam döngüsü ve **sıcak yol** (Unity `Update/FixedUpdate/LateUpdate/OnGUI`, Unreal `Tick/TickComponent`).
- Döngüler: tür (for/while/do/foreach, C++ range-for dahil), iç içe derinlik, **sınır sınıfı** (LINEAR / LOG / CONSTANT / UNKNOWN; emin değilse UNKNOWN), iki işaretçi (two-pointer) şüphesi.
- Çağrılar: döngü derinliği ve `data/call_costs.yaml`'dan bilinen maliyet (tip dosyadaki bildirimden çözülür; tahmin yok).
- Özyineleme (dallanma faktörü, yarılama), tahsis/serbest bırakma (malloc, new, make_unique, C# referans `new`, metin birleştirme, LINQ, closure), motor sembolleri (`UPROPERTY`, `UObject*` alanları, olay abonelikleri, `OnEnable/OnDisable`).
- Hiçbir durumda çökmez: bölümler yalıtılmış, hata olursa o bölüm boş + uyarı.

### Karmaşıklık ipucu (`analysis/complexity_hint.py`)
- İç içe döngü yolu boyunca çarpım + döngüdeki bilinen çağrı maliyeti + aynı dosyadaki fonksiyonların ipucu; özyinelemede üstel şüphe, böl-yönet ve karşılıklı özyineleme.
- Her ipucu `confidence` (low/medium/high) ve açıklayıcı `basis` ile gelir. Örnek: "Update: satır 24 for (linear) × satır 26 for (linear) → n^2".
- Two-pointer vakasında ipucu bilerek yanılır (n² der) ve **düşük güven** verir.

### Önemli olaylar
- **Kod denetimi (`kod-denetci`):** Yüksek ×6 (yanlış LOG/CONSTANT sınıfları, sahte LINQ maliyeti, karşılıklı özyinelemede "1 high", `mid` argümanıyla gizlenen üstel şüphe, tek istisnanın tüm olguları silmesi), Orta ×8 (dört karesel yol dahil), Düşük ×7. Hepsi düzeltildi; her biri `test_facts_review.py`'de sabitlendi.
- 40 KB sınırındaki kötü niyetli girdilerde (1300 iç içe döngü, 6000 terimli `+` zinciri) süre < 1 s.

### Testler (966 test)
- `test_loop_bounds.py`, `test_extractor.py`, `test_call_costs.py`, `test_complexity_hint.py`, `test_facts_review.py`.
- 15 golden vaka (`tests/golden/facts/`), güncelleme: `uv run pytest tests/golden --update-golden`.
- 12 karmaşıklık fixture'ı (`tests/fixtures/complexity/`): O(1), O(log n), O(n), O(n log n), O(n²), üstel, two-pointer ...

## Faz 6 (daraltılmış) — Kural Motoru ve 10 Statik Kural ✅

### Ne yapıldı
- Kayıt defterli kural motoru (`rules/`): her kural bir sınıf, `@register_rule` ile eklenir; dil/motor filtresi (Unity kuralı düz C#'ta çalışmaz), yapılandırmadan tek tek kapatma (`[rules] disabled`).
- 10 kural: C-BUF-001, C-MEM-001, CPP-OWN-001, CS-ALLOC-001, CS-PERF-001, UNITY-GC-001, UNITY-PERF-001, UNITY-EVT-001, UE-GC-001, UE-PERF-001. Kalan 10 kural Faz 10 sonrasına ertelendi.
- `codementor rules list|doc`, otomatik `docs/rules-catalog.md`.
- 57 fixture (kural başına ≥2 pozitif + ≥2 "neredeyse ihlal" negatif, `// EXPECT:` satırıyla).

### Önemli olaylar
- Denetim: C-MEM-001 iç içe girdide 106 sn sürüyordu (→ 0,37 sn) ve bağlı liste kodunda yanlış bulgu veriyordu; satır bazlı eşleşme yanlış bulgular; hepsi düzeltildi.

## Faz 7 — LLM Sağlayıcı Adaptörleri ✅

### Ne yapıldı
- Tek `LLMProvider` arayüzü arkasında 7 sağlayıcı: Fake, Ollama, OpenAI, DeepSeek, Anthropic (HTTP) ve **Claude Code CLI**, **Antigravity CLI** (abonelikle, API anahtarsız).
- `SchemaAdapter`: tek Pydantic modelinden sağlayıcıya özel şema; OpenAI katı mod, Ollama kısıtları korur, zorlanamayan kısıtlar açıklamaya not.
- Yeniden deneme yalnızca ağ/429/5xx; fallback zinciri ve rapora Türkçe uyarılar; `codementor providers check`.
- Log'da API anahtarı maskeleme (global yapılandırmadan bağımsız).
- GitHub'da private repo açıldı, CI ilk kez yeşil (gcc/clang ve POSIX testleri Linux'ta doğrulandı).

### Önemli kararlar
- **ADR-0011:** Anthropic'te zorunlu `tool_choice` yerine `output_config.format` (güncel modeller zorunlu aracı reddediyor).
- **ADR-0012:** CLI ajanları: tüm mesajlar stdin'den, Claude'da araçlar kapalı, `agy` deneysel ve açık onay gerektirir.

### Canlı denemeler (aynı Unity kodu)
- Claude CLI: ~32 sn, asıl mantık hatasını buldu, Sokratik sorular çözüm vermiyor.
- deepseek-r1:8b (Ollama): 3–10 dk, hatayı kaçırdı; `think=false` ile 187 sn, 12/16.

### Güvenlik denetimleri
- Derin JSON ile çökme, `Retry-After: nan` ile sonsuz bekleme, istisna zincirinde API anahtarı, Windows'ta çalışma dizinindeki `claude.exe`'nin seçilmesi — hepsi düzeltildi.
- Aynı "çalışma dizini" açığı Faz 4 derleyici çalıştırıcısında da kapatıldı: `run_process` artık yalnızca mutlak yol kabul ediyor.

### Testler (1366 test)
- 6 adaptörün geçtiği ortak sözleşme paketi (respx ile ağsız), `tests/live/` canlı testler (`-m live`).

