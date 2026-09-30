# Eval bulguları (Faz 12)

Mimari §14. Tüm sayılar `eval/results/*.json` dosyalarından gelir; tablolar
`codementor eval compare` çıktısıdır. Sürümler: prompt `v1+fbc08625` · kurallar
`r1+d3065584` · şema `1.0`. Model: `claude-opus-5-5` (`claude_cli` sağlayıcısı; "yerel model"
satırları kullanıcı tercihiyle Ollama yerine bununla ölçüldü). Önbellek kapalı.

**Yöntem.** Veri seti 80 elle incelenmiş örnek: dev 31 / test 49; her dil/motor (C, C++, C#,
Unity, Unreal) 16; %25 sözdizimi hatalı, %12,5 prompt injection. Prompt'lar dev üzerinde
**ayarlanmadı** (Faz 8 prompt'ları olduğu gibi ölçüldü); test bölümü en sonda bir kez
(`--final`) koşuldu. Bulgu eşleşmesi: aynı kategori + satır farkı ≤ 2, bire bir.

Ortam notu: bu makinede gcc/clang yok; C/C++/Unreal örneklerinde Tier 1 `skipped`
(yalnızca tree-sitter). Sözdizimi hatalı örneklerin tümü Tier 0'da yakalandığı için erken
çıkış metrikleri etkilenmedi.

## 1. Ana karşılaştırma — dev (31 örnek)

| Koşu | Mod | Ablasyon | Şema (ilk / onarım sonrası) | Erken çıkış P / R | Big-O birebir / sınıf | Denetim P / R / F1 | Satır doğruluğu | Sızıntı | Injection direnci | p50 / p95 (sn) | Token ort. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Yalnızca statik (LLM yok) | static | — | — / — | 100% / 100% | 92% / 92% | 100% / 38% / 55% | 100% | 0% | — ¹ | 0.0 / 0.1 | — |
| claude-opus-5-5 | two_pass | — | 100% / 100% | 100% / 100% | 96% / 96% | 27% / 92% / 42% | 100% | 0% | 100% | 23.5 / 40.0 | 14219 |
| claude-opus-5-5 | single_pass | — | 100% / 100% | 100% / 100% | 92% / 92% | 32% / 96% / 47% | 96% | 0% | 100% | 13.1 / 24.5 | 9359 |
| claude-opus-5-5 | two_pass | facts | 100% / 100% | 100% / 100% | 85% / 92% | 28% / 100% / 43% | 96% | 0% | 100% | 20.5 / 42.3 | 13227 |
| claude-opus-5-5 | two_pass | line_numbers | 100% / 100% | 100% / 100% | 92% / 92% | 28% / 100% / 44% | 96% | 0% | 100% | 20.4 / 41.3 | 13861 |

¹ `compare` bu hücrede %0 yazar: statik modda LLM çağrılmadığı için metrik anlamlı değildir.

Tüm LLM koşularında LLM'e giden 26 örneğin 26'sı hatasız tamamlandı (`degraded` 0).
Onarım denemesi: two_pass 5, single_pass 1, facts ablasyonu 7.

### 1.1 LLM'in katma değeri (taban çizgisine göre)

- **Recall 38% → 92–96%.** Statik kurallar 24 beklenen bulgunun 9'unu bulur (hepsi doğru).
  LLM 22–23'ünü bulur; kategori yok sayıldığında **24/24** (kaçırdığı sorun yok).
- **Precision 100% → 27–32%.** Kalan kayıpların hepsi LLM kaynaklı ek bulgular. Dağılım
  (two_pass, 60 FP): `design` 17, `edge_case` 14, `input_handling` 10, `performance` 9,
  diğer 10. Çoğu yanlış değil, **etiketlenmemiş** küçük gözlemler (ör. `malloc` dönüşü
  kontrol edilmiyor, `int` bölmesi kesir kaybeder). Yalnızca orta ve üstü önemdeki bulgular
  sayıldığında precision **%40–43**.
- **Kategori belirsizliği** kaçan 1–2 bulgunun tek nedeni: C'de sıfıra bölme (`edge_case`
  vs `undefined_behavior`), null dereference (`edge_case` vs `memory_safety`).
- **Big-O:** statik ipucu 26 örneğin 24'ünde doğru; LLM two_pass statiğin kaçırdığı
  `unreal-014`'ü (`n^2`) ve `cpp-009`'u düzeltir, tek ıska `csharp-014` (`1` → `k`).

### 1.2 Ablasyonlar (§14.4)

**Statik olgular çıkarıldığında (`--ablate facts`):** Big-O birebir **96% → 85%**, sınıf
96% → 92%. Iskaların çoğu değişken adlandırması: model olgu listesindeki kanonik `n` yerine
kendi değişkenini yazıyor (`unity-007`: `n` → `m`, `unity-009`: `1` → `k`, `cpp-005`:
`n` → `n + s`). Olgular hem doğruluğu hem de gösterim tutarlılığını sağlıyor. Denetim
recall'u değişmedi (100%); sızıntı koruması 2 yerine 6 kez devreye girdi.

**Satır numaralı görünüm kapatıldığında (`--ablate line_numbers`):** satır doğruluğu
**100% → 96%** (eşleşen 24 bulgunun 1'inde satır 1–2 kaydı), recall/precision etkilenmedi.
Bu model için numaralı görünümün katkısı küçük ama yönü beklenen gibi; daha zayıf
modellerde etkinin büyümesi beklenir (ölçülmedi).

Few-shot 0/1 ablasyonu koşulmadı (kabul kriteri ≥ 2 ablasyon; kota sınırı).

### 1.3 two_pass vs single_pass

| | two_pass | single_pass |
|---|---|---|
| Big-O birebir | 96% | 92% |
| Denetim F1 | 42% | 47% |
| Satır doğruluğu | 100% | 96% |
| Sızıntı (son çıktı) | 0% | 0% |
| Sızıntı korumasının müdahale sayısı | 2 | 6 |
| p50 / p95 | 23.5 / 40.0 sn | 13.1 / 24.5 sn |
| Token ort. | 14.2 bin | 9.4 bin |

Kalite farkları 1–2 örnek düzeyinde (26 örnekte tek örnek ≈ 4 puan); anlamlı bir kalite
üstünlüğü yok. single_pass ~%45 hızlı ve ~%34 daha az token. Buna karşılık single_pass'te
sızıntı koruması (Faz 9/10) dev'de üç kat sık devreye girdi (6 vs 2); test'te fark küçük
(11 vs 9, §2). Toplamda LLM'e giden 60 örneğin **17'sinde vs 11'inde** (~1,5×): tek geçişte
model soruyu yazarken çözümü daha sık ele veriyor; son çıktıdaki %0 sızıntı bu korumanın
işi. Karar: ADR-0003.

## 2. Test bölümü (49 örnek, `--final`, tek sefer)

| Koşu | Mod | Şema (ilk / onarım sonrası) | Erken çıkış P / R | Big-O birebir / sınıf | Denetim P / R / F1 | Satır doğruluğu | Sızıntı | Injection direnci | p50 / p95 (sn) | Token ort. |
|---|---|---|---|---|---|---|---|---|---|---|
| Yalnızca statik (LLM yok) | static | — / — | 100% / 100% | 88% / 88% | 100% / 42% / 59% | 100% | 0% | — | 0.0 / 0.1 | — |
| claude-opus-5-5 | two_pass | 100% / 100% | 100% / 100% | 91% / 94% | 27% / 92% / 42% | 94% | 0% | 100% | 20.3 / 57.3 | 15673 |
| claude-opus-5-5 | single_pass | 100% / 100% | 100% / 100% | 94% / 97% | 32% / 94% / 48% | 94% | 0% | 100% | 13.5 / 35.7 | 10182 |

LLM'e giden 34 örneğin 34'ü hatasız (`degraded` 0); onarım denemesi two_pass 7, single_pass 2.
Bilgisayar two_pass koşusunda 21:21–21:54 arası uykuya geçti; `cpp-012`'nin 2036 sn'lik
süresi bu yüzden geçersiz. En yakın sıra yöntemiyle p95 49 değerin 47.'sini aldığı için
p50/p95 bu tek aykırı değerden etkilenmez.

Dev bulguları test'te de tutuyor:
- **LLM katma değeri:** recall 42% → 92–94%, kategorisiz eşleşmede **36/36**. Statik
  taban çizgisinin kaçırdığı 21 bulgunun tamamını LLM buluyor; kaçanlar yine kategori
  belirsizliği (`c-016` realloc sonrası kenar durumu, `cpp-008` UB).
- **Precision 27–32%**, orta+ önemde 35–37%. FP'lerin başı `edge_case` (24–28), `design`
  (18–20), `input_handling` (14–16): etiketlenmemiş küçük gözlemler.
- **Big-O:** statik 88% (4 ıska; `csharp-006`/`cpp-015` iç içe döngü `n^2`'yi kaçırıyor),
  LLM 91–94%; kalan ıskalar yine değişken adlandırması (`l*n`, `k`, `c*n`).
- **two_pass vs single_pass:** kalite yine eşit ya da single_pass lehine (F1 48 vs 42),
  single_pass p50 %34, token %35 daha düşük. Sızıntı koruması müdahalesi two_pass 9,
  single_pass 11.

## 3. Kararlar

- ADR-0003: bkz. `docs/adr/0003-iki-gecisli-prompt.md`.
- ADR-0003 özeti: varsayılan `two_pass` kalır; gerekçe kalite değil sızıntı korumasına
  daha az yaslanması (güvenlik payı). `single_pass` kalite kaybı olmadan hızlı mod.
- Precision'ı artırmak için (Sonraya): `design` bulgularını yalnızca soru
  gereksinimi varken üretmek; önem eşiği (`low` bulguları raporda ayrı göstermek).
