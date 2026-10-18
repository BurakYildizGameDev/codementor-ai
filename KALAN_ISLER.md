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

### [ ] 🤖 2b. §1 özet tablosunu §4/§10 kapanışlarıyla hizala
- **Kapsam (iş 2 sırasında ölçüldü):** §4 başlığında `✅ Faz X` olan ama §1 satırında kapanış etiketi
  bulunmayan bulgular — O3, O4, O5, O9, O12, O15, O16, O17 ve Y1, Y3, Y4, Y5, Y7, Y8, Y9 (O10/O13/O14
  iş 2'de yapıldı). Yalnız 6. kolona `Evet (Faz X)` eklenir; 5. kolon (Doğrulama) **değişmez**.
- **Dosyalar:** `docs/BulgularVeDuzeltilecekler.md` (yalnız).
- **Doğrulama:** her satır §4 başlığı ve §10 kutusuyla karşılaştırılır; satır sayısı sabit kalır.
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

### [ ] 🤖 4b. Zamanlama testlerini yük altında kırılgan olmaktan çıkar (O1-O4 + Tier 0 bütçesi)
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

### [ ] 🤖 4c. `docs/ZAYIF_VE_GELISTIRILECEK_YONLER.md` bayat sayıları tazele + teste bağla
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

### [ ] 🤖 6. Statik kapsam boşluklarını kapatacak yeni kurallar
- **Kapsam:** CSS (`outline:none` + focus göstergesi yok → CSS-CL-004, sabit `px` yükseklik taşması
  → CSS-CL-006, `position:absolute` + margin ile ortalama → CSS-CL-007) · C++ (döngüde
  `std::string +`/`+=`, döngüde `std::endl`, `reserve` yokken döngüde `push_back`) · C (genişliksiz
  `scanf("%s")`) · C# (döngüde `string +=`).
- **Dosyalar:** `src/codementor/rules/*.py`, `docs/rules-catalog.md`, `data/checklists/` (yalnız
  gerekiyorsa), `tests/rules/` fixture'ları.
- **Doğrulama:** kural başına pozitif/negatif fixture + test; katalog satırı; tam suite; varsa
  eval precision'ı etkilenmiyor.
- **Boyut:** orta-büyük (kural başına ~1 saat).

### [ ] 🤖 7. Kural bazında öneri türü + etiket/veri seti sürümü (Faz 36 açığı + Faz 51)
- **Kapsam:** doğru eşleşmiş `new`/`delete` → CPP-OWN-001, `Reserve` yok → UE-MEM-001, `with`
  dışı `open` → PY-RES-001; `RunConfig`'e etiket/veri seti özeti + `eval compare` dipnotu;
  etiketlerde serbest metin sezgisi yerine yapısal `boundary:` alanı; `memory_safety` uyumsuz
  örnekleri (dev `cpp-009`, `cpp-105`; test `cpp-006`).
- **Dosyalar:** `src/codementor/rules/`, `src/codementor/eval/`, `src/codementor/models/`,
  `eval/` veri seti, ilgili testler.
- **Doğrulama:** eski koşuların yeni etiketlerle **sessizce yeniden puanlanmadığı** testle
  sabitlenir; eval/Pydantic testleri + golden'lar yeşil.
- **Boyut:** orta-büyük.

### [ ] 🤖 8. Depolama borcu (Faz 49 Ü9 + `sessions` budama)
- **Kapsam:** eksik sütunlu eski şema (`OperationalError`) ve bozuk `created_at` için şema göçü /
  bozuk kaydı atlama; `list_analyses`'in bu durumlarda korunması; `sessions` tablosunun
  `updated_at`'e göre budanması (oturum başına bir satır, sınırsız büyüyor).
- **Dosyalar:** `src/codementor/storage/*.py`, `src/codementor/desktop/` (çağrı yerleri),
  `tests/unit/storage/`.
- **Doğrulama:** göç + bozuk DB testleri; mevcut storage testleri yeşil.
- **Boyut:** orta.

### [ ] 🤖 9. Faz F/G küçük açıkları
- **Kapsam:** **F10 denetiminin 3 küçük maddesi** (ör. `SequenceRunner` hata/zaman aşımı dallarına
  birim testleri, model adı doğrulaması) · `ollama pull` iptal edilebilirliği (köprüde
  `Cancellation`, arayüzde iptal düğmesi).
- **Dosyalar:** `tests/unit/` (SequenceRunner), `src/codementor/desktop/`, web arayüzü + testleri.
- **Doğrulama:** birim testleri; `pytest tests/desktop -q`; web tarafında tip kontrolü/derleme.
- **Boyut:** küçük-orta.

### [ ] 🤖 10. Faz I — eval altyapısı (canlı model ölçümü olmadan yapılabilen kısım)
- **Kapsam:** `select_part` parça atamasını kimlik özetiyle sabitleme · `eval breakdown`'a
  gecikme/token sütunları · HTML precision için bulgu ölçütü + kategori tanımları (yalnız dev) ·
  few-shot'lara `certainty` + Python few-shot örnekleri · LLM-as-judge iskeleti (prompt + şema +
  test, canlı puanlama kullanıcıda).
- **Dosyalar:** `src/codementor/eval/`, `prompts/v1/`, `tests/unit/eval/`.
- **Doğrulama:** FakeProvider ile testler; eval CLI testleri; ağa çıkmaz.
- **Boyut:** orta (madde başına küçük).

### [ ] 🤖 11. Faz I — deterministik Sokratik kalite kapısı
- **Kapsam:** tekrar/döngü/koda değme denetimleri, karmaşıklık politikası, bulgu sağduyu denetimi,
  `small`/`standard` model profili, isteğe bağlı `pipeline.verify_provider`.
- **Dosyalar:** `src/codementor/verify/` (yeni modül), `src/codementor/pipeline/`,
  `src/codementor/config/`, testler.
- **Doğrulama:** FakeProvider ile uçtan uca; küçük model profili testleri.
- **Boyut:** büyük (dilim dilim). **Not:** mimari sapma gerektirirse DUR → ADR önerisi (kural 1);
  bu iş büyük olasılıkla `docs/adr/ADR-0030+` gerektirir.

### [ ] 🤖 12. Faz J havuzundan kod işleri
- **Kapsam:** zig budama (J2) betiği/spec'i — **doğrulaması CI'da** (bu makinede gcc/clang/zig yok) ·
  Tier 0 yalıtımında sıcak işçi havuzu (~280 ms süreç açma maliyeti) · CI Windows'ta MinGW g++
  soğuk başlangıç süresi + clang için `--target=x86_64-w64-mingw32` · `METHOD_LEAKS`'in soru
  verisine taşınması · soru bankasına örnek giriş/çıkış alanı (öğretmen incelemesi hariç).
- **Dosyalar:** `src/codementor/toolchain/`, `src/codementor/validation/`,
  `src/codementor/questions/`, `data/questions/`, `.github/workflows/`.
- **Doğrulama:** birim testleri; toolchain/CI maddelerinde gerçek kanıt CI koşusundan gelir
  (yerelde doğrulanamaz → iş "kod hazır, CI bekliyor" olarak işaretlenir).
- **Boyut:** orta-büyük (madde başına değişken).

### [ ] 🤖 13. Doküman tutarlılık turu (ikinci dalga)
- **Kapsam:** `docs/UYGULAMA_PLANI.md` yol haritası tablosu ve `docs/mimari.md` §20 ADR tablosunun
  güncel faz/ADR kümesiyle eşlenmesi; `docs/rules-catalog.md` ↔ `src/codementor/rules/` kural
  listesi farkı; `docs/gelistirme-gunlugu/README.md` dizininin yeni dosyaları listelemesi.
- **Dosyalar:** ilgili `docs/` belgeleri.
- **Doğrulama:** betikle fark çıkarılır (kural kimlikleri, ADR numaraları); çıktı boş olana kadar
  belgeler düzeltilir.
- **Boyut:** küçük-orta.

## B. Yalnız kullanıcının yapabileceği işler

### [ ] 👤 U1. `git push`
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

### [ ] 👤 U5. Canlı ölçümler ve elle denemeler
- agy canlı doğrulaması (oturum var) · Gemini/Codex/Claude canlı doğrulama (anahtar/kota) ·
  Claude Opus dev ölçümü (Faz 36/38 karşılaştırması) · Ollama yerel model ölçümü (Faz I tabanı) ·
  masaüstü elle deneme (Geçmiş → Tümünü temizle, Ctrl+S, başka dosya açma) · Linux/macOS
  "Oturum aç" · gerçek zig indirme/`güncelleme` akışı.

## C. Karar bekleyenler

- [ ] ⏸ **P12:** `.agents/`, `.claude/` repoda kalacak mı (kalması önerildi; bilinçli karar
  `BulgularVeDuzeltilecekler.md` §6'ya yazılır).
- [ ] ⏸ **P6 ikinci arşiv turu:** `PROGRESS.md` 140 KB (Faz D'de 263 → 31 KB'ydı; E-J notlarıyla
  tekrar büyüdü). İstenirse E-J notları `docs/gelistirme-gunlugu/PROGRESS-faz-E-J.md`'ye taşınır,
  kökte "Durum" tablosu + son fazların özeti kalır.
- [ ] ⏸ **Faz 18 etiket kararı:** `c-008`, `csharp-009` için Faz 17 bulgularının etiketlenmesi
  (kullanıcı kararı, Bulgular §10 Faz J).

## D. Kaynaklar ve tazeleme kuralı

- Bulgu kimlikleri ve ayrıntı: `docs/BulgularVeDuzeltilecekler.md` (§1 özet, §4 orta, §5 düşük,
  §6 public hazırlığı P1-P13, §8 eksik testler, §9 önerilen özellikler, §10 faz planı A-J).
- Faz notları ve "Sonraya" (~60 madde): `PROGRESS.md`.
- Faz planı ve fazların kabul kriterleri: `docs/UYGULAMA_PLANI.md`.
- Bu dosya **yaşayan listedir**: iş bitince `[x]` yapılır + `PROGRESS.md`'ye işlenir; ayrıntılı
  gerekçe buraya kopyalanmaz, kaynağına bağlantı verilir.
- Kayıt tarihi: 2026-10-17 (Faz J5 sonrası tarama).


