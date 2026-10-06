# ADR-0026: İpucu merdiveninin yalnız sayılan denemelerle ilerlemesi

**Tarih:** 2026-10-06 · **Durum:** Kabul edildi · **Günceller:** ADR-0008, ADR-0015 ·
**Etkilenen bölümler:** mimari §5.4.3, §6.2, §11; plan Faz 61

## Bağlam

CodeMentor AI'da ipucu merdiveni, öğrencinin her gönderiminde Sokratik rehberliğin doğrudanlığını
adım adım artırır (Seviye 1: yüksek seviye düşündürme → Seviye 3: somut çözüm ipucu).

Masaüstü el testlerinde (2026-10-06, bkz. `docs/GUNCELLEMELER.md`), başarısız olan bir Antigravity
çağrısı ("Model kullanılamadı", bozulmuş rapor) ipucu seviyesini 2 → 3'e taşımış; öğrencinin kodu
henüz hiç mentorluk almamışken Claude'un ilk analizi doğrudan Seviye 3 (en açık) ipucuyla
gelmiştir. Benzer biçimde, sözdizimi hatalarındaki erken çıkışlar (`early_exit`) ve aynı kodu
yalnızca farklı bir modelle denemek amacıyla yeniden "Denetle" düğmesine basmak da ipucu
seviyesini tüketmektedir.

İpucu merdiveninin pedagojik amacı öğrencinin **anlamlı deneme adımlarını** takip etmektir;
altyapı hataları veya yazım hataları öğrencinin ipucu hakkını harcamamalıdır.

## Karar

1. **K1 (Bozulmuş analiz sayılmaz):** LLM sonucu olmadan dönen analizlerde
   (`report.meta.degraded == True`: sağlayıcı hatası, süre aşımı, iki denemede şema onarımının
   tükenmesi) analiz başında ayrılan deneme rapor kaydedildikten sonra `sessions.release_attempt`
   ile geri verilir. Rapor veritabanına ve geçmişe kaydedilir ancak oturum sayacı artmaz.
2. **K2 (Sözdizimi hatasıyla erken çıkış sayılmaz):** Sözdizimi hatası nedeniyle statik aşamada
   kesilen analizlerde (`report.meta.early_exit == True`) deneme `sessions.release_attempt` ile
   geri verilir. Öğrenci sözdizimini düzelttiğinde ipucu seviyesi kaldığı yerden devam eder.
3. **K3 (İstek seçeneği ve masaüstü mantığı):**
   - `AnalysisOptions` modeline `advance_hint: bool | None` alanı eklenir (`False`: merdiveni
     ilerletmez; `None`/`True`: ilerletir).
   - `orchestrator._traced` içinde `advance_hint is False` ise analiz başında deneme
     ayrılmaz (`reserve_attempt` çağrılmaz, son geçerli deneme okunur). İstisna ve kayıt
     yollarında da sayaç değiştirilmez.
   - Masaüstünde **"Bir ipucu daha"** düğmesi her zaman `advance_hint=True` ile çalışır.
   - Masaüstünde **"Denetle"** düğmesi, editördeki kod ve seçili soru bir önceki analizle
     birebir aynıysa ve bir önceki analiz sayılmışsa (`self._last_counted is True`),
     otomatik olarak `advance_hint=False` gönderir (böylece sadece model değiştirmek veya
     aynı kodu yeniden koşturmak seviyeyi harcamaz). Kod değiştiğinde `None` (varsayılan ilerleme)
     ile çalışır.

## Sonuçlar

- Sağlayıcı kesintileri, API kotaları veya sözdizimi hataları öğrencinin ipucu merdivenini
  tüketmez.
- Geçmiş ve hata ayıklama kayıtları bozulmaz: analiz raporu her durumda veritabanına işlenir;
  yalnızca `sessions` tablosundaki deneme ve seviye sayacı korunur.
- Public API şeması (`AnalysisOptions`) geriye dönük uyumlu olarak genişler (`advance_hint` opsiyoneldir);
  JSON şemaları ve web tipleri güncellenir.
- Testler: Başarısız sağlayıcı, süre aşımı, şema hatası, erken çıkış ve `advance_hint=False` durumlarında
  sayaç değişmezliği zorunlu olumsuz testlerle doğrulanır.
