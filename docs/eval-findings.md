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

## 4. Python, HTML, CSS (Faz 18)

Faz 16'da eklenen diller için 36 yeni incelenmiş örnek (dil başına 12; dev 5 / test 7; her
dilde 3 sözdizimi hatalı, 2 injection, 2 temiz). Koşular yalnızca bu dillerde
(`eval run --language python --language html --language css`); dil dökümü
`codementor eval breakdown <sonuç.json>`. Sürümler: prompt `v1+e485058f` · kurallar
`r1+286dfb2f` · şema `1.0`. Prompt ayarı yapılmadı; test bölümü bir kez (`--final`).
HTML/CSS'te karmaşıklık yok (ADR-0015): Big-O metrikleri yalnızca Python örneklerinden gelir.

| Koşu | Mod | Örnek | Şema (ilk / onarım sonrası) | Erken çıkış P / R | Big-O birebir | Denetim P / R / F1 | Satır doğruluğu | Sızıntı | Injection direnci | p50 / p95 (sn) | Token ort. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Yalnızca statik | static | 15 (dev) | — / — | 100% / 100% | 100% | 100% / 55% / 71% | 100% | 0% | — | 0.0 / 0.0 | — |
| Yalnızca statik | static | 21 (test) | — / — | 100% / 100% | 100% | 100% / 67% / 80% | 100% | 0% | — | 0.0 / 0.0 | — |
| claude-opus-5-5 | two_pass | 15 (dev) | 100% / 100% | 100% / 100% | 100% | 54% / 95% / 69% | 89% | 0% | 100% | 16.2 / 34.2 | 9530 |
| claude-opus-5-5 | two_pass | 21 (test) | 100% / 100% | 100% / 100% | 100% | 33% / 81% / 47% | 100% | 0% | 100% | 16.5 / 36.5 | 9665 |
| claude-opus-5-5 | single_pass | 21 (test) | 100% / 100% | 100% / 100% | 100% | 34% / 86% / 49% | 100% | 0% | 100% | 14.1 / 23.4 | 7328 |

Test bölümü, dil başına (denetim P / R / F1):

| Dil | Statik | two_pass | single_pass |
|---|---|---|---|
| Python | 100% / 83% / 91% | 46% / 100% / 63% | 50% / 100% / 67% |
| HTML | 100% / 50% / 67% | 23% / 83% / 36% | 22% / 83% / 34% |
| CSS | 100% / 67% / 80% | 38% / 67% / 48% | 39% / 78% / 52% |

LLM'e giden 42 örneğin (3 koşu; sözdizimi hatalılar LLM'e gitmez) hepsi hatasız (`degraded` 0); şema ilk denemede %100.

- **Erken çıkış ve injection:** 9 sözdizimi hatalı örneğin hepsi Tier 0'da yakalandı; 6 injection
  örneğinin (Türkçe ve İngilizce, Python `#`, HTML `<!-- -->`, CSS `/* */` yorumu) hepsinde
  direnç %100, sızıntı %0 (kod bloğu ya da çözüm parçası çıkmadı).
- **Big-O (Python):** Big-O etiketli örneklerde statik ipucu ve LLM test 2/2, dev 4/4 birebir
  (diğer Python örnekleri sözdizimi hatalı ya da dosya düzeyinde tek karmaşıklık yok).
- **Recall:** CSS'teki kaçırmalar (`css-005`, `css-009`, `css-011` sabit boyut/ortalama) satır
  doğru bulunup `design` yerine `edge_case`/`maintainability` kategorisiyle raporlandı; Faz 12'deki
  kategori belirsizliğinin aynısı. Gerçekten bulunmayanlar: `html-009` başlık düzeyi atlama (h1→h4)
  ve `html-004` başlık yerine `div` (dev); ikisi de "anlamsal yapı" gözlemi.
- **Precision:** HTML'de en düşük (22–23%; HTML FP'leri two_pass / single_pass `edge_case` 7 / 7,
  `design` 5 / 6). Üç dilin test toplamında da FP'lerin başı `edge_case` (15 / 14) ve `design`
  (7 / 9): etiketlenmemiş küçük gözlemler (eksik `meta charset`, `onclick` adlandırması,
  form doğrulaması). İşaretleme dillerinde LLM'in "iyi uygulama" önerileri bulgu olarak geliyor.
- **two_pass vs single_pass:** C ailesindeki gibi kalite eşit (F1 47 vs 49), single_pass p95
  %36, token %24 daha düşük.
- **Ortam notu:** tam bir HTML belgesinde eşi olmayan `</div>` Tier 0'da hata sayılmıyor
  (tree-sitter-html hoşgörülü); veri setinde bu örnek yakalanan bir hatayla değiştirildi.

**Faz 17 kurallarının eski veri setine etkisi** (dev, C/C++/C#/Unity/Unreal, static-only): denetim
P / R / F1 100 / 38 / 55 → 85 / 46 / 59. İki "yanlış pozitif" aslında etiketlenmemiş doğru
bulgular: `c-008` NULL denetimsiz `malloc` (C-MEM-003), `csharp-009` döngüde `Average()`
(CS-ALLOC-002). Etiketler bu fazda değiştirilmedi; Faz 21'de eklendi (§5).

## 5. Faz 21 güncellemesi: statik taban çizgisi (C ailesi)

Kullanıcı kararıyla Faz 17 kurallarının bulduğu iki doğru bulgu dev etiketlerine eklendi
(`c-008` 4. satır `memory_safety` C-MEM-003, `csharp-009` 11. satır `garbage_collection`
CS-ALLOC-002). Faz 17-21 kuralları ve maliyet tablosu düzeltmeleriyle static-only koşular C ailesi
için yeniden yapıldı (`eval run --static-only --language c --language cpp --language csharp`);
README tabloları bu dosyalardan gelir. LLM satırları Faz 12'de eski etiketlerle hesaplanan
metriklerini korur (yeniden koşulmadı).

| Bölüm | Big-O birebir | Denetim P / R / F1 | Önce (Faz 12) |
|---|---|---|---|
| dev (31) | 96% | 100% / 50% / 67% | 92%, 100 / 38 / 55 |
| test (49) | 91% | 84% / 44% / 58% | 88%, 100 / 42 / 59 |

- **Recall** her iki bölümde arttı (yeni kurallar: C-IO/C-UB/C-MEM-002/003, CPP-SP/PERF,
  CS-ALLOC-002, UNITY-PERF-002, UE-MEM-001; `IList` ve `GetAllActorsOfClass` maliyetleri).
- **Test precision %84:** tek kaynak `c-016` 12. satır (`s->data = realloc(s->data, …)`):
  C-MEM-002 ve C-MEM-003 doğru bulgular ama etiket bu satırı `resource_leak` olarak işaretliyor
  (Faz 12 kullanıcı kararı); kural tablosu (§8.2) C-MEM-002'yi `memory_safety` sayar. Kategori
  uyuşmazlığı hem FP hem FN üretir; test etiketi değiştirilmedi (kullanıcı kararı bekliyor).


## 6. Faz 22 Aşama A: precision analizi (dev, çevrimdışı)

`codementor eval analyze <sonuç.json>` ile mevcut dev koşuları yeniden incelendi (LLM çağrısı
yok). Etiketler güncel veri setinden geldiği için katı metrikler kayıtlı Faz 12 değerlerinden
biraz farklıdır: Faz 21'de eklenen iki etiket (`c-008` C-MEM-003, `csharp-009` CS-ALLOC-002)
LLM koşularında FN olarak görünüyor (two_pass dev recall %92 → %85).

| Koşu (dev) | Katı P / R / F1 | Kategorisiz P / R | `low` hariç P / R | Tahmin / beklenen | Koruma |
|---|---|---|---|---|---|
| C ailesi two_pass | 27 / 85 / 41 | 32 / 100 | 40 / 85 | 82 / 26 | 2 |
| C ailesi single_pass | 32 / 88 / 46 | 36 / 100 | 43 / 88 | 73 / 26 | 6 |
| C ailesi two_pass, olgusuz | 28 / 92 / 42 | 30 / 100 | 40 / 92 | 87 / 26 | 6 |
| C ailesi two_pass, satır no.suz | 28 / 92 / 43 | 31 / 100 | 40 / 88 | 85 / 26 | 4 |
| Python/HTML/CSS two_pass | 54 / 95 / 69 | 57 / 100 | 63 / 60 | 35 / 20 | 1 |

"Koruma" yeni `guard_interventions` metriğidir. Sızıntı korumasının devreye girdiği örnek
sayısını verir ve ADR-0003'teki elle sayılmış değerlerle birebir tutar.

**Bulgular.**
- **Kategori karışıklığı küçük bir pay:** kategorisiz eşleşme precision'ı yalnızca 3–5 puan
  artırıyor (C ailesi two_pass: 60 FP'nin 4'ü). FP'lerin hepsi LLM kaynaklı, statik kurallar
  FP üretmiyor.
- **FP'lerin ana kaynağı fazla bulgu sayısı:** 26 beklenen bulguya karşı 82 tahmin var. FP
  kategorileri: `design` 17, `edge_case` 14, `input_handling` 10, `performance` 9.
- **`low` önemli bulgular FP'lerin %45'i (27/60).** Bunları atmak C ailesinde precision'ı
  %27'den %40'a çıkarıyor ve recall'u düşürmüyor. Python/HTML/CSS'te ise recall %95'ten %60'a
  iniyor, çünkü işaretleme dillerinde etiketli sorunların çoğunu model `low` olarak bildiriyor.
  Önem filtresi bu yüzden tek başına çözüm değil.
- **C ailesi two_pass'teki 60 FP elle sınıflandırıldı (yaklaşık):**
  - savunmacı girdi denetimi, 15: public metotta null parametre, negatif `n`, Inspector'da
    atanmamış alan gibi durumlar;
  - soru gereksinimi karşılanmamış (`design`, çoğu `high`), 8: kod istenen işlevi yapmıyor. Bu
    bulgular büyük olasılıkla doğru; etiketler yalnızca yerleştirilmiş hataları kapsıyor;
  - kuramsal uç değerler, 4: `INT_MIN`, 2³¹ satır, işaretli taşma;
  - kategori karışıklığı, 4;
  - kalan 29: mikro performans, stil ve en iyi uygulama önerileri. Bunların ~5'i gerçek ama
    etiketsiz hata: `c-012` baş işaretçinin değerle geçirilmesi, `cpp-009` beşler kuralı,
    `unity-011` yerçekimi, `unreal-011` açık kalan Tick, `c-007` çakışan bellek.
- **Python/HTML/CSS** (16 FP): 8'i `edge_case`; bunların 4'ü eksik `viewport`/`charset`
  meta etiketi, kalanlar sınır durumu ayrıntıları.

**Aşama B için somut prompt önerisi** (yalnız dev'de ölçülecek):
1. Kategori tanımları: `input_handling` yalnızca dışarıdan gelen girdi için (stdin, dosya,
   ağ, kullanıcı) ya da soru o girdiyi tanımlıyorsa kullanılır; iç/public metot
   parametresinin null denetimi bulgu değildir. `edge_case`, sorunun girdi alanında
   bulunan durumlar içindir (boş dizi, `n = 0`); `INT_MIN` veya 2³¹ gibi kuramsal uç değerler
   bu kapsama girmez, soru aralık vermediği sürece raporlanmaz.
2. `design` yalnızca (a) soru gereksinimi karşılanmadığında ya da (b) yapısal bir sorun hataya
   yol açtığında kullanılır. Stil ve "daha iyi olabilir" önerileri bulgu değildir.
3. Önem disiplini: `low` önemde en fazla 2 bulgu, ve bunlar da yalnızca gerçek sorunlar için.
   İşaretleme dillerinde "sorun" ölçütü: görüntülemeyi, erişilebilirliği ya da standardı
   bozuyorsa sorundur, bozmuyorsa öneridir.
4. Python için tek bir few-shot örneği.

**Kullanıcı kararı gereken nokta:** soru gereksinimi karşılanmadığı için bildirilen `design`
bulgularının (~8) dev etiketlerine eklenip eklenmeyeceği. Etiketlemek precision'ı doğrudan
yükseltir ama Faz 12 sayılarıyla doğrudan kıyası bozar.

## 7. Faz 22 Aşama B: precision için prompt ayarı (dev, canlı)

Yalnızca dev bölümünde ayarlandı; test bölümüne dokunulmadı. Model `claude-opus-5-5`
(`claude_cli`), two_pass, prompt `v1+fdc16030`.

**Etiket değişikliği (kullanıcı kararı).** C ailesinde soruya bağlı 7 dev örneği tek bir hatayı
içeren kısa parçalar; model bu örneklerde sorunun karşılanmamış gereksinimlerini (eksik işlev,
yanlış değer) doğru biçimde buluyordu. Bu bulgular etiketlere eklendi: `c-012`, `cpp-009`,
`cpp-014`, `unity-009` (×2), `unreal-007`, `unreal-009`, `unreal-011` (+ tick kapanmıyor,
`performance`). Konum kuralı prompt'la aynı: somut bir değer yanlışsa o satır, istenen işlev hiç
yoksa dosyadaki ilk sınıf ya da fonksiyon bildirimi. `unreal-011` artık "temiz" örnek değil.
Python/HTML/CSS örnekleri kendi sorularını karşılıyor; değişmedi. Statik dev satırı güncel
etiketlerle yeniden koşuldu (recall %50 → %37: eklenen gereksinim bulgularını statik kurallar
bulamaz).

**Prompt değişiklikleri.**
- "Sorun" ölçütü: yalnızca yanlış sonuç, çökme, tanımsız davranış, sızıntı, ölçülebilir
  performans kaybı ya da karşılanmamış gereksinim. Stil ve savunmacı öneriler bulgu değil.
- Kod dilleri için kategori tanımları (önceden yalnızca HTML/CSS'te vardı): `input_handling`
  yalnızca dış girdi; `edge_case` gerçekçi girdi alanı (kuramsal uç değer yok); `design`
  yalnızca eksik/yanlış istenen işlev ya da hataya yol açan yapı; soru bir süre veya girdi
  şartı koyuyorsa o sorunun kendi kategorisi.
- Önem tanımları, `low` en fazla 2, toplam en fazla 6 bulgu (önceden 10).
- HTML/CSS için "sorun mu öneri mi" ölçütü.
- İlk Python few-shot örneği (`python_none_window_sum`; dev/test ile çakışmaz).

**Ayar turları** (güncel etiketlerle, `eval analyze`):

| Koşu (dev) | C ailesi P / R / F1 | Tahmin | Python/HTML/CSS P / R / F1 | Tahmin |
|---|---|---|---|---|
| Önce (Faz 12/18 prompt'u) | 34 / 80 / 48 | 82 | 54 / 95 / 69 | 35 |
| 1. tur | 58 / 80 / 67 | 48 | 62 / 80 / 70 | 26 |
| 2. tur (son) | **67 / 86 / 75** | 45 | **68 / 85 / 76** | 25 |

İlk tur sonuçları `eval/results/iterations/` altındadır (README tablosunda yok). İlk turda
prompt'a eklenen bir kategori eşlemesi ("sıfıra bölme → `undefined_behavior`, sarkan işaretçi →
`memory_safety`") veri setinin etiketleriyle çelişti ve 3 doğru bulguyu kaçırttı; ikinci turda
kaldırıldı. `design` tanımı da soru performans/girdi şartı koyduğunda yanlış kategoriye
çekiyordu; düzeltildi.

**Son durum (2. tur).**
- Big-O birebir %96, satır doğruluğu %100, sızıntı %0, injection direnci %100, şema %100.
- p50 17,5 sn (önce 23,5), token ortalaması 13,4 bin (önce 14,2 bin).
- Sızıntı korumasının müdahalesi C ailesinde 6 örnek (önce 2). Son çıktıdaki sızıntı yine %0.
  Artışın sebebi ölçülmedi (gereksinim bulguları soru metnine yakın olabilir); Faz 35'te izlenir.
- Dil başına: C 89/100/94, C++ 80/100/89, C# 67/80/73, Unity 50/83/62, Unreal 50/62/56;
  CSS 82/100/90, HTML 56/71/63, Python 60/75/67.
- Kalan 15 FP'nin (C ailesi) ~5'i Unity/Unreal'da null denetimi (`GetComponent`,
  `FindObjectOfType`, Inspector alanı), 3'ü kategori karışıklığı (`memory_safety` ↔
  `undefined_behavior`: etiketler de bu sınırda tutarsız, ör. `unreal-009` vs `unreal-014`),
  ~4'ü gerçek ama etiketsiz (ör. `cpp-009` beşler kuralı).
- Few-shot 0/1 ablasyonu koşulmadı (Faz 34).

**Sonraki adımlar:** bulgu doğrulama geçişi (Faz 35), hatalar/öneriler ayrımı (Faz 36);
`memory_safety` / `undefined_behavior` etiket sınırının netleştirilmesi (dev etiket kararı).

## 8. Faz 32: statik kural doğruluğu II (C ailesi, statik taban çizgisi)

Statik koşu (`eval run --static-only --language c --language cpp --language csharp`) dev ve
test'te yeniden yapıldı (LLM yok; test bölümünü kirletmez):

| Bölüm | Big-O birebir | Denetim P / R / F1 |
|---|---|---|
| test (49), Faz 21 | 91% | 89% / 46% / 61% |
| test (49), Faz 32 | **97%** | **90% / 49% / 63%** |
| dev (31) | 96% → 96% | 100% / 37% / 54% (değişmedi) |

- Big-O artışı döngüde metin biriktirmeden geliyor: C# `s += x` / `s = s + x` ve C++
  `s = s + x` artık tur başına O(n) sayılıyor (C++ `s += x` yerinde büyüdüğü için O(n) kalır).
- Denetim artışı: aynı dosyadaki fonksiyona ödünç verilen işaretçinin sızıntısı (C-MEM-001),
  `TArray`/`TMap`/`TSet` içindeki UObject alanları (UE-GC-001).
- p95 gecikmesi 0,1 → 0,5-0,6 sn: Faz 29'da geliştirici makinesine kurulan zig ile Tier 1'in
  C++ denetiminden (Tier 1 kapalıyken yine 0,1 sn; metrikler aynı).

## 9. Faz 34 ve Faz 35B: ikinci model, doğrulama geçişi, few-shot ablasyonu (dev, canlı)

Yalnızca dev bölümü (46 örnek: C ailesi 31 + Python/HTML/CSS 15), `claude_cli`, önbellek kapalı,
prompt `v1+14a294f9`, kurallar `r1+d1852061`. Test bölümüne dokunulmadı. Taban: Opus two_pass
(2026-10-03, Faz 33 sonrası kod).

| Koşu (dev, 46) | Denetim P / R / F1 | Big-O birebir | Satır | p50 / p95 (sn) | Token ort. | Koruma müdahalesi |
|---|---|---|---|---|---|---|
| Opus two_pass (taban) | 69 / 89 / 78 | 93% | 98% | 17,9 / 36,1 | 14,1 bin | 11 |
| Opus two_pass + **doğrulama** | **79 / 89 / 84** | 93% | 98% | 22,1 / 38,3 | 15,9 bin | 6 |
| Opus two_pass, few-shot 0 | 68 / 91 / 78 | 97% | 98% | 19,3 / 33,9 | 13,7 bin | 11 |
| Opus two_pass, few-shot 1 | 68 / 89 / 77 | 93% | 98% | 16,9 / 28,3 | 12,6 bin | 8 |
| Haiku 4.5 two_pass (thinking=0) | 45 / 78 / 57 | 97% | 88% | 14,7 / 32,3 | 14,9 bin | 16 |
| Haiku 4.5 single_pass (thinking=0) | 48 / 78 / 59 | 100% | 84% | 14,3 / 66,9 | 17,2 bin | 11 |

Bütün koşularda hata 0, sızıntı %0, injection direnci %100.

**Doğrulama geçişi (Faz 35B, ADR-0019).** Precision 69 → 79, recall değişmedi (89), F1
78 → 84. Bedeli: p50 gecikme ~%24, token ~%13. Rapordaki toplam bulgu 71 → 62 (iki ayrı koşu;
model çıktısı koşudan koşuya değişir), recall aynı kaldı. Sızıntı korumasının müdahalesi 11 → 6 (düşen bulgular Sokratik sorulara
da girmiyor). Güven eşiği (`eval analyze`) F1'i artırmıyor: ≥ 0,85 eşiği P'yi 90'a çıkarıyor ama
R 78'e düşüyor (F1 83). **Karar:** `pipeline.verify_findings` varsayılanı açık, güven eşiği yok.

**İkinci model (Faz 34, ADR-0003).** API anahtarı olmadığından ikinci model `claude_cli` ile
Claude Haiku 4.5. CLI bu modelde uzun düşünme açıyordu (örnek başına ~176 sn, ~44 bin token);
`providers.claude_cli.thinking_tokens = 0` (`MAX_THINKING_TOKENS`) ile ~15 sn'ye indi. Haiku'da
F1 57-59: precision belirgin düşük (45-48), satır doğruluğu %84-88. two_pass ile single_pass
arasında anlamlı fark yok (2 puan, ~1 örnek). ADR-0003'ün "zayıf modelde doğrulanmamış bulgu
soruya dönüşür" kaygısı bu ölçümde ayırt edici çıkmadı. Haiku two_pass'te sızıntı korumasının
müdahalesi en yüksek (16) ama son çıktıda sızıntı %0: koruma çalışıyor ve zayıf modelde daha çok
iş yapıyor. Varsayılan model Opus kalır.

**Few-shot ablasyonu (§14.4).** 0, 1 ve 2 örnek (taban) arasında denetim F1'i 77-78; fark
gürültü düzeyinde. Big-O ve satır doğruluğu da değişmiyor. Few-shot'ların bu modelde ölçülebilir
katkısı yok; çıktı biçimini ve "statik bulguyu tekrar etme" davranışını öğretmek için (Faz 8)
2 örnek varsayılan kalır. Zayıf modellerde etkisi ölçülmedi.

**Sınır.** Dev 46 örnek; bir örnek yaklaşık 2 puan eder. Dev setini yeni sorulardan büyütmek
etiket incelemesi gerektirdiği için yapılmadı (PROGRESS "Sonraya").

## 10. Dev genişletmesi: 46 → 96 örnek (2026-10-04, statik)

50 yeni örnek `docs/EVAL_ORNEK_REHBERI.md` ile dış yazara yazdırıldı, `check-drafts` ve elle
incelemeden sonra `eval promote` ile dev'e taşındı (C/C++/C#/Python 6'şar, Unity/Unreal 8'er,
HTML 6, CSS 4; 12 sözdizimi hatalı, 6 injection, 9 temiz, 23 hatalı).

**İnceleme düzeltmeleri.** `check-drafts` başta hepsine "uyumlu" diyordu ama ±2 satır toleransı
yüzünden 6 örnekte 1 satırlık kaymayı göstermedi (statik kural satırıyla birebir karşılaştırılıp
düzeltildi). İki "temiz" örnek aslında hatalıydı: `cpp-103` son turdaki gereksiz kare alma
yüzünden sonuç sığsa da işaretli taşma yapıyordu (`base=2, exp=32`); `unreal-106`'da kurucu
olmadığından `bCanEverTick` kapalıydı ve etiketlenen `Tick` sorunu hiç oluşmazdı. `unity-103`'e
`Update` içinde `AddForce` (kare hızına bağlı kuvvet) bulgusu eklendi. Her yanıtta geçebilecek
`must_not_contain` parçaları (`"}"`, `");"`, `"UPROPERTY()"`) ayırt edici parçalarla değiştirildi.

**Statik koşu (96 örnek).** Big-O %97 (tek ıska eski `unreal-014`; yeni örneklerin hepsi
birebir), P / R / F1 100 / 58 / 73 (46 örnekte yok; 31 örnekte 100 / 37 / 54), satır doğruluğu
%100. Recall artışı yeni örneklerde statik kuralların yakaladığı türlerin oranının yüksek
olmasından; LLM satırları bu setle henüz koşulmadı, karşılaştırma için yeniden koşulmalı.

**Açık konular.** `cpp-105` (doğru eşleşmiş `new[]`/`delete[]`, `cpp-009` emsaline uyularak
CPP-OWN-001 ile `memory_safety`), `unreal-107` (`Reserve` yok) ve `python-105` (`with` dışında
`open`) kural kaynaklı, "öneri" sınırında bulgular; Faz 36'da hata/öneri ayrımında yeniden ele
alınmalı.
