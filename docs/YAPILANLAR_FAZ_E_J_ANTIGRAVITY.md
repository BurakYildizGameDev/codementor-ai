# Antigravity Faz E-J Teslim Raporu

## Özet
| Faz | Dal | Son commit | Durum | Madde (✅/⚠️/❌) |
|---|---|---|---|---|
| E | faz/e-web | f8a2be4 | tam | 12/0/0 |
| F | faz/f-masaustu | 138fbcf | tam | 13/0/0 |
| G | faz/g-saglayici | 0472603 | tam | 11/0/0 |

> **Kapanış denetimi (2026-10-16):** F satırı "sürüyor 3/0/10" iken yazılmıştı; Faz F'nin tamamı
> (F0-F12) bitti (`PROGRESS.md` Faz F "Yapılanlar", son commit `138fbcf`) ve satır güncellendi.
> G satırı bu denetimde eklendi: G0-G7 (sevk belgesi §7) + G8 (dosya bölme) + G9 (belge temizliği)
> + G kapanış denetimi = 11 madde, hepsi ✅. Kod kapanış commit'i: `0472603`; kayıt commit'i:
> `5d72072` (+ bu hash'i işleyen commit). Ayrıntı: aşağıdaki "Faz G" bölümü.

## Faz E
### E1 — GET /v1/analyses — ✅
- Değişen dosyalar: `src/codementor/models/api.py`, `src/codementor/storage/cache.py`, `src/codementor/api/routes.py`, `schemas/analysis_page.schema.json`, `web/src/types/analysis_page.ts`
- Yeni testler: `tests/api/test_analyses_list.py` (`test_empty_list`, `test_order_newest_first`, `test_pagination`, `test_limit_bounds`, `test_list_requires_key_when_configured`, `test_list_has_no_code`)
- Mutasyon kontrolü: `list_stored` rotası devre dışı bırakılınca ilgili testler düştü (9 failed).
- Not: `report_json` gövdesi sayfalı listede döndürülmez (yalnızca özet metadatalar).

### E2 — DELETE /v1/analyses ve DELETE /v1/sessions/{id} — ✅
- Değişen dosyalar: `src/codementor/storage/cache.py`, `src/codementor/storage/sessions.py`, `src/codementor/api/routes.py`, `src/codementor/models/api.py`, `schemas/deleted_count.schema.json`, `web/src/types/deleted_count.ts`
- Yeni testler: `tests/api/test_analyses_list.py` (`test_delete_all_analyses`, `test_delete_all_requires_key`, `test_delete_session`, `test_delete_unknown_session_404`)
- Mutasyon kontrolü: `clear_analyses` ve `delete_session` rotaları devre dışı bırakılınca testler düştü.

### E3 — Web'de geçmiş paneli — ✅
- Değişen dosyalar: `web/src/components/HistoryPanel.tsx`, `web/src/components/HistoryPanel.test.tsx`, `web/src/api/client.ts`, `web/src/App.tsx`, `web/src/styles.css`, `web/e2e/app.spec.ts`
- Yeni testler: `web/src/components/HistoryPanel.test.tsx` (6 birim testi), `web/e2e/app.spec.ts` (Playwright e2e testi).
- Doğrulama: Satır silme, tümünü temizleme (onaylı), sayfalama (Daha fazla), tıklanan raporu ana ekranda açma ve silinen açık raporu ekrandan kaldırma destekleniyor.

### E4 — Web istemcisi X-API-Key gönderebilsin — ✅
- Değişen dosyalar: `web/src/lib/apiKey.ts`, `web/src/lib/apiKey.test.ts`, `web/src/api/client.ts`, `web/src/App.tsx`, `web/src/styles.css`
- Yeni testler: `web/src/lib/apiKey.test.ts` (3 birim testi), `web/src/api/client.test.ts` (10 birim testi).
- Not: API anahtarı güvenli şekilde `sessionStorage`'da saklanır (`localStorage`'a yazılmaz). 401 durumunda kullanıcıya Türkçe uyarı ve doğrudan anahtar giriş alanı sunulur.

### E5 — O15: Monaco hover'da güvenilmeyen markdown — ✅
- Değişen dosyalar: `web/src/lib/markdown.ts`, `web/src/lib/markers.ts`, `web/src/lib/markers.test.ts`
- Yeni testler: `web/src/lib/markers.test.ts` (`hover mesajında güvenilmeyen markdown ve bağlantıları kaçışlar`).
- Doğrulama: `escapeMarkdown` ile LLM bulguları ve derleyici tanıları kaçışlanır, kalın markdown işaretleri korunurken bağlantı ve resimler etkisizleştirilir.

### E6 — O16: Güvenlik başlıkları — ✅
- Değişen dosyalar: `web/index.html`, `web/vite.config.ts`, `src/codementor/api/security_headers.py`, `src/codementor/api/app.py`, `tests/api/test_security_headers.py`
- Yeni testler: `tests/api/test_security_headers.py` (4 test).
- Doğrulama: Web için CSP meta etiketi (`default-src 'self'; ...`), API yanıtları için `X-Content-Type-Options: nosniff` ve `Referrer-Policy: no-referrer` başlıkları en dış ara katmanda 401/404/413 dahil tüm yanıtlara eklenir. Playwright testinde CSP konsol hatası 0'dır.

### E7 — D14: Anahtar varken iç uçlar korunur — ✅
- Değişen dosyalar: `src/codementor/api/auth.py`, `tests/api/test_api_auth.py`
- Yeni testler: `tests/api/test_api_auth.py` (`test_internal_endpoints_protected_with_key`, `test_internal_endpoints_open_without_key`).
- Doğrulama: Anahtar tanımlıyken `/v1/*`, `/health/ready`, `/docs`, `/redoc`, `/openapi.json`, `/docs/oauth2-redirect` korunur; `/health` açık kalır.

### E8 — D15: Markdown dışa aktarımında HTML kaçışı — ✅
- Değişen dosyalar: `src/codementor/report/markdown.py`, `tests/unit/test_report_render.py`
- Yeni testler: `tests/unit/test_report_render.py` (`test_markdown_html_escaping`).
- Doğrulama: Serbest metindeki `&`, `<`, `>` kaçışlanır; kod blokları ve satır içi kod (`...`) korunur.

### E9 — D17: İndirme URL'si gecikmeli iptal — ✅
- Değişen dosyalar: `web/src/lib/download.ts`, `web/src/lib/download.test.ts`
- Yeni testler: `web/src/lib/download.test.ts` (`saveBlob creates link, clicks it, and revokes URL after delay`).
- Doğrulama: `URL.revokeObjectURL(url)` 1000ms gecikmeli çağrılır.

### E10 — Soru filtresi boşsa mesaj — ✅
- Değişen dosyalar: `web/src/components/Controls.tsx`, `web/src/components/Controls.test.tsx`
- Yeni testler: `web/src/components/Controls.test.tsx` (3 test).
- Doğrulama: Zorluk filtresi sonucu boş olduğunda "Bu filtrelerle eşleşen soru yok." mesajı gösterilir.

### E11 — Dışa açık serve ve hız sınırı — ✅
- Değişen dosyalar: `src/codementor/cli/serve.py`, `src/codementor/config.py`, `src/codementor/api/guard.py`, `src/codementor/api/state.py`, `src/codementor/api/routes.py`, `codementor.toml`, `docs/mimari.md`, `tests/unit/test_cli_serve.py`, `tests/api/test_trust_boundary.py`
- Yeni testler: `tests/unit/test_cli_serve.py` (3 test), `tests/api/test_trust_boundary.py` (`test_rate_limit_exceeded_429`).
- Mutasyon kontrolü: `RateLimiter.check` devre dışı bırakılınca `test_rate_limit_exceeded_429` düştü (200 != 429).
- Doğrulama: Dışa açık adrese anahtarsız ve `--insecure` olmaksızın bağlanılamaz (kod 3). Dakikalık analiz hız sınırı aşılınca 429 ve `Retry-After: 60` döner.

### E12 — CSRF / text/plain güven sınırı regresyonu — ✅
- Değişen dosyalar: `tests/api/test_trust_boundary.py` (`test_text_plain_post_rejected`).
- Doğrulama: `POST /v1/analyze` isteklerine `text/plain` gönderildiğinde istek 415/422 ile reddedilir, arka planda 0 LLM çağrısı yapılır.

## Faz F
### F0 — app.py controller'lara bölündü — ✅
- Değişen dosyalar: `src/codementor/desktop/history_controller.py` (yeni, 137 satır), `src/codementor/desktop/config_controller.py` (yeni, 89 satır), `src/codementor/desktop/app.py` (396 satır).
- Sonuç: `app.py` 506 satırdan 396 satıra düşürüldü (< 400 satır sınırı korundu). Modüller tkinter-free içe aktarılabiliyor (`tests/unit/test_tkinter_free_imports.py::MODULES` listesine eklendi, 9 test yeşil).
- Commit: `769dca6` (`refactor(faz-f): app.py controller'lara bolundu`).

### F1 — O10: Bozuk/kilitli veritabanında açılış kurtarma — ✅
- Değişen dosyalar: `src/codementor/desktop/runtime.py`, `src/codementor/desktop/launch.py`, `src/codementor/desktop/app.py`, `src/codementor/storage/db.py`, `src/codementor/config.py`, `src/codementor/storage/sessions.py`
- Yeni testler: `tests/desktop/test_launch_db.py` (`test_corrupted_db_recovery_yes`, `test_corrupted_db_recovery_no`, `test_backup_corrupted_db_with_wal_and_shm`, `test_corrupted_db_recovery_rename_fails`), `tests/desktop/test_app.py::test_report_callback_exception_shows_toast`.
- Doğrulama & Denetim Bulgusu ve Düzeltmesi:
  - Bozuk DB açılışında `askyesno` ile kullanıcı onayı alınır, onaylanırsa dosya `codementor.db.bozuk-YYYYAAGG-SSDDss` olarak (varsa `-wal`, `-shm` ile) yeniden adlandırılır ve temiz `ApiState` ile yeni veritabanı kurulur.
  - Reddedilirse veya yedekleme başarısızsa (kilitli) `SystemExit(3)` döner.
  - Windows SQLite dosya kilidi çözümü: SQLite motorunun `create_all` hatası sonrası açık kalan bağlantısı `Database.__init__` `except` bloğunda `self.engine.dispose()` ile ve `launch.py`'de `state.close()` + `gc.collect()` ile temizlenerek dosya kilidi kalkar.
  - Denetim düzeltmesi: `Database.from_settings` içindeki `settings.storage.session_retention_days` çağrısının modelde henüz tanımlanmamış olması tespit edildi; `config.py::StorageSettings`'e `session_retention_days` ve `storage/sessions.py`'ye `prune_old_sessions` eklenerek hata tamamen giderildi.
  - `App.report_callback_exception` ile arayüzdeki beklenmeyen hatalar loglanır ve kullanıcıya Türkçe toast ("Beklenmeyen bir hata oldu; ayrıntı desktop.log'da.") gösterilir.

### F2 — O13: Dışa aktarma hatası bildirimi — ✅
- Değişen dosyalar: `src/codementor/desktop/history_controller.py`
- Yeni testler: `tests/desktop/test_app.py::test_export_oserror_shows_toast`.
- Doğrulama: Rapor dışa aktarılırken `OSError` oluşursa sessizce geçmek yerine Türkçe toast ("Rapor kaydedilemedi: ...") ile bildirilir. Testte geçersiz dizin yolunda toast üretildiği ve istisna fırlatılmadığı doğrulandı.

### F3 — O14: "Geçmişi temizle" gizlilik ve disk temizliği — ✅
- Değişen dosyalar: `src/codementor/storage/cache.py`, `src/codementor/desktop/history_controller.py`, `tests/unit/test_storage.py`, `tests/desktop/test_app.py`.
- Yeni testler: `tests/unit/test_storage.py::test_clear_analyses_vacuums_and_removes_bytes`, `tests/desktop/test_app.py::test_clear_history_confirmation_and_cleanup` (recent_files kontrolü eklendi).
- Doğrulama: `clear_analyses` sonrasında `VACUUM` ve `PRAGMA wal_checkpoint(TRUNCATE)` çalıştırılarak diskteki SQLite dosyasından ve WAL dosyasından silinen öğrenci kodunun bayt izleri tamamen temizlenir (`BENZERSIZ_ISARET_9f3a` bulunamaz). `clear_history` aynı zamanda `recent_files` listesini boşaltır.

### F4 — D19: Veritabanı sağlamlığı ve meşguliyet kontrolleri — ✅
- Değişen dosyalar: `src/codementor/storage/db.py`, `src/codementor/config.py`, `src/codementor/storage/sessions.py`, `src/codementor/desktop/views/history_view.py`, `src/codementor/desktop/history_controller.py`, `src/codementor/desktop/app.py`, `codementor.toml`, `docs/mimari.md`, `tests/unit/test_storage.py`, `tests/desktop/test_app.py`.
- Yeni testler: `tests/unit/test_storage.py::test_database_pragmas_and_version`, `tests/unit/test_storage.py::test_prune_old_sessions_and_retention`, `tests/desktop/test_app.py::test_delete_history_while_analysis_running_is_blocked`, `tests/desktop/test_app.py::test_history_view_delete_button_disabled_when_busy`.
- Doğrulama:
  - SQLite bağlantı dinleyicisinde `PRAGMA journal_mode=WAL`, `busy_timeout=5000`, `secure_delete=ON`, `user_version=1` (`_migrate`) aktif.
  - Analiz sürerken (`app.analyze_view.busy`) `HistoryView`'daki "Sil" butonları `disabled` duruma geçer; `delete_history` çağrısı meşgulken toast ("Analiz sürerken silinemez...") ile engellenir.
  - `StorageSettings.session_retention_days = 90` ayarı `codementor.toml` ve `docs/mimari.md` §11, §17'ye işlendi; 90 günden eski oturumlar açılışta budanır.

### F5 — D18: Dosya kaydetme (Ctrl+S / Farklı Kaydet), CRLF koruması ve kirli durum takibi — ✅
- Değişen dosyalar: `src/codementor/desktop/files.py`, `src/codementor/desktop/widgets/code_editor.py`, `src/codementor/desktop/views/analyze_view.py`, `src/codementor/desktop/history_controller.py`, `src/codementor/desktop/questions_controller.py`, `src/codementor/desktop/app.py`, `tests/desktop/test_app.py`.
- Yeni testler:
  - `tests/desktop/test_app.py::test_dirty_file_discard_confirm_and_save`
  - `tests/desktop/test_app.py::test_save_as_for_new_unsaved_file`
  - `tests/desktop/test_app.py::test_save_preserves_original_crlf_newline`
  - `tests/desktop/test_app.py::test_save_oserror_shows_toast`
  - `tests/desktop/test_app.py::test_close_with_unsaved_changes_confirm`
- Doğrulama:
  - `FileController` içinde `current_path`, `is_dirty`, `_newline` tespiti ve koruması eklendi.
  - Dosya açıldığında veya kod yazıldığında dosyanın orijinal satır sonu biçimi (`\r\n` veya `\n`) tespit edilir ve kaydederken korunur.
  - Kaydedilmemiş değişiklik varken yeni dosya açma (`open_dialog`, `open_recent`), sürükle-bırak (`on_drop`), geçmişten yükleme (`open_history`), örnek kod yükleme (`load_sample`), soru başlatma (`start`) ve pencereyi kapatma (`close`) öncesinde kullanıcıya onay sorulur (`confirm_discard`).
  - Ctrl+S kısayolu `<Control-s>` ve `<Control-S>` ile global olarak `self.files.save` fonksiyonuna bağlandı.
  - Kaydetme esnasında `OSError` oluşursa kullanıcıya Türkçe toast ("Dosya kaydedilemedi: ...") ile bildirilir.
  - `CodeEditor.set()` metodunda `edit_modified(False)` sıfırlaması yapılarak programatik yüklemelerin yanlışlıkla dirty olarak algılanması önlendi.

### F6 — Geçmişte sayfalama ve arama — ✅
- Değişen dosyalar: `src/codementor/storage/cache.py`, `src/codementor/desktop/views/history_view.py`, `src/codementor/desktop/history_controller.py`, `src/codementor/desktop/app.py`, `tests/unit/test_storage.py`, `tests/desktop/test_app.py`.
- Yeni testler:
  - `tests/unit/test_storage.py::test_list_analyses_page_pagination`
  - `tests/unit/test_storage.py::test_list_analyses_page_search_and_escaping`
  - `tests/desktop/test_app.py::test_history_view_pagination_and_search`
- Doğrulama:
  - `storage/cache.py::list_analyses_page`'e `search` parametresi eklendi; soru kimliği (`question_id`), dil (`language`) ve sağlayıcı (`provider`) alanlarında büyük/küçük harf duyarsız (`ilike`) filtreleme sağlandı.
  - SQL `LIKE` özel karakterleri (`%`, `_` ve kaçış ayracı `/`) `replace('/', '//').replace('%', '/%').replace('_', '/_')` ile kaçışlandı; joker olarak çalışmaları engellendi.
  - `HistoryView` üstüne arama kutusu (`CTkEntry`) ve "Ara" butonu eklendi; altta "Daha fazla yükle" butonu dinamik bağlandı (`clear` sonrası taze referans).
  - 60 kayıt ile test edildi: ilk yüklemede 50 satır + "Daha fazla yükle", tıklanınca 60 satır + buton gizlenmesi; "c-medium" aramasıyla tekil eşleşme; `_` ve `%` aramasında joker kaçışının çalıştığı masaüstü ve birim testleriyle kanıtlandı.

## Faz G
> **Özet:** 11/0/0 (G0-G9 + kapanış denetimi) · Dal `faz/g-saglayici` · Kod kapanış commit'i `0472603`,
> kayıt commit'i `5d72072` · Sevk belgesi: `docs/DEVIR_FAZ_E_J.md` §7. Kapanışta `Bulgular` §5'te ✅
> işareti olmayan D satırı kalmadı (D1-D20 tamamı ✅) ve 400 satırı aşan dosya kalmadı.

### G0 — `orchestrator.py` (465) ve `passes.py` (426) bölündü — ✅ (`ef5bd7a`)
- Değişen dosyalar: `pipeline/orchestrator.py`, yeni `pipeline/cache_flow.py`, `pipeline/deadline.py`,
  `pipeline/llm_session.py`, `pipeline/verify_pass.py`, `pipeline/passes.py`, `pipeline/assemble.py`.
- Yeni testler: **yok** — madde "davranış DEĞİŞMEDEN" koşuluyla geldi; `git diff -- tests/` BOŞ ve
  mevcut 3454 test aynı sonucu verdi (maddenin kabul kriteri bu).
- Doğrulama: `orchestrator.py` 465 → **393**, `passes.py` 426 → **330**; `ruff check`/`ruff format --check`
  temiz, `mypy src/` 211 dosyada hatasız, `pytest -m "not live"` 3454 geçti / 15 atlandı.
- Not: testler `Orchestrator._validation/_tier1/_remaining` ile `passes.build_repair_messages` /
  `build_socratic_messages`'i yamadığı için bu adlar sarmalayıcı olarak yerinde bırakıldı; taşınan
  adlar `__all__` ile yeniden dışa aktarılır (`pipeline/assemble.py`, `eval/runner.py` değişmedi).

### G1 — O5: CLI ajan çıktısı 64 KB'de kesiliyor — ✅ (`d362e19`)
- Değişen dosyalar: `validation/runner.py` (`ProcessLimits.output_limit`), `providers/_cli_common.py`,
  `providers/cli_agent.py`, `providers/codex_cli.py`, `config.py` (`CliConfig.output_limit_bytes`),
  `codementor.toml`, `docs/mimari.md`.
- Testler: `tests/providers/test_cli_agent.py`, `test_cli_agent_e2e.py`, `test_codex_cli.py`,
  `tests/providers/fake_cli_script.py` (`BOYUT:<n>` gürültü modu), `tests/unit/test_config.py`,
  `tests/unit/test_runner.py`.
- Doğrulama: 200 KB sahte çıktı varsayılan sınırla (1 MB, config'ten) tam okunuyor;
  `output_limit_bytes=65536` ile yanıt korunuyor + `ProviderResult.warnings`'e
  "Model yanıtı çok uzundu, kesildi." ekleniyor (raporda `meta.warnings`); Tier 1 derleyici 64 KB'de kalıyor.
- Açık (kullanıcıda): gerçek `agy`/`codex` çıktısıyla elle deneme (O5'in "canlı doğrulanmadı" notu).

### G2 — O6: kalıcı CLI hataları yeniden denenmez — ✅ (`3efcf80`)
- Değişen dosyalar: `providers/base.py` (`retryable` sözleşmesi), `providers/_cli_common.py`
  (`CliPermanentError`, `CliTimeoutError`), `providers/cli_agent.py`, `providers/codex_cli.py`.
- Testler: `tests/providers/test_cli_agent.py` (`test_logged_out_result_is_not_retried`,
  `test_claude_unknown_subtype_is_retried`, `test_server_error_is_still_retried`, ...).
- Doğrulama: oturum/kimlik ve bilinen `subtype` hataları `retryable = False`; sunucu hatası (5xx) ve
  bilinmeyen `subtype` yeniden denenmeye devam ediyor (fallback'e hemen geçilmiyor).

### G3 — D1-D12 küçük düzeltmeler — ✅ (`1857829`, `062528c`, `313128c`, `5f51dec`)
- **D1/D6/D7 (`1857829`):** prompt ve sağlayıcı/maliyet düzeltmeleri; `tests/integration/test_pipeline.py`,
  `test_pipeline_partial.py`, `tests/unit/test_prompt_builder.py`, `test_prompt_render.py`,
  `test_usage.py`, `tests/golden/report_example.json`.
- **D8 (`062528c`):** bozuk few-shot şablonu raporu düşürmüyor; yeni `tests/unit/test_prompt_degrade.py`.
- **D9-D11 (`313128c`):** ölü kod/test kancası temizliği, `LLMMarkupAnalysisOutput` şeması
  (`schemas/llm_markup_analysis.schema.json`), olay döngüsündeki küçük G/Ç (mtime anahtarlı önbellek);
  `tests/unit/test_schema_export.py`, `test_prompt_version.py`, `test_prompt_budget.py`.
- **D2-D5 + D12 (`5f51dec`):** `extract_json` tırnak durumu (D2), `codex_cli._events` `RecursionError` (D3),
  kelime sınırlı 429/401 regex'i (D4), `apply_verdicts` `finding_id` (D5) ve `_json_document` doğrusal
  tarama (D12; 160 KB düşman çıktıda < 0,25 sn).
- Doğrulama: `Bulgular` §5'te D1-D12 satırlarının tamamı ✅.

### G4 — D18: Tier 0 durdurma tanısı yapısal bayrak — ✅ (`ed21509`, `a92e23c`)
- Değişen dosyalar: `models/validation.py`, `validation/tier0_isolation.py` (metinle tanıma yerine
  yapısal bayrak), `api/auth.py` (D14 denetimi + sondaki eğik çizgi sertleştirmesi).
- Testler: `tests/unit/test_tier0_isolation.py`, `tests/api/test_api_auth.py`.
- Doğrulama: durdurma tanısı metin değişse de tanınıyor; anahtar varken iç uçlar korunuyor ve
  sondaki eğik çizgili biçim de aynı kurala giriyor.

### G5 — D20 kalanları (CLI/exe temizliği) — ✅ (`c1a1b91`)
- Değişen dosyalar: `buildinfo.py` (`get_logger("codementor.buildinfo")`), `cli/eval.py`
  (`eval run --language` → `Language` enum; geçersiz değer çıkış kodu 2 + izinli değer listesi),
  `build_exe.py` (`EXCLUDES`'a `uvicorn`), `docs/adr/0030-primary-name-protokolu.md`, `docs/mimari.md`.
- Testler: `tests/unit/test_buildinfo.py`, `tests/unit/eval/test_languages.py`, `tests/desktop/test_build_exe.py`.
- Doğrulama: exe duman testi `sc.json` `"ok": true` (çıkış 0). `fastapi`/`starlette` hariç tutulamadı
  (`--self-check` çıkış 1 verince geri alındı), `--help` İngilizce ipucu Typer/click içinden geldiği için
  değiştirilemedi, `pyproject.toml` `[desktop]` extra yapılmadı — üçü de **kabul edilen** sınır.

### G6 — Denetimden ertelenen 6 madde — ✅ (`c3f64fa`, `a39ec09`, `644852b`; senkron `48f4e16`)
- **Parça 1-2 (`c3f64fa`):** `desktop/config_writer.py` — dizi tablosu (`[[providers.x]]`) ezilmiyor,
  CRLF/LF satır sonu korunuyor; `tests/desktop/test_config_writer.py`.
- **Parça 3 (`a39ec09`):** `models/questions.py::UserQuestionDraft.from_question` — kullanıcı `genel`
  etiketini/varsayılan kısıtı açıkça yazdıysa silinmiyor; `tests/unit/test_user_questions.py`.
- **Parça 4-5 (`644852b`):** `cli/errors.py` ağ hatası metni, `UsageTotals` → `models/usage.py`
  (katman temizliği: `report` artık `storage`'dan içe aktarmıyor), `LLMProvider.primary_name`
  (ADR-0030); `tests/unit/test_cli_errors.py`, `test_usage_label.py`, `tests/providers/test_contract.py`,
  `test_factory.py`.
- **Senkron (`48f4e16`):** `docs/mimari.md` §5.5.1/§16 güncellendi, `.tmp_*.log` artıkları repodan
  çıkarıldı (`.gitignore`'a `.tmp_*.log`).
- Doğrulama: `ruff check`/`ruff format --check` temiz (469 dosya), `mypy src/` 212 dosyada hatasız,
  `pytest -m "not live"` 3511 geçti / 15 atlandı.

### G7 — `ProviderResult.schema_enforced` ve token kalibrasyon günlüğü — ✅ (`c403070`)
- Değişen dosyalar: `models/provider.py` (`schema_enforced: bool = False`), `pipeline/llm_session.py`
  (`log.debug("token_estimate_ratio", estimated, actual, ratio)`), `providers/anthropic.py`,
  `openai_compat.py`, `ollama.py` (True), `cli_agent.py`/`codex_cli.py` (False), `docs/mimari.md`.
- Testler: `tests/providers/test_adapters.py`, `test_gemini.py`, `test_fake.py`, `test_cli_agent.py`,
  `test_codex_cli.py`, `tests/unit/test_usage.py` (+9 test).
- Doğrulama: `ruff`/`format` temiz (469 dosya), `mypy src/` 212 dosya, `pytest -m "not live"`
  3520 geçti / 15 atlandı. Raporda gösterilmez; rapor şeması ve `schemas/` çıktısı değişmedi.

### G8 — `providers/cli_agent.py` 400 satır altına indi — ✅ (`0472603`)
- **Gerekçe:** dosya Faz G'de dört kez değişti (G1, G2, G6, D2-D4); kapanış denetiminde **420 satır**
  ölçüldü. G0 kabul kriteri yalnız `orchestrator.py`/`passes.py` idi, bu dosya "Sonraya"ya yazılmıştı;
  kullanıcı talimatıyla (2026-10-16) Faz G kapsamında kapatıldı.
- Değişen dosyalar: `providers/cli_agent.py` (**420 → 345**), yeni `providers/cli_result.py` (104).
- Taşınanlar: `_json_document`, `_object_spans`, `_served_model`, `_mapping`, `auth_error` (+ `_AUTH_HINTS`).
  Adlar `cli_agent`'tan aynen yeniden dışa aktarılır (testler `cli_agent._json_document` içe aktarıyor) —
  G0'daki `passes.py` kalıbı.
- Testler: **yok/değişmedi**; `git diff -- tests/` BOŞ. Kanıt: mevcut sağlayıcı testleri geçiyor
  (`tests/providers` + `tests/unit/test_prompt_role_tags.py` → 455 passed / 3 skipped).

### G9 — Belge temizliği: ADR tablosu ve `make` notu — ✅ (`c2968e2`)
- `docs/mimari.md` §20 ADR tablosuna eksik satırlar eklendi: **ADR-0024, ADR-0025, ADR-0028, ADR-0029**
  (denetimde 26/30 idi; artık 30 ADR dosyasının 30'u tabloda — komutla doğrulandı).
- `AGENTS.md` "Komutlar" bölümüne not: `make` her makinede yok (bu ortamda kurulu değil); `make check`
  yerine dört komut tek tek koşulur.

### G kapanış denetimi (2026-10-16) — ✅ (`c8e2e89`, `8616232`, `953b9e1`)
- **`c8e2e89` — `orchestrator.py` 421 → 379:** G0'da 393'e inmiş dosya G6/G7 eklemeleriyle yeniden
  400'ü aşmıştı; `Run`, `AnalysisTrace`, `PipelineError`, `PipelineErrorKind`, `ProviderFactory` ve
  `BANK_UNREADABLE` `pipeline/run_state.py`'ye alındı (bağımlılık yönü tek yönlü:
  `cache_flow`/`deadline` → `run_state`).
- **`8616232` — D16 belge notu:** `session_id` sahipliği `docs/mimari.md` §12 tehdit tablosuna yazıldı
  (kod değişmedi); `Bulgular` D16 ✅.
- **`953b9e1` — D20 satırındaki iki bayat madde:** `rules list` `[rules] disabled` uygulanıyor
  (**Faz C**, `test_rules_list_marks_disabled`) ve kapanışta süren analiz/indirme onayı var
  (**Faz F/F7**, `runtime.confirm_close`; `test_close_while_busy_confirm`,
  `test_close_while_downloading_confirm`) — ikisi de kod olarak hazırdı, yalnız kayıt satırı bayattı.
- **Doğrulama (kapanış):** `ruff check` → `All checks passed!`; `ruff format --check` → 471 dosya;
  `mypy src/` → 213 dosya, hatasız; `pytest -m "not live"` → **3524 passed, 15 skipped, 6 deselected** (3:34).
- **Kalan yok.** Ertelenen "elle deneme" işleri kullanıcıda (G1 gerçek `agy`/`codex` çıktısı; Faz F
  etkileşimli masaüstü maddeleri).

## Denetim komutlarının GERÇEK çıktısı
### faz/f-masaustu (F0-F6 güncel)
- `uv run ruff check .` → `All checks passed!`
- `uv run ruff format --check .` → `460 files already formatted`
- `uv run mypy src/` → `Success: no issues found in 206 source files`
- `uv run pytest tests/desktop/test_launch_db.py` → `4 passed in 0.35s`
- `uv run pytest tests/unit/test_tkinter_free_imports.py` → `9 passed in 5.11s`
- `uv run pytest tests/unit/test_storage.py` → `42 passed in 0.77s`
- `uv run pytest tests/desktop/test_app.py` → `59 passed in 56.12s`
- Satır sayıları: `app.py` → `399` (< 400), `files.py` → `129`, `history_controller.py` → `155`, `config_controller.py` → `89`, `history_view.py` → `273`, `cache.py` → `272`.

### faz/g-saglayici (G0-G9, kapanış dahil)
> Ölçümler sırayla: G0 sonrası ve her maddenin kendi commit'i ile; **son satırlar kapanış kolunun
> (G8/G9 sonrası, 2026-10-16) tam takım çıktısıdır.**
- `uv run ruff check .` → `All checks passed!`
- `uv run ruff format --check .` → `472 files already formatted`  (G0'da 460, kapanışta 471 → G8/G9 ile 472)
- `uv run mypy src/` → `Success: no issues found in 214 source files`  (G0: 211 → kapanış: 213 → G8: 214)
- `uv run pytest -m "not live" -q` → `3524 passed, 15 skipped, 6 deselected in 183.27s (0:03:03)`
- Hedefli (G8): `uv run pytest tests/providers tests/unit/test_prompt_role_tags.py -m "not live" -q`
  → `455 passed, 3 skipped in 5.67s`
- Satır sayıları: `orchestrator.py` **379** (465 idi), `passes.py` **366** (426 idi),
  `cli_agent.py` **345** (420 idi), yeni `cli_result.py` **104**, `run_state.py` 69,
  `desktop/app.py` 395.
- `git diff --stat` (G8): yalnız `src/codementor/providers/cli_agent.py` (+10/-85) ve yeni
  `cli_result.py`; **`tests/` diff'i boş** (davranış değişmedi).

### faz/e-web
- `uv run ruff check .` → `All checks passed!`
- `uv run ruff format --check .` → `456 files already formatted`
- `uv run mypy src/` → `Success: no issues found in 204 source files`
- `uv run pytest -m "not live"` → `3383 passed, 15 skipped, 6 deselected in 178.37s (0:02:58)`
- Linux taklidi (§3.1) → `7 passed in 4.49s`
- web: typecheck → `tsc -b --noEmit (exit code 0)` · test → `54 passed (54) in 2.76s` · build → `built in 404ms` · e2e → `4 passed (5.0s)`
- `git diff main...faz/e-web --stat -- tests/`:
  - `tests/api/test_analyses_list.py` (+226)
  - `tests/api/test_api_auth.py` (+55, -2)
  - `tests/api/test_errors_and_app.py` (+4, -2)
  - `tests/api/test_security_headers.py` (+60)
  - `tests/api/test_trust_boundary.py` (+38, -1)
  - `tests/unit/test_cli_serve.py` (+48)
  - `tests/unit/test_report_render.py` (+19, -1)
  - (Var olan hiçbir test silinmedi veya gevşetilmedi; `test_errors_and_app.py` dışa açık IP testine E11 gereği `--insecure` eklendi)

## Yapamadıklarım ve neden
- Yok. Tüm E1-E12 maddeleri eksiksiz tamamlandı ve test edildi.
- **Faz G:** kod tarafında yapılamayan yok (G0-G9 + kapanış denetimi tamam, kalan madde yok). Yalnız
  **elle deneme** işleri kullanıcıda: (a) O5'in gerçek `agy`/`codex` çıktısıyla doğrulanması (canlı CLI
  oturumu gerekir; testler sahte CLI ile ağsız koşuyor), (b) Faz F'nin etkileşimli masaüstü maddeleri.
  G5'te üç sınır **kabul edildi**: İngilizce `--help` ipucu (Typer/click kaynağından), `fastapi`/
  `starlette`'ın exe'den çıkarılamaması ve `pyproject.toml` `[desktop]` extra yapılmaması.

## Mimariden sapma gerektiren öneriler (uygulanmadı)
- Yok. Tüm mimari kurallarına ve `docs/mimari.md` §17 ilkelerine tam uyuldu.
- **Faz G:** sapma yok. G0 ve G8 (dosya bölme) mimari değişikliği değildir: yalnız modül sınırı taşındı,
  davranış ve sözleşmeler aynı kaldı (`tests/` diff'i boş; taşınan adlar yeniden dışa aktarılır).

## Var olan bir testi değiştirdiysem: hangisi, neden
- `tests/api/test_errors_and_app.py::test_serve_uses_config_and_warns_when_exposed`: `serve --host 0.0.0.0` çağrısına E11 kuralı gereğince anahtarsız dış bağlantı engeli geldiği için `--insecure` argümanı eklendi.
- **Faz G:** hiçbir test gevşetilmedi/silinmedi. G0 ve G8'de `tests/` **hiç değişmedi** (bölmeler
  davranışsız refactor); G1-G7'de yalnız yeni testler eklendi, `tests/providers/fake_cli_script.py`
  sahte CLI'sine `BOYUT:<n>` gürültü modu eklendi (G1).


## Claude Code'un özellikle bakmasını istediğim yerler
- `src/codementor/api/guard.py::RateLimiter` ve `ApiState` bağlantısı.
- `web/src/components/HistoryPanel.tsx` ve `web/src/App.tsx` entegrasyonu.
