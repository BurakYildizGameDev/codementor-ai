# CodeMentor AI

**Kodu düzeltmeyen, denetleyip Sokratik sorular soran kod mentorluk motoru.** C, C++, C#
(Unity, Unreal), Python, HTML ve CSS kodunu statik analiz (tree-sitter + deterministik kurallar + isteğe bağlı yerel
derleyici) ve bir LLM ile birlikte inceler. Çözümü vermez; öğrenciyi sorunu kendisinin
bulmasına yönelten sorular ve kademeli ipuçları üretir.

![Masaüstü uygulaması: işaretli bulgu satırları, analiz akışı, Sokratik mentor kartı](docs/img/desktop-live.png)

<sub>Masaüstü uygulamasında gerçek bir analiz (claude_cli, `claude-opus-5-5`, 34.5 sn): bellek
sızıntısı ve sıfıra bölme satırları yüksek, 8. satır orta önemde işaretli; mentor cevabı değil
soruyu veriyor. Web arayüzü: [docs/img/web-live.png](docs/img/web-live.png).</sub>

## Neden?

- **Çözüm yerine soru.** LLM çıktısı doğrudan öğrenciye gitmez: bulgular satır kanıtıyla
  doğrulanır, Sokratik sorular bir sızıntı korumasından geçer. Sızıntı eval'de ölçülür.
- **Deterministik temel.** Sözdizimi hataları, bilinen bellek/GC/motor hataları ve karmaşıklık
  ipucu LLM'e gitmeden statik olarak bulunur. LLM yanıt vermezse rapor yine döner
  (`meta.degraded`).
- **Ölçülmüş iddialar.** 80 elle etiketlenmiş örnekle dev/test ayrımlı eval; aşağıdaki tablolar
  `eval/results/` dosyalarından üretilir.

## Nasıl çalışır?

```mermaid
flowchart LR
    A[Kod + dil/motor + soru] --> K0[K0 Giriş<br/>normalize, dil tespiti]
    K0 --> K1[K1 Ön doğrulama<br/>Tier 0 tree-sitter<br/>Tier 1 yerel derleyici]
    K1 -- sözdizimi hatası --> EE[Erken çıkış<br/>LLM çağrısı yok]
    K1 --> K2[K2 Statik analiz<br/>olgular, Big-O ipucu, kurallar]
    K2 --> K3[K3 Prompt<br/>numaralı kod, olgular, kontrol listesi]
    K3 --> A1[Geçiş A: analiz<br/>Big-O + gerekçe + ek bulgular]
    A1 --> V1[K5 Doğrulama<br/>şema, satır kanıtı, ipucu uyumu]
    V1 --> B1[Geçiş B: mentorluk<br/>Sokratik sorular]
    B1 --> V2[Sızıntı koruması]
    V2 --> K6[K6 Rapor<br/>JSON · Markdown · SARIF · Web]
    EE --> K6
```

Ayrıntı: [docs/mimari.md](docs/mimari.md). Kararlar: [docs/adr/](docs/adr/).

## Masaüstü uygulaması (Windows .exe)

`CodeMentor.exe`'yi çift tıkla açman yeterli: Python, Node.js ya da tarayıcı gerekmez
(ADR-0013). Gereken tek şey bir LLM sağlayıcısı; varsayılan, oturum açılmış
[Claude Code](https://claude.com/claude-code) CLI'ı (`claude` PATH'te olmalı). Sol alttaki rozet
sağlayıcının hazır olup olmadığını gösterir.

- **Analiz:** kodu yaz, aç (`.c .h .cpp .hpp .cs .py .html .css`) ya da örnek yükle; dil/motor seç, isteğe bağlı
  bir görev seç, **Denetle** (Ctrl+Enter). Analiz akışı 6 adımda canlı izlenir; bulgu satırları
  editörde önem rengiyle boyanır, karta tıklayınca satıra gidilir.
- **Sokratik mentor:** ana kavram, yönlendirici sorular ve sonraki adım. **Bir ipucu daha**
  aynı oturumla yeniden denetler ve ipucu seviyesini (1→3) artırır; **Baştan başla** sıfırlar.
- **Soru bankası:** 18 görev (C, C++, C#, Unity, Unreal, Python, HTML, CSS); seçilen görev
  editörün üstünde hedefiyle görünür.
- **Geçmiş:** önceki analizler kodlarıyla yeniden açılır; raporlar Markdown/SARIF/JSON olarak
  dışa aktarılır.
- **Bağlantılar:** Claude Code, Antigravity (agy), Ollama, Anthropic, OpenAI ve DeepSeek için
  birer kart. Model seçimi (Ollama'da kurulu modeller, agy'de hesabındaki modeller listelenir),
  **Oturum aç** (CLI'nın kendi girişini yeni pencerede açar), API anahtarı (Windows Kimlik
  Bilgisi Yöneticisi'nde saklanır, dosyaya yazılmaz), **Bağlantıyı dene** ve **Varsayılan yap**.
  Analiz ekranındaki rozet hangi model ile çalıştığını gösterir (ADR-0014).

Derlemek için (Windows, depo kökünde):

```bash
uv sync
uv run python build_exe.py --both    # dist/CodeMentor.exe (~37 MB) + dist/CodeMentor-0.1.0-win64.zip
uv run python -m codementor.desktop  # derlemeden çalıştırmak için
```

Sağlayıcı ve model ayarlarını **Bağlantılar** ekranından yaparsın; ileri ayarlar için exe'nin
yanına bir `codementor.toml` koyarsan paketteki varsayılan yerine o kullanılır. Veritabanı, tercihler ve log `~/.codementor`
altındadır. Hazır exe ve zip, GitHub Actions'taki her `main` koşusunda `CodeMentor-win64`
artefaktı olarak indirilebilir.

Yapılandırmadaki göreli yollar çalışma dizinine bağlı değildir: `codementor.toml`'daki yol
toml'un bulunduğu dizine, varsayılanlar paketin kendi `data/` ve `prompts/` dizinlerine göre
çözülür (ADR-0016). Bu yüzden `codementor` komutu her dizinden çalışır.

## Hızlı başlangıç (Docker gerekmez)

Gerekenler: Python 3.12 + [uv](https://docs.astral.sh/uv/), Node.js 20+ ve bir LLM sağlayıcısı
(varsayılan: oturum açılmış [Claude Code](https://claude.com/claude-code) CLI'ı, `claude`).
İsteğe bağlı: gcc/clang (C/C++/Unreal Tier 1) ve .NET SDK (C# Tier 1, `make roslyn-check`).
Derleyici yoksa Tier 1 atlanır, analiz yine çalışır.

```bash
git clone https://github.com/BurakYildizGameDev/codementor-ai.git
cd codementor-ai
uv sync
uv run codementor serve            # API: http://127.0.0.1:8000/docs

# ikinci terminalde
cd web
npm install
npm run dev                        # arayüz: http://127.0.0.1:5173
```

Hazırlık denetimi: `curl http://127.0.0.1:8000/health/ready` (sağlayıcı ve bulunan derleyiciler).
Komutlar depo kökünden çalıştırılmalı (`data/` ve `codementor.toml` göreli yollarla okunur).

Komut satırından:

```bash
uv run codementor analyze kod.c                       # Rich panel
uv run codementor analyze kod.cs --engine unity --format sarif --out rapor.sarif
uv run codementor questions list
```

### Sağlayıcılar

`codementor.toml` içinde `[providers] default = "..."`. Model adları yalnızca yapılandırmada
tutulur (ADR-0008).

| Sağlayıcı | Kurulum | Not |
|---|---|---|
| `claude_cli` (varsayılan) | `claude` CLI'ında oturum aç | API anahtarı gerekmez; araçları kapalı, prompt stdin'den (ADR-0012). Eval bununla ölçüldü. |
| `anthropic` | `ANTHROPIC_API_KEY`, `[providers.anthropic] model` | Yapılandırılmış çıktı (ADR-0011) |
| `ollama` (yerel) | [Ollama](https://ollama.com) kur, `ollama pull qwen2.5-coder:7b`, `default = "ollama"` | Tamamen çevrimdışı; kalite modele bağlı, **eval'de ölçülmedi** |
| `openai`, `deepseek` | `OPENAI_API_KEY` / `DEEPSEEK_API_KEY` ve model adı | Eval'de ölçülmedi |

## Eval sonuçları

80 elle etiketlenmiş örnek (her dil/motor 16; %25 sözdizimi hatalı, %12,5 prompt injection),
dev 31 / test 49. Prompt'lar dev'de **ayarlanmadı**; test bölümü en sonda **bir kez** koşuldu.
Bulgu eşleşmesi: aynı kategori + satır farkı ≤ 2. Model: `claude-opus-5-5` (`claude_cli`),
önbellek kapalı.

> Not (Faz 21): "Yalnızca statik" satırları güncel kurallarla ve Faz 21'de iki bulgu eklenmiş
> dev etiketleriyle yeniden koşuldu; LLM satırları Faz 12'deki kurallar ve etiketlerle hesaplandı
> (yeniden koşulmadı). Satırlar bu yüzden tam karşılaştırılabilir değil; ayrıntı
> `docs/eval-findings.md` §5.

**Test (49 örnek):**

<!-- eval-table:test:start -->
| Koşu | Mod | Ablasyon | Örnek | Şema (ilk / onarım sonrası) | Erken çıkış P / R | Big-O birebir / sınıf | Denetim P / R / F1 | Satır doğruluğu | Sızıntı | Injection direnci | p50 / p95 (sn) | Token ort. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude_cli / claude-opus-5-5 | two_pass | — | 49 (test) | 100% / 100% | 100% / 100% | 91% / 94% | 27% / 92% / 42% | 94% | 0% | 100% | 20.3 / 57.3 | 15673 |
| claude_cli / claude-opus-5-5 | single_pass | — | 49 (test) | 100% / 100% | 100% / 100% | 94% / 97% | 32% / 94% / 48% | 94% | 0% | 100% | 13.5 / 35.7 | 10182 |
| Yalnızca statik (LLM yok) | static | — | 49 (test) | — / — | 100% / 100% | 91% / 91% | 89% / 46% / 61% | 100% | 0% | 0% | 0.0 / 0.1 | — |

Sürümler: prompt v1+e485058f · kurallar r1+fa6fff47 · şema 1.0
Sürümler: prompt v1+fbc08625 · kurallar r1+d3065584 · şema 1.0
<!-- eval-table:test:end -->

> Not: `c-016` etiketine 2026-10-01'de ikinci beklenen bulgu (`memory_safety`, C-MEM-003) eklendi; LLM satırları eski etiketle puanlandı.

**Dev (31 örnek) ve ablasyonlar:**

<!-- eval-table:dev:start -->
| Koşu | Mod | Ablasyon | Örnek | Şema (ilk / onarım sonrası) | Erken çıkış P / R | Big-O birebir / sınıf | Denetim P / R / F1 | Satır doğruluğu | Sızıntı | Injection direnci | p50 / p95 (sn) | Token ort. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude_cli / claude-opus-5-5 | two_pass | — | 31 (dev) | 100% / 100% | 100% / 100% | 96% / 96% | 27% / 92% / 42% | 100% | 0% | 100% | 23.5 / 40.0 | 14219 |
| claude_cli / claude-opus-5-5 | single_pass | — | 31 (dev) | 100% / 100% | 100% / 100% | 92% / 92% | 32% / 96% / 47% | 96% | 0% | 100% | 13.1 / 24.5 | 9359 |
| claude_cli / claude-opus-5-5 | two_pass | facts | 31 (dev) | 100% / 100% | 100% / 100% | 85% / 92% | 28% / 100% / 43% | 96% | 0% | 100% | 20.5 / 42.3 | 13227 |
| claude_cli / claude-opus-5-5 | two_pass | line_numbers | 31 (dev) | 100% / 100% | 100% / 100% | 92% / 92% | 28% / 100% / 44% | 96% | 0% | 100% | 20.4 / 41.3 | 13861 |
| Yalnızca statik (LLM yok) | static | — | 31 (dev) | — / — | 100% / 100% | 96% / 96% | 100% / 50% / 67% | 100% | 0% | 0% | 0.0 / 0.1 | — |

Sürümler: prompt v1+e485058f · kurallar r1+fa6fff47 · şema 1.0
Sürümler: prompt v1+fbc08625 · kurallar r1+d3065584 · şema 1.0
<!-- eval-table:dev:end -->

**Python, HTML, CSS (Faz 18, 36 örnek; dil başına 12):** test 21 / dev 15, yalnızca bu dillerde koşuldu (`eval run --language`). Dil başına döküm ve yorum: `docs/eval-findings.md` §4.

<!-- eval-table:test-diller:start -->
| Koşu | Mod | Ablasyon | Örnek | Şema (ilk / onarım sonrası) | Erken çıkış P / R | Big-O birebir / sınıf | Denetim P / R / F1 | Satır doğruluğu | Sızıntı | Injection direnci | p50 / p95 (sn) | Token ort. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Yalnızca statik (LLM yok) | static | — | 21 (test) | — / — | 100% / 100% | 100% / 100% | 100% / 67% / 80% | 100% | 0% | 0% | 0.0 / 0.0 | — |
| claude_cli / claude-opus-5-5 | two_pass | — | 21 (test) | 100% / 100% | 100% / 100% | 100% / 100% | 33% / 81% / 47% | 100% | 0% | 100% | 16.5 / 36.5 | 9665 |
| claude_cli / claude-opus-5-5 | single_pass | — | 21 (test) | 100% / 100% | 100% / 100% | 100% / 100% | 34% / 86% / 49% | 100% | 0% | 100% | 14.1 / 23.4 | 7328 |

Sürümler: prompt v1+e485058f · kurallar r1+286dfb2f · şema 1.0
<!-- eval-table:test-diller:end -->

<!-- eval-table:dev-diller:start -->
| Koşu | Mod | Ablasyon | Örnek | Şema (ilk / onarım sonrası) | Erken çıkış P / R | Big-O birebir / sınıf | Denetim P / R / F1 | Satır doğruluğu | Sızıntı | Injection direnci | p50 / p95 (sn) | Token ort. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Yalnızca statik (LLM yok) | static | — | 15 (dev) | — / — | 100% / 100% | 100% / 100% | 100% / 55% / 71% | 100% | 0% | 0% | 0.0 / 0.0 | — |
| claude_cli / claude-opus-5-5 | two_pass | — | 15 (dev) | 100% / 100% | 100% / 100% | 100% / 100% | 54% / 95% / 69% | 89% | 0% | 100% | 16.2 / 34.2 | 9530 |

Sürümler: prompt v1+e485058f · kurallar r1+286dfb2f · şema 1.0
<!-- eval-table:dev-diller:end -->

Tablolar `uv run codementor eval compare eval/results/*_test.json` (ve `*_dev.json`) çıktısıdır;
`tests/unit/eval/test_readme_table.py` sonuç dosyalarıyla birebir olduklarını denetler.
"Yalnızca statik" satırındaki injection direnci anlamsızdır (LLM çağrılmaz).

Okuma notları (ayrıntı: [docs/eval-findings.md](docs/eval-findings.md)):

- **LLM'in katkısı recall'da:** statik kurallar beklenen bulguların %42'sini (test) kesin doğrulukla
  bulur; LLM ile %92–94. Kategori yok sayıldığında LLM test'teki 36 bulgunun 36'sını buluyor.
- **Precision düşük (%27–32):** LLM etiketlenmemiş küçük gözlemler de ekliyor (`edge_case`,
  `design`, `input_handling`). Orta ve üstü önemde %35–37.
- **Statik olgular Big-O'ya katkı veriyor:** olgular prompt'tan çıkarılınca dev'de birebir doğruluk
  %96 → %85.
- **Erken çıkış:** test'teki 49 örneğin 15'i (%31) LLM çağrılmadan yanıtlandı; erken çıkış
  kararlarının precision ve recall'u %100.
- **two_pass vs single_pass:** kalite farkı ölçülmedi; single_pass ~%35–45 daha hızlı ama sızıntı
  koruması ~1,5 kat daha sık devreye giriyor. Varsayılan two_pass (ADR-0003).

## Sınırlamalar

- **Unreal yalnızca stub başlıkla derlenir** (`data/stubs/ue_stubs.h`). Motor başlıkları olmadan
  tam derleme yapılamaz; stub kaynaklı hatalar uyarıya düşürülür (ADR-0007). C#/Unity'de Tier 1
  yalnızca Roslyn sözdizimi ayrıştırmasıdır; tür/anlam denetimi ve Unity motor derlemesi yok.
- **Tier 1 derleyici isteğe bağlıdır.** gcc/clang/.NET yoksa yalnızca tree-sitter denetimi yapılır.
  Windows'ta clang varsayılan olarak MSVC hedefler; Unreal stub denetimi atlanabilir.
- **Kod çalıştırılmaz** (ADR-0005): Big-O statik ipucu + LLM gerekçesidir, ölçülmüş çalışma süresi
  değildir.
- **Eval tek model ve 80 örnekle yapıldı.** Sonuçlar `claude-opus-5-5` içindir; yerel modeller
  (Ollama) ölçülmedi. Test bölümü küçük olduğundan bir örnek yaklaşık 2–3 puan eder.
- **Precision düşük:** LLM gerçek ama etiketlenmemiş küçük sorunları da raporluyor; öğrenciye çok
  sayıda düşük önemli bulgu gidebilir.
- **Sızıntı koruması sezgiseldir** (n-gram + işaret listesi). Eval'deki %0 sızıntı ölçülen işaretler
  içindir; başka biçimde sızmış bir çözümü kaçırabilir.
- **Statik kural kapsamı:** v1 planındaki 20 C ailesi kuralının 10'u + 13 Python/HTML/CSS kuralı (katalog: `codementor rules list`,
  [docs/rules-catalog.md](docs/rules-catalog.md)).
- **API'de kimlik doğrulama ve hız sınırı yok.** Varsayılan olarak yalnızca `127.0.0.1`'e bağlanır;
  başka adrese bağlanırsa `serve` uyarır. Paylaşılan sunucuda çalıştırmayın.
- **Docker paketi yok** (ADR-0009): kurulum `uv` + `npm` ile yereldir.
- **Python, HTML ve CSS eval'i küçük** (dil başına 12 örnek, Faz 18; bkz. yukarıdaki tablo):
  sızıntı %0 ve injection direnci %100, ama precision özellikle HTML'de düşük (~%22; LLM "iyi
  uygulama" önerilerini bulgu olarak raporluyor). HTML/CSS'te karmaşıklık analizi yapılmaz; HTML'de kapanmamış etiketler sözdizimi hatası sayılmaz (tarayıcılar gibi).

## Yol haritası

- **v1.1:** kalan statik kurallar; cppcheck/clang-tidy entegrasyonu; precision iyileştirmesi
  (düşük önemli bulguları ayrı göstermek); imzalı Windows kurulum paketi; LLM-as-judge ile Sokratik kalite
  puanı; yerel modellerin (Ollama) eval'i.
- **v2.0:** yalıtılmış ortamda ampirik karmaşıklık ölçümü; test senaryosu tabanlı doğruluk;
  VS Code eklentisi (SARIF + canlı analiz); Rust ve Go.

## Geliştirme

```bash
make check                         # ruff + mypy --strict + pytest (make yoksa: AGENTS.md komutları)
make test-compiler                 # yerel derleyici testleri (araç yoksa atlanır)
make web-types                     # schemas/*.schema.json → web/src/types (elle yazılmaz)
make web-test                      # tip kontrolü + Vitest + üretim derlemesi
make web-e2e                       # Playwright (API taklit edilir)
CODEMENTOR_E2E_LIVE=1 npx playwright test live   # web/ içinde; gerçek API ve sağlayıcıyla
uv run codementor eval run --split dev --provider claude_cli --mode two_pass
```

Belgeler: [mimari](docs/mimari.md) · [uygulama planı](docs/UYGULAMA_PLANI.md) ·
[eval bulguları](docs/eval-findings.md) · [kural kataloğu](docs/rules-catalog.md) ·
[ilerleme](PROGRESS.md)
