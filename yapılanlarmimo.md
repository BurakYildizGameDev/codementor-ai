# Yapılanlar (mimo) — CodeMentor AI, Faz 52–54 (2026-10-05)
> **Not:** Bu belge ana özet. Mimari ağırlıklı ek: `mimoyapılanlar.md` (bağımlılık
> diyagramı §4.2, tasarım kararları §4.3).

Bu belge, Faz 52–54 boyunca yapılan işlerin tek yerde kaydıdır. Ayrıntılı teknik devir
notları: `devirfaz52-54yapılanlar.md`; faz faz tarihçe: `PROGRESS.md`.
Çalışma dalı: `faz/53-54-kapsama-bolumleme`, taban: `main` @ `90f1795`.

---

## 1. Ne yapıldı (özet)

| Faz | İş | Durum | Commit |
|---|---|---|---|
| 52 | Statik kurallarda öneri türü (ADR-0022'nin açık maddesi) | ✅ | `90f1795` |
| 53 | Ölçüm altyapısı (pytest-cov, CI) + belge tazeleme | ✅ | `a911a71` |
| 54 | 400 satırı aşan 4 modülün bölünmesi (davranış değişmeden) | ✅ | `ede397f` |

## 2. Faz 52 — Kural bazında öneri türü

Statik kurallara (CPP-OWN-001, UE-MEM-001, PY-RES-001 vb.) öneri türü eklendi;
öneri/engelleme ayrımı ADR-0022 açık maddesini kapattı. Ayrık commit: `90f1795`.

## 3. Faz 53 — Ölçüm altyapısı ve belge tazeleme

- `pytest-cov` eklendi (`pyproject.toml` + `uv.lock`); CI Linux adımı `--cov` ile
  kapsama raporu basar.
- **Kapsama: %96** (2933 test, 13.516 deyim; `src/` 3.782 satır). `<100%` hedefi korundu.
- README eval tabloları 166 örneklik güncel etiketle tazelendi (dev 96: 78/96/86;
  test 70: 63/52/61) — `eval compare` çıktıları `eval/results/` ile birebir.
- Flakli eşik testleri iki yönlü sağlandı: çıplak koşuda 31 test / 1,62 s (sert eşikler),
  `--cov` koşusunda 31 / 3,50 s. `_deadline()` yardımcısı `coverage.Coverage.current()`
  sinyali varsa ×4 tolerans uyguladı; makine hızından bağımsız.
- `tests/unit/test_packaging.py` güncellendi; `.gitignore`'a kapsama artıkları eklendi.

## 4. Faz 54 — Büyük dosyaların bölünmesi

400 satırı aşan 4 modül, **hiçbir davranış değişikliği olmadan** bölündü. Gerçek ölçüm:

| Modül | Önce | Sonra | Taşınan | Yeni dosya |
|---|---|---|---|---|
| `analysis/_loops.py` | 449 | **276** | Döngü sınıflandırma (`LoopShape`, `AssignmentIndex`, `classify`, `_python_iteration`, `_binary_search`, `_from_counter`, `_has_halving`, ...) | `_loop_bounds.py` (214) |
| `analysis/extractor.py` | 438 | **398** | Desen tabloları (`_USING_STD`, `_USING_LINQ`, `_STRING_TYPES`, `_TYPE_DECLARATIONS`), tip kısayolları, modül yardımcıları (`_name`, `_start`, `_leftmost_operand`, `_MAX_CHAIN`), 5 uyarı sabiti | `_extractor_sections.py` (71) |
| `desktop/app.py` | 415 | **395** | Soru sorguları (`questions_for`, `filtered`), soruya başlama, örnek yükleme, ipucu merdiveni sıfırlama + yeni oturum | `questions_controller.py` (73) |
| `providers/cli_agent.py` | 403 | **333** | Sabitler, `CliTimeoutError`, `resolve_executable`, `profile_env`, `render_prompt`, `short_error`, `agent_limits` | `_cli_common.py` (123) |

**Korunan hassas yüzeyler:**
- `App.questions_for` / `_filtered_questions` aynı adlarla sarmalayıcı kaldı ve gövdeleri
  yalnız `self.core`'a dokunuyor — `test_app_logging.py` bu yöntemleri Tk'sız, yalnız
  `core` alanlı nesneyle çağırıyor (maymun-yaması yüzeyi kırılmadı).
- `cli_agent.py` `__all__` ile açık yeniden dışa aktarım yapıyor: `ruff` kullanılmayan
  sembolü silmek (F401) isterken `mypy --strict` tanımsız adı (F822) reddediyor;
  `codex_cli.py` ve testlerin gördüğü adlar korundu.

**DEVİR belgesinden kasıtlı sapmalar (3 adet, gerekçeli):**
1. `_extractor_sections` bölüm-kurucu fonksiyonlar değil desen+yardımcı modülü oldu —
   gerçek kod sınıf tabanlı (`_Extractor`), sınıfı dağıtmak riskliydi.
2. `build_argv` fonksiyon değil **method** olarak kaldı — gövde kullanıcı kodunu metin/
   yorum olarak işletiyor (§12 güven yorumu), yer değişikliği sözleşmeye dokunurdu.
3. `__all__` re-export planda yoktu; iki lint aracı arasındaki boşluk için eklendi.

## 5. Doğrulama kanıtları (nihai tur, sıfır hata)

| Denetim | Sonuç |
|---|---|
| `uv run pytest -m "not live"` (tam paket) | **2933 passed, 14 skipped, 6 deselected** (94,86 s) — `FAILED/ERROR` taraması boş |
| Bölünmüş modüllerin dilimleri | **208 passed** (3,79 s) |
| Prompt + golden + mentor şablonları | **145 passed** (2,66 s) |
| Desktop (`test_app.py` + `test_app_logging.py`) | 34 + 1 passed |
| `uv run mypy src/` (--strict) | **Success** — 194 dosya |
| `uv run ruff check .` + `ruff format --check .` | Temiz — 407 dosya formatlı |
| Import duman testi | `App` delegate yüzeyi ve `cli_agent` re-export'ları yerinde |
| ≤400 satır kuralı | En büyük `src/` dosyası **398** ✓ |

Notlar: `14 skipped` platforma bağlı (POSIX rlimit, gcc/clang/dotnet yoksa atlanan
`compiler` testleri — ADR-0009); `6 deselected` `@pytest.mark.live` ağ testleri, plan
gereği koşulmaz.

## 6. Commit'ler (tek dal, ayrık sorumluluk)

```
ede397f refactor(faz-54): 400 satırı aşan 4 modülün bölünmesi   (10 dosya)
a911a71 chore(faz-53): pytest-cov, CI kapsama adımı ve belge tazeleme (7 dosya)
90f1795 feat(faz-52): statik kurallarda öneri türü
```

Yeni dosyalar: `analysis/_loop_bounds.py`, `analysis/_extractor_sections.py`,
`desktop/questions_controller.py`, `providers/_cli_common.py`,
`devirfaz52-54yapılanlar.md` (bu belge commit'lerden sonra yazıldı, henüz commit'lenmedi).

## 7. Kasıtlı olarak yapılmayanlar

- **`faz/36` dalının `main`'e birleştirilmesi** (Faz 53 plan maddesinin son parçası):
  birleştirme kararı kullanıcıda; kasıtlı olarak dokunulmadı (`PROGRESS.md` madde 26'da
  "kısmen yapıldı" işaretli).
- Sınırın altındaki dosyalara (`pipeline/orchestrator.py` 395, `views/analyze_view.py`
  391) "erken bölme" yapılmadı — kural 2 gereği faz kapsamına sadık kalındı.

## 8. Sıradaki işler (PROGRESS.md plan maddeleri 28–30)

28. Faz 55 — Tier 0 ayrıştırma ve maskeleme sağlamlığı (süre sınırı, raw string, D2).
29. Faz 56 — HTML-STD-003 kenar durumları.
30. Faz 57 — C-MEM-003 akış sıralı null denetimi.

---

*Özet: 3 faz eksiksiz, davranış korunarak; 2933 test yeşil, mypy strict temiz, tüm
`src/` dosyaları ≤ 400 satır. Eline sağlık. 🎉*