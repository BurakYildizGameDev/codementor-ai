# İlerleme Günlüğü

> Faz 0-63'ün ayrıntılı notları ve eski yol haritası arşivde: [docs/gelistirme-gunlugu/PROGRESS-faz-0-63.md](docs/gelistirme-gunlugu/PROGRESS-faz-0-63.md). Yeni fazların notları buraya eklenir (AGENTS.md faz bitirme protokolü).

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
| 34 + 35B | ✅ | faz/34-eval-genisletme | 2026-10-03 | Claude Code / — |
| 37 | ✅ | faz/37-saglayici-sadelestirme | 2026-10-03 | Claude Code / — |
| 36 | ✅ | faz/36-hata-oneri | 2026-10-04 | Claude Code / — |
| 38 | ✅ Claude 96 ölçümü 2026-10-05 (77/88/82) | faz/36-hata-oneri | 2026-10-05 | Codex / Claude Code |
| 39 | ✅ (`cpp-007` canlıda doğrulandı) | faz/39-dogrulama-performans | 2026-10-04 | Claude Code / kod-denetci |
| 47 | ✅ | faz/47-api-guven-siniri | 2026-10-05 | Claude Code / — |
| 48 | ✅ | faz/48-rol-siniri-sure | 2026-10-05 | Claude Code / — |
| 49 | ✅ | faz/49-depolama-tutarlilik | 2026-10-05 | Claude Code / — |
| 50 | ✅ | faz/50-dil-kodlama-ci | 2026-10-05 | Claude Code / — |
| 51 | ✅ | faz/51-kategori | 2026-10-05 | Claude Code / — |
| 52 | ✅ (denetim düzeltmesiyle) | faz/52-kural-oneri | 2026-10-05 | Mimo (Cline) / Claude Code |
| 53 | ✅ (birleştirme kullanıcıda) | faz/53-54-kapsama-bolumleme | 2026-10-05 | Mimo (Cline) / Claude Code |
| 54 | ✅ | faz/53-54-kapsama-bolumleme | 2026-10-05 | Mimo (Cline) / Claude Code |
| 55 | ✅ (ADR-0024) | faz/55-tier0-saglamlik | 2026-10-06 | GLM (Cline) / Claude Code |
| 56 | ✅ | faz/56-html-std003-kenarlar | 2026-10-06 | Claude Code / kod-denetci |
| 57 | ✅ | faz/57-c-mem003-akis | 2026-10-06 | Claude Code / kod-denetci |
| 58 | ✅ | faz/58-toolchain-test-kararlilik | 2026-10-06 | Claude Code / — |
| 59 | ✅ (ADR-0025) | faz/59-tier0-alt-surec | 2026-10-06 | Claude Code / kod-denetci |
| 60 | ✅ | faz/60-surum-uyumu | 2026-10-06 | Antigravity / — |
| 61 | ✅ (ADR-0026) | faz/61-ipucu-merdiveni | 2026-10-07 | Antigravity / — |
| 62 | ✅ | faz/62-gecmis-silme | 2026-10-07 | Antigravity / — |
| 63 | ✅ | faz/63-agy-haiku-canli | 2026-10-09 | Claude Code / — |
| A1 | ✅ (denetim sonraya) | faz/a1-guvenlik | 2026-10-12 | Claude Code / — |
| A2 | ✅ (denetim sonraya) | faz/a2-guvenlik | 2026-10-13 | Claude Code / — |
| B | ✅ (denetim sonraya) | faz/b-bulgu-kaybi-onbellek | 2026-10-13 | Claude Code / — |
| K | ✅ (ADR-0028) | faz/k-kullanici-soru-token | 2026-10-13 | Claude Code / — |
| C | ✅ (denetim sonraya) | faz/c-ipucu-yapilandirma | 2026-10-13 | Claude Code / — |
| E | ✅ | faz/e-web | 2026-10-13 | Antigravity / — |
| F | ✅ (elle deneme + denetim sonraya) | faz/f-masaustu | 2026-10-14 | Antigravity / — |
| G | 🟡 (G0-G3; G2, G4-G7 açık) | faz/g-saglayici | 2026-10-15 | Cline / — |

## Faz G — Notlar (sağlayıcı sağlamlığı ve kod temizliği; 2026-10-15)

**G0 — `orchestrator.py` ve `passes.py` bölündü (dosya başına 400 satır kuralı):**
- `pipeline/orchestrator.py` 465 → 393 satır. Yeni modüller: `cache_flow.py` (önbellek anahtarı/imza,
  Tier 1 ayarı, deneme geri alma, rapor kaydı) ve `deadline.py` (`_timed_out`, `_remaining` gövdeleri).
  `Orchestrator` yöntemleri ince sarmalayıcı kaldı (`self._validation(...)`, `self._tier1(...)`,
  `self._remaining(...)`): testler `monkeypatch.setattr(Orchestrator, ...)` ile yamıyor, adlar korundu.
- `pipeline/passes.py` 426 → 330 satır. Yeni modüller: `llm_session.py` (`LLMSession`) ve
  `verify_pass.py` (`VERIFY_STAGES`, `VERIFY_FAILED`, `run_pass_verify`). Onarım/sokratik prompt kuran
  `run_pass_a`, `_socratic` ve `call_structured` bilinçli olarak `passes.py`'de kaldı: testler
  `passes.build_repair_messages` / `passes.build_socratic_messages`'i yamıyor.
- `passes.py` taşınan adları `__all__` ile yeniden dışa aktarır (`pipeline/assemble.py` ve
  `eval/runner.py` değişmedi). `verify_pass.run_pass_verify`, `call_structured`'i çağrı anında alır
  (döngüsel içe aktarma olmasın diye).
- `Orchestrator._report` gövdesi `assemble.assemble_with_cost` oldu (rapor + maliyet tahmini);
  `pipeline/assemble.py` 145 satır (< 400). `desktop/app.py` zaten 395 satır (F0).
- **Doğrulama:** davranış değişmedi — değişen dosyalar yalnız `src/` (test yok); `ruff` ve
  `ruff format --check` temiz; `mypy src/` 211 dosyada hatasız; `pytest -m "not live"` 3454 geçti,
  15 atlandı, 6 deselected (G0 öncesiyle aynı sayılar).

**G1 — CLI ajan çıktısı 64 KB'de kesiliyordu (bulgu O5):**
- `ProcessLimits.output_limit` eklendi (varsayılan `OUTPUT_LIMIT` = 64 KB). `_CappedReader` ve
  `_supervise` sınırı bu alandan alır; derleyici (Tier 0/1) yolu varsayılanda kalır.
- `CliConfig.output_limit_bytes` (65536-16777216, varsayılan 1 MB) config'ten gelir; `agent_limits`
  bunu `ProcessLimits`'e geçirir, `claude_cli`/`agy`/`codex` aynı yolu kullanır (mimari §12: sınır
  koda gömülmez).
- Kesilme sonucu düşürmez: `ProviderResult.warnings`'e "Model yanıtı çok uzundu, kesildi." eklenir
  (`_cli_common.clip_warning`) ve rapora `meta.warnings` olarak gider. Yanıt hiç ayrıştırılamadıysa
  eski hata ("çıktı boyutu sınırı aşıldı") korunur.
- Örnek yapılandırmalar (`codementor.toml`, `docs/mimari.md`) üç CLI sağlayıcısı için alanı gösterir.
- **Doğrulama:** ruff ve `ruff format --check` temiz; `mypy src/` 207 dosyada hatasız;
  `pytest -m "not live"` 3454 geçti, 15 atlandı, 6 deselected. Sahte CLI'ye `BOYUT:<n>` gürültü modu
  eklendi: 200 KB çıktı varsayılan sınırla tam okunuyor; `output_limit_bytes=65536` ile yanıt
  korunuyor + uyarı geliyor (Tier 1 sınırı değişmedi, `tests/unit/test_runner.py` geçiyor).
- **Açık:** G2-G7 yapılmadı; O5'in "canlı doğrulanmadı" notu hâlâ
  geçerli (gerçek `agy`/`codex` çıktısıyla elle deneme kullanıcıya bırakıldı).

**G3 — düşük öncelikli D serisi bulguları (`docs/BulgularVeDuzeltilecekler.md` §5):**
- **İlk parti (commit `5f51dec`):** D2 (`extract_json` tırnak durumu yalnız `{` içinde izlenir),
  D3 (`codex_cli._events` `RecursionError`), D4 (`429`/`401` kelime sınırlı regex),
  D5 (`apply_verdicts` yeni `finding_id`'yi `FindingCheck`'e yazar), D12 (`_json_document` doğrusal
  tarama).
- **D6 — geçiş başına sağlayıcı/maliyet:** `LLMSession.stage_providers/stage_models` yerine
  `stage_usage: dict[tuple[str, str, str], TokenSplit]` — anahtar `(aşama, sağlayıcı, model)`.
  Aynı aşama fallback ile iki sağlayıcıya bölünürse tokenler ayrı gruplanır;
  `cost_of_stages(pricing, usage)` her grubu kendi modelinin fiyatıyla çarpar. Fiyatı olmayan ya da
  sıfır tokenlı grup varsa `meta.cost_est` `None` (uydurma maliyet yazılmaz). `meta.provider/model`
  sözleşmesi değişmedi (son çağrının değerleri; raporda belgeli).
- **D1 — onarım prompt'unda doğru neden:** `guard_delimiters` artık `validation_errors` etiketini de
  nötrler (Pydantic `extra_forbidden` mesajı modelin uydurduğu anahtar adını taşıyor ve veri bloğunu
  kapatabiliyordu). `build_repair_messages(..., cause=...)` + `REPAIR_REASONS` ile giriş cümlesi
  nedene göre; `_repair_cause` şema dışı bir neden varsa onu seçer (karmaşıklık onarımında
  "şemaya uymadı" denmiyor).
- **D7 — sızıntı sonrası yeniden üretim notu:** `build_socratic_messages(..., abstract=True)`
  prompt'un sonuna içerik sızdırmayan "daha soyut sor" notunu ekler; `run_pass_b(..., rebuild=...)`
  ikinci turda `rebuild(True)` ile prompt'u yeniden kurar. Not, sabit sıcaklıklı sağlayıcılarda
  (claude_cli) aynı sızıntının tekrarlanmasını azaltmayı amaçlar; `prompt_b` süresi her kurulumda
  ölçülür (yeniden üretimde ikinci pencere, `stage_latency_ms` son değeri taşır).
- **D8 — bozuk prompt şablonu raporu düşürmez:** `prompts/templates.py`'ye `PromptTemplateError(ValueError)`
  eklendi; eksik/okunamayan şablon dizini ve Jinja `TemplateError` (şablon dosya adıyla) artık bu tipe
  dönüşüyor, ham `FileNotFoundError` yükselmiyor. `builder._fewshots` `FewShotError`'ı da aynı tipe
  çevirir (bozuk YAML tüm raporu bozar → tek tek örnek atlanmaz). `orchestrator.prompt_version(...)`
  hatayı yakalayıp `prompt_templates_unreadable` günlüğüyle sürümü `UNAVAILABLE_VERSION`
  (`v1+00000000`) yapar ve `run.cacheable = False` işaretler: rapor LLM geçişi yapılmadan statik
  analizle `degraded` döner, kurulum düzeltildiğinde yeniden üretilir (önbellekten gelmez).
  Tier 0 ve doğrulama geçişleri de aynı tipi yakalar. Uyarı metni "Few-shot" içerir.
- **D9 — ölü/tekrar kod temizliği:** `providers/anthropic.py`'deki ikinci `DEFAULT_MAX_TOKENS`
  kaldırıldı; tek kaynak `config.ANTHROPIC_DEFAULT_MAX_TOKENS` (hem `AnthropicConfig.max_tokens`
  varsayılanı hem adaptörün `opts.max_tokens or ...` yedeği). `prompts/budget._single_budget`'teki
  `PROVIDER_NAMES`/`isinstance` denetimi ve üretimdeki `TEST_PROVIDERS = {"fake"}` test kancası
  silindi: ad için yapılandırma bölümü varsa bağlam/çıktı payı oradan, yoksa ad yapılandırılmış
  zincirde geçiyorsa prompt varsayılanları (testlerin `FakeProvider`'ı zincirde tanımlanır, üretim
  kodu onu bilmez); ne bölümü ne zinciri olan ad yine `PromptConfigError`. `passes.call_structured`
  ve `run_pass_socratic_schema` artık kullanılmayan tek kullanımlık `BuiltPrompt`'u döndürmüyor
  (yalnız ayrıştırılmış sonuç); `verify_pass.run_pass_verify` ve `run_pass_b` çağrıları güncellendi.
- **D10 — HTML/CSS LLM şeması dışa aktarılıyor:** `LLMMarkupAnalysisOutput` (ADR-0015)
  `SCHEMA_MODELS`'e eklendi ve `schemas/llm_markup_analysis.schema.json` üretildi
  (`uv run codementor schema export --out schemas/`); `test_schema_export.py` beklenen dosya
  listesine ve "sistem alanı sızdırmaz" denetimine eklendi. UI tip listesi (`gen-types.mjs`)
  yalnız `UI_SCHEMAS`'ı üretir; web tipleri değişmedi.
- **D11 — olay döngüsündeki küçük G/Ç önbelleğe alındı:** `prompts/templates.prompt_version`
  dosya kümesini artık `_names` (stat'sız `os.walk`/`scandir`) anahtarıyla önbelleğe alıp `rglob`
  taramasını küme değişmedikçe yinelemiyor — dizin mtime'ı Windows'ta ~1 ms çözünürlükte olduğu
  için anahtar olarak güvenilmez (ölçüldü), bu yüzden dosya adı kümesinin kendisi kullanıldı;
  içerik değişimi yine boyut+mtime imzasından gelir. `Orchestrator._rules_version` ve
  `_question_bank` örnek başına bir kez çalışır: aynı analizde önbellek anahtarı ile rapor
  `meta`'sı aynı sürümü paylaşır (önceden maliyet tablosu + mentor şablonları iki kez okunuyordu)
  ve enjekte edilmeyen banka aynı orkestratörde diskten tekrar yüklenmez. Örnek istek/örnekleme
  başına kurulduğu için (API, masaüstü, CLI, eval) tazelik korunur. Yeni testler:
  `test_prompt_version.py::test_prompt_version_scans_once_per_file_set`,
  `test_pipeline_sessions.py::{test_question_bank_loaded_once_per_orchestrator,
  test_rules_version_reads_data_files_once_per_analysis}` (son ikisi düzeltme öncesi `[1, 1]`
  görüyordu; defekt kanıtlandı).

- **Prompt sürümü (D6-D8):** `repair.user.j2` ve `socratic.user.j2` değiştiği için hash
  `v1+3fa9c2d1` → **`v1+632620d8`**; `tests/golden/report_example.json` ve
  `src/codementor/api/examples/report.json` güncellendi. **Doğrulama (D6-D8):** `pytest -m "not live"`
  **3479 geçti**, 15 atlandı, 6 deselected (G1 sonrası 3454 → +25 test: D6 maliyet, D1 neden
  metni/guard, D7 soyut not, D8 şablon bozulması).
- **Prompt sürümü:** D9-D11'de şablon/few-shot dosyalarına dokunulmadı → hash `v1+632620d8`
  sabit; golden dosyalar güncellenmedi.
- **Doğrulama (D9-D11):** `ruff check`/`ruff format --check` temiz (467 dosya); `mypy src/` 211
  dosyada hatasız; `pytest -m "not live"` **3482 geçti**, 15 atlandı, 6 deselected (D8 sonrası
  3479 → +3 test). Bir koşuda `tests/rules/test_engine.py::test_linear_time_large_input[html-*]`
  zaman sınırını aştı (38 s > 2 s); tek başına ve sonraki tam koşuda geçti → makine yükü kaynaklı,
  değişiklikle ilgisiz.
- **Açık (D9-D11 sonrası):** D14-D20 ve `schema_enforced` duruyor; G2 sırada.

**G2 — O6: kalıcı CLI hataları yeniden denenmiyor:**
- `providers/cli_agent.py`'ye oturum/kimlik sınıflandırması eklendi: `_AUTH_HINTS` (İngilizce
  `not logged in` / `please run /login` / `unauthorized` / `authentication` / `invalid api key` +
  Türkçe `oturum açıl` / `giriş yap`) ve `auth_error(provider, detail, command)` →
  `ProviderConfigError` (`retryable = False`, `codex_cli._classify` ile aynı sözleşme).
- Claude sonuç nesnesindeki hata (`_claude_error`) artık kimlik ipucunu 429/5xx dallarından sonra,
  4xx'ten önce kontrol eder: oturumu kapanmış CLI `ProviderUnavailableError` (yeniden denenir) değil,
  "oturum açılmamış; terminalde `claude login` çalıştırın" mesajlı kalıcı hata verir. `data is None`
  (JSON çıktı yok) yolunda stderr/`çıkış kodu` ayrıntısı da aynı sınıflandırmadan geçer; agy için
  komut metni `agy`. 5xx ve 429 davranışı değişmedi (geçici → yeniden denenir).
- `_cli_common.CliPermanentError(ProviderUnavailableError)` (`retryable = False`) eklendi
  (`CliTimeoutError` deseni): agy'nin boş yanıtı ("oturum açık mı?"; MCP takılması dahil) ve
  deterministik Claude `subtype`'ları (`error_max_structured_output_retries`, `error_max_budget_usd`,
  `error_max_turns`) artık kalıcı. Böylece `agy` her biri ~20 sn süren 3 süreç açmıyor; sıradan
  `subtype` hataları ve ağ benzeri hatalar eskisi gibi yeniden denenmeye devam ediyor
  (ortak sözleşme testi `test_network_error_retried_then_unavailable` korunuyor).
- Yeni testler (`tests/providers/test_cli_agent.py`): `test_logged_out_result_is_not_retried`
  (`max_retries=2` ile bile sağlayıcı bir kez çağrılır), `test_logged_out_stderr_is_not_retried`,
  `test_server_error_is_still_retried` (kontrol: 5xx iki kez denenir),
  `test_agy_empty_response_is_not_retried`, `test_claude_permanent_subtype_is_not_retried`,
  `test_claude_unknown_subtype_is_retried` (kontrol: sıradan `subtype` yine denenir).
- **Doğrulama (G2):** `ruff check`/`ruff format --check` temiz (467 dosya); `mypy src/` 211 dosyada
  hatasız; `pytest -m "not live"` **3488 geçti**, 15 atlandı (D9-D11 sonrası 3482 → +6 test).
- **Açık:** D14-D20 ve `schema_enforced` duruyor (D8-D11 ✅, G2 ✅); G4-G7 sırada.

## Faz F — Notlar (masaüstü sağlamlık ve kullanılabilirlik; 2026-10-14)

### Yapılanlar
- **F0 (app.py controller'lara bölündü):** `history_controller.py` (141 satır) ve `config_controller.py` (89 satır) modülleri oluşturuldu; `app.py` 397 satıra düşürüldü (< 400).
- **F1 (O10 Bozuk veritabanı kurtarma):** `runtime.backup_corrupted_db` (`codementor.db.bozuk-YYYYAAGG-SSDDss`), `launch.py` onaylı yedekleme kurtarma mekanizması ve `App.report_callback_exception` eklendi; `tests/desktop/test_launch_db.py` yazıldı. Windows dosya kilidi ve `gc.collect()` çözüldü.
- **F2 (O13 Dışa aktarma hatası bildirimi):** `history_controller.export` içinde `OSError` yakalanıp Türkçe toast ile bildirildi; test eklendi.
- **F3 (O14 Geçmişi temizle gizlilik ve disk temizliği):** `storage/cache.py::clear_analyses` içine `VACUUM` ve `PRAGMA wal_checkpoint(TRUNCATE)` eklendi; `clear_history`'ye `app.save_prefs(recent_files=[])` bağlanarak son dosyalar listesi temizlendi; `tests/unit/test_storage.py`'de `clear_analyses` sonrası diskte öğrenci kodu kalmadığı bayt düzeyinde doğrulandı; `tests/desktop/test_app.py`'de `recent_files` boşalması doğrulandı.
- **F4 (D19 Veritabanı sağlamlığı ve meşguliyet kontrolleri):** SQLite bağlantı dinleyicisine `PRAGMA journal_mode=WAL`, `busy_timeout=5000`, `secure_delete=ON`, `user_version=1` (`_migrate`) eklendi; analiz sürerken (`app.analyze_view.busy`) `HistoryView` satırlarındaki "Sil" butonu `disabled` yapıldı ve `delete_history` çağrısı toast ile engellendi; `StorageSettings.session_retention_days = 90` varsayılanı `codementor.toml` ve `docs/mimari.md` §11, §17'ye işlendi; 90 günden eski oturumların açılışta budanması test edildi.
- **F5 (D18 Dosya kaydetme, CRLF koruması ve kirli durum takibi):** `FileController`'a `save()`, `save_as()`, `confirm_discard()` metodları eklendi; dosya açma, sürükleme, geçmiş yükleme, soru seçme ve pencere kapatmada kaydedilmemiş değişiklik onayı sağlandı; Ctrl+S kısayolu bağlandı; orijinal satır sonu (`\r\n` / `\n`) kaydedilirken korundu; kaydetme hatası toast ile bildirildi; `CodeEditor.set()` içindeki `edit_modified(False)` sıfırlamasıyla programatik yüklemelerin yanlış dirty algısı önlendi.
- **F6 (Geçmişte sayfalama ve arama):** `storage/cache.py::list_analyses_page`'e `search` parametresi eklendi; soru kimliği, dil ve sağlayıcı alanlarında büyük/küçük harf duyarsız `ilike` filtreleme yapıldı; SQL `LIKE` joker karakterleri (`%`, `_` ve `/`) kaçışlandı; `HistoryView` üstüne arama kutusu ve altta dinamik "Daha fazla yükle" butonu eklendi; 60 kayıt ile 50+10 sayfalama, "c-medium" tekil araması ve joker kaçışları birim ve masaüstü duman testleriyle doğrulandı.
- **F7 (Kapanırken "sürüyor" onayı):** Kapanış mantığı `runtime.confirm_close(app)` yardımcısına taşındı; `App.close` kirli dosya onayından sonra `app.analyze_view.busy` ya da süren zig indirmesi (`connections.download_cancellation is not None`) varsa `confirm("Çıkış", "Analiz (ya da indirme) sürüyor. Çıkılsın mı?")` ile onay ister; Hayır → pencere kapanmaz. `app.py` 398 satırda tutuldu (< 400). Testler: `tests/desktop/test_app.py::test_close_while_busy_confirm`, `::test_close_while_downloading_confirm` (ikisi de `confirm` casusluğuyla, ağsız).
- **F8 (ADR-0021 eski OpenAI/DeepSeek anahtarları):** `connections.LEGACY_KEY_PROVIDERS = ("openai", "deepseek")` ve `KeyStore.purge_legacy() -> int` (mevcut `get`/`delete` yeniden kullanılır; kasa kilitliyse Türkçe `KeyStoreError`); `ConnectionsController.purge_legacy_keys()` sonucu toast'lar ("N eski anahtar kimlik kasasından silindi" / "Silinecek eski anahtar bulunamadı"); bağlantılar ekranına "Eski anahtarları temizle" düğmesi (`connections_view.purge_legacy_button`) eklendi ve `app.py`'de `purge_legacy=self.connections.purge_legacy_keys` ile bağlandı. Testler: `test_purge_legacy_removes_only_removed_providers` (2 eski + 1 güncel kayıt → 2 silinir, güncel kalır; ikinci çağrı 0), `test_purge_legacy_locked_vault_is_turkish_error`, `test_purge_legacy_keys_button` (pencere duman testi).
- **F9 (Kurulu zig eskiyse "güncelle" önerisi):** `validation/toolchain_install.py`'ye `installed_marker(root)` (işaretçiyi okur; yoksa/bozuksa `None`) ve `needs_update(settings, *, platform=None) -> bool` eklendi: kurulum yoksa, işaretçi okunamıyorsa ya da platform için kaynak tanımlı değilse `False`; aksi hâlde işaretçideki `version` **ya da** `sha256` yapılandırmadan farklıysa `True`. Masaüstünde GUI'siz sarmalayıcı `services.compiler_update_available(settings)`; bağlantılar denetleyicisi bunu `show_compilers(...)`'a geçirir. Kartta "Güncelleme var: kurulu zig, yapılandırmadaki sürümden farklı." metni ve **"Derleyiciyi güncelle"** düğmesi görünür; indirme akışı (ilerleme, iptal, sha256 doğrulaması, atomik kurulum) aynen yeniden kullanılır, `offer_compiler_download` davranışı değişmedi. Testler: `tests/unit/test_toolchain_install.py::test_needs_update_only_when_marker_differs`, `::test_needs_update_false_on_missing_or_broken_marker`, `::test_needs_update_false_without_configured_source` (sahte dizin + işaretçi, ağ yok); `tests/desktop/test_app.py::test_compiler_update_button_when_installed_zig_is_old`, `::test_compiler_update_button_downloads_through_same_flow`.
- **F10 (Bağlantılar'da `ollama pull` düğmesi):** GUI'siz yardımcılar `desktop/services.py`'ye eklendi: `ollama_pull_argv(model, search_path)` → `[mutlak yol, "pull", model]` (mutlak yol `validation.runner.find_on_path("ollama", PATH)` ile bulunur; çalışma dizinine bakılmaz) ve `run_ollama_pull(model, argv, runner=None) -> PullOutcome`. Model adı `^[A-Za-z0-9._:/-]+$` dışındaysa ya da `ollama` PATH'te yoksa `OllamaPullError` (Türkçe mesaj) yükselir ve **hiçbir süreç başlatılmaz**; doğrulama düğme basılırken senkron yapılır, geçerliyse iş `bridge.submit("pull:ollama", ...)` ile arka plana verilir (arayüz kilitlenmez, kart "… indiriliyor…" gösterir). Sonuç (`PullOutcome.ok/message`) kart ayrıntısına ve toast'a düşer. Ollama kartına (kind `local`) **"Modeli indir"** düğmesi eklendi (`CardActions.pull_model`); `App._on_message` `pull:` görevini `CONNECTIONS_TASKS` üzerinden bağlantılar denetleyicisine yönlendirir. Hata beklenen sonuçtur (istisna köprüde anlamsız genel metne dönüşürdü): `ok=False` + Türkçe neden. Testler: `tests/desktop/test_connections.py::test_ollama_pull_argv_is_absolute_and_shell_free`, `::test_ollama_pull_runner_gets_validated_argv`, `::test_ollama_pull_rejects_unsafe_model_names` (9 kötü niyetli ad), `::test_ollama_pull_missing_binary_is_turkish_error`, `::test_ollama_pull_failure_outcome_is_turkish`; `tests/desktop/test_app.py::test_ollama_pull_button_runs_through_background_task`, `::test_ollama_pull_without_binary_warns_and_starts_nothing`. **Gerçek `ollama` çalıştırılmadı, ağa çıkılmadı** (kural 7/8): süreç yalnız enjekte edilen sahte `runner` ile başlar.

- **F11 (SQLite çağrılarını iş parçacığına alma):** Geçmiş ekranının tüm DB işleri `desktop/bridge.py` desenine taşındı: `history_controller` artık üç arka plan görevi kullanır — `history` (liste), `history_delete` (tekil silme), `history_clear` (tümünü temizle); `history_view.refresh()`/`_handle_load_more()` yalnız **istek** yapar (`request_page` geri çağrısı, `App._request_history_page` → `history_controller.refresh`), sonuçlar ana iş parçacığında `history_controller.handle` ile uygulanır (`apply_page`/`apply_error`). Liste yükleme, silme ve temizlik boyunca **"Yükleniyor…"** gösterilir (`HistoryView.show_loading`, `append=True` iken "Daha fazla yükle" düğmesi devre dışı). Toplam token/maliyet etiketi de artık ana iş parçacığında değil, işçinin içinde (`usage_totals_label(usage_totals(db))`) hesaplanır ve sayfayla birlikte gelir; `usage_totals`/`AnalysisRow`/`usage_totals_label` içe aktarımları `app.py`'den kalktı, kullanılmayan `history_rows`/`history_page` sarmalayıcıları silindi. Hata Türkçedir: `history` görevi hatasında liste `apply_error` ile metni gösterir, silme/temizlik hatasında liste tazelenip toast çıkar (liste "Yükleniyor…"da kalmaz). Testler: `tests/desktop/test_app.py::test_history_list_loads_off_main_thread` (DB çağrısı `threading.main_thread()` DEĞİL; bekleme kapısı açıkken "Yükleniyor…" görünür), `::test_history_page_renders_rows_and_totals`, `::test_history_page_error_is_shown_in_turkish`, `::test_history_stale_page_result_is_dropped` (eski kuşağın geç gelen sonucu atılır), `::test_history_delete_runs_off_main_thread`, `::test_history_clear_runs_off_main_thread`; mevcut 12 geçmiş testi `pump_history`/`pump` ile sonucu bekleyecek şekilde güncellendi (davranış aynı, zamanlama asenkron).

- **F12 (Linux/macOS'ta "Oturum aç"):** Oturum açma akışı GUI'siz yeni `desktop/login.py` modülüne çıkarıldı (Tk içe aktarmaz, `spawn` enjekte edilebilir): `login_argv(name, providers)` sağlayıcının komutunu üretir (`claude_cli` → `… auth login`, `codex` → `… login`, `agy` → çıplak yürütülebilir; yollar `resolve_executable` ile PATH'in mutlak dizinlerinden) ve saf `login_command(platform, cli_path, *, login_args, find)` platforma göre pencere argv'sini döndürür: Windows mevcut davranış (yeni konsol, `CREATE_NEW_CONSOLE`), Linux `x-terminal-emulator -e <cli> …` yoksa `gnome-terminal -- <cli> …`, macOS `open -a Terminal <cli>`; hiçbiri bulunamazsa `None`. `open_login_console` süreci yalnız enjekte edilen `spawn` (varsayılan `subprocess.Popen`) ile başlatır; terminal yoksa **hiç süreç başlatılmaz** ve `LoginUnavailableError` yükseltilir, `ConnectionsController.login` bunu toast'a çevirir: "Terminalde şu komutu çalıştırın: <komut>" (`shlex.join` ile boşluklu yollar tırnaklanır; sağlayıcı ön eki kullanıcıya gösterilmez). Konsol ortamı (`login_env`, Faz 50) aynen korundu: API anahtarı değişkenleri miras alınmaz. Testler: `tests/desktop/test_login.py` (üç platform için argv, `gnome-terminal` yedeği, terminal yoksa `None` + hiç `spawn` çağrılmadığı, varsayılan başlatıcının gerçek `subprocess.Popen` olduğu, ortam süzme), `tests/desktop/test_app.py::test_login_starts_console_and_points_to_check`, `::test_login_without_terminal_shows_command_toast`; `tests/unit/test_tkinter_free_imports.py` listesine `codementor.desktop.login` eklendi; `connections.py`'den taşınan 3 test `test_login.py`'ye geçti. **Gerçek terminal/süreç açılmadı** (kural 4/7): `find` ve `spawn` sahtedir.

### Kararlar & Denetim Bulgusu

- **Windows SQLite kilidi:** Bozuk dosyada `SQLModel.metadata.create_all` hata fırlattığında motor açık bağlantı tutuyordu; `Database.__init__` `except` bloğunda `self.engine.dispose()` ve `launch.py`'de `state.close()` + `gc.collect()` ile işletim sistemi dosya kilidi bırakıldı.
- **Şema ayar bağımlılığı:** Denetim sırasında `Database.from_settings`'in henüz tanımlanmamış `session_retention_days` alanına erişimi yakalandı; `StorageSettings`'e alan ve `storage/sessions.py`'ye `prune_old_sessions` eklenerek tam uyum sağlandı.
- **Tcl/Tk Widget Yaşam Döngüsü (F6):** `HistoryView.refresh()` sırasında `clear(self.list)` altındaki tüm widget'ları yok ettiği için `load_more_btn`'nin `_render_rows` içerisinde dinamik olarak yeniden üretilmesi sağlandı; böylece "bad window path name" Tcl hatası önlendi.
- **Kapanış onayı tek noktada (F7):** `App.close` içindeki onay mantığı `runtime.confirm_close(app)` içine çıkarıldı; "kaydedilmemiş değişiklik" (F5) ve "süren iş" (F7) onayları tek akışta sıralandı (önce kirli dosya, sonra meşguliyet) ve `app.py` kabul kriterinin (400 satır) altında tutuldu.
- **Meşguliyet ölçütü (F7):** Süren iş, `app.analyze_view.busy` **veya** `app.connections.download_cancellation is not None` ile yoklanıyor; indirme başlarken `Cancellation` atanıp biterken/iptalde `None`'a çekildiği için "analiz sürüyor" ve "zig indiriliyor" aynı onayla kapsandı. Onay reddedilirse kapatma iptal edilir (pencere açık kalır).
- **Eski anahtar kalıntısı (F8):** ADR-0021 ile sağlayıcı listesinden çıkarılan `openai`/`deepseek` kayıtları kimlik kasasında kalıyordu; temizlik `LEGACY_KEY_PROVIDERS` sabitine dayandığından yalnızca kaldırılan sağlayıcıları siler, güncel kayıtlara dokunmaz ve silinecek kayıt yokken idempotenttir (0 döner). Kasa kilitliyse `KeyStoreError` Türkçe toast'a dönüşür; gizli anahtar hiçbir yerde loglanmaz/gösterilmez.
- **Denetim bulgusu (F8):** `desktop/connections.py` F8 eklemeleriyle 402 satıra çıktı (> 400, AGENTS.md "bölmeyi öner"); `KeyStore`/`LEGACY_KEY_PROVIDERS`'ın ayrı bir `desktop/keystore.py`'ye taşınması önerisi "Sonraya"ya yazıldı (Faz G0'daki bölme disipliniyle aynı yaklaşım). Faz F kabul kriteri yalnız `app.py` < 400 olduğundan bu, kabul engeli değil.
- **Güncelleme ölçütü (F9):** "eski sürüm" yalnız sürüm dizesine bakmaz, işaretçideki **sha256**'yı da karşılaştırır: aynı sürümde adres/sha256 değişse bile güncelleme önerilir (§12: adres ve sha256 yalnız yapılandırmadan gelir, kurcalanmış arşiv yeniden indirilir). Kurulum hiç yoksa `needs_update` `False` döner — eksik kurulumu `offer_compiler_download` yönetir; iki düğme de aynı `install_zig` yolunu kullanır (yeni indirme yolu yok, ADR-0018 korunur).
- **Yarım kurulum ayrımı (F9):** işaretçisiz dizin (kopyalanmış/eski kurulum) kurulu sayılmaz ve güncelleme istemez; bu, `installed_zig` ile aynı ölçütü paylaşır (işaretçi + çalıştırılabilir dosya).
- **`ollama` komutu yalnız argv listesi (F10):** Kabuk hiç kullanılmaz; model adı tek bir argv öğesi olarak geçer ve `^[A-Za-z0-9._:/-]+$` ile **komut başında** doğrulanır (spec'teki karakter sınıfı birebir uygulandı; `.` ve `/` sınıfın parçası olduğu için `../x` gibi adlar reddedilmez, ancak tek argv öğesi olduğundan yol/kabuk anlamı taşımaz). Yol `find_on_path` ile yalnız PATH'in mutlak dizinlerinde aranır — `run_process` zaten mutlak olmayan `argv[0]`'ı reddeder (Faz A2, Y1).
- **Hata beklenen sonuç (F10):** `run_ollama_pull` istisna fırlatmaz; başarısızlık `PullOutcome(ok=False, message=<Türkçe neden>)` olur. Nedeni: köprü, tanımadığı istisnalar için "Beklenmeyen bir hata oluştu" gibi genel metin üretir ve kullanıcı `ollama`nın gerçek çıktısını görmezdi. Başarısız `returncode`'da `stderr`'in son satırı mesaja girer.
- **Doğrulama zamanlaması (F10):** Model adı ve `ollama` varlığı denetimi düğme basılırken senkron yapılır (kullanıcı anında Türkçe uyarı görür, boşuna arka plan görevi açılmaz); süreç başlatma ve bekleme arka planda köprüde koşar (arayüz kilitlenmez). İndirme süresi `ProcessLimits.timeout_s = 3600` (büyük modeller dakikalarca inebilir); çıktı ilerlemesi akış olarak gösterilmez (köprü `run_process` sonucunu tek seferde döner), kart yalnız "indiriliyor…" der.

- **Sonuç teslimi ana iş parçacığında (F11):** İşçi iş parçacığı Tk'ye dokunmaz; yalnız sonucu köprünün `queue.Queue`'suna yazar, `App._poll` (ana iş parçacığında `after` ile zamanlanır) `drain()` edip `history_controller.handle`'e verir. İş parçacığından doğrudan `app.after(0, ...)` çağrılmadı: köprü deseni (Faz 19'dan beri kullanılıyor) aynı işi kuşak denetimi ve iptalle birlikte yapıyor, doğrudan `after` çağrısı Tk'de iş parçacığı güvenli değil.
- **Kuşak denetimi (F11):** Aynı görev adı yeniden gönderilirse köprü kuşağı artırır ve eski iş parçacığının geç gelen sonucu `drain()` sırasında atılır; hızlı iki yükleme (ör. art arda arama) eski listeyi geri getirmez (`test_history_stale_page_result_is_dropped`).
- **Silme/temizlikte de "Yükleniyor…" (F11):** Silme ve temizlik akışları sonunda listeyi tazelediği için yükleme göstergesi görev başında açılır (`show_loading`); kullanıcı işlem sürerken eski satırları görmez. Kayıt yoksa ya da iş hata verirse liste `refresh()` ile toparlanır, "Yükleniyor…" ekranda kalmaz.
- **Kapsam sınırı (F11):** `open_history` (kaydı açma) hâlâ ana iş parçacığında `get_analysis`/`get_row` + `runtime.load_source` yapar; F11 kapsamı spec'te sayılan liste/silme/temizleme ile sınırlı tutuldu, kayıt açma "Sonraya"ya yazıldı.
- **Platform seçimi saf fonksiyonda (F12):** `login_command` platforma göre yalnızca argv üretir (süreç başlatmaz; terminal araması `find` ile enjekte edilir). Böylece Linux/macOS dalları Windows'ta da deterministik test edilir ve testler makinede kurulu terminale bağlı kalmaz. Windows davranışı korundu: eski kod yalnız Windows'ta çalışıyordu, artık aynı yol `CREATE_NEW_CONSOLE` ile devam ediyor; "konsoldan oturum açma yalnızca Windows'ta destekleniyor" hatası tamamen kalktı.
- **macOS'ta argüman geçirme sınırı (F12):** `open -a Terminal <cli>` ek argümanları belge yolu saydığı için macOS dalında yalnız çalıştırılabilir yol geçilir (`auth login` ekleri düşer); `claude`, `codex` ve `agy` argümansız da kendi oturum açma akışını başlattığından kabul edildi, `osascript` ile argümanlı sürüm "Sonraya"ya yazıldı.
- **Terminal yoksa sessiz kalmama (F12):** Konsol açılamadığında hiçbir süreç başlatılmaz ve istisna toast'a dönüşür; kullanıcı tam komutu görür (`login_env` sayesinde anahtarlar gizli kalır). Kart ayrıntısı yerine toast seçildi: metin kart satırından uzun ve kopyalanabilir olmalı.

### Doğrulama
- `uv run ruff check .` → All checks passed!
- `uv run ruff format --check .` → 460 files already formatted
- `uv run mypy src/` → Success: no issues found in 206 source files
- `uv run pytest tests/desktop/test_launch_db.py` → 4 passed in 0.35s
- `uv run pytest tests/unit/test_tkinter_free_imports.py` → 9 passed in 5.11s
- `uv run pytest tests/unit/test_storage.py` → 42 passed in 0.77s
- `uv run pytest tests/desktop/test_app.py` → 59 passed in 56.12s
- Dosya satır sayıları: `app.py` 399, `files.py` 129, `history_controller.py` 155, `config_controller.py` 89, `history_view.py` 273, `cache.py` 272 (< 400).
- F7+F8 sonrası (HEAD `2598026`) tam takım: `uv run pytest -m "not live" -q` → 3409 passed, 15 skipped, 6 deselected in 194s; `uv run ruff check .` ve `uv run ruff format --check .` temiz; `uv run mypy src/` → 206 kaynak dosyada hata yok.
- F7+F8 sonrası dosya satır sayıları: `app.py` 398 (< 400), `runtime.py` 252, `connections_controller.py` 287, `connections_view.py` 280; `connections.py` 402 (bölme önerisi yukarıda).
- F9 sonrası tam takım: `uv run pytest -m "not live" -q` → **3414 passed, 15 skipped, 6 deselected** in 201s; `uv run ruff check .` → "All checks passed!"; `uv run ruff format --check .` → "460 files already formatted"; `uv run mypy src/` → "Success: no issues found in 206 source files".
- F9 mutasyon kontrolü: F9 kaynağı `git stash` ile geri alınınca yeni 5 test düştü — 3 birim testi `ImportError: cannot import name 'needs_update'`, 2 pencere testi FAILED (`AttributeError` ve kutu görünürlüğü); `git stash pop` sonrası `git stash list` boş.
- F9 sonrası dosya satır sayıları: `toolchain_install.py` 380, `services.py` 71, `connections_controller.py` 292, `connections_view.py` 297, `app.py` 398 (< 400).
- F10 sonrası tam takım: `uv run pytest -m "not live" -q` → **3429 passed, 15 skipped, 6 deselected** in 208s (+15 test: 13 `test_connections.py`, 2 `test_app.py`); `uv run ruff check .` → "All checks passed!"; `uv run ruff format --check .` → "460 files already formatted"; `uv run mypy src/` → "Success: no issues found in 206 source files".
- F10 mutasyon kontrolü: (a) dört kaynak dosya (`services.py`, `provider_card.py`, `connections_controller.py`, `app.py`) `git stash` ile geri alınınca derleme aşaması düştü (`ImportError: cannot import name 'PullOutcome'`); (b) yalnız GUI bağlantıları (`provider_card.py`, `connections_controller.py`, `app.py`) geri alınınca 2 pencere testi FAILED (`AttributeError: 'ProviderCard' object has no attribute 'pull_button'`) — `git stash pop` sonrası `git stash list` boş, çalışma ağacında yalnız bu maddenin 9 dosyası değişik.
- F10 sonrası dosya satır sayıları: `services.py` 143, `provider_card.py` 253, `connections_controller.py` 327, `connections_view.py` 297, `app.py` 399 (< 400; `CONNECTIONS_TASKS` sabiti tek satırda tutuldu). `connections.py` 402 (F8'den kalan, bölme önerisi "Sonraya").
- F11 sonrası tam takım: `uv run pytest -m "not live" -q` → **3435 passed, 15 skipped, 6 deselected** in 209s (+6 test: hepsi `tests/desktop/test_app.py`); `uv run ruff check .` → "All checks passed!"; `uv run ruff format --check .` → "460 files already formatted"; `uv run mypy src/` → "Success: no issues found in 206 source files".
- F11 mutasyon kontrolü: `app.py`, `history_controller.py` ve `views/history_view.py` `git stash` ile geri alınınca yeni 6 pencere testi FAILED (`AttributeError: HistoryView object has no attribute loading`); `git stash pop` sonrası `git stash list` boş, çalışma ağacında yalnız bu maddenin 5 dosyası değişik.
- F11 sonrası dosya satır sayıları: `app.py` 395 (< 400), `history_controller.py` 241, `views/history_view.py` 347, `tests/desktop/test_app.py` 1680. `connections.py` 402 (F8'den kalan, bölme önerisi "Sonraya").
- F12 sonrası tam takım: `uv run pytest -m "not live" -q` → **3447 passed, 15 skipped, 6 deselected** in 212s (+12 test: `tests/desktop/test_login.py` 12 yeni; `tests/desktop/test_app.py` 2 yeni; `tests/desktop/test_connections.py` −3 (oturum testleri `test_login.py`'ye taşındı); `tests/unit/test_tkinter_free_imports.py` +1); `uv run ruff check .` → "All checks passed!"; `uv run ruff format --check .` → "462 files already formatted"; `uv run mypy src/` → "Success: no issues found in 207 source files".
- F12 mutasyon kontrolü: kaynak değişiklikleri (`desktop/login.py`, `desktop/connections.py`, `desktop/connections_controller.py`) `git stash` ile geri alınınca — testler yerinde bırakılarak — `tests/desktop/test_login.py` derleme aşamasında düştü (`ModuleNotFoundError: No module named 'codementor.desktop.login'`), `tests/desktop/test_app.py` import hatasıyla ERROR verdi ve `tests/unit/test_tkinter_free_imports.py::test_imports_without_tkinter[codementor.desktop.login]` başarısız oldu; `git stash pop` sonrası `git stash list` boş, çalışma ağacında yalnız bu maddenin 7 dosyası değişik.
- F12 sonrası dosya satır sayıları: `desktop/login.py` 144 (yeni), `desktop/connections.py` 402 → **366** (F8 denetim bulgusu kapandı), `desktop/connections_controller.py` 331, `desktop/app.py` 395 (< 400), `tests/desktop/test_login.py` 190, `tests/desktop/test_app.py` 1716, `tests/desktop/test_connections.py` 465.
- F10 denetimi (2026-10-14): kritik/önemli bulgu yok, birleştirilebilir; 3 küçük bulgu (test kapsamı, `pull` iptali, model adı deseni) `docs/BulgularVeDuzeltilecekler.md` §10 Faz F ve Sonraya bölümüne yazıldı.

### Açık kalanlar
- **Faz F kabulündeki "elle deneme" yapılmadı (kullanıcıda):** `uv run python -m codementor.desktop` ile (a) Geçmiş → Tümünü temizle, (b) dosyayı düzenleyip Ctrl+S, (c) düzenleyip başka dosya açma → onay maddeleri etkileşimli masaüstü oturumu gerektirir; bu ortamda ÇALIŞTIRILMADI (kural 7/8). Gerçek zig indirmesi/`güncelleme` akışı, `ollama pull` ve canlı sağlayıcılar (gemini/agy) da çalıştırılmadı; bozuk DB elle denemesi `CODEMENTOR_DB_PATH` ile geçici bir veritabanında yapılmalı.
- **F12 elle denemesi (kullanıcıda):** Linux/macOS "Oturum aç" davranışı bu makinede (Windows) koşturulamadı; platform dalları yalnız testlerle (enjekte edilen `find`/`spawn`, hiç gerçek terminal yok) doğrulandı. Gerçek `x-terminal-emulator`/`gnome-terminal`/`open` denemesi ve §3.1 Linux taklidi kullanıcıya bırakıldı.
- **`connections.py` 402 satır (F8 denetimi) KAPANDI:** F12'de oturum açma akışı `desktop/login.py`'ye çıkarıldı; dosya **366 satıra** indi (< 400) ve `KeyStore` taşıma önerisi "Sonraya" listesinden kapatıldı. Başka denetim bulgusu (F10'un 3 küçük maddesi) hâlâ açık.
- **`docs/BulgularVeDuzeltilecekler.md` §10:** F1–F12'ye karşılık gelen kutular `- [x] … — **Faz F**` yapıldı (son olarak F12). Açık kalan tek kutu 400 satır bölme işi: `desktop/app.py` 395 satırla sağlanıyor; `pipeline/orchestrator.py` Faz G0'da bölünecek.

## Faz E — Notlar (web geçmişi, silme ve güvenlik başlıkları; 2026-10-13)

### Yapılanlar
- **E1 & E2 (API geçmişi ve silme):** `AnalysisSummary`, `AnalysisPage`, `DeletedCount` modelleri (`models/api.py`).
  `storage/cache.py`'de `list_analyses_page(db, limit, before)` (en yeni önce, cursor tabanlı sayfalama) ve
  `storage/sessions.py`'de `delete_session(db, session_id)` (belirli oturumu silme). `GET /v1/analyses`,
  `DELETE /v1/analyses` (toplu silme), `DELETE /v1/sessions/{session_id}` uç noktaları eklendi.
  Şemalar dışa aktarıldı (`schemas/`) ve TypeScript tipleri üretildi (`web/src/types/`).
- **E3 & E4 (Web geçmişi ve API anahtarı):** `web/src/lib/apiKey.ts` (`sessionStorage` tabanlı `getApiKey`/`setApiKey`/`clearApiKey`),
  `web/src/api/client.ts` (`X-API-Key` ekleme, 401 için Türkçe hata mesajı, `listAnalyses`, `getAnalysis`, `deleteAnalysis`, `deleteAllAnalyses`).
  `web/src/components/HistoryPanel.tsx` (geçmiş listesi, silme, tümünü temizle onaylı, sayfalama).
  `web/src/App.tsx` içine geçmiş paneli ve başlıkta API anahtarı ayarı entegre edildi.
- **E5 (O15 Monaco hover güvenliği):** `web/src/lib/markdown.ts` içinde `escapeMarkdown` eklendi;
  `markers.ts` Monaco hover içerisindeki LLM bulgu açıklamaları ve derleyici iletilerini kaçışlayarak
  güvenilmeyen bağlantı ve görselleri etkisizleştirdi.
- **E6 (O16 Güvenlik başlıkları):** `web/index.html`'e sıkı CSP meta etiketi (`default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; ...`);
  `web/vite.config.ts` dev modunda HMR için `connect-src` genişletmesi; `src/codementor/api/security_headers.py`
  ile API yanıtlarına `X-Content-Type-Options: nosniff` ve `Referrer-Policy: no-referrer` başlıkları eklendi.
- **E7 (D14 İç uçların korunması):** `src/codementor/api/auth.py` içinde `_is_protected` ile `/health/ready`,
  `/docs`, `/redoc`, `/openapi.json`, `/docs/oauth2-redirect` ve `/v1/*` yolları API anahtarı açıkken korundu;
  yalnız `/health` açık bırakıldı.
- **E8 (D15 Markdown dışa aktarımında HTML kaçışı):** `src/codementor/report/markdown.py` içinde `_escape_html`
  fonksiyonu ile kod içi (`...`) ve kod blokları korunarak serbest metindeki `<`, `>`, `&` karakterleri kaçışlandı.
- **E9 (D17 İndirme URL gecikmeli iptal):** `web/src/lib/download.ts` içinde `URL.revokeObjectURL(url)` 1000 ms
  gecikmeyle (`setTimeout`) çağrılacak şekilde güncellendi.
- **E10 (Soru filtresi boş mesajı):** `web/src/components/Controls.tsx` soru listesi boş olduğunda
  "Bu filtrelerle eşleşen soru yok." mesajı gösterir.
- **E11 (Dışa açık serve ve hız sınırı):** `src/codementor/cli/serve.py` dışa açık IP'de anahtarsız ve `--insecure`
  olmaksızın başlatmayı reddeder (kod 3). `ApiSettings.rate_limit_per_minute` (varsayılan 30); `RateLimiter`
  (`api/guard.py`) ve `ApiState` üzerinde kayan pencere ile 429 Too Many Requests + `Retry-After: 60` üretilir.
- **E12 (CSRF / text/plain güven sınırı):** `tests/api/test_trust_boundary.py` içinde `POST /v1/analyze`
  `text/plain` içerik türüyle reddedildiği ve LLM çağrılmadığı doğrulandı.

### Kararlar
- **RateLimiter mimarisi:** Hız sınırlayıcı durum bilgisi `src/codementor/api/guard.py` içinde `RateLimiter` sınıfında
  toplandı ve `ApiState` üzerinden uygulama durumuna bağlandı; böylece test ortamlarında her ASGI uygulaması
  tamamen yalıtılmış hız sayacına sahip oldu.
- **API Anahtarı saklama:** Web tarafında API anahtarı `localStorage` yerine `sessionStorage`'da tutuldu; sekme
  kapanınca anahtar temizlenerek paylaşılan bilgisayarlarda güvenlik sağlandı.

### Doğrulama
- `uv run ruff check .` → All checks passed!
- `uv run ruff format --check .` → 456 files already formatted
- `uv run mypy src/` → Success: no issues found in 204 source files
- `uv run pytest -m "not live"` → 3383 passed, 15 skipped, 6 deselected in 178s
- `npm run typecheck` → 0 errors
- `npm test` → 12 passed (54 tests)
- `npm run build` → built in 404ms
- `npx playwright test e2e/app.spec.ts` → 4 passed (5.0s, CSP console hatası 0)
- Linux tkinter-free yalıtım testi → 7 passed
- Görünmez karakter taraması → 0 bulgu

## Denetim — Faz A1-D (kod-denetci, 2026-10-13)
İki kod-denetci ajanı (A1+A2+B ve K+C) "birleştirilemez" dedi; bulgular doğrulanmıştı. Dal
`fix/denetim-a-d` (`faz/d-public-release`dan).
**Düzeltilenler:**
- Include: satır birleştirmeyle kurulan `##`/`%:%:` (ham kodda görünmüyordu) reddediliyor;
  `_Pragma("GCC dependency …")` ile host dosyası yoklama kapandı.
- `guard_delimiters`: iyelik nicelikleri ve öznitelikli/özniteliksiz dal ayrımıyla doğrusal (39 bin
  boşlukta 3,5 sn → 0,02 sn); `&` içeren öznitelik değeri (A2 gerilemesi) ve `&#60;`, `&#x3c;`,
  noktalı virgülsüz `&lt` nötrleniyor.
- Önbellek imzası `asyncio.to_thread`'de (derleyici keşfi olay döngüsünü kilitliyordu); imza kontrol
  listesi damgalarını, sağlayıcı ayarlarını ve referans çözüm damgasını da kapsıyor.
- Önbelleğe girmeyenler: sızıntı yüzünden tüm soruları atılan rapor, Tier 0 durdurma raporu, Tier 1
  zaman aşımı/araç hatası. Onarım prompt'u bütçe hatası verse ya da onarım sürerken süre dolsa da
  geçerli bulgular korunuyor.
- Kullanıcı sorusu: başlık, metin, kısıt, işlem adı ve ipucu prompt'ta `guard`'dan geçiyor; kullanıcı
  görevi "talimat değil" diye işaretleniyor (`QuestionContext.origin`); taslakta uzunluk sınırları.
  Kullanıcı deposu yalnız `.yaml` okuyor, yinelenen kimlik atlanıyor; yerleşik banka kullanıcı
  kaynaklı hiçbir hatayla düşmüyor; masaüstünde atlanan dosya sayısı görünüyor; düzenleme formu
  formla uyumsuz dosyada çökmüyor.
- Kavram: gizli seviyede kavram adının sorularda/ipucunda geçmesi `concept_named` ihlali (Türkçe
  büyük/küçük ve aksan duyarsız); bayraksız eski önbellek kayıtlarında kavram model düzeyinde boş.
- Yapılandırma (ADR-0029, kullanıcı kararı): çalışma dizinindeki toml güvenilmez katman (tehlikeli
  anahtarlar yok sayılır, uyarı); katmanlar env → cwd → `~/.codementor/codementor.toml` → paket;
  kurulu wheel'de CLI masaüstünün yazdığı dosyayı okuyor.
- `usage_totals` bozuk `report_json`'a dayanıklı (`json_valid`); Geçmiş'te hata log'a yazılıyor.
- Testler: `integration/test_audit_fixes.py` (10; düzeltmeler geri alınınca hepsi düşüyor),
  `unit/test_audit_fixes_unit.py` (10), include (+3), guard (+13). mimari §11, §17 güncellendi.
**Doğrulama:** ruff, format, mypy temiz; `pytest -m "not live"` 3355 geçti, 15 atlandı.
**Ertelenen (Sonraya):** `config_writer` dizi tablosunu (`[[providers.x]]`) ezer, CRLF'yi LF yazar;
`from_question` `genel` etiketini/varsayılan kısıtı düzenlemede siler; `system_errors` ağ
hatalarını "dosya işlemi" diye anar; `report/usage` → `storage.cache.UsageTotals` katman bağımlılığı;
`detect.py` `<meta …` deseni çok büyük girdide karesele yakın (40 KB'de ölçülmedi);
`guard_delimiters` `&lt;` için idempotent değil; `primary` sağlayıcı adı `getattr` ile; 400 satır:
`orchestrator.py`, `passes.py`, `desktop/app.py` (Faz G).

## Faz D — Notlar (public belgeler ve otomatik release; 2026-10-13)
Kaynak: `docs/BulgularVeDuzeltilecekler.md` P5-P9, P11, O1, O17, O18, D20.
**Yapılanlar:**
- İç belgeler (`DEVIR_*`, `CODEX_3_4_YAPILANLAR`, `YAPILANLAR*`, `FAZ36_OLCUM_DURUMU`,
  `EVAL_PARCA_REHBERI`) `docs/gelistirme-gunlugu/`'ye taşındı (+ dizin README'si, bağlantılar).
  PROGRESS 263 KB → 31 KB: Faz 0-63 notları `PROGRESS-faz-0-63.md` arşivinde.
- GUNCELLEMELER Faz 62: yapılmayan web/toplu silme açık işaretlendi (→ Faz E).
- README: sayılar (28 ADR, 3.300+ test, ~29/28 bin satır), faz anlatımı, dil bağlantısı, release
  indirme metni; `README.en.md`, `SECURITY.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, issue/PR
  şablonları.
- Sürüm tek kaynak `codementor.__version__` = **0.1.1** (hatch dinamik sürüm; `build_exe`
  oradan okur); `pyproject` authors/keywords/classifiers/urls.
- `desktop/self_check.py` + `CodeMentor.exe --self-check <json>`: pencere açmadan kaynaklar,
  soru bankası (64), `.scm` sorguları, olgu çıkarımı, Roslyn.
- CI: `permissions: contents: read`, `concurrency`, action'lar commit SHA'sına sabit. Yeni
  `release.yml` (etiket = sürüm denetimi → test → Roslyn sc → exe → iki paketle duman testi →
  `SHA256SUMS` → CHANGELOG bölümüyle `gh release create`; yazma izni yalnız yayın işinde),
  `dependabot.yml` (uv, npm, actions). actionlint temiz.
- Yerel: `dist/` eski exe/zip ve exe yanındaki eski `codementor.toml` (scratchpad'e yedeklendi)
  silindi; 0.1.1 onefile + onedir derlendi, ikisi de `--self-check` ile geçti (Faz 60'ın açık
  maddesi: güncel exe'de 64 görev).
- Testler: `test_release_readiness.py` (sürüm eşitliği, CHANGELOG, duman testi, eksik sorgu,
  isteğe bağlı denetim, `--self-check` bayrağı).
**Kararlar:** `analyze` çıkış kodu 2 = derleme başarısız (mimari §10); yanlış yazdığım
açıklamalar düzeltildi. agy canlı denemesi yapılmadı.
**Kullanıcıda:** main birleştirme + push + `v0.1.1` etiketi (release otomatik); GitHub'da secret
scanning, push protection, Dependabot alerts (P13).

## Faz A1 — Notlar (include koruması yorum atlatması, dil tespiti ReDoS; 2026-10-12)
Kaynak: `docs/BulgularVeDuzeltilecekler.md` K1, K2 (tam tarama). Kod-denetçi denetimi token
nedeniyle sonraya bırakıldı.
**Yapılanlar:**
- `validation/include_guard.py`: maskelenmiş birleşik metinde `#`/`%:` + boşluk(yorum) + yönerge
  adı aranır; arada ham metinde `/*` varsa hedeften bağımsız red (`#/**/include`, `%:/**/include`,
  satır aşan `#/*` + yeni satır + `*/include`). Yorumsuz `#` + yeni satır + `include` yönerge
  değil, dokunulmadı.
- `ingest/detect.py`: CSS özellik deseni (kübik) ve `re.M` + `^\s*` desenleri (karesel; Java dahil)
  `^[ \t]*`, satır içi `[^…\n]` ve `[^)]{0,300}` ile doğrusal. 13 desende `\b` yerine U+0008 vardı
  (Faz 16); düzeltildi, Python/HTML/CSS sinyallerinin bir kısmı ilk kez çalışıyor.
- `pipeline/orchestrator.py`: `_ingest` async; `normalize` `asyncio.to_thread` ile.
- Testler: 6 yeni red + 2 izin (include), 10 kötü niyetli girdi × tüm tespit desenleri < 0,25 sn,
  40 KB ReDoS girdisi < 1 sn, ölü sinyallerin eşleşmesi ve kaynakta U+0008 yokluğu,
  `test_offloop` ingest'i kapsıyor.
**Doğrulama:** ruff, format, mypy temiz; `pytest -m "not live"` 3148 geçti, 14 atlandı.
**Açık:** `_recursion.py`/`verify/lines.py`/`verify/proof.py` ve `rules/` regex taraması; kod-denetçi
denetimi; Y1, D13, `.gitignore` (Faz A2).



## Faz C — Notlar (ipucu merdiveni, yapılandırma, CLI çıkış kodları; 2026-10-13)
Kaynak: `docs/BulgularVeDuzeltilecekler.md` Y6, Y7, Y8, Y9, O7, O8, O9, O11, O12, D20.
**Yapılanlar:**
- **Y6:** `SocraticResult.concept_revealed` (varsayılan False). Kural kaynağında:
  `verify_socratic(name_concept=…)` (`MentoringProfile.name_concept`, `run_pass_b` →
  `VerifyArgs.socratic`) açılmayacaksa `key_flaw_concept=""`; API/JSON/indirme dahil hiçbir yere
  gitmez. Açılacaksa kavram `check_leaks` hedefi (`LeakField` += `key_flaw_concept`): önce yeniden
  üretim, sonra kavram gizlenir, sorular kalır. Şablonlar (genel ad) True. Masaüstü kartı, CLI,
  Markdown bayrağa bakar (`hint_level >= 3` kalktı).
- **O7:** `_RelativeTomlSource._read_file` BOM'u atar; `config_writer` BOM'lu okur, BOM'suz yazar.
- **Y7:** `config_writer` satır içi tabloyu ve nokta anahtarlı `providers.x`'i yerinde günceller
  (başlıklı tablo yalnız başlıklı tablonun altına; aksi tomlkit sonraki satırları yanlış tabloya
  kaydırıyordu), yazım atomik.
- **Y8/O9:** `config.config_file()` (env → çalışma dizini → paketteki varsayılan);
  `pyproject` wheel'e `codementor.toml`'u ekler. `runtime.writable_config_file()`: env → exe yanı /
  kurulu wheel'de `~/.codementor/codementor.toml` (paketteki kopyalanır) → depodaki etkin dosya;
  seçilen yol `CODEMENTOR_CONFIG_FILE`'a yazılır (yeniden yükleme ve Bağlantılar'daki konum aynı
  dosya). `prepare_environment` kurulu wheel'de kullanıcı toml'unu etkinleştirir.
- **O8 (karar):** `.env` yüklenmez (öğrenci projesindeki `.env` sağlayıcı komutunu
  değiştirebilirdi, §12); `.env.example` başlığı + güncel liste, README.
- **Y9/O12:** `cli/errors.py` `system_errors`: OSError, SQLAlchemyError, ValidationError,
  TOMLDecodeError, DataFileError → `Hata: …` + 3 (`typer.Exit`'e dokunmaz). `analyze` (DB, `--out`
  `with` ile), `toolchain status/install`, `eval compare/analyze`.
- **O11:** `cli.main.run()` giriş noktası (`[project.scripts]`), kök `--help` UTF-8.
- **D20:** `rules list` "Durum" sütunu (kapalı/açık; ayar okunamazsa "—").
- Testler: `test_pipeline_concept.py`, `test_analysis.py` (+4 kavram), `test_config_cli_faz_c.py`
  (17), `desktop/test_faz_c_app.py` (3). Yazıcı/CLI değişiklikleri geri alınınca 9 test düşüyor.
  `tests/conftest.py` `_restore_config_env`: `writable_config_file` env'e yazdığı için testler arası
  sızıntıyı keser (önce sıra bağımlı 30 düşüş görüldü).
**Doğrulama:** ruff, format, mypy temiz; `pytest -m "not live"` 3313 geçti, 15 atlandı; web 36 test + `tsc`;
wheel geçici venv'e kuruldu: toml'suz dizinde varsayılan `claude_cli`, 6 zig kaynağı, kök `--help`
UTF-8; masaüstünde seviye 1 kartında kavram gizli, 2. denemede açık (ekran görüntüsü).
**Açık:** `toolchain install` indirme hatası hâlâ 1 dönüyor (sistem hatası sayılabilir; Faz G).
Önbellekteki eski raporlar bayraksız: kavram gösterilmez (güvenli taraf).

## Faz K — Notlar (kullanıcı soruları + token kullanımı; 2026-10-13)
Kaynak: kullanıcı isteği (Faz C'den önce). Kararlar (kullanıcı): soru ekleme masaüstü formu + CLI;
basit form (başlık, açıklama, dil, zorluk zorunlu); token her zaman görünür, aşama dağılımı,
toplam/geçmiş.
**Yapılanlar:**
- **Kullanıcı soruları (ADR-0028):** `QuestionPublic.origin` (`builtin|user`; hedef karmaşıklık
  yalnız yerleşikte zorunlu, kullanıcı kimliği `kullanici-` önekli), `UserQuestionDraft`
  (boşlar genel kısıt/etiket/ipucuyla dolar, `O(...)` sarmalayıcısı atılır, zaman+bellek
  birlikte). `questions/user_store.py`: slug kimlik (Türkçe katlama, çakışmada `-2`), atomik YAML
  yazımı, düzenlemede sürüm artışı, yerleşik soru silinemez, bozuk dosya atlanır + uyarı.
  `QuestionBank.load_all` (API, orkestratör, CLI, demo); `ApiState.reload_questions`.
  `config.data.user_questions_dir` (varsayılan `~/.codementor/questions`, yazılabilir yol).
- Masaüstü: Sorular ekranında "+ Soru ekle", "Kendi sorularım" filtresi, kartta "Kendi sorum"
  rozeti + Düzenle/Sil (onaylı); `views/question_form.py` (dile göre motor, HTML/CSS'te hedef
  alanları kapalı, hata formda Türkçe); mantık `questions_controller.py`'de.
- CLI: `questions add <yaml>`, `questions remove <id>`, `list`'te `(kendi)`; `validate` yalnız
  yerleşik banka.
- **Token:** `ReportMeta.stage_tokens` (`TokenSplit`; `llm_a` onarımlar dahil, `llm_v`, `llm_b`;
  toplamı `tokens_in/out`), `usage_label` hiç gizlenmez (`token 0 (önbellekten | model
  çağrılmadı | derleme hatası… | model yanıt vermedi)`), biçim `1.540 token (giriş 1.200 · çıkış
  340) · tahmini · ~$x`; `usage_breakdown_label`; `storage.cache.usage_totals` (SQL toplam,
  maliyet `json_extract`) → Geçmiş başlığında "Toplam: N analiz · X token · ~$Y". CLI altbilgisi,
  masaüstü rapor başlığı ve web paneli aynı metin; `schemas/` + `web/src/types` yeniden üretildi.
- Testler: `test_user_questions.py` (35), `test_pipeline_usage.py` (6),
  `test_user_questions_app.py` (11), `test_usage_label.py` yeniden yazıldı, web `usage.test.ts`.
**Ekranda doğrulama:** masaüstü gerçek `App` ile açılıp gezildi (geçici dizin). Bulunan iki sorun
düzeltildi: uzun token etiketi rapor başlığıyla çakışıyordu (ayrı satıra alındı); dağılım onarımı
"Analiz"e yazıyordu, oysa `repair_attempts` tüm aşamaların toplamı (sona `N onarım`).
**Kararlar:** web/API'de yazma yok (güvenlik incelemesi ayrı iş). Etiket biçimi bilinçli değişti;
eski etiket testleri yeni metne güncellendi.
**Doğrulama:** ruff, format, mypy temiz; `pytest -m "not live"` 3287 geçti, 15 atlandı; web 36 test,
`tsc` temiz.
**Açık:** `desktop/app.py` 504 satır (Faz G bölme). Web'de prettier uyarısı 22 dosyada (önceden
vardı, CI'da yok).

## Faz B — Notlar (kısmi LLM hatasında bulgu kaybı, önbellek doğruluğu; 2026-10-13)
Kaynak: `docs/BulgularVeDuzeltilecekler.md` Y3, Y4, Y5, O2, O3, O4. Dal `faz/a2-guvenlik`ten.
**Yapılanlar:**
- `pipeline/passes.py`: `LLMSession.providers/incomplete/checkpoint` ve `fail_part`.
  `run_pass_a` şemaya uyan son yanıtı saklar; onarım tükenir ya da onarım çağrısı sağlayıcı hatası
  verirse bulgular korunur, karmaşıklık boş + `COMPLEXITY_UNVERIFIED` (Y3). Geçiş B ayrı `try`:
  sağlayıcı/bütçe/yapılandırma hatası Geçiş A'yı silmez, sorular şablondan (Y4). Karmaşıklık
  Geçiş B prompt'una yalnız doğrulandıysa girer. Tek geçişte K5 bulgu attıysa ya da karmaşıklık
  kurtarıldıysa ayrı Geçiş B (O2).
- `pipeline/orchestrator.py`: süre sınırında Geçiş A bittiyse `checkpoint` kullanılır (doğrulama
  geçişi yarıda kaldıysa `VERIFY_FAILED`); `run.cacheable` = yarım değil ∧ yalnız birincil
  sağlayıcı yanıt verdi (Y5); Tier 1 ayarı analiz başına bir kez (`_run_validation`).
- `pipeline/signature.py` (yeni): `pipeline` imzası mod/doğrulama öneki + kural, prompt, doğrulayıcı,
  onarım ayarları, Tier 1 etkinliği + seçilecek aracın kimliği ve dosya boyutu/zamanı, soru modeli
  özeti (O3). `storage/cache.save_analysis(cacheable=)`: değilse boş anahtar (`NOT_CACHEABLE`).
- `pipeline/assemble.from_cache`: `cost_est=None`, `usage_estimated=False` (O4).
- Testler: `test_pipeline_partial.py` (18), `test_pipeline_cache_key.py` (12),
  `test_pipeline_signature.py` (6). Önbellek denetimi kapatılınca 8, eski imzayla 9 test düşüyor.
**Kararlar:** DB şeması değişmedi (yarım rapor boş anahtarla geçmişte durur). Derleyici sürümü süreç
açmadan dosya boyutu + değişiklik zamanıyla temsil edilir. Fallback testleri iki koşuda da aynı
zincir yapısını kullanır (anahtar sağlayıcı/model etiketine bağlı; aksi hâlde test boşuna geçer).
**Doğrulama:** ruff, format, mypy temiz; `pytest -m "not live"` 3224 geçti, 15 atlandı; statik dev
eval A2 ile birebir aynı (zamanlamalar hariç).
**Açık:** `orchestrator.py` 457, `passes.py` 406 satır (400 sınırı; bölme Faz G'de). Önbellek
anahtarında referans çözüm dosyası ve `data/checklists` içeriği yok. A1+A2+B kod-denetçi denetimi.

## Faz A2 — Notlar (araç keşfi çalışma dizini, sınırlayıcı benzerleri, .gitignore; 2026-10-13)
Kaynak: `docs/BulgularVeDuzeltilecekler.md` Y1, D13, P3. Dal `faz/a1-guvenlik`ten açıldı.
**Yapılanlar:**
- `validation/runner.py` `find_on_path(name, search_path)`: yalnız mutlak `PATH` dizinleri, Windows'ta
  `PATHEXT`, POSIX'te çalıştırma izni; çalışma dizini ve göreli girdiler hiç denenmez.
  `toolchain._which` (`shutil.which` yerine) ve `providers/_cli_common` (`_candidates` → `_locate`)
  aynı yardımcıyı kullanıyor.
- `prompts/templates.py`: `˂` U+02C2, `❮` U+276E, `❰` U+2770, `«` U+00AB `<` sayılır; `&lt;`/`&LT;`
  biçimli sınırlayıcı ve rol etiketleri `&amp;lt;` yapılır. `﹤` U+FE64 NFKC ile zaten kapsanıyordu.
- `.gitignore`: `linkedin metini.md`.
- Testler: çalışma dizinine bırakılan sahte `gcc/g++/clang/clang++/zig/dotnet` (`.exe/.bat/.cmd`)
  seçilmez (eski kodla düşüyordu), göreli `PATH` girdileri yok sayılır, mutlak dizin bulunur,
  `find_on_path` PATHEXT/dizin/çalıştırma izni; 5 benzer × 4 etiket, 6 varlık biçimi, 5 olağan metin.
**Doğrulama:** ruff, format, mypy temiz; `pytest -m "not live"` 3188 geçti, 15 atlandı.
**Açık:** Y2 (kullanıcı, `private/`), K2 kalan regex taraması, A1+A2 kod-denetçi denetimi.

## Sonraya (kapsam dışı fikirler)
- **Public öncesi zorunlu (kullanıcı, 2026-10-13):** Y2 — `tests/fixtures/llm_responses/unity03_reference.cs`
  bankadaki unity-03 referans çözümüyle (`private/`) karşılaştırılacak; aynı/benzerse yapay bir
  çözümle değiştirilip golden'lar yeniden üretilecek. GitHub'da secret scanning, push protection,
  Dependabot alerts açılacak (P13).
- CPP-OWN-001 akış duyarlı eşleşme: erken `return`/istisna yolunda atlanan `delete` öneri yerine hata sayılsın (Faz 52 denetimi).
- Faz 51 denetimi: `RunConfig` etiket/veri seti sürümü taşımıyor; eski koşular yeni etiketlerle sessizce yeniden puanlanabiliyor (etiket özeti `RunConfig`'e + `compare` dipnotu). Ters yön: bellek erişimi olmayan `memory_safety` etiketleri (CPP-OWN-001 çıplak `new[]`: dev `cpp-009`, `cpp-105`, test `cpp-006`) yeni tanıma uymuyor → Faz 52 (kural bazında öneri türü) ile birlikte ele alınmalı. Etiketlerde serbest metin sezgisi yerine yapısal `boundary:` alanı.
- Faz 49: `sessions` tablosu da sınırsız büyüyor (oturum başına bir satır); eski oturumları `updated_at`'e göre budamak. ~~Tier 1 derleyici sürümü önbellek imzasında yok.~~ (Faz B: araç kimliği + dosya boyutu/zamanı)
- Faz 49 denetimi O3 (**Faz B'de kısmen kapandı:** soru modeli özeti imzada; referans çözüm dosyası, `data/checklists` ve kod değişiklikleri hâlâ yok): önbellek anahtarında soru içeriği yok (`question_id` var; referans çözüm, `concept_tags`, `data/checklists` ve `pipeline/assemble.py`/`stages.py` değişince eski rapor dönebilir). Soru içeriği özeti anahtara eklenebilir.
- Faz 49 denetimi Ü9: eksik sütunlu eski şema (`OperationalError`) ve bozuk `created_at` için şema göçü yok; `list_analyses` korunmuyor.
- ~~Faz 48 denetimi~~ (**Faz B'de kapandı**): süre Geçiş B (Sokratik) sırasında dolarsa doğrulanmış Geçiş A sonucu da atılıyor; bulguları koruyup yalnız Sokratik kısmı şablona düşürmek `run_pass_b is None` yoluyla tutarlı olur (`run_llm_passes` kısmi sonuç döndürmeli).
- Faz 36: kural bazında öneri türü (doğru eşleşmiş `new`/`delete` için CPP-OWN-001, `Reserve` yok UE-MEM-001, `with` dışı `open` PY-RES-001). ~~Claude Opus canlı dev ölçümü~~ → yapıldı (2026-10-05).
- Eval: `select_part` etiket değişikliğine duyarlı; parça atamasını kimlik özetiyle sabitlemek ya da sonuç dosyasına parça kimliklerini yazıp birleştirmede eksik/çakışanı uyarmak.
- Faz 37: kullanıcının keyring'inde kalmış eski OpenAI/DeepSeek anahtarlarını temizleme seçeneği.
- ~~Faz 34: dev setini büyütmek~~ → yapıldı (2026-10-04, dev 96). Kalan: few-shot'ların zayıf modelde etkisi.
- Faz 35: few-shot örneklerine `certainty` alanı eklemek (şu an yalnız kural metninde). ~~Doğrulama kararlarını eval sonucuna yazıp düşürülenlerin TP/FP dağılımını ölçmek~~ → Faz 39.
- Faz 30: web soru seçicisinde filtre sonucu boşsa 'eşleşen soru yok' mesajı (şu an yalnız 'Serbest mod' seçeneği kalıyor).
- ~~Faz 30: `validate` ile `load_reference` aynı çözüm yolu doğrulayıcısını paylaşsın (validate şu an yalnız `is_file()`); dağıtımda `private/` olmadığı için `reference_solution_unreadable` uyarısı her soru bağlamlı analizde loglanıyor, düzeyi `debug` olabilir.~~ → Faz 31.
- Faz 30: yöntem işaretlerini (`METHOD_LEAKS`) soru verisine taşıyıp `validate`'e eklemek; eski soruların kontrol listesi seçimini kilitleyen bir anlık görüntü testi.
- Faz 30: Unreal stub'ına sık türler (`Super` için sınıf içi typedef deseni, `FMath`, `EEndPlayReason`, `FHitResult`, `UPrimitiveComponent`, `USphereComponent`, dinamik delege makroları, `GetWorldTimerManager`); şu an referans çözümler bile yalnız tavsiye uyarılarıyla geçiyor.
- Faz 30: soru bankası için öğretmen/kullanıcı içerik incelemesi ve sorulara örnek giriş/çıkış alanı.
- Faz 29: kurulu zig sürümünü `codementor.toml` ile karşılaştırıp masaüstünde "güncelle" önermek (işaret dosyasında sürüm/sha var, okunmuyor).
- Faz 29: indirilen zig'den yerel hedef dışındaki libc başlıklarını budamak (382 MB → tahminen <150 MB).
- Faz 29: tek dosya exe gömülü RoslynCheck.exe'yi %TEMP%'e açıyor; AppLocker/antivirüs engellerse `/health/ready`'de araç hatası. Gerekirse onedir dağıtımı ya da kullanıcı dizinine kopyalama.
- Faz 26: API hız sınırı (istemci başına, süreçler arası doğru); web arayüzünün API anahtarı göndermesi.
- Faz 26: SQLite çağrılarını da iş parçacığına almak (bağlantı başına iş parçacığı ya da havuz).
- Faz 25: OpenAI katı mod kısıtlarını canlı anahtarla doğrulayıp `SchemaAdapter.openai_strict`'te desteklenenleri korumak.
- ~~Faz 25: masaüstü ve web raporunda tahmini token/maliyet gösterimi (şu an yalnız CLI alt satırı ve JSON).~~ → Faz 33.
- Faz 25: agy canlı doğrulaması (oturum var; `allow_tool_agent = true` ile tek analiz).
- ~~Faz 24: arama büyük/küçük harf ve "tam sözcük" seçenekleri, değiştir (Ctrl+H); bırakılan klasördeki kaynak dosyalarını listeleme.~~ → Faz 33.
- ~~Faz 24: toml'a yazıldıktan sonra masaüstü tercihlerindeki aynı geçersiz kılmalar gereksizleşir (zararsız); "toml'dan yeniden yükle" düğmesi yok.~~ → Faz 33.
- ~~Faz 23: `reference_solution_path` (`private/solutions/`) hâlâ çalışma dizinine göre; soru dosyasının ya da kaynak kökünün dizinine göre çözülmeli (sızıntı testi buna göre güncellenmeli).~~ → Faz 31.
- ~~Faz 23: mimari §20 ADR tablosunda ADR-0013/0014/0015 satırları eksik.~~ → Faz 31.
- ~~Faz 23: CI exe işi Roslyn denetleyicisini derlemiyor~~ → Faz 27.
- ~~Faz 21 denetimi O3: kurallar sıcak yolu fonksiyon adıyla eşliyordu.~~ → Faz 32'de fonksiyon kimliğiyle eşleştirme yapıldı.
- ~~Faz 21: `rules_version` yalnız `rules/*.py` hash'i; `analysis/` ve `data/call_costs.yaml` değişiklikleri önbellek anahtarına yansımıyor (bayat önbellek riski).~~ → Faz 31.
- ~~Faz 21: `log.exception` izi sınırsız ve CLI'da WARNING düzeyinde stderr'e basılır; kural istisna mesajı kullanıcı kodu parçası içerebilir (§12) — iz DEBUG'a ya da kısaltılmış mesaja alınabilir. `captured_logs` teardown'u önceki yapılandırmayı değil varsayılanı geri yükler.~~ → Faz 31.
- Faz 21: `file_value_types` ad çakışması (`struct Hit` + başka ad alanında `class Hit`) nadir yanlış negatif; yalnız arayüzden türeyen `class A : IFoo` sıcak sayılır (muhafazakâr).
- Faz 21'den kalan işler Faz 32'de kısmen kapandı: C-MEM-001 aynı dosyadaki kullanıcı fonksiyonu, UE-GC-001 `TArray` alanları ve CS-PERF-001 `IList` çözüldü. ~~C-MEM-003 akış duyarlılığı~~ (Faz 57'de çözüldü). Açık: döngüde `std::string +`/C# `string +=` karesel ipucu (Sonraya).
- ~~Faz 16: eval veri setine Python/HTML/CSS örnekleri ve ölçüm~~ → Faz 18'de yapıldı.
- ~~Faz 18: Tier 0 `</div>` kör noktası~~ → Faz 20'de HTML-STD-003 ile bulgu olarak.
- ~~Faz 20: HTML-STD-003 kaçırmaları (Faz 56): dosya sonunda bitmemiş `<div`, `<p><span>a<div>`, DOCTYPE'sız belgede `table`/`p`, aynı satırdaki farklı ihlaller, katalog açıklaması.~~ → Faz 56'da çözüldü.
- HTML-STD-003: adoption agency (biçimlendirme öğesi yeniden kurulumu), foster parenting ve `form`/`button` kapsam ayrıntıları modellenmiyor (Faz 56 bilinen sınır).
- ~~Kural motoru: bulgu sayısına üst sınır yok (600 satırlık kötü niyetli girdi 600 bulgu üretip prompt'a gidebilir).~~ → Faz 31.
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
- ~~Faz 5/6 öncesi: tree-sitter ayrıştırmasına süre sınırı; 40 KB girdide yüzlerce ms ölçülmüştü.~~ → Faz 55'te kapatıldı (ADR-0024): süreç içi iptal 0.25.2'de kullanılamıyor; boyut/eşzamanlılık sınırları + gerileme testiyle idare, C# gramer yavaşlaması kabul edildi.
- ~~Tier 0: kapanmamış blok varken dosya sonuna uzanan ERROR düğümleri özete dönüşüyor; bağımsız gerçek hata ayrıca raporlanmayabilir (D2; Faz 55).~~ → Faz 55'te çözüldü (`trailing_semicolon_gap`).
- ~~`mask_non_code` C++ raw string (`R"(...)"`) içindeki tırnak/yorum/ayraçları doğru maskelemiyor (Faz 55).~~ → Faz 55'te çözüldü (delimiter sınırlı maskeleme).
- C# 11 raw string (`"""…"""`) maskelemesi (Faz 55'te kapsam dışı bırakıldı).
- `mask_non_code` dil bilgisi almıyor: Python'da `R"(…"` C++ ham metni sanılabilir (Faz 55 denetimi).
- ~~Tier 0 parse'ı sert zaman aşımıyla alt süreçte izole etmek (ADR-0024 sonucu)~~ → Faz 59'da yapıldı (ADR-0025; varsayılan kapalı).
- Tier 0 yalıtımında sıcak işçi havuzu (her analizde ~280 ms süreç açma maliyeti; yüksek yükte) (Faz 59).
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
- ~~Faz 17: C-MEM-003 denetimin kullanımdan sonra yapıldığını görmüyor~~ (Faz 57'de çözüldü; yanlış dal ve koşullu koruma ayırt edilmiyor). UNITY-GC-001 closure bastırması satır bazlı.
- `test_toolchain_install.py` tam koşuda bir kez 4 testle aralıklı düştü (Faz 57); tek başına yeşil. Tekrarlarsa paylaşılan geçici dizin/yarış incelenmeli. → Faz 58'de çözüldü (Windows tarayıcı kilidi; `_rename` yeniden denemesi).
- C-MEM-001: aynı dosyadaki kullanıcı fonksiyonuna geçirilen işaretçi (`print_arr(arr, n)`) sahiplik aktarımı sayılıyor (sık kaçırma); çağrılan fonksiyon aynı dosyadaysa ve `free`/saklama yoksa bulgu verilebilir. Aynı değişkene iki kez `malloc`, gölgeleme ve `realloc` de bilinçli sınırlar.
- UNITY-GC-001: dosyada tanımlı kullanıcı `struct`'ı için `new Hit(3)` yanlış bulgu (değer tipi); Faz 5 `CSHARP_VALUE_TYPES` dosyadaki struct adlarıyla genişletilebilir.
- UE-GC-001: `TArray<AActor*>`/`TMap<..., UObject*>` kapsayıcı alanları kaçırılıyor; UCLASS olmayan sınıfta (`FPlain`) öneri `UPROPERTY` değil `TStrongObjectPtr`/`FGCObject` olmalı.
- CS-PERF-001: `IList`/`IReadOnlyList`/`ICollection` tipli değişkenler maliyet tablosunda çözülmüyor (kaçırma).
- ~~Kural motoru: çöken kuralın istisna izi loglanmıyor; structlog (Faz 10) ile `log.exception` eklenmeli.~~ → Faz 21/31.
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
- ~~Faz 10: CLI ilerleme göstergesi yalnızca aşama adını gösteriyor; token/süre canlı gösterilebilir.~~ → Faz 33.
- ~~Faz 11: senkron aşamaları `asyncio.to_thread`'e taşımak~~ → Faz 24 (Tier 1) + Faz 26 (Tier 0, olgular); SQLite Sonraya.
- Faz 11: API anahtarı / hız sınırlama (§12); yerel olmayan bağlamada zorunlu kılınabilir. (Faz 13 kararı: v1'de yok, README Sınırlamalar.)
- ~~CLI ajanı iptali~~ → Faz 19'da yapıldı.
- ~~Faz 5 hatası (csharp-011): `foreach` koleksiyon ifadesindeki çağrı döngü içinde sayılıyordu → `high` O(n²)~~ → çözüldü (2026-09-30, kullanıcı isteğiyle Faz 12 içinde): `_context.contexts` döngü başlığında bir kez değerlendirilen alanlara (`initializer`, `right`: C `for` başlatıcısı, C++ range-for, C# `foreach`) dış bağlamı verir; `tests/fixtures/complexity/on_{foreach_header_call,range_for_header_call,for_initializer_strlen}` + koşuldaki `strlen` için `on2_strlen_condition`. Dev static-only Big-O %88 → %92.
- Çağrı maliyeti tablosu eksikleri (eval notları): `std::memset`/`memcpy` (n), `UGameplayStatics::GetAllActorsOfClass` (n), `TArray::Remove` (n); `std::string operator+` / C# `string +=` döngüde karesel (şu an n).
- ~~Faz 12: eval'e `guard_interventions` metriği~~ → Faz 22 Aşama A.
- ~~Faz 12: `eval analyze` aracı (kategorisiz eşleşme, önem filtreli precision, örnek bazında FP/FN); `compare` statik satırında injection direncini "—" göstermeli.~~ → Faz 22A / Faz 31.
- Faz 12: precision iyileştirme — `design` bulgularını yalnızca soru gereksinimi varken üretmek, `low` bulguları raporda ayrı göstermek; kategori belirsizliği (sıfıra bölme `edge_case`/`undefined_behavior`, null `edge_case`/`memory_safety`) için prompt'ta kategori tanımları. Değişiklik sonrası dev'de yeniden ölçülmeli (test artık kullanıldı).
- Faz 12: few-shot 0/1 ablasyonu (§14.4) koşulmadı. → Faz 34.
- CI Windows işi (2026-09-30): `windows-latest`'te g++ (MinGW) ilk derlemede 10 sn sınırını aşıyor (`test_cpp_type_error_failed` → `timeout`); clang++ varsayılan MSVC hedefli olduğundan Unreal stub denetimi `tool_error` ile atlanıyor (2 test). Ürün zarif atlıyor ama Windows'ta clang için `--target=x86_64-w64-mingw32` / başlık yolu ve soğuk başlangıç süresi ele alınmalı; o zamana kadar Windows CI `-m "not live and not compiler"`.
- ~~Faz 13: README için GIF demo~~ → Faz 26 (Pillow).
- ~~Faz 13: Web UI'da indirme, sağlayıcı ve mod seçimi~~ → Faz 26.
- ~~Faz 13: Monaco'yu tembel yükleme~~ → Faz 26.
- ~~Faz 13: `YAPILANLAR.md`'ye Faz 8–12 özetleri~~ → Faz 26.
- ~~Faz F (F8 denetimi): `desktop/connections.py` 402 satır (> 400, AGENTS.md)~~ → F12'de oturum açma akışı `desktop/login.py`'ye çıkarılınca **366 satıra** indi (400 satır kuralı sağlanıyor); `KeyStore`/katalog taşıma önerisi gereksiz kaldı.
- Faz F (F11 kapsamı): `history_controller.open_history` kaydı hâlâ ana iş parçacığında okuyor (`get_analysis`/`get_row` + `runtime.load_source`) ve diskten kod yüklüyor; F11 yalnız liste/silme/temizleme ile sınırlı tutuldu, kayıt açmayı da arka plana almak Sonraya.
- Faz F (F12): macOS'ta `open -a Terminal <cli>` ek argümanları (ör. `claude auth login`) Terminal uygulamasına geçirmez; `osascript -e 'tell application "Terminal" to do script "…"'` ile argümanlı sürüm Sonraya (şimdilik CLI argümansız açılıp kendi oturum açma akışını başlatıyor).
- Faz F (F10 denetimi, 2026-10-14): küçük bulgular — `run_ollama_pull` içindeki `result.error` ve `result.timed_out` dalları test edilmiyor; model adı deseni `.` ve `/` karakterlerini kabul ediyor (`/x`, `../x` zararsız); `ollama pull` süreci iptal edilemiyor (köprüde `Cancellation`, arayüzde iptal düğmesi yok). Ayrıntı: `docs/BulgularVeDuzeltilecekler.md` §10 Faz F.
