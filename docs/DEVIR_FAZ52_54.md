# Devir: Faz 52, 53, 54 (başka bir ajana)

Bu belge Faz 52-54'ü uygulayacak ajan içindir. Claude Code işi sonra test edip denetleyecek.
Önce `AGENTS.md`'yi oku; oradaki altın kurallar bu belgeden önce gelir. Ayrıntılı faz tanımları
`docs/UYGULAMA_PLANI.md` içinde ("### Faz 52", "### Faz 53", "### Faz 54").

## 0. Başlangıç durumu ve genel kurallar

- **Dal:** Her şey `faz/51-kategori` (origin'de, `e981ae2`) üzerine kurulu. Faz 47-51 bu dalda;
  `main` 22 commit geride. Her fazı bir öncekinin üstünde kendi dalında yap:
  `faz/51-kategori` → `faz/52-kural-oneri` → `faz/53-olcum-belge` → `faz/54-bolme`.
- **Doğrulama:** Her fazın sonunda şunlar yeşil olmalı (Windows'ta `make` yok, tek tek koş):
  `uv run ruff check .` · `uv run ruff format --check .` · `uv run mypy src/` ·
  `uv run pytest -m "not live"` (bugün 2888 geçiyor, 14 atlanıyor).
- **Testler ağa çıkamaz:** `tests/conftest.py` loopback dışı bağlantıyı engeller (Faz 50).
- **Yapma:**
  - Canlı LLM eval'i (`eval run` sağlayıcıyla) koşma; token harcar, kullanıcı onayı gerekir.
    Statik koşular (`--static-only`) serbest.
  - `main`'e birleştirme ve `git push` yapma; kullanıcı ve Claude karar verir.
  - Test setindeki (`eval/dataset/test/`) etiketleri kullanıcı onayı olmadan değiştirme.
  - Commit mesajına AI/Claude/Codex atıf satırı (Co-Authored-By vb.) ekleme.
  - 400 satırı aşan yeni dosya yaratma.
- **Commit:** Conventional commit, fazın plandaki mesajıyla. Faz başına bir commit; denetim
  düzeltmesi gerekirse ikinci commit.
- **Belgeler:** Her faz sonunda `docs/UYGULAMA_PLANI.md` bölümünü "(YAPILDI tarih)" ve `[x]` yap;
  `PROGRESS.md`'ye "## Faz N — Notlar" bölümü ekle (Yapılanlar / Alınan kararlar / Açık sorular),
  durum tablosuna satır ekle, "Kaldığımız yer" satırını güncelle.
- **Bitince:** §4'teki teslim raporunu yaz.

## 1. Faz 52 — Kural bazında öneri türü

**Neden:** Statik bulgular bugün hep `kind = issue`. Bazı kurallar gerçek hata değil, iyi uygulama
işaret ediyor ve eval'de yanlış alarm üretiyor. Faz 36 hata/öneri ayrımı: `docs/adr/0022-hata-oneri-ayrimi.md`.

**Yapılacaklar:**

1. **Kural meta verisi** (`src/codementor/rules/base.py`, `class Rule`): Sınıf özniteliği
   `default_kind: ClassVar[FindingKind] = FindingKind.ISSUE` ve kural içinden bulgu başına tür
   verilebilecek bir yol ekle (bulgu oluşturan yardımcıya `kind` parametresi ya da `kind_for(...)`
   kancası; mevcut kural kodlarına bakıp en az değişiklikli olanı seç). `RuleInfo`/katalog türü de
   göstersin (`docs/rules-catalog.md` üretiliyorsa yeniden üret: `make rules-doc` hedefine bak).
2. **Kurallar:**
   - `CPP-OWN-001` (`rules/cpp.py`): Aynı fonksiyonda eşleşen `delete`/`delete[]` varsa
     `suggestion` + `low` (akıllı işaretçi önerisi). Eşleşen `delete` yoksa `issue` kalır.
   - `UE-MEM-001` (`rules/unreal.py`, `Reserve` olmadan `TArray::Add`): `suggestion` + `low`.
   - `PY-RES-001` (`rules/python.py`, `with` dışı `open`): Aynı fonksiyonda `close()` varsa
     `suggestion`. Hiç kapatılmıyorsa `issue`.
3. **Birleştirme:** Aynı satırda statik öneri ve LLM hatası varsa sonuç **hata** olmalı.
   `src/codementor/verify/merge.py` (satır ~28) bunu yapıyor gibi; bir testle doğrula, eksikse düzelt.
   Öneriler puana girmez (`eval/metrics.py`, yalnız `kind = issue` puanlanır); Sokratik sorular
   yalnız hatalardan üretilir. Bunu bozma.
4. **Eval etiketleri:** Bu kuralların öneriye dönen bulguları için dev/test etiketlerini listele:
   - Faz 52 planındakiler: dev `cpp-105`, `unreal-107`, `python-105`.
   - Faz 51 denetiminden: CPP-OWN-001 ile `memory_safety` etiketli "çıplak new[]" bulguları
     (dev `cpp-009` L6, dev `cpp-105` L4/L8, test `cpp-006` L3/L12).

   Önerilen işlem: beklenen bulgudan çıkarıp `notes`'a taşıma (`docs/EVAL_ORNEK_REHBERI.md` §4.2).
   **Listeyi kullanıcıya sun, onay almadan değiştirme.** Test etiketi değişirse PROGRESS'e
   "test sonuçları bu örneklerde karşılaştırılamaz" notu düş.
5. **Statik eval'i yenile:** `uv run codementor eval run --split dev --static-only` ve
   `--split test --static-only`. README tabloları sonuç dosyalarından üretilir (bkz. Faz 53 §2).
   Bu fazda yeni statik sonuç dosyası ekliyorsan README'yi de yenile, yoksa
   `tests/unit/eval/test_readme_table.py` düşer.

**Testler (önce yaz):**
- Kural fixture'larında tür beklentisi: Eşleşen `delete` varken CPP-OWN-001 `suggestion`, yokken
  `issue`. UE-MEM-001 `suggestion`. PY-RES-001 `close()` var/yok. Mevcut kural testleri
  `tests/rules/` altında; kalıbı izle.
- Birleştirme: statik öneri + aynı satırda LLM hatası → tek bulgu, `issue`.
- Katalog/`RuleInfo` türü içeriyor.

**Kabul:** Yukarıdaki testler; `make check` eşdeğeri yeşil; etiket değişiklikleri yalnız onaylı olanlar.
**Commit:** `feat(faz-52): statik kurallarda öneri türü`

## 2. Faz 53 — Ölçüm altyapısı ve belge tazeleme

1. **Kapsama:**
   - `uv add --dev pytest-cov`.
   - CI'ın Linux pytest adımına (`.github/workflows/ci.yml`) şunu ekle:
     `--cov=codementor --cov-report=term-missing:skip-covered`.
   - **Eşik koyma** (yalnız rapor). Yerelde bir kez koşup toplam ve en düşük 5 modülün kapsamasını
     PROGRESS'e yaz; mimari §15 hedefleri (%95 / %90) ile kıyasla.
   - `tests/unit/test_packaging.py`'ye CI'da `--cov` olduğunu denetleyen bir test ekle
     (mevcut `test_ci_runs_pip_audit_and_npm_audit` kalıbı).
2. **README:**
   - "Eval sonuçları" girişini güncelle: veri seti **dev 96 / test 70**; dil başına örnek
     sayısını `eval/dataset/{dev,test}/` dizin adlarından say.
   - Eski "80 örnek, dev 31 / test 49" ifadeleri kalmasın.
   - Tablolar elle yazılmaz: `<!-- eval-table:...:start/end -->` blokları
     `codementor.eval.compare.compare_table` çıktısıdır. Seçim mantığı
     `tests/unit/eval/test_readme_table.py`'de; aynı seçimle üretip yapıştır.
   - Sağlayıcı notunda Claude ölçümleri ile Codex (`gpt-6-luna`) alternatifi ayrı yazılsın.
   - En güncel dev sonucu Faz 51: Claude 96 örnek **78 / 96 / 86** (P/R/F1). Ayrıntı `PROGRESS.md`
     "Faz 51 — Notlar".
3. **Statik koşular:** Faz 52'de yenilenmediyse dev ve test statik koşularını güncel etiketlerle
   yenile; README tablolarını üret.
4. **Birleştirme ve push:** Planda "`faz/36` dalının main'e birleştirilmesi" yazıyor; bu artık
   tüm zincir (`faz/36` … `faz/54`) demek. **Bunu yapma.** Yalnız PROGRESS'e "birleştirmeye
   hazır, kullanıcı onayı bekliyor" yaz. Claude test ettikten sonra kullanıcı karar verecek.

**Kabul:** CI'da kapsama raporu; README girişi güncel; README tablo testleri yeşil.
**Commit:** `chore(faz-53): kapsama ölçümü, README ve statik eval tazeleme`

## 3. Faz 54 — Büyük dosyaların bölünmesi

Davranış **değişmeden** 400 satırı aşan dört modülü böl. Güncel satır sayıları: `analysis/_loops.py` 449,
`analysis/extractor.py` 438, `desktop/app.py` 415, `providers/cli_agent.py` 403 (Faz 52-53 bunları
değiştirirse yeniden say).

1. **Önce öneri:** Her dosya için sorumluluk sınırlarını yaz, hangi fonksiyon/sınıf nereye taşınır,
   PROGRESS'e ekle. Örnek yönler, kodu okuyup karar ver:
   - `analysis/_loops.py`: Döngü sınırı sınıflandırması (bound/derinlik çıkarımı) ayrı modüle.
   - `analysis/extractor.py`: Bölüm kurucuları (`_section` ile çağrılanlar) ayrı modüle.
   - `providers/cli_agent.py`: CLI ortak yardımcıları (`render_prompt`, `profile_env`,
     `resolve_executable`, `.cmd` çözümleme, `short_error`, `agent_limits`) `providers/_cli_common.py`'ye.
   - `desktop/app.py`: Soru bankası/geçmiş işleyicileri ayrı bir denetleyiciye (`files.py`,
     `connections_controller.py` kalıbı).
2. **İçe aktarma yolları korunur:** Testler ve diğer modüller `from codementor.providers.cli_agent
   import render_prompt, short_error, agent_limits, CliTimeoutError, ...` gibi yolları kullanıyor.
   Eski modülden yeniden dışa aktar (`__all__` ya da açık import). Testleri değiştirme;
   değiştirmek zorunda kalırsan nedenini yaz.
3. **Monkeypatch tuzağı:** Bazı testler modül özniteliklerini yamalıyor (ör.
   `monkeypatch.setattr(orchestrator_module, "run_tier0", ...)`,
   `monkeypatch.setattr(analyze_module, "Orchestrator", ...)`). Taşınan bir fonksiyon başka modülden
   çağrılıyorsa yama artık etkisiz kalır. Testlerin hâlâ gerçekten sınadığından emin ol.
4. **Golden'lar aynı kalmalı:** `uv run pytest tests/golden` (`--update-golden` kullanma; gerekirse
   fark davranış değişikliğidir, dur ve raporla).
5. Tek sorumluluk, tip ipuçları, `mypy --strict`; yeni modüllere kısa modül docstring'i.

**Kabul:** 400 satırı aşan `src/` dosyası yok (`find src -name "*.py" | xargs wc -l`);
testler değişmeden ve golden'lar aynı geçer.
**Commit:** `refactor(faz-54): 400 satırı aşan modüllerin bölünmesi`

## 4. Teslim raporu (Claude'un test edeceği)

Her faz için kısa bir blok yaz (PROGRESS'e de girer):

- Dal adı ve commit kimliği.
- Değişen dosyalar listesi (`git diff --stat`).
- Dört doğrulama komutunun son satırları (geçen/atlanan test sayısı dahil).
- Kabul kriterlerinin her biri `[x]` ya da `[ ]` + neden.
- Kullanıcı onayı bekleyen kararlar (özellikle Faz 52 etiket listesi).
- Emin olmadığın ya da kapsam dışı bıraktığın her şey.

Claude teslimden sonra şunları yapacak:
- Her dalda dört komutu yeniden koşmak,
- `kod-denetci` ile mimari/test/güvenlik denetimi,
- Faz 54 için `git diff --stat` + golden ve içe aktarma kontrolü.
