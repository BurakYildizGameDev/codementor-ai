# Devir: Faz 60, 61, 62 (başka bir ajana)

**Hazırlayan:** Claude Code, 2026-10-06 · **Uygulayacak:** GLM (Cline) · **Denetleyecek:** Claude Code
**Bağlam:** [docs/GUNCELLEMELER.md](../GUNCELLEMELER.md) (kullanıcı testlerinden çıkan bulgular ve kanıtları)

Bu belge üç fazı adım adım anlatır: hangi dosya, hangi fonksiyon, hangi test. Belgede olmayan
bir karar gerekirse **DUR ve kullanıcıya sor**; kendi başına mimari karar verme.

---

## Önce bunu oku: önceki devirden dersler (Faz 55)

Faz 55'te teslim iyiydi ama denetimde şu hatalar çıktı. Bu kez yapma:

1. **Mutlu yol testi yetmez.** Faz 55'te yeni `;` ipucu `if (x)` sonrasında da çıkıyordu; çünkü
   yalnız "çalıştığı" vakalar test edilmişti. Bu belgede her faz için **zorunlu olumsuz testler**
   listelendi; hepsini yaz. Ayrıca kendine sor: "Bu değişiklik nerede yanlış davranır?" ve en
   az bir vaka daha ekle.
2. **Belgeye doğrulamadığın iddia yazma.** Faz 55 notlarında testin tersini söyleyen bir cümle
   ve gerçekte var olmayan bir kod yapısı anlatılmıştı. PROGRESS'e yazdığın her cümleyi kodla
   ve test çıktısıyla karşılaştır.
3. **Söylenmeyen kapsam değişikliği yapma.** Mevcut bir fonksiyonun davranışını değiştirdiysen
   PROGRESS'e açıkça yaz.
4. **Mevcut testleri gevşetme.** Bu belgede "değişmesi beklenir" diye listelenmeyen bir mevcut
   test kırılırsa, testi değil kodu düzelt. Listelenen bir test değişirse PROGRESS'te gerekçesini
   yaz. Denetimde `git diff main...HEAD -- tests/` ile kontrol edilecek.
5. **Repoya artık bırakma.** Ölçüm/deneme betikleri repo dışında (`%TEMP%`). Kök dizine
   `*Yapilanlar.md` gibi özet dosyası yazma; tek kayıt yeri `PROGRESS.md`.
6. **`eval run` koşarsan** `eval/results/` altına dosya yazar ve README tablo testini kırar;
   bu fazlarda eval koşman gerekmiyor.

## Genel kurallar

- `AGENTS.md` ve `CLAUDE.md` geçerli. Python 3.12, `mypy --strict`, ruff. Pydantic modelleri
  yalnız `src/codementor/models/` altında. Kullanıcıya dönük mesajlar Türkçe.
- Her faz **ayrı dalda**, sırayla: `faz/60-surum-uyumu` (main'den), `faz/61-ipucu-merdiveni`
  (60'ın üstünden), `faz/62-gecmis-silme` (61'in üstünden).
- Her fazın sonunda dört komut yeşil olmalı:
  ```bash
  uv run ruff check . && uv run ruff format --check .
  uv run mypy src/
  uv run pytest -m "not live"
  ```
- Commit mesajı: `feat(faz-N): ...` ya da `fix(faz-N): ...`. **Commit'e "Co-Authored-By" ya da
  "Generated with" satırı ekleme.** Push etme, main'e birleştirme (denetimden sonra yapılacak).
- Her faz sonunda `PROGRESS.md`'de: durum tablosuna satır, "## Faz N — Notlar" bölümü
  (Yapılanlar / Alınan kararlar / Değiştirilen mevcut testler ve neden / Doğrulama çıktısı),
  `docs/GUNCELLEMELER.md`'deki ilgili kutuları [x] yap.

---

## Faz 60 — Sürüm bilgisi ve geçmiş uyumu

**Dal:** `faz/60-surum-uyumu` · **Neden:** Kullanıcı 1 Ekim'de derlenmiş (34 faz eski) bir exe ile
test etti ve bunu fark edemedi. Ayrıca farklı sürümün kaydettiği rapor geçmişten açılınca
yanıltıcı "Bu analiz artık bulunamıyor" mesajı çıkıyor.

> Not: GUNCELLEMELER.md'deki "referans çözüm uyarısı" maddesi **zaten çözülmüş** (Faz 31,
> `pipeline/stages.py` `load_reference`: dosya yoksa `log.debug`). Logdaki uyarı eski exe'dendi.
> Bu maddeyi kodlama; GUNCELLEMELER.md'de "Faz 31'de çözülmüştü" diye işaretle.

### 60.1 Derleme bilgisi modeli

- `src/codementor/models/build.py` (yeni) içine:
  ```python
  class BuildInfo(StrictModel):
      version: str  # codementor.__version__
      commit: str | None  # kısa git özeti; bilinmiyorsa None
      built_at: datetime | None  # exe derleme zamanı (UTC); kaynaktan çalışırken None
      source: Literal["exe", "kaynak"]
  ```
  `StrictModel` için mevcut modellerin içe aktarma biçimine bak (`models/_base.py`).

### 60.2 Derleme bilgisini okuma

- `src/codementor/buildinfo.py` (yeni) içine `build_info() -> BuildInfo`:
  - `resource_path("data/build_info.json")` (bkz. `paths.py`) varsa onu okur → `source="exe"`.
  - Yoksa `source="kaynak"`, `version=__version__`, `commit=None`, `built_at=None`.
    Çalışma anında `git` çağırma (exe'de git yok; kaynakta gereksiz alt süreç).
  - Dosya bozuksa çökme: kaynak modundaki değeri döndür ve `log.warning("build_info_unreadable")`.
  - `functools.lru_cache` ile bir kez okunsun.
- Kısa gösterim için `def describe(info: BuildInfo) -> str`:
  `"0.1.0 · a1b2c3d · 06.10.2026"` (exe), `"0.1.0 · kaynaktan"` (kaynak).

### 60.3 Exe derlemesi bilgiyi yazsın

- `build_exe.py`:
  - Derlemeden önce `build/build_info.json` yaz (repo `data/`'sına yazma; `build/` zaten
    git dışı mı kontrol et, değilse `.gitignore`'a bak):
    `{"version": __version__, "commit": <git rev-parse --short HEAD ya da null>,
    "built_at": <UTC ISO>, "source": "exe"}`.
    `git` yoksa ya da hata verirse `commit` null olsun, derleme durmasın.
  - `pyinstaller_args` içinde mevcut `--add-data` kalıbıyla bu dosyayı pakette
    `data/build_info.json` olarak ekle (satır ~164'teki döngüye bak).
- `tests/desktop/test_build_exe.py`'deki kalıpla test: argümanlarda `build_info.json`'ın
  `data/` hedefiyle eklendiği; git yokken (`subprocess` hatası taklit) `commit=None` yazıldığı.

### 60.4 Sürümü göster

- **CLI:** `src/codementor/cli/main.py` satır ~26: `codementor --version` çıktısı
  `codementor 0.1.0 (kaynaktan)` ya da `codementor 0.1.0 (a1b2c3d, 2026-10-06, exe)`.
  Bu satırı denetleyen mevcut bir test varsa (`grep -rn "__version__\|--version" tests/`) yeni
  biçime göre güncelle ve PROGRESS'e yaz.
- **Masaüstü:** `desktop/widgets/sidebar.py` (`Sidebar`): alt kısımda, sağlayıcı rozetinin
  altına küçük, soluk bir etiket: `describe(build_info())`. Ayrıca Bağlantılar ekranında
  (`desktop/views/` altında settings/connections görünümü) "Sürüm: ..." satırı.
- **API:** `/health` zaten `version` döndürüyor (`models/api.py` `Health`); dokunma (şema
  değişikliği bu fazın kapsamı dışında).

### 60.5 Geçmişte uyumsuz rapor

Bugün: `desktop/app.py` `open_history` → `storage/cache.py` `get_analysis` → `_decode` uyumsuz
raporda `None` döndürür → "Bu analiz artık bulunamıyor." toast'ı (yanlış: kayıt var, okunamıyor).

- `storage/cache.py`'ye `get_row(db, analysis_id) -> AnalysisRow | None` ekle (yalnız satır).
- `open_history`'yi şöyle değiştir:
  1. `report = get_analysis(...)`; `report` varsa bugünkü davranış.
  2. `report is None` ise `row = get_row(...)`:
     - `row is None` → "Bu analiz artık bulunamıyor." (bugünkü mesaj).
     - `row` var → kodu yine aç: `runtime.load_source(analysis_id, ...)`; dil/motor/soruyu
       `row.language`, `row.engine`, `row.question_id`'den seç (`view.select(...)`; dil/motor
       değeri `Language(...)`/`Engine(...)` ile dönüştürülemezse dokunma); sonuç alanını temizle
       (`view.reset_results()`) ve toast:
       "Bu rapor farklı bir CodeMentor sürümüyle oluşturulduğu için gösterilemiyor. Kodu
       editöre açtım; yeniden denetleyebilirsin."
- API (`GET /v1/analyses/{id}`) davranışı değişmez (404).

### 60.6 Exe'yi yeniden derle ve elle doğrula (kod değil, kontrol)

```bash
uv run python build_exe.py --both
```
Sonra `dist/CodeMentor.exe`'yi aç ve PROGRESS'e işaretle: sol altta sürüm + commit görünüyor;
Soru bankası 64 görev; geçmişte eski bir rapor açılınca yeni mesaj. `dist/` commit'lenmez.

### Faz 60 testleri (hepsi zorunlu)

| Test | Dosya |
|---|---|
| `build_info()` dosya varken exe bilgisini, yokken kaynak bilgisini döndürür | `tests/unit/test_buildinfo.py` (yeni) |
| **Olumsuz:** bozuk JSON, eksik alan, `version` dışında tip → çökmez, kaynak bilgisi + uyarı | aynı |
| `describe()` iki biçim | aynı |
| `build_exe` argümanları `data/build_info.json`'ı içerir; git hatasında `commit=None` | `tests/desktop/test_build_exe.py` |
| CLI `--version` iki biçim | mevcut CLI test dosyası |
| `open_history`: kayıt yok → eski mesaj; **kayıt var ama rapor uyumsuz** → kod açılır, yeni mesaj, sonuç alanı temiz | `tests/desktop/test_app.py` (mevcut kalıplara bak) |
| **Olumsuz:** uyumsuz kaydın kodu da yoksa (`load_source` None) → "kod saklanmamış" metni, çökme yok | aynı |
| **Olumsuz:** satırdaki dil değeri geçersizse dil seçimi değişmez, çökme yok | aynı |

**Commit:** `feat(faz-60): sürüm bilgisi ve sürümler arası geçmiş uyumu`

---

## Faz 61 — İpucu merdiveni yalnız sayılan denemelerle ilerlesin

**Dal:** `faz/61-ipucu-merdiveni` · **Neden (kanıt):** Kullanıcının oturumunda başarısız bir
Antigravity denemesi (rapor `degraded`, "Model kullanılamadı") ipucu seviyesini 2 → 3 yaptı;
Claude'un ilk gerçek analizi bile en açık ipucuyla geldi. Erken çıkışlar da (sözdizimi hatası)
seviyeyi ilerletiyordu.

### Kullanıcının onayladığı kararlar (değiştirme)

- **K1:** LLM sonucu olmadan dönen analiz (`report.meta.degraded == True`: sağlayıcı yok/hata,
  zaman aşımı, şema iki denemede tutmadı) ipucu merdivenini **ilerletmez**.
- **K2:** Sözdizimi hatasıyla erken çıkış (`report.meta.early_exit == True`) merdiveni
  **ilerletmez**.
- **K3:** Masaüstünde **"Bir ipucu daha"** her zaman ilerletir. **"Denetle"**, kod son analizdekiyle
  birebir aynıysa (ör. yalnız model değiştirildi) ilerletmez; kod değiştiyse ilerletir.

Bunları **ADR-0026** olarak yaz: `docs/adr/0026-ipucu-merdiveni-sayilan-denemeler.md`
(biçim için `docs/adr/0025-tier0-alt-surec.md`'ye bak; Bağlam / Karar / Sonuçlar).

### Bugünkü akış (oku, anla)

- `pipeline/orchestrator.py` `_traced`: analiz başında `sessions.reserve_attempt` (atomik +1).
  İstisna/iptal olursa `_release` → `sessions.release_attempt` (sayaç hâlâ o denemedeyse −1).
- `_run_attempt`: `mentoring_profile(difficulty, run.attempt)` ile ipucu seviyesi; rapor
  kaydedilince `sessions.record_attempt` (sayaç ve seviye `max` ile yazılır).
- `prompts/mentoring.py` `mentoring_profile`: seviye = `min(3, başlangıç + attempt − 1)`.
- `storage/sessions.py`: `next_attempt`, `reserve_attempt`, `release_attempt`, `record_attempt`.

### 61.1 K1 + K2: sayılmayan denemeyi geri ver

`_run_attempt`'te rapor kaydedildikten sonra (`cache.save_analysis` ve `run.saved = True`
satırlarından sonra):

```python
counts = not report.meta.early_exit and not report.meta.degraded
if counts:
    sessions.record_attempt(...)  # bugünkü çağrı
else:
    sessions.release_attempt(self.db, request.session_id, request.question_id, run.attempt)
```

- Analiz kaydı **silinmez**; yalnız merdiven geri alınır. `_traced`'deki "kayıt yazıldıysa
  deneme geri alınmaz" yorumu artık yalnız istisnalar için geçerli; yorumu buna göre düzelt.
- Önbellekten dönen rapor (`from_cache`) da aynı kurala uyar (önbellek bozulmuş raporu zaten
  döndürmez; erken çıkış raporu dönebilir → sayılmaz).
- `sessions.py` modül docstring'ine K1/K2'yi bir cümleyle ekle.

### 61.2 K3 için istek seçeneği

- `models/request.py` `AnalysisOptions`'a:
  ```python
  advance_hint: bool | None = Field(
      default=None,
      description="False: bu gönderim ipucu merdivenini ilerletmez (aynı kodu yeniden "
      "denetlemek, model değiştirmek); None/True: ilerletir",
  )
  ```
- `orchestrator._traced`: `request.options.advance_hint is False` ise **ayırma yapma**:
  ```python
  current = sessions.next_attempt(self.db, sid, qid) - 1  # sayılmış son deneme
  run.attempt = max(1, current)
  run.advance = False  # _Run'a alan ekle (varsayılan True)
  ```
  `run.advance` False iken 61.1'de ne `record_attempt` ne `release_attempt` çağrılır;
  istisna yolunda da `_release` çağrılmaz (ayrılmış deneme yok).
- Önbellek anahtarı ipucu seviyesini zaten içeriyor (`cache_key(... hint_level ...)`); dokunma.
- Bu bir **public şema değişikliği**: şemaları ve web tiplerini yeniden üret:
  ```bash
  uv run codementor schema export --out schemas/
  make web-types        # make yoksa Makefile'daki komutu doğrudan çalıştır
  ```
  Şema anlık görüntü testleri kırılırsa üretilen dosyalarla güncelle (elle düzenleme yok) ve
  PROGRESS'e yaz. `cd web && npm run build` (ya da `make web-test`) yeşil kalmalı.

### 61.3 Masaüstü

- `desktop/app.py` `analyze()` imzası: `analyze(self, *, advance: bool | None = None)`.
  `AnalysisRequest(..., options=AnalysisOptions(advance_hint=advance))`.
- **"Bir ipucu daha"**: `desktop/widgets/socratic_card.py` satır ~100 düğmesi
  `self._on_next_hint`'i çağırıyor; zincirin sonunda `app.analyze(advance=True)` çağrılsın
  (zinciri `grep -rn "_on_next_hint\|next_hint" src/codementor/desktop` ile izle).
- **"Denetle"** (`analyze_view.py` `_run_or_stop` → `actions.analyze()`): `app.analyze()`
  içinde karar ver:
  ```python
  if advance is None and code == self._last_code and <aynı soru> and self._last_counted:
      advance = False
  ```
  `self._last_counted`: son raporun `not early_exit and not degraded` olup olmadığı;
  `_on_analyze` (rapor gelince) içinde güncelle. Soru değiştiyse ya da ilk analizse `None`.
- "Baştan başla" (`restart`) davranışı değişmez.

### Faz 61 testleri (hepsi zorunlu)

| Test | Dosya |
|---|---|
| Başarılı analiz: sayaç +1, sonraki gönderimde seviye artar (mevcut test korunur) | `tests/integration/test_pipeline.py` |
| **Olumsuz (K1):** sağlayıcı hatası (FakeProvider `ProviderError` fırlatır) → rapor `degraded`, kayıt var, sayaç değişmez, sonraki başarılı gönderim **aynı** seviyede | `tests/integration/test_pipeline_sessions.py` |
| **Olumsuz (K1):** analiz süre sınırı aşımı (`pipeline.analysis_timeout_s` çok küçük) → sayaç değişmez | aynı |
| **Olumsuz (K1):** şema onarımı tükendi (FakeProvider iki kez bozuk JSON) → sayaç değişmez | aynı |
| **Olumsuz (K2):** sözdizimi hatası (erken çıkış) → sayaç değişmez; düzeltilmiş kodla ilk gönderim seviye 1 | aynı |
| `advance_hint=False`: sayaç ve seviye değişmez; oturum hiç yokken seviye 1 ve sayaç 0 kalır | aynı |
| **Olumsuz:** `advance_hint=False` + iptal → `release_attempt` çağrılmaz (sayaç bozulmaz) | aynı |
| Eşzamanlı iki gönderim (mevcut `test_concurrent_submissions_get_attempts_1_and_2`) hâlâ geçer | mevcut |
| Masaüstü: "Bir ipucu daha" → `advance_hint=True`; aynı kodla "Denetle" (son analiz sayılmışsa) → `False`; kod değişince → `None`; son analiz degraded ise aynı kodla "Denetle" → `None` | `tests/desktop/test_app.py` |
| API: `options.advance_hint` kabul edilir; bilinmeyen alan hâlâ 422 | `tests/api/` (mevcut istek testlerinin yanına) |

**Değişmesi beklenebilecek mevcut testler:** erken çıkışın ya da bozulmuş raporun merdiveni
ilerlettiğini varsayan testler (`grep -rn "hint_level\|attempt" tests/integration tests/api
tests/desktop`). Değiştirdiğin her testi PROGRESS'te gerekçesiyle listele.

**Commit:** `fix(faz-61): ipucu merdiveni yalnız sayılan denemelerle ilerler`

---

## Faz 62 — Geçmişi silme

**Dal:** `faz/62-gecmis-silme` · **Neden:** Kullanıcı isteği. Analizler `~/.codementor/codementor.db`
(`analyses` tablosu), analiz edilen kod `~/.codementor/desktop-sources/<id>.txt` olarak duruyor;
silme hiçbir katmanda yok. Bu bir gizlilik özelliği: silinen şey gerçekten silinmeli.

### Kararlar

- **Tek analiz silme:** analiz satırı + o analizin kod dosyası. İpucu merdivenine (`sessions`)
  dokunmaz.
- **Tüm geçmişi temizle:** tüm `analyses` satırları + tüm `desktop-sources/*.txt` + tüm
  `sessions` satırları (ipucu ilerlemesi de geçmiştir). Onay ister.
- **API:** yalnız tek silme: `DELETE /v1/analyses/{analysis_id}`. Toplu silme API'ye
  **eklenmez** (yanlışlıkla tüm verinin silinmesi riski; masaüstüne özgü).
- **Web:** web arayüzünde geçmiş ekranı yok; web'e bir şey eklenmez.

### 62.1 Depolama

`storage/cache.py`:
```python
def delete_analysis(db: Database, analysis_id: str) -> bool:
    """Analizi siler; vardıysa True."""


def clear_analyses(db: Database) -> int:
    """Tüm analizleri siler; silinen sayı."""
```
`storage/sessions.py`:
```python
def clear_sessions(db: Database) -> int:
```
Var olan `delete(...)` kullanımına bak (`save_analysis` içindeki budama, `sqlmodel.delete`).

### 62.2 Kod dosyaları

`desktop/runtime.py` (`load_source`'un yanına):
```python
def delete_source(analysis_id: str, directory: Path | None = None) -> None:
def clear_sources(directory: Path | None = None) -> int:
```
- `delete_source`: `load_source`'taki gibi `analysis_id.isalnum()` değilse hiçbir şey yapma
  (yol aşımı koruması). `OSError` yut (dosya zaten yok olabilir).
- `clear_sources`: yalnız `SOURCES_DIR` içindeki `*.txt` dosyalarını siler; klasördeki başka
  dosyalara ve klasörün dışına dokunmaz.

### 62.3 Masaüstü

- `desktop/views/history_view.py` `HistoryView`:
  - Kurucuya `on_delete: Callable[[str], None]` ve `on_clear: Callable[[], None]` ekle.
  - Başlığın sağına **"Tümünü temizle"** düğmesi (liste boşken devre dışı).
  - Her satırın sağına küçük **"Sil"** düğmesi. Satıra tıklama (`open_row`) satırdaki bütün
    widget'lara bağlı (satır ~108); sil düğmesine tıklamak **analizi açmamalı**: düğmeyi
    `<Button-1>` bağlamasının dışında tut.
- `desktop/app.py`:
  - `delete_history(analysis_id)`: `delete_analysis` + `runtime.delete_source(...,
    self.prefs_dir)` → listeyi yenile → toast "Analiz silindi." Ekranda o analiz açıksa sonuç
    alanını temizle (`view.reset_results()`); bunun için açık analizin kimliğini tut
    (`open_history` ve `_on_analyze`'da `self._shown_analysis_id`).
  - `clear_history()`: onay (`tkinter.messagebox.askyesno`, metin: "Tüm analiz geçmişi, saklanan
    kodlar ve ipucu ilerlemen silinecek. Emin misin?"). Testte taklit edilebilsin diye onay
    fonksiyonunu enjekte edilebilir yap (ör. `self.confirm = messagebox.askyesno`). Onaylanırsa
    `clear_analyses` + `clear_sessions` + `runtime.clear_sources(self.prefs_dir)`, sonuç
    alanını temizle, toast "Geçmiş temizlendi (N analiz)."
  - `HistoryView`'ı oluşturduğun yerde iki geri çağrıyı bağla.

### 62.4 API

`api/routes.py`:
```python
@router.delete(
    "/v1/analyses/{analysis_id}", status_code=204,
    responses=_problems(404), tags=["analiz"],
)
def delete_stored(request: Request, analysis_id: str) -> Response:
```
- Kimlik `_stored`'daki gibi `ULID_PATTERN` ile denetlensin; biçim bozuksa veritabanına gitmeden
  404 (varlığı sızdırmama kuralı, Faz 27).
- API anahtarı tanımlıysa `/v1/` öneki zaten korumalı (`api/auth.py` `PROTECTED_PREFIX`); ek iş
  yok ama test et.
- `api/app.py` satır ~49: CORS `allow_methods=["GET", "POST"]` → `"DELETE"` ekle.
- API kod dosyası yazmıyor (masaüstüne özgü); API'de silme yalnız veritabanı satırıdır.

### 62.5 Belgeler

- README "Masaüstü uygulaması" → **Geçmiş** maddesine: "tek tek ya da tümü silinebilir
  (saklanan kod ve ipucu ilerlemesi dahil)".
- `docs/mimari.md` §11 (depolama) ve API uç listesi varsa `DELETE` satırı.

### Faz 62 testleri (hepsi zorunlu)

| Test | Dosya |
|---|---|
| `delete_analysis` var olanı siler (True), sonra `get_analysis` None | `tests/unit/test_storage.py` |
| **Olumsuz:** olmayan kimlik → False, başka kayıt etkilenmez | aynı |
| **Olumsuz:** silinen analiz önbellekten dönmez (`find_cached` None) | aynı |
| `clear_analyses` + `clear_sessions` sayıları doğru; sonrasında yeni analiz normal kaydedilir | aynı |
| **Olumsuz:** tek silme `sessions`'a dokunmaz | aynı |
| `delete_source`/`clear_sources`: yalnız ilgili `.txt`; **olumsuz:** `"../x"`, `"a/b"` kimliği hiçbir şey silmez; klasördeki `.txt` olmayan dosya ve klasör dışı dosya kalır | `tests/desktop/test_runtime.py` |
| Masaüstü: satır silme listeyi yeniler; açık analiz silinince sonuç alanı temizlenir; "Tümünü temizle" onaylanmazsa **hiçbir şey silinmez**, onaylanırsa üçü de silinir | `tests/desktop/test_app.py` |
| **Olumsuz:** Sil düğmesine tıklamak analizi açmaz | `tests/desktop/` (görünüm testi; mevcut görünüm test kalıbına bak) |
| API: `DELETE` 204, ardından `GET` 404; olmayan → 404; bozuk kimlik → 404 (DB'ye gitmeden) | `tests/api/test_storage_api.py` |
| **Olumsuz:** API anahtarı tanımlıyken anahtarsız `DELETE` → 401; CORS ön kontrolünde `DELETE` izinli | `tests/api/` (mevcut anahtar testlerinin yanına) |

**Commit:** `feat(faz-62): geçmişi ve saklanan kodu silme`

---

## Teslim

Üç faz bitince:
1. Üç dal, her birinde faz commit'i; dört komut yeşil (çıktıları PROGRESS'e yapıştır).
2. `PROGRESS.md` ve `docs/GUNCELLEMELER.md` güncel; ADR-0026 yazılmış.
3. `git diff main...HEAD -- tests/` çıktısını gözden geçir: listelenmeyen bir test değiştiyse
   neden değiştiğini PROGRESS'e yaz.
4. Kullanıcıya "Claude Code denetimine hazır" de. Push etme.
