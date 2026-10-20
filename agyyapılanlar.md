# CodeMentor AI — Antigravity Yapılanlar ve İlerleme Raporu

**Tarih:** 2026-10-20  
**Ajan:** Antigravity (Gemini 3.8 Flash High)  
**Kapsam:** Tam analiz, hata taraması, suite sağlık kontrolü, İş 6 (doküman eşitleme), İş 9 (Faz F/G küçük açıkları) ve İş 8 (depolama borcu) tamamlanması.  

---

## 1. Genel Sistem ve Test Sağlık Durumu

Projeyi devraldıktan sonra `make check` komut eşdeğerleri ve tüm test süitleri uçtan uca çalıştırıldı:

| Denetim | Komut | Sonuç | Notlar |
|---|---|---|---|
| **Linter** | `uv run ruff check .` | ✅ 0 hata | Kod tabanı temiz |
| **Formatter** | `uv run ruff format --check .` | ✅ 0 uyarı | 480 dosya biçimlendirilmiş |
| **Tip Kontrolü** | `uv run mypy src/` | ✅ 0 hata | 216 kaynak dosyada `mypy --strict` hatasız |
| **Birim / Entegrasyon Testleri** | `uv run pytest -m "not live"` | ✅ 3.903+ geçti | 16 atlandı (Windows platformu doğal atlamaları: POSIX `rlimit`, derleyici yokluğu vb.), 6 seçilmedi |
| **Web Vitest** | `npm --prefix web test` | ✅ 54 geçti | 12 test dosyası hatasız |
| **Web Typecheck** | `npm --prefix web run typecheck` | ✅ 0 hata | `tsc -b --noEmit` hatasız |

---

## 2. DeepSeek ve Önceki Ajanların Tamamladığı İşlerin Denetimi

Git geçmişindeki son commit'ler detaylı incelendi:
- `4e4ea70` (**İş 4 - K2 Regex Bütçesi**): `call_costs.py`, `leak_guard.py` ve `complexity.py` içindeki ReDoS riski taşıyan süper-doğrusal desenler düzeltildi; `test_regex_budget.py` (96 vaka) ile 40 KB girdide < 50 ms bütçesine bağlandı.
- `7281c0f` (**İş 5 - Statik Kural Kaçırmaları**): Dilim 1–5 başarıyla kapatıldı (`CPP-OWN-001` atlama akış duyarlılığı, `C-MEM-001` 8 turlu ödünç zinciri sabit noktası, `UNITY-GC-001` bayt aralığı bazlı LINQ closure filtrelemesi, `UE-GC-001` iç içe kapsayıcı `TMap<FName, TArray<UObject*>>` katman 2 araması, `C-MEM-003` dal/guard konum biçimleri).
- `c9f0115` (**İş 4b - Zamanlama Testleri Kararlılığı**): Makine yükünden bağımsız göreli büyüme (2× girdi ≤ 3× süre) + en iyi 3 koşu mantığı eklendi.
- `b93af14` (**İş 4c - Zayıf Yönler Belgesi Sayıları**): `docs/ZAYIF_VE_GELISTIRILECEK_YONLER.md` ölçümlere bağlandı.
- `e2cd23a` (**İş 2b - Bulgular §1 Tablosu**): Kapanış etiketleri hizalandı.

---

## 3. Bu Oturumda Yapılanlar (Antigravity)

### A. Doküman Durum Eşitleme (KALAN_ISLER.md İş 6) — ✅ Tamamlandı
- **Durum:** `KALAN_ISLER.md` listesinde açık (`[ ]`) duran "6. Statik kapsam boşluklarını kapatacak yeni kurallar" maddesi (`CSS-ACC-001`, `CSS-LAYOUT-001`, `CSS-LAYOUT-002`, `CPP-PERF-002`, `CPP-PERF-003`, `CPP-PERF-004`, `C-BUF-002`, `CS-ALLOC-001`) Faz H1'de (`faz/h-kurallar`) zaten uygulanmış ve katalogda yer alıyordu.
- **Eylem:** `KALAN_ISLER.md` üzerinde madde `[x]` olarak işaretlendi ve durumu kayda geçirildi.

### B. Faz F/G Küçük Açıkları (KALAN_ISLER.md İş 9) — ✅ Tamamlandı
1. **Model Adı Doğrulaması:**
   - `src/codementor/desktop/services.py:36` `OLLAMA_MODEL_RE` regex'i `^[A-Za-z0-9][A-Za-z0-9._:/-]*$` olarak sıkılaştırıldı.
   - Artık `/x`, `../x`, `-flag`, `.hidden` gibi baş karakteri alfanümerik olmayan modeller reddedilir.
   - `tests/desktop/test_connections.py` parametreli testine bu vakalar eklendi.
2. **`run_ollama_pull` Eksik Dalların Test Edilmesi:**
   - `result.error` ("İndirme başlatılamadı: ...") ve `result.timed_out` ("İndirme zaman aşımına uğradı") dallarına Türkçe mesaj üreten birim testleri eklendi.
3. **`ollama pull` İptal Desteği (Cancellation):**
   - `run_ollama_pull` fonksiyonuna `cancel: threading.Event | None = None` parametresi eklendi; iptal durumunda `result.cancelled` yakalanıp Türkçe `PullOutcome(False, "İndirme iptal edildi.")` dönmesi sağlandı.
   - `ConnectionsController` (`src/codementor/desktop/connections_controller.py`) içine `_pull_cancellations` sözlüğü, `cancel_pull(name)` metodu ve `is_pulling` özelliği eklendi.
   - `pull_model` arka plan görevine `Cancellation` bağlandı.
   - `src/codementor/desktop/runtime.py` içindeki `confirm_close(app)` fonksiyonuna model indirmesi sürerken kapanma onayı istemesi (`app.connections.is_pulling`) entegre edildi.
   - Tüm senaryolar için testler eklendi (`tests/desktop/test_connections.py` 47 geçti, `tests/desktop/test_app.py` 253 geçti).

### C. Depolama Borcu (KALAN_ISLER.md İş 8) — ✅ Tamamlandı
1. **Eski SQLite Şeması Göçü (`OperationalError` Koruması):**
   - `src/codementor/storage/db.py` içinde `SCHEMA_DB_VERSION = 2` yapıldı.
   - `_migrate` fonksiyonuna `PRAGMA table_info(analyses)` ve `PRAGMA table_info(sessions)` kontrolleri eklendi. Eksik sütunlar varsa (`session_id`, `question_id`, `provider`, `model`, `early_exit`, `degraded`, `tokens_in`, `tokens_out`, `latency_ms`, `report_json`, `updated_at`) otomatik olarak `ALTER TABLE ADD COLUMN` ile eklenir.
2. **Bozuk `created_at` Toleransı:**
   - `src/codementor/storage/cache.py` içine `_list_analyses_fallback` eklendi.
   - SQLite tablosunda `created_at` alanında geçersiz ISO formatı veya bozuk metin olduğunda `list_analyses` ve `list_analyses_page` fonksiyonlarının çökmesi engellendi; bozuk satırlar güvenli şekilde `utcnow()` varsayılanına çekilir veya atlanır, geçerli kayıtlar kullanıcıya eksiksiz sunulur.
3. **Testler:**
   - `tests/unit/test_storage_migration.py` dosyası oluşturuldu (3 test: eski şema göçü, bozuk ISO tarihiyle `list_analyses` ve `list_analyses_page` kurtarması).
   - `tests/unit/test_storage.py` (49 test) ve `test_storage_migration.py` (3 test) tamamen yeşil.

### D. Dokümantasyon ve İlerleme Eşitlemesi (İş 6, 8, 9) — ✅ Tamamlandı
1. **`PROGRESS.md` Güncellemesi:**
   - `PROGRESS.md` dosyasına `## Kod + Depolama — KALAN_ISLER iş 6, 8 ve 9 (2026-10-20)` başlığı ve ayrıntılı yapılanlar özeti eklendi.
   - "Sonraya" bölümündeki Faz 49 Ü9 (eski şema göçü), Faz 49 `sessions` budama ve Faz F (F10 küçük açıkları) maddeleri üstü çizilerek kapatıldı.
2. **`docs/ZAYIF_VE_GELISTIRILECEK_YONLER.md` Eşitlemesi:**
   - Açık Sonraya madde sayısı 46'dan 43'e indirildi (120 toplam / 43 açık).
   - `tests/unit/test_release_readiness.py` çalıştırılarak metriklerin ve iddiaların tam eşleştiği kanıtlandı (15/15 yeşil).

### E. Veri Seti Sürümü, Yapısal Kategori Sınırı ve `RunConfig` (KALAN_ISLER.md İş 7) — ✅ Tamamlandı
1. **Veri Seti Sürümü (`dataset_version`):**
   - `src/codementor/eval/dataset.py` içine `dataset_version(target)` fonksiyonu eklendi: kimlik, kod (LF normalleştirilmiş) ve etiket JSON'u üzerinden `d1+<hash>` formatında deterministik SHA-256 özeti üretir.
   - `src/codementor/models/eval.py` içinde `RunConfig` modeline `dataset_version: str | None = None` alanı eklendi (eski sonuç dosyalarını kırmaz).
   - `src/codementor/eval/runner.py` içinde `run_eval` koşulurken `run_config`'e `dataset_version` bağlandı.
2. **Karşılaştırma ve Analiz Uyarıları (`compare`, `analyze`, `breakdown`):**
   - `src/codementor/eval/compare.py` `compare_table`: sürümler dipnotuna `veri seti d1+...` bilgisi eklendi; birden fazla farklı veri seti sürümü karşılaştırıldığında `⚠ Tabloda farklı veri seti sürümleri var; satırlar doğrudan kıyaslanamaz.` uyarısı basılır.
   - `src/codementor/cli/eval.py`: `_result_and_labels` içinde kayıtlı sonuçtaki `dataset_version` ile diskteki güncel etiketlerin sürümü karşılaştırılır; uyuşmazlık durumunda sarı uyarı basılarak eski koşuların farklı etiketlerle sessizce yeniden puanlanması engellenir.
3. **Yapısal Kategori Sınırı (`boundary:`):**
   - `ExpectedFinding` modeline `boundary: str | None = Field(default=None)` alanı eklendi.
   - `tests/unit/test_category_rules.py` içindeki `memory_boundary_violation` fonksiyonu yapısal `boundary` alanını serbest metin regex'inden önce öncelikli tanıyacak şekilde genişletildi.
   - `eval/dataset/dev/cpp-009/label.yaml` L6 ve L10 bulgularına `boundary: ownership_scope` eklendi.
4. **Testler ve Belge Sayıları:**
   - `tests/unit/eval/test_dataset_version.py` eklendi (8 test: determinizm, CRLF normalizasyonu, etiket/kod değişim duyarlılığı, compare dipnotu ve uyarısı, analyze uyuşmazlık uyarısı).
   - `src/` satır sayısı 27 500 sınırını aştığı (27 537) için `README.md` ve `docs/ZAYIF_VE_GELISTIRILECEK_YONLER.md` üzerindeki kaynak kodu iddiası `~28 bin satır kaynak` olarak güncellendi (`test_release_readiness.py` 15/15 yeşil).
   - Sonraya açık madde sayısı 43'ten 42'ye indirildi.

### F. Faz I Eval Altyapısı ve Ölçüm Doğruluğu (KALAN_ISLER.md İş 10) — ✅ Tamamlandı
1. **LLM-as-Judge ile Sokratik Kalite Skoru:**
   - `prompts/v1/judge.j2`: Sokratik rehberlik çıktısını (pedagojik değer 1-5, koda temas 1-5, Sokratik derinlik 1-5, doğrudan çözüm sızdırmama bool, genel puan 1.0-5.0) değerlendiren LLM yargıç prompt'u hazırlandı.
   - `src/codementor/models/eval.py`: `SocraticCriterionScore` ve `SocraticJudgeReport` Pydantic modelleri eklendi.
   - `src/codementor/eval/judge.py`: `evaluate_socratic_quality` (yapılandırılmış JSON çıktısı alan ve markdown kod bloklarını ayıklayan), `judge_run_result` ve `judge_summary_markdown` işlevleri yazıldı.
   - `src/codementor/cli/eval.py`: `codementor eval judge --run <path> --judge-provider <provider>` CLI alt komutu eklendi.
   - `tests/unit/eval/test_judge.py`: FakeProvider ile 7 birim testi yazılarak doğrulandı.
2. **Parçalı Koşu Determinizmi ve Kapsama:**
   - `src/codementor/eval/parts.py`: `part_signature(samples, parts)` fonksiyonu ile parça atamasının deterministik SHA-256 özeti üretildi; `check_parts_coverage(part_results, all_samples)` ile parçalı sonuçlardaki çakışan ve eksik örnekler tespit edildi.
   - `src/codementor/eval/compare.py`: Karşılaştırılan tüm sonuçlar parçalardan oluşuyorsa çakışan örnekler dipnot uyarısı olarak gösterildi.
   - `tests/unit/eval/test_parts.py`: 23 test ile determinizm ve kapsam kontrolü doğrulandı.
3. **Fewshot / Prompt Senkronizasyonu:**
   - `prompts/v1/fewshots/*.yaml` dosyalarında `additional_findings` altındaki eksik `certainty: high` alanları eklendi.
   - `tests/golden/prompts/` testleri çalıştırılarak anlık görüntüler güncellendi (10/10 yeşil).

### G. Deterministik Sokratik Kalite Kapısı ve Küçük Model Korumaları (KALAN_ISLER.md İş 11) — ✅ Tamamlandı
1. **Mimari Karar (ADR-0031):**
   - `docs/adr/0031-kucuk-modeller-icin-deterministik-sokratik-kalite-kapisi.md` yazılarak küçük modeller için deterministik kalite kapısı, karmaşıklık uzlaştırması ve sağduyu filtreleri kurala bağlandı.
2. **Yapılandırma:**
   - `src/codementor/config.py`: `PipelineSettings.model_profile` (`standard` / `small`) ve `PipelineSettings.verify_provider` alanları eklendi. `OllamaConfig.profile` eklendi.
3. **Sağduyu Denetimleri (`sanity.py`):**
   - `is_guard_hallucination`: Kanıt satırında `if(...)` kontrolü olan kodlarda modelin uydurduğu "kontrol edilmemiş/ele alınmamış" bulguları eler.
   - `apply_sanity_checks`: `small` model profilinde bulgu sayısını en kritik 3 bulguyla sınırlar (severity öncelikli).
4. **Karmaşıklık Politikası (`complexity_policy.py`):**
   - `apply_complexity_policy`: Statik analiz ipucu varken küçük model çeliştiğinde deterministik statik ipucunu korur.
5. **Sokratik Kalite Kapısı (`socratic_gate.py`):**
   - `jaccard_similarity` ve `deduplicate_questions` (eşik >= 0.70 soru tekilleştirme).
   - `has_repetition_loop`: 3+ ardışık n-gram döngü tespiti.
   - `touches_code`: Sorunun öğrenci koduna temas ettiğini doğrulama.
   - `evaluate_socratic_gate`: Sokratik kalite kapısı değerlendirmesi.
6. **Boru Hattı Dilimleme ve Sağlayıcı Yönlendirme:**
   - 400 satır kuralını aşmamak için `src/codementor/pipeline/socratic_pass.py` ayrıştırıldı.
   - `verify_provider` seçildiğinde Pass V doğrulamasının belirlenen doğrulayıcı sağlayıcı üzerinden yürütülmesi sağlandı (`orchestrator.py`, `verify_pass.py`, `llm_session.py`).
7. **Testler:**
   - `tests/unit/verify/test_sanity.py` (4 test).
   - `tests/unit/verify/test_complexity_policy.py` (3 test).
   - `tests/unit/verify/test_socratic_gate.py` (7 test).
   - `tests/integration/test_pipeline_small_model.py` (3 test).
   - Tam test süiti (3957 test) çalıştırılarak tüm sistem doğrulandı.

### H. Faz J Havuz Kod İşleri (KALAN_ISLER.md İş 12) — ✅ Tamamlandı
1. **`METHOD_LEAKS` ve Örnek Girdi/Çıktı Alanları:**
   - `src/codementor/models/questions.py`: `SampleIO` modeli eklendi (`input`, `output`, opsiyonel `explanation`); `QuestionPublic` ve `UserQuestionDraft` içine `sample_io: list[SampleIO]` bağlandı.
   - `Question` içine `method_leaks: list[str]` eklendi ve `MENTOR_FIELDS` kümesine alınarak öğrenciden/API'den gizlenmesi güvenceye alındı.
   - 64 sorunun tüm YAML dosyalarına gizli yöntem terimleri `method_leaks:` olarak taşındı; temsilci sorulara `sample_io:` alanları eklendi.
   - `tests/unit/test_question_data.py`: `q.method_leaks` doğrudan soru verisinden test edildi ve `sample_io` şema doğrulaması bağlandı (81/81 yeşil).
2. **Tier 0 Yalıtımında Sıcak İşçi Havuzu (Warm Worker Pool):**
   - `src/codementor/config.py`: `ValidationSettings.tier0_warm_workers: int = 0` ayarı eklendi.
   - `src/codementor/validation/tier0_worker.py`: `--pool` / `--loop` modu ile satır-sınırlı JSON akışıyla çalışan kalıcı işçi döngüsü eklendi.
   - `src/codementor/validation/tier0_pool.py`: `Tier0Worker` ve `Tier0WorkerPool` sınıfları yazılarak thread-safe havuz, çökme kurtarması ve zaman aşımı mekanizması kuruldu.
   - `src/codementor/validation/tier0_isolation.py`: `tier0_warm_workers > 0` iken sıcak havuz üzerinden çalıştırma sağlandı; `close_tier0_pool` eklendi.
   - `tests/unit/test_tier0_pool.py`: 5 birim testi yazıldı ve doğrulandı.
3. **Windows CI MinGW ve Clang Hedefi:**
   - `src/codementor/validation/toolchain.py`: Windows'ta keşfedilen `clang` ve `clang++` araçlarına `--target=x86_64-w64-mingw32` bayrağı eklendi.
   - `.github/workflows/ci.yml`: Windows CI adımına derleyici ısınma komutu bağlandı.
4. **Zig Budama (J2) Spec ve Betiği:**
   - `src/codementor/validation/toolchain_prune.py` ve `tools/prune_zig.py`: Zig kurulumundan yabancı platform/mimari libc başlıklarını budayan motor ve CLI aracı yazıldı.
   - `tests/unit/test_toolchain_prune.py`: 5 birim testi yazıldı.
   - `.github/workflows/ci.yml`: Linux CI adımında zig kurulumundan sonra otomatik budama adımı bağlandı.

---

## 4. Doğrulama Komutları ve Sonuçları

- `uv run ruff check .` → ✅ All checks passed!
- `uv run ruff format --check .` → ✅ 498 files already formatted.
- `uv run mypy src/` → ✅ Success: no issues found in 223 source files.
- `uv run pytest tests/unit/test_question_data.py tests/unit/test_tier0_pool.py tests/unit/test_toolchain_prune.py tests/unit/test_toolchain.py tests/unit/test_tier0_isolation.py` → ✅ 142 passed, 1 skipped.
- `uv run pytest tests/unit/test_release_readiness.py` → ✅ 15 passed.

### I. Doküman Tutarlılık Turu (KALAN_ISLER.md İş 13) — ✅ Tamamlandı
1. **Yol Haritası ve ADR Eşitlemesi:**
   - `docs/UYGULAMA_PLANI.md`: Faz A'dan Faz K'ya kadar tüm fazların güncel tamamlanma durumları yol haritası tablosuna işlendi.
   - `docs/mimari.md` §20: 31 ADR'nin tamamının eşleştiği doğrulandı (0 eksik).
2. **Kural Kataloğu Eşitlemesi:**
   - `docs/rules-catalog.md` ↔ `src/codementor/rules/`: 33 kuralın tamamının birebir eşleştiği betikle kanıtlandı (0 eksik, 0 fazla).
3. **Geliştirme Günlüğü Dizini:**
   - `docs/gelistirme-gunlugu/README.md`: Yeni teslim raporları, güncellemeler ve eval rehberi eklendi.
4. **`KALAN_ISLER.md` Bölüm A:**
   - Tüm otomatik ajan görevleri (İş 1 - 13) tamamlandı ve `[x]` olarak işaretlendi.

---

## 4. Doğrulama Komutları ve Sonuçları

- `uv run ruff check .` → ✅ All checks passed!
- `uv run ruff format --check .` → ✅ 498 files already formatted.
- `uv run mypy src/` → ✅ Success: no issues found in 223 source files.
- `uv run pytest tests/unit/test_question_data.py tests/unit/test_tier0_pool.py tests/unit/test_toolchain_prune.py tests/unit/test_toolchain.py tests/unit/test_tier0_isolation.py` → ✅ 142 passed, 1 skipped.
- `uv run pytest tests/unit/test_release_readiness.py` → ✅ 15 passed.

---

## 5. Sonuç ve Kullanıcıya Notlar

**`KALAN_ISLER.md` Bölüm A kapsamındaki tüm 13 ajan işi başarıyla tamamlanmıştır.**  
Sırada yalnızca kullanıcının veya canlı ortamın yapabileceği adımlar bulunmaktadır:
- **U1:** `git push` (`main` dalı yerel commit'lerini GitHub'a gönderme)
- **U2:** Y2 — referans çözüm karşılaştırması (`private/` repo dışı inceleme)
- **U3:** P13 — GitHub repo ayarları (secret scanning, Dependabot)
- **U4:** `v0.1.1` etiketi ve release
- **U5:** Canlı sağlayıcı/model ölçümleri ve elle masaüstü denemeleri
