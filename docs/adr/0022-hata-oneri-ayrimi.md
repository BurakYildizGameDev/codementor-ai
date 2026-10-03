# ADR-0022: Bulgularda hata ve öneri ayrımı

**Tarih:** 2026-10-04 · **Durum:** Kabul edildi ·
**Etkilenen bölümler:** mimari §5.4.2, §5.4.4, §5.7, §6.3, §6.4, §6.5, §14.2; ADR-0019

## Bağlam

Faz 22 analizine göre precision kaybının büyük kısmı, modelin gerçek ama hataya yol açmayan
gözlemleri (küçük `edge_case`, `design`, `input_handling` notları) hata gibi raporlamasından
geliyor. Faz 22B'de prompt'a "öneri bulgu değildir" kuralı eklendi. Bu kural precision'ı artırdı
ama bilgiyi de sildi: bir mentorun değineceği iyileştirmeler öğrenciye hiç ulaşmıyor. Öte
yandan bu gözlemler hatalarla aynı listede durursa öğrenci önce asıl hatayı göremiyor ve
Sokratik sorular önemsiz bir noktaya kayabiliyor.

## Karar

1. Bulguya tür eklenir: `Finding.kind` ve `LLMFinding.kind`, değerleri `issue` (gerçek hata)
   ve `suggestion` (hataya yol açmayan öneri). Varsayılan `issue` olduğu için eski LLM
   yanıtları, few-shot'lar ve raporlar geçerli kalır. Rapor `schema_version` 1.1 olur. 1.0
   raporlar (geçmiş, önbellek) okunmaya devam eder ve bulguları hata sayılır.
2. **Öneri yalnızca `low` önemde olabilir.** Orta ya da yüksek önemli bir `suggestion` sistem
   tarafından `issue`'ya çevrilir. "Soru gereksinimi ihlali öneri değildir" kuralı prompt'ta
   yer alır, çünkü sistem bunu ayırt edemez.
3. **Statik bulgular her zaman hatadır.** Kurallar "sorun" için seçilmiştir ve eval etiketleri
   de böyledir. Statik bulguyla birleşen LLM bulgusu hata olarak kalır. LLM aynı sorunu hem
   hata hem öneri olarak yazdıysa tekilleştirmede hata kalır.
4. **Doğrulama geçişi (ADR-0019) önerileri sınamaz.** Somut bir hatalı girdi gösterilemeyeceği
   için öneriler doğrulamaya sokulsaydı hepsi düşerdi. Kanıtlanamayan hata ise eskisi gibi
   düşer; öneriye indirilmez, çünkü kanıtsız bir iddia öneri olarak da yanlış bilgi olabilir.
5. **Sokratik geçiş yalnızca hatalara dayanır.** Geçiş B'ye ve şablon sorulara yalnız `issue`
   bulguları gider. `single_pass`'ta bu kural mentorluk kurallarındadır. Sızıntı koruması öneri
   açıklamalarına da uygulanır.
6. **Gösterim:** Markdown'da "Hatalar" tablosu ve katlanmış `<details>` "Öneriler (n)"; SARIF'te
   öneri `note` düzeyindedir (`properties.kind`). Terminalde öneriler ayrı bir başlık altında,
   masaüstünde ve web'de katlı bölümde gösterilir. Editörde yalnız hata satırları boyanır.
7. **Eval:** Denetim precision/recall/F1 yalnız hatalarla hesaplanır. Öneri sayısı
   `Metrics.suggestions_total` alanında ve `eval analyze` çıktısında ayrıca raporlanır.
8. **Prompt:** Kural metni hata ile öneriyi tanımlar (en fazla 6 hata ve 2 öneri). Her dil
   ailesine (C, C++/Unreal, C#/Unity, Python, HTML) bir "temiz kod" few-shot'ı eklenir. Bu
   örneklerin ikisi tek bir öneri gösterir. Seçim limit ≥ 2 iken önce en uygun hatalı örneği,
   sonra en uygun temiz örneği alır; limit 1'de yalnız hatalı örnek seçilir (Faz 34 ablasyonu
   değişmez). Şemaya giren model docstring'leri yoruma çevrildi. Bu metinler modele bir şey
   anlatmıyordu ve 2048 bağlamlı bütçede `kind` alanına yer açtı.

## Sonuçlar

- (+) Önemsiz gözlemler silinmeden ayrılır. Öğrenci önce hataları görür.
- (+) Eval precision'ı önerilerden etkilenmez. Recall'un düşmemesi beklenir, çünkü prompt artık
  belirsiz gözlemi silmek yerine öneriye yönlendirir.
- (−) Model bir hatayı öneri olarak işaretlerse bu hata eval'de kaçırılmış sayılır ve Sokratik
  sorulara girmez. Bu risk, öneriyi `low` ile sınırlayan kuralla daraltılır. Canlı ölçümde
  `suggestions_total` ile birlikte izlenmelidir.
- (−) Rapor şeması değiştiği için önbellek anahtarı değişti ve eski önbellek kayıtları
  kullanılmaz.
- Açık: Kural bazında öneri (ör. CPP-OWN-001'in doğru eşleşmiş `new`/`delete` için öneri
  olması) bu kararın dışındadır.
