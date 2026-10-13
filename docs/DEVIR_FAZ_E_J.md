# Devir belgesi — Faz E, F, G, H (+ isteğe bağlı J) · Antigravity için

> **Bu belge kimin için:** Antigravity (ya da başka bir kodlama ajanı).
> **Kim yazdı:** Claude Code, 2026-10-13. Durum: main = `3ef973c`, `v0.1.1` yayında, CI yeşil.
> **İşi bitirince:** Claude Code her şeyi tek tek denetleyecek (§12). Uydurma sayı yazma, yapmadığın
> şeye "yaptım" deme; önceki devirlerde bu oldu ve hepsi yakalandı.

---

## İçindekiler

0. [Önce bunu oku: 12 kural](#0-önce-bunu-oku-12-kural)
1. [Kurulum ve komutlar](#1-kurulum-ve-komutlar)
2. [Her faz için çalışma akışı (adım adım)](#2-her-faz-için-çalışma-akışı-adım-adım)
3. [Bilinen tuzaklar (bunlar bizi defalarca yaktı)](#3-bilinen-tuzaklar)
4. [Faz E — Web: geçmiş, silme, güvenlik başlıkları](#4-faz-e--web)
5. [Faz F — Masaüstü sağlamlık ve kullanılabilirlik](#5-faz-f--masaüstü)
6. [Faz G — Sağlayıcı sağlamlığı ve kod temizliği](#6-faz-g--sağlayıcı-ve-kod-temizliği)
7. [Faz H — Statik kurallar ve analiz doğruluğu](#7-faz-h--statik-kurallar)
8. [Faz I — YAPMA (kullanıcı kararı gerekiyor)](#8-faz-i--yapma)
9. [Faz J — İsteğe bağlı küçük işler](#9-faz-j--isteğe-bağlı)
10. [Kullanıcının kendi yapacakları (sen dokunma)](#10-kullanıcının-kendi-yapacakları)
11. [Teslim raporu şablonu](#11-teslim-raporu-şablonu)
12. [Claude Code'un denetimde bakacakları](#12-claude-codeun-denetimde-bakacakları)

**Önerilen sıra:** E → F → G → H. Her faz ayrı dal, ayrı commit. Bir faz bitmeden ötekine geçme.
Token/zaman biterse yarım fazı commit'leme; o fazın dalında bırak ve teslim raporuna "yarım" yaz.

---

## 0. Önce bunu oku: 12 kural

1. **`AGENTS.md`'yi baştan sona oku.** Oradaki kurallar bu belgenin üstündedir.
2. **`docs/mimari.md`'den sapma.** Sapman gerekiyorsa DUR, gerekçeyi teslim raporuna yaz, işi yapma.
   (Bu turda yeni ADR yazma; gerekiyorsa öneri olarak rapora yaz, Claude Code yazar.)
3. **main'e dokunma.** Birleştirme, `git push`, etiket (`git tag`) YOK. Hepsi yerel dallarda kalır.
4. **Her yeni davranış testle gelir.** "Bitti" demek için testin hem yeni kodla geçmesi hem de
   değişikliği geri alınca düşmesi gerekir (bkz. §2 adım 7).
5. **Testler ağa çıkmaz.** LLM çağıran her şey `FakeProvider` ile test edilir. Gerçek API ya da
   `claude`, `agy`, `codex`, `ollama` komutlarını ÇALIŞTIRMA (token harcar). Canlı deneme yok.
6. **Docker yok.** Hiçbir yerde Docker önerme ya da kullanma.
7. **Ollama kullanma.** Yerel model denemesi yok (Faz I bu yüzden bu devirde yok).
8. **Model adları, anahtarlar, URL'ler koda gömülmez;** `codementor.toml` / `config.py`'den gelir.
9. **Kullanıcı kodu güvenilmeyen veridir** (mimari §12): çalıştırılmaz, prompt'a veri olarak girer.
10. **Kullanıcıya dönük her metin Türkçe;** tanımlayıcılar İngilizce. Tüm fonksiyonlarda tip ipucu,
    `mypy --strict` geçmeli. Pydantic modelleri yalnız `src/codementor/models/` altında.
11. **400 satırı geçen dosyaya yeni kod ekleme**; önce böl (Faz F/G'de bölme işleri var).
12. **Commit mesajında Claude/AI atfı yok.** `Co-Authored-By`, "Generated with" satırı ekleme.
    Biçim: `feat(faz-e): ...`, `fix(faz-f): ...`.

---

## 1. Kurulum ve komutlar

Depo kökü: `C:\Users\Burak\Desktop\Application\CodeMentor AI`

```powershell
uv sync                                   # Python 3.12 bağımlılıkları
cd web; npm ci; cd ..                     # web (Faz E için)
```

**Denetimler (her commit'ten önce dördü de yeşil olmalı):**

```powershell
uv run ruff check .
uv run ruff format --check .
uv run mypy src/
uv run pytest -m "not live"               # ~2,5 dk, 3350+ test, ağa çıkmaz
```

**Web (Faz E'de ayrıca):**

```powershell
cd web
npm run typecheck
npm test                                  # Vitest
npm run build
npx playwright test                       # e2e (API taklit edilir)
cd ..
```

**Şema/tip üretimi** (bir Pydantic modeline alan ekledin ya da değiştirdiysen ZORUNLU):

```powershell
uv run codementor schema export --out schemas/
cd web; npm run gen:types; cd ..
```

Sonra `git diff schemas/ web/src/types/` ile değişikliği gör ve commit'e kat. CI, üretilen tiplerle
commit'tekiler farklıysa kırılır.

**Tek test dosyası çalıştırmak:** `uv run pytest -q tests/unit/test_storage.py`
**Bir testi isimle:** `uv run pytest -q -k "delete_all"`

---

## 2. Her faz için çalışma akışı (adım adım)

Her faz için bu 10 adımı sırayla uygula. Atlama.

1. **main'den dal aç:** `git switch main` → `git switch -c faz/e-web` (dal adları her fazın başında).
2. **Fazın bölümünü bu belgeden oku** (§4-§9). Her maddenin "Nerede / Ne yap / Test / Kabul" kısmı var.
3. **İlgili kodu bul:** satır numaraları kayabilir; her maddede `grep` ipucu var. Örn.
   `uv run python -c "import codementor"` çalışıyorsa ortam doğru demektir.
4. **Önce testi yaz** (mümkünse): testin eski kodla DÜŞTÜĞÜNÜ gör (`uv run pytest -q <dosya>`).
5. **Kodu yaz.** Küçük adımlarla; her maddeden sonra ilgili testleri koş.
6. **Dört denetimi koş** (§1). Kırmızı varsa düzelt; testi gevşetme, `skip` ekleme, eşiği büyütme.
7. **Mutasyon kontrolü:** düzeltmeyi geçici geri al (`git stash push -- <kaynak dosya>`), yeni testi
   koş → DÜŞMELİ. Sonra `git stash pop`. Düşmüyorsa test hiçbir şey ölçmüyor demektir; düzelt.
   (Dikkat: `stash` sonrası `pop`'u unutma; `git stash list` boş olmalı.)
8. **Belgeleri güncelle:**
   - `docs/BulgularVeDuzeltilecekler.md` §10'da o fazın maddesini `- [x]` yap, sonuna `— **Faz E**` yaz.
   - `PROGRESS.md`: "Durum" tablosuna satır ekle (`| E | ✅ | faz/e-web | <tarih> | Antigravity / — |`),
     "## Faz A1 — Notlar"dan ÖNCE yeni bir "## Faz E — Notlar" bölümü: Yapılanlar / Kararlar /
     Doğrulama (gerçek test sayısı) / Açık kalanlar.
   - README'de anlatılan bir davranışı değiştirdiysen README'yi de güncelle.
9. **Commit:** `git add -A` → `git commit -m "feat(faz-e): web geçmişi, silme ve güvenlik başlıkları"`.
10. **Teslim raporuna yaz** (§11): bu fazın her maddesi için durum + kanıt.

---

## 3. Bilinen tuzaklar

Bunların her biri bu projede gerçekten oldu. Okumadan başlama.

### 3.1 Linux CI'da `tkinter` yok
- CI'daki Ubuntu Python'unda tkinter yok. `src/codementor/desktop/` altındaki bazı modüller
  (`questions_controller.py`, `runtime.py`, `viewmodel.py`, `config_writer.py`, `self_check.py`)
  tkinter'sız İÇE AKTARILABİLMELİ.
- Bu modüllerin EN ÜSTÜNE `customtkinter`, `tkinter` ya da `desktop/views/*`, `desktop/widgets/*`
  içe aktarması KOYMA. Gerekirse fonksiyonun içinde içe aktar (bkz. `questions_controller.open_add`).
- Bunu yakalayan test: `tests/unit/test_tkinter_free_imports.py`. Yeni bir tkinter'sız modül
  eklersen `MODULES` listesine ekle.
- Pencere açan testler (`tests/desktop/test_app.py` vb.) `tests/desktop/conftest.py`'deki
  `collect_ignore` listesinde olmalı. Yeni bir pencere testi dosyası eklersen oraya ekle.
- Yerelde Linux'u taklit etmek için: tkinter'ı engelleyen bir eklentiyle tüm testleri koş:
  ```powershell
  # scratch klasörüne block_tk.py: import sys; [sys.modules.__setitem__(n, None) for n in ("tkinter","customtkinter","_tkinter","tkinterdnd2")]
  $env:PYTHONPATH="<scratch klasörü>"; uv run pytest -p block_tk -m "not live" -q
  ```

### 3.2 Ortam değişkeni sızıntısı
- `desktop/runtime.writable_config_file()` `CODEMENTOR_CONFIG_FILE`'ı süreç ortamına yazar.
  `tests/conftest.py`'deki `_restore_config_env` her testten sonra geri alır. Testte ortam
  değişkeni değiştireceksen `monkeypatch.setenv/delenv` kullan, `os.environ[...] = ...` değil.
- Testler kullanıcının `~/.codementor` dizinine ASLA yazmamalı. `tests/conftest.py` toolchain,
  kullanıcı soruları ve kullanıcı toml'u için bunu zaten yalıtıyor; yeni bir `~/.codementor`
  yolu eklersen aynı deseni (`_default_*` fonksiyonu + autouse fikstür) uygula.

### 3.3 Windows'ta kaçış karakterleri bozuluyor
- Python kaynağına `\n`, `\t`, `\b`, `\u00ab` gibi kaçışları heredoc ya da betikle yazarken gerçek
  karaktere dönüşebiliyor (bir keresinde 13 regex'te `\b` görünmez backspace'e dönüştü).
- Dosya yazdıktan sonra görünmez karakter tara:
  ```powershell
  uv run python -I -c "import pathlib;[print(p) for p in pathlib.Path('src').rglob('*.py') if any((ord(c)<32 and c not in '\n') or ord(c) in (0xfeff,0x200b) for c in p.read_text(encoding='utf-8'))]"
  ```
  Çıktı boş olmalı (`tests/unit/test_normalize.py`'deki BOM bilinçli, ona dokunma).
- Görünmez/benzer karakter gerekiyorsa kaynağa `chr(0x...)` ile yaz (bkz. `prompts/templates.py`).

### 3.4 Regex: karesel/kübik süre (ReDoS)
- Kullanıcı kodu 40 KB'a kadar olabilir. `\s*X?\s*` gibi ardışık tekrarlar ve `^\s*` + `re.M`
  karesel olur. Yeni regex yazarsan 40 KB'lık kötü niyetli girdiyle süre testi ekle
  (`< 0.25 sn`). Örnek: `tests/unit/test_prompt_role_tags.py::test_guard_is_linear_on_adversarial_input`.
- Eski (yavaş) regex'le karşılaştırma testi koşarken zaman sınırı koy; felaket girdide saatlerce
  takılabiliyor.

### 3.5 Satır sınırı
- `desktop/app.py` ~505, `pipeline/orchestrator.py` ~460, `pipeline/passes.py` ~415 satır.
  Bunlara yeni özellik EKLEME; önce Faz F/G'deki bölme maddesini yap.

### 3.6 Golden testler
- `tests/golden/` çıktıyı birebir karşılaştırır. Bilinçli bir değişiklikse
  `uv run pytest --update-golden tests/golden` ile güncelle ve `git diff` ile değişikliği oku;
  rapora "golden şu yüzden değişti" yaz. Bilinçsiz değişiklikse kodunu düzelt.

### 3.7 Tek kaynaklı sürüm
- Sürüm yalnız `src/codementor/__init__.py`'de (`__version__`). pyproject'e `version =` ekleme.
  Sürümü sen DEĞİŞTİRME (yeni release Claude Code + kullanıcı kararı).

---

## 4. Faz E — Web

**Dal:** `faz/e-web` · **Commit:** `feat(faz-e): web geçmişi, silme ve güvenlik başlıkları`
**Neden:** README web'de geçmiş/silme varmış gibi anlatıyordu ama yoktu (bulgu O1). Ayrıca web'de
güvenilmeyen markdown ve eksik güvenlik başlıkları var (O15, O16).

Önce şu dosyaları oku (ne olduğunu anlamak için):
- `src/codementor/api/routes.py` (tüm uçlar; `DELETE /v1/analyses/{id}` zaten var — örnek al)
- `src/codementor/api/auth.py` (API anahtarı koruması)
- `src/codementor/storage/cache.py` (`list_analyses`, `delete_analysis`, `clear_analyses`)
- `src/codementor/storage/sessions.py` (`clear_sessions`)
- `web/src/api/client.ts`, `web/src/App.tsx`, `web/src/lib/markers.ts`, `web/index.html`
- `tests/api/test_storage_api.py` (API test deseni), `web/src/*.test.ts(x)` (Vitest deseni)

### E1 — `GET /v1/analyses` (sayfalı liste)
- **Nerede:** `api/routes.py`; yanıt modeli `models/api.py`'ye (Pydantic yalnız orada).
- **Ne yap:**
  1. `models/api.py`'ye `AnalysisSummary` (id, created_at, language, engine, question_id,
     provider, degraded, early_exit, tokens_in, tokens_out) ve `AnalysisPage`
     (`items: list[AnalysisSummary]`, `next_cursor: str | None`) ekle.
  2. `storage/cache.py`'ye `list_analyses_page(db, limit, before: str | None)` ekle:
     `created_at` azalan, eşitlikte `id` azalan; `before` verilirse o kimlikten eskileri döndür.
     `limit` 1-100 arası (dışı → 422).
  3. `GET /v1/analyses?limit=20&before=<id>` ucu. API anahtarı açıksa korumalı olmalı (mevcut
     `/v1/*` korumasını kullan, ayrı bir şey yazma).
  4. Rapor gövdesini (`report_json`) listede DÖNDÜRME (kod içerir; ayrıntı için mevcut
     `GET /v1/analyses/{id}` var).
- **Test (`tests/api/`):** boş liste; 3 kayıt → sıralama; `limit=2` → `next_cursor` dolu, ikinci
  sayfa kalan 1 kayıt; `limit=0` ve `limit=101` → 422; anahtar tanımlıyken başlıksız istek → 401.
- **Kabul:** yukarıdaki testler + `schemas/` ve `web/src/types` yeniden üretildi.

### E2 — `DELETE /v1/analyses` (toplu) ve `DELETE /v1/sessions/{id}`
- **Nerede:** `api/routes.py`, `storage/cache.clear_analyses`, `storage/sessions.clear_sessions`.
- **Ne yap:** toplu silme silinen sayıyı döner (`{"deleted": n}`); oturum silme o oturumun ipucu
  merdiveni kaydını siler. İkisi de API anahtarı açıksa korumalı. Başarısız/olmayan → 404 (oturum).
- **Test:** 2 analiz → toplu sil → liste boş, yanıt `deleted: 2`; anahtarlı modda başlıksız → 401;
  olmayan oturum → 404; oturum silinince aynı oturumla yeni analiz 1. denemeden başlar
  (`tests/integration/test_pipeline_sessions.py` desenini kullan).

### E3 — Web'de geçmiş paneli
- **Nerede:** `web/src/` (yeni bileşen, ör. `components/HistoryPanel.tsx`), `api/client.ts`.
- **Ne yap:** son analizlerin listesi (tarih, dil, soru, sağlayıcı, token), "daha fazla" ile sayfa;
  satıra tıklayınca raporu açar (`GET /v1/analyses/{id}`); satır başına "Sil"; "Tümünü temizle"
  (onay penceresi: `window.confirm` yeterli). Silinen rapor açıksa ekran temizlenir.
- **Test:** Vitest (bileşen: liste, sil, temizle onayı iptal/kabul) + Playwright e2e (API taklit:
  mevcut e2e dosyalarındaki `page.route` desenine bak).
- **Kabul:** `npm test`, `npm run typecheck`, `npx playwright test` yeşil.

### E4 — Web istemcisi `X-API-Key` gönderebilsin
- **Neden:** API anahtarı tanımlanırsa web şu an tamamen çalışmıyor.
- **Ne yap:** ayarlar alanında anahtar girişi; `sessionStorage`'da tut (localStorage değil);
  `api/client.ts` her istekte `X-API-Key` başlığı ekler. 401 gelirse "API anahtarı gerekli/yanlış"
  Türkçe mesajı göster.
- **Test:** Vitest: anahtar varken başlık gidiyor, yokken gitmiyor; 401 mesajı.

### E5 — O15: Monaco hover'da güvenilmeyen markdown
- **Nerede:** `web/src/lib/markers.ts` (`hoverMessage: { value }`, `f.description`, `d.message`).
- **Sorun:** LLM bulgu açıklaması ve derleyici iletisi markdown olarak işleniyor; `![](https://dış)`
  dış istek, `[x](https://phish)` tıklanabilir bağlantı üretir.
- **Ne yap:** markdown özel karakterlerini kaçışla: `\ * _ [ ] ( ) ! < > # + - . | \``. Ayrı bir
  `escapeMarkdown(text)` fonksiyonu yaz, `markers.ts` kullansın.
- **Test (Vitest):** `![x](http://e)` ve `[a](https://p)` içeren açıklama kaçışlanmış metin olarak
  çıkıyor (ham `](` kalmıyor); normal Türkçe metin değişmiyor.

### E6 — O16: güvenlik başlıkları
- **Web (`web/index.html`):** `<meta http-equiv="Content-Security-Policy" content="default-src 'self';
  img-src 'self' data:; worker-src 'self' blob:; style-src 'self' 'unsafe-inline';
  connect-src 'self' http://127.0.0.1:8000">`. Monaco çalışmaya devam etmeli (dev ve build).
  Monaco CDN'den yükleniyorsa ona göre izin ver; nereden yüklendiğine `grep -rn "monaco" web/src`
  ile bak. Çalışmadığını görürsen CSP'yi gevşetmek yerine nedenini rapora yaz.
- **API:** tüm yanıtlara `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`
  (FastAPI ara katmanı; `api/app.py`'deki mevcut ara katman desenini izle).
- **Test:** API testi başlıkların her yanıtta olduğunu doğrular (200 ve 404 dahil). Web için
  Playwright testi CSP meta etiketinin var olduğunu ve sayfanın konsolda CSP hatası vermeden
  yüklendiğini doğrular.

### E7 — D14: anahtar varken `/health/ready` korunur
- **Nerede:** `api/auth.py` (~satır 105), `providers/health.py`.
- **Sorun:** anahtar tanımlıyken bile `/health/ready`, `/docs`, `/openapi.json` açık; sağlayıcı/
  model adları, çalıştırılabilir yolları sızıyor.
- **Ne yap:** anahtar tanımlıysa `/health/ready`, `/docs`, `/redoc`, `/openapi.json` da anahtar
  ister. `/health` (yalnız "ayakta mı") açık kalır.
- **Test:** anahtarlı modda bu dört uç başlıksız 401, başlıklı 200; `/health` başlıksız 200;
  anahtarsız modda hepsi eskisi gibi.

### E8 — D15: Markdown dışa aktarımında kaçış
- **Nerede:** `src/codementor/report/markdown.py` (LLM metni ve derleyici iletisi ham yazılıyor;
  yalnız `|` kaçışlı).
- **Ne yap:** `< > &` karakterlerini `&lt; &gt; &amp;` yap (kod blokları ``` içindekiler HARİÇ;
  kod bloğunun içi olduğu gibi kalmalı). Tablo hücresindeki `|` kaçışı korunur.
- **Test:** `<script>alert(1)</script>` içeren açıklama Markdown'da `&lt;script&gt;`; kod bloğu
  içindeki `<stdio.h>` aynen kalıyor. Golden değişirse §3.6.

### E9 — D17: indirme URL'si gecikmeli iptal
- **Nerede:** `web/src/lib/download.ts` (~satır 10): `revokeObjectURL` `click()`'ten hemen sonra.
- **Ne yap:** `setTimeout(() => URL.revokeObjectURL(url), 0)` (ya da 1000 ms).
- **Test (Vitest):** sahte zamanlayıcıyla `revokeObjectURL`'ün tıklamadan sonra çağrıldığını doğrula.

### E10 — Soru filtresi boşsa mesaj
- Web'de soru seçicide filtre sonucu boşsa "Bu filtrelerle eşleşen soru yok." göster.
- **Test (Vitest).**

### E11 — Hız sınırı ve dışa açık `serve`
- **Ne yap:**
  1. `cli/serve.py`: `--host` `127.0.0.1`/`localhost`/`::1` DIŞINDA bir adresse ve API anahtarı
     tanımlı değilse başlamayı reddet: Türkçe mesaj + çıkış 3. `--insecure` bayrağı verilirse
     uyarıyla başlar.
  2. İstemci başına basit hız sınırı (bellek içi, IP başına dakikada N analiz;
     N `config.api.rate_limit_per_minute`, varsayılan 30, `None` = kapalı). Aşılırsa 429 +
     Türkçe mesaj. Config'e alan eklersen `codementor.toml`'a yorumlu satır ve `mimari.md` §17'ye
     bir satır ekle.
- **Test:** CLI: dışa açık host + anahtarsız → çıkış 3; `--insecure` ile başlama yolu (sunucuyu
  gerçekten başlatma; `uvicorn.run`'ı monkeypatch'le). API: sınır 2 iken 3. istek 429.

### E12 — CSRF `text/plain` regresyonu
- Tarayıcı `Content-Type: text/plain` ile basit POST atabilir. `POST /v1/analyze`'a
  `text/plain` gövdeyle istek → 415 ya da 422 olmalı (analiz başlamamalı). Bunu doğrulayan bir
  API testi ekle (kod değişikliği gerekmeyebilir; test yalnız davranışı sabitler).

**Faz E kabul:** E1-E12 testleri; web `typecheck/test/build/e2e`; Python dört denetim; `schemas/`
ve `web/src/types` güncel; README'nin Web bölümünde geçmiş/silme anlatılıyor.

---

## 5. Faz F — Masaüstü

**Dal:** `faz/f-masaustu` · **Commit:** `fix(faz-f): masaüstü sağlamlık ve kullanılabilirlik`

Önce oku: `desktop/launch.py`, `desktop/app.py`, `desktop/runtime.py`, `storage/db.py`,
`storage/cache.py`, `storage/sessions.py`, `desktop/views/history_view.py`,
`tests/desktop/test_app.py` (pencere test deseni: `_open` yardımcısı, `app` fikstürü).

### F0 — ÖNCE: `desktop/app.py`'yi böl (≈505 satır)
- **Ne yap:** davranışı DEĞİŞTİRMEDEN, ilgili yöntemleri mevcut controller desenine taşı
  (`questions_controller.py`, `connections_controller.py` örnek). Önerilen yeni modüller:
  `desktop/history_controller.py` (geçmiş aç/sil/temizle, dışa aktarma),
  `desktop/config_controller.py` (`write_config`, `reload_config`, `_locations`).
  `App`'te ince sarmalayıcılar kalsın (testler `app.write_config()` gibi çağırıyor).
- **Kabul:** `app.py` < 400 satır; `tests/desktop` hiç değişmeden geçiyor (`git diff tests/`
  boş olmalı). Yeni modüller tkinter'sız içe aktarılabiliyorsa `test_tkinter_free_imports.py`'ye ekle.

### F1 — O10: bozuk/kilitli veritabanında exe açılmıyor
- **Nerede:** `desktop/launch.py` (`state.database()` korumasız).
- **Ne yap:**
  1. `state.database()` istisnasını yakala → `messagebox.askyesno` ile Türkçe: "Veritabanı açılamadı
     (…). Yedekleyip yeni bir veritabanıyla başlansın mı?" Evet → dosyayı
     `codementor.db.bozuk-<tarih>` adıyla yeniden adlandır (silme!) ve yeniden aç. Hayır → çıkış 3.
  2. `App`'e `report_callback_exception` tanımla: istisnayı log'a yaz + toast ile "Beklenmeyen bir
     hata oldu; ayrıntı desktop.log'da" göster (uygulama kapanmasın).
- **Test:** pencere açmadan: bozuk DB dosyası (rastgele baytlar) + `messagebox`'ı monkeypatch'le
  (Evet) → yedek dosya oluştu, yeni DB açıldı; Hayır → `SystemExit(3)`.
  `report_callback_exception` için pencere testi (`tests/desktop/`): bir geri çağrıda istisna
  → toast metni.

### F2 — O13: dışa aktarma hatası sessiz
- **Nerede:** `desktop/app.py` dışa aktarma (~`write_text`; F0'dan sonra yeni controller'da).
- **Ne yap:** `OSError` yakala → toast: "Rapor kaydedilemedi: <neden>".
- **Test:** hedefi var olmayan bir dizinin altı yap (`tmp/dosya/alt/rapor.md`, `dosya` bir dosya)
  → toast'ta "kaydedilemedi".

### F3 — O14: "Geçmişi temizle" gizlilik
- **Nerede:** `storage/cache.clear_analyses`, `storage/db.py`, `desktop/runtime` (son dosyalar).
- **Ne yap:** veritabanı açılışında `PRAGMA secure_delete=ON`; `clear_analyses` sonrası `VACUUM`;
  masaüstü "Tümünü temizle" son dosyalar listesini (`prefs.recent_files`) de boşaltır.
  `~/.codementor/desktop-sources/` kod dosyaları zaten siliniyor mu kontrol et; silinmiyorsa sil.
- **Test:** temizlikten sonra DB dosyasının ham baytlarında daha önce kaydedilen kodun benzersiz
  bir dizesi YOK (`b"benzersiz_isaret_123" not in db_path.read_bytes()`); son dosyalar boş.

### F4 — D19: veritabanı sağlamlığı
- **Ne yap:**
  1. Bağlantı açılışında `PRAGMA journal_mode=WAL` ve `PRAGMA busy_timeout=5000`.
  2. Şema sürümü: `PRAGMA user_version`; 0 ise mevcut şemayı 1 yap; ileride göç için tek bir
     `_migrate(conn, from_version)` noktası. (Şimdilik göç yok, yalnız altyapı + test.)
  3. Analiz sürerken tekil "Sil" düğmesi devre dışı (toplu temizlik zaten engelli).
  4. Eski oturumları budama: `sessions` tablosunda `updated_at` 90 günden eskiler açılışta silinir
     (gün sayısı config'den: `storage.session_retention_days`, varsayılan 90, `None` = kapalı).
- **Test:** yeni DB'de `journal_mode` = `wal`, `user_version` = 1; 100 gün önceki oturum açılışta
  siliniyor, 10 gün önceki kalıyor; analiz sürerken sil düğmesi `disabled`.

### F5 — Ctrl+S kaydet, kaydedilmemiş değişiklik uyarısı
- **Ne yap:** editörde Ctrl+S → açık dosya varsa üzerine yazar, yoksa "Farklı kaydet". Dosya
  açma/bırakma/geçmişten açma/çıkışta kaydedilmemiş değişiklik varsa onay sorar (`app.confirm`).
- **Test (pencere):** düzenleme sonrası dosya açmaya kalkınca `confirm` çağrıldı; Hayır → mevcut
  metin korunur; Ctrl+S dosyaya yazar (`filedialog`'u monkeypatch'le).

### F6 — Geçmişte sayfalama ve arama
- Şu an `list_analyses` son 50. "Daha fazla yükle" + metin arama (soru kimliği/dil/sağlayıcı).
  E1'deki `list_analyses_page`'i yeniden kullan (Faz E önce yapıldıysa).
- **Test:** 60 kayıt → ilk sayfa 50, "daha fazla" ile 60; arama "c-medium" yalnız eşleşenler.

### F7 — Kapanırken onay
- Analiz ya da zig indirmesi sürerken pencere kapatılırsa "Analiz sürüyor, çıkılsın mı?" (`confirm`).
- **Test (pencere):** meşgulken `close()` → `confirm` çağrıldı; Hayır → pencere açık.

### F8 — Keyring'deki eski OpenAI/DeepSeek anahtarları
- **Nerede:** `desktop/connections.py` (`KeyStore`, `PROVIDERS`).
- Bağlantılar ekranında "Eski anahtarları temizle": `openai`, `deepseek` kayıtlarını keyring'den
  siler. **Test:** sahte `KeyStore` (mevcut testlerdeki `store` fikstürü) ile siliniyor.

### F9 — Kurulu zig eskiyse "güncelle" önerisi
- **Nerede:** `validation/toolchain_install.py` (`installed_zig`, kurulum işaretçisi),
  `codementor.toml` `validation.zig.sources` (sürüm burada).
- Kurulu sürüm yapılandırmadakinden farklıysa Bağlantılar'da "Zig güncellemesi var" + düğme.
- **Test:** sahte kurulum işaretçisi eski sürümle → `needs_update` True.

### F10 — Bağlantılar'da `ollama pull` düğmesi
- **DİKKAT:** Ollama kullanma (kural 7). Düğmeyi ekle ama testte `subprocess`'i monkeypatch'le;
  gerçekten çalıştırma. Komut yalnız config'deki modeli argüman olarak alır, kabuk kullanmaz
  (`run_process`/liste argv).

### F11 — SQLite çağrılarını iş parçacığına alma
- Masaüstünde geçmiş listeleme/silme ana Tk iş parçacığında. Uzun sürerse arayüz donar.
  `desktop/bridge.py`'deki arka plan deseniyle çalıştır, sonucu `after` ile arayüze ver.
- **Test:** listeleme çağrısının ana iş parçacığında OLMADIĞINI doğrula (`threading.current_thread()`).

### F12 — Linux/macOS'ta "Oturum aç"
- Şu an yalnız Windows konsolu açıyor. Linux'ta `x-terminal-emulator`/`gnome-terminal`, macOS'ta
  `open -a Terminal` ile; yoksa "Terminalde şu komutu çalıştırın: …" mesajı.
- **Test:** `sys.platform` monkeypatch'iyle doğru komut listesi seçiliyor (çalıştırmadan).

**Faz F kabul:** F0-F12 testleri; `app.py` < 400; dört denetim; tkinter'sız içe aktarma testi
yeşil; masaüstünü elle açıp (`uv run python -m codementor.desktop`) bozuk DB, temizle, Ctrl+S
akışlarını dene ve rapora ne gördüğünü yaz.

---

## 6. Faz G — Sağlayıcı ve kod temizliği

**Dal:** `faz/g-saglayici` · **Commit:** `fix(faz-g): sağlayıcı sağlamlığı ve kod temizliği`

### G0 — ÖNCE: `pipeline/orchestrator.py` (~460) ve `pipeline/passes.py` (~415) bölünmesi
- **Ne yap:** davranış DEĞİŞMEDEN:
  - `orchestrator.py`: önbellek anahtarı/kaydı (`_cache_key`, `_pipeline_signature`,
    `_run_validation`, kaydetme bloğu) → `pipeline/cache_flow.py`; `_timed_out`, `_remaining` →
    `pipeline/deadline.py`.
  - `passes.py`: `run_pass_verify` + `call_structured` → `pipeline/verify_pass.py`;
    `_socratic` + `run_pass_b` → `pipeline/socratic_pass.py`. `passes.py` dışa aynı adları
    yeniden dışa aktarsın (`from ... import run_pass_b` gibi) ki testler değişmesin.
- **Kabul:** iki dosya da < 400; `git diff tests/` boş; tüm testler geçiyor.

### G1 — O5: CLI ajan çıktısı 64 KB'de kesiliyor
- **Nerede:** `validation/runner.py` (`OUTPUT_LIMIT`), `providers/_cli_common.py` (`ProcessLimits`).
- Config'e `providers.<cli>.output_limit_bytes` (varsayılan 1 MB, en çok 16 MB); CLI ajanları bu
  sınırı kullanır. Kesilirse uyarı: "Model yanıtı çok uzun, kesildi".
- **Test:** sahte CLI betiği (`tests/providers/fake_cli_script.py` deseni) 100 KB yazıyor → kesilmeden
  okunuyor; sınır 10 KB → uyarı.

### G2 — O6: kalıcı CLI hataları yeniden denenmez
- Oturum açılmamış / komut bulunamadı / geçersiz model gibi hatalar `retryable=False` olmalı
  (bkz. `CliTimeoutError`). Hangi metinlerin kalıcı olduğuna `providers/cli_agent.py`,
  `codex_cli.py`'deki ipucu listelerinden bak.
- **Test:** bu hatalarda `RetryPolicy` ikinci deneme yapmıyor (çağrı sayacı 1).

### G3 — D1-D12 (küçük düzeltmeler; her biri ayrı test)
| No | Nerede | Ne yap | Test |
|---|---|---|---|
| D1 | `prompts/v1/repair.user.j2`, `prompts/templates.py` | `<validation_errors>` etiketi `guard` listesine; karmaşıklık onarımında "şemaya uymadı" yerine nedene göre metin | `</validation_errors>` içeren hata nötrleniyor |
| D2 | `verify/schema_check.py` (`extract_json`) | tırnak durumunu yalnız `{` içinde izle | `Model "notu: {"a": 1}` → `{"a": 1}` |
| D3 | `providers/codex_cli.py` (`_events`) | `RecursionError` da yakala | 10.000 iç içe `[` satırı çökmeden atlanıyor |
| D4 | `codex_cli.py` `_LIMIT_HINTS`/`_LOGIN_HINTS` | çıplak `"429"`/`"401"` → kelime sınırlı regex | "line 4291" eşleşmiyor, "HTTP 429" eşleşiyor |
| D5 | `verify/proof.py` (`apply_verdicts`) | `FindingCheck.finding_id` yeni kimliği yazsın | yeniden numaralamadan sonra kimlikler eşleşiyor |
| D6 | `pipeline/passes.py` `LLMSession` | geçiş başına sağlayıcı/model kaydı; maliyet her geçişin fiyatıyla | fallback'e düşen geçişin maliyeti doğru fiyatla |
| D7 | `passes.run_pass_b` | sızıntıdan sonra yeniden üretimde prompt'a "daha soyut sor" notu (içerik sızdırmadan) | ikinci çağrının prompt'unda not var |
| D8 | `prompts/builder.py`, `orchestrator.py` | bozuk few-shot YAML / Jinja hatası → `degraded`, 500 değil | bozuk few-shot dosyasıyla rapor `degraded` |
| D9 | `providers/anthropic.py`, `prompts/budget.py` | tekrar eden `DEFAULT_MAX_TOKENS`, gereksiz `isinstance`, kullanılmayan dönüşler; `TEST_PROVIDERS` test kancası üretimden çıkar | mevcut testler geçiyor; `grep TEST_PROVIDERS src` boş ya da yalnız test yardımcısında |
| D10 | `models/schemas.py` | `LLMMarkupAnalysisOutput` `SCHEMA_MODELS`'e; `schemas/` yeniden üret | `schemas/llm_markup_analysis.schema.json` var |
| D11 | `prompts/builder.py`, `orchestrator.py` | `prompt_version`, `_rules_version`, CLI soru bankası önbelleklensin (mtime ile) | iki analizde dosya sistemi taraması 1 kez (sayaçlı monkeypatch) |
| D12 | `providers/cli_agent.py` (`_json_document`) | doğrusal tarama | 160 KB girdide < 0,25 sn |

### G4 — D18: Tier 0 durdurma tanısı yapısal bayrak
- **Nerede:** `validation/tier0_isolation.py` (`stopped()` metinle tanıyor: `startswith("Kodun sözdizimi")`).
- `Tier0Result`'a `stopped: bool` alanı (model `models/validation.py`'de); `stopped()` bayrağa bakar.
- **Test:** mesaj metni değişse de durdurma tanınıyor; şema/tipleri yeniden üret.

### G5 — D20 kalanları
- `buildinfo.py` maskesiz global logger → `codementor.log.get_logger`.
- `--help` metinlerinde İngilizce kalanlar ("Show this message and exit.") — Typer'ın kendi
  metni; değiştirilebiliyorsa Türkçeleştir, değilse rapora "değiştirilemedi" yaz.
- `eval run --language` serbest metin → enum (`Language`).
- `build_exe.py`: FastAPI/uvicorn masaüstü exe'ye gerekmiyor → `EXCLUDES`'a ekle; sonra
  `uv run python build_exe.py --onedir` + `dist\CodeMentor\CodeMentor.exe --self-check sc.json`
  ile duman testi GEÇMELİ (geçmezse geri al ve rapora yaz).
- `pyproject.toml`: GUI bağımlılıkları (`customtkinter`, `tkinterdnd2`, `pillow`, `keyring`)
  `[project.optional-dependencies] desktop` altına. **DİKKAT:** CI ve `uv sync` bunları hâlâ
  kurmalı (`uv sync --all-extras` ya da dev grubuna ekle); `release.yml` ve `ci.yml`'i buna göre
  güncelle ve `uv lock` çalıştır. Emin değilsen bu maddeyi YAPMA, rapora yaz.

### G6 — Denetimden ertelenenler (PROGRESS "Denetim — Faz A1-D" notunda)
| Madde | Ne yap | Test |
|---|---|---|
| `config_writer` dizi tablosu | `[[providers.x]]` ya da `providers = "metin"` varsa ezme; Türkçe hata dön | dizi tablosu dosyası → hata, dosya değişmedi |
| `config_writer` CRLF | dosya CRLF ise CRLF yaz (`newline` korunur) | CRLF giriş → CRLF çıkış |
| `from_question` kayıplı | `genel` etiketi/varsayılan kısıt kullanıcı açıkça yazdıysa silinmesin: varsayılanı yalnız `to_question` doldurduysa çıkar (bir işaret alanı ya da karşılaştırma) | `concept_tags=['genel','dizi']` gidiş-dönüş eşit |
| `system_errors` | `ConnectionError`/`TimeoutError` için "ağ hatası" metni | mesaj testi |
| Katman | `UsageTotals`'ı `models/` altına taşı; `report/usage.py` storage'a bağımlı olmasın | import testi |
| `primary` sağlayıcı adı | `orchestrator`'da `getattr(provider, "chain", ...)` yerine `LLMProvider` protokolünde açık `primary_name` | mevcut önbellek testleri geçiyor |

### G7 — `ProviderResult` "şema zorlandı mı" + token kalibrasyonu
- `ProviderResult.schema_enforced: bool` (sağlayıcı katı şema uyguladı mı). Raporda gösterilmez;
  eval/log için. Token tahmini (`prompts/budget.estimate_tokens`) gerçek `usage` ile karşılaştırılıp
  log'a oran yazılır (davranış değişmez).
- **Test:** FakeProvider ile alanın taşındığı.

**Faz G kabul:** G0-G7 testleri; iki büyük dosya < 400; dört denetim; exe duman testi (G5).

---

## 7. Faz H — Statik kurallar

**Dal:** `faz/h-kurallar` · **Commit:** `feat(faz-h): yeni statik kurallar ve doğruluk düzeltmeleri`

**Önce öğren — bir kural nasıl eklenir:**
1. Mevcut bir kuralı uçtan uca incele: `grep -rn "C-MEM-003" src tests data docs` (kural sınıfı
   `src/codementor/rules/c_memory.py`, kayıt `rules/registry.py`, fixture'lar `tests/rules/`,
   katalog `docs/rules-catalog.md`).
2. Her yeni kural: kimlik (`DİL-KATEGORİ-NNN`, var olanların devamı), Türkçe başlık, **soru
   biçiminde** açıklama ("…olursa ne olur?"), önem, tür (hata/öneri), en az 2 pozitif + 2 negatif
   fixture, 40 KB kötü niyetli girdiyle süre testi (< 0,25 sn).
3. `uv run codementor rules doc` ile `docs/rules-catalog.md`'yi yeniden üret.
4. README'deki "34 statik kural" sayısını güncelle (iki yerde: "Bir bakışta" tablosu ve CLI örneği;
   `grep -n "34" README.md README.en.md`).

### H1 — Yeni kurallar
| Dil | Kural | Pozitif örnek | Negatif örnek |
|---|---|---|---|
| CSS | `outline: none` + odak göstergesi yok | `button:focus { outline: none; }` (başka focus stili yok) | aynı seçicide `box-shadow` ya da `:focus-visible` stili var |
| CSS | sabit `px` yükseklik + içerik taşması | `.kart { height: 200px; }` metin kutusu | `min-height: 200px` |
| CSS | `position:absolute` + margin ile ortalama | `left:50%; margin-left:-100px` | `transform: translateX(-50%)` |
| C++ | döngüde `std::string +`/`+=` (karesel) | `for(...) s = s + x;` | döngü dışında; `s.reserve` sonrası `+=` (öneri) |
| C++ | döngüde `std::endl` | `for(...) cout << x << std::endl;` | `'\n'` |
| C++ | `reserve` olmadan döngüde `push_back` (öneri, düşük) | bilinen sayıda `push_back` | önce `v.reserve(n)` |
| C | genişliksiz `scanf("%s")` | `scanf("%s", buf);` | `scanf("%99s", buf);` |
| C# | döngüde `string +=` | `for(...) s += x;` | `StringBuilder` |

### H2 — Bilinen kaçırmalar ve yanlış pozitifler (her biri fixture'la)
- CPP-OWN-001: erken `return`/istisna yolunda atlanan `delete` → hata (öneri değil).
- C-MEM-001: aynı dosyadaki kullanıcı fonksiyonuna geçirilen işaretçi (fonksiyon serbest bırakıyorsa
  bulgu yok).
- UNITY-GC-001: kullanıcı `struct`'ı için `new` yanlış bulgusu → bulgu olmamalı.
- UE-GC-001: `TArray<AActor*>` / `TMap<…, UObject*>` alanları yakalansın; UCLASS olmayan sınıfta
  doğru öneri.
- CS-PERF-001: `IList`/`IReadOnlyList`/`ICollection` tipli değişkenler.
- Sıcak yol tespiti sınıf tabanını (MonoBehaviour/UCLASS) denetlesin.

### H3 — Analiz verisi
- `data/call_costs.yaml`: `memset`, `memcpy`, `GetAllActorsOfClass`, `TArray::Remove`, C#
  `RemoveAll`, `RemoveAt(0)`, `Insert(0, …)` maliyetleri (biçim için mevcut satırlara bak).
- `parse_bigo` (`models/_bigo_parser.py`): `log log n`, `Θ(...)`/`Ω(...)`, `max(n, m)`, değişken
  üsler (`n^k`). Her biri için `tests/unit/test_bigo.py`'ye örnek.
- Maskeleme (`analysis/lexical.py` `mask_non_code`): C# 11 raw string (`"""…"""`); dil bilgisi
  parametresi.
- Unreal stub (`data/stubs/ue_stubs.h`): `FMath`, `FHitResult`, dinamik delegeler,
  `GetWorldTimerManager`. Değişiklikten sonra `uv run pytest -m compiler` (zig kuruluysa koşar).
- Include koruması: `#pragma` makro / `#line` için izin listesi — GÜVENLİK İÇİN DİKKAT:
  `validation/include_guard.py`'de reddetmeyi gevşetirsen `tests/unit/test_include_guard.py`'deki
  hiçbir red testi düşmemeli. Emin değilsen YAPMA, rapora yaz.
- gcc/clang/Tier 0 kolon birimi: `-fdiagnostics-column-unit=byte` bayrağı (Tier 1 komutuna).

### H4 — Ölçüm
- Statik dev eval'i yeniden koş: `uv run codementor eval run --split dev --static-only`.
  Sonuç dosyası `eval/results/` altına yazılır; README'deki "Yalnızca statik" satırını
  `uv run codementor eval compare eval/results/*_dev.json` çıktısından GÜNCELLE (elle sayı yazma;
  `tests/unit/eval/test_readme_table.py` tabloyu dosyalarla karşılaştırır).
- Precision düşerse (yeni kural yanlış pozitif üretiyorsa) o kuralı düzelt; rapora önce/sonra yaz.

**Faz H kabul:** her yeni kural fixture + süre testi; katalog yeniden üretildi; README sayıları;
statik dev eval sonucu commit'te; dört denetim.

---

## 8. Faz I — YAPMA

Faz I (yerel modeller, eski Faz 64-66) **Ollama ve canlı model denemesi** gerektirir. Kullanıcı
Ollama kullanılmamasını istedi ve canlı ölçüm token harcar. Bu devirde Faz I'ya DOKUNMA.
Ayrıntısı `docs/BulgularVeDuzeltilecekler.md` §10 Faz I ve `docs/GUNCELLEMELER.md` Faz 64-66'da.

---

## 9. Faz J — İsteğe bağlı

Yalnız E-H bitti ve vaktin varsa. Hepsi küçük ve bağımsız; her biri ayrı commit:
- Zig kurulumunda gereksiz libc başlıklarını budama (382 MB → <150 MB): `toolchain_install.py`;
  `uv run pytest -m compiler` geçmeli.
- Soru bankası: kontrol listesi anlık görüntü testi (`data/checklists/*` içeriğinin özetini
  sabitleyen test).
- `session_id`'yi API anahtarına bağlama (paylaşılan sunucu, D16): önce rapora tasarım öner,
  uygulama.
- **YAPMA:** imzalı exe / Inno Setup (sertifika gerekir), cppcheck/clang-tidy, VS Code eklentisi,
  Rust/Go, JS desteği (büyük işler; kullanıcı kararı).

---

## 10. Kullanıcının kendi yapacakları

Bunlara SEN dokunma:
- **Y2:** `tests/fixtures/llm_responses/unity03_reference.cs` ↔ `private/` altındaki unity-03 referans
  çözümü karşılaştırması (`private/` sana kapalı olabilir; açık olsa da değiştirme).
- GitHub ayarları: secret scanning, push protection, Dependabot alerts.
- Repoyu public yapmak, main'e birleştirme, push, yeni sürüm etiketi.

---

## 11. Teslim raporu şablonu

İş bitince (ya da token bitince) `docs/YAPILANLAR_FAZ_E_J_ANTIGRAVITY.md` dosyasını bu şablonla yaz
ve son commit'e kat:

```markdown
# Faz E-J — Antigravity teslim raporu (<tarih>)

## Dallar ve commit'ler
| Faz | Dal | Commit | Durum (tam / yarım / yapılmadı) |
|---|---|---|---|

## Madde madde
### Faz E
- E1 GET /v1/analyses — ✅ / ⚠️ / ❌
  - Değişen dosyalar: …
  - Testler: `tests/api/test_xxx.py::test_yyy` (… adet)
  - Mutasyon kontrolü: düzeltme geri alınınca <N> test düştü
  - Not: …
(her madde için aynı)

## Denetim komutlarının GERÇEK çıktısı (son satırlar, kopyala-yapıştır)
- ruff check: …
- ruff format --check: …
- mypy: …
- pytest -m "not live": `NNNN passed, NN skipped …`
- web: typecheck / test / build / e2e: …

## Yapamadıklarım ve neden
## Mimariden sapma gerektiren öneriler (uygulanmadı)
## Claude Code'un özellikle bakmasını istediğim yerler
```

**Kurallar:** sayıları komut çıktısından KOPYALA, tahmin etme. Yapmadığın maddeyi ✅ işaretleme.
`git diff main...<dal> -- tests/` ile testleri gevşetip gevşetmediğini kendin kontrol et ve yaz.

---

## 12. Claude Code'un denetimde bakacakları

Bunu bil ki işi buna göre yap:
1. Her dalda dört denetimi kendisi koşar; raporundaki sayılarla karşılaştırır.
2. `git diff main...<dal> -- tests/`: var olan bir testin silinmesi, `skip` eklenmesi, eşiğin
   büyütülmesi, beklentinin gevşetilmesi = red.
3. Yeni testleri düzeltmeyi geri alarak çalıştırır (mutasyon kontrolü); düşmeyen test = red.
4. Linux CI taklidi (tkinter engelli) ile tüm testleri koşar (§3.1).
5. Görünmez karakter taraması (§3.3), 400 satır kontrolü, mypy strict.
6. Güvenlik maddeleri (E5-E8, E11, H3 include) için kendi kötü niyetli girdileriyle dener.
7. kod-denetci ajanıyla bağımsız inceleme; bulgular düzeltilmeden main'e birleşmez.
