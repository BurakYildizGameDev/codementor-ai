# Kalan İşler

> **Kaynak:** Faz J5 sonrası tarama (2026-10-17). Bulguların ayrıntısı
> `docs/BulgularVeDuzeltilecekler.md` (§1-§10) ve `PROGRESS.md` "Sonraya" bölümünde; bu dosya
> yalnızca **iş listesidir**. Ayrıntılı gerekçe/kanıt için o iki belgeye bakılır.
>
> **İşaretler:** 🤖 = ajan uçtan uca yapabilir (ağ, API anahtarı, elle oturum gerekmez) ·
> 👤 = yalnız kullanıcı (erişim, anahtar, etiket, donanım, elle deneme) · ⏸ = karar/onay bekliyor.
>
> **Nasıl kullanılır:** iş bitince ilgili kutu `[x]` yapılır, `PROGRESS.md`'ye (faz notu ya da
> "Sonraya") işlenir. Kapsam dışı yeni fikirler doğrudan buraya değil, önce `PROGRESS.md`
> "Sonraya" bölümüne yazılır (AGENTS.md altın kural 2). Öncelik sırası bölüm içinde yukarıdan
> aşağıdır.

## A. Ajan ile yapılabilecek işler

### [x] 🤖 1. README ve belge sayılarını gerçekle eşitleme (P7) — ✅ **BİTTİ 2026-10-17**
- **Kapsam:** `README.md` s.13 badge `testler-3300%2B` → **3700+** · s.42 "3.300+ test … 29 ADR" →
  **3.700+ test … 30 ADR** · s.150 "(docs/adr/, 29 kayıt)" → **30 kayıt** · s.480 "~28 bin satır test
  (~29 bin satır kaynak koda karşı)" → **"~38 bin satır test (~28 bin satır kaynak koda karşı)"** ·
  s.485 faz anlatımı "Faz 0-63, ardından public öncesi Faz A-D ve K" → **"… Faz A-H, J ve K"**;
  ayrıca `README.en.md` s.43 "3,300+ tests … 29 ADRs" → **"3,700+ tests … 30 ADRs"**.
- **Ölçüm (2026-10-18'de doğrulandı):** yöntem = izlenen **metin** dosyalarında **boş olmayan** satır
  sayısı (`git ls-files`, boş satırlar hariç; ilk 8 KB'da NUL baytı olan binary dosyalar atlanır —
  aksi halde `desktop/assets/*.png|ico` 546 sahte satır ekliyor) · `docs/adr/*.md` = **30 dosya** ·
  `src/` **27 194** satır, `tests/` **37 595** satır, `web/` **6 139** satır ·
  `pytest -m "not live"` **3758 geçti / 16 atlandı**.
- **Dosyalar:** `README.md`, `README.en.md`.
- **Doğrulama:** `uv run pytest tests/unit/eval/test_readme_table.py -q` (eval tablosu testle
  denetleniyor, elle düzenlenmez) + `uv run pytest tests/unit/test_release_readiness.py -q`.
- **Sonuç (2026-10-17):** uygulandı; ayrıca diğer sayı iddiaları ölçülüp **doğru** bulundu (41 statik
  kural, 166 eval örneği dev 96 / test 70, 60'tan fazla faz). Eski kalıp taraması temiz, iki dosyada
  CR=0, `ruff check` temiz, `pytest -m "not live"` 3758 geçti.
- **Düzeltme (2026-10-18):** (a) `src/` için kaydedilen **28 369 yanlıştı** → **27 740**, iş 3'ün
  derin doğrulamasında yöntem netleşince (binary varlıklar hariç) → **27 194**; bu yüzden README'nin
  kaynak iddiası da düzeltildi: "~28 bin" → **"~27 bin"** (`tests/` tarafı "~38 bin" doğru).
  (b) faz listesi iş 3'te teste bağlanınca **K**'nın atlandığı çıktı: README
  "… Faz A-H ve J" → **"… Faz A-H, J ve K"** (PROGRESS.md'de bölümü olan fazlar; I henüz
  yapılmadığı için listede yok).
- **Boyut:** küçük (2 dosya, ~8 satır).

### [x] 🤖 2. `docs/BulgularVeDuzeltilecekler.md` durum tazeleme — ✅ **BİTTİ 2026-10-17**
- **Kapsam:** §1 özet tabloda **O10/O13/O14** satırlarına `✅ Faz F`; §4'te bu üç başlığa `✅ Faz F`;
  §6 P-tablosu gerçek durumla yenilenir (P5-P9 ✅ Faz D, P10 kısmi → `v0.1.1` etiketi kullanıcıda,
  P11 ✅ Faz D'de onefile+onedir derlendi ve `--self-check` geçti, P12 karar, P13 açık, P4/Y2 açık);
  P6 satırındaki "252 KB" → **140 KB** (Faz D'de 263 → 31 KB arşivlendi, E-J notlarıyla tekrar
  büyüdü); §10'da **P11** kutusu `[x]`.
- **Dosyalar:** `docs/BulgularVeDuzeltilecekler.md` (yalnız).
- **Doğrulama:** dosya varlık kontrolü (`README.en.md`, `SECURITY.md`, `CONTRIBUTING.md`,
  `CHANGELOG.md`, `docs/gelistirme-gunlugu/`, `dist/CodeMentor-0.1.1-win64.zip`),
  `uv run pytest tests/unit/test_release_readiness.py -q`.
- **Boyut:** küçük-orta (1 dosya).
- **Sonuç (2026-10-17):** uygulandı — 19 parça, tek dosyada +20/−19 satır. Kanıt: taşınan belgeler
  kökte yok / `docs/gelistirme-gunlugu/` altında (10 dosya) · `PROGRESS.md` 146 KB + arşiv 224 KB ·
  `dist`: `CodeMentor.exe` (13 Eki), onedir, `CodeMentor-0.1.1-win64.zip` (16 Eki), `codementor.toml`
  yok · `git tag` → `v0.1.0`/`v0.1.1` · `README.en.md`/`SECURITY.md`/`CONTRIBUTING.md`/`CHANGELOG.md`
  ve `.github` şablonları var · `pytest tests/unit/test_release_readiness.py` 6 geçti.
- **Sapmalar (kayıt için):** (a) P6 için spec'teki "140 KB" yerine ölçülen değer yazıldı
  (146 KB / 142,6 KiB). (b) §1'de 5. kolon lejantı "Doğrulama" = **bulgunun tespit yöntemi** olduğu
  için O10/O13/O14 satırlarında 📖 korundu; kapanış 6. kolona `Evet (Faz F)` yazıldı (O1 `Evet (belge)`,
  O6 `G2` konvansiyonu). (c) §10 P11 kutusu ikiye ayrıldı: derleme `[x]`, eski Faz 60 elle doğrulaması
  kullanıcıya devredildi (U5).

### [x] 🤖 2b. §1 özet tablosunu §4/§10 kapanışlarıyla hizala — ✅ **BİTTİ 2026-10-18**
- **Kapsam (iş 2 sırasında ölçüldü):** §4 başlığında `✅ Faz X` olan ama §1 satırında kapanış etiketi
  bulunmayan bulgular — O3, O4, O5, O9, O12, O15, O16, O17 ve Y1, Y3, Y4, Y5, Y7, Y8, Y9 (O10/O13/O14
  iş 2'de yapıldı). Yalnız 6. kolona `Evet (Faz X)` eklenir; 5. kolon (Doğrulama) **değişmez**.
- **Dosyalar:** `docs/BulgularVeDuzeltilecekler.md` (yalnız).
- **Doğrulama:** her satır §4 başlığı ve §10 kutusuyla karşılaştırılır; satır sayısı sabit kalır.
- **Sonuç (2026-10-18):** uygulandı — 15 satır (+0/−0, tablo 32 satır). Etiketler: Y1 → A2 ·
  Y3/Y4/Y5, O3/O4 → B · Y7/Y8/Y9, O9/O12 → C · O5 → G1 · O15/O16 → E · O17 → "release; D". 5. kolon
  ve diğer satırlar değişmedi; PROGRESS'e işlendi.
- **Boyut:** küçük (~15 satır).

### [x] 🤖 3. Sayı iddialarını teste bağlama (tekrar bayatlamasın) — ✅ **BİTTİ 2026-10-18**
- **Kapsam:** `tests/unit/test_release_readiness.py` yanına yeni testler: `README.md` ve
  `README.en.md`'deki ADR sayısı iddiası == `docs/adr/*.md` sayısı; README badge test sayısı ↔
  gerçek toplama sayısı (ya da alt sınır); `~N bin satır` iddiaları ölçüme karşı; README'deki faz
  anlatımı ↔ `PROGRESS.md` durum tablosundaki faz kümesi.
- **Dosyalar:** `tests/unit/test_release_readiness.py` (+ gerekirse küçük yardımcı).
- **Doğrulama:** yeni testler yeşil; kasıtlı bozma (mutation) ile kırmızı olduğu kanıtlanır; ağa
  çıkmaz.
- **Boyut:** küçük-orta (yeni vakalar ~120 satır).
- **Sonuç (2026-10-18):** uygulandı — `tests/unit/test_release_readiness.py` içine **5 test + 8
  yardımcı** (+167 satır; ilk tur +136, doğrulama turu +31): (1) ADR sayısı iddiaları (TR "30 ADR"/"30 kayıt", EN "30 ADRs") ↔
  `docs/adr/*.md`; (2) badge ve "N+ test" iddiaları ↔ gerçek toplama sayısı (alt sınır; alt
  süreçte `--collect-only -q -m "not live"`, ~7 sn, tek koşu); (3) "~N bin satır" iddiaları ↔
  `git ls-files` + **metin** dosyalarda boş olmayan satır ölçümü (binary varlıklar atlanır; binde
  yuvarlama; git yoksa atlanır) + `test_line_count_measurement_skips_binary_assets` bu atlamayı
  ayrıca kanıtlar; (4) README faz
  listesi ↔ `PROGRESS.md`'de bölümü olan faz harfleri + `PROGRESS-faz-0-63.md` arşivi.
- **Mutasyon kanıtı (16/16 kırmızı):** ilk tur 4/4 (ADR 30→31 · badge 3700→9999 · "~38 bin"→
  "~44 bin" · faz listesi "A-H, J ve K"→"A-H ve J"), derin doğrulama turu 12/12 (EN "30 ADRs"→"29" ·
  "30 kayıt"→"9 kayıt" · TR/EN "N+ test" · "~38 bin"→"~44 bin" · "~27 bin"→"~33 bin" · faz listesi K
  düşürme · PROGRESS'e sahte `## Faz I` · arşiv aralığı 0-63→0-62 · binary guard kaldırma
  (`_is_binary` → `False`; 2 test kırmızı)). Hepsi ilgili testi kırmızı yaptı, geri alınınca yeşil;
  dosyalar bayt-bayt eski hâline döndü (SHA-256 kontrolü).
- **Ölçüm (iş 3 + doğrulama turu sonrası, metin dosyaları):** `src/` **27 194**, `tests/` **37 732**
  (iş 3 öncesi 37 595'ten +137), `web/` **6 139** → README "~38 bin / ~27 bin" iddiası geçerli. Bağımsız yöntem
  (PowerShell/.NET `-split "`r?`n"`) aynı üç değeri verdi.
- **Sapmalar (kayıt için):** (a) kapsam "PROGRESS.md durum tablosu" diyordu; tabloda D satırı
  yok, bu yüzden ölçüt **bölümü olan fazlar** alındı (A-H, J, K). (b) Test yazılırken README'nin
  faz listesinin K'yı atladığı bulundu → iş 1 düzeltmesi (yukarıda). (c) Derin doğrulamada
  sayımın binary varlıkları metin gibi saydığı çıktı (`src/` 546 sahte satır) → yöntem metin-only
  yapıldı, README kaynak iddiası "~28 bin" → "~27 bin".

### [x] 🤖 4. K2 kalan regex taraması (kod + test) — ✅ **BİTTİ 2026-10-18**
- **Kapsam:** `analysis/_recursion.py`, `verify/lines.py`, `verify/proof.py` ve `analysis/`+`rules/`
  içindeki desenler **en kötü girdiyle** ölçülür; karesel/kübik davranış varsa doğrusallaştırılır.
  Test: desen başına < 50 ms bütçesi + hypothesis ile uzunluk eğrisi.
- **Dosyalar:** yeni test dosyası (`tests/unit/`) + olası 2-3 küçük desen düzeltmesi.
- **Doğrulama:** yeni testler; tam suite (`uv run pytest -m "not live"`) yeşil kalır.
- **Boyut:** orta.
- **Kaynak:** Bulgular §10 Faz A "K2 — Kalan tarama" kutusu (tek açık kutu).
- **Sonuç (2026-10-18):** uygulandı — `tests/unit/test_regex_budget.py` (**339 satır**, 96 vaka):
  (1) desenler `codementor.analysis` / `codementor.rules` / `codementor.verify` paketlerinden
  **otomatik keşfedilir** (şu an 44 desen; alt sınır `>= 40` ile keşif bozulmasına karşı test);
  (2) her desen 18 "en kötü girdi ailesi" ile 40 KB'da **< 50 ms** bütçesine karşı ölçülür
  (CPU saati, en iyi 4 koşu); (3) hypothesis ile **uzunluk eğrisi** (4x girdi 8x'ten fazla
  süre üretmez, 2 ms taban; duvar saati); (4) düzeltilen dört girdi noktası bilinen en kötü
  yüküyle ayrıca sabitlenir; (5) eski desenler karşılaştırma ölçütü olarak testte tutulur ve
  **eşdeğerlik** hem örnek hem rastgele (hypothesis fuzz) girdide doğrulanır.
- **Bulunan ve düzeltilen beş desen (hepsi aynı zamanda değer üretir):**
  (a) `analysis/call_costs.py` `_LAST_INDEX`/`_END_INDEX` — sınırsız taban sınıfı `[\w.]*`
  geri izleme yapıyordu (`"a"*4000` → 48 ms, karesel; 40 KB → ~4-9 sn). Sondan çapalı küçük
  desen + geriye doğru taban doğrulaması (`_index_base`); davranış eski `(?P<base>…)` ile aynı
  (14 parametreli vaka + fuzz testi).
  (b) `verify/leak_guard.py` `_ASSIGNMENT` — sol/sağ taraf sınırsız (`"_"*1600` → 29 ms, karesel).
  Baştaki `\b`, sınırlı + sahiplenici sınıflar (`_MAX_ASSIGN_LHS=64`, `_MAX_ASSIGN_RHS=128`),
  ayrıca `code_violations` içinde `;`/`=` hızlı elemesi (aynı işlevde `FENCE` kalıbı vardı).
  (c) `verify/leak_guard.py` yorum/metin taraması — `/\*.*?\*/` kapanmayan yorumda ve
  kapanmayan tırnaklarda karesel (`"/*a"*k` 40 KB'da ~1,2 sn). Desen yerine **ters yönlü tek
  geçişle** hesaplanan kapanış dizisi + tek geçişli tarayıcı (`_body_closers`): sonuç eski
  desenle birebir aynı, süre doğrusal.
  (d) `verify/complexity.py` `_TRAILER` — baştaki `\s*` boşluk dizisinde karesel
  (`" "*400` → 18 ms; 40 KB → dakikalar). `_before_trailer` (arama + `rstrip`) ile aynı sonuç.
- **Mutasyon/eşdeğerlik kanıtı:** eski (süper-doğrusal) beş desen yeni büyüme kontrolüne
  sokuldu → **5/5 kırmızı** (1 KB → 4 KB aralığında 16x büyüme; 40 KB'da 3,1 s – 176 s olurdu);
  yeni desenler 40 KB'da 0,0–29,8 ms (en yüksek: `_ASSIGNMENT` tam yıldız/boşluk dizisinde).
  Fuzz testi yazım sırasında iki gerçek hata yakaladı ve ikisi de düzeltildi
  (`code="/"` → `IndexError`; `code="'//"` → eski desenden sapan çıktı).
- **Doğrulama:** `ruff check` temiz · `ruff format --check` 478 dosya · `mypy src/` 216 dosya
  temiz · yeni dosya **96 geçti** (~3 sn) · tam suite `pytest -m "not live"` **3859 geçti /
  16 atlandı** (4:45; iş 3 sonrası 3763'ten +96) · testler ağa çıkmaz.
- **Sapmalar (kayıt için):** (a) kapsam `analysis/` + `rules/` diyordu; `verify/` de eklendi
  (üç adlandırılmış dosya orada). (b) `verify/` → `analysis/` importu **yok** (katman): yorum/metin
  tarayıcısı `analysis/lexical.py` yerine `leak_guard` içinde yerel yazıldı. (c) İki desende
  davranış birebir korunamazdı (`_ASSIGNMENT` sınırları): sınırlar tek deyim ölçeğinde cömert
  seçildi ve testle belgelendi.
- **Kaynak:** Bulgular §10 Faz A "K2 — Kalan tarama" kutusu → **kapandı**. Not: `detect.py`
  taraması Faz A1'de yapılmıştı; bu tur üç paketin tamamını kapsar.

### [x] 🤖 4b. Zamanlama testlerini yük altında kırılgan olmaktan çıkar (O1-O4 + Tier 0 bütçesi) — ✅ **BİTTİ 2026-10-18**
- **Sorun:** `tests/unit/test_facts_review.py` O1-O4 doğrusal süre testleri ve
  `tests/unit/test_tier0_budget.py` **mutlak duvar saati** bütçesiyle koşuyor (1,5 sn). Tek başına
  ölçülen süreler 0,14-0,76 sn; tam suite yükü altında **1,10 sn** (ölçüldü) ve tam suite koşusunda
  `test_o1_many_inner_loops_linear` bir kez bütçeyi aşıp kırmızı oldu (yeniden koşuda yeşil).
  `src/` değişmediği için iş 3/4 ile ilgisi yok: kırılganlık **eşiğin kendisinde**.
- **Kapsam (önce karar, sonra uygulama):** üç yol var, seçim gerekçesiyle `PROGRESS.md`'ye yazılır —
  (a) bütçeyi gerçekçi hâle getir (ör. 3 sn) + gerileme duyarlılığını korumak için ölçümü "en iyi N
  koşu"ya çevir; (b) bu testleri `slow` işaretleyip `make check` dışında ayrı koş; (c) iş 4'teki
  **göreli büyüme** kalıbını (büyük girdi ≤ N × küçük girdi) mutlak bütçenin yanına koy. Öneri:
  (c) birincil (makine yükünden bağımsız), + (b) yalnız mutlak bütçe için.
- **Dikkat (AGENTS.md altın kural 1):** eşik/niyet değişirse `docs/adr/0024-tier0-sure-siniri.md`
  "gerileme testi < 1,5 s" ifadesi güncellenir; bu **ADR değişikliğidir** → gerekçe yazılıp onay
  alınır (yeni ADR değil, mevcut ADR'e not).
- **Dosyalar:** `tests/unit/test_facts_review.py`, `tests/unit/test_tier0_budget.py`; gerekirse
  `pyproject.toml` (işaret) + `Makefile`/`AGENTS.md` komut notu, `docs/adr/0024-*.md`.
- **Doğrulama:** seçilen kalıpla ilgili testler **3 tam suite koşusunda hiç kırmızı olmaz**; kasıtlı
  yavaşlatma (ör. O1 girdisini karesel hâle getiren geçici yama) ilgili testi **kırmızı** yapar
  (duyarlılık kanıtı); `ruff`/`format`/`mypy` temiz.
- **Boyut:** küçük-orta (~1-2 saat; karar + küçük test düzenlemesi).
- **Kaynak:** PROGRESS "Sonraya" (2026-10-18) — iş 3 derin doğrulamasından çıktı, iş 4 tam suite
  koşusunda (4:45) tekrar görüldü.
- **Sonuç (2026-10-18):** uygulandı — seçim **(c)+(a)**: göreli büyüme (2× girdi ≤ 3× süre) birincil,
  mutlak bütçe 1,5 s **korunur** ve ölçüm ısınma + 3 koşunun **en hızlısı**; `slow` işaretleyip
  `make check` dışına alma (b) seçilmedi (gerileme korumasını boşaltırdı). Eşik değişmedi → ADR-0024
  notu/onayı gerekmedi. `test_facts_review.py`: `_best_of` + 4 büyüme testi;
  `test_tier0_budget.py`: `_best_of` + 3 büyüme vakası (HTML kapanmamış `<div>` doğası gereği
  süper-doğrusal → yalnız bütçede). Duyarlılık: geçici karesel yama O1'de **0,336 → 1,071 sn**
  (kırmızı; mutlak test 1,071 < 1,5 olduğu için yeşil kalırdı), Tier 0'da CSS **97 → 347 ms** ve
  C **86 → 323 ms** (kırmızı); yamalar geri alındı, dosyalar SHA-256 ile aynı. İlgili testler
  **3 tam suite** koşusunda kırmızı olmadı; `ruff`/`format`/`mypy` temiz.

### [x] 🤖 4c. `docs/ZAYIF_VE_GELISTIRILECEK_YONLER.md` bayat sayıları tazele + teste bağla — ✅ **BİTTİ 2026-10-18**
- **Kapsam (iş 1/3'te bilinçli kapsam dışıydı):** belgedeki sayı iddiaları ölçümle değiştirilir ve
  teste bağlanır. Ölçülen bayatlıklar (2026-10-18, iş 4 sonrası; yöntem: izlenen **metin**
  dosyalarında boş olmayan satır, binary varlıklar hariç):
  - s.399 "~29 bin satır kaynak, ~28 bin satır test" → **~27 bin** (27 289) / **~38 bin** (37 732 +
    yeni test dosyası 339 = 38 071) — README kardeşi iş 1/3'te tazelenip teste bağlanmıştı.
  - s.50 ve s.91 "3.300+ test" → **3.700+ test** (README badge'iyle aynı, iş 1); s.50 ve s.423
    "29 ADR" → **30 ADR** (`docs/adr/*.md` = 30).
  - s.397-398 "400 satırı aşan dosyalar: `desktop/app.py` 505, `pipeline/orchestrator.py` 465,
    `pipeline/passes.py` 426 (Faz F/G'de bölünecek)" → gerçek: **350 / 350 / 323**; bölmeler
    yapıldı, "Faz F/G'de bölünecek" notu düşer.
  - s.402-403 "`report/usage.py` → `storage`; Faz G'de düzeltilecek" → `usage.py` 62 satır ve
    yalnız `models/` içe aktarıyor: **kapandı**, not düşer.
  - s.404 ve s.572 "(~60 madde)" Sonraya sayısı → ölçüm: **120 madde / 52'si açık** (kapananlar
    üstü çizili); hangi sayının raporlanacağı belgede tanımlanır (öneri: "açık" sayısı).
- **Teste bağlama (tekrar bayatlamasın):** `tests/unit/test_release_readiness.py`'deki
  `_tracked_nonblank_lines()` + ADR sayımı bu belge için de kullanılır: belgedeki "~N bin satır …"
  iddiası ölçümün binde yuvarlamasıyla, "N ADR" iddiası `docs/adr/` sayısıyla, "N+ test" iddiası
  gerçek toplamanın alt sınırıyla eşleşmeli. 400-satır listesi için: belgede `dosya NNN` diye yazılan
  her satır sayısı gerçek dosya satır sayısıyla **toleranssız** eşleşmeli (amaç tazelik).
- **Dosyalar:** `docs/ZAYIF_VE_GELISTIRILECEK_YONLER.md`, `tests/unit/test_release_readiness.py`.
- **Doğrulama:** yeni testler yeşil; mutasyon kanıtı: "~27 bin"→"~33 bin", "30 ADR"→"29 ADR" ve bir
  dosya satır sayısı kaydırıldığında ilgili test **kırmızı** olur; ağa çıkmaz; tam suite yeşil.
- **Boyut:** küçük-orta (~1-1,5 saat; ~8 satır belge + ~60 satır test).
- **Kaynak:** PROGRESS "Sonraya" (2026-10-18), `docs/ZAYIF_VE_GELISTIRILECEK_YONLER.md` s.399;
  kardeş iş: KALAN_ISLER.md iş 3 (README sayıları) ve iş 2 (Bulgular durum tazeleme).
- **Sonuç (2026-10-18):** uygulandı — belge ölçümle tazelendi: s.50/91 "3.300+ test" → **3.700+**,
  s.50/423 "29 ADR" → **30 ADR**, s.399 "~29/~28 bin" → **"~27 bin / ~39 bin satır"**, s.397-404
  dosya satırları (400 üstü **0**; en büyük `analysis/extractor.py` 396, `config.py` 390; bölünenler
  350/350/323) + `report/usage.py` 62 satır / yalnız `models/` → bağımlılık notu **kapandı** +
  "Sonraya" **46 açık / 120 madde**, §10 tabloda iki satır (400 satır: 3 → 0; Sonraya ~60 → 46).
  `tests/unit/test_release_readiness.py` **+4 test** (~70 satır): satır sayısı iddiaları (yuvarlama),
  "N+ test" (alt sınır) ve "N ADR" (eşitlik), `path.py NNN` (toleranssız), Sonraya açık madde sayısı
  (`- ~~` = kapalı). Mutasyon **5/5 kırmızı** ("~27"→"~33", 30→29 ADR, 396→397, 48→47 madde,
  "3.700+"→"9.999+"); belge bayt-bayt geri döndü (SHA-256).
- **Sapmalar (kayıt için):** (a) test sayısı iddiası "~38 bin" → **"~39 bin"**: yeni testler `tests/`
  satır sayısını **38 550**'ye çıkardı ve iş 3'ün yuvarlama testi 39 bekliyor; README'deki kardeş
  iddia da aynı gerekçeyle güncellendi. (b) "400 satırı aşan dosya" metriği belgede **boş satır hariç**
  olarak tanımlandı: toplam satırla `config.py` 492 / `extractor.py` 431 olurdu ve bu, belgedeki diğer
  (boş satır hariç) sayılarla tutarsız kalırdı; tablo satırı "0 (en büyük 396)" oldu.
  (c) "Sonraya" sayısı için **açık** madde sayısı raporlanıyor (belgede tanım yazılı); 48 → 46
  çünkü iş 4b/4c maddeleri bu turda kapandı.


### [x] 🤖 5. Statik kural kaçırmaları (madde başına bağımsız dilim) — ✅ **BİTTİ 2026-10-18**
- **Kapsam (tek tek yapılabilir):** CPP-OWN-001 akış duyarlılığı (erken `return`/istisna yolunda
  atlanan `delete` öneri değil **hata** sayılır, Faz 52 denetimi) · C-MEM-001 aynı dosyada başka
  fonksiyona geçirilen işaretçi (`print_arr(arr, n)`) sık kaçırma · UNITY-GC-001 dosyada tanımlı
  kullanıcı `struct`'ı için `new Hit(3)` yanlış bulgu (değer tipi) · UE-GC-001
  `TArray<AActor*>`/`TMap<…, UObject*>` kapsayıcı alanları + UCLASS olmayan sınıfta öneri metni ·
  C-MEM-003 kullanımdan sonra/yani yanlış dal ve koşullu korumanın ayırt edilmemesi · UNITY-GC-001
  closure bastırmasının satır bazlı olması.
- **Dosyalar:** `src/codementor/rules/*.py`, `tests/rules/` (pozitif+negatif fixture),
  `docs/rules-catalog.md`, gerekirse golden'lar (`tests/golden/…`, `--update-golden`).
- **Doğrulama:** her dilim için yeni fixture + test; golden'lar üretilir; tam suite yeşil.
- **Boyut:** orta (madde başına ~1-2 saat).
- **Kaynak:** PROGRESS "Sonraya" (CPP-OWN-001, C-MEM-001/003, UNITY-GC-001, UE-GC-001 satırları).
- **Sonuç (dilim 1 — CPP-OWN-001 akış duyarlılığı, 2026-10-18):** ✅ Davranış Faz H2'de zaten
  vardı, ama o gün yalnız 4 fixture'la sınanıyordu ve PROGRESS "Sonraya" kaydı "açık" gibi
  duruyordu. Fixture'lar genişletildi:
  `tests/rules/fixtures/CPP-OWN-001/positive/` altına **6 dosya** (`goto_skip`, `loop_break_skip`,
  `loop_continue_skip`, `nested_block_return` → `EXPECT_KIND: issue`; `loop_pair`,
  `jump_outside_pair` → `suggestion`) + `tests/rules/test_finding_kinds.py`'ye **3 birim test**
  (çift aralığının sınırları: `return` `new`'dan önce / `delete`'ten sonra; aynı dosyada iki türün
  birlikte çıkması — fixture'ın ifade edemediği durumlar).
- **Mutasyon kanıtı (dilim 1):** erken çıkış taraması devre dışı (`_skipped_deletes` → boş küme)
  → **7 kırmızı** (6 fixture + 1 birim test); aşırı duyarlı hâle getirilmiş (aralık yerine kapsamda
  herhangi bir atlama + lambda hariç tutması kaldırılmış) → **8 kırmızı** (yanlış pozitif
  koruyucuları: `lambda_between`, `other_scope_return`, `jump_outside_pair`, `new_delete` + 4 birim
  test). İki mutasyon da geri alındı: `src/codementor/rules/cpp.py` **değişmedi** (`git diff` boş).
- **Doğrulama (dilim 1):** `ruff check` temiz · `ruff format --check` 478 dosya · `mypy src/` 216
  dosya temiz · tam suite `pytest -m "not live"` **3868 geçti / 16 atlandı** (iş 4 sonrası 3859'dan
  +9 = 6 fixture vakası + 3 birim test) · testler ağa çıkmaz.
- **Sonuç (dilim 2 — C-MEM-001 okuyucu zinciri, 2026-10-18):** ✅ Gerçek kaçırma vardı: ödünç
  aktarımı tek geçişte yalnız ilk halkayı görüyordu, `report` → `show` → `dump` zincirinde bulgu
  çıkmıyordu. `rules/c.py` `_borrowers` artık sabit noktaya yakınsıyor (`_MAX_BORROW_ROUNDS = 8`;
  küme yalnız büyür, tur başına bir halka, dosya başına sabit sayıda gezinti — mimari §12).
  Yeni fixture'lar: `positive/passed_to_reader_chain.c` (2 halka), `positive/reader_defined_after.c`
  (okuyucu sonra tanımlı); bilinçli sınırlar `negative/helper_returns_derived_pointer.c`
  (`return v + i` sahiplik aktarımı), `negative/duplicate_helper_names.c` (`#ifdef` çift tanım),
  `negative/prototype_only_helper.c` (yalnız bildirim). `tests/rules/test_c_memory_flow.py`:
  4 test (1 halka, bütçe içi 6 halka, bütçeden derin zincir muhafazakâr, karşılıklı özyineleme
  sabit noktaya yakınsar). **Mutasyon:** sabit nokta tek geçişe indirilince **2 kırmızı**
  (`passed_to_reader_chain.c` + bütçe testi); geri alındı.
- **Sonuç (dilim 3 — UNITY-GC-001 closure bastırması, 2026-10-18):** ✅ Bastırma satır yerine
  **bayt aralığı** bazlı: LINQ lambdasının closure'ı olgularda artık ayrı `CLOSURE` değil
  (`analysis/extractor.py` `_without_linq_lambdas`; önek maksimumu + `bisect`, O(L log L + C log L)),
  `rules/unity.py`'deki satır kümesi ve `AllocationKind.LINQ` bağımlılığı kaldırıldı. Böylece aynı
  satırdaki LINQ dışı lambda **bulgu veriyor** (eskiden sessizce bastırılıyordu) ve LINQ lambdası
  çift raporlanmıyor. Yeni fixture `UNITY-GC-001/positive/closure_next_to_linq.cs`;
  `tests/unit/test_extractor.py`'ye olgu testi (`test_sibling_lambda_on_linq_line_is_still_a_closure`)
  + mevcut LINQ hot-path beklentisi güncellendi; `csharp-03`/`unity-03` facts golden'larında yalnız
  LINQ satırındaki `closure` kaydı düştü. **Mutasyon:** bütün closure'ları bastır → **2 kırmızı**;
  hiç bastırma → **3 kırmızı** (LINQ lambdası çift bulgu); ikisi de geri alındı.
- **Sonuç (dilim 4 — UE-GC-001 iç içe kapsayıcı, 2026-10-18):** ✅ `TMap<FName, TArray<UObject*>>`
  kaçırılıyordu: `_holds_uobject` artık `type_descriptor` sarmalayıcısını açıp
  `_MAX_CONTAINER_DEPTH = 2` katmana kadar iniyor (sınır hem karesel süreyi hem yapay iç içe girdide
  özyineleme taşmasını önlüyor). Yeni fixture'lar `UE-GC-001/positive/nested_container_fields.h`
  (iç içe iki katman + UPROPERTY'li olan hariç + sınırı aşan), `negative/gc_safe_wrappers.h`
  (`TWeakObjectPtr`/`TStrongObjectPtr`/`TSoftObjectPtr` sayılmaz) + `tests/rules/test_unreal_gc.py`'ye
  2 test. **Mutasyon:** katman sınırı 1'e indirilince **3 kırmızı**; geri alındı.
- **Sonuç (dilim 5 — C-MEM-003 denetim akışı, 2026-10-18):** ✅ Davranış Faz 57'de gelmişti
  (`src/` değişmedi); eksik kalan **biçimler** sabitlendi. Yeni fixture'lar:
  `positive/guard_before_allocation.c` (denetim tahsisten **önceyse** sayılmaz — aynı ad bir önceki
  tahsise aitti), `positive/guard_on_one_switch_path.c` (tek dallı denetim `default` yolunu
  kapatmaz), `positive/use_only_in_condition.c` (koşul içindeki ilk kullanım da kullanımdır),
  `negative/guard_forms_in_branches.c` (aynı `case` içi denetim, `do/while` + `break`, döngüde
  `continue`, `NULL == p`). `test_c_memory_flow.py`'ye 5 test: tahsis başına değerlendirme (aynı
  dosyada korumalı/korumasız tahsis), `if (!(p = malloc(..)))` biçimi, switch dalı, koşulda kullanım.
  **Mutasyon:** denetimin yol/konum ayrımı kaldırılınca **3 kırmızı**; geri alındı.
- **Not (kapsam):** dilim 3–4'ün düzeltmesi `src/codementor/rules/` yerine analiz katmanında
  (`analysis/extractor.py`, `analysis/_engine.py`) yapıldı: kaçırma orada üretilen olgulardan
  kaynaklanıyordu (closure'ın `CLOSURE` olarak ayrı sayılması, şablon argümanının yalnız ilk
  katmanının taranması). Dört kurala `catalog_note` eklendi; `docs/rules-catalog.md` `make
  rules-doc` ile üretildi (elle düzenlenmez).
- **Kalan dilimler:** yok — iş 5'in bütün maddeleri işlendi (CPP-OWN-001 dilim 1, C-MEM-001 dilim 2,
  UNITY-GC-001 dilim 3, UE-GC-001 dilim 4, C-MEM-003 dilim 5).

### [x] 🤖 6. Statik kapsam boşluklarını kapatacak yeni kurallar — ✅ **BİTTİ (Faz H1)**
- **Durum tespiti:** Kapsamda listelenen kurallar (`CSS-ACC-001`, `CSS-LAYOUT-001`, `CSS-LAYOUT-002`,
  `CPP-PERF-002`, `CPP-PERF-003`, `CPP-PERF-004`, `C-BUF-002`, `CS-ALLOC-001`) Faz H1'de (`faz/h-kurallar`)
  zaten eksiksiz uygulanmış, test edilmiş ve kataloğa işlenmiştir; `KALAN_ISLER.md` listesi hazırlanırken
  eski taslaktan sehven açık kopyalanmıştır.
- **Doğrulama:** `src/codementor/rules/` altında 41 kural eksiksiz; `docs/rules-catalog.md` senkron;
  `tests/rules/` fixture'ları yeşil.

### [x] 🤖 7. Kural bazında öneri türü + etiket/veri seti sürümü (Faz 36 açığı + Faz 51) — ✅ **BİTTİ 2026-10-20**
- **Kapsam:** kural bazında öneri türü (`CPP-OWN-001`, `UE-MEM-001`, `PY-RES-001`) Faz 52'de tamamlanmıştı;
  bu turda `RunConfig` modeline `dataset_version: str | None` alanı eklendi (`dataset_version` hash fonksiyonu);
  `eval compare` tablosuna `veri seti d1+...` dipnotu ve farklı sürümler karşılaştırılıyorsa uyarı eklendi;
  `eval analyze` ve `eval breakdown` komutlarına kayıtlı `dataset_version` ile diskteki etiketler uyuşmadığında
  sessiz yeniden puanlamayı engelleyen uyarı eklendi; `ExpectedFinding` modeline yapısal `boundary: str | None` alanı
  eklendi, `test_category_rules.py`'de desteklendi ve `cpp-009`'a `boundary: ownership_scope` işlendi.
- **Dosyalar:** `src/codementor/models/eval.py`, `src/codementor/eval/dataset.py`, `src/codementor/eval/runner.py`,
  `src/codementor/eval/compare.py`, `src/codementor/cli/eval.py`, `eval/dataset/dev/cpp-009/label.yaml`,
  `tests/unit/test_category_rules.py`, `tests/unit/eval/test_dataset_version.py`.
- **Doğrulama:** `tests/unit/eval/test_dataset_version.py` (8 test), `test_category_rules.py` (13 test),
  `tests/unit/eval/test_readme_table.py` (5 test), tam suite `pytest -m "not live"` 3927 geçti / 16 atlandı.
- **Sonuç:** uygulandı; `make check` eşdeğeri tüm testler ve linter/formatter temiz.

### [x] 🤖 8. Depolama borcu (Faz 49 Ü9 + `sessions` budama) — ✅ **BİTTİ 2026-10-20**
- **Kapsam:** eksik sütunlu eski şema (`OperationalError`) için `Database._migrate` fonksiyonuna
  `PRAGMA table_info` denetimi ve `ALTER TABLE` göçü eklendi (`SCHEMA_DB_VERSION = 2`); bozuk `created_at`
  için `cache._list_analyses_fallback` güvenli tekil çözümleme eklendi (`list_analyses` ve `list_analyses_page`
  çökmez); `sessions` tablosunun `updated_at`'e göre budanması (`prune_old_sessions`) Faz F'de zaten uygulanmıştı.
- **Dosyalar:** `src/codementor/storage/db.py`, `src/codementor/storage/cache.py`,
  `tests/unit/test_storage_migration.py`.
- **Doğrulama:** `tests/unit/test_storage_migration.py` (3 test) + `test_storage.py` (49 test yeşil).
- **Boyut:** orta.

### [x] 🤖 9. Faz F/G küçük açıkları — ✅ **BİTTİ 2026-10-20**
- **Kapsam:** **F10 denetiminin 3 küçük maddesi** kapatıldı:
  - `desktop/services.py`: `OLLAMA_MODEL_RE` model adının harf/rakamla başlamasını zorunlu kılacak
    şekilde sıkılaştırıldı (`^[A-Za-z0-9][A-Za-z0-9._:/-]*$`); `/x`, `../x`, `-flag`, `.hidden` reddedilir.
  - `desktop/services.py`: `run_ollama_pull` `result.error` ve `result.timed_out` dallarına birim testleri
    eklendi (`tests/desktop/test_connections.py`).
  - `ollama pull` iptal edilebilirliği: `run_ollama_pull`'a `cancel: threading.Event | None = None`
    parametresi eklendi, `result.cancelled` ele alındı; `ConnectionsController` içine `cancel_pull`
    ve iptal işareti desteği eklendi; `runtime.confirm_close` süren model indirmesini kontrol edecek şekilde
    genişletildi.
- **Doğrulama:** `tests/desktop/test_connections.py` (47 geçti), `test_app.py` (253 geçti), `ruff check`/`format`/`mypy` temiz.

### [x] 🤖 10. Faz I — eval altyapısı (canlı model ölçümü olmadan yapılabilen kısım) — ✅ **BİTTİ 2026-10-20**
- **Kapsam:** `select_part` parça atamasını kimlik özetiyle sabitleme (`part_signature`) · parçaların
  çakışmadığını ve eksik örnek bırakmadığını denetleyen `check_parts_coverage` · `eval compare` tablosuna
  parçalı koşularda çakışma durumunda uyarı dipnotu · `prompts/v1/fewshots/*.yaml` dosyalarında
  `additional_findings` listesine eksik `certainty: high` alanlarının işlenmesi ve golden prompt
  testlerinin güncellenmesi · LLM-as-judge ile Sokratik kalite skoru (`prompts/v1/judge.j2`,
  `src/codementor/eval/judge.py`, `eval judge` CLI komutu, `SocraticJudgeReport`, FakeProvider testleri).
- **Dosyalar:** `prompts/v1/judge.j2`, `src/codementor/eval/judge.py`, `src/codementor/eval/parts.py`,
  `src/codementor/eval/compare.py`, `src/codementor/cli/eval.py`, `src/codementor/models/eval.py`,
  `prompts/v1/fewshots/*.yaml`, `tests/golden/prompts/`, `tests/unit/eval/test_judge.py`,
  `tests/unit/eval/test_parts.py`.
- **Doğrulama:** `tests/unit/eval/test_judge.py` (7 test), `tests/unit/eval/test_parts.py` (23 test),
  `tests/golden/prompts/test_prompts_golden.py` (10 test), tüm `tests/unit/eval/` (132 test yeşil),
  `ruff check`/`format`/`mypy` temiz; testler ağa çıkmaz.
- **Boyut:** orta.

### [x] 🤖 11. Faz I — deterministik Sokratik kalite kapısı — ✅ **BİTTİ 2026-10-20**
- **Kapsam:** tekrar/döngü/koda değme denetimleri, karmaşıklık politikası, bulgu sağduyu denetimi,
  `small`/`standard` model profili, isteğe bağlı `pipeline.verify_provider`.
- **Dosyalar:** `src/codementor/verify/` (`sanity.py`, `complexity_policy.py`, `socratic_gate.py`),
  `src/codementor/pipeline/` (`socratic_pass.py`, `passes.py`, `orchestrator.py`, `verify_pass.py`, `llm_session.py`),
  `src/codementor/config.py`, `docs/adr/0031-kucuk-modeller-icin-deterministik-sokratik-kalite-kapisi.md`,
  `tests/unit/verify/` (`test_sanity.py`, `test_complexity_policy.py`, `test_socratic_gate.py`),
  `tests/integration/test_pipeline_small_model.py`.
- **Doğrulama:** FakeProvider ile uçtan uca küçük model profili testleri, 17 yeni birim/entegrasyon testi;
  tam test paketi 3957 test yeşil, `ruff check`, `ruff format`, `mypy --strict` temiz; testler ağa çıkmaz.
- **Boyut:** büyük (dilim dilim, ADR-0031 kabul edildi).

### [x] 🤖 12. Faz J havuzundan kod işleri — ✅ **BİTTİ 2026-10-20**
- **Kapsam:** zig budama (J2) betiği/spec'i (`src/codementor/validation/toolchain_prune.py`, `tools/prune_zig.py`, CI entegrasyonu) ·
  Tier 0 yalıtımında sıcak işçi havuzu (`src/codementor/validation/tier0_pool.py`, `tier0_worker.py --pool`, `tier0_warm_workers` config) ·
  CI Windows'ta MinGW g++ soğuk başlangıç ısınması + clang için `--target=x86_64-w64-mingw32` · `METHOD_LEAKS`'in 64 soru verisine
  taşınması (`Question.method_leaks`, `MENTOR_FIELDS`) · soru bankasına örnek giriş/çıkış alanı (`SampleIO`, `QuestionPublic.sample_io`, `UserQuestionDraft.sample_io`).
- **Dosyalar:** `src/codementor/validation/` (`toolchain_prune.py`, `tier0_pool.py`, `tier0_isolation.py`, `tier0_worker.py`, `toolchain.py`),
  `src/codementor/models/questions.py`, `data/questions/*.yaml` (64 dosya), `tools/prune_zig.py`, `.github/workflows/ci.yml`,
  `tests/unit/test_question_data.py`, `tests/unit/test_tier0_pool.py`, `tests/unit/test_toolchain_prune.py`, `tests/unit/test_toolchain.py`.
- **Doğrulama:** 142 birim testi (tüm soru testleri 81/81, tier0 havuz testleri 5/5, zig budama 5/5, toolchain 28/28);
  toolchain/CI adımları kodlandı, CI'da koşmaya hazır; `ruff check`, `ruff format`, `mypy --strict` temiz.
- **Boyut:** orta-büyük.

### [x] 🤖 13. Doküman tutarlılık turu (ikinci dalga) — ✅ **BİTTİ 2026-10-20**
- **Kapsam:** `docs/UYGULAMA_PLANI.md` yol haritası tablosu ve `docs/mimari.md` §20 ADR tablosunun
  güncel faz/ADR kümesiyle (31 ADR tam) eşlenmesi; `docs/rules-catalog.md` ↔ `src/codementor/rules/` kural
  listesi farkı (33 kural tam birebir); `docs/gelistirme-gunlugu/README.md` dizininin yeni dosyaları listelemesi.
- **Dosyalar:** `docs/UYGULAMA_PLANI.md`, `docs/mimari.md`, `docs/rules-catalog.md`,
  `docs/gelistirme-gunlugu/README.md`.
- **Doğrulama:** Betikle doğrulandı: 31/31 ADR tam eşleşiyor (fark 0), 33/33 kural tam eşleşiyor (fark 0),
  `test_release_readiness.py` 15/15 yeşil; `ruff check`, `ruff format`, `mypy --strict` temiz.
- **Boyut:** küçük-orta.

### Tam tarama (2026-10-20) kalan işleri
> Kaynak: ruff/mypy/pytest + kod-denetci tam taraması. #1 (sağduyu filtresi, `17b8242`), #3 (güvenilmeyen
> toml, `516ffc9`), #4 (karmaşıklık politikası, `395b1ea`) ve satır sayısı belgeleri kapandı. Kanıt ve
> satır numaraları: `PROGRESS.md` "Sonraya" → "Tam tarama kalan bulguları".

### [x] 🤖 14. Tier 0 sıcak işçi havuzunu güvenlik sınırına bağla (tarama #2 — **Yüksek**) — ✅ **BİTTİ 2026-10-20** (seçenek a, ADR-0032)
- **Sorun:** `tier0_pool.Tier0Worker` düz `subprocess.Popen` kullanıyor; `runner.run_process`'in bellek
  sınırı (Job Object/RLIMIT, `tier0_memory_mb`), ortam izin listesi (API anahtarları işçiye geçiyor), boş
  cwd ve `CREATE_NO_WINDOW` yok. Havuz boşken her istek yeni işçi açıyor → eşzamanlı işçi sınırsız.
  Yalnız `tier0_warm_workers > 0` iken etkin. Havuzun ADR'si yok (ADR-0025:58 hâlâ "Sonraya").
- **Karar (⏸ kullanıcı):** (a) işçiyi `runner`'ın sınır/ortam/Job Object yoluyla başlat + eşzamanlılık
  semaforu, ya da (b) havuzu varsayılan kapalı tut, açılınca uyar, ADR'de "güvenlik sınırı yok" diye yaz.
- **Aynı işte:** `close()` boruları kapatmıyor / `kill()` sonrası `wait()` yok (tutamak, POSIX zombi),
  `stderr=PIPE` okunmuyor · `str(exc)` kullanıcı kodu parçasını logluyor (§12) · `close_tier0_pool`
  hiçbir yerde çağrılmıyor, `get_tier0_pool` sonraki `max_workers`'ı yok sayıyor · hata mesajları
  `data/mentor_templates.yaml` önekiyle eşleşmiyor, `TIMEOUT/INFRA/FAILURE_MESSAGE` kullanılmıyor (ADR-0025 Ö2).
- **Dosyalar:** `src/codementor/validation/` (`tier0_pool.py`, `tier0_isolation.py`, `runner.py`),
  yeni ADR, `docs/mimari.md` §12/§16, `tests/unit/test_tier0_pool.py` (zaman aşımı, bellek, eşzamanlılık,
  pid ile yeniden kullanım).
- **Boyut:** orta-büyük.

### [x] 🤖 15. Sokratik kapı doğruluğu (tarama #5) — ✅ **BİTTİ 2026-10-20**
- **Sorun:** `verify/socratic_gate.py` `_LINE_REF_RE` "lineer"i ve rakamsız "satır"ı koda temas sayıyor
  (jenerik sorular kapıdan geçiyor); `has_repetition_loop` "0 0 0 0 0 0" gibi sayı dizilerini dejenerasyon
  sanıp tüm çıktıyı şablona düşürüyor; ADR-0031 4-gram diyor, kod 3/4/5. `pipeline/socratic_pass.py:73`
  kapı `passed=True` + uyarı döndüğünde soru listesi değişmemişse uyarılar kayboluyor.
- **Dosyalar:** `socratic_gate.py`, `socratic_pass.py`, `tests/unit/verify/test_socratic_gate.py`,
  gerekirse ADR-0031 notu.
- **Boyut:** küçük-orta.

### [x] 🤖 16. Web tip senkronu ve örnek giriş/çıkış gösterimi (tarama #6) — ✅ **BİTTİ 2026-10-20**
- **Sorun:** `web/src/types/question_public.ts` bayat (`sample_io`, `SampleIO` yok); API gönderiyor ama
  arayüz göstermiyor. Şema→TS kaymasını yakalayan test yok.
- **Kapsam:** `npm run gen:types`; soru panelinde örnekler; CI/test: `gen:types` sonrası `git diff --exit-code`.
- **Dosyalar:** `web/src/types/`, ilgili soru bileşeni + vitest, `.github/workflows/ci.yml`.
- **Boyut:** küçük.

### [x] 🤖 17. Test ağ korumasını Windows async yoluna genişlet (tarama #8) — ✅ **BİTTİ 2026-10-20**
- **Sorun:** `tests/network_guard.py` yalnız `socket.connect/connect_ex`'i yamalıyor; Windows Proactor
  `sock_connect` `_overlapped.ConnectEx` kullanıyor, DNS de engellenmiyor → respx'siz `httpx.AsyncClient`
  geliştirici makinesinde ağa çıkabilir (şu an böyle test yok).
- **Kapsam:** `loop.sock_connect` / `getaddrinfo` / `socket.create_connection` yamaları + async test.
- **Dosyalar:** `tests/network_guard.py`, `tests/unit/test_network_guard.py`. **Boyut:** küçük.

### [x] 🤖 18. Python Tier 1 uyarı yakalamasını iş parçacığı güvenli yap (tarama #9) — ✅ **BİTTİ 2026-10-20**
- **Sorun:** `validation/python_check.py:26` `warnings.catch_warnings` global durumu değiştiriyor;
  `asyncio.to_thread` ile eşzamanlı (API'de 4 yuva) → uyarılar kaybolur/başka analize düşer.
- **Kapsam:** kilit ya da `compile` uyarılarını alt süreçte/ayrı mekanizmayla toplamak + eşzamanlı test.
- **Boyut:** küçük.

### [x] 🤖 19. Eval yargıcı sağlamlığı (tarama #11) — ✅ **BİTTİ 2026-10-20**
- **Sorun:** `prompts/v1/judge.j2` `{{ code }}`/`{{ q }}` `guard`'sız ve ```` ``` ```` çitli (çit kırılır,
  model çıktısı yargıca talimat verebilir) · `judge.py` özel `_environment`'ı doğrudan çağırıyor,
  `TemplateError` → `PromptTemplateError` değil · `settings.prompts.dir` yok sayılıyor
  (`cli/eval.py:320`) · tek `ValidationError`/`ProviderError` tüm koşuyu düşürüyor · `judge_summary_markdown`
  `|`/satır sonunu kaçırmıyor.
- **Dosyalar:** `src/codementor/eval/judge.py`, `prompts/v1/judge.j2`, `src/codementor/cli/eval.py`, eval testleri.
- **Boyut:** küçük-orta.

### [x] 🤖 20. Codex iptalinde geçici dizin temizliği (tarama #7, doğrulandı) — ✅ **BİTTİ 2026-10-20**
- **Sorun:** `providers/codex_cli.py:195` `TemporaryDirectory` `ignore_cleanup_errors` olmadan; iptalde süreç
  0,1 sn daha yaşarken Windows WinError 32 → `PermissionError` `CancelledError`'ı maskeler, dizin sızar.
- **Kapsam:** `ignore_cleanup_errors=True` + süreç bitişini bekleme; iptal testi. **Boyut:** küçük.

### [x] 🤖 21. Düşük öncelikli tarama maddeleri (tek dilimde) — ✅ **BİTTİ 2026-10-20** (+ `root_path` API anahtarı atlaması)
- `api/guard.py` `RateLimiter._records` boşalan IP'leri silmiyor (sınırsız büyüme), `time.time()` yerine
  `time.monotonic()` · `docs/mimari.md:1126` "hız sınırı yok" ↔ kod varsayılan 30/dk (belge çelişkisi) ·
  `storage/db.py:53` göçle eklenen `sessions.updated_at` NULL → `prune_old_sessions` budamıyor ·
  `validation/toolchain_prune.py:140` `rmtree(ignore_errors=True)` silinemeyeni de "kaldırıldı" sayıyor ·
  `toolchain_prune.py:40` `PruneReport` `models/` dışında (AGENTS kod stili) · OLASI: `api/auth.py:61`
  `root_path` arkasında `/v1/` öneki, `desktop/bridge.py:165` `str(exc)[:300]` loglaması.
- **Boyut:** küçük (madde başına).

### [x] 🤖 22. Büyük dosyaları böl — ✅ **BİTTİ 2026-10-20**
- `src/codementor/config.py` boş olmayan **400** satırda (sınırda; öneri: katman/güven mantığı →
  `config_layers.py`). Testlerde 400'ü aşanlar: `desktop/test_app.py`, `unit/test_extractor.py`,
  `unit/test_models.py`, `providers/test_cli_agent.py`, `unit/test_toolchain_install.py`,
  `unit/test_storage.py`, `unit/test_bigo.py`, `rules/test_engine.py`, `desktop/test_connections.py`,
  `integration/test_pipeline.py` (toplama kimlikleri birebir korunmalı; J5 `test_tier1.py` örneği).
- `docs/ZAYIF_VE_GELISTIRILECEK_YONLER.md` dosya satırı iddiaları birlikte güncellenir. **Boyut:** orta.

### [x] 🤖 23. Satır sayısı testlerini kırılganlıktan çıkar — ✅ **BİTTİ 2026-10-20**
- `tests/unit/test_release_readiness.py` "~N bin satır" ve `path.py NNN` iddiaları neredeyse her kod
  değişikliğinde kırılıyor (bu taramada 3 kez). Öneri: bin yuvarlamasına ±1 tolerans ya da iddiaları
  belgeden kaldırıp ölçümü `make` hedefine bağlamak. **Boyut:** küçük.

## B. Yalnız kullanıcının yapabileceği işler

### [x] 👤 U1. `git push` — ✅ **2026-10-20** (`3ef973c..9a65052`, 105 commit)
- `main`, `origin/main`'in **yetmişin üzerinde** commit önünde (bu dosyanın kaydı sırasında 71; kesin
  sayı: `git rev-list --count origin/main..main`). Push olmadan CI ve release akışı yeni commit'leri
  görmez.

### [ ] 👤 U2. Y2 — referans çözüm karşılaştırması (**public öncesi zorunlu**)
- `tests/fixtures/llm_responses/unity03_reference.cs`, `private/` altındaki banka çözümüyle
  karşılaştırılır; aynı/benzer ise bankada olmayan yapay çözümle değiştirilir ve golden'lar
  yeniden üretilir (`--update-golden`). Ayrıntı: Bulgular §10 Faz A "Y2" kutusu.

### [ ] 👤 U3. P13 — GitHub repo ayarları
- secret scanning + push protection + Dependabot alerts açılır (`dependabot.yml` kodda hazır).

### [ ] 👤 U4. `v0.1.1` etiketi ve release
- Etiket atılınca `release.yml` otomatik çalışır (sürüm denetimi → test → exe → duman testi →
  `SHA256SUMS` → CHANGELOG bölümüyle release). Sürüm kaynağı `codementor.__version__` = 0.1.1.
- Not (2026-10-20): `v0.1.1` 3ef973c'de zaten atıldı ve release yayında; sonraki sürüm yeni etiket
  ister. Dependabot #1 ile `release.yml`'daki upload/download-artifact ana sürüm atladı — bu yol
  yalnız etiketle koşar, ilk etikette izlenmeli (bozulursa release oluşmaz, yarım yayın olmaz).

### [ ] 👤 U5. Canlı ölçümler ve elle denemeler
- agy canlı doğrulaması (oturum var) · Gemini/Codex/Claude canlı doğrulama (anahtar/kota) ·
  Claude Opus dev ölçümü (Faz 36/38 karşılaştırması) · Ollama yerel model ölçümü (Faz I tabanı) ·
  masaüstü elle deneme (Geçmiş → Tümünü temizle, Ctrl+S, başka dosya açma) · Linux/macOS
  "Oturum aç" · gerçek zig indirme/`güncelleme` akışı.

## C. Karar bekleyenler

- [x] ⏸ **P12:** `.agents/`, `.claude/` repoda kalacak mı → **kalıyor** (2026-10-20 incelendi:
  izin listesi, `private/` okuma yasağı, denetçi ajanı ve faz akışı; kişisel yol/anahtar yok;
  `BulgularVeDuzeltilecekler.md` §6).
- [x] ⏸ **P6 ikinci arşiv turu:** ✅ 2026-10-20 — 203 KB → 35 KB; notlar
  `docs/gelistirme-gunlugu/PROGRESS-faz-A-J.md`'de. Eski metin: `PROGRESS.md` 140 KB (Faz D'de 263 → 31 KB'ydı; E-J notlarıyla
  tekrar büyüdü). İstenirse E-J notları `docs/gelistirme-gunlugu/PROGRESS-faz-E-J.md`'ye taşınır,
  kökte "Durum" tablosu + son fazların özeti kalır.
- [x] ⏸ **Faz 18 etiket kararı:** ✅ Faz 21'de uygulanmıştı (`label.yaml` notları), 2026-10-20
  doğrulandı. Eski metin: `c-008`, `csharp-009` için Faz 17 bulgularının etiketlenmesi
  (kullanıcı kararı, Bulgular §10 Faz J).

## D. Kaynaklar ve tazeleme kuralı

- Bulgu kimlikleri ve ayrıntı: `docs/BulgularVeDuzeltilecekler.md` (§1 özet, §4 orta, §5 düşük,
  §6 public hazırlığı P1-P13, §8 eksik testler, §9 önerilen özellikler, §10 faz planı A-J).
- Faz notları: `docs/gelistirme-gunlugu/PROGRESS-faz-A-J.md` (A-K, iş 1-23); "Sonraya" (121
  madde, 42 açık): `PROGRESS.md`.
- Faz planı ve fazların kabul kriterleri: `docs/UYGULAMA_PLANI.md`.
- Bu dosya **yaşayan listedir**: iş bitince `[x]` yapılır + `PROGRESS.md`'ye işlenir; ayrıntılı
  gerekçe buraya kopyalanmaz, kaynağına bağlantı verilir.
- Kayıt tarihi: 2026-10-17 (Faz J5 sonrası tarama); iş 14-23 2026-10-20 tam taramasından eklendi.


