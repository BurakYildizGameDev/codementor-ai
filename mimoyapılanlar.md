# Yapılanlar — Faz 52–54 (CodeMentor AI, 2026-10-05)

> **Not:** Ana özet `yapılanlarmimo.md`'dedir; bu belge onun mimari ağırlıklı
> eki/çapraz okumasıdır (bağımlılık diyagramı §4.2, tasarım kararları §4.3 için bkz.).

> Tek belgedeki özet. Ayrıntılar: `PROGRESS.md` (faz notları), `devirfaz52-54yapılanlar.md`
> (devir ek raporu), `devirfaz52.md` (bir sonraki modele devir). Dal: `faz/53-54-kapsama-bolumleme`.
> Üzerine inşa edilen: `main` @ `90f1795` (Faz 52).

## 1. Özet tablo

| Faz | İş | Durum | Commit |
|---|---|---|---|
| Faz 52 | Statik kurallarda öneri türü (ADR-0022 açık maddesi) | ✅ | `90f1795` |
| Faz 53 | Ölçüm altyapısı: `pytest-cov`, CI kapsama, belge tazeleme | ✅ | `a911a71` |
| Faz 54 | 400 satırı aşan 4 modülün bölünmesi (davranış değişmeden) | ✅ | `ede397f` |

---

## 2. Faz 52 — Statik kurallarda öneri türü

- Kurallara **öneri türü** kazandırıldı (`CPP-OWN-001`, `UE-MEM-001`, `PY-RES-001` vb.);
  öneri eşleştirme sonuçları (`eval`) tek etiket şemasına bağlandı.
- ADR-0022'nin açık maddesi kapandı; README eval girişleri güncellendi.
- Doğrulama: tam paket yeşil; eval raporu `eval/results/` ile README birebir tutuldu.

## 3. Faz 53 — Ölçüm altyapısı ve belge tazeleme

| İş | Ayrıntı |
|---|---|
| `pytest-cov` | `pyproject.toml` + `uv.lock`; `--cov=codementor --cov-branch` |
| CI | Linux adımında kapsama raporu; Windows/macOS etkilenmedi |
| Kapsama | **%96** (2933 test, 13.516 deyim; `src/` 3.782 satır) — `<100%` hedefi korundu |
| README | 166 örneklik güncel etiketle tazelendi (dev 96: 78/96/86; test 70: 63/52/61) |
| Flake fix | `tests/unit/test_facts_review.py` `_deadline()`: çıplak koşuda sert eşikler (31 test / 1,62 s), `--cov` koşusunda `coverage.Coverage.current()` varsa ×4 tolerans (31 test / 3,50 s) — iki yönlü doğrulandı |
| Hijyen | `.gitignore`'a `.coverage`, `coverage.xml`, `htmlcov/`, `cov-*.txt` artıkları |

**Karar:** Zaman toleransı makine hızına sabit çarpanla değil, `coverage.Coverage.current()`
gibi bağlamsal sinyalle verildi (enstrümantasyon süreleri 2-3× uzatıyor).

---

## 4. Faz 54 — Büyük dosyaların bölünmesi (mimari)

### 4.1 Bölünme tablosu (gerçek ölçüm)

| Modül | Önce | Sonra | Taşınan |
|---|---|---|---|
| `analysis/_loops.py` | 449 | **276** + `_loop_bounds.py` **214** | Döngü sınıflandırma: `LoopShape`, `AssignmentIndex`, `classify`/`_classify`, `_python_iteration`, `_binary_search`, `_from_counter`, `_has_halving`, `_comparisons`, `_initial_value` |
| `analysis/extractor.py` | 438 | **398** + `_extractor_sections.py` **71** | Desen tabloları (`_USING_STD`, `_USING_LINQ`, `_STRING_TYPES`, `_TYPE_DECLARATIONS`), tip kısayolları, modül yardımcıları (`_name`, `_start`, `_leftmost_operand`, `_MAX_CHAIN`), 5 uyarı sabiti |
| `desktop/app.py` | 415 | **395** + `questions_controller.py` **73** | Soru sorguları (`questions_for`, `filtered`), soruya başlama, örnek yükleme, ipucu merdiveni sıfırlama + yeni oturum |
| `providers/cli_agent.py` | 403 | **333** + `_cli_common.py` **123** | Sabitler (`FIXED_SYSTEM`, `MEMORY_MB`, `MAX_PROCESSES`, `FILE_SIZE_BYTES`), `CliTimeoutError`, `resolve_executable`/`_candidates`, `profile_env`, `render_prompt`, `short_error`, `agent_limits` |

Kural: tüm `src/` dosyaları ≤ 400 satır (en yükseği 398). Fasade'ler (`analysis/__init__.py`,
`providers` dışa aktarımları) değişmedi — kullanıcı görünen API sabit.

### 4.2 Bağımlılık yönü (sonrası)

```
analysis/extraction.py ─▶ extractor.py ─▶ _extractor_sections.py (desen + yardımcı)
                          _loops.py ─▶ _loop_bounds.py (sınıflandırma)

providers/codex_cli.py ─┐
providers/cli_agent.py ─┴─▶ _cli_common.py (sabit + exec + render)   [cli_agent __all__ ile re-export]

desktop/app.py (ince sarmalayıcılar) ─▶ questions_controller.py ─▶ runtime, viewmodel.SAMPLES
                                      (App'e geri bağ yalnız TYPE_CHECKING)
```

### 4.3 Tasarım kararları

1. **`App` sarmalayıcıları korundu** (zorunlu): `test_app_logging.py` `questions_for` /
   `_filtered_questions` yöntemlerini yalnız `core` alanı olan `SimpleNamespace` ile
   *bağımsız* çağırıyor → controller gövdeleri serbest fonksiyon (`core`/`app` parametreli),
   `App` yöntemleri aynı adlarla ince sarmalayıcı kaldı. Maymun-yaması yüzeyi değişmedi.
2. **`__all__` ile re-export** (`cli_agent`): `ruff` F401 kullanılmayan sembolü silmek
   isterken `mypy --strict` F822 ile reddediyor; `codex_cli.py`/testlerin gördüğü adlar
   korunsun diye açık re-export tercih edildi.
3. **DEVIR'dan sapmalar** (gerekçeli): `_extractor_sections` bağımsız bölüm-kurucu
   fonksiyonlar yerine desen tabloları + modül yardımcılarını aldı (kod sınıf tabanlı
   `_Extractor`, durum `self` üzerinde); `build_argv` metod olarak kaldı (kullanıcı kodu
   güvenilmeyen veri yorumu — mimari §12 — bozulmasın).

---

## 5. Doğrulama matrisi (nihai tur, sıfır hata)

| Denetim | Sonuç |
|---|---|
| Tam paket `pytest -m "not live"` | **2933 passed, 14 skipped, 6 deselected** (94,86 s); `FAILED/ERROR` taraması boş |
| Bölme dilimleri (extractor, loop_bounds, facts_review, python_facts, packaging, providers, app_logging) | **208 passed** |
| Prompt + golden + mentor şablonları | **145 passed** |
| Desktop yüzeyi | `test_app.py` 34 passed + `test_app_logging.py` 1 passed |
| `mypy src/` (`--strict`) | Success — 194 dosya |
| `ruff check .` + `ruff format --check .` | Temiz — 407 dosya formatlı |
| Import duman testi | `App` delegate yüzeyi ✅, `cli_agent` re-export yüzeyi ✅ |
| ≤400 satır | ✅ (max 398) |

`14 skipped` = platforma bağlı (POSIX rlimit; `compiler` testleri araç zinciri yoksa — ADR-0009).
`6 deselected` = `@pytest.mark.live` (ağ) testleri, plan gereği koşulmuyor.

## 6. Açık işler

- `faz/36` dalının `main`'e birleştirilmesi (Faz 53 plan maddesinin son parçası) — **kullanıcı kararı**.
- Derleyici testleri yalnız gcc/clang/dotnet olan ortamlarda koşar (ADR-0009).

## 7. Dosya haritası (yeni)

| Dosya | Satır | Rol |
|---|---|---|
| `src/codementor/analysis/_loop_bounds.py` | 214 | Döngü sınıflandırma |
| `src/codementor/analysis/_extractor_sections.py` | 71 | Olgu çıkarımı desen/yardımcıları |
| `src/codementor/desktop/questions_controller.py` | 73 | Soru oturumu davranışı |
| `src/codementor/providers/_cli_common.py` | 123 | CLI ortak sabit/exec/render |
| `devirfaz52-54yapılanlar.md` | — | Devir ek raporu |
| `mimoyapılanlar.md` | — | Bu belge |