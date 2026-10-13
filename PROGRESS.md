# İlerleme Günlüğü

> Faz 0-63'ün ayrıntılı notları ve eski yol haritası arşivde: [docs/gelistirme-gunlugu/PROGRESS-faz-0-63.md](docs/gelistirme-gunlugu/PROGRESS-faz-0-63.md). Yeni fazların notları buraya eklenir (AGENTS.md faz bitirme protokolü).

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
| D | ✅ (release etiketi kullanıcıda) | faz/d-public-release | 2026-10-13 | Claude Code / — |
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
**Ertelenen (Sonraya):** `config_writer` dizi tablosunu (`[[providers.x]]`) ezer, CRLF'yi LF yazar;
`from_question` `genel` etiketini/varsayılan kısıtı düzenlemede siler; `system_errors` ağ
hatalarını "dosya işlemi" diye anar; `report/usage` → `storage.cache.UsageTotals` katman bağımlılığı;
`detect.py` `<meta …` deseni çok büyük girdide karesele yakın (40 KB'de ölçülmedi);
`guard_delimiters` `&lt;` için idempotent değil; `primary` sağlayıcı adı `getattr` ile; 400 satır:
`orchestrator.py`, `passes.py`, `desktop/app.py` (Faz G).

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
- CPP-OWN-001 akış duyarlı eşleşme: erken `return`/istisna yolunda atlanan `delete` öneri yerine hata sayılsın (Faz 52 denetimi).
- Faz 51 denetimi: `RunConfig` etiket/veri seti sürümü taşımıyor; eski koşular yeni etiketlerle sessizce yeniden puanlanabiliyor (etiket özeti `RunConfig`'e + `compare` dipnotu). Ters yön: bellek erişimi olmayan `memory_safety` etiketleri (CPP-OWN-001 çıplak `new[]`: dev `cpp-009`, `cpp-105`, test `cpp-006`) yeni tanıma uymuyor → Faz 52 (kural bazında öneri türü) ile birlikte ele alınmalı. Etiketlerde serbest metin sezgisi yerine yapısal `boundary:` alanı.
- Faz 49: `sessions` tablosu da sınırsız büyüyor (oturum başına bir satır); eski oturumları `updated_at`'e göre budamak. ~~Tier 1 derleyici sürümü önbellek imzasında yok.~~ (Faz B: araç kimliği + dosya boyutu/zamanı)
- Faz 49 denetimi O3 (**Faz B'de kısmen kapandı:** soru modeli özeti imzada; referans çözüm dosyası, `data/checklists` ve kod değişiklikleri hâlâ yok): önbellek anahtarında soru içeriği yok (`question_id` var; referans çözüm, `concept_tags`, `data/checklists` ve `pipeline/assemble.py`/`stages.py` değişince eski rapor dönebilir). Soru içeriği özeti anahtara eklenebilir.
- Faz 49 denetimi Ü9: eksik sütunlu eski şema (`OperationalError`) ve bozuk `created_at` için şema göçü yok; `list_analyses` korunmuyor.
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
- C# 11 raw string (`"""…"""`) maskelemesi (Faz 55'te kapsam dışı bırakıldı).
- `mask_non_code` dil bilgisi almıyor: Python'da `R"(…"` C++ ham metni sanılabilir (Faz 55 denetimi).
- ~~Tier 0 parse'ı sert zaman aşımıyla alt süreçte izole etmek (ADR-0024 sonucu)~~ → Faz 59'da yapıldı (ADR-0025; varsayılan kapalı).
- Tier 0 yalıtımında sıcak işçi havuzu (her analizde ~280 ms süreç açma maliyeti; yüksek yükte) (Faz 59).
- ~~`data/` dizini paket dışında; `pip install` ile dağıtımda veri dosyaları gelmez. Faz 13'te (Docker/dağıtım) `importlib.resources` veya paket verisi olarak ele alınmalı.~~ → Faz 23
- ~~Göreli veri dizinleri (`data.questions_dir`) çalışma dizinine göre çözülüyor; proje dışından çalıştırınca bulunamıyor. Config dosyasına göre çözme veya paket verisi (yukarıdaki madde) ile birlikte ele alınmalı.~~ → Faz 23
- ~~`.gitattributes` ile `* text=auto eol=lf`: Windows'taki CRLF uyarılarını ve şema dosyalarında satır sonu farklarını önler.~~ → Faz 23
- `parse_bigo` şu an `log log n`, `n^n`, `Θ(...)`/`Ω(...)`, `max(n,m)` ve `k` gibi değişken üsleri desteklemiyor; eval'de LLM çıktılarında görülürse eklenebilir.
- ~~`AnalysisReport.analysis_id` için ULID biçim doğrulaması~~ → Faz 27.
- ~~CI'a `actions/setup-dotnet` + `make roslyn-check` adımı~~ → Faz 27.
- `ue_stubs.h` genişletilebilir (`Super` için `GENERATED_BODY` yerine sınıf başına typedef mümkün değil; delegeler `OnDestroyed.AddDynamic`, `FTimerManager`); eval'de Unreal uyarı gürültüsüne göre karar verilmeli.
- ~~`validation.stub_header` / `roslyn_check_dll` göreli yolları da çalışma dizinine göre çözülüyor (veri dizinleri maddesiyle birlikte ele alınmalı).~~ → Faz 23
- `#pragma` makro genişletmeli biçimleri (`#pragma MACRO`) ve `#line` şu an serbest; derleyici kaynak okumadığı için risk düşük, ama include korumasına izin listesi eklenebilir.
- gcc kolonları "display" birimli, clang bayt; Tier 0 karakter. Unicode içeren satırlarda kolonlar farklı olabilir (`-fdiagnostics-column-unit=byte` gcc ≥ 11).
- ~~Faz 6'da ertelenen 10 statik kural~~ → Faz 17'de yapıldı (2026-10-01).
- ~~Faz 17: C-MEM-003 denetimin kullanımdan sonra yapıldığını görmüyor~~ (Faz 57'de çözüldü; yanlış dal ve koşullu koruma ayırt edilmiyor). UNITY-GC-001 closure bastırması satır bazlı.
- `test_toolchain_install.py` tam koşuda bir kez 4 testle aralıklı düştü (Faz 57); tek başına yeşil. Tekrarlarsa paylaşılan geçici dizin/yarış incelenmeli. → Faz 58'de çözüldü (Windows tarayıcı kilidi; `_rename` yeniden denemesi).
- C-MEM-001: aynı dosyadaki kullanıcı fonksiyonuna geçirilen işaretçi (`print_arr(arr, n)`) sahiplik aktarımı sayılıyor (sık kaçırma); çağrılan fonksiyon aynı dosyadaysa ve `free`/saklama yoksa bulgu verilebilir. Aynı değişkene iki kez `malloc`, gölgeleme ve `realloc` de bilinçli sınırlar.
- UNITY-GC-001: dosyada tanımlı kullanıcı `struct`'ı için `new Hit(3)` yanlış bulgu (değer tipi); Faz 5 `CSHARP_VALUE_TYPES` dosyadaki struct adlarıyla genişletilebilir.
- UE-GC-001: `TArray<AActor*>`/`TMap<..., UObject*>` kapsayıcı alanları kaçırılıyor; UCLASS olmayan sınıfta (`FPlain`) öneri `UPROPERTY` değil `TStrongObjectPtr`/`FGCObject` olmalı.
- CS-PERF-001: `IList`/`IReadOnlyList`/`ICollection` tipli değişkenler maliyet tablosunda çözülmüyor (kaçırma).
- ~~Kural motoru: çöken kuralın istisna izi loglanmıyor; structlog (Faz 10) ile `log.exception` eklenmeli.~~ → Faz 21/31.
- Sıcak yol tespiti sınıf tabanını (MonoBehaviour / UCLASS) da denetlemeli (Faz 5 olgusu).
- Faz 7: OpenAI katı modu bugün `maxLength`, `maxItems`, `pattern`, `minimum`, `maximum` destekliyor; `SchemaAdapter` kısıt temizliğini sağlayıcıya göre ayırabilir (şu an hepsi çıkarılıyor, K5 doğruluyor).
- Faz 7: `ProviderResult`'a yanıt veren sağlayıcının yeteneği (şema zorlandı mı) eklenebilir; fallback sonrası K5 için.
- Faz 7: `FakeReply` bir dataclass olarak `providers/fake.py`'de (Pydantic şeması değil, test düzeneği); gerekirse `models/`'e taşınabilir.
- ~~Faz 7: token tahmini ve `pricing.yaml` maliyet tahmini (mimari §13)~~ → Faz 25.
- ~~Faz 4 `run_process` çıplak `argv[0]`~~ → çözüldü (2026-09-29): yalnızca mutlak yol, `test_bare_or_relative_executable_rejected`.
- ~~CLI ajanları: gerçek `run_process` ile uçtan uca test~~ → Faz 25; agy canlı doğrulaması hâlâ açık (oturum var).
- Faz 8: `call_costs.yaml`'a C# `RemoveAll`/`RemoveAt(0)`/`Insert(0, …)` maliyetleri (golden'da `Remove: O(1)` ipucu).
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
