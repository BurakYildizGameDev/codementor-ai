# Faz 52–54 Yapılanlar — Ek Devir Raporu (2026-10-05)

Bu belge `devirfaz52.md`'yi değiştirmez; yanına eklenen "ne yapıldı" raporudur.
Dal: `faz/53-54-kapsama-bolumleme`. Üzerine inşa: `main` @ `90f1795` (Faz 52).

## 1. Durum tablosu

| Faz | İş | Durum | Kanıt |
|---|---|---|---|
| 52 | Kural bazında öneri türü | ✅ commit `90f1795` | ADR-0022 açık maddesi kapandı; öneri eşiği |
| 53 | Ölçüm altyapısı + belge tazeleme | ✅ tamam (kısmen: `faz/36` birleştirmesi açık) | Kapsama **%96**, CI `--cov` adımı, README 166 örnek |
| 54 | Büyük dosyaların bölünmesi | ✅ tamam | Tüm `src/` dosyaları ≤ 400 satır, davranış değişmedi |

**Genel doğrulama (nihai):**
- `uv run pytest -m "not live"` → **2933 passed, 14 skipped, 6 deselected** (6 = `live` işaretli, plan gereği)
- `uv run mypy src/` → Success, 194 dosya (`--strict`)
- `uv run ruff check .` / `ruff format --check .` → temiz
- Masaüstü yüzeyi: `tests/desktop/test_app.py` 34 passed, `test_app_logging.py` 1 passed

## 2. Faz 53 — Kapsama kanıtı ve flake

- Komut: `uv run pytest -m "not live" --cov=codementor --cov-branch --cov-report=term-missing:skip-covered`
- Sonuç: **%96** (2933 test, 13.516 deyim; `src/` 3.782 satır). `<100%` hedefi korundu (Aİ kararına uygun).
- Flake kanıtı (iki yönlü):
  - Çıplak koşu: `tests/unit/test_facts_review.py` 31 test / **1,62 s** (sert eşikler `benchmark_below_thousands_ms` vb.)
  - `--cov` koşusu: aynı 31 test / **3,50 s** → `_deadline()` yardımcısı `coverage.Coverage.current()` varsa ×4 tolerans uyguladı ve testler yeşil kaldı.
- CI: Linux adımına `--cov` ile raporlama; Windows/macOS iş akışları etkilenmedi.
- `.gitignore`: `.coverage`, `coverage.xml`, `htmlcov/`, `cov-*.txt` vb. artıkları eklendi.

## 3. Faz 54 — Bölünmeler (öncesi → sonrası, gerçek ölçüm)

| Modül | Önce | Sonra | Taşınan |
|---|---|---|---|
| `analysis/_loops.py` | 449 | **276** (+`_loop_bounds.py` **214**) | Döngü sınıflandırma: `LoopShape`, `AssignmentIndex`, `classify`/`_classify`, `_python_iteration`, `_binary_search`, `_from_counter`, `_has_halving`, `_comparisons`, `_initial_value` |
| `analysis/extractor.py` | 438 | **398** (+`_extractor_sections.py` **71**) | Desen tabloları (`_USING_STD`, `_USING_LINQ`, `_STRING_TYPES`, `_TYPE_DECLARATIONS`), tip kısayolları, modül yardımcıları (`_name`, `_start`, `_leftmost_operand`, `_MAX_CHAIN`), 5 uyarı sabiti |
| `desktop/app.py` | 415 | **395** (+`questions_controller.py` **73**) | Soru sorguları (`questions_for`, `filtered`), soruya başlama, örnek yükleme, ipucu merdiveni sıfırlama + yeni oturum |
| `providers/cli_agent.py` | 403 | **333** (+`_cli_common.py` **123**) | Sabitler (`FIXED_SYSTEM`, `MEMORY_MB`, `MAX_PROCESSES`, `FILE_SIZE_BYTES`), `CliTimeoutError`, `resolve_executable`/`_candidates`, `profile_env`, `render_prompt`, `short_error`, `agent_limits` |

Davranış güvencesi: bölünmüş dosyalardan geçen test dilimleri yeşil (providers 62, extraction 178, desktop 35); tam paket 2933 yeşil. `App.questions_for`/`_filtered_questions`/`start_question`/`export`/`restart`/`_new_session` sınıf yöntemi olarak kaldı (maymun-yaması yüzeyi korundu).

## 4. DEVİR belgesinden sapmalar (gerekçeli)

1. **`_extractor_sections.py` bölüm kurucu değil, desen+yardımcı modülü.** DEVİR `_function`/`_loops`/`_call` tarzı bağımsız bölüm-kurucu fonksiyonlar varsayıyordu; gerçek `extractor.py` sınıf tabanlı (`class _Extractor`) ve durum `self` üzerinde taşınıyor. Sınıfı dağıtmak davranış riski büyüktü; sınıftan bağımsız sabitler/yardımcılar taşındı, sınıf gövdesi yerinde kaldı.
2. **`build_argv` metod olarak kaldı** (DEVİR'de fonksiyon sanılmış). Gövde kullanıcı kodunu yorum/metin olarak işletmeye devam ediyor (§12 "güvenilmeyen veri" yorumu); yer değiştirmesi sözleşme değişikliği sayılabilir, kasıtlı olarak dokunulmadı.
3. **`cli_agent.py` `__all__` ile yeniden dışa aktarım yapıyor** (planda yoktu). `ruff` F401 kullanılmayan sembolü silmek isterken `mypy --strict` F822 ile reddediyor; `codex_cli.py`/testlerin gördüğü adlar korunsun diye açık re-export tercih edildi.

## 5. Açık işler

- `faz/36` dalının `main`'e birleştirilmesi (Faz 53 plan maddesinin son parçası) — kullanıcı kararı bekliyor.
- Derleyici testleri `@pytest.mark.compiler` işaretli; gcc/clang/dotnet olmayan ortamlarda atlanır (ADR-0009 gereği).

## 6. Commit planı (bu dalda)

1. `chore(faz-53): pytest-cov, CI kapsama adımı ve belge tazeleme` — `pyproject.toml`, `uv.lock`, `.github/workflows/ci.yml`, `README.md`, `tests/unit/test_packaging.py`, `tests/unit/test_facts_review.py`, `.gitignore`
2. `refactor(faz-54): 400 satırı aşan modüllerin bölünmesi` — 8 kaynak dosya + `PROGRESS.md` + bu belge

Conventional commit mesajları hazır; birleştirme kararı kullanıcıya aittir.