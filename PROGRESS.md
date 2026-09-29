# İlerleme Günlüğü

## Durum
| Faz | Durum | Dal | Tarih | Araç (uygulayan / denetleyen) |
|---|---|---|---|---|
| 0 | ✅ | faz/0-iskelet | 2026-09-29 | Claude Code / — |
| 1 | ✅ | faz/1-modeller | 2026-09-29 | Claude Code / — |
| 2 | ✅ | faz/2-soru-bankasi | 2026-09-29 | Claude Code / — |
| 3 | ✅ | faz/3-tier0 | 2026-09-29 | Claude Code / kod-denetci |
| 4 | ⏳ | | | |

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

## Sonraya (kapsam dışı fikirler)
- Faz 5/6 öncesi: tree-sitter ayrıştırmasına süre sınırı (`progress_callback` ile iptal). Kötü niyetli C++ girdisi (`"a<" * 20000`) Tier 0'da ~240 ms sürüyor; gerçekçi girdide 1–4 ms.
- Tier 0: kapanmamış blok varken dosya sonuna uzanan ERROR düğümleri özet mesajla değiştiriliyor; son satırdaki ayrı bir gerçek hata bu durumda ayrıca raporlanmayabilir (denetim D2, etkisi sınırlı).
- `mask_non_code` C++ ham metinlerini (`R"(...)"`) tanımıyor; içlerinde `"` geçerse maskeleme erken biter (öğrenci kodunda nadir).
- Faz 5: `call_costs.yaml` içindeki amortize `1*` gösterimi `parse_bigo`'ya verilmeden önce `*` ayıklanmalı (ya da `BigO`'ya `amortized` bayrağı). Faz 2'de soru bankası için `removesuffix("*")` yaklaşımı kullanıldı; ortak bir yardımcıya taşınabilir.
- `data/` dizini paket dışında; `pip install` ile dağıtımda veri dosyaları gelmez. Faz 13'te (Docker/dağıtım) `importlib.resources` veya paket verisi olarak ele alınmalı.
- Göreli veri dizinleri (`data.questions_dir`) çalışma dizinine göre çözülüyor; proje dışından çalıştırınca bulunamıyor. Config dosyasına göre çözme veya paket verisi (yukarıdaki madde) ile birlikte ele alınmalı.
- `.gitattributes` ile `* text=auto eol=lf`: Windows'taki CRLF uyarılarını ve şema dosyalarında satır sonu farklarını önler.
- `parse_bigo` şu an `log log n`, `n^n`, `Θ(...)`/`Ω(...)`, `max(n,m)` ve `k` gibi değişken üsleri desteklemiyor; eval'de LLM çıktılarında görülürse eklenebilir.
- `AnalysisReport.analysis_id` için ULID biçim doğrulaması (şu an serbest `str`, §6.4 böyle).
