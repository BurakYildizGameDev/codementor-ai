# İlerleme Günlüğü

> Faz 0-63'ün ayrıntılı notları ve eski yol haritası arşivde: [docs/gelistirme-gunlugu/PROGRESS-faz-0-63.md](docs/gelistirme-gunlugu/PROGRESS-faz-0-63.md). Yeni fazların notları buraya eklenir (AGENTS.md faz bitirme protokolü).
>
> Kalan işlerin işaretli listesi (🤖 ajan / 👤 kullanıcı / ⏸ karar ayrımıyla):
> [KALAN_ISLER.md](KALAN_ISLER.md) — 2026-10-17 Faz J5 sonrası tarama. Bir iş bitince orada `[x]`
> yapılır ve buraya işlenir.

## Durum
| Faz | Durum | Dal | Tarih | Araç (uygulayan / denetleyen) |
|---|---|---|---|---|
| 0 | ✅ | faz/0-iskelet | 2026-09-29 | Claude Code / — |
| 1 | ✅ | faz/1-modeller | 2026-09-29 | Claude Code / — |
| 2 | ✅ | faz/2-soru-bankasi | 2026-09-29 | Claude Code / — |
| 3 | ✅ | faz/3-tier0 | 2026-09-29 | Claude Code / kod-denetci |
| 4 | ✅ | faz/4-tier1 | 2026-09-29 | Claude Code / kod-denetci |
| 5 | ✅ | faz/5-olgular | 2026-09-29 | Claude Code / kod-denetci |
| 6 (daraltılmış) | ✅ | faz/6-kurallar | 2026-09-29 | Claude Code / kod-denetci |
| 7 | ✅ | faz/7-saglayicilar | 2026-09-29 | Claude Code / kod-denetci |
| 8 | ✅ | faz/8-promptlar | 2026-09-30 | Claude Code / kod-denetci |
| 9 | ✅ | faz/9-dogrulayici | 2026-09-30 | Claude Code / — |
| 10 | ✅ | faz/10-pipeline | 2026-09-30 | Claude Code / — |
| 11 | ✅ | faz/11-api | 2026-09-30 | Claude Code / — |
| 12 | ✅ | faz/12-eval | 2026-09-30 | Claude Code / — |
| 13 | ✅ | faz/13-sunum | 2026-09-30 | Claude Code / — |
| 14 | ✅ | faz-14-masaustu | 2026-10-01 | Claude Code / — |
| 15 | ✅ | faz-15-baglantilar | 2026-10-01 | Claude Code / — |
| 16 | ✅ | faz-16-diller | 2026-10-01 | Claude Code / — |
| 17 | ✅ | faz/17-kurallar | 2026-10-01 | Claude Code / kod-denetci |
| 18 | ✅ | faz/18-eval-diller | 2026-10-01 | Claude Code / kod-denetci |
| 19 | ✅ | faz/19-durdur | 2026-10-01 | Claude Code / kod-denetci |
| 20 | ✅ | faz/20-html-denge | 2026-10-01 | Claude Code / kod-denetci |
| 21 | ✅ | faz/21-kural-dogrulugu | 2026-10-01 | Claude Code / kod-denetci |
| 23 | ✅ | faz/23-dagitim-yollar | 2026-10-01 | Claude Code / — |
| 24 | ✅ | faz/24-masaustu-kullanilabilirlik | 2026-10-01 | Claude Code / — |
| 25 | ✅ | faz/25-saglayicilar | 2026-10-02 | Claude Code / — |
| 26 | ✅ | faz/26-api-web | 2026-10-02 | Claude Code / — |
| 27 | ✅ | faz/27-saglamlik | 2026-10-02 | Claude Code / — |
| 22 | ✅ | faz/22-eval-precision, faz/22b-precision | 2026-10-02 | Claude Code / — |
| 28 (Codex) | ✅ | faz/28-cli-ajanlari | 2026-10-02 | Claude Code / — |
| 34 + 35B | ✅ | faz/34-eval-genisletme | 2026-10-03 | Claude Code / — |
| 37 | ✅ | faz/37-saglayici-sadelestirme | 2026-10-03 | Claude Code / — |
| 36 | ✅ | faz/36-hata-oneri | 2026-10-04 | Claude Code / — |
| 38 | ✅ Claude 96 ölçümü 2026-10-05 (77/88/82) | faz/36-hata-oneri | 2026-10-05 | Codex / Claude Code |
| 39 | ✅ (`cpp-007` canlıda doğrulandı) | faz/39-dogrulama-performans | 2026-10-04 | Claude Code / kod-denetci |
| 47 | ✅ | faz/47-api-guven-siniri | 2026-10-05 | Claude Code / — |
| 48 | ✅ | faz/48-rol-siniri-sure | 2026-10-05 | Claude Code / — |
| 49 | ✅ | faz/49-depolama-tutarlilik | 2026-10-05 | Claude Code / — |
| 50 | ✅ | faz/50-dil-kodlama-ci | 2026-10-05 | Claude Code / — |
| 51 | ✅ | faz/51-kategori | 2026-10-05 | Claude Code / — |
| 52 | ✅ (denetim düzeltmesiyle) | faz/52-kural-oneri | 2026-10-05 | Mimo (Cline) / Claude Code |
| 53 | ✅ (birleştirme kullanıcıda) | faz/53-54-kapsama-bolumleme | 2026-10-05 | Mimo (Cline) / Claude Code |
| 54 | ✅ | faz/53-54-kapsama-bolumleme | 2026-10-05 | Mimo (Cline) / Claude Code |
| 55 | ✅ (ADR-0024) | faz/55-tier0-saglamlik | 2026-10-06 | GLM (Cline) / Claude Code |
| 56 | ✅ | faz/56-html-std003-kenarlar | 2026-10-06 | Claude Code / kod-denetci |
| 57 | ✅ | faz/57-c-mem003-akis | 2026-10-06 | Claude Code / kod-denetci |
| 58 | ✅ | faz/58-toolchain-test-kararlilik | 2026-10-06 | Claude Code / — |
| 59 | ✅ (ADR-0025) | faz/59-tier0-alt-surec | 2026-10-06 | Claude Code / kod-denetci |
| 60 | ✅ | faz/60-surum-uyumu | 2026-10-06 | Antigravity / — |
| 61 | ✅ (ADR-0026) | faz/61-ipucu-merdiveni | 2026-10-07 | Antigravity / — |
| 62 | ✅ | faz/62-gecmis-silme | 2026-10-07 | Antigravity / — |
| 63 | ✅ | faz/63-agy-haiku-canli | 2026-10-09 | Claude Code / — |
| A1 | ✅ (denetim sonraya) | faz/a1-guvenlik | 2026-10-12 | Claude Code / — |
| A2 | ✅ (denetim sonraya) | faz/a2-guvenlik | 2026-10-13 | Claude Code / — |
| B | ✅ (denetim sonraya) | faz/b-bulgu-kaybi-onbellek | 2026-10-13 | Claude Code / — |
| K | ✅ (ADR-0028) | faz/k-kullanici-soru-token | 2026-10-13 | Claude Code / — |
| C | ✅ (denetim sonraya) | faz/c-ipucu-yapilandirma | 2026-10-13 | Claude Code / — |
| E | ✅ | faz/e-web | 2026-10-13 | Antigravity / — |
| F | ✅ (elle deneme + denetim sonraya) | faz/f-masaustu | 2026-10-14 | Antigravity / — |
| G | ✅ | faz/g-saglayici | 2026-10-16 | Cline / — |
| H | ✅ (denetim + Önemli-3 düzeltmesi + entegrasyon testleri) | faz/h-kurallar (+ faz/h-denetim, faz/h-pragma-izin) | 2026-10-17 | Cline / Claude Code denetimi |
| J | ✅ (yalnız anlık görüntü maddesi; Zig budama bilinçli atlandı) | faz/j-checklist-snapshot | 2026-10-17 | Cline / — |
| J4 | ✅ (O3 kapanışı; kaynak kod değişti) | faz/j4-onbellek-surumu | 2026-10-17 | Cline / — |
| J5 | ✅ (Faz J denetimi küçük maddeleri; test-only) | faz/j5-test-hijyeni | 2026-10-17 | Cline / — |
| I (dilim 1) | ✅ (yargıç + parçalar + fewshot) | faz/i-eval-altyapi | 2026-10-20 | Antigravity / — |

## Kod — Tam tarama işleri (KALAN_ISLER 14-19; 2026-10-20)

**İş 14 — Tier 0 sıcak işçi havuzu güvenlik sınırında (ADR-0032, seçenek a):** `Tier0Worker` artık
`runner`'ın `ProcessTree` (Windows askıda başlat + Job Object, fail-closed), `sanitized_env`,
`launch_argv` (POSIX rlimit) parçalarıyla, ömrü boyunca yaşayan boş geçici cwd'de ve `stderr`
atılarak başlıyor. POSIX CPU sınırı birikimli olduğundan işçi 100 istekte geri dönüştürülüyor.
Canlı işçi sayısı semaforla sınırlı; hepsi meşgulse `try_check_syntax` `None` → aynı sınırlarla soğuk
yol. Mesajlar soğuk yolla ortak (`TIMEOUT/FAILURE/INFRA_MESSAGE`), loglarda yalnız hata türü. `close()`
stdin'i kapatıp bekliyor, gerekirse ağacı öldürüyor, boruları + Job Object'i kapatıyor; `get_tier0_pool`
ayar değişince yeniden kuruyor, `atexit` ile kapanıyor. `runner._Tree`/`_launch_argv` → `ProcessTree`/
`launch_argv`, `tier0_isolation._stopped` → `stopped_result`. **Testler:** `test_tier0_pool.py` 5 → 14
(ortam/cwd/Job Object sandbox, gerçek bellek sınırı — ADR-0024 bombası 1024 MB'de ~2 sn'de durdu, eski
havuzda ~4,2 GB alıp geçerdi —, fail-closed başlatma, pid yeniden kullanımı, bütçe ile geri dönüşüm,
süre aşımı, işçi hatası, ölü işçi, işçi sınırı, meşgulken soğuk yol, ayar değişince yeniden kurulum).
Belgeler: ADR-0032, ADR-0025 sonuç satırı, `mimari.md` §5.2/§12/§16/§20, ADR sayısı 31 → 32.

**İş 15 — Sokratik kapı doğruluğu:** `_LINE_REF_RE` rakam istiyor ("12. satır", "satır 12",
"line 8", "3-5. satırlar"); "lineer", "Hangi satır?" artık koda temas sayılmıyor (small profilde jenerik
sorular kapıdan geçiyordu). `has_repetition_loop` yalnız rakamlardan oluşan n-gram'ları saymıyor
("0 0 0 …" girdi örneği tüm çıktıyı şablona düşürüyordu). `socratic_pass.apply_gate` (saf yardımcı):
kapı geçip uyardığında uyarı soru listesi değişmese de rapora taşınıyor (eskiden atılıyordu).
ADR-0031 Karar 1'e tarihli not (n-gram boyu 3/4/5 kodla hizalandı). **Testler:** `test_socratic_gate.py`
+3 (11 parametreli vaka), yeni `test_socratic_pass_gate.py` (4); eski kodla 4 vaka kırmızı.

**İş 16 — Web tipleri ve soru ayrıntısı:** `npm run gen:types` (`question_public.ts`'e `sample_io` /
`SampleIO`; CI'nin `git diff --exit-code -- src/types` adımı push'ta kırılırdı). Arayüz seçili sorunun
metnini hiç göstermiyordu: yeni `QuestionDetails` kartı (başlık, metin, kısıtlar, örnek girdi/beklenen
çıktı + açıklama) yan panelin başında. **Testler:** `QuestionDetails.test.tsx` (3); web 54 → 57 test,
`tsc` ve `vite build` temiz. Playwright e2e bu makinede koşulmadı (CI'da koşar).

**İş 17 — Test ağ koruması Windows async yolu:** Proactor döngüsü `sock_connect`'i `socket.connect`
yerine `IocpProactor.connect` → `_overlapped.ConnectEx` ile yapıyordu; respx'siz `httpx.AsyncClient`
Windows'ta ağa çıkabilirdi. `tests/network_guard.guarded_patches()` artık bu yolu (Windows) ve
`socket.getaddrinfo`'yu (loopback adı / IP literali dışı ad → DNS sızıntısı) da yamalıyor;
`conftest._no_network` hepsini uyguluyor. **Testler:** `test_network_guard.py` +4 test + 8 vaka
(async dış bağlantı düşer, async loopback serbest, DNS engelli, yerel çözümleme serbest). Tam paket
4028 test yeşil: hiçbir mevcut test DNS'e ya da dış ağa çıkmıyormuş.

## Kod — Tam tarama bulgusu #4: karmaşıklık politikası tutarsız rapor üretiyordu (2026-10-20)

**Sorun:** `verify/complexity_policy.py` küçük profilde zamanı statik ipucuyla değiştirirken
`display_time`'ı ham `O(n^2)` yazıyordu (normal yol `parse_bigo(...).display` → `O(n²)`) ve
`is_optimal`'ı modelin eski zamanına göre bırakıyordu: model `n` (optimal), ipucu `n^2` → rapor
"O(n^2), optimal".

**Yapılanlar:** Gösterim ve gerekçe notu `parse_bigo(...).display`; `is_optimal` ipucundan
`verify/complexity.is_optimal` ile yeniden hesaplanıyor (normal yol ve `degraded_complexity` ile aynı);
`passes.py` sorunun `expected`'ını geçiriyor. **Bilinçli karar:** `agreement="agrees"` korundu (zaman
artık ipucunun kendisi; çatışma notta ve `meta.warnings`'te), `confidence` analiz geneli skor olduğu
için değişmedi, `optimal_time_target` modelin iddiası olarak kaldı.

**Testler:** `test_complexity_policy.py` 3 → 7 (gösterim, iki yönde optimallik, sorusuz `None`);
eski kodla 4 kırmızı. `README`/`ZAYIF` "~28 bin satır kaynak" → **~29 bin** (ölçüm 28 506).

## Kod — Tam tarama bulgusu #3: güvenilmeyen toml geçmişi budayabiliyordu (2026-10-20)

**Sorun:** ADR-0029 listesi `storage`'da yalnız `db_path`'i, `data`'da yalnız `user_questions_dir`'i
engelliyordu. Öğrenci projesindeki `[storage] max_analyses = 1` global veritabanındaki tüm geçmişi,
`session_retention_days = 1` ipucu merdivenini budayabiliyordu; `data.checklists_dir` (prompt'a
`guard`'sız giren maddeler), `mentor_templates_file` (öğrenciye gösterilen metin) ve
`verify.common_identifiers_file` (sızıntı denetimini körleştirebilir) serbestti.

**Yapılanlar:** `config._UNTRUSTED_SECTION_KEYS` → `storage` bölümünün tamamı, `data`'nın tüm yol
alanları (`frozenset(DataSettings.model_fields)`: yeni veri yolu da kendiliğinden engellenir),
`verify.common_identifiers_file`. `config.py` boş olmayan **400** satırda (sınırda; bir sonraki
eklemede bölünmeli — ör. katman/güven mantığı `config_layers.py`'ye). ADR-0029 Karar 3 listesi tarihli notla genişletildi
(sapma değil, gerekçe aynı); `mimari.md` §17 cümlesi güncellendi. `CODEMENTOR_CONFIG_FILE` ile verilen
dosya bu ayarları hâlâ değiştirebilir.

**Testler:** `test_audit_fixes_unit.py` +2: güvenilmeyen katman beş anahtarı yok sayar, stderr'de adıyla
listeler, aynı dosyadaki güvenli `verify.leak_ngram_n` uygulanır; açık dosyada `max_analyses == 1`.
Eski kodla ilk test kırmızı.

## Kod — Tam tarama bulgusu #1: sağduyu filtresi geçerli bulguları siliyordu (2026-10-20)

> Tam tarama (ruff/mypy/pytest + kod-denetci) sonrası en acil madde. Kalan bulgular "Sonraya"da.

**Sorun:** `verify/sanity.py` ters denetim filtresi (ADR-0031 Karar 2) kanıtta *gerçek denetim*
değil herhangi bir `<`, `>`, `==`, `null`, `None` arıyordu; baştaki `\b` tüm alternatiflere
uygulandığından sonuç boşluğa bağlıydı. `for(int i=0;i<=n;i++)`, `cout<<a[n];`,
`while(i<n) … a[i+1]` kanıtlı "sınır kontrol edilmiyor" bulguları **tüm profillerde** düşüyordu;
aynı satır boşluklu yazılınca korunuyordu. Ters yönde `elif n <= 0:` gerçek denetimi kaçırılıyordu.

**Yapılanlar:** Kalıp ADR metnine çekildi: yalnızca `if` / `else if` / `elif` / `assert`
(`Debug.Assert` dahil). Eşleşmeden önce dize/karakter sabitleri ve yorumlar (`//`, `/* */`, `#`)
siliniyor; `printf("if …")`, `// if n is 0`, `ifstream` denetim sayılmıyor. İmza ve profil
davranışı aynı; ADR sapması yok. `test_regex_budget` ilk sürümü yakaladı (kapanmayan `/*` 2,1 sn,
`"\` zinciri 3,1 sn — karesel): kapanışlar isteğe bağlı yapıldı (dize satır sonunda, blok yorum
metin sonunda biter) → bütçe içinde.

**Testler:** `tests/unit/verify/test_sanity.py` 4 → 22 (10 korunmalı + 7 düşürülmeli parametreli vaka,
standard profilde sıkışık taşma bulgusunun korunduğu bir `apply_sanity_checks` testi). Eski kodla
11 vaka kırmızı, yeni kodla 22/22 yeşil.

## Belge — Kalan işler listesi ve sayı tazeleme (doküman-only; 2026-10-17)

> Faz J5 kapanışından sonra yapılan "yapılması gerekenler" taramasının çıktısı kayda geçirildi.
> Kaynak kod **değişmedi**: `KALAN_ISLER.md` (yeni) + `PROGRESS.md` işaretçileri.

**Yapılanlar:** `KALAN_ISLER.md` eklendi — 13 ajan işi (🤖), 5 kullanıcı işi (👤) ve 3 karar bekleyen
(⏸) madde; her maddede kapsam, dokunulacak dosyalar, doğrulama ve boyut var. Yeni fikirlerin akışı
netleşti: fikir önce buradaki "Sonraya" bölümüne, iş sırası/kabul kriteri `KALAN_ISLER.md`'ye.
Tarama sırasında ölçülen gerçekler de kayda geçirildi: **ADR 30** (`README.md` s.42/s.150 ve
`README.en.md` s.43 hâlâ 29 diyor), `src/` **27 740** satır (iş 3'ün derin doğrulamasında
binary varlıklar hariç tutuldu → **27 194**) / `tests/` **37 595** satır
(`README.md` s.480 "~28 bin satır test (~29 bin satır kaynak koda karşı)" diyor → sayılar ters),
`pytest -m "not live"` **3758** geçti.

**Doğrulama:** `ruff check` temiz · `ruff format --check` 477 dosya · `pytest -m "not live"`
3758 geçti / 16 atlandı (doküman değişikliğinden önceki tam koşu) · yeni dosyada CR=0 ve blob
boyutu çalışma kopyasıyla aynı (LF, `.gitattributes` `eol=lf`).

**Açık:** tazelemenin kendisi (README sayıları, `BulgularVeDuzeltilecekler.md` §6/§10) henüz
uygulanmadı → `KALAN_ISLER.md` iş 1-2; `git push` ve Y2 kullanıcıda.

## Belge — README sayı tazeleme (KALAN_ISLER.md iş 1; doküman-only; 2026-10-17)

> P7 kapandı. Kaynak kod **değişmedi**: `README.md`, `README.en.md`, `KALAN_ISLER.md`.

**Yapılanlar:** `README.md` s.13 badge `testler-3300%2B` → `testler-3700%2B` · s.42 "3.300+ test …
29 ADR" → "3.700+ test … 30 ADR" · s.150 "29 kayıt" → "30 kayıt" · s.480 "~28 bin satır test
(~29 bin satır kaynak koda karşı)" → "~38 bin satır test (~28 bin satır kaynak koda karşı)"
(ölçüm (iş 1 anı): izlenen tüm dosyalarda boş olmayan satır — `src/` 27 740, `tests/` 37 595,
`web/` 6 139; iş 3'te yöntem **metin dosyaları** olarak netleşti → `src/` 27 194) · s.485-486 faz listesi "Faz A-D ve K" → "Faz A-H ve
J"; `README.en.md` s.43 "3,300+ tests … 29 ADRs" → "3,700+ tests … 30 ADRs". Diğer sayı iddiaları
ölçülüp **doğru** çıktı: 41 statik kural (katalog ve registry 41), 166 eval örneği (dev 96 / test
70), 60'tan fazla faz.

**Doğrulama:** eski kalıplar taraması temiz (`3300`, `3.300`, `3,300`, `29 ADR`, `29 kay`, `28 bin
satır test`, `Faz A-D` hiçbirinde yok) · `ruff check` temiz · `ruff format --check` 477 dosya ·
`pytest -m "not live"` **3758 geçti**, 16 atlandı, 6 seçilmedi (4:52) · iki README'de CR=0 ve blob
boyutu çalışma kopyasıyla aynı (LF).

**Düzeltme (2026-10-18):** (a) bu bölümde önce kaydedilen `src/` değeri **28 369 yanlıştı**; aynı
yöntemle yeniden ölçüldü → **27 740** (`tests/` 37 595 ve `web/` 6 139 birebir tutuyor).
(b) Faz listesi iş 3'ün testiyle ölçülünce **K**'nın atlandığı çıktı → `README.md` s.485-486 artık
**"… Faz A-H, J ve K"** (aşağıdaki iş 3 bölümü). (c) İş 3'ün derin doğrulamasında `src/`
sayımının `desktop/assets/` altındaki 3 binary dosyayı (ico/png) metin gibi saydığı çıktı (546
sahte satır): yöntem **metin dosyaları** olarak netleşti → `src/` **27 194**, bu yüzden README'nin
kaynak iddiası "~28 bin" → **"~27 bin"** (aşağıdaki iş 3 bölümü).

**Açık:** aynı sayıların tekrar bayatlamasını önleyen test iş 3'te → **iş 3 tamamlandı**;
`BulgularVeDuzeltilecekler.md` §6/§10 tazelemesi iş 2'de → **iş 2 tamamlandı**.

## Belge — Bulgular durum tazeleme (KALAN_ISLER.md iş 2; doküman-only; 2026-10-17)

> Kaynak kod **değişmedi**: `docs/BulgularVeDuzeltilecekler.md` (+20/−19), `KALAN_ISLER.md`, `PROGRESS.md`.

**Not (düzeltme):** iş 2'yi kaydederken iş 1 sırasında yanlışlıkla değiştirilen `## Faz J5` başlığı
geri kondu (aynı düzenlemede düzeltildi; J5 gövdesi başlıksız kalmıştı).

**Yapılanlar (19 parça, atomik betikle — her parça tek eşleşme doğrulandı):** §1'de O10/O13/O14
satırlarına kapanış etiketi `Evet (Faz F)`; §4'te bu üç başlığa `✅ Faz F`; §6 P-tablosu yenilendi —
P5 ✅ (belgeler `docs/gelistirme-gunlugu/` altında), P6 ✅ (252 KB → 146 KB; arşiv 224 KB), P7 ✅ (Faz D
+ 2026-10-17 tazeleme), P8 ✅ `README.en.md`, P9 ✅ dört dosya + `.github` şablonları, P10 ⚠️ kısmi
(yerel `v0.1.1` etiketi var; GitHub Release + zip yüklemesi kullanıcıda), P11 ✅ (13/16 Ekim derlemeleri,
`codementor.toml` yok), P12 ✅ bilinçli karar, P13 ℹ️ açık (kullanıcı), P4 ❓ Y2 açık; §10 Faz D'de P11
kutusu `[x]` + eski Faz 60 elle doğrulaması kullanıcıya devredildi (U5).

**Doğrulama:** dosya varlıkları (`README.en.md`, `SECURITY.md`, `CONTRIBUTING.md`, `CHANGELOG.md`,
`docs/gelistirme-gunlugu/` 10 dosya, `dist/CodeMentor-0.1.1-win64.zip`) · `git tag` → `v0.1.0`, `v0.1.1` ·
`pytest tests/unit/test_release_readiness.py` **6 geçti** · `ruff check` temiz · `ruff format --check`
477 dosya · dosyada CR=0 (LF) · eski kalıplar (`252 KB`, `59 fazda`, `P11 (yerel)`) kalmadı.

**Kararlar/sapmalar:** (1) P6'da spec "140 KB" diyordu; ölçülen değer yazıldı (146 KB / 142,6 KiB).
(2) §1 lejantı gereği 5. kolon "Doğrulama" = bulgunun **tespit yöntemi** (✅ elle doğrulandı · 🔬 ajan ·
📖 kod okuması · ❓ doğrulanmadı); bu yüzden O10/O13/O14'te 📖 korundu, kapanış 6. kolona yazıldı.
(3) §10 P11 tek kutu iken derleme ve elle doğrulama ayrıldı.

**Açık:** iş 2b (iş 2 sırasında ölçülen §1 kayması: O3, O4, O5, O9, O12, O15-O17 ve Y1, Y3-Y9
satırlarında kapanış etiketi yok) sırada; iş 3 (sayıları teste bağlama) → **tamamlandı**.

## Belge — Sayı iddialarını teste bağlama (KALAN_ISLER.md iş 3; 2026-10-18)

> `README.md` (2 satır) + `tests/unit/test_release_readiness.py` (+136 satır). Kaynak kod (`src/`) değişmedi.

**Yapılanlar:** `tests/unit/test_release_readiness.py` içine 4 test + 5 yardımcı eklendi:
(1) `test_readme_adr_claims_match_adr_directory` — TR "30 ADR" / "(docs/adr/, 30 kayıt)" ve EN
"30 ADRs" iddiaları `docs/adr/*.md` sayısına eşit. (2) `test_readme_test_count_claims_are_lower_bounds`
— badge `3700+`, "3.700+ test" ve EN "3,700+ tests" iddiaları gerçek toplama sayısının **alt sınırı**
(toplam alt süreçte: `pytest tests --collect-only -q -m "not live"`, ~7 sn, `lru_cache` ile tek koşu;
şu an 3774). (3) `test_readme_line_count_claims_match_measurement` — "~38 bin satır test (~27 bin
satır kaynak koda karşı)" iddiası ölçümün binde yuvarlamasıyla aynı (`git ls-files` + **metin**
dosyalarında boş olmayan satır; binary varlıklar NUL baytıyla atlanır, `git` yoksa test atlanır);
`test_line_count_measurement_skips_binary_assets` bu atlamayı ayrıca kanıtlar (sayılsalardı +546
sahte satır). (4) `test_readme_phase_claims_match_progress` — README'nin
"(Faz 0-63, ardından public öncesi Faz A-H, J ve K)" ifadesi, `PROGRESS.md`'de bölümü olan faz
harfleriyle birebir; ayrıca `docs/gelistirme-gunlugu/PROGRESS-faz-0-63.md` arşivi var ve aralığı doğru.

**Düzeltmeler (testin bulduğu bayatlık):** (a) README'nin faz listesi **K**'yı atlıyordu (iş 1'de
"A-H ve J" yazılmıştı); kaynak kodda bölümü olan fazlar A-H, J, K olduğundan `README.md` s.485-486
"… Faz A-H, J ve K" olarak düzeltildi (**I** henüz yapılmadı, listede yok — `KALAN_ISLER.md` iş 10-11).
(b) İş 1'de kaydedilen `src/` satır sayısı düzeltildi: 28 369 → **27 740**, sonra yöntem
netleşince (binary varlıklar hariç) → **27 194**; sayım yöntemi artık yazılı (izlenen **metin**
dosyalarda boş olmayan satır) ve iki testle bağlı (`tests/` 37 595 ve `web/` 6 139 aynı yöntemle
birebir tutuyor). (c) Bu yüzden README'nin kaynak iddiası da düzeltildi: "~28 bin" → **"~27 bin"**;
`tests/` tarafı ("~38 bin") doğru.

**Doğrulama:** `pytest tests/unit/test_release_readiness.py -q` **11 geçti** (~6 sn) ·
`test_readme_table.py` ile birlikte **16 geçti** · **mutasyon kanıtı 16/16 kırmızı** (12'si betikle
tek turda; her mutasyon sonrası dosyalar bayt-bayt geri yüklendi, SHA-256 doğrulandı): ilk tur ADR
30→31, badge 3700→9999, "~38 bin"→"~44 bin", faz listesi "A-H, J ve K"→"A-H ve J"; derin doğrulama
turu EN "30 ADRs"→"29", "30 kayıt"→"9 kayıt", TR/EN "N+ test", "~27 bin"→"~33 bin", faz listesi K
düşürme, PROGRESS'e sahte `## Faz I`, arşiv aralığı 0-63→0-62, binary guard'ın kaldırılması
(`_is_binary` → `False`; 2 test kırmızı) — hepsi ilgili testi kırmızı yaptı,
geri alınınca yeşil · sayım iki bağımsız yöntemle aynı sonucu verdi (Python `split("\n")` ve
PowerShell/.NET `-split "`r?`n"`; ikisinde de binary varlıklar atlanır) · `ruff check` temiz ·
`ruff format --check` 477 dosya · `mypy src/` 216 dosya temiz · testler ağa çıkmaz (yalnız yerel `git`
+ alt süreç pytest) · tam suite `pytest -m "not live"` **3763 geçti / 16 atlandı** (5:15; ilk koşuda
O1 zamanlama testi bir kez kırmızı oldu — makine yükü, bkz. aşağıdaki "Sonraya" maddesi).

**Ölçüm (iş 3 + doğrulama turu sonrası, metin dosyaları):** `src/` **27 194** · `tests/` **37 732**
(iş 3 öncesi 37 595'ten +137) · `web/` **6 139** → README "~38 bin / ~27 bin" iddiası geçerli ve artık teste bağlı.

**Kararlar:** faz ölçütü "durum tablosu" değil **bölümü olan fazlar** (durum tablosunda D satırı yok) ·
sayım yöntemi tek ve yazılı: **metin** dosyalarında boş olmayan satır (`git ls-files`; ilk 8 KB'da
NUL baytı olan binary dosyalar atlanır — ham baytlar sahte satır üretiyor) · badge için toplama sayısı
alt sınır
olarak alındı (tam eşitlik testleri sayı büyüdükçe anlamsız kırar).

**Açık:** bayatlama sınırı — `tests/` 38 500 satırı geçerse (iddia "~39"), `src/` 27 500'ü geçerse
(iddia "~28") ya da toplama 3 700'ün altına düşerse test kırmızı olur ve README güncellenmelidir. Sırada iş 2b; iş 4 (K2 regex taraması) → **tamamlandı** (aşağıda).

## Kod — K2 kalan regex taraması (KALAN_ISLER.md iş 4; 2026-10-18)

> Yeni `tests/unit/test_regex_budget.py` (339 satır, 96 vaka) + üç kaynak dosyada desen
> düzeltmesi: `analysis/call_costs.py`, `verify/leak_guard.py`, `verify/complexity.py`.
> Bulgular §10 Faz A "K2 — Kalan tarama" kutusu **kapandı**.

**Yapılanlar:** `codementor.analysis` / `codementor.rules` / `codementor.verify` paketlerindeki
**tüm modül düzeyi desenler** (44) otomatik keşfedilip 18 "en kötü girdi ailesi" ile 40 KB'da
ölçüldü (aileler: harf/rakam/boşluk/yeni satır dizileri, kapanmayan blok yorum ve tırnaklar,
kaçış tırnakları, `@"…"`, `a.Count` zincirleri, `=b` tekrarları, `UPROPERTY(`, `#include` +
boşluk). Beş desen süper-doğrusal çıktı ve **davranışı koruyarak** doğrusallaştırıldı:

- `analysis/call_costs.py` `_LAST_INDEX`/`_END_INDEX`: sınırsız taban sınıfı geri izleme yapıyordu
  (`"a"*4000` → 48 ms; 40 KB karesel). Yerine sondan çapalı küçük desen + `_index_base`
  (geriye doğru taban doğrulaması). `test_call_costs.py` vakalarıyla birebir aynı sonuç.
- `verify/leak_guard.py` `_ASSIGNMENT`: sınırsız sol/sağ taraf (`"_"*1600` → 29 ms). Baştaki `\b`,
  sınırlı **ve sahiplenici** sınıflar (`_MAX_ASSIGN_LHS=64`, `_MAX_ASSIGN_RHS=128`) ve
  `code_violations` içinde `;`/`=` hızlı elemesi (aynı işlevde `FENCE` kalıbı vardı).
- `verify/leak_guard.py` yorum/metin taraması: `/\*.*?\*/` kapanmayan yorumda, tırnak alternatifleri
  kapanmayan tırnakta kareseldi (`"/*a"×k` 40 KB'da ~1,2 sn). Desen, **ters yönlü tek geçişle**
  hesaplanan kapanış dizisi (`_body_closers`) + tek geçişli tarayıcıyla değiştirildi; çıktı eski
  desenle birebir aynı. `verify/` katmanı `analysis/` import etmediği için
  (`analysis/lexical.py` kullanılamadı) tarayıcı yerel yazıldı.
- `verify/complexity.py` `_TRAILER`: baştaki `\s*` boşluk dizisinde kareseldi (`" "*400` → 18 ms).
  `_before_trailer` (arama + `rstrip`) eski `split(...)[0]` ile aynı sonucu verir.

**Test tasarımı:** (1) keşif + `>= 40` alt sınırı (keşif sessizce boşalmasın);
(2) desen başına **40 KB < 50 ms** bütçesi — CPU saati, en iyi 4 koşu: Windows'ta `process_time`
kuantumu ~15,6 ms olduğundan hızlı desen 0 okunur, bütçeyi aşan en az bir kuantum gösterir;
(3) hypothesis ile **uzunluk eğrisi** (4x girdi ≤ 8x süre + 2 ms taban) — duvar saati, en iyi
5 koşu (oran ince değerlere duyarlı); (4) düzeltilen dört girdi noktası bilinen en kötü yüküyle
ayrıca sabitlenir; (5) eski desenler **karşılaştırma ölçütü** olarak testte tutulur: hem örnek
hem rastgele (hypothesis fuzz) girdide yeni/yeni-yol ile eski desenin çıktısı birebir karşılaştırılır.

**Kanıt (mutasyon eşdeğeri):** eski beş desen yeni büyüme kontrolüne sokuldu → **5/5 kırmızı**
(1 KB → 4 KB aralığında ~16x; 40 KB'a taşınsa 3,1 s – 176 s). Yeni desenler 40 KB'da
0,0–29,8 ms. Fuzz testi yazım sırasında **iki gerçek hata** yakaladı, ikisi de düzeltildi:
tek `/` girdisinde (`code="/"`) `"" in "/*"` doğru olduğu için `IndexError` (sabit
`frozenset` ile çözüldü) ve `code="'//"` girdisinde "kapanmayan tırnak bölgesini atla" kısayolunun
eski desenden sapması (kısayol tümden kaldırıldı, kapanış dizisi tasarımına geçildi).

**Doğrulama:** `ruff check` temiz · `ruff format --check` **478 dosya** · `mypy src/` **216 dosya**
temiz · yeni dosya **96 geçti** (~3 sn) · tam suite `pytest -m "not live"` **3859 geçti / 16 atlandı**
(4:45; iş 3 sonrası 3763'ten +96) · testler ağa çıkmaz (yalnız yerel dosya sistemi).

**Kararlar:** bütçe testi CPU saati, büyüme testi duvar saati kullanır (kuantum/çözünürlük
gerekçeleri testte yazılı) · `_ASSIGNMENT` sınırları tek deyim ölçeğinde cömert seçildi (64/128)
ve `test_assignment_bound_only_affects_oversized_statements` ile belgelendi · yeni desen eklenince
bütçe/eşdeğerlik kapsamı otomatik genişler (keşif).

**Açık:** iş 2b (§1 özet tablosu) hâlâ sırada; 2026-10-18'de listeye iki iş daha eklendi — **4b**
(zamanlama testlerinin tam suite yükünde kırılganlığı) ve **4c**
(`docs/ZAYIF_VE_GELISTIRILECEK_YONLER.md` bayat sayıları; bkz. "Sonraya" maddeleri). `_TRAILER`
40 KB'da doğrusal ama sabiti görece yüksek (~25 ms, 13 alternatif); üretimde karmaşıklık dizeleri
kısa olduğu için öncelik düşük.

## Statik — CPP-OWN-001 akış duyarlılığı doğrulaması (KALAN_ISLER.md iş 5 dilim 1; test-only; 2026-10-18)

> `tests/rules/fixtures/CPP-OWN-001/positive/` (+6 dosya) ve `tests/rules/test_finding_kinds.py`
> (+3 test). **`src/` değişmedi:** davranış Faz H2'de gelmişti; bu tur onu sınadı ve kaydı tazeledi.

**Durum tespiti:** İş listesindeki "CPP-OWN-001 akış duyarlılığı" maddesi açık görünüyordu ama
`rules/cpp.py` (`_jump_positions`/`_skipped_deletes`) bunu Faz H2'de uygulamış ve 4 fixture
(`early_return`, `throw_path`, `other_scope_return`, `lambda_between`) `EXPECT_KIND` ile tür ayrımını
sabitliyordu. Eksik kalan **kapsamdı**: `goto`, döngü içi `break`/`continue`, iç bloktaki `return` ve
çift aralığının sınırları hiç sınanmıyordu; PROGRESS "Sonraya" kaydı da kapanışı işaretlemiyordu.

**Yapılanlar (test-only):**
- Yeni fixture'lar (tek türlü durumlar, `EXPECT_KIND` ile): `goto_skip`, `loop_break_skip`,
  `loop_continue_skip`, `nested_block_return` → **issue**; `loop_pair`, `jump_outside_pair` → **suggestion**.
- Yeni birim testleri (fixture'ın ifade edemediği durumlar): çıkış `new`'dan **önce** → öneri · çıkış
  `delete`'ten **sonra** → öneri · aynı fonksiyonda iki çift, yalnız korumasız olan hata (karışık tür
  tek dosyada; fixture biçimi tek tür varsayıyor).

**Mutasyon kanıtı (iki yön):** (a) erken çıkış taraması devre dışı (`_skipped_deletes` → boş küme):
**7 kırmızı** = 6 fixture + 1 birim test. (b) aşırı duyarlı sürüm (aralık yerine "kapsamda herhangi bir
atlama" + lambda hariç tutması kaldırılmış): **8 kırmızı** = `lambda_between`, `other_scope_return`,
`jump_outside_pair`, `new_delete` fixture'ları + 4 birim test (yanlış pozitif koruyucuları). İkisi de
geri alındı; `git diff src/codementor/rules/cpp.py` **boş** çıktı.

**Doğrulama:** `ruff check` temiz · `ruff format --check` 478 dosya · `mypy src/` 216 dosya temiz ·
tam suite `pytest -m "not live"` **3868 geçti / 16 atlandı** (iş 4 sonrası 3859 → +9: 6 fixture vakası
+ 3 birim test) · testler ağa çıkmaz.

**Kararlar:** kapsam fonksiyon düzeyindedir (`scope_key`), bu yüzden döngü gövdesindeki eşleşme de
öneri sayılır — `loop_pair.cpp` beklenen tür `suggestion` · `new int[i]` ile `delete p` **kasten**
eşleşmez (aile uyuşmazlığı), bu yüzden loop fixture'ları `new int(i)` + `delete p` kullanır ·
`break`/`continue` erken çıkış sayılır (o turun `delete`'i atlanır), `switch` içindeki `break` de aynı
yola girer.

**Açık:** yok — iş 5'in bütün dilimleri tamamlandı (dilim 2–5 aşağıdaki bölümde).

## Statik — iş 5 dilim 2–5: dört kural kaçırması (2026-10-18)

> KALAN_ISLER.md iş 5'in kalan dört maddesi. **Dilim 2 ve 4'te gerçek kaçırma kapatıldı** (ödünç
> zinciri, iç içe kapsayıcı), **dilim 3** satır bazlı closure bastırmasını olgu düzeyinde kaldırdı,
> **dilim 5** Faz 57 davranışını eksik biçimlerle sınadı. 12 yeni fixture + 12 test.

**Yapılanlar:**
- **C-MEM-001 (dilim 2):** `_borrowers` tek geçişte yalnız ilk halkayı görüyordu; artık sabit
  noktaya yakınsıyor (`_MAX_BORROW_ROUNDS = 8`, küme yalnız büyür) → `report` → `show` → `dump`
  zinciri bulgu veriyor. Bilinçli sınırlar fixture'la sabitlendi (türetilmiş işaretçi döndüren
  yardımcı, `#ifdef` çift tanım, yalnız bildirim).
- **UNITY-GC-001 (dilim 3):** LINQ lambdasının closure'ı `CLOSURE` olarak ayrı sayılmıyor
  (`_without_linq_lambdas`; bayt aralığı + önek maksimumu, O(L log L + C log L)); `rules/unity.py`
  satır kümesi kaldırıldı → aynı satırdaki LINQ dışı lambda artık bastırılmıyor.
- **UE-GC-001 (dilim 4):** `_holds_uobject` `type_descriptor` sarmalayıcısını açıp
  `_MAX_CONTAINER_DEPTH = 2` katmana iniyor → `TMap<FName, TArray<UObject*>>` sayılıyor.
- **C-MEM-003 (dilim 5):** `src/` değişmedi; denetimin tahsise göre konumu (önce/sonra), tek dallı
  denetim, switch/do-while/continue biçimleri ve koşulda kullanım fixture+test ile sabitlendi.
- `docs/rules-catalog.md` dört kurala `catalog_note` eklenerek `make rules-doc` ile yeniden
  üretildi (belge elle düzenlenmiyor; `test_committed_catalog_up_to_date` bunu zorluyor).

**Mutasyon kanıtı (hepsi geri alındı):** sabit nokta → tek geçiş **2 kırmızı** · tüm closure'ları
bastır **2**, hiç bastırma **3 kırmızı** (LINQ lambdası çift bulgu) · kapsayıcı katmanı 1 **3
kırmızı** · C-MEM-003'te denetimin yol/konum ayrımı kaldırılınca **3 kırmızı**.

**Doğrulama:** `ruff check` temiz · `ruff format --check` 479 dosya · `mypy src/` 216 dosya temiz ·
tam suite `pytest -m "not live"` **3892 geçti / 16 atlandı** (dilim 1 sonrası 3868 → +24: 12 fixture
vakası + 12 birim/olgu testi) · facts golden'ları `--update-golden` ile tazelendi: `csharp-03` ve
`unity-03`'te yalnız LINQ satırındaki `closure` kaydı düştü (lambda zincirin içinde) · testler ağa
çıkmaz.

**Kararlar:** ödünç zinciri için tur bütçesi (8) sabit: dosya başına sabit sayıda ağaç gezintisi
(mimari §12), daha derin zincirde kaçırma kabul edildi · kapsayıcı derinliği 2: yapay iç içe girdide
özyineleme taşması ve karesel süre yok; `TWeakObjectPtr`/`TSoftObjectPtr`/`TStrongObjectPtr` zaten
GC-güvenli sayılıyor · LINQ lambda closure'ı **olgu** düzeyinde birleştirildi (kural düzeyinde satır
karşılaştırması yerine): hem çift bulgu bitti hem aynı satırdaki başka lambda görünür oldu.

## Faz J5 — Faz J denetiminden kalan küçük maddeler (test-only; 2026-10-17)

> J1b'de "kayda geçen" üç maddenin üçü de kapandı. Kaynak kod **değişmedi**: yalnız `tests/`.

**Yapılanlar:**
- **Küçük-1'in eşi (satır sonu):** `tests/golden/test_facts_golden.py::write_snapshot`,
  `Path.write_text` varsayılanına düşüyordu → Windows'ta `--update-golden` **15 `expected_facts.json`'ı
  CRLF ile kirletirdi** (ölçüldü: 15/15 dosyada CR>0, `git status` 15 dosya kirli; düzeltmeden sonra
  CR=0 + ağaç temiz). `newline="\n"` açıkça verildi; iddia `read_bytes()` üzerinden
  (`test_write_snapshot_writes_lf_bytes`) çünkü `read_text` CRLF'i gizliyordu (Küçük-1'deki ders).
- **Küçük-4'ün eşi (negatif yol):** `test_facts_golden_negative_paths` — gerçek `tests/golden/facts`
  ellenmeden, geçici dizinde kurulan vakayla: eksik anlık görüntü `--update-golden`'ı işaret eder,
  `--update-golden` sonrası geçer (ve LF yazar), içerik kayması düşürür ve mesaj dosyayı adıyla söyler.
  Ayrıca `test_every_case_has_snapshot` (eksik dosyalar tek mesajda listelenir) eklendi ve içerik
  uyuşmazlığı mesajı eyleme dönük hâle geldi (eskiden çıplak `assert`'ti).
- **Küçük-5 (dosya bölme):** `tests/unit/test_tier1.py` **633 → 349 satır**. Ortak düzenek
  `tests/unit/tier1_helpers.py` (80 satır: `FakeRunner`, örnek kodlar, araç zinciri, `normalize_code`,
  `read_stderr`); kalan vakalar `tests/unit/test_tier1.py` (atlama yolları + çağrı biçimi) ve
  `tests/unit/test_tier1_verdict.py` (292 satır: sonuç sınıflandırma + güvenlik/kolon regresyonları).
  **Vaka adları ve iddialar birebir aynı:** `pytest --collect-only` kimlikleri **58 → 58, birebir**
  (karşılaştırma orijinal dosya geçici olarak geri konularak yapıldı); AST karşılaştırmasında
  38 vaka / 127 assert iki tarafta eşit. Yardımcı adı `_code` → **`normalize_code`** (genel ad;
  `tests/` içinde özel modül importu yok — Küçük-3 kapanışındaki ilkenin devamı). `code` adı
  bilinçli seçilmedi: testlerde yerel `code = normalize_code(...)` değişkeni yaygın ve gölgeleme
  sessiz `UnboundLocalError` üretiyordu.

**Doğrulama:** `ruff check` temiz · `ruff format --check` **476 dosya** · `mypy src/` 216 dosya ·
`pytest -m "not live"` **3755 → 3758 geçti** (16 atlandı, 6 seçilmedi, 4:58) ·
`tests/golden/test_facts_golden.py` 18 → **21** vaka.
**Mutasyon kanıtı:** (a) `newline="\n"` kaldırılınca 2 test düşer ve `--update-golden` 15 golden'ı
CR>0 yapar; (b) içerik uyuşmazlığı mesajı eski çıplak `assert`'e döndürülünce
`test_facts_golden_negative_paths` düşer (1 failed). İkisi de geri alındı, ağaç temiz.
**Açık:** Zig budama (J2) hâlâ yerelde doğrulanamıyor (bu makinede gcc/clang/zig yok) → CI · repodaki
diğer 400+ satırlık test dosyaları bu kapsamda bölünmedi (denetimde adı geçen tek dosya buydu).

## Faz J4 — Önbellek sürümünde kontrol listesi içeriği ve kod kapsamı (O3 kapanışı; 2026-10-17)

> "Sonraya"daki **Faz 49 denetimi O3** maddesinin kalanı kapatıldı. Faz B soru modeli özetini ve
> referans çözüm damgasını imzaya eklemişti; kontrol listesi *içeriği* ile raporu belirleyen
> `pipeline/`+`prompts/` kodu hâlâ sürümde değildi (başka bir çalışma kopyasında eski rapor
> dönebilirdi). Bu fazda **`src/` ilk kez değişti**; mimariden sapma yok: §11'deki anahtar alanları
> aynı, yalnız `rules_version`'ın kapsamı ve öneki güncellendi.

**Yapılanlar:**
- `pipeline/versions.py` — `rules_version` artık kontrol listesi dizinini de özetler: dosya **adı +
  içerik** (LF normalleştirilmiş), liste ölçütü yükleyicininkiyle **aynı**
  (`questions.list_yaml_files`), dizin yoksa yer tutucu (eksiklik de bir sürümdür; sessiz ıska yok).
  Sürüm öneki `r2+` → **`r3+`** (Faz 49'daki `r1+`→`r2+` ile aynı gerekçe).
- `pipeline/versions.py` — `hashed_sources()` artık `pipeline/*.py` ve `prompts/*.py` dosyalarını da
  kapsar (yollar tekilleştirilir): `assemble.py`/`stages.py`/`signature.py` ya da prompt kurucusu
  değişince eski önbellek dönmez (O3'ün "kod değişiklikleri yok" maddesi).
- `pipeline/orchestrator.py` — `_rules_version` dizini yapılandırmadan verir (`data.checklists_dir`);
  yol/model koda gömülmez (AGENTS kural 5).
- `pipeline/signature.py` — kontrol listelerinin **dosya damgası** (boyut+mtime) girdisi kaldırıldı:
  içerik artık `rules_version`'da; damga yalnız `git checkout`/kopyalama gibi mtime değişimlerinde
  gereksiz önbellek ıskası üretiyordu (`_dir_stamps` yardımcısı da kalktı).
- `questions/__init__.py` — `list_yaml_files` + `DataFileError` genel API'ye alındı: `versions.py` ve
  `tests/golden/test_checklists_golden.py` artık özel modülü (`questions._loader`) import etmiyor
  (Faz J denetimi **Küçük-3** de böylece kapandı).
- **Testler (+9 vaka, ağ yok / FakeProvider):** `test_prompt_version.py` (+5: içerik değişimi, dosya
  kümesi, `.yaml` dışı dosyalar + satır sonu, eksik dizin/varsayılan dizin, `pipeline/`+`prompts/`
  kapsamı), `test_pipeline_signature.py` (+1: imza kontrol listesi damgası taşımaz),
  `test_pipeline_cache_key.py` (+2 uçtan uca: içerik değişimi ıskalar, yalnız mtime isabet eder),
  `test_audit_fixes_unit.py` (+1). Eski denetim testi `test_signature_tracks_stamped_files` içinden
  kontrol listesi vakası çıkarıldı (davranış bilinçli değişti, yeni yerine iddia eklendi).
- **Kanıt (gerçek veri üzerinde geçici prob, `TEMP`):** `data/checklists/css.yaml` sonuna yorum →
  `r3+b8c43ec8` değişti, `cache_key` değişti; baytlar geri → ikisi de aynı; **yalnız** mtime +7 sn →
  `rules_version`, `pipeline` imzası ve `cache_key` **aynı** (düzeltme öncesi imza değişirdi).
  `data/` altında iz bırakılmadı, ağaç temiz.
- **Doğrulama:** `ruff check` temiz · `ruff format --check` **474 dosya** · `mypy src/` **216 dosya
  hatasız** · `pytest -m "not live"` **3746 → 3755 geçti** (16 atlandı, 6 seçilmedi).
- **Not:** README'deki eval tablosundaki `r2+…` satırları **tarihsel kayıt** (o koşuların sürümleri);
  yeniden üretilmedi, yeni koşular `r3+…` yazar. `tests/providers/test_cli_agent.py`
  `test_json_document_is_linear_on_hostile_output` (duvar saati eşiği < 0,25 sn) ara koşuda yük
  altında düştü, tek başına ve diğer koşuda geçti → değişiklikle ilgisiz, bilinen kırılgan test.
- **Açık:** `meta.rules_version` biçimi değişti (eski eval kayıtları `r2+` kalır; karşılaştırmada
  sürüm farkı normaldir). Önbellek anahtarında referans çözüm **içeriği** hâlâ dosya damgasıyla
  temsil ediliyor ve etiket/veri seti sürümü yok (Faz 51 denetimi) → "Sonraya".

## Eval — KALAN_ISLER iş 7: Veri seti sürümü ve yapısal sınır (2026-10-20)

> KALAN_ISLER.md iş 7 (Faz 51 denetimi ve Faz 36 açığı).
> `src/` içinde `models/eval.py`, `eval/dataset.py`, `eval/runner.py`, `eval/compare.py`, `cli/eval.py` güncellendi;
> `tests/unit/eval/test_dataset_version.py` (+8 test) eklendi; `tests/unit/test_category_rules.py` genişletildi;
> `eval/dataset/dev/cpp-009/label.yaml` yapısal `boundary` aldı.

**Yapılanlar:**
- `RunConfig` modeline `dataset_version: str | None = None` alanı eklendi (`models/eval.py`).
- `dataset_version(target)` fonksiyonu eklendi (`eval/dataset.py`): kimlik, kod (LF normalleştirilmiş)
  ve etiket (JSON) içeriklerinden `d1+<hash>` formatında SHA-256 özeti üretir. Satır sonu farkından etkilenmez.
- `eval/runner.py`: `run_eval` çalıştırılırken `run_config` içine `dataset_version` otomatik doldurulur.
- `eval/compare.py`: `compare_table` dipnotunda `veri seti d1+...` bilgisi gösterilir; birden fazla farklı
  veri seti sürümü karşılaştırıldığında açık uyarı satırı basılır.
- `cli/eval.py`: `_result_and_labels` içinde kayıtlı sonuçtaki `dataset_version` ile diskteki güncel etiketler
  karşılaştırılır; uyuşmazlık varsa sarı uyarı basılarak eski koşuların sessizce yeniden puanlanması engellenir.
- `models/eval.py`: `ExpectedFinding` modeline `boundary: str | None = None` eklendi.
- `tests/unit/test_category_rules.py`: `memory_boundary_violation` artık yapısal `boundary` alanını serbest
  metin sezgisinden önce öncelikli olarak değerlendirir. `cpp-009/label.yaml` L6 ve L10'a `boundary: ownership_scope`
  işlendi.
- `README.md` ve `docs/ZAYIF_VE_GELISTIRILECEK_YONLER.md`: `src/` satır sayısı 27 500'ü geçtiği için
  `~28 bin satır kaynak` iddiası eşitlendi; `test_release_readiness.py` yeşil.

**Doğrulama:** `ruff check` temiz · `ruff format --check` 482 dosya · `mypy src/` 216 dosya hatasız ·
`tests/unit/eval/test_dataset_version.py` 8 geçti · `test_category_rules.py` 13 geçti ·
`test_readme_table.py` 5 geçti · `test_release_readiness.py` 15 geçti ·
tam suite `pytest -m "not live"` **3927 geçti / 16 atlandı**.

## Kod + Depolama — KALAN_ISLER iş 6, 8 ve 9 (2026-10-20)

> KALAN_ISLER.md iş 6 (doküman eşitleme), iş 8 (depolama borcu) ve iş 9 (Faz F/G küçük açıkları).
> `src/` içinde `storage/db.py`, `storage/cache.py`, `desktop/services.py`, `desktop/connections_controller.py`,
> `desktop/runtime.py` güncellendi; `tests/unit/test_storage_migration.py` (+3 test) eklendi;
> `tests/desktop/test_connections.py` genişletildi.

**6 — Statik kapsam kuralları durumu (Faz H1 eşitlemesi)**
- `KALAN_ISLER.md` iş 6 maddesindeki kuralların (`CSS-ACC-001`, `CSS-LAYOUT-001`, `CSS-LAYOUT-002`,
  `CPP-PERF-002`, `CPP-PERF-003`, `CPP-PERF-004`, `C-BUF-002`, `CS-ALLOC-001`) Faz H1'de zaten
  eksiksiz uygulandığı ve katalogda yer aldığı doğrulandı, liste `[x]` yapıldı.

**8 — Depolama borcu (Faz 49 Ü9 kapanışı)**
- `src/codementor/storage/db.py`: `SCHEMA_DB_VERSION = 2` yapıldı. `_migrate` içine `PRAGMA table_info`
  denetimi eklendi; eski veritabanlarındaki eksik sütunlar (`analyses` ve `sessions` tabloları)
  otomatik `ALTER TABLE ADD COLUMN` ile eklenir (`OperationalError` koruması).
- `src/codementor/storage/cache.py`: `_list_analyses_fallback` eklendi. SQLite tablosundaki bozuk ISO
  tarih formatları `list_analyses` ve `list_analyses_page` sorgularını çökertmez; bozuk satırlar
  toleransla ele alınır.
- `tests/unit/test_storage_migration.py`: 3 yeni test (eski şema göçü, bozuk tarihle analiz listeleme ve sayfalama).

**9 — Faz F/G küçük açıkları (F10 denetimi kapanışı)**
- `src/codementor/desktop/services.py`: `OLLAMA_MODEL_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]*$")`
  olarak sıkılaştırıldı (`/x`, `../x`, `-flag`, `.hidden` reddedilir).
- `services.py` + `tests/desktop/test_connections.py`: `run_ollama_pull`'un `result.error` ve
  `result.timed_out` dallarına testler eklendi.
- Model indirme iptal desteği: `run_ollama_pull`'a `cancel: threading.Event | None = None` parametresi,
  `ConnectionsController`'a `_pull_cancellations`, `cancel_pull(name)` ve `is_pulling` özelliği eklendi.
  `runtime.confirm_close` süren model indirmesini algılayıp kullanıcıdan teyit ister.

**Doğrulama:** `ruff check` temiz · `ruff format --check` 481 dosya · `mypy src/` 216 dosya hatasız ·
`tests/desktop/test_connections.py` 47 geçti · `tests/desktop/test_app.py` 253 geçti ·
`tests/unit/test_storage_migration.py` 3 geçti · `tests/unit/test_storage.py` 46 geçti.

## Testler + Belgeler — KALAN_ISLER iş 2b/4b/4c (2026-10-18)

> KALAN_ISLER.md iş 2b (§1 özet tablosu), iş 4b (zamanlama testleri) ve iş 4c (zayıf yönler
> belgesinin sayıları). `src/` **değişmedi**; iş 4b yalnız testlerin ölçüm yöntemini sertleştirdi.

**2b — §1 özet tablo hizalaması**
- `docs/BulgularVeDuzeltilecekler.md` §1'de 15 satırın 6. kolonuna kapanış etiketi eklendi
  (Y1 → A2; Y3/Y4/Y5, O3/O4 → B; Y7/Y8/Y9, O9/O12 → C; O5 → G1; O15/O16 → E; O17 → "release; D").
  5. kolon (Doğrulama) ve satır sayısı değişmedi; etiketler §4 başlıkları ve §10 `[x]` kutularıyla
  birebir.

**4b — zamanlama testleri (karar: göreli büyüme + min-of-3; ADR-0024 eşiği aynı)**
- Seçim: **göreli büyüme birincil** (makine yükünden bağımsız) + mutlak bütçe korunur, ölçüm
  **en iyi 3 koşu** (ısınma + 3 ölçüm). `slow` işaretleyip `make check` dışına alma **seçilmedi**:
  gerileme koruması zayıflardı. Eşik **1,5 sn değişmedi** → ADR-0024 notu/onayı gerekmedi.
- `tests/unit/test_facts_review.py`: `_best_of` (min) + O1/O2/O3 için dört büyüme testi
  (`large <= 3 × small`, taban 20 ms; 2× girdi doğrusalda ≈2×, kareselde ≈4×).
  `tests/unit/test_tier0_budget.py`: aynı `_best_of` + üç büyüme vakası (C++/CSS/C). HTML kapanmamış
  `<div>` gramerde doğası gereği süper-doğrusal (ölçüm 2× girdi ≈3,3×) → yalnız mutlak bütçede
  bırakıldı (gerekçe testte yazılı).
- **Duyarlılık kanıtı:** `extract_facts`'a geçici karesel yama → `test_o1_growth_is_linear`
  **0,336 → 1,071 sn** (kırmızı; mutlak test 1,071 < 1,5 olduğu için yeşil kalırdı → büyüme testinin
  gerekliliği). `run_tier0`'a aynı yama → CSS **97 → 347 ms**, C **86 → 323 ms** (ikisi kırmızı).
  Yamalar geri alındı; iki dosya SHA-256 ile bayt-bayt eski hâlinde.
- **Kırılganlık kanıtı:** ilgili testler **3 tam suite koşusunda** hiç kırmızı olmadı.

**4c — `docs/ZAYIF_VE_GELISTIRILECEK_YONLER.md` tazeleme + teste bağlama**
- Ölçüm (izlenen metin dosyaları, boş satır hariç): `src/` **27 367**, `tests/` **38 550** (iş 4b/4c
  test eklemeleriyle +123; README'deki kardeş iddia yuvarlama testi yüzünden **~39 bin**'e
  güncellendi), `web/` 6 139; `docs/adr/` **30** dosya; 400 satırı aşan dosya **0** (en büyükler:
  `analysis/extractor.py` 396, `config.py` 390; Faz F/G'de bölünenler 350/350/323);
  `report/usage.py` 62 satır ve yalnız `models/` import ediyor → bağımlılık notu **kapandı**;
  "Sonraya" **46 açık / 120 madde**.
- Belge düzeltmeleri: s.50/91 "3.300+" → **3.700+**, s.50/423 "29 ADR" → **30 ADR**, s.399
  "~29 bin kaynak, ~28 bin test" → **"~27 bin satır kaynak, ~39 bin satır test"**, s.397-404
  (dosya satırları, kapalı bağımlılık, madde sayısı), §10 özet tabloda iki satır (400 satır: 3 → **0**;
  "Sonraya": ~60 → **46**).
- `tests/unit/test_release_readiness.py` **+4 test** (~70 satır): satır sayısı iddiaları, "N+ test"
  (alt sınır) ve "N ADR" (eşitlik), `path.py NNN` iddiaları **toleranssız**, "Sonraya" açık madde
  sayısı (`PROGRESS.md` "Sonraya" bölümü; kapalı = `- ~~`).
- **Mutasyon kanıtı (5/5 kırmızı):** "~27 bin"→"~33 bin" · "30 ADR"→"29 ADR" · extractor 396→397 ·
  "48"→"47" (Sonraya) · "3.700+"→"9.999+". Belge bayt-bayt geri döndü (SHA-256).

**Doğrulama:** `ruff check` temiz · `ruff format --check` 479 dosya · `mypy src/` 216 dosya hatasız ·
hedefli testler yeşil · tam suite `pytest -m "not live"` **3 kez** yeşil: **3903 geçti / 16 atlandı**
(352 s · 337 s · 240 s; iş 5 sonrası 3892 → +11: 4 büyüme (O1-O3) + 3 büyüme (Tier 0) + 4 belge testi).
**Açık:** yok.


## Faz J — Notlar (isteğe bağlı küçük işler; 2026-10-17)

> Devir §10'un üç maddesinden **biri** alındı: kontrol listesi anlık görüntü testi. Zig budama
> bilinçli olarak yapılmadı (gerekçe aşağıda); "YAPMA" listesine dokunulmadı.

**J1 — Kontrol listesi içerik anlık görüntüsü (`e7f50d7`):** `data/checklists/*.yaml` içeriğinin
sha256 özeti `tests/golden/checklists_sha256.json` içinde sabitlendi (8 dosya); test
`tests/golden/test_checklists_golden.py` (**5 vaka**). Bu dosyalar prompt'a girdiği (mimari §8.3) ve
ölçümü etkilediği için sessiz değişim istenmiyor: içerik, dosya kümesi ya da kodlama bozulursa test
düşer ve mesaj **değişen dosyayı adıyla** söyleyip `--update-golden`'ı işaret eder.
- **Karar — özet ham baytlardan, LF normalleştirilmiş:** `.gitattributes` tüm metin dosyalarını LF'e
  sabitliyor; yine de `\r\n` → `\n` normalleştirildi ki farklı çalışma kopyası ayarları testi bozmasın.
  Windows'ta `Get-FileHash -Algorithm SHA256` çıktısı golden JSON ile **birebir aynı** çıktı: sekiz
  dosya için normalleştirme hiçbir şeyi gizlemiyor.
- **Dosya kümesi kaynağı:** `questions._loader.YAML_SUFFIXES` içe aktarılır; anlık görüntü yükleyicinin
  okuduğu kümeyle aynı ölçütü kullanır (`.yaml`/`.yml`, büyük/küçük harf duyarsız) ve ayrıca
  "özet dosya kümesi = dizin" testi vardır — eklenen/silinen dosya sessiz kalmaz.
- **Mutasyon kanıtı:** `data/checklists/css.yaml` sonuna yorum eklenince **1 test** düştü (mesaj:
  `Kontrol listesi içeriği değişti: css.yaml`); `data/checklists/gecici.yaml` eklenince **2 test**
  düştü (içerik özeti + dosya kümesi). İkisi de geri alındı; ağaç temiz.
- **Doğrulama:** `ruff check` temiz, `ruff format --check` **474 dosya**, `mypy src/` hatasız (**216
  dosya**), `pytest -m "not live"` **3738 → 3743 geçti** (16 atlandı, 6 seçilmedi; +5 vaka). Kaynak kod
  **değişmedi**: yalnız test + golden veri.

**J1b — Bağımsız denetim düzeltmeleri (dal `faz/j-denetim`):** Faz H + J teslimi salt-okur denetlendi
(`faz-denetim`): **Kritik/Önemli bulgu yok**, 5 küçük bulgu; üçü kapatıldı — yalnız
`tests/golden/test_checklists_golden.py` değişti (99 → **167 satır**), kaynak kod yine değişmedi.
- **Küçük-1 (satır sonu) kapatıldı:** `write_golden` `Path.write_text`'in Windows varsayılanı
  (`os.linesep`) yüzünden CRLF yazıyordu; `--update-golden` sonrası dosya **CR=10** olup git
  "CRLF will be replaced by LF" uyarısıyla ağacı kirletiyordu (içerik farkı yok). Düzeltme öncesi
  ` M tests/golden/checklists_sha256.json`, sonrası **CR=0 + ağaç temiz**. `newline` açıkça verildi ve
  iddia artık `read_bytes()` üzerinden (`test_write_golden_writes_lf_bytes`) — eski tur-gidiş iddiası
  CRLF'i gizliyordu.
- **Küçük-2 (kopya ölçüt) kapatıldı:** `checklist_files` listeyi yeniden yazmıyor,
  `_loader.list_yaml_files(directory, DataFileError)` çağırıyor → yükleyicinin listeleme kuralı
  değişirse anlık görüntü sessizce ayrışamaz (PROGRESS'teki "aynı ölçüt" iddiası artık kopya değil).
- **Küçük-4 (negatif yol) kapatıldı:** gerçek `data/checklists` ellenmeden, modül sabitleri geçici
  dizine yönlendirilerek içerik değişimi (**mesaj değişen dosyayı adıyla söyler**), dosya kümesi kayması
  ve golden-yok durumu süite içinde kanıtlanıyor. Ayrıca dosya kümesi iddiasına eksik/fazla listesi
  içeren mesaj eklendi (eskiden çıplak `assert`'ti → CI'da eyleme dönük değildi).
- **Kapatılmayan ikisi kayda geçti:** Küçük-3 (`tests/` içinde özel modül `questions._loader` importu —
  bilinçli kabul; **Faz J4'te kapandı** — yardımcı `questions.list_yaml_files` olarak genel API'ye alındı), Küçük-5 (`tests/unit/test_tier1.py` 633 satır) → "Sonraya".
- **Doğrulama:** `ruff check` temiz · `ruff format --check` 474 dosya · `mypy src/` 216 dosya hatasız ·
  `pytest -m "not live"` **3743 → 3746 geçti** (16 atlandı, 6 seçilmedi) · `tests/golden` **40 geçti**.
  Gerçek veri mutasyonu (`css.yaml` + yorum) → **1 fail**, geri alınınca 40 geçti.

**Yapılmayan (bilinçli):** **Zig budama** — kurulumdan sonra kullanılmayan libc başlık dizinlerini
silmek (382 MB → <150 MB) yerelde doğrulanamıyor: bu makinede gcc/clang/zig yok, `uv run pytest -m
compiler` koşulamıyor ve devir "emin değilsen YAPMA" diyor. Doğrulama CI'ya (ya da zig kurulu bir
makineye) bırakıldı. "YAPMA" listesi (imzalı exe/Inno Setup, cppcheck/clang-tidy, VS Code eklentisi,
Rust/Go/JS desteği, `session_id`'yi anahtara bağlama) zaten kapsam dışı; hiçbirine dokunulmadı.

## Faz G — Notlar (sağlayıcı sağlamlığı ve kod temizliği; 2026-10-15, kapanış 2026-10-16)

**G0 — `orchestrator.py` ve `passes.py` bölündü (dosya başına 400 satır kuralı):**
- `pipeline/orchestrator.py` 465 → 393 satır. Yeni modüller: `cache_flow.py` (önbellek anahtarı/imza,
  Tier 1 ayarı, deneme geri alma, rapor kaydı) ve `deadline.py` (`_timed_out`, `_remaining` gövdeleri).
  `Orchestrator` yöntemleri ince sarmalayıcı kaldı (`self._validation(...)`, `self._tier1(...)`,
  `self._remaining(...)`): testler `monkeypatch.setattr(Orchestrator, ...)` ile yamıyor, adlar korundu.
- `pipeline/passes.py` 426 → 330 satır. Yeni modüller: `llm_session.py` (`LLMSession`) ve
  `verify_pass.py` (`VERIFY_STAGES`, `VERIFY_FAILED`, `run_pass_verify`). Onarım/sokratik prompt kuran
  `run_pass_a`, `_socratic` ve `call_structured` bilinçli olarak `passes.py`'de kaldı: testler
  `passes.build_repair_messages` / `passes.build_socratic_messages`'i yamıyor.
- `passes.py` taşınan adları `__all__` ile yeniden dışa aktarır (`pipeline/assemble.py` ve
  `eval/runner.py` değişmedi). `verify_pass.run_pass_verify`, `call_structured`'i çağrı anında alır
  (döngüsel içe aktarma olmasın diye).
- `Orchestrator._report` gövdesi `assemble.assemble_with_cost` oldu (rapor + maliyet tahmini);
  `pipeline/assemble.py` 145 satır (< 400). `desktop/app.py` zaten 395 satır (F0).
- **Doğrulama:** davranış değişmedi — değişen dosyalar yalnız `src/` (test yok); `ruff` ve
  `ruff format --check` temiz; `mypy src/` 211 dosyada hatasız; `pytest -m "not live"` 3454 geçti,
  15 atlandı, 6 deselected (G0 öncesiyle aynı sayılar).

**G1 — CLI ajan çıktısı 64 KB'de kesiliyordu (bulgu O5):**
- `ProcessLimits.output_limit` eklendi (varsayılan `OUTPUT_LIMIT` = 64 KB). `_CappedReader` ve
  `_supervise` sınırı bu alandan alır; derleyici (Tier 0/1) yolu varsayılanda kalır.
- `CliConfig.output_limit_bytes` (65536-16777216, varsayılan 1 MB) config'ten gelir; `agent_limits`
  bunu `ProcessLimits`'e geçirir, `claude_cli`/`agy`/`codex` aynı yolu kullanır (mimari §12: sınır
  koda gömülmez).
- Kesilme sonucu düşürmez: `ProviderResult.warnings`'e "Model yanıtı çok uzundu, kesildi." eklenir
  (`_cli_common.clip_warning`) ve rapora `meta.warnings` olarak gider. Yanıt hiç ayrıştırılamadıysa
  eski hata ("çıktı boyutu sınırı aşıldı") korunur.
- Örnek yapılandırmalar (`codementor.toml`, `docs/mimari.md`) üç CLI sağlayıcısı için alanı gösterir.
- **Doğrulama:** ruff ve `ruff format --check` temiz; `mypy src/` 207 dosyada hatasız;
  `pytest -m "not live"` 3454 geçti, 15 atlandı, 6 deselected. Sahte CLI'ye `BOYUT:<n>` gürültü modu
  eklendi: 200 KB çıktı varsayılan sınırla tam okunuyor; `output_limit_bytes=65536` ile yanıt
  korunuyor + uyarı geliyor (Tier 1 sınırı değişmedi, `tests/unit/test_runner.py` geçiyor).
- **Açık:** G2-G7 yapılmadı; O5'in "canlı doğrulanmadı" notu hâlâ
  geçerli (gerçek `agy`/`codex` çıktısıyla elle deneme kullanıcıya bırakıldı).

**G3 — düşük öncelikli D serisi bulguları (`docs/BulgularVeDuzeltilecekler.md` §5):**
- **İlk parti (commit `5f51dec`):** D2 (`extract_json` tırnak durumu yalnız `{` içinde izlenir),
  D3 (`codex_cli._events` `RecursionError`), D4 (`429`/`401` kelime sınırlı regex),
  D5 (`apply_verdicts` yeni `finding_id`'yi `FindingCheck`'e yazar), D12 (`_json_document` doğrusal
  tarama).
- **D6 — geçiş başına sağlayıcı/maliyet:** `LLMSession.stage_providers/stage_models` yerine
  `stage_usage: dict[tuple[str, str, str], TokenSplit]` — anahtar `(aşama, sağlayıcı, model)`.
  Aynı aşama fallback ile iki sağlayıcıya bölünürse tokenler ayrı gruplanır;
  `cost_of_stages(pricing, usage)` her grubu kendi modelinin fiyatıyla çarpar. Fiyatı olmayan ya da
  sıfır tokenlı grup varsa `meta.cost_est` `None` (uydurma maliyet yazılmaz). `meta.provider/model`
  sözleşmesi değişmedi (son çağrının değerleri; raporda belgeli).
- **D1 — onarım prompt'unda doğru neden:** `guard_delimiters` artık `validation_errors` etiketini de
  nötrler (Pydantic `extra_forbidden` mesajı modelin uydurduğu anahtar adını taşıyor ve veri bloğunu
  kapatabiliyordu). `build_repair_messages(..., cause=...)` + `REPAIR_REASONS` ile giriş cümlesi
  nedene göre; `_repair_cause` şema dışı bir neden varsa onu seçer (karmaşıklık onarımında
  "şemaya uymadı" denmiyor).
- **D7 — sızıntı sonrası yeniden üretim notu:** `build_socratic_messages(..., abstract=True)`
  prompt'un sonuna içerik sızdırmayan "daha soyut sor" notunu ekler; `run_pass_b(..., rebuild=...)`
  ikinci turda `rebuild(True)` ile prompt'u yeniden kurar. Not, sabit sıcaklıklı sağlayıcılarda
  (claude_cli) aynı sızıntının tekrarlanmasını azaltmayı amaçlar; `prompt_b` süresi her kurulumda
  ölçülür (yeniden üretimde ikinci pencere, `stage_latency_ms` son değeri taşır).
- **D8 — bozuk prompt şablonu raporu düşürmez:** `prompts/templates.py`'ye `PromptTemplateError(ValueError)`
  eklendi; eksik/okunamayan şablon dizini ve Jinja `TemplateError` (şablon dosya adıyla) artık bu tipe
  dönüşüyor, ham `FileNotFoundError` yükselmiyor. `builder._fewshots` `FewShotError`'ı da aynı tipe
  çevirir (bozuk YAML tüm raporu bozar → tek tek örnek atlanmaz). `orchestrator.prompt_version(...)`
  hatayı yakalayıp `prompt_templates_unreadable` günlüğüyle sürümü `UNAVAILABLE_VERSION`
  (`v1+00000000`) yapar ve `run.cacheable = False` işaretler: rapor LLM geçişi yapılmadan statik
  analizle `degraded` döner, kurulum düzeltildiğinde yeniden üretilir (önbellekten gelmez).
  Tier 0 ve doğrulama geçişleri de aynı tipi yakalar. Uyarı metni "Few-shot" içerir.
- **D9 — ölü/tekrar kod temizliği:** `providers/anthropic.py`'deki ikinci `DEFAULT_MAX_TOKENS`
  kaldırıldı; tek kaynak `config.ANTHROPIC_DEFAULT_MAX_TOKENS` (hem `AnthropicConfig.max_tokens`
  varsayılanı hem adaptörün `opts.max_tokens or ...` yedeği). `prompts/budget._single_budget`'teki
  `PROVIDER_NAMES`/`isinstance` denetimi ve üretimdeki `TEST_PROVIDERS = {"fake"}` test kancası
  silindi: ad için yapılandırma bölümü varsa bağlam/çıktı payı oradan, yoksa ad yapılandırılmış
  zincirde geçiyorsa prompt varsayılanları (testlerin `FakeProvider`'ı zincirde tanımlanır, üretim
  kodu onu bilmez); ne bölümü ne zinciri olan ad yine `PromptConfigError`. `passes.call_structured`
  ve `run_pass_socratic_schema` artık kullanılmayan tek kullanımlık `BuiltPrompt`'u döndürmüyor
  (yalnız ayrıştırılmış sonuç); `verify_pass.run_pass_verify` ve `run_pass_b` çağrıları güncellendi.
- **D10 — HTML/CSS LLM şeması dışa aktarılıyor:** `LLMMarkupAnalysisOutput` (ADR-0015)
  `SCHEMA_MODELS`'e eklendi ve `schemas/llm_markup_analysis.schema.json` üretildi
  (`uv run codementor schema export --out schemas/`); `test_schema_export.py` beklenen dosya
  listesine ve "sistem alanı sızdırmaz" denetimine eklendi. UI tip listesi (`gen-types.mjs`)
  yalnız `UI_SCHEMAS`'ı üretir; web tipleri değişmedi.
- **D11 — olay döngüsündeki küçük G/Ç önbelleğe alındı:** `prompts/templates.prompt_version`
  dosya kümesini artık `_names` (stat'sız `os.walk`/`scandir`) anahtarıyla önbelleğe alıp `rglob`
  taramasını küme değişmedikçe yinelemiyor — dizin mtime'ı Windows'ta ~1 ms çözünürlükte olduğu
  için anahtar olarak güvenilmez (ölçüldü), bu yüzden dosya adı kümesinin kendisi kullanıldı;
  içerik değişimi yine boyut+mtime imzasından gelir. `Orchestrator._rules_version` ve
  `_question_bank` örnek başına bir kez çalışır: aynı analizde önbellek anahtarı ile rapor
  `meta`'sı aynı sürümü paylaşır (önceden maliyet tablosu + mentor şablonları iki kez okunuyordu)
  ve enjekte edilmeyen banka aynı orkestratörde diskten tekrar yüklenmez. Örnek istek/örnekleme
  başına kurulduğu için (API, masaüstü, CLI, eval) tazelik korunur. Yeni testler:
  `test_prompt_version.py::test_prompt_version_scans_once_per_file_set`,
  `test_pipeline_sessions.py::{test_question_bank_loaded_once_per_orchestrator,
  test_rules_version_reads_data_files_once_per_analysis}` (son ikisi düzeltme öncesi `[1, 1]`
  görüyordu; defekt kanıtlandı).

- **Prompt sürümü (D6-D8):** `repair.user.j2` ve `socratic.user.j2` değiştiği için hash
  `v1+3fa9c2d1` → **`v1+632620d8`**; `tests/golden/report_example.json` ve
  `src/codementor/api/examples/report.json` güncellendi. **Doğrulama (D6-D8):** `pytest -m "not live"`
  **3479 geçti**, 15 atlandı, 6 deselected (G1 sonrası 3454 → +25 test: D6 maliyet, D1 neden
  metni/guard, D7 soyut not, D8 şablon bozulması).
- **Prompt sürümü:** D9-D11'de şablon/few-shot dosyalarına dokunulmadı → hash `v1+632620d8`
  sabit; golden dosyalar güncellenmedi.
- **Doğrulama (D9-D11):** `ruff check`/`ruff format --check` temiz (467 dosya); `mypy src/` 211
  dosyada hatasız; `pytest -m "not live"` **3482 geçti**, 15 atlandı, 6 deselected (D8 sonrası
  3479 → +3 test). Bir koşuda `tests/rules/test_engine.py::test_linear_time_large_input[html-*]`
  zaman sınırını aştı (38 s > 2 s); tek başına ve sonraki tam koşuda geçti → makine yükü kaynaklı,
  değişiklikle ilgisiz.
- **Açık (D9-D11 sonrası):** D14-D20 ve `schema_enforced` duruyor; G2 sırada.

**G2 — O6: kalıcı CLI hataları yeniden denenmiyor:**
- `providers/cli_agent.py`'ye oturum/kimlik sınıflandırması eklendi: `_AUTH_HINTS` (İngilizce
  `not logged in` / `please run /login` / `unauthorized` / `authentication` / `invalid api key` +
  Türkçe `oturum açıl` / `giriş yap`) ve `auth_error(provider, detail, command)` →
  `ProviderConfigError` (`retryable = False`, `codex_cli._classify` ile aynı sözleşme).
- Claude sonuç nesnesindeki hata (`_claude_error`) artık kimlik ipucunu 429/5xx dallarından sonra,
  4xx'ten önce kontrol eder: oturumu kapanmış CLI `ProviderUnavailableError` (yeniden denenir) değil,
  "oturum açılmamış; terminalde `claude login` çalıştırın" mesajlı kalıcı hata verir. `data is None`
  (JSON çıktı yok) yolunda stderr/`çıkış kodu` ayrıntısı da aynı sınıflandırmadan geçer; agy için
  komut metni `agy`. 5xx ve 429 davranışı değişmedi (geçici → yeniden denenir).
- `_cli_common.CliPermanentError(ProviderUnavailableError)` (`retryable = False`) eklendi
  (`CliTimeoutError` deseni): agy'nin boş yanıtı ("oturum açık mı?"; MCP takılması dahil) ve
  deterministik Claude `subtype`'ları (`error_max_structured_output_retries`, `error_max_budget_usd`,
  `error_max_turns`) artık kalıcı. Böylece `agy` her biri ~20 sn süren 3 süreç açmıyor; sıradan
  `subtype` hataları ve ağ benzeri hatalar eskisi gibi yeniden denenmeye devam ediyor
  (ortak sözleşme testi `test_network_error_retried_then_unavailable` korunuyor).
- Yeni testler (`tests/providers/test_cli_agent.py`): `test_logged_out_result_is_not_retried`
  (`max_retries=2` ile bile sağlayıcı bir kez çağrılır), `test_logged_out_stderr_is_not_retried`,
  `test_server_error_is_still_retried` (kontrol: 5xx iki kez denenir),
  `test_agy_empty_response_is_not_retried`, `test_claude_permanent_subtype_is_not_retried`,
  `test_claude_unknown_subtype_is_retried` (kontrol: sıradan `subtype` yine denenir).
- **Doğrulama (G2):** `ruff check`/`ruff format --check` temiz (467 dosya); `mypy src/` 211 dosyada
  hatasız; `pytest -m "not live"` **3488 geçti**, 15 atlandı (D9-D11 sonrası 3482 → +6 test).
- **Açık:** G5-G7 ve D14-D17/D19/D20 kalemleri (G0-G4 ✅) — sıra ve kapsam için aşağıdaki
  "Sıradaki oturum — Faz G kalanı" bölümüne bak.

**G4 — D18: Tier 0 durdurma tanısı artık yapısal:**
- `models/validation.Tier0Result`'a `stopped: bool = False` alanı eklendi; durdurma tanısı üreten tek
  yer (`tier0_isolation._stopped`) bayrağı True kurar, `stopped()` önce bayrağa bakar. Böylece tanı
  metni (`TIMEOUT_MESSAGE`/`FAILURE_MESSAGE`/`INFRA_MESSAGE`) değişse de erken çıkış kararı sessizce
  bozulmaz. Metin karşılaştırması yalnızca bayrağı taşımayan sonuçlar (eski işçi JSON'u, elle kurulmuş
  sonuç) için yedek kaldı; davranış bu yollarda değişmedi.
- `Tier0Result` rapor şemasının parçası değil (`SCHEMA_MODELS`), bu yüzden `schemas/` ve web tipleri
  yeniden üretilmedi.
- Test: `tests/unit/test_tier0_isolation.py::test_stopped_flag_is_structural_not_textual` —
  değiştirilmiş mesajlı ama bayraklı sonuç yine "durduruldu"; sıradan sözdizimi hatası değil; bayrak
  JSON gidiş-dönüşünde (işçi süreci sınırı) korunuyor.
- **Doğrulama (G4):** `ruff`/`ruff format --check` temiz (467 dosya); `mypy src/` 211 dosyada hatasız;
  `pytest -m "not live"` **3489 geçti**, 15 atlandı (G2 sonrası 3488 → +1 test).

**G4+ — D14 yeniden denetimi (Faz E'de kapanmış bulundu) + sertleştirme:**
- Denetim: `api/auth.py` zaten `PROTECTED_EXACT_PATHS` (`/health/ready`, `/docs`, `/redoc`,
  `/openapi.json`, `/docs/oauth2-redirect`) + `_is_protected` içeriyor ve `tests/api/test_api_auth.py::`
  `test_internal_endpoints_protected_with_key` bu davranışı kapsıyordu (Faz E, `f8a2be4`); `tests/api`
  **123 test** yeşil. Yani D14'ün asıl kodu eksik değildi, **kalan açık doküman işaretiydi**.
- Ampirik atlatma denemesi (`%76%31/rules`, `//v1/rules`, `/v1//rules`, `/v1/./rules`, büyük harf):
  koruma atlanmıyor — Starlette `URL.path`/eşleştirme ikisi de çözülmüş `scope["path"]` kullanıyor,
  yüzde kodlamalı `/v1` yazımı 401 veriyor.
- **Gerçek bulgu:** korumalı tam yolların sondaki `/` varyantları (`/docs/`, `/openapi.json/`,
  `/health/ready/`) anahtar denetiminden önce FastAPI `redirect_slashes` 307'sini döndürüyordu (içerik
  sızmıyordu ama tutarsızdı). `_is_protected` artık `path.rstrip("/") in PROTECTED_EXACT_PATHS`
  kullanıyor; `/health/` açık kalıyor (307 → `/health`).
- Test: `tests/api/test_api_auth.py::test_trailing_slash_and_encoding_do_not_escape_key` — 5 yolun
  sondaki `/` varyantı başlıksız **401** (307 değil), başlıklıyken 200/307; `%76%31` varyantı
  başlıksız 401/başlıklı 200; `//v1/rules` 404; `/health` 200, `/health/` 307.
- Doğrulama: `ruff check`/`format --check` temiz (467 dosya), `mypy src/` 211 dosyada hatasız;
  `pytest -m "not live"` **3490 geçti**, 15 atlandı (G4 sonrası 3489 → +1 test);
  `npx vitest run src/lib/download.test.ts` 1 geçti (web değişmedi, doğrulama amaçlı).

**G6 (parça 1-2) — `config_writer` kullanıcı dosyasını bozmuyor (dizi tablosu + satır sonu):**
- **Dizi tablosu:** `[providers]` beklenmeyen biçimdeyse (dizi tablosu `[[providers.x]]` ya da tablo olmayan
  değer, ör. `providers = "ollama"`) `_table` üzerine yazmıyor; yazma
  `ValueError("codementor.toml'da [providers] beklenmeyen biçimde; elle düzeltin.")` ile duruyor ve dosya
  bayt bayt korunuyor (masaüstünde mevcut `ValueError` yakalayıcısı mesajı bildirim olarak gösterir).
- **Satır sonu:** dosya artık `newline=""` ile okunuyor; eskiden evrensel satır sonu çevirisi CRLF'li dosyayı
  sessizce LF'e döndürüyordu. Ölçüm (probe): `tomlkit.parse` CRLF girdisinde `dumps` yine CRLF verir ama
  **yeni eklediği bölümleri LF** yazar (`[limits]\r\nmax_lines = 1\r\n` + yeni `[yeni]` → `…\r\n\n[yeni]\na = 1\n`).
  Bu yüzden CRLF/LF dosyalarda çıktı önce LF'e indirilip dosyanın biçimine çevriliyor; LF dosyaya dokunulmuyor.
- `Path.read_text` `newline` parametresini yalnız 3.13'te aldığı için okuma `path.open(newline="")` ile
  yapılıyor (proje Python 3.12).
- Testler (`tests/desktop/test_config_writer.py`): `test_unexpected_providers_shape_is_not_overwritten`
  (dizi tablosu ve `providers = "x"` → `ValueError`, dosya bayt bayt değişmedi),
  `test_line_endings_are_preserved` (LF→LF, CRLF→CRLF; tek satır sonu bile dönüşmüyor, içerik TOML olarak
  tekrar yüklenebiliyor).
- **Doğrulama (G6-1/2):** `ruff check`/`ruff format --check` temiz (467 dosya); `mypy src/` 211 dosyada
  hatasız; `pytest -m "not live"` **3494 geçti / 15 atlandı** (G4+ sonrası 3490 → +4 test).

**G6 (parça 4-5) — ağ hata metni, `UsageTotals` katmanı, `primary_name`:**
- **Ağ hatası metni:** `cli/errors.py::describe` artık `ConnectionError`/`TimeoutError` (`OSError` alt
  sınıfları; `NETWORK_ERRORS`) için `ağ hatası (hedef): ayrıntı` yazıyor; ayrıntı yoksa
  "bağlantı kurulamadı ya da zaman aşımı". Dosya hatalarının "dosya işlemi başarısız" metni ve
  `system_errors` çıkış kodu 3 değişmedi.
- **Katman:** `UsageTotals` `storage/cache.py`'den `models/usage.py`'ye taşındı (veri sözleşmesi);
  `storage.cache` ve `report.usage` onu oradan içe aktarıyor. `rg -n "from codementor.storage"
  src/codementor/report` artık boş: rapor katmanı depo katmanını bilmiyor.
- **`primary_name`:** `LLMProvider` protokolüne `primary_name` özelliği eklendi. Zincirsiz adaptörler
  ortak `NamedProvider` tabanından türüyor (ollama, gemini, anthropic, claude_cli/agy, codex, fake ve
  eval'in `StaticOnlyProvider`'ı) ve kendi `name`'ini döndürüyor; `FallbackProvider` zincirin ilk
  halkasını. `orchestrator` artık `getattr(provider, "chain", [provider])` yoklamıyor: `run.cacheable`
  kararı `provider.primary_name` üzerinden veriliyor.
- Testler: `tests/unit/test_cli_errors.py` (5; ağ/dosya ayrımı, ayrıntısız zaman aşımı, `system_errors`
  çıkış 3 ve traceback'siz metin), `tests/unit/test_usage_label.py` (+2; tek tanım yeri ve rapor
  katmanında `storage` içe aktarımı yok), `tests/providers/test_factory.py` (+3; zincirin ilk halkası,
  tek sağlayıcı), `tests/providers/test_contract.py` (+1, her adaptörde `primary_name == name`).
- **Doğrulama (G6-4/5):** `ruff check`/`ruff format --check` temiz (469 dosya); `mypy src/` 212 dosyada
  hatasız; `pytest -m "not live"` **3511 geçti / 15 atlandı** (G6-3 sonrası 3496 → +15 test).
- Tamamlanan altı maddenin kabul ölçütleri: dosya baytları değişmiyor, `['genel', 'dizi']` kayıpsız,
  ağ hatası metni test edilmiş, rapor katmanında `storage` içe aktarımı yok, önbellek/fallback testleri
  yeşil.
- **G6 sonrası denetim (`48f4e16`):** `docs/mimari.md` §5.5.1 protokol örneğine `primary_name`, §16 dizin
  listesine `models/usage.py` eklendi (doküman koda senkron); yanlışlıkla commit edilmiş `.tmp_full.log`
  (10 KB) ve `.tmp_g1.log` (964 B) repodan çıkarıldı, `.gitignore`'a `.tmp_*.log` kuralı geldi. Denetim
  ayrıca `make check` eşdeğerini koştu: ruff/format temiz, `mypy` 212 dosya hatasız, 3511 geçti.

**G7 — `ProviderResult.schema_enforced` ve token kalibrasyon günlüğü:**
- **Şema zorlaması:** `models/provider.py::ProviderResult`'a `schema_enforced: bool = False` eklendi;
  rapora yazılmaz, tanı/loglama alanıdır (rapor şeması ve `schemas/` çıktısı değişmez).
  Anthropic (`output_config.format`), OpenAI uyumlu uç (`response_format.json_schema.strict`) ve Ollama
  (`format`) **True** bildirir; CLI alt süreçleri (claude_cli, agy, codex) **False** (alt süreç çıktısı
  sözleşmesi garanti değil; metinden JSON da gelebilir), fake sağlayıcının varsayılanı False.
- **Kalibrasyon:** `pipeline/llm_session._log_calibration`, sağlayıcı gerçek `usage.input_tokens`
  bildirdiğinde `log.debug("token_estimate_ratio", estimated=…, actual=…, ratio=…)` yazar. Oran
  `gerçek / tahmin`; 1'e yakınsa `prompts.budget.estimate_messages` (`⌈karakter/3⌉`) tutarlı demektir.
  Token muhasebesi, rapor alanları ve önbellek kararı değişmez (yalnız DEBUG satırı eklenir).
- Testler: `tests/providers/test_fake.py` (+1 varsayılan False), `tests/providers/test_adapters.py`
  (+2: ollama ve anthropic True), `tests/providers/test_gemini.py` (+1: openai_compat True),
  `tests/providers/test_cli_agent.py` (+2: claude_cli/agy False), `tests/providers/test_codex_cli.py`
  (+1 False), `tests/unit/test_usage.py` (+2: gerçek usage varken oran loglanır, yoksa loglanmaz).
  Sağlayıcı testlerinin tamamı respx/sahte çalıştırıcı ile ağsız koşar.
- **Doğrulama (G7):** `ruff check`/`ruff format --check` temiz (469 dosya); `mypy src/` 212 dosyada
  hatasız; `pytest -m "not live"` **3520 geçti / 15 atlandı** (G6-4/5 sonrası 3511 → +9 test).

**G5 / D20 — buildinfo logger, `--help` dil tutarlılığı, `eval run --language`, exe hariç tutmaları:**
- **`buildinfo.py` (D20-1):** modül düzeyindeki maskesiz `structlog.get_logger()` yerine
  `codementor.log.get_logger("codementor.buildinfo")`. Eskiden maskeleme küresel structlog
  yapılandırmasına bağlıydı; artık her çağrıda `redact_secrets` işlemcisiyle kuruluyor. Test:
  `tests/unit/test_buildinfo.py::test_build_info_logger_is_masked_project_logger` (JSON satırında
  `logger == "codementor.buildinfo"`, `level == "warning"`).
- **`--help` İngilizce metni (D20-2) — değiştirilemedi:** "Show this message and exit." Typer'ın kendi
  kopyasından geliyor: `typer/_click/decorators.py:624`
  (`kwargs.setdefault("help", _("Show this message and exit."))`), onu `TyperCommand.get_help_option`
  doğrudan çağırır. `context_settings`/Typer parametresi yok (yalnız `help_option_names`), click/Typer
  çeviri kataloğu (`.mo`) taşımıyor. Kendi `--help` seçeneğimizi yazmak plan dışı olduğu için metin
  bırakıldı; aynı gerekçe kullanım hatasındaki "Try '… --help' for help." ipucu için de geçerli.
- **`eval run --language` (D20-3):** `list[str]` → `list[Language]`. Geçersiz değer artık Typer kullanım
  hatası: **çıkış 2**, `Invalid value for '--language': 'cobol' is not one of 'c', 'cpp', 'csharp',
  'python', 'html', 'css'.`; `--help` tipi `<c|cpp|csharp|python|html|css>`. Filtre enum üzerinden
  (`s.label.language in set(language)`; `StrEnum` karma karışımı yok), `run_eval`'a `lang.value`
  geçilir (sözleşme `list[str]` kaldı). Testler: `test_eval_run_language_is_typer_enum`,
  `test_eval_run_help_lists_language_choices`.
- **Exe hariç tutmaları (D20-4):** `EXCLUDES`'a `uvicorn` eklendi (yalnız `cli/serve.py` kullanır;
  masaüstü exe CLI'ı içermez, ADR-0013). `fastapi`/`starlette` **denendi, duman testi düşünce geri
  alındı**: `--onedir` derleme (74 sn) + `.exe --self-check sc.json` → **çıkış 1**,
  `ModuleNotFoundError: No module named 'starlette'` (`desktop/launch.py` → `api/state.py` →
  `api/guard.py`; `guard` → `api/errors` → `fastapi` zinciri masaüstünde gerçekten yüklü). Yalnız
  `uvicorn` hariçken duman testi **çıkış 0** ve `sc.json` `"ok": true` (kaynak kökü, varsayılan toml,
  prompt şablonları, kontrol listeleri, 64 soru, 17 sorgu dosyası, C olgu çıkarımı, Roslyn
  denetleyicisi). Regresyon testi:
  `tests/desktop/test_build_exe.py::test_uvicorn_excluded_but_server_stack_kept`.
- **`[desktop]` extra (D20-5):** **yapılmadı** — kullanıcı kararı (CI/release/exe derlemesini etkiler;
  exe gerekli her şeyi `COLLECT_ALL`/`--add-data` ile paketliyor).
- **ADR-0030:** G6'da yapılan `primary_name` protokol eklemesinin karar kaydı yazıldı
  (`docs/adr/0030-primary-name-protokolu.md`: protokol üyesi, `NamedProvider` tabanı,
  `FallbackProvider` ilk halkayı döndürür; `orchestrator` sağlayıcıya özel `chain` alanını yoklamıyor).

**G5 durumu:** bitti (`c1a1b91`; D20-1/3/4 kod + build, D20-2 rapor, D20-5 kullanıcı kararı; +4 test).
Doğrulama: `ruff check`/`ruff format --check` temiz (470 dosya), `mypy src/` 212 dosyada hatasız,
`pytest -m "not live"` **3524 geçti / 15 atlandı** (G7 sonrası 3520 → +4 test); exe duman testi ayrıca
`--onedir` derleme + `--self-check` ile koşuldu (çıkış 0, `"ok": true`).

### Sıradaki oturum — Faz G kalanı (kayıt: 2026-10-15; G4+ denetimiyle güncellendi)

Durum: **G0-G4, G4+, G5/D20, G6 (altı maddenin tamamı) ve G7 bitti** (`062528c` G3 parçası → `313128c` D9-D11 → `3efcf80` G2 → `ed21509` G4 → `a92e23c` G4+ → `c3f64fa` G6-1/2 → `a39ec09` G6-3 → `644852b` G6-4/5 → `48f4e16` G6 denetim düzeltmeleri → `c403070` G7 → `c1a1b91` G5+D20 ve ADR-0030). Ağaç temiz; `ruff`/`ruff format --check`/`mypy src/` yeşil; `pytest -m "not live"` **3524 geçti / 15 atlandı** (G5 sonrası). **Kapanış (2026-10-16):** `orchestrator.py` 421 → **379**
satır (`Run`/`AnalysisTrace`/`PipelineError` ailesi `pipeline/run_state.py`'ye taşındı; içe aktarımlar
tek yönlü), D16 belge notu `docs/mimari.md` §12'ye yazıldı. Son ölçüm: `ruff check` +
`ruff format --check` temiz (**471 dosya**), `mypy src/` hatasız (**213 dosya**),
`pytest -m "not live"` **3524 geçti / 15 atlandı** (3:34).

**Düzeltme (G4 sonrası denetim):** listenin ilk sürümü D14/D15/D17/D19'u açık sanıyordu; kaynağı §5
tablosundaki ✅ işaretsiz satırlardı. Dördü de kapalı çıktı: D14/D15/D17 **Faz E**, D19 **Faz F**
(kod + test var; `tests/api` 123 test, `test_markdown_html_escaping`, `web/src/lib/download.test.ts`,
`tests/unit/test_storage.py` pragma testi yeşil). Tablo satırları ✅ işaretlendi; D14'ün sondaki `/`
sertleştirmesi bu oturumda yapıldı (G4+).

**Düzeltme (kapanış denetimi, 2026-10-16):** aynı türden bir bayatlık D20'de çıktı — §5 satırı
"`rules list` `[rules] disabled`'ı uygulamıyor" ve "kapanışta süren analiz/indirme için onay yok"
diyordu; ikisi de kapalı ve testli: sırasıyla **Faz C**
(`tests/unit/test_config_cli_faz_c.py::test_rules_list_marks_disabled` — kapalı/açık satırları) ve
**Faz F/F7** (`desktop/runtime.confirm_close`; `tests/desktop/test_app.py::test_close_while_busy_confirm`,
`::test_close_while_downloading_confirm`). Kod değişmedi; `Bulgular` D20 satırı ✅'e çekildi ve parça 6
notu eklendi. Böylece §5'te ✅ işareti olmayan D satırı kalmadı (D1-D20 tamamı ✅).

Kalan işler, önerilen sıra (her madde kendi commit'i + `PROGRESS.md`/`BulgularVeDuzeltilecekler.md` güncellemesi):

1. **G6 (denetimden ertelenen 6 madde):** ✅ **tamam** — parça 1-3: `desktop/config_writer` dizi
   tablosu + satır sonu (CRLF/LF) koruması ve `models/questions.from_question` (yalnız tamamen varsayılan
   listeler boşalıyor, `['genel', 'dizi']` düzenle→kaydet kayıpsız); parça 4-5: `cli/errors.describe` ağ
   hatası metni, `UsageTotals` → `models/usage.py`, `LLMProvider.primary_name`. — *kalan yok*
2. **G7:** ✅ **tamam** — `ProviderResult.schema_enforced` (anthropic/openai_compat/ollama True,
   CLI'lar False, fake varsayılanı False) + token tahmininin `usage` ile
   `log.debug("token_estimate_ratio")` kalibrasyonu (davranış değişmez, +9 test). — *kalan yok*
3. **G5 / D20:** ✅ **tamam** — `buildinfo.py` → `get_logger("codementor.buildinfo")`;
   `eval run --language` → `Language` enum (geçersiz değer çıkış 2 + izinli değer listesi);
   `build_exe.py` `EXCLUDES`'a `uvicorn` eklendi (`fastapi`/`starlette` denendi, `--self-check` çıkış 1
   verince geri alındı; yalnız `uvicorn` hariçken **çıkış 0**, `sc.json` `"ok": true`); `--help`
   İngilizce metni Typer/click ile **değiştirilemedi** (kaynak `typer/_click/decorators.py`;
   `context_settings` anahtarı ve `.mo` kataloğu yok). +4 test.
   - **Kullanıcı kararı (G5-5):** `pyproject.toml` `[desktop]` extra **yapılmadı** (CI/release/exe
     derlemesini etkiliyor).
   - **ADR-0030:** `primary_name` protokol eklemesi karar kaydına geçti.
4. **D16:** ✅ **tamam** — `session_id` sahipliği **yalnız belgeye** yazıldı (kod değişmedi):
   `docs/mimari.md` §12 tehdit tablosuna satır eklendi ("`session_id` yetki sırrı değildir; yerel tek
   kullanıcı varsayımıdır; paylaşılan sunucuda kimlik anahtara bağlanmalı — Sonraya"); `Bulgular` D16
   satırı ✅ ve §10 kutusuna not düşüldü.
5. **Dosya bölme:** ✅ **tamam** — `pipeline/orchestrator.py` **421 → 379 satır**; `Run`,
   `AnalysisTrace`, `PipelineError`, `PipelineErrorKind`, `ProviderFactory` ve `BANK_UNREADABLE`
   `pipeline/run_state.py`'ye taşındı. Bağımlılık yönü artık tek yönlü (`cache_flow`/`deadline` →
   `run_state`); `api/`, `cli/`, `desktop/`, `eval/` içe aktarımları yeni modüle çevrildi. `passes.py`
   **366** satır (< 400). **Kapanış denetimi bulgusu:** `providers/cli_agent.py` **420 satır** (> 400;
   Faz G'de dört kez değişti) — kullanıcı talimatıyla **madde 7 (G8)**'de kapatıldı.
6. **Faz G kapanışı:** ✅ **tamam** — `ruff check` / `ruff format --check` temiz (**472 dosya**),
   `mypy src/` hatasız (**214 dosya**), `pytest -m "not live"` **3524 geçti / 15 atlandı / 6 seçilmedi**
   (3:03). §3.1 Linux taklidi, G5-4 exe duman testi (`sc.json` `"ok": true`) ve dört denetim (dal içi
   G6, G4 sonrası, G5/D20, kapanış öncesi) `docs/DEVIR_FAZ_E_J.md`'de. Durum satırı ✅'e çekildi.
   - **Ortam notu:** bu makinede `make` yok; `make check` yerine dört komut tek tek koşuldu
     (`uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy src/`,
     `uv run pytest -m "not live"`). Not **G9**'da `AGENTS.md`'ye yazıldı.
7. **G8 — `providers/cli_agent.py` bölünmesi (420 → 345 satır):** ✅ **tamam** — sonuç ayrıştırma
   (`_json_document`, `_object_spans`, `_served_model`, `_mapping`) ve kimlik hatası sınıflandırması
   (`auth_error` + `_AUTH_HINTS`) yeni `providers/cli_result.py`'ye (104 satır) taşındı; `cli_agent` bu
   adları aynen yeniden dışa aktarır (G0 `passes.py` kalıbı; testler `cli_agent._json_document` içe
   aktarıyor), bu yüzden `git diff -- tests/` **BOŞ**. Commit `0472603`; doğrulama: `tests/providers` +
   `tests/unit/test_prompt_role_tags.py` **455 passed / 3 skipped**, `mypy src/` 214 dosyada hatasız.
8. **G9 — belge temizliği:** ✅ **tamam** — `docs/mimari.md` §20 ADR tablosuna ADR-0024/0025/0028/0029
   satırları eklendi (artık **30/30** ADR dosyası tabloda; kapanış denetiminde 26/30 idi) ve `AGENTS.md`
   "Komutlar" bölümüne "`make` her makinede yok; dört komut tek tek" notu yazıldı. Commit `c2968e2`.
9. **Kayıt:** ✅ **tamam** — Faz G madde madde teslim raporuna işlendi (`docs/YAPILANLAR_FAZ_E_J_ANTIGRAVITY.md`
   "Faz G" bölümü: G0-G9 + kapanış denetimi, her maddede commit + dosya + test + doğrulama; Özet
   tablosuna `G` satırı eklendi ve `F` satırı "sürüyor 3/0/10" → "tam 12/0/0" düzeltildi).


### Faz H — H1: 7 yeni statik kural (kayıt: 2026-10-16)

Dal `faz/h-kurallar` (`faz/g-saglayici` uç noktası `b67c94d` üstüne açıldı). Devir §8.2 tablosundaki
**yedi kuralın tamamı** yazıldı; C#'ta "döngüde `string +=`" zaten `CS-ALLOC-001` olduğu için alınmadı
(devir notu). Kural sayısı **34 → 41**.

| Kural | Dil | Kategori / Önem / Tür | Modül |
|---|---|---|---|
| CSS-ACC-001 — Odak göstergesi kaldırılmış | CSS | accessibility / medium / hata | `rules/css.py` |
| CSS-LAYOUT-001 — Sabit yükseklikte metin kutusu | CSS | edge_case / low / öneri | `rules/css.py` |
| CSS-LAYOUT-002 — Negatif margin ile ortalama | CSS | maintainability / low / öneri | `rules/css.py` |
| CPP-PERF-002 — Döngüde tam metin kopyası | C++ | performance / medium / hata | **yeni** `rules/cpp_perf.py` |
| CPP-PERF-003 — Döngüde `std::endl` | C++ | performance / low / öneri | `rules/cpp_perf.py` |
| CPP-PERF-004 — `reserve` olmadan `push_back` | C++ | performance / low / öneri | `rules/cpp_perf.py` |
| C-BUF-002 — Sınırı olmayan `scanf("%s")` | C | memory_safety / high / hata | **yeni** `rules/c_buffer.py` |

- **Dosya bölme:** `cpp.py` ve `c.py` 359 satırdı; yedi kuralı oraya eklemek 400 satır sınırını aşacaktı
  (AGENTS.md kod stili). Bu yüzden C++ performans kuralları `rules/cpp_perf.py`'ye (CPP-PERF-001 o turda
  `cpp.py`'de kaldı; **H denetimi düzeltmesiyle `cpp_perf.py`'ye taşındı**, bkz. "Faz H — denetim
  düzeltmeleri"), C tampon kuralı `rules/c_buffer.py`'ye taşındı — `c.py`/`c_memory.py` kalıbının
  aynısı. İki modül `rules/__init__.py`'de kayda girer; `docs/mimari.md` paket haritasındaki `rules/`
  modül listesi gerçek içerikle yazıldı.
- **Muhafazakâr sınırlar (her biri `catalog_note` ile katalogda yazılı):** CSS-ACC-001 yalnız `:focus`
  bloklarını tarar (aynı blokta `border`/`box-shadow`/`background`… ya da ayrı `:focus-visible` kuralı
  varsa susar); CSS-LAYOUT-001 yalnız `height: <sayı>px` (yüzde, `rem`, `min/max-height` ve tümü görsel
  öğelerden oluşan seçiciler kapsam dışı); CPP-PERF-002 yalnız `s = s + …` (aynı yalın ad sağda yaprak);
  CPP-PERF-003 yalnız `std::endl` yazımı (yalın `endl`, `std::flush` dışı); CPP-PERF-004 yalnız sınırı
  bilinen `for`/aralık döngüleri + koşulsuz `push_back`/`emplace_back` + `reserve`/`resize` yoksa;
  C-BUF-002 yalnız `scanf`/`fscanf` + biçim metin sabiti (`%99s` sınırlı, `%*s` atamasız; `sscanf` ve
  `%[` taraması kapsam dışı — bilinçli kaçırma, negatif fixture'la sabitlendi).
- **Fixture:** 7 kural × (2 pozitif + 2-3 negatif) = **32 dosya**, `tests/rules/fixtures/{ID}/…`;
  `tests/rules/test_all_rules.py` klasörleri otomatik bulur (kayıt/katalog değişikliği gerekmedi).
- **Süre:** `tests/rules/test_engine.py::test_linear_time_large_input` listesine **7 kötü niyetli 40 KB
  vaka** eklendi (CSS odak / sabit yükseklik / negatif margin, 5 000 terimli `+` zinciri, döngü içi
  `std::endl`, `push_back`, `scanf`); hepsi < 2 sn (kısıt: ≤ 40 960 bayt, ≤ 600 satır).
- **Katalog/belge:** `uv run codementor rules doc` → `docs/rules-catalog.md` "Toplam: 41 kural";
  `README.md` (3 yer) ve `README.en.md` (2 yer) kural sayısı 34 → 41.
- **Değişen testler (yalnız sayı bekleyenler):** `tests/unit/test_cli_rules.py` ("Kurallar (41)",
  `Engine.NONE` kümesi, CPP+Unreal kümesi) ve `tests/rules/test_registry.py::test_c_rules_only_for_c`
  (C kümesi). Davranış testleri değişmedi.
- **Doğrulama:** `ruff check` temiz, `ruff format --check` **474 dosya**, `mypy src/` hatasız (**216
  dosya**), `pytest -m "not live"` **3577 geçti / 15 atlandı / 6 seçilmedi** (3:01) — H1 öncesi 3524'e
  göre **+53 test** (32 fixture + 7 süre + 7 "her kuralın fixture'ı var" + 7 katalog türü).
- **Bilinçli sonda hatası (kayıt):** `selectors` alan adı tree-sitter-css'te yok; sonda betiği bunu
  yakaladı, `_selectors` konum çocuğuna çevrildi. Fixture'sız kural yazmanın riski burada somutlaştı.
- **Sonraki (Faz H kalanı):** H2 bilinen kaçırma/yanlış pozitifler, H3 analiz verisi (`call_costs`,
  `parse_bigo`, C# 11 ham metin maskeleme, Unreal stub, `-fdiagnostics-column-unit=byte`), H4 statik dev
  eval + README ölçüm satırları. Kapanışta `docs/ZAYIF_VE_GELISTIRILECEK_YONLER.md` §4.8'deki "34 kural"
  sayısı/dökümü de güncellenecek (`CHANGELOG.md`'ye §3.7 gereği dokunulmaz).

### Faz H — H2: bilinen kaçırma ve yanlış pozitifler (kayıt: 2026-10-16)

Devir §8.2 H2 tablosundaki altı satır madde madde denetlendi. Faz 21/32'de kapatılan beş satırda
davranış **zaten istenen** durumdaydı; bunlar yeni fixture'larla sabitlendi. Tek açık kalem
CPP-OWN-001'di ve **kural düzeltildi**.

| H2 satırı | Ölçülen davranış (H2 öncesi → sonrası) | Kanıt |
|---|---|---|
| CPP-OWN-001 erken `return`/`throw` yolunda atlanan `delete` | öneri → **hata** (düzeltildi) | `CPP-OWN-001/positive/early_return.cpp`, `throw_path.cpp` (kind: issue) |
| C-MEM-001 aynı dosyadaki `free` eden kullanıcı fonksiyonu | bulgu yok — zaten doğru (Faz 32) | `C-MEM-001/negative/passed_to_freeing_helper.c` |
| UNITY-GC-001 kullanıcı `struct`'ı için `new` | bulgu yok — zaten doğru (Faz 32) | `UNITY-GC-001/negative/user_struct_new.cs` |
| UE-GC-001 `TArray<AActor*>`/`TMap<…, UObject*>`; UCLASS olmayan sınıfta doğru öneri | bulgu var + `_UNREFLECTED` sorusu — zaten doğru (Faz 32) | `UE-GC-001/positive/container_fields.h`, `positive/plain_class_pointer.h`, `tests/rules/test_unreal_gc.py` |
| CS-PERF-001 `IList` + `IReadOnlyList` | bulgu var: `IList` → `List.Contains` (Faz 21), `IReadOnlyList.Contains` → `Enumerable.Contains` (H2) | `positive/ilist_parameter.cs`, `positive/ireadonlylist_linq_contains.cs` |
| Sıcak yol: MonoBehaviour/UCLASS tabanı yoksa sayılmaz | sayılmıyor — zaten doğru (Faz 32) | `UNITY-GC-001/negative/update_in_plain_class.cs`, `UNITY-PERF-001/positive/same_name_plain_class.cs`, `UE-PERF-001/positive/same_name_plain_struct.cpp` |

- **CPP-OWN-001 düzeltmesi (`rules/cpp.py`):** eşleşen `new`–`delete` çifti arasında **aynı kapsamda**
  erken çıkış (`return_statement`/`throw_statement`/`goto_statement`/`break_statement`/
  `continue_statement`) varsa serbest bırakma atlanabilir sayılır ve iki ucun bulgusu da `issue` olur.
  Uygulama: kapsam → atlama baytları sözlüğü bir kez kurulur (`_jump_positions`), çift eşlemesi
  (`_matched_pairs`) ad başına belge sırasında yürür, çıkış sorgusu `bisect` ile **O(log n)**
  (`_skips_delete`) — 40 KB girdide doğrusal kalır. Lambda gövdesindeki atlamalar dışarıdan çıkış
  sayılmaz (en içteki lambda aralığı ikili aramayla bulunur).
- **Yanlış pozitife karşı sabitlenen sınırlar:** ayrı kapsamdaki `return` (`other_scope_return.cpp`)
  ve `delete`'ten sonraki `return` öneri kalır; lambda içindeki `return` (`lambda_between.cpp`) da
  öneri kalır. Ölçüm: erken `return`/`throw` → `issue`, diğer üç durum → `suggestion` (sonda).
- **Kapsam notu:** kural yalnızca *tür* yükseltmesi yaptı; satır/eşleşme mantığı (Faz 52) değişmedi,
  bu yüzden mevcut `new_delete.cpp` / `array_new.cpp` fixture'ları öneri olarak geçmeye devam ediyor.
  `catalog_note` eklendi (katalogda "Kapsam ve sınırlar" satırı).
- **CS-PERF-001 `IReadOnlyList`/`ICollection` (onay sonrası uygulandı):** kök neden `using System.Linq`
  altında `IReadOnlyList<T>.Contains` **zaten** `Enumerable.Contains` (n) olarak çözülüyordu; eksik
  olan kuralın `Enumerable` alıcısını tanımamasıydı → `rules/csharp.py::_LINEAR_COLLECTIONS`'a
  `"Enumerable"` eklendi. `ICollection` ise **bilinçli kaçırma** olarak korundu: `ICollection<T>.
  Contains` örnek metottur (alıcı bir `HashSet` olabilir) ve C# çözümlemesinde LINQ uzantısı
  *bağlanmaz*; bunun için `analysis/call_costs.py::_INSTANCE_METHODS` ile LINQ aday üretimi
  engellendi (yani `ICollection` eskiden yanlışlıkla `Enumerable.Contains`'e bağlanıyordu — bu
  düzeltme aynı zamanda bir doğruluk iyileştirmesi, Faz 21 kararının kodda karşılığı).
  Kapsam `catalog_note` ile yazıldı. Fixture'lar: `positive/ireadonlylist_linq_contains.cs`,
  `negative/icollection_in_loop.cs`, `negative/readonly_list_outside_loop.cs`; çözücü davranışı
  `tests/unit/test_call_costs.py::test_icollection_with_linq_still_unknown` ve
  `::test_ireadonlylist_contains_costs_linear` ile sabitlendi.
- **Süre:** `tests/rules/test_engine.py::test_linear_time_large_input` listesine H2 vakası eklendi
  (tek kapsamda 660 `new`–`delete` çifti + 660 `return`; 36 490 bayt / 168 satır — kısıtlar
  40 960 bayt ve 600 satır). İlk deneme satır sınırını aştı (`CodeTooLargeError: 732 satır`); vaka
  satır başına dört çift olacak biçimde yeniden kuruldu.
- **Kayıt:** `docs/BulgularVeDuzeltilecekler.md` §10 Faz H "Bilinen kaçırmalar ve yanlış pozitifler"
  kutuları işaretlendi; `docs/rules-catalog.md` `codementor rules doc` ile yeniden üretildi (yalnız
  CPP-OWN-001 kapsam satırı değişti — kural sayısı 41 aynı).
- **Doğrulama:** `ruff check` temiz, `ruff format --check` 474 dosya, `mypy src/` hatasız (216 dosya),
  `pytest -m "not live"` **3587 geçti / 15 atlandı / 6 seçilmedi** (3:33) — H2 öncesi 3577'ye göre
  **+10 test** (4 CPP-OWN-001 fixture'ı, 1 süre vakası, 3 CS-PERF-001 fixture'ı, 2 çözücü testi).

### Faz H — H3: analiz verisi (kayıt: 2026-10-16)

Devir §8 H3'ün altı maddesi ele alındı: beşi kod değişikliğiyle kapandı, `n^k` bilinçli olarak
reddedilmeye devam ediyor (mimari metni bu gerçeğe göre düzeltildi) ve **madde 4'te beklenmeyen bir
boşluk** bulundu: delege bildirimleri analizi tamamen düşürüyordu.

| H3 maddesi | Sonuç | Kanıt |
|---|---|---|
| `call_costs`: `RemoveAt(0)`/`Insert(0, …)` O(n) ayrımı | **yapıldı (argümana duyarlı)**: `RemoveAt(xs.Count - 1)` → `1`, `Insert(xs.Count, …)` → `1*`; `0`/bilinmeyen indeks → `n` | `analysis/call_costs.py::_refined_cost`, `tests/unit/test_call_costs.py` (11 çözücü + 4 olgu vakası) |
| `parse_bigo`: `Θ(...)`/`Ω(...)` | **eklendi**: iç ifadeye indirger, gösterim `O(...)`; yalnızca tam ifadeyi sarabilir | `tests/unit/test_bigo.py::test_theta_and_omega_wrappers_inner_expression`, `::test_wrapper_only_at_expression_start` |
| `parse_bigo`: `max(a, b)` | **eklendi**: çok değişkenli toplam olarak normalleşir (`max(a,b) = Θ(a+b)`) | `::test_max_is_normalized_to_sum`, `::test_max_requires_two_arguments_and_parentheses` |
| `parse_bigo`: `log log n` | **eklendi**: modele `log_log_power` çarpanı; `log(log n)` = `log log n`; `log log log n` reddedilir | `models/_bigo_algebra.py`, `::test_log_log_n`, `::test_log_log_ordering_and_roundtrip` |
| `parse_bigo`: `n^k` (değişken üs) | **reddediliyor** (sembolik üs modellenmiyor; `2^n` destekli); `docs/mimari.md` §5.6'daki yanıltıcı `n^k` örneği düzeltildi | `::test_variable_exponent_of_variable_base_is_rejected` |
| 40 KB anlamsız girdide hızlı hata | **eklendi** (süre testi) | `::test_hostile_overlong_input_fails_fast`, `::test_hostile_nesting_within_limit_fails_fast` |
| C# 11 ham metin maskeleme | **eklendi** (`mask_non_code(text, language=None)`) | `analysis/lexical.py`, `tests/unit/test_lexical.py` (+12 test) |
| Unreal stub: `FMath`, `FHitResult`, delegeler, timer | **eklendi** (+ ayrıştırma yolunda delege makroları) | `data/stubs/ue_stubs.h`, `tests/unit/test_ue_stubs.py`, `unreal_wave_spawner.cpp` |
| Include koruması `#pragma`/`#line` izin listesi | **eklendi (güvenlik)** | `validation/include_guard.py`, `tests/unit/test_include_guard.py` (+16 red / +12 izin vakası) |
| Tier 1 kolon birimi bayt | **eklendi** + bayrağı tanımayan sürümde bayraksız yeniden deneme | `validation/tier1.py`, `tests/unit/test_tier1.py`, `tests/compiler/test_tier1_compiler.py` |



1. **`call_costs` argümana duyarlı indeks (madde 1).** Tablo değeri `List.RemoveAt`/`List.Insert` için
   `n` (muhafazakâr: kaydırma olabilir). Ayrım için `CallName`'e **`first_arg`** alanı eklendi
   (`analysis/_symbols.py`; 120 bayttan uzun argüman okunmaz → `…`, `_MAX_RECEIVER_BYTES` ile aynı
   ilke). `_refined_cost` yalnızca **aynı liste** üzerinde daraltır: `xs.RemoveAt(xs.Count - 1)` →
   `1`, `xs.Insert(xs.Count, …)` → `1*`. `RemoveAt(0)`/`Insert(0, …)` tablo değeriyle (`n`) kalır;
   `other.Count - 1` gibi başka koleksiyonun indeksi `n` sayılır (yanlış `1` demek yanlış negatif
   olurdu). `this.`/`this->`/`base.` önekleri iki tarafta da kırpılır.
2. **`parse_bigo` (madde 2).** `Θ(...)`/`Ω(...)` (ve küçük harfleri) sarmalayıcı belirteci olarak
   token'laştırılır; yalnızca tam ifadeyi sarabilir (`n * Θ(m)` reddedilir). `max(a, b, …)` en az iki
   argüman ister ve toplam olarak temsil edilir (Big-O'da `max(a,b) = Θ(a+b)`; `V+E` ile aynı model).
   `log log n` için modele **`log_log_power`** çarpanı eklendi; alan sırası büyüme önceliği olduğundan
   `log_power`'dan sonra gelir (`1 < log log n < log n < n` sıralaması korunur, mevcut ifadelerin
   davranışı değişmez). `log(log n)` = `log log n`; `log((log n)^k)` = `Θ(log log n)` (sabit katsayı
   düşer); `log log log n` desteklenmez (açık hata). `n^k` **eklenmedi**: model sayısal taban + sembolik
   üs (`2^n`) taşıyor, sembolik üs modellenmeden `n^k`'yi `n` saymak sessiz bir yanlış olurdu.
3. **C# 11 ham metin (madde 3).** `mask_non_code(text, language=None)`: `language=Language.CSHARP`
   iken en az üç tırnakla açılan ham metin (ve `$`/`$$` önekli biçimler) içeriği boşlukla maskelenir,
   açılış/kapanış tırnakları yerinde kalır (satır/uzunluk korunur, tek geçiş = doğrusal). Çağıranlar:
   `analysis/extractor.py` dili geçirir; `ingest/detect.py` (dil burada belirleniyor),
   `validation/include_guard.py` ve `parsers.neutralize_unreal_macros` bilinçli olarak varsayılanla
   kalır — davranışları değişmedi, korumanın fail-closed tarafı aynı.
4. **Unreal stub (madde 4) + bulunan boşluk.** Stub'a `FMath` (`Clamp`/`Abs`/`Max`/`Min`/`Sqrt`,
   `if constexpr` ile işaretsiz tip uyarısı doğmadan), `FHitResult`, `FTimerManager` + `AActor`/
   `UActorComponent::GetWorldTimerManager()`, `FTimerHandle` (vardı) ve
   `DECLARE_DYNAMIC_MULTICAST_DELEGATE*` (0–5 parametre) makroları eklendi; makrolar alan olarak
   kullanılabilen boş bir struct üretir (`Broadcast`/`AddDynamic`/`RemoveDynamic`/`Clear`).
   **Denetim sırasında bulundu:** `DECLARE_DYNAMIC_MULTICAST_DELEGATE_*(...)` dosya kapsamında çıplak
   makro çağrısı olduğu için tree-sitter bunu ayrıştıramıyordu → Tier 0 "sözdizimi hatası" → erken
   çıkış (Tier 1 hiç çalışmıyordu). Yani delege kullanan **geçerli Unreal kodu yanlışlıkla hatalı**
   sayılıyordu ve stub desteği erişilemez kalacaktı. Çözüm: makrolar yalnızca **ayrıştırma yolunda**
   boşaltılır (`neutralize_unreal_macros(..., delegates=True)` ← `parse_source`); **derleyici yolunda
   boşaltılmaz**, çünkü tipi stub tanımlar (boşaltılsaydı delege adı tanımsız kalırdı).
   `unreal_wave_spawner.cpp` fixture'ı yeni API'yi (delege alanı + `Broadcast`, `FMath`, `FHitResult`,
   `GetWorldTimerManager().SetTimer/ClearTimer`) kullanacak biçimde genişletildi; böylece hem Tier 0
   ayrıştırması hem `-m compiler` (CI) bu yolu sınar.
5. **Include koruması izin listesi (madde 5, güvenlik).** `#pragma` operandı artık izin listesidir
   (`once`, `region`, `endregion`); operand **maskelenmiş** metinden okunur ve yalnızca yönerge
   konumunda denetlenir. Gerekçe somut bir atlatma: `#define X GCC dependency "/etc/passwd"` +
   `#pragma X` — derleyici makroyu açar, isim dizesi satırda geçmediği için eski kural görmezdi
   (`_Pragma(...)` yolu zaten kapalıydı). Aynı nedenle izin listesindeki adları tanımlayan `#define` de
   reddedilir. `#line` yalnızca `#line <sayı>` biçiminde geçer (dosya adı yok); yönerge konumu aranır,
   çünkü `#line` host dosyası okumaz — riski sahte tanı konumudur ve yorum/metindeki geçişin yanlış
   pozitif üretmesi gerekmez. **Bilinçli yan etki:** `#pragma pack`/`#pragma warning` gibi diğer
   pragmalar artık Tier 1'i atlatır (`SKIPPED` + Türkçe uyarı; fail-closed). Depodaki tüm fixture,
   eval veri seti ve stub taramasında yalnızca `#pragma once` var (başka pragma/`#line` yok) — bu
   yüzden ölçüme ve katalog testlerine etkisi yok.
6. **Kolon birimi (madde 6).** Tier 1 komutuna `-fdiagnostics-column-unit=byte` eklendi: gcc'nin
   varsayılanı `display`, clang'ınki `byte` olduğu için aynı kod iki derleyicide farklı kolon
   verebiliyordu; artık ikisi de bayt (Tier 0 karakter sayar → ASCII satırlarda özdeş, Unicode'da
   farklı olabilir; belgelerde yazılı). Bayrağı tanımayan eski sürümde (`stderr` bayrağı anıyorsa)
   komut **bir kez bayraksız** yeniden denenir — yerelleştirilmiş "bilinmeyen seçenek" mesajları da
   yakalanır; en fazla bir fazladan çağrı maliyeti, sessiz atlama yok. `tests/compiler` tarafına
   Unicode içeren geçerli C örneği eklendi.
- **Doğrulama:** `ruff check` temiz, `ruff format --check` **474 dosya**, `mypy src/` hatasız (**216
  dosya**), `pytest -m "not live"` **3717 geçti / 16 atlandı / 6 seçilmedi** (3:49) — H2 sonundaki
  3587'ye göre **+130 test** (`-m compiler` yerel: **81 geçti / 10 atlandı**; bu makinede gcc/clang
  yok, C/C++/Unreal derleyici testleri CI'da koşar — stub/fixture derleme doğrulaması yerelde
  **yapılamadı**, raporda işaretli).
- **Kayıt:** `docs/mimari.md` §5.2.2 (komut tablosu, stub içeriği, delege notu), §5.2.3 (include izin
  listesi + kolon birimi), §5.3.2 (argümana duyarlı maliyet), §5.6 (Big-O dilbilgisi);
  `data/call_costs.yaml` başlık notu; `docs/BulgularVeDuzeltilecekler.md` §10 H3 kutuları.

### Faz H — H4: statik dev ölçümü (kayıt: 2026-10-16)

- **Koşu:** `uv run codementor eval run --split dev --static-only` (LLM yok, ağ yok) →
  `eval/results/20261016T212522_static_none_static_dev.json` (96 örnek).
  Eski sonuç dosyaları **silinmedi** (devir kuralı); karşılaştırma `eval compare` ile.
- **Önce/sonra (yalnızca statik, dev 96):**

| Koşu (kurallar) | Denetim P | R | F1 | Big-O birebir/sınıf | Erken çıkış P/R | p50 / p95 |
|---|---|---|---|---|---|---|
| `20261003T211404` (r1) | %100 | %57,8 | %73,2 | %97/%97 | %100/%100 | 0,09 / 0,53 sn |
| `20261005T151516` (r2, H1 sonrası) | %100 | %55,2 | %71,1 | %97/%97 | %100/%100 | 0,11 / 0,68 sn |
| `20261016T212522` (r2, H2+H3 sonrası) | %100 | %57,5 | %73,0 | %97/%97 | %100/%100 | 0,13 / 0,80 sn |

- **Precision düşmedi** (%100 → %100): H1'in yedi yeni kuralı yanlış pozitif üretmiyor (H4'ün asıl
  kontrolü buydu). Recall H1 sonrası %55,2'den %57,5'e çıktı (H2'nin CS-PERF-001 `IReadOnlyList`
  düzeltmesi bir etiketi daha yakalıyor), F1 %71,1 → %73,0. Gecikme p50 125 ms (kural sayısı arttı).
- **README:** "dev" eval bloğu `eval compare` çıktısından **yeniden üretildi** (bir yeni statik satır +
  bir yeni sürüm satırı; elle düzenlenmedi); özet tablodaki "Yalnızca statik" dev satırı
  `100 / 55 / 71` → **`100 / 57 / 73`** ve H4 notu eklendi. `tests/unit/eval/test_readme_table.py`
  **değiştirilmedi** ve yeşil. Test bölümü `--final` olmadan koşulmadı (H4 kapsamı dev; test koşusu
  sürüm öncesi kullanıcı kararı).
- **`docs/ZAYIF_VE_GELISTIRILECEK_YONLER.md` §4.8:** bayat "34 kural / CSS ve C++ en zayıf / recall
  %55" satırları güncel sayımla değiştirildi (41 kural; C 8, C++ 9, C# 7, HTML 6, CSS 6, Python 5;
  Unity 4, Unreal 3; statik recall %57,5) — H1 kapanış notunda işaretlenen iş.
- **Doğrulama:** `ruff check` temiz, `ruff format --check` **474 dosya**, `mypy src/` hatasız (**216
  dosya**), `pytest -m "not live"` **3717 geçti / 16 atlandı / 6 seçilmedi** (3:49); Linux taklidi (§3.1,
  `block_tk`) → **3624 geçti / 17 atlandı / 6 seçilmedi** (toplama hatası yok).

Sonraki faz: **Faz H** (`faz/h-kurallar`) — **H1, H2, H3 ve H4 bitti**; devir tablosundaki yedinci
kural olan C# "döngüde `string +=`" zaten `CS-ALLOC-001` olduğundan yerine C-BUF-002 alındı
(yukarıdaki tablo); H2'de altı satır denetlendi (CPP-OWN-001 erken çıkış + CS-PERF-001
`IReadOnlyList` düzeltmeleri), H3'te altı analiz-verisi maddesi kapandı (tek istisna `n^k`),
H4'te statik dev ölçümü yenilendi (precision %100, F1 %73) ve README/§4.8 sayıları sonuç
dosyalarından güncellendi. **Kalan iş: yok** — faz kapanışı `485e69a` (teslim raporu
`docs/YAPILANLAR_FAZ_E_J_ANTIGRAVITY.md` "Faz H" bölümü) ve denetim düzeltmeleri aşağıdaki kayıtta
kapandı; `main`, `faz/h-kurallar` ucuna **hızlı ileri** alındı (Faz F/G/H birlikte). Faz I ve Faz J
devirde kapsam dışı/isteğe bağlı (§9, §10).

### Faz H — denetim düzeltmeleri (kayıt: 2026-10-17 — `ae86816`, `fd4bad7`, `39e94de`)

- **Bağlam:** Faz H tesliminden sonra uçtan uca denetim yapıldı: `git diff b67c94d..485e69a` = 79 dosya,
  +11 404/−103; kapsam dışı dosya yok; **41 kayıt / 41 benzersiz kural kimliği**; dört denetim yeşil
  (3717 geçti); katman/şema/güvenlik sapması yok. Karar: **birleştirilebilir** (kritik bulgu yok; tek
  doğrulanamayan boyut yerelde koşulamayan `-m compiler`). Denetimin bıraktığı iki bulgu bu dalda
  (`faz/h-denetim`) kapatıldı.
- **1) CSS-ACC-001 aşırı susturma (`src/codementor/rules/css.py`):** dosyada yalın bir `:focus-visible`
  kuralı varsa (`_focus_visible_bases` kümesinde `""`) kural **tüm** `:focus { outline: none }`
  bloklarını susturuyordu. `:focus-visible` (0,1,0) ile `.x:focus` (0,2,0) karşılaştırıldığında
  özgüllük `.x:focus` lehine olduğu için bu gerçek bir a11y kaçırmasıydı. `or "" in covered` koşulu
  kaldırıldı; susturma artık yalnız **aynı kök seçici** için geçerli (yalın `:focus` ↔ yalın
  `:focus-visible` eşleşmesi korunuyor). `catalog_note` yeni davranışı yazıyor,
  `docs/rules-catalog.md` yeniden üretildi.
- **2) `rules/cpp.py` 452 satır (AGENTS.md 400 satır sınırı):** H2'nin CPP-OWN-001 düzeltmesi dosyayı
  93 satır büyütmüştü. CPP-PERF-001 bloğu (`_LARGE_TYPES`, `_PARAMETERS`, `_MOVES`,
  `_function_declarator`, `_Kept`, `_kept_argument`, `_is_large`, kural sınıfı) `rules/cpp_perf.py`'ye
  taşındı → `cpp.py` **338**, `cpp_perf.py` **360** satır. Taşıma davranışsız: içerik birebir, mevcut
  fixture/test **değişmedi**, yalnız kullanılmayan `strip_templates` içe aktarımı temizlendi.
- **3) Kabul edilen küçük notlar (düzeltme yok):** aynı `scanf` satırında `c_buffer.py` + C-IO-001'den
  ikili bulgu (sunum gürültüsü), `cpp_perf.py` yerel sınıf metotlarını atlamıyor (muhafazakâr kaçırma),
  `tier1.py:219` geniş `except` (günlükle sınırlı, H öncesinden). Üçü de
  `docs/BulgularVeDuzeltilecekler.md` §10'a işlendi.
- **5) Denetim Önemli-3 kapandı (izin listesi genişletildi, 2026-10-17, `faz/h-pragma-izin`):** kullanıcı
  kararıyla `validation/include_guard.py` izin listesine `pack` ve `warning` alındı: hiçbir dosyayı
  okumazlar (GCC `dependency` gibi bir yan biçimi yok); öncesinde bu pragmaları içeren dosya Tier 1'i
  gereksiz atlıyordu. `_PRAGMA_NAMES` demeti tek kaynak: `_PRAGMA_ALLOWED` regex'i ve
  `_PRAGMA_RESERVED` kümesi ondan **türetilir** — ayrı tutulursa `#define pack GCC dependency "…"` +
  `#pragma pack` makro atlatması (H3'te kapatılan yol) geri açılır. Ad eşleşmesi harf duyarlı ve tam
  sözcük: `#pragma PACK(1)`, `#pragma packable`, `#pragma warning(GCC dependency "…")` hâlâ reddedilir;
  `#define pack`/`#define warning` tanımlayan dosya fail-closed atlanır (Türkçe gerekçe gösterilir).
  Kullanıcıya dönük hata metni de listeden üretiliyor (`_PRAGMA_LIST_TEXT`); `docs/mimari.md` §5.2.3,
  `docs/BulgularVeDuzeltilecekler.md` §10 ve `docs/YAPILANLAR_FAZ_E_J_ANTIGRAVITY.md` güncellendi.
- **Mutasyon denetimi (devir §2/§7 — düzeltme geri alınınca test düşüyor):** izin listesi eski hâline
  alınınca `tests/unit/test_include_guard.py` **9 test** düşüyor; yalnız `_PRAGMA_RESERVED`
  daraltılınca **3 test** düşüyor (`define_pack_macro`, `define_pack_macro_with_pragma`,
  `define_warning_macro`). Vakalar: 103 → 116 (`pragma_pack`/`pragma_warning` REJECTED → ALLOWED
  taşındı — bilinçli davranış değişikliği; aynı dosyada 6 yeni red vakası makro atlatmasını koruyor).
  `pytest -m "not live"` **3719 → 3732 geçti** (16 atlandı, 6 seçilmedi); mevcut testlerden hiçbiri
  gevşetilmedi/silinmedi.
- **Tier 1 entegrasyon testleri (aynı gün, Önemli-3 doğrulama turu):** izin listesi kararı yalnız birim
  düzeyinde değil **gerçek Tier 1 yolu** üzerinde de sabitlendi — `tests/unit/test_tier1.py` **+6 vaka**:
  (a) `#pragma pack`/`#pragma warning` içeren C++ dosyası derleyiciye ulaşır (`PASSED`, atlama yok),
  (b) Unreal yolundaki **iki** guard çağrısından da geçer, (c) sahte derleyici = `sys.executable` ile
  **gerçek alt süreç** başlatılır ve gcc tanı ayrıştırma yolu denenir, (d) `#define pack`/`#define warning`
  + `#pragma` makro atlatması `SKIPPED`/`include_guard` (süreç hiç başlamaz), (e) `#pragma PACK(1)` harf
  duyarlılığı korunur. Mutasyon: izin listesi eski hâline alınınca bu 3 yeni test + 9 birim testi düşer;
  `_PRAGMA_RESERVED` ayrı tutulup daraltılınca **6 test** düşer. `pytest -m "not live"` **3732 → 3738
  geçti** (16 atlandı, 6 seçilmedi); kaynak kod değişmedi, yalnız test eklendi.
- **Testler:** 2 yeni fixture (`CSS-ACC-001/positive/global_focus_visible_override.css`,
  `…/negative/bare_both.css`) → `pytest -m "not live"` **3717 → 3719 geçti** (16 atlandı, 6 seçilmedi,
  4:12). Fixture'lar otomatik bulunur; test kodu değişmedi.
- **Ölçüm:** statik dev yeniden koşuldu (`eval/results/20261017T161712_static_none_static_dev.json`):
  precision **%100** (değişmedi), recall **%57,5** (0,5747 — değişmedi), F1 **%73,0**, Big-O %97/%97,
  erken çıkış %100/%100, p50 0,14 sn. README `eval-table:dev` bloğu sonuç dosyalarından yeniden
  üretildi; `tests/unit/eval/test_readme_table.py` değişmedi ve yeşil.
- **Doğrulama:** `ruff check` temiz, `ruff format --check` **474 dosya**, `mypy src/` hatasız (**216
  dosya**), `pytest -m "not live"` **3719 geçti / 16 atlandı / 6 seçilmedi** (4:12).

Bilinen kararsız test (değişiklikle ilgisiz): `tests/rules/test_engine.py::test_linear_time_large_input[html-*]`
yük altında 38 sn'yi geçip düşebiliyor; tek başına geçiyor.

## Faz F — Notlar (masaüstü sağlamlık ve kullanılabilirlik; 2026-10-14)

### Yapılanlar
- **F0 (app.py controller'lara bölündü):** `history_controller.py` (141 satır) ve `config_controller.py` (89 satır) modülleri oluşturuldu; `app.py` 397 satıra düşürüldü (< 400).
- **F1 (O10 Bozuk veritabanı kurtarma):** `runtime.backup_corrupted_db` (`codementor.db.bozuk-YYYYAAGG-SSDDss`), `launch.py` onaylı yedekleme kurtarma mekanizması ve `App.report_callback_exception` eklendi; `tests/desktop/test_launch_db.py` yazıldı. Windows dosya kilidi ve `gc.collect()` çözüldü.
- **F2 (O13 Dışa aktarma hatası bildirimi):** `history_controller.export` içinde `OSError` yakalanıp Türkçe toast ile bildirildi; test eklendi.
- **F3 (O14 Geçmişi temizle gizlilik ve disk temizliği):** `storage/cache.py::clear_analyses` içine `VACUUM` ve `PRAGMA wal_checkpoint(TRUNCATE)` eklendi; `clear_history`'ye `app.save_prefs(recent_files=[])` bağlanarak son dosyalar listesi temizlendi; `tests/unit/test_storage.py`'de `clear_analyses` sonrası diskte öğrenci kodu kalmadığı bayt düzeyinde doğrulandı; `tests/desktop/test_app.py`'de `recent_files` boşalması doğrulandı.
- **F4 (D19 Veritabanı sağlamlığı ve meşguliyet kontrolleri):** SQLite bağlantı dinleyicisine `PRAGMA journal_mode=WAL`, `busy_timeout=5000`, `secure_delete=ON`, `user_version=1` (`_migrate`) eklendi; analiz sürerken (`app.analyze_view.busy`) `HistoryView` satırlarındaki "Sil" butonu `disabled` yapıldı ve `delete_history` çağrısı toast ile engellendi; `StorageSettings.session_retention_days = 90` varsayılanı `codementor.toml` ve `docs/mimari.md` §11, §17'ye işlendi; 90 günden eski oturumların açılışta budanması test edildi.
- **F5 (D18 Dosya kaydetme, CRLF koruması ve kirli durum takibi):** `FileController`'a `save()`, `save_as()`, `confirm_discard()` metodları eklendi; dosya açma, sürükleme, geçmiş yükleme, soru seçme ve pencere kapatmada kaydedilmemiş değişiklik onayı sağlandı; Ctrl+S kısayolu bağlandı; orijinal satır sonu (`\r\n` / `\n`) kaydedilirken korundu; kaydetme hatası toast ile bildirildi; `CodeEditor.set()` içindeki `edit_modified(False)` sıfırlamasıyla programatik yüklemelerin yanlış dirty algısı önlendi.
- **F6 (Geçmişte sayfalama ve arama):** `storage/cache.py::list_analyses_page`'e `search` parametresi eklendi; soru kimliği, dil ve sağlayıcı alanlarında büyük/küçük harf duyarsız `ilike` filtreleme yapıldı; SQL `LIKE` joker karakterleri (`%`, `_` ve `/`) kaçışlandı; `HistoryView` üstüne arama kutusu ve altta dinamik "Daha fazla yükle" butonu eklendi; 60 kayıt ile 50+10 sayfalama, "c-medium" tekil araması ve joker kaçışları birim ve masaüstü duman testleriyle doğrulandı.
- **F7 (Kapanırken "sürüyor" onayı):** Kapanış mantığı `runtime.confirm_close(app)` yardımcısına taşındı; `App.close` kirli dosya onayından sonra `app.analyze_view.busy` ya da süren zig indirmesi (`connections.download_cancellation is not None`) varsa `confirm("Çıkış", "Analiz (ya da indirme) sürüyor. Çıkılsın mı?")` ile onay ister; Hayır → pencere kapanmaz. `app.py` 398 satırda tutuldu (< 400). Testler: `tests/desktop/test_app.py::test_close_while_busy_confirm`, `::test_close_while_downloading_confirm` (ikisi de `confirm` casusluğuyla, ağsız).
- **F8 (ADR-0021 eski OpenAI/DeepSeek anahtarları):** `connections.LEGACY_KEY_PROVIDERS = ("openai", "deepseek")` ve `KeyStore.purge_legacy() -> int` (mevcut `get`/`delete` yeniden kullanılır; kasa kilitliyse Türkçe `KeyStoreError`); `ConnectionsController.purge_legacy_keys()` sonucu toast'lar ("N eski anahtar kimlik kasasından silindi" / "Silinecek eski anahtar bulunamadı"); bağlantılar ekranına "Eski anahtarları temizle" düğmesi (`connections_view.purge_legacy_button`) eklendi ve `app.py`'de `purge_legacy=self.connections.purge_legacy_keys` ile bağlandı. Testler: `test_purge_legacy_removes_only_removed_providers` (2 eski + 1 güncel kayıt → 2 silinir, güncel kalır; ikinci çağrı 0), `test_purge_legacy_locked_vault_is_turkish_error`, `test_purge_legacy_keys_button` (pencere duman testi).
- **F9 (Kurulu zig eskiyse "güncelle" önerisi):** `validation/toolchain_install.py`'ye `installed_marker(root)` (işaretçiyi okur; yoksa/bozuksa `None`) ve `needs_update(settings, *, platform=None) -> bool` eklendi: kurulum yoksa, işaretçi okunamıyorsa ya da platform için kaynak tanımlı değilse `False`; aksi hâlde işaretçideki `version` **ya da** `sha256` yapılandırmadan farklıysa `True`. Masaüstünde GUI'siz sarmalayıcı `services.compiler_update_available(settings)`; bağlantılar denetleyicisi bunu `show_compilers(...)`'a geçirir. Kartta "Güncelleme var: kurulu zig, yapılandırmadaki sürümden farklı." metni ve **"Derleyiciyi güncelle"** düğmesi görünür; indirme akışı (ilerleme, iptal, sha256 doğrulaması, atomik kurulum) aynen yeniden kullanılır, `offer_compiler_download` davranışı değişmedi. Testler: `tests/unit/test_toolchain_install.py::test_needs_update_only_when_marker_differs`, `::test_needs_update_false_on_missing_or_broken_marker`, `::test_needs_update_false_without_configured_source` (sahte dizin + işaretçi, ağ yok); `tests/desktop/test_app.py::test_compiler_update_button_when_installed_zig_is_old`, `::test_compiler_update_button_downloads_through_same_flow`.
- **F10 (Bağlantılar'da `ollama pull` düğmesi):** GUI'siz yardımcılar `desktop/services.py`'ye eklendi: `ollama_pull_argv(model, search_path)` → `[mutlak yol, "pull", model]` (mutlak yol `validation.runner.find_on_path("ollama", PATH)` ile bulunur; çalışma dizinine bakılmaz) ve `run_ollama_pull(model, argv, runner=None) -> PullOutcome`. Model adı `^[A-Za-z0-9._:/-]+$` dışındaysa ya da `ollama` PATH'te yoksa `OllamaPullError` (Türkçe mesaj) yükselir ve **hiçbir süreç başlatılmaz**; doğrulama düğme basılırken senkron yapılır, geçerliyse iş `bridge.submit("pull:ollama", ...)` ile arka plana verilir (arayüz kilitlenmez, kart "… indiriliyor…" gösterir). Sonuç (`PullOutcome.ok/message`) kart ayrıntısına ve toast'a düşer. Ollama kartına (kind `local`) **"Modeli indir"** düğmesi eklendi (`CardActions.pull_model`); `App._on_message` `pull:` görevini `CONNECTIONS_TASKS` üzerinden bağlantılar denetleyicisine yönlendirir. Hata beklenen sonuçtur (istisna köprüde anlamsız genel metne dönüşürdü): `ok=False` + Türkçe neden. Testler: `tests/desktop/test_connections.py::test_ollama_pull_argv_is_absolute_and_shell_free`, `::test_ollama_pull_runner_gets_validated_argv`, `::test_ollama_pull_rejects_unsafe_model_names` (9 kötü niyetli ad), `::test_ollama_pull_missing_binary_is_turkish_error`, `::test_ollama_pull_failure_outcome_is_turkish`; `tests/desktop/test_app.py::test_ollama_pull_button_runs_through_background_task`, `::test_ollama_pull_without_binary_warns_and_starts_nothing`. **Gerçek `ollama` çalıştırılmadı, ağa çıkılmadı** (kural 7/8): süreç yalnız enjekte edilen sahte `runner` ile başlar.

- **F11 (SQLite çağrılarını iş parçacığına alma):** Geçmiş ekranının tüm DB işleri `desktop/bridge.py` desenine taşındı: `history_controller` artık üç arka plan görevi kullanır — `history` (liste), `history_delete` (tekil silme), `history_clear` (tümünü temizle); `history_view.refresh()`/`_handle_load_more()` yalnız **istek** yapar (`request_page` geri çağrısı, `App._request_history_page` → `history_controller.refresh`), sonuçlar ana iş parçacığında `history_controller.handle` ile uygulanır (`apply_page`/`apply_error`). Liste yükleme, silme ve temizlik boyunca **"Yükleniyor…"** gösterilir (`HistoryView.show_loading`, `append=True` iken "Daha fazla yükle" düğmesi devre dışı). Toplam token/maliyet etiketi de artık ana iş parçacığında değil, işçinin içinde (`usage_totals_label(usage_totals(db))`) hesaplanır ve sayfayla birlikte gelir; `usage_totals`/`AnalysisRow`/`usage_totals_label` içe aktarımları `app.py`'den kalktı, kullanılmayan `history_rows`/`history_page` sarmalayıcıları silindi. Hata Türkçedir: `history` görevi hatasında liste `apply_error` ile metni gösterir, silme/temizlik hatasında liste tazelenip toast çıkar (liste "Yükleniyor…"da kalmaz). Testler: `tests/desktop/test_app.py::test_history_list_loads_off_main_thread` (DB çağrısı `threading.main_thread()` DEĞİL; bekleme kapısı açıkken "Yükleniyor…" görünür), `::test_history_page_renders_rows_and_totals`, `::test_history_page_error_is_shown_in_turkish`, `::test_history_stale_page_result_is_dropped` (eski kuşağın geç gelen sonucu atılır), `::test_history_delete_runs_off_main_thread`, `::test_history_clear_runs_off_main_thread`; mevcut 12 geçmiş testi `pump_history`/`pump` ile sonucu bekleyecek şekilde güncellendi (davranış aynı, zamanlama asenkron).

- **F12 (Linux/macOS'ta "Oturum aç"):** Oturum açma akışı GUI'siz yeni `desktop/login.py` modülüne çıkarıldı (Tk içe aktarmaz, `spawn` enjekte edilebilir): `login_argv(name, providers)` sağlayıcının komutunu üretir (`claude_cli` → `… auth login`, `codex` → `… login`, `agy` → çıplak yürütülebilir; yollar `resolve_executable` ile PATH'in mutlak dizinlerinden) ve saf `login_command(platform, cli_path, *, login_args, find)` platforma göre pencere argv'sini döndürür: Windows mevcut davranış (yeni konsol, `CREATE_NEW_CONSOLE`), Linux `x-terminal-emulator -e <cli> …` yoksa `gnome-terminal -- <cli> …`, macOS `open -a Terminal <cli>`; hiçbiri bulunamazsa `None`. `open_login_console` süreci yalnız enjekte edilen `spawn` (varsayılan `subprocess.Popen`) ile başlatır; terminal yoksa **hiç süreç başlatılmaz** ve `LoginUnavailableError` yükseltilir, `ConnectionsController.login` bunu toast'a çevirir: "Terminalde şu komutu çalıştırın: <komut>" (`shlex.join` ile boşluklu yollar tırnaklanır; sağlayıcı ön eki kullanıcıya gösterilmez). Konsol ortamı (`login_env`, Faz 50) aynen korundu: API anahtarı değişkenleri miras alınmaz. Testler: `tests/desktop/test_login.py` (üç platform için argv, `gnome-terminal` yedeği, terminal yoksa `None` + hiç `spawn` çağrılmadığı, varsayılan başlatıcının gerçek `subprocess.Popen` olduğu, ortam süzme), `tests/desktop/test_app.py::test_login_starts_console_and_points_to_check`, `::test_login_without_terminal_shows_command_toast`; `tests/unit/test_tkinter_free_imports.py` listesine `codementor.desktop.login` eklendi; `connections.py`'den taşınan 3 test `test_login.py`'ye geçti. **Gerçek terminal/süreç açılmadı** (kural 4/7): `find` ve `spawn` sahtedir.

### Kararlar & Denetim Bulgusu

- **Windows SQLite kilidi:** Bozuk dosyada `SQLModel.metadata.create_all` hata fırlattığında motor açık bağlantı tutuyordu; `Database.__init__` `except` bloğunda `self.engine.dispose()` ve `launch.py`'de `state.close()` + `gc.collect()` ile işletim sistemi dosya kilidi bırakıldı.
- **Şema ayar bağımlılığı:** Denetim sırasında `Database.from_settings`'in henüz tanımlanmamış `session_retention_days` alanına erişimi yakalandı; `StorageSettings`'e alan ve `storage/sessions.py`'ye `prune_old_sessions` eklenerek tam uyum sağlandı.
- **Tcl/Tk Widget Yaşam Döngüsü (F6):** `HistoryView.refresh()` sırasında `clear(self.list)` altındaki tüm widget'ları yok ettiği için `load_more_btn`'nin `_render_rows` içerisinde dinamik olarak yeniden üretilmesi sağlandı; böylece "bad window path name" Tcl hatası önlendi.
- **Kapanış onayı tek noktada (F7):** `App.close` içindeki onay mantığı `runtime.confirm_close(app)` içine çıkarıldı; "kaydedilmemiş değişiklik" (F5) ve "süren iş" (F7) onayları tek akışta sıralandı (önce kirli dosya, sonra meşguliyet) ve `app.py` kabul kriterinin (400 satır) altında tutuldu.
- **Meşguliyet ölçütü (F7):** Süren iş, `app.analyze_view.busy` **veya** `app.connections.download_cancellation is not None` ile yoklanıyor; indirme başlarken `Cancellation` atanıp biterken/iptalde `None`'a çekildiği için "analiz sürüyor" ve "zig indiriliyor" aynı onayla kapsandı. Onay reddedilirse kapatma iptal edilir (pencere açık kalır).
- **Eski anahtar kalıntısı (F8):** ADR-0021 ile sağlayıcı listesinden çıkarılan `openai`/`deepseek` kayıtları kimlik kasasında kalıyordu; temizlik `LEGACY_KEY_PROVIDERS` sabitine dayandığından yalnızca kaldırılan sağlayıcıları siler, güncel kayıtlara dokunmaz ve silinecek kayıt yokken idempotenttir (0 döner). Kasa kilitliyse `KeyStoreError` Türkçe toast'a dönüşür; gizli anahtar hiçbir yerde loglanmaz/gösterilmez.
- **Denetim bulgusu (F8):** `desktop/connections.py` F8 eklemeleriyle 402 satıra çıktı (> 400, AGENTS.md "bölmeyi öner"); `KeyStore`/`LEGACY_KEY_PROVIDERS`'ın ayrı bir `desktop/keystore.py`'ye taşınması önerisi "Sonraya"ya yazıldı (Faz G0'daki bölme disipliniyle aynı yaklaşım). Faz F kabul kriteri yalnız `app.py` < 400 olduğundan bu, kabul engeli değil.
- **Güncelleme ölçütü (F9):** "eski sürüm" yalnız sürüm dizesine bakmaz, işaretçideki **sha256**'yı da karşılaştırır: aynı sürümde adres/sha256 değişse bile güncelleme önerilir (§12: adres ve sha256 yalnız yapılandırmadan gelir, kurcalanmış arşiv yeniden indirilir). Kurulum hiç yoksa `needs_update` `False` döner — eksik kurulumu `offer_compiler_download` yönetir; iki düğme de aynı `install_zig` yolunu kullanır (yeni indirme yolu yok, ADR-0018 korunur).
- **Yarım kurulum ayrımı (F9):** işaretçisiz dizin (kopyalanmış/eski kurulum) kurulu sayılmaz ve güncelleme istemez; bu, `installed_zig` ile aynı ölçütü paylaşır (işaretçi + çalıştırılabilir dosya).
- **`ollama` komutu yalnız argv listesi (F10):** Kabuk hiç kullanılmaz; model adı tek bir argv öğesi olarak geçer ve `^[A-Za-z0-9._:/-]+$` ile **komut başında** doğrulanır (spec'teki karakter sınıfı birebir uygulandı; `.` ve `/` sınıfın parçası olduğu için `../x` gibi adlar reddedilmez, ancak tek argv öğesi olduğundan yol/kabuk anlamı taşımaz). Yol `find_on_path` ile yalnız PATH'in mutlak dizinlerinde aranır — `run_process` zaten mutlak olmayan `argv[0]`'ı reddeder (Faz A2, Y1).
- **Hata beklenen sonuç (F10):** `run_ollama_pull` istisna fırlatmaz; başarısızlık `PullOutcome(ok=False, message=<Türkçe neden>)` olur. Nedeni: köprü, tanımadığı istisnalar için "Beklenmeyen bir hata oluştu" gibi genel metin üretir ve kullanıcı `ollama`nın gerçek çıktısını görmezdi. Başarısız `returncode`'da `stderr`'in son satırı mesaja girer.
- **Doğrulama zamanlaması (F10):** Model adı ve `ollama` varlığı denetimi düğme basılırken senkron yapılır (kullanıcı anında Türkçe uyarı görür, boşuna arka plan görevi açılmaz); süreç başlatma ve bekleme arka planda köprüde koşar (arayüz kilitlenmez). İndirme süresi `ProcessLimits.timeout_s = 3600` (büyük modeller dakikalarca inebilir); çıktı ilerlemesi akış olarak gösterilmez (köprü `run_process` sonucunu tek seferde döner), kart yalnız "indiriliyor…" der.

- **Sonuç teslimi ana iş parçacığında (F11):** İşçi iş parçacığı Tk'ye dokunmaz; yalnız sonucu köprünün `queue.Queue`'suna yazar, `App._poll` (ana iş parçacığında `after` ile zamanlanır) `drain()` edip `history_controller.handle`'e verir. İş parçacığından doğrudan `app.after(0, ...)` çağrılmadı: köprü deseni (Faz 19'dan beri kullanılıyor) aynı işi kuşak denetimi ve iptalle birlikte yapıyor, doğrudan `after` çağrısı Tk'de iş parçacığı güvenli değil.
- **Kuşak denetimi (F11):** Aynı görev adı yeniden gönderilirse köprü kuşağı artırır ve eski iş parçacığının geç gelen sonucu `drain()` sırasında atılır; hızlı iki yükleme (ör. art arda arama) eski listeyi geri getirmez (`test_history_stale_page_result_is_dropped`).
- **Silme/temizlikte de "Yükleniyor…" (F11):** Silme ve temizlik akışları sonunda listeyi tazelediği için yükleme göstergesi görev başında açılır (`show_loading`); kullanıcı işlem sürerken eski satırları görmez. Kayıt yoksa ya da iş hata verirse liste `refresh()` ile toparlanır, "Yükleniyor…" ekranda kalmaz.
- **Kapsam sınırı (F11):** `open_history` (kaydı açma) hâlâ ana iş parçacığında `get_analysis`/`get_row` + `runtime.load_source` yapar; F11 kapsamı spec'te sayılan liste/silme/temizleme ile sınırlı tutuldu, kayıt açma "Sonraya"ya yazıldı.
- **Platform seçimi saf fonksiyonda (F12):** `login_command` platforma göre yalnızca argv üretir (süreç başlatmaz; terminal araması `find` ile enjekte edilir). Böylece Linux/macOS dalları Windows'ta da deterministik test edilir ve testler makinede kurulu terminale bağlı kalmaz. Windows davranışı korundu: eski kod yalnız Windows'ta çalışıyordu, artık aynı yol `CREATE_NEW_CONSOLE` ile devam ediyor; "konsoldan oturum açma yalnızca Windows'ta destekleniyor" hatası tamamen kalktı.
- **macOS'ta argüman geçirme sınırı (F12):** `open -a Terminal <cli>` ek argümanları belge yolu saydığı için macOS dalında yalnız çalıştırılabilir yol geçilir (`auth login` ekleri düşer); `claude`, `codex` ve `agy` argümansız da kendi oturum açma akışını başlattığından kabul edildi, `osascript` ile argümanlı sürüm "Sonraya"ya yazıldı.
- **Terminal yoksa sessiz kalmama (F12):** Konsol açılamadığında hiçbir süreç başlatılmaz ve istisna toast'a dönüşür; kullanıcı tam komutu görür (`login_env` sayesinde anahtarlar gizli kalır). Kart ayrıntısı yerine toast seçildi: metin kart satırından uzun ve kopyalanabilir olmalı.

### Doğrulama
- `uv run ruff check .` → All checks passed!
- `uv run ruff format --check .` → 460 files already formatted
- `uv run mypy src/` → Success: no issues found in 206 source files
- `uv run pytest tests/desktop/test_launch_db.py` → 4 passed in 0.35s
- `uv run pytest tests/unit/test_tkinter_free_imports.py` → 9 passed in 5.11s
- `uv run pytest tests/unit/test_storage.py` → 42 passed in 0.77s
- `uv run pytest tests/desktop/test_app.py` → 59 passed in 56.12s
- Dosya satır sayıları: `app.py` 399, `files.py` 129, `history_controller.py` 155, `config_controller.py` 89, `history_view.py` 273, `cache.py` 272 (< 400).
- F7+F8 sonrası (HEAD `2598026`) tam takım: `uv run pytest -m "not live" -q` → 3409 passed, 15 skipped, 6 deselected in 194s; `uv run ruff check .` ve `uv run ruff format --check .` temiz; `uv run mypy src/` → 206 kaynak dosyada hata yok.
- F7+F8 sonrası dosya satır sayıları: `app.py` 398 (< 400), `runtime.py` 252, `connections_controller.py` 287, `connections_view.py` 280; `connections.py` 402 (bölme önerisi yukarıda).
- F9 sonrası tam takım: `uv run pytest -m "not live" -q` → **3414 passed, 15 skipped, 6 deselected** in 201s; `uv run ruff check .` → "All checks passed!"; `uv run ruff format --check .` → "460 files already formatted"; `uv run mypy src/` → "Success: no issues found in 206 source files".
- F9 mutasyon kontrolü: F9 kaynağı `git stash` ile geri alınınca yeni 5 test düştü — 3 birim testi `ImportError: cannot import name 'needs_update'`, 2 pencere testi FAILED (`AttributeError` ve kutu görünürlüğü); `git stash pop` sonrası `git stash list` boş.
- F9 sonrası dosya satır sayıları: `toolchain_install.py` 380, `services.py` 71, `connections_controller.py` 292, `connections_view.py` 297, `app.py` 398 (< 400).
- F10 sonrası tam takım: `uv run pytest -m "not live" -q` → **3429 passed, 15 skipped, 6 deselected** in 208s (+15 test: 13 `test_connections.py`, 2 `test_app.py`); `uv run ruff check .` → "All checks passed!"; `uv run ruff format --check .` → "460 files already formatted"; `uv run mypy src/` → "Success: no issues found in 206 source files".
- F10 mutasyon kontrolü: (a) dört kaynak dosya (`services.py`, `provider_card.py`, `connections_controller.py`, `app.py`) `git stash` ile geri alınınca derleme aşaması düştü (`ImportError: cannot import name 'PullOutcome'`); (b) yalnız GUI bağlantıları (`provider_card.py`, `connections_controller.py`, `app.py`) geri alınınca 2 pencere testi FAILED (`AttributeError: 'ProviderCard' object has no attribute 'pull_button'`) — `git stash pop` sonrası `git stash list` boş, çalışma ağacında yalnız bu maddenin 9 dosyası değişik.
- F10 sonrası dosya satır sayıları: `services.py` 143, `provider_card.py` 253, `connections_controller.py` 327, `connections_view.py` 297, `app.py` 399 (< 400; `CONNECTIONS_TASKS` sabiti tek satırda tutuldu). `connections.py` 402 (F8'den kalan, bölme önerisi "Sonraya").
- F11 sonrası tam takım: `uv run pytest -m "not live" -q` → **3435 passed, 15 skipped, 6 deselected** in 209s (+6 test: hepsi `tests/desktop/test_app.py`); `uv run ruff check .` → "All checks passed!"; `uv run ruff format --check .` → "460 files already formatted"; `uv run mypy src/` → "Success: no issues found in 206 source files".
- F11 mutasyon kontrolü: `app.py`, `history_controller.py` ve `views/history_view.py` `git stash` ile geri alınınca yeni 6 pencere testi FAILED (`AttributeError: HistoryView object has no attribute loading`); `git stash pop` sonrası `git stash list` boş, çalışma ağacında yalnız bu maddenin 5 dosyası değişik.
- F11 sonrası dosya satır sayıları: `app.py` 395 (< 400), `history_controller.py` 241, `views/history_view.py` 347, `tests/desktop/test_app.py` 1680. `connections.py` 402 (F8'den kalan, bölme önerisi "Sonraya").
- F12 sonrası tam takım: `uv run pytest -m "not live" -q` → **3447 passed, 15 skipped, 6 deselected** in 212s (+12 test: `tests/desktop/test_login.py` 12 yeni; `tests/desktop/test_app.py` 2 yeni; `tests/desktop/test_connections.py` −3 (oturum testleri `test_login.py`'ye taşındı); `tests/unit/test_tkinter_free_imports.py` +1); `uv run ruff check .` → "All checks passed!"; `uv run ruff format --check .` → "462 files already formatted"; `uv run mypy src/` → "Success: no issues found in 207 source files".
- F12 mutasyon kontrolü: kaynak değişiklikleri (`desktop/login.py`, `desktop/connections.py`, `desktop/connections_controller.py`) `git stash` ile geri alınınca — testler yerinde bırakılarak — `tests/desktop/test_login.py` derleme aşamasında düştü (`ModuleNotFoundError: No module named 'codementor.desktop.login'`), `tests/desktop/test_app.py` import hatasıyla ERROR verdi ve `tests/unit/test_tkinter_free_imports.py::test_imports_without_tkinter[codementor.desktop.login]` başarısız oldu; `git stash pop` sonrası `git stash list` boş, çalışma ağacında yalnız bu maddenin 7 dosyası değişik.
- F12 sonrası dosya satır sayıları: `desktop/login.py` 144 (yeni), `desktop/connections.py` 402 → **366** (F8 denetim bulgusu kapandı), `desktop/connections_controller.py` 331, `desktop/app.py` 395 (< 400), `tests/desktop/test_login.py` 190, `tests/desktop/test_app.py` 1716, `tests/desktop/test_connections.py` 465.
- F10 denetimi (2026-10-14): kritik/önemli bulgu yok, birleştirilebilir; 3 küçük bulgu (test kapsamı, `pull` iptali, model adı deseni) `docs/BulgularVeDuzeltilecekler.md` §10 Faz F ve Sonraya bölümüne yazıldı.

### Açık kalanlar
- **Faz F kabulündeki "elle deneme" yapılmadı (kullanıcıda):** `uv run python -m codementor.desktop` ile (a) Geçmiş → Tümünü temizle, (b) dosyayı düzenleyip Ctrl+S, (c) düzenleyip başka dosya açma → onay maddeleri etkileşimli masaüstü oturumu gerektirir; bu ortamda ÇALIŞTIRILMADI (kural 7/8). Gerçek zig indirmesi/`güncelleme` akışı, `ollama pull` ve canlı sağlayıcılar (gemini/agy) da çalıştırılmadı; bozuk DB elle denemesi `CODEMENTOR_DB_PATH` ile geçici bir veritabanında yapılmalı.
- **F12 elle denemesi (kullanıcıda):** Linux/macOS "Oturum aç" davranışı bu makinede (Windows) koşturulamadı; platform dalları yalnız testlerle (enjekte edilen `find`/`spawn`, hiç gerçek terminal yok) doğrulandı. Gerçek `x-terminal-emulator`/`gnome-terminal`/`open` denemesi ve §3.1 Linux taklidi kullanıcıya bırakıldı.
- **`connections.py` 402 satır (F8 denetimi) KAPANDI:** F12'de oturum açma akışı `desktop/login.py`'ye çıkarıldı; dosya **366 satıra** indi (< 400) ve `KeyStore` taşıma önerisi "Sonraya" listesinden kapatıldı. Başka denetim bulgusu (F10'un 3 küçük maddesi) hâlâ açık.
- **`docs/BulgularVeDuzeltilecekler.md` §10:** F1–F12'ye karşılık gelen kutular `- [x] … — **Faz F**` yapıldı (son olarak F12). Açık kalan tek kutu 400 satır bölme işi: `desktop/app.py` 395 satırla sağlanıyor; `pipeline/orchestrator.py` Faz G0'da bölünecek.

## Faz E — Notlar (web geçmişi, silme ve güvenlik başlıkları; 2026-10-13)

### Yapılanlar
- **E1 & E2 (API geçmişi ve silme):** `AnalysisSummary`, `AnalysisPage`, `DeletedCount` modelleri (`models/api.py`).
  `storage/cache.py`'de `list_analyses_page(db, limit, before)` (en yeni önce, cursor tabanlı sayfalama) ve
  `storage/sessions.py`'de `delete_session(db, session_id)` (belirli oturumu silme). `GET /v1/analyses`,
  `DELETE /v1/analyses` (toplu silme), `DELETE /v1/sessions/{session_id}` uç noktaları eklendi.
  Şemalar dışa aktarıldı (`schemas/`) ve TypeScript tipleri üretildi (`web/src/types/`).
- **E3 & E4 (Web geçmişi ve API anahtarı):** `web/src/lib/apiKey.ts` (`sessionStorage` tabanlı `getApiKey`/`setApiKey`/`clearApiKey`),
  `web/src/api/client.ts` (`X-API-Key` ekleme, 401 için Türkçe hata mesajı, `listAnalyses`, `getAnalysis`, `deleteAnalysis`, `deleteAllAnalyses`).
  `web/src/components/HistoryPanel.tsx` (geçmiş listesi, silme, tümünü temizle onaylı, sayfalama).
  `web/src/App.tsx` içine geçmiş paneli ve başlıkta API anahtarı ayarı entegre edildi.
- **E5 (O15 Monaco hover güvenliği):** `web/src/lib/markdown.ts` içinde `escapeMarkdown` eklendi;
  `markers.ts` Monaco hover içerisindeki LLM bulgu açıklamaları ve derleyici iletilerini kaçışlayarak
  güvenilmeyen bağlantı ve görselleri etkisizleştirdi.
- **E6 (O16 Güvenlik başlıkları):** `web/index.html`'e sıkı CSP meta etiketi (`default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; ...`);
  `web/vite.config.ts` dev modunda HMR için `connect-src` genişletmesi; `src/codementor/api/security_headers.py`
  ile API yanıtlarına `X-Content-Type-Options: nosniff` ve `Referrer-Policy: no-referrer` başlıkları eklendi.
- **E7 (D14 İç uçların korunması):** `src/codementor/api/auth.py` içinde `_is_protected` ile `/health/ready`,
  `/docs`, `/redoc`, `/openapi.json`, `/docs/oauth2-redirect` ve `/v1/*` yolları API anahtarı açıkken korundu;
  yalnız `/health` açık bırakıldı.
- **E8 (D15 Markdown dışa aktarımında HTML kaçışı):** `src/codementor/report/markdown.py` içinde `_escape_html`
  fonksiyonu ile kod içi (`...`) ve kod blokları korunarak serbest metindeki `<`, `>`, `&` karakterleri kaçışlandı.
- **E9 (D17 İndirme URL gecikmeli iptal):** `web/src/lib/download.ts` içinde `URL.revokeObjectURL(url)` 1000 ms
  gecikmeyle (`setTimeout`) çağrılacak şekilde güncellendi.
- **E10 (Soru filtresi boş mesajı):** `web/src/components/Controls.tsx` soru listesi boş olduğunda
  "Bu filtrelerle eşleşen soru yok." mesajı gösterir.
- **E11 (Dışa açık serve ve hız sınırı):** `src/codementor/cli/serve.py` dışa açık IP'de anahtarsız ve `--insecure`
  olmaksızın başlatmayı reddeder (kod 3). `ApiSettings.rate_limit_per_minute` (varsayılan 30); `RateLimiter`
  (`api/guard.py`) ve `ApiState` üzerinde kayan pencere ile 429 Too Many Requests + `Retry-After: 60` üretilir.
- **E12 (CSRF / text/plain güven sınırı):** `tests/api/test_trust_boundary.py` içinde `POST /v1/analyze`
  `text/plain` içerik türüyle reddedildiği ve LLM çağrılmadığı doğrulandı.

### Kararlar
- **RateLimiter mimarisi:** Hız sınırlayıcı durum bilgisi `src/codementor/api/guard.py` içinde `RateLimiter` sınıfında
  toplandı ve `ApiState` üzerinden uygulama durumuna bağlandı; böylece test ortamlarında her ASGI uygulaması
  tamamen yalıtılmış hız sayacına sahip oldu.
- **API Anahtarı saklama:** Web tarafında API anahtarı `localStorage` yerine `sessionStorage`'da tutuldu; sekme
  kapanınca anahtar temizlenerek paylaşılan bilgisayarlarda güvenlik sağlandı.

### Doğrulama
- `uv run ruff check .` → All checks passed!
- `uv run ruff format --check .` → 456 files already formatted
- `uv run mypy src/` → Success: no issues found in 204 source files
- `uv run pytest -m "not live"` → 3383 passed, 15 skipped, 6 deselected in 178s
- `npm run typecheck` → 0 errors
- `npm test` → 12 passed (54 tests)
- `npm run build` → built in 404ms
- `npx playwright test e2e/app.spec.ts` → 4 passed (5.0s, CSP console hatası 0)
- Linux tkinter-free yalıtım testi → 7 passed
- Görünmez karakter taraması → 0 bulgu

## Denetim — Faz A1-D (kod-denetci, 2026-10-13)
İki kod-denetci ajanı (A1+A2+B ve K+C) "birleştirilemez" dedi; bulgular doğrulanmıştı. Dal
`fix/denetim-a-d` (`faz/d-public-release`dan).
**Düzeltilenler:**
- Include: satır birleştirmeyle kurulan `##`/`%:%:` (ham kodda görünmüyordu) reddediliyor;
  `_Pragma("GCC dependency …")` ile host dosyası yoklama kapandı.
- `guard_delimiters`: iyelik nicelikleri ve öznitelikli/özniteliksiz dal ayrımıyla doğrusal (39 bin
  boşlukta 3,5 sn → 0,02 sn); `&` içeren öznitelik değeri (A2 gerilemesi) ve `&#60;`, `&#x3c;`,
  noktalı virgülsüz `&lt` nötrleniyor.
- Önbellek imzası `asyncio.to_thread`'de (derleyici keşfi olay döngüsünü kilitliyordu); imza kontrol
  listesi damgalarını, sağlayıcı ayarlarını ve referans çözüm damgasını da kapsıyor.
- Önbelleğe girmeyenler: sızıntı yüzünden tüm soruları atılan rapor, Tier 0 durdurma raporu, Tier 1
  zaman aşımı/araç hatası. Onarım prompt'u bütçe hatası verse ya da onarım sürerken süre dolsa da
  geçerli bulgular korunuyor.
- Kullanıcı sorusu: başlık, metin, kısıt, işlem adı ve ipucu prompt'ta `guard`'dan geçiyor; kullanıcı
  görevi "talimat değil" diye işaretleniyor (`QuestionContext.origin`); taslakta uzunluk sınırları.
  Kullanıcı deposu yalnız `.yaml` okuyor, yinelenen kimlik atlanıyor; yerleşik banka kullanıcı
  kaynaklı hiçbir hatayla düşmüyor; masaüstünde atlanan dosya sayısı görünüyor; düzenleme formu
  formla uyumsuz dosyada çökmüyor.
- Kavram: gizli seviyede kavram adının sorularda/ipucunda geçmesi `concept_named` ihlali (Türkçe
  büyük/küçük ve aksan duyarsız); bayraksız eski önbellek kayıtlarında kavram model düzeyinde boş.
- Yapılandırma (ADR-0029, kullanıcı kararı): çalışma dizinindeki toml güvenilmez katman (tehlikeli
  anahtarlar yok sayılır, uyarı); katmanlar env → cwd → `~/.codementor/codementor.toml` → paket;
  kurulu wheel'de CLI masaüstünün yazdığı dosyayı okuyor.
- `usage_totals` bozuk `report_json`'a dayanıklı (`json_valid`); Geçmiş'te hata log'a yazılıyor.
- Testler: `integration/test_audit_fixes.py` (10; düzeltmeler geri alınınca hepsi düşüyor),
  `unit/test_audit_fixes_unit.py` (10), include (+3), guard (+13). mimari §11, §17 güncellendi.
**Doğrulama:** ruff, format, mypy temiz; `pytest -m "not live"` 3355 geçti, 15 atlandı.
**Ertelenen (Sonraya):** ~~`config_writer` dizi tablosunu (`[[providers.x]]`) ezer, CRLF'yi LF yazar~~ (G6: çözüldü);
~~`from_question` `genel` etiketini/varsayılan kısıtı düzenlemede siler~~ (G6 parça 3: çözüldü);
~~`system_errors` ağ hatalarını "dosya işlemi" diye anar~~ (G6-4: çözüldü); ~~`report/usage` →
`storage.cache.UsageTotals` katman bağımlılığı~~ (G6-4: çözüldü);
`detect.py` `<meta …` deseni çok büyük girdide karesele yakın (40 KB'de ölçülmedi);
`guard_delimiters` `&lt;` için idempotent değil; ~~`primary` sağlayıcı adı `getattr` ile~~ (G6-5: çözüldü);
~~400 satır: `orchestrator.py` (421 → 379; kapanış oturumu), `passes.py` (366), `desktop/app.py` (395)~~
— üçü de < 400; kalan tek sınır aşımı `providers/cli_agent.py` 420 (kapanış denetimi, Sonraya).

## Faz D — Notlar (public belgeler ve otomatik release; 2026-10-13)
Kaynak: `docs/BulgularVeDuzeltilecekler.md` P5-P9, P11, O1, O17, O18, D20.
**Yapılanlar:**
- İç belgeler (`DEVIR_*`, `CODEX_3_4_YAPILANLAR`, `YAPILANLAR*`, `FAZ36_OLCUM_DURUMU`,
  `EVAL_PARCA_REHBERI`) `docs/gelistirme-gunlugu/`'ye taşındı (+ dizin README'si, bağlantılar).
  PROGRESS 263 KB → 31 KB: Faz 0-63 notları `PROGRESS-faz-0-63.md` arşivinde.
- GUNCELLEMELER Faz 62: yapılmayan web/toplu silme açık işaretlendi (→ Faz E).
- README: sayılar (28 ADR, 3.300+ test, ~29/28 bin satır), faz anlatımı, dil bağlantısı, release
  indirme metni; `README.en.md`, `SECURITY.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, issue/PR
  şablonları.
- Sürüm tek kaynak `codementor.__version__` = **0.1.1** (hatch dinamik sürüm; `build_exe`
  oradan okur); `pyproject` authors/keywords/classifiers/urls.
- `desktop/self_check.py` + `CodeMentor.exe --self-check <json>`: pencere açmadan kaynaklar,
  soru bankası (64), `.scm` sorguları, olgu çıkarımı, Roslyn.
- CI: `permissions: contents: read`, `concurrency`, action'lar commit SHA'sına sabit. Yeni
  `release.yml` (etiket = sürüm denetimi → test → Roslyn sc → exe → iki paketle duman testi →
  `SHA256SUMS` → CHANGELOG bölümüyle `gh release create`; yazma izni yalnız yayın işinde),
  `dependabot.yml` (uv, npm, actions). actionlint temiz.
- Yerel: `dist/` eski exe/zip ve exe yanındaki eski `codementor.toml` (scratchpad'e yedeklendi)
  silindi; 0.1.1 onefile + onedir derlendi, ikisi de `--self-check` ile geçti (Faz 60'ın açık
  maddesi: güncel exe'de 64 görev).
- Testler: `test_release_readiness.py` (sürüm eşitliği, CHANGELOG, duman testi, eksik sorgu,
  isteğe bağlı denetim, `--self-check` bayrağı).
**Kararlar:** `analyze` çıkış kodu 2 = derleme başarısız (mimari §10); yanlış yazdığım
açıklamalar düzeltildi. agy canlı denemesi yapılmadı.
**Kullanıcıda:** main birleştirme + push + `v0.1.1` etiketi (release otomatik); GitHub'da secret
scanning, push protection, Dependabot alerts (P13).

## Faz A1 — Notlar (include koruması yorum atlatması, dil tespiti ReDoS; 2026-10-12)
Kaynak: `docs/BulgularVeDuzeltilecekler.md` K1, K2 (tam tarama). Kod-denetçi denetimi token
nedeniyle sonraya bırakıldı.
**Yapılanlar:**
- `validation/include_guard.py`: maskelenmiş birleşik metinde `#`/`%:` + boşluk(yorum) + yönerge
  adı aranır; arada ham metinde `/*` varsa hedeften bağımsız red (`#/**/include`, `%:/**/include`,
  satır aşan `#/*` + yeni satır + `*/include`). Yorumsuz `#` + yeni satır + `include` yönerge
  değil, dokunulmadı.
- `ingest/detect.py`: CSS özellik deseni (kübik) ve `re.M` + `^\s*` desenleri (karesel; Java dahil)
  `^[ \t]*`, satır içi `[^…\n]` ve `[^)]{0,300}` ile doğrusal. 13 desende `\b` yerine U+0008 vardı
  (Faz 16); düzeltildi, Python/HTML/CSS sinyallerinin bir kısmı ilk kez çalışıyor.
- `pipeline/orchestrator.py`: `_ingest` async; `normalize` `asyncio.to_thread` ile.
- Testler: 6 yeni red + 2 izin (include), 10 kötü niyetli girdi × tüm tespit desenleri < 0,25 sn,
  40 KB ReDoS girdisi < 1 sn, ölü sinyallerin eşleşmesi ve kaynakta U+0008 yokluğu,
  `test_offloop` ingest'i kapsıyor.
**Doğrulama:** ruff, format, mypy temiz; `pytest -m "not live"` 3148 geçti, 14 atlandı.
**Açık:** `_recursion.py`/`verify/lines.py`/`verify/proof.py` ve `rules/` regex taraması; kod-denetçi
denetimi; Y1, D13, `.gitignore` (Faz A2).



## Faz C — Notlar (ipucu merdiveni, yapılandırma, CLI çıkış kodları; 2026-10-13)
Kaynak: `docs/BulgularVeDuzeltilecekler.md` Y6, Y7, Y8, Y9, O7, O8, O9, O11, O12, D20.
**Yapılanlar:**
- **Y6:** `SocraticResult.concept_revealed` (varsayılan False). Kural kaynağında:
  `verify_socratic(name_concept=…)` (`MentoringProfile.name_concept`, `run_pass_b` →
  `VerifyArgs.socratic`) açılmayacaksa `key_flaw_concept=""`; API/JSON/indirme dahil hiçbir yere
  gitmez. Açılacaksa kavram `check_leaks` hedefi (`LeakField` += `key_flaw_concept`): önce yeniden
  üretim, sonra kavram gizlenir, sorular kalır. Şablonlar (genel ad) True. Masaüstü kartı, CLI,
  Markdown bayrağa bakar (`hint_level >= 3` kalktı).
- **O7:** `_RelativeTomlSource._read_file` BOM'u atar; `config_writer` BOM'lu okur, BOM'suz yazar.
- **Y7:** `config_writer` satır içi tabloyu ve nokta anahtarlı `providers.x`'i yerinde günceller
  (başlıklı tablo yalnız başlıklı tablonun altına; aksi tomlkit sonraki satırları yanlış tabloya
  kaydırıyordu), yazım atomik.
- **Y8/O9:** `config.config_file()` (env → çalışma dizini → paketteki varsayılan);
  `pyproject` wheel'e `codementor.toml`'u ekler. `runtime.writable_config_file()`: env → exe yanı /
  kurulu wheel'de `~/.codementor/codementor.toml` (paketteki kopyalanır) → depodaki etkin dosya;
  seçilen yol `CODEMENTOR_CONFIG_FILE`'a yazılır (yeniden yükleme ve Bağlantılar'daki konum aynı
  dosya). `prepare_environment` kurulu wheel'de kullanıcı toml'unu etkinleştirir.
- **O8 (karar):** `.env` yüklenmez (öğrenci projesindeki `.env` sağlayıcı komutunu
  değiştirebilirdi, §12); `.env.example` başlığı + güncel liste, README.
- **Y9/O12:** `cli/errors.py` `system_errors`: OSError, SQLAlchemyError, ValidationError,
  TOMLDecodeError, DataFileError → `Hata: …` + 3 (`typer.Exit`'e dokunmaz). `analyze` (DB, `--out`
  `with` ile), `toolchain status/install`, `eval compare/analyze`.
- **O11:** `cli.main.run()` giriş noktası (`[project.scripts]`), kök `--help` UTF-8.
- **D20:** `rules list` "Durum" sütunu (kapalı/açık; ayar okunamazsa "—").
- Testler: `test_pipeline_concept.py`, `test_analysis.py` (+4 kavram), `test_config_cli_faz_c.py`
  (17), `desktop/test_faz_c_app.py` (3). Yazıcı/CLI değişiklikleri geri alınınca 9 test düşüyor.
  `tests/conftest.py` `_restore_config_env`: `writable_config_file` env'e yazdığı için testler arası
  sızıntıyı keser (önce sıra bağımlı 30 düşüş görüldü).
**Doğrulama:** ruff, format, mypy temiz; `pytest -m "not live"` 3313 geçti, 15 atlandı; web 36 test + `tsc`;
wheel geçici venv'e kuruldu: toml'suz dizinde varsayılan `claude_cli`, 6 zig kaynağı, kök `--help`
UTF-8; masaüstünde seviye 1 kartında kavram gizli, 2. denemede açık (ekran görüntüsü).
**Açık:** `toolchain install` indirme hatası hâlâ 1 dönüyor (sistem hatası sayılabilir; Faz G).
Önbellekteki eski raporlar bayraksız: kavram gösterilmez (güvenli taraf).

## Faz K — Notlar (kullanıcı soruları + token kullanımı; 2026-10-13)
Kaynak: kullanıcı isteği (Faz C'den önce). Kararlar (kullanıcı): soru ekleme masaüstü formu + CLI;
basit form (başlık, açıklama, dil, zorluk zorunlu); token her zaman görünür, aşama dağılımı,
toplam/geçmiş.
**Yapılanlar:**
- **Kullanıcı soruları (ADR-0028):** `QuestionPublic.origin` (`builtin|user`; hedef karmaşıklık
  yalnız yerleşikte zorunlu, kullanıcı kimliği `kullanici-` önekli), `UserQuestionDraft`
  (boşlar genel kısıt/etiket/ipucuyla dolar, `O(...)` sarmalayıcısı atılır, zaman+bellek
  birlikte). `questions/user_store.py`: slug kimlik (Türkçe katlama, çakışmada `-2`), atomik YAML
  yazımı, düzenlemede sürüm artışı, yerleşik soru silinemez, bozuk dosya atlanır + uyarı.
  `QuestionBank.load_all` (API, orkestratör, CLI, demo); `ApiState.reload_questions`.
  `config.data.user_questions_dir` (varsayılan `~/.codementor/questions`, yazılabilir yol).
- Masaüstü: Sorular ekranında "+ Soru ekle", "Kendi sorularım" filtresi, kartta "Kendi sorum"
  rozeti + Düzenle/Sil (onaylı); `views/question_form.py` (dile göre motor, HTML/CSS'te hedef
  alanları kapalı, hata formda Türkçe); mantık `questions_controller.py`'de.
- CLI: `questions add <yaml>`, `questions remove <id>`, `list`'te `(kendi)`; `validate` yalnız
  yerleşik banka.
- **Token:** `ReportMeta.stage_tokens` (`TokenSplit`; `llm_a` onarımlar dahil, `llm_v`, `llm_b`;
  toplamı `tokens_in/out`), `usage_label` hiç gizlenmez (`token 0 (önbellekten | model
  çağrılmadı | derleme hatası… | model yanıt vermedi)`), biçim `1.540 token (giriş 1.200 · çıkış
  340) · tahmini · ~$x`; `usage_breakdown_label`; `storage.cache.usage_totals` (SQL toplam,
  maliyet `json_extract`) → Geçmiş başlığında "Toplam: N analiz · X token · ~$Y". CLI altbilgisi,
  masaüstü rapor başlığı ve web paneli aynı metin; `schemas/` + `web/src/types` yeniden üretildi.
- Testler: `test_user_questions.py` (35), `test_pipeline_usage.py` (6),
  `test_user_questions_app.py` (11), `test_usage_label.py` yeniden yazıldı, web `usage.test.ts`.
**Ekranda doğrulama:** masaüstü gerçek `App` ile açılıp gezildi (geçici dizin). Bulunan iki sorun
düzeltildi: uzun token etiketi rapor başlığıyla çakışıyordu (ayrı satıra alındı); dağılım onarımı
"Analiz"e yazıyordu, oysa `repair_attempts` tüm aşamaların toplamı (sona `N onarım`).
**Kararlar:** web/API'de yazma yok (güvenlik incelemesi ayrı iş). Etiket biçimi bilinçli değişti;
eski etiket testleri yeni metne güncellendi.
**Doğrulama:** ruff, format, mypy temiz; `pytest -m "not live"` 3287 geçti, 15 atlandı; web 36 test,
`tsc` temiz.
**Açık:** `desktop/app.py` 504 satır (Faz G bölme). Web'de prettier uyarısı 22 dosyada (önceden
vardı, CI'da yok).

## Faz B — Notlar (kısmi LLM hatasında bulgu kaybı, önbellek doğruluğu; 2026-10-13)
Kaynak: `docs/BulgularVeDuzeltilecekler.md` Y3, Y4, Y5, O2, O3, O4. Dal `faz/a2-guvenlik`ten.
**Yapılanlar:**
- `pipeline/passes.py`: `LLMSession.providers/incomplete/checkpoint` ve `fail_part`.
  `run_pass_a` şemaya uyan son yanıtı saklar; onarım tükenir ya da onarım çağrısı sağlayıcı hatası
  verirse bulgular korunur, karmaşıklık boş + `COMPLEXITY_UNVERIFIED` (Y3). Geçiş B ayrı `try`:
  sağlayıcı/bütçe/yapılandırma hatası Geçiş A'yı silmez, sorular şablondan (Y4). Karmaşıklık
  Geçiş B prompt'una yalnız doğrulandıysa girer. Tek geçişte K5 bulgu attıysa ya da karmaşıklık
  kurtarıldıysa ayrı Geçiş B (O2).
- `pipeline/orchestrator.py`: süre sınırında Geçiş A bittiyse `checkpoint` kullanılır (doğrulama
  geçişi yarıda kaldıysa `VERIFY_FAILED`); `run.cacheable` = yarım değil ∧ yalnız birincil
  sağlayıcı yanıt verdi (Y5); Tier 1 ayarı analiz başına bir kez (`_run_validation`).
- `pipeline/signature.py` (yeni): `pipeline` imzası mod/doğrulama öneki + kural, prompt, doğrulayıcı,
  onarım ayarları, Tier 1 etkinliği + seçilecek aracın kimliği ve dosya boyutu/zamanı, soru modeli
  özeti (O3). `storage/cache.save_analysis(cacheable=)`: değilse boş anahtar (`NOT_CACHEABLE`).
- `pipeline/assemble.from_cache`: `cost_est=None`, `usage_estimated=False` (O4).
- Testler: `test_pipeline_partial.py` (18), `test_pipeline_cache_key.py` (12),
  `test_pipeline_signature.py` (6). Önbellek denetimi kapatılınca 8, eski imzayla 9 test düşüyor.
**Kararlar:** DB şeması değişmedi (yarım rapor boş anahtarla geçmişte durur). Derleyici sürümü süreç
açmadan dosya boyutu + değişiklik zamanıyla temsil edilir. Fallback testleri iki koşuda da aynı
zincir yapısını kullanır (anahtar sağlayıcı/model etiketine bağlı; aksi hâlde test boşuna geçer).
**Doğrulama:** ruff, format, mypy temiz; `pytest -m "not live"` 3224 geçti, 15 atlandı; statik dev
eval A2 ile birebir aynı (zamanlamalar hariç).
**Açık:** `orchestrator.py` 457, `passes.py` 406 satır (400 sınırı; bölme Faz G'de). Önbellek
anahtarında referans çözüm dosyası ve `data/checklists` içeriği yok. A1+A2+B kod-denetçi denetimi.

## Faz A2 — Notlar (araç keşfi çalışma dizini, sınırlayıcı benzerleri, .gitignore; 2026-10-13)
Kaynak: `docs/BulgularVeDuzeltilecekler.md` Y1, D13, P3. Dal `faz/a1-guvenlik`ten açıldı.
**Yapılanlar:**
- `validation/runner.py` `find_on_path(name, search_path)`: yalnız mutlak `PATH` dizinleri, Windows'ta
  `PATHEXT`, POSIX'te çalıştırma izni; çalışma dizini ve göreli girdiler hiç denenmez.
  `toolchain._which` (`shutil.which` yerine) ve `providers/_cli_common` (`_candidates` → `_locate`)
  aynı yardımcıyı kullanıyor.
- `prompts/templates.py`: `˂` U+02C2, `❮` U+276E, `❰` U+2770, `«` U+00AB `<` sayılır; `&lt;`/`&LT;`
  biçimli sınırlayıcı ve rol etiketleri `&amp;lt;` yapılır. `﹤` U+FE64 NFKC ile zaten kapsanıyordu.
- `.gitignore`: `linkedin metini.md`.
- Testler: çalışma dizinine bırakılan sahte `gcc/g++/clang/clang++/zig/dotnet` (`.exe/.bat/.cmd`)
  seçilmez (eski kodla düşüyordu), göreli `PATH` girdileri yok sayılır, mutlak dizin bulunur,
  `find_on_path` PATHEXT/dizin/çalıştırma izni; 5 benzer × 4 etiket, 6 varlık biçimi, 5 olağan metin.
**Doğrulama:** ruff, format, mypy temiz; `pytest -m "not live"` 3188 geçti, 15 atlandı.
**Açık:** Y2 (kullanıcı, `private/`), K2 kalan regex taraması, A1+A2 kod-denetçi denetimi.

## Sonraya (kapsam dışı fikirler)
> 📋 Ajan ile yapılabilecek işlerin öncelikli listesi ve durumu: [KALAN_ISLER.md](KALAN_ISLER.md).
> Bu bölüm fikirlerin kaynağıdır; iş sırası ve kabul kriterleri KALAN_ISLER.md'de tutulur.
- **Tam tarama kalan bulguları (kod-denetci, 2026-10-20; #1, #3, #4 ve KALAN_ISLER 14-17 kapandı;
  iş sırası `KALAN_ISLER.md` 14-23):**
  - ~~Yüksek: `validation/tier0_pool.py` sıcak işçileri düz `Popen` (bellek/ortam/cwd sınırı yok,
    işçi sayısı sınırsız, tutamak/zombi sızıntısı, `close_tier0_pool` çağrılmıyor, mesajlar şablonla
    eşleşmiyor)~~ → **KAPANDI (iş 14, ADR-0032).**
  - ~~Orta: güvenilmeyen toml `storage.max_analyses` / `session_retention_days` / `data.checklists_dir`
    serbest~~ → **KAPANDI (#3, 2026-10-20).**
  - ~~Orta: `verify/complexity_policy.py` `O(n^2)` (≠ `parse_bigo` gösterimi), `is_optimal`
    yeniden hesaplanmıyor~~ → **KAPANDI (#4, 2026-10-20)**; `agreement="agrees"` bilinçli korundu.
  - ~~Orta (iş 15): `verify/socratic_gate.py` `_LINE_REF_RE` "lineer"i satır referansı sayıyor; tekrar
    algılayıcı sayı dizilerini dejenerasyon sanıyor; kapı uyarıları kayboluyor~~ → **KAPANDI (iş 15).**
  - ~~Orta (iş 16): `web/src/types/question_public.ts` bayat (`sample_io` yok)~~ → **KAPANDI (iş 16).**
  - ~~Orta (iş 17): `tests/network_guard.py` Windows Proactor `ConnectEx` yolunu yakalamıyor~~ → **KAPANDI (iş 17).**
  - Orta (iş 18): `python_check.py` `warnings.catch_warnings` iş parçacığı güvenli değil.
  - Orta (iş 19): `eval/judge.py` + `judge.j2` girdileri `guard`'sız, hata yönetimi zayıf.
  - Orta (iş 20): Codex iptalinde `TemporaryDirectory` temizlik hatası iptali maskeleyebilir.
  - Düşük (iş 21): `RateLimiter._records` sınırsız, `mimari.md:1126` hız sınırı çelişkisi,
    `sessions.updated_at` NULL budanmıyor, `toolchain_prune.py:40` `PruneReport` models/ dışında.
    (README/ZAYIF satır sayıları ölçüme göre güncel; büyüdükçe yine kırılır → iş 23.)
- ~~**Zamanlama testleri kırılgan (iş 3 derin doğrulamasından çıktı, 2026-10-18)**~~ → **KAPANDI (iş 4b,
  2026-10-18):** eşik değişmedi (1,5 sn, ADR-0024); ölçüm ısınma + 3 koşunun en hızlısına çevrildi ve
  yanına **göreli büyüme** testleri eklendi (2× girdi ≤ 3× süre). Kasıtlı karesel yavaşlatma O1'i
  0,34 → 1,07 sn (kırmızı), Tier 0'da CSS/C'yi 3,6-3,8× (kırmızı) yaptı; testler 3 tam suite koşusunda
  kırmızı olmadı.
- ~~**`docs/ZAYIF_VE_GELISTIRILECEK_YONLER.md` (s.399) satır sayıları bayat**~~ → **KAPANDI (iş 4c,
  2026-10-18):** belge ölçümle tazelendi ("~27 bin / ~38 bin satır", "3.700+ test", "30 ADR",
  400 satırı aşan dosya **0**, açık "Sonraya" maddesi **46 / 120**) ve `test_release_readiness.py`'de
  dört testle ölçüme bağlandı.
- ~~**`tests/golden/test_facts_golden.py:50` aynı satır sonu kusuru (Faz J denetimi Küçük-1, 2026-10-17)**~~
  → **KAPANDI (J5)**: `write_snapshot` `newline="\n"` ile yazıyor; `--update-golden` sonrası 15 golden
  **CR=0** ve `git status` temiz; iddia `read_bytes()` üzerinden (`test_write_snapshot_writes_lf_bytes`).
  Eski kodla kanıt: 15/15 dosyada CR>0 ve ağaç kirli.
- ~~**facts golden negatif yolu (Faz J denetimi Küçük-4'ün eşi, 2026-10-17)**~~ → **KAPANDI (J5)**:
  `test_facts_golden_negative_paths` (eksik → `--update-golden` işaret edilir; yazılan dosya LF; içerik
  kayması düşürür ve mesaj dosyayı adıyla söyler) + `test_every_case_has_snapshot` + eyleme dönük mesaj.
- ~~**`tests/unit/test_tier1.py` 633 satır (Faz J denetimi Küçük-5, 2026-10-17)**~~ → **KAPANDI (J5)**:
  633 → 349 satır; düzenek `tests/unit/tier1_helpers.py` (80), sonuç/güvenlik vakaları
  `tests/unit/test_tier1_verdict.py` (292). Toplama kimlikleri 58 → 58 birebir; 38 vaka / 127 assert
  AST ile doğrulandı.
- ~~**`docs/mimari.md` §20 ADR tablosu boşlukları (denetim notu, 2026-10-16)**~~ → **KAPANDI (G9,
  `c2968e2`)**: ADR-0024, 0025, 0028 ve 0029 satırları eklendi; tabloda 30/30 ADR dosyası var.
- ~~**`providers/cli_agent.py` 420 satır (kapanış denetimi, 2026-10-16)**~~ → **KAPANDI (G8,
  `0472603`, kullanıcı talimatı)**: `cli_agent.py` **345 satır**; sonuç ayrıştırma + kimlik hatası
  `providers/cli_result.py`'de (104 satır), adlar yeniden dışa aktarılır (`tests/` değişmedi).
- **Public öncesi zorunlu (kullanıcı, 2026-10-13):** Y2 — `tests/fixtures/llm_responses/unity03_reference.cs`
  bankadaki unity-03 referans çözümüyle (`private/`) karşılaştırılacak; aynı/benzerse yapay bir
  çözümle değiştirilip golden'lar yeniden üretilecek. GitHub'da secret scanning, push protection,
  Dependabot alerts açılacak (P13).
- ~~CPP-OWN-001 akış duyarlı eşleşme: erken `return`/istisna yolunda atlanan `delete` öneri yerine hata sayılsın (Faz 52 denetimi).~~ → **KAPANDI (Faz H2; kaydı 2026-10-18'de tazelendi — KALAN_ISLER iş 5 dilim 1):** davranış H2'de geldi ama o gün yalnız 4 fixture'la sınanıyordu. Doğrulama genişletmesi: `fixtures/CPP-OWN-001/positive/` altına 6 fixture (`goto_skip`, `loop_break_skip`, `loop_continue_skip`, `nested_block_return` → hata; `loop_pair`, `jump_outside_pair` → öneri) + `tests/rules/test_finding_kinds.py`'de 3 birim test (çift aralığı sınırları, aynı dosyada iki tür). Mutasyon: erken çıkış taraması devre dışı → 7 kırmızı, aşırı duyarlı (aralık yerine kapsam) → 8 kırmızı; ikisi de geri alınınca yeşil, `src/` değişmedi.
- ~~Faz 51 denetimi: `RunConfig` etiket/veri seti sürümü taşımıyor; eski koşular yeni etiketlerle sessizce yeniden puanlanabiliyor (etiket özeti `RunConfig`'e + `compare` dipnotu). Ters yön: bellek erişimi olmayan `memory_safety` etiketleri (CPP-OWN-001 çıplak `new[]`: dev `cpp-009`, `cpp-105`, test `cpp-006`) yeni tanıma uymuyor → Faz 52 (kural bazında öneri türü) ile birlikte ele alınmalı. Etiketlerde serbest metin sezgisi yerine yapısal `boundary:` alanı.~~ → **KAPANDI (İş 7, 2026-10-20):** `RunConfig.dataset_version` eklendi (`d1+<hash>`); `compare_table` dipnotu ve uyuşmazlık uyarısı eklendi; `ExpectedFinding.boundary` alanı yapısal hâle getirildi; `cpp-009`'a `boundary: ownership_scope` işlendi.
- ~~Faz 49: `sessions` tablosu da sınırsız büyüyor (oturum başına bir satır); eski oturumları `updated_at`'e göre budamak.~~ → **KAPANDI (Faz F):** `prune_old_sessions` eklendi. ~~Tier 1 derleyici sürümü önbellek imzasında yok.~~ (Faz B: araç kimliği + dosya boyutu/zamanı)
- ~~Faz 49 denetimi O3~~ → **KAPANDI (Faz B + Faz J4, 2026-10-17)**: soru içeriği özeti ve
  referans çözüm damgası Faz B'de imzaya girdi; `data/checklists` **içeriği** ile raporu
  belirleyen `pipeline/`+`prompts/` kodu da Faz J4'te `rules_version`'a alındı (`r2+` → `r3+`).
  `concept_tags` soru modeli özetinin içinde olduğu için ayrıca gerekmiyor. Etiket/veri seti
  sürümü ayrı madde (Faz 51 denetimi) olarak duruyor.
- ~~Faz 49 denetimi Ü9: eksik sütunlu eski şema (`OperationalError`) ve bozuk `created_at` için şema göçü yok; `list_analyses` korunmuyor.~~ → **KAPANDI (İş 8, 2026-10-20):** `Database._migrate`'e `SCHEMA_DB_VERSION = 2` ile eksik sütun denetimi ve `ALTER TABLE` göçü eklendi; `cache._list_analyses_fallback` bozuk `created_at` durumunda `list_analyses`/`list_analyses_page`'in çökmesini engeller.
- ~~Faz 48 denetimi~~ (**Faz B'de kapandı**): süre Geçiş B (Sokratik) sırasında dolarsa doğrulanmış Geçiş A sonucu da atılıyor; bulguları koruyup yalnız Sokratik kısmı şablona düşürmek `run_pass_b is None` yoluyla tutarlı olur (`run_llm_passes` kısmi sonuç döndürmeli).
- Faz 36: kural bazında öneri türü (doğru eşleşmiş `new`/`delete` için CPP-OWN-001, `Reserve` yok UE-MEM-001, `with` dışı `open` PY-RES-001). ~~Claude Opus canlı dev ölçümü~~ → yapıldı (2026-10-05).
- Eval: `select_part` etiket değişikliğine duyarlı; parça atamasını kimlik özetiyle sabitlemek ya da sonuç dosyasına parça kimliklerini yazıp birleştirmede eksik/çakışanı uyarmak.
- Faz 37: kullanıcının keyring'inde kalmış eski OpenAI/DeepSeek anahtarlarını temizleme seçeneği.
- ~~Faz 34: dev setini büyütmek~~ → yapıldı (2026-10-04, dev 96). Kalan: few-shot'ların zayıf modelde etkisi.
- Faz 35: few-shot örneklerine `certainty` alanı eklemek (şu an yalnız kural metninde). ~~Doğrulama kararlarını eval sonucuna yazıp düşürülenlerin TP/FP dağılımını ölçmek~~ → Faz 39.
- Faz 30: web soru seçicisinde filtre sonucu boşsa 'eşleşen soru yok' mesajı (şu an yalnız 'Serbest mod' seçeneği kalıyor).
- ~~Faz 30: `validate` ile `load_reference` aynı çözüm yolu doğrulayıcısını paylaşsın (validate şu an yalnız `is_file()`); dağıtımda `private/` olmadığı için `reference_solution_unreadable` uyarısı her soru bağlamlı analizde loglanıyor, düzeyi `debug` olabilir.~~ → Faz 31.
- Faz 30: yöntem işaretlerini (`METHOD_LEAKS`) soru verisine taşıyıp `validate`'e eklemek; eski soruların kontrol listesi seçimini kilitleyen bir anlık görüntü testi.
- Faz 30: Unreal stub'ına sık türler (`Super` için sınıf içi typedef deseni, `FMath`, `EEndPlayReason`, `FHitResult`, `UPrimitiveComponent`, `USphereComponent`, dinamik delege makroları, `GetWorldTimerManager`); şu an referans çözümler bile yalnız tavsiye uyarılarıyla geçiyor.
- Faz 30: soru bankası için öğretmen/kullanıcı içerik incelemesi ve sorulara örnek giriş/çıkış alanı.
- Faz 29: kurulu zig sürümünü `codementor.toml` ile karşılaştırıp masaüstünde "güncelle" önermek (işaret dosyasında sürüm/sha var, okunmuyor).
- Faz 29: indirilen zig'den yerel hedef dışındaki libc başlıklarını budamak (382 MB → tahminen <150 MB).
- Faz 29: tek dosya exe gömülü RoslynCheck.exe'yi %TEMP%'e açıyor; AppLocker/antivirüs engellerse `/health/ready`'de araç hatası. Gerekirse onedir dağıtımı ya da kullanıcı dizinine kopyalama.
- Faz 26: API hız sınırı (istemci başına, süreçler arası doğru); web arayüzünün API anahtarı göndermesi.
- Faz 26: SQLite çağrılarını da iş parçacığına almak (bağlantı başına iş parçacığı ya da havuz).
- Faz 25: OpenAI katı mod kısıtlarını canlı anahtarla doğrulayıp `SchemaAdapter.openai_strict`'te desteklenenleri korumak.
- ~~Faz 25: masaüstü ve web raporunda tahmini token/maliyet gösterimi (şu an yalnız CLI alt satırı ve JSON).~~ → Faz 33.
- Faz 25: agy canlı doğrulaması (oturum var; `allow_tool_agent = true` ile tek analiz).
- ~~Faz 24: arama büyük/küçük harf ve "tam sözcük" seçenekleri, değiştir (Ctrl+H); bırakılan klasördeki kaynak dosyalarını listeleme.~~ → Faz 33.
- ~~Faz 24: toml'a yazıldıktan sonra masaüstü tercihlerindeki aynı geçersiz kılmalar gereksizleşir (zararsız); "toml'dan yeniden yükle" düğmesi yok.~~ → Faz 33.
- ~~Faz 23: `reference_solution_path` (`private/solutions/`) hâlâ çalışma dizinine göre; soru dosyasının ya da kaynak kökünün dizinine göre çözülmeli (sızıntı testi buna göre güncellenmeli).~~ → Faz 31.
- ~~Faz 23: mimari §20 ADR tablosunda ADR-0013/0014/0015 satırları eksik.~~ → Faz 31.
- ~~Faz 23: CI exe işi Roslyn denetleyicisini derlemiyor~~ → Faz 27.
- ~~Faz 21 denetimi O3: kurallar sıcak yolu fonksiyon adıyla eşliyordu.~~ → Faz 32'de fonksiyon kimliğiyle eşleştirme yapıldı.
- ~~Faz 21: `rules_version` yalnız `rules/*.py` hash'i; `analysis/` ve `data/call_costs.yaml` değişiklikleri önbellek anahtarına yansımıyor (bayat önbellek riski).~~ → Faz 31.
- ~~Faz 21: `log.exception` izi sınırsız ve CLI'da WARNING düzeyinde stderr'e basılır; kural istisna mesajı kullanıcı kodu parçası içerebilir (§12) — iz DEBUG'a ya da kısaltılmış mesaja alınabilir. `captured_logs` teardown'u önceki yapılandırmayı değil varsayılanı geri yükler.~~ → Faz 31.
- Faz 21: `file_value_types` ad çakışması (`struct Hit` + başka ad alanında `class Hit`) nadir yanlış negatif; yalnız arayüzden türeyen `class A : IFoo` sıcak sayılır (muhafazakâr).
- Faz 21'den kalan işler Faz 32'de kısmen kapandı: C-MEM-001 aynı dosyadaki kullanıcı fonksiyonu, UE-GC-001 `TArray` alanları ve CS-PERF-001 `IList` çözüldü. ~~C-MEM-003 akış duyarlılığı~~ (Faz 57'de çözüldü). Açık: döngüde `std::string +`/C# `string +=` karesel ipucu (Sonraya).
- ~~Faz 16: eval veri setine Python/HTML/CSS örnekleri ve ölçüm~~ → Faz 18'de yapıldı.
- ~~Faz 18: Tier 0 `</div>` kör noktası~~ → Faz 20'de HTML-STD-003 ile bulgu olarak.
- ~~Faz 20: HTML-STD-003 kaçırmaları (Faz 56): dosya sonunda bitmemiş `<div`, `<p><span>a<div>`, DOCTYPE'sız belgede `table`/`p`, aynı satırdaki farklı ihlaller, katalog açıklaması.~~ → Faz 56'da çözüldü.
- HTML-STD-003: adoption agency (biçimlendirme öğesi yeniden kurulumu), foster parenting ve `form`/`button` kapsam ayrıntıları modellenmiyor (Faz 56 bilinen sınır).
- ~~Kural motoru: bulgu sayısına üst sınır yok (600 satırlık kötü niyetli girdi 600 bulgu üretip prompt'a gidebilir).~~ → Faz 31.
- ~~Faz 18: `codementor eval check-drafts` Windows konsolunda (cp1254) çöküyor~~ → Faz 27 (konsol UTF-8).
- Faz 18: eski veri seti etiketlerine Faz 17 bulguları (`c-008` 4. satır `memory_safety` C-MEM-003, `csharp-009` 11. satır `garbage_collection` CS-ALLOC-002) eklenmeli mi? (test etiketleri de etkilenebilir; kullanıcı kararı)
- Faz 18: HTML precision (%22) için işaretleme prompt'unda bulgu ölçütü ("iyi uygulama önerisi" ile "sorun" ayrımı); kategori tanımları (`design` vs `edge_case`). Ayar yalnız dev'de yapılmalı.
- Faz 18: `eval breakdown` tablosuna gecikme/token sütunları; `breakdown` etiketleri koşu anındaki değil güncel veri setinden alıyor.
- ~~Faz 16: HTML etiket dengesi denetimi~~ → Faz 20 (statik kural).
- Faz 16: Python için few-shot örnekleri; JS (tarayıcı) desteği HTML ile birlikte istenebilir.
- Faz 15: Bağlantılar'da Ollama modelini indirme (`ollama pull`) düğmesi ve ilerleme göstergesi.
- ~~Faz 15: Masaüstü tercihleri ile `codementor.toml` arasında "toml'a yaz" seçeneği.~~ → Faz 24
- Faz 14: exe imzası yok; Windows SmartScreen ilk açılışta uyarabilir (kod imzalama sertifikası + Inno Setup kurulum paketi).
- ~~Faz 14: CI'da Windows exe derleme işi (artefakt olarak zip); şu an elle `make exe`.~~ → Faz 23
- ~~Faz 14: analiz iptali yok~~ → Faz 19'da yapıldı.
- ~~Faz 19: Tier 1 derleyici/çalıştırma sürecine iptal olayı iletilmiyor~~ → Faz 24 (durdurulan analizde Tier 1 kendi zaman aşımına kadar sürebilir; arayüz bu sırada yeni analizi bildirimle reddeder).
- ~~Faz 14: editörde arama (Ctrl+F), son dosyalar menüsü, sürükle-bırak ile dosya açma (tkinterdnd2).~~ → Faz 24
- Faz 14: onefile açılışı arşiv çözme nedeniyle birkaç saniye; hızlı açılış için onedir zip önerilir.
- ~~Faz 5/6 öncesi: tree-sitter ayrıştırmasına süre sınırı; 40 KB girdide yüzlerce ms ölçülmüştü.~~ → Faz 55'te kapatıldı (ADR-0024): süreç içi iptal 0.25.2'de kullanılamıyor; boyut/eşzamanlılık sınırları + gerileme testiyle idare, C# gramer yavaşlaması kabul edildi.
- ~~Tier 0: kapanmamış blok varken dosya sonuna uzanan ERROR düğümleri özete dönüşüyor; bağımsız gerçek hata ayrıca raporlanmayabilir (D2; Faz 55).~~ → Faz 55'te çözüldü (`trailing_semicolon_gap`).
- ~~`mask_non_code` C++ raw string (`R"(...)"`) içindeki tırnak/yorum/ayraçları doğru maskelemiyor (Faz 55).~~ → Faz 55'te çözüldü (delimiter sınırlı maskeleme).
- ~~C# 11 raw string (`"""…"""`) maskelemesi (Faz 55'te kapsam dışı bırakıldı).~~ → Faz H3'te yapıldı (`mask_non_code(text, language)`; `$`/`$$` önekleri ve kapanış tırnağı dizisi dahil).
- `mask_non_code` bir `language` parametresi aldı (Faz H3, C# 11 ham metni için) ama C++ ham metni yolu bilinçli olarak dilden bağımsız kaldı: Python/C# dosyasındaki `R"(…)` görünümü ham metin sayılıp içeriği maskelenir. Etkisi yalnızca `using_std`/`using_linq` sinyalleriyle sınırlı (Python'da kullanılmıyor); C++ yolunu dille sınırlamak gerekirse `language is Language.CPP` koşulu eklenir.
- ~~Tier 0 parse'ı sert zaman aşımıyla alt süreçte izole etmek (ADR-0024 sonucu)~~ → Faz 59'da yapıldı (ADR-0025; varsayılan kapalı).
- ~~Tier 0 yalıtımında sıcak işçi havuzu (her analizde ~280 ms süreç açma maliyeti; yüksek yükte) (Faz 59).~~
  → **KAPANDI** (Faz J iş 12; güvenlik sınırı KALAN_ISLER iş 14, ADR-0032).
- ~~`data/` dizini paket dışında; `pip install` ile dağıtımda veri dosyaları gelmez. Faz 13'te (Docker/dağıtım) `importlib.resources` veya paket verisi olarak ele alınmalı.~~ → Faz 23
- ~~Göreli veri dizinleri (`data.questions_dir`) çalışma dizinine göre çözülüyor; proje dışından çalıştırınca bulunamıyor. Config dosyasına göre çözme veya paket verisi (yukarıdaki madde) ile birlikte ele alınmalı.~~ → Faz 23
- ~~`.gitattributes` ile `* text=auto eol=lf`: Windows'taki CRLF uyarılarını ve şema dosyalarında satır sonu farklarını önler.~~ → Faz 23
- ~~`parse_bigo` şu an `log log n`, `n^n`, `Θ(...)`/`Ω(...)`, `max(n,m)` ve `k` gibi değişken üsleri desteklemiyor; eval'de LLM çıktılarında görülürse eklenebilir.~~ → Faz H3: `log log n`, `Θ`/`Ω` ve `max(a, b)` eklendi; `n^n` ve `n^k` bilinçli olarak reddedilmeye devam ediyor (sembolik üs modellenmiyor; `2^n` destekli) ve `docs/mimari.md` §5.6 buna göre düzeltildi.
- ~~`AnalysisReport.analysis_id` için ULID biçim doğrulaması~~ → Faz 27.
- ~~CI'a `actions/setup-dotnet` + `make roslyn-check` adımı~~ → Faz 27.
- ~~`ue_stubs.h` genişletilebilir (`Super` için `GENERATED_BODY` yerine sınıf başına typedef mümkün değil; delegeler `OnDestroyed.AddDynamic`, `FTimerManager`); eval'de Unreal uyarı gürültüsüne göre karar verilmeli.~~ → Faz H3'te delegeler, `FMath`, `FHitResult`, `FTimerHandle`/`FTimerManager` + `GetWorldTimerManager()` eklendi. `Super` (sınıf başına typedef) ve `AActor::OnDestroyed` gibi motor alanları hâlâ eksik → o satırlar uyarıya düşer; gürültü H4 eval'inde izlenecek.
- ~~`validation.stub_header` / `roslyn_check_dll` göreli yolları da çalışma dizinine göre çözülüyor (veri dizinleri maddesiyle birlikte ele alınmalı).~~ → Faz 23
- ~~`#pragma` makro genişletmeli biçimleri (`#pragma MACRO`) ve `#line` şu an serbest; derleyici kaynak okumadığı için risk düşük, ama include korumasına izin listesi eklenebilir.~~ → Faz H3'te yapıldı: `#pragma` izin listesi (`once`/`region`/`endregion`) + izin listesindeki adları tanımlayan `#define` reddi (macro ile `GCC dependency` atlatması kapanır) + `#line` yalnızca `#line <sayı>`. Kalan sınır: kullanıcının dahil ettiği bir başlık izin listesindeki adı tanımlarsa (yerel include'lar geçici/boş çalışma dizinine göre çözülür) izin listesi yine aldatılabilir; korunma için makro tablosu izlemek gerekir (yapılmadı).
- ~~gcc kolonları "display" birimli, clang bayt; Tier 0 karakter. Unicode içeren satırlarda kolonlar farklı olabilir (`-fdiagnostics-column-unit=byte` gcc ≥ 11).~~ → Faz H3'te `-fdiagnostics-column-unit=byte` eklendi (gcc ≥ 9, clang ≥ 14); Tier 0 karakter saymaya devam eder, ASCII'de özdeş. Bayrağı tanımayan sürümde komut bayraksız yeniden denenir.
- ~~Faz 6'da ertelenen 10 statik kural~~ → Faz 17'de yapıldı (2026-10-01).
- ~~Faz 17: C-MEM-003 denetimin kullanımdan sonra yapıldığını görmüyor~~ (Faz 57'de çözüldü; yanlış
  dal ve koşullu koruma ayırt edilmiyordu). UNITY-GC-001 closure bastırması satır bazlıydı.
  → **KAPANDI (iş 5 dilim 3 ve 5, 2026-10-18):** LINQ lambdasının closure'ı olgularda ayrı `CLOSURE`
  sayılmıyor (bayt aralığı; aynı satırdaki LINQ dışı lambda bulgu kalır, `positive/closure_next_to_linq.cs`);
  C-MEM-003'ün akış biçimleri fixture+test ile sabitlendi (denetim tahsisten önceyse sayılmaz, tek
  dallı denetim diğer yolu kapatmaz, koşulda kullanım; `negative/guard_forms_in_branches.c`).
- `test_toolchain_install.py` tam koşuda bir kez 4 testle aralıklı düştü (Faz 57); tek başına yeşil. Tekrarlarsa paylaşılan geçici dizin/yarış incelenmeli. → Faz 58'de çözüldü (Windows tarayıcı kilidi; `_rename` yeniden denemesi).
- ~~C-MEM-001: aynı dosyadaki kullanıcı fonksiyonuna geçirilen işaretçi (`print_arr(arr, n)`) sahiplik aktarımı sayılıyor (sık kaçırma)~~ → **KAPANDI (Faz 32 + iş 5 dilim 2, 2026-10-18):** aynı dosyada tanımlı okuyucu yardımcıya vermek kaçış sayılmıyor (`_borrowers`) ve ödünç artık **zincir boyunca** yayılıyor (`_MAX_BORROW_ROUNDS = 8` sabit noktası; `positive/passed_to_reader_chain.c`, `test_c_memory_flow.py`). Bilinçli sınırlar (kaçırma): aynı değişkene iki kez `malloc`, gölgeleme, `realloc`, yalnız bildirimli/çift adlı yardımcı ve işaretçiyi döndüren/saklayan yardımcı.
- ~~UNITY-GC-001: dosyada tanımlı kullanıcı `struct`'ı için `new Hit(3)` yanlış bulgu (değer tipi)~~ → **KAPANDI (Faz 21 + iş 5 dilim 3, 2026-10-18):** `analysis/_memory.py` `file_value_types` dosyadaki `struct`/`record struct` adlarını topluyor (fixture `negative/user_struct_new.cs`, `negative/value_types_in_update.cs`); dosyada tanımlı **sınıf** için bulgu sürüyor. Ayrıca closure bastırması satır bazlı olmaktan çıktı (bkz. üstteki Faz 17 satırı).
- ~~UE-GC-001: `TArray<AActor*>`/`TMap<..., UObject*>` kapsayıcı alanları kaçırılıyor; UCLASS olmayan sınıfta (`FPlain`) öneri `UPROPERTY` değil `TStrongObjectPtr`/`FGCObject` olmalı~~ → **KAPANDI (Faz 32 + iş 5 dilim 4, 2026-10-18):** tek katman Faz 32'de gelmişti; **iç içe** kapsayıcı (`TMap<FName, TArray<UObject*>>`) da sayılıyor (`_MAX_CONTAINER_DEPTH = 2`, `type_descriptor` açılıyor). `TWeakObjectPtr`/`TSoftObjectPtr`/`TStrongObjectPtr` kapsam dışı (`negative/gc_safe_wrappers.h`); UCLASS/USTRUCT olmayan tipte soru `_UNREFLECTED` metnini kullanıyor.
- ~~CS-PERF-001: `IList`/`IReadOnlyList`/`ICollection` tipli değişkenler maliyet tablosunda çözülmüyor (kaçırma).~~ → Faz H2: `IList` → `List.Contains` (Faz 21), `IReadOnlyList.Contains` → `Enumerable.Contains` (LINQ) düzeltildi; `ICollection` bilinçli kaçırma (örnek metot).
- ~~Kural motoru: çöken kuralın istisna izi loglanmıyor; structlog (Faz 10) ile `log.exception` eklenmeli.~~ → Faz 21/31.
- Sıcak yol tespiti sınıf tabanını (MonoBehaviour / UCLASS) da denetlemeli (Faz 5 olgusu).
- Faz 7: OpenAI katı modu bugün `maxLength`, `maxItems`, `pattern`, `minimum`, `maximum` destekliyor; `SchemaAdapter` kısıt temizliğini sağlayıcıya göre ayırabilir (şu an hepsi çıkarılıyor, K5 doğruluyor).
- Faz 7: `ProviderResult`'a yanıt veren sağlayıcının yeteneği (şema zorlandı mı) eklenebilir; fallback sonrası K5 için.
- Faz 7: `FakeReply` bir dataclass olarak `providers/fake.py`'de (Pydantic şeması değil, test düzeneği); gerekirse `models/`'e taşınabilir.
- ~~Faz 7: token tahmini ve `pricing.yaml` maliyet tahmini (mimari §13)~~ → Faz 25.
- ~~Faz 4 `run_process` çıplak `argv[0]`~~ → çözüldü (2026-09-29): yalnızca mutlak yol, `test_bare_or_relative_executable_rejected`.
- ~~CLI ajanları: gerçek `run_process` ile uçtan uca test~~ → Faz 25; agy canlı doğrulaması hâlâ açık (oturum var).
- ~~Faz 8: `call_costs.yaml`'a C# `RemoveAll`/`RemoveAt(0)`/`Insert(0, …)` maliyetleri (golden'da `Remove: O(1)` ipucu).~~ → `RemoveAll`/`RemoveAt`/`Insert` tabloda `n` idi (Faz 21); Faz H3'te argümana duyarlı ayrım eklendi: `RemoveAt(xs.Count - 1)` → `1`, `Insert(xs.Count, …)` → `1*`.
- ~~Faz 8 denetim D3 (`&lt;` kanıtı)~~ → Faz 9'da çözüldü (`normalize_evidence`).
- ~~Faz 8 denetim D2: `prompt_version` her build'de şablon dosyalarını okuyor~~ → Faz 26.
- Faz 8 denetim D8: ~~`prompts.dir`~~ Faz 23'te çözüldü; demo'nun golden dizini (`tests/golden/prompts`, geliştirici aracı) hâlâ çalışma dizinine göre.
- Faz 8: prompt'ların `claude_cli` ile canlı karşılaştırması (analysis vs single_pass) Faz 12 eval'inde; token tahmininin gerçek `usage` ile kalibrasyonu.
- ~~Faz 9: sızıntı korumasını `reasoning_steps` ve LLM açıklamalarına genişletmek~~ → Faz 10'da yapıldı.
- ~~Faz 9: `guiding_questions` öğelerine şemada `max_length`~~ → Faz 27.
- ~~Faz 10: `prompt_version` mtime önbelleği~~ → Faz 26.
- ~~Faz 10: CLI ilerleme göstergesi yalnızca aşama adını gösteriyor; token/süre canlı gösterilebilir.~~ → Faz 33.
- ~~Faz 11: senkron aşamaları `asyncio.to_thread`'e taşımak~~ → Faz 24 (Tier 1) + Faz 26 (Tier 0, olgular); SQLite Sonraya.
- Faz 11: API anahtarı / hız sınırlama (§12); yerel olmayan bağlamada zorunlu kılınabilir. (Faz 13 kararı: v1'de yok, README Sınırlamalar.)
- ~~CLI ajanı iptali~~ → Faz 19'da yapıldı.
- ~~Faz 5 hatası (csharp-011): `foreach` koleksiyon ifadesindeki çağrı döngü içinde sayılıyordu → `high` O(n²)~~ → çözüldü (2026-09-30, kullanıcı isteğiyle Faz 12 içinde): `_context.contexts` döngü başlığında bir kez değerlendirilen alanlara (`initializer`, `right`: C `for` başlatıcısı, C++ range-for, C# `foreach`) dış bağlamı verir; `tests/fixtures/complexity/on_{foreach_header_call,range_for_header_call,for_initializer_strlen}` + koşuldaki `strlen` için `on2_strlen_condition`. Dev static-only Big-O %88 → %92.
- Çağrı maliyeti tablosu eksikleri (eval notları): `std::memset`/`memcpy` (n), `UGameplayStatics::GetAllActorsOfClass` (n), `TArray::Remove` (n); `std::string operator+` / C# `string +=` döngüde karesel (şu an n).
- ~~Faz 12: eval'e `guard_interventions` metriği~~ → Faz 22 Aşama A.
- ~~Faz 12: `eval analyze` aracı (kategorisiz eşleşme, önem filtreli precision, örnek bazında FP/FN); `compare` statik satırında injection direncini "—" göstermeli.~~ → Faz 22A / Faz 31.
- Faz 12: precision iyileştirme — `design` bulgularını yalnızca soru gereksinimi varken üretmek, `low` bulguları raporda ayrı göstermek; kategori belirsizliği (sıfıra bölme `edge_case`/`undefined_behavior`, null `edge_case`/`memory_safety`) için prompt'ta kategori tanımları. Değişiklik sonrası dev'de yeniden ölçülmeli (test artık kullanıldı).
- Faz 12: few-shot 0/1 ablasyonu (§14.4) koşulmadı. → Faz 34.
- CI Windows işi (2026-09-30): `windows-latest`'te g++ (MinGW) ilk derlemede 10 sn sınırını aşıyor (`test_cpp_type_error_failed` → `timeout`); clang++ varsayılan MSVC hedefli olduğundan Unreal stub denetimi `tool_error` ile atlanıyor (2 test). Ürün zarif atlıyor ama Windows'ta clang için `--target=x86_64-w64-mingw32` / başlık yolu ve soğuk başlangıç süresi ele alınmalı; o zamana kadar Windows CI `-m "not live and not compiler"`.
- ~~Faz 13: README için GIF demo~~ → Faz 26 (Pillow).
- ~~Faz 13: Web UI'da indirme, sağlayıcı ve mod seçimi~~ → Faz 26.
- ~~Faz 13: Monaco'yu tembel yükleme~~ → Faz 26.
- ~~Faz 13: `YAPILANLAR.md`'ye Faz 8–12 özetleri~~ → Faz 26.
- ~~Faz F (F8 denetimi): `desktop/connections.py` 402 satır (> 400, AGENTS.md)~~ → F12'de oturum açma akışı `desktop/login.py`'ye çıkarılınca **366 satıra** indi (400 satır kuralı sağlanıyor); `KeyStore`/katalog taşıma önerisi gereksiz kaldı.
- Faz F (F11 kapsamı): `history_controller.open_history` kaydı hâlâ ana iş parçacığında okuyor (`get_analysis`/`get_row` + `runtime.load_source`) ve diskten kod yüklüyor; F11 yalnız liste/silme/temizleme ile sınırlı tutuldu, kayıt açmayı da arka plana almak Sonraya.
- Faz F (F12): macOS'ta `open -a Terminal <cli>` ek argümanları (ör. `claude auth login`) Terminal uygulamasına geçirmez; `osascript -e 'tell application "Terminal" to do script "…"'` ile argümanlı sürüm Sonraya (şimdilik CLI argümansız açılıp kendi oturum açma akışını başlatıyor).

## Faz I (dilim 1) — Eval Altyapısı ve Ölçüm Doğruluğu (KALAN_ISLER.md iş 10; 2026-10-20)

> İş 10 kapandı. Canlı model harcaması olmadan eval araçları ve ölçüm determinizmi tamamlandı.

**Yapılanlar:**
- `src/codementor/eval/parts.py`: Parça atamasının deterministikliğini SHA-256 ile özetleyen `part_signature(samples, parts)` ve parçalı sonuçların çakışma/eksiklik durumunu denetleyen `check_parts_coverage(part_results, all_samples)` eklendi.
- `src/codementor/eval/compare.py`: Yalnızca parçalı koşular karşılaştırıldığında (`all(r.config.part is not None)`), parçaların çakışan örnekler içerip içermediğini denetleyen dipnot uyarısı bağlandı.
- `prompts/v1/fewshots/*.yaml`: 8 fewshot dosyasındaki `additional_findings` girdilerine `certainty: high` alanı eklendi; `tests/golden/prompts/` golden snapshot'ları güncellendi.
- `prompts/v1/judge.j2`: LLM-as-judge ile Sokratik rehberlik kalitesini (pedagojik değer, koda temas, sokratik derinlik 1-5, doğrudan çözüm sızdırmama bool) puanlayan Jinja2 şablonu oluşturuldu.
- `src/codementor/eval/judge.py`: `evaluate_socratic_quality`, `judge_run_result`, `judge_summary_markdown` fonksiyonları ile yapılandırılmış çıktı üreten yargıç motoru kuruldu.
- `src/codementor/cli/eval.py`: `codementor eval judge --run <path> --judge-provider <provider>` CLI alt komutu eklendi.
- `tests/unit/eval/test_judge.py` ve `tests/unit/eval/test_parts.py`: 30 yeni test eklenerek FakeProvider ile tüm yargıç ve parça mantığı uçtan uca doğrulandı.

**Doğrulama:**
- `uv run ruff check .` temiz.
- `uv run ruff format --check .` 484 dosya temiz.
- `uv run mypy src/` 217 kaynak dosya temiz.
- `uv run pytest tests/unit/eval/` 132/132 geçti.
- `uv run pytest tests/golden/prompts/` 10/10 geçti.
- ~~Faz F (F10 denetimi, 2026-10-14): küçük bulgular — `run_ollama_pull` içindeki `result.error` ve `result.timed_out` dalları test edilmiyor; model adı deseni `.` ve `/` karakterlerini kabul ediyor (`/x`, `../x` zararsız); `ollama pull` süreci iptal edilemiyor (köprüde `Cancellation`, arayüzde iptal düğmesi yok). Ayrıntı: `docs/BulgularVeDuzeltilecekler.md` §10 Faz F.~~ → **KAPANDI (İş 9, 2026-10-20):** `OLLAMA_MODEL_RE` alfanümerik başlangıcı zorunlu kıldı; eksik dallar test edildi; `cancel: threading.Event`, `cancel_pull` ve `confirm_close` entegrasyonu sağlandı.

## Faz I (dilim 2) — Deterministik Sokratik Kalite Kapısı ve Küçük Model Korumaları (KALAN_ISLER.md iş 11; 2026-10-20)

> İş 11 kapandı. ADR-0031 mimari kararı uygulandı. Küçük modeller (7B/8B/Ollama) için deterministik sağduyu denetimleri, karmaşıklık politikası ve Sokratik kalite kapısı tamamlandı.

**Yapılanlar:**
- `docs/adr/0031-kucuk-modeller-icin-deterministik-sokratik-kalite-kapisi.md`: Küçük modeller için deterministik sokratik kalite kapısı, karmaşıklık uzlaştırması ve sağduyu filtreleri ADR olarak belgelendi; `docs/mimari.md` ve README belgelerine işlendi.
- `src/codementor/config.py`: `PipelineSettings.model_profile` (`standard` / `small`) ve `PipelineSettings.verify_provider` (Pass V için ayrı sağlayıcı yönlendirmesi) alanları eklendi. `OllamaConfig.profile` eklendi.
- `src/codementor/verify/sanity.py`: `apply_sanity_checks` ve `is_guard_hallucination` fonksiyonları geliştirildi; kanıt satırında `if(...)` kontrolü olan kodlarda modelin uydurduğu "kontrol edilmemiş/ele alınmamış" halüsinasyon bulguları elenir; `small` profilde en kritik 3 bulguya sınırlandırma uygulanır.
- `src/codementor/verify/complexity_policy.py`: `apply_complexity_policy` ile statik ipucu ile küçük model çeliştiğinde deterministik statik ipucuna öncelik veren uzlaştırma politikası bağlandı.
- `src/codementor/verify/socratic_gate.py`: Jaccard benzerliği (>= 0.70 deduplication), n-gram ardışık döngü tespiti (`has_repetition_loop`), koda temas denetimi (`touches_code`) ve Sokratik soru kalitesi kapısı (`evaluate_socratic_gate`) eklendi.
- `src/codementor/pipeline/socratic_pass.py`: 400 satır sınırını korumak için Sokratik mantık dilimlendi; orkestratör ve test yamalarıyla tam uyumlu hale getirildi.
- `src/codementor/pipeline/orchestrator.py` & `verify_pass.py`: `verify_provider` tanımlandığında Pass V doğrulamasının belirlenen sağlayıcı üzerinden yürütülmesi sağlandı.
- `tests/unit/verify/`: `test_sanity.py`, `test_complexity_policy.py`, `test_socratic_gate.py` ve `test_pipeline_small_model.py` (17 yeni test) FakeProvider ile deterministik olarak doğrulandı.

**Doğrulama:**
- `uv run ruff check .` temiz.
- `uv run ruff format --check .` 493 dosya temiz.
- `uv run mypy src/` 221 kaynak dosya temiz.
- `uv run pytest -m "not live"` 3957 geçti, 16 atlandı, 0 hata.

## Faz J — Havuz Kod İşleri (KALAN_ISLER.md iş 12; 2026-10-20)

> İş 12 kapandı. Zig budama, Tier 0 sıcak işçi havuzu, Windows CI MinGW/clang hedefi, METHOD_LEAKS ve örnek girdi/çıktı alanları tamamlandı.

**Yapılanlar:**
- `src/codementor/models/questions.py`: `SampleIO` modeli eklendi; `QuestionPublic` ve `UserQuestionDraft` içine `sample_io: list[SampleIO]` bağlandı. `Question` içine `method_leaks: list[str]` eklendi ve `MENTOR_FIELDS`'a dahil edilerek public çıktıda gizlenmesi garantilendi.
- `data/questions/*.yaml`: Tüm 64 yerleşik soru YAML dosyasına çözüm yöntemini ele veren gizli terimler `method_leaks:` listesi olarak taşındı; temsilci sorulara `sample_io:` örnekleri eklendi.
- `tests/unit/test_question_data.py`: `test_prompts_do_not_reveal_method` doğrudan soru verisindeki `q.method_leaks`'i test edecek şekilde güncellendi; `test_sample_io_structure_and_coverage` eklendi (81 test yeşil).
- `src/codementor/config.py`: `ValidationSettings.tier0_warm_workers` ayarı eklendi.
- `src/codementor/validation/tier0_worker.py`: `--pool` ve `--loop` modları eklenerek satır-sınırlı JSON akışıyla sürekli çalışan sıcak işçi protokolü geliştirildi.
- `src/codementor/validation/tier0_pool.py`: `Tier0Worker` ve `Tier0WorkerPool` sınıfları yazılarak thread-safe işçi havuzu, çökme kurtarması ve zaman aşımı denetimi bağlandı.
- `src/codementor/validation/tier0_isolation.py`: `tier0_warm_workers > 0` iken istekleri sıcak işçi havuzuna yönlendiren akış bağlandı; `close_tier0_pool` eklendi.
- `tests/unit/test_tier0_pool.py`: İşçi yaşam döngüsü, yeniden kullanım, çökme kurtarma ve yalıtım entegrasyonunu doğrulayan 5 yeni birim testi yazıldı.
- `src/codementor/validation/toolchain.py`: Windows'ta clang/clang++ keşfedildiğinde otomatik olarak `--target=x86_64-w64-mingw32` bayrağı bağlandı.
- `.github/workflows/ci.yml`: Linux CI'da zig kurulumundan sonra otomatik budama adımı (`tools/prune_zig.py`), Windows CI'da derleyici ısınma adımı eklendi.
- `src/codementor/validation/toolchain_prune.py` & `tools/prune_zig.py`: Zig kurulumundan yabancı platform/mimari libc başlıklarını budayan motor ve CLI aracı yazıldı.
- `tests/unit/test_toolchain_prune.py`: Kuru çalıştırma (dry-run), gerçek temizlik ve CLI çağrılarını doğrulayan 5 test yazıldı.

**Doğrulama:**
- `uv run ruff check .` temiz.
- `uv run ruff format --check .` 498 dosya temiz.
- `uv run mypy src/` 223 kaynak dosya temiz.
- `uv run pytest tests/unit/test_question_data.py tests/unit/test_tier0_pool.py tests/unit/test_toolchain_prune.py tests/unit/test_toolchain.py tests/unit/test_tier0_isolation.py` 142 geçti, 1 atlandı.

## Doküman Tutarlılık Turu (KALAN_ISLER.md iş 13; 2026-10-20)

> İş 13 kapandı. Tüm otomatik ajan görevleri (A.1 - A.13) başarıyla tamamlandı.

**Yapılanlar:**
- `docs/UYGULAMA_PLANI.md`: Faz A'dan Faz K'ya kadar tüm harfli fazların güncel tamamlanma durumları ve tarihleri yol haritası tablosuna işlendi.
- `docs/mimari.md`: §20 Mimari Karar Kayıtları (ADR) tablosunun diskteki 31 ADR ile tam birebir eşleştiği doğrulandı (0 eksik).
- `docs/rules-catalog.md`: Kural kataloğu ile `src/codementor/rules/` modüllerinin 33 kuralının tam eşleştiği doğrulandı (0 eksik, 0 fazla).
- `docs/gelistirme-gunlugu/README.md`: Dizin güncellenerek Faz H raporu, güncellemeler ve eval rehberi eklendi.
- `KALAN_ISLER.md`: Bölüm A altındaki tüm ajan maddeleri `[x]` olarak işaretlendi.

**Doğrulama:**
- `uv run ruff check .` temiz.
- `uv run ruff format --check .` 498 dosya temiz.
- `uv run mypy src/` 223 kaynak dosya temiz.
- `tests/unit/test_release_readiness.py` 15/15 geçti.



