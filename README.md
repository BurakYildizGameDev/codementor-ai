<div align="center">

# CodeMentor AI

**Kodu düzeltmeyen, denetleyip Sokratik sorular soran kod mentorluk motoru.**

Statik analiz + yerel derleyici + LLM: hatayı bulur, cevabı vermez; öğrenciyi
sorunu kendisinin bulmasına yönelten sorular sorar.

[![CI](https://github.com/BurakYildizGameDev/codementor-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/BurakYildizGameDev/codementor-ai/actions/workflows/ci.yml)
![Python 3.12](https://img.shields.io/badge/python-3.12-3776AB?logo=python&logoColor=white)
![mypy strict](https://img.shields.io/badge/mypy-strict-2A6DB2)
![tests](https://img.shields.io/badge/testler-3700%2B-success)
![Docker yok](https://img.shields.io/badge/Docker-gerekmez-lightgrey)
[![Lisans: MIT](https://img.shields.io/badge/lisans-MIT-blue)](LICENSE)

C · C++ · C# · Unity · Unreal · Python · HTML · CSS

**Türkçe** · [English](README.en.md)

![Masaüstü uygulaması: işaretli bulgu satırları, analiz akışı, Sokratik mentor kartı](docs/img/desktop-live.png)

<sub>Masaüstü uygulamasında gerçek bir analiz (`claude_cli`, `claude-opus-5-5`, 34,5 sn): bellek
sızıntısı ve sıfıra bölme satırları yüksek, 8. satır orta önemde işaretli; mentor cevabı değil
soruyu veriyor. Web arayüzü: [docs/img/web-live.png](docs/img/web-live.png).</sub>

</div>

---

## Bir bakışta

| | |
|---|---|
| **Diller** | C, C++, C#, Python, HTML, CSS + Unity ve Unreal motor bağlamı |
| **Statik kurallar** | 41 deterministik kural ([katalog](docs/rules-catalog.md)) |
| **Ön doğrulama** | tree-sitter (her zaman) + gcc / clang / Roslyn (kuruluysa; yoksa tek tıkla zig) |
| **LLM** | Claude Code CLI (varsayılan), Codex, Anthropic API, Ollama, Gemini |
| **Eval** | 166 elle etiketlenmiş örnek, dev/test ayrımlı (dev 96 / test 70) |
| **Arayüzler** | Windows masaüstü (.exe), web (React), CLI, REST API + SSE |
| **Çıktılar** | JSON · Markdown · SARIF · Rich terminal paneli |
| **Kalite** | 3.700+ test, `mypy --strict`, ruff, Windows + Ubuntu CI, 32 ADR |

## İçindekiler

- [Neden?](#neden) · [Örnek](#öğrenci-ne-görüyor) · [Nasıl çalışır?](#nasıl-çalışır)
- [Mühendislik kararları](#mühendislik-kararları) · [Sonuçlar](#sonuçlar)
- [Hızlı başlangıç](#hızlı-başlangıç) · [Masaüstü uygulaması](#masaüstü-uygulaması)
- [Sağlayıcılar](#sağlayıcılar) · [Güvenlik](#güvenlik) · [Sınırlamalar](#sınırlamalar)
- [Geliştirme](#geliştirme) · [Yol haritası](#yol-haritası)

## Neden?

Bir LLM'e "kodumda ne yanlış?" diye sorulduğunda genellikle düzeltilmiş kodu verir. Öğrenci
hatayı görmeden ödevi teslim eder; öğrenme kaybolur. CodeMentor bu akışı tersine çevirir:

- **Çözüm yerine soru.** LLM çıktısı öğrenciye doğrudan gitmez. Bulgular satır kanıtıyla
  doğrulanır, Sokratik sorular bir **sızıntı korumasından** geçer; çözüm sızdıran soru yeniden
  üretilir. Sızıntı eval'de ölçülür (%0).
- **Deterministik temel.** Sözdizimi hataları, bilinen bellek / GC / motor hataları ve Big-O
  ipucu LLM'e gitmeden statik olarak bulunur. Sözdizimi hatasında **LLM hiç çağrılmaz**; LLM
  yanıt vermezse rapor statik analizle yine döner.
- **Kademeli ipucu.** Aynı oturumda her "bir ipucu daha" seviyeyi yükseltir (1 → 3):
  önce kavram, sonra satır, en sonda yön. Cevap hiçbir seviyede verilmez.
- **Ölçülmüş iddialar.** Her prompt ve kural değişikliği etiketli bir eval setiyle ölçülür;
  aşağıdaki tablolar sonuç dosyalarından üretilir ve bir test onları denetler.

## Öğrenci ne görüyor?

Aşağıdaki çıktılar gerçek koşulardan alındı (LLM gerektirmeyen iki yol). LLM'li tam bir
analizin ekran görüntüsü yukarıda.

**1. Sözdizimi hatası: erken çıkış, LLM çağrısı yok (~1 ms)**

```c
int main(void) {
    int toplam = 0          // 4. satır
    for (int i = 0; i <= 10; i++) {
```

`codementor analyze ornek.c --format md` çıktısından (başlık ve künye satırları çıkarıldı):

```markdown
- **Derleme:** başarısız
- **Not:** kod derlenmediği için analiz derleme aşamasında durdu.

## Derleme tanıları
- 4. satır (error): Burada noktalı virgül (;) eksik görünüyor.

## Mentor soruları
İpucu seviyesi: 1
1. 4. satırda bir ifade `;` ile bitmiyor gibi görünüyor. Derleyici bu satırdan sonra neyi
   bekliyor olabilir?

> Sonraki adım: Önce ilk hatayı düzelt; sonraki hatalar çoğu zaman onun sonucudur.
> Kod derlendiğinde analiz devam edecek.
```

Kod düzeltilmez; `;` yazılmaz. Öğrenciye neye bakacağı söylenir.

**2. Statik kural: bağlı listede denetlenmeyen tahsis**

```c
void push_back(Node **head, int value) {
    Node *n = malloc(sizeof(Node));   // 17. satır
    n->value = value;
```

```text
C-MEM-003 (orta) 17. satır
`malloc`/`calloc`/`realloc` bellek ayıramazsa NULL döndürür. Bu işaretçi denetlenmeden
kullanılıyor; tahsis başarısız olursa bu satırdan sonra ne olur?
```

Kural açıklamaları bile soru biçimindedir. Ardından LLM geçişi statik olguları (çağrı grafiği,
döngü derinliği, Big-O ipucu) görerek ek bulgular üretir; her bulgu satır kanıtıyla doğrulanır
ve mentorluk geçişi bunları sorulara çevirir.

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

| Katman | Ne yapar |
|---|---|
| **K0 Giriş** | Satır sonu/kodlama normalizasyonu, dil ve motor tespiti, boyut sınırı |
| **K1 Ön doğrulama** | Tier 0: tree-sitter `ERROR`/`MISSING` → Türkçe tanı. Tier 1: gcc/clang `-fsyntax-only`, Roslyn; kod **çalıştırılmaz** |
| **K2 Statik analiz** | tree-sitter sorgularıyla olgular (döngüler, çağrılar, tahsisler), Big-O ipucu, 41 kural |
| **K3 Prompt** | Numaralı kod, olgular, dile/motora özgü kontrol listesi, few-shot; kod `<user_code>` içinde veri olarak |
| **K4 LLM** | İki geçiş (analiz → mentorluk), şema onarımı, isteğe bağlı bulgu doğrulama geçişi |
| **K5 Doğrulama** | JSON şeması, satır kanıtı, statik ipucuyla Big-O uyumu, sızıntı koruması |
| **K6 Rapor** | Tek şema; JSON, Markdown, SARIF 2.1.0, web ve masaüstü görünümü |

Ayrıntı: [docs/mimari.md](docs/mimari.md).

## Mühendislik kararları

Her önemli karar bir ADR'dir ([docs/adr/](docs/adr/), 32 kayıt). Öne çıkanlar:

- **Hibrit, LLM sarmalayıcısı değil.** Deterministik katman, yanıtların bir kısmını LLM'siz
  verir (sözdizimi hatalarında erken çıkış precision/recall %100) ve LLM'e olgu sağlar: olgular
  prompt'tan çıkarılınca Big-O birebir doğruluk %96'dan %85'e düşüyor (ablasyon).
- **Kullanıcı kodu güvenilmeyen veridir.** Kod hiçbir zaman çalıştırılmaz; derleyiciye yalnız
  stdin ile gider, boş geçici dizinde, temizlenmiş ortamla, POSIX rlimit / Windows Job Object
  sınırlarıyla. `#include "/etc/passwd"` gibi yollar Tier 1'e gitmeden reddedilir. Prompt
  injection fixture'ları eval'in %12,5'idir; direnç %100.
- **Docker yok, yine de yalıtım var** (ADR-0009). Paylaşılan sunucu için Tier 0 ayrıştırması
  süre ve bellek sınırlı alt süreçte koşturulabilir (ADR-0025): kasıtlı bir C# girdisinin süreç
  içinde ~10 sn ve ~4,2 GB tükettiği ölçüldü, alt süreçte ~1 sn'de durur.
- **Zarif bozulma.** Sağlayıcı yoksa, zaman aşımı olursa ya da şema iki denemede tutmazsa
  rapor statik analiz ve şablon sorularla döner (`meta.degraded`); analiz asla boş dönmez.
- **Sağlayıcıdan bağımsız.** Model adları ve anahtarlar yalnız yapılandırmada; CLI ajanları
  araçları kapalı, prompt stdin'den koşar (ADR-0012, ADR-0017). Testler ağa çıkmaz
  (`FakeProvider`); gerçek API testleri `@pytest.mark.live` ile ayrıdır.
- **Doğrusal zaman sözü.** 40 KB'lık kötü niyetli girdiler (iç içe yapılar, binlerce denetim,
  derin etiket yığınları) her kural için performans testinde; karesel davranış test kırar.

## Sonuçlar

166 elle etiketlenmiş örnek: dev 96 / test 70; %25'i sözdizimi hatalı, %12,5'i prompt
injection içerir. Bulgu eşleşmesi: aynı kategori + satır farkı ≤ 2. Prompt'lar dev'de
geliştirildi; test bölümü dokunulmadan tutuldu.

| Ölçüm | Claude Opus (`claude_cli`) | Yalnızca statik (LLM yok) |
|---|---|---|
| Denetim P / R / F1, dev 96 | **78 / 96 / 86** (Faz 51, güncel prompt) | 100 / 57 / 73 |
| Denetim P / R / F1, test 70 | 27 / 92 / 42 (Faz 12 prompt'u, 49 örnek) | 94 / 55 / 69 |
| Erken çıkış P / R | %100 / %100 | %100 / %100 |
| Big-O birebir / sınıf (test) | %91–94 / %94–97 | %97 / %97 |
| Çözüm sızıntısı | %0 | — |
| Prompt injection direnci | %100 | — |
| Gecikme p50 | ~16–24 sn (iki geçiş) | ~0,1 sn |

Okuma notları:

- **İş bölümü net:** statik kurallar az ama kesin bulur (precision %94–100); LLM recall'ı
  %55'ten %92–96'ya taşır. İkisi birlikte bulunur, biri diğerinin yerine geçmez.
- **Precision'ın hikâyesi:** ilk prompt'ta LLM etiketlenmemiş küçük gözlemler ekliyordu
  (precision %27). Dev'de "sorun" ölçütü, kategori tanımları, ayrı bir bulgu doğrulama geçişi
  (ADR-0019) ve kategori tutarlılığıyla dev precision'ı %27'den %78'e çıktı, recall korundu
  (bu arada dev seti de 31'den 96 örneğe büyüdü). Test bölümü bu iyileştirmelerden sonra
  yeniden koşulmadı; tablodaki test satırı bilinçli olarak eski ölçümdür.
- **Küçük veri:** test bölümünde bir örnek ~2–3 puan eder. Sonuçlar yön göstericidir.

<details>
<summary><b>Tüm eval tabloları (sonuç dosyalarından üretilir, test ile denetlenir)</b></summary>

Tablolar `uv run codementor eval compare eval/results/*_test.json` (ve `*_dev.json`)
çıktısıdır; `tests/unit/eval/test_readme_table.py` sonuç dosyalarıyla birebir olduklarını
denetler. "Yalnızca statik" satırındaki injection direnci anlamsızdır (LLM çağrılmaz).

> Not (Faz 21): "Yalnızca statik" satırları güncel kurallarla ve Faz 21'de iki bulgu eklenmiş
> dev etiketleriyle yeniden koşuldu; LLM satırları Faz 12'deki kurallar ve etiketlerle hesaplandı
> (yeniden koşulmadı). Satırlar bu yüzden tam karşılaştırılabilir değil; ayrıntı
> `docs/eval-findings.md` §5.

> Not (Faz H4, 2026-10-16): statik dev koşusu H1–H3 değişiklikleriyle yeniden koşuldu
> (`eval/results/20261016T212522_static_none_static_dev.json`, 96 örnek): precision **%100'de
> kaldı**, recall %55 → **%57,5**, F1 %71 → **%73**; Big-O %97/%97, erken çıkış %100/%100.
> Özet tablodaki "Yalnızca statik" dev satırı bu koşudan; test bölümü `--final` olmadan
> koşulmadı (H4 kapsamı dev).

**Test (70 örnek):**

<!-- eval-table:test:start -->
| Koşu | Mod | Ablasyon | Örnek | Şema (ilk / onarım sonrası) | Erken çıkış P / R | Big-O birebir / sınıf | Denetim P / R / F1 | Satır doğruluğu | Sızıntı | Injection direnci | p50 / p95 (sn) | Token ort. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude_cli / claude-opus-5-5 | two_pass | — | 49 (test) | 100% / 100% | 100% / 100% | 91% / 94% | 27% / 92% / 42% | 94% | 0% | 100% | 20.3 / 57.3 | 15673 |
| claude_cli / claude-opus-5-5 | single_pass | — | 49 (test) | 100% / 100% | 100% / 100% | 94% / 97% | 32% / 94% / 48% | 94% | 0% | 100% | 13.5 / 35.7 | 10182 |
| Yalnızca statik (LLM yok) | static | — | 49 (test) | — / — | 100% / 100% | 97% / 97% | 90% / 49% / 63% | 100% | 0% | — | 0.1 / 0.5 | — |
| Yalnızca statik (LLM yok) | static | — | 70 (test) | — / — | 100% / 100% | 97% / 97% | 94% / 55% / 69% | 100% | 0% | — | 0.0 / 0.6 | — |

Sürümler: prompt v1+14a294f9 · kurallar r1+d1852061 · şema 1.0
Sürümler: prompt v1+2579008b · kurallar r2+2256b8a8 · şema 1.1
Sürümler: prompt v1+fbc08625 · kurallar r1+d3065584 · şema 1.0
<!-- eval-table:test:end -->

> Not: `c-016` etiketine 2026-10-01'de ikinci beklenen bulgu (`memory_safety`, C-MEM-003) eklendi; LLM satırları eski etiketle puanlandı.

**Dev ve ablasyonlar (31 → 46 → 96 örnek):**

<!-- eval-table:dev:start -->
| Koşu | Mod | Ablasyon | Örnek | Şema (ilk / onarım sonrası) | Erken çıkış P / R | Big-O birebir / sınıf | Denetim P / R / F1 | Satır doğruluğu | Sızıntı | Injection direnci | p50 / p95 (sn) | Token ort. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| claude_cli / claude-opus-5-5 | two_pass | — | 31 (dev) | 100% / 100% | 100% / 100% | 96% / 96% | 27% / 92% / 42% | 100% | 0% | 100% | 23.5 / 40.0 | 14219 |
| claude_cli / claude-opus-5-5 | single_pass | — | 31 (dev) | 100% / 100% | 100% / 100% | 92% / 92% | 32% / 96% / 47% | 96% | 0% | 100% | 13.1 / 24.5 | 9359 |
| claude_cli / claude-opus-5-5 | two_pass | facts | 31 (dev) | 100% / 100% | 100% / 100% | 85% / 92% | 28% / 100% / 43% | 96% | 0% | 100% | 20.5 / 42.3 | 13227 |
| claude_cli / claude-opus-5-5 | two_pass | line_numbers | 31 (dev) | 100% / 100% | 100% / 100% | 92% / 92% | 28% / 100% / 44% | 96% | 0% | 100% | 20.4 / 41.3 | 13861 |
| claude_cli / claude-opus-5-5 | two_pass | — | 31 (dev) | 100% / 100% | 100% / 100% | 96% / 96% | 67% / 86% / 75% | 100% | 0% | 100% | 17.5 / 31.3 | 13389 |
| Yalnızca statik (LLM yok) | static | — | 31 (dev) | — / — | 100% / 100% | 96% / 96% | 100% / 37% / 54% | 100% | 0% | — | 0.1 / 0.6 | — |
| claude_cli / claude-opus-5-5 | two_pass | — | 46 (dev) | 100% / 100% | 100% / 100% | 93% / 97% | 69% / 89% / 78% | 98% | 0% | 100% | 17.9 / 36.1 | 14111 |
| claude_cli / claude-haiku-4-5-20251001 (thinking=0) | two_pass | — | 46 (dev) | 97% / 100% | 100% / 100% | 97% / 97% | 45% / 78% / 57% | 88% | 0% | 100% | 14.7 / 32.3 | 14926 |
| claude_cli / claude-haiku-4-5-20251001 (thinking=0) | single_pass | — | 46 (dev) | 100% / 100% | 100% / 100% | 100% / 100% | 48% / 78% / 59% | 84% | 0% | 100% | 14.3 / 66.9 | 17247 |
| claude_cli / claude-opus-5-5 | two_pass | verify | 46 (dev) | 100% / 100% | 100% / 100% | 93% / 93% | 79% / 89% / 84% | 98% | 0% | 100% | 22.1 / 38.3 | 15891 |
| claude_cli / claude-opus-5-5 | two_pass | fewshot0 | 46 (dev) | 100% / 100% | 100% / 100% | 97% / 97% | 68% / 91% / 78% | 98% | 0% | 100% | 19.3 / 33.9 | 13737 |
| claude_cli / claude-opus-5-5 | two_pass | fewshot1 | 46 (dev) | 100% / 100% | 100% / 100% | 93% / 97% | 68% / 89% / 77% | 98% | 0% | 100% | 16.9 / 28.3 | 12641 |
| Yalnızca statik (LLM yok) | static | — | 96 (dev) | — / — | 100% / 100% | 97% / 97% | 100% / 58% / 73% | 100% | 0% | — | 0.1 / 0.5 | — |
| claude_cli / claude-opus-5-5 | two_pass | — | 24 (dev) | 100% / 100% | 100% / 100% | 100% / 100% | 71% / 77% / 74% | 100% | 0% | 100% | 16.7 / 44.4 | 14366 |
| claude_cli / claude-opus-5-5 | two_pass | — | 24 (dev) | 100% / 100% | 100% / 100% | 93% / 93% | 78% / 90% / 84% | 100% | 0% | 100% | 20.7 / 33.4 | 13768 |
| codex / gpt-6-luna | two_pass | — | 24 (dev) | 100% / 100% | 100% / 100% | 87% / 100% | 79% / 79% / 79% | 100% | 0% | 100% | 19.8 / 29.8 | 39501 |
| codex / gpt-6-luna | two_pass | — | 24 (dev) | 100% / 100% | 100% / 100% | 93% / 93% | 81% / 85% / 83% | 100% | 0% | 100% | 18.2 / 41.3 | 41074 |
| codex / gpt-6-luna | two_pass | — | 24 (dev) | 100% / 100% | 100% / 100% | 100% / 100% | 71% / 65% / 68% | 94% | 0% | 100% | 20.2 / 40.3 | 38687 |
| codex / gpt-6-luna | two_pass | — | 24 (dev) | 100% / 100% | 100% / 100% | 87% / 93% | 84% / 80% / 82% | 100% | 0% | 100% | 19.0 / 29.8 | 37761 |
| claude_cli / claude-opus-5-5 | two_pass | — | 24 (dev) | 100% / 100% | 100% / 100% | 93% / 100% | 83% / 100% / 90% | 100% | 0% | 100% | 17.2 / 31.6 | 14709 |
| claude_cli / claude-opus-5-5 | two_pass | — | 24 (dev) | 100% / 100% | 100% / 100% | 93% / 93% | 74% / 88% / 81% | 96% | 0% | 100% | 24.0 / 44.6 | 16484 |
| claude_cli / claude-opus-5-5 | two_pass | — | 3 (dev) | 100% / 100% | — / — | 100% / 100% | 60% / 100% / 75% | 100% | 0% | — | 30.2 / 31.4 | 16757 |
| claude_cli / claude-opus-5-5 | two_pass | — | 1 (dev) | 100% / 100% | — / — | 100% / 100% | 100% / 100% / 100% | 100% | 0% | — | 19.8 / 19.8 | 13589 |
| claude_cli / claude-opus-5-5 | two_pass | — | 24 (dev) | 100% / 100% | 100% / 100% | 100% / 100% | 80% / 92% / 86% | 100% | 0% | 100% | 16.4 / 35.1 | 14892 |
| claude_cli / claude-opus-5-5 | two_pass | — | 24 (dev) | 100% / 100% | 100% / 100% | 93% / 93% | 87% / 100% / 93% | 100% | 0% | 100% | 16.0 / 34.4 | 14023 |
| claude_cli / claude-opus-5-5 | two_pass | — | 24 (dev) | 100% / 100% | 100% / 100% | 100% / 100% | 78% / 95% / 86% | 100% | 0% | 100% | 16.2 / 27.6 | 14416 |
| claude_cli / claude-opus-5-5 | two_pass | — | 24 (dev) | 100% / 100% | 100% / 100% | 93% / 93% | 71% / 96% / 82% | 100% | 0% | 100% | 18.2 / 38.0 | 15080 |
| Yalnızca statik (LLM yok) | static | — | 96 (dev) | — / — | 100% / 100% | 97% / 97% | 100% / 55% / 71% | 100% | 0% | — | 0.1 / 0.7 | — |
| Yalnızca statik (LLM yok) | static | — | 96 (dev) | — / — | 100% / 100% | 97% / 97% | 100% / 57% / 73% | 100% | 0% | — | 0.1 / 0.8 | — |
| Yalnızca statik (LLM yok) | static | — | 96 (dev) | — / — | 100% / 100% | 97% / 97% | 100% / 57% / 73% | 100% | 0% | — | 0.1 / 0.9 | — |

Sürümler: prompt v1+14a294f9 · kurallar r1+d1852061 · şema 1.0
Sürümler: prompt v1+2579008b · kurallar r2+2256b8a8 · şema 1.1
Sürümler: prompt v1+2579008b · kurallar r2+5f39f401 · şema 1.1
Sürümler: prompt v1+632620d8 · kurallar r2+6d038ca1 · şema 1.1
Sürümler: prompt v1+632620d8 · kurallar r2+e29a16e4 · şema 1.1
Sürümler: prompt v1+7205d091 · kurallar r1+d1852061 · şema 1.1
Sürümler: prompt v1+a4c5ebfc · kurallar r1+d1852061 · şema 1.1
Sürümler: prompt v1+fbc08625 · kurallar r1+d3065584 · şema 1.0
Sürümler: prompt v1+fdc16030 · kurallar r1+fa6fff47 · şema 1.0
<!-- eval-table:dev:end -->

> En güncel dev ölçümü (Faz 51, 2026-10-05): **Claude 96 örnek — Denetim P / R / F1 = 78 / 96 / 86** (karışıklık 7 → 2). Ayrıntı: `PROGRESS.md` "Faz 51 — Notlar".

> Faz 36 (2026-10-04): Claude Opus parçaları 1/4 + 2/4 (48 örnek) kayıtlı metrikte 75 / 83 / 78; `unity-104` etiketi güncellenince 75 / 81 / 78. Codex `gpt-6-luna` aynı promptla dört parçayı koştu: 96 örnekte 79 / 77 / 78. Sağlayıcılar farklı olduğundan sonuçlar birleştirilmez. Ayrıntı: `docs/eval-findings.md` §11.

> Dev genişletmesi (2026-10-04): dev 46 → 96 örnek. Statik satır ve Codex `gpt-6-luna` ölçümü 96 örnekliktir; Claude Opus satırları eski 46 örnek ve kısmi 24'er örnek koşularıdır. Ayrıntı: `docs/eval-findings.md` §10–11.

> Faz 34/35B (2026-10-03): `verify` = bulgu doğrulama geçişi (artık varsayılan açık, ADR-0019): precision 69 → 79, recall aynı. İkinci model Claude Haiku 4.5 (düşünme kapalı). Few-shot 0/1/2 arasında fark yok. Ayrıntı: `docs/eval-findings.md` §9.

> Faz 22B (2026-10-02): `v1+fdc16030` prompt'u ("sorun" ölçütü, kategori tanımları, en fazla 6 bulgu, Python few-shot). Ayrıntı: `docs/eval-findings.md` §7.

**Python, HTML, CSS (Faz 18, 36 örnek; dil başına 12):** test 21 / dev 15, yalnızca bu dillerde
koşuldu (`eval run --language`). Dil başına döküm: `docs/eval-findings.md` §4.

<!-- eval-table:test-diller:start -->
| Koşu | Mod | Ablasyon | Örnek | Şema (ilk / onarım sonrası) | Erken çıkış P / R | Big-O birebir / sınıf | Denetim P / R / F1 | Satır doğruluğu | Sızıntı | Injection direnci | p50 / p95 (sn) | Token ort. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Yalnızca statik (LLM yok) | static | — | 21 (test) | — / — | 100% / 100% | 100% / 100% | 100% / 67% / 80% | 100% | 0% | — | 0.0 / 0.0 | — |
| claude_cli / claude-opus-5-5 | two_pass | — | 21 (test) | 100% / 100% | 100% / 100% | 100% / 100% | 33% / 81% / 47% | 100% | 0% | 100% | 16.5 / 36.5 | 9665 |
| claude_cli / claude-opus-5-5 | single_pass | — | 21 (test) | 100% / 100% | 100% / 100% | 100% / 100% | 34% / 86% / 49% | 100% | 0% | 100% | 14.1 / 23.4 | 7328 |

Sürümler: prompt v1+e485058f · kurallar r1+286dfb2f · şema 1.0
<!-- eval-table:test-diller:end -->

<!-- eval-table:dev-diller:start -->
| Koşu | Mod | Ablasyon | Örnek | Şema (ilk / onarım sonrası) | Erken çıkış P / R | Big-O birebir / sınıf | Denetim P / R / F1 | Satır doğruluğu | Sızıntı | Injection direnci | p50 / p95 (sn) | Token ort. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Yalnızca statik (LLM yok) | static | — | 15 (dev) | — / — | 100% / 100% | 100% / 100% | 100% / 55% / 71% | 100% | 0% | — | 0.0 / 0.0 | — |
| claude_cli / claude-opus-5-5 | two_pass | — | 15 (dev) | 100% / 100% | 100% / 100% | 100% / 100% | 54% / 95% / 69% | 89% | 0% | 100% | 16.2 / 34.2 | 9530 |
| claude_cli / claude-opus-5-5 | two_pass | — | 15 (dev) | 100% / 100% | 100% / 100% | 100% / 100% | 68% / 85% / 76% | 94% | 0% | 100% | 15.6 / 25.8 | 10127 |

Sürümler: prompt v1+e485058f · kurallar r1+286dfb2f · şema 1.0
Sürümler: prompt v1+fdc16030 · kurallar r1+fa6fff47 · şema 1.0
<!-- eval-table:dev-diller:end -->

> Son two_pass satırı Faz 22B prompt'udur (`v1+fdc16030`).

</details>

## Hızlı başlangıç

### Seçenek 1: Masaüstü uygulaması (Windows)

[Releases](https://github.com/BurakYildizGameDev/codementor-ai/releases/latest) sayfasından
`CodeMentor-<sürüm>-win64.zip`'i indir, aç ve `CodeMentor.exe`'ye çift tıkla (imzasız olduğu
için Windows SmartScreen uyarı verebilir: "Ek bilgi" → "Yine de çalıştır"). Release'ler bir
etiketten otomatik derlenir, duman testinden geçer ve `SHA256SUMS` ile gelir
(`sha256sum -c SHA256SUMS`). Her `main` koşusunun derlediği exe GitHub Actions'ta
`CodeMentor-win64` artefaktı olarak da bulunur. Python, Node.js
ya da tarayıcı gerekmez (ADR-0013). Gereken tek şey bir LLM sağlayıcısı: varsayılan, oturum açılmış [Claude Code](https://claude.com/claude-code) CLI'ı.

### Seçenek 2: Web arayüzü + API

Gerekenler: Python 3.12 + [uv](https://docs.astral.sh/uv/), Node.js 20+, bir LLM sağlayıcısı.

```bash
git clone https://github.com/BurakYildizGameDev/codementor-ai.git
cd codementor-ai
uv sync
uv run codementor serve            # API: http://127.0.0.1:8000/docs

# ikinci terminalde
cd web && npm install && npm run dev   # arayüz: http://127.0.0.1:5173
```

![Web arayüzü: sağlayıcı/mod seçimi, analiz, bulguya gitme, raporu indirme](docs/img/web-demo.gif)

<sub>Rapor gelince bulgular editörde işaretlenir, bulguya tıklayınca satıra gidilir, rapor JSON /
Markdown / SARIF olarak indirilir. GIF e2e karelerinden üretilir:
`cd web && npx playwright test -g GIF` ardından `uv run python tools/make_demo_gif.py`.</sub>

### Seçenek 3: Komut satırı

```bash
uv run codementor analyze kod.c                                   # Rich panel
uv run codementor analyze kod.cs --engine unity --format sarif --out rapor.sarif
uv run codementor questions list                                  # 64 görevlik soru bankası
uv run codementor questions add sorum.yaml                        # kendi görevini ekle
uv run codementor rules list                                      # 41 statik kural
```

**Derleyici (isteğe bağlı):** gcc/clang (C/C++/Unreal Tier 1) ve .NET SDK (C# Tier 1,
`make roslyn-check`). Yoksa Tier 1 atlanır, analiz yine çalışır; ya da
`uv run codementor toolchain install zig` zig'i (~100 MB, sha256 doğrulamalı) `~/.codementor`
altına kurar (ADR-0018). Durum: `codementor toolchain status`, hazırlık:
`curl http://127.0.0.1:8000/health/ready`.

Komutlar her dizinden çalışır: `codementor.toml` önce `CODEMENTOR_CONFIG_FILE`'dan, sonra
çalışma dizininden, `~/.codementor/codementor.toml`'dan ve paketle gelen varsayılandan okunur
(`pip install` ile kurulumda da). Çalışma dizinindeki dosya güvenilmez sayılır: içindeki sağlayıcı
komutu, `base_url`, yol ve ağ ayarları yok sayılır ve uyarı basılır; bunlar için dosyayı
`CODEMENTOR_CONFIG_FILE` ile verin (ADR-0029). İçindeki göreli yollar toml'un dizinine göre çözülür (ADR-0016). Not Defteri'nin
"UTF-8 BOM" ile kaydettiği dosya da okunur. CLI'da sistem hataları (okunamayan yapılandırma ya
da dosya, açılamayan veritabanı) Türkçe mesaj ve **çıkış kodu 3** ile biter; 1 yalnız yüksek
önemli bulgu demektir.

## Masaüstü uygulaması

- **Analiz:** kodu yaz, aç (`.c .h .cpp .hpp .cs .py .html .css`) ya da örnek yükle; dil/motor
  seç, isteğe bağlı bir görev seç, **Denetle** (Ctrl+Enter). Analiz akışı 6 adımda canlı izlenir;
  bulgu satırları editörde önem rengiyle boyanır, karta tıklayınca satıra gidilir.
- **Sokratik mentor:** ana kavram, yönlendirici sorular ve sonraki adım. **Bir ipucu daha**
  aynı oturumla yeniden denetler ve ipucu seviyesini (1 → 3) artırır; **Baştan başla** sıfırlar.
- **Soru bankası:** 64 görev; her dil/motorda çok kolaydan zora 8 görev, dil ve zorluk filtresiyle.
  **+ Soru ekle** ile kendi görevini ekleyebilirsin: başlık, açıklama, dil ve zorluk yeterli;
  hedef karmaşıklık, kısıtlar, kavram etiketleri ve ipuçları isteğe bağlı. Kendi soruların
  `~/.codementor/questions` altında durur, kartlarından düzenlenir ya da silinir (ADR-0028).
- **Token kullanımı:** her raporda harcanan token (giriş/çıkış, tahmini maliyet) ve aşama
  dağılımı (analiz, doğrulama, mentor soruları) görünür; önbellekten dönen ya da modelin
  çağrılmadığı analizde `token 0` ve nedeni yazılır.
- **Geçmiş:** önceki analizler kodlarıyla yeniden açılır; başlıkta tüm analizlerin toplam token'ı
  ve tahmini maliyeti; raporlar Markdown / SARIF / JSON olarak dışa aktarılır.
- **Bağlantılar:** her sağlayıcı için bir kart: model seçimi, **Oturum aç**, API anahtarı
  (Windows Kimlik Bilgisi Yöneticisi'nde, dosyaya yazılmaz), **Bağlantıyı dene**, **Varsayılan
  yap**, Ollama kartında **Modeli indir** (`ollama pull`), **Derleyiciyi indir** (zig; kurulu zig
  eskiyse **Derleyiciyi güncelle**). Seçimler tek tuşla
  `codementor.toml`'a yazılır (yorumlar
  korunur); CLI ve API de aynı modeli kullanır (ADR-0014).
- **Editör:** Ctrl+F arama, **Son ▾** menüsünde son dosyalar, sürükle-bırak ile açma.

Derlemek için (Windows, depo kökünde):

```bash
uv sync
make roslyn-check-sc                 # isteğe bağlı: dotnet gerektirmeyen C# denetleyicisi (+~15 MB)
uv run python build_exe.py --both    # dist/CodeMentor.exe (~37 MB) + dist/CodeMentor-0.1.0-win64.zip
uv run python -m codementor.desktop  # derlemeden çalıştırmak için
```

Exe'nin yanına bir `codementor.toml` koyarsan paketteki varsayılan yerine o kullanılır;
"toml'a yaz" düğmesi de bu dosyayı oluşturur (pip ile kurulumda `~/.codementor/codementor.toml`)
ve Bağlantılar ekranı hangi dosyanın okunduğunu gösterir. Yazarken satır içi tablolar, nokta
anahtarları ve yorumlar korunur. Veritabanı, tercihler ve log `~/.codementor` altındadır.

## Sağlayıcılar

`codementor.toml` içinde `[providers] default = "..."`. Model adları yalnızca yapılandırmada
tutulur (ADR-0008). API anahtarları **ortam değişkeni** olarak verilir; `.env` dosyası bilerek
otomatik yüklenmez (öğrenci projesindeki bir `.env` ayarları değiştirebilirdi; bkz.
`.env.example`). Masaüstünde anahtarlar Bağlantılar ekranından girilir.

| Sağlayıcı | Kurulum | Not |
|---|---|---|
| `claude_cli` (varsayılan) | `claude` CLI'ında oturum aç | API anahtarı gerekmez; araçları kapalı, prompt stdin'den (ADR-0012). Tüm Claude eval ölçümleri bununla yapıldı. |
| `codex` | `codex login`, `[providers.codex] model` (ör. `gpt-6-luna`), `allow_tool_agent = true` | API anahtarı gerekmez; salt okunur sandbox, prompt stdin'den (ADR-0017). Dev 96'da ayrıca ölçüldü. |
| `anthropic` | `ANTHROPIC_API_KEY`, `[providers.anthropic] model` | Yapılandırılmış çıktı (ADR-0011) |
| `ollama` (yerel) | [Ollama](https://ollama.com) kur, `ollama pull qwen2.5-coder:7b`, `default = "ollama"` | Tamamen çevrimdışı; kalite modele bağlı, **eval'de ölçülmedi** |
| `gemini` (deneysel) | `GEMINI_API_KEY`, `[providers.gemini] model` | OpenAI uyumlu uç, katı şema (ADR-0020). Canlı doğrulanmadı |
| `agy` (deneysel) | Antigravity CLI'ında oturum aç, `allow_tool_agent = true` | Araçları kapatılamıyor (ADR-0012); eval'de ölçülmedi |

> OpenAI ve DeepSeek sağlayıcıları 2026-10-03'te kaldırıldı (ADR-0021): canlı doğrulanamıyordu.

> **agy yanıt vermiyorsa** (analiz "Derin analiz"de bekleyip boş dönüyorsa): agy, global MCP
> sunucularının hepsini her çağrıda başlatır; bağlanamayan biri (ör. Unity kapalıyken
> `unity-mcp`) turu hiç başlatmaz. `agy mcp list` ile bak; kullanmadığın sunucuyu
> `agy mcp remove <ad>` ile kaldır ya da yalnız ilgili projenin `.agents/mcp_config.json`'una
> taşı. `agy mcp disable` yetmez: başsız modda yok sayılıyor (Faz 63, ADR-0012).

## Güvenlik

- **Varsayılan yerel.** API yalnızca `127.0.0.1`'e bağlanır; başka adrese bağlanırsa `serve`
  uyarır. Host başlığı izin listesi, gövde boyutu sınırı, eşzamanlı analiz sınırı (4) ve analiz
  başına toplam süre sınırı vardır; istek isteği Tier 1'i kapatabilir ama açamaz (ADR-0023).
- **İsteğe bağlı API anahtarı:** `codementor.toml`'da `[api] api_key_env = "CODEMENTOR_API_KEY"`
  ve ortamda `CODEMENTOR_API_KEY=<anahtar>`; bu durumda `/v1/*` ve dahili uçlar `X-API-Key` başlığı
  ister (`/health` açık kalır). Web arayüzü anahtarı tarayıcı oturumunda (`sessionStorage`) saklar ve
  isteklerde iletir.
- **Paylaşılan sunucuda** ayrıca `[validation] tier0_isolation = true` açılmalı (ADR-0025).
  İstemci IP başına dakikalık hız sınırı `[api] rate_limit_per_minute` (varsayılan 30) ile korunur;
  dışa açık adrese anahtarsız `serve` reddedilir (`--insecure` ile geçilebilir).
- **Bağımlılıklar:** `uv.lock` sabit; CI'da `pip-audit --strict` ve `npm audit`. İndirilen
  derleyici yalnız yapılandırmadaki https adresinden, sha256 doğrulanarak, güvenli açma ile kurulur.

## Sınırlamalar

- **Unreal yalnızca stub başlıkla derlenir** (`data/stubs/ue_stubs.h`); stub kaynaklı hatalar
  uyarıya düşürülür (ADR-0007). C#/Unity'de Tier 1 yalnızca Roslyn sözdizimi ayrıştırmasıdır.
- **Kod çalıştırılmaz** (ADR-0005): Big-O statik ipucu + LLM gerekçesidir, ölçülmüş çalışma
  süresi değildir.
- **Eval küçük ve iki model ağırlıklı.** Ana sonuçlar `claude-opus-5-5` içindir; Claude Haiku 4.5
  ve Codex `gpt-6-luna` dev'de ayrıca ölçüldü. Ollama, Gemini ve Anthropic API ölçülmedi.
- **Statik kurallar muhafazakârdır:** emin olunmayan durumda susar (ör. HTML'de tarayıcının
  biçimlendirme öğelerini yeniden kurması, C'de yanlış daldaki null denetimi). Bilinen sınırlar
  [kural kataloğunda](docs/rules-catalog.md) yazılıdır.
- **Sızıntı koruması sezgiseldir** (n-gram + işaret listesi). Eval'deki %0 ölçülen işaretler
  içindir; başka biçimde sızmış bir çözümü kaçırabilir.
- **HTML/CSS'te** karmaşıklık analizi yapılmaz; HTML'de kapanmamış etiketler sözdizimi hatası
  değil, bulgu (HTML-STD-003) olarak raporlanır.
- **Docker paketi yok** (ADR-0009): kurulum `uv` + `npm` ile yereldir.

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

**Test disiplini:** ~41 bin satır test (~29 bin satır kaynak koda karşı): birim, entegrasyon,
golden prompt anlık görüntüleri, hypothesis özellik testleri, her kural için pozitif/negatif
fixture'lar, 40 KB kötü niyetli girdiyle doğrusal zaman testleri, Playwright e2e. Testler ağa
çıkmaz; CI Ubuntu ve Windows'ta koşar, her `main` koşusu exe'yi de derler.

**Nasıl geliştirildi:** proje 60'tan fazla fazda (Faz 0-63, ardından public öncesi Faz A-K),
her faz ayrı dalda, kabul kriterleri ve testlerle geliştirildi
([uygulama planı](docs/UYGULAMA_PLANI.md), [ilerleme günlüğü](PROGRESS.md),
[geliştirme günlüğü](docs/gelistirme-gunlugu/)).
Mimariden her sapma bir ADR'dir. Kodlama ajanlarıyla çalışıldı; fazların çoğu bağımsız bir
kod denetimi ajanından geçti ve bulunan hatalar birleştirmeden önce düzeltildi.

## Yol haritası

- **v1.1:** cppcheck / clang-tidy entegrasyonu; düşük önemli bulguları ayrı göstermek; imzalı
  Windows kurulum paketi; LLM-as-judge ile Sokratik kalite puanı; yerel modellerin (Ollama) eval'i.
- **v2.0:** yalıtılmış ortamda ampirik karmaşıklık ölçümü; test senaryosu tabanlı doğruluk;
  VS Code eklentisi (SARIF + canlı analiz); Rust ve Go.

---

Belgeler: [mimari](docs/mimari.md) · [ADR'ler](docs/adr/) · [uygulama planı](docs/UYGULAMA_PLANI.md) ·
[eval bulguları](docs/eval-findings.md) · [kural kataloğu](docs/rules-catalog.md) ·
[ilerleme](PROGRESS.md) · [geliştirme günlüğü](docs/gelistirme-gunlugu/) ·
[değişiklikler](CHANGELOG.md) · [güvenlik](SECURITY.md) · [katkı](CONTRIBUTING.md)

Lisans: [MIT](LICENSE).
