# ADR-0031: Küçük Modeller İçin Deterministik Sokratik Kalite Kapısı ve Sağduyu Korumaları

**Tarih:** 2026-10-20 · **Durum:** Kabul edildi · **Etkilenen bölümler:** mimari §4, §5.4, §5.6, §20

## Bağlam

Küçük ve yerel modeller (8B/14B parametreli modeller veya yerel Ollama örnekleri) dev değerlendirmelerinde ve gerçek kullanımda büyük bulut modellerine (Claude Opus vb.) kıyasla farklı zayıflıklar gösterir:
1. **Döngüsel Tekrar (Degeneration):** Model yanıtlarında aynı cümleler veya n-gram öbekleri ardı ardına tekrarlanabilir.
2. **Neredeyse Özdeş Sorular:** Birden fazla soru üretirken aynı soruyu çok ufak kelime farklarıyla iki kez sorabilir.
3. **Koda Temas Eksikliği:** Sorular koddaki değişken, fonksiyon veya satır numaralarına hiç temas etmeyen, öğrenciye faydasız jenerik metinlerden ("Kodunuzu inceleyin", "Mantığı gözden geçirin") ibaret kalabilir.
4. **Ters Denetim Çelişkisi (Guard Hallucination):** Model, kanıt satırının bizzat kendisi bir denetim (`if (ptr == NULL)` veya `if (n <= 0)`) iken "null kontrolü yapılmıyor" veya "sıfır denetlenmemiş" gibi temelsiz iddialar üretebilir.
5. **Karmaşıklık Çelişkisi:** Deterministik K1/K2 statik analizi somut olarak `O(n)` hesaplamışken, küçük model `O(n^2)` iddia edebilir.

Bu durumları engellemek için deterministik, LLM çağrısı gerektirmeyen kurallarla zayıf çıktının öğrenciye gitmesi engellenmeli ve zarif bozulma ile statik şablon sorulara dönülmelidir.

## Karar

1. **Sokratik Kalite Kapısı (`src/codementor/verify/socratic_gate.py`):**
   - **Özdeş Soru Eleme:** Sorular tokenize edilip ikili Jaccard benzerliği hesaplanır; `similarity >= 0.70` olan soruların ikincisi elenir.
   - **Tekrar/Döngü Tespiti:** Sorularda ve ipucunda 3, 4 veya 5'li kelime n-gram'larının ardışık 3 tekrarı dejenerasyon kabul edilir; yalnız rakamlardan oluşan öbekler ("0 0 0 …" girdi örneği) sayılmaz.
   - **Koda Temas (`touches_code`):** İpucu seviyesi >= 2 olduğunda veya küçük model profilinde, Sokratik soruların veya ipucunun koddaki tanımlayıcılardan (tanımlı fonksiyon, değişken, parametre veya satır numarası) en az birine temas etmesi beklenir. Satır referansı rakam ister ("12. satır", "satır 12", "line 8"); rakamsız "satır" ya da "lineer" temas sayılmaz.
   - *Güncelleme 2026-10-20 (tam tarama #5, KALAN_ISLER iş 15):* n-gram boyu kodla hizalandı (önceki metin "4'lü" diyordu), sayı dizisi ve rakamsız satır kelimesi istisnaları eklendi; kapı geçip uyardığında (soru listesi değişmese de) uyarı rapora taşınır.
   - **Zarif Şablona Düşüş:** Çıktı kapıdan geçemezse model soruları yerine statik olgulardan üretilen şablon sorulara dönülür ve rapora `degraded_socratic` uyarısı işlenir.

2. **Bulgu Sağduyu Denetimi (`src/codementor/verify/sanity.py`):**
   - **Ters Denetim Filtresi:** Bir bulgunun açıklaması "kontrol edilmiyor / denetlenmiyor / eksik" gibi ifadeler içerirken kanıt satırı `if (...)` ile bir kontrol gerçekleştiriyorsa bulgu halüsinasyon kabul edilerek düşürülür.
   - **Küçük Profil Bulgu Tavanı:** `model_profile == "small"` durumunda en fazla 3 bulgu kabul edilir; fazlası önem sırasına göre elenir.

3. **Karmaşıklık Politikası (`src/codementor/verify/complexity_policy.py`):**
   - Küçük model profilinde modelin karmaşıklığı statik ipucuyla çelişiyorsa (`conflicts`), deterministik statik ipucu tercih edilir ve gerekçeye bilgilendirici not düşülür.

4. **Yapılandırma (`src/codementor/config.py`):**
   - `pipeline.model_profile`: `"standard"` (varsayılan) veya `"small"`.
   - `pipeline.verify_provider: str | None`: Doğrulama geçişini isteğe bağlı olarak farklı bir sağlayıcıya yönlendirme imkânı.

## Sonuçlar

- (+) Küçük yerel modellerle çalışırken öğrenciye ulaşan anlamsız döngüsel tekrarlar ve bariz çelişkili bulgular tamamen deterministik olarak engellenir.
- (+) Testler ağa çıkmadan FakeProvider ile tüm sınır durumları ve filtreleri kapsar.
- (−) Çok katı bir eşik bazı geçerli soyut soruları şablona düşürebilir; bu nedenle koda temas kuralı ipucu merdivenine ve model profiline göre kademelendirilmiştir.
