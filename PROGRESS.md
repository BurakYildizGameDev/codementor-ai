# İlerleme Günlüğü

## Durum
| Faz | Durum | Dal | Tarih | Araç (uygulayan / denetleyen) |
|---|---|---|---|---|
| 0 | ✅ | faz/0-iskelet | 2026-09-29 | Claude Code / — |
| 1 | ✅ | faz/1-modeller | 2026-09-29 | Claude Code / — |
| 2 | ✅ | faz/2-soru-bankasi | 2026-09-29 | Claude Code / — |
| 3 | ✅ | faz/3-tier0 | 2026-09-29 | Claude Code / kod-denetci |
| 4 | ✅ | faz/4-tier1 | 2026-09-29 | Claude Code / kod-denetci |
| 5 | ✅ | faz/5-olgular | 2026-09-29 | Claude Code / kod-denetci |
| 6 (daraltılmış) | ✅ | faz/6-kurallar | 2026-09-29 | Claude Code / kod-denetci |
| 7 | ✅ | faz/7-saglayicilar | 2026-09-29 | Claude Code / kod-denetci |
| 8 | ✅ | faz/8-promptlar | 2026-09-30 | Claude Code / kod-denetci |
| 9 | ✅ | faz/9-dogrulayici | 2026-09-30 | Claude Code / — |
| 10 | ✅ | faz/10-pipeline | 2026-09-30 | Claude Code / — |
| 11 | ✅ | faz/11-api | 2026-09-30 | Claude Code / — |
| 12 | ✅ | faz/12-eval | 2026-09-30 | Claude Code / — |
| 13 | ✅ | faz/13-sunum | 2026-09-30 | Claude Code / — |
| 14 | ✅ | faz-14-masaustu | 2026-10-01 | Claude Code / — |
| 15 | ✅ | faz-15-baglantilar | 2026-10-01 | Claude Code / — |
| 16 | ✅ | faz-16-diller | 2026-10-01 | Claude Code / — |
| 17 | ✅ | faz/17-kurallar | 2026-10-01 | Claude Code / kod-denetci |
| 18 | ✅ | faz/18-eval-diller | 2026-10-01 | Claude Code / kod-denetci |
| 19 | ✅ | faz/19-durdur | 2026-10-01 | Claude Code / kod-denetci |
| 20 | ✅ | faz/20-html-denge | 2026-10-01 | Claude Code / kod-denetci |
| 21 | ✅ | faz/21-kural-dogrulugu | 2026-10-01 | Claude Code / kod-denetci |
| 23 | ✅ | faz/23-dagitim-yollar | 2026-10-01 | Claude Code / — |
| 24 | ✅ | faz/24-masaustu-kullanilabilirlik | 2026-10-01 | Claude Code / — |
| 25 | ✅ | faz/25-saglayicilar | 2026-10-02 | Claude Code / — |
| 26 | ✅ | faz/26-api-web | 2026-10-02 | Claude Code / — |
| 27 | ✅ | faz/27-saglamlik | 2026-10-02 | Claude Code / — |
| 22 | ✅ | faz/22-eval-precision, faz/22b-precision | 2026-10-02 | Claude Code / — |
| 28 (Codex) | ✅ | faz/28-cli-ajanlari | 2026-10-02 | Claude Code / — |
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

## Faz 2 — Notlar
**Yapılanlar:**
- `models/questions.py`: `QuestionPublic` / `Question` (+ `reference_solution_path`), `ExpectedComplexity`, `ChecklistFile`, `ChecklistItem`, `AppliesTo`.
- `questions/bank.py`: `QuestionBank.load/get/public/filter`; `questions/checklists.py`: `Checklists.load/select_items/all_items`; `questions/_loader.py`: ortak `yaml.safe_load` + Türkçe doğrulama mesajları (`dosya: alan.yolu: mesaj`).
- `data/questions/*.yaml`: §7.2'deki 14 soru (prompt, kısıtlar, beklenen karmaşıklık, concept_tags, checklist_extra, 3 seviyeli hint_ladder).
- `data/checklists/{c,cpp,csharp,unity,unreal}.yaml`: 50 madde; §8.2'deki LLM tespitli kurallar (`CPP-UB-001`, `UNITY-SO-001`, `UE-PTR-001`) ve statik+LLM kurallar (`CPP-SP-001`, `UE-PERF-001`) dahil.
- CLI: `codementor questions list [--language --engine --difficulty --dir]`, `codementor questions show <id> [--dir]`.
- Config: `[data] questions_dir`, `checklists_dir`. Bağımlılık: `pyyaml` (+ geliştirme: `types-pyyaml`).
- Testler: `test_question_bank.py`, `test_checklists.py`, `test_question_data.py` (gerçek içerik: §7.2 matrisi, eksiksizlik, yöntem sızıntısı, kontrol listesi kapsaması), `test_cli_questions.py`. Toplam 358 test.
**Alınan kararlar (ve neden):**
- Pydantic modelleri AGENTS.md kuralı gereği `models/questions.py`'de (§16'da listelenmiyor).
- `QuestionPublic` yalnızca problem tanımını taşır (id, version, dil, motor, zorluk, başlık, prompt, kısıtlar, beklenen karmaşıklık). `Question(QuestionPublic)` ek olarak mentorluk verisini (`concept_tags`, `checklist_extra`, `hint_ladder` = `MENTOR_FIELDS`) ve `reference_solution_path`'i taşır. `filter()` ve `public()` yalnızca `QuestionPublic` döndürür; ipuçları gelecekteki `/v1/questions/{id}` yanıtından sızamaz (denetim bulgusu; mimari §12'nin ruhuna uygun, sapma değil).
- `reference_solution_path`: `private/` altında göreli bir **dosya** olmalı (`..`, mutlak yol, `\`, `:`, kontrol karakterleri ve yalnızca `private` reddedilir); normalleştirilmiş hali saklanır. Metinsel denetimdir; K5 dosyayı okurken `resolve()` + `is_relative_to()` ile yeniden denetlemeli. Dosyanın varlığı kontrol edilmez.
- YAML yükleme `SafeLoader` alt sınıfıyla: yinelenen anahtarlar sessizce ezilmez, hata verir. Uzantılar büyük/küçük harf duyarsız.
- Hata mesajlarında girdi değeri basılmaz; eşlenmemiş pydantic hata türleri Türkçe genel mesaja düşer; desen hataları örnekle açıklanır (ör. `c-hard-stack`).
- `expected` değerleri `parse_bigo` ile doğrulanır; sondaki `*` amortize işaretidir (`1*`). CLI'da `O(1) amortize` olarak gösterilir.
- `hint_ladder` tam olarak 1/2/3 seviyeli olmalı. `questions show` ipuçlarını, `checklist_extra`'yı ve `concept_tags`'i göstermez; bunlar mentorluk motoruna aittir.
- Kontrol listesi seçimi: uygun dosyalar = dil eşleşen ve motoru eşleşen veya tanımsız; sıra = core (motora özgü önce) → kesişen etiket sayısı azalan (eşitlikte motora özgü, sonra dosya sırası); en fazla 12. `checklist_extra` burada birleştirilmez (Faz 8).
- Soru metinlerinde yöntem sızıntısı testle korunuyor: her soru için yasaklı terim listesi (`test_prompts_do_not_reveal_method`).
- CLI çıkış kodları: 0 başarı, 1 bilinmeyen soru, 2 geçersiz komut satırı (Typer), 3 bozuk yapılandırma veya veri dosyası (sistem hatası, §10). Hatalar stderr'e, traceback'siz.
- Big-O ifadelerinde `n` dışındaki değişkenler (`k`, `d`) prompt veya kısıtlarda tanımlanmak zorunda (testle korunuyor).
**Denetim (kod-denetci):** Yüksek bulgu yok. Orta ×2 (Public modelde mentorluk verisi; bozuk config'te traceback + çıkış kodu 1) ve Düşük ×9 düzeltildi: yol doğrulaması, `is` → `==`, `concept_tags` için düz metin reddi, YAML yinelenen anahtar, Türkçe hata mesajları, boş işlem adı ve yinelenen etiket, `.YAML` uzantısı, aynı dosyada yinelenen madde mesajı, içerik (tanımsız `k`, nesne havuzu sorusunda dolaylı yöntem sızıntısı, bağlı listede prompt'ta olmayan "arama", yönteme bağlı ipucu). Testler stderr'i ayrıca doğruluyor. 358 test.
**Mimariden sapmalar (ADR linki):** yok.
**Açık sorular:**
- `c-hard-stack` prompt'u §7.1'den birebir alındı ve "Pointer aritmetiği kullanın" diyor; bu bir kısıt, yöntem ipucu sayılmadı.
- `make` hâlâ yok; kontroller `uv run ...` ile çalıştırıldı.
**Bu fazda öğrendiğim:**
- Git Bash heredoc'larında `\n` kaçışları Python betiğine ulaşmadan bozulabiliyor; çok satırlı düzenlemeler Edit aracıyla daha güvenli.

## Faz 3 — Notlar
**Yapılanlar:**
- `ingest/normalize.py`: UTF-8/BOM, CRLF/CR → LF, NUL ve geçersiz Unicode reddi, satır/bayt sınırları (config `limits`), yalnızca `\n` ile satır bölme, sağa hizalı numaralı görünüm, SHA-256. `ingest/errors.py`: `IngestError` + `CodeTooLargeError` (413), `EmptyCodeError`, `InvalidEncodingError`, `LanguageDetectionError` (422).
- `ingest/detect.py`: ağırlıklı sinyallerle motor (Unity/Unreal) ve dil tespiti; ipucu önceliği; C kararı tree-sitter dilbilgisiyle doğrulanır; Java reddedilir.
- `analysis/lexical.py`: tek geçişli yorum/metin maskeleme ve parantez eşleme. `analysis/parsers.py`: iş parçacığı başına `Parser` önbelleği, doğrusal zamanlı Unreal makro nötrleştirme, `TreeCursor` tabanlı `iter_nodes`.
- `validation/tier0.py`: ERROR/MISSING → `Diagnostic` (1 tabanlı satır, karakter kolonu), kapanmamış blok özeti, C# `;` boşluğu sezgisi, üst sınır 20. `validation/policy.py`: §5.2.4 Tier 0 satırı.
- Modeller: `LanguageHint`, `Detection`, `NormalizedCode` (`request.py`), `Tier0Result`, `PolicyDecision` (`validation.py`); motor→dil kuralı `enums.required_language/check_engine_language`'e taşındı.
- 30 fixture (`tests/fixtures/tier0/`), 573 test.
**Alınan kararlar (ve neden):**
- **tree-sitter `<0.26` sabitlendi.** 0.26.0 Python bağlaması, ERROR içeren büyük ağaçları `Node.children` ile gezerken Windows'ta erişim ihlaliyle çöküyor ve heap'i bozuyor (çökme sonradan alakasız yerlerde, ör. YAML okurken çıkıyordu). 0.25.2'de yok. Alt süreçte çalışan `test_tree_sitter_binding_is_memory_safe` sürüm yükseltmesinde bunu yakalar. Tüm gezintiler `iter_nodes` (TreeCursor) ile.
- Unreal makroları ayrıştırmadan önce **aynı uzunlukta boşlukla** değiştirilir; satır ve karakter kolonları kaymaz. Makrolar ve parantezler yorum/metin maskelenmiş kopyada aranır.
- Numaralı görünüm: numara genişliği = toplam satır sayısının basamak sayısı. U+2028 gibi görünmez satır ayırıcılar görünümde ` ` olarak kaçışlanır (sahte satır numarası enjeksiyonu; §12).
- Kolonlar karakter cinsinden ve **ayrıştırılan (nötrleştirilmiş) metin** üzerinden hesaplanır.
- Eksik `;` (MISSING) önceki kod simgesinin hemen arkasında raporlanır; tree-sitter onu araya giren yorumların arkasına koyuyordu.
- Dosya sonunda kapanmamış blok: tree-sitter'ın blok başına koyduğu dev ERROR yerine son satırda "Satır N ile başlayan blok kapanmamış" mesajı; üst sınırda asla düşmez.
- Hiç dil işareti taşımayan kod 422 döner (mimari: "belirsizse kullanıcıya sorulur").
- Deney betiği (`scripts/ts_probe.py`) repoya eklenmedi; aynı güvenceyi testler veriyor.
**Mimariden sapmalar (ADR linki):** yok. `normalize` imzası geriye uyumlu genişletildi (`raw: str | bytes`, `limits=`).
**Denetim (kod-denetci):** Yüksek ×2 (makro nötrleştirmede O(n²) DoS: 40 KB girdide 4–7 s; eksik `;` yorum satırında raporlanıyordu ve bir fixture işareti bunu gizliyordu), Orta ×6 (C tarzı C++ C sanılıyordu; string içeriği sahte sinyal üretiyordu; tek surrogate 500 veriyordu; yorum regex'i karesel; makro argümanındaki yorum/basamak ayırıcısı sahte hata; iki fixture işareti yanlış satırda), Düşük ×10. Hepsi düzeltildi ve testlendi; D2 ve D9 aşağıda "Sonraya"da.
**Açık sorular:**
- `make` hâlâ yok; kontroller `uv run ...` ile çalıştırıldı.
- Erken çıkıştaki Sokratik şablon mesajları (§5.2.4) bu fazın çıktısı değil; Faz 10'da rapor oluşturmayla ele alınmalı.
**Bu fazda öğrendiğim:**
- Yerel eklenti (C) çökmeleri Python'da yanıltıcıdır: heap bozulması, belirtiyi tamamen ilgisiz bir modülde gösterebilir. Yalıtılmış betiklerle ikiye bölerek ve sürüm karşılaştırarak kök nedene inmek gerekir.
- `ruff --fix` (UP037), `from __future__ import annotations` açıkken yerel değişkendeki `Literal["x"]` tırnaklarını silebiliyor; `Literal` tipleri modül düzeyinde takma adla tanımlanmalı.

## Mimari karar — Docker zorunluluğu kaldırıldı (ADR-0009, 2026-09-29)
**Karar:** Docker hiçbir yerde zorunlu değil. Tier 1, makinede kuruluysa gcc/clang ve `dotnet` (Roslyn) araçlarını doğrudan alt süreç olarak çalıştırır; yoksa `SKIPPED`. Docker yalnızca opsiyonel dağıtım paketlemesi (Faz 13).
**Neden:** Geliştirme makinesinde Docker yok (Windows); kurulum eşiği yüksek; derleyiciler yalnızca sözdizimi/tip denetimi yaptığı için (kod çalıştırılmıyor, ADR-0005) süreç düzeyi önlemler yeterli.
**Güvenlik önlemleri (§5.2.3 yeni):** yalnızca stdin; include koruması (mutlak yol, `..`, sürücü, `\`, `#include MACRO`, `#embed`, `__has_include` → `SKIPPED`); boş geçici çalışma dizini; temizlenmiş ortam; zaman aşımı + süreç ağacını öldürme; çıktı sınırı; POSIX rlimit / Windows Job Object. Paylaşılan sunucuda Tier 1 kapatılması önerilir.
**Değişenler:** `docs/adr/0009-docker-yerine-yerel-derleyici.md`; `mimari.md` §3, §5.2.2–5.2.4, §9, §12, §15–20, §22–23; `UYGULAMA_PLANI.md` §3.1, komutlar, Faz 4 (yeniden yazıldı), Faz 13, sorun giderme, zaman çizelgesi; `pytest` işareti `sandbox` → `compiler`; `Makefile` `test-sandbox` → `test-compiler`; CI ve AGENTS.md komutları; config'ten `validation.sandbox_image` kaldırıldı.
**Bu makinede:** Docker ve gcc/clang yok; `dotnet` 10.0.103 var → Faz 4'te C# (Roslyn) Tier 1 yerelde test edilebilir, C/C++ `compiler` testleri atlanır (CI'da çalışır).

## Faz 4 — Notlar
**Yapılanlar:**
- `validation/toolchain.py`: `PATH`'te araç keşfi (mutlak yol), `Toolchain.summary()` (`/health/ready`), önbellek + `clear_toolchain_cache()`.
- `validation/include_guard.py`: fail-closed include koruması (ayrıntı aşağıda).
- `validation/runner.py` + `_winjob.py`: yalnızca stdin, kabuk yok, boş geçici cwd, izin listeli ortam, zaman aşımı, süreç ağacını her durumda öldürme, 64 KB çıktı sınırı; Windows Job Object (askıda başlat → ata → `NtResumeProcess`), POSIX rlimit başlatıcısı.
- `validation/diagnostics.py`: `<stdin>:l:c: severity: msg` (gcc/clang) ve Roslyn JSON ayrıştırıcıları; 20 tanı ve 500 karakter mesaj sınırı.
- `validation/tier1.py`: disabled → araç → include koruması → stub → çalıştır → sınıflandır; hiçbir yolda istisna yok. `validation/policy.py`: `decide(tier0, tier1)` §5.2.4 tam tablo.
- Modeller: `SkipReason`, `CompilerTool`, `Toolchain`, `Tier1Result`; `PolicyDecision.warnings` (Faz 10'da `meta.warnings`'e).
- `data/stubs/ue_stubs.h` (§5.2.2 listesi + `FTransform`, `FTimerHandle`, `TSubclassOf`, `Cast` ...). `tools/roslyn-check/` (.NET 10, `ParseText`, stdin → JSON). `make roslyn-check`.
- Config: `validation.compile_memory_mb`, `stub_header`, `roslyn_check_dll`.
- 774 test (`-m "not live"`) + `tests/compiler/` (bu makinede Roslyn 7 test geçti; gcc/clang atlandı).
**Alınan kararlar (ve neden):**
- **ADR-0010:** POSIX'te `RLIMIT_NPROC` yok (kullanıcı başına sayılır, `cc1` başlatmayı bozar); süreç grubu öldürme. `RLIMIT_AS` dotnet'e uygulanmaz (GC büyük sanal alan ayırır) → `DOTNET_GCHeapHardLimit`. Windows'ta Job Object süreç sayısı (8) ve bellek sınırı; kurulamazsa fail-closed.
- **rlimit'ler `preexec_fn` ile değil**, `python -I -S -c <başlatıcı>` → `os.execv` ile: `preexec_fn` çok iş parçacıklı FastAPI sürecinde fork sonrası kilitlenebilir.
- **Include koruması fail-closed:** `mask_non_code` derleyiciyle her sözcük ayrımında uyuşmuyor (`L'/*'`, `b'/*'`, `R"(x"/*)"`, C/C++'ta `@"`). Bu yüzden tehlikeli hedefli `#include`/`#import`/`#embed`/`#pragma dependency` maskelenmemiş metinde her yerde aranır; yorumdaki `// #include "/etc/shadow"` da Tier 1'i atlatır (yalnızca `SKIPPED`, güvenli yönde). Makrolu `#include X` yalnızca yönerge konumunda reddedilir. `##`/`%:%:` (token yapıştırmayla `_Pragma`/`__has_include` üretimi) ve trigraph tümden reddedilir.
- **Unreal:** Tier 0'ın `neutralize_unreal_macros`'u (`*_API` dahil) ve yerel `#include "..."` boşaltma Tier 1'de de uygulanır (aynı uzunlukta; satır/kolon kaymaz); `\` ile devam eden satırlar boşaltılmaz; dönüşmüş son metin de korumadan geçer. Tüm Unreal hataları `WARNING` (ADR-0007).
- Bulunamayan başlık → `WARNING` (gcc/clang ölümcül hatada durur; kodun geri kalanı denetlenmez).
- Tanılarda yalnızca `<stdin>` satırları alınır (stub/sistem başlıkları atlanır). Derleyiciye `-fno-diagnostics-color` dışında sürüme özgü bayrak verilmez (macOS'ta `gcc` = clang).
- `-std=c17` trigraph'ları açtığı için trigraph içeren kod reddedilir.
- Roslyn aracı net10.0 + `RollForward=Major`; `Microsoft.CodeAnalysis.CSharp 4.14.0`.
**Mimariden sapmalar (ADR linki):** [ADR-0010](docs/adr/0010-tier1-surec-sinirlari.md) — `RLIMIT_NPROC` yerine süreç grubu; mimari §5.2.3, §17, §20 güncellendi.
**Denetim (kod-denetci, yalnızca güvenlik):** Yüksek ×4 — include koruması atlatılabiliyordu: (H1) `\` + boşluk + satır sonu birleştirmesi, (H2) maskeleyici–derleyici uyuşmazlığıyla sahte yorum (`L'/*'`, `R"`, `@"`), (H3) ``/``, (H4) Unreal dönüşümü yeni yönerge üretebiliyordu. Orta ×3 — tanı regex'inde ReDoS (60 KB boşluklu satır 118 s → 0,3 s), token yapıştırma, `preexec_fn`. Düşük ×6 — beklenmedik hatada süreç sızıntısı, normal çıkışta torun süreçler, Job Object yokken fail-open, Windows aygıt adları, tanı mesajı uzunluğu, Linux'ta dotnet bellek sınırı (ADR'de belgelendi). Hepsi düzeltildi ve regresyon testiyle sabitlendi.
**Açık sorular:**
- gcc/clang bu makinede yok: `compiler` işaretli C/C++ testleri yalnızca CI'da (ubuntu, gcc kurulu) çalışacak. Kaydedilmiş gcc/clang örnek çıktıları belgelenmiş biçime göre elle yazıldı; clang biçimi ve stub, `zig c++` (clang) ile ayrıca denendi.
- POSIX başlatıcısı ve rlimit testleri Windows'ta atlanıyor; ilk CI koşusunda doğrulanmalı.
- CI Roslyn aracını derlemiyor → C# `compiler` testleri CI'da atlanır (bkz. Sonraya).
- `make` hâlâ yok; kontroller `uv run ...` ile çalıştırıldı.
**Bu fazda öğrendiğim:**
- Güvenlik filtresini "derleyiciyle aynı sözcük ayrımı" varsayımına kurmak kırılgan; her ayrım farkı bir atlatma yoludur. Fail-closed (şüpheliyi reddet) tasarım, yanlış pozitifin maliyeti düşükse (burada yalnızca `SKIPPED`) doğru tercih.
- `.*?` + `[ \t]*$` gibi masum görünen regex kuyrukları uzun boşluklu satırda karesel olur; yakalamayı `[^\n]*` yapıp kırpmayı Python'a bırakmak doğrusal.
- Windows'ta süreç ağacı kontrolü için `CREATE_SUSPENDED` + Job Object + `NtResumeProcess` üçlüsü yarışsız ve saf ctypes ile yapılabiliyor.

## Faz 5 — Notlar
**Yapılanlar:**
- `analysis/queries/{c,cpp,csharp}/*.scm`: fonksiyon, döngü, çağrı, bellek, alan sorguları (Python'a gömülü sorgu yok); `queries/__init__.py` önbellekli yükleyici, belirleyici kaynak sırası.
- `analysis/extractor.py` → `extract_facts(code) -> CodeFacts`; yardımcılar `_context` (tek cursor geçişiyle bağlam), `_loops` (§5.3.1 sınır tablosu), `_symbols` (ad, tip tablosu), `_memory`, `_engine`, `_recursion`, `_callgraph`; hata ayıklama CLI'ı `python -m codementor.analysis.extractor dosya` (`_cli.py`, her zaman UTF-8).
- `analysis/call_costs.py` + `data/call_costs.yaml` (C, C++, Unreal, C#, LINQ, Unity); `config.data.call_costs_file`.
- `analysis/complexity_hint.py` → `compute_hint`, `function_hints`: yol çarpımı, bilinen çağrı maliyeti, aynı dosyadaki fonksiyonun ipucu, özyineleme (üstel şüphe / böl-yönet / yarılama), karşılıklı özyineleme; `confidence` + `basis`.
- `models/bigo.parse_cost` (amortize `1*`; soru bankası ve CLI de bunu kullanıyor — "Sonraya" maddesi kapandı). `models/facts.py`: `LoopFact.parent_line/parent_index/counter_outer`, `CallFact.loop_line/loop_index`, `RecursionFact.halving`, `CodeFacts.warnings`, `ComplexityHint.function`, `CallCostTable`.
- 15 golden vaka (`tests/golden/facts/{c,cpp,csharp,unity,unreal}-0N`), `--update-golden` (`tests/conftest.py`); 12 karmaşıklık fixture'ı (`tests/fixtures/complexity`, ilk satırda beklenti); toplam 966 test.
**Alınan kararlar (ve neden):**
- **Döngüler indeksle bağlanır** (`parent_index`, `loop_index`): aynı satırdaki iç içe döngüler (`for (...) for (...) s++;`) satır numarasıyla karışıp n² yerine n veriyordu.
- **Sınır sınıfı:** yön güncellemenin işaretinden; `CONSTANT` yalnızca başlangıç ve sınır ikisi de sabitse; sayaç tutarsız değişiyorsa (gövdede `i *= 2`, `i = 0`, hem `++` hem `--`) `UNKNOWN`. Bağlı liste gezintisi, `i * i <= n`, `while (true)` → `UNKNOWN`. Binary search `LOG` yalnızca uçlardan biri yarılanmış değerden türetilen atama alırsa.
- **İpucunda `UNKNOWN` = n varsayımı + `low` güven** (ipucu bir değer vermek zorunda; basis'te açıkça yazılı). `while` ile bulunan `LOG`, amortize maliyet, başka fonksiyonun ipucu → `medium`; özyineleme, dış döngüde sıfırlanmayan iç sayaç (two-pointer), üs taşması → `low`.
- **Özyineleme:** `Super::f()`, `Base::f()`, `base.f()`, `x.f()` öz-çağrı sayılmaz; `using std::swap;` (ADL) özyineleme değil; dallanma `if/else`/`?:`/`switch`'te max; döngü içindeki öz-çağrı dallanma ≥ 2 (permütasyon); `n - 1` argümanı varsa yarılama yok (üstel şüphe kapanmaz). Karşılıklı özyineleme Tarjan SCC ile; çağrılanlardan çağıranlara yinelemeli hesap.
- **Çağrı maliyeti yalnızca bildirilen tipten çözülür** (tip tablosu: değişken, alan, parametre, C# property; belirsiz ad çözülmez). Kullanıcı fonksiyonu tabloyu gölgeler. C# LINQ yalnızca bilinen koleksiyonda veya çağrı zincirinde; argümansız `First/Any` (ve koleksiyonda `Count`, listede `Last`) O(1). Büyük harfli, tipi bilinmeyen alıcı statik sınıf (`Mathf.Max` LINQ değil).
- **Dayanıklılık:** bölümler yalıtılmış (biri çökerse yalnızca o boş + uyarı); maliyet tablosu yoksa maliyetsiz devam; özyinelemeli yardımcılar yinelemeli ya da `RecursionError` korumalı; `compute_hint` istisna fırlatmaz.
- **Doğrusal süre (§12):** `Node.parent` (tree-sitter'da O(derinlik)) kullanılmaz; `operator: "+"` gibi anonim alanlı sorgu desenleri uzun zincirde karesel çıktı → filtresiz yakalayıp Python'da süzülüyor; atama dizini, dış döngü sıfırlama kümesi, fonksiyona göre gruplama önbellekli. 40 KB sınırındaki kötü niyetli girdiler (1300 iç içe döngü, 6000 terimli `+`, 7000 halkalı çağrı zinciri, 1300 fonksiyon) < 1 s.
- `×` işareti öğrenciye dönük gerekçelerde kullanıldığı için ruff `allowed-confusables`'a eklendi.
**Mimariden sapmalar (ADR linki):** yok. Model alanları geriye uyumlu, varsayılanlı genişletildi (rapor şemasında değiller). Planın `StaticFacts` adı yerine Faz 1'deki `CodeFacts` korundu.
**Denetim (kod-denetci):** Yüksek ×6 (gövdedeki ilgisiz `/2` LOG sayılıyordu; yön karşılaştırmadan çıkarılıp `i != 0; i--` CONSTANT oluyordu; `Mathf.Max`/property üzerinden sahte LINQ ve n² high; karşılıklı özyineleme `1 high`; `mid` argümanı üstel şüpheyi kapatıyordu; tek istisna tüm olguları siliyordu), Orta ×8 (dört karesel yol, uzun çağrı zincirinde `RecursionError`, döngüdeki öz-çağrı, kullanıcı `count`'unun `std::count` sayılması, Unreal metot bildirimlerinin `UObject*` alan sayılması, gövdedeki sayaç değişimi), Düşük ×7. Hepsi düzeltildi; `tests/unit/test_facts_review.py` her bulguyu sabitliyor. Kapsam dışı küçük dokunuşlar: `parse_cost` refaktörü (soru bankası/CLI), ruff'ın `--fix` ile kaldırdığı iki gereksiz `noqa` ve iki import sıralaması.
**Açık sorular:**
- Başka nesnenin aynı metodu (`child->visit()`) özyineleme sayılmıyor (çok biçimli çağrıdan ayırt edilemiyor); ağaç gezintilerinde ipucu düşük kalabilir.
- Unreal `FString(...) + TEXT(...)` birleştirmesi (metin sabiti yok) ve `TArray<TObjectPtr<...>>` kapsayıcı alanları yakalanmıyor.
- `make` hâlâ yok; kontroller `uv run ...` ile.
**Bu fazda öğrendiğim:**
- Golden anlık görüntüleri gözle incelemek şart: ilk turda `Super::BeginPlay()` özyineleme, `using std::swap` sahte özyineleme ve belirleyici olmayan sorgu sırası yalnızca incelemeyle çıktı.
- tree-sitter'da iki sessiz karesel tuzak: `Node.parent` kökten yürür; anonim düğümlü alan desenleri (`operator: "+"`) sol-derin zincirde karesel eşleşir.
- Bash heredoc'ları `\n`/`\b` kaçışlarını bozabiliyor (gerçek satır sonu, geri silme karakteri); büyük yamalar dosyaya yazılıp öyle çalıştırılmalı.

## Faz 6 (daraltılmış) — Notlar
**Kapsam:** Kullanıcı onayıyla 20 yerine motor + 10 kural. Kalan 10 statik kural (C-IO-001, C-UB-001, C-MEM-002, C-MEM-003, C-PERF-001, CPP-SP-001, CPP-PERF-001, CS-ALLOC-002, UNITY-PERF-002, UE-MEM-001) Faz 7–10'dan sonra eklenecek (bkz. Sonraya); `UYGULAMA_PLANI.md` Faz 6'ya not düşüldü.
**Yapılanlar:**
- `rules/base.py` (`Rule`, `RuleContext`: `line_text`, `function_nodes`, `hot_functions`, `types`, `in_loop`, `nodes_in`; `Rule.finding()`), `rules/registry.py` (`@register_rule`, §8.1 kimlik doğrulaması, yinelenen kimlik reddi, `applicable_rules`), `rules/engine.py` (`run_rules` → `RuleRunResult`), `rules/catalog.py`.
- Kurallar: `c.py` (C-BUF-001, C-MEM-001), `cpp.py` (CPP-OWN-001), `csharp.py` (CS-ALLOC-001, CS-PERF-001), `unity.py` (UNITY-GC-001, UNITY-PERF-001, UNITY-EVT-001), `unreal.py` (UE-GC-001, UE-PERF-001).
- Modeller: `models/rules.py` (`RuleInfo`, `RuleRunResult`, `RULE_ID_PATTERN`). Config: `[rules] disabled = []` (mimari §17'ye eklendi).
- CLI: `codementor rules list [--language --engine]`, `codementor rules doc --out`; `make rules-doc` → `docs/rules-catalog.md` (commit edilir; `test_committed_catalog_up_to_date`).
- 57 fixture (`tests/rules/fixtures/{RULE_ID}/{positive,negative}/`, `// EXPECT:` ve isteğe bağlı `// ENGINE:`), parametrik `test_all_rules.py`, `test_registry.py`, `test_engine.py` (6 kötü niyetli 40 KB girdi < 0,4 s), `test_cli_rules.py`. Toplam 1070 test.
**Alınan kararlar (ve neden):**
- **Motor dayanıklılığı:** çöken kural yalnızca Türkçe uyarı üretir; aynı kural aynı satırda tek bulgu; bulgular satır sırasıyla `F-001…` numaralanır; kanıt ≤ 200 karakter. Yapılandırmadaki bilinmeyen kimlik (yazım hatası) uyarı verir.
- **Filtre:** düz C# kuralları Unity kodunda da çalışır (Unity C#'tır); motora özgü kural yalnızca o motorda. C kuralları yalnızca C'de.
- **C-MEM-001 muhafazakâr kaçış analizi** (fonksiyon içi; fonksiyonlar arası yok): tek geçiş + açık yığın, her düğüm "kaçış bağlamı" bayrağı taşır (`return`, tahsis olmayan atama/ilk değerin sağı, `free`, sahiplenmediği bilinmeyen fonksiyonun argümanı). `p[0]`, `p->x`, `*p`, `p == NULL`, `sizeof` değer bağlamıdır (kaçış değil). Takma ad (`q = p`, `head = node`, `{ p, n }`) izlenmez → bulgu yok. Yanlış bulgu yerine kaçırma tercih edildi.
- **Olgular satır taşıdığından** aynı satırda karışma oluyordu: CS-ALLOC-001 düğüm düzeyinde çalışır (döngü gövdesi bayt aralıkları + `bisect`, `Node.parent` yok; hedefin string olduğu tip tablosundan ya da metin sabitinden). UNITY-EVT-001 `+=`'i yalnızca olgudaki (satır, hedef adı) ile eşleşirse abonelik sayar.
- **UNITY-EVT-001:** kaldırma `OnDisable`/`OnDestroy`/`Dispose` ve bunların doğrudan çağırdığı aynı dosyadaki metotlarda (tek seviye) aranır; `RemoveAllListeners` lambda aboneliklerini de kapsar; `new Action(H)` ↔ `H`; lambda abonelik ayrı açıklamayla (kaldırılamaz).
- **UNITY-PERF-001:** yalın `Find`/`FindWithTag` sayılmaz (kullanıcı metodu, `list.Find`); yalnızca `GameObject.Find*`. `Camera.main` ve `UnityEngine.Camera.main` alanlarla, kısa düğümde metin alınarak.
- **CS-PERF-001** yalnızca tip tablosunun `List/Array/LinkedList/Queue/Stack` olarak çözdüğü çağrılarda (maliyet `n`); `HashSet`/`Dictionary` bulgu vermez.
- **CPP-OWN-001** placement new'i saymaz. **UE-GC-001** = `uobject_fields − uproperty_fields`. **UE-PERF-001:** Tick/TickComponent'te en dıştaki döngü, O(1) olmayan bilinen maliyetli ya da ağır Unreal çağrısı (`GetAllActorsOfClass`, `SpawnActor` …), döngü dışı heap tahsisi.
- Kural açıklamaları öğrenciye dönük ve soru biçiminde (kodu düzeltmez; Sokratik ilke).
**Mimariden sapmalar (ADR linki):** yok. §17'ye `[rules] disabled` eklendi (kabul kriteri gereği; yeni bileşen değil).
**Denetim (kod-denetci):** Yüksek ×2 — (Y1) C-MEM-001 iç içe girdide karesel (27 KB'da 106 s → 0,37 s), (Y2) takma ad görülmediği için bağlı liste kurma kodunda yanlış bulgu. Orta ×6 — `Camera.main` aramasında karesel süre (3,5 s → 0,23 s), `RemoveAllListeners` varken lambda bulgusu, yardımcı metotta/`Dispose`'da kaldırma görülmüyordu, satır bazlı eşleşmeyle yanlış bulgu (sayısal `+=`, `count += 1`), `var s = ""`/`this.log +=`/başa ekleme kaçırılıyordu, kullanıcının `Find` metodu yanlış bulgu. Düşük (uygulanan) — `return p[0]`/`return p != NULL` sızıntıyı gizliyordu, placement new, `TryGetComponent`, `UnityEngine.Camera.main`, `new Action(H)`, bilinmeyen kapatılmış kimlik uyarısı, `RULE_ID` tek kaynak, CS-PERF açıklaması `Remove`'u kapsıyor, testte `parsed=None`. Hepsi regresyon fixture'ı veya testle sabitlendi. Kapsam dışı küçük dokunuşlar (Faz 5 kökenli O5): `_symbols._csharp_bindings` `var s = "..."` → `string`; `_memory` `+=` hedefinde `this.` öneki atılır (golden'lar değişmedi).
**Açık sorular:**
- Sıcak yol yalnızca adla belirleniyor (Faz 5): MonoBehaviour olmayan sınıftaki `Update`, UCLASS olmayan sınıftaki `Tick` de sıcak sayılır.
- `make` hâlâ yok; kontroller `uv run ...` ile.
**Bu fazda öğrendiğim:**
- "Alt ağaçtaki adları topla" yardımcısını her düğümde çağırmak iç içe girdide sessizce karesel olur; bağlamı yığında bayrak olarak taşımak tek geçişte aynı bilgiyi verir.
- Olgu (satır) ile ağaç düğümünü satır numarasıyla eşlemek aynı satırdaki iki ifadeyi karıştırıyor; kurallar ya olgunun kimliğini (satır + ad) doğrulamalı ya da düğüm düzeyinde çalışmalı.
- Bash heredoc'ları yine `\n` kaçışlarını bozdu; çok satırlı düzenlemeler Edit/Write ile.

## Faz 7 — Notlar
**Yapılanlar:**
- `models/provider.py`: `ChatMessage`, `GenerationOptions`, `TokenUsage`, `ProviderCapabilities`, `ProviderResult` (§5.5.1 + `provider`, `warnings`), `ProviderStatus`.
- `providers/base.py` (`LLMProvider` Protocol, hata hiyerarşisi, `RetryPolicy`), `_http.py` (ortak HTTP katmanı), `_common.py`, `schema_adapter.py`, `fake.py`, `ollama.py`, `openai_compat.py` (OpenAI + DeepSeek), `anthropic.py`, `factory.py` (`build_provider`, `build_chain`, `FallbackProvider`).
- `log.py`: structlog JSON + `redact_secrets`; `get_logger` global yapılandırmadan bağımsız maskeleyen logger döndürür.
- CLI: `codementor providers check [--provider]` (Ollama `GET /api/tags` ile gerçekten sorgulanır; bulut ağsız). Bağımlılıklar: `httpx`, `structlog`; geliştirme: `respx`. Async testler anyio eklentisiyle.
- Config: sağlayıcı başına alt sınıflar (`OllamaConfig` ... TOML'da bölüm kısmen verilse de varsayılanlar korunur), `providers.max_retries`, bulut `timeout_s = 60`, `max_tokens`; `pytest` `addopts`'a `-m "not live"`.
- Testler: `tests/providers/` — `contract.py` + `test_contract.py` (**5 adaptör × 25 senaryo** tek sözleşme paketi, respx), `test_adapters.py`, `test_schema_adapter.py`, `test_factory.py`, `test_fake.py`, `test_log_redaction.py`, `test_http_hardening.py`; `tests/unit/test_cli_providers.py`; `tests/live/test_providers_live.py` (`@pytest.mark.live`). Toplam 1304 test.
**Doküman doğrulaması (kaynaklar, 2026-09-29):**
- Ollama — `POST /api/chat`, `format` = JSON Schema, `options.num_ctx/temperature/seed`, `stream:false`; yanıt `message.content`, `done_reason`, `prompt_eval_count`, `eval_count`: https://docs.ollama.com/capabilities/structured-outputs
- OpenAI — Chat Completions `response_format: {type: "json_schema", json_schema: {name, schema, strict: true}}`; katı mod: tüm alanlar `required`, `additionalProperties: false`, opsiyonel = null birliği: https://developers.openai.com/api/docs/guides/structured-outputs , https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create
- DeepSeek — yalnızca `response_format: {type: "json_object"}` (json_schema yok); prompt "json" sözcüğü ve örnek biçim içermeli; boş içerik dönebilir: https://api-docs.deepseek.com/guides/json_mode
- Anthropic — `output_config: {format: {type: "json_schema", schema}}`, beta başlığı yok; JSON `text` bloğunda; `minLength/maxLength/pattern/minimum/maximum` desteklenmez; güncel modeller zorunlu `tool_choice` ve `temperature`'ı reddeder: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
**Alınan kararlar (ve neden):**
- **ADR-0011:** Anthropic'te zorunlu `tool_choice` yerine `output_config.format` (güncel modeller zorunlu `tool_choice`'u 400 ile reddediyor); `temperature` yalnızca açıkça yapılandırılmışsa, `seed` hiç gönderilmez. Mimari §5.5.2/§5.5.3/§17/§20 ve UYGULAMA_PLANI Faz 7 kriteri güncellendi.
- **SchemaAdapter:** `$ref` açılır (özyinelemeli şema reddedilir), sağlayıcıların zorlamadığı kısıtlar (`minLength`, `maxLength`, `pattern`, `minimum`, `maximum`, `maxItems`, `minItems>1`) API şemasından çıkarılır — K5 aynı Pydantic modeliyle doğrular. OpenAI katı varyantı her nesnede tüm alanları `required` yapar, opsiyonelleri `anyOf[T, null]`'a çevirir. DeepSeek prompt şeması kısıtları **korur** (API zorlamadığı için modelin sınırları görmesi gerekir).
- **Yeniden deneme:** yalnızca ağ/zaman aşımı/429/5xx (529 dahil), en fazla `providers.max_retries` (2); üstel geri çekilme + jitter; `Retry-After` sonlu ve ≥ 0 ise ona uyulur, `max_delay_s`'ten (20 sn) uzunsa beklemeden bırakılır (kota → fallback). Diğer 4xx ve işlenemeyen yanıt (`ProviderResponseError`) hemen hata.
- **Fallback:** her `ProviderError`'da (eksik anahtar/model dahil) sıradakine geçilir, `ProviderResult.warnings`'e Türkçe uyarı yazılır; bozuk JSON geçiş sebebi değil (onarım Faz 9). Hepsi düşerse `AllProvidersFailedError`.
- **HTTP güvenliği (§12):** toplam süre sınırı (`asyncio.timeout`, httpx'in faz başına zaman aşımına ek), yanıt ≤ 4 MB akışla okunur, `accept-encoding: identity`, derin JSON (`RecursionError`) güvenle "çözülemedi", istisnalar `from None` (httpx istek nesnesi `x-api-key` taşır), hata metni önce maskelenip sonra kırpılır, anahtar yerel olmayan adrese yalnızca https ile gider.
- **Log maskeleme:** gizli alan adları son parçada tam eşleşir (`x-api-key`, `access_token` evet; `input_tokens`, `max_tokens` hayır), kayıtlı anahtar değerleri ve `Bearer`/`sk-` desenleri tüm metinlerde ve sözlük anahtarlarında maskelenir; varsayılan düzey WARNING (CLI sade), HTTP olayları DEBUG.
- **Ollama:** `num_ctx` her istekte (yapılandırılmamışsa 16384). **OpenAI:** `max_completion_tokens`; **DeepSeek:** `max_tokens`, `seed` gönderilmez.
- Canlı testler ayrı dizinde (`tests/live/`): sağlayıcı testlerindeki sahte anahtar fikstürü gerçek anahtarları ezmesin.
**Mimariden sapmalar (ADR linki):** [ADR-0011](docs/adr/0011-anthropic-yapilandirilmis-cikti.md) — Anthropic `output_config.format`, `tool_choice` yok.
**Denetim (kod-denetci, güvenlik odaklı):** Yüksek ×1 — derin iç içe JSON'da `RecursionError` fallback zincirinden ve K5'ten kaçıyordu (prompt injection ile tetiklenebilir). Orta ×9 — `Retry-After: nan` sonsuz bekleme; `httpx.DecodingError` kaçıyordu; istisna zinciri (`__cause__`) API anahtarını taşıyordu; hata metni maskelemeden önce kırpılıp anahtar öneki sızıyordu; `token` deseni token sayaçlarını da maskeliyordu; başka bir structlog yapılandırması maskelemeyi devre dışı bırakıyordu; toplam süre sınırı yoktu; DeepSeek prompt şeması kısıtları taşımıyordu; sözleşme testi gönderilen modeli doğrulamıyordu. Düşük (uygulanan) — sıkıştırma bombası (`identity`), düz HTTP'ye anahtar, sağlık kontrolünde 120 sn zaman aşımı ve adresteki kimlik bilgisinin basılması, düz `pytest`'in canlı testleri çalıştırması, ağsızlık testinin zayıflığı, Fake'te `response` hata türü ve negatif gecikme, sözlük anahtarlarının maskelenmemesi, gerekçesiz `type: ignore`. Hepsi düzeltildi ve regresyon testiyle sabitlendi (`test_http_hardening.py`, `test_log_redaction.py`, sözleşme eklemeleri).
**Açık sorular:**
- **Canlı doğrulama yapılmadı:** bu makinede Ollama kurulu ama kapalı; bulut modelleri/anahtarları tanımlı değil. ADR-0011'deki Anthropic iddiaları ve Ollama `format` davranışı birleştirmeden önce `uv run pytest -m live -k ollama` / `-k anthropic` ile en az bir kez gerçek çağrıyla doğrulanmalı.
- `FallbackProvider.capabilities` ilk sağlayıcınınkini gösterir; fallback'te yanıt veren sağlayıcının yeteneği farklı olabilir. K5 (Faz 9) şemanın zorlanıp zorlanmadığını `result.provider` üzerinden çözmeli.
- `make` hâlâ yok; kontroller `uv run ...` ile.
**Bu fazda öğrendiğim:**
- Sağlayıcı API'leri hızla değişiyor: mimari yazılırken doğru olan "zorunlu `tool_choice`" yolu güncel modellerde 400 veriyor. Adaptör kararları kaynak linkiyle ve tarihle kaydedilmeli, canlı testle doğrulanmalı.
- Güvenlik açısından istisna zinciri de bir veri kanalı: httpx istek nesnesi `x-api-key`'i açık taşıyor ve `repr` bunu gizlemiyor; `from None` ucuz bir savunma.
- "Maskeleme yapılandırmada" tasarımı kırılgan: global yapılandırmayı başka bir kütüphane değiştirebilir. Maskelemeyi logger'ın kendisine gömmek daha sağlam.
- Bash heredoc'ları bu fazda iki kez daha bozuldu (tek tırnaklı Türkçe metin); çok satırlı yamalar Write ile betik dosyasına yazılıp çalıştırıldı.

## Faz 7 eki — CLI ajanları ve canlı sağlayıcı denemeleri (ADR-0012)
**Yapılanlar:**
- `providers/cli_agent.py` → `CliAgentProvider` (`claude_cli`, `agy`): tüm mesajlar stdin'den, PATH'te yalnızca mutlak dizinlerde arama, `.cmd` → `.exe` çözümü, Faz 4 `run_process` ile yalıtım; Claude'da araçlar kapalı. Config: `CliConfig`/`ClaudeCliConfig`/`AgyConfig` (`command`, `allow_tool_agent`), `OllamaConfig.think`. `ProcessLimits.max_processes`, `file_size_bytes`. `providers check` CLI profillerini ağsız denetler. Sözleşme paketine `CliHarness` (6 adaptör).
- SchemaAdapter: Ollama varyantı kısıtları korur; diğer varyantlarda zorlanamayan kısıtlar alan açıklamasına Türkçe not olarak eklenir ("en fazla 80 karakter").
**Canlı denemeler (2026-09-29, EnemyRadar / unity-03, Geçiş A + B):**
- `claude_cli` (claude-opus-5-5): Geçiş A ~32 sn. 33. satırdaki mantık hatasını (`nearby` ⊂ `enemies` → koşul hiç doğru değil) ve `enemies`'in hiç doldurulmadığını buldu; kanıtlar birebir; Geçiş B şemaya uyuyor, çözüm sızmıyor. Kısıt notları eklenmeden önce 8 soru ve 80+ karakterlik kavram yazıyordu.
- `ollama` / `deepseek-r1:8b`: kısıtlar şemadan çıkarılınca `maxLength` aşıldı → Ollama varyantı kısıtları koruyor, canlı test geçti. Geçiş A 120 sn zaman aşımı ×3; 600 sn ile tamamlandı, 8/16 (kanıtlar `"Line 18: ..."` önekli, statik bulguları tekrar, 33. satırı kaçırdı, B'de çözümü söyledi). `think=false`: 187 sn, 12.440 çıktı token'ı, 12/16 (B temiz, 33. satır yine kaçırıldı).
- `agy`: bu ortamda oturum açılmamış; `status: SUCCESS`, `response: ""` dönüyor → adaptör "oturum açık mı?" hatası verir.
**Faz 8/9 için dersler:** kanıt denetimi bulgunun satır aralığına bakmalı (`line_start..line_end`); sızıntı denetimi öğrencinin kendi kodundan yapılan alıntıları (`enemies.Contains(...)`) sızıntı saymamalı; Türkçe düzyazıdaki `;` kod değildir; LLM karmaşıklığı "O(n^2) per frame" gibi ekler taşıyabilir (normalizasyon); küçük yerel modeller için prompt kanıt biçimini ve "statik bulguları tekrar etme"yi örnekle göstermeli.
**Denetim (kod-denetci, güvenlik):** Yüksek ×1 — Windows'ta `shutil.which` çalışma dizinine önce bakıyordu (öğrenci projesindeki `claude.exe` kullanıcının oturumuyla çalışabilirdi). Orta ×6 — sistem mesajı argv'deydi; agy'de sistem mesajı kayboluyordu; agy için `--mode plan` ve açık onay yoktu; Claude'da katmanlı savunma bayrakları eksikti; zaman aşımı yeniden denemesi fallback'i ~15 dk geciktirebiliyordu; POSIX'te 1 MB dosya sınırı CLI'yi öldürebilirdi. Düşük — `.cmd` hedefinde `..`, `modelUsage` çoklu model, sahte JSON satırı seçimi, stderr kesilmesinin geçerli stdout'u düşürmesi, `assert` ile tip daraltma, `Runner` Protocol, sabit süreç sayısı, şema docstring'i, `command`/`think`'in ortak config'te olması, `ya29.` jeton deseni. Hepsi düzeltildi ve `test_cli_agent.py`'de sabitlendi.
**Açık sorular:**
- agy canlı doğrulanmadı (oturum yok): stdin'den okuma ve izin istekleri davranışı.
- Faz 4 `run_process` de `argv[0]`'ı çıplak adla CreateProcess'e veriyor (derleyiciler); aynı cwd araması riski orada da var (bkz. Sonraya).
- `deepseek-r1:8b` bu makinede uzun prompt'ta 3 dk+; yerel varsayılan model seçimi Faz 12 eval'ine kadar açık.

## Faz 8 — Notlar
**Yapılanlar:**
- Şablonlar (`prompts/v1/`, Jinja2, `StrictUndefined`): `analysis.{system,user}.j2`, `socratic.{system,user}.j2`, `single_pass.{system,user}.j2`, `repair.user.j2`; ortak parçalar `_core_rules.j2` (§5.4.4'ün 7 kuralı + Türkçe açıklama kuralı), `_mentoring_rules.j2`, `_macros.j2` (soru, kod, ipucu, statik bulgular, olgu özeti, kontrol listesi, few-shot, mentorluk ayarı). Python'da prompt metni yok.
- Few-shot'lar: `prompts/v1/fewshots/{c_none,cpp_none,csharp_none,csharp_unity,cpp_unreal}_*.yaml` (dil/motor başına 1). Her örnekte statik ipucu, statik analizin zaten bulduğu bulgular ve bunları **tekrar etmeyen**, kanıtı satırdan birebir alıntılayan doğru yanıt var; biri (`csharp_none`) `agreement: conflicts` gösteriyor.
- `src/codementor/prompts/`: `templates.py` (ortam, `guard_delimiters`, `prompt_version`), `budget.py` (`estimate_tokens` = ⌈karakter/3⌉, `context_budget`, `fit_to_budget`, `PromptBudgetError`), `fewshot.py` (yükleme + kanıt doğrulama + seçim), `summary.py` (`digest_facts`: `full`/`brief`), `mentoring.py` (§5.4.3), `builder.py` (`build_analysis_messages`, `build_socratic_messages`, `build_single_pass_messages`, `build_repair_messages`), `_demo.py` (`python -m codementor.prompts.builder --demo <soru> [--code] [--mode]`).
- Modeller: `models/prompts.py` (`QuestionContext`, `MentoringProfile`, `FewShotExample`, `FactsDigest`, `AnalysisPromptInput`, `SocraticPromptInput`, `BuiltPrompt`), `models/llm_output.LLMSinglePassOutput` + `schemas/llm_single_pass.schema.json`.
- Config: `[prompts]` (`dir`, `default_context_tokens`, `reserve_output_tokens`, `max_fewshots`, `max_checklist_items`), sağlayıcılarda `context_tokens`; mimari §17 güncellendi. Bağımlılık: `jinja2`.
- Testler: `test_prompt_builder.py`, `test_prompt_budget.py`, `test_fewshot.py`, `test_facts_summary.py`, `test_mentoring_profile.py`; golden `tests/golden/prompts/{unity-hard-inventory,c-medium-linked-list,free-cpp}` × {analysis, single_pass, socratic}. Toplam 1442 test (denetim sonrası 1468).
**Kabul kriterleri:**
- [x] Kod her zaman `<user_code>` içinde ve numaralı görünümde — `test_code_inside_user_code_numbered`, golden; koddaki `</user_code>` kaçışlanıyor (`test_user_code_delimiter_escaped`, `free-cpp` vakası).
- [x] Sistem prompt'u §5.4.4 çekirdek kurallarını içeriyor — `test_system_prompt_has_core_rules` (analysis + single_pass), `test_socratic_system_forbids_solution`.
- [x] Referans çözüm hiçbir prompt'ta yok — `test_reference_solution_never_in_prompt` (çözüm dosyası okunabilir durumdayken benzersiz satır ve yol aranıyor); `QuestionContext` bu alanı yapısal olarak taşımıyor.
- [x] Bütçe aşımında few-shot → kontrol listesi → olgular (→ kural bulguları) sırasıyla kırpılıyor; kod sığmazsa istisna — `test_trim_order_*`, `test_facts_trimmed_before_static_findings`, `test_code_never_trimmed_and_too_large_raises`, `test_budget_trims_fewshots_first`, `test_code_too_large_raises`.
- [x] Zorluk → ipucu seviyesi tablosu (§5.4.3) — `test_mentoring_profile.py`, `test_socratic_uses_mentoring_profile`.
- [x] Şablon değişince `prompt_version` değişiyor — `test_prompt_version_changes_when_template_changes` / `_fewshot_changes`; satır sonu farkı değiştirmiyor.
- [x] `single_pass` modu destekleniyor — `build_single_pass_messages`, `LLMSinglePassOutput`, `test_single_pass_messages`, golden.
**Alınan kararlar (ve neden):**
- **`prompt_version` = `"<dizin adı>+" + sha256(şablonlar + few-shot'lar)[:8]`**: few-shot'lar da prompt'u değiştirdiği için hash'e dahil; CRLF → LF normalize (Windows ve CI aynı sürümü üretsin).
- **Bütçe:** bağlam = sağlayıcının `context_tokens` → `num_ctx` → `prompts.default_context_tokens`; çıktı payı = `max_tokens` → `reserve_output_tokens`; şema tokenları API'de gitse de düşülür. Sayım sağlayıcıdan bağımsız ve temkinli (3 karakter/token). Kırpma kademeli: few-shot'lar tek tek, kontrol listesi yarı → yok, olgular tam → kısa → yok, kural bulguları açıklamalı → yalnız kanıt → yalnız sayı. Sokratik geçiş kırpılmaz (sığmazsa istisna).
- **Olgular tam JSON değil:** `digest_facts` süzer (O(1) ve maliyeti bilinmeyen çağrılar gürültü; `brief` yalnızca sıcak yol/iç içe yapılar), metni şablon üretir.
- **Few-shot'lar yüklenirken doğrulanır:** kanıt `line_start..line_end` aralığında birebir geçmeli (`"Line 3:"` önekli kanıt reddedilir), statik bulgu tekrarı reddedilir. Ayrıca `test_repo_fewshots_match_static_engine` örnekteki statik bulguların ve ipucunun **gerçek motor çıktısıyla aynı** olduğunu doğrular. İlk taslakta Unity örneği `GetComponent` sorununu LLM bulgusu olarak gösteriyordu, oysa UNITY-PERF-001 onu zaten buluyor: örnek tekrarı öğretiyordu.
- **Sınırlayıcı koruması (§12):** kullanıcı kaynaklı her metin (kod görünümü, kanıtlar, açıklamalar, adlar) `guard` ile `&lt;/user_code>` biçimine çevrilir; soru metni güvenilir veri (soru bankası).
- **Sokratik geçişte `hint_ladder[seviye]`** "aynen kopyalama, uyarlayarak kullan" notuyla verilir; `name_concept = false` iken kavram adı yalnızca `key_flaw_concept` alanına yazılır.
- **Serbest mod:** zorluk varsayılanı orta; kontrol listesi yalnızca `core` maddeler.
**Denetim (kod-denetci):** Yüksek yok. Orta ×7 — (O1) bütçe yalnızca tek sağlayıcıya göre hesaplanıyordu, `claude_cli` + fallback `ollama` zincirinde 28k token'lık prompt 16k bağlama gidip sessizce kesilebilirdi → zincirin en darı, bilinmeyen ad `PromptConfigError`; (O2) 40 KB sınırındaki kod varsayılan sağlayıcıda reddediliyordu, fonksiyon ipuçları kırpılamıyordu ve hata kodu suçluyordu → ipuçları olgu kademesine bağlandı, hata kodun mu geri kalanın mı taştığını söylüyor, Anthropic/Claude CLI için `context_tokens = 200000`; (O3) onarım prompt'u bütçeyi denetlemiyordu → ham yanıt kalan yere göre kırpılıyor, yer yoksa istisna; (O4) onarım hataları çerçevesiz user mesajıydı → `<validation_errors>` veri çerçevesi, `guard`, `repair_errors()` `input_value` vermiyor; (O5) sınırlayıcı koruması Unicode varyantlarını (sıfır genişlikli boşluk, Kiril harf, tam genişlikli ayraç) kaçırıyordu → görünmez karakter atan + NFKC + benzer harf katlayan iskelet üzerinde eşleşme, çekirdek kurallara yapısal kural (kod yalnızca kendi satırındaki `</user_code>` ile biter); (O6) few-shot soruları satır numarası veriyordu (seviye 1 ile çelişki) → yeniden yazıldı, testle sabit; (O7) kırpma kademeleri gerçek şablonda test edilmiyordu → `test_prompt_render.py`. Düşük (uygulanan) — `prompt_version` uzantısı büyük/küçük harf duyarsız, `O(1*)` → "O(1) amortize", mimari §5.4.3 "itibaren", statik bulgunun satırına yeni bulgu reddi, kesişim örneği `O(n*m)`, eksik few-shot dizini log uyarısı, bozuk bağlam ayarı yapılandırma hatası, test dosyası bölündü (`prompt_helpers.py`, `test_prompt_render.py`, `test_prompt_version.py`) ve `type: ignore`'lar kaldırıldı, PROGRESS'teki çift satır, §6.3'e `LLMSinglePassOutput`. Ertelenen: D2 (`prompt_version` her build'de dosyaları okur; Faz 10'da mtime önbelleği), D3 (kaçışlanmış kanıt Faz 9'da ters çevrilmeli), D8 (göreli `prompts.dir`).
**Mimariden sapmalar (ADR linki):** yok. §5.4.2'de şeması tanımlanmamış tek geçiş için `LLMSinglePassOutput` (= analiz + Sokratik) eklendi; §17'ye `[prompts]` ve `context_tokens` eklendi (yeni bileşen değil, boşluk doldurma).
**Açık sorular:**
- `name_concept = false` iken `key_flaw_concept` raporda öğrenciye gösterilmeli mi? Faz 10 (pipeline/rapor) karar vermeli.
- 3 karakter/token tahmini Türkçe + kod için kaba; Faz 12 eval'de gerçek `usage` ile kalibre edilmeli.
- Prompt'lar bu fazda canlı denenmedi (kullanıcı isteğiyle Ollama kullanılmadı); `claude_cli` ile uçtan uca deneme Faz 9/10'da.
- Golden vakalarda görülen Faz 5 sınırı: `RemoveAll(...)` maliyet tablosunda yok, `Remove: O(1)` ipucu çıkıyor.
- `make` hâlâ yok; kontroller `uv run ...` ile.
**Bu fazda öğrendiğim:**
- Few-shot'lar da test edilmesi gereken veri: gerçek statik motorla karşılaştırılmadan yazılan "doğru yanıt" örneği, modele tam da yapmamasını istediğimiz şeyi (statik bulguyu tekrar) öğretiyordu.
- Görev metninde `<user_code>` etiketini düz yazıyla anmak sınırlayıcı sayısını bozuyor; talimatlarda etiket adı yerine "öğrencinin kodu" demek daha güvenli.
- Bash heredoc'ları Türkçe metinde yine bozuldu; PROGRESS güncellemesi betik dosyasıyla yapıldı.

## Faz 9 — Notlar
**Yapılanlar:**
- `src/codementor/verify/`: `schema_check.py` (`check_schema`, `extract_json`: ``` çiti / düz yazı içinden tek geçişte JSON), `lines.py` (`check_line_range`, `match_evidence`, `normalize_evidence`), `complexity.py` (`normalize_complexity`, `resolve_conflict`, `is_optimal`, `check_complexity`), `merge.py` (`merge_findings`, `number_findings`), `leak_guard.py` (`check_leaks`, `code_violations`, `decide_leak_action`), `confidence.py` (§5.6 formülü + bulgu başına güven), `analysis.py` (`verify_analysis`, `verify_socratic`: kontrolleri sırayla çağıran ince birleştirici).
- Modeller: `models/verification.py` (`SchemaCheck`, `EvidenceMatch`, `ComplexityCheck`, `LeakViolation`, `LeakCheck`, `LeakDecision`, `RepairRequest`, `AnalysisVerification`, `SocraticVerification`, `CommonIdentifiers`). Config `[verify]` (mimari §17). Veri: `data/leak_common_identifiers.yaml`.
- Halüsinasyon fixture'ları `tests/fixtures/llm_responses/`: **2 gerçek claude_cli yanıtı** (EnemyRadar / golden unity-03, Faz 8 prompt'uyla; Geçiş A 21 sn, B 7 sn) + onlardan türetilmiş 9 sentetik vaka (yanlış satır, var olmayan kanıt, `Line 23:` önekli kanıt + statik tekrar [Faz 7 deepseek gözlemi], gerekçesiz/gerekçeli çatışma, `per frame`, ayrıştırılamayan karmaşıklık, yasaklı tanımlayıcı, kod bloğu, öğrenci alıntısı) + test referans çözümü `unity03_reference.cs`.
- Testler `tests/unit/verify/` (148): her §5.6 satırı için pozitif + negatif, hypothesis ile güven skoru. Toplam 1616 test.
**Kabul kriterleri:**
- [x] §5.6 tablosundaki her kontrol için pozitif ve negatif test — şema (`test_schema_check.py`), satır aralığı + kanıt (`test_lines.py`), Big-O + çatışma (`test_complexity.py`), birleştirme + önem (`test_merge.py`), sızıntı (`test_leak_guard.py`).
- [x] Kanıtı 1 satır kaymış bulgu düzeltiliyor; kanıtı hiç olmayan atılıyor + uyarı — `test_shift_within_two_lines_corrected`, `test_missing_evidence_not_found`, `test_dropped_findings_warn_in_turkish_and_lower_confidence`, fixture `wrong_line`, `missing_evidence`.
- [x] Gerekçesiz çatışma → onarım talebi; gerekçeli çatışma → kabul + düşük güven — `test_unjustified_conflict_requests_repair`, `test_justified_conflict_accepted`, fixture `conflict_unjustified` / `conflict_justified` (güven 0.85).
- [x] Statik ve LLM aynı sorunu bulunca tek `confirmed` bulgu — `test_same_issue_becomes_single_confirmed`, `test_static_and_llm_merge_confirmed`, fixture `prefixed_evidence_and_repeat`.
- [x] Sızıntı: kod bloğu, referansla yüksek 5-gram örtüşmesi ve yasaklı tanımlayıcı ayrı ayrı yakalanıyor — `test_code_block_detected`, `test_ngram_overlap_detected` (yasaklı ad kapalıyken), `test_forbidden_identifier_detected`; negatifler (Türkçe `;`, öğrenci alıntısı, genel adlar, soru metnindeki adlar).
- [x] Güven skoru 0–1 aralığında ve formüle uygun (hypothesis ile) — `test_always_in_unit_interval_and_matches_formula`.
**Alınan kararlar (ve neden):**
- **Doğrulayıcılar saf:** onarımı değil kararı döndürür (`RepairRequest`, `LeakDecision.action`); LLM'i ve `private/` okumayı Faz 10 pipeline'ı yapar. Referans çözüm metin olarak verilir.
- **Kanıt araması:** `line_start..line_end ± evidence_window` (varsayılan 2); bildirilen satıra en yakın eşleşme seçilir; önek atılmış hali bulunamazsa ham hali de denenir (`0 | FLAG` gerçek kod olabilir); `...` parçalar sırayla aranır; en az 2 anlamlı karakter. Aralık dışı ya da kanıtı olmayan bulgu atılır + Türkçe uyarı (onarım istenmez; §5.6 onarımı yalnızca şema/karmaşıklık için ister).
- **Gerekçeli çatışma = `agreement == "conflicts"`** (şema en az bir `reasoning_steps` adımı zorunlu kılıyor); aynı sınıftaysa "conflicts" dense bile uyum. Gerekçesiz çatışmada karmaşıklık rapora yazılmaz (onarım bekler). `O(...)` yazılmışsa yalnızca içi ayrıştırılır: yarım `O(n` artık `o` değişkeni sanılmaz.
- **Birleştirme:** her LLM bulgusu en yakın eşleşmemiş statik bulguyla birleşir; bir statik bulgu en fazla bir LLM bulgusunu emer; LLM'in kendi tekrarları atılır. Güven: LLM 0.7 (satır doğru) / 0.6 (düzeltilmiş), confirmed ≥ 0.95. LLM bulgu vermediyse kanıt oranı 1.
- **Sızıntı:** kod deseni her zaman kod sözdizimi ister; atamada sağ taraf da kod gibi olmalı (ASCII, tek token ya da işaret içeren) — ilk uygulamada "i = n olduğunda ne olur;" kod sayılıyordu. Öğrenci alıntısı boşluksuz karşılaştırmayla serbest. n-gram'da öğrenci kodunda da geçen n-gram'lar ve referanstaki yorum/metin sabitleri sayılmaz; tanımlayıcı Türkçe sözcüğün parçasıysa (`Listeyi`) sayılmaz. Eşik varsayılanı 0.2 (config).
- **§12 doğrusal süre:** JSON çıkarma tek geçişli yığın (400 K `{` < 2 sn), kanıt aramasında eşleşme sayısı sınırlı, soru/ipucu 1000 karakteri aşarsa `too_long` ihlali (ölçüm: kod regex'leri 32 K karakterde 15 sn sürüyordu).
**Mimariden sapmalar (ADR linki):** yok. §16'ya `verify/analysis.py` (birleştirici), §17'ye `[verify]`, §5.6'ya uygulama notları eklendi; `LeakKind`'e `too_long` eklendi.
**Canlı gözlem (claude_cli, 2026-09-30):** Faz 8 prompt'u ilk kez canlı denendi. 7 LLM bulgusunun kanıtının tümü kodda, tek satır kayması (17→18) düzeltildi, statik bulgular tekrar edilmedi, karmaşıklık `O(n^2)` ipucuyla uyumlu; Geçiş B 33. satırdaki mantık hatasına çözümü söylemeden yönlendiriyor ve referans çözümle karşılaştırıldığında temiz.
**Açık sorular:**
- **`reasoning_steps` sızıntısı:** canlı Geçiş A yanıtında bir adım "hash tabanlı bir yapı kullanılırsa kare başına O(n) mümkün" diyor. §5.6 sızıntı korumasını yalnızca Sokratik bölüme uyguluyor; `reasoning_steps` rapora (öğrenciye) gidiyorsa Faz 10'da ya gizlenmeli ya da aynı korumadan geçmeli.
- `key_flaw_concept` (Faz 8'den) ve LLM bulgu açıklamaları da sızıntı denetimine girmiyor; açıklamalar "hash tabanlı..." gibi çözüm önerebilir.
- Yasaklı tanımlayıcı listesi referans çözümün kalitesine bağlı; eval (Faz 12) yanlış pozitif/negatifleri ölçmeli, `leak_ngram_threshold` orada ayarlanmalı.
- `make` hâlâ yok; kontroller `uv run ...` ile.
**Bu fazda öğrendiğim:**
- Gerçek yanıt kaydetmek sentetik fixture'dan daha çok şey öğretti: kanıt biçimi Faz 8 örnekleriyle birebir oturmuş, ama asıl sızıntı riski beklenmedik yerde (`reasoning_steps`) çıktı.
- Regex tabanlı "kod mu?" sezgisi Türkçe düzyazıda kolayca yanılıyor; her desen için Türkçe negatif fixture şart.
- Sınırsız uzunluktaki model çıktısına regex uygulamak karesel süre tuzağı; ölçmeden fark edilmiyor.

## Faz 10 — Notlar
**Yapılanlar:**
- `pipeline/`: `orchestrator.py` (§4 akışı; katmanları çağırır, 235 satır), `stages.py` (statik aşama, referans çözüm yükleme, `VerifyArgs`, gerekçe/açıklama sızıntı süzgeci, bozulmada statik karmaşıklık), `passes.py` (`LLMSession`, onarım döngülü Geçiş A, sızıntıda 1 kez yeniden üretimli Geçiş B, `single_pass`), `assemble.py` (rapor + `stage_latency_ms`), `events.py` (`EventBus`, `StageTimer`), `templates.py` (LLM'siz erken çıkış ve bozulma soruları), `ids.py` (bağımlılıksız ULID), `versions.py` (`rules_version`).
- `storage/`: `db.py` (SQLModel: `analyses`, `sessions`, `eval_runs`, `eval_results`), `cache.py` (§11'in 10 alanlı anahtarı, uzunluk önekli), `sessions.py` (ipucu merdiveni).
- `report/`: `cli_render.py` (Rich; bulgular satır numaralı, vurgulu kod parçasıyla), `markdown.py`, `sarif.py` (SARIF 2.1.0).
- CLI `codementor analyze PATH [--language --engine --question --session --provider --mode --format pretty|json|md|sarif --out --no-cache --tier1/--no-tier1]`; çıkış kodları §10; `asyncio.run` tek noktada; JSON/MD/SARIF stdout'a UTF-8 bayt.
- Veri: `data/mentor_templates.yaml`. Modeller: `models/pipeline.py` (`StageEvent`, `ALL_STAGES`, `MentorTemplates`). Config: `[storage]`, `data.mentor_templates_file`. Bağımlılık: `sqlmodel`; geliştirme: `jsonschema`, `types-jsonschema`. Resmi şema: `tests/fixtures/sarif-schema-2.1.0.json` (oasis-tcs/sarif-spec).
- Testler: `tests/integration/test_pipeline.py` (20 uçtan uca senaryo, FakeProvider, geçici SQLite), `test_cli_analyze.py`, `test_report_render.py`, `test_storage.py`, `test_mentor_templates.py`. Toplam 1687 test.
- Demo: `docs/demo/analyze-unity-hard-inventory.{svg,json}` (claude_cli, gerçek çalıştırma).
**Kabul kriterleri:**
- [x] Erken çıkışta sağlayıcı hiç çağrılmıyor — `test_early_exit_never_calls_provider`, `test_exit_2_on_compile_failure_without_llm` (FakeProvider çağrı listesi boş).
- [x] Onarım en fazla `max_repair_attempts` kez — `test_repair_bounded_then_degraded[0,1,2]`, `test_repair_succeeds`, `test_unjustified_conflict_repaired`.
- [x] Bozulmada rapor dönüyor, `degraded=true`, Sokratik bölüm şablondan — aynı test + `test_provider_failure_degrades`.
- [x] Aynı istek ikinci kez → `cache_hit=true`, sağlayıcı çağrılmıyor — `test_cache_hit_skips_provider`; canlı demoda 44 sn → 1,2 sn, 0 token.
- [x] Aynı oturum + soru ile 3. gönderimde `hint_level=3` — `test_hint_level_rises_per_session_submission` (orta zorluk: 1 → 2 → 3, prompt'ta da görülüyor).
- [x] SARIF çıktısı resmi SARIF 2.1.0 şemasıyla doğrulanıyor — `test_sarif_validates_against_official_schema`, `test_sarif_output_valid` (Draft4Validator).
- [x] `meta.stage_latency_ms` tüm aşamaları içeriyor — `test_all_stage_latencies_present` (erken çıkışta da; çalışmayan aşama 0).
- [x] Gerçek sağlayıcıyla manuel demo çalışıyor — **Ollama yerine claude_cli** (kullanıcı tercihi): `codementor analyze tests/golden/prompts/unity-hard-inventory/code.cs --engine unity --question unity-hard-inventory --provider claude_cli` → 44 sn, 20.480/4.455 token, onarım yok, O(n) ipucuyla uyumlu, 6 doğrulanmış LLM + 2 statik bulgu, Sokratik sorular SO asset'inin çalışma zamanında değiştirilmesine çözümü söylemeden yönlendiriyor; çıkış kodu 1 (yüksek önemli bulgu). Bozuk C → çıkış 2, LLM çağrısı yok.
**Alınan kararlar (ve neden):**
- **Bozulma kapsamı (§5.6):** Geçiş A onarımdan sonra da doğrulanamazsa ya da sağlayıcı/bütçe hatası olursa rapor yalnızca K1+K2'dir: LLM bulguları atılır, zaman karmaşıklığı statik ipucundan (`space_complexity = "?"`, güven ipucu güveninden 0.3/0.5/0.7), sorular şablondan. Yalnızca Geçiş B düşerse bozulma sayılmaz; sorular şablondan gelir, uyarı yazılır.
- **Önbellek:** bozulmuş rapor önbellekten dönmez (geçici sağlayıcı hatası kalıcı olmasın); erken çıkış raporu önbelleğe girer (belirleyici). İsabet de `analyses`'a yeni kimlikle yazılır (iz). Anahtar alanları uzunluk önekli: alan sınırları kayarak çakışamaz.
- **Oturum:** deneme sayısı önbellek isabetinde de artar (yeni gönderim = yeni deneme; ipucu seviyesi değiştiği için anahtar da değişir). Oturumsuz istek hep 1. deneme.
- **Sızıntı süzgeci genişletildi (Faz 9 açık sorusu):** `reasoning_steps`'te çözüm ima eden adım rapordan çıkarılır, LLM bulgu açıklaması nötr şablonla değiştirilir (yeniden üretim yok). Test sırasında C işaretçi bildirimi (`Node *next = cur->next;`) kod sayılmıyordu → desen eklendi, `a * b = c` düzyazısı negatif testle korunuyor.
- **`key_flaw_concept`:** raporda kalır (öğretmen/eval için); CLI ve Markdown yalnızca ipucu seviyesi 3'te gösterir (seviye 3 = kavram adı).
- **SARIF:** kuralı olmayan LLM bulgusu `CM-LLM-<KATEGORİ>`, derleme tanıları `CM-COMPILE`; `artifactLocation.uri` ileri eğik çizgili.
- **Katman sınırı:** SQLModel tabloları `storage/db.py`'de (veritabanı şeması; API/rapor şeması `models/`'de kalır, rapor JSON olarak saklanır). Orkestratör 250 satır sınırı için aşamalar `stages.py` + `passes.py` + `assemble.py`'ye bölündü.
**Mimariden sapmalar (ADR linki):** yok. §16 pipeline dosya listesi, §17 `[storage]`, §5.2.4 şablon dosyası notu güncellendi. Canlı demo Ollama yerine claude_cli (kullanıcı kararı, 2026-09-30).
**Açık sorular:**
- "Referans çözüm okunamadı" uyarısı öğrenciye de görünüyor (`private/` yoksa); yerel geliştirmede gürültülü. Faz 11 API'sinde yalnızca log'a mı yazılmalı?
- Typer'ın kendi kullanım hatası (geçersiz `--language` değeri) çıkış kodu 2 veriyor; §10'da 2 "derleme başarısız". Typer davranışını değiştirmek yerine belgelemek yeterli mi?
- Maliyet tahmini (`pricing.yaml`, §13) ve `usage_estimated` bayrağının rapora taşınması yapılmadı (Faz 12).
- `make` hâlâ yok; kontroller `uv run ...` ile.
**Bu fazda öğrendiğim:**
- Uçtan uca testler, birim testlerin kaçırdığı bir sızıntı desenini (C işaretçi bildirimi) buldu; öğrenci kodundan alıntı toleransı ile yeni kod arasındaki çizgi ince.
- FakeProvider senaryolarıyla onarım/yeniden üretim sayılarını doğrudan saymak, "en fazla N kez" kriterini kanıtlamanın en net yolu.
- Windows'ta Rich/Typer çıktısı kod sayfasına takılıyor; yönlendirilen biçimlerde stdout'a UTF-8 bayt yazmak gerekiyor.

## Faz 11 — Notlar
**Yapılanlar:**
- `api/`: `app.py` (`create_app(settings, db=, provider_factory=)`, CORS yalnızca `api.cors_origins`, `/docs`), `routes.py` (§9'un 10 uç noktası, ince), `sse.py` (istek başına `EventBus` + `asyncio.Queue`; bağlantı kesilirse görev iptal), `errors.py` (RFC 7807; `PipelineError.kind` → 413/422/404/503, doğrulama hatası girdiyi yansıtmaz, beklenmeyen hata 500 ayrıntısız), `state.py` (istek başına orkestratör, tembel veritabanı/soru bankası), `examples/` (OpenAPI istek + §6.5 rapor örneği, paket verisi).
- `codementor serve [--host --port]` (uvicorn; varsayılan `127.0.0.1:8000`, döngü dışı adreste uyarı). `models/api.py` (`Problem`, `Health`, `Readiness`, `CompilerStatus`). Config `[api]`.
- Refaktör: sağlayıcı sağlık kontrolleri `cli/providers.py` → `providers/health.py` (CLI ve API aynı kod); `PipelineError(kind)`; `StageStatus` `done` → `completed` (§9 örneği); SQLite `check_same_thread=False` + `:memory:` için `StaticPool`; `cache.get_analysis`.
- Testler `tests/api/` (32): rotalar, hata eşlemesi, SSE (sıra, son olay, hata olayı, başlıklar, eşzamanlı akışlar karışmıyor), CORS, OpenAPI örnekleri, `serve`. Toplam 1719 test.
**Kabul kriterleri:**
- [x] §9 tablosundaki her uç nokta çalışıyor ve testli — `test_routes.py` (analyze, stream, analyses/{id}, /sarif, questions, questions/{id}, providers, rules, health, health/ready).
- [x] `/v1/questions/{id}` referans çözüm yolu döndürmüyor — `test_question_detail_hides_solution_and_mentor_data` (ipucu merdiveni ve kavram etiketleri de yok).
- [x] Hata yanıtları `application/problem+json` — 404/405/413/422/503 testleri, SSE `error` olayı da problem gövdesi.
- [x] SSE: `stage` olayları doğru sırada, son olay `report` — `test_stage_events_in_order_then_report` (her `completed`'dan önce `started`); canlı `curl -N`: 26 aşama olayı + `report`, 20 sn.
- [x] Varsayılan bağlama `127.0.0.1` — `test_default_bind_is_loopback`, `test_serve_uses_config_and_warns_when_exposed`.
- [x] OpenAPI dokümanı `/docs`'ta, örnek istek/yanıtlar dolu — `test_openapi_has_examples` (istek, 200 rapor, 413 problem, SSE örneği).
**Canlı doğrulama (claude_cli, 2026-09-30):** `codementor serve --port 8765` + `curl -N -X POST /v1/analyze/stream` (c-medium-linked-list): aşamalar doğru sırada akıyor (llm_a 11 sn, llm_b 9 sn); model koda bilerek konmuş iki use-after-free'yi (30. ve 43. satır) ve boş listede NULL erişimini (21. satır) buldu, Sokratik sorular çözümü söylemiyor; `/v1/analyses/{id}/sarif` çalışıyor; bilinmeyen soru 404 problem+json.
**Alınan kararlar (ve neden):**
- **§9 hata tablosu:** tüm sağlayıcılar düşse de bozulmuş rapor üretilebildiği için 502 yerine 200 + `degraded=true`; sağlayıcı hiç kurulamazsa (yapılandırma) 503.
- **SSE hata semantiği:** istek gövdesi geçersizse akış açılmadan 422; akış başladıktan sonraki hata son olay `event: error`. Eşzamanlı istekler için orkestratör istek başına (paylaşılan bus olayları karıştırırdı).
- **Referans çözüm uyarısı (Faz 10 açık sorusu):** öğrenciye dönen `meta.warnings`'ten çıkarıldı, `reference_solution_unreadable` log olayına dönüştü (iç yapı söylenmesin).
- **SARIF uç noktası:** yüklenen dosya adı bilinmediği için `artifactLocation.uri = <analysis_id>.<uzantı>`; içerik türü `application/sarif+json`.
**Mimariden sapmalar (ADR linki):** yok. §9'a aşama durumları / SSE hata olayı / 404 notu, §16'ya `state.py` ve `examples/`, §17'ye `[api]` eklendi.
**Açık sorular:**
- Pipeline'ın senkron parçaları (tree-sitter, Tier 1 derleyici süreci, SQLite) async rotada olay döngüsünü kısa süre bloklar; tek kullanıcılı yerel kullanımda sorun değil, çok kullanıcıda `asyncio.to_thread` gerekir (Sonraya).
- API'de kimlik doğrulama ve hız sınırlama yok (§12 "API hız sınırlama" azaltımı); yalnızca yerel bağlama ile korunuyor. Faz 13'te (web/kurulum) ele alınmalı.
- Typer kullanım hatası çıkış kodu 2 çakışması (Faz 10'dan) hâlâ açık.
- `make` hâlâ yok; kontroller `uv run ...` ile.
**Bu fazda öğrendiğim:**
- SSE için istek başına olay yolu şart: paylaşılan bir abonelik listesi eşzamanlı iki analizin olaylarını birbirine karıştırırdı; bunu doğrudan test etmek (asyncio.gather ile iki akış) ucuz.
- FastAPI senkron rotaları iş parçacığı havuzunda çalıştırıyor; SQLite bağlantısının iş parçacığına bağlı olduğu burada ortaya çıkıyor.

## Faz 12 — Notlar
**Durum:** 12A (altyapı), 12B (80 örneklik veri seti, etiketler kullanıcı onaylı) ve 12C (ölçümler, `docs/eval-findings.md`, ADR-0003) bitti.
**Yapılanlar (12A):**
- `src/codementor/eval/`: `dataset.py` (yükleme + doğrulama: şema, kimlik = dizin, uzantı = dil, satırlar kodda, dev/test/_draft arasında aynı kimlik/kod yok; `promote` yorumları koruyarak `reviewed: true` yazar), `metrics.py` (§14.2'nin tamamı; eşleşme: aynı kategori + satır farkı ≤ 2, bire bir, en yakın önce), `runner.py` (önbellek kapalı, veritabanı yok; `StaticOnlyProvider` ile LLM'siz taban çizgisi; ablasyonlar `facts|line_numbers|fewshot0|fewshot1`; sonuç `eval/results/{zaman}_{sağlayıcı}_{model}_{mod}[_abl]_{bölüm}.json`), `compare.py` (Markdown tablo + sürüm dipnotu), `review.py` (taslak etiketleri statik analizle karşılaştırır, etiketi değiştirmez).
- CLI: `codementor eval run --split dev|test [--provider --mode --static-only --ablate --limit --final]` (test yalnızca `--final` ile), `eval compare`, `eval check-drafts`, `eval promote <id…> --split`.
- Modeller `models/eval.py`; `data/pricing.yaml` (boş, fiyatlar elle); config `prompts.include_facts`, `prompts.numbered_code` (ablasyon); `verify_a` olayına `schema:ok|invalid` notu (rapor şeması değişmeden şema metriği için); few-shot'lar da `numbered_code` ablasyonuna uyar.
- `.gitignore`: `eval/results/*.json` artık commit edilebilir (Faz 13 README tablosu bu dosyalarla birebir olacak).
- Testler `tests/unit/eval/` (35): her metrik için elle hesaplanmış bilinen girdi → skor, veri seti, koşucu, ablasyon prompt'u, karşılaştırma, taslak kontrolü, CLI. Toplam 1754 test.
- **Taslaklar:** `eval/dataset/_draft/c-001…c-016` (C grubu: 4 sözdizimi hatalı, 2 injection, 2 temiz, 8 sorunlu; dev 6 / test 10). Satırlar betikle koddan hesaplandı; `check-drafts` 16/16 uyumlu (statik ipucu ve kural bulguları etiketle aynı). **Etiketler henüz insan tarafından incelenmedi (`reviewed: false`).**
**Yapılanlar (12B):**
- C incelemesi: c-006 alan O(n)→O(1); c-008'e `n = 0` sıfıra bölme (`edge_case`, satır 10) eklendi (LLM'in doğru bulgusu yanlış pozitif sayılmasın); c-005 `must_not_contain`'de masum bağlamda geçebilecek "düzeltilmiş kod" yerine kod bloğu işareti. Kullanıcı kararları: c-016 realloc → `resource_leak`, c-014 `performance` bulgusu kalır, c-013 `input_handling` kalır.
- C++, C#, Unity, Unreal: 16'şar örnek (her grupta 4 sözdizimi hatalı, 2 injection, 1–2 temiz). Satırlar betikle koddan hesaplandı; `check-drafts` 64/64 uyumlu. Kalan notlar bilinen statik kör noktalar (etiket doğru): `memset`, döngüde string kopyası, `GetAllActorsOfClass`, `TArray::Remove` maliyet tablosunda yok (bkz. Sonraya).
- Dağılım: 80 örnek, dev 31 / test 49; %25 sözdizimi hatalı, %12,5 injection; her dil/motor 16. `tests/unit/eval/test_dataset_content.py` (9 test) dağılımı, inceleme bayrağını, bölüm ayrıklığını, kural/soru kimliklerini, sızıntı işaretlerinin kodda geçmemesini ve satır sınırlarını korur.
- Etiket kararları: dosya düzeyinde tek doğru karmaşıklık yoksa (unity-012 havuz: Awake O(n), Get/Release O(1); cpp-016 sonsuz döngü) `time_complexity` boş bırakıldı. C#'ta "istisna fırlatır" türü hatalar (foreach içinde koleksiyon değişimi) için uygun kategori olmadığından örnek konmadı.
- Veri setinde bulunan Faz 5 `foreach` hatası kullanıcı isteğiyle düzeltildi (bkz. Sonraya). Dev static-only: erken çıkış 100/100, Big-O %92, denetim P/R/F1 100/38/55.
**Kararlar:** "yerel model" satırları Ollama yerine claude_cli ile ölçülecek (kullanıcı tercihi); `leak_rate` §14.2 gereği `must_not_contain` ile ölçülür, `private/solutions/` zorunlu değil; injection örneğinde erken çıkış da direnç sayılır; `complexity_time_class_acc` değişkenleri tek değişkene indirger (`m*n` ≈ `n^2`).
**Yapılanlar (12C):** tüm koşular `claude_cli` / `claude-opus-5-5`, önbellek kapalı, prompt dev'de ayarlanmadı; sonuç dosyaları `eval/results/` (8 dosya: dev 5, test 3).
- Dev (31): static-only, two_pass, single_pass, two_pass `--ablate facts`, two_pass `--ablate line_numbers` (önceki geçersiz koşu 429 sonrası yeniden koşuldu; 26/26 LLM çağrısı hatasız).
- Test (49, `--final`, tek sefer): static-only Big-O %88, P/R/F1 100/42/59 · two_pass Big-O %91, 27/92/42, sızıntı %0, injection %100, 20,3/57,3 sn, 15,7k token · single_pass Big-O %94, 32/94/48, %0, %100, 13,5/35,7 sn, 10,2k token.
- Ablasyonlar: olgular çıkarılınca Big-O birebir %96 → %85 (model kanonik `n` yerine kendi değişkenini yazıyor); numaralı görünüm kapatılınca satır doğruluğu %100 → %96 (bu modelde küçük etki). Few-shot ablasyonu koşulmadı (kriter ≥ 2).
- LLM katma değeri: recall %38–42 → %92–96; kategorisiz eşleşmede dev 24/24, test 36/36. Precision %27–32 (orta+ önemde %35–43); FP'ler etiketlenmemiş küçük `edge_case`/`design`/`input_handling` gözlemleri.
- `docs/eval-findings.md` (tablolar, ablasyonlar, two_pass vs single_pass), `docs/adr/0003-iki-gecisli-prompt.md`, mimari §5.4.2 ve §23 ADR-0003'e bağlandı.
**Kararlar:** ADR-0003: varsayılan `two_pass` kalır ama gerekçe kalite değil (kalite üstünlüğü teyit edilmedi; F1'de single_pass biraz önde); single_pass'te sızıntı koruması 60 örneğin 17'sinde, two_pass'te 11'inde devreye girdi → two_pass sezgisel korumaya daha az yaslanıyor. `single_pass` kalite kaybı olmadan hızlı mod (~%35–45 hızlı, ~%35 az token).
**Kabul kriterleri:** [x] 80 örnek elle kontrol · [x] metrik birim testleri · [x] önbellek kapalı · [x] sonuç dosyasında metrikler + sürümler · [x] ≥ 3 satırlı tablo (statik / two_pass / single_pass; "yerel model" yerine claude_cli, kullanıcı tercihi) · [x] 2 ablasyon (facts, line_numbers) · [x] prompt ayarı yalnız dev, test en sonda bir kez · [x] ADR-0003 güncellendi. `private/solutions/` oluşturulmadı: `leak_rate` §14.2 gereği `must_not_contain` ile ölçülüyor.
**Ortam notu:** two_pass test koşusunda bilgisayar 21:21–21:54 uykuya geçti; `cpp-012` süresi (2036 sn) geçersiz, p50/p95 etkilenmedi (en yakın sıra). Makinede gcc/clang yok: C/C++/Unreal Tier 1 `skipped`.
**Açık sorular:** `make` hâlâ yok. Precision analiz betiği (kategorisiz eşleşme, önem filtresi, FP/FN dökümü) scratchpad'de kaldı; Sonraya. Tam pakette bir kez zamanlamaya bağlı tek test hatası görüldü, tekrarlanmadı (yük altında süre sınırlı bir performans testi olabilir).

## Faz 13 — Notlar
**Yapılanlar:**
- `web/` (Vite 8 + React 19 + TS, Monaco yerel paketten, CDN yok; yalnızca çekirdek editör + C/C++/C# renklendirme): dil/motor/soru seçimi, SSE aşama ilerlemesi (`fetch` + `ReadableStream`; POST olduğu için `EventSource` değil), Monaco satır işaretleri (önem derecesine göre; aynı satırda en yüksek önem, mesajlar birleşik), bulgu listesi (tıkla → satır), Sokratik panel + "Sonraki ipucu" (kalıcı `session_id` ile aynı kodu yeniden gönderir; ipucu merdiveni sunucuda, yeni uç nokta yok), karmaşıklık kartı (gerekçe adımları, güven, statik uyum), uyarı/bozulma bildirimi, Türkçe hata mesajları. ≤ 900 px tek sütun.
- Tipler elle yazılmadı: `models/schemas.py`'ye `request`, `stage_event`, `question_public`, `problem` şemaları eklendi; `web/scripts/gen-types.mjs` (json-schema-to-typescript) → `web/src/types/*.ts` (başlıkta "OTOMATİK ÜRETİLDİ"). CI `web` işi tipleri yeniden üretip `git diff --exit-code` ile sapmayı yakalar.
- Testler: Vitest 24 (`sse`, `client`, `markers`, `progress`, `session`, `App`), Playwright 2 (API `page.route` ile taklit: işaret sınıfları, 375 px'de yatay kaydırma yok) + 1 canlı (`CODEMENTOR_E2E_LIVE=1`, gerçek API + claude_cli). Python: `test_ui_schemas_exported`, `test_readme_table.py` (README eval tabloları `compare` çıktısıyla birebir), `test_repo_config_default_provider_is_claude_cli`. Toplam Python 1772.
- Kurulum: `codementor.toml` varsayılan sağlayıcı `claude_cli` (fallback yok); Makefile `serve`, `web-install`, `web-types`, `web`, `web-test`, `web-e2e`; CI'a `web` işi (npm ci, tip senkronu, typecheck, test, build, Playwright).
- README baştan: gerçek analiz ekran görüntüsü (`docs/img/web-live.png`), mermaid diyagram, Docker'sız hızlı başlangıç, sağlayıcı tablosu (Ollama `ollama pull` adımı dahil), eval tabloları (işaretler arasında, testle korunur), dürüst Sınırlamalar, yol haritası. ADR 0001, 0002, 0004–0008 yazıldı; mimari §18, §19, §20 (bağlantılar), §22, §23.1/§23.2 ölçülen sayılarla güncellendi.
**Kararlar:** (1) Docker dosyaları yazılmadı (kullanıcı kuralı; ADR-0009 Faz 13 eki, mimari §18.1). (2) Varsayılan sağlayıcı `claude_cli` (eval bununla ölçüldü, kullanıcı Ollama kullanmıyor). (3) API kimlik/hız sınırı v1'de yok; `serve` yerel olmayan adreste uyarıyor, README Sınırlamalar'da. (4) GIF yerine PNG (ffmpeg yok); ekran görüntüleri Playwright ile üretilir. (5) Monaco çekirdeği ~3 MB (gzip ~770 kB), yerel araç olduğu için kabul; `chunkSizeWarningLimit` 3500.
**Doğrulama:** README adımları git'in izleyeceği dosyaların temiz kopyasında (`.venv`/`node_modules` yok) birebir uygulandı: `uv sync`, `serve`, `npm install`, `npm run dev`; `/health/ready`, soru listesi ve Vite proxy üzerinden SSE analiz (26 aşama + rapor), canlı Playwright testi geçti. Canlı ekran görüntüsünde aynı satırda yüksek + düşük bulgu varken düşük rengin görünmesi hatası bulundu ve düzeltildi (testli).
**Açık sorular:** `YAPILANLAR.md` Faz 7'den sonra güncellenmemiş (Faz 8–12 özetleri yok); Faz 13 bölümü eklendi.

## Faz 14 — Notlar (masaüstü uygulaması, ADR-0013)
**Yapılanlar:**
- `src/codementor/desktop/` (CustomTkinter): sol menü (Analiz, Soru bankası, Geçmiş, Ayarlar; altta sağlayıcı durumu), araç çubuğu (dil, motor, görev, Dosya aç, Örnek, Dışa aktar, altın **Denetle** / Ctrl+Enter), görev şeridi, satır numaralı ve renklendirmeli kod editörü (bulgu satırları önem rengiyle, imleç satırındaki bulgu alt şeritte), sağ panel: rapor özeti + uyarılar, 6 adımlık canlı analiz akışı, Sokratik mentor kartı (ipucu merdiveni 1-3, "Bir ipucu daha", "Baştan başla"), karmaşıklık kartı, bulgu kartları (tıkla → satır). Koyu lacivert + altın/mor tema tek dosyada (`theme.py`); Windows 11'de koyu başlık çubuğu.
- Çekirdek doğrudan çağrılır (sunucu yok): `ApiState` + `bridge.Bridge` (görev başına thread + `asyncio.run`, kuyruk, kuşak sayacıyla eski mesajları atma). GUI'siz mantık: `viewmodel.py`, `highlight.py`, `runtime.py`, `services.py`.
- Tercihler `models/desktop.py` (`DesktopPrefs`) → `~/.codementor/desktop.json`; analiz edilen kod `desktop-sources/` (geçmişten yeniden açmak için). `storage.cache.list_analyses` eklendi.
- `build_exe.py`: onefile (`dist/CodeMentor.exe`, açılış görseli, Windows sürüm bilgisi, ~37 MB) + onedir + zip. Görseller `tools/make_desktop_assets.py` ile üretildi (logo, ikon, açılış). `pyproject`: `customtkinter`, `pillow`; dev `pyinstaller`; `codementor-desktop` gui-script; Makefile `desktop`, `desktop-assets`, `exe`.
- Testler: `tests/desktop/` 45 test (görünüm modeli + hypothesis, renklendirme + hypothesis, çalışma ortamı/exe kökü, köprü FakeProvider'lı gerçek orkestratörle, gerçek Tk penceresiyle duman testleri: tam mentorluk akışı ve ipucu artışı, geçmişten açma, soru bankası, dosya açma/boyut sınırı, sağlayıcı tercihi; `build_exe` yardımcıları). Ekran yoksa GUI testleri atlanır.
**Kararlar:** (1) CustomTkinter + PyInstaller (ADR-0013); pywebview/Electron reddedildi. (2) `web/` silinmedi, ikincil istemci. (3) `customtkinter`/`pillow` ana bağımlılık (exe ve `python -m codementor.desktop` için; ayrı grup ek karmaşa). (4) Rapor kodu içermediği için kod masaüstünde ayrı saklanıyor (yerel). (5) `pyi_splash` doğrudan import edilmeli; `importlib` ile PyInstaller modülü pakete koymuyor ve açılış görseli kapanmıyordu (exe'de bulundu, düzeltildi).
**Doğrulama:** `make check` yeşil. Exe derlendi ve açıldı (açılış görseli kapanıyor, `claude_cli` hazır); FakeProvider ile tüm ekranların görüntüsü alındı; claude_cli ile canlı analiz (34.5 sn, 7 bulgu, Sokratik sorular) `docs/img/desktop-live.png`.

## Faz 15 — Notlar (bağlantı merkezi, ADR-0014)
**Yapılanlar:**
- Ayarlar ekranı → **Bağlantılar**: 6 sağlayıcı kartı (`widgets/provider_card.py`, `views/connections_view.py`), denetleyici `connections_controller.py`, GUI'siz mantık `connections.py`.
- Model seçimi: öneriler `data/desktop_models.yaml`; Ollama `/api/tags` ve `agy models` canlı keşif; seçim `DesktopPrefs.providers` (`ProviderOverride`) → `apply_overrides` ile toml'un üstüne (CLI/API etkilenmez). Model seçilmemiş CLI'da da liste keşfedilir.
- Yetkilendirme: API anahtarları `keyring` (Windows Kimlik Bilgisi Yöneticisi) → yalnız süreç ortamına; dış ortamdaki anahtar ezilmez; `register_secret` ile maskeleme. claude_cli `auth status --json` (hesap gösterilir), agy araç onayı anahtarı (ADR-0012), "Oturum aç" yeni konsolda CLI'nın kendi girişini açar. "Bağlantıyı dene" küçük gerçek istek (`ConnectionPing`).
- Analiz araç çubuğunda sağlayıcı/model rozeti (tıkla → Bağlantılar); kenar çubuğu seçili sağlayıcının gerçek durumunu gösterir.
- Testler: `tests/desktop/test_connections.py` (sahte kasa, respx, sahte süreç çalıştırıcı) + GUI (model seçimi kalıcı, varsayılan değişimi, anahtar kaydet/sil → ortam, yoklama sonuçları kartlara). Tk kökü art arda kurulurken Tcl'nin `init.tcl` okuma hatası (Windows, aralıklı) için fikstürde yeniden deneme.
**Kararlar:** (1) Masaüstü tercihleri yalnız masaüstüne uygulanır; toml kaynak olarak kalır. (2) Anahtar dosyaya asla yazılmaz. (3) Oturum açma CLI'ya bırakılır; uygulama kimlik bilgisi görmez.
**Doğrulama:** Gerçek ortamda Bağlantılar ekranı: Ollama `qwen2.5-coder:14b` seçilince "hazır" (4 yerel model listelendi), Claude Code "oturum açık" + hesap. Kullanıcının tercihlerine Ollama modeli `qwen2.5-coder:14b` yazıldı (şikâyet edilen "hazır değil" düzeltmesi).

## Faz 16 — Notlar (Python, HTML, CSS; ADR-0015)
**Yapılanlar:**
- `Language` + python/html/css, `AuditCategory` + accessibility/maintainability, `has_complexity`/`MARKUP_LANGUAGES`; tree-sitter-python/html/css; Tier 0 fixture'ları (her dilde 5+5).
- Python: süreç içi Tier 1 (`validation/python_check.py`, `ast`; kod çalıştırılmaz), olgular (`queries/python`, `_symbols`/`_loops` Python dalları, kavramalar örtük döngü, `x in liste` → `list.__contains__` maliyeti), `call_costs.yaml` `python` bölümü. Big-O: iç içe O(n²), ikili arama/`//=` O(log n), `range(10)` sabit, `fib` O(2ⁿ), küme üyeliği O(1).
- HTML/CSS: olgu/Big-O yok, Tier 1 uyarısız atlanır, Geçiş A `LLMMarkupAnalysisOutput` + `markup_analysis.*.j2`, `verify_markup_analysis`; rapor `complexity = null`.
- 13 kural + 52 fixture (`rules/python.py`, `html.py`, `css.py`); fixture düzeneği `#`, `<!--`, `/*` EXPECT yorumlarını tanır; fixture dizinleri ruff dışında (biçimlendirici satırları kaydırıyordu).
- Dil tespiti: Python/HTML/CSS sinyalleri ham kodda; 30 geçerli fixture'ın hepsi doğru tespit.
- Veri: 3 kontrol listesi, 2 mentor kategorisi, 4 soru (`expected` HTML/CSS'te yok; model doğrulayıcısı), soru testleri ve sızıntı tablosu.
- Arayüzler: masaüstü (6 dil, renklendirme, uzantılar, örnekler, derleyici kartında Python), web (dil listesi, Monaco python/html/css Monarch tanımları, tipler şemadan). Araç çubuğu taşmasın diye sağlayıcı rozeti kenar çubuğu kutusuna taşındı (tıkla → Bağlantılar).
- Şemalar ve kural kataloğu yeniden üretildi; golden prompt'lar ("ve Python") güncellendi.
**Kararlar:** (1) İşaretleme dillerinde karmaşıklık kavramı yok; ayrı şema/şablon (ADR-0015). (2) Kural kimliği `HTML-ACC-*` (desen rakamlı kategoriye izin vermiyor). (3) Tipi bilinmeyen `in` araması maliyet almaz (tahmin yok).
**Doğrulama:** `make check` yeşil (2000+ test). claude_cli canlı: Python örneği 28 sn, O(n²) + PY-PERF-001; HTML örneği 26 sn, karmaşıklık yok, 3 statik + 5 LLM erişilebilirlik bulgusu.
**Açık sorular:** Yeni 4 sorunun referans çözümleri `private/solutions/` altına kullanıcı tarafından eklenmeli (bu klasör erişim dışında).

## Faz 17 — Notlar (Faz 6'da ertelenen 10 statik kural)
**Yapılanlar:**
- C: `c.py`'ye C-IO-001 (dönüşü atılan `scanf/fscanf/sscanf`), C-UB-001 (`fflush(stdin)`), C-PERF-001 (döngü koşulunda `strlen`); yeni `c_memory.py`'de C-MEM-002 (`X = realloc(X, …)`), C-MEM-003 (deref edilen ama NULL'a karşı hiç denetlenmeyen tahsis). C-MEM-001 yardımcıları public oldu (`unwrap_call`, `callee_name`, `NON_OWNING`).
- C++: CPP-SP-001 (sınıf alanlarındaki `shared_ptr<T>` grafiğinde güçlü bağlı bileşen; yinelemeli Tarjan), CPP-PERF-001 (değerle geçirilen `std::vector/string/map/…`, `TArray/TMap/TSet/FString`).
- C#/Unity/Unreal: CS-ALLOC-002 (LINQ, Update/Tick ya da döngüde), UNITY-PERF-002 (`tag ==`/`tag.Equals`), UE-MEM-001 (sayılı döngüde `Reserve`'siz `TArray::Add`).
- 52 yeni fixture (her kurala ≥2+2, denetim regresyonları dahil), `test_engine.py`'ye 11 kötü niyetli girdi ve `test_linq_in_update_reported_once`; kayıt/CLI sayımları (33 kural); `docs/rules-catalog.md` yeniden üretildi.
- Few-shot `c_none_off_by_one.yaml`: statik listeye C-MEM-003 eklendi, aynı konudaki LLM ek bulgusu çıkarıldı (örnek statik bulguyu tekrar etmeyi öğretmesin; `test_repo_fewshots_match_static_engine`). Golden prompt'lar güncellendi (bağlı liste örneğinde 10. ve 17. satırda C-MEM-003).
- `prefixed_evidence_and_repeat.json` beklentisi: LINQ satırındaki tekrar artık CS-ALLOC-002 ile birleşiyor; test, birleşen bulgunun önemini kuralın varsayılan önemiyle karşılaştırıyor (sabit "high" yerine).
**Kararlar (ve neden):**
- **CS-ALLOC-002 "sıcak yol" = Update/Tick ya da döngü gövdesi.** Düz C#'ta Update yok; döngü sayılmasaydı kural düz C#'ta hiç çalışmazdı.
- **LINQ tek kuralda:** UNITY-GC-001 artık LINQ'i ve LINQ satırındaki closure'ı raporlamıyor (aynı satırda iki GC bulgusu olmasın). Closure bastırma satır bazlı (aynı satırdaki bağımsız lambda da düşer; etkisi düşük).
- **UNITY-PERF-002** `OnTriggerStay/OnCollisionStay(2D)`'yi kapsar, `*Enter/*Exit`'i kapsamaz (her karede değil). Kodda `tag` adlı değişken ya da Unity dışı tiple bildirilmiş alıcı (`Item item; item.tag`) bulgu vermez.
- **CPP-SP-001 öz-referans** yalnız geri işaretçi sözcüğü (`parent`, `prev`, `previous`, `owner`, `back`; camelCase/`_` ile bölünmüş) olan alanda; `left/right/next`, `fallback/preview` ve `std::function<…>` içindeki `shared_ptr` sayılmaz. Güven 0,7 (şüphe).
- **CPP-PERF-001** `std::move(param)` ya da `return param;` varsa (sink / kopyala-değiştir-döndür) bulgu yok.
- **C-MEM-003** muhafazakâr: kullanıcı fonksiyonuna geçirilen işaretçi (`die_if_null(p)`) denetlenmiş sayılır; denetimin kullanımdan sonra olması fark edilmez. **C-MEM-002** fonksiyonda `exit/abort` varsa bulgu vermez. **C-IO-001** atama yapmayan biçimleri (`%*[^\n]`, `%*c`) saymaz. **C-PERF-001** koşulda okuyucu (`fgets`, `getline`…) varsa bulgu vermez.
- **UE-MEM-001** döngüde `break/continue/return/goto` varsa ya da `Add` bir `if`/`switch` altındaysa bulgu yok; `Reserve/SetNum/Init` ya da sayılı `Empty(n)/Reset(n)` yer ayırmış sayılır.
**Mimariden sapmalar (ADR linki):** yok (§8.2 tablosunun yorumu).
**Denetim (kod-denetci):** Kritik ×5: 40 KB girdide karesel süre. C-MEM-003 sola iç içe atama zinciri 29,8 sn'den 0,16 sn'ye indi (`_key` açma adımı sınırlı). C-PERF-001 iç içe GNU deyim ifadesi 14,9 sn'den 0,18 sn'ye (koşulda `compound_statement`'e inilmiyor). UE-MEM-001 yerel struct metotları 8,8 sn'den 0,14 sn'ye ve UNITY-PERF-002 iç içe `Update` 5,1 sn'den 0,01 sn'ye (yalnız en dıştaki fonksiyon geziliyor). CPP-PERF-001 3,2 sn'den doğrusala (kök bir kez geziliyor, bayt aralığında ikili arama). Önemli: bu girdiler testlere eklendi; yanlış pozitifler (`scanf("%*c")`, kopyala-değiştir-döndür, `continue` ile süzme, `fallback`/`std::function`, `fgets && strlen`) negatif fixture'larla sabitlendi. Küçük: `reserved.cpp`'deki hatalı `SetNum`+`Add` örneği `Empty(Count)` oldu; `item.tag`, `die_if_null`, `(void *)0`, `exit` sonrası `realloc` düzeltildi; CS-ALLOC-002 ve UE-MEM-001 açıklamaları çözümü söylemeyen sorulara çevrildi. **Kapsam dışı düzeltme:** Faz 6'dan gelen UNITY-PERF-001 aynı iç içe `Update` girdisinde 5,1 sn sürüyordu; aynı dört satırlık düzeltme uygulandı (test bunu birlikte ölçüyor).
**Açık sorular:**
- Bağlı liste golden'ında iki C-MEM-003 bulgusu prompt'a giriyor; Sokratik odağı asıl hatadan (boş listede `cur->next`) uzaklaştırabilir. Eval'de izlenmeli.
**Bu fazda öğrendiğim:**
- "Sarmalayıcıyı aç" döngüsü her düğümde çağrılınca sola iç içe zincirde karesel olur; adım sınırı ya da tek geçiş şart.
- `function_nodes` iç içe (yerel fonksiyon/sınıf metodu) düğümler içerir; fonksiyon başına alt ağaç gezen her kural yalnız en dıştakini gezmeli.
- Bash heredoc'u `\b`/`\w` kaçışlarını yine bozdu; regex içeren düzenlemeler Edit ile.

## Faz 18 — Notlar (Python/HTML/CSS eval)
**Yapılanlar:**
- Altyapı: `SAMPLE_ID_PATTERN` + `python|html|css`, veri seti uzantıları (`.py/.html/.css`), `RunConfig.languages: list[Language]` (eski sonuç dosyaları varsayılan boş listeyle yüklenir), `eval run --language` (filtre `--limit`'ten önce; filtre sonrası örnek yoksa çıkış 2), sonuç dosya adına dil eki (`_css-html-python_test.json`).
- `eval/breakdown.py` + `codementor eval breakdown <sonuç.json>`: kayıtlı sonuçtan dil/motor grubuna göre metrik tablosu (LLM çağrısı yok). `compare.py` `pct`/`pair` public oldu.
- Veri seti: 36 yeni örnek (dil başına 12; dev 5 / test 7; her dilde 3 sözdizimi hatalı, 2 injection, 2 temiz). Kullanıcı etiketleri onayladı, `eval promote` ile taşındı (dev 46 / test 70, toplam 116). `check-drafts` 36/36 uyumlu. `test_dataset_content`: 8 grup, işaretleme dillerinde Big-O etiketi yok.
- Ölçüm (`claude_cli` / `claude-opus-5-5`, prompt ayarı yok): static-only dev+test, two_pass dev, two_pass test `--final`, single_pass test `--final`; 42 LLM örneğinin hepsi hatasız. Koşular uykuyu yalnız süreç boyunca engelleyen bir sarmalayıcıyla yapıldı (`SetThreadExecutionState`; kalıcı ayar değişmedi).
- Belgeler: `docs/eval-findings.md` §4 (dil başına tablo ve yorum), README'ye `test-diller`/`dev-diller` tabloları (`test_readme_table` dil filtreli koşuları ayrı blokta denetler) ve "Sınırlamalar" güncellemesi, ADR-0015'e Faz 18 notu, `UYGULAMA_PLANI.md` Faz 18 bölümü. `pyproject.toml`: ruff `extend-exclude` + `eval/dataset` (bilerek hatalı öğrenci kodu).
**Sonuçlar (test, 21 örnek):** statik P/R/F1 100/67/80 · two_pass 33/81/47 · single_pass 34/86/49; sızıntı %0, injection direnci %100, erken çıkış 100/100, Python Big-O 2/2 (dev 4/4). HTML precision en düşük (%22–23). CSS kaçırmaları satır doğru, kategori farklı (`design` → `edge_case`); gerçekten kaçırılan: başlık düzeyi atlama, başlık yerine `div`.
**Kararlar:** (1) Dil başına 12 örnek (16 yerine; kota ve inceleme yükü). (2) Dil filtreli koşular eski C ailesi tablolarına karışmaz; README'de ayrı blok. (3) `--language csharp` Unity'yi, `cpp` Unreal'ı da kapsar (filtre dil, döküm motor bazlı; yardım metninde). (4) Faz 17'nin eski veri setine etkisi yalnız raporlandı, etiketler değişmedi.
**Mimariden sapmalar (ADR linki):** yok (§14; ADR-0015'e not).
**Denetim (kod-denetci):** Kritik yok. Orta: §4'te Python Big-O paydası 7/7 yazılmıştı (doğrusu test 2/2), FP sayıları HTML'e bağlanmıştı (üç dilin toplamıydı), PROGRESS ve ADR-0015 notu eksikti → düzeltildi. Düşük (uygulanan): `languages` modelde `list[Language]`, filtre sonrası boş örnekte hata, yardım metninde motor notu, `breakdown` docstring'inde maliyet/etiket sınırları, README `-diller` ölçütü yalnız Python/HTML/CSS, testler (filtre `--limit`'ten önce, eski JSON yüklenir, `breakdown` uyarısı).
**Açık sorular:**
- Faz 17 kuralları eski 80 örnekte iki etiketlenmemiş doğru bulgu üretiyor (`c-008` C-MEM-003, `csharp-009` CS-ALLOC-002); dev statik precision %100 → %85. Etiket güncellemesi kullanıcı kararı (Sonraya).
- `private/solutions/` hâlâ yok; sızıntı `must_not_contain` ile ölçülüyor.
**Bu fazda öğrendiğim:**
- Bire bir en yakın eşleşmede aynı kategoride iki komşu beklenti, bulunan tek satırı "yanlış" beklentiye verebiliyor; FN dökümünü kategorisiz ve satır bazlı da okumak gerekiyor.
- PowerShell 5.1 yerel komutun stderr'ini `NativeCommandError` olarak sarıyor; arka plan günlüğünde hata gibi görünüyor ama çıkış kodu 0.

## Faz 19 — Notlar (masaüstünde analizi durdurma)
**Yapılanlar:**
- `validation/runner.py`: `run_process(..., cancel=threading.Event)`; `_wait` 0,1 sn dilimlerle bekler, iptalde süreç ağacı (Job Object / süreç grubu, torunlar dahil) öldürülür, `ProcessResult.cancelled`. `cancel=None` iken davranış aynı.
- `providers/cli_agent.py`: `once()` iş parçacığına iptal olayı verir, `asyncio.CancelledError`'da set eder; `cancelled` sonucu `CancelledError` olarak yükselir (retry/fallback'e girmez). API'de kopan SSE bağlantısı da artık CLI sürecini hemen öldürüyor.
- `desktop/bridge.py`: `Cancellation` (thread güvenli olay + geri çağrılar), `AnalysisCancelledError`, `submit(..., cancellation=)`; `cancel()` işi gerçekten durdurur, yeniden `submit` eski işi iptal eder, biten işin kaydı temizlenir; `analysis_work` asyncio görevini `call_soon_threadsafe(task.cancel)` ile iptal eder (kapanmış loop'ta sessiz).
- `pipeline/orchestrator.py`: kayıttan önce `await asyncio.sleep(0)` iptal kontrol noktası (Tier 0/1, önbellek, erken çıkış yolları `await` içermiyordu).
- Masaüstü: analiz sürerken "Denetle" düğmesi kırmızımsı "Durdur" olur (0,5 sn çift tıklama koruması), Esc yalnız analiz sayfasında durdurur, "Analiz durduruldu." bildirimi; önceki iş parçacığı kapanırken yeniden başlatma bildirimle reddedilir; kapanışta iptal + 2 sn bekleme.
- Testler (23 yeni): gerçek alt süreç + torun iptali (PID dosyasıyla, sabit uyku yok), zaman aşımı/iptal ayrımı, sağlayıcı iptali (retry ve fallback zincirine geçmez), köprü (LLM'de ve eşzamanlı yolda iptal → kayıt yok, ipucu merdiveni ilerlemez; iptal ERROR log'u üretmez; yeniden gönderim), pencere (Durdur, çift tıklama, kapanırken yeniden deneme, Esc sayfa sınırı).
- Belgeler: ADR-0012'ye güncelleme notu, `UYGULAMA_PLANI.md` Faz 19 bölümü.
**Doğrulama:** gerçek `claude` CLI ile analiz başlatılıp 3 sn sonra iptal: yeni `claude` süreci 0,23–0,24 sn içinde kapandı.
**Kararlar:** (1) Ayrı "Durdur" düğmesi yerine aynı düğme (araç çubuğu dar). (2) Yarıda kalan analiz kaydedilmez, ipucu merdiveni ilerlemez. (3) Tier 1 derleyici sürecine iptal iletilmedi: Tier 1 kısa süreli; o arada yeniden "Denetle" bildirimle reddedilir.
**Mimariden sapmalar (ADR linki):** yok (ADR-0012'ye not).
**Denetim (kod-denetci):** Kritik yok. Orta: (O1) eşzamanlı yolda (Tier 1 erken çıkış/önbellek) gelen iptal analizi yine kaydediyor ve ipucu merdivenini ilerletiyordu → orkestratörde kontrol noktası + test; (O2) Durdur sonrası "Denetle" sessizce yok sayılıyordu → bildirim; (O3) çift tıklama başlatıp durduruyordu → 0,5 sn koruma; (O4) her iptalde sahte ERROR log'u → `user_message` iptali ayırıyor; (O5) PROGRESS; (O6) testte sabit uyku → PID dosyası. Düşük (uygulanan): yeniden `submit` eski iptali çağırır, biten iş kaydı silinir, kapanışta `join`, Esc yalnız analiz sayfasında, `_wait` normal çıkışı beklemeden fark eder, `cancelled` sonucu sağlayıcı hatasına dönüşmez, fallback zinciri iptal testi.
**Açık sorular:**
- Tam pakette bir kez zamanlamaya bağlı tek test hatası görüldü (hangisi olduğu kaydedilmedi); ardından 2 tam koşu ve yeni testlerin 6 tekrarı temiz. Faz 12'deki benzer gözlemle birlikte izlenmeli.
**Bu fazda öğrendiğim:**
- `call_soon_threadsafe(task.cancel)` ancak görev askıya alındığında etkili olur; `await` içermeyen yollar için açık bir kontrol noktası (`asyncio.sleep(0)`) gerekiyor.
- Aynı düğmenin anlamı değişince (Denetle → Durdur) çift tıklama yeni bir hata türü doğuruyor.

## Faz 20 — Notlar (HTML etiket dengesi, HTML-STD-003)
**Yapılanlar:**
- `rules/html_balance.py`: `HTML-STD-003 "Dengesiz etiket"` (design, medium). tree-sitter-html tutarsız olduğundan (tam belgede eşsiz `</div>` hata değil, `<div><span>x</div>` hiç işaretlenmiyor) stdlib `html.parser` ile açık etiket yığını. Boş öğeler, isteğe bağlı kapanışlar (p, li, dt/dd, tablo bölümleri, option…), sade örtük kapanış tablosu (`p` blok/`hr` açılışıyla, `li`→`li` …), kapsam sınırları (`table`, `template`, `object`; hücreler `td/th/caption`), RCDATA (`title`, `textarea` …) kural içinde, `<div/>`/`<script/>` açık sayılır (SVG/MathML içinde `/>` kapatır).
- Bulgular: eşi olmayan kapanış → kapanış satırı, ayrı Sokratik soru ("Bu kapanışın açılışı nerede?"); kapanmayan / iç içe karışan zorunlu kapanışlı öğe → açılış satırı.
- Testler: 6 pozitif + 5 negatif fixture (Faz 18'in `</div>` örneği, tablo hücresi sınırı, `/>` JSX alışkanlığı; isteğe bağlı kapanışlar, iç içe tablolar, şablon, SVG/MathML, büyük harf, öznitelikte `>`, `</br>`, `<img></img>`, script/yorum/title/textarea içi etiket metni), `test_html_balance.py` (7), `test_engine.py`'ye 7 kötü niyetli HTML girdisi (en yavaşı 0,46 sn, tüm hat dahil). 34 kural; katalog yeniden üretildi.
- Mevcut HTML eval etiketleri etkilenmedi (geçerli örneklerde yeni bulgu yok). ADR-0015'e not, `UYGULAMA_PLANI.md` Faz 20 bölümü.
**Kararlar:** (1) Kullanıcı kararı: sözdizimi hatası/Tier 1 uyarısı değil, statik kural (analiz durmaz, LLM'e "statik analizin bulduğu" olarak gider). (2) Tam HTML5 ağaç kurma algoritması yerine sade tablo; emin olunmayan durumda kaçırma. (3) Belge iskeleti (`html/head/body`) eşsiz kapanışı raporlanmaz.
**Mimariden sapmalar (ADR linki):** yok (ADR-0015'e not).
**Denetim (kod-denetci):** Kritik yok. Orta: (O1) kapsam sınırı yoktu, hücredeki tek hatalı `</div>` tablo ve dış div için de yanlış bulgu üretiyordu → sınır konum listeleriyle O(1) kapsam denetimi + fixture; (O2) `title`/`textarea` RCDATA davranışı Python yama sürümüne bağlıydı → kural `set_cdata_mode` ile kendisi ayarlıyor + fixture; (O3) PROGRESS. Düşük (uygulanan): `hr` `p`'yi kapatıyor, `<div/>`/`<script/>` açık sayılıyor, `kind` `Literal`, açıklama türü testi, HTMLParser zayıf nokta girdileri (bitmemiş yorum, `<!`/`</` tekrarı).
**Açık sorular:** Eski 3.12 yama sürümlerinde HTMLParser'ın `close()` yolunda karesel süre vardı (CVE-2025-6069); yerel 3.12.13'te test 0,08 sn. CI Python sürümü güncel; `requires-python` alt sınırı yükseltilmeli mi?
**Bu fazda öğrendiğim:** stdlib ayrıştırıcıların davranışı güvenlik yamalarıyla değişebiliyor (RCDATA listesi); kurala özgü davranış açıkça ayarlanmalı ve fixture ile kilitlenmeli.

## Faz 21 — Notlar (statik kural ve maliyet tablosu doğruluğu, dar kapsam)
**Kullanıcı kararları:** dar kapsam; eski eval etiketlerine Faz 17 bulguları eklensin.
**Yapılanlar:**
- `data/call_costs.yaml`: C++ `std::memset/memcpy/memmove` (+ çıplak adlar), Unreal `UGameplayStatics::GetAllActors*`, C# `List.RemoveAll/RemoveRange/InsertRange` = `n`.
- `analysis/call_costs.py`: bildirilen tip `IList` ise `List.<metot>` adayı (CS-PERF-001 artık `IList` alıcısında). `IReadOnlyList` (örnek `Contains`/`IndexOf` yok → LINQ) ve `ICollection` (HashSet olabilir) bilinçli dışarıda.
- `analysis/_memory.py` `file_value_types`: dosyadaki C# `struct`/`record struct` değer tipi → UNITY-GC-001 `new Hit(3)` için bulgu vermez.
- `analysis/_engine.py` `engine_inert_members`: tabanı olmayan sınıfın ve C# struct/record'un doğrudan metotları Unity/Unreal'da sıcak yol değil (`partial` sınıf hariç: taban başka parçada). Taban varsa ve sınıf dışı `AFoo::Tick` tanımında davranış aynı.
- `rules/engine.py` çöken kural için `log.exception("rule_failed")` (`RedactingLogger.exception` eklendi; iz `format_exc_info` → maskeleme sırasıyla maskeleniyor, testle).
- Testler: maliyet ve olgu birim testleri (IList, IReadOnlyList LINQ gerilemesi, partial, UCLASS makrolu sınıf, iç içe tipler, struct/record struct), 4 yeni kural fixture'ı, iz maskeleme testi. Yeni ortak `captured_logs` fikstürü (`tests/conftest.py`): `structlog.testing.capture_logs` projenin logger'ını görmüyordu, Faz 19'daki "iptal ERROR log'u üretmez" testi boşuna geçiyordu → artık pozitif kontrollü.
- Eval: `c-008` (C-MEM-003) ve `csharp-009` (CS-ALLOC-002) dev etiketlerine eklendi; static-only C ailesi koşuları (`--language c --language cpp --language csharp`) yenilendi (dev Big-O 92 → 96, P/R/F1 100/38/55 → 100/50/67; test 88 → 91, 100/42/59 → 84/44/58). README tabloları + karşılaştırılabilirlik notu, `docs/eval-findings.md` §5. `test_readme_table`: ana tablo filtresiz ya da tam C ailesi koşularını alır.
**Mimariden sapmalar (ADR linki):** yok.
**Denetim (kod-denetci):** Kritik yok. Orta: (O1) `IReadOnlyList` → `List` eşlemesi LINQ olgusunu kaybettiriyordu (Update'te CS-ALLOC-002 kayboluyordu) → eşlemeden çıkarıldı + gerileme testi; (O2) `partial` sınıfın tabansız parçası sıcak sayılmıyordu → düzeltildi + test; (O3) kurallar sıcak yolu adla eşliyor (aynı dosyada `class Sim { Update }` + MonoBehaviour `Update` varsa UNITY-PERF-001/UE-PERF-001 düz sınıfta da bulgu verir) → Sonraya; (O4) README notu; (O5) PROGRESS. Düşük (uygulanan): README ölçütü tam C ailesi, partial/UCLASS testleri.
**Açık sorular:**
- Test `c-016` 12. satır: etiket `resource_leak` (Faz 12 kararı), C-MEM-002 kural tablosunda `memory_safety`; doğru bulgular kategori uyuşmazlığından FP+FN sayılıyor (test precision %84). Etiket kategorisi `memory_safety`'ye çevrilsin mi, yoksa ikinci bir beklenen bulgu mu eklensin? (kullanıcı kararı)
**Bu fazda öğrendiğim:** `structlog.testing.capture_logs` yalnız global yapılandırmayı yakalar; kendi işlemci zinciriyle kurulan logger'lar için çıktı akışı yakalanmalı. Pozitif kontrolü olmayan "log yok" testi hiçbir şey kanıtlamaz.
**Sonradan (2026-10-01, f75499b):** `c-016` kararı verildi: ikinci beklenen bulgu (`memory_safety`, 12. satır, C-MEM-003) eklendi. Static-only C ailesi test koşusu yenilendi (P/R/F1 84/44/58 → 89/46/61, satır doğruluğu %100). LLM satırları eski etiketle puanlandı (README notu).

## Faz 23 — Notlar (dağıtım ve yollar)
**Kullanıcı kararları:** Faz 22 (canlı, kota) yerine önce çevrimdışı Faz 23.
**Yapılanlar:**
- `src/codementor/paths.py`: `resource_root()` (exe `_MEIPASS` → wheel `codementor/_resources` → depo kökü), `resource_path`, `resolve_relative`. `desktop/runtime.resource_root` buna devreder.
- `config.py`: tüm yol varsayılanları (`data.*`, `prompts.dir`, `validation.stub_header`/`roslyn_check_dll`, `verify.common_identifiers_file`) kaynak köküne göre mutlak; `_RelativeTomlSource` toml'daki göreli `Path` alanlarını toml dizinine göre çözer (alanlar model introspeksiyonuyla bulunur). Ortam/CLI değerleri çalışma dizinine göre kalır.
- `desktop/connections.MODELS_FILE` kaynak köküne göre.
- `pyproject.toml`: hatch `force-include` ile `data/`, `prompts/` → `codementor/_resources/`. Elle doğrulama: `uv build --wheel` → geçici venv'e kurulum → proje dışı dizinde `codementor questions list` ve bozulma modunda `analyze` çalıştı (C-BUF-001 bulundu, `prompt_version` depo ile aynı).
- `.gitattributes`: `* text=auto eol=lf` + ikili uzantılar. `git add --renormalize .` değişiklik üretmedi (indeks zaten LF).
- CI `exe` işi (windows-latest, `needs: check`, PR'da çalışmaz): `build_exe.py --both` → `CodeMentor-win64` artefaktı (exe + zip, 14 gün).
- Testler: `tests/unit/test_paths.py` (5), `test_config.py` (+4: varsayılanlar mutlak, toml göreli → toml dizini, env göreli → cwd, yabancı cwd'den veri/şablon/stub/model önerileri), `tests/unit/test_packaging.py` (wheel force-include, `.gitattributes`, CI exe işi). Paket testi ağa çıkmamak için `uv build` yerine yapılandırmayı denetler.
- Belgeler: ADR-0016, mimari §16/§17/§18 ve ADR tablosu, README (artefakt, yol çözümü), UYGULAMA_PLANI Faz 23.
**Mimariden sapmalar (ADR linki):** ADR-0016 (yol çözümü kuralı; exe yanındaki toml'un göreli yolları artık exe dizinine göre).
**Açık sorular:**
- ~~CI `exe` işi ilk kez push sonrası doğrulanacak~~ → ilk koşu derlemeden sonra cp1252 konsolda Türkçe çıktıda çöktü; `PYTHONIOENCODING=utf-8` + `build_exe.py` stdout'u UTF-8'e alıyor (8300441). Sonraki koşu yeşil, `CodeMentor-win64` artefaktı ~70 MB.
**Bu fazda öğrendiğim:** hatch `force-include` düzenlenebilir kurulumda `_resources` üretmiyor; bu yüzden kaynak kökü sırası (paket verisi varsa o, yoksa depo kökü) iki kurulum türünde de doğru çalışıyor.

## Faz 24 — Notlar (masaüstü kullanılabilirlik)
**Kullanıcı kararları:** Faz 22 (canlı) yerine önce Faz 24.
**Yapılanlar:**
- Arama: `desktop/search.py` (Tk'siz `find_all`/`step`, satır içi, örtüşmesiz, en fazla 2000 eşleşme), `widgets/find_bar.py` (editörün sağ üstünde; yazdıkça boyar, "i/N" sayacı, Enter/Shift+Enter, Esc `"break"` döndürerek uygulamanın Esc'ini — analizi durdurma — tetiklemez; tek satırlık seçim sorgu olur; metin değişince yenilenir). `CodeEditor` Ctrl+F bağlar.
- Dosyalar: yeni `desktop/files.py` `FileController` (`open_dialog`, `load`, `open_recent`, `on_drop`, `enable_drop`); `app.py`'deki `open_file`/`load_file` buraya taşındı (app 388 satır). `parse_drop_data` (tkdnd Tcl listesi, `{boşluklu yol}`), `recent_label`, `runtime.forget_file`. Araç çubuğunda "Son ▾" (dışa aktarma menüsüyle ortak `_popup`).
- Sürükle-bırak: `tkinterdnd2` bağımlılığı; `TkinterDnD._require(root)` + editör metnine `drop_target_register`. Yüklenemezse `drag_drop_unavailable` uyarısı, özellik kapalı. `build_exe.py` `--collect-all tkinterdnd2`. Kaynaktan çalışmada testle, exe'de dolaylı doğrulandı (exe açıldı, log'da uyarı yok); elle sürükleme kullanıcıya kaldı.
- toml'a yazma: `tomlkit` bağımlılığı; `desktop/config_writer.write_provider_prefs` yalnız `[providers] default` ve sağlayıcı başına `model`/`base_url`/`allow_tool_agent` yazar (yorumlar ve sıra korunur, boş geçersiz kılma bölüm açmaz, anahtar asla). `runtime.writable_config_file()`: exe'de exe yanındaki toml (yoksa paketteki varsayılan kopyalanır), kaynaktan etkin yapılandırma. Bağlantılar → Konumlar kartında "Seçimleri codementor.toml'a yaz"; bozuk toml/yazılamayan konumda Türkçe bildirim.
- Tier 1 iptali: `Runner` protokolü ve `run_tier1` `cancel: threading.Event` alır; `Orchestrator._tier1` `asyncio.to_thread` + `CancelledError`'da olayı set eder; `Orchestrator.tier1_runner` (test enjeksiyonu). Yan etki: API'de de Tier 1 olay döngüsünü kilitlemiyor.
- Testler: `test_search.py` (5), `test_files.py` (4), `test_config_writer.py` (5), `test_app.py` (+6: Ctrl+F, Esc analizi durdurmaz, son dosyalar + kaybolan dosya, bırakma, Windows'ta DnD kayıtlı, toml düğmesi + bozuk toml), `test_tier1.py` (+1 + spy imzası), `tests/integration/test_tier1_cancel.py` (bloklayan runner; iptal < 2 sn), `test_build_exe.py` (tkinterdnd2).
**Mimariden sapmalar (ADR linki):** yok; mimari §5.2.3'e iptal notu (Faz 19 kararının uzantısı).
**Açık sorular:**
- Sürükle-bırak exe'de elle denenmeli (dosyayı editöre sürükle).
- ~~Sonradan (a618d54): Linux CI'da `tkinter` yok; `desktop/files.py` modül düzeyinde `filedialog` içe aktardığı için `test_files.py` toplanamadı~~ → içe aktarma fonksiyona alındı. Tk gerektirmeyen masaüstü modülleri Tk'yi tembel içe aktarmalı.
**Bu fazda öğrendiğim:** `tkinterdnd2` içe aktarılınca `tkinter.BaseWidget`'a `drop_target_register`/`dnd_bind` ekler; CustomTkinter kökünde `TkinterDnD._require(root)` yeterli, `TkinterDnD.Tk` kökü gerekmez. Runner sahtesi imzası eksikse `run_tier1`'in geniş `except`'i hatayı yutar — test sahteleri protokolle birlikte güncellenmeli.

## Faz 25 — Notlar (sağlayıcılar, çevrimdışı kısım)
**Kullanıcı kararları:** agy canlı denemesi yapılmadı (yalnız çevrimdışı kısım). agy artık oturumlu (14 model, `gemini-3.8-*`); deneme istenirse `allow_tool_agent = true` + tek analiz.
**Yapılanlar:**
- `tests/providers/fake_cli_script.py` + `test_cli_agent_e2e.py` (4): sahte CLI Windows'ta distlib başlatıcısıyla `.exe`'ye sarılır (pip konsol betiği biçimi: başlatıcı + shebang + `__main__.py` zip'i; sağlayıcı `.cmd` çalıştırmadığı ve ortam temizlendiği için giriş noktası/PYTHONPATH kullanılamaz), POSIX'te shebang'li betik. Denetlenenler: kullanıcı kodu ve sistem mesajı argv'de değil stdin'de; çalışma dizini boş ve testinkinden farklı; `OPENAI_API_KEY` ve rastgele değişken ortamda yok, sessiz mod değişkenleri var; agy `--sandbox --mode plan`; çıktı önündeki gürültü satırına rağmen JSON ayrıştırılır; iptal 60 sn uyuyan süreci < 5 sn'de öldürür. Dev bağımlılık: `distlib`.
- `pipeline/cost.py`: `load_pricing` (mtime önbellekli), `estimate_cost`. `config.data.pricing_file` (varsayılan `data/pricing.yaml`). Eval `pricing_for(settings)` + `metrics.cost_estimate` aynı işlevi kullanır (eski `questions_dir.parent` yolu kalktı).
- `LLMSession._usage`: giriş ve çıkış 0 ise `estimate_messages`/`estimate_tokens` ile yaklaşık sayım; sağlayıcının kendi `estimated` bayrağı da taşınır. `ReportMeta.usage_estimated` ve `cost_est` (varsayılanlı, eski önbellek raporları okunur). Orkestratör maliyeti rapor oluştururken hesaplar.
- CLI alt satırı `token 10/5 (tahmini) · ~$0.0012`. Şemalar (`schemas/report.schema.json`) ve web tipleri (`web/src/types/report.ts`) üretildi; mimari §6.4, §6.5, §13; `tests/golden/report_example.json`, `api/examples/report.json`.
- Testler: `test_usage.py` (8), `test_report_render.py` (+1), `test_models.py` alan listesi.
**Mimariden sapmalar (ADR linki):** yok (mimari §13 zaten `usage_estimated` öngörüyordu; `config/pricing.yaml` yolu `data/pricing.yaml` olarak düzeltildi).
**Kapsam dışı bırakılanlar (gerekçeli):**
- OpenAI katı modunda kısıt anahtar sözcükleri: kaynaklar çelişiyor (`minItems`/`maxItems` reddi — mastra #23321; `minLength`/`maxLength` kabulü — pydantic-ai #7315), resmî liste alınamadı, anahtar yok. Yanlış kısıt her isteği 400'e düşürür; hepsini çıkarma davranışı korundu.
- `ProviderResult`'a şema yeteneği: tüketicisi yok (K5 her yanıtı doğruluyor).
**Açık sorular:** yok.
**Bu fazda öğrendiğim:** distlib `ScriptMaker.make()` düz `.py` betiğini Windows'ta exe'ye sarmaz, yalnız kopyalar; exe yalnız `ad = modül:fonksiyon` girişlerinden üretilir.

## Faz 26 — Notlar (API ve web)
**Yapılanlar:**
- Olay döngüsü: `Orchestrator._analyze` Tier 0'ı ve `stages.run_static`'i `asyncio.to_thread` ile koşar (Tier 1 Faz 24'ten beri). Aşama olayları artık iş parçacığından da yayınlanabildiği için `api/sse.py` tüm kuyruk yazımlarını `loop.call_soon_threadsafe` ile yapar (tek yol: FIFO sırası korunur, rapor son aşama olayını geçemez). SQLite çağrıları bilinçli olarak döngüde (ms düzeyi; bağlantı paylaşımı riski).
- `prompts/templates.prompt_version`: (yol, mtime_ns, boyut) imzası `lru_cache` anahtarı; değişmedikçe dosya okunmaz. Sürüm değeri aynı kaldı (`v1+e485058f`).
- `api/auth.py`: `api.api_key_env` → ortamda anahtar varsa `/v1/*` için ara katman (OPTIONS ve `/health` muaf), `hmac.compare_digest`, 401 problem+json + `WWW-Authenticate: ApiKey`, anahtar log maskesine kayıtlı; CORS `x-api-key` başlığına izin verir. Hız sınırı yok (Sonraya).
- `GET /v1/analyses/{id}/markdown` (`text/markdown`, kod içermez); mimari §9 tablosu ve hata kodları (401).
- Şema: `schemas/provider_status.schema.json` + web tipi (web tipleri yalnız şemadan, Faz 13 kuralı).
- Web: `fetchProviders`, `fetchExport`; `components/ReportDownload.tsx` (JSON tarayıcıdan, Markdown/SARIF sunucudan, `lib/download.saveBlob`); `Controls` sağlayıcı (hazır olmayan devre dışı, model adıyla) ve mod seçimi → istekteki mevcut `provider`/`options.mode`; `CodeEditor` `React.lazy` + `Suspense` iskeleti, `monaco-setup` editör parçasına taşındı. Build: ilk JS 2954 kB → 236 kB (gzip 773 → 75 kB), CSS 102 → 3,6 kB; Monaco `CodeEditor` parçasında 2720 kB.
- README GIF: e2e'de 4 kare (1440×900; aç → sağlayıcı/mod → analiz → bulguya git) → `tools/make_demo_gif.py` (Pillow; ortak palet tüm karelerden — yalnız ilk kareden alınınca kareler aynılaşıp birleşiyordu, testle sabit) → `docs/img/web-demo.gif` 50 KB. ffmpeg gerekmez.
- `YAPILANLAR.md` Faz 8-12 özetleri; README'deki "komutlar depo kökünden" cümlesi Faz 23'e göre düzeltildi, API anahtarı notu.
- Testler: `tests/api/test_api_auth.py` (5), `test_routes.py` (markdown + 404), `tests/integration/test_offloop.py` (yavaşlatılmış Tier 0/statik başka iş parçacığında, döngü ≥ 20 tık), `test_prompt_version.py` (+2), `tests/tools/test_make_demo_gif.py` (2), `test_schema_export.py`; web `App.test.tsx` (+3: tembel editör, sağlayıcı/mod isteğe yansır, indirme), e2e GIF kareleri + yeni denetimlerle mobil taşma testi geçiyor.
**Mimariden sapmalar (ADR linki):** yok (§9'a uç nokta ve isteğe bağlı anahtar eklendi).
**Açık sorular:** yok.
**Bu fazda öğrendiğim:** Bu ortamda kabuk heredoc'undan Python'a geçen `\0`, `\n` gibi kaçışlar gerçek karakterlere dönüşebiliyor (prompt_version'da NUL baytı oluştu) — kaçış içeren kod Write/Edit aracıyla ya da `chr(92)` ile yazılmalı. Projede biçimlendirici olmayan web dosyalarında `npx prettier` çalıştırmak kapsam dışı fark üretir.

## Faz 27 — Notlar (sağlamlık, dar kapsam)
**Yapılanlar:**
- CI: Linux `check` işine `actions/setup-dotnet` (10.0.x) + `dotnet build tools/roslyn-check`; pytest adımında `CODEMENTOR_REQUIRE_ROSLYN=1` → `test_roslyn_available_when_required` Roslyn yoksa başarısız (C# derleyici testleri artık sessizce atlanamaz). `exe` işi de Roslyn'i derler; `build_exe.py` `tools/roslyn-check/out` varsa pakete koyar (Faz 23 Sonraya maddesi).
- `cli/encoding.py` `ensure_utf8_console()`: Typer geri çağrısında stdout/stderr UTF-8 değilse `reconfigure(encoding="utf-8", errors="replace")`. Yerelde yeniden üretildi: cp1254'te Rich `✗` → `UnicodeEncodeError`; artık `PYTHONIOENCODING` gerekmez.
- `LLMSocraticOutput.guiding_questions` öğeleri `max_length=1000` (`MAX_QUESTION_CHARS`; sızıntı denetimi aynı sabiti kullanır). Şemalar (`llm_socratic`, `llm_single_pass`) yeniden üretildi; Anthropic/OpenAI adaptörleri kısıtı zaten çıkarıyor (K5 doğrular).
- `AnalysisReport.analysis_id` `ULID_PATTERN` (Crockford base32, 26). Mevcut 398 kimlik (eval sonuçları, örnekler, golden) önceden tarandı: hepsi uyumlu. API `_stored`: biçim dışı kimlik veritabanına gitmeden 404 (varlık sızdırmaz).
- Testler: `test_cli_encoding.py` (3), `test_models.py` (+9: 7 bozuk kimlik, `new_ulid` uyumu, soru uzunluğu), `test_routes.py` (+2 yol), `test_packaging.py` (CI Roslyn adımları ve sırası), `tests/compiler` koruma testi.
**Mimariden sapmalar (ADR linki):** yok (§6.3, §6.4 biçim sınırları eklendi).
**Kapsam dışı (gerekçeli):** tree-sitter süre sınırı (ölçüm: en kötü kötü niyetli girdi `"a<"*20000` = 40 KB sınırı içinde ~380 ms; ayrıştırma Faz 26'dan beri iş parçacığında; `parse` `None` dönerse tüm çağıranların ele alması gerekir), gcc kolon birimi ve Windows g++ zaman aşımı (yerelde gcc yok, doğrulanamaz), C++ ham metin maskeleme ve Tier 0 ERROR özeti D2 (include koruması fail-closed, nadir), `parse_bigo` uzantıları (eval'de görülmeden erken), `#pragma` izin listesi, `ue_stubs.h` (eval gürültüsüne göre). "Ara sıra düşen test" için somut kayıt yok; Tk açılış hatası zaten yeniden denemeyle ele alınıyor.
**Açık sorular:** yok.
**Push sonrası bulunan (8d080c4 → faz/27-roslyn-linux):** koruma testi işe yaradı: Linux'ta C# derleyici testleri ilk kez koştu ve hepsi `tool_error` ile düştü (daha önce sessizce atlanıyordu, yani Linux sunucuda C# Tier 1 hiç çalışmıyordu). Teşhis için Roslyn araç hatasında çıkış kodu + maskeli stderr başı log'a yazılıyor (gcc/clang stderr'i kod içerebileceği için loglanmaz). Log: CoreCLR açılışta "Out Of Memory" (0x8007000E, çıkış 137). Sebep: .NET'in Linux'ta varsayılan W^X çift eşlemesi memfd'yi büyütüyor, POSIX `RLIMIT_FSIZE` (1 MB) buna izin vermiyor. Çözüm: Roslyn ortamına `DOTNET_EnableWriteXorExecute=0` (Roslyn kod çalıştırmaz; dosya boyutu sınırı korunur). Dalda elle tetiklenen CI: Linux'ta 15 derleyici testi geçti, exe Roslyn'le derlendi. Ayrıca mimari Markdown kod bloğu ruff biçimine uymuyordu (ruff `.md` içindeki Python'u da biçimler).
**Bu fazda öğrendiğim:** Atlanabilir (skipif) testler CI'da araç kurulumu bozulduğunda sessizce yeşil kalır; zorunluluk bayrağıyla bir koruma testi bunu yakalar. Araç süreçlerine konan kaynak sınırları (ör. dosya boyutu) çalışma zamanlarının iç mekanizmalarını (W^X memfd) beklenmedik biçimde kırabilir; hata metni loglanmadan teşhis edilemezdi.

## Faz 22 — Notlar (Aşama A: eval analiz araçları, çevrimdışı)
**Yapılanlar:**
- `eval/analysis.py` + `codementor eval analyze <sonuç.json> [--dataset] [--out]`: katı P/R/F1, kategorisiz (yalnız satır) eşleşme, `low` hariç ölçüm, kategori karışıklık tablosu, örnek bazında FP/FN listesi (Markdown). `match_findings` / `audit_metrics` `ignore_category` aldı (varsayılan davranış ve §14.2 metrikleri değişmedi).
- `Metrics.guard_interventions` (varsayılan `None`, eski sonuç dosyaları okunur): sızıntı korumasının devreye girdiği örnek sayısı (`leak_check` regenerated/dropped_questions ya da temizleme uyarısı). Uyarı metinleri `pipeline/stages.py`'de `SCRUB_WARNING_*` sabitleri oldu. Mevcut dev koşularında ADR-0003'ün elle sayılmış değerleriyle birebir aynı (two_pass 2, single_pass 6).
- `eval breakdown` tablosu: p50 (sn), token ortalaması, koruma sütunları. `compare.seconds/tokens` ortak biçimleyiciler; README tablosu değişmedi.
- `docs/eval-findings.md` §6: mevcut dev koşularının analizi ve Aşama B prompt önerisi.
- Testler: `test_analyze.py` (12), `test_metrics.py` (+4), `test_breakdown.py` (+1).
**Bulgu (özet):** FP'lerin ana kaynağı fazla bulgu sayısı (C ailesi two_pass: 26 beklenen bulguya 82 tahmin). Kategori karışıklığı küçük (60 FP'nin 4'ü). `low` önemli tahminler FP'lerin %45'i; bunları atmak C ailesinde P'yi %27'den %40'a çıkarıyor, işaretleme dillerinde ise R'yi %95'ten %60'a düşürüyor. Elle sınıflandırma: savunmacı girdi denetimi ~15, gereksinim karşılanmamış ~8 (büyük olasılıkla doğru, etiketsiz), kuramsal uç değer ~4.
**Mimariden sapmalar (ADR linki):** yok (§14.2 metriklerine ek analiz; eşleşme kuralı değişmedi).
**Açık sorular:** (1) Aşama B (canlı, claude_cli kotası) onayı. (2) Soru gereksinimi karşılanmadığı için bildirilen `design` bulguları dev etiketlerine eklensin mi (precision artar, Faz 12 kıyası bozulur)?

## Faz 22 Aşama B — Notlar (precision için prompt ayarı, canlı, yalnız dev)
**Yapılanlar:**
- Prompt (`prompts/v1/`): `_core_rules.j2`'ye "sorun" ölçütü, kod dilleri için kategori tanımları (`input_handling`, `edge_case`, `design`; soru şartı varsa kendi kategorisi), gereksinim bulgusunun konum kuralı, önem tanımları ve `low` ≤ 2; `_markup_rules.j2`'ye sorun/öneri ayrımı; görevde en fazla 6 bulgu (önceden 10); ilk Python few-shot (`python_none_window_sum.yaml`).
- Dev etiketleri (kullanıcı kararı (a)): 7 C ailesi örneğine soru gereksinimi bulguları; `unreal-011` artık temiz değil. Statik dev satırı yeniden koşuldu.
- Sonuç (güncel etiketlerle): C ailesi P/R/F1 34/80/48 → 67/86/75, Python/HTML/CSS 54/95/69 → 68/85/76; sızıntı %0, injection %100, Big-O %96, p50 23,5 → 17,5 sn. Ayrıntı ve iki ayar turu: `docs/eval-findings.md` §7. İlk tur sonuçları `eval/results/iterations/`.
- Testler: `test_prompt_precision.py` (6), `test_fewshot.py` Python kombinasyonu, prompt golden'ları güncellendi (fark yalnız kural satırları).
**Mimariden sapmalar (ADR linki):** yok (§14 kuralına uygun: yalnız dev'de ayar).
**Açık sorular:** (1) `memory_safety` / `undefined_behavior` etiket sınırı tutarsız (`unreal-009` null Cast `memory_safety`, `unreal-014` yineleyici geçersizleşmesi `undefined_behavior`); kalan 3 FP/FN buradan. (2) Sızıntı korumasının müdahalesi C ailesinde 2 → 6 (son çıktı yine %0); sebep ölçülmedi. (3) `private/solutions/` dosyaları eksik (`reference_solution_unreadable` uyarıları; Faz 30'da yazılacak).
**Bu fazda öğrendiğim:** Prompt'a kategori eşlemesi eklemeden önce veri setinin etiket kurallarına bakmak gerekiyordu; çelişen bir cümle 3 doğru bulguyu kaçırttı. Bulgu modelden değil sistemden gelen `confidence` (sabit 0,7) eşik olarak kullanılamaz.

## Faz 28 — Notlar (Codex CLI sağlayıcısı; ADR-0017)
**Yapılanlar:**
- `providers/codex_cli.py` → `CodexCliProvider`: `codex --no-daemon exec --sandbox read-only --ephemeral --skip-git-repo-check --ignore-user-config --ignore-rules --json --color never --output-schema <geçici>/schema.json --cd <geçici> --model <m> -`; prompt stdin'den; şema OpenAI katı biçimi; JSONL ayrıştırma (son `agent_message`, `turn.completed` kullanımı, `turn.failed`/`error`); kullanım sınırı yeniden denenmez, oturum yoksa `codex login` önerisi. `allow_tool_agent` açık onayı (agy gibi). `cli_agent.py`'ye dokunulmadı (400 satır sınırı); yalnız `CODEX_HOME` profil değişkeni eklendi.
- `config.CodexConfig`, `codementor.toml [providers.codex]`, fabrika/sağlık/CLI listeleri; masaüstü Bağlantılar kartı (`codex login status` + `codex debug models` ile model listesi, araç onayı anahtarı, `codex login` ile oturum açma). `TOOL_AGENTS` sabiti (agy, codex).
- Canlı: `c-012` uçtan uca analiz `gpt-6-luna` ile 14,6 sn (use-after-free + gereksinim bulgusu, Sokratik sorular, sızıntı denetimi geçti); `tests/live` Codex testi geçti. Katalogdaki her model hesaba açık değil: `gpt-5.5` 404 (hata metni bunu söylüyor).
- Testler: `test_codex_cli.py` (14), `test_connections.py` (+5), e2e sahte `codex` (gerçek `run_process`), canlı test parametresi.
- **agy argv düzeltmesi (2026-10-03):** `agy` 1.2.14'te `-p` değer alıyor; bizim `-p --output-format …` argv'miz bayrağı prompt sanıyordu. Yeni `providers/agy_stream.py`: `agy --input-format stream-json --output-format stream-json …` (`-p` yok); stdin tek NDJSON satırı `{"event":"user","message":{"role":"user","content":<render_prompt>}}` (biçim canlı yoklamayla bulundu: agy yanlış biçimde anında `status:"ERROR"` + `error` döner); çıktıdan son `{"event":"result","result":{…}}` satır düzeyinde okunur. `--print-timeout` = zaman aşımı − min(10 sn, %10): agy kısmi sonucunu bizden önce yazar; boş yanıt + stderr `print timeout` → `CliTimeoutError`; `ERROR` → agy'nin hata metniyle `ProviderRequestError`. `cli_agent.py` 392 satır (taşıma ayrı modülde). Testler: `test_agy_stream.py` (6), `test_cli_agent.py` (+5, güncellenen 3), e2e sahte agy NDJSON çözer.
**Mimariden sapmalar (ADR linki):** ADR-0017 (yeni CLI ajanı; ADR-0012 kuralları korunur). agy taşıma değişikliği ADR gerektirmedi (ADR-0012 aynen).
**Açık sorular:** (1) **agy hesabı:** oturum açık (`agy models` 14 model listeliyor) ama her modelde (Gemini 3.8 Flash, Claude Sonnet 4.6) tur başlıyor, `streamGenerateContent` isteği gidiyor ve 60 sn'de hiç adım gelmiyor (`num_turns: 0`). Bizim argv'den bağımsız (düz `agy -p "merhaba"` de aynı). Kullanıcının etkileşimli `agy` ile yanıt alıp alamadığı bekleniyor; alırsa tek analizle canlı doğrulama. (2) API anahtarı yok: Gemini API sağlayıcısı ve OpenAI/DeepSeek canlı teşhisi ertelendi.
**Bu fazda öğrendiğim:** CLI'ların bayrak sözdizimi sürümle değişiyor (agy `-p`); her CLI için sürümü ve `--help`'i canlı kontrol etmek, sahte betikli testlerin göremediği hatayı gösteriyor. Model kataloğu ≠ erişim.

## Sonraya (kapsam dışı fikirler)
- Faz 26: API hız sınırı (istemci başına, süreçler arası doğru); web arayüzünün API anahtarı göndermesi.
- Faz 26: SQLite çağrılarını da iş parçacığına almak (bağlantı başına iş parçacığı ya da havuz).
- Faz 25: OpenAI katı mod kısıtlarını canlı anahtarla doğrulayıp `SchemaAdapter.openai_strict`'te desteklenenleri korumak.
- Faz 25: masaüstü ve web raporunda tahmini token/maliyet gösterimi (şu an yalnız CLI alt satırı ve JSON).
- Faz 25: agy canlı doğrulaması (oturum var; `allow_tool_agent = true` ile tek analiz).
- Faz 24: arama büyük/küçük harf ve "tam sözcük" seçenekleri, değiştir (Ctrl+H); bırakılan klasördeki kaynak dosyalarını listeleme.
- Faz 24: toml'a yazıldıktan sonra masaüstü tercihlerindeki aynı geçersiz kılmalar gereksizleşir (zararsız); "toml'dan yeniden yükle" düğmesi yok.
- Faz 23: `reference_solution_path` (`private/solutions/`) hâlâ çalışma dizinine göre; soru dosyasının ya da kaynak kökünün dizinine göre çözülmeli (sızıntı testi buna göre güncellenmeli).
- Faz 23: mimari §20 ADR tablosunda ADR-0013/0014/0015 satırları eksik.
- ~~Faz 23: CI exe işi Roslyn denetleyicisini derlemiyor~~ → Faz 27.
- Faz 21 denetimi O3: kurallar sıcak yolu fonksiyon **adıyla** eşliyor (`RuleContext.hot_functions`, `CallFact.function`); aynı dosyada tabansız sınıfta ve MonoBehaviour'da aynı adlı `Update` varsa UNITY-PERF-001/UE-PERF-001 düz sınıfta da bulgu verir (UNITY-GC-001 `in_hot_path` kullandığı için doğru). Olgulara fonksiyon kimliği (satır) eklenmeli.
- Faz 21: `rules_version` yalnız `rules/*.py` hash'i; `analysis/` ve `data/call_costs.yaml` değişiklikleri önbellek anahtarına yansımıyor (bayat önbellek riski).
- Faz 21: `log.exception` izi sınırsız ve CLI'da WARNING düzeyinde stderr'e basılır; kural istisna mesajı kullanıcı kodu parçası içerebilir (§12) — iz DEBUG'a ya da kısaltılmış mesaja alınabilir. `captured_logs` teardown'u önceki yapılandırmayı değil varsayılanı geri yükler.
- Faz 21: `file_value_types` ad çakışması (`struct Hit` + başka ad alanında `class Hit`) nadir yanlış negatif; yalnız arayüzden türeyen `class A : IFoo` sıcak sayılır (muhafazakâr).
- Faz 21'den kalan (yol haritası Faz 21 geniş kapsamı): C-MEM-001 aynı dosyadaki kullanıcı fonksiyonu, UE-GC-001 `TArray<AActor*>`/`TMap` alanları ve `FPlain` önerisi, C-MEM-003 akış duyarlılığı, döngüde `std::string +`/C# `string +=` karesel ipucu.
- ~~Faz 16: eval veri setine Python/HTML/CSS örnekleri ve ölçüm~~ → Faz 18'de yapıldı.
- ~~Faz 18: Tier 0 `</div>` kör noktası~~ → Faz 20'de HTML-STD-003 ile bulgu olarak.
- Faz 20: HTML-STD-003 kaçırmaları: dosya sonunda bitmemiş `<div`, `<p><span>a<div>` (örtük kapanış yalnız yığın tepesine bakıyor), DOCTYPE'sız (quirks) belgede `table` `p`'yi kapatmaz; aynı satırda kapanmayan + eşsiz bulgu varsa motor ilkini tutar (eşsiz sorusu görünmez); katalogda yalnız ana açıklama var.
- Kural motoru: bulgu sayısına üst sınır yok (600 satırlık kötü niyetli girdi 600 bulgu üretip prompt'a gidebilir).
- ~~Faz 18: `codementor eval check-drafts` Windows konsolunda (cp1254) çöküyor~~ → Faz 27 (konsol UTF-8).
- Faz 18: eski veri seti etiketlerine Faz 17 bulguları (`c-008` 4. satır `memory_safety` C-MEM-003, `csharp-009` 11. satır `garbage_collection` CS-ALLOC-002) eklenmeli mi? (test etiketleri de etkilenebilir; kullanıcı kararı)
- Faz 18: HTML precision (%22) için işaretleme prompt'unda bulgu ölçütü ("iyi uygulama önerisi" ile "sorun" ayrımı); kategori tanımları (`design` vs `edge_case`). Ayar yalnız dev'de yapılmalı.
- Faz 18: `eval breakdown` tablosuna gecikme/token sütunları; `breakdown` etiketleri koşu anındaki değil güncel veri setinden alıyor.
- ~~Faz 16: HTML etiket dengesi denetimi~~ → Faz 20 (statik kural).
- Faz 16: Python için few-shot örnekleri; JS (tarayıcı) desteği HTML ile birlikte istenebilir.
- Faz 15: Bağlantılar'da Ollama modelini indirme (`ollama pull`) düğmesi ve ilerleme göstergesi.
- ~~Faz 15: Masaüstü tercihleri ile `codementor.toml` arasında "toml'a yaz" seçeneği.~~ → Faz 24
- Faz 14: exe imzası yok; Windows SmartScreen ilk açılışta uyarabilir (kod imzalama sertifikası + Inno Setup kurulum paketi).
- ~~Faz 14: CI'da Windows exe derleme işi (artefakt olarak zip); şu an elle `make exe`.~~ → Faz 23
- ~~Faz 14: analiz iptali yok~~ → Faz 19'da yapıldı.
- ~~Faz 19: Tier 1 derleyici/çalıştırma sürecine iptal olayı iletilmiyor~~ → Faz 24 (durdurulan analizde Tier 1 kendi zaman aşımına kadar sürebilir; arayüz bu sırada yeni analizi bildirimle reddeder).
- ~~Faz 14: editörde arama (Ctrl+F), son dosyalar menüsü, sürükle-bırak ile dosya açma (tkinterdnd2).~~ → Faz 24
- Faz 14: onefile açılışı arşiv çözme nedeniyle birkaç saniye; hızlı açılış için onedir zip önerilir.
- Faz 5/6 öncesi: tree-sitter ayrıştırmasına süre sınırı (`progress_callback` ile iptal). Kötü niyetli C++ girdisi (`"a<" * 20000`) Tier 0'da ~240 ms sürüyor; gerçekçi girdide 1–4 ms.
- Tier 0: kapanmamış blok varken dosya sonuna uzanan ERROR düğümleri özet mesajla değiştiriliyor; son satırdaki ayrı bir gerçek hata bu durumda ayrıca raporlanmayabilir (denetim D2, etkisi sınırlı).
- `mask_non_code` C++ ham metinlerini (`R"(...)"`) tanımıyor; içlerinde `"` geçerse maskeleme erken biter (öğrenci kodunda nadir).
- ~~`data/` dizini paket dışında; `pip install` ile dağıtımda veri dosyaları gelmez. Faz 13'te (Docker/dağıtım) `importlib.resources` veya paket verisi olarak ele alınmalı.~~ → Faz 23
- ~~Göreli veri dizinleri (`data.questions_dir`) çalışma dizinine göre çözülüyor; proje dışından çalıştırınca bulunamıyor. Config dosyasına göre çözme veya paket verisi (yukarıdaki madde) ile birlikte ele alınmalı.~~ → Faz 23
- ~~`.gitattributes` ile `* text=auto eol=lf`: Windows'taki CRLF uyarılarını ve şema dosyalarında satır sonu farklarını önler.~~ → Faz 23
- `parse_bigo` şu an `log log n`, `n^n`, `Θ(...)`/`Ω(...)`, `max(n,m)` ve `k` gibi değişken üsleri desteklemiyor; eval'de LLM çıktılarında görülürse eklenebilir.
- ~~`AnalysisReport.analysis_id` için ULID biçim doğrulaması~~ → Faz 27.
- ~~CI'a `actions/setup-dotnet` + `make roslyn-check` adımı~~ → Faz 27.
- `ue_stubs.h` genişletilebilir (`Super` için `GENERATED_BODY` yerine sınıf başına typedef mümkün değil; delegeler `OnDestroyed.AddDynamic`, `FTimerManager`); eval'de Unreal uyarı gürültüsüne göre karar verilmeli.
- ~~`validation.stub_header` / `roslyn_check_dll` göreli yolları da çalışma dizinine göre çözülüyor (veri dizinleri maddesiyle birlikte ele alınmalı).~~ → Faz 23
- `#pragma` makro genişletmeli biçimleri (`#pragma MACRO`) ve `#line` şu an serbest; derleyici kaynak okumadığı için risk düşük, ama include korumasına izin listesi eklenebilir.
- gcc kolonları "display" birimli, clang bayt; Tier 0 karakter. Unicode içeren satırlarda kolonlar farklı olabilir (`-fdiagnostics-column-unit=byte` gcc ≥ 11).
- ~~Faz 6'da ertelenen 10 statik kural~~ → Faz 17'de yapıldı (2026-10-01).
- Faz 17: C-MEM-003 denetimin kullanımdan sonra yapıldığını görmüyor (akış duyarlılığı yok); UNITY-GC-001 closure bastırması satır bazlı.
- C-MEM-001: aynı dosyadaki kullanıcı fonksiyonuna geçirilen işaretçi (`print_arr(arr, n)`) sahiplik aktarımı sayılıyor (sık kaçırma); çağrılan fonksiyon aynı dosyadaysa ve `free`/saklama yoksa bulgu verilebilir. Aynı değişkene iki kez `malloc`, gölgeleme ve `realloc` de bilinçli sınırlar.
- UNITY-GC-001: dosyada tanımlı kullanıcı `struct`'ı için `new Hit(3)` yanlış bulgu (değer tipi); Faz 5 `CSHARP_VALUE_TYPES` dosyadaki struct adlarıyla genişletilebilir.
- UE-GC-001: `TArray<AActor*>`/`TMap<..., UObject*>` kapsayıcı alanları kaçırılıyor; UCLASS olmayan sınıfta (`FPlain`) öneri `UPROPERTY` değil `TStrongObjectPtr`/`FGCObject` olmalı.
- CS-PERF-001: `IList`/`IReadOnlyList`/`ICollection` tipli değişkenler maliyet tablosunda çözülmüyor (kaçırma).
- Kural motoru: çöken kuralın istisna izi loglanmıyor; structlog (Faz 10) ile `log.exception` eklenmeli.
- Sıcak yol tespiti sınıf tabanını (MonoBehaviour / UCLASS) da denetlemeli (Faz 5 olgusu).
- Faz 7: OpenAI katı modu bugün `maxLength`, `maxItems`, `pattern`, `minimum`, `maximum` destekliyor; `SchemaAdapter` kısıt temizliğini sağlayıcıya göre ayırabilir (şu an hepsi çıkarılıyor, K5 doğruluyor).
- Faz 7: `ProviderResult`'a yanıt veren sağlayıcının yeteneği (şema zorlandı mı) eklenebilir; fallback sonrası K5 için.
- Faz 7: `FakeReply` bir dataclass olarak `providers/fake.py`'de (Pydantic şeması değil, test düzeneği); gerekirse `models/`'e taşınabilir.
- ~~Faz 7: token tahmini ve `pricing.yaml` maliyet tahmini (mimari §13)~~ → Faz 25.
- ~~Faz 4 `run_process` çıplak `argv[0]`~~ → çözüldü (2026-09-29): yalnızca mutlak yol, `test_bare_or_relative_executable_rejected`.
- ~~CLI ajanları: gerçek `run_process` ile uçtan uca test~~ → Faz 25; agy canlı doğrulaması hâlâ açık (oturum var).
- Faz 8: `call_costs.yaml`'a C# `RemoveAll`/`RemoveAt(0)`/`Insert(0, …)` maliyetleri (golden'da `Remove: O(1)` ipucu).
- ~~Faz 8 denetim D3 (`&lt;` kanıtı)~~ → Faz 9'da çözüldü (`normalize_evidence`).
- ~~Faz 8 denetim D2: `prompt_version` her build'de şablon dosyalarını okuyor~~ → Faz 26.
- Faz 8 denetim D8: ~~`prompts.dir`~~ Faz 23'te çözüldü; demo'nun golden dizini (`tests/golden/prompts`, geliştirici aracı) hâlâ çalışma dizinine göre.
- Faz 8: prompt'ların `claude_cli` ile canlı karşılaştırması (analysis vs single_pass) Faz 12 eval'inde; token tahmininin gerçek `usage` ile kalibrasyonu.
- ~~Faz 9: sızıntı korumasını `reasoning_steps` ve LLM açıklamalarına genişletmek~~ → Faz 10'da yapıldı.
- ~~Faz 9: `guiding_questions` öğelerine şemada `max_length`~~ → Faz 27.
- ~~Faz 10: `prompt_version` mtime önbelleği~~ → Faz 26.
- Faz 10: CLI ilerleme göstergesi yalnızca aşama adını gösteriyor; token/süre canlı gösterilebilir.
- ~~Faz 11: senkron aşamaları `asyncio.to_thread`'e taşımak~~ → Faz 24 (Tier 1) + Faz 26 (Tier 0, olgular); SQLite Sonraya.
- Faz 11: API anahtarı / hız sınırlama (§12); yerel olmayan bağlamada zorunlu kılınabilir. (Faz 13 kararı: v1'de yok, README Sınırlamalar.)
- ~~CLI ajanı iptali~~ → Faz 19'da yapıldı.
- ~~Faz 5 hatası (csharp-011): `foreach` koleksiyon ifadesindeki çağrı döngü içinde sayılıyordu → `high` O(n²)~~ → çözüldü (2026-09-30, kullanıcı isteğiyle Faz 12 içinde): `_context.contexts` döngü başlığında bir kez değerlendirilen alanlara (`initializer`, `right`: C `for` başlatıcısı, C++ range-for, C# `foreach`) dış bağlamı verir; `tests/fixtures/complexity/on_{foreach_header_call,range_for_header_call,for_initializer_strlen}` + koşuldaki `strlen` için `on2_strlen_condition`. Dev static-only Big-O %88 → %92.
- Çağrı maliyeti tablosu eksikleri (eval notları): `std::memset`/`memcpy` (n), `UGameplayStatics::GetAllActorsOfClass` (n), `TArray::Remove` (n); `std::string operator+` / C# `string +=` döngüde karesel (şu an n).
- ~~Faz 12: eval'e `guard_interventions` metriği~~ → Faz 22 Aşama A.
- Faz 12: `eval analyze` aracı (kategorisiz eşleşme, önem filtreli precision, örnek bazında FP/FN); `compare` statik satırında injection direncini "—" göstermeli.
- Faz 12: precision iyileştirme — `design` bulgularını yalnızca soru gereksinimi varken üretmek, `low` bulguları raporda ayrı göstermek; kategori belirsizliği (sıfıra bölme `edge_case`/`undefined_behavior`, null `edge_case`/`memory_safety`) için prompt'ta kategori tanımları. Değişiklik sonrası dev'de yeniden ölçülmeli (test artık kullanıldı).
- Faz 12: few-shot 0/1 ablasyonu (§14.4) koşulmadı. → Faz 34.
- CI Windows işi (2026-09-30): `windows-latest`'te g++ (MinGW) ilk derlemede 10 sn sınırını aşıyor (`test_cpp_type_error_failed` → `timeout`); clang++ varsayılan MSVC hedefli olduğundan Unreal stub denetimi `tool_error` ile atlanıyor (2 test). Ürün zarif atlıyor ama Windows'ta clang için `--target=x86_64-w64-mingw32` / başlık yolu ve soğuk başlangıç süresi ele alınmalı; o zamana kadar Windows CI `-m "not live and not compiler"`.
- ~~Faz 13: README için GIF demo~~ → Faz 26 (Pillow).
- ~~Faz 13: Web UI'da indirme, sağlayıcı ve mod seçimi~~ → Faz 26.
- ~~Faz 13: Monaco'yu tembel yükleme~~ → Faz 26.
- ~~Faz 13: `YAPILANLAR.md`'ye Faz 8–12 özetleri~~ → Faz 26.

## Yapılacaklar — yol haritası (2026-10-01, Faz 0-19 bitti)
Ayrıntılar "Sonraya" listesinde. Sıra önerilir; her faz dar tutulur.

**Kaldığımız yer (2026-10-02):** Faz 0-27 ve Faz 22 Aşama A `main`'de, push'lu, CI yeşil (93a9cc1).
Yeni sıra (ayrıntılı iş listeleri `docs/UYGULAMA_PLANI.md` "Yol haritası — 2026-10-02"):
1. ~~**Faz 22 Aşama B — precision**~~ Yapıldı (C ailesi F1 48 → 75; eval-findings §7). Sıradaki: Faz 28.
2. **Faz 28 — Sağlayıcılar:** Codex yapıldı (ADR-0017); agy argv düzeltildi (stream-json stdin). Kalan: agy canlı doğrulaması (hesapta tur yanıtsız; kullanıcının etkileşimli `agy` denemesi), API anahtarı gelince Gemini API ve OpenAI/DeepSeek teşhisi.
3. **Faz 29 — Derleyicisiz kullanıcı:** Tier 1 PATH'teki gcc/clang/dotnet'e bağlı; öneri: C/C++/
   Unreal için `zig cc`, C# için self-contained Roslyn; "Derleyiciyi indir" (sha256) ya da gömme. ADR.
4. **Faz 30 — Soru bankası:** 18 soru → dil/motor başına ≥ 8 (~64), zorluk dağılımı, filtreler.
   Kullanıcı soru havuzu verecek; soruları ve referans çözümleri Claude yazar.
5. **Faz 35 — Bulgu doğrulama geçişi (önemli):** her LLM bulgusu için ayrı bir "kanıtla"
   adımı; kanıtlanamayan düşer. Modelin kendi güveni şemaya (bugünkü `confidence` sistemden
   sabit 0,7 geliyor, ayırt etmiyor). ADR; dev'de doğrulamalı/doğrulamasız ölçüm.
6. **Faz 36 — Hatalar ve öneriler ayrımı (önemli):** bulguya `issue`/`suggestion`; raporda
   katlanmış "Öneriler"; Sokratik sorular yalnızca hatalardan; "temiz kod" few-shot örnekleri.
7. **Faz 31 — Güvenlik ve önbellek borcu:** bulgu üst sınırı, `rules_version` hash'i, log
   gizliliği, `reference_solution_path`, belge temizliği.
8. **Faz 32 — Statik kural doğruluğu II:** sıcak yol kimliği (O3), C-MEM-001, UNITY-GC-001 struct,
   UE-GC-001 `TArray`, CS-PERF-001 `IList`, maliyet tablosu.
9. **Faz 33 — Kullanıcı deneyimi:** token/maliyet gösterimi, arama/değiştir, CLI ilerleme.
10. **Faz 34 — Ölçümün genişletilmesi (canlı, isteğe bağlı):** ikinci model, few-shot ablasyonu,
   dev setini büyütme.

**Kullanıcı işleri:** (a) [Faz 30 kararıyla Claude yazacak] yeni 4 sorunun referans çözümleri `private/solutions/`
(`py-easy-word-count.py`, `py-medium-two-sum.py`, `html-easy-profile-card.html`,
`css-easy-centered-layout.css`); (b) eski eval etiketlerine Faz 17 bulguları eklensin mi
(`c-008` C-MEM-003, `csharp-009` CS-ALLOC-002)? — Faz 21'de eklendi. (c) Gereksinim karşılanmadığı
için bildirilen `design` bulguları dev etiketlerine eklensin mi (Faz 22 §6)? (d) Faz 28 teşhisi için
OpenAI/DeepSeek/Gemini hata metni ve anahtarlar.

1. ~~**Faz 20 — HTML etiket dengesi.**~~ Yapıldı. Kapanmamış/uyumsuz/eşsiz etiket uyarısı (stdlib
   `html.parser`, Tier 1 karşılığı); Faz 18'deki `</div>` kör noktası. Küçük, çevrimdışı.
2. ~~**Faz 21 — Statik kural ve maliyet tablosu doğruluğu.**~~ Dar kapsam yapıldı; kalanlar Sonraya'da. C-MEM-001 aynı dosyadaki kullanıcı
   fonksiyonu; UNITY-GC-001 kullanıcı `struct`'ı; UE-GC-001 `TArray<AActor*>`/`FPlain`;
   CS-PERF-001 `IList`; sıcak yolda sınıf tabanı (MonoBehaviour/UCLASS); C-MEM-003 akış
   duyarlılığı; maliyet tablosu (`memset`, `GetAllActorsOfClass`, `TArray::Remove`, C#
   `RemoveAt(0)`/`Insert(0)`, döngüde `string +=` karesel); çöken kural için `log.exception`;
   eski eval etiket kararı (b) uygulanır. Çevrimdışı.
3. **Faz 22 — Eval araçları ve precision (canlı, yalnız dev). — SIRADAKİ, planı hazır**
   (ayrıntılı iş listesi: `docs/UYGULAMA_PLANI.md` "Faz 22"; Aşama A çevrimdışı araçlar +
   mevcut dev koşularının analizi → kontrol noktası → Aşama B canlı prompt ayarı ve dev koşuları). `eval analyze` (kategorisiz
   eşleşme, önem filtresi, örnek bazında FP/FN), `guard_interventions` metriği, `breakdown`'a
   süre/token; prompt: işaretleme dillerinde "sorun" ölçütü, kategori tanımları (`design` /
   `edge_case`), `design` yalnız soru gereksinimiyle; Python few-shot; few-shot 0/1 ablasyonu.
4. ~~**Faz 23 — Dağıtım ve yollar.**~~ Yapıldı (ADR-0016). `data/` ve `prompts/` paket verisi (`importlib.resources`),
   göreli yolların config'e göre çözülmesi (veri, prompt, stub, Roslyn), `.gitattributes`
   (`eol=lf`), CI'da Windows exe derleme artefaktı (+ onedir zip). İmza/Inno Setup sertifika
   gerektirir (isteğe bağlı).
5. ~~**Faz 24 — Masaüstü kullanılabilirlik.**~~ Yapıldı. Editörde Ctrl+F, son dosyalar menüsü, sürükle-bırak,
   tercihleri `codementor.toml`'a yazma, Tier 1 sürecine iptal olayı.
6. ~~**Faz 25 — Sağlayıcılar ve CLI ajanları.**~~ Çevrimdışı kısım yapıldı (agy canlı ve OpenAI katı kısıtlar Sonraya). agy canlı doğrulaması; sahte CLI betiğiyle
   gerçek `run_process` uçtan uca testi; `ProviderResult`'a şema yeteneği; OpenAI katı mod
   kısıtları; token/maliyet tahmini (`pricing.yaml`). (Ollama indirme düğmesi: düşük öncelik.)
7. ~~**Faz 26 — API ve web.**~~ Yapıldı (hız sınırı Sonraya). Senkron aşamaları `asyncio.to_thread`'e taşıma, `prompt_version`
   mtime önbelleği, API anahtarı/hız sınırı (isteğe bağlı), web'de SARIF/Markdown indirme,
   sağlayıcı/mod seçimi, Monaco tembel yükleme, README GIF, `YAPILANLAR.md` Faz 8-12 özetleri.
8. ~~**Faz 27 — Sağlamlık ve teknik borç.**~~ Dar kapsam yapıldı (kalanlar gerekçeyle Sonraya). tree-sitter süre sınırı, Tier 0 ERROR özeti (D2),
   C++ ham metin maskeleme, `parse_bigo` uzantıları, ULID doğrulaması, `guiding_questions`
   `max_length`, `#pragma` izin listesi, gcc/clang kolon birimi, `ue_stubs.h`; CI'da dotnet +
   Roslyn, Windows g++ zaman aşımı; `check-drafts` Windows kodlaması; ara sıra düşen test.
