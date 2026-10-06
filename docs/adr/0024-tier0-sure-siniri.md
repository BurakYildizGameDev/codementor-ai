# ADR-0024: Tier 0 ayrıştırma süre sınırı

**Tarih:** 2026-10-06 · **Durum:** Kabul edildi; ADR-0025 ile güncellendi (isteğe bağlı alt süreç yalıtımı) ·
**Etkilenen bölümler:** mimari §4.3, §12; plan Faz 55

## Bağlam

Kullanıcı kodu güvenilmeyen veridir (mimari §12); 40 KB'a yakın kötü niyetli girdide Tier 0
ayrıştırmasının süresi PROGRESS "Sonraya"da açık riskti. tree-sitter **0.25.2**
(`pyproject.toml`: `>=0.25.2,<0.26`, Windows 11, Python 3.12) üzerinde iptal denemeleri
(Claude Code, 2026-10-05):

| Deneme | Sonuç |
|---|---|
| `parser.parse(bytes)`, `("a<" * 20000)` (40 KB C++) | ağaç döner, ~236 ms |
| `parser.timeout_micros = …` | `DeprecationWarning` |
| `parser.parse(bytes, progress_callback=cb)` | `UserWarning: progress_callback is ignored when parsing a bytestring` → etkisiz |
| `parser.parse(read_callback, progress_callback=cb)` | **süreç çöküyor (segfault)**; 6 KB geçerli C++'ta bile |

Faz 55 ölçümü (2026-10-06; betik ve tam tablo PROGRESS "Faz 55 — Notlar"): 600 satır /
40 KB sınırlarının içindeki patolojik girdilerde `run_tier0` + `extract_facts` uçtan uca
süreler:

- **C# `a<`×20000 (40 KB): `run_tier0` ~11,9 s** — sürenin tamamı parse'ın kendisi
  (tree-sitter-c-sharp grameri). Tier 0 boru hattında her zaman koştuğundan **erişilebilir**.
- `(`/`{`×40000 (C, C++, Python): parse hızlı (25–33 ms), sorgu katmanı
  (`QueryCursor.captures`, 5 sorgu) hatalı ağaçlarda ~5,5–7,6 s. Boru hattı Tier 0
  hatasında erken çıktığından (orchestrator `_analyze`) bu yol **erişilemez**; yalnızca
  `extract_facts`'ı doğrudan çağıran araçlar (eval, `python -m codementor.analysis.extractor`)
  kötü girdide bu maliyeti taşır.
- Geçerli derin iç içe girdiler (40 KB dengeli parantez, derinlik ~20.000): 118–182 ms.
- Diğer tüm girdiler < 0,8 s (en yüksek: HTML 40 KB kapanmamış `<div>`, 564 ms); sınıra
  yakın geçerli C++ (≈39 KB, 600 satır) 4,8 ms.

## Karar

1. **Süreç içi iptal yok.** `progress_callback` + okuma geri çağrısı yolu segfault,
   `timeout_micros` deprecation nedeniyle üretim koduna girmez (§1 tablosu).
2. **Koruma katmanları değişmez:** 600 satır / 40 KB boyut sınırı (K0), ayrıştırmanın
   `asyncio.to_thread` içinde koşması (Faz 26), toplam analiz süresi sınırı
   `pipeline.analysis_timeout_s` (Faz 48), API eşzamanlı analiz sınırı (4, Faz 47).
3. **Ölçülen en kötü erişilebilir durum kabul edilir** (kullanıcı kararı, 2026-10-06):
   C# `a<`×20000 girdisi bir analiz iş parçacığını ~12 s meşgul eder. Araç yereldir;
   bu yalnız kasıtlı kötü niyetli girdiyle tetiklenir, süreci çökertmez (CPU meşguliyeti),
   eşzamanlılık sınırı etkiyi sınırlar ve sistem kendini kurtarır.
4. **Gerileme testi** (`tests/unit/test_tier0_budget.py`): ölçülen sınırlı girdiler
   `run_tier0 < 1,5 s` ile sabitlenir (kapsamda yavaşlama varsa 4× tolerans, Faz 53
   `_deadline` kalıbı). C# `a<` vakası süresi ve karar 3 gereği **bilinçli olarak kapsam
   dışıdır**; bu gerekçe test dosyasında ve PROGRESS'te yazılıdır. Ayrıca sınıra yakın
   geçerli C++ dosyasının hatasız ayrıştırıldığı sabitlenir.
5. Plandaki **"zaman sınırı aşılırsa kısmi olgu üretme" maddesi geçersizdir**: bu yolda
   süre sınırı yoktur; dolayısıyla kısmi olgu durumu da yoktur.

## Sonuçlar

- 40 KB'lık kasıtlı C# girdisi yerel API'de kısa süreli yavaşlamaya yol açabilir (4 eşzamanlı
  analizle sınırlı); çökme veya kalıcı hasar yoktur.
- `extract_facts`'ın hatalı ağaçlardaki sorgu maliyeti boru hattında erişilemez; doğrudan
  çağıranlarda kötü girdi ~7,5 s'ye kadar sürebilir.
- tree-sitter sürümü yükseltildiğinde (≥ 0.26) iptal mekanizmaları ve gramer/sorgu
  performansı yeniden değerlendirilmelidir.
- Parse'ı sert zaman aşımıyla alt süreçte izole etme fikri Sonraya'dadır; gerekirse ayrı faz.
