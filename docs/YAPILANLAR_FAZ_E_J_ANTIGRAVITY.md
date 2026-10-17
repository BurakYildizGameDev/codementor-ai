# Antigravity Faz E-J Teslim Raporu

## Özet
| Faz | Dal | Son commit | Durum | Madde (✅/⚠️/❌) |
|---|---|---|---|---|
| E | faz/e-web | f8a2be4 | tam | 12/0/0 |
| F | faz/f-masaustu | 138fbcf | tam | 13/0/0 |
| G | faz/g-saglayici | 0472603 | tam | 11/0/0 |
| H | faz/h-kurallar | 0fb7162 (H4) | H1–H4 tam | 4/0/0 |
| J | faz/j-checklist-snapshot | e7f50d7 | kısmi (Zig budama bilinçli atlandı) | 1/0/0 |

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

## Faz H
### H1 — yedi yeni statik kural — ✅ (`145d8a9`)
- Değişen dosyalar: `src/codementor/rules/css.py`, `src/codementor/rules/cpp_perf.py`,
  `src/codementor/rules/c_buffer.py`, `tests/rules/fixtures/{CSS-ACC-001,CSS-LAYOUT-001,CSS-LAYOUT-002,
  CPP-PERF-002,CPP-PERF-003,CPP-PERF-004,C-BUF-002}/…`, `tests/rules/test_engine.py`,
  `tests/rules/test_registry.py`, `tests/unit/test_cli_rules.py`, `docs/rules-catalog.md`,
  `README.md`, `README.en.md`.
- Yeni testler: her kural için pozitif/negatif fixture (otomatik bulunur), 7 süre vakası (40 KB sınırı),
  "her kuralın fixture'ı var" denetimi, katalog tür testleri → **+53 test**.
- Mutasyon kontrolü: H1 turunda kurallar tek tek devre dışı bırakılıp fixture testleri düşürülerek
  doğrulandı (fixture'sız kural yazmanın riski `selectors` alan adı sondası hatasıyla somutlaştı).
- Karar: devir tablosundaki yedinci kural (C# döngüde `string +=`) zaten `CS-ALLOC-001` olduğundan
  yerine **C-BUF-002** (`scanf("%s")` genişlik sınırı) yazıldı; kural sayısı **34 → 41**.

### H2 — bilinen kaçırma ve yanlış pozitifler — ✅ (`492f955`, `3a15f40`)
- Değişen dosyalar: `src/codementor/rules/cpp.py` (CPP-OWN-001 tür yükseltmesi),
  `src/codementor/rules/csharp.py` (`Enumerable` alıcısı), `src/codementor/analysis/call_costs.py`
  (`_INSTANCE_METHODS`), `tests/rules/fixtures/CPP-OWN-001/*`,
  `tests/rules/fixtures/CS-PERF-001/*`, `tests/unit/test_call_costs.py`, `tests/rules/test_engine.py`,
  `docs/rules-catalog.md`.
- Yeni testler: 4 CPP-OWN-001 fixture'ı + 1 süre vakası (660 çift, 36 490 bayt) + 3 CS-PERF-001
  fixture'ı + 2 çözücü testi → **+10 test**.
- Mutasyon kontrolü: `_skips_delete` devre dışı bırakılınca CPP-OWN-001 fixture'ları `suggestion`
  döndü (issue bekleyen testler düştü); `_INSTANCE_METHODS` kaldırılırsa
  `test_icollection_with_linq_still_unknown` düştü.
- Karar: `IReadOnlyList<T>.Contains` **zaten** `Enumerable.Contains` olarak çözülüyordu; eksik olan
  kuralın `Enumerable` alıcısını tanımamasıydı. `ICollection<T>.Contains` örnek metottur ve alıcı bir
  `HashSet` olabilir → bilinçli kaçırma (LINQ adayı üretilmez).

### H3 — analiz verisi — ✅ (`deb2eda`)
- Değişen dosyalar: `src/codementor/analysis/{call_costs.py,_symbols.py,lexical.py,parsers.py,
  extractor.py}`, `src/codementor/models/{bigo.py,_bigo_parser.py,_bigo_algebra.py}`,
  `src/codementor/validation/{include_guard.py,tier1.py}`, `data/stubs/ue_stubs.h`,
  `data/call_costs.yaml`, `tests/unit/{test_call_costs,test_extractor,test_bigo,test_lexical,
  test_parsers,test_include_guard,test_tier1,test_ue_stubs}.py`,
  `tests/fixtures/tier0/cpp/valid/unreal_wave_spawner.cpp`, `tests/compiler/test_tier1_compiler.py`,
  `docs/mimari.md`.
- Yeni testler: **+130 test** (sayılar: `pytest -m "not live"` 3587 → 3717): `call_costs` argümana
  duyarlı indeks (11 çözücü + 4 olgu + 3 `first_arg`), `parse_bigo` Θ/Ω + `max` + `log log n` +
  40 KB süre (14), C# 11 ham metin (12), Unreal stub/delege (12), include koruması izin listesi (28),
  kolon birimi (5), delege ayrıştırma (4).
- Mutasyon kontrolü (9 mutasyon, her biri ilgili testleri düşürdü):
  | Mutasyon | Düşen test |
  |---|---|
  | `_refined_cost` devre dışı | 6 (`test_argument_aware_index_costs`, `test_index_costs_reach_facts`, …) |
  | Θ/Ω sarmalayıcı kaldırıldı | 7 (`test_theta_*`, `test_omega_*`) |
  | `log log` kolu kaldırıldı | 16 (`test_log_log_n`, sıralama + hypothesis özellikleri) |
  | `csharp = False` (leksik) | 6 (`test_csharp_*`) |
  | `parse_source`'da `delegates=False` | 2 (`test_delegate_source_parses_*`, Tier 0 fixture) |
  | `#pragma` izin listesi kapalı | 7 (`pragma_macro_dependency` dahil) |
  | `#line` denetimi kapalı | 4 (`line_with_filename` dahil) |
  | `-fdiagnostics-column-unit=byte` çıkarıldı | 2 (argv + yeniden deneme) |
  | `_first_argument` → None | 3 (metin taşıma + olgu zinciri) |
- Karar/not: madde 1'de ayrım yalnızca **aynı liste** üzerinde yapılır (`xs.RemoveAt(xs.Count - 1)`) —
  başka koleksiyonun indeksi `n` kalır (yanlış `1` yanlış negatif olurdu). `Θ/Ω` yalnızca tam ifadeyi
  sarabilir. `max(a,b)` toplam olarak normalleşir (`max(a,b) = Θ(a+b)`), belgeye yazıldı. `n^k`
  eklenmedi (sembolik üs modellenmiyor) ve `docs/mimari.md` §5.6 bu gerçeğe göre düzeltildi.
  **Denetimde ikinci bir boşluk bulundu:** `DECLARE_DYNAMIC_MULTICAST_DELEGATE_*(...)` bildirimleri
  tree-sitter'da sözdizimi hatası verdiği için delege kullanan geçerli Unreal kodu Tier 0'da erken
  çıkıyordu (Tier 1 hiç çalışmıyordu); makrolar artık yalnızca ayrıştırma yolunda boşaltılır
  (`neutralize_unreal_macros(..., delegates=True)`), derleyici yolunda stub açar. Include korumasına
  izin listesi eklendi (`#pragma once/region/endregion`, `#line <sayı>`): `#define X GCC dependency
  "…"` + `#pragma X` ile host dosyası yoklanabiliyordu. `-fdiagnostics-column-unit=byte` ile gcc/clang
  aynı kolon birimini kullanır; bayrağı tanımayan eski sürümde komut bayraksız yeniden denenir.

### H4 — statik dev ölçümü — ✅ (`0fb7162`)
- Değişen dosyalar: `README.md` (dev eval bloğu `eval compare` çıktısından yeniden üretildi + özet
  satır), `docs/ZAYIF_VE_GELISTIRILECEK_YONLER.md` §4.8, `PROGRESS.md`,
  `eval/results/20261016T212522_static_none_static_dev.json` (yeni sonuç dosyası; eskiler silinmedi).
- Yeni testler: yok (ölçüm maddesi); `tests/unit/eval/test_readme_table.py` **değiştirilmedi** ve yeşil.
- Karar/not: yalnızca statik dev (96 örnek): precision **%100 → %100** (H1'in yeni kuralları yanlış
  pozitif üretmiyor), recall %55,2 → **%57,5**, F1 %71,1 → **%73,0**, Big-O %97/%97, erken çıkış
  %100/%100, p50 0,13 sn. Test bölümü `--final` olmadan koşulmadı (devir §5 kuralı).

### H denetimi (2026-10-17) — ✅ (`ae86816`, `fd4bad7`, `39e94de`)
- **Denetim kapsamı:** `git diff b67c94d..485e69a` = 79 dosya, +11 404/−103 (8 739 satırı H4'ün statik dev
  sonuç JSON'u); kapsam dışı dosya yok. Kayıtlı kural sayısı **41 kayıt / 41 benzersiz kimlik**
  (`PROGRESS.md`, `docs/rules-catalog.md`, `README.md`, `README.en.md` ile uyumlu). `docs/mimari.md`
  §6.1/§12/§5.2.2/§5.6 sapmasızlığı, katman sınırları, yeni Pydantic modeli yokluğu ve kullanıcı
  metnini okuma sınırları (`_MAX_TEXT`/`_MAX_RECEIVER_BYTES` 120 B, `_MAX_FORMAT_BYTES`/
  `_MAX_TYPE_BYTES` 200 B) doğrulandı. **Birleştirme kararı: evet** (kritik bulgu yok); tek
  doğrulanamayan boyut yerelde koşulamayan `-m compiler` (CI'ya bırakıldı).
- **Düzeltilen iki bulgu** (davranış değişikliği yalnız CSS-ACC-001'deki kaçırmanın kapanması):
  1. **CSS-ACC-001 aşırı susturma** (`rules/css.py`): `any(… or "" in covered …)` koşulu, dosyada
     *herhangi* bir yalın `:focus-visible` kuralı varsa **tüm** `:focus { outline: none }` bloklarını
     susturuyordu; `.x:focus` kuralı `:focus-visible`'dan daha özgül olduğu için bu gerçek bir a11y
     kaçırmasıydı. Koşul kaldırıldı (susturma artık aynı kök seçici için geçerli). Fixture:
     `CSS-ACC-001/positive/global_focus_visible_override.css` (bulgu) + `…/negative/bare_both.css`
     (yalın `:focus` ↔ yalın `:focus-visible` hâlâ susar). `catalog_note` ve `docs/rules-catalog.md`
     güncellendi.
  2. **`rules/cpp.py` 452 satır** (AGENTS.md 400 satır sınırı; H2 sonrası): CPP-PERF-001 bloğu
     (`_LARGE_TYPES`, `_PARAMETERS`, `_MOVES`, `_function_declarator`, `_Kept`, `_kept_argument`,
     `_is_large`, kural sınıfı) `rules/cpp_perf.py`'ye taşındı → `cpp.py` **338**, `cpp_perf.py` **360**
     satır. Taşınan blok birebir aynı; mevcut fixture/test **değişmedi**, yalnız kullanılmayan
     `strip_templates` içe aktarımı temizlendi ve iki modülün docstring'i konu ayrımını yazıyor.
- **Ölçüm:** statik dev yeniden koşuldu (`eval/results/20261017T161712_static_none_static_dev.json`):
  precision **%100** ve recall **%57,5** (0,5747) **değişmedi**, F1 %73,0, Big-O %97/%97, erken çıkış
  %100/%100, p50 0,14 sn (H4: 0,13 sn — makine gürültüsü). README'nin `dev` bloğu sonuç dosyalarından
  yeniden üretildi; `tests/unit/eval/test_readme_table.py` **değiştirilmedi** ve yeşil.
- **Açık karar kalmadı:** denetimin bıraktığı tek ürün kararı (`include_guard` izin listesine
  `pack`/`warning` eklenmesi, aşağıdaki 3. madde) 2026-10-17'de kullanıcı kararıyla kapandı.
- **Kapanan bulgu — include koruması izin listesi** (`src/codementor/validation/include_guard.py`):
  `_PRAGMA_NAMES = ("once", "region", "endregion", "pack", "warning")`; `_PRAGMA_ALLOWED` regex'i ve
  `_PRAGMA_RESERVED` kümesi bu demetten **türetilir** (izin listesi ile makro atlatması koruması ayrı
  tutulamaz). `#pragma pack`/`#pragma warning` hiçbir dosyayı okumaz; öncesinde bu dosyalar Tier 1'i
  gereksiz atlıyordu. Ad eşleşmesi harf duyarlı/tam sözcük kalır (`#pragma PACK(1)`,
  `#pragma packable`, `#pragma warning(GCC dependency "…")` reddedilir); `#define pack` /
  `#define warning` tanımlayan dosya fail-closed atlanır. Testler: `pragma_pack`/`pragma_warning`
  REJECTED → ALLOWED (bilinçli davranış değişikliği), vaka sayısı 103 → 116.
- **Tier 1 entegrasyon testleri (`76aba22`, 2026-10-17):** aynı karar **gerçek Tier 1 yolunda** da
  sabitlendi (`tests/unit/test_tier1.py`, **+6 vaka**): `#pragma pack`/`#pragma warning` içeren C++
  dosyası derleyiciye ulaşır (`PASSED`, atlama yok); Unreal yolundaki **iki** guard çağrısından da
  geçer; sahte derleyici = `sys.executable` ile **gerçek alt süreç** başlatılır (gcc tanı ayrıştırma
  yolu denenir); `#define pack`/`#define warning` + `#pragma` makro atlatması `SKIPPED`/`include_guard`
  (süreç hiç başlamaz); `#pragma PACK(1)` harf duyarlılığı korunur. Mutasyon: izin listesi eski hâle →
  **12 fail** (3'ü yeni); `_PRAGMA_RESERVED` ayrı tutulup daraltılınca → **6 fail**. Kaynak kod
  değişmedi; `pytest -m "not live"` **3732 → 3738**.


## Faz J — İsteğe bağlı küçük işler (2026-10-17)

### J1 — Kontrol listesi içerik anlık görüntüsü — ✅ (`e7f50d7`)
- **Ne:** `data/checklists/*.yaml` içeriğinin sha256 özeti `tests/golden/checklists_sha256.json`'a
  sabitlendi (8 dosya); test `tests/golden/test_checklists_golden.py` (**5 vaka**): içerik özeti,
  "özet dosya kümesi = dizin" kontrolü, özetin içeriği gerçekten izlediği, satır sonu farkının özeti
  değiştirmediği ve golden yazıcısının tur-gidişi. Güncelleme mevcut desenle: `--update-golden`.
- **Neden:** bu dosyalar prompt'a girer (mimari §8.3) ve ölçümü etkiler; yanlışlıkla düzenleme, satır
  kaybı, kodlama bozulması ya da dosya ekleme/silme sessiz kalmamalı. Hata mesajı **değişen dosyayı
  adıyla** söyler ve `--update-golden`'ı işaret eder (golden deseni: `tests/conftest.py`).
- **Karar:** özet, **LF normalleştirilmiş ham baytlardan** hesaplanır (`.gitattributes` LF'i zorluyor;
  CRLF farkı yine de özeti değiştirmez). Dosya kümesi `questions._loader.YAML_SUFFIXES`'ten türetilir:
  anlık görüntü, yükleyicinin okuduğu kümenin aynısını kapsar (biri eklenirse diğeri sessiz kalmaz).
- **Mutasyon kanıtı:** (a) `css.yaml` sonuna yorum → **1 fail** (`Kontrol listesi içeriği değişti:
  css.yaml`); (b) `gecici.yaml` ekle → **2 fail** (içerik özeti + dosya kümesi). İkisi de geri alındı,
  ağaç temiz.
- **Bağımsız çapraz kontrol:** `Get-FileHash -Algorithm SHA256` (Windows) çıktısı golden JSON ile
  8/8 dosyada birebir aynı — normalleştirme bir şeyi gizlemiyor.
- **Sayılar:** `pytest -m "not live"` **3738 → 3743 geçti** (16 atlandı, 6 seçilmedi, 4:22). **Kaynak
  kod değişmedi**: yalnız test + golden veri.

### J2 — Zig budama — ❌ (bilinçli yapılmadı)
- Kurulumdan sonra kullanılmayan libc başlık dizinlerini silmek (382 MB → <150 MB) **yerelde
  doğrulanamıyor**: bu makinede gcc/clang/zig yok, `uv run pytest -m compiler` koşulamıyor; devir
  "emin değilsen YAPMA" diyor. Kod değişikliği yapılmadı; doğrulama CI'ya / zig kurulu bir makineye
  bırakıldı.

### J3 — "YAPMA" listesi — ❌ (kapsam dışı, dokunulmadı)
- İmzalı exe / Inno Setup, cppcheck/clang-tidy, VS Code eklentisi, Rust/Go/JS desteği,
  `session_id`'yi anahtara bağlama: devir §10'un açık yasağı; hiçbirine dokunulmadı.


## Denetim komutlarının GERÇEK çıktısı
### faz/h-kurallar (H1–H4, 2026-10-16)
- `uv run ruff check .` → `All checks passed!`
- `uv run ruff format --check .` → `474 files already formatted`
- `uv run mypy src/` → `Success: no issues found in 216 source files`
- `uv run pytest -m "not live" -q` → `3717 passed, 16 skipped, 6 deselected in 229.31s (0:03:49)`
- `uv run pytest -m compiler -q` → `81 passed, 10 skipped, 3645 deselected in 18.45s`
  (bu makinede **gcc/clang/zig yok**; C/C++/Unreal derleyici testleri CI'da koşar → H3'ün stub ve
  fixture derleme doğrulaması yerelde **yapılamadı**, CI'ya bırakıldı)
- Linux taklidi (§3.1, `PYTHONPATH=$TEMP\notk; pytest -p block_tk -m "not live" -q`)
  → `3624 passed, 17 skipped, 6 deselected in 124.19s` (toplama hatası yok)
- Eval (yalnızca statik dev, 96 örnek):
  `uv run codementor eval run --split dev --static-only` →
  `eval/results/20261016T212522_static_none_static_dev.json`; denetim P/R/F1 **100% / 57% / 73%**,
  Big-O 97% / 97%, erken çıkış 100% / 100%, sızan 0%, p50 0.1 / p95 0.8 sn
- `uv run pytest tests/unit/eval/test_readme_table.py -q` → `5 passed in 0.39s`
- `git diff` (H4): `README.md` **2 satır eklendi** (yeni statik satır + sürüm satırı), kod dosyası yok.

### faz/h-denetim (H denetimi + iki düzeltme, 2026-10-17)
- `uv run ruff check .` → `All checks passed!`
- `uv run ruff format --check .` → `474 files already formatted`
- `uv run mypy src/` → `Success: no issues found in 216 source files`
- `uv run pytest -m "not live" -q` → `3719 passed, 16 skipped, 6 deselected in 252.79s (0:04:12)`
  (H sonu 3717; +2 = iki yeni CSS-ACC-001 fixture'ı; test kodu değişmedi)
- Hedefli: `uv run pytest tests/rules tests/unit -q` → `2740 passed, 3 skipped` (katalog güncelliği dahil;
  düzeltme öncesi katalog testi düşüyordu)
- Satır sayıları: `rules/cpp.py` → **338**, `rules/cpp_perf.py` → **360**, `rules/css.py` → 294 (< 400)
- Eval (yalnızca statik dev, 96 örnek): `uv run codementor eval run --split dev --static-only` →
  `eval/results/20261017T161712_static_none_static_dev.json`; denetim P/R/F1 **100% / 57% / 73%**
  (precision ve recall H4 ile birebir aynı: 0,5747), Big-O 97% / 97%, erken çıkış 100% / 100%, p50 0.1 /
  p95 0.9 sn
- `uv run pytest tests/unit/eval/test_readme_table.py -q` → `5 passed` (README `dev` bloğu +2 satır:
  yeni koşu satırı + sürüm satırı)
- `uv run pytest -m compiler -q` → **yerelde koşulamadı** (gcc/clang/zig yok, H notundaki gibi);
  H denetimi düzeltmeleri C/C++ derleyici yoluna dokunmadığı için CI koşusu yeterli


### faz/h-pragma-izin + entegrasyon testleri (Önemli-3, 2026-10-17)
- `uv run ruff check .` → `All checks passed!`
- `uv run ruff format --check .` → `474 files already formatted`
- `uv run mypy src/` → `Success: no issues found in 216 source files`
- `uv run pytest -m "not live" -q` → `3732 passed, 16 skipped, 6 deselected in 259.98s (0:04:19)`
  (izin listesi genişletildikten sonra); entegrasyon testleri eklendikten sonra →
  `3738 passed, 16 skipped, 6 deselected in 256.34s (0:04:16)`
- Hedefli: `uv run pytest tests/unit/test_tier1.py tests/unit/test_include_guard.py -q` → `174 passed`
- Mutasyon: izin listesi eski hâle → **12 fail** (3'ü yeni Tier 1 testi); `_PRAGMA_RESERVED` ayrı
  tutulup daraltılınca → **6 fail**; geri alınınca → `174 passed`
- `uv run pytest -m compiler -q` → **yerelde koşulamadı** (gcc/clang/zig yok); değişiklik derleyici
  çağrı biçimini değil, yalnız guard'ın atlama kararını değiştiriyor

### faz/j-checklist-snapshot (2026-10-17)
- `uv run ruff check .` → `All checks passed!`
- `uv run ruff format --check .` → `474 files already formatted`
- `uv run mypy src/` → `Success: no issues found in 216 source files`
- `uv run pytest -m "not live" -q` → `3743 passed, 16 skipped, 6 deselected in 262.73s (0:04:22)`
- Hedefli: `uv run pytest tests/golden/test_checklists_golden.py -q` → `5 passed`
- `Get-FileHash -Algorithm SHA256 data/checklists/*.yaml` → golden JSON ile birebir (8/8 dosya)
- Masaüstü/web/eval denetimleri bu değişiklikten etkilenmez (yalnız test + golden veri)

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
- **Faz J:** üç maddenin yalnız anlık görüntü maddesi yapıldı (`e7f50d7`).
  1. **Zig budama yapılmadı:** kurulum sonrası kullanılmayan libc başlık dizinlerini silmek
     (382 MB → <150 MB) bu makinede doğrulanamıyor (gcc/clang/zig yok → `-m compiler` koşulamıyor);
     devir §10 "emin değilsen YAPMA" diyor. Doğrulama CI'ya / zig kurulu bir makineye bırakıldı.
  2. **"YAPMA" maddeleri** (imzalı exe/Inno Setup, cppcheck/clang-tidy, VS Code eklentisi,
     Rust/Go/JS desteği, `session_id`'yi anahtara bağlama) kapsam dışı; dokunulmadı.
  3. Anlık görüntü testi **test bölümü/eval koşusu gerektirmez** (LLM yok, ağ yok): ek sınır yok.
- **Faz H:** H1–H4 tamamlandı; aşağıdakiler bilinçli sınırlardır (hepsi `PROGRESS.md`'de de yazılı):
  1. **`-m compiler` yerelde koşulamadı** (bu Windows makinesinde gcc/clang/zig yok): H3'ün Unreal
     stub'ı ve `unreal_wave_spawner.cpp` fixture'ı **derleme ile** doğrulanamadı; yalnızca tree-sitter
     ayrıştırması ve stub yapısı (birim testleri) doğrulandı. Derleme doğrulaması CI'ya bırakıldı;
     `-m compiler` yerelde `81 geçti / 10 atlandı`.
  2. **`n^k` (sembolik üs) eklenmedi:** model sayısal taban + sembolik üs (`2^n`) taşıyor; `n^k`'yi `n`
     ya da `n^2` saymak sessiz yanlış olurdu. Reddedilmeye devam ediyor; `docs/mimari.md` §5.6
     dilbilgisi listesi bu gerçeğe göre düzeltildi (yanıltıcı `n^k` örneği kaldırıldı).
  3. **Include korumasında bilinçli yan etki (2026-10-17'de kapatıldı):** H3'te `#pragma
      pack`/`#pragma warning` içeren dosyalar Tier 1'i atlıyordu (`SKIPPED` + Türkçe uyarı; fail-closed
      tercih). Kullanıcı kararıyla ikisi izin listesine alındı: bunlar hiçbir dosyayı okumaz (GCC
      `dependency` gibi bir yan biçimi yok), bu yüzden derleyici denetimini engellememeleri doğru.
      Fail-closed taraf korundu: `_PRAGMA_RESERVED = frozenset(_PRAGMA_NAMES)` (izin listesindeki adı
      tanımlayan `#define` + `#pragma <ad>` makro atlatması kapalı kalır) ve ad eşleşmesi harf
      duyarlı/tam sözcük. Depodaki fixture/eval/stub verisinde pragma yok → ölçüme etkisi yok.
  4. **Kalan include-koruması sınırı:** izin listesindeki adı (`once`/`region`/`endregion`/`pack`/`warning`) kullanıcının
     `#include` ettiği bir başlık tanımlarsa atlatma teorik olarak mümkün (yerel include'lar boş geçici
     çalışma dizinine göre çözülür, pratikte erişilemez). Tam kapatma makro tablosu izlemeyi gerektirir;
     yapılmadı, `PROGRESS.md` "Sonraya" bölümünde.
  5. **Test bölümü (`--final`) koşulmadı:** devir gereği test koşusu sürüm öncesi kullanıcı kararıdır;
     H4 kapsamı yalnızca dev.
  6. **K1–K3 küçük notları** (H1 denetimi): **K1 (CSS `:focus-visible {}` aşırı susturma) ve K3'ün
     `cpp.py` parçası (452 satır) H denetiminde düzeltildi** (yukarıdaki "H denetimi" bölümü);
     K2 (`scanf` satırında ikili bulgu) ve `cpp_perf.py` yerel sınıf metodu notu **kabul edildi**
     (sunum gürültüsü / muhafazakâr kaçırma), davranış fixture'la sabitlendi.
- Yok. Tüm E1-E12 maddeleri eksiksiz tamamlandı ve test edildi.
- **Faz G:** kod tarafında yapılamayan yok (G0-G9 + kapanış denetimi tamam, kalan madde yok). Yalnız
  **elle deneme** işleri kullanıcıda: (a) O5'in gerçek `agy`/`codex` çıktısıyla doğrulanması (canlı CLI
  oturumu gerekir; testler sahte CLI ile ağsız koşuyor), (b) Faz F'nin etkileşimli masaüstü maddeleri.
  G5'te üç sınır **kabul edildi**: İngilizce `--help` ipucu (Typer/click kaynağından), `fastapi`/
  `starlette`'ın exe'den çıkarılamaması ve `pyproject.toml` `[desktop]` extra yapılmaması.

## Mimariden sapma gerektiren öneriler (uygulanmadı)
- **Faz H:** sapma yok. H1–H4 `docs/mimari.md` sınırları içinde kaldı; yapılan belge düzenlemeleri
  mimariyi **koda uydurma** amaçlıdır (sapma değil): §5.2.2 komut tablosuna kolon birimi bayrağı ve
  stub içeriği, §5.2.3 include izin listesi, §5.3.2 argümana duyarlı maliyet, §5.6 Big-O dilbilgisi
  (yanlış `n^k` örneği → `2^n` + `log log n`/`Θ/Ω`/`max`). ADR gerekmedi: yeni ADR'lik bir mimari
  karar (katman, sözleşme, güvenlik modeli değişikliği) yok.
- Yok. Tüm mimari kurallarına ve `docs/mimari.md` §17 ilkelerine tam uyuldu.
- **Faz G:** sapma yok. G0 ve G8 (dosya bölme) mimari değişikliği değildir: yalnız modül sınırı taşındı,
  davranış ve sözleşmeler aynı kaldı (`tests/` diff'i boş; taşınan adlar yeniden dışa aktarılır).
- **Faz J:** sapma yok — üretim kodu ve veri dosyaları değişmedi; yalnız yeni bir golden testi ve onun
  beklenen dosyası eklendi (mimari §14 test stratejisi içinde). ADR gerekmedi.

## Var olan bir testi değiştirdiysem: hangisi, neden
- `tests/api/test_errors_and_app.py::test_serve_uses_config_and_warns_when_exposed`: `serve --host 0.0.0.0` çağrısına E11 kuralı gereğince anahtarsız dış bağlantı engeli geldiği için `--insecure` argümanı eklendi.
- **Faz H:** hiçbir test gevşetilmedi/silinmedi. H1'de yalnız **kural sayısını** bekleyen testler
  (`tests/unit/test_cli_rules.py`, `tests/rules/test_registry.py::test_c_rules_only_for_c`) yeni sayıya
  (41) ve yeni C kümesine çekildi; H2/H3'te yalnız ekleme yapıldı. H3'te **tek beklenti değişikliği**
  `tests/unit/test_bigo.py`'de oldu: `"log log n"` **geçersiz** girdi listesinden **çıkarıldı**, çünkü
  artık geçerli bir ifade (karşılığında 2 yeni test eklendi) — bu bir **sıkılaştırmadır**, gevşetme
  değil. `tests/fixtures/tier0/cpp/valid/unreal_wave_spawner.cpp` **genişletildi** (yeni stub API'sini
  kullanır); mevcut satırlar/iddialar korundu ve testler yalnızca ekleme yaptı.
  **H denetimi düzeltmelerinde (2026-10-17) hiçbir mevcut test değişmedi:** yalnız iki yeni CSS
  fixture'ı eklendi (`CSS-ACC-001/positive/global_focus_visible_override.css`,
  `…/negative/bare_both.css`), `docs/rules-catalog.md` yeniden üretildi ve README'nin `dev` bloğu
  sonuç dosyalarından yenilendi (`test_readme_table.py` değişmedi).
- **Faz G:** hiçbir test gevşetilmedi/silinmedi. G0 ve G8'de `tests/` **hiç değişmedi** (bölmeler
  davranışsız refactor); G1-G7'de yalnız yeni testler eklendi, `tests/providers/fake_cli_script.py`
  sahte CLI'sine `BOYUT:<n>` gürültü modu eklendi (G1).
- **Faz J:** hiçbir mevcut test değişmedi/gevşetilmedi; yalnız **yeni** bir golden testi ve onun
  beklenen dosyası eklendi (`tests/golden/test_checklists_golden.py`,
  `tests/golden/checklists_sha256.json`). `data/checklists/*.yaml` içeriği **değişmedi** (özetler
  mevcut içerikten üretildi).


## Claude Code'un özellikle bakmasını istediğim yerler
- **Faz J / kontrol listesi anlık görüntüsü** (`tests/golden/test_checklists_golden.py`): özetin
  **LF normalleştirilmiş ham baytlardan** alınması (`.gitattributes` LF'i zorluyor; CRLF'li bir çalışma
  kopyası testi kırmasın) ve dosya kümesinin `questions._loader.YAML_SUFFIXES`'ten türetilmesi.
  Alternatif: YAML'i ayrıştırıp **anlamsal** özet almak (biçim değişikliğine toleranslı olurdu ama
  yorum/sıra değişimini gizlerdi). Hangisi tercih edilir?
- **Faz H / include koruması izin listesi** (`src/codementor/validation/include_guard.py`): izin
  listesinin **fail-closed** tarafı ve `#pragma X` makro atlatmasının kapanışı. `#pragma pack`/
  `#pragma warning`'in Tier 1'i atlatması (bilinçli yan etki) kullanıcı kararıyla **kapandı**
  (2026-10-17): ikisi izin listesine alındı ve `_PRAGMA_RESERVED` artık `_PRAGMA_NAMES`'ten
  türetiliyor — denetimde özellikle bu türetmenin korunmasına bakılmalı.
- **Faz H / delege makroları** (`src/codementor/analysis/parsers.py`): `DECLARE_DYNAMIC_MULTICAST_DELEGATE*`
  makrolarının **yalnızca ayrıştırma yolunda** boşaltılması (derleyici yolunda stub açar). İki yolun
  ayrılması doğru mu, yoksa tek listede tutmak mı gerekir?
- **Faz H / kolon birimi** (`src/codementor/validation/tier1.py`): `-fdiagnostics-column-unit=byte` +
  "stderr bayrağı anıyorsa bir kez bayraksız yeniden dene" sezgisi (yerelleştirilmiş hata mesajlarına
  dayanıklı, ama kullanıcı kodu bayrak metnini içerirse fazladan bir çağrı).
- **Faz H / `CallName.first_arg`** (`src/codementor/analysis/_symbols.py`): 120 bayt sınırı ve
  `…` döndürme; indeks desenlerinin yalnızca **aynı liste** üzerinde daraltılması (muhafazakâr yön).
- `src/codementor/api/guard.py::RateLimiter` ve `ApiState` bağlantısı.
- `web/src/components/HistoryPanel.tsx` ve `web/src/App.tsx` entegrasyonu.
