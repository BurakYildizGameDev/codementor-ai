# Devir: Faz 55 — Tier 0 ayrıştırma ve maskeleme sağlamlığı (başka bir ajana)

Bu belge Faz 55'i uygulayacak ajan içindir. Claude Code işi sonra test edip denetleyecek.
Önce `AGENTS.md`'yi oku; oradaki altın kurallar bu belgeden önce gelir. Plan tanımı:
`docs/UYGULAMA_PLANI.md` "### Faz 55". Mimari: `docs/mimari.md` §4 (boyut sınırı satır ~205),
§12 (tehdit modeli, "Kaynak tüketimi" satırı).

## 0. Başlangıç durumu ve kurallar

- **Dal:** `main` (`a702872`) üzerinden `faz/55-tier0-saglamlik` aç.
- **Doğrulama:** Fazın sonunda dördü de yeşil olmalı (Windows'ta `make` yok, tek tek koş):
  `uv run ruff check .` · `uv run ruff format --check .` · `uv run mypy src/` ·
  `uv run pytest -m "not live"` (bugün **2948 geçiyor, 14 atlanıyor**).
- **Faz 52-54 denetiminden çıkan kesin kurallar** (bunlar ihlal edilirse iş reddedilir):
  1. **Mevcut bir testi gevşetme** (eşik büyütme, `<` → `<=`, beklenen değeri koda göre
     değiştirme, `skip` ekleme). Bir test düşüyorsa ya kod yanlıştır ya da test; hangisi
     olduğunu yaz ve **dur, sor**.
  2. **Ölçmediğin sayıyı yazma.** PROGRESS'e ve teslim raporuna yazılan her sayı (süre, test
     sayısı, satır sayısı) ya komut çıktısından ya da bir dosyadan gelir; yanına komutu yaz.
  3. Kökte özet/rapor dosyası bırakma. Teslim raporu yalnız PROGRESS'teki faz bölümüne girer.
     Geçici log dosyalarını (`*.out`, `*.err`) sil, `.gitignore`'a ekleme.
  4. Commit mesajına AI atıf satırı (Co-Authored-By vb.) ekleme. `main`'e birleştirme ve push yapma.
  5. 400 satırı aşan dosya yaratma. Yeni `src/` modülüne kısa modül docstring'i ekle.
- **Testler ağa çıkamaz** (`tests/conftest.py`). Tk testleri Linux CI'da toplanmaz
  (`tests/desktop/conftest.py`); yeni test Tk gerektirmesin.

## 1. Kritik ön bilgi: tree-sitter'da süre sınırı (Claude Code ölçtü, 2026-10-05)

Ortam: `tree-sitter` **0.25.2** (`pyproject.toml`: `>=0.25.2,<0.26`), Windows 11, Python 3.12.

| Deneme | Sonuç |
|---|---|
| `parser.parse(bytes)` ile `("a<" * 20000)` (40 KB, C++) | ağaç döner, **~236 ms** |
| `parser.timeout_micros = …` | `DeprecationWarning: Use the progress_callback in parse()` |
| `parser.parse(bytes, progress_callback=cb)` | `UserWarning: The progress_callback is ignored when parsing a bytestring` → **etkisiz** |
| `parser.parse(read_callback, progress_callback=cb)` | **Süreç çöküyor (segfault, çıkış kodu 139)**; 200 baytlık `a<a<…` ve 6 KB'lık geçerli C++'ta bile. 21 baytlık geçerli kodda çalışıyor. Parçaları önceden saklamak da çökmeyi önlemedi. |

**Sonuç:** Aynı süreç içinde iptal edilebilir ayrıştırma bu sürümde **kullanılamaz**. Okuma geri
çağrısı + `progress_callback` yolunu üretim koduna **koyma**. Kullanımdan kalkmış
`timeout_micros`'a da yaslanma.

Mevcut koruma zaten var: 600 satır / 40 KB boyut sınırı (mimari §4), ayrıştırma
`asyncio.to_thread` içinde (Faz 26), toplam analiz süresi sınırı `pipeline.analysis_timeout_s`
(Faz 48). Eksik olan şey, en kötü durum süresinin **ölçülüp testle sabitlenmesi**.

## 2. Yapılacaklar

### 2.1 Ayrıştırma süresi (önerilen yol: ölç + sabitle + ADR)

1. **Ölçüm betiği** (scratch, commit'lenmez): Her Tier 0 dili için (C, C++, C#, Python, HTML,
   CSS) sınıra yakın (≤ 40 KB, ≤ 600 satır) patolojik girdiler üret ve
   `codementor.validation.tier0.run_tier0` + `codementor.analysis.extractor.extract_facts`
   sürelerini ölç. Asgari girdi listesi:
   - `"a<" * 20000` (C++ şablon belirsizliği), `"(" * 40000`, `"{" * 40000`, `"[" * 40000`
   - 600 satırlık iç içe `if (x) {` (kapanmamış), 600 satırlık uzun makro devamı (`\` ile)
   - C#: `"a<" * 20000`, iç içe lambda; Python: 600 satır iç içe girinti, `"(" * 40000`
   - HTML: 40 KB kapanmamış `<div>`; CSS: 40 KB iç içe `{`
   Sonuçları tablo halinde PROGRESS'e yaz (girdi, dil, ms; komutu da yaz).
2. **Karar eşiği:** En kötü durum **< 1 s** ise süre sınırı yerine boyut sınırı + gerileme testi
   yeterlidir → ADR yaz (aşağıda). Herhangi bir girdi **≥ 1 s** ise **dur ve raporla**: o zaman
   alt süreçte ayrıştırma gibi mimari bir değişiklik gerekir, Claude/kullanıcı karar verecek.
3. **ADR:** `docs/adr/0024-tier0-sure-siniri.md` (son ADR 0023). Bağlam (yukarıdaki §1 tablosu),
   karar (süreç içi iptal yok, gerekçesi segfault ve deprecation; koruma = boyut sınırı + iş
   parçacığı + analiz süresi sınırı + ölçüm testi), sonuçlar (tree-sitter sürümü yükseltilince
   yeniden değerlendir). Mimari §12 "Kaynak tüketimi" satırına ADR'ye bir atıf ekle; başka
   mimari değişiklik yapma.
4. **Gerileme testi:** `tests/unit/test_tier0_budget.py` (yeni). En kötü 3-4 girdiyi
   parametrize et; `run_tier0` süresi `< 1.5 s` olsun. Kapsama koşusunda süreler 2-3 kat
   uzuyor: `tests/unit/test_facts_review.py` içindeki `_deadline()` kalıbını kullan (kopyalama;
   ortak bir yardımcıya taşımak gerekirse `tests/` altında küçük bir modüle al). Ayrıca sınıra
   yakın **geçerli** bir C++ dosyasının (≈ 39 KB) hatasız ayrıştığını doğrulayan bir test ekle.
5. Plandaki "zaman sınırı aşılırsa kısmi olgu üretme" maddesi bu yolda geçersizdir (süre sınırı
   yok); ADR'de ve PROGRESS'te bunu açıkça yaz, `[x]` yerine gerekçeli `[~]` işaretle.

### 2.2 C++ raw string maskelemesi

Yer: `src/codementor/analysis/lexical.py` → `mask_non_code` (satır ~50) ve `_string_end`.
Çağıranlar: `analysis/extractor.py`, `analysis/parsers.py`, `analysis/_engine.py`,
`ingest/detect.py`, `validation/include_guard.py`.

Bugünkü hata (Claude Code doğruladı):
```
girdi : const char* s = R"(a"b)";
çıktı : const char* s = R"  "b)"      ← string `"(a"`'da bitti sanılıyor, `b)"` kod sayılıyor
```
Çok satırlı raw string içindeki `/*`, `//`, `"` ve ayraçlar kod/yorum sanılıyor.

1. Raw string biçimleri: önek `R`, `LR`, `uR`, `UR`, `u8R`; `R"delim( … )delim"`. `delim` 0-16
   karakter, boşluk/`(`/`)`/`\` içermez. Kapanış tam olarak `)` + `delim` + `"`. İçerik satır
   sonlarını aşabilir; kaçış (`\`) yoktur.
2. Önekin kimlik parçası olmamasına dikkat: `FOO_R"(…)"` geçerli bir raw string değildir;
   `R`'den önceki karakter `_WORD_CHARS` içinde olmamalı (`u8R`/`LR` gibi önekler hariç).
3. Maskeleme sözleşmesi korunur: uzunluk ve satır sonları aynı kalır, içerik boşluk olur,
   açılış `R"delim(` ve kapanış `)delim"` görünür kalabilir (mevcut `"…"` kalıbına uy).
4. Kapanmamış raw string: dosya sonuna kadar maskele (mevcut kapanmamış string davranışına bak).
5. C# 11 raw string (`"""…"""`) bu fazın kapsamı dışında; dokunma, PROGRESS "Sonraya"ya yaz.
6. **Testler** (`tests/unit/` altında, mevcut `lexical` testlerinin yanında; dosyayı bul):
   - pozitif: tek satır, özel `delim`'li (`R"x(a)"b)x"`), çok satırlı, içinde `/*`, `//`, `"`,
     `{`, `}`, `#include` olan; `u8R`/`LR` önekli; kapanmamış.
   - negatif: `FOO_R"(x)"` gibi kimlik + string; normal `"…"`; `R` adlı değişken (`R + 1`).
   - özellik testi (hypothesis): rastgele metinde uzunluk ve `\n` konumları korunur.
   - **güvenlik gerilemesi:** aşağıdaki girdide `include_guard.check_includes` 4. satırdaki
     mutlak yolu **hâlâ** reddetmeli (bugün reddediyor; bozma):
     ```
     const char* s = R"(
     /*
     )";
     #include "/etc/passwd"
     // */
     int main(){return 0;}
     ```
     Ayrıca raw string **içindeki** `#include "/etc/passwd"` satırı için `include_guard`'ın
     bugünkü davranışını ölç ve testle sabitle. Fail-closed (reddetmek) kabul edilebilir;
     değişirse gerekçesini yaz.
7. Golden testleri (`uv run pytest tests/golden`) değişirse bu bir davranış değişikliğidir:
   `--update-golden` kullanmadan önce farkı PROGRESS'e yaz ve nedenini açıkla.

### 2.3 Tier 0 D2: kapanmamış blok + bağımsız gerçek hata

Yer: `src/codementor/validation/tier0.py` → `run_tier0` (satır ~150). Bugün kapanmamış blok
varken dosya sonuna (`tokens.last_end`) uzanan **tüm** ERROR düğümleri atılıp tek bir özet
mesaja çevriliyor. Dosya sonuna uzanan ama kapanmamış bloktan **bağımsız** gerçek bir hata
varsa (ör. son fonksiyonda eksik `;`) kayboluyor olabilir.

1. **Önce yeniden üret:** Hatayı gösteren başarısız bir test yaz (kapanmamış `{` + dosyanın
   sonlarına doğru ayrı bir sözdizimi hatası; C ve C++ için). Birkaç biçim dene.
   **Hata yeniden üretilemezse kod değiştirme**; denediğin girdileri ve çıktıyı PROGRESS'e yaz,
   D2'yi "yeniden üretilemedi" diye kapat.
2. Üretilebilirse: özet mesaj kalsın, bağımsız hata da ayrı tanı olarak raporlansın. Ayrımı
   ERROR düğümünün başlangıcının kapanmamış blok satırlarıyla (`open_rows`) ilişkisine göre yap;
   tahmini çözümü testlerle sınırla.
3. `MAX_DIAGNOSTICS` üst sınırı ve "özet asla düşmez" kuralı korunur (mevcut testler).
4. Eval etkisi: `uv run codementor eval run --split dev --static-only` koş (serbest, token
   harcamaz). Sonucu `eval/results/`'taki en son statik dev dosyasıyla örnek örnek karşılaştır
   (değişen örnek kimliklerini yaz). Test bölümünü **koşma**.

## 3. Bitirme

- `docs/UYGULAMA_PLANI.md` Faz 55 başlığı "(YAPILDI tarih)", maddeler `[x]` (ya da gerekçeli `[~]`).
- `PROGRESS.md`: durum tablosuna `| 55 | … | faz/55-tier0-saglamlik | tarih | Mimo (Cline) / — |`;
  "## Faz 55 — Notlar" (Yapılanlar / Alınan kararlar / Açık sorular / ölçüm tablosu);
  "Kaldığımız yer" satırı; "Sonraya"daki iki Faz 55 maddesini (`D2`, raw string) üstü çizili kapat.
- Commit: `fix(faz-55): Tier 0 ayrıştırma ve C++ raw string sınırları` (gerekirse ADR'yi ayrı
  `docs(adr): …` commit'iyle).

## 4. Teslim raporu (PROGRESS faz bölümüne)

- Dal, commit kimlikleri, `git diff --stat main...HEAD`.
- Dört doğrulama komutunun **son satırları** (kopyala-yapıştır, elle yazma).
- §2.1 ölçüm tablosu (komutla birlikte).
- Kabul maddeleri tek tek `[x]` / `[~]` / `[ ]` + neden.
- Değiştirdiğin **her mevcut test** için: dosya, eski → yeni, gerekçe (hiç yoksa "yok" yaz).
- Emin olmadığın ya da kapsam dışı bıraktığın her şey.

Claude teslimden sonra: dört komutu yeniden koşacak, `git diff main...HEAD -- tests/` ile test
değişikliklerini tek tek okuyacak, ölçüm tablosundan birkaç satırı yeniden ölçecek ve raw string
/ include koruması testlerini kendi girdileriyle deneyecek.
