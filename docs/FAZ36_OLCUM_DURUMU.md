# Faz 36 ve dev ölçümü (parça 3/4–4/4): durum özeti

**Tarih:** 2026-10-04 · **Dal:** `faz/36-hata-oneri` (main'e birleştirilmedi, push yok) ·
**İlgili:** ADR-0022, `docs/EVAL_PARCA_REHBERI.md`, `docs/eval-findings.md` §11,
`docs/CODEX_3_4_YAPILANLAR.md`

Kısa cevap: **Faz 36'nın ölçümü tamamlandı (2026-10-05, §7).** Claude Opus 96 örnek:
**77 / 88 / 82**. Öneri sınıfı precision'ı artırmadı, ama recall'u da düşürmedi: hiçbir gerçek
hata öneriye düşmedi. §1-6 ölçüm yarımken yazıldı; güncel karar §7'de.

---

## 1. Faz 36 ne yaptı?

**Sorun:** Model, gerçek hataların yanında "olsa iyi olur" türünden önemsiz bulgular da
üretiyordu. Bunlar yanlış alarm (FP) sayılıyor, precision'ı düşürüyor ve öğrencinin dikkatini
asıl hatadan dağıtıyordu. Bu bulguları silmek ise bilgi kaybı demekti.

**Çözüm (ADR-0022):** Her bulguya bir tür alanı eklendi: `kind: "issue" | "suggestion"`.

| | Hata (`issue`) | Öneri (`suggestion`) |
|---|---|---|
| Ne zaman | Gerçek hata, gereksinim ihlali | Düşük önemli iyileştirme, ihlal yok |
| Sokratik sorular | Bunlardan üretilir | Kullanılmaz |
| Doğrulama geçişi | Girer | Girmez |
| Arayüz | "Hatalar" bölümü | Katlanmış "Öneriler" bölümü (SARIF'te `note`) |
| Eval metrikleri | P/R/F1 bunlarla hesaplanır | Ayrı sayılır (`suggestions_total`) |

Ayrıca: statik kural bulguları her zaman hatadır. Şema 1.1 oldu (1.0 raporlar hâlâ okunuyor).
Her dil ailesine "temiz kod, bulgu yok" ve "öneri" few-shot örnekleri eklendi.

**Hedef iki cümleydi:**
1. Precision artmalı (önemsiz bulgular artık FP sayılmıyor).
2. **Kaçırma oranı düşmemeli**, yani recall korunmalı. Gerçek bir hata "öneri" sınıfına düşüp
   gözden kaçmamalı.

Commit'ler: `b221c0e` (özellik), `1151440` (`eval run --part k/n`), `d990099` ve `6707229`
(Claude parça 1 ve 2), `2f51cdc` (`unity-104` etiket düzeltmesi), `2638c9e` (Codex ölçümü).

---

## 2. Ölçüm neden parçalı?

96 örneklik dev seti tek seferde ~0,6–0,7M token harcıyor. Bütçe yüzünden
`eval run --part k/4` ile dört dengeli parçaya (24'er örnek) bölündü. Parçalar ayrı ayrı koşulup
sonra güncel etiketlerle birleştirilir (birleştirme betiği: rehber §4.2).

---

## 3. Şu ana kadar ne ölçüldü?

### 3.1 Claude Opus 5.5: asıl ölçüm (yarım)

| Parça | P / R / F1 | Öneri | Durum |
|---|---|---|---|
| 1/4 | 71 / 77 / 74 | 9 | ✅ koşuldu |
| 2/4 | 78 / 90 / 84 (güncel etiketle 78 / 86 / 82) | 5 | ✅ koşuldu |
| 3/4 | — | — | ❌ **koşulmadı** |
| 4/4 | — | — | ❌ **koşulmadı** |
| 1+2 (48 örnek) | **75 / 81 / 78** (güncel etiket) | 14 | — |

### 3.2 Codex `gpt-6-luna`: alternatif ölçüm (tam)

Claude CLI Codex'in ortamında çalışmadı. Codex tutarlı kalsın diye **dört parçanın hepsini**
kendi modeliyle koştu, Claude'un daha önce koştuğu 1/4 ve 2/4 dahil. Prompt, kural ve şema
sürümleri Claude koşularıyla aynı (`v1+7205d091`, `r1+d1852061`, 1.1). Etiket ve kod
değiştirilmedi. Rakamlar Claude tarafından bağımsız betikle yeniden hesaplandı ve tuttu.

| | P / R / F1 |
|---|---|
| Parça 1 / 2 / 3 / 4 | 71/65/68 · 84/80/82 · 79/79/79 · 81/85/83 |
| **96 örnek** | **79 / 77 / 78** (19 FP, 21 FN), 1 öneri |
| Kategori yok sayılınca | 89 / 87 / 88 |

Dillere göre F1: CSS 90, HTML 87, Unity 83, C 80, C# 78, Python 77, **C++ 64, Unreal 61**.

### 3.3 Aynı prompt, iki model (parça 1+2, 48 örnek)

| Model | P / R / F1 | Öneri | Token/örnek |
|---|---|---|---|
| Claude Opus 5.5 | 75 / **81** / 78 | **14** | ~14 bin |
| Codex gpt-6-luna | **79** / 72 / 76 | **1** | ~39 bin |

---

## 4. Neden "çözüldü" diyemiyoruz?

1. **Codex ölçümü Faz 36'yı sınamıyor.** Faz 36'nın özü öneri sınıfı. Codex 96 örnekte yalnız
   1 öneri üretti, yani mekanizmayı neredeyse hiç kullanmadı. Faz 36'yı test etmek için öneri
   sınıfını kullanan bir model, yani Claude, gerekiyor.
2. **Model farklı olunca kıyas nedensel değil.** Faz 35B tabanı (Faz 36 öncesi) Claude Opus ile
   ölçüldü: ortak 46 örnekte 79 / 89 / 84. Codex aynı örneklerde 75 / 73 / 74 verdi. Bu farkın
   ne kadarı Faz 36'dan, ne kadarı modelden geliyor, ayrılamaz.
3. **Claude yarısı tek başına kararsız.** 48 örnekte 75 / 81 / 78. Faz 35B ile ortak 25 örnekte
   Claude Faz 36 öncesi 80 / 83 / 81, sonrası 71 / 76 / 73. Bu, recall'da düşüş *eğilimi*
   gösteriyor ama 25 örnek kesin karar için az.

**Sonuç:** Faz 36'nın iki hedefi (precision arttı mı, recall korundu mu) için Claude ile
parça 3/4 ve 4/4 gerekli.

---

## 5. Ölçümün yan ürünü: iki gerçek sorun

### 5.1 Doğrulama geçişi doğru bulguları atıyor (→ Faz 39)

Doğrulama geçişi (Faz 35, ADR-0019) her hata için "somut girdiyle kanıt" istiyor. Codex
koşusunda 10 bulgu "kanıtlayamadı; bulgu atıldı" diye düşürüldü. Bunların **en az 5'i gerçek
hataydı** ve FN listesine geçti:

| Örnek | Satır | Etiketli kategori |
|---|---|---|
| `cpp-009` | 20 | memory_safety |
| `unreal-014` | 9 | undefined_behavior |
| `c-103` | 5 | memory_safety |
| `unreal-108` | 13 | engine_best_practice |
| `unreal-007` | 8 | design |
| `unity-009` (olası) | 15–16 | garbage_collection |

Yani 21 FN'nin yaklaşık dörtte biri buradan geliyor. Claude parça 2'deki `cpp-007` (performans,
döngüde `erase`) aynı sorunun bilinen örneğiydi.

**Önemli not:** Faz 39 planı yalnız performans/GC için "ölçek kanıtı" ekliyor. Yukarıdaki
düşürmelerin çoğu ise memory_safety, undefined_behavior, design ve engine_best_practice
kategorisinde. Faz 39 kapsamı bunu dikkate almalı.

### 5.2 Kategori karışıklığı (→ Faz 40)

Kategori yok sayılınca F1 78'den 88'e çıkıyor. Model çoğu zaman doğru satırı buluyor ama farklı
kategori seçiyor. En sık karışanlar: `undefined_behavior` ↔ `memory_safety` (`cpp-005`,
`cpp-102`, `cpp-106`) ve `edge_case` ↔ başka kategoriler (`csharp-009`, `csharp-106`,
`python-008`).

### 5.3 `unity-104` önerisi

Codex'in tek önerisi (satır 13: girdinin `FixedUpdate` içinde okunması) eşleştiricide satır
14'teki etiketli hatayla (velocity ataması yerçekimini iptal ediyor) aday çakışma gibi göründü.
Elle incelendi: konular farklı, gerçek hata öneriye düşmemiş.

---

## 6. Kalan iş: nasıl tamamlanır?

**Seçenek A: hemen tamamla (token yenilenince).** ~0,6M token, ~20 dk:

```powershell
uv run codementor eval run --split dev --provider claude_cli --mode two_pass --part 3/4
uv run codementor eval run --split dev --provider claude_cli --mode two_pass --part 4/4
```

Uyku engelleyiciyle koş (rehber §3). Sonra rehber §4.2 betiğinde glob'u
`*_claude_cli_claude-opus-5-5_two_pass_part*-4_dev.json` yapıp birleştir.

**Seçenek B (önerilen): Faz 39'dan sonra tek seferde ölç.** Faz 39 doğrulama geçişini
değiştirecek, bu yüzden bugünkü Claude parça 1–2 sonuçları zaten eskiyecek. Faz 39 bitince
96 örneğin dördünü Claude ile tek seferde koşmak hem Faz 36 hem Faz 39 için güncel bir sonuç
verir ve tokenı bir kez harcar. Bunun bedeli şu: Faz 36'nın etkisi Faz 39'dan ayrı ölçülemez.
Faz 36'yı tek başına görmek istersek A seçeneği gerekir.

**Karar ölçütü** (hangisi seçilirse seçilsin, 96 örnek Claude):
- Precision Faz 35B'nin 79'unun üstündeyse ve recall 89'a yakınsa (±3): Faz 36 başarılı.
- Recall belirgin düştüyse: önerilere düşen gerçek hataları rehber §4.2 eşleştiricisiyle bul,
  elle incele ve prompt'taki öneri tanımını daralt.

---

## 7. Sonuç (2026-10-05): ölçüm tamamlandı

**Koşular:** Parça 3/4 (`20261004T223206`) ve 4/4 (`20261004T223841`), Claude Opus 5.5,
`two_pass`, Faz 39 kodu (prompt `v1+a4c5ebfc`). Fark yalnız `verify.system.j2`: parça 1-2
`v1+7205d091` ile koşulmuştu.

**Parça kayması:** `select_part` bölmeyi etiketlere göre yapıyor. Parça 1-2 koşulduktan sonra
`unity-104` etiketi değişti (`2f51cdc`), bu da atamayı kaydırdı. Sonuç: 3/4 ve 4/4, 1-2 ile
3 örnekte çakıştı (`unity-009`, `unity-106`, `unreal-105`; skorlar her iki koşuda aynı) ve
3 örnek hiç koşulmadı (`unity-014`, `unity-105`, `unreal-007`). Eksik 3 örnek ayrıca koşuldu
(`20261004T224756_..._missing3_dev.json`). Birleşimde çakışan örneklerin parça 1-2 koşusu
kullanıldı. Codex'in dört parçası düzeltmeden sonra koşulduğu için kendi içinde tutarlı.

| | P / R / F1 | TP / FP / FN | Öneri |
|---|---|---|---|
| **Claude 96 (birleşik)** | **77 / 88 / 82** | 80 / 24 / 11 | 32 |
| Claude parça 1+2 (48, Faz 39 öncesi) | 75 / 81 / 78 | | 14 |
| Claude yeni koşular (51, Faz 39) | 76 / 94 / 84 | | 20 (çakışanlar dahil) |
| Codex gpt-6-luna 96 | 79 / 77 / 78 | 70 / 19 / 21 | 1 |

Dillere göre F1 (Claude 96): CSS 93, C 92, Python 86, Unreal 85, HTML 83, C++ 74, C# 74,
**Unity 69**.

**Faz 36 kararı (Faz 35B ile ortak 46 örnek):**

| | P / R / F1 | TP / FP / FN |
|---|---|---|
| Faz 35 öncesi (doğrulama geçişi yok) | 69 / 89 / 78 | |
| Faz 35B (doğrulama geçişi, Faz 36 öncesi) | 79 / 89 / 84 | 49 / 13 / 6 |
| Faz 36 sonrası | 76 / 85 / 80 | 47 / 15 / 8 |

- **Precision artmadı** (79 → 76, 2 FP fazla). §6 ölçütü karşılanmadı.
- **Recall korundu sayılır.** Öneri↔etiket eşleştiricisi 32 önerinin hiçbirinde etiketli hata
  bulmadı, yani gerçek hata öneriye düşmedi. 2 FN farkının kaynağı Faz 36 değil:
  - `cpp-007`: doğrulama geçişi performans bulgusunu attı. Parça 2, Faz 39 öncesi koşulmuştu.
    Güncel kodla tek örnek yeniden koşuldu (`20261004T225020_..._cpp007-faz39_dev.json`):
    bulgu korundu, düşürme uyarısı yok (1 TP). Bu düzeltmeyle recall 87 olur (±3 içinde).
  - `csharp-014` (resource_leak → garbage_collection) ve `unreal-014` (undefined_behavior →
    memory_safety): doğru satır, farklı kategori → Faz 40.
- Fark 46 örnekte 2 TP / 2 FP. Tek koşunun gürültüsü bu düzeyde (§4.3), yani etki "nötr".

**Özet cümle:** Faz 36 öneri sınıfı gerçek hataları yutmadan 32 düşük önemli bulguyu ayırıyor.
Ancak bunu precision artışına çeviremedi: kalan FP'ler önemsiz bulgu değil, kategori karışıklığı
ve gerçek yanlış alarm. Sıradaki kazanç Faz 40'ta (kategori tutarlılığı).
