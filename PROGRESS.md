# İlerleme Günlüğü

> Ayrıntılı notlar arşivde: Faz 0-63 → [docs/gelistirme-gunlugu/PROGRESS-faz-0-63.md](docs/gelistirme-gunlugu/PROGRESS-faz-0-63.md); public öncesi Faz A-K, KALAN_ISLER iş 1-23 ve 2026-10-20 tam taraması → [docs/gelistirme-gunlugu/PROGRESS-faz-A-J.md](docs/gelistirme-gunlugu/PROGRESS-faz-A-J.md). Yeni fazların notları buraya eklenir (AGENTS.md faz bitirme protokolü).
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

## CI — Faz E-J'nin ilk Linux/CI koşusu (2026-10-20)

Faz E-J ve KALAN_ISLER commit'leri 2026-10-20'ye dek hiç push edilmemişti; ilk CI koşusu yalnız testlerdeki
platform varsayımlarını yakaladı (ürün kodu değişmedi):
- `tests/desktop/test_connections_2.py` (iş 22 bölmesi) `ConnectionsController`'ı modül düzeyinde içe
  aktarıyordu (customtkinter → tkinter); Linux CI'da tkinter yok → dosya toplanamadı. İki test
  `pytest.importorskip` ile alır; dosyanın Tk'siz 27 testi Linux'ta koşar. Yerel taklit: `sys.modules`'ta
  `tkinter`/`_tkinter` = None ile tam koşu 3969 geçti.
- `test_login.py` (4): `resolve_executable` sembolik bağlantıyı çözer (Linux venv python → `/usr/bin/python3.x`);
  beklenen yol da çözülmüş yol.
- `test_needs_update_false_without_configured_source`: host'un `linux-x86_64` olmadığını varsayıyordu →
  `platform_key` sahtelenir.
- `test_linear_time_large_input[c-nested-call]` Windows CI'da 2,046 sn > 2,0 sn (yerelde 0,42; `--cov`
  yavaşlatması). Üç dosyada kopyalanmış Faz 53 `_deadline` kalıbı ortak `tests/timing.py` oldu; kural
  motoru testi de kullanır (kapsamasız 2,0 sn, `--cov` altında 8,0 sn).
- `test_tier0_growth_is_linear[cpp-template-ambiguity]` Windows CI'da 2× girdide 3,12× (sınır 3,0×);
  yerelde her 2× adımda ~2,0× (ölçüldü, gerileme yok). Neden: küçük ve büyük girdi art arda ölçülüyordu,
  koşucudaki geçici yük yalnız büyüğe denk gelince oran şişiyordu. Ortak `tests/timing.best_pair` iki
  girdiyi **dönüşümlü** ölçer (ısınma + 3 tur, en iyisi); Tier 0 ve O1-O3 büyüme testleri kullanır.
  Sınır değişmedi; sonda: karesel iş 4,39× (yakalanır), doğrusal 1,98×.

## Bağımlılıklar — Dependabot PR'ları (#1, #3, #5, #6, #7; 2026-10-20)

- **#7 (python-minor, 12 paket) olduğu gibi alınmadı:** Dependabot `tree-sitter>=0.25.2,<0.26` sınırını
  `<0.27`'ye genişletmişti; 0.26.0 ile Linux CI'da `test_parsers` kırmızı ve ardından segfault (çıkış 139).
  Sınır korundu, diğer 11 paket `uv lock --upgrade-package` ile güncellendi (pydantic 2.14.1,
  pydantic-settings 2.16.1, fastapi 0.143.3 — PR'daki sürüm; serbest yükseltme 0.156'ya atlıyordu —,
  ruff 0.17.1, mypy 2.4.0 ve diğerleri); #5 (`types-jsonschema`) aynı kilitte. `dependabot.yml`'a
  tree-sitter minor/major için `ignore` eklendi (her hafta yeniden önerilmesin).
- **#1 (Actions ana sürümleri), #6 (npm-minor), #3 (jsdom 30)** cherry-pick edildi; #3 ile #6
  `web/package*.json`'da çakıştı → #6 temel alındı, jsdom ^30.1.2 yazılıp kilit `npm install` ile yeniden
  üretildi (`npm ci` tutarlı). Not: jsdom 30'un alt bağımlılıkları Node ≥24.15 istiyor (bu makinede
  24.13.1 uyarı verdi; CI en güncel 24.x).
- **Doğrulama:** ruff (0.17.1 ile yeni uyarı yok), mypy 2.4.0 strict temiz, tam paket yeşil; web
  gen:types farksız, typecheck, 57 vitest, build; `npm audit --omit=dev --audit-level=high` geçiyor
  (yalnız 2 düşük: monaco-editor → dompurify, önceden de vardı). `release.yml`'daki upload/download-artifact
  ana sürümleri yalnız etiketle koşar → ilk etikette doğrulanmalı (KALAN_ISLER U4).

## Son durum (2026-10-20)

- Faz 0-63 ve public öncesi Faz A-K bitti; `KALAN_ISLER.md` ajan işleri (1-23) kapandı. Son oturumda
  oturum commit'lerine kod-denetci denetimi yapıldı ve Windows dosya kilidinde atomik yazımların sessizce
  başarısız olması düzeltildi (`paths.replace_file`). Ayrıntı: arşivdeki son bölümler.
- Kalanlar yalnız kullanıcı işleri (`KALAN_ISLER.md` §B: Y2 referans çözüm kontrolü, GitHub ayarları,
  canlı ölçümler). §C kararları 2026-10-20'de kapandı: `.agents/`/`.claude/` repoda kalıyor (P12),
  bu dosya arşivlendi (P6), Faz 18 etiket sorusu Faz 21'de zaten uygulanmıştı.
- Açık fikirler aşağıdaki "Sonraya" bölümünde.

## Sonraya (kapsam dışı fikirler)
> 📋 Ajan ile yapılabilecek işlerin öncelikli listesi ve durumu: [KALAN_ISLER.md](KALAN_ISLER.md).
> Bu bölüm fikirlerin kaynağıdır; iş sırası ve kabul kriterleri KALAN_ISLER.md'de tutulur.
- ~~**Tam tarama kalan bulguları (kod-denetci, 2026-10-20; #1, #3, #4 ve KALAN_ISLER 14-23 kapandı;
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
  - ~~Orta (iş 18): `python_check.py` `warnings.catch_warnings` iş parçacığı güvenli değil~~ → **KAPANDI (iş 18).**
  - ~~Orta (iş 19): `eval/judge.py` + `judge.j2` girdileri `guard`'sız, hata yönetimi zayıf~~ → **KAPANDI (iş 19).**
  - ~~Orta (iş 20): Codex iptalinde `TemporaryDirectory` temizlik hatası iptali maskeleyebilir~~ → **KAPANDI (iş 20).**
  - ~~Düşük (iş 21): `RateLimiter._records` sınırsız, `mimari.md:1126` hız sınırı çelişkisi,
    `sessions.updated_at` NULL budanmıyor, `PruneReport` models/ dışında~~ → **KAPANDI (iş 21)**; ayrıca
    `root_path` arkasında API anahtarı atlanması bulundu ve kapandı.
    (README/ZAYIF satır sayısı testleri artık toleranslı → iş 23 kapandı.)~~ → **KAPANDI (2026-10-20): tüm alt maddeler kapandı (iş 14-23).**
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
- ~~**Public öncesi zorunlu (kullanıcı, 2026-10-13):** Y2 — `tests/fixtures/llm_responses/unity03_reference.cs`
  bankadaki unity-03 referans çözümüyle (`private/`) karşılaştırılacak; aynı/benzerse yapay bir
  çözümle değiştirilip golden'lar yeniden üretilecek. GitHub'da secret scanning, push protection,
  Dependabot alerts açılacak (P13).~~ → **TAŞINDI (2026-10-20): kullanıcı işi, `KALAN_ISLER.md` U2 (Y2) ve U3 (GitHub ayarları).**
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
- ~~Faz 36: kural bazında öneri türü (doğru eşleşmiş `new`/`delete` için CPP-OWN-001, `Reserve` yok UE-MEM-001, `with` dışı `open` PY-RES-001). ~~Claude Opus canlı dev ölçümü~~ → yapıldı (2026-10-05).~~ → **KAPANDI: KALAN_ISLER iş 7 (`Rule.kind`, ADR-0022) — 2026-10-20 doğrulandı.**
- ~~Eval: `select_part` etiket değişikliğine duyarlı; parça atamasını kimlik özetiyle sabitlemek ya da sonuç dosyasına parça kimliklerini yazıp birleştirmede eksik/çakışanı uyarmak.~~ → **KAPANDI: iş 10 (`part_signature`, `check_parts_coverage`) — 2026-10-20 doğrulandı.**
- ~~Faz 37: kullanıcının keyring'inde kalmış eski OpenAI/DeepSeek anahtarlarını temizleme seçeneği.~~ → **KAPANDI: `KeyStore.purge_legacy` + Bağlantılar düğmesi — 2026-10-20 doğrulandı.**
- ~~Faz 34: dev setini büyütmek~~ → yapıldı (2026-10-04, dev 96). Kalan: few-shot'ların zayıf modelde etkisi.
- ~~Faz 35: few-shot örneklerine `certainty` alanı eklemek (şu an yalnız kural metninde). ~~Doğrulama kararlarını eval sonucuna yazıp düşürülenlerin TP/FP dağılımını ölçmek~~ → Faz 39.~~ → **KAPANDI: iş 10 (few-shot `certainty: high`) — 2026-10-20 doğrulandı.**
- ~~Faz 30: web soru seçicisinde filtre sonucu boşsa 'eşleşen soru yok' mesajı (şu an yalnız 'Serbest mod' seçeneği kalıyor).~~ → **KAPANDI: "Bu filtrelerle eşleşen soru yok." (`Controls.test.tsx`) — 2026-10-20 doğrulandı.**
- ~~Faz 30: `validate` ile `load_reference` aynı çözüm yolu doğrulayıcısını paylaşsın (validate şu an yalnız `is_file()`); dağıtımda `private/` olmadığı için `reference_solution_unreadable` uyarısı her soru bağlamlı analizde loglanıyor, düzeyi `debug` olabilir.~~ → Faz 31.
- ~~Faz 30: yöntem işaretlerini (`METHOD_LEAKS`) soru verisine taşıyıp `validate`'e eklemek; eski soruların kontrol listesi seçimini kilitleyen bir anlık görüntü testi.~~ → **KAPANDI: `Question.method_leaks` (iş 12) + Faz J anlık görüntü testi — 2026-10-20 doğrulandı.**
- ~~Faz 30: Unreal stub'ına sık türler (`Super` için sınıf içi typedef deseni, `FMath`, `EEndPlayReason`, `FHitResult`, `UPrimitiveComponent`, `USphereComponent`, dinamik delege makroları, `GetWorldTimerManager`); şu an referans çözümler bile yalnız tavsiye uyarılarıyla geçiyor.~~ → **KAPANDI (2026-10-20): stub'a bileşen/aktör türleri, `UGameplayStatics`, `EEndPlayReason`, `StaticClass`; `Super` Tier 1'de UHT gibi typedef'le (`unreal_super_typedefs`); 24 Unreal örneğinde temiz geçen 2 → 4.**
- Faz 30: soru bankası için öğretmen/kullanıcı içerik incelemesi ve sorulara örnek giriş/çıkış alanı.
- ~~Faz 29: kurulu zig sürümünü `codementor.toml` ile karşılaştırıp masaüstünde "güncelle" önermek (işaret dosyasında sürüm/sha var, okunmuyor).~~ → **KAPANDI: Faz F (F9) `needs_update` + masaüstü güncelle — 2026-10-20 doğrulandı.**
- ~~Faz 29: indirilen zig'den yerel hedef dışındaki libc başlıklarını budamak (382 MB → tahminen <150 MB).~~ → **KAPANDI: iş 12 `toolchain_prune.prune_zig_directory` — 2026-10-20 doğrulandı.**
- ~~Faz 29: tek dosya exe gömülü RoslynCheck.exe'yi %TEMP%'e açıyor; AppLocker/antivirüs engellerse `/health/ready`'de araç hatası. Gerekirse onedir dağıtımı ya da kullanıcı dizinine kopyalama.~~ → **BİLİNÇLİ (2026-10-20): release onedir zip'i de veriyor (AppLocker/antivirüs ortamında o kullanılır); tek dosya kolaylık için kalıyor.**
- ~~Faz 26: API hız sınırı (istemci başına, süreçler arası doğru); web arayüzünün API anahtarı göndermesi.~~ → **KAPANDI: Faz E hız sınırı + `X-API-Key` (web istemcisi gönderiyor, `client.test.ts`) — 2026-10-20 doğrulandı.**
- ~~Faz 26: SQLite çağrılarını da iş parçacığına almak (bağlantı başına iş parçacığı ya da havuz).~~ → **BİLİNÇLİ (2026-10-20): liste/silme uçları senkron `def` (FastAPI iş parçacığı havuzu); analiz yolundaki çağrılar ms düzeyinde ve `reserve_attempt`/iptalde `release_attempt` Faz 19/49 atomiklik garantilerinin içinde — iş parçacığına taşımanın getirisi küçük, riski gerçek.**
- ~~Faz 25: OpenAI katı mod kısıtlarını canlı anahtarla doğrulayıp `SchemaAdapter.openai_strict`'te desteklenenleri korumak.~~ → **GEÇERSİZ: OpenAI sağlayıcısı kaldırıldı (ADR-0021); Gemini katı modu ADR-0020'de — 2026-10-20.**
- ~~Faz 25: masaüstü ve web raporunda tahmini token/maliyet gösterimi (şu an yalnız CLI alt satırı ve JSON).~~ → Faz 33.
- ~~Faz 25: agy canlı doğrulaması (oturum var; `allow_tool_agent = true` ile tek analiz).~~ → **KAPANDI: Faz 63'te agy uçtan uca canlı çalıştı — 2026-10-20 doğrulandı.**
- ~~Faz 24: arama büyük/küçük harf ve "tam sözcük" seçenekleri, değiştir (Ctrl+H); bırakılan klasördeki kaynak dosyalarını listeleme.~~ → Faz 33.
- ~~Faz 24: toml'a yazıldıktan sonra masaüstü tercihlerindeki aynı geçersiz kılmalar gereksizleşir (zararsız); "toml'dan yeniden yükle" düğmesi yok.~~ → Faz 33.
- ~~Faz 23: `reference_solution_path` (`private/solutions/`) hâlâ çalışma dizinine göre; soru dosyasının ya da kaynak kökünün dizinine göre çözülmeli (sızıntı testi buna göre güncellenmeli).~~ → Faz 31.
- ~~Faz 23: mimari §20 ADR tablosunda ADR-0013/0014/0015 satırları eksik.~~ → Faz 31.
- ~~Faz 23: CI exe işi Roslyn denetleyicisini derlemiyor~~ → Faz 27.
- ~~Faz 21 denetimi O3: kurallar sıcak yolu fonksiyon adıyla eşliyordu.~~ → Faz 32'de fonksiyon kimliğiyle eşleştirme yapıldı.
- ~~Faz 21: `rules_version` yalnız `rules/*.py` hash'i; `analysis/` ve `data/call_costs.yaml` değişiklikleri önbellek anahtarına yansımıyor (bayat önbellek riski).~~ → Faz 31.
- ~~Faz 21: `log.exception` izi sınırsız ve CLI'da WARNING düzeyinde stderr'e basılır; kural istisna mesajı kullanıcı kodu parçası içerebilir (§12) — iz DEBUG'a ya da kısaltılmış mesaja alınabilir. `captured_logs` teardown'u önceki yapılandırmayı değil varsayılanı geri yükler.~~ → Faz 31.
- ~~Faz 21: `file_value_types` ad çakışması (`struct Hit` + başka ad alanında `class Hit`) nadir yanlış negatif; yalnız arayüzden türeyen `class A : IFoo` sıcak sayılır (muhafazakâr).~~ → **BİLİNÇLİ (2026-10-20): çözüm ad alanı/`using` çözümlemesi ister; belirsizlikte struct'ı "heap ayırma" diye raporlamak yanlış öneri olurdu (precision öncelikli, Faz 35/39); nadir.**
- ~~Faz 21'den kalan işler Faz 32'de kısmen kapandı: C-MEM-001 aynı dosyadaki kullanıcı fonksiyonu, UE-GC-001 `TArray` alanları ve CS-PERF-001 `IList` çözüldü. ~~C-MEM-003 akış duyarlılığı~~ (Faz 57'de çözüldü). Açık: döngüde `std::string +`/C# `string +=` karesel ipucu (Sonraya).~~ → **KAPANDI: Faz 32 `_accumulations` — döngüde `s += x` (C#) / `s = s + x` (C++) `n^2` ipucu verir (2026-10-20 canlı denendi).**
- ~~Faz 16: eval veri setine Python/HTML/CSS örnekleri ve ölçüm~~ → Faz 18'de yapıldı.
- ~~Faz 18: Tier 0 `</div>` kör noktası~~ → Faz 20'de HTML-STD-003 ile bulgu olarak.
- ~~Faz 20: HTML-STD-003 kaçırmaları (Faz 56): dosya sonunda bitmemiş `<div`, `<p><span>a<div>`, DOCTYPE'sız belgede `table`/`p`, aynı satırdaki farklı ihlaller, katalog açıklaması.~~ → Faz 56'da çözüldü.
- ~~HTML-STD-003: adoption agency (biçimlendirme öğesi yeniden kurulumu), foster parenting ve `form`/`button` kapsam ayrıntıları modellenmiyor (Faz 56 bilinen sınır).~~ → **BİLİNÇLİ (2026-10-20): HTML ayrıştırma algoritmasının köşe kuralları; öğretim kodunda nadir, yanlış pozitif riski yüksek (Faz 56 kararı).**
- ~~Kural motoru: bulgu sayısına üst sınır yok (600 satırlık kötü niyetli girdi 600 bulgu üretip prompt'a gidebilir).~~ → Faz 31.
- ~~Faz 18: `codementor eval check-drafts` Windows konsolunda (cp1254) çöküyor~~ → Faz 27 (konsol UTF-8).
- ~~Faz 18: eski veri seti etiketlerine Faz 17 bulguları (`c-008` 4. satır `memory_safety` C-MEM-003, `csharp-009` 11. satır `garbage_collection` CS-ALLOC-002) eklenmeli mi? (test etiketleri de etkilenebilir; kullanıcı kararı)~~ → **KAPANDI (2026-10-20):** iki etiket de Faz 21'de eklenmiş (`label.yaml` notu "Faz 21: Faz 17 kuralı"); madde bayattı.
- ~~Faz 18: HTML precision (%22) için işaretleme prompt'unda bulgu ölçütü ("iyi uygulama önerisi" ile "sorun" ayrımı); kategori tanımları (`design` vs `edge_case`). Ayar yalnız dev'de yapılmalı.~~ → **KAPANDI (2026-10-21, ölçüldü, değişiklik gerekmedi):** canlı dev 96'da HTML precision 10/13 (%77); "sorun" ölçütü Faz 22B'de, öneri/hata ayrımı Faz 36'da geldi.
- ~~Faz 18: `eval breakdown` tablosuna gecikme/token sütunları; `breakdown` etiketleri koşu anındaki değil güncel veri setinden alıyor.~~ → **KAPANDI: gecikme/token sütunları var; etiket uyumsuzluğu iş 7 `dataset_version` uyarısıyla — 2026-10-20 doğrulandı.**
- ~~Faz 16: HTML etiket dengesi denetimi~~ → Faz 20 (statik kural).
- ~~Faz 16: Python için few-shot örnekleri; JS (tarayıcı) desteği HTML ile birlikte istenebilir.~~ → **KAPANDI: Python few-shot'ları var (`python_none_*`); JS desteği yeni dil özelliği, kapsam dışı — 2026-10-20.**
- ~~Faz 15: Bağlantılar'da Ollama modelini indirme (`ollama pull`) düğmesi ve ilerleme göstergesi.~~ → **KAPANDI: Faz F (F10) `ollama pull` düğmesi + iptal — 2026-10-20 doğrulandı.**
- ~~Faz 15: Masaüstü tercihleri ile `codementor.toml` arasında "toml'a yaz" seçeneği.~~ → Faz 24
- ~~Faz 14: exe imzası yok; Windows SmartScreen ilk açılışta uyarabilir (kod imzalama sertifikası + Inno Setup kurulum paketi).~~ → **BİLİNÇLİ (2026-10-20): kod imzalama sertifikası ücretli; README SmartScreen uyarısını anlatıyor, release SHA256SUMS veriyor.**
- ~~Faz 14: CI'da Windows exe derleme işi (artefakt olarak zip); şu an elle `make exe`.~~ → Faz 23
- ~~Faz 14: analiz iptali yok~~ → Faz 19'da yapıldı.
- ~~Faz 19: Tier 1 derleyici/çalıştırma sürecine iptal olayı iletilmiyor~~ → Faz 24 (durdurulan analizde Tier 1 kendi zaman aşımına kadar sürebilir; arayüz bu sırada yeni analizi bildirimle reddeder).
- ~~Faz 14: editörde arama (Ctrl+F), son dosyalar menüsü, sürükle-bırak ile dosya açma (tkinterdnd2).~~ → Faz 24
- ~~Faz 14: onefile açılışı arşiv çözme nedeniyle birkaç saniye; hızlı açılış için onedir zip önerilir.~~ → **KAPANDI: release onedir zip'i de yayımlıyor — 2026-10-20 doğrulandı.**
- ~~Faz 5/6 öncesi: tree-sitter ayrıştırmasına süre sınırı; 40 KB girdide yüzlerce ms ölçülmüştü.~~ → Faz 55'te kapatıldı (ADR-0024): süreç içi iptal 0.25.2'de kullanılamıyor; boyut/eşzamanlılık sınırları + gerileme testiyle idare, C# gramer yavaşlaması kabul edildi.
- ~~Tier 0: kapanmamış blok varken dosya sonuna uzanan ERROR düğümleri özete dönüşüyor; bağımsız gerçek hata ayrıca raporlanmayabilir (D2; Faz 55).~~ → Faz 55'te çözüldü (`trailing_semicolon_gap`).
- ~~`mask_non_code` C++ raw string (`R"(...)"`) içindeki tırnak/yorum/ayraçları doğru maskelemiyor (Faz 55).~~ → Faz 55'te çözüldü (delimiter sınırlı maskeleme).
- ~~C# 11 raw string (`"""…"""`) maskelemesi (Faz 55'te kapsam dışı bırakıldı).~~ → Faz H3'te yapıldı (`mask_non_code(text, language)`; `$`/`$$` önekleri ve kapanış tırnağı dizisi dahil).
- ~~`mask_non_code` bir `language` parametresi aldı (Faz H3, C# 11 ham metni için) ama C++ ham metni yolu bilinçli olarak dilden bağımsız kaldı: Python/C# dosyasındaki `R"(…)` görünümü ham metin sayılıp içeriği maskelenir. Etkisi yalnızca `using_std`/`using_linq` sinyalleriyle sınırlı (Python'da kullanılmıyor); C++ yolunu dille sınırlamak gerekirse `language is Language.CPP` koşulu eklenir.~~ → **KAPANDI (2026-10-20): C++ ham metin yolu yalnız C++ ve dil bilinmezken (`59202d6`).**
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
- ~~`test_toolchain_install.py` tam koşuda bir kez 4 testle aralıklı düştü (Faz 57); tek başına yeşil. Tekrarlarsa paylaşılan geçici dizin/yarış incelenmeli. → Faz 58'de çözüldü (Windows tarayıcı kilidi; `_rename` yeniden denemesi).~~ → **KAPANDI: Faz 58 (`_rename` yeniden denemesi).**
- ~~C-MEM-001: aynı dosyadaki kullanıcı fonksiyonuna geçirilen işaretçi (`print_arr(arr, n)`) sahiplik aktarımı sayılıyor (sık kaçırma)~~ → **KAPANDI (Faz 32 + iş 5 dilim 2, 2026-10-18):** aynı dosyada tanımlı okuyucu yardımcıya vermek kaçış sayılmıyor (`_borrowers`) ve ödünç artık **zincir boyunca** yayılıyor (`_MAX_BORROW_ROUNDS = 8` sabit noktası; `positive/passed_to_reader_chain.c`, `test_c_memory_flow.py`). Bilinçli sınırlar (kaçırma): aynı değişkene iki kez `malloc`, gölgeleme, `realloc`, yalnız bildirimli/çift adlı yardımcı ve işaretçiyi döndüren/saklayan yardımcı.
- ~~UNITY-GC-001: dosyada tanımlı kullanıcı `struct`'ı için `new Hit(3)` yanlış bulgu (değer tipi)~~ → **KAPANDI (Faz 21 + iş 5 dilim 3, 2026-10-18):** `analysis/_memory.py` `file_value_types` dosyadaki `struct`/`record struct` adlarını topluyor (fixture `negative/user_struct_new.cs`, `negative/value_types_in_update.cs`); dosyada tanımlı **sınıf** için bulgu sürüyor. Ayrıca closure bastırması satır bazlı olmaktan çıktı (bkz. üstteki Faz 17 satırı).
- ~~UE-GC-001: `TArray<AActor*>`/`TMap<..., UObject*>` kapsayıcı alanları kaçırılıyor; UCLASS olmayan sınıfta (`FPlain`) öneri `UPROPERTY` değil `TStrongObjectPtr`/`FGCObject` olmalı~~ → **KAPANDI (Faz 32 + iş 5 dilim 4, 2026-10-18):** tek katman Faz 32'de gelmişti; **iç içe** kapsayıcı (`TMap<FName, TArray<UObject*>>`) da sayılıyor (`_MAX_CONTAINER_DEPTH = 2`, `type_descriptor` açılıyor). `TWeakObjectPtr`/`TSoftObjectPtr`/`TStrongObjectPtr` kapsam dışı (`negative/gc_safe_wrappers.h`); UCLASS/USTRUCT olmayan tipte soru `_UNREFLECTED` metnini kullanıyor.
- ~~CS-PERF-001: `IList`/`IReadOnlyList`/`ICollection` tipli değişkenler maliyet tablosunda çözülmüyor (kaçırma).~~ → Faz H2: `IList` → `List.Contains` (Faz 21), `IReadOnlyList.Contains` → `Enumerable.Contains` (LINQ) düzeltildi; `ICollection` bilinçli kaçırma (örnek metot).
- ~~Kural motoru: çöken kuralın istisna izi loglanmıyor; structlog (Faz 10) ile `log.exception` eklenmeli.~~ → Faz 21/31.
- ~~Sıcak yol tespiti sınıf tabanını (MonoBehaviour / UCLASS) da denetlemeli (Faz 5 olgusu).~~ → **BİLİNÇLİ (2026-10-20): Faz 21 `engine_inert_members` tabanı olmayan tipleri eler; tabanı denetlemek kullanıcının kendi `MonoBehaviour` türevi tabanında yanlış negatif üretir (yorumda gerekçesi var).**
- ~~Faz 7: OpenAI katı modu bugün `maxLength`, `maxItems`, `pattern`, `minimum`, `maximum` destekliyor; `SchemaAdapter` kısıt temizliğini sağlayıcıya göre ayırabilir (şu an hepsi çıkarılıyor, K5 doğruluyor).~~ → **GEÇERSİZ: OpenAI kaldırıldı (ADR-0021) — 2026-10-20.**
- ~~Faz 7: `ProviderResult`'a yanıt veren sağlayıcının yeteneği (şema zorlandı mı) eklenebilir; fallback sonrası K5 için.~~ → **KAPANDI: Faz G7 `ProviderResult.schema_enforced` — 2026-10-20 doğrulandı.**
- ~~Faz 7: `FakeReply` bir dataclass olarak `providers/fake.py`'de (Pydantic şeması değil, test düzeneği); gerekirse `models/`'e taşınabilir.~~ → **BİLİNÇLİ (2026-10-20): test düzeneği, şema değil; `models/` yalnız şemalar için (AGENTS.md).**
- ~~Faz 7: token tahmini ve `pricing.yaml` maliyet tahmini (mimari §13)~~ → Faz 25.
- ~~Faz 4 `run_process` çıplak `argv[0]`~~ → çözüldü (2026-09-29): yalnızca mutlak yol, `test_bare_or_relative_executable_rejected`.
- ~~CLI ajanları: gerçek `run_process` ile uçtan uca test~~ → Faz 25; agy canlı doğrulaması hâlâ açık (oturum var).
- ~~Faz 8: `call_costs.yaml`'a C# `RemoveAll`/`RemoveAt(0)`/`Insert(0, …)` maliyetleri (golden'da `Remove: O(1)` ipucu).~~ → `RemoveAll`/`RemoveAt`/`Insert` tabloda `n` idi (Faz 21); Faz H3'te argümana duyarlı ayrım eklendi: `RemoveAt(xs.Count - 1)` → `1`, `Insert(xs.Count, …)` → `1*`.
- ~~Faz 8 denetim D3 (`&lt;` kanıtı)~~ → Faz 9'da çözüldü (`normalize_evidence`).
- ~~Faz 8 denetim D2: `prompt_version` her build'de şablon dosyalarını okuyor~~ → Faz 26.
- ~~Faz 8 denetim D8: ~~`prompts.dir`~~ Faz 23'te çözüldü; demo'nun golden dizini (`tests/golden/prompts`, geliştirici aracı) hâlâ çalışma dizinine göre.~~ → **KAPANDI (2026-10-20): demo `GOLDEN_DIR` depo kökünden (`216d92e`).**
- ~~Faz 8: prompt'ların `claude_cli` ile canlı karşılaştırması (analysis vs single_pass) Faz 12 eval'inde; token tahmininin gerçek `usage` ile kalibrasyonu.~~ → **KAPANDI (2026-10-21):** two_pass/single_pass karşılaştırması README dev tablosunda (Faz 12). Kalibrasyon: Geçiş A tahmini gerçek girdinin ~yarısıydı (medyan 0,48; onarımsız 53 örnekte gerçek ≈ 1,64 × tahmin + 1379, r = 0,998) → `CHARS_PER_TOKEN` 3 → 2 (ADR-0033).
- ~~Faz 9: sızıntı korumasını `reasoning_steps` ve LLM açıklamalarına genişletmek~~ → Faz 10'da yapıldı.
- ~~Faz 9: `guiding_questions` öğelerine şemada `max_length`~~ → Faz 27.
- ~~Faz 10: `prompt_version` mtime önbelleği~~ → Faz 26.
- ~~Faz 10: CLI ilerleme göstergesi yalnızca aşama adını gösteriyor; token/süre canlı gösterilebilir.~~ → Faz 33.
- ~~Faz 11: senkron aşamaları `asyncio.to_thread`'e taşımak~~ → Faz 24 (Tier 1) + Faz 26 (Tier 0, olgular); SQLite Sonraya.
- ~~Faz 11: API anahtarı / hız sınırlama (§12); yerel olmayan bağlamada zorunlu kılınabilir. (Faz 13 kararı: v1'de yok, README Sınırlamalar.)~~ → **KAPANDI: Faz E `api.api_key` + IP başına hız sınırı — 2026-10-20 doğrulandı.**
- ~~CLI ajanı iptali~~ → Faz 19'da yapıldı.
- ~~Faz 5 hatası (csharp-011): `foreach` koleksiyon ifadesindeki çağrı döngü içinde sayılıyordu → `high` O(n²)~~ → çözüldü (2026-09-30, kullanıcı isteğiyle Faz 12 içinde): `_context.contexts` döngü başlığında bir kez değerlendirilen alanlara (`initializer`, `right`: C `for` başlatıcısı, C++ range-for, C# `foreach`) dış bağlamı verir; `tests/fixtures/complexity/on_{foreach_header_call,range_for_header_call,for_initializer_strlen}` + koşuldaki `strlen` için `on2_strlen_condition`. Dev static-only Big-O %88 → %92.
- ~~Çağrı maliyeti tablosu eksikleri (eval notları): `std::memset`/`memcpy` (n), `UGameplayStatics::GetAllActorsOfClass` (n), `TArray::Remove` (n); `std::string operator+` / C# `string +=` döngüde karesel (şu an n).~~ → **KAPANDI: `memset`/`memcpy`/`GetAllActorsOfClass`/`TArray::Remove` `call_costs.yaml`'da; string birikimi Faz 32 — 2026-10-20 doğrulandı.**
- ~~Faz 12: eval'e `guard_interventions` metriği~~ → Faz 22 Aşama A.
- ~~Faz 12: `eval analyze` aracı (kategorisiz eşleşme, önem filtreli precision, örnek bazında FP/FN); `compare` statik satırında injection direncini "—" göstermeli.~~ → Faz 22A / Faz 31.
- ~~Faz 12: precision iyileştirme — `design` bulgularını yalnızca soru gereksinimi varken üretmek, `low` bulguları raporda ayrı göstermek; kategori belirsizliği (sıfıra bölme `edge_case`/`undefined_behavior`, null `edge_case`/`memory_safety`) için prompt'ta kategori tanımları. Değişiklik sonrası dev'de yeniden ölçülmeli (test artık kullanıldı).~~ → **KAPANDI (2026-10-21, ölçüldü, prompt değişmedi):** canlı dev 96 (79 / 97 / 87): `low` precision 15/18 (%83) `medium`dan (36/53, %68) yüksek → ayrı gösterim gereksiz; kategori karışıklığı 2 (Faz 51'de 7 → 2). `design` en büyük FP kaynağı (14/24), ama 23 FP'nin 14'ü doğru bir bulgunun ±1 satırında: bir kısmı aynı sorunu başka kategoriyle yineliyor (`unity-107:6`, `cpp-102:7`), bir kısmı etiket dışı olası gerçek sorun (`css-004:4` eksik medya sorgusu, `python-012:6` tekrarlı kopya). Kategori tanımı bunu çözmez → aşağıdaki madde.
- Test etiketleri sonradan eklenen kuralların bulgularını içermiyor (2026-10-21 statik test koşusu, P 94 → 86): `c-006:8`, `c-016:12` NULL denetimi, `cpp-006:3,12` elle ömür, `cpp-015:9` döngüde `s = s + x`. Kodun gerçeğine göre insan etiket incelemesi; test bölümü olduğu için prompt/kural ayarına kullanılmaz.
- Kategori-ötesi yakın yineleme (2026-10-21 ölçümünden): LLM bulgusu, aynı/komşu satırdaki statik ya da teyitli bulguyla aynı sorunu anlatıyorsa birleştirme deneyi; yalnız dev'de, birleştirme öncesi/sonrası P/R ölçülerek (kör birleştirme `css-004:4` gibi ayrı sorunları düşürür). Ayrıca `design` FP'leri için insan etiket incelemesi (`css-004`, `python-012`, `cpp-009`, `unity-106`, `unreal-104`).
- ~~Faz 12: few-shot 0/1 ablasyonu (§14.4) koşulmadı. → Faz 34.~~ → **KAPANDI: Faz 34.**
- ~~CI Windows işi (2026-09-30): `windows-latest`'te g++ (MinGW) ilk derlemede 10 sn sınırını aşıyor (`test_cpp_type_error_failed` → `timeout`); clang++ varsayılan MSVC hedefli olduğundan Unreal stub denetimi `tool_error` ile atlanıyor (2 test). Ürün zarif atlıyor ama Windows'ta clang için `--target=x86_64-w64-mingw32` / başlık yolu ve soğuk başlangıç süresi ele alınmalı; o zamana kadar Windows CI `-m "not live and not compiler"`.~~ → **KAPANDI (2026-10-20): `-m "not live"` ile Windows CI denendi (g++ 15.2, clang 20.1; 4031 geçti, zig/Roslyn araç yokluğundan atlandı); `ci.yml` Windows adımı derleyici testlerini artık dışlamıyor.**
- ~~Faz 13: README için GIF demo~~ → Faz 26 (Pillow).
- ~~Faz 13: Web UI'da indirme, sağlayıcı ve mod seçimi~~ → Faz 26.
- ~~Faz 13: Monaco'yu tembel yükleme~~ → Faz 26.
- ~~Faz 13: `YAPILANLAR.md`'ye Faz 8–12 özetleri~~ → Faz 26.
- ~~Faz F (F8 denetimi): `desktop/connections.py` 402 satır (> 400, AGENTS.md)~~ → F12'de oturum açma akışı `desktop/login.py`'ye çıkarılınca **366 satıra** indi (400 satır kuralı sağlanıyor); `KeyStore`/katalog taşıma önerisi gereksiz kaldı.
- ~~Faz F (F11 kapsamı): `history_controller.open_history` kaydı hâlâ ana iş parçacığında okuyor (`get_analysis`/`get_row` + `runtime.load_source`) ve diskten kod yüklüyor; F11 yalnız liste/silme/temizleme ile sınırlı tutuldu, kayıt açmayı da arka plana almak Sonraya.~~ → **KAPANDI (2026-10-20): `open_history` de arka planda (`20a1eb1`).**
- tree-sitter 0.26 uyumu — **upstream bekleniyor (kök neden bulundu, 2026-10-20):** py-tree-sitter 0.26.0'da `Point` referans sayımı fazla düşürülüyor (tree-sitter/py-tree-sitter#472; düzeltme ana dalda, 0.26.1 yayımlanmadı — #500). Bizde `node.start_point.row` erişimiyle tetikleniyor (Windows 0xC0000005, Linux segfault; `test_parsers.py::test_tree_sitter_binding_is_memory_safe` yakalıyor). Kaldırma koşulu: 0.26.1+ yayımlanınca `pyproject` sınırı ve `dependabot.yml` ignore kaldırılır, bu sonda testi yeşil olmalı. Geçici çözüm (tüm `start_point` kullanımını yeniden yazmak) değmez.
- ~~Faz F (F12): macOS'ta `open -a Terminal <cli>` ek argümanları (ör. `claude auth login`) Terminal uygulamasına geçirmez; `osascript -e 'tell application "Terminal" to do script "…"'` ile argümanlı sürüm Sonraya (şimdilik CLI argümansız açılıp kendi oturum açma akışını başlatıyor).~~ → **KAPANDI (2026-10-20): `osascript` ile argümanlı komut (`e2cda35`); gerçek macOS denemesi KALAN_ISLER U5.**
