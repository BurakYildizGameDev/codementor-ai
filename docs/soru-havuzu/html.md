# CodeMentor AI — 200 HTML Sorusu

Bu belge, `docs/SORU_YAZIM_REHBERI.md` standartlarına uygun olarak hazırlanmış 200 adet HTML sorusunu içerir.
HTML işaretleme dili olduğu için karmaşıklık analizi içermez (`expected` alanı yer almaz); anlamsal yapı (semantic HTML), erişilebilirlik (WAI-ARIA, a11y), form kontrolleri, odak yönetimi ve modern web standartlarına odaklanır.

---

## Soru Bankası Değerlendirmesi ve Pedagojik Kullanım Notu

Bu soru bankası iki temel amaç gözetilerek yapılandırılmıştır:

1. **Öğrenci ve Bireysel Gelişim İçin (Kapsamlı Rehber Bankası):**
   - Sorularda öğrencilerin doğru W3C/WHATWG etiket ve ARIA niteliklerini doğrudan öğrenip pekiştirebilmesi amacıyla, başlıklarda ve kısıtlarda ilgili kavramlar (ör. `(picture ve media sorgusu)`, `(dialog ve form method dialog)`) açıkça belirtilmiştir.
   - Bu yaklaşım, öğrencinin konuyu sıfırdan öğrenirken veya pratik yaparken "hangi ihtiyaca hangi modern HTML standardının karşılık geldiğini" hızlıca bağdaştırmasını sağlar.

2. **İş Mülakatları ve Sokratik Mentörlük İçin Kullanım Uyarısı:**
   - **Gerçek Teknik Mülakatlarda:** Bir adaya soru yöneltilirken başlık ve kısıtlardaki parantez içi etiket adları gizlenmeli; adaya yalnızca `prompt` (problem senaryosu ve işlevsel gereksinimler) verilmelidir. Adaydan çözümü sağlayan doğru etiketi (örneğin arka planı kilitleyen modal için `<dialog>`, çözünürlük duyarlılığı için `<picture>` veya `srcset`) kendisinin akıl etmesi beklenmelidir.
   - **Sokratik Kod Mentörlüğünde:** Mentör motoru adaya doğrudan etiketi söylememeli; 3 basamaklı `hint_ladder` hiyerarşisini kullanarak yönlendirici sorularla adayı doğru etikete ulaştırmalıdır.

### Kapsam ve İstatistikler
- **Toplam Soru:** 200 adet (50 Çok Kolay, 50 Kolay, 50 Orta, 50 Zor)
- **Konsept Dağılımı:** Standartlar (121), Erişilebilirlik/WAI-ARIA (109), Semantik (69), Formlar & Doğrulama (60), Web Performansı/LCP/CLS (39), Klavye/Odak (34), Güvenlik/CSP/SRI (21), Tablolar (14), Gezinti (14), İletişim Pencereleri (7).
- **Standart Uyumu:** HTML5.2, WHATWG Living Standard, WAI-ARIA 1.2 APG kalıpları, Speculation Rules API (2024+).

---

## 1. Çok Kolay (Very Easy) — 50 Soru

### html-veryeasy-basic-doctype

```yaml
id: html-veryeasy-basic-doctype
version: 1
language: html
engine: none
difficulty: very_easy
title: "Modern HTML5 belge bildirimi ve kök dil tanımı"
prompt: |
  Tarayıcının standart kipte (standards mode) çalışmasını sağlayan modern HTML5 belge türü
  bildirimini içeren, Türkçe içeriğe sahip bir sayfanın kök elemanını ve temel gövdesini
  tanımlayan bir HTML iskeleti oluşturun. Belgenin dili arama motorları ve ekran okuyucular
  için doğru belirtilmelidir.
constraints:
  - "Belgenin ilk satırında modern HTML5 doctype bildirimi yer almalı"
  - "html kök elemanında geçerli bir dil niteliği (lang='tr') bulunmalı"
concept_tags: [standards, accessibility, semantics]
checklist_extra:
  - "Doctype bildirimi eski HTML4 veya XHTML sözdizimiyle mi yazılmış?"
  - "html elemanında lang niteliği unutulmuş mu?"
reference_solution_path: private/solutions/html-veryeasy-basic-doctype.html
hint_ladder:
  1: "Tarayıcının sayfayı geriye uyumluluk tuhaflık kipinde (quirks mode) açmaması için en üstte ne yer almalıdır?"
  2: "Ekran okuyucunun Türkçe metni doğru telaffuzla okuyabilmesi için kök etiket hangi niteliği almalıdır?"
  3: "Bu bildirim 'HTML5 belge türü bildirimi (DOCTYPE) ve kök dil özniteliği' olarak bilinir."
```

### html-veryeasy-charset-meta

```yaml
id: html-veryeasy-charset-meta
version: 1
language: html
engine: none
difficulty: very_easy
title: "Karakter kodlaması meta bildirimi"
prompt: |
  Türkçe karakterlerin (ş, ğ, ç, ı, ö, ü) tarayıcıda bozulmadan ve hatalı semboller
  oluşmadan görüntülenebilmesi için `<head>` bölümünün en başında yer alması gereken
  karakter seti meta etiketini içeren geçerli bir HTML başlık yapısı yazın.
constraints:
  - "Karakter kodlaması UTF-8 olarak bildirilmelidir"
  - "Meta etiketi head bölümü içinde, tercihen ilk sıralarda yer almalıdır"
concept_tags: [standards, semantics]
checklist_extra:
  - "Karakter seti bildirimi eski http-equiv sözdizimiyle gereksiz uzatılmış mı?"
  - "Karakter seti meta etiketi title veya diğer etiketlerden sonraya mı bırakılmış?"
reference_solution_path: private/solutions/html-veryeasy-charset-meta.html
hint_ladder:
  1: "Tarayıcı metni okumaya başladığı ilk baytlarda hangi karakter kodlamasını kullandığını nereden anlar?"
  2: "HTML5'te karakter kodlamasını belirten en kısa ve standart meta niteliği hangisidir?"
  3: "Bu standart 'UTF-8 karakter kodlaması meta bildirimi' olarak bilinir."
```

### html-veryeasy-viewport-meta

```yaml
id: html-veryeasy-viewport-meta
version: 1
language: html
engine: none
difficulty: very_easy
title: "Mobil uyumlu görünüm alanı (viewport) bildirimi"
prompt: |
  Mobil cihazlarda ve farklı ekran genişliklerinde sayfanın masaüstü görünümüne küçültülerek
  (zoom-out) açılmasını önleyen, cihazın kendi fiziksel piksel genişliğini baz alan standart
  görünüm alanı meta etiketini `<head>` bloğuna ekleyin.
constraints:
  - "Cihaz genişliğine uyum sağlayan width=device-width tanımı bulunmalı"
  - "Başlangıç ölçeği initial-scale=1.0 olarak ayarlanmalı"
concept_tags: [standards, performance]
checklist_extra:
  - "Kullanıcının yakınlaştırma yapmasını engelleyen (user-scalable=no) erişilebilirlik karşıtı bir kısıt eklenmiş mi?"
  - "Görünüm alanı meta etiketinin name ve content nitelikleri doğru eşleşmiş mi?"
reference_solution_path: private/solutions/html-veryeasy-viewport-meta.html
hint_ladder:
  1: "Akıllı telefonların sayfayı 980 piksellik sanal masaüstü olarak render etmesini nasıl engellersin?"
  2: "Genişliği cihaz genişliğine eşitleyen ve ölçeği 1 yapan meta içeriği nedir?"
  3: "Bu tanımlama 'duyarlı tasarım görünüm alanı bildirimi (responsive viewport meta tag)' olarak bilinir."
```

### html-veryeasy-heading-hierarchy

```yaml
id: html-veryeasy-heading-hierarchy
version: 1
language: html
engine: none
difficulty: very_easy
title: "Başlık hiyerarşisi ve ana başlık kullanımı"
prompt: |
  Bir blog yazısının ana başlığını (`<h1>`), iki alt bölümünü (`<h2>`) ve bölümlerden birinin
  altındaki alt başlığı (`<h3>`) anlamsal sırayı atlamadan gösteren bir başlık yapısı
  oluşturun. Sayfada yalnızca tek bir ana başlık bulunmalı ve seviyeler atlanmamalıdır
  (örneğin h1'den doğrudan h3'e geçilmemelidir).
constraints:
  - "Sayfada tam olarak bir adet h1 etiketi yer almalı"
  - "Başlık seviyeleri atlanmadan hiyerarşik sırada (h1 -> h2 -> h3) kullanılmalı"
concept_tags: [accessibility, semantics, standards]
checklist_extra:
  - "h1 etiketi birden fazla kez kullanılmış mı?"
  - "Görsel boyutlandırma amacıyla h1'den doğrudan h3'e atlama yapılmış mı?"
reference_solution_path: private/solutions/html-veryeasy-heading-hierarchy.html
hint_ladder:
  1: "Ekran okuyucu kullanıcıları sayfa haritasını çıkarırken başlık seviyelerinin ardışık olmasını neden bekler?"
  2: "Bir dokümanın ana konusunu belirten en üst düzey başlık etiketi hangisidir?"
  3: "Bu kural 'anlamsal başlık seviyelendirme hiyerarşisi (heading level hierarchy)' olarak bilinir."
```

### html-veryeasy-paragraph-text

```yaml
id: html-veryeasy-paragraph-text
version: 1
language: html
engine: none
difficulty: very_easy
title: "Paragraf yapısı ve metin blokları"
prompt: |
  İki bağımsız düşünceyi temsil eden iki ayrı paragraf metni oluşturun. Paragraflar
  arasında görsel boşluk oluşturmak için ardışık satır sonu (`<br>`) etiketleri kullanmak
  yerine anlamsal paragraf blokları tercih edilmelidir.
constraints:
  - "Paragraflar anlamsal `<p>` etiketleri içine alınmalı"
  - "Paragraf ayrımı için ardışık `<br>` etiketleri kullanılmamalı"
concept_tags: [semantics, standards]
checklist_extra:
  - "Paragraf boşluğu elde etmek için metinler arasına çok sayıda <br> serpiştirilmiş mi?"
  - "Düz metin blokları herhangi bir etiket olmadan doğrudan gövdeye mi bırakılmış?"
reference_solution_path: private/solutions/html-veryeasy-paragraph-text.html
hint_ladder:
  1: "Her bir bağımsız metin bloğunu sarmalamak için hangi blok seviyesi etiketi kullanmalısın?"
  2: "Satır sonu etiketi (<br>) sadece şiir veya adres gibi satırın zorunlu kırıldığı yerlerde mi kullanılmalıdır?"
  3: "Bu kullanım 'anlamsal paragraf yapılandırması' olarak bilinir."
```

### html-veryeasy-image-alt-text

```yaml
id: html-veryeasy-image-alt-text
version: 1
language: html
engine: none
difficulty: very_easy
title: "Bilgilendirici görsel ve alternatif metin"
prompt: |
  Bir şirketin logosunu veya ürün fotoğrafını gösteren bir görsel etiketi tanımlayın.
  Görsel yüklenemediğinde veya ekran okuyucu kullanan görme engelli bir ziyaretçi sayfayı
  gezdiğinde görselin amacını tam olarak anlatan bilgilendirici bir alternatif metin
  tanımlanmalıdır.
constraints:
  - "img etiketi geçerli ve boş olmayan bir alt niteliği içermeli"
  - "Alternatif metin görselin işlevini ve içeriğini özetlemeli"
concept_tags: [images, accessibility, standards]
checklist_extra:
  - "alt niteliği tamamen unutulmuş veya 'resim', 'fotoğraf' gibi anlamsız bir sözcükle mi doldurulmuş?"
  - "Görselin kaynak (src) adresi tanımlı mı?"
reference_solution_path: private/solutions/html-veryeasy-image-alt-text.html
hint_ladder:
  1: "Görme engelli bir kullanıcı web sayfasındaki resmin ne ifade ettiğini nasıl öğrenir?"
  2: "İnternet bağlantısı kesildiğinde kırık resim simgesi yerine neyin görüntülenmesini sağlarsın?"
  3: "Bu erişilebilirlik gereksinimi 'bilgilendirici görsel alternatif metni (image alt attribute)' olarak bilinir."
```

### html-veryeasy-decorative-image-alt

```yaml
id: html-veryeasy-decorative-image-alt
version: 1
language: html
engine: none
difficulty: very_easy
title: "Dekoratif görsel için alternatif metin yönetimi"
prompt: |
  Sayfada yalnızca süsleme, arka plan deseni veya ayrım çizgisi amacıyla bulunan, içeriğe
  hiçbir bilgi katmayan bir dekoratif görsel ekleyin. Ekran okuyucuların bu gereksiz süsü
  seslendirip kullanıcıyı rahatsız etmesini engellemek için doğru alternatif metin
  biçimini uygulayın.
constraints:
  - "img etiketinde alt niteliği boş dize (alt='') olarak bulunmalı"
  - "alt niteliği kesinlikle etiket üzerinden tamamen silinmemeli"
concept_tags: [images, accessibility]
checklist_extra:
  - "alt niteliği tamamen kaldırılmış ve ekran okuyucunun dosya adını okumasına yol açılmış mı?"
  - "Boşluk karakteri (alt=' ') verilerek ekran okuyucunun duraksamasına neden olunmuş mu?"
reference_solution_path: private/solutions/html-veryeasy-decorative-image-alt.html
hint_ladder:
  1: "Ekran okuyucunun bir görseli tamamen yok sayması için alt niteliğine ne yazılmalıdır?"
  2: "alt niteliğini hiç yazmamak ile boş bırakmak (alt='') arasındaki fark nedir?"
  3: "Bu teknik 'dekoratif görsel boş alt niteliği (null alt attribute)' olarak bilinir."
```

### html-veryeasy-ordered-list

```yaml
id: html-veryeasy-ordered-list
version: 1
language: html
engine: none
difficulty: very_easy
title: "Sıralı adım listesi oluşturma"
prompt: |
  Bir yazılımın kurulum adımlarını veya bir yemek tarifinin sıralı işlem basamaklarını
  gösteren, sırası değiştiğinde anlamı bozulacak bir numaralı liste yapısı oluşturun.
  En az üç adım yer almalıdır.
constraints:
  - "Numaralandırılmış liste için anlamsal `<ol>` etiketi kullanılmalı"
  - "Her adım `<li>` etiketi içinde tanımlanmalı"
concept_tags: [lists, semantics]
checklist_extra:
  - "Sıralı liste yerine sırasız <ul> veya düz paragraflar içine elle '1.', '2.' mi yazılmış?"
  - "<ol> etiketinin doğrudan çocukları yalnızca <li> etiketleri mi?"
reference_solution_path: private/solutions/html-veryeasy-ordered-list.html
hint_ladder:
  1: "Sırasının önemli olduğu aşamaları numaralandırmak için hangi liste etiketini kullanırsın?"
  2: "Liste elemanlarını sarmalamak için kullanılan ortak etiket hangisidir?"
  3: "Bu işaretleme 'anlamsal sıralı liste (ordered list)' olarak bilinir."
```

### html-veryeasy-unordered-list

```yaml
id: html-veryeasy-unordered-list
version: 1
language: html
engine: none
difficulty: very_easy
title: "Sırasız madde işaretli liste"
prompt: |
  Bir kullanıcının ilgi alanlarını veya bir market alışveriş sepetindeki ürünleri gösteren,
  maddelerinin sırası değiştiğinde anlam kaybı yaşanmayan madde işaretli bir liste oluşturun.
  En az üç madde içermelidir.
constraints:
  - "Sırasız liste için anlamsal `<ul>` etiketi kullanılmalı"
  - "Her madde `<li>` etiketi ile sarmalanmalı"
concept_tags: [lists, semantics]
checklist_extra:
  - "Liste maddeleri div veya p etiketleri içine tire (-) konularak mı yapılmış?"
  - "<ul> etiketinin içine <li> dışında doğrudan metin yerleştirilmiş mi?"
reference_solution_path: private/solutions/html-veryeasy-unordered-list.html
hint_ladder:
  1: "Maddelerin sırasının önemsiz olduğu listeler için hangi etiket tercih edilir?"
  2: "Ekran okuyucuların '3 maddelik liste' şeklinde duyurabilmesi için liste nasıl yapılandırılır?"
  3: "Bu yapı 'anlamsal sırasız liste (unordered list)' olarak bilinir."
```

### html-veryeasy-hyperlink-href

```yaml
id: html-veryeasy-hyperlink-href
version: 1
language: html
engine: none
difficulty: very_easy
title: "Temel web bağlantısı ve açıklayıcı metin"
prompt: |
  Kullanıcıyı güvenilir bir dış kaynağa veya dokümantasyona yönlendiren bir köprü (link)
  oluşturun. Bağlantı metni 'buraya tıklayın' gibi belirsiz ve erişilebilirlik dışı bir
  ifade yerine, gidilecek hedefi açıkça belirten açıklayıcı bir metin içermelidir.
constraints:
  - "Geçerli bir href hedefi olan `<a>` etiketi kullanılmalı"
  - "Bağlantı metni bağlamdan bağımsız olarak hedefi anlatmalı ('buraya tıkla' kullanılmamalı)"
concept_tags: [links, accessibility, standards]
checklist_extra:
  - "Bağlantı metni yalnızca 'tıklayın' veya 'link' gibi anlamsız ifadelerden mi oluşuyor?"
  - "href niteliği boş veya eksik bırakılmış mı?"
reference_solution_path: private/solutions/html-veryeasy-hyperlink-href.html
hint_ladder:
  1: "Ekran okuyucu kullanıcıları sayfadaki tüm bağlantıları liste olarak çektiğinde sadece 'buraya tıkla' duyarlarsa ne anlarlar?"
  2: "Kullanıcıya nereye gideceğini söyleyen tanımlayıcı bağlantı metni nasıl kurulmalıdır?"
  3: "Bu ilke 'açıklayıcı bağlantı metni (meaningful link text)' olarak bilinir."
```

### html-veryeasy-email-link

```yaml
id: html-veryeasy-email-link
version: 1
language: html
engine: none
difficulty: very_easy
title: "E-posta gönderme bağlantısı"
prompt: |
  Kullanıcı tıkladığında varsayılan e-posta istemcisini açarak belirtilen destek adresine
  (örneğin destek@example.com) yeni bir e-posta taslağı başlatan bir bağlantı oluşturun.
constraints:
  - "href niteliğinde 'mailto:' protokol şeması doğru biçimde tanımlanmalı"
  - "E-posta adresi geçerli formatta olmalı"
concept_tags: [links, forms]
checklist_extra:
  - "mailto: protokolü unutulup düz e-posta adresi web sayfası gibi mi bağlanmış?"
  - "Bağlantı metni e-posta gönderme eylemini açıkça ifade ediyor mu?"
reference_solution_path: private/solutions/html-veryeasy-email-link.html
hint_ladder:
  1: "Tarayıcının bir bağlantıyı web sayfası yerine e-posta programına yönlendirmesi için href ne ile başlamalıdır?"
  2: "mailto: ile e-posta adresi arasında boşluk olmamasına dikkat ettin mi?"
  3: "Bu protokol 'mailto URL şeması ile e-posta köprüsü' olarak bilinir."
```

### html-veryeasy-phone-link

```yaml
id: html-veryeasy-phone-link
version: 1
language: html
engine: none
difficulty: very_easy
title: "Telefon arama bağlantısı"
prompt: |
  Özellikle mobil cihazlarda dokunulduğunda telefon arama uygulamasını açıp numarayı
  çeviriciye aktaran bir telefon bağlantısı oluşturun. Numara uluslararası formatta
  (örneğin +902120000000) tanımlanmalıdır.
constraints:
  - "href niteliğinde 'tel:' protokolü kullanılmalı"
  - "Telefon numarası boşluksuz ve uluslararası kod ile belirtilmeli"
concept_tags: [links, performance]
checklist_extra:
  - "tel: protokolü yerine geçersiz bir link yapısı mı kullanılmış?"
  - "Görünen metin okunabilir formatlanırken href içindeki numara standart çevrilebilir mi?"
reference_solution_path: private/solutions/html-veryeasy-phone-link.html
hint_ladder:
  1: "Mobil tarayıcıların numarayı doğrudan arama ekranına göndermesi için hangi URL şeması kullanılır?"
  2: "tel: protokolünde ülke kodunun (+90...) yer alması neden önemlidir?"
  3: "Bu bağlantı 'tel URL şeması ile doğrudan arama köprüsü' olarak bilinir."
```

### html-veryeasy-strong-importance

```yaml
id: html-veryeasy-strong-importance
version: 1
language: html
engine: none
difficulty: very_easy
title: "Ciddi önem ve aciliyet belirten metin vurgusu"
prompt: |
  Bir güvenlik uyarısı veya son teslim tarihi uyarısı içeren metin bloğu yazın.
  Metindeki kritik uyarı kelimesini, yalnızca görsel olarak kalın yapmak yerine,
  içeriğin ciddi bir önem ve aciliyet taşıdığını ekran okuyuculara ve arama motorlarına
  bildiren anlamsal etiketle sarmalayın.
constraints:
  - "Yalnızca görsel kalınlaştırma (`<b>`) yerine anlamsal `<strong>` etiketi kullanılmalı"
  - "Cümle içinde kritik uyarı sözcüğü doğru vurgulanmalı"
concept_tags: [semantics, accessibility, standards]
checklist_extra:
  - "Anlamsal önem taşımayan eski <b> etiketi mi kullanılmış?"
  - "strong etiketi cümlenin tamamı yerine gerçekten kritik olan kelimeleri mi sarmalıyor?"
reference_solution_path: private/solutions/html-veryeasy-strong-importance.html
hint_ladder:
  1: "HTML'de bir kelimenin sadece görsel değil 'anlamsal olarak yüksek önem' taşıdığını belirten etiket hangisidir?"
  2: "<b> ile <strong> arasındaki erişilebilirlik farkı nedir?"
  3: "Bu kullanım 'anlamsal güçlü önem vurgusu (strong importance)' olarak bilinir."
```

### html-veryeasy-emphasis-stress

```yaml
id: html-veryeasy-emphasis-stress
version: 1
language: html
engine: none
difficulty: very_easy
title: "Cümle vurgusu ve tonlama değişimi"
prompt: |
  Cümlenin anlamını veya tonlamasını değiştiren bir sözcüğü vurgulayan bir paragraf
  yazın (örneğin: 'Bunu *ben* yapmadım'). Yalnızca görsel eğik yazı (`<i>`) kullanmak
  yerine, konuşma sentezleyicilerinin ses tonunu değiştirmesini sağlayan anlamsal
  etiketi tercih edin.
constraints:
  - "Görsel italik (`<i>`) yerine anlamsal `<em>` etiketi kullanılmalı"
  - "Vurgulanacak sözcük doğru hedeflenmeli"
concept_tags: [semantics, accessibility]
checklist_extra:
  - "Anlamsal tonlama taşımayan <i> etiketi mi tercih edilmiş?"
  - "Ekran okuyucuların ses perdesini değiştirecek anlamsal etiket yerinde mi?"
reference_solution_path: private/solutions/html-veryeasy-emphasis-stress.html
hint_ladder:
  1: "Bir cümlenin sesli okunuşunda belirli bir kelimenin üstüne basılmasını sağlayan etiket hangisidir?"
  2: "<i> etiketinin genel taksonomi veya yabancı sözcükler için ayrıldığını biliyor musun?"
  3: "Bu işaretleme 'anlamsal tonlama vurgusu (stress emphasis)' olarak bilinir."
```

### html-veryeasy-block-quote

```yaml
id: html-veryeasy-block-quote
version: 1
language: html
engine: none
difficulty: very_easy
title: "Geniş alıntı bloğu ve kaynak belirtme"
prompt: |
  Başka bir yazardan veya kitaptan alınan çok satırlı bir alıntı bloğu oluşturun.
  Alıntılanan metin anlamsal alıntı bloğu etiketine alınmalı ve alıntının alındığı URL
  kaynağı ilgili etiket niteliğinde (`cite`) belirtilmelidir.
constraints:
  - "Geniş alıntı için `<blockquote>` etiketi kullanılmalı"
  - "Kaynak adresi etiket üzerinde `cite` niteliği olarak tanımlanmalı"
concept_tags: [semantics, standards]
checklist_extra:
  - "Blok alıntı yerine düz paragraf ve tırnak işaretleri mi kullanılmış?"
  - "cite niteliğine geçerli bir URL değeri atanmış mı?"
reference_solution_path: private/solutions/html-veryeasy-block-quote.html
hint_ladder:
  1: "Uzun ve bağımsız alıntı bloklarını temsil eden HTML5 etiketi hangisidir?"
  2: "Alıntının internetteki referans kaynağını etiketin içine nitelik olarak nasıl eklersin?"
  3: "Bu yapı 'blok alıntı ve kaynak referansı (blockquote with cite attribute)' olarak bilinir."
```

### html-veryeasy-inline-quote

```yaml
id: html-veryeasy-inline-quote
version: 1
language: html
engine: none
difficulty: very_easy
title: "Satır içi kısa alıntı"
prompt: |
  Bir paragrafın akışı içerisinde geçen kısa bir cümlelik alıntıyı temsil eden bir yapı
  oluşturun. Klavyeden elle tırnak işaretleri yazmak yerine, tarayıcının dil ayarlarına
  uygun tırnak işaretlerini otomatik olarak eklemesini sağlayan satır içi alıntı etiketini
  kullanın.
constraints:
  - "Satır içi alıntı için `<q>` etiketi kullanılmalı"
  - "Metin içine elle çift tırnak (\"\") yazılmamalı"
concept_tags: [semantics, standards]
checklist_extra:
  - "Elle tırnak işareti eklenerek tarayıcının eklediği tırnaklarla çift tırnak karmaşası yaratılmış mı?"
  - "<q> etiketinin satır içi (inline) bir etiket olduğu gözetilmiş mi?"
reference_solution_path: private/solutions/html-veryeasy-inline-quote.html
hint_ladder:
  1: "Tarayıcının dile göre doğru tırnak işaretini (örneğin Türkçe için « » veya \" \") kendisinin basması için hangi etiket kullanılır?"
  2: "Elle tırnak işareti koyarsan ekran okuyucu iki kez tırnak sesi çıkarır mı?"
  3: "Bu etiket 'satır içi alıntı etiketi (inline quotation)' olarak bilinir."
```

### html-veryeasy-abbreviation-title

```yaml
id: html-veryeasy-abbreviation-title
version: 1
language: html
engine: none
difficulty: very_easy
title: "Kısaltma ve tam açılım tanımlama"
prompt: |
  Bir metin içinde geçen 'HTML' veya 'NASA' gibi bir kısaltmayı anlamsal etiketiyle
  tanımlayın. Kullanıcı fareyi üzerine getirdiğinde veya ekran okuyucu kısaltmaya ulaştığında
  kısaltmanın tam Türkçe veya orijinal açılımının görüntülenebilmesini sağlayın.
constraints:
  - "Kısaltma `<abbr>` etiketi ile sarmalanmalı"
  - "Açılım `title` niteliğinde eksiksiz belirtilmeli"
concept_tags: [accessibility, semantics]
checklist_extra:
  - "Eski <acronym> etiketi mi kullanılmış?"
  - "title niteliği unutulup açılım tanımsız mı bırakılmış?"
reference_solution_path: private/solutions/html-veryeasy-abbreviation-title.html
hint_ladder:
  1: "Web standartlarında kısaltmaları ve akronimleri temsil eden tek resmi etiket hangisidir?"
  2: "Kısaltmanın uzun halini farenin ipucu baloncuğunda göstermek için hangi nitelik eklenir?"
  3: "Bu tanımlama 'kısaltma etiketi ve başlık açıklaması (abbr with title)' olarak bilinir."
```

### html-veryeasy-superscript-subscript

```yaml
id: html-veryeasy-superscript-subscript
version: 1
language: html
engine: none
difficulty: very_easy
title: "Alt simge ve üst simge kimyasal/matematiksel ifadeler"
prompt: |
  Bir kimyasal formülü (örneğin su için 'H2O') ve bir matematiksel üslü ifadeyi (örneğin 'x2')
  içeren iki formül yazın. Rakamlar metin satırının altında veya üstünde yer alacak şekilde
  doğru anlamsal alt simge ve üst simge etiketleriyle işaretlenmelidir.
constraints:
  - "Alt simge rakamı için `<sub>` etiketi kullanılmalı"
  - "Üst simge rakamı için `<sup>` etiketi kullanılmalı"
concept_tags: [semantics, standards]
checklist_extra:
  - "Alt ve üst simge etiketleri birbirine karıştırılmış mı?"
  - "Yalnızca CSS ile font küçültmek yerine anlamsal etiketler tercih edilmiş mi?"
reference_solution_path: private/solutions/html-veryeasy-superscript-subscript.html
hint_ladder:
  1: "Kimyasal formüllerde taban çizgisi altına inen rakamlar hangi etiketle yazılır?"
  2: "Matematikte üs sayıları için hangi etiket kullanılır?"
  3: "Bu etiketler 'alt simge (subscript) ve üst simge (superscript)' olarak bilinir."
```

### html-veryeasy-horizontal-rule-thematic

```yaml
id: html-veryeasy-horizontal-rule-thematic
version: 1
language: html
engine: none
difficulty: very_easy
title: "Tematik konu değişimi ayracı"
prompt: |
  Bir hikayede sahne değiştiğinde veya bir makalede tamamen farklı bir konuya geçildiğinde
  paragraflar arasına tematik bir kırılma (konu geçişi) ekleyin. Yalnızca görsel bir çizgi
  çekmek amacıyla değil, içerikteki konu değişimini belirten anlamsal ayraç etiketini kullanın.
constraints:
  - "Tematik konu değişimi için `<hr>` etiketi kullanılmalı"
  - "Etiket iki anlamsal paragraf arasına yerleştirilmeli"
concept_tags: [semantics, standards]
checklist_extra:
  - "Konu değişimi olmayan yerlere sırf tasarım gereği hr serpiştirilmiş mi?"
  - "hr etiketinin kapanış etiketi gerektirmeyen boş bir etiket (void element) olduğu unutulmuş mu?"
reference_solution_path: private/solutions/html-veryeasy-horizontal-rule-thematic.html
hint_ladder:
  1: "HTML5 standartlarında yatay çizgi etiketi artık görsel değil, hangi anlama gelir?"
  2: "Bir sahne veya bölüm geçişini temsil eden boş etiket hangisidir?"
  3: "Bu işaretleme 'tematik kırılma ayracı (thematic break / horizontal rule)' olarak bilinir."
```

### html-veryeasy-preformatted-code

```yaml
id: html-veryeasy-preformatted-code
version: 1
language: html
engine: none
difficulty: very_easy
title: "Önceden biçimlendirilmiş çok satırlı kod bloğu"
prompt: |
  Web sayfasında çok satırlı bir Python veya C kod bloğu sergileyin. Kodun girintileri,
  boşlukları ve satır sonları tarayıcı tarafından yutulmadan olduğu gibi korunmalı,
  ayrıca içeriğin bir bilgisayar kodu olduğu anlamsal olarak belirtilmelidir.
constraints:
  - "Boşlukları korumak için `<pre>` etiketi kullanılmalı"
  - "İçerideki kod parçası `<code>` etiketi ile sarmalanmalı (`<pre><code>...</code></pre>`)"
concept_tags: [standards, semantics]
checklist_extra:
  - "<pre> kullanılmadan sadece <code> kullanılıp satır başı girintileri kaybedilmiş mi?"
  - "HTML özel karakterleri (<, >) kaçış karakterleriyle (&lt;, &gt;) yazılmış mı?"
reference_solution_path: private/solutions/html-veryeasy-preformatted-code.html
hint_ladder:
  1: "HTML'de girintileri ve ardışık boşlukları olduğu gibi koruyan blok etiketi hangisidir?"
  2: "Bunun içine yazılan metnin yazılım kodu olduğunu semantik olarak nasıl etiketlersin?"
  3: "Bu yapı 'ön biçimli kod bloğu (preformatted code block)' olarak bilinir."
```

### html-veryeasy-inline-code

```yaml
id: html-veryeasy-inline-code
version: 1
language: html
engine: none
difficulty: very_easy
title: "Cümle içi kod ve fonksiyon adı gösterimi"
prompt: |
  Bir kılavuz cümlesi içinde geçen bir fonksiyon adını veya terminal komutunu
  (örneğin 'Terminalde `npm install` komutunu çalıştırın') gösteren bir paragraf yazın.
  Komut adı satır içi kod etiketi ile işaretlenmelidir.
constraints:
  - "Satır içi kod gösterimi için `<code>` etiketi kullanılmalı"
  - "Paragraf akışı bozulmadan tek satırda kalmalı"
concept_tags: [semantics, standards]
checklist_extra:
  - "Satır içi kod için blok oluşturan <pre> etiketi mi kullanılmış?"
  - "Yalnızca tırnak işareti koymak yerine <code> etiketi tercih edilmiş mi?"
reference_solution_path: private/solutions/html-veryeasy-inline-code.html
hint_ladder:
  1: "Bir paragraf içinde tek bir değişken veya komut adını işaretleyen satır içi etiket hangisidir?"
  2: "Kod parçasının etrafındaki metin akışını kırmadan sabit genişlikli fontla görüntülenmesini ne sağlar?"
  3: "Bu işaretleme 'satır içi kod etiketi (inline code)' olarak bilinir."
```

### html-veryeasy-time-datetime

```yaml
id: html-veryeasy-time-datetime
version: 1
language: html
engine: none
difficulty: very_easy
title: "Makine tarafından okunabilir zaman damgası"
prompt: |
  Bir haberin yayımlanma tarihini gösteren bir metin yazın (örneğin: '29 Ekim 2026 tarihinde yayımlandı').
  İnsanların okuduğu bu metnin arka planda arama motorları ve takvim yazılımları tarafından
  ISO 8601 standart formatında (YYYY-AA-GG) anlaşılabilmesini sağlayın.
constraints:
  - "Tarih `<time>` etiketi içine alınmalı"
  - "Makine formatı `datetime` niteliğinde (örneğin '2026-10-29') belirtilmeli"
concept_tags: [semantics, standards]
checklist_extra:
  - "datetime niteliğinde ISO 8601 formatı yerine geçersiz veya yerel tarih formatı mı yazılmış?"
  - "<time> etiketi metin içeriği olmadan boş mu bırakılmış?"
reference_solution_path: private/solutions/html-veryeasy-time-datetime.html
hint_ladder:
  1: "İnsanların okuduğu Türkçe tarih ile tarayıcıların anladığı standart tarihi bağlayan etiket hangisidir?"
  2: "Tarihin standart YYYY-MM-DD değerini hangi nitelikte saklarsın?"
  3: "Bu etiketleme 'makine tarafından okunabilir zaman damgası (time with datetime)' olarak bilinir."
```

### html-veryeasy-mark-highlight

```yaml
id: html-veryeasy-mark-highlight
version: 1
language: html
engine: none
difficulty: very_easy
title: "Arama sonucu vurgulama (fosforlu kalem efekti)"
prompt: |
  Bir arama sonucunda kullanıcının aradığı anahtar kelimenin eşleştiğini belirten bir
  cümle yazın. Eşleşen kelime, önem taşıdığı için değil, kullanıcının o anki arama
  eylemiyle ilgili olduğu için sarı fosforlu kalemle çizilmiş gibi anlamsal olarak
  vurgulanmalıdır.
constraints:
  - "İlgi odağı vurgusu için `<mark>` etiketi kullanılmalı"
  - "`<strong>` veya `<em>` ile karıştırılmamalı"
concept_tags: [semantics, standards]
checklist_extra:
  - "Arama sonucu vurgusu yerine güçlü önem belirten <strong> etiketi mi kullanılmış?"
  - "Sadece CSS arka plan rengi vermek yerine anlamsal <mark> etiketi tercih edildi mi?"
reference_solution_path: private/solutions/html-veryeasy-mark-highlight.html
hint_ladder:
  1: "Kullanıcının yaptığı bir aramada eşleşen kısımları işaretlemek için tasarlanmış özel HTML5 etiketi hangisidir?"
  2: "Varsayılan olarak sarı arka planla gelen bu anlamsal etiket nedir?"
  3: "Bu işaretleme 'arama ve ilgi vurgusu etiketi (mark element)' olarak bilinir."
```

### html-veryeasy-deleted-inserted-text

```yaml
id: html-veryeasy-deleted-inserted-text
version: 1
language: html
engine: none
difficulty: very_easy
title: "Belge düzenleme geçmişi (silinen ve eklenen metin)"
prompt: |
  Bir fiyat indirimini veya sözleşme taslağındaki değişikliği gösteren bir cümle kurun
  (örneğin: 'Eski fiyat: 100 TL, Yeni fiyat: 80 TL'). Eski değerin belgeden çıkarıldığını,
  yeni değerin ise belgeye sonradan eklendiğini ekran okuyuculara belirten anlamsal
  düzenleme etiketlerini kullanın.
constraints:
  - "Çıkarılan metin için `<del>` etiketi kullanılmalı"
  - "Eklenen yeni metin için `<ins>` etiketi kullanılmalı"
concept_tags: [semantics, accessibility]
checklist_extra:
  - "Yalnızca görsel üstü çizili (<s>) etiketi kullanılarak düzenleme anlamı kaybedilmiş mi?"
  - "Eklenen metin <u> ile sadece altı çizili mi yapılmış?"
reference_solution_path: private/solutions/html-veryeasy-deleted-inserted-text.html
hint_ladder:
  1: "Bir belgede resmi olarak silinmiş içeriği işaretleyen etiket hangisidir?"
  2: "Belgeye sonradan eklenmiş yeni içeriği temsil eden etiket nedir?"
  3: "Bu etiket ikilisi 'belge düzenleme geçmişi işaretlemesi (del and ins elements)' olarak bilinir."
```

### html-veryeasy-keyboard-input

```yaml
id: html-veryeasy-keyboard-input
version: 1
language: html
engine: none
difficulty: very_easy
title: "Klavye kısayol tuşları gösterimi"
prompt: |
  Bir programdaki kısayol tuşunu anlatan bir yönerge cümlesi yazın (örneğin: 'Kaydetmek
  için Ctrl + S tuşlarına basın'). Kullanıcının klavyeden basması gereken her bir tuş
  özel klavye girdi etiketiyle ayrı ayrı işaretlenmelidir.
constraints:
  - "Her klavye tuşu `<kbd>` etiketi içine alınmalı"
  - "Tuş kombinasyonları (örneğin Ctrl ve S) ayrı ayrı sarmalanmalı"
concept_tags: [semantics, standards]
checklist_extra:
  - "Klavye tuşları için genel <code> etiketi mi kullanılmış?"
  - "Tüm kombinasyon tek bir kbd içine atılmak yerine tuşlar bağımsız kbd etiketlerine bölünmüş mü?"
reference_solution_path: private/solutions/html-veryeasy-keyboard-input.html
hint_ladder:
  1: "Kullanıcının klavyeden veya sesle girmesi beklenen tuş vuruşlarını gösteren etiket hangisidir?"
  2: "Ctrl ve S tuşlarını ayrı iki tuş olarak nasıl etiketlersin?"
  3: "Bu etiket 'klavye girdisi etiketi (keyboard input element - kbd)' olarak bilinir."
```

### html-veryeasy-sample-output

```yaml
id: html-veryeasy-sample-output
version: 1
language: html
engine: none
difficulty: very_easy
title: "Program veya terminal çıktısı gösterimi"
prompt: |
  Bir yazılımın veya komut satırı aracının ürettiği örnek bir hata mesajını veya sistem
  yanıtını (örneğin: '404 Not Found' veya 'İşlem başarıyla tamamlandı') gösteren bir
  paragraf yazın. Çıktı metni, kullanıcı girdisi veya koddan ayırt edilerek sistem
  çıktısı etiketiyle işaretlenmelidir.
constraints:
  - "Sistem veya konsol çıktısı için `<samp>` etiketi kullanılmalı"
  - "Düz kod etiketi (`<code>`) ile karıştırılmamalı"
concept_tags: [semantics, standards]
checklist_extra:
  - "Program çıktısı için <code> kullanılarak ayrım kaçırılmış mı?"
  - "Örnek çıktının etrafında açıklayıcı bir bağlam metni var mı?"
reference_solution_path: private/solutions/html-veryeasy-sample-output.html
hint_ladder:
  1: "Bilgisayar programının kullanıcıya verdiği yanıtı/çıktıyı temsil eden etiket hangisidir?"
  2: "Sample (örnek çıktı) sözcüğünden türeyen etiketi hatırlıyor musun?"
  3: "Bu kullanım 'örnek program çıktısı etiketi (sample output - samp)' olarak bilinir."
```

### html-veryeasy-variable-definition

```yaml
id: html-veryeasy-variable-definition
version: 1
language: html
engine: none
difficulty: very_easy
title: "Matematiksel veya programlama değişkeni gösterimi"
prompt: |
  Matematiksel bir formülü veya bir yazılım denkliğini anlatan bir cümle kurun
  (örneğin: 'Üçgenin alanı a ve h değişkenleri için (a * h) / 2 formülüyle bulunur').
  Cümledeki matematiksel değişken harfleri anlamsal değişken etiketiyle işaretlenmelidir.
constraints:
  - "Değişken harfleri için `<var>` etiketi kullanılmalı"
  - "Yalnızca görsel italik (`<i>`) kullanılmamalı"
concept_tags: [semantics, standards]
checklist_extra:
  - "Değişken harfi için anlamsal <var> yerine sadece görsel <i> mi kullanılmış?"
  - "Her bağımsız değişken ayrı ayrı mı etiketlenmiş?"
reference_solution_path: private/solutions/html-veryeasy-variable-definition.html
hint_ladder:
  1: "Matematiksel ifadelerdeki bilinmeyenleri veya formül değişkenlerini belirten etiket hangisidir?"
  2: "Variable sözcüğünün kısaltması olan HTML etiketi nedir?"
  3: "Bu etiketleme 'matematiksel değişken etiketi (variable element - var)' olarak bilinir."
```

### html-veryeasy-document-title

```yaml
id: html-veryeasy-document-title
version: 1
language: html
engine: none
difficulty: very_easy
title: "Tarayıcı sekme başlığı tanımlama"
prompt: |
  Tarayıcı sekmesinde, yer imlerinde ve arama motoru sonuç sayfalarında görüntülenecek
  olan sayfa başlığını `<head>` etiketi içerisinde tanımlayın. Başlık sitenin genel adı
  ve geçerli sayfanın konusunu içermelidir (örneğin: 'Giriş Yap — KodMentor').
constraints:
  - "`<head>` içinde geçerli bir `<title>` etiketi bulunmalı"
  - "Başlık boş olmamalı ve sayfayı özetlemeli"
concept_tags: [standards, accessibility]
checklist_extra:
  - "<title> etiketi body içine mi yazılmış?"
  - "Başlık 'Sayfa 1' veya 'Başlıksız' gibi anlamsız bir metin mi içeriyor?"
reference_solution_path: private/solutions/html-veryeasy-document-title.html
hint_ladder:
  1: "Tarayıcının en üst sekmesinde görünen metni hangi etiket belirler?"
  2: "Bu etiket <head> içinde mi yoksa <body> içinde mi yer almalıdır?"
  3: "Bu zorunlu alan 'belge başlığı etiketi (document title)' olarak bilinir."
```

### html-veryeasy-favicon-link

```yaml
id: html-veryeasy-favicon-link
version: 1
language: html
engine: none
difficulty: very_easy
title: "Site simgesi (favicon) bağlama"
prompt: |
  Tarayıcı sekmesinde sayfa başlığının solunda görüntülenecek olan küçük site simgesini
  (favicon) `<head>` bölümünde harici kaynak bağlama etiketi ile tanımlayın. Simge
  dosyasının yolu ve mime tipi doğru belirtilmelidir.
constraints:
  - "`<link>` etiketi üzerinde rel='icon' niteliği bulunmalı"
  - "href niteliği simge dosyasını göstermeli"
concept_tags: [standards, images]
checklist_extra:
  - "rel niteliği yerine hatalı bir ilişki adı mı yazılmış?"
  - "<link> etiketinin kapanış etiketi olmayan boş etiket olduğu doğru kurgulanmış mı?"
reference_solution_path: private/solutions/html-veryeasy-favicon-link.html
hint_ladder:
  1: "Harici kaynakları HTML belgesine bağlamak için hangi etiket kullanılır?"
  2: "Site simgesi ilişkisini belirtmek için rel niteliğine ne yazılır?"
  3: "Bu tanımlama 'site simgesi bağlama (favicon link)' olarak bilinir."
```

### html-veryeasy-stylesheet-link

```yaml
id: html-veryeasy-stylesheet-link
version: 1
language: html
engine: none
difficulty: very_easy
title: "Harici CSS stil dosyası bağlama"
prompt: |
  Sayfanın görsel tasarımını belirleyen harici bir 'styles.css' dosyasını `<head>` bölümüne
  bağlayan geçerli link etiketini yazın. İlişki türü eksiksiz belirtilmelidir.
constraints:
  - "`<link>` etiketi kullanılmalı"
  - "rel='stylesheet' niteliği bulunmalı ve href geçerli bir css dosyasını göstermeli"
concept_tags: [standards, performance]
checklist_extra:
  - "rel niteliği unutulup tarayıcının dosyayı CSS olarak işlememesi riski oluşmuş mu?"
  - "<link> etiketi yanlışlıkla <body> içine mi yerleştirilmiş?"
reference_solution_path: private/solutions/html-veryeasy-stylesheet-link.html
hint_ladder:
  1: "Stil sayfalarını HTML dokümanına bağlayan rel değeri hangisidir?"
  2: "Dosya yolu hangi nitelik aracılığıyla belirtilir?"
  3: "Bu işlem 'harici stil sayfası bağlama (external stylesheet link)' olarak bilinir."
```

### html-veryeasy-definition-list

```yaml
id: html-veryeasy-definition-list
version: 1
language: html
engine: none
difficulty: very_easy
title: "Tanım listesi ve terim-açıklama ikilileri"
prompt: |
  Bir sözlük veya teknik terimler kılavuzu oluşturun. En az iki terim (`<dt>`) ve bu
  terimlerin açıklamalarını (`<dd>`) barındıran anlamsal tanım listesi etiketini kullanın.
  Bir terime birden fazla açıklama da bağlanabilir.
constraints:
  - "Kök liste için `<dl>` etiketi kullanılmalı"
  - "Terimler için `<dt>`, açıklamalar için `<dd>` etiketleri doğru sırada kullanılmalı"
concept_tags: [lists, semantics]
checklist_extra:
  - "Tanım listesi yerine standart <ul> veya tablolar mı kullanılmış?"
  - "<dt> ve <dd> etiketleri <dl> dışında bağımsız mı kullanılmış?"
reference_solution_path: private/solutions/html-veryeasy-definition-list.html
hint_ladder:
  1: "Anahtar-değer veya terim-tanım ikililerini temsil eden özel HTML listesi hangisidir?"
  2: "Definition Term ve Definition Description etiketlerinin kısaltmaları nedir?"
  3: "Bu yapı 'anlamsal tanım listesi (description/definition list - dl)' olarak bilinir."
```

### html-veryeasy-nested-list-steps

```yaml
id: html-veryeasy-nested-list-steps
version: 1
language: html
engine: none
difficulty: very_easy
title: "İç içe çok seviyeli liste yapısı"
prompt: |
  Bir ana başlık listesi ve bu maddelerden birinin altında yer alan alt maddeleri gösteren
  iç içe geçmiş (nested) bir liste oluşturun. Alt liste, doğrudan dıştaki `<ul>` veya `<ol>`
  etiketinin çocuğu olmamalı; mutlaka ait olduğu ebeveyn `<li>` etiketinin içine
  yerleştirilmelidir.
constraints:
  - "Alt liste doğrudan dış listenin değil, bir `<li>` etiketinin içinde yer almalı"
  - "HTML sözdizimi geçerli ve kapanış etiketleri doğru kapatılmış olmalı"
concept_tags: [lists, standards]
checklist_extra:
  - "Alt <ul> etiketi <li> dışına, iki <li> arasına doğrudan mı konulmuş (sözdizimi hatası)?"
  - "Ekran okuyucuların liste derinliğini doğru anlaması sağlandı mı?"
reference_solution_path: private/solutions/html-veryeasy-nested-list-steps.html
hint_ladder:
  1: "Bir listenin içine başka bir liste koyarken alt listenin hangi etiketin içinde yaşaması zorunludur?"
  2: "<li> etiketi kapanmadan önce içine yeni bir <ul> açmak neden şarttır?"
  3: "Bu kural 'geçerli iç içe liste yapısı (valid nested list)' olarak bilinir."
```

### html-veryeasy-button-element

```yaml
id: html-veryeasy-button-element
version: 1
language: html
engine: none
difficulty: very_easy
title: "Tıklanabilir buton ve varsayılan tip belirleme"
prompt: |
  Form dışındaki bir arayüz etkileşimini tetikleyen tıklanabilir bir buton oluşturun.
  HTML'de bir butonun varsayılan tipi `submit` olduğundan, beklenmedik form gönderimlerini
  önlemek için butonun türünü açıkça genel amaçlı buton (`type="button"`) olarak belirtin.
constraints:
  - "Anlamsal `<button>` etiketi kullanılmalı (`<div>` ile buton yapılmamalı)"
  - "`type='button'` niteliği açıkça yazılmalı"
concept_tags: [forms, accessibility, standards]
checklist_extra:
  - "Buton yerine <div onclick=...> veya <a> etiketi mi kullanılmış (erişilebilirlik hatası)?"
  - "type niteliği atlanarak varsayılan submit tipine mi bırakılmış?"
reference_solution_path: private/solutions/html-veryeasy-button-element.html
hint_ladder:
  1: "Klavye ile odaklanılabilen ve Enter/Boşluk tuşlarıyla tetiklenen yerleşik etiket hangisidir?"
  2: "Butonun bir formu göndermesini engellemek için hangi type değerini vermelisiniz?"
  3: "Bu tanım 'açık tip bildirimli buton etiketi (button with explicit type)' olarak bilinir."
```

### html-veryeasy-address-contact

```yaml
id: html-veryeasy-address-contact
version: 1
language: html
engine: none
difficulty: very_easy
title: "Yazar ve kurum iletişim bilgisi bloğu"
prompt: |
  Bir web sitesinin alt bilgisinde (footer) veya bir makalenin sonunda yazarın ya da
  şirketin iletişim bilgilerini (e-posta, fiziksel adres, telefon) sunan anlamsal iletişim
  etiketini oluşturun. Genel amaçlı posta kutusu veya rastgele adresler için değil,
  sayfanın sahibinin iletişim bilgileri için kullanılmalıdır.
constraints:
  - "İletişim bilgileri `<address>` etiketi içinde yer almalı"
  - "İçerisinde en az bir e-posta veya telefon bağlantısı barındırmalı"
concept_tags: [semantics, standards]
checklist_extra:
  - "<address> etiketi genel bir posta adresi veya alakasız adresler için mi kullanılmış?"
  - "Sayfanın sorumlusunun iletişim bilgilerini doğru temsil ediyor mu?"
reference_solution_path: private/solutions/html-veryeasy-address-contact.html
hint_ladder:
  1: "Belgenin veya makalenin sahibine ait iletişim bilgilerini belirtmek için tasarlanmış etiket hangisidir?"
  2: "Bu etiket rastgele adresler için değil, sayfanın yazarı/sahibi için mi geçerlidir?"
  3: "Bu anlamsal alan 'iletişim bilgisi etiketi (address element)' olarak bilinir."
```

### html-veryeasy-meta-description

```yaml
id: html-veryeasy-meta-description
version: 1
language: html
engine: none
difficulty: very_easy
title: "Arama motoru sayfa açıklaması meta etiketi"
prompt: |
  Google ve diğer arama motorlarının arama sonuçları listesinde (SERP) sayfa başlığının
  altında özet metin olarak göstereceği sayfa açıklaması meta etiketini `<head>` içerisine
  ekleyin. Açıklama 50 ile 160 karakter arasında bilgilendirici bir metin olmalıdır.
constraints:
  - "name='description' niteliği bulunmalı"
  - "content niteliğinde anlamlı bir sayfa özeti yer almalı"
concept_tags: [standards, performance]
checklist_extra:
  - "name yerine property veya geçersiz bir nitelik mi yazılmış?"
  - "content niteliği boş veya sadece anahtar kelime yığını mı içeriyor?"
reference_solution_path: private/solutions/html-veryeasy-meta-description.html
hint_ladder:
  1: "Arama sonuçlarında sayfanın altında çıkan kısa özeti hangi meta etiketi sağlar?"
  2: "Meta etiketinin name niteliğine ne yazılmalıdır?"
  3: "Bu tanımlama 'arama motoru açıklama meta etiketi (meta description)' olarak bilinir."
```

### html-veryeasy-ruby-annotation

```yaml
id: html-veryeasy-ruby-annotation
version: 1
language: html
engine: none
difficulty: very_easy
title: "Doğu Asya karakterleri telaffuz kılavuzu"
prompt: |
  Japonca Kanji veya Çince karakterlerin üzerinde okunuşlarını (furigana/pinyin) küçük
  metin olarak gösteren bir dil kılavuzu yapısı oluşturun. Karakter ve telaffuz anlamsal
  etiketlerle eşleştirilmelidir.
constraints:
  - "Kök sarmalayıcı olarak `<ruby>` etiketi kullanılmalı"
  - "Telaffuz açıklaması `<rt>` etiketi içinde belirtilmeli"
concept_tags: [semantics, standards]
checklist_extra:
  - "Eski tarayıcılar için parantezli yedekleme (<rp>) düşünülmüş mü?"
  - "<rt> etiketi doğru kanji karakteriyle hizalanmış mı?"
reference_solution_path: private/solutions/html-veryeasy-ruby-annotation.html
hint_ladder:
  1: "Uzak doğu dillerinde harflerin üzerine küçük telaffuz notu ekleyen etiket hangisidir?"
  2: "Ruby text anlamına gelen ve açıklamayı taşıyan etiket nedir?"
  3: "Bu işaretleme 'yakut metin telaffuz açıklaması (ruby annotation)' olarak bilinir."
```

### html-veryeasy-bdi-bi-directional

```yaml
id: html-veryeasy-bdi-bi-directional
version: 1
language: html
engine: none
difficulty: very_easy
title: "Çift yönlü metin yalıtımı (LTR/RTL güvenliği)"
prompt: |
  Kullanıcıların Arapça veya İbranice gibi sağdan sola (RTL) yazılan kullanıcı adları
  belirleyebildiği bir yorum listesi oluşturun. Bu kullanıcı adının etrafındaki soldan
  sağa (LTR) Türkçe cümlenin hizalamasını ve noktalama işaretlerini bozmaması için kullanıcı
  adını metin yönünden yalıtan anlamsal etiketi kullanın.
constraints:
  - "Bilinmeyen yönlü dinamik metin `<bdi>` etiketi ile sarmalanmalı"
  - "Dışarıdaki metnin akış yönünün bozulması engellenmeli"
concept_tags: [standards, accessibility, security]
checklist_extra:
  - "Zorla yön dayatan <bdo> yerine otomatik yalıtım sağlayan <bdi> mı tercih edildi?"
  - "Kullanıcı adından sonra gelen iki nokta üst üste (:) işaretinin sola kayması önlendi mi?"
reference_solution_path: private/solutions/html-veryeasy-bdi-bi-directional.html
hint_ladder:
  1: "Dışarıdan gelen metnin yönü bilinmediğinde etrafındaki metnin yönünü bozmamasını sağlayan etiket hangisidir?"
  2: "Bi-directional Isolation ifadesinin kısaltması olan etiket nedir?"
  3: "Bu etiket 'çift yönlü metin yalıtımı (bi-directional isolation - bdi)' olarak bilinir."
```

### html-veryeasy-small-fine-print

```yaml
id: html-veryeasy-small-fine-print
version: 1
language: html
engine: none
difficulty: very_easy
title: "Yasal uyarı ve küçük dipnot metni"
prompt: |
  Bir web sitesinin en altında yer alan telif hakkı bildirimini veya yasal sorumluluk
  reddi metnini yazın. Metin görsel olarak küçük görünmenin ötesinde, hukuki dipnot
  veya ikincil öneme sahip yan açıklama olduğunu belirten anlamsal etiketle işaretlenmelidir.
constraints:
  - "Yasal dipnot metni için `<small>` etiketi kullanılmalı"
  - "Telif hakkı veya feragatname metni içermeli"
concept_tags: [semantics, standards]
checklist_extra:
  - "Sadece CSS 'font-size: small' verilip anlamsal <small> etiketi atlanmış mı?"
  - "<small> etiketi ana metnin yerine gereksiz yere tüm sayfaya mı uygulanmış?"
reference_solution_path: private/solutions/html-veryeasy-small-fine-print.html
hint_ladder:
  1: "HTML5'te telif hakkı, şartlar ve koşullar gibi küçük puntolu yasal metinleri belirten etiket hangisidir?"
  2: "Eski HTML'de sadece görsel olan ama HTML5'te anlamsal kılınan etiket nedir?"
  3: "Bu işaretleme 'anlamsal küçük dipnot etiketi (small element)' olarak bilinir."
```

### html-veryeasy-span-inline

```yaml
id: html-veryeasy-span-inline
version: 1
language: html
engine: none
difficulty: very_easy
title: "Anlamsal olmayan satır içi sarmalayıcı"
prompt: |
  Bir paragraf içindeki belirli bir kelime grubunu (örneğin bir fiyat etiketi veya renkli
  bir kelime) CSS ile hedefleyebilmek için satır içi akışı bozmadan ve fazladan hiçbir
  anlamsal anlam yüklemeden sarmalayan jenerik satır içi etiketi kullanın.
constraints:
  - "Anlamsal olmayan satır içi gruplama için `<span>` etiketi kullanılmalı"
  - "Paragrafın satır akışı kırılmamalı"
concept_tags: [standards, semantics]
checklist_extra:
  - "Satır içi hedefleme için blok oluşturan <div> mi kullanılmış?"
  - "Anlamsal bir etiket (strong, em vb.) gerekmediğinde doğru şekilde span mı seçilmiş?"
reference_solution_path: private/solutions/html-veryeasy-span-inline.html
hint_ladder:
  1: "Hiçbir varsayılan anlamı veya görsel etkisi olmayan satır içi etiket hangisidir?"
  2: "Bir cümlenin ortasındaki bir kelimeye sınıf (class) atamak için ne kullanırsın?"
  3: "Bu etiket 'jenerik satır içi sarmalayıcı (generic inline container - span)' olarak bilinir."
```

### html-veryeasy-div-generic

```yaml
id: html-veryeasy-div-generic
version: 1
language: html
engine: none
difficulty: very_easy
title: "Anlamsal olmayan blok düzeyinde sarmalayıcı"
prompt: |
  Sayfadaki iki bağımsız paragrafı yalnızca CSS ızgara/kutu yerleşimi amacıyla bir araya
  getiren, ancak semantik olarak hiçbir özel anlam (makale, navigasyon vb.) taşımayan
  jenerik blok sarmalayıcı etiketi oluşturun.
constraints:
  - "Anlamsal olmayan blok düzeyinde sarmalama için `<div>` etiketi kullanılmalı"
  - "İçerisinde en az bir çocuk eleman barındırmalı"
concept_tags: [standards, semantics]
checklist_extra:
  - "Header, nav veya main gibi semantik bir etiket yerine tembellikle div mi kullanılmış?"
  - "Yalnızca biçimlendirme ve stil hedefi için div doğru amaçla mı tercih edilmiş?"
reference_solution_path: private/solutions/html-veryeasy-div-generic.html
hint_ladder:
  1: "Hiçbir anlamsal değeri olmayan blok seviyesi kutu etiketi hangisidir?"
  2: "CSS ile stillendirmek için elemanları gruplarken semantik alternatif yoksa ne kullanılır?"
  3: "Bu eleman 'jenerik blok sarmalayıcı (generic block container - div)' olarak bilinir."
```

### html-veryeasy-external-link-target

```yaml
id: html-veryeasy-external-link-target
version: 1
language: html
engine: none
difficulty: very_easy
title: "Yeni sekmede açılan güvenli dış bağlantı"
prompt: |
  Kullanıcıyı yeni bir tarayıcı sekmesinde (`target="_blank"`) açılacak harici bir web
  sitesine yönlendiren bir bağlantı oluşturun. Açılan yeni sayfanın orijinal sayfanızın
  pencere nesnesine (window.opener) erişip kötü niyetli yönlendirmeler yapmasını önleyen
  ve performansı koruyan güvenlik ilişkisini eksiksiz ekleyin.
constraints:
  - "target='_blank' niteliği bulunmalı"
  - "Güvenlik açığını kapatmak için rel='noopener noreferrer' niteliği eklenmeli"
concept_tags: [links, security, standards]
checklist_extra:
  - "target='_blank' kullanıldığı halde rel='noopener' veya 'noreferrer' unutulmuş mu?"
  - "Açıklayıcı metin içinde bağlantının yeni sekmede açılacağı belirtilmiş mi?"
reference_solution_path: private/solutions/html-veryeasy-external-link-target.html
hint_ladder:
  1: "Bir bağlantıyı yeni sekmede açtığında hedef sayfanın sitenizi ele geçirmesini önleyen rel değeri nedir?"
  2: "Reverse tabnabbing saldırısını engelleyen ilişki nitelikleri hangileridir?"
  3: "Bu güvenlik kuralı 'yeni sekme bağlantı güvenliği (target blank with noopener)' olarak bilinir."
```

### html-veryeasy-anchor-jump-id

```yaml
id: html-veryeasy-anchor-jump-id
version: 1
language: html
engine: none
difficulty: very_easy
title: "Sayfa içi konuma atlama bağlantısı (Çapa linki)"
prompt: |
  Sayfanın en üstünde yer alan ve tıklandığında sayfanın alt kısımlarındaki 'İletişim'
  bölümüne pürüzsüzce kaymasını sağlayan bir sayfa içi atlama bağlantısı (anchor jump)
  kurun. Hedeflenen bölümün kimliği (`id`) ile bağlantının hedefi (`href`) doğru eşleşmelidir.
constraints:
  - "Hedef elemanın benzersiz bir id niteliği olmalı (örneğin id='iletisim')"
  - "Bağlantının href niteliği diyez işaretiyle bu kimliği göstermeli (href='#iletisim')"
concept_tags: [links, navigation, standards]
checklist_extra:
  - "href niteliğindeki # işareti unutulmuş mu?"
  - "Sayfada aynı id değerine sahip birden fazla eleman kullanılmış mı (geçersiz HTML)?"
reference_solution_path: private/solutions/html-veryeasy-anchor-jump-id.html
hint_ladder:
  1: "Sayfa içi bir elemana atlamak için linkin href değerine kimlikten önce ne yazılır?"
  2: "Hedef elemana bu bağlantıyı yakalaması için hangi nitelik verilmelidir?"
  3: "Bu yöntem 'sayfa içi parça bağlantısı (fragment identifier / anchor link)' olarak bilinir."
```

### html-veryeasy-download-link

```yaml
id: html-veryeasy-download-link
version: 1
language: html
engine: none
difficulty: very_easy
title: "Doğrudan dosya indirme bağlantısı"
prompt: |
  Kullanıcı tıkladığında dosyayı tarayıcı penceresinde açmak yerine, doğrudan kullanıcının
  bilgisayarına indirmesini sağlayan ve indirilecek varsayılan dosya adını belirten bir
  indirme bağlantısı oluşturun.
constraints:
  - "`<a>` etiketi üzerinde `download` niteliği bulunmalı"
  - "download niteliğine önerilen dosya adı (örneğin download='rapor.pdf') atanmalı"
concept_tags: [links, standards]
checklist_extra:
  - "download niteliği atlanarak tarayıcının dosyayı doğrudan görüntülemesine mi bırakılmış?"
  - "href niteliği geçerli bir dosya yolunu gösteriyor mu?"
reference_solution_path: private/solutions/html-veryeasy-download-link.html
hint_ladder:
  1: "Bir bağlantının tıklanınca sayfada açılmak yerine indirilmesini tetikleyen HTML niteliği nedir?"
  2: "İndirilen dosyanın varsayılan adını bu niteliğe değer olarak nasıl verirsin?"
  3: "Bu nitelik 'bağlantı indirme özniteliği (download attribute)' olarak bilinir."
```

### html-veryeasy-figure-caption

```yaml
id: html-veryeasy-figure-caption
version: 1
language: html
engine: none
difficulty: very_easy
title: "Açıklamalı görsel ve altyazı bloğu"
prompt: |
  Bir görseli ve hemen altında yer alan açıklama altyazısını (caption) tek bir bağımsız
  içerik birimi olarak birleştiren anlamsal görsel bloğu oluşturun. Ekran okuyucular
  görsel ile altyazı arasındaki bağı doğrudan kurabilmelidir.
constraints:
  - "Dış sarmalayıcı olarak `<figure>` etiketi kullanılmalı"
  - "Altyazı metni `<figcaption>` etiketi içinde yer almalı"
  - "figure etiketi içinde bir `<img>` bulunmalı"
concept_tags: [images, semantics, accessibility]
checklist_extra:
  - "Altyazı için figcaption yerine düz <p> mi kullanılmış?"
  - "figcaption etiketi figure sınırlarının dışına mı taşmış?"
reference_solution_path: private/solutions/html-veryeasy-figure-caption.html
hint_ladder:
  1: "Şema, fotoğraf ve açıklamalarını bağımsız bir ünite olarak toplayan etiket hangisidir?"
  2: "Görselin altındaki resmi başlığı/altyazıyı temsil eden çocuk etiket nedir?"
  3: "Bu yapı 'anlamsal figür ve altyazı bloğu (figure with figcaption)' olarak bilinir."
```

### html-veryeasy-audio-controls

```yaml
id: html-veryeasy-audio-controls
version: 1
language: html
engine: none
difficulty: very_easy
title: "Kullanıcı denetimli ses oynatıcı"
prompt: |
  Kullanıcının çalma, duraklatma ve ses seviyesini ayarlayabileceği yerleşik bir ses çalar
  bileşeni ekleyin. Sayfa açılır açılmaz kullanıcının izni olmadan ses çalmaya başlamamalı
  (otomatik oynatma olmamalı) ve kullanıcıya görünür denetim düğmeleri sunulmalıdır.
constraints:
  - "`<audio>` etiketi üzerinde `controls` niteliği bulunmalı"
  - "`autoplay` niteliği kesinlikle kullanılmamalı"
  - "İçerisinde en az bir `<source>` etiketi veya src bulunmalı"
concept_tags: [standards, accessibility, performance]
checklist_extra:
  - "controls niteliği unutulup ses oynatıcının ekranda görünmez kalması hatası yapılmış mı?"
  - "Kullanıcı deneyimini bozan autoplay niteliği verilmiş mi?"
reference_solution_path: private/solutions/html-veryeasy-audio-controls.html
hint_ladder:
  1: "Tarayıcının varsayılan oynatma/durdurma arayüzünü ekrana getirmesi için audio etiketine ne eklenir?"
  2: "Kullanıcının haberi olmadan müziğin başlamasını önlemek için hangi nitelikten kaçınmalısın?"
  3: "Bu bileşen 'denetimli yerel ses oynatıcı (audio with controls)' olarak bilinir."
```

### html-veryeasy-video-controls

```yaml
id: html-veryeasy-video-controls
version: 1
language: html
engine: none
difficulty: very_easy
title: "Görünür denetimli temel video oynatıcı"
prompt: |
  Bir web sayfasında video içeriği gösteren bir oynatıcı tanımlayın. Oynatıcının ekranda
  doğru boyutlanması için genişlik ve yükseklik değerleri belirtilmeli, kullanıcının
  videoyu kontrol edebilmesi için oynatma denetimleri aktif edilmelidir.
constraints:
  - "`<video>` etiketi üzerinde `controls` niteliği bulunmalı"
  - "Düzen kaymasını (CLS) önlemek için `width` ve `height` nitelikleri tanımlanmalı"
concept_tags: [standards, performance, accessibility]
checklist_extra:
  - "controls niteliği unutularak video durağan bir resim gibi mi kalmış?"
  - "Video yüklenene kadar sayfa düzeninin zıplamasını önleyen genişlik/yükseklik boyutları tanımlı mı?"
reference_solution_path: private/solutions/html-veryeasy-video-controls.html
hint_ladder:
  1: "Kullanıcının videoyu başlatıp durdurabilmesi için video etiketine hangi boole niteliği eklersin?"
  2: "Sayfa düzeni kaymasını (Cumulative Layout Shift) engellemek için hangi iki boyut niteliğini yazmalısın?"
  3: "Bu tanımlama 'boyutlandırılmış ve denetimli video bileşeni' olarak bilinir."
```

### html-veryeasy-meter-gauge

```yaml
id: html-veryeasy-meter-gauge
version: 1
language: html
engine: none
difficulty: very_easy
title: "Skaler ölçüm göstergesi (Disk doluluğu vb.)"
prompt: |
  Sabit bir minimum ve maksimum aralığı bilinen bir değeri (örneğin 500 GB diskin 350 GB
  dolu olması veya bir sınavdan 100 üzerinden 85 alınması) anlamsal gösterge etiketiyle
  gösterin. Bir işlemin devam eden ilerlemesi değil, bilinen bir aralıktaki anlık skaler
  ölçüm temsil edilmelidir.
constraints:
  - "Skaler ölçüm için anlamsal `<meter>` etiketi kullanılmalı"
  - "`value`, `min` ve `max` nitelikleri doğru sayısal değerlerle tanımlanmalı"
concept_tags: [forms, standards, semantics]
checklist_extra:
  - "Sabit ölçüm için progress (ilerleme çubuğu) etiketi mi kullanılmış (kavram yanılgısı)?"
  - "Eski tarayıcılar için etiket içinde metin tabanlı yedek değer bırakılmış mı?"
reference_solution_path: private/solutions/html-veryeasy-meter-gauge.html
hint_ladder:
  1: "Sabit aralıklı bir göstergeyi (termometre, disk alanı, yakıt deposu) gösteren HTML5 etiketi hangisidir?"
  2: "Belirli bir aralıktaki anlık skaler büyüklükleri ve kapasiteleri ölçmek için hangi etiket kullanılır?"
  3: "Bu etiket 'skaler ölçüm göstergesi etiketi (meter element)' olarak bilinir."
```

### html-veryeasy-progress-bar

```yaml
id: html-veryeasy-progress-bar
version: 1
language: html
engine: none
difficulty: very_easy
title: "İşlem ilerleme çubuğu"
prompt: |
  Bir dosya indirme işleminin veya form tamamlama sürecinin o anki tamamlanma oranını
  (örneğin %70 tamamlandı) gösteren anlamsal bir ilerleme çubuğu oluşturun.
  Değer ve maksimum sınır nitelikleri açıkça tanımlanmalıdır.
constraints:
  - "Devam eden bir süreç için `<progress>` etiketi kullanılmalı"
  - "`value` ve `max` nitelikleri eksiksiz belirtilmeli"
concept_tags: [forms, standards, semantics]
checklist_extra:
  - "İlerleme çubuğu yerine meter etiketi mi kullanılmış?"
  - "Ekran okuyucular ve eski tarayıcılar için etiket arasına metin alternatifi (örneğin %70) yazılmış mı?"
reference_solution_path: private/solutions/html-veryeasy-progress-bar.html
hint_ladder:
  1: "Bir görevin tamamlanma yüzdesini gösteren dinamik HTML5 ilerleme etiketi hangisidir?"
  2: "0 ile 100 arasındaki ilerlemeyi belirtmek için hangi iki nitelik eşleşir?"
  3: "Bu bileşen 'ilerleme çubuğu etiketi (progress element)' olarak bilinir."
```

### html-veryeasy-wbr-word-break

```yaml
id: html-veryeasy-wbr-word-break
version: 1
language: html
engine: none
difficulty: very_easy
title: "Uzun kelimelerde önerilen satır bölme noktası"
prompt: |
  Çok uzun bir URL adresi veya tek parça teknik bir terim içeren dar bir metin kutusu
  yazın. Kelimenin kutuyu taşırıp yatay kaydırma çubuğu çıkarmaması için, tarayıcıya
  ihtiyaç duyduğu takdirde bu uzun kelimeyi tam olarak nereden bölebileceğini öneren
  satır bölme fırsatı etiketini ekleyin.
constraints:
  - "Satır bölme fırsatı için `<wbr>` etiketi kullanılmalı"
  - "Uzun kelimenin doğal hece veya ayrım noktasına yerleştirilmeli"
concept_tags: [standards, performance]
checklist_extra:
  - "Kelimeyi doğrudan bölen sert <br> etiketi mi kullanılmış?"
  - "Tarayıcının yalnızca sığmadığı durumda bölmesini sağlayan <wbr> doğru konumlandırıldı mı?"
reference_solution_path: private/solutions/html-veryeasy-wbr-word-break.html
hint_ladder:
  1: "Tarayıcıya 'eğer satıra sığmıyorsan bu kelimeyi tam buradan bölebilirsin' diyen yumuşak bölme etiketi nedir?"
  2: "Word Break Opportunity ifadesinin kısaltması olan etiket hangisidir?"
  3: "Bu etiket 'isteğe bağlı satır bölme fırsatı etiketi (word break opportunity - wbr)' olarak bilinir."
```

### html-veryeasy-template-element

```yaml
id: html-veryeasy-template-element
version: 1
language: html
engine: none
difficulty: very_easy
title: "Görünmeyen HTML şablon bloğu"
prompt: |
  JavaScript tarafından klonlanıp sayfaya dinamik olarak eklenecek, ancak sayfa ilk
  yüklendiğinde tarayıcı tarafından ekranda kesinlikle render edilmeyen (görünmez kalan)
  ve içindeki resimleri erkenden yüklemeyen standart HTML şablon bloğu oluşturun.
constraints:
  - "İstemci tarafı şablonu için `<template>` etiketi kullanılmalı"
  - "İçerisinde bir kart veya liste elemanı şablon iskeleti yer almalı"
concept_tags: [standards, performance, semantics]
checklist_extra:
  - "Şablon içeriğini gizlemek için 'display: none' verilmiş div mi kullanılmış?"
  - "<template> etiketinin içindeki medya kaynaklarının sayfa açılışında indirilmediği doğru anlaşılmış mı?"
reference_solution_path: private/solutions/html-veryeasy-template-element.html
hint_ladder:
  1: "Sayfa açıldığında render edilmeyen ve script ile kopyalanmayı bekleyen resmi HTML5 etiketi hangisidir?"
  2: "CSS ile gizlenmiş div yerine tarayıcının çalıştırmadığı şablon etiketini hatırlıyor musun?"
  3: "Bu eleman 'HTML içerik şablonu etiketi (template element)' olarak bilinir."
```

---

## 2. Kolay (Easy) — 50 Soru

### html-easy-accessible-text-input

```yaml
id: html-easy-accessible-text-input
version: 1
language: html
engine: none
difficulty: easy
title: "Açık etiket bağlantılı metin giriş alanı"
prompt: |
  Bir kullanıcı kayıt formunda 'Adınız ve Soyadınız' bilgisini alan bir metin kutusu
  tasarlayın. Ekran okuyucuların alana odaklanıldığında etiketi seslendirebilmesi ve
  fareyle metne tıklandığında imlecin kutu içine otomatik odaklanabilmesi için etiket
  ile girdi alanını açıkça (explicit association) birbirine bağlayın.
constraints:
  - "`<label>` etiketinin `for` niteliği ile `<input>` etiketinin `id` niteliği birebir eşleşmeli"
  - "`<input>` etiketinde `type='text'` açıkça belirtilmeli"
concept_tags: [forms, accessibility, input-validation]
checklist_extra:
  - "for ve id nitelikleri arasındaki harf veya yazım farkı yüzünden bağlantı kopmuş mu?"
  - "label etiketi yerine anlamsız span veya p etiketi mi kullanılmış?"
reference_solution_path: private/solutions/html-easy-accessible-text-input.html
hint_ladder:
  1: "Etiketin hangi girdi kutusuna ait olduğunu tarayıcıya söyleyen nitelik ikilisi hangisidir?"
  2: "label etiketinin for niteliğine input'un hangi değerini yazmalısın?"
  3: "Bu yöntem 'açık etiket-girdi eşleştirmesi (explicit label association)' olarak bilinir."
```

### html-easy-password-input

```yaml
id: html-easy-password-input
version: 1
language: html
engine: none
difficulty: easy
title: "Maskeli şifre alanı ve parola yöneticisi uyumu"
prompt: |
  Kullanıcının girdiği karakterleri ekranda noktalarla maskeleyen ve parola yöneticilerinin
  (password managers) bu alanın mevcut bir parola mı yoksa yeni oluşturulan bir parola mı
  olduğunu anlamasını sağlayan standart bir şifre giriş alanı oluşturun.
constraints:
  - "`<input>` üzerinde `type='password'` niteliği bulunmalı"
  - "Parola yöneticileri için uygun `autocomplete` niteliği ('current-password' veya 'new-password') eklenmeli"
concept_tags: [forms, security, accessibility]
checklist_extra:
  - "autocomplete niteliği atlanarak parola yöneticilerinin yanlış alanı doldurması riski alınmış mı?"
  - "Şifre alanına bağlı erişilebilir bir <label> tanımlı mı?"
reference_solution_path: private/solutions/html-easy-password-input.html
hint_ladder:
  1: "Girdi karakterlerini ekranda gizleyen yerel form girdi tipi nedir?"
  2: "Tarayıcının şifre kaydetme önerisini doğru tetiklemek için autocomplete niteliğine ne yazılır?"
  3: "Bu alan 'güvenli şifre girişi ve otomatik tamamlama ipucu' olarak bilinir."
```

### html-easy-email-input-validation

```yaml
id: html-easy-email-input-validation
version: 1
language: html
engine: none
difficulty: easy
title: "E-posta giriş alanı ve yerel format denetimi"
prompt: |
  Kullanıcıdan e-posta adresi alan bir form elemanı yazın. Mobil cihazlarda klavyenin
  otomatik olarak '@' ve '.com' tuşlarını içeren e-posta moduna geçmesini ve form
  gönderilmeden önce tarayıcının yerel olarak '@' işareti denetimi yapmasını sağlayın.
constraints:
  - "`<input>` üzerinde `type='email'` niteliği kullanılmalı"
  - "Açıkça bağlı bir `<label>` etiketi bulunmalı"
concept_tags: [forms, input-validation, accessibility]
checklist_extra:
  - "Standart type='text' kullanılarak mobil klavye ve tarayıcı doğrulama avantajı kaçırılmış mı?"
  - "E-posta alanı için name niteliği tanımlanmış mı?"
reference_solution_path: private/solutions/html-easy-email-input-validation.html
hint_ladder:
  1: "Mobil cihazlarda klavyeyi e-posta düzenine geçiren girdi tipi hangisidir?"
  2: "Form gönderilirken tarayıcının geçersiz adreste uyarı balonu çıkarmasını ne sağlar?"
  3: "Bu girdi türü 'anlamsal e-posta giriş kontrolü (email input element)' olarak bilinir."
```

### html-easy-number-stepper

```yaml
id: html-easy-number-stepper
version: 1
language: html
engine: none
difficulty: easy
title: "Aralık ve adım kısıtlı sayısal giriş alanı"
prompt: |
  Bir ürün sipariş formunda ürün adedini alan bir sayı giriş kutusu oluşturun.
  Kullanıcı en az 1, en fazla 10 adet ürün seçebilmeli ve artırma/azaltma adımları
  birer birer (1) ilerlemelidir. Sayısal kısıtlar yerel HTML nitelikleriyle güvenceye alınmalıdır.
constraints:
  - "`type='number'` niteliği kullanılmalı"
  - "`min='1'`, `max='10'` ve `step='1'` kısıtlama nitelikleri eksiksiz tanımlanmalı"
concept_tags: [forms, input-validation, standards]
checklist_extra:
  - "Negatif veya sıfır girilmesini engelleyen min niteliği unutulmuş mu?"
  - "step niteliği kesirli sayılara izin verecek şekilde yanlış mı kurgulanmış?"
reference_solution_path: private/solutions/html-easy-number-stepper.html
hint_ladder:
  1: "Yalnızca sayısal girdileri kabul eden ve yukarı/aşağı oklar sunan girdi tipi nedir?"
  2: "İzin verilen en küçük ve en büyük değeri sınırlandırmak için hangi iki nitelik kullanılır?"
  3: "Bu kontrol 'kısıtlanmış sayısal girdi alanı (bounded number input)' olarak bilinir."
```

### html-easy-checkbox-agreement

```yaml
id: html-easy-checkbox-agreement
version: 1
language: html
engine: none
difficulty: easy
title: "Kullanım şartları onay kutusu"
prompt: |
  Kullanıcının kayıt olurken 'Kullanım Koşullarını okudum ve kabul ediyorum' onayını
  vermesini sağlayan bağımsız bir onay kutusu (checkbox) tasarlayın. Kullanıcı onay
  kutusunun minik karesine tıklamak zorunda kalmadan, doğrudan açıklama metnine
  tıkladığında da kutunun işaretlenebilmesini sağlayın.
constraints:
  - "`type='checkbox'` niteliği kullanılmalı"
  - "Metin tıklandığında kutunun durumunu değiştiren geçerli bir `<label>` bağı kurulmalı"
concept_tags: [forms, accessibility, standards]
checklist_extra:
  - "label etiketi input'u doğru bağlamadığı için sadece küçük kareye mi tıklanabiliyor?"
  - "Onay kutusuna formda ayırt edilebilmesi için bir name ve value atanmış mı?"
reference_solution_path: private/solutions/html-easy-checkbox-agreement.html
hint_ladder:
  1: "İkili (seçili/seçili değil) onay durumlarını temsil eden girdi tipi hangisidir?"
  2: "Kullanıcının tıklama alanını genişletmek için metin ile kutuyu hangi etiketle bağlarsın?"
  3: "Bu bileşen 'erişilebilir onay kutusu kontrolü (accessible checkbox)' olarak bilinir."
```

### html-easy-radio-group-gender

```yaml
id: html-easy-radio-group-gender
version: 1
language: html
engine: none
difficulty: easy
title: "Tekil seçimli radyo düğmesi grubu"
prompt: |
  Kullanıcıdan teslimat hızı seçeneğini (Standart, Hızlı, Aynı Gün) alan üç seçenekli
  bir radyo düğmesi grubu oluşturun. Seçenekler birbirini dışlamalıdır; yani kullanıcı
  bir seçeneğe tıkladığında diğer seçenek otomatik olarak devreden çıkmalıdır.
constraints:
  - "Tüm seçeneklerde `type='radio'` kullanılmalı"
  - "Tekil seçimi sağlamak için üç radyo düğmesinin `name` niteliği birebir aynı olmalı"
  - "Her seçeneğin kendine ait benzersiz `id` ve `for` ile bağlı `<label>` etiketi bulunmalı"
concept_tags: [forms, accessibility, standards]
checklist_extra:
  - "name nitelikleri farklı verilerek birden çok radyo düğmesinin aynı anda seçilebilmesi hatası yapılmış mı?"
  - "Sunucuya gidecek veriyi ayırt etmek için her radyo düğmesine farklı bir value atanmış mı?"
reference_solution_path: private/solutions/html-easy-radio-group-gender.html
hint_ladder:
  1: "Birden çok radyo düğmesini tek bir seçim havuzunda toplamak için hangi nitelikleri ortak olmalıdır?"
  2: "Her düğmenin formda neyi temsil ettiğini belirten value değerleri tanımlandı mı?"
  3: "Bu yapı 'birbirini dışlayan radyo grubu (mutually exclusive radio group)' olarak bilinir."
```

### html-easy-fieldset-legend

```yaml
id: html-easy-fieldset-legend
version: 1
language: html
engine: none
difficulty: easy
title: "İlişkili form alanlarını anlamsal gruplama"
prompt: |
  Bir sipariş formunda yer alan 'Fatura Adresi' ile ilgili form alanlarını (sokak, şehir,
  posta kodu) görsel ve anlamsal bir çerçeve içine alarak gruplayın. Ekran okuyucuların
  bu alanlara girildiğinde hangi grubun içinde olduğunu duyurabilmesi için grup başlığını
  standart etiketle tanımlayın.
constraints:
  - "Gruplama için `<fieldset>` etiketi kullanılmalı"
  - "Grubun başlığı fieldset'in ilk çocuğu olan `<legend>` etiketiyle verilmeli"
concept_tags: [forms, accessibility, semantics]
checklist_extra:
  - "<legend> etiketi <fieldset> dışında veya ilk sırada olmayan bir konuma mı konulmuş?"
  - "Ekran okuyucu kullanıcıları için grup bağlamı sağlandı mı?"
reference_solution_path: private/solutions/html-easy-fieldset-legend.html
hint_ladder:
  1: "İlişkili form kontrollerini bir araya toplayan anlamsal form konteyneri hangisidir?"
  2: "Bu konteynerin çerçevesi üzerinde başlık görevi gören ilk çocuk etiket nedir?"
  3: "Bu yapı 'fieldset ve legend ile form gruplaması' olarak bilinir."
```

### html-easy-select-dropdown

```yaml
id: html-easy-select-dropdown
version: 1
language: html
engine: none
difficulty: easy
title: "Açılır liste menüsü ve varsayılan devre dışı seçenek"
prompt: |
  Kullanıcının yaşadığı şehri seçebileceği bir açılır liste menüsü oluşturun. Menünün
  en başında 'Lütfen bir şehir seçin' uyarısı yer almalı; ancak bu seçenek geçerli bir
  şehir sayılmamalı, varsayılan olarak seçili gelmeli ve kullanıcının formda bu seçenekte
  kalmasını önleyecek şekilde devre dışı bırakılmış olmalıdır.
constraints:
  - "Açılır menü için `<select>` etiketi kullanılmalı"
  - "İlk seçenek `selected` ve `disabled` niteliklerine sahip olmalı, `value=''` taşımalı"
  - "En az üç gerçek şehir `<option>` etiketi eklenmeli"
concept_tags: [forms, input-validation, accessibility]
checklist_extra:
  - "İlk yer tutucu seçeneğe boş value ('') verilmediği için form gönderiminde geçerli mi sayılıyor?"
  - "<select> etiketine bağlı bir <label> var mı?"
reference_solution_path: private/solutions/html-easy-select-dropdown.html
hint_ladder:
  1: "Açılır listedeki ilk ipucu maddesinin sonradan tekrar seçilmesini nasıl engellersin?"
  2: "Bir option etiketine hem varsayılan seçili hem de pasif olma durumunu hangi iki nitelikle verirsin?"
  3: "Bu desen 'devre dışı yer tutuculu açılır liste seçimi (disabled placeholder option)' olarak bilinir."
```

### html-easy-optgroup-categorized

```yaml
id: html-easy-optgroup-categorized
version: 1
language: html
engine: none
difficulty: easy
title: "Kategorilere ayrılmış açılır liste seçenekleri"
prompt: |
  Bir otomobil markası ve model seçimi açılır menüsü hazırlayın. Seçenekler 'Sedan Modeller'
  ve 'SUV Modeller' olmak üzere iki ayrı mantıksal alt kategoriye ayrılmalı, kullanıcı
  kategori başlıklarını seçememeli ancak altındaki modelleri seçebilmelidir.
constraints:
  - "Kategori grupları için `<optgroup>` etiketi kullanılmalı"
  - "Kategori adı `label` niteliği ile belirtilmeli"
concept_tags: [forms, accessibility, semantics]
checklist_extra:
  - "Kategori başlığı olarak devre dışı <option> kullanılarak yanlış semantik mi üretilmiş?"
  - "optgroup etiketlerinin label nitelikleri ekran okuyucular için açıklayıcı mı?"
reference_solution_path: private/solutions/html-easy-optgroup-categorized.html
hint_ladder:
  1: "Açılır listedeki seçenekleri kalın başlıklı alt gruplara bölen etiket hangisidir?"
  2: "Grup başlığını optgroup üzerine hangi nitelikle yazarsın?"
  3: "Bu yapı 'kategorize edilmiş seçenek grubu (option group - optgroup)' olarak bilinir."
```

### html-easy-textarea-multiline

```yaml
id: html-easy-textarea-multiline
version: 1
language: html
engine: none
difficulty: easy
title: "Çok satırlı metin kutusu ve boyutlandırma"
prompt: |
  Kullanıcının şikayet, öneri veya detaylı mesajını yazabileceği çok satırlı bir metin
  alanı oluşturun. Alanın başlangıç fiziksel boyutunu CSS olmadan belirlemek için standart
  satır (`rows`) ve sütun (`cols`) niteliklerini tanımlayın. Etiket ile bağlantısını eksiksiz kurun.
constraints:
  - "Çok satırlı metin için `<textarea>` etiketi kullanılmalı"
  - "`rows` ve `cols` nitelikleri sayısal değerlerle belirtilmeli"
  - "Açık bir `<label>` ile bağlanmalı"
concept_tags: [forms, accessibility, standards]
checklist_extra:
  - "<textarea> etiketinin açılış ve kapanışı arasına gereksiz boşluk bırakılarak kutunun içi baştan boşlukla mı doldurulmuş?"
  - "rows ve cols nitelikleri doğru formatta mı?"
reference_solution_path: private/solutions/html-easy-textarea-multiline.html
hint_ladder:
  1: "Birden çok satır yazı girilmesine izin veren yerleşik HTML formu bileşeni nedir?"
  2: "Başlangıçta kutunun yüksekliğini satır, genişliğini karakter sütunu olarak belirleyen iki nitelik hangisidir?"
  3: "Bu bileşen 'çok satırlı metin alanı (multiline textarea)' olarak bilinir."
```

### html-easy-form-submit-reset

```yaml
id: html-easy-form-submit-reset
version: 1
language: html
engine: none
difficulty: easy
title: "Form gönderim ve temizleme butonları ayrımı"
prompt: |
  Bir formun altında yer alan iki farklı buton tanımlayın: birincisi formu sunucuya
  gönderen birincil eylem butonu (`submit`), ikincisi ise formdaki tüm alanları başlangıç
  değerlerine döndüren temizleme butonu (`reset`) olmalıdır. Butonların işlevleri açık
  tip tanımlarıyla belirtilmelidir.
constraints:
  - "Gönderim butonu `<button type='submit'>` olarak tanımlanmalı"
  - "Temizleme butonu `<button type='reset'>` olarak tanımlanmalı"
concept_tags: [forms, standards]
checklist_extra:
  - "type niteliği yazılmayarak her iki butonun da yanlışlıkla formu göndermesi hatası yapılmış mı?"
  - "Buton metinleri kullanıcıya eylemi açıkça anlatıyor mu?"
reference_solution_path: private/solutions/html-easy-form-submit-reset.html
hint_ladder:
  1: "Formu tetikleyen buton tipi ile form verilerini sıfırlayan buton tipi nedir?"
  2: "Varsayılan buton tipine güvenmek yerine türleri açıkça belirtmek neden en iyi uygulamadır?"
  3: "Bu tanımlama 'açık form eylem butonları (submit and reset button types)' olarak bilinir."
```

### html-easy-input-placeholder-accessible

```yaml
id: html-easy-input-placeholder-accessible
version: 1
language: html
engine: none
difficulty: easy
title: "Yer tutucu ve etiket ayrımı (Erişilebilirlik kuralı)"
prompt: |
  Bir arama kutusu veya kullanıcı adı alanı tasarlayın. Kullanıcıya alanın amacını
  anlatan kalıcı bir görünür etiket (`<label>`) sunun ve kutunun içine de yalnızca örnek
  formatı gösteren geçici bir yer tutucu (`placeholder`) ekleyin. Yer tutucunun kesinlikle
  etiketin yerine kullanılmaması kuralını uygulayın.
constraints:
  - "Görünür ve input'a bağlı bir `<label>` bulunmalı"
  - "`placeholder` yalnızca örnek bir girdi formatı göstermeli (örneğin 'ornek@alan.com')"
concept_tags: [forms, accessibility, standards]
checklist_extra:
  - "label etiketi tamamen atlanıp sadece placeholder mı kullanılmış (büyük erişilebilirlik hatası)?"
  - "placeholder kutuya yazı yazılmaya başlandığı anda kaybolacağı için etiketin varlığı korundu mu?"
reference_solution_path: private/solutions/html-easy-input-placeholder-accessible.html
hint_ladder:
  1: "Kullanıcı kutuya bir şey yazdığı anda kaybolan geçici ipucuna ne denir?"
  2: "Ekran okuyucuların ve yaşlı kullanıcıların ne yazdığını unutmaması için daima görünür kalması gereken etiket nedir?"
  3: "Bu kural 'etiket yerine yer tutucu kullanmama ilkesi (label vs placeholder)' olarak bilinir."
```

### html-easy-input-required-attribute

```yaml
id: html-easy-input-required-attribute
version: 1
language: html
engine: none
difficulty: easy
title: "Zorunlu alan bildirimi ve doğrulama"
prompt: |
  Kullanıcının boş bırakarak formu göndermesini engelleyen 'E-posta' ve 'Şifre' alanları
  oluşturun. Alanların doldurulması zorunlu olduğunu tarayıcının yerel doğrulama motoruna
  bildiren standart boole niteliğini ekleyin ve etiket yanında görsel olarak da belirtin.
constraints:
  - "Her iki input üzerinde `required` niteliği bulunmalı"
  - "Etiketlerde kullanıcıyı bilgilendiren bir işaret (örneğin '*') yer almalı"
concept_tags: [forms, input-validation, accessibility]
checklist_extra:
  - "required niteliği atlanarak formun boş gönderilmesine izin verilmiş mi?"
  - "Zorunlu alanlar ekran okuyuculara hem görsel hem semantik olarak aktarıldı mı?"
reference_solution_path: private/solutions/html-easy-input-required-attribute.html
hint_ladder:
  1: "Tarayıcının form gönderilirken boş bırakılan alanı işaretlemesini sağlayan HTML5 niteliği nedir?"
  2: "Tek başına yazılan bir boole nitelik olan bu özellik hangisidir?"
  3: "Bu kural 'yerel zorunlu alan doğrulaması (required attribute validation)' olarak bilinir."
```

### html-easy-basic-table-structure

```yaml
id: html-easy-basic-table-structure
version: 1
language: html
engine: none
difficulty: easy
title: "Temel tablo yapısı ve hücre hiyerarşisi"
prompt: |
  İki sütun ve iki veri satırından oluşan bir ürün fiyat tablosu hazırlayın.
  Tabloda satırları oluşturan etiketler, başlık hücreleri (`<th>`) ve standart veri
  hücreleri (`<td>`) anlamsal olarak doğru hiyerarşide yer almalıdır.
constraints:
  - "Kök eleman `<table>` olmalı"
  - "Satırlar `<tr>`, sütun başlıkları `<th>`, veriler `<td>` içinde bulunmalı"
concept_tags: [tables, semantics, standards]
checklist_extra:
  - "Sütun başlıkları için th yerine td mi kullanılmış?"
  - "tr etiketleri atlanarak hücreler doğrudan table içine mi bırakılmış?"
reference_solution_path: private/solutions/html-easy-basic-table-structure.html
hint_ladder:
  1: "Tabloda bir satır başlatmak için hangi etiket kullanılır?"
  2: "Başlık hücresi ile standart veri hücresi arasındaki etiket farkı nedir?"
  3: "Bu yapı 'standart HTML tablo iskeleti (basic table structure)' olarak bilinir."
```

### html-easy-table-header-scope

```yaml
id: html-easy-table-header-scope
version: 1
language: html
engine: none
difficulty: easy
title: "Tablo başlıklarının etki alanı kapsamı (scope)"
prompt: |
  Çalışanların isimlerini ve departmanlarını gösteren bir tablo hazırlayın.
  Ekran okuyucu bir veri hücresine geldiğinde hangi başlığa ait olduğunu karıştırmadan
  seslendirebilmesi için sütun başlıklarının sütuna (`scope="col"`), satır başlıklarının
  ise satıra (`scope="row"`) ait olduğunu açıkça belirtin.
constraints:
  - "Sütun başlığı olan `<th>` etiketlerinde `scope='col'` bulunmalı"
  - "Satır başlığı olan `<th>` etiketlerinde `scope='row'` bulunmalı"
concept_tags: [tables, accessibility, standards]
checklist_extra:
  - "scope nitelikleri boş veya geçersiz değerler mi içeriyor?"
  - "Ekran okuyucuların hücre-başlık ilişkisini kurmasını sağlayan açık kapsam tanımlandı mı?"
reference_solution_path: private/solutions/html-easy-table-header-scope.html
hint_ladder:
  1: "Bir başlık hücresinin dikey sütunu mu yoksa yatay satırı mı yönettiğini belirten nitelik nedir?"
  2: "Sütun başlıklarına scope='col', satır başlıklarına scope='row' vermek neden erişilebilirlik standardıdır?"
  3: "Bu tanımlama 'tablo başlığı kapsam bildirimi (table header scope attribute)' olarak bilinir."
```

### html-easy-table-caption-accessibility

```yaml
id: html-easy-table-caption-accessibility
version: 1
language: html
engine: none
difficulty: easy
title: "Tablo başlık özeti ve açıklaması (caption)"
prompt: |
  Bir şirketin çeyreklik gelir tablosunu oluşturun. Tablonun ne içerdiğini görme engelli
  kullanıcıların tabloya girmeden önce duyabilmesi için tablonun en başına resmi tablo
  başlığı etiketini ekleyin. Başlık dışarıda bir `<p>` veya `<h3>` olarak değil, tablonun
  kendi yerel başlık etiketi olarak verilmelidir.
constraints:
  - "Tablonun ilk çocuğu olarak `<caption>` etiketi kullanılmalı"
  - "caption metni tablonun amacını net bir şekilde açıklamalı"
concept_tags: [tables, accessibility, semantics]
checklist_extra:
  - "caption etiketi table dışında bağımsız bir başlık olarak mı yazılmış?"
  - "caption etiketi tr etiketlerinden sonraya mı bırakılmış (ilk çocuk olmalıdır)?"
reference_solution_path: private/solutions/html-easy-table-caption-accessibility.html
hint_ladder:
  1: "Bir tablonun resmi başlığını ve konusunu belirten özel tablo etiketi hangisidir?"
  2: "Bu etiket <table> etiketinin hemen ardından gelen ilk eleman mıdır?"
  3: "Bu eleman 'tablo başlık etiketi (table caption)' olarak bilinir."
```

### html-easy-table-thead-tbody-tfoot

```yaml
id: html-easy-table-thead-tbody-tfoot
version: 1
language: html
engine: none
difficulty: easy
title: "Tablo anlamsal bölümleri (Başlık, Gövde, Alt Toplam)"
prompt: |
  Alışveriş faturasını gösteren bir veri tablosu hazırlayın. Tabloyu anlamsal olarak
  üç ana bölüme ayırın: Sütun isimlerinin yer aldığı başlık bölümü, ürün satırlarının
  yer aldığı gövde bölümü ve en altta genel toplamın hesaplandığı alt toplam bölümü.
constraints:
  - "Başlık satırları `<thead>` içinde yer almalı"
  - "Veri satırları `<tbody>` içinde yer almalı"
  - "Toplam satırı `<tfoot>` içinde yer almalı"
concept_tags: [tables, semantics, standards]
checklist_extra:
  - "Tablo bölümlendirmesi yapılmadan tüm tr etiketleri doğrudan table altına mı serilmiş?"
  - "Yazıcıdan çıktı alınırken sayfa bölünmesinde başlığın tekrarlanmasını sağlayan thead kullanıldı mı?"
reference_solution_path: private/solutions/html-easy-table-thead-tbody-tfoot.html
hint_ladder:
  1: "Tablonun başlık, ana içerik ve dipnot bölümlerini ayıran üç semantik etiket hangileridir?"
  2: "Genel toplam satırı hangi özel bölümün içine yerleştirilmelidir?"
  3: "Bu yapı 'anlamsal tablo bölümlendirmesi (thead, tbody, tfoot)' olarak bilinir."
```

### html-easy-nav-landmark

```yaml
id: html-easy-nav-landmark
version: 1
language: html
engine: none
difficulty: easy
title: "Ana dolaşım menüsü işaret noktası (nav landmark)"
prompt: |
  Bir web sitesinin ana sayfasına yönlendiren, sitenin 'Hakkımızda', 'Hizmetler' ve
  'İletişim' sayfalarına giden bağlantılarını içeren ana navigasyon bloğunu oluşturun.
  Ekran okuyucu kullanıcılarının doğrudan menüye atlayabilmesi için genel bir `<div>`
  yerine anlamsal dolaşım etiketi kullanılmalıdır.
constraints:
  - "Dolaşım alanı `<nav>` etiketi ile sarmalanmalı"
  - "Bağlantılar liste (`<ul>` ve `<li>`) yapısı içinde anlamsal olarak sunulmalı"
concept_tags: [navigation, accessibility, semantics]
checklist_extra:
  - "Dolaşım menüsü için div class='nav' kullanılarak anlamsal landmark haritası kaçırılmış mı?"
  - "Menü bağlantıları liste yapısı yerine rastgele a etiketleri olarak mı bırakılmış?"
reference_solution_path: private/solutions/html-easy-nav-landmark.html
hint_ladder:
  1: "Ekran okuyucuların 'navigasyon alanı' olarak tanıdığı HTML5 işaret noktası etiketi nedir?"
  2: "Menü bağlantılarını erişilebilir kılmak için bunları bir sırasız liste içinde nasıl düzenlersin?"
  3: "Bu alan 'anlamsal dolaşım işaret noktası (navigation landmark)' olarak bilinir."
```

### html-easy-main-content-landmark

```yaml
id: html-easy-main-content-landmark
version: 1
language: html
engine: none
difficulty: easy
title: "Sayfanın birincil içerik alanı (main landmark)"
prompt: |
  Bir web sayfasında üst bilgi, alt bilgi ve yan menüler dışında kalan, yalnızca o
  sayfaya özgü ana içeriğin yer aldığı birincil bölümü oluşturun. Bir HTML dokümanında
  yalnızca bir adet bulunması gereken anlamsal ana içerik etiketini kullanın.
constraints:
  - "Ana içerik için `<main>` etiketi kullanılmalı"
  - "Sayfada birden fazla görünür `<main>` etiketi bulunmamalı"
concept_tags: [semantics, accessibility, standards]
checklist_extra:
  - "Ana içerik için div class='content' mi kullanılmış?"
  - "<main> etiketi header veya footer etiketlerinin içine yanlışlıkla gömülmüş mü?"
reference_solution_path: private/solutions/html-easy-main-content-landmark.html
hint_ladder:
  1: "Ekran okuyucu kullanıcısının menüleri atlayıp doğrudan sayfanın asıl konusuna gitmesini sağlayan etiket hangisidir?"
  2: "Bir HTML belgesinde bu etiketten en fazla kaç tane bulunabilir?"
  3: "Bu işaret noktası 'birincil içerik alanı (main landmark)' olarak bilinir."
```

### html-easy-header-banner

```yaml
id: html-easy-header-banner
version: 1
language: html
engine: none
difficulty: easy
title: "Sayfa üst bilgisi ve logo alanı (header banner)"
prompt: |
  Bir web sitesinin en üstünde yer alan, site logosunu, ana başlığını ve giriş butonunu
  barındıran tanıtıcı üst bilgi alanını oluşturun. Jenerik bir kutu yerine anlamsal üst
  bilgi etiketini tercih edin.
constraints:
  - "Üst bilgi alanı `<header>` etiketi ile tanımlanmalı"
  - "İçerisinde bir logo veya başlık barındırmalı"
concept_tags: [semantics, accessibility]
checklist_extra:
  - "div class='header' kullanılarak anlamsal banner rolü atlanmış mı?"
  - "<header> etiketinin <head> etiketiyle karıştırılması hatası yapılmış mı?"
reference_solution_path: private/solutions/html-easy-header-banner.html
hint_ladder:
  1: "Sayfanın veya bir makalenin tanıtıcı üst bloğunu temsil eden etiket nedir?"
  2: "<head> (meta veriler) ile <header> (görünür üst bilgi) arasındaki farkı biliyor musun?"
  3: "Bu alan 'anlamsal üst bilgi alanı (header landmark)' olarak bilinir."
```

### html-easy-footer-contentinfo

```yaml
id: html-easy-footer-contentinfo
version: 1
language: html
engine: none
difficulty: easy
title: "Sayfa alt bilgisi (footer contentinfo)"
prompt: |
  Bir web sayfasının en altında yer alan telif hakkı bildirimini, gizlilik sözleşmesi
  bağlantısını ve yazar bilgisini içeren alt bilgi alanını oluşturun.
constraints:
  - "Alt bilgi alanı anlamsal `<footer>` etiketi ile sarmalanmalı"
  - "İçerisinde telif metni ve en az bir yasal bağlantı yer almalı"
concept_tags: [semantics, accessibility]
checklist_extra:
  - "div class='footer' kullanılarak semantik alt bilgi yapısı göz ardı edilmiş mi?"
  - "<footer> etiketinin sayfa sonu haricinde makale sonlarında da kullanılabileceği biliniyor mu?"
reference_solution_path: private/solutions/html-easy-footer-contentinfo.html
hint_ladder:
  1: "Telif hakkı, yasal bağlantılar ve site haritasını toplayan sayfa altı etiketi hangisidir?"
  2: "Ekran okuyucuların 'contentinfo' olarak tanıdığı standart etiket nedir?"
  3: "Bu bölüm 'anlamsal alt bilgi alanı (footer landmark)' olarak bilinir."
```

### html-easy-article-independent

```yaml
id: html-easy-article-independent
version: 1
language: html
engine: none
difficulty: easy
title: "Bağımsız ve taşınabilir makale bloğu"
prompt: |
  Bir blog gönderisini veya haber bültenini temsil eden bir içerik bloğu oluşturun.
  Bu blok siteden tamamen koparılıp başka bir RSS okuyucuda veya sitede tek başına
  yayımlandığında da kendi içinde bütünlüğü olan bağımsız bir makale etiketiyle tanımlanmalıdır.
constraints:
  - "Bağımsız içerik için `<article>` etiketi kullanılmalı"
  - "İçerisinde kendi başlığını (`<h2>` vb.) ve yayımlanma tarihini barındırmalı"
concept_tags: [semantics, standards]
checklist_extra:
  - "Yalnızca görsel bölme amacıyla section yerine bağımsız içerik için article doğru seçildi mi?"
  - "article bloğunun kendine ait bir başlığı var mı?"
reference_solution_path: private/solutions/html-easy-article-independent.html
hint_ladder:
  1: "Kendi başına anlam ifade eden bir blog yazısı, forum mesajı veya haber kartı hangi etiketle sarmalanır?"
  2: "RSS beslemelerine doğrudan beslenebilecek bağımsız yapıyı hangi etiket temsil eder?"
  3: "Bu yapı 'anlamsal bağımsız makale bloğu (article element)' olarak bilinir."
```

### html-easy-aside-complementary

```yaml
id: html-easy-aside-complementary
version: 1
language: html
engine: none
difficulty: easy
title: "Tamamlayıcı yan bilgi ve kenar çubuğu (aside)"
prompt: |
  Bir makalenin yanında yer alan 'Yazarın Diğer Yazıları', 'İlgili Bağlantılar' veya bir
  terim sözlüğü gibi ana içerikle dolaylı yoldan ilişkili ancak çıkarıldığında ana metnin
  anlamını bozmayan tamamlayıcı yan içerik alanını oluşturun.
constraints:
  - "Tamamlayıcı içerik için `<aside>` etiketi kullanılmalı"
  - "İçerisinde ilgili yan bağlantılar veya ek bilgi yer almalı"
concept_tags: [semantics, accessibility]
checklist_extra:
  - "Ana içerik yanlışlıkla aside içine mi alınmış?"
  - "div class='sidebar' yerine anlamsal aside etiketi tercih edilmiş mi?"
reference_solution_path: private/solutions/html-easy-aside-complementary.html
hint_ladder:
  1: "Ana akıştan ayrı duran yan paneller, reklamlar veya dipnotlar için hangi etiket kullanılır?"
  2: "Ekran okuyucuların 'tamamlayıcı içerik (complementary landmark)' olarak gördüğü etiket nedir?"
  3: "Bu bölüm 'anlamsal yan içerik alanı (aside element)' olarak bilinir."
```

### html-easy-section-generic-themed

```yaml
id: html-easy-section-generic-themed
version: 1
language: html
engine: none
difficulty: easy
title: "Tematik konu bölümlemesi ve başlık bağı"
prompt: |
  Tek sayfalık bir tanıtım sitesinde 'Özelliklerimiz' konusunu ele alan tematik bir bölüm
  oluşturun. Bölüm sadece stil vermek için değil, bir konu bütünlüğü taşıdığı için
  anlamsal bölüm etiketiyle kurulmalı ve mutlaka kendine ait bir bölüm başlığı içermelidir.
constraints:
  - "Tematik bölüm için `<section>` etiketi kullanılmalı"
  - "Her section içinde doğrudan ilişkili bir başlık etiketi (`<h2>` veya `<h3>`) yer almalı"
concept_tags: [semantics, accessibility, standards]
checklist_extra:
  - "<section> etiketi başlık olmadan yalnızca görsel sarmalayıcı (div gibi) mi kullanılmış?"
  - "Belge anahat (document outline) hiyerarşisi doğru kuruldu mu?"
reference_solution_path: private/solutions/html-easy-section-generic-themed.html
hint_ladder:
  1: "Bir dokümanın belirli bir temaya sahip alt bölümlerini işaretleyen etiket hangisidir?"
  2: "W3C standartlarına göre bir section elemanının içinde mutlaka ne bulunmalıdır?"
  3: "Bu yapı 'başlıklı tematik bölüm (themed section)' olarak bilinir."
```

### html-easy-details-summary-disclosure

```yaml
id: html-easy-details-summary-disclosure
version: 1
language: html
engine: none
difficulty: easy
title: "Tıklanıp açılan yerel akordeon bileşeni"
prompt: |
  Bir Sıkça Sorulan Sorular (SSS) maddesi oluşturun. JavaScript yazmadan, kullanıcının
  soru başlığına tıkladığında cevabın aşağıya doğru açılmasını ve tekrar tıklandığında
  kapanmasını sağlayan yerleşik HTML5 açılır-kapanır bilgi bileşenini kullanın.
constraints:
  - "Kök eleman olarak `<details>` etiketi kullanılmalı"
  - "Görünür soru başlığı `<summary>` etiketi içine alınmalı"
  - "Açılan içerik summary'nin ardından tanımlanmalı"
concept_tags: [dialogs, accessibility, semantics]
checklist_extra:
  - "<summary> etiketi <details> dışına mı konulmuş?"
  - "JS gerektirmeyen bu yerel HTML bileşeni klavye ile Enter/Boşluk ile açılabiliyor mu?"
reference_solution_path: private/solutions/html-easy-details-summary-disclosure.html
hint_ladder:
  1: "Tarayıcının yerel olarak açılır-kapanır panel oluşturmasını sağlayan etiket ikilisi hangisidir?"
  2: "Tıklanacak başlığı hangi çocuk etiket içine yazarsın?"
  3: "Bu bileşen 'yerel detay ve özet akordeonu (details and summary disclosure widget)' olarak bilinir."
```

### html-easy-search-input-clearable

```yaml
id: html-easy-search-input-clearable
version: 1
language: html
engine: none
difficulty: easy
title: "Arama giriş alanı ve temizleme kolaylığı"
prompt: |
  Web sitesinde arama yapmak için kullanılan bir arama kutusu tasarlayın. Standart metin
  kutusu yerine, arama yapıldığını anlamsal olarak bildiren ve bazı tarayıcılarda içine
  otomatik 'temizle (X)' butonu getiren arama girdi tipini kullanın.
constraints:
  - "`<input>` üzerinde `type='search'` niteliği kullanılmalı"
  - "Erişilebilir bir etiket veya arama butonuyla ilişkilendirilmeli"
concept_tags: [forms, input-validation, accessibility]
checklist_extra:
  - "type='search' yerine jenerik type='text' mi kullanılmış?"
  - "Arama kutusu için form rolü veya etiket tanımı eksiksiz mi?"
reference_solution_path: private/solutions/html-easy-search-input-clearable.html
hint_ladder:
  1: "Arama kutuları için optimize edilmiş özel HTML5 girdi tipi nedir?"
  2: "Mobil cihazlarda klavyede 'Git' yerine 'Ara' butonu çıkmasını ne sağlar?"
  3: "Bu girdi türü 'arama girdi alanı (search input)' olarak bilinir."
```

### html-easy-tel-input-pattern

```yaml
id: html-easy-tel-input-pattern
version: 1
language: html
engine: none
difficulty: easy
title: "Telefon giriş alanı ve sayısal tuş takımı"
prompt: |
  Mobil cihazlarda tıklandığında yalnızca telefon numarası çevirme klavyesini açan bir
  telefon girdi alanı oluşturun. Belirli bir formatı (örneğin 0555-555-55-55) zorunlu kılmak
  için standart düzenli ifade (`pattern`) niteliğini ekleyin.
constraints:
  - "`type='tel'` niteliği kullanılmalı"
  - "Doğrulama için geçerli bir `pattern` regex niteliği tanımlanmalı"
concept_tags: [forms, input-validation, performance]
checklist_extra:
  - "type='text' kullanılarak mobil sayısal klavye avantajı kaçırılmış mı?"
  - "Kullanıcıya beklenen telefon formatını anlatan bir ipucu veya etiket sunuldu mu?"
reference_solution_path: private/solutions/html-easy-tel-input-pattern.html
hint_ladder:
  1: "Mobil cihazlarda doğrudan telefon tuş takımını çağıran girdi türü hangisidir?"
  2: "Girdinin belirli bir biçime uymasını zorunlu kılan regex deseni niteliği nedir?"
  3: "Bu kontrol 'desen kısıtlı telefon giriş alanı (telephone input with pattern)' olarak bilinir."
```

### html-easy-url-input-validation

```yaml
id: html-easy-url-input-validation
version: 1
language: html
engine: none
difficulty: easy
title: "Web sitesi adresi giriş alanı ve protokol denetimi"
prompt: |
  Kullanıcının portfolyo veya şirket web sitesi adresini girmesini isteyen bir form alanı
  oluşturun. Tarayıcının girilen metnin geçerli bir web adresi ('http://' veya 'https://')
  olup olmadığını form gönderilmeden önce otomatik denetlemesini sağlayın.
constraints:
  - "`<input>` üzerinde `type='url'` niteliği kullanılmalı"
  - "Açıkça bağlı bir `<label>` etiketi bulunmalı"
concept_tags: [forms, input-validation, accessibility]
checklist_extra:
  - "Standart metin alanı kullanılarak protokol kontrolü atlanmış mı?"
  - "Mobil cihazlarda '.' ve '/' tuşlarını öne çıkaran klavye düzeni sağlandı mı?"
reference_solution_path: private/solutions/html-easy-url-input-validation.html
hint_ladder:
  1: "Web adresi girişleri için tasarlanmış ve URL doğrulaması yapan girdi türü nedir?"
  2: "Kullanıcı protokol yazmadığında tarayıcının uyarı vermesini sağlayan type değeri hangisidir?"
  3: "Bu girdi tipi 'URL doğrulama giriş alanı (url input)' olarak bilinir."
```

### html-easy-date-picker-input

```yaml
id: html-easy-date-picker-input
version: 1
language: html
engine: none
difficulty: easy
title: "Yerel takvim tarih seçici alanı"
prompt: |
  Harici bir JavaScript takvim kütüphanesi kullanmadan, kullanıcının doğum tarihini
  seçebileceği tarayıcının kendi yerleşik takvim açılır penceresini getiren bir tarih
  giriş alanı oluşturun.
constraints:
  - "`<input>` üzerinde `type='date'` niteliği kullanılmalı"
  - "Erişilebilir bir etiket ile bağlanmalı"
concept_tags: [forms, input-validation, standards]
checklist_extra:
  - "Tarih için düz metin kutusu kullanılıp kullanıcı GG/AA/YYYY yazmaya mı zorlanmış?"
  - "Tarayıcının yerel tarih seçicisini açan type='date' doğru tanımlandı mı?"
reference_solution_path: private/solutions/html-easy-date-picker-input.html
hint_ladder:
  1: "Tarayıcının takvim arayüzünü doğrudan çağıran HTML5 form girdi türü nedir?"
  2: "Sunucuya YYYY-MM-DD formatında standart veri göndermeyi ne sağlar?"
  3: "Bu kontrol 'yerel tarih seçici (native date picker)' olarak bilinir."
```

### html-easy-color-picker-input

```yaml
id: html-easy-color-picker-input
version: 1
language: html
engine: none
difficulty: easy
title: "Görsel renk seçici (Color Picker)"
prompt: |
  Kullanıcının bir tema rengi seçebileceği yerleşik renk paletini açan bir renk seçici
  alanı oluşturun. Varsayılan başlangıç rengi olarak siyah dışında bir renk
  (örneğin mavi '#0000ff') tanımlayın.
constraints:
  - "`<input>` üzerinde `type='color'` niteliği bulunmalı"
  - "Başlangıç rengi `value='#rrggbb'` biçiminde onaltılık (hex) kodla belirtilmeli"
concept_tags: [forms, standards]
checklist_extra:
  - "value değeri hex formatı dışında (örneğin 'blue' veya 'rgb()') yazılarak geçersiz kılınmış mı?"
  - "Renk seçiciye bağlı bir label etiketi mevcut mu?"
reference_solution_path: private/solutions/html-easy-color-picker-input.html
hint_ladder:
  1: "Tarayıcının renk seçme penceresini ekrana getiren form girdi türü hangisidir?"
  2: "Varsayılan rengi belirlerken value niteliğine 7 karakterli hex kodu (#RRGGBB) nasıl verilir?"
  3: "Bu bileşen 'renk seçici kontrolü (color picker input)' olarak bilinir."
```

### html-easy-range-slider-input

```yaml
id: html-easy-range-slider-input
version: 1
language: html
engine: none
difficulty: easy
title: "Sayısal kaydırıcı çubuğu (Range Slider)"
prompt: |
  Kullanıcının ses seviyesini veya ekran parlaklığını 0 ile 100 arasında hassas olmayan
  bir şekilde kaydırarak seçebileceği bir kaydırıcı kontrolü (slider) oluşturun.
  Minimum, maksimum ve başlangıç değerleri belirtilmelidir.
constraints:
  - "`<input>` üzerinde `type='range'` niteliği kullanılmalı"
  - "`min`, `max` ve başlangıç `value` nitelikleri tanımlanmalı"
concept_tags: [forms, standards, accessibility]
checklist_extra:
  - "Kaydırıcının neyi kontrol ettiğini belirten bir label etiketi eklendi mi?"
  - "min ve max değerleri arasındaki farka uygun step tanımlandı mı?"
reference_solution_path: private/solutions/html-easy-range-slider-input.html
hint_ladder:
  1: "Kesin sayı girmek yerine yatay bir çubuk üzerinde kaydırma yaparak değer seçtiren girdi tipi nedir?"
  2: "Aralık sınırlarını belirlemek için hangi iki niteliği kullanırsın?"
  3: "Bu kontrol 'kaydırıcı aralık çubuğu (range slider input)' olarak bilinir."
```

### html-easy-file-upload-accept

```yaml
id: html-easy-file-upload-accept
version: 1
language: html
engine: none
difficulty: easy
title: "Dosya yükleme ve izin verilen uzantı filtresi"
prompt: |
  Kullanıcının yalnızca özgeçmiş PDF veya Word belgesi yüklemesine izin veren bir dosya
  yükleme alanı oluşturun. Kullanıcı dosya seçiciyi açtığında diğer dosya türlerinin
  otomatik olarak gizlenmesi için dosya türü filtresi tanımlayın.
constraints:
  - "`<input>` üzerinde `type='file'` niteliği bulunmalı"
  - "`accept` niteliğinde izin verilen uzantılar (örneğin '.pdf,.docx') belirtilmeli"
concept_tags: [forms, input-validation, security]
checklist_extra:
  - "accept niteliği atlanarak kullanıcının her türlü dosyayı seçebilmesine mi izin verilmiş?"
  - "Dosya yükleme alanının bağlı bir label etiketi var mı?"
reference_solution_path: private/solutions/html-easy-file-upload-accept.html
hint_ladder:
  1: "Kullanıcının bilgisayarından dosya seçmesini sağlayan girdi tipi nedir?"
  2: "Dosya seçici penceresinde sadece belirli uzantıları filtreleyen nitelik hangisidir?"
  3: "Bu form elemanı 'filtrelenmiş dosya yükleme kontrolü (file input with accept)' olarak bilinir."
```

### html-easy-hidden-input-token

```yaml
id: html-easy-hidden-input-token
version: 1
language: html
engine: none
difficulty: easy
title: "Görünmeyen form verisi ve güvenlik jetonu alanı"
prompt: |
  Kullanıcıya ekranda görüntülenmeyen, ancak form gönderildiğinde sunucuya oturum kimliği,
  güvenlik jetonu (CSRF token) veya ürün ID'si taşıyan gizli bir form alanı ekleyin.
constraints:
  - "`<input>` üzerinde `type='hidden'` niteliği kullanılmalı"
  - "Geçerli bir `name` ve `value` çifti içermeli"
concept_tags: [forms, security]
checklist_extra:
  - "Gizli alan için CSS 'display: none' verilmiş text alanı mı kullanılmış?"
  - "Ekranda görünmeyen bu alana gereksiz label etiketi verilerek ekran okuyucu karmaşası yaratılmış mı?"
reference_solution_path: private/solutions/html-easy-hidden-input-token.html
hint_ladder:
  1: "Kullanıcıya gösterilmeden form verisine gizlice eklenen yerel girdi tipi hangisidir?"
  2: "Güvenlik jetonlarını veya kayıt kimliklerini göndermek için ne kullanılır?"
  3: "Bu form elemanı 'gizli veri alanı (hidden input)' olarak bilinir."
```

### html-easy-datalist-autocomplete

```yaml
id: html-easy-datalist-autocomplete
version: 1
language: html
engine: none
difficulty: easy
title: "Metin kutusuna öneri listesi bağlama (Datalist)"
prompt: |
  Kullanıcının serbestçe istediği metni yazabileceği, ancak yazmaya başladığında
  altında popüler web tarayıcılarını öneri olarak listeleyen bir otomatik tamamlama
  yapısı oluşturun. Kullanıcı önerilerden birini seçebileceği gibi listede olmayan
  farklı bir şey de yazabilmelidir.
constraints:
  - "`<input>` üzerindeki `list` niteliği ile `<datalist>` etiketinin `id` niteliği eşleşmeli"
  - "datalist içinde `<option>` etiketleriyle öneriler sunulmalı"
concept_tags: [forms, input-validation, standards]
checklist_extra:
  - "Kullanıcıyı yalnızca listedekilere zorlayan standart select etiketiyle karıştırılmış mı?"
  - "input'un list niteliği ile datalist'in id değeri tam eşleşiyor mu?"
reference_solution_path: private/solutions/html-easy-datalist-autocomplete.html
hint_ladder:
  1: "Bir metin kutusuna açılır öneri listesi bağlayan HTML5 etiketi hangisidir?"
  2: "Metin kutusuna bu listeyi bağlamak için hangi nitelik kullanılır?"
  3: "Bu yapı 'veri listesi ile otomatik tamamlama (datalist autocomplete)' olarak bilinir."
```

### html-easy-output-calculation

```yaml
id: html-easy-output-calculation
version: 1
language: html
engine: none
difficulty: easy
title: "Form hesaplama sonucu alanı"
prompt: |
  İki sayının veya bir kaydırıcı ile bir sayının toplamını anlık olarak gösteren bir form
  tasarlayın. Matematiksel hesaplama sonucunun yazıldığı alanı, ekran okuyuculara buranın
  bir hesaplama çıktısı olduğunu belirten anlamsal sonuç etiketiyle işaretleyin.
constraints:
  - "Hesaplama sonucu için `<output>` etiketi kullanılmalı"
  - "`for` niteliği ile hesaplamaya katılan girdi elemanlarının id değerleri ilişkilendirilmeli"
concept_tags: [forms, semantics, accessibility]
checklist_extra:
  - "Çıktı alanı için anlamsız span veya p mi kullanılmış?"
  - "output etiketinin for niteliğinde girdilerin id'leri boşlukla ayrılarak listelenmiş mi?"
reference_solution_path: private/solutions/html-easy-output-calculation.html
hint_ladder:
  1: "Form üzerindeki hesaplamaların veya kullanıcı etkileşimi sonucunun yazıldığı HTML etiketi nedir?"
  2: "Bu sonucun hangi girdilerden beslendiğini for niteliğiyle nasıl belirtirsin?"
  3: "Bu eleman 'form hesaplama sonucu etiketi (output element)' olarak bilinir."
```

### html-easy-table-colspan-cell

```yaml
id: html-easy-table-colspan-cell
version: 1
language: html
engine: none
difficulty: easy
title: "Sütun birleştiren tablo hücresi (colspan)"
prompt: |
  3 sütunlu bir bütçe tablosunun en altında yer alan ve tablonun 3 sütununu birden
  kaplayarak tek parça halinde 'Toplam Harcama: 15.000 TL' yazan bir alt toplam satırı
  oluşturun. Sütunların birleştirildiğini belirten standart tablo niteliğini kullanın.
constraints:
  - "Hücre üzerinde `colspan='3'` niteliği kullanılmalı"
  - "Tablonun diğer satırlarındaki sütun sayısıyla matematiksel denge sağlanmalı"
concept_tags: [tables, standards]
checklist_extra:
  - "colspan değeri diğer satırlardaki toplam sütun sayısıyla uyuşmayıp tablo düzenini bozmuş mu?"
  - "Birleştirilen hücre doğru th veya td etiketinde mi?"
reference_solution_path: private/solutions/html-easy-table-colspan-cell.html
hint_ladder:
  1: "Bir hücrenin yatayda birden fazla sütun boyunca uzamasını sağlayan nitelik hangisidir?"
  2: "3 sütunu tek hücrede birleştirmek için ne yazarsın?"
  3: "Bu işlem 'sütun birleştirme niteliği (colspan attribute)' olarak bilinir."
```

### html-easy-table-rowspan-cell

```yaml
id: html-easy-table-rowspan-cell
version: 1
language: html
engine: none
difficulty: easy
title: "Satır birleştiren tablo hücresi (rowspan)"
prompt: |
  Bir ders programı tablosunda, iki ders saati boyunca süren bir dersi temsil etmek için
  dikeyde iki satırı birden kaplayan tek bir ders hücresi oluşturun. Sonraki satırda
  birleşen bu sütunun hücresi atlanarak satır dengesi korunmalıdır.
constraints:
  - "Dikey birleştirme için `rowspan='2'` niteliği kullanılmalı"
  - "İkinci satırda birleştirilen hücrenin yeri boş bırakılarak sütun kayması engellenmeli"
concept_tags: [tables, standards]
checklist_extra:
  - "İkinci satırda fazladan bir td bırakılarak tablonun sağa doğru taşmasına yol açılmış mı?"
  - "rowspan doğru başlangıç satırındaki hücreye mi verilmiş?"
reference_solution_path: private/solutions/html-easy-table-rowspan-cell.html
hint_ladder:
  1: "Bir hücrenin dikeyde birden fazla satır boyunca uzamasını sağlayan nitelik nedir?"
  2: "Alt satıra geçtiğinde o sütunun hücresini tekrar yazmaman gerektiğini hatırladın mı?"
  3: "Bu işlem 'satır birleştirme niteliği (rowspan attribute)' olarak bilinir."
```

### html-easy-video-poster-image

```yaml
id: html-easy-video-poster-image
version: 1
language: html
engine: none
difficulty: easy
title: "Video yüklenene kadar gösterilecek kapak görseli"
prompt: |
  Bir web videosu tanımlayın. Video kullanıcı tarafından oynatılana kadar veya video
  verisi indirilirken siyah boş bir ekran görünmesini önlemek için videonun ilk karesini
  veya özel bir afiş görselini kapak resmi olarak gösterin.
constraints:
  - "`<video>` etiketi üzerinde `poster` niteliği bulunmalı"
  - "poster niteliği geçerli bir resim dosyasını göstermeli"
concept_tags: [standards, performance, images]
checklist_extra:
  - "poster niteliği unutularak video açılışında boş gri/siyah kutu mu bırakılmış?"
  - "Video kontrolleri (controls) ve kapak resmi birlikte tanımlı mı?"
reference_solution_path: private/solutions/html-easy-video-poster-image.html
hint_ladder:
  1: "Video başlamadan önce ekranda afiş gibi duran kapak resmini hangi nitelik tanımlar?"
  2: "Kullanıcı tıklayana kadar gösterilecek görselin yolunu nereye yazarsın?"
  3: "Bu tanımlama 'video kapak görseli niteliği (video poster attribute)' olarak bilinir."
```

### html-easy-video-subtitles-track

```yaml
id: html-easy-video-subtitles-track
version: 1
language: html
engine: none
difficulty: easy
title: "Video altyazı ve işitme engelli metin desteği"
prompt: |
  Bir video oynatıcıya işitme engelli kullanıcılar veya sessiz ortamda izleyenler için
  Türkçe altyazı dosyası (WebVTT formatında) bağlayın. Altyazının türü, dili ve etiketi
  standart altyazı izi etiketiyle belirtilmelidir.
constraints:
  - "`<video>` içinde `<track>` etiketi kullanılmalı"
  - "`kind='subtitles'`, `srclang='tr'` ve `label='Türkçe'` nitelikleri eksiksiz bulunmalı"
concept_tags: [accessibility, standards]
checklist_extra:
  - "kind niteliği atlanarak altyazının işlevi tanımsız mı bırakılmış?"
  - "srclang niteliğinde geçerli dil kodu ('tr') belirtilmiş mi?"
reference_solution_path: private/solutions/html-easy-video-subtitles-track.html
hint_ladder:
  1: "Videolara altyazı veya sesli betimleme eklemek için hangi çocuk etiket kullanılır?"
  2: "Altyazı dosyasının türünü 'subtitles' ve dilini 'tr' olarak hangi niteliklerle belirtirsin?"
  3: "Bu erişilebilirlik alanı 'video altyazı izi (timed text track)' olarak bilinir."
```

### html-easy-picture-responsive-formats

```yaml
id: html-easy-picture-responsive-formats
version: 1
language: html
engine: none
difficulty: easy
title: "Modern görsel formatları için aşamalı geri dönüş (picture)"
prompt: |
  Modern tarayıcılar için yeni nesil hafif WebP görsel formatını sunan, ancak WebP
  desteklemeyen eski tarayıcılar için standart JPEG formatına güvenle geri dönen
  duyarlı görsel bileşeni oluşturun.
constraints:
  - "Kök eleman olarak `<picture>` etiketi kullanılmalı"
  - "WebP formatı için `<source type='image/webp'>` bulunmalı"
  - "Geri dönüş (fallback) için standart bir `<img>` etiketi yer almalı"
concept_tags: [images, performance, standards]
checklist_extra:
  - "picture içinde img etiketi unutularak eski tarayıcıların hiçbir şey gösterememesi hatası yapılmış mı?"
  - "Görselin alt niteliği <picture> yerine içindeki <img> etiketine mi yazılmış?"
reference_solution_path: private/solutions/html-easy-picture-responsive-formats.html
hint_ladder:
  1: "Farklı görsel formatlarını veya çözünürlüklerini sırayla sunan konteyner etiket hangisidir?"
  2: "Tarayıcı WebP'yi desteklemiyorsa en alttaki standart img etiketine düşmesini nasıl sağlarsın?"
  3: "Bu teknik 'picture etiketi ile format bazlı aşamalı iyileştirme (format fallback)' olarak bilinir."
```

### html-easy-dialog-native-modal

```yaml
id: html-easy-dialog-native-modal
version: 1
language: html
engine: none
difficulty: easy
title: "Yerel diyalog penceresi (dialog elementi)"
prompt: |
  Bir web uygulamasında kullanıcıya onay sorusu soran (örneğin 'Hesabınızı silmek istediğinize
  emin misiniz?') yerleşik bir diyalog penceresi oluşturun. Sayfa açılışında doğrudan görünür
  olması için standart açık (`open`) niteliğini ekleyin ve içinde bir kapatma butonu barındırın.
constraints:
  - "Yerel modal için anlamsal `<dialog>` etiketi kullanılmalı"
  - "Açık durumda görüntülenmesi için `open` boole niteliği bulunmalı"
concept_tags: [dialogs, accessibility, standards]
checklist_extra:
  - "Modal pencere için div class='modal' yerine anlamsal <dialog> etiketi tercih edildi mi?"
  - "İçerisinde bir onay ve bir iptal butonu yer alıyor mu?"
reference_solution_path: private/solutions/html-easy-dialog-native-modal.html
hint_ladder:
  1: "HTML5'te tarayıcının yerel açılır pencere/diyalog kutusu etiketi nedir?"
  2: "Diyalog penceresinin varsayılan olarak açık durması için hangi niteliği eklersin?"
  3: "Bu bileşen 'yerel diyalog penceresi (native dialog element)' olarak bilinir."
```

### html-easy-form-action-method-post

```yaml
id: html-easy-form-action-method-post
version: 1
language: html
engine: none
difficulty: easy
title: "Güvenli form gönderim metodu ve hedef uç nokta"
prompt: |
  Kullanıcı şifresi veya kredi kartı gibi hassas verilerin URL çubuğunda açıkça
  görünmesini engellemek için verileri istek gövdesinde (HTTP body) gönderen ve
  '/api/giris' adresine yönlendiren güvenli bir form tanımlayın.
constraints:
  - "`<form>` üzerinde `method='post'` niteliği kullanılmalı"
  - "`action='/api/giris'` hedef adresi tanımlanmalı"
concept_tags: [forms, security, standards]
checklist_extra:
  - "Hassas form için varsayılan ve güvensiz olan 'get' metodu mu bırakılmış?"
  - "action niteliği eksik mi?"
reference_solution_path: private/solutions/html-easy-form-action-method-post.html
hint_ladder:
  1: "Form verilerini URL yerine HTTP istek gövdesinde taşımak için hangi metot kullanılır?"
  2: "Formun verileri göndereceği sunucu adresini belirten nitelik hangisidir?"
  3: "Bu tanımlama 'POST metodu ile güvenli form gönderimi' olarak bilinir."
```

### html-easy-button-formaction-override

```yaml
id: html-easy-button-formaction-override
version: 1
language: html
engine: none
difficulty: easy
title: "Buton düzeyinde form gönderim hedefini ezme"
prompt: |
  Varsayılan olarak 'action="/taslak-kaydet"' adresine gönderilen bir formun içine,
  tıklandığında formu ana action adresi yerine 'action="/yayinla"' adresine yönlendiren
  özel bir 'Yayımla' butonu ekleyin.
constraints:
  - "`<button>` üzerinde `formaction='/yayinla'` niteliği kullanılmalı"
  - "Buton tipi `submit` olmalı"
concept_tags: [forms, standards]
checklist_extra:
  - "formaction niteliği yerine JavaScript ile form adresi mi değiştirilmeye çalışılmış?"
  - "Formun ana action adresi ile butonun özel formaction adresi doğru ayrıştı mı?"
reference_solution_path: private/solutions/html-easy-button-formaction-override.html
hint_ladder:
  1: "Bir submit butonunun tıklandığında formun genel action adresini ezmesini sağlayan HTML5 niteliği nedir?"
  2: "Aynı form içinde farklı iki sunucu hedefine gönderme butonları nasıl yapılır?"
  3: "Bu nitelik 'buton düzeyinde form hedefi ezme (formaction attribute)' olarak bilinir."
```

### html-easy-input-readonly-vs-disabled

```yaml
id: html-easy-input-readonly-vs-disabled
version: 1
language: html
engine: none
difficulty: easy
title: "Salt okunur (readonly) ve devre dışı (disabled) alan ayrımı"
prompt: |
  Bir profil güncelleme formunda iki kısıtlı alan oluşturun:
  1) 'Referans Kodu' alanı kullanıcı tarafından değiştirilemez olmalı ancak form
  gönderildiğinde sunucuya iletilmelidir.
  2) 'Eski Kullanıcı Adı' alanı tamamen devre dışı bırakılmalı, odaklanılamamalı ve
  form gönderildiğinde sunucuya gitmemelidir.
constraints:
  - "Değeri sunucuya gidecek değiştirilemez alan için `readonly` niteliği kullanılmalı"
  - "Tamamen pasif ve sunucuya gitmeyecek alan için `disabled` niteliği kullanılmalı"
concept_tags: [forms, input-validation, security]
checklist_extra:
  - "Sunucuya gitmesi gereken alana yanlışlıkla disabled verilmiş mi?"
  - "readonly ile disabled arasındaki form gönderim farkı gözetildi mi?"
reference_solution_path: private/solutions/html-easy-input-readonly-vs-disabled.html
hint_ladder:
  1: "Kullanıcının değiştiremediği ama formla birlikte sunucuya iletilen alan niteliği nedir?"
  2: "Hem ekranda soluk duran hem de form verisinden tamamen muaf tutulan alan niteliği hangisidir?"
  3: "Bu ayrım 'salt okunur ile devre dışı girdi alanı farkı (readonly vs disabled)' olarak bilinir."
```

### html-easy-input-autofocus-attribute

```yaml
id: html-easy-input-autofocus-attribute
version: 1
language: html
engine: none
difficulty: easy
title: "Sayfa açılışında otomatik odaklanma (autofocus)"
prompt: |
  Özel bir oturum açma sayfasında, sayfa yüklenir yüklenmez kullanıcının fareye dokunmasına
  gerek kalmadan imlecin doğrudan 'Kullanıcı Adı' kutusunun içinde hazır yanıp sönmesini
  sağlayan standart HTML niteliğini ekleyin.
constraints:
  - "`<input>` üzerinde `autofocus` niteliği bulunmalı"
  - "Sayfada yalnızca tek bir elemana autofocus verilmeli"
concept_tags: [forms, focus, accessibility]
checklist_extra:
  - "Sayfada birden fazla elemana autofocus verilerek kafa karışıklığı yaratılmış mı?"
  - "Kullanıcı deneyimini bozmayacak bir giriş sayfasında mı kullanıldı?"
reference_solution_path: private/solutions/html-easy-input-autofocus-attribute.html
hint_ladder:
  1: "Sayfa açıldığında imleci doğrudan belirli bir form kutusuna odaklayan boole nitelik nedir?"
  2: "JavaScript ile element.focus() çağırmak yerine yerel HTML niteliği hangisidir?"
  3: "Bu nitelik 'otomatik girdi odaklanma niteliği (autofocus attribute)' olarak bilinir."
```

### html-easy-input-minlength-maxlength

```yaml
id: html-easy-input-minlength-maxlength
version: 1
language: html
engine: none
difficulty: easy
title: "Karakter sayısı alt ve üst sınır kısıtlaması"
prompt: |
  Kullanıcı adı giriş kutusuna karakter sınırı getirin: Kullanıcı adı en az 3 karakter,
  en fazla 15 karakter uzunluğunda olmalıdır. Kullanıcının 15 karakterden fazla yazmasını
  engelleyen ve 3 karakterden az yazdığında formu göndermesini durduran yerel nitelikleri ekleyin.
constraints:
  - "`minlength='3'` niteliği bulunmalı"
  - "`maxlength='15'` niteliği bulunmalı"
concept_tags: [forms, input-validation, standards]
checklist_extra:
  - "Sayısal değer kısıtı olan min/max ile metin uzunluk kısıtı olan minlength/maxlength karıştırılmış mı?"
  - "Kullanıcıya izin verilen karakter uzunluğu etikette açıklanmış mı?"
reference_solution_path: private/solutions/html-easy-input-minlength-maxlength.html
hint_ladder:
  1: "Bir metin kutusuna girilebilecek en az karakter sayısını hangi nitelik denetler?"
  2: "Kullanıcının kutuya daha fazla karakter yazmasını fiziksel olarak durduran nitelik nedir?"
  3: "Bu kısıtlar 'metin uzunluk sınırlandırma nitelikleri (minlength and maxlength)' olarak bilinir."
```

### html-easy-img-loading-lazy

```yaml
id: html-easy-img-loading-lazy
version: 1
language: html
engine: none
difficulty: easy
title: "Ekran dışı görsellerde gecikmeli yükleme (Lazy Loading)"
prompt: |
  Sayfanın en altında yer alan ve kullanıcı sayfayı aşağı kaydırana kadar ilk yüklemede
  indirilmesine gerek olmayan bir blog görseli tanımlayın. Ağ trafiğini ve sayfa açılış
  hızını korumak için tarayıcının yerel tembel yükleme mekanizmasını devreye sokun.
constraints:
  - "`<img>` etiketi üzerinde `loading='lazy'` niteliği bulunmalı"
  - "Düzen kaymasını önlemek için görselin `width` ve `height` değerleri açıkça yazılmalı"
concept_tags: [images, performance, standards]
checklist_extra:
  - "Sayfanın en tepesindeki ilk açılış görseline (LCP görseli) yanlışlıkla loading='lazy' verilmiş mi?"
  - "Görselin genişlik ve yükseklik piksel boyutları belirtilmiş mi?"
reference_solution_path: private/solutions/html-easy-img-loading-lazy.html
hint_ladder:
  1: "Tarayıcının resmi yalnızca ekranda görünür alana yaklaştığında indirmesini sağlayan nitelik nedir?"
  2: "loading niteliğine hangi değer atanmalıdır?"
  3: "Bu performans tekniği 'yerel tembel görsel yükleme (native image lazy loading)' olarak bilinir."
```

### html-easy-img-aspect-ratio-dimensions

```yaml
id: html-easy-img-aspect-ratio-dimensions
version: 1
language: html
engine: none
difficulty: easy
title: "Kümülatif düzen kaymasını (CLS) önleyen görsel boyutları"
prompt: |
  Bir web sayfasında yüksek çözünürlüklü bir fotoğraf sergileyin. Görsel dosya ağdan
  yüklenirken tarayıcının görsel için ekranda doğru en-boy oranında boş bir alan rezerve
  etmesini sağlayan, böylece görsel yüklendiğinde metinlerin aşağı doğru zıplamasını
  (Cumulative Layout Shift) engelleyen temel boyutlandırma niteliklerini ekleyin.
constraints:
  - "`<img>` üzerinde piksel birimi olmadan `width` ve `height` nitelikleri bulunmalı (ör. width='800' height='600')"
  - "Geçerli bir `alt` metni bulunmalı"
concept_tags: [images, performance, standards]
checklist_extra:
  - "Boyut niteliklerine 'px' yazılarak HTML kuralları ihlal edilmiş mi?"
  - "Boyutlar atlanarak sayfa yüklenirken içeriklerin zıplamasına yol açılmış mı?"
reference_solution_path: private/solutions/html-easy-img-aspect-ratio-dimensions.html
hint_ladder:
  1: "Tarayıcının resim inmeden önce en-boy oranını (aspect-ratio) hesaplayabilmesi için img etiketine hangi iki niteliği yazmalısın?"
  2: "Modern web performansında CLS (Cumulative Layout Shift) puanını düşüren en ucuz yöntem nedir?"
  3: "Bu tanımlama 'en-boy oranı korumalı görsel boyutlandırması' olarak bilinir."
```

### html-easy-iframe-basic-embed

```yaml
id: html-easy-iframe-basic-embed
version: 1
language: html
engine: none
difficulty: easy
title: "Gömülü çerçeve (iframe) ve erişilebilir başlık"
prompt: |
  Web sayfanızın içine harici bir harita veya video içeriği gömen bir `<iframe>` etiketi
  yerleştirin. Ekran okuyucu kullanan bir ziyaretçi çerçevenin üzerine geldiğinde içine
  girmeden önce çerçevenin ne içerdiğini anlayabilmesi için çerçeveye erişilebilir bir
  başlık tanımlayın.
constraints:
  - "`<iframe>` etiketi üzerinde anlamlı bir `title` niteliği bulunmalı"
  - "Geçerli bir `src` kaynağı belirtilmeli"
concept_tags: [accessibility, standards, security]
checklist_extra:
  - "title niteliği tamamen unutulmuş veya 'iframe' gibi anlamsız mı bırakılmış?"
  - "Gömülü çerçevenin genişlik ve yükseklik boyutları tanımlanmış mı?"
reference_solution_path: private/solutions/html-easy-iframe-basic-embed.html
hint_ladder:
  1: "Ekran okuyucuların bir iframe ile karşılaştığında kullanıcıya okuduğu zorunlu nitelik nedir?"
  2: "title niteliğinde çerçevenin içeriğini (örneğin 'Şirket Merkez Ofisi Google Haritası') nasıl özetlersin?"
  3: "Bu erişilebilirlik gereksinimi 'erişilebilir çerçeve başlığı (accessible iframe title)' olarak bilinir."
```

### html-easy-meta-robots-noindex

```yaml
id: html-easy-meta-robots-noindex
version: 1
language: html
engine: none
difficulty: easy
title: "Arama motoru dizinleme engeli (noindex meta)"
prompt: |
  Yalnızca kurum içi kullanıcılara açık olan bir intranet sayfasına veya ödeme başarı
  ekranına ait bir HTML şablonu hazırlayın. Arama motorlarının bu sayfayı kesinlikle
  arama sonuçlarında dizine eklememesini (indexlememesini) bildiren standart robots
  meta etiketini `<head>` bölümüne yerleştirin.
constraints:
  - "name='robots' niteliği bulunmalı"
  - "content niteliğinde 'noindex' talimatı yer almalı"
concept_tags: [standards, security]
checklist_extra:
  - "noindex yerine hatalı anahtar kelimeler mi kullanılmış?"
  - "Meta etiketi head bölümü içinde mi?"
reference_solution_path: private/solutions/html-easy-meta-robots-noindex.html
hint_ladder:
  1: "Arama motoru botlarına 'bu sayfayı arama sonuçlarına ekleme' diyen meta etiketi hangisidir?"
  2: "name='robots' meta etiketinin content değerine ne yazılır?"
  3: "Bu yönerge 'arama motoru dizin engelleme bildirimi (robots noindex meta)' olarak bilinir."
```

---
## Orta Düzey Sorular (101 - 150)

### html-medium-responsive-picture-art-direction

```yaml
id: html-medium-responsive-picture-art-direction
version: 1
language: html
engine: none
difficulty: medium
title: "Sanatsal yönlendirme ile duyarlı görsel seçimi (picture ve media sorgusu)"
prompt: |
  Bir e-ticaret vitrini için duyarlı banner bileşeni tasarlıyorsunuz. Masaüstü ekranlarda
  geniş açılı yatay banner görseli sunulurken, dar mobil ekranlarda görselin önemli detayını
  merkeze alan dikey kırpılmış kare versiyonu sunulmalıdır. Ayrıca tarayıcı bu modern yapıyı
  desteklemediğinde standart bir yedek görsel görüntülenmelidir. Bu sanatsal yönlendirmeyi
  sağlayan HTML yapısını kurun.
constraints:
  - "<picture> kapsayıcısı kullanılmalı"
  - "En az bir <source> elemanında media sorgusu bulunmalı"
  - "Yedekleme ve erişilebilirlik için geçerli alt metnine sahip <img> elemanı içermeli"
concept_tags: [images, performance, semantics]
checklist_extra:
  - "source etiketleri img etiketinden önce mi yerleştirilmiş?"
  - "alt özniteliği img elemanına mı tanımlanmış?"
reference_solution_path: private/solutions/html-medium-responsive-picture-art-direction.html
hint_ladder:
  1: "Farklı ekran genişliklerine göre farklı görsel dosyaları seçtirmek için hangi HTML5 kapsayıcısı kullanılır?"
  2: "Medya sorgusu ile alternatif görsel kaynağı tanımlamak için kapsayıcı içine hangi etiket yerleştirilir?"
  3: "Bu teknik HTML'de 'sanatsal yönlendirme görsel kapsayıcısı (picture ve source media)' olarak bilinir."
```

---

### html-medium-responsive-img-srcset-sizes

```yaml
id: html-medium-responsive-img-srcset-sizes
version: 1
language: html
engine: none
difficulty: medium
title: "Çözünürlük ve genişlik duyarlı görsel yükleme (srcset ve sizes)"
prompt: |
  Bir seyahat blogu için makale kapak görseli yerleştiriyorsunuz. Kullanıcının cihaz ekran genişliğine
  ve piksel yoğunluğuna bağlı olarak tarayıcının en optimum görsel boyutunu seçmesini istiyorsunuz.
  Küçük ekranlarda 400px genişlikte, orta ekranlarda 800px genişlikte ve büyük ekranlarda 1200px
  genişlikte dosya alternatifleri tanımlanmalı, ayrıca sayfa düzeninde görselin hangi ekran genişliğinde
  ne kadar alan kaplayacağı tarayıcıya önceden bildirilmelidir.
constraints:
  - "<img> etiketi üzerinde 'srcset' niteliği ile genişlik tanımlayıcıları (w) belirtilmeli"
  - "'sizes' niteliği ile medya koşulları ve yuva genişlikleri tanımlanmalı"
  - "src ve alt nitelikleri eksiksiz bulunmalı"
concept_tags: [images, performance, standards]
checklist_extra:
  - "Genişlik tanımlayıcılarında px yerine w birimi mi kullanılmış?"
  - "sizes niteliğinde son fallback genişliği belirtilmiş mi?"
reference_solution_path: private/solutions/html-medium-responsive-img-srcset-sizes.html
hint_ladder:
  1: "Tarayıcıya tek bir görsel için farklı genişlik alternatiflerini hangi nitelikle listeleriz?"
  2: "Görselin ekranda kaplayacağı genişliği tarayıcının düzen hesaplamadan önce bilmesini sağlayan nitelik nedir?"
  3: "Bu yöntem duyarlı görsellerde 'kaynak kümesi ve yuva boyutu bildirimi (srcset ve sizes)' olarak bilinir."
```

---

### html-medium-accessible-modal-dialog

```yaml
id: html-medium-accessible-modal-dialog
version: 1
language: html
engine: none
difficulty: medium
title: "Yerel erişilebilir modal iletişim kutusu (dialog ve form method dialog)"
prompt: |
  Kullanıcı hesap ayarlarını silmek istediğinde ekranda beliren yerel bir onay penceresi
  oluşturun. Sayfa arkasını karartan ve klavye odağını içine hapseden yerel HTML pencere
  elemanını kullanın. Pencere içinde başlık, açıklama metni, iptal butonu ve onay butonu
  bulunmalıdır. İptal butonuna tıklandığında pencereyi JavaScript yazmaya gerek kalmadan
  kendiliğinden kapatan form yöntemini uygulayın.
constraints:
  - "<dialog> elemanı kullanılmalı"
  - "İçerisinde method='dialog' olan bir <form> yer almalı"
  - "Pencereyi kapatan buton form içinde yer almalı"
concept_tags: [dialogs, accessibility, focus]
checklist_extra:
  - "Form method özniteliği dialog olarak ayarlanmış mı?"
  - "Modal başlığı için anlamsal bir başlık etiketi kullanılmış mı?"
reference_solution_path: private/solutions/html-medium-accessible-modal-dialog.html
hint_ladder:
  1: "HTML5 ile gelen yerel modal ve iletişim kutusu etiketi nedir?"
  2: "Dialog elemanını JavaScript kodu çalıştırmadan kapatmak için hangi form gönderim metodu kullanılır?"
  3: "Bu mekanizma modern web standartlarında 'yerel iletişim kutusu ve kapatma formu (dialog method dialog)' olarak bilinir."
```

---

### html-medium-accessible-accordion-disclosure

```yaml
id: html-medium-accessible-accordion-disclosure
version: 1
language: html
engine: none
difficulty: medium
title: "Erişilebilir açılır kapanır akordeon paneli (WAI-ARIA disclosure)"
prompt: |
  Bir sıkça sorulan sorular bölümünde özel JavaScript ile yönetilecek bir akordeon başlığı ve
  içerik paneli çifti tasarlıyorsunuz. Görme engelli ekran okuyucu kullanıcılarının, tetikleyici
  butonun hangi içerik alanını kontrol ettiğini ve o içeriğin şu anda açık mı yoksa kapalı mı
  olduğunu net bir şekilde duyabilmesini sağlayacak erişilebilirlik bağlantılarını ve durum
  niteliklerini HTML yapısına eksiksiz ekleyin.
constraints:
  - "Tetikleyici bir <button> elemanı olmalı"
  - "Buton üzerinde kontrol edilen alanın id'sini belirten aria-controls bulunmalı"
  - "Buton üzerinde panelin açık/kapalı durumunu belirten aria-expanded niteliği bulunmalı"
  - "Açılan içerik paneli butondaki referans id ile eşleşmeli"
concept_tags: [accessibility, focus, semantics]
checklist_extra:
  - "aria-expanded değeri boolean ('true' veya 'false') dizesi olarak verilmiş mi?"
  - "Tetikleyici olarak div yerine anlamsal button etiketi tercih edilmiş mi?"
reference_solution_path: private/solutions/html-medium-accessible-accordion-disclosure.html
hint_ladder:
  1: "Ekran okuyucuya bir panelin açılıp kapandığını bildiren WAI-ARIA niteliği nedir?"
  2: "Tetikleyici buton ile açılan panelin id değerini birbirine bağlayan ARIA niteliği hangisidir?"
  3: "Bu erişilebilirlik deseni 'açılır kapanır durum bildirimi (aria-expanded ve aria-controls)' olarak bilinir."
```

---

### html-medium-skip-to-main-link

```yaml
id: html-medium-skip-to-main-link
version: 1
language: html
engine: none
difficulty: medium
title: "Ana içeriğe atlama bağlantısı (skip navigation link)"
prompt: |
  Çok sayıda menü bağlantısı içeren karmaşık bir web portalında, yalnızca klavye kullanan veya
  ekran okuyucu kullanan ziyaretçilerin her sayfada onlarca menü elemanını tek tek geçmek
  zorunda kalmadan doğrudan sayfanın birincil içerik alanına odaklanmasını sağlayacak bir
  atlama köprüsü kurun. Sayfanın en başında yer alacak bu bağlantı ana içeriği hedeflemelidir.
constraints:
  - "Sayfanın en üstünde gövde içindeki ilk odaklanabilir eleman bir <a> bağlantısı olmalı"
  - "Bağlantının href değeri ana içerik alanının id değerine yönlenmeli (örn. #main-content)"
  - "Hedef <main> elemanı ilgili id değerini taşımalı"
concept_tags: [navigation, accessibility, focus]
checklist_extra:
  - "Atlama bağlantısı sayfa yapısında navigasyon menüsünden önce mi?"
  - "Href değeri başındaki diyez (#) işareti ile hedef kimliği birebir eşleşiyor mu?"
reference_solution_path: private/solutions/html-medium-skip-to-main-link.html
hint_ladder:
  1: "Klavye kullanıcılarının uzun menüleri atlayıp doğrudan içeriğe geçmesini sağlayan yapı nedir?"
  2: "Sayfa içi bağlantı oluştururken href niteliğinde hedef öğenin id'si nasıl belirtilir?"
  3: "Bu erişilebilirlik bileşeni 'ana içeriğe atlama bağlantısı (skip link)' olarak bilinir."
```

---

### html-medium-table-id-headers-association

```yaml
id: html-medium-table-id-headers-association
version: 1
language: html
engine: none
difficulty: medium
title: "Çok düzeyli karmaşık tablo hücre ilişkilendirmesi (id ve headers)"
prompt: |
  Bir şirketin çeyreklik finansal tablosunu hazırlıyorsunuz. Tabloda birden fazla düzeyde
  kategori başlıkları (örneğin üst başlık '2024 Gelirleri', alt başlık 'Avrupa Bölgesi')
  ve satır başlıkları bulunmaktadır. Yalnızca scope niteliğinin yetersiz kaldığı bu karmaşık
  yapıda, her veri hücresinin (td) hangi üst ve satır başlıklarına ait olduğunu ekran
  okuyucuların kesin olarak okuyabilmesi için doğrudan kimlik tabanlı ilişkilendirme kurun.
constraints:
  - "Tüm başlık (<th>) hücrelerinde benzersiz 'id' nitelikleri bulunmalı"
  - "Veri (<td>) hücrelerinde ait oldukları başlıkların id listesini içeren 'headers' niteliği bulunmalı"
  - "Headers değeri aralarında boşluk olan ilgili başlık id'lerini içermeli"
concept_tags: [tables, accessibility, standards]
checklist_extra:
  - "Headers niteliğinde birden çok id varsa boşlukla ayrılmış mı?"
  - "Tüm th id değerleri sayfada tekil mi?"
reference_solution_path: private/solutions/html-medium-table-id-headers-association.html
hint_ladder:
  1: "Karmaşık tablolarda hücreleri birden çok hiyerarşik başlıkla eşleştirmek için td'de hangi nitelik kullanılır?"
  2: "Başlık hücrelerine verilen benzersiz kimlikler veri hücresinin hangi niteliğine virgül olmadan yazılır?"
  3: "Bu teknik tablolarda 'hücre ve başlık kimlik eşleştirmesi (id ve headers nitelikleri)' olarak bilinir."
```

---

### html-medium-form-floating-label-structure

```yaml
id: html-medium-form-floating-label-structure
version: 1
language: html
engine: none
difficulty: medium
title: "Kayan etiketli erişilebilir form alanı yapısı (floating label)"
prompt: |
  Modern arayüz tasarımlarında sıklıkla tercih edilen kayan etiket (floating label) stilini
  CSS ile uygulayabilmek için gereken anlamsal HTML iskeletini hazırlayın. Girdi kutusu boşken
  veya odaklandığında CSS kardeş seçicilerinin (+ veya ~) doğru çalışabilmesi için etiket ve
  girdi elemanının sıralaması kritik önemdedir. Ancak bu görsel sıralamaya rağmen alanın ekran
  okuyucular için tam erişilebilir kalmasını sağlayın.
constraints:
  - "<input> elemanı <label> elemanından hemen önce gelmeli"
  - "İki eleman ortak bir kapsayıcı (<div>) içinde yer almalı"
  - "input 'id' değeri ile label 'for' değeri birebir eşleşmeli"
  - "input üzerinde CSS kardeş seçicisi kontrolü için boşluk placeholder'ı veya standart placeholder bulunmalı"
concept_tags: [forms, accessibility, semantics]
checklist_extra:
  - "CSS kardeş seçicisinin çalışması için input etiketi label etiketinin önünde mi?"
  - "for ve id bağlantısı eksiksiz kurulmuş mu?"
reference_solution_path: private/solutions/html-medium-form-floating-label-structure.html
hint_ladder:
  1: "CSS'te input:focus + label kuralının çalışabilmesi için HTML'de eleman sırası nasıl olmalıdır?"
  2: "Girdi alanı ile etiketinin tarayıcı ve yardımcı teknolojilerce bağlanması için hangi ikili kullanılır?"
  3: "Bu düzenleme 'kayan etiket HTML iskeleti (floating label pattern)' olarak bilinir."
```

---

### html-medium-aria-live-polite-notifications

```yaml
id: html-medium-aria-live-polite-notifications
version: 1
language: html
engine: none
difficulty: medium
title: "Nezaket bildirimli dinamik canlı bölge (aria-live polite)"
prompt: |
  Bir mesajlaşma veya sipariş takip arayüzünde, sayfa yenilenmeden arka planda güncellenen
  durum mesajlarının (örneğin 'Mesajınız iletildi' veya 'Sepet güncellendi') ekran okuyucu
  kullanıcılarına kullanıcı o anki işini bitirdikten sonra sakin bir şekilde seslendirilmesini
  sağlayacak bir bildirim kapsayıcısı oluşturun. Bildirimin parça parça değil bütün olarak
  okunmasını garanti altına alın.
constraints:
  - "Canlı bölge kapsayıcısında 'aria-live=\"polite\"' niteliği bulunmalı"
  - "İçeriğin tamamının birlikte okunması için 'aria-atomic=\"true\"' niteliği tanımlanmalı"
  - "Elemanın bir 'id' veya anlamlı bir 'role=\"status\"' niteliği bulunmalı"
concept_tags: [accessibility, focus, standards]
checklist_extra:
  - "aria-live değeri 'assertive' yerine kullanıcıyı bölmeyen 'polite' olarak seçilmiş mi?"
  - "aria-atomic değeri true olarak belirlenmiş mi?"
reference_solution_path: private/solutions/html-medium-aria-live-polite-notifications.html
hint_ladder:
  1: "Dinamik olarak değişen içerikleri ekran okuyucuya kullanıcıyı bölmeden okutmak için hangi ARIA niteliği kullanılır?"
  2: "Bölgedeki metin değiştiğinde yalnızca değişen harflerin değil tüm cümlenin okunması için hangi nitelik eklenir?"
  3: "Bu erişilebilirlik alanı 'nezaket canlı bölgesi (aria-live polite ve aria-atomic)' olarak bilinir."
```

---

### html-medium-aria-live-assertive-alert

```yaml
id: html-medium-aria-live-assertive-alert
version: 1
language: html
engine: none
difficulty: medium
title: "Acil hata ve uyarı canlı bölgesi (role alert)"
prompt: |
  Bir bankacılık transfer formunda, işlem sırasında internet bağlantısı koptuğunda veya
  oturum süresi dolduğunda anında gösterilecek kritik bir hata paneli tasarlayın. Bu uyarının,
  ekran okuyucunun o anda okuduğu diğer tüm içerikleri derhal keserek kullanıcıya en yüksek
  öncelikle acilen bildirilmesi gerekmektedir. Bu kritik uyarıyı temsil eden WAI-ARIA
  rolünü ve canlı bölge mantığını kurun.
constraints:
  - "Uyarı paneli üzerinde 'role=\"alert\"' veya 'aria-live=\"assertive\"' tanımlanmalı"
  - "İçerik değiştiğinde tamamının okunması için 'aria-atomic=\"true\"' yer almalı"
  - "Anlamsal olarak hata mesajını net açıklayan bir metin barındırmalı"
concept_tags: [accessibility, forms, standards]
checklist_extra:
  - "Kritik kesici bildirimler için standart alert rolü atanmış mı?"
  - "Hata mesajı metni kullanıcı için açıklayıcı mı?"
reference_solution_path: private/solutions/html-medium-aria-live-assertive-alert.html
hint_ladder:
  1: "Kullanıcının mevcut okumasını yarıda kesip acil hata bildiren WAI-ARIA rolü hangisidir?"
  2: "Acil uyarılar için aria-live niteliğinin alması gereken en agresif değer nedir?"
  3: "Bu uyarı mekanizması 'acil hata canlı bildirim bölgesi (role alert veya aria-live assertive)' olarak bilinir."
```

---

### html-medium-accessible-search-landmark

```yaml
id: html-medium-accessible-search-landmark
version: 1
language: html
engine: none
difficulty: medium
title: "Anlamsal arama alanı sınır noktası (search elementi ve arama formu)"
prompt: |
  Web sitenizin üst başlığında (header) yer alacak global site arama bölümünü inşa edin.
  HTML5.2 ve güncel web standartlarıyla gelen anlamsal arama sınır noktası (landmark)
  etiketini kullanarak arama formunu çevreleyin. Form içinde arama kutusu ve arama butonu
  yer almalı, ekran okuyucular arama kutusunun işlevini etiket veya erişilebilir isim
  üzerinden doğrudan tanıyabilmelidir.
constraints:
  - "<search> elemanı kapsayıcı olarak kullanılmalı"
  - "İçerisinde method='get' olan bir <form> yer almalı"
  - "<input type='search'> elemanı ve ona bağlı erişilebilir etiket bulunmalı"
  - "Gönderim için uygun bir arama butonu yer almalı"
concept_tags: [semantics, navigation, accessibility]
checklist_extra:
  - "Modern search etiketi kullanılmış mı veya rol search atanmış mı?"
  - "Arama girdisinin tipi 'search' olarak belirlenmiş mi?"
reference_solution_path: private/solutions/html-medium-accessible-search-landmark.html
hint_ladder:
  1: "Modern HTML'de arama formlarını sarmak için eklenen anlamsal sınır noktası etiketi nedir?"
  2: "Arama kutusu için type özniteliğine hangi değer verilmelidir?"
  3: "Bu anlamsal sınır noktası 'HTML arama elemanı (search landmark)' olarak bilinir."
```

---

### html-medium-iframe-sandboxing-security

```yaml
id: html-medium-iframe-sandboxing-security
version: 1
language: html
engine: none
difficulty: medium
title: "Güvenli harici içerik gömme ve kum havuzu kısıtlaması (iframe sandbox)"
prompt: |
  Kullanıcıların kendi sitelerine üçüncü taraf bir anket sağlayıcısının formunu gömmesi
  gerekmektedir. Ancak bu gömülü içeriğin üst pencerenin çerezlerine erişmesini, zararlı
  açılır pencereler (pop-up) oluşturmasını ve otomatik form göndermesini engellemek; yalnızca
  belirtilen formun kendi içinde script çalıştırmasına ve form post etmesine izin vermek
  istiyorsunuz. Bu izolasyonu sağlayan güvenlik niteliklerini tanımlayın.
constraints:
  - "<iframe> etiketi üzerinde 'sandbox' niteliği bulunmalı"
  - "Yalnızca 'allow-scripts' ve 'allow-forms' izinleri açıkça listelenmeli"
  - "'title' niteliği ile çerçevenin amacı erişilebilir şekilde belirtilmeli"
concept_tags: [security, standards, accessibility]
checklist_extra:
  - "allow-same-origin izni gereksiz yere eklenerek güvenlik zafiyeti oluşturulmuş mu?"
  - "iframe için açıklayıcı bir title niteliği verilmiş mi?"
reference_solution_path: private/solutions/html-medium-iframe-sandboxing-security.html
hint_ladder:
  1: "Bir iframe'in çalıştırabileceği yetkileri kısıtlayan güvenlik niteliği hangisidir?"
  2: "Kısıtlı kum havuzunda yalnızca betik çalıştırmaya ve form göndermeye izin veren anahtar kelimeler nelerdir?"
  3: "Bu güvenlik önlemi 'çerçeve kum havuzu kısıtlaması (iframe sandbox)' olarak bilinir."
```

---

### html-medium-form-inputmode-virtual-keyboard

```yaml
id: html-medium-form-inputmode-virtual-keyboard
version: 1
language: html
engine: none
difficulty: medium
title: "Sanal klavye optimizasyonu (inputmode ve enterkeyhint)"
prompt: |
  Mobil cihaz kullanıcılarının üye kayıt ve ödeme adımlarında form doldurmasını kolaylaştırmak
  istiyorsunuz. Kullanıcı kredi kartı son kullanma tarihini yazarken doğrudan rakamsal tuş takımının,
  arama çubuğunda arama yaparken klavyede 'Ara' eylem butonunun, e-posta alanında ise '@' işaretini
  barındıran e-posta klavyesinin açılmasını sağlayan standart HTML girdi modu niteliklerini
  içeren üç farklı girdi alanı kurgulayın.
constraints:
  - "Sayısal girdi için 'inputmode=\"numeric\"' kullanılmalı"
  - "E-posta veya arama girdisinde uygun inputmode ('email' veya 'search') yer almalı"
  - "Klavyedeki onay tuşunun etiketini belirten 'enterkeyhint' niteliği en az bir alanda kullanılmalı"
concept_tags: [forms, input-validation, standards]
checklist_extra:
  - "Mobil sanal klavye tipini belirlemek için inputmode niteliği doğru atanmış mı?"
  - "Tüm girdi alanlarının etiketleri (label) bulunuyor mu?"
reference_solution_path: private/solutions/html-medium-form-inputmode-virtual-keyboard.html
hint_ladder:
  1: "Mobil cihazlarda girdi alanına tıklandığında açılacak klavye düzenini belirleyen nitelik nedir?"
  2: "Mobil klavyenin 'Git/Tamam' tuşunun işlevini 'Arama' veya 'Gönder' olarak özelleştiren ipucu niteliği nedir?"
  3: "Bu mobil arayüz optimizasyonu 'sanal klavye modu yönlendirmesi (inputmode ve enterkeyhint)' olarak bilinir."
```

---

### html-medium-form-autocomplete-payment

```yaml
id: html-medium-form-autocomplete-payment
version: 1
language: html
engine: none
difficulty: medium
title: "Ödeme formu tarayıcı otomatik tamamlama standartları (autocomplete payment)"
prompt: |
  E-ticaret ödeme adımında kullanıcıların kredi kartı bilgilerini tarayıcı cüzdanlarından
  tek tıkla doldurabilmeleri için WHATWG standartlarına uygun bir kredi kartı formu oluşturun.
  Kart üzerindeki isim, kart numarası, son kullanma ayı/yılı ve güvenlik kodu (CVV/CVC)
  alanlarını tarayıcının doğru tanıyabilmesi için uluslararası otomatik doldurma standart
  değerlerini ilgili alanlara tanımlayın.
constraints:
  - "Kart sahibi adı için 'autocomplete=\"cc-name\"' bulunmalı"
  - "Kart numarası için 'autocomplete=\"cc-number\"' bulunmalı"
  - "Son kullanma tarihi için 'autocomplete=\"cc-exp\"' veya ay/yıl ayrık değerleri bulunmalı"
  - "Güvenlik kodu için 'autocomplete=\"cc-csc\"' bulunmalı"
concept_tags: [forms, security, standards]
checklist_extra:
  - "Autocomplete değerleri standart cc-* öneklerini taşıyor mu?"
  - "Girdi tipleri ve güvenlik kodu alanında uygun şifreleme/maskeleme düşünülmüş mü?"
reference_solution_path: private/solutions/html-medium-form-autocomplete-payment.html
hint_ladder:
  1: "Tarayıcıların kredi kartı numarasını otomatik doldurması için autocomplete niteliğine hangi standart değer verilir?"
  2: "Güvenlik kodu (CVV) için tanımlanmış global autocomplete değeri nedir?"
  3: "Bu standart ödeme formu doldurma kuralı 'kredi kartı otomatik tamamlama nitelikleri (autocomplete cc-*)' olarak bilinir."
```

---

### html-medium-form-autocomplete-address

```yaml
id: html-medium-form-autocomplete-address
version: 1
language: html
engine: none
difficulty: medium
title: "Teslimat adresi otomatik tamamlama standartları (autocomplete shipping)"
prompt: |
  Bir kargo teslimat formu hazırlıyorsunuz. Kullanıcının kayıtlı adresini tarayıcısından
  veya parola yöneticisinden sorunsuz şekilde çekebilmesi için form alanlarını standartlaştırın.
  Sokak adresi, şehir/il, posta kodu ve ülke alanlarının hem teslimat (shipping) kapsamında
  olduğunu hem de ilgili veri türüne karşılık geldiğini belirten standart otomatik doldurma
  sözdizimini uygulayın.
constraints:
  - "Sokak adresi için 'autocomplete=\"shipping street-address\"' kullanılmalı"
  - "Şehir için 'autocomplete=\"shipping address-level2\"' kullanılmalı"
  - "Posta kodu için 'autocomplete=\"shipping postal-code\"' kullanılmalı"
  - "Ülke için 'autocomplete=\"shipping country\"' veya ülke adı değeri bulunmalı"
concept_tags: [forms, standards, input-validation]
checklist_extra:
  - "Adres seviyeleri için standart address-level2 terimi kullanılmış mı?"
  - "Teslimat adresi olduğunu belirtmek üzere shipping kapsam öneki eklenmiş mi?"
reference_solution_path: private/solutions/html-medium-form-autocomplete-address.html
hint_ladder:
  1: "Tarayıcıya bir adres alanının teslimat adresi olduğunu belirtmek için hangi kapsam öneki kullanılır?"
  2: "Standart adres doldurmada şehir/ilçe alanı hangi address-level anahtarı ile ifade edilir?"
  3: "Bu uluslararası form standardı 'teslimat adresi otomatik tamamlama bildirimi (autocomplete shipping)' olarak bilinir."
```

---

### html-medium-accessible-breadcrumbs-nav

```yaml
id: html-medium-accessible-breadcrumbs-nav
version: 1
language: html
engine: none
difficulty: medium
title: "Erişilebilir ekmek kırıntısı gezintisi (breadcrumbs ve aria-current page)"
prompt: |
  Kullanıcının sitede nerede olduğunu gösteren bir ekmek kırıntısı (breadcrumbs) gezinti
  yolu tasarlayın. Bu yapıyı diğer gezinme menülerinden ayırt etmek için açıklayıcı bir
  etiketle donatın. Sıralı bir liste kullanarak sayfaları hiyerarşik olarak dizin ve
  kullanıcının şu anda üzerinde bulunduğu son öğenin aktif sayfa olduğunu hem arama
  motorlarına hem de ekran okuyuculara açıkça bildirin.
constraints:
  - "<nav aria-label='...'> kapsayıcısı kullanılmalı"
  - "Hiyerarşik sıralama için <ol> ve <li> etiketleri kullanılmalı"
  - "Son öğede veya o öğenin bağlantısında 'aria-current=\"page\"' niteliği bulunmalı"
  - "Son öğe genellikle tıklanabilir olmayan bir metin veya bağlantısız eleman olmalı"
concept_tags: [navigation, accessibility, semantics]
checklist_extra:
  - "Ekmek kırıntısı gezintisi için ol listesi tercih edilmiş mi?"
  - "Geçerli sayfayı işaretlemek için aria-current='page' kullanılmış mı?"
reference_solution_path: private/solutions/html-medium-accessible-breadcrumbs-nav.html
hint_ladder:
  1: "Ekmek kırıntısı menüsünü sayfanın ana menüsünden ayırt etmek için nav etiketine ne eklenir?"
  2: "Kullanıcının o an bulunduğu son adımı ekran okuyucuya aktarmak için hangi ARIA niteliği kullanılır?"
  3: "Bu navigasyon deseni 'erişilebilir ekmek kırıntısı gezintisi (breadcrumbs aria-current)' olarak bilinir."
```

---

### html-medium-accessible-pagination-nav

```yaml
id: html-medium-accessible-pagination-nav
version: 1
language: html
engine: none
difficulty: medium
title: "Erişilebilir sayfalandırma gezintisi (pagination nav)"
prompt: |
  Bir arama sonuçları sayfasının altında yer alacak sayfalandırma (pagination) bileşeni
  geliştiriyorsunuz. Gezinme bölgesinin amacını belirten bir etiket verin, sayfa numaralarını
  bir liste içinde sunun. Kullanıcının o anda görüntülemekte olduğu aktif sayfa numarasını
  yardımcı teknolojilerin açıkça seslendirebilmesini sağlayın ve önceki/sonraki sayfa
  bağlantılarına açıklayıcı etiketler tanımlayın.
constraints:
  - "<nav aria-label='Sayfalandırma'> kapsayıcısı bulunmalı"
  - "Sayfa numaraları <ul> ve <li> içinde bağlantılar olarak yer almalı"
  - "Aktif sayfa bağlantısında 'aria-current=\"page\"' yer almalı"
  - "Önceki ve sonraki butonları için erişilebilir etiketleme veya metin bulunmalı"
concept_tags: [navigation, accessibility, links]
checklist_extra:
  - "Nav etiketine amaca yönelik açıklayıcı aria-label verilmiş mi?"
  - "Aktif sayfa numarası aria-current niteliği ile vurgulanmış mı?"
reference_solution_path: private/solutions/html-medium-accessible-pagination-nav.html
hint_ladder:
  1: "Sayfa numaraları bloğunu diğer bağlantılardan ayırmak için hangi anlamsal etiket ve nitelik kullanılır?"
  2: "Mevcut aktif sayfayı gösteren bağlantıya hangi WAI-ARIA durumu eklenir?"
  3: "Bu gezinti yapısı 'erişilebilir sayfalandırma menüsü (accessible pagination)' olarak bilinir."
```

---

### html-medium-video-multiple-sources-subtitles

```yaml
id: html-medium-video-multiple-sources-subtitles
version: 1
language: html
engine: none
difficulty: medium
title: "Çoklu format ve altyazı destekli erişilebilir video oynatıcı (video track subtitles)"
prompt: |
  Bir eğitim platformunda video ders oynatıcısı yerleştiriyorsunuz. Farklı tarayıcı
  uyumluluğu ve yüksek sıkıştırma verimliliği için hem WebM hem de MP4 formatında iki ayrı
  video kaynağı sunun. İşitme engelli kullanıcılar veya sessiz ortamda izleyenler için
  Türkçe altyazı dosyası (.vtt) ekleyin ve varsayılan olarak bu altyazının aktif gelmesini sağlayın.
  Son olarak hiçbir video oynatıcısını desteklemeyen eski sistemler için bir yedek metin sunun.
constraints:
  - "<video controls> elemanı kullanılmalı"
  - "En az iki farklı formatta <source> etiketi bulunmalı"
  - "<track kind='subtitles' srclang='tr' default> etiketi yer almalı"
  - "Yedek indirme veya uyarı metni içermeli"
concept_tags: [accessibility, standards, performance]
checklist_extra:
  - "Altyazı dosyasının türü kind='subtitles' olarak tanımlanmış mı?"
  - "Varsayılan olarak açılması için track elemanına default boolean niteliği eklenmiş mi?"
reference_solution_path: private/solutions/html-medium-video-multiple-sources-subtitles.html
hint_ladder:
  1: "HTML5 video elemanına altyazı veya açıklama metni eklemek için hangi etiket kullanılır?"
  2: "Altyazı parçasının varsayılan olarak açık gelmesini sağlayan mantıksal (boolean) nitelik nedir?"
  3: "Bu multimedya yapısı 'altyazılı ve çok kaynaklı video bileşeni (video track subtitles)' olarak bilinir."
```

---

### html-medium-audio-accessible-transcripts

```yaml
id: html-medium-audio-accessible-transcripts
version: 1
language: html
engine: none
difficulty: medium
title: "Metin dökümlü erişilebilir ses çalar (audio ve metin transkripti)"
prompt: |
  Bir haber sitesinde yayınlanan haftalık podcast bölümü için ses oynatıcı bileşeni
  kuruyorsunuz. MP3 ve OGG formatlarında alternatif ses kaynakları sunun. İşitme engelli
  kullanıcıların ses kaydındaki tüm içeriğe eksiksiz ulaşabilmesi için oynatıcının hemen
  altında sesin tam metin dökümünü (transkript) barındıran anlamsal bir açılır/kapanır
  bölüm yerleştirin.
constraints:
  - "<audio controls> kapsayıcısı ve alternatif <source> etiketleri bulunmalı"
  - "Ses kaydının tam metin dökümü için <details> ve <summary> kullanılmalı"
  - "Bileşen anlamsal bir <section> veya <article> içinde yapılandırılmalı"
concept_tags: [accessibility, semantics, standards]
checklist_extra:
  - "Ses oynatıcı kontrolleri controls niteliği ile açılmış mı?"
  - "Erişilebilirlik transkripti details etiketiyle kullanıcıya sunulmuş mu?"
reference_solution_path: private/solutions/html-medium-audio-accessible-transcripts.html
hint_ladder:
  1: "HTML5 ses oynatıcılarına tarayıcı kontrollerini eklemek için hangi nitelik yazılır?"
  2: "Podcast metnini varsayılan olarak kapalı tutup istenildiğinde açtırmak için hangi yerel etiket çifti kullanılır?"
  3: "Bu kapsayıcı ses tasarımı 'transkript dökümlü erişilebilir ses bileşeni (audio with text transcript)' olarak bilinir."
```

---

### html-medium-svg-accessible-icon-button

```yaml
id: html-medium-svg-accessible-icon-button
version: 1
language: html
engine: none
difficulty: medium
title: "Erişilebilir SVG simgeli buton tasarımı (icon button)"
prompt: |
  Bir web uygulamasının üst çubuğunda yalnızca büyüteç simgesinden oluşan bir arama butonu
  yer alacaktır. Butonun içinde görünür bir metin bulunmayacak, yalnızca satır içi (inline)
  bir `<svg>` ikonu yer alacaktır. Ancak görme engelli ekran okuyucu kullanıcılarının bu butona
  odaklandıklarında 'Arama Yap' işlevini net biçimde duyabilmesi, görsel simgenin ise ekran
  okuyucular tarafından anlamsız kod yığını olarak seslendirilmemesi için gereken erişilebilirlik
  niteliklerini uygulayın.
constraints:
  - "<button> elemanında açıklayıcı 'aria-label' veya görsel olarak gizlenmiş metin span'ı bulunmalı"
  - "İçerideki <svg> üzerinde 'aria-hidden=\"true\"' ve 'focusable=\"false\"' yer almalı"
  - "Buton anlamsal olarak tıklanabilir bir buton öğesi olmalı"
concept_tags: [accessibility, focus, images]
checklist_extra:
  - "SVG simgesi aria-hidden='true' ile ekran okuyuculardan gizlenmiş mi?"
  - "Butonun görevi aria-label veya gizli metinle açıkça belirtilmiş mi?"
reference_solution_path: private/solutions/html-medium-svg-accessible-icon-button.html
hint_ladder:
  1: "Metin içermeyen butonlara ekran okuyucunun okuyacağı bir isim vermek için hangi ARIA niteliği kullanılır?"
  2: "Dekoratif SVG simgelerinin ekran okuyucu tarafından okunmasını engellemek için ne yazılır?"
  3: "Bu tasarım deseni 'erişilebilir simge butonu (accessible icon button)' olarak bilinir."
```

---

### html-medium-standalone-svg-graphic-accessibility

```yaml
id: html-medium-standalone-svg-graphic-accessibility
version: 1
language: html
engine: none
difficulty: medium
title: "Müstakil erişilebilir SVG grafik tasarımı (role img ve svg title)"
prompt: |
  Bir analiz raporunda bağımsız bir infografik veya şirket logo vektörü olarak satır içi
  `<svg>` kullanıyorsunuz. Bu grafiğin sadece dekoratif bir süs değil, önemli bir görsel
  içerik olduğunu tarayıcılara ve ekran okuyuculara bildirin. Grafiğe bir başlık ve detaylı
  açıklama metni tanımlayarak, bunları SVG elemanına erişilebilir isim ve açıklama olarak
  bağlayın.
constraints:
  - "<svg> üzerinde 'role=\"img\"' niteliği bulunmalı"
  - "SVG içinde benzersiz id'lere sahip <title> ve <desc> etiketleri bulunmalı"
  - "<svg> üzerinde bu id'leri referans alan 'aria-labelledby' veya 'aria-describedby' bulunmalı"
concept_tags: [accessibility, images, standards]
checklist_extra:
  - "SVG elemanına role='img' atanmış mı?"
  - "title ve desc etiketlerinin id değerleri aria-labelledby ile ilişkilendirilmiş mi?"
reference_solution_path: private/solutions/html-medium-standalone-svg-graphic-accessibility.html
hint_ladder:
  1: "Bir SVG elemanının grafik olduğunu yardımcı teknolojilere bildirmek için hangi ARIA rolü atanır?"
  2: "SVG içine erişilebilir başlık ve açıklama ekleyen yerel SVG etiketleri hangileridir?"
  3: "Bu grafik tanımlama yöntemi 'erişilebilir bağımsız SVG grafiği (SVG role img ve aria-labelledby)' olarak bilinir."
```

---

### html-medium-form-custom-validation-pattern

```yaml
id: html-medium-form-custom-validation-pattern
version: 1
language: html
engine: none
difficulty: medium
title: "Düzenli ifade ile özel girdi doğrulaması (pattern ve title)"
prompt: |
  Bir kullanıcı kayıt formunda kullanıcı adı alanının yalnızca 4 ila 16 karakter arasında,
  küçük harf, rakam ve alt çizgi içerecek şekilde sınırlandırılmasını istiyorsunuz. Tarayıcının
  yerel form doğrulama mekanizmasını kullanarak bu kuralı uygulayın ve kullanıcı kurallara
  uymayan bir metin girdiğinde tarayıcının yerel hata baloncuğunda gösterilecek bilgilendirici
  ipucu metnini tanımlayın.
constraints:
  - "<input> elemanında 'pattern' niteliği düzenli ifade (regex) ile tanımlanmalı"
  - "Geçersiz giriş durumunda açıklama sunmak için 'title' niteliği bulunmalı"
  - "Girdi zorunlu olmalı ('required')"
concept_tags: [forms, input-validation, standards]
checklist_extra:
  - "Regex kuralı pattern niteliğine doğru formatta yazılmış mı?"
  - "Hata mesajı rehberliği için title özniteliği açıklayıcı bir metin taşıyor mu?"
reference_solution_path: private/solutions/html-medium-form-custom-validation-pattern.html
hint_ladder:
  1: "HTML girdi alanına özel düzenli ifade (regex) kuralı koymak için hangi nitelik kullanılır?"
  2: "Pattern kuralı ihlal edildiğinde tarayıcı uyarı penceresinde görünen yardım metni hangi nitelikte saklanır?"
  3: "Bu yerel form kontrolü 'düzenli ifade girdi kısıtı (pattern ve title doğrulaması)' olarak bilinir."
```

---

### html-medium-form-error-summary-list

```yaml
id: html-medium-form-error-summary-list
version: 1
language: html
engine: none
difficulty: medium
title: "Erişilebilir form hata özeti bloğu (error summary landmark)"
prompt: |
  Kullanıcı bir başvuru formunu eksik veya hatalı doldurup gönderdiğinde, sayfanın en üstünde
  tüm hataları listeleyen erişilebilir bir 'Hata Özeti' paneli oluşturun. Görme engelli bir
  kullanıcı formu gönderdiğinde odağın doğrudan bu panele aktarılabilmesi için panelin klavye
  ile programatik olarak odaklanabilir olması gerekir. Listedeki her hata maddesi, tıklandığında
  kullanıcıyı doğrudan ilgili hatalı form alanına götüren sayfa içi bağlantılardan oluşmalıdır.
constraints:
  - "Hata özeti kapsayıcısında 'tabindex=\"-1\"' niteliği bulunmalı"
  - "Kapsayıcı 'role=\"alert\"' veya belirgin bir hata başlığı taşımalı"
  - "Hatalar <ul> listesi içinde ve her biri ilgili girdi id'sine işaret eden birer <a> bağlantısı olmalı"
concept_tags: [forms, accessibility, focus]
checklist_extra:
  - "JavaScript ile odaklanabilmesi için hata kutusuna tabindex='-1' verilmiş mi?"
  - "Hata listesindeki bağlantı hedefleri form alanlarının id değerleriyle birebir örtüşüyor mu?"
reference_solution_path: private/solutions/html-medium-form-error-summary-list.html
hint_ladder:
  1: "Bir div elemanını JavaScript odağı (focus) alabilir kılmak için tabindex değeri kaç olmalıdır?"
  2: "Hata özetinden doğrudan hatalı girdi kutusuna atlamak için bağlantı href'inde ne kullanılır?"
  3: "Bu kurumsal erişilebilirlik deseni 'form hata özeti listesi (accessible error summary)' olarak bilinir."
```

---

### html-medium-form-field-error-aria-describedby

```yaml
id: html-medium-form-field-error-aria-describedby
version: 1
language: html
engine: none
difficulty: medium
title: "Hata mesajı ve yardım metni alan ilişkilendirmesi (aria-describedby ve aria-invalid)"
prompt: |
  Bir e-posta giriş alanında hem alanın altında sürekli duran bir yardım ipucu ('Örn: ad@sirket.com')
  hem de doğrulama hatası oluştuğunda görünen bir hata iletisi bulunmaktadır. Ekran okuyucu
  bu girdi kutusuna geldiğinde hem alanın geçersiz durumda olduğunu hem de hem hata metnini
  hem yardım metnini seslendirebilmelidir. Bu ilişkiyi kuran standart WAI-ARIA niteliklerini
  girdi elemanına bağlayın.
constraints:
  - "<input> elemanında 'aria-invalid=\"true\"' niteliği bulunmalı"
  - "Yardım metni ve hata iletisi ayrı id değerlerine sahip olmalı"
  - "Girdinin 'aria-describedby' niteliğinde bu iki id aralarında boşlukla yer almalı"
  - "Standart <label> bağlantısı korunmalı"
concept_tags: [forms, accessibility, input-validation]
checklist_extra:
  - "aria-invalid değeri true olarak işaretlenmiş mi?"
  - "aria-describedby birden fazla id'yi boşlukla birleştirerek kapsıyor mu?"
reference_solution_path: private/solutions/html-medium-form-field-error-aria-describedby.html
hint_ladder:
  1: "Bir form alanının geçersiz değer içerdiğini ekran okuyucuya bildiren nitelik nedir?"
  2: "Bir girdi alanını birden fazla açıklama ve hata metni kutusuna bağlamak için hangi nitelik kullanılır?"
  3: "Bu erişilebilirlik eşleştirmesi 'hata ve açıklama metni ilişkilendirmesi (aria-describedby ve aria-invalid)' olarak bilinir."
```

---

### html-medium-form-required-fields-indication

```yaml
id: html-medium-form-required-fields-indication
version: 1
language: html
engine: none
difficulty: medium
title: "Zorunlu alanların görsel ve anlamsal bildirimi (aria-required ve legend)"
prompt: |
  Bir profil düzenleme formunda bazı alanlar isteğe bağlı iken bazı alanlar zorunludur.
  Formun en başında tüm kullanıcılara zorunlu alanların kırmızı yıldızla (*) işaretlendiğini
  açıklayan bir yönerge yer almalıdır. Zorunlu alanlarda ise hem HTML5 yerel doğrulama kuralı
  hem de yardımcı teknolojilere yönelik bildirim niteliği bulunmalı, görsel yıldız simgesi ise
  ekran okuyuculara gereksiz gürültü yapmaması için dekoratif olarak gizlenmelidir.
constraints:
  - "Zorunlu girdilerde hem 'required' hem de 'aria-required=\"true\"' bulunmalı"
  - "Kırmızı yıldız işareti <span aria-hidden='true'>*</span> şeklinde gizlenmeli"
  - "Form başında zorunlu alan göstergesini açıklayan genel bir bilgilendirme metni yer almalı"
concept_tags: [forms, accessibility, input-validation]
checklist_extra:
  - "Yıldız simgesi aria-hidden='true' ile ekran okuyucudan gizlenmiş mi?"
  - "Girdilerde hem required hem de aria-required yer alıyor mu?"
reference_solution_path: private/solutions/html-medium-form-required-fields-indication.html
hint_ladder:
  1: "Ekran okuyucuya bir form alanının doldurulmasının şart olduğunu açıkça söyleyen ARIA niteliği nedir?"
  2: "Yıldız işaretinin 'yıldız' olarak okunup kafa karıştırmaması için hangi öznitelikle gizlenir?"
  3: "Bu kapsayıcı form bildirimi 'anlamsal zorunlu alan gösterimi (aria-required ve aria-hidden yıldız)' olarak bilinir."
```

---

### html-medium-multi-step-form-progress

```yaml
id: html-medium-multi-step-form-progress
version: 1
language: html
engine: none
difficulty: medium
title: "Çok adımlı form aşama göstergesi (step navigation ve aria-current step)"
prompt: |
  Üç aşamadan oluşan bir rezervasyon sürecinde (1. Kişisel Bilgiler, 2. Ödeme Seçenekleri,
  3. Onay) sayfanın en üstünde kullanıcının kaçıncı adımda olduğunu gösteren bir adım
  çubuğu (stepper) hazırlayın. Aşama listesini sıralı bir liste olarak kurun ve o anda
  aktif olan ikinci adımı ekran okuyucu kullanıcılarına adım aşaması olarak net biçimde
  duyuracak standart ARIA niteliğini tanımlayın.
constraints:
  - "<nav aria-label='...'> kapsayıcısı içinde bir <ol> sıralı liste kullanılmalı"
  - "Aktif adım öğesinde 'aria-current=\"step\"' niteliği bulunmalı"
  - "Her adım metni anlaşılır ve sıralı olmalı"
concept_tags: [navigation, accessibility, forms]
checklist_extra:
  - "aria-current niteliğinin değeri 'step' olarak atanmış mı?"
  - "Adımların ardışık olduğunu belirtmek için sıralı liste (ol) kullanılmış mı?"
reference_solution_path: private/solutions/html-medium-multi-step-form-progress.html
hint_ladder:
  1: "Çok adımlı bir süreçte bulunulan aktif aşamayı belirtmek için aria-current hangi değeri alır?"
  2: "Aşama adımlarının sırasını semantik olarak temsil eden liste etiketi hangisidir?"
  3: "Bu navigasyon göstergesi 'çok adımlı form aşama bildirimi (stepper aria-current step)' olarak bilinir."
```

---

### html-medium-details-accordion-name-attribute

```yaml
id: html-medium-details-accordion-name-attribute
version: 1
language: html
engine: none
difficulty: medium
title: "Birbirini kapatan özel akordeon grubu (details name özniteliği)"
prompt: |
  Bir web sitesinin yardım merkezinde 3 maddelik sıkça sorulan sorular bölümü hazırlıyorsunuz.
  Kullanıcı bir sorunun cevabını açtığında, daha önce açık olan diğer sorunun hiçbir JavaScript
  kodu yazılmadan otomatik olarak kendiliğinden kapanmasını istiyorsunuz. Modern HTML standardında
  aynı gruba ait detay kutularını birbirine bağlayarak tek seferde yalnızca birinin açık kalmasını
  sağlayan yerel özniteliği kullanın.
constraints:
  - "En az üç adet <details> ve <summary> bloğu bulunmalı"
  - "Tüm <details> elemanlarında ortak bir 'name' niteliği değeri paylaşılmalı"
  - "Sorular ve cevap metinleri anlamsal olarak yapılandırılmalı"
concept_tags: [semantics, accessibility, standards]
checklist_extra:
  - "Tüm details elemanları aynı name değerine sahip mi?"
  - "Her detayın bir summary başlığı bulunuyor mu?"
reference_solution_path: private/solutions/html-medium-details-accordion-name-attribute.html
hint_ladder:
  1: "Açılır kapanır panellerin tek bir grup gibi davranması için HTML standardına yeni eklenen nitelik nedir?"
  2: "Radyo butonlarındaki gibi details elemanlarını gruplayan öznitelik hangisidir?"
  3: "Bu yerel akordeon özelliği 'bağlantılı detay grubu (details name özniteliği)' olarak bilinir."
```

---

### html-medium-meter-disk-quota-gauge

```yaml
id: html-medium-meter-disk-quota-gauge
version: 1
language: html
engine: none
difficulty: medium
title: "Depolama kotası anlamsal göstergesi (meter elemanı ve eşik değerleri)"
prompt: |
  Bir bulut depolama kontrol panelinde kullanıcının disk kullanımını (örneğin 100 GB kotanın
  82 GB'ı dolu) görsel ve anlamsal olarak sunan bir gösterge hazırlayın. Belirli sınırlar
  içindeki bilinen bir büyüklüğü ölçen HTML elemanını kullanın. Kritik eşik değerlerini
  (düşük, yüksek, optimum) tanımlayın ve ekran okuyucuların bu değeri net algılayabilmesi için
  göstergeyi bir etiket ile bağlayın.
constraints:
  - "<meter> elemanı kullanılmalı"
  - "'min', 'max', 'value' değerleri eksiksiz girilmeli"
  - "'low', 'high' ve 'optimum' sınır değerleri tanımlanmalı"
  - "Göstergeye bağlı bir <label> veya erişilebilir metin bulunmalı"
concept_tags: [semantics, accessibility, standards]
checklist_extra:
  - "progress yerine sabit kapasite ölçümü için meter etiketi tercih edilmiş mi?"
  - "Eşik sınırları sayısal olarak mantıklı bir düzende mi?"
reference_solution_path: private/solutions/html-medium-meter-disk-quota-gauge.html
hint_ladder:
  1: "Belli bir kapasite veya kota içerisindeki mevcut ölçümü anlamsal olarak göstermek için hangi etiket kullanılır?"
  2: "Bu ölçüm elemanında uyarı seviyelerini belirlemek için hangi sınır nitelikleri kullanılır?"
  3: "Bu anlamsal grafik bileşeni 'skaler ölçüm göstergesi (meter elemanı)' olarak bilinir."
```

---

### html-medium-progress-file-upload-status

```yaml
id: html-medium-progress-file-upload-status
version: 1
language: html
engine: none
difficulty: medium
title: "Dinamik dosya yükleme ilerleme çubuğu (progress ve canlı durum)"
prompt: |
  Bir dosya paylaşım sitesinde devam eden bir dosya yükleme işleminin yüzdesini (%65)
  temsil eden bir ilerleme bileşeni kurun. Süreç devam ettiği için bu amaçla özel
  tasarlanmış HTML5 ilerleme elemanını kullanın. Ekran okuyucu kullanıcılarının hem
  görsel çubuğu hem de yanında yazan metinsel yüzdeyi rahatça takip edebilmesi için
  bileşeni erişilebilir bir etiketle ilişkilendirin.
constraints:
  - "<progress> elemanı kullanılmalı"
  - "'value' ve 'max' nitelikleri sayısal olarak tanımlanmalı"
  - "İlerleme çubuğunu tanımlayan bir <label> veya açıklama bulunmalı"
  - "Eski tarayıcılar için eleman içinde metinsel yedek yüzde yer almalı"
concept_tags: [semantics, accessibility, standards]
checklist_extra:
  - "Tamamlanma süreci için meter yerine progress etiketi kullanılmış mı?"
  - "Erişilebilir bir etiket veya açıklama ile ilişkilendirilmiş mi?"
reference_solution_path: private/solutions/html-medium-progress-file-upload-status.html
hint_ladder:
  1: "Bir görevin tamamlanma durumunu ve yüzdesini gösteren standart HTML5 etiketi hangisidir?"
  2: "İlerleme çubuğunun mevcut durumunu ve tavan değerini belirten nitelikler nelerdir?"
  3: "Bu görev tamamlama bileşeni 'anlamsal ilerleme çubuğu (progress elemanı)' olarak bilinir."
```

---

### html-medium-table-column-group-styling

```yaml
id: html-medium-table-column-group-styling
version: 1
language: html
engine: none
difficulty: medium
title: "Tablo sütun grubu ve yapısal biçimlendirme (colgroup ve col)"
prompt: |
  Bir e-ticaret karşılaştırma tablosunda ilk sütun ürün özelliklerini listelerken, sonraki
  üç sütun farklı paket fiyatlarını içermektedir. CSS ile sütun genişliklerini ve arka planlarını
  her hücreye tek tek sınıf yazmadan sütun bazında topluca yönetebilmek için tablonun
  başında sütunları mantıksal gruplara ayıran standart HTML tablo elemanlarını tanımlayın.
constraints:
  - "<colgroup> elemanı kullanılmalı"
  - "İçerisinde sütunları temsil eden <col> etiketleri bulunmalı"
  - "'span' niteliği ile birden çok sütunu kapsayan en az bir tanım yer almalı"
  - "Sütunlara amaca uygun sınıf (class) adları atanmalı"
concept_tags: [tables, semantics, standards]
checklist_extra:
  - "colgroup elemanı thead veya tbody'den önce mi yerleştirilmiş?"
  - "span niteliği doğru sütun sayısını temsil ediyor mu?"
reference_solution_path: private/solutions/html-medium-table-column-group-styling.html
hint_ladder:
  1: "Bir tablonun sütunlarını topluca tanımlamak ve stil uygulamak için hangi etiket kullanılır?"
  2: "Bir sütun tanımının yan yana birden fazla sütunu kapsamasını sağlayan nitelik nedir?"
  3: "Bu tablo mimarisi 'sütun grubu yapılandırması (colgroup ve col span)' olarak bilinir."
```

---

### html-medium-table-sortable-header-marking

```yaml
id: html-medium-table-sortable-header-marking
version: 1
language: html
engine: none
difficulty: medium
title: "Sıralanabilir veri tablosu başlığı (aria-sort ve sıralama butonu)"
prompt: |
  Bir kullanıcı listesi tablosunda 'Kullanıcı Adı' ve 'Kayıt Tarihi' sütun başlıklarına
  tıklandığında sıralama yapılabilmektedir. Şu anda tablo 'Kayıt Tarihi' sütununa göre
  artan (küçükten büyüğe) sıralanmış durumdadır. Bu durumu görme engelli kullanıcılara
  aktarabilmek için WAI-ARIA tablo sıralama niteliğini ve başlık hücresi içine yerleştirilmiş
  erişilebilir sıralama butonunu kurgulayın.
constraints:
  - "Aktif sıralanan <th> üzerinde 'aria-sort=\"ascending\"' niteliği bulunmalı"
  - "Diğer sıralanabilir sütunda 'aria-sort=\"none\"' bulunmalı"
  - "Başlık hücrelerinin içinde etkileşimi tetikleyen <button> elemanı bulunmalı"
concept_tags: [tables, accessibility, focus]
checklist_extra:
  - "aria-sort özniteliği buton yerine doğrudan th hücresine mi atanmış?"
  - "Aktif sıralama yönü ascending veya descending olarak doğru belirtilmiş mi?"
reference_solution_path: private/solutions/html-medium-table-sortable-header-marking.html
hint_ladder:
  1: "Ekran okuyucuya bir tablo sütununun küçükten büyüğe sıralı olduğunu bildiren ARIA niteliği nedir?"
  2: "Klavye erişilebilirliği için th başlığı içine hangi tıklanabilir eleman konulmalıdır?"
  3: "Bu tablo standardı 'erişilebilir sıralanabilir sütun başlığı (th aria-sort)' olarak bilinir."
```

---

### html-medium-semantic-card-component

```yaml
id: html-medium-semantic-card-component
version: 1
language: html
engine: none
difficulty: medium
title: "Anlamsal makale kartı bileşeni (article, figure ve time)"
prompt: |
  Bir blog ana sayfasında en son yazıları sergileyen bir makale kartı (card) tasarlayın.
  Tasarım bir görsel, kategori rozeti, yazı başlığı, yayınlanma tarihi, kısa bir özet
  ve 'Devamını Oku' bağlantısı içermelidir. Tüm bu parçaları div çorbasına dönüştürmeden,
  tamamen anlamsal HTML5 etiketleri (bağımsız içerik, görsel kapsayıcısı, makinece okunabilir
  tarih) kullanarak yapılandırın.
constraints:
  - "Kart kapsayıcısı olarak <article> kullanılmalı"
  - "Görsel <figure> içinde yer almalı"
  - "Yayın tarihi makine tarafından okunabilir datetime niteliğine sahip bir <time> elemanı olmalı"
  - "Kartın birincil başlığı uygun bir başlık etiketi (<h3> vb.) olmalı"
concept_tags: [semantics, images, links]
checklist_extra:
  - "Tarih elemanında ISO 8601 uyumlu datetime özniteliği var mı?"
  - "Kart bağımsız bir article olarak kurgulanmış mı?"
reference_solution_path: private/solutions/html-medium-semantic-card-component.html
hint_ladder:
  1: "Bağımsız olarak yeniden dağıtılabilir bir kart veya makaleyi sarmak için hangi etiket kullanılır?"
  2: "Tarih bilgisini hem insan hem de arama botları için anlaşılır kılan HTML5 etiketi hangisidir?"
  3: "Bu anlamsal bileşen 'bağımsız içerik kartı (article, figure ve time)' olarak bilinir."
```

---

### html-medium-semantic-author-bio-section

```yaml
id: html-medium-semantic-author-bio-section
version: 1
language: html
engine: none
difficulty: medium
title: "Yazar biyografisi ve iletişim bilgileri bölümü (address ve rel author)"
prompt: |
  Bir haber makalesinin sonunda, makaleyi kaleme alan yazarın fotoğrafı, adı, e-posta
  adresi ve profil sayfası bağlantısını içeren bir yazar künyesi hazırlayın. HTML
  standartlarında bir makalenin veya sitenin yazarının iletişim bilgilerini belirtmek
  için tanımlanmış özel iletişim etiketini kullanın ve yazarın profil sayfasına giden
  köprüye anlamsal ilişki belirtecini ekleyin.
constraints:
  - "Yazar iletişim bilgileri <address> etiketi içinde yapılandırılmalı"
  - "Yazar profiline giden bağlantıda 'rel=\"author\"' niteliği bulunmalı"
  - "E-posta için 'mailto:' şemalı bir bağlantı yer almalı"
concept_tags: [semantics, links, standards]
checklist_extra:
  - "İletişim bilgileri için address etiketi kullanılmış mı?"
  - "Yazar bağlantısına rel='author' ilişkisi verilmiş mi?"
reference_solution_path: private/solutions/html-medium-semantic-author-bio-section.html
hint_ladder:
  1: "Bir sayfanın veya makalenin yazarının iletişim bilgilerini sarmak için hangi HTML etiketi kullanılır?"
  2: "Bir bağlantının makale yazarına ait olduğunu arama motorlarına bildiren rel değeri nedir?"
  3: "Bu anlamsal yazar yapısı 'iletişim künyesi ve yazar ilişkisi (address ve rel author)' olarak bilinir."
```

---

### html-medium-meta-open-graph-social-sharing

```yaml
id: html-medium-meta-open-graph-social-sharing
version: 1
language: html
engine: none
difficulty: medium
title: "Sosyal medya paylaşım kartı meta etiketleri (Open Graph)"
prompt: |
  Web sitenizdeki bir ürün sayfasının bağlantısı Facebook, WhatsApp, LinkedIn veya Slack gibi
  platformlarda paylaşıldığında zengin bir önizleme kartı (başlık, görsel, açıklama, sayfa URL'si
  ve içerik türü) olarak görüntülenmesini istiyorsunuz. Bu platformların okuduğu resmi Open Graph
  protokolü meta etiketlerini sayfanın `<head>` bölümüne yerleştirin.
constraints:
  - "'property=\"og:title\"' meta etiketi bulunmalı"
  - "'property=\"og:description\"' meta etiketi bulunmalı"
  - "'property=\"og:image\"' meta etiketi bulunmalı"
  - "'property=\"og:url\"' ve 'property=\"og:type\"' meta etiketleri bulunmalı"
concept_tags: [standards, performance, links]
checklist_extra:
  - "Meta etiketlerinde name yerine property özniteliği kullanılmış mı?"
  - "Tüm og:* alanları geçerli content değerlerine sahip mi?"
reference_solution_path: private/solutions/html-medium-meta-open-graph-social-sharing.html
hint_ladder:
  1: "Sosyal ağlarda paylaşılan linklerin zengin kart olarak görünmesini sağlayan protokolün adı nedir?"
  2: "Open Graph etiketlerinde nitelik anahtarı olarak name yerine ne yazılır?"
  3: "Bu standart meta protokolü 'açık grafik sosyal paylaşım etiketleri (Open Graph meta)' olarak bilinir."
```

---

### html-medium-meta-twitter-cards

```yaml
id: html-medium-meta-twitter-cards
version: 1
language: html
engine: none
difficulty: medium
title: "X ve Twitter paylaşım önizleme kartları (twitter meta etiketleri)"
prompt: |
  Bir teknoloji haber portalında yayınlanan makalelerin X (Twitter) üzerinde paylaşıldığında
  büyük görsel formatında (summary_large_image) çarpıcı bir kart şeklinde belirmesini istiyorsunuz.
  Platformun ihtiyaç duyduğu kart türü, site hesabı, başlık, açıklama ve önizleme görseli
  bilgilerini içeren standart meta etiketlerini `<head>` bölümünde kurgulayın.
constraints:
  - "<meta name='twitter:card' content='summary_large_image'> tanımlanmalı"
  - "'twitter:title' ve 'twitter:description' etiketleri yer almalı"
  - "'twitter:image' etiketi bulunmalı"
concept_tags: [standards, links, images]
checklist_extra:
  - "Kart tipi olarak summary_large_image belirtilmiş mi?"
  - "Meta etiketlerinde name='twitter:*' formatı kullanılmış mı?"
reference_solution_path: private/solutions/html-medium-meta-twitter-cards.html
hint_ladder:
  1: "X/Twitter için büyük görselli paylaşım kartı oluşturan twitter:card değeri nedir?"
  2: "Twitter önizleme etiketlerinde nitelik tanımlayıcısı olarak ne kullanılır?"
  3: "Bu sosyal platform standardı 'Twitter önizleme kartı etiketleri (twitter card meta)' olarak bilinir."
```

---

### html-medium-meta-canonical-url

```yaml
id: html-medium-meta-canonical-url
version: 1
language: html
engine: none
difficulty: medium
title: "Yinelenen içerik ve yetkili URL bildirimi (canonical link)"
prompt: |
  Bir e-ticaret sitesinde aynı ürün hem kategori sayfalarından farklı URL parametreleriyle
  (örn: ?ref=search, ?color=blue) hem de sade bir URL ile açılabilmektedir. Arama motorlarının
  bu yinelenen (duplicate) sayfaları tek bir ana sayfa altında puanlaması ve arama sonuçlarında
  yalnızca ana ürün bağlantısını göstermesi için sayfanın `<head>` bölümüne standart yetkili
  bağlantı bildirimini ekleyin.
constraints:
  - "<link rel='canonical' href='...'> etiketi kullanılmalı"
  - "Href değeri tam (mutlak/absolute) URL yapısında olmalı"
  - "Etiket <head> elemanı içine yerleştirilmeli"
concept_tags: [standards, links, performance]
checklist_extra:
  - "rel değeri canonical olarak belirtilmiş mi?"
  - "Href değeri mutlak bir URL içeriyor mu?"
reference_solution_path: private/solutions/html-medium-meta-canonical-url.html
hint_ladder:
  1: "Arama motorlarına bir sayfanın orijinal/yetkili URL'sini gösteren link ilişkisi nedir?"
  2: "Bu link etiketinin rel değerine hangi İngilizce kelime yazılır?"
  3: "Bu SEO standardı 'yetkili URL referans bildirimi (canonical link)' olarak bilinir."
```

---

### html-medium-resource-hints-preconnect-dns-prefetch

```yaml
id: html-medium-resource-hints-preconnect-dns-prefetch
version: 1
language: html
engine: none
difficulty: medium
title: "Harici kaynaklar için ağ bağlantı ipuçları (preconnect ve dns-prefetch)"
prompt: |
  Web siteniz yazı tiplerini Google Fonts gibi harici bir CDN üzerinden, ürün görsellerini ise
  başka bir statik medya sunucusundan çekmektedir. Tarayıcının bu kritik harici sunucularla
  henüz CSS dosyaları indirilmeden önce DNS çözümlemesini, TCP el sıkışmasını ve TLS müzakeresini
  erkenden başlatması için `<head>` içine iki seviyeli bağlantı ipucu etiketlerini ekleyin.
constraints:
  - "Kritik yazı tipi CDN'i için '<link rel=\"preconnect\" href=\"...\" crossorigin>' tanımlanmalı"
  - "Yedek veya ikincil kaynak için '<link rel=\"dns-prefetch\" href=\"...\">' yer almalı"
  - "Tüm ipuçları <head> bölümünde yer almalı"
concept_tags: [performance, standards, links]
checklist_extra:
  - "preconnect etiketinde yazı tipleri için crossorigin niteliği unutulmamış mı?"
  - "dns-prefetch bağlantı ipucu doğru rel değeriyle eklenmiş mi?"
reference_solution_path: private/solutions/html-medium-resource-hints-preconnect-dns-prefetch.html
hint_ladder:
  1: "Tarayıcıya bir dış etki alanına erkenden soket açmasını ve TLS bağlantısı kurmasını söyleyen rel değeri nedir?"
  2: "Yalnızca alan adı DNS çözümlemesini erkenden yaptırmak için hangi rel değeri kullanılır?"
  3: "Bu performans optimizasyonu 'erken ağ bağlantı ipuçları (preconnect ve dns-prefetch)' olarak bilinir."
```

---

### html-medium-resource-hints-preload-critical-font

```yaml
id: html-medium-resource-hints-preload-critical-font
version: 1
language: html
engine: none
difficulty: medium
title: "Kritik web yazı tipi ön yüklemesi (link rel preload font)"
prompt: |
  Sayfa açılışında metinlerin parlayıp sonradan değişmesini (FOUT) engellemek ve en büyük içerikli
  boyama (LCP) süresini iyileştirmek istiyorsunuz. Sayfanın en üst başlığında kullanılan birincil
  WOFF2 yazı tipi dosyasının, CSS dosyası çözümlenmeyi beklemeden en yüksek öncelikle tarayıcı
  tarafından derhal indirilmeye başlanmasını sağlayacak kaynak ön yükleme etiketini yazın.
constraints:
  - "<link rel='preload' ...> etiketi kullanılmalı"
  - "'as=\"font\"' ve 'type=\"font/woff2\"' nitelikleri bulunmalı"
  - "Yazı tiplerinde tarayıcı CORS zorunluluğu nedeniyle 'crossorigin' niteliği mutlaka yer almalı"
concept_tags: [performance, standards, links]
checklist_extra:
  - "as niteliği 'font' olarak doğru atanmış mı?"
  - "Yazı tiplerinde zorunlu olan crossorigin niteliği eklenmiş mi?"
reference_solution_path: private/solutions/html-medium-resource-hints-preload-critical-font.html
hint_ladder:
  1: "Kritik bir kaynağın sayfa oluşturulurken en başta indirilmesini sağlayan rel değeri nedir?"
  2: "Yazı tipi ön yüklemelerinde dosya türünü tarayıcıya bildiren 'as' değeri nedir?"
  3: "Bu kaynak optimizasyonu 'kritik yazı tipi ön yüklemesi (preload as font)' olarak bilinir."
```

---

### html-medium-form-file-upload-restrictions

```yaml
id: html-medium-form-file-upload-restrictions
version: 1
language: html
engine: none
difficulty: medium
title: "Kısıtlamalı ve çoklu dosya yükleme alanı (file accept ve multiple)"
prompt: |
  Bir iş başvuru formunda adayların özgeçmiş ve sertifikalarını yükleyeceği bir dosya yükleme
  alanı tasarlayın. Kullanıcıların yalnızca PDF belgelerini ve Word dokümanlarını seçebilmesi
  için dosya seçim penceresini mime tipleri ve uzantılarla filtreleyin. Kullanıcının aynı anda
  birden çok dosya seçebilmesini sağlayın ve hemen altında izin verilen formatları belirten
  erişilebilir bir yardım açıklaması ilişkilendirin.
constraints:
  - "<input type='file'> elemanı kullanılmalı"
  - "'accept' niteliğinde PDF ve Word MIME/uzantı türleri tanımlanmalı"
  - "Birden fazla dosya seçimi için 'multiple' boolean niteliği bulunmalı"
  - "Açıklayıcı bir yardım metni 'aria-describedby' ile girdi alanına bağlanmalı"
concept_tags: [forms, input-validation, accessibility]
checklist_extra:
  - "accept niteliğinde izin verilen uzantılar virgülle ayrılmış mı?"
  - "Birden fazla dosya seçilebilmesi için multiple niteliği eklenmiş mi?"
reference_solution_path: private/solutions/html-medium-form-file-upload-restrictions.html
hint_ladder:
  1: "Dosya yükleme kutusunda seçilebilecek dosya türlerini kısıtlayan nitelik hangisidir?"
  2: "Kullanıcının tek seferde birden fazla dosya seçmesini sağlayan öznitelik nedir?"
  3: "Bu form denetimi 'kısıtlamalı çoklu dosya yükleme (input file accept ve multiple)' olarak bilinir."
```

---

### html-medium-form-datalist-autocomplete-search

```yaml
id: html-medium-form-datalist-autocomplete-search
version: 1
language: html
engine: none
difficulty: medium
title: "Öneri listeli serbest metin arama alanı (datalist entegrasyonu)"
prompt: |
  Bir seyahat portalında kalkış şehri seçimi için bir metin kutusu hazırlayın. Kullanıcı
  hem listede olmayan serbest bir şehir adı yazabilmeli hem de klavyeden yazmaya başladığında
  altında popüler şehir seçenekleri (İstanbul, Ankara, İzmir, Antalya) otomatik öneri olarak
  listelenmelidir. Bu yerel otomatik tamamlama listesini JavaScript kütüphanesi kullanmadan
  HTML5 standart elemanlarıyla kurun.
constraints:
  - "<input type='text' list='cities-list'> şeklinde 'list' niteliği bulunmalı"
  - "<datalist id='cities-list'> elemanı ile eşleşmeli"
  - "Datalist içinde en az dört adet <option> önerisi bulunmalı"
  - "Girdinin bağlı bir <label> etiketi bulunmalı"
concept_tags: [forms, input-validation, accessibility]
checklist_extra:
  - "input üzerindeki list niteliği ile datalist id değeri eşleşiyor mu?"
  - "Select yerine serbest yazıma izin veren datalist yapısı kurulmuş mu?"
reference_solution_path: private/solutions/html-medium-form-datalist-autocomplete-search.html
hint_ladder:
  1: "Girdi alanlarına yerel otomatik öneri listesi sunan HTML5 etiketi hangisidir?"
  2: "Bir input elemanını bu öneri listesine bağlayan nitelik nedir?"
  3: "Bu yerel form bileşeni 'otomatik öneri veri listesi (datalist ve input list)' olarak bilinir."
```

---

### html-medium-accessible-toggle-switch

```yaml
id: html-medium-accessible-toggle-switch
version: 1
language: html
engine: none
difficulty: medium
title: "Erişilebilir iki durumlu açma/kapama anahtarı (role switch)"
prompt: |
  Bir profil ayarları sayfasında 'Karanlık Mod' veya 'E-posta Bildirimleri' seçeneğini
  açıp kapatmak için görsel olarak modern bir sürgü (toggle switch) tasarlıyorsunuz.
  Yardımcı teknolojilerin bu bileşeni sıradan bir buton gibi değil, açık veya kapalı
  durumu olan iki durumlu bir anahtar (switch) olarak algılamasını sağlayın. Anahtarın
  o anki aktif/pasif durumunu aktaran standart ARIA niteliğini ekleyin.
constraints:
  - "<button role='switch' ...> elemanı kullanılmalı"
  - "Mevcut durumu bildiren 'aria-checked=\"false\"' veya 'aria-checked=\"true\"' yer almalı"
  - "Bileşenin görünen bir etiketi veya 'aria-label' açıklaması bulunmalı"
concept_tags: [accessibility, focus, forms]
checklist_extra:
  - "Anahtar rolü olarak 'switch' atanmış mı?"
  - "Durum göstergesi olarak aria-checked niteliği kullanılmış mı?"
reference_solution_path: private/solutions/html-medium-accessible-toggle-switch.html
hint_ladder:
  1: "Bir elemanın iki durumlu açma/kapama sürgüsü olduğunu bildiren ARIA rolü nedir?"
  2: "Anahtarın açık veya kapalı olduğunu belirtmek için hangi ARIA durumu kullanılır?"
  3: "Bu arayüz bileşeni 'erişilebilir durum anahtarı (role switch ve aria-checked)' olarak bilinir."
```

---

### html-medium-accessible-menu-button-dropdown

```yaml
id: html-medium-accessible-menu-button-dropdown
version: 1
language: html
engine: none
difficulty: medium
title: "Açılır menü tetikleyici butonu ve menü yapısı (aria-haspopup ve menu)"
prompt: |
  Bir web uygulamasında kullanıcının hesap ayarları ve çıkış seçeneklerine ulaştığı bir
  açılır profil menüsü kurguluyorsunuz. Menüyü açan butona odaklanan bir ekran okuyucu
  kullanıcısı, bu butona tıklandığında bir alt menünün açılacağını ve menünün o anda açık mı
  kapalı mı olduğunu bilmelidir. Buton ile altındaki menü listesi arasındaki ARIA rol ve
  durum ilişkilerini kurun.
constraints:
  - "Tetikleyici butonda 'aria-haspopup=\"menu\"' veya 'aria-haspopup=\"true\"' bulunmalı"
  - "Butonda menünün durumunu belirten 'aria-expanded=\"false\"' yer almalı"
  - "Açılan liste '<ul role=\"menu\">' ve elemanları '<li role=\"none\">' veya '<a role=\"menuitem\">' olmalı"
concept_tags: [accessibility, navigation, focus]
checklist_extra:
  - "aria-haspopup niteliği butona tanımlanmış mı?"
  - "Menü maddeleri için menuitem rolleri uygulanmış mı?"
reference_solution_path: private/solutions/html-medium-accessible-menu-button-dropdown.html
hint_ladder:
  1: "Bir butonun bir açılır menü tetiklediğini belirten ARIA niteliği hangisidir?"
  2: "Açılır menünün şu an açık olup olmadığını hangi boolean ARIA niteliği söyler?"
  3: "Bu navigasyon bileşeni 'erişilebilir menü butonu deseni (menu button aria-haspopup)' olarak bilinir."
```

---

### html-medium-accessible-tooltip-anchor

```yaml
id: html-medium-accessible-tooltip-anchor
version: 1
language: html
engine: none
difficulty: medium
title: "Erişilebilir ipucu balonu ilişkilendirmesi (role tooltip ve aria-describedby)"
prompt: |
  Bir kontrol panelindeki 'İstatistikleri Yenile' butonunun üzerine gelindiğinde veya klavye ile
  odaklanıldığında beliren özel bir ipucu balonu (tooltip) yer almaktadır. Bu ipucunun yalnızca
  fare kullanıcılarına değil, klavye ile gezen veya ekran okuyucu kullanan kullanıcılara da
  aktarılabilmesi için buton ile ipucu kutusunu WAI-ARIA standartlarında birbirine bağlayın.
constraints:
  - "İpucu balonu üzerinde 'role=\"tooltip\"' ve benzersiz bir 'id' bulunmalı"
  - "Tetikleyici butonda ipucuna işaret eden 'aria-describedby' bulunmalı"
  - "İpucu balonu varsayılan olarak gizlenebilir yapıda olmalı"
concept_tags: [accessibility, focus, standards]
checklist_extra:
  - "İpucu elemanına rol olarak tooltip verilmiş mi?"
  - "aria-describedby ile buton ve ipucu id'si eşleştirilmiş mi?"
reference_solution_path: private/solutions/html-medium-accessible-tooltip-anchor.html
hint_ladder:
  1: "Ek bilgi veren baloncuklara hangi WAI-ARIA rolü atanır?"
  2: "Butona odaklanıldığında bu baloncuğun okunmasını sağlayan ilişkilendirme niteliği nedir?"
  3: "Bu erişilebilirlik bağlantısı 'erişilebilir ipucu balonu (role tooltip ve aria-describedby)' olarak bilinir."
```

---

### html-medium-tabindex-modal-focus-trap

```yaml
id: html-medium-tabindex-modal-focus-trap
version: 1
language: html
engine: none
difficulty: medium
title: "Programatik odaklanabilir panel kapsayıcısı (tabindex eksi bir)"
prompt: |
  Özel bir yan panel (off-canvas drawer) veya uyarı kutusu açıldığında, JavaScript ile
  kullanıcının klavye odağını doğrudan bu panel kapsayıcısının kendisine taşımak istiyorsunuz.
  Kapsayıcı normalde Tab tuşu ile gezinirken sekme sırasına girmemeli, ancak kod tarafında
  element.focus() çağrıldığında odağı kabul edebilmelidir. Bu odak yönetimini sağlayan
  HTML niteliğini ve anlamsal dialog rolünü uygulayın.
constraints:
  - "Panel kapsayıcısında 'tabindex=\"-1\"' niteliği bulunmalı"
  - "Kapsayıcıda 'role=\"dialog\"' veya 'role=\"region\"' ve 'aria-labelledby' bulunmalı"
  - "İçerisinde başlık ve odaklanılabilir en az bir kapatma butonu yer almalı"
concept_tags: [focus, accessibility, dialogs]
checklist_extra:
  - "tabindex değeri tam olarak -1 olarak atanmış mı?"
  - "Panel bir başlığa aria-labelledby ile bağlanmış mı?"
reference_solution_path: private/solutions/html-medium-tabindex-modal-focus-trap.html
hint_ladder:
  1: "Bir etiketin klavye sekme sırasına girmeden yalnızca script ile odaklanabilmesini sağlayan tabindex değeri nedir?"
  2: "Panelin başlığını ekran okuyucuya modal ismi olarak tanıtmak için hangi nitelik kullanılır?"
  3: "Bu odak yönetimi tekniği 'programatik odak hedefi (tabindex -1 odaklanabilir kapsayıcı)' olarak bilinir."
```

---

### html-medium-link-download-attribute

```yaml
id: html-medium-link-download-attribute
version: 1
language: html
engine: none
difficulty: medium
title: "Doğrudan dosya indirme köprüsü (a download niteliği)"
prompt: |
  Bir web sitesinin kaynaklar sayfasında kullanıcıların '2024 Faaliyet Raporu' PDF belgesini
  tarayıcı sekmesinde görüntülemek yerine doğrudan bilgisayarlarına indirmelerini istiyorsunuz.
  Kullanıcı bağlantıya tıkladığında tarayıcının indirme penceresini başlatmasını ve indirilen
  dosyanın varsayılan adını 'sirket-faaliyet-raporu-2024.pdf' olarak belirlemesini sağlayan
  HTML köprü niteliğini kullanın.
constraints:
  - "<a> köprüsünde 'download' niteliği bulunmalı"
  - "Download niteliğinde hedef dosya adı ('sirket-faaliyet-raporu-2024.pdf') tanımlanmalı"
  - "Href değeri indirilecek dosya yoluna işaret etmeli"
  - "Bağlantı metni dosyanın indirileceğini ve formatını açıkça belirtmeli"
concept_tags: [links, standards, accessibility]
checklist_extra:
  - "download niteliğine önerilen dosya adı atanmış mı?"
  - "Bağlantı metni görme engelliler için dosya türünü açıkça ifade ediyor mu?"
reference_solution_path: private/solutions/html-medium-link-download-attribute.html
hint_ladder:
  1: "Bir bağlantıya tıklandığında hedefin yeni sekmede açılmayıp indirilmesini sağlayan nitelik nedir?"
  2: "İndirilen dosyaya özel bir kayıt ismi vermek için bu niteliğe ne yazılır?"
  3: "Bu indirme yönlendirmesi 'köprü dosya indirme niteliği (anchor download)' olarak bilinir."
```

---

### html-medium-secure-external-link-target

```yaml
id: html-medium-secure-external-link-target
version: 1
language: html
engine: none
difficulty: medium
title: "Güvenli harici sekme açma bağlantısı (target blank ve rel noopener noreferrer)"
prompt: |
  Kullanıcıları sitenizden harici bir iş ortağının web sitesine yeni bir tarayıcı sekmesinde
  yönlendiren bir köprü oluşturun. Açılan yeni sayfanın, JavaScript üzerinden pencere nesnesine
  (window.opener) erişerek kaynak sayfanızı zararlı bir adrese yönlendirmesini (reverse tabnabbing)
  ve yönlendiren sayfa referans bilgilerini çalmasını engelleyen güvenlik ilişkilerini tanımlayın.
constraints:
  - "'target=\"_blank\"' niteliği bulunmalı"
  - "'rel=\"noopener noreferrer\"' niteliği eksiksiz yer almalı"
  - "Bağlantı metninde veya ekran okuyucu etiketinde bağlantının yeni sekmede açılacağı belirtilmeli"
concept_tags: [security, links, standards]
checklist_extra:
  - "rel niteliğinde hem noopener hem de noreferrer yer alıyor mu?"
  - "Yeni sekmede açılacağı bilgisi ekran okuyucular için belirtilmiş mi?"
reference_solution_path: private/solutions/html-medium-secure-external-link-target.html
hint_ladder:
  1: "target='_blank' kullanılan bağlantılarda yeni sayfanın ana sayfaya erişimini kesen rel değeri nedir?"
  2: "Referans gönderici bilgilerini gizleyen rel parametresi hangisidir?"
  3: "Bu güvenlik kuralı 'güvenli harici sekme bağlantısı (rel noopener noreferrer)' olarak bilinir."
```

---

### html-medium-figure-code-snippet-caption

```yaml
id: html-medium-figure-code-snippet-caption
version: 1
language: html
engine: none
difficulty: medium
title: "Başlıklı ve açıklamalı kod bloğu figürü (figure, figcaption ve pre code)"
prompt: |
  Bir yazılım eğitim dokümanında örnek bir Python kod parçasını açıklayan anlamsal bir blok
  oluşturun. Kod bloğunun üzerinde veya altında 'Örnek 1: Fibonacci Algoritması' şeklinde
  resmi bir başlık yer almalıdır. Blok hem metinsel düzeni ve boşlukları korumalı hem de
  kod içeriği olduğunu anlamsal olarak tarayıcıya bildirmelidir.
constraints:
  - "<figure> kapsayıcısı kullanılmalı"
  - "Blok başlığı için <figcaption> etiketi bulunmalı"
  - "Kod parçası <pre><code>...</code></pre> iç içe yapısıyla sunulmalı"
  - "Kod bloğu için programlama dili sınıfı (class='language-python') belirtilmeli"
concept_tags: [semantics, standards, accessibility]
checklist_extra:
  - "figcaption figürün ilk veya son elemanı olarak konumlandırılmış mı?"
  - "pre ve code etiketleri doğru hiyerarşide iç içe yerleştirilmiş mi?"
reference_solution_path: private/solutions/html-medium-figure-code-snippet-caption.html
hint_ladder:
  1: "Görsel, şema veya kod bloklarını başlığıyla birlikte sarmak için hangi anlamsal etiket kullanılır?"
  2: "Bu figürün başlığını veya alt yazısını tanımlayan etiket hangisidir?"
  3: "Bu anlamsal gösterim 'kod bloğu figürü ve başlığı (figure, figcaption ve pre code)' olarak bilinir."
```

---

### html-medium-microdata-article-schema

```yaml
id: html-medium-microdata-article-schema
version: 1
language: html
engine: none
difficulty: medium
title: "Arama motorları için mikro veri yapılandırılmış içerik (Microdata Schema.org)"
prompt: |
  Bir haber makalesinin arama motorları tarafından zengin sonuçlar (rich snippets) olarak
  dizine eklenebilmesi için HTML elemanlarının içine doğrudan Microdata standart özniteliklerini
  yerleştirin. Makalenin kendisini Schema.org 'NewsArticle' türü olarak tanımlayın; başlık,
  yazar adı ve yayınlanma tarihi alanlarını ilgili veri özellikleri ile etiketleyin.
constraints:
  - "Kapsayıcıda 'itemscope' ve 'itemtype=\"https://schema.org/NewsArticle\"' bulunmalı"
  - "Başlıkta 'itemprop=\"headline\"' yer almalı"
  - "Yazarda 'itemprop=\"author\"' ve yayın tarihinde 'itemprop=\"datePublished\"' yer almalı"
concept_tags: [semantics, standards, performance]
checklist_extra:
  - "itemscope mantıksal niteliği eklenmiş mi?"
  - "itemtype şeması geçerli bir schema.org URL'sine işaret ediyor mu?"
reference_solution_path: private/solutions/html-medium-microdata-article-schema.html
hint_ladder:
  1: "HTML elemanlarına doğrudan arama motoru şeması ekleyen W3C mikro veri nitelik kümesi nedir?"
  2: "Öğe kapsamını açan ve şema tipini belirten nitelik ikilisi hangisidir?"
  3: "Bu anlamsal veri standardı 'HTML5 mikro veri yapılandırması (Microdata itemscope ve itemprop)' olarak bilinir."
```

---

### html-medium-content-security-policy-meta

```yaml
id: html-medium-content-security-policy-meta
version: 1
language: html
engine: none
difficulty: medium
title: "İstemci taraflı içerik güvenlik politikası bildirimi (meta CSP)"
prompt: |
  Bir web sayfasında XSS (Cross-Site Scripting) saldırılarını hafifletmek amacıyla sayfanın
  yalnızca kendi sunucusundan script yüklemesine, inline scriptleri engellemesine ve görselleri
  yalnızca kendi kaynağından ve güvenilir bir CDN'den (https://images.ornekcdn.com) çekmesine
  izin veren katı bir İçerik Güvenlik Politikasını `<head>` bölümüne meta etiket olarak ekleyin.
constraints:
  - "<meta http-equiv='Content-Security-Policy' ...> etiketi kullanılmalı"
  - "content içinde 'default-src \\'self\\'' tanımlanmalı"
  - "Görseller için 'img-src \\'self\\' https://images.ornekcdn.com' kuralı yer almalı"
  - "Etiket <head> elemanı içine yerleştirilmeli"
concept_tags: [security, standards, performance]
checklist_extra:
  - "http-equiv değeri Content-Security-Policy olarak yazılmış mı?"
  - "Direktifler noktalı virgül (;) ile birbirinden ayrılmış mı?"
reference_solution_path: private/solutions/html-medium-content-security-policy-meta.html
hint_ladder:
  1: "Tarayıcının hangi kaynaklardan script ve medya yükleyebileceğini kısıtlayan güvenlik başlığı/meta etiketi nedir?"
  2: "Meta etikette bu kuralı bildirmek için http-equiv değerine ne yazılır?"
  3: "Bu web güvenlik standardı 'İçerik Güvenlik Politikası bildirimi (Content Security Policy meta)' olarak bilinir."
```

---

### html-medium-meta-referrer-policy

```yaml
id: html-medium-meta-referrer-policy
version: 1
language: html
engine: none
difficulty: medium
title: "Referans gönderici gizlilik politikası (meta referrer policy)"
prompt: |
  Kullanıcı gizliliğini korumak amacıyla, web sitenizdeki sayfalar arası gezinmelerde ve dış
  bağlantılara tıklamalarda tarayıcının referans başlığını (Referer header) nasıl göndereceğini
  kontrol etmek istiyorsunuz. Aynı kök (same-origin) isteklerinde tam URL'nin gönderilmesini,
  ancak HTTPS'ten HTTP'ye geçişte veya güvensiz dış bağlantılarda hassas yol bilgilerinin
  gizlenmesini sağlayan modern standart gizlilik politikasını meta etiketiyle tanımlayın.
constraints:
  - "<meta name='referrer' content='strict-origin-when-cross-origin'> etiketi bulunmalı"
  - "Etiket <head> bölümüne yerleştirilmeli"
  - "Politika değeri standart W3C referans kurallarına uygun olmalı"
concept_tags: [security, standards, links]
checklist_extra:
  - "name özniteliği referrer olarak atanmış mı?"
  - "content değeri modern tarayıcı varsayılanı olan strict-origin-when-cross-origin olarak verilmiş mi?"
reference_solution_path: private/solutions/html-medium-meta-referrer-policy.html
hint_ladder:
  1: "Tarayıcının diğer sayfalara geçerken URL gönderme davranışını yöneten meta etiketi nedir?"
  2: "Çapraz köklerde yalnızca kök adresini gönderip güvensiz bağlantıda hiç göndermeyen standart değer nedir?"
  3: "Bu gizlilik kuralı 'referans gönderici gizlilik politikası (meta referrer policy)' olarak bilinir."
```

---

### html-medium-dialog-nested-confirmation

```yaml
id: html-medium-dialog-nested-confirmation
version: 1
language: html
engine: none
difficulty: medium
title: "İki aşamalı eylem onay iletişim kutusu (dialog cancel ve confirm)"
prompt: |
  Kullanıcının kritik bir işlemi (örneğin abonelik iptali) gerçekleştirmeden önce uyarılmasını
  sağlayan bir onay modal kutusu hazırlayın. İletişim kutusunun içinde eylemin geri alınamaz
  olduğunu anlatan bir açıklama, vazgeçmeyi sağlayan 'İptal' butonu ve işlemi kesinleştiren
  'Onayla' butonu yer almalıdır. İptal butonu form method dialog kullanarak pencereyi
  kapatırken, onayla butonu form submit işlemi gerçekleştirerek sunucuya bildirim göndermelidir.
constraints:
  - "<dialog> elemanı kullanılmalı ve başlığı ile 'aria-labelledby' bağlantısı kurulmalı"
  - "Kapatma/vazgeçme için 'method=\"dialog\"' form yapısı kullanılmalı"
  - "Onay işlemi için ayrı bir gönderim eylemi veya buton tanımlanmalı"
  - "Modal pencere erişilebilir bir başlık ve paragraf içermeli"
concept_tags: [dialogs, forms, accessibility]
checklist_extra:
  - "Dialog başlığı aria-labelledby ile dialog elemanına bağlanmış mı?"
  - "İptal ve onayla eylemleri anlamsal olarak ayrıştırılmış mı?"
reference_solution_path: private/solutions/html-medium-dialog-nested-confirmation.html
hint_ladder:
  1: "Yerleşik onay pencereleri için kullanılan modern HTML5 etiketi nedir?"
  2: "İptal butonunun modalı kapatması için hangi form metodu kullanılır?"
  3: "Bu kullanıcı onay mekanizması 'onay iletişim kutusu (confirmation dialog)' olarak bilinir."
```

---

## Zor Düzey Sorular (151 - 200)

### html-hard-wai-aria-tablist-widget

```yaml
id: html-hard-wai-aria-tablist-widget
version: 1
language: html
engine: none
difficulty: hard
title: "Tam erişilebilir sekmeli içerik bileşeni (WAI-ARIA Tablist Pattern)"
prompt: |
  Kullanıcıların tek bir görünümde farklı paneller arasında geçiş yapabildiği üç sekmeli bir
  hesap yönetim paneli (Genel Bakış, Güvenlik Ayarları, Bildirimler) tasarlıyorsunuz. Sekme
  çubuğu ile alttaki içerik panelleri arasındaki hiyerarşik WAI-ARIA rollerini eksiksiz kurun.
  Klavye ile dolaşırken (roving tabindex kuralına uygun olarak) yalnızca o anda aktif olan
  sekmenin sekme sırasında (Tab) yer almasını, pasif sekmelerin ise sekme sırasından çıkarılmasını
  sağlayın. Her sekmenin hangi paneli kontrol ettiğini ve her panelin hangi sekme tarafından
  adlandırıldığını iki yönlü kimlik ilişkileriyle bağlayın.
constraints:
  - "Sekme kapsayıcısında 'role=\"tablist\"' bulunmalı"
  - "Sekme butonlarında 'role=\"tab\"', 'aria-selected' ve 'aria-controls' yer almalı"
  - "Yalnızca seçili sekmede 'tabindex=\"0\"', diğerlerinde 'tabindex=\"-1\"' olmalı"
  - "İçerik panellerinde 'role=\"tabpanel\"' ve 'aria-labelledby' bulunmalı"
concept_tags: [accessibility, focus, navigation]
checklist_extra:
  - "Sekmeler ile paneller arasındaki aria-controls ve aria-labelledby bağlantıları çift taraflı eşleşiyor mu?"
  - "Dolaşan sekme sırası (roving tabindex) için seçili olmayan sekmeler -1 ile işaretlenmiş mi?"
reference_solution_path: private/solutions/html-hard-wai-aria-tablist-widget.html
hint_ladder:
  1: "Sekmeli arayüzlerde sekmeleri sarmalayan çubuğa ve her bir sekme başlığına hangi WAI-ARIA rolleri verilir?"
  2: "Kullanıcının klavye ok tuşlarıyla sekmeler arasında gezinmesi için aktif olmayan sekmelerin tabindex değeri kaç olmalıdır?"
  3: "Bu karmaşık erişilebilirlik deseni 'WAI-ARIA sekmeli içerik bileşeni (tablist, tab, tabpanel)' olarak bilinir."
```

---

### html-hard-wai-aria-combobox-autocomplete

```yaml
id: html-hard-wai-aria-combobox-autocomplete
version: 1
language: html
engine: none
difficulty: hard
title: "Açılır öneri kutusu bileşeni (WAI-ARIA 1.2 Combobox Pattern)"
prompt: |
  Kullanıcı bir ülke arama kutusuna yazmaya başladığında altında dinamik olarak bir liste
  açılan özel bir arama bileşeni kurguluyorsunuz. W3C WAI-ARIA 1.2 standartlarına göre,
  metin girdi alanının bir açılır öneri kutusu olduğunu, listenin o anda açık olup olmadığını,
  açılan listenin kimliğini ve klavye ile liste öğeleri üzerinde gezinirken sanal odaklanan
  öğenin kimliğini yardımcı teknolojilere bildiren tüm durum ve ilişkilendirme niteliklerini
  girdi kutusu ve altındaki liste yapısına uygulayın.
constraints:
  - "<input> elemanında 'role=\"combobox\"', 'aria-autocomplete=\"list\"' bulunmalı"
  - "Listenin açık durumunu belirten 'aria-expanded=\"true\"' veya 'false' bulunmalı"
  - "Kontrol edilen listeyi gösteren 'aria-controls' ve sanal odağı gösteren 'aria-activedescendant' bulunmalı"
  - "Açılan liste '<ul role=\"listbox\">' ve maddeleri '<li role=\"option\">' olmalı"
concept_tags: [accessibility, focus, forms]
checklist_extra:
  - "Kombine kutu girdi elemanına aria-activedescendant niteliği tanımlanmış mı?"
  - "Liste elemanı listbox, elemanları ise option rolüne sahip mi?"
reference_solution_path: private/solutions/html-hard-wai-aria-combobox-autocomplete.html
hint_ladder:
  1: "Hem metin girişi hem de açılır liste seçimi sunan hibrit girdi bileşeni hangi ARIA rolünü alır?"
  2: "Gerçek klavye odağını girdi alanında tutarken listedeki seçili öğeyi ekran okuyucuya aktaran nitelik nedir?"
  3: "Bu gelişmiş erişilebilirlik yapısı 'WAI-ARIA açılır öneri kutusu deseni (combobox ve aria-activedescendant)' olarak bilinir."
```

---

### html-hard-wai-aria-roving-tabindex-toolbar

```yaml
id: html-hard-wai-aria-roving-tabindex-toolbar
version: 1
language: html
engine: none
difficulty: hard
title: "Dolaşan sekme sıralı araç çubuğu (WAI-ARIA Toolbar ve Roving Tabindex)"
prompt: |
  Bir zengin metin editöründe kalın, italik, altı çizili, liste ve bağlantı ekleme butonlarından
  oluşan bir araç çubuğu (toolbar) inşa ediyorsunuz. Klavye kullanıcısı sayfayı turlarken Tab
  tuşuna bastığında bu araç çubuğundaki her butona tek tek uğrayıp zaman kaybetmemeli; tüm
  araç çubuğu tek bir durak olmalıdır. Araç çubuğunun içine girildiğinde ok tuşlarıyla dolaşım
  (roving tabindex) mantığını desteklemek üzere o anki aktif butonda 'tabindex="0"', diğer tüm
  butonlarda ise 'tabindex="-1"' yer almalıdır. Araç çubuğu ve butonların semantik yapısını kurun.
constraints:
  - "Kapsayıcıda 'role=\"toolbar\"' ve açıklayıcı 'aria-label' bulunmalı"
  - "İlk (veya aktif) buton 'tabindex=\"0\"' değerine sahip olmalı"
  - "Diğer tüm butonlar 'tabindex=\"-1\"' değerine sahip olmalı"
  - "İki durumlu butonlarda (kalın, italik vb.) 'aria-pressed' durumu belirtilmeli"
concept_tags: [accessibility, focus, standards]
checklist_extra:
  - "Araç çubuğu rolü toolbar olarak atanmış mı?"
  - "Tek bir butonda tabindex='0', diğerlerinde tabindex='-1' kuralı uygulanmış mı?"
reference_solution_path: private/solutions/html-hard-wai-aria-roving-tabindex-toolbar.html
hint_ladder:
  1: "Bir grup etkileşimli butonu tek bir mantıksal kontrol çubuğu olarak tanımlayan ARIA rolü nedir?"
  2: "Kullanıcının bileşen içine tek bir Tab basışıyla girip ok tuşlarıyla gezmesi için pasif butonlara hangi tabindex verilir?"
  3: "Bu klavye dolaşım deseni 'araç çubuğu ve dolaşan sekme sırası (toolbar roving tabindex)' olarak bilinir."
```

---

### html-hard-wai-aria-treeview-file-explorer

```yaml
id: html-hard-wai-aria-treeview-file-explorer
version: 1
language: html
engine: none
difficulty: hard
title: "Hiyerarşik dosya gezgini ağaç yapısı (WAI-ARIA Treeview Pattern)"
prompt: |
  Bir bulut kod editöründe klasör ve dosyaların iç içe listelendiği bir dosya gezgini
  ağaç bileşeni (treeview) tasarlıyorsunuz. W3C ağaç deseni standartlarına göre kök liste,
  dallar (klasörler), alt gruplar ve yaprak düğümler (dosyalar) için gerekli semantik rolleri
  tanımlayın. Klasörlerin açık/kapalı durumunu bildiren durum niteliklerini ve klavye odağının
  yalnızca seçili öğede olmasını sağlayan odaklama indekslerini ekleyin.
constraints:
  - "Kök listede 'role=\"tree\"' ve 'aria-label' bulunmalı"
  - "Klasör ve dosya elemanlarında 'role=\"treeitem\"' bulunmalı"
  - "Açılır klasörlerde 'aria-expanded=\"true\"' veya 'false' yer almalı"
  - "Klasör altındaki alt listelerde 'role=\"group\"' bulunmalı"
  - "Seçili olan tek bir öğede 'tabindex=\"0\"', diğerlerinde 'tabindex=\"-1\"' olmalı"
concept_tags: [accessibility, navigation, focus]
checklist_extra:
  - "İç içe alt dallar için role='group' kullanılmış mı?"
  - "Klasör genişletme durumları aria-expanded ile doğru modellenmiş mi?"
reference_solution_path: private/solutions/html-hard-wai-aria-treeview-file-explorer.html
hint_ladder:
  1: "İç içe hiyerarşik klasör ve dosya listelerini temsil eden standart WAI-ARIA rolü hangisidir?"
  2: "Bir ağaç dalının altındaki alt öğeler kümesini tanımlamak için hangi rol kullanılır?"
  3: "Bu navigasyon mimarisi 'erişilebilir ağaç görünümü deseni (WAI-ARIA treeview)' olarak bilinir."
```

---

### html-hard-wai-aria-custom-slider-widget

```yaml
id: html-hard-wai-aria-custom-slider-widget
version: 1
language: html
engine: none
difficulty: hard
title: "Özel tasarımlı erişilebilir kaydırıcı bileşeni (WAI-ARIA Slider)"
prompt: |
  Bir müzik prodüksiyon uygulamasında standart HTML range girdisinin izin vermediği
  özel görsel efektlere sahip bir ses seviyesi kaydırıcısı (fader) geliştiriyorsunuz.
  Görsel olarak `<div>` etiketleriyle oluşturulacak bu özel kaydırıcı tutamacının (thumb)
  klavye ile odaklanabilmesini, yardımcı teknolojilerin bunu bir kaydırıcı olarak tanımasını,
  minimum, maksimum ve o anki değerini seslendirmesini, ayrıca yüzdeyi 'Yüzde 75 Ses Seviyesi'
  şeklinde insan tarafından okunabilir bir metinle aktarmasını sağlayın.
constraints:
  - "Kaydırıcı tutamacında 'role=\"slider\"' bulunmalı"
  - "'tabindex=\"0\"' ile klavye odağı verilmeli"
  - "'aria-valuemin', 'aria-valuemax' ve 'aria-valuenow' sayısal değerleri yer almalı"
  - "İnsan dostu metinsel okuma için 'aria-valuetext' niteliği bulunmalı"
  - "Kaydırıcının neyi kontrol ettiğini belirten 'aria-label' veya 'aria-labelledby' yer almalı"
concept_tags: [accessibility, focus, forms]
checklist_extra:
  - "Sayısal değerlerin yanında aria-valuetext ile açıklayıcı metin sağlanmış mı?"
  - "Tutamaca klavyeden erişilebilmesi için tabindex='0' eklenmiş mi?"
reference_solution_path: private/solutions/html-hard-wai-aria-custom-slider-widget.html
hint_ladder:
  1: "Özel bir elemanı kaydırıcı bileşeni olarak tanıtmak için hangi WAI-ARIA rolü atanır?"
  2: "Kaydırıcının anlık değerini ekranda görünen biçimiyle seslendirmek için hangi nitelik kullanılır?"
  3: "Bu özel kontrol 'WAI-ARIA kaydırıcı deseni (slider ve aria-valuetext)' olarak bilinir."
```

---

### html-hard-wai-aria-alertdialog-modal

```yaml
id: html-hard-wai-aria-alertdialog-modal
version: 1
language: html
engine: none
difficulty: hard
title: "Kritik eylem onay uyarı penceresi (WAI-ARIA Alertdialog Pattern)"
prompt: |
  Bir kurumsal veritabanı yönetim panelinde kullanıcının 'Tüm Müşteri Kayıtlarını Sil' butonuna
  bastığında açılan kritik bir onay penceresi tasarlayın. Standart bir bilgilendirme penceresinden
  farklı olarak, bu pencere kullanıcının acil dikkatini talep eder ve sayfa arkasındaki hiçbir
  elemanla etkileşime girilmesine izin vermez. W3C erişilebilirlik standartlarına uygun acil durum
  iletişim kutusu rolünü, başlık ve gövde açıklaması ilişkilendirmelerini ve klavye odağının
  doğrudan en güvenli eyleme (İptal butonuna) yönlendirilmesini sağlayan yapıyı kurun.
constraints:
  - "Kapsayıcıda 'role=\"alertdialog\"' ve 'aria-modal=\"true\"' bulunmalı"
  - "Kapsayıcı başlığa 'aria-labelledby', açıklama metnine 'aria-describedby' ile bağlanmalı"
  - "Pencere içinde 'autofocus' niteliği güvenli eylem olan 'Vazgeç/İptal' butonunda olmalı"
  - "Onay ve iptal butonları belirgin şekilde yapılandırılmalı"
concept_tags: [dialogs, accessibility, focus]
checklist_extra:
  - "Standart dialog yerine acil durum onayları için role='alertdialog' tercih edilmiş mi?"
  - "Varsayılan odak autofocus ile yıkıcı olmayan iptal butonuna verilmiş mi?"
reference_solution_path: private/solutions/html-hard-wai-aria-alertdialog-modal.html
hint_ladder:
  1: "Kullanıcıdan kritik bir karar veya onay bekleyen acil pencerelere hangi özel rol atanır?"
  2: "Pencerenin tüm sayfayı bloke eden kalıcı bir modal olduğunu belirten ARIA niteliği nedir?"
  3: "Bu kritik arayüz deseni 'acil onay iletişim kutusu (WAI-ARIA alertdialog)' olarak bilinir."
```

---

### html-hard-complex-multidimensional-table

```yaml
id: html-hard-complex-multidimensional-table
version: 1
language: html
engine: none
difficulty: hard
title: "Çok boyutlu karmaşık matris finans tablosu (headers ve id matrisi)"
prompt: |
  Bir holdingin 2 yıllık finansal konsolidasyon tablosunu hazırlıyorsunuz. Tablo sütunlarında
  en üstte yıllar (2023, 2024), onların altında çeyrekler (Q1, Q2, Q3, Q4) ve onların altında
  para birimleri yer almaktadır. Satırlarda ise ana faaliyet kolları ve onların altında alt
  departmanlar gruplanmıştır. Hiçbir görsel tarayıcıda kayma yaşanmaması için sütun ve satır
  birleştirmelerini (colspan, rowspan) hatasız kurgulayın; en önemlisi görme engelli bir finans
  denetçisinin ekran okuyucusuyla herhangi bir hücreye geldiğinde o hücrenin yılını, çeyreğini,
  para birimini ve departmanını eksiksiz duyabilmesi için tam kimlik eşleştirme matrisini kurun.
constraints:
  - "Birden fazla düzeyde <th> başlıklarında benzersiz 'id' nitelikleri bulunmalı"
  - "Karmaşık birleştirmeler için 'colspan' ve 'rowspan' doğru hesaplanmalı"
  - "Tüm veri hücrelerinde (<td>) ilgili tüm başlık id'lerini boşlukla sıralayan 'headers' niteliği bulunmalı"
  - "Tablo anlamsal bir <caption> ve <colgroup> mimarisi barındırmalı"
concept_tags: [tables, accessibility, standards]
checklist_extra:
  - "Hücrelerdeki headers özniteliği hiyerarşideki tüm üst ve yan başlıkları eksiksiz içeriyor mu?"
  - "colspan ve rowspan toplamları tablonun tüm satır ve sütun genişlikleriyle matematiksel olarak uyuşuyor mu?"
reference_solution_path: private/solutions/html-hard-complex-multidimensional-table.html
hint_ladder:
  1: "Çok katmanlı tablolarda hücreleri hiyerarşik başlık zincirine bağlayan yöntem nedir?"
  2: "Hücrenin headers niteliğine birden fazla başlık id'si yazılırken aralarına ne konur?"
  3: "Bu ileri tablo mimarisi 'çok boyutlu matris tablo başlık eşleştirmesi (complex table headers and id matrix)' olarak bilinir."
```

---

### html-hard-sri-hash-security

```yaml
id: html-hard-sri-hash-security
version: 1
language: html
engine: none
difficulty: hard
title: "Alt kaynak bütünlüğü ve CDN güvenlik doğrulaması (Subresource Integrity - SRI)"
prompt: |
  Kurumsal bir bankacılık arayüzünde harici bir CDN sağlayıcısından (örneğin cdn.ornekcdn.com)
  kritik bir JavaScript kütüphanesi ve CSS stil dosyası çekilmektedir. CDN sunucusunun ele
  geçirilmesi (supply-chain attack) durumunda zararlı kodların kullanıcıların tarayıcısında
  çalışmasını engellemek için, indirilen dosyanın SHA-384 kriptografik hash özetini tarayıcıya
  doğrulatan ve çapraz kök kimlik bilgilerini kısıtlayan Subresource Integrity (SRI) etiketlerini
  hem script hem link elemanına uygulayın.
constraints:
  - "<script> etiketinde 'integrity=\"sha384-...\"' niteliği bulunmalı"
  - "<link rel='stylesheet'> etiketinde 'integrity=\"sha384-...\"' bulunmalı"
  - "Her iki etikette de 'crossorigin=\"anonymous\"' niteliği mutlaka yer almalı"
  - "Etiketler geçerli harici HTTPS URL'lerine işaret etmeli"
concept_tags: [security, standards, performance]
checklist_extra:
  - "integrity özniteliği sha384 veya sha512 algoritma önekiyle başlıyor mu?"
  - "SRI hash kontrolünün çalışabilmesi için şart olan crossorigin='anonymous' eklenmiş mi?"
reference_solution_path: private/solutions/html-hard-sri-hash-security.html
hint_ladder:
  1: "Harici CDN'den çekilen dosyaların değiştirilmediğini doğrulamak için hangi güvenlik niteliği kullanılır?"
  2: "Tarayıcının hash kontrolünü CORS kuralları dahilinde yapabilmesi için hangi ek nitelik zorunludur?"
  3: "Bu web güvenlik standardı 'alt kaynak bütünlüğü doğrulaması (Subresource Integrity - SRI)' olarak bilinir."
```

---

### html-hard-speculation-rules-prerender

```yaml
id: html-hard-speculation-rules-prerender
version: 1
language: html
engine: none
difficulty: hard
title: "Tahmine dayalı anında sayfa ön oluşturma (Speculation Rules API)"
prompt: |
  Bir e-ticaret sitesinde kullanıcının sepet sayfasına girdiğinde, çok yüksek bir ihtimalle
  'Ödeme Adımına Geç' bağlantısına tıklayacağını biliyorsunuz. Kullanıcı tıkladığı anda sayfanın
  sıfır milisaniyede anında yüklenmesi için, modern tarayıcıların desteklediği Tahmin Kuralları
  (Speculation Rules) API'sini kullanarak hedef ödeme URL'sinin arka planda tamamen önceden
  işlenmesini (prerender) ve ürün detay bağlantılarının ise sadece önceden getirilmesini
  (prefetch) sağlayan JSON yapılandırmasını HTML belgesine gömün.
constraints:
  - "<script type='speculationrules'> etiketi kullanılmalı"
  - "JSON içinde 'prerender' kuralı ve 'where' veya 'urls' listesi bulunmalı"
  - "JSON içinde 'prefetch' kuralı tanımlanmalı"
  - "Öncelik veya gizlilik kısıtlamaları geçerli JSON sözdiziminde olmalı"
concept_tags: [performance, standards, links]
checklist_extra:
  - "Script etiketinin type değeri tam olarak speculationrules olarak verilmiş mi?"
  - "İçerik geçerli bir JSON veri yapısı taşıyor mu?"
reference_solution_path: private/solutions/html-hard-speculation-rules-prerender.html
hint_ladder:
  1: "Gelecekte ziyaret edilecek sayfaları arka planda sıfır gecikmeyle önceden render ettiren yeni nesil API nedir?"
  2: "Bu tahmin kurallarını HTML'e eklemek için script etiketinin type özniteliğine ne yazılır?"
  3: "Bu ileri düzey performans standardı 'tahmin kuralları ile ön oluşturma (Speculation Rules API)' olarak bilinir."
```

---

### html-hard-jsonld-ecommerce-product-schema

```yaml
id: html-hard-jsonld-ecommerce-product-schema
version: 1
language: html
engine: none
difficulty: hard
title: "E-ticaret zengin ürün arama kartı şeması (JSON-LD Product, Offer ve Review)"
prompt: |
  Google arama sonuçlarında bir ürünün fiyatı, stok durumu, ortalama kullanıcı puanı ve
  örnek bir müşteri incelemesi ile birlikte zengin kart (rich snippet) olarak gösterilmesini
  istiyorsunuz. W3C ve Google tarafından önerilen en güncel yapı olan JSON-LD formatında,
  sayfanın `<head>` bölümüne gömülü yapılandırılmış veri hazırlayın. Şema 'Product' türünde
  olmalı; 'offers' (fiyat, para birimi, stok durumu) ve 'aggregateRating' (ortalama puan,
  değerlendirme sayısı) nesnelerini içermelidir.
constraints:
  - "<script type='application/ld+json'> kapsayıcısı kullanılmalı"
  - "'@context': 'https://schema.org' ve '@type': 'Product' tanımlanmalı"
  - "'offers' nesnesi altında 'Offer', 'price', 'priceCurrency' ve 'availability' yer almalı"
  - "'aggregateRating' nesnesi altında 'AggregateRating', 'ratingValue' ve 'reviewCount' yer almalı"
concept_tags: [standards, performance, semantics]
checklist_extra:
  - "Stok durumu Schema.org standart URL'si (InStock vb.) ile mi belirtilmiş?"
  - "JSON formatı hatasız ve geçerli mi?"
reference_solution_path: private/solutions/html-hard-jsonld-ecommerce-product-schema.html
hint_ladder:
  1: "Arama motorlarına yapılandırılmış veriyi harici blok olarak sunan script tipi nedir?"
  2: "Schema.org ürün şemalarında teklif ve stok bilgilerini temsil eden alt nesne tipi hangisidir?"
  3: "Bu SEO mimarisi 'JSON-LD ürün yapılandırılmış veri şeması (Product JSON-LD schema)' olarak bilinir."
```

---

### html-hard-jsonld-faqpage-rich-snippets

```yaml
id: html-hard-jsonld-faqpage-rich-snippets
version: 1
language: html
engine: none
difficulty: hard
title: "Arama sonuçları için dinamik SSS zengin kart şeması (JSON-LD FAQPage)"
prompt: |
  Bir SaaS ürününün sıkça sorulan sorular sayfasındaki soru ve cevapların doğrudan Google
  arama sonuçları sayfasında açılır kapanır akordeon şeklinde görüntülenmesi (FAQ rich results)
  için gerekli yapılandırılmış veriyi oluşturun. En az üç farklı soru ve detaylı cevap
  çiftini barındıran geçerli bir JSON-LD FAQPage şemasını sayfanın `<head>` bölümüne ekleyin.
constraints:
  - "<script type='application/ld+json'> kullanılmalı"
  - "'@type': 'FAQPage' kök tipi bulunmalı"
  - "'mainEntity' dizisi içinde en az 3 adet 'Question' ve ona bağlı 'Answer' yer almalı"
  - "Her sorunun 'name' ve cevabın 'text' özellikleri eksiksiz olmalı"
concept_tags: [standards, semantics, accessibility]
checklist_extra:
  - "mainEntity dizisindeki her öğe Question tipinde mi?"
  - "acceptedAnswer nesnesi altında text özelliği ile cevap metni verilmiş mi?"
reference_solution_path: private/solutions/html-hard-jsonld-faqpage-rich-snippets.html
hint_ladder:
  1: "Arama sonuçlarında SSS akordeonu oluşturan Schema.org ana tipi nedir?"
  2: "Her bir soru ve kabul edilmiş cevap çifti hangi nesne adlarıyla tanımlanır?"
  3: "Bu zengin arama yapısı 'JSON-LD sıkça sorulan sorular şeması (FAQPage Schema)' olarak bilinir."
```

---

### html-hard-hreflang-internationalization

```yaml
id: html-hard-hreflang-internationalization
version: 1
language: html
engine: none
difficulty: hard
title: "Çok dilli ve çok bölgeli SEO yönlendirme matrisi (link rel alternate hreflang)"
prompt: |
  Küresel hizmet veren bir şirketin ana sayfasında; Türkiye (Türkçe), Birleşik Krallık (İngilizce),
  Amerika Birleşik Devletleri (İngilizce), Almanya (Almanca) ve eşleşmeyen tüm diğer dünya
  ülkeleri için varsayılan genel İngilizce sayfası bulunmaktadır. Arama motorlarının her ülkedeki
  kullanıcıyı kendi bölgesel ve dil sürümüne yönlendirmesi için sayfanın `<head>` bölümüne
  karşılıklı hreflang alternatif bağlantı matrisini eksiksiz ekleyin.
constraints:
  - "Türkiye için 'hreflang=\"tr-TR\"' veya 'tr' bulunmalı"
  - "İngiltere için 'hreflang=\"en-GB\"' ve ABD için 'hreflang=\"en-US\"' yer almalı"
  - "Eşleşmeyen bölgeler için 'hreflang=\"x-default\"' mutlaka tanımlanmalı"
  - "Mevcut sayfanın kendi kendine de referans veren (self-referencing) linki bulunmalı"
concept_tags: [standards, links, performance]
checklist_extra:
  - "Varsayılan küresel yedek sayfa için x-default direktifi kullanılmış mı?"
  - "Mevcut sayfa kendi hreflang alternatifleri arasında kendine de yer vermiş mi?"
reference_solution_path: private/solutions/html-hard-hreflang-internationalization.html
hint_ladder:
  1: "Arama motorlarına bir sayfanın farklı dillerdeki karşılıklarını bildiren link ilişkisi nedir?"
  2: "Eşleşmeyen tüm diğer ülke ve diller için kullanılan evrensel yedekleme kodu nedir?"
  3: "Bu uluslararası SEO mimarisi 'çok dilli alternatif bağlantı matrisi (hreflang ve x-default)' olarak bilinir."
```

---

### html-hard-picture-nextgen-avif-webp-fallback

```yaml
id: html-hard-picture-nextgen-avif-webp-fallback
version: 1
language: html
engine: none
difficulty: hard
title: "Yeni nesil görsel formatları ve piksel yoğunluğu hiyerarşisi (AVIF, WebP ve Retina)"
prompt: |
  Bir fotoğrafçılık portföyünde devasa bir kahraman (hero) görseli sunuyorsunuz. Görsel dosya
  boyutunu en aza indirmek için modern tarayıcılara önce son derece verimli AVIF formatını,
  desteklemiyorsa WebP formatını, en son çare olarak ise optimize edilmiş standart JPEG formatını
  sunmalısınız. Üstelik her iki yeni nesil formatta da standart ekranlar (1x) ve yüksek çözünürlüklü
  Retina ekranlar (2x) için ikişer çözünürlük alternatifi tanımlanmalıdır. Tarayıcının en modern
  ve en hafif görseli seçmesini sağlayan tam teşekküllü görsel kapsayıcısını kurun.
constraints:
  - "<picture> kapsayıcısı kullanılmalı"
  - "İlk <source> elemanında 'type=\"image/avif\"' ve 1x/2x srcset bulunmalı"
  - "İkinci <source> elemanında 'type=\"image/webp\"' ve 1x/2x srcset bulunmalı"
  - "Son fallback olarak geçerli width, height ve alt değerlerine sahip <img> bulunmalı"
concept_tags: [images, performance, standards]
checklist_extra:
  - "Tarayıcının format önceliğini doğru seçmesi için AVIF kaynağı WebP'den önce mi yerleştirilmiş?"
  - "Piksel yoğunluğu tanımlayıcısı olarak 1x ve 2x kullanılmış mı?"
reference_solution_path: private/solutions/html-hard-picture-nextgen-avif-webp-fallback.html
hint_ladder:
  1: "Görsel formatının MIME türüne göre alternatif seçilmesini sağlayan source niteliği nedir?"
  2: "Retina ve yüksek DPI ekranlar için görsel varyasyonları srcset içinde nasıl ayrıştırılır?"
  3: "Bu ileri düzey medya tekniği 'yeni nesil format kademeli yükleme mimarisi (picture AVIF WebP srcset)' olarak bilinir."
```

---

### html-hard-inline-svg-sprite-sheet

```yaml
id: html-hard-inline-svg-sprite-sheet
version: 1
language: html
engine: none
difficulty: hard
title: "Performanslı satır içi SVG simge kütüphanesi (SVG sprite ve symbol defs)"
prompt: |
  Bir web uygulamasında düzinelerce farklı yerde kullanılan simgeleri (kullanıcı profili, sepet,
  arama, ayarlar) her seferinde tüm SVG kodlarıyla sayfaya basıp DOM boyutunu şişirmek yerine,
  sayfanın görünmeyen bir köşesinde bir kez tanımlanan bir SVG sembol kütüphanesi (sprite sheet)
  oluşturun. Ardından sayfanın farklı yerlerinde bu sembolleri kimlikleri üzerinden çağıran
  iki adet erişilebilir buton oluşturun.
constraints:
  - "Görünmez bir SVG içinde <defs> veya doğrudan <symbol id='...'> blokları bulunmalı"
  - "Sembollerde 'viewBox' koordinat sistemi tanımlanmalı"
  - "Kullanım yerinde '<svg><use href=\"#simge-id\"></use></svg>' yapısı kullanılmalı"
  - "Tüketilen simgeler erişilebilir butonlar içine 'aria-hidden=\"true\"' ile yerleştirilmeli"
concept_tags: [images, performance, accessibility]
checklist_extra:
  - "Kütüphane içinde semboller symbol etiketi ve benzersiz id'lerle mi saklanmış?"
  - "Sembolleri çağırmak için standart use href köprüsü kullanılmış mı?"
reference_solution_path: private/solutions/html-hard-inline-svg-sprite-sheet.html
hint_ladder:
  1: "Birden çok kez kullanılacak SVG simgelerini tek bir şablonda tanımlamak için hangi SVG etiketi kullanılır?"
  2: "Tanımlanan sembolü sayfa içinde başka bir SVG'ye kopyalamadan dahil eden eleman hangisidir?"
  3: "Bu vektör optimizasyon deseni 'SVG sembol kütüphanesi ve kullanımı (SVG sprite symbol use)' olarak bilinir."
```

---

### html-hard-form-interdependent-aria-errormessage

```yaml
id: html-hard-form-interdependent-aria-errormessage
version: 1
language: html
engine: none
difficulty: hard
title: "Programatik canlı hata mesajı ilişkilendirmesi (aria-errormessage ve aria-invalid)"
prompt: |
  Bir kurumsal kayıt formunda TC Kimlik No veya Vergi Kimlik No gibi özel algoritmik doğrulama
  gerektiren bir alan bulunmaktadır. JavaScript ile doğrulama yapıldığında, standart yardım
  metninden bağımsız olarak ortaya çıkan hata bildirim kutusunu girdi alanıyla doğrudan bağlayın.
  W3C ARIA standartlarının form hataları için özel olarak tanımladığı hata mesajı bağlantı
  niteliğini kullanın ve hata oluştuğunda ekran okuyucunun hatayı anında seslendirmesini sağlayın.
constraints:
  - "<input> elemanında 'aria-invalid=\"true\"' yer almalı"
  - "Girdi elemanı 'aria-errormessage=\"error-id\"' niteliği ile hata kutusuna bağlanmalı"
  - "Hata mesajı kutusu 'id=\"error-id\"' taşımalı ve 'aria-live=\"polite\"' canlı bölgesi olmalı"
  - "Genel yardım metni varsa ayrı bir 'aria-describedby' ile korunmalı"
concept_tags: [forms, accessibility, input-validation]
checklist_extra:
  - "Hata mesajı için describedby yerine doğrudan aria-errormessage kullanılmış mı?"
  - "Hata kutusu canlı bölge (aria-live) olarak yapılandırılmış mı?"
reference_solution_path: private/solutions/html-hard-form-interdependent-aria-errormessage.html
hint_ladder:
  1: "WAI-ARIA'da bir form alanını yalnızca ve doğrudan hata metnine bağlayan özel nitelik nedir?"
  2: "Girdinin o an hatalı olduğunu belirten doğruluk durumu niteliği hangisidir?"
  3: "Bu form erişilebilirlik standardı 'doğrudan hata mesajı ilişkilendirmesi (aria-errormessage)' olarak bilinir."
```

---

### html-hard-password-strength-checklist

```yaml
id: html-hard-password-strength-checklist
version: 1
language: html
engine: none
difficulty: hard
title: "Canlı parola kriterleri doğrulama listesi (accessible password checklist)"
prompt: |
  Bir kullanıcı yeni parola belirlerken parolanın taşıması gereken kriterleri (en az 8 karakter,
  en az bir büyük harf, en az bir rakam, en az bir özel karakter) anlık olarak denetleyen
  bir parola alanı tasarlıyorsunuz. Kullanıcı yazdıkça kriter listesindeki maddeler tamamlandı
  olarak işaretlenmektedir. Görme engelli bir kullanıcının hangi kriterlerin sağlandığını ve
  hangilerinin eksik kaldığını dinamik olarak takip edebilmesi için girdi ile kriter listesini
  bağlayın; listenin ekran okuyucuya anlık durum değişikliklerini duyurabilmesi için gerekli
  canlı bölge ve semantik liste yapısını kurun.
constraints:
  - "<input type='password' autocomplete='new-password'> bulunmalı"
  - "Kriterler listesi 'id' ile girdinin 'aria-describedby' niteliğine bağlanmalı"
  - "Kriter listesi veya durum kutusu 'aria-live=\"polite\"' taşımalı"
  - "Her kriter maddesinde tamamlanma durumunu belirten metinsel veya ARIA durumu yer almalı"
concept_tags: [forms, accessibility, security]
checklist_extra:
  - "Yeni parola alanı için autocomplete='new-password' belirtilmiş mi?"
  - "Kriter listesi değişiklikleri kullanıcıyı rahatsız etmeden duyurmak için aria-live='polite' kullanılmış mı?"
reference_solution_path: private/solutions/html-hard-password-strength-checklist.html
hint_ladder:
  1: "Parola yöneticilerinin bu alanın yeni parola üretimi olduğunu anlamasını sağlayan autocomplete değeri nedir?"
  2: "Parola kriterlerinin karşılanma durumunu arka planda seslendirmek için hangi canlı bölge niteliği eklenir?"
  3: "Bu güvenlik arayüzü 'erişilebilir canlı parola kriter listesi (password checklist aria-live)' olarak bilinir."
```

---

### html-hard-drag-drop-file-upload-zone

```yaml
id: html-hard-drag-drop-file-upload-zone
version: 1
language: html
engine: none
difficulty: hard
title: "Erişilebilir sürükle-bırak dosya yükleme alanı (accessible dropzone)"
prompt: |
  Modern web uygulamalarında sıkça görülen 'Dosyaları buraya sürükleyin veya seçmek için tıklayın'
  alanı tasarlıyorsunuz. Sürükle bırak alanları genellikle görme engelliler ve klavye kullanıcıları
  için erişilmez bir tuzağa dönüşür. Bu tasarımı hem fare ile sürüklemeye izin veren hem de
  klavye ile tıklandığında standart dosya seçiciyi açan anlamsal bir `<label>` ve gizlenmiş
  `<input type="file">` kombinasyonuyla inşa edin. Ayrıca seçilen dosyaların listeleneceği
  ve ekran okuyuculara duyurulacağı canlı bir dosya listesi kapsayıcısı ekleyin.
constraints:
  - "<input type='file' multiple> görsel olarak gizlenmeli ancak klavye odağını kaybetmemeli"
  - "Geniş tıklama alanı anlamsal bir <label> olarak input ile eşleşmeli"
  - "Seçilen dosyaların duyurulacağı bir 'aria-live=\"polite\"' liste alanı bulunmalı"
  - "İzin verilen dosya türleri ve boyut kısıtı açıkça metin olarak belirtilmeli"
concept_tags: [forms, accessibility, focus]
checklist_extra:
  - "Input tamamen display:none yapılmak yerine erişilebilir şekilde mi gizlenmiş?"
  - "Seçilen dosyalar listesi için canlı bölge tanımlanmış mı?"
reference_solution_path: private/solutions/html-hard-drag-drop-file-upload-zone.html
hint_ladder:
  1: "Görsel sürükle bırak alanına tıklandığında dosya diyaloğunu açmanın en anlamsal HTML yolu hangi etikettir?"
  2: "Dosya seçildikten sonra listeye eklenen yeni dosyaları ekran okuyucuya bildirmek için ne kullanılır?"
  3: "Bu form bileşeni 'erişilebilir sürükle bırak dosya yükleme bölgesi (accessible dropzone pattern)' olarak bilinir."
```

---

### html-hard-dynamic-form-array-accessible-list

```yaml
id: html-hard-dynamic-form-array-accessible-list
version: 1
language: html
engine: none
difficulty: hard
title: "Dinamik satır eklenip silinen erişilebilir form grubu (repeater pattern)"
prompt: |
  Bir vize başvuru formunda kullanıcının birden fazla çocuk veya seyahat geçmişi ekleyebildiği
  dinamik bir form grubu (repeater / array) tasarlıyorsunuz. Kullanıcı 'Yeni Satır Ekle'
  butonuna bastığında yeni bir satır eklenmekte, her satırda ise o satırı silen bir buton
  yer almaktadır. Ekran okuyucu kullanıcılarının yeni bir satır eklendiğini veya silindiğini
  anında duyabilmesi, ayrıca her 'Sil' butonunun hangi satırı sileceğini net bir şekilde
  ayrıştırabilmesi (örneğin '2. Çocuğu Sil') için gereken erişilebilirlik altyapısını kurun.
constraints:
  - "Satır listesi bir canlı bölge ('aria-live=\"polite\"') içinde veya ona bağlı olmalı"
  - "Her satır anlamsal bir <fieldset> veya rol grubu içine alınmalı"
  - "Her silme butonu hangi satıra ait olduğunu belirten 'aria-label' taşımalı"
  - "Satır ekleme butonu anlamsal ve erişilebilir olmalı"
concept_tags: [forms, accessibility, focus]
checklist_extra:
  - "Silme butonları tek başına belirsiz 'Sil' yerine satır numarasıyla mı etiketlenmiş?"
  - "Dinamik ekleme/çıkarma hareketleri canlı bölge ile ekran okuyucuya aktarılıyor mu?"
reference_solution_path: private/solutions/html-hard-dynamic-form-array-accessible-list.html
hint_ladder:
  1: "Tekrarlayan veri gruplarını form içinde anlamsal olarak ayırmak için hangi HTML etiketi kullanılır?"
  2: "Belirsiz buton metinlerini ekran okuyucuya zenginleştirmek için hangi ARIA özniteliği atanır?"
  3: "Bu dinamik form yapısı 'erişilebilir dinamik satır tekrarlayıcı (accessible repeater pattern)' olarak bilinir."
```

---

### html-hard-wai-aria-menubar-navigation

```yaml
id: html-hard-wai-aria-menubar-navigation
version: 1
language: html
engine: none
difficulty: hard
title: "Masaüstü tipi hiyerarşik menü çubuğu (WAI-ARIA Menubar Pattern)"
prompt: |
  Bir web tabanlı grafik düzenleyicide (örneğin Figma benzeri) üst kısımda yer alan
  'Dosya', 'Düzenle', 'Görünüm' ana menülerini ve bunlara tıklandığında aşağı açılan alt
  menü seçeneklerini kurguluyorsunuz. Standart web sitesi navigasyonundan farklı olarak,
  bu tip masaüstü yazılım benzeri menüler için W3C tarafından tanımlanmış özel menü çubuğu
  rollerini, alt menü sahipliğini ve açılma durumlarını eksiksiz uygulayın.
constraints:
  - "Kök menü kapsayıcısında 'role=\"menubar\"' bulunmalı"
  - "Ana menü tetikleyicilerinde 'role=\"menuitem\"', 'aria-haspopup=\"true\"' ve 'aria-expanded' yer almalı"
  - "Açılan alt menülerde 'role=\"menu\"' ve içindeki maddelerde 'role=\"menuitem\"' bulunmalı"
  - "Dolaşan sekme sırasına uygun tabindex dağılımı yapılmalı"
concept_tags: [navigation, accessibility, focus]
checklist_extra:
  - "Kök gezinme için standart nav yerine masaüstü uygulaması menubar rolü atanmış mı?"
  - "Alt menüleri tetikleyen maddelerde aria-haspopup ve aria-expanded kullanılmış mı?"
reference_solution_path: private/solutions/html-hard-wai-aria-menubar-navigation.html
hint_ladder:
  1: "Masaüstü benzeri yatay uygulama menülerini temsil eden en üst düzey ARIA rolü nedir?"
  2: "Menü çubuğundaki her bir tıklanabilir seçenek hangi role sahip olmalıdır?"
  3: "Bu gelişmiş uygulama menüsü 'WAI-ARIA menü çubuğu deseni (menubar pattern)' olarak bilinir."
```

---

### html-hard-wai-aria-spinbutton-quantity

```yaml
id: html-hard-wai-aria-spinbutton-quantity
version: 1
language: html
engine: none
difficulty: hard
title: "Özel artır/azalt sayısal sayaç bileşeni (WAI-ARIA Spinbutton)"
prompt: |
  Bir e-ticaret sepetinde ürün adetini artırıp azaltmak için tasarlanmış, eksi (-) ve artı (+)
  butonları ile ortasında sayısal değer kutusundan oluşan özel bir miktar seçici (quantity picker)
  oluşturuyorsunuz. Bu üç parçalı görsel bileşeni yardımcı teknolojilere tek bir sayısal sayaç
  bileşeni olarak sunun. Bileşenin minimum (1), maksimum (10) sınırlarını, anlık değerini ve
  klavye ile yukarı/aşağı oklarla değer değiştirilebildiğini bildiren standart ARIA sayaç
  yapısını uygulayın.
constraints:
  - "Sayaç elemanında 'role=\"spinbutton\"' bulunmalı"
  - "'aria-valuemin=\"1\"', 'aria-valuemax=\"10\"' ve 'aria-valuenow' sayısal nitelikleri yer almalı"
  - "'tabindex=\"0\"' ile klavye odağı kabul etmeli"
  - "Artırma ve azaltma butonları anlamsal butonlar olmalı ve açıklayıcı etiket taşımalı"
concept_tags: [forms, accessibility, focus]
checklist_extra:
  - "Sayısal döner sayaç için role='spinbutton' kullanılmış mı?"
  - "Minimum, maksimum ve anlık değerler aria-value* nitelikleri ile eksiksiz tanımlanmış mı?"
reference_solution_path: private/solutions/html-hard-wai-aria-spinbutton-quantity.html
hint_ladder:
  1: "Artırılıp azaltılabilen sayısal giriş kontrollerine hangi WAI-ARIA rolü atanır?"
  2: "Sayacın anlık sayısal durumunu bildiren nitelik hangisidir?"
  3: "Bu etkileşimli sayı denetimi 'WAI-ARIA sayısal sayaç bileşeni (spinbutton)' olarak bilinir."
```

---

### html-hard-csp-nonce-strict-dynamic

```yaml
id: html-hard-csp-nonce-strict-dynamic
version: 1
language: html
engine: none
difficulty: hard
title: "Kriptografik rastgele sayılı katı güvenlik politikası (CSP nonce ve strict-dynamic)"
prompt: |
  Yüksek güvenlikli bir ödeme ağ geçidi sayfasında, XSS saldırılarına karşı beyaz liste
  (allowlist) tabanlı eski CSP yöntemleri yerine modern 'nonce' ve 'strict-dynamic' tabanlı
  katı İçerik Güvenlik Politikasını uygulayın. Sayfadaki meşru script etiketine sunucu tarafından
  üretilmiş kriptografik rastgele sayıyı (nonce) verin; meta etiketinde ise bu nonce değerine
  sahip scriptlerin çocuk scriptler yüklemesine izin veren ancak sahte inline scriptleri
  engelleyen kuralları tanımlayın.
constraints:
  - "<meta http-equiv='Content-Security-Policy' ...> etiketi bulunmalı"
  - "Politikada 'script-src \\'nonce-...\\' \\'strict-dynamic\\'' kuralı yer almalı"
  - "'object-src \\'none\\'' ve 'base-uri \\'none\\'' katı güvenlik kısıtları bulunmalı"
  - "Sayfa içindeki <script> etiketinde aynı 'nonce' niteliği taşınmalı"
concept_tags: [security, standards, performance]
checklist_extra:
  - "Modern dinamik script yüklemelerine izin vermek için strict-dynamic direktifi eklenmiş mi?"
  - "Script etiketi üzerindeki nonce değeri ile meta politikasındaki eşleşiyor mu?"
reference_solution_path: private/solutions/html-hard-csp-nonce-strict-dynamic.html
hint_ladder:
  1: "Her sayfa isteğinde tek kullanımlık üretilen ve scriptlere kimlik doğrulama sağlayan öznitelik nedir?"
  2: "Güvenilen bir scriptin dinamik olarak başka scriptler çağırmasına izin veren CSP direktifi hangisidir?"
  3: "Bu kurumsal güvenlik kuralı 'rastgele sayı tabanlı katı CSP (nonce ve strict-dynamic)' olarak bilinir."
```

---

### html-hard-cross-origin-isolation-headers

```yaml
id: html-hard-cross-origin-isolation-headers
version: 1
language: html
engine: none
difficulty: hard
title: "Çapraz kök izolasyonu ve yüksek çözünürlüklü zamanlayıcı güvenliği (COOP ve COEP)"
prompt: |
  WebAssembly ve çoklu iş parçacığı (Web Workers / SharedArrayBuffer) kullanan yüksek
  performanslı bir tarayıcı içi oyun motoru veya video düzenleyici geliştiriyorsunuz.
  Tarayıcıların Spectre benzeri yan kanal donanım saldırılarını önlemek amacıyla SharedArrayBuffer
  nesnesini kullanabilmesi için sayfanın 'çapraz kök izolasyonu' (cross-origin isolated)
  durumunda olması şarttır. Bu izolasyonu istemci tarafında meta etiketleri aracılığıyla
  sağlayan Cross-Origin Opener Policy ve Cross-Origin Embedder Policy tanımlarını yapın.
constraints:
  - "'http-equiv=\"Cross-Origin-Opener-Policy\"' meta etiketi 'same-origin' ile tanımlanmalı"
  - "'http-equiv=\"Cross-Origin-Embedder-Policy\"' meta etiketi 'require-corp' ile tanımlanmalı"
  - "Etiketler <head> bölümüne yerleştirilmeli"
concept_tags: [security, standards, performance]
checklist_extra:
  - "COOP başlığı için same-origin değeri kullanılmış mı?"
  - "COEP başlığı için require-corp direktifi verilmiş mi?"
reference_solution_path: private/solutions/html-hard-cross-origin-isolation-headers.html
hint_ladder:
  1: "Pencere izolasyonu sağlayıp pencere nesnesi paylaşımını kesen çapraz kök politikası nedir?"
  2: "Sayfadaki tüm dış kaynakların açıkça izin vermesini zorunlu kılan gömücü politikası nedir?"
  3: "Bu ileri güvenlik ortamı 'çapraz kök izolasyonu meta tanımları (COOP ve COEP)' olarak bilinir."
```

---

### html-hard-wai-aria-datagrid-interactive

```yaml
id: html-hard-wai-aria-datagrid-interactive
version: 1
language: html
engine: none
difficulty: hard
title: "İki boyutlu etkileşimli veri ızgarası (WAI-ARIA DataGrid Pattern)"
prompt: |
  Bir e-tablo (spreadsheet) veya interaktif CRM tablosunda kullanıcıların klavye ok tuşlarıyla
  hücreler arasında iki boyutlu olarak serbestçe gezebildiği, satırları seçebildiği ve hücre
  içinde düzenleme yapabildiği bir veri ızgarası (DataGrid) tasarlıyorsunuz. Standart statik
  tablolardan farklı olarak, W3C Grid deseni standartlarına uygun ızgara, satır ve hücre
  rollerini uygulayın; o an odaklanılmış hücrede 'tabindex="0"', diğer hücrelerde ise
  'tabindex="-1"' tutarak iki boyutlu dolaşan sekme indeksini kurun.
constraints:
  - "Tablo veya kapsayıcıda 'role=\"grid\"' bulunmalı"
  - "Satırlarda 'role=\"row\"' yer almalı"
  - "Başlıklarda 'role=\"columnheader\"' ve veri hücrelerinde 'role=\"gridcell\"' bulunmalı"
  - "Aktif hücrede 'tabindex=\"0\"', diğerlerinde 'tabindex=\"-1\"' yer almalı"
  - "Seçili satırda 'aria-selected=\"true\"' belirtilmeli"
concept_tags: [tables, accessibility, focus]
checklist_extra:
  - "Statik tablo yerine etkileşimli kontrol için role='grid' atanmış mı?"
  - "Veri hücreleri standart td yerine gridcell rolüyle tanımlanmış mı?"
reference_solution_path: private/solutions/html-hard-wai-aria-datagrid-interactive.html
hint_ladder:
  1: "Hücreler arasında klavye ok tuşlarıyla dolaşılabilen etkileşimli tablolara hangi ARIA rolü atanır?"
  2: "Grid içindeki düzenlenebilir veri hücrelerine hangi rol verilir?"
  3: "Bu ileri arayüz bileşeni 'WAI-ARIA etkileşimli veri ızgarası (grid ve gridcell pattern)' olarak bilinir."
```

---

### html-hard-wai-aria-feed-infinite-scroll

```yaml
id: html-hard-wai-aria-feed-infinite-scroll
version: 1
language: html
engine: none
difficulty: hard
title: "Sonsuz kaydırmalı erişilebilir içerik akışı (WAI-ARIA Feed Pattern)"
prompt: |
  Bir sosyal medya uygulamasında kullanıcının aşağı kaydırdıkça yeni gönderilerin otomatik
  yüklendiği bir içerik akışı (feed) geliştiriyorsunuz. Sonsuz kaydırma mekanizmaları klavye
  ve ekran okuyucu kullanıcıları için altbilgiye (footer) ulaşmayı imkansız kıldığı için
  erişilebilirlik felaketine dönüşebilir. W3C tarafından bu tür dinamik akışlar için özel
  olarak tanımlanan akış rolünü, akışın o anda yeni içerik yükleyip yüklemediğini bildiren
  meşguliyet durumunu ve her gönderinin anlamsal bağımsız makale yapısını kurgulayın.
constraints:
  - "Akış kapsayıcısında 'role=\"feed\"' ve 'aria-label' bulunmalı"
  - "Yeni içerik yüklenirken 'aria-busy=\"true\"' durumu yer almalı"
  - "Akış içindeki her gönderi 'role=\"article\"' ve 'aria-labelledby' taşımalı"
  - "Kullanıcının akış dışına atlayabilmesi için akış öncesi veya sonrası bir navigasyon ipucu bulunmalı"
concept_tags: [accessibility, semantics, focus]
checklist_extra:
  - "Sonsuz akışlar için WAI-ARIA role='feed' kullanılmış mı?"
  - "Yükleme anındaki durumu bildirmek için aria-busy niteliği eklenmiş mi?"
reference_solution_path: private/solutions/html-hard-wai-aria-feed-infinite-scroll.html
hint_ladder:
  1: "Sonsuz kaydırmalı dinamik gönderi listelerini sarmak için hangi özel ARIA rolü kullanılır?"
  2: "Bir bileşenin o an yeni veriler indirip güncellendiğini ekran okuyucuya bildiren nitelik nedir?"
  3: "Bu sosyal medya arayüz yapısı 'WAI-ARIA içerik akışı deseni (feed ve aria-busy)' olarak bilinir."
```

---

### html-hard-accessible-dual-thumb-range-slider

```yaml
id: html-hard-accessible-dual-thumb-range-slider
version: 1
language: html
engine: none
difficulty: hard
title: "Çift tutamaçlı erişilebilir fiyat aralığı seçici (dual thumb slider)"
prompt: |
  Bir alışveriş sitesinde minimum ve maksimum fiyat aralığını (örneğin 100 TL ile 5000 TL arası)
  belirlemek için kullanılan iki tutamaçlı (çift başlı) özel bir aralık kaydırıcısı tasarlıyorsunuz.
  Her iki tutamacın da bağımsız olarak klavyeden odaklanabilmesini ve kontrol edilebilmesini
  sağlayın. Birinci tutamacın 'Minimum Fiyat', ikinci tutamacın 'Maksimum Fiyat' olduğunu
  belirten erişilebilir isimleri, her ikisinin anlık değerini ve insan dostu para birimi
  metinlerini (örn: 'En düşük 250 Türk Lirası') eksiksiz tanımlayın.
constraints:
  - "İki ayrı eleman üzerinde 'role=\"slider\"' bulunmalı"
  - "Her iki slider da 'tabindex=\"0\"' ile odaklanabilir olmalı"
  - "Biri 'aria-label=\"Minimum Fiyat\"', diğeri 'aria-label=\"Maksimum Fiyat\"' taşımalı"
  - "'aria-valuemin', 'aria-valuemax', 'aria-valuenow' ve 'aria-valuetext' eksiksiz girilmeli"
concept_tags: [accessibility, focus, forms]
checklist_extra:
  - "İki ayrı tutamaç da bağımsız slider rollerine ve etiketlerine sahip mi?"
  - "Para birimiyle birlikte insan tarafından anlaşılır aria-valuetext sağlanmış mı?"
reference_solution_path: private/solutions/html-hard-accessible-dual-thumb-range-slider.html
hint_ladder:
  1: "Çift taraflı aralık seçiminde her iki kontrol noktasına hangi ARIA rolü atanır?"
  2: "Tutamakların hangi sınır değerini temsil ettiğini ayırt etmek için ne kullanılır?"
  3: "Bu gelişmiş filtreleme bileşeni 'çift tutamaçlı erişilebilir aralık seçici (dual range slider)' olarak bilinir."
```

---

### html-hard-permissions-policy-meta

```yaml
id: html-hard-permissions-policy-meta
version: 1
language: html
engine: none
difficulty: hard
title: "İstemci taraflı tarayıcı donanım izinleri kısıtlaması (Permissions Policy meta)"
prompt: |
  Hassas bir finansal işlem sayfasında veya kurumsal portaldaki iframe ve harici scriptlerin
  kullanıcının kamerasını, mikrofonunu ve coğrafi konumunu (geolocation) izinsiz olarak
  kullanmasını kesin olarak yasaklamak istiyorsunuz. Bu kısıtlamayı doğrudan sayfanın
  `<head>` bölümünde standart İzin Politikası (Permissions Policy / eski adıyla Feature Policy)
  etiketiyle tanımlayarak, bu donanım özelliklerinin kök sayfa dahil hiçbir kaynak tarafından
  erişilememesini sağlayın.
constraints:
  - "<meta http-equiv='Permissions-Policy' ...> etiketi bulunmalı"
  - "content içinde 'camera=()', 'microphone=()' ve 'geolocation=()' tanımlanmalı"
  - "Politika boş parantezlerle tüm köklere kapalı olarak belirtilmeli"
  - "Etiket <head> bölümüne yerleştirilmeli"
concept_tags: [security, standards, performance]
checklist_extra:
  - "Özelliklerin tamamen kapatılması için boş parantez sözdizimi kullanılmış mı?"
  - "http-equiv değeri Permissions-Policy olarak doğru yazılmış mı?"
reference_solution_path: private/solutions/html-hard-permissions-policy-meta.html
hint_ladder:
  1: "Tarayıcıda kamera ve konum gibi donanım özelliklerine erişimi kısıtlayan güncel güvenlik politikası nedir?"
  2: "Bir özelliğin hiçbir kök tarafından kullanılamayacağını belirtmek için politikada hangi sembol kullanılır?"
  3: "Bu tarayıcı donanım kısıtlaması 'İzin Politikası direktifi (Permissions Policy meta)' olarak bilinir."
```

---

### html-hard-wai-aria-listbox-multiselect

```yaml
id: html-hard-wai-aria-listbox-multiselect
version: 1
language: html
engine: none
difficulty: hard
title: "Çoklu seçimli özel liste kutusu bileşeni (WAI-ARIA Multiselect Listbox)"
prompt: |
  Bir görev yönetim uygulamasında kullanıcıların bir göreve birden fazla etiket (örneğin 'Frontend',
  'Erişilebilirlik', 'Kritik Hata') atayabildiği özel bir çoklu seçim liste kutusu (listbox)
  geliştiriyorsunuz. W3C standartlarına uygun olarak listenin çoklu seçime izin verdiğini,
  hangi etiketlerin seçili olduğunu, klavye ile liste öğeleri arasında nasıl gezinileceğini
  ve seçili öğe sayısını ekran okuyuculara aktaran tam teşekküllü ARIA yapısını kurun.
constraints:
  - "Kapsayıcıda 'role=\"listbox\"' ve 'aria-multiselectable=\"true\"' bulunmalı"
  - "Seçeneklerde 'role=\"option\"' ve seçilme durumunu belirten 'aria-selected' bulunmalı"
  - "Klavye erişilebilirliği için dolaşan sekme sırası veya 'aria-activedescendant' kullanılmalı"
  - "Liste açıklayıcı bir başlığa 'aria-labelledby' ile bağlanmalı"
concept_tags: [accessibility, focus, forms]
checklist_extra:
  - "Çoklu seçimi bildirmek için aria-multiselectable='true' kullanılmış mı?"
  - "Her seçeneğin seçilme durumu aria-selected ile açıkça işaretlenmiş mi?"
reference_solution_path: private/solutions/html-hard-wai-aria-listbox-multiselect.html
hint_ladder:
  1: "Bir liste kutusunun birden çok öğe seçimine izin verdiğini belirten ARIA niteliği hangisidir?"
  2: "Liste kutusu seçeneklerinin seçili olup olmadığını hangi durum niteliği gösterir?"
  3: "Bu arayüz bileşeni 'çoklu seçimli liste kutusu deseni (multiselect listbox pattern)' olarak bilinir."
```

---

### html-hard-accessible-drag-drop-reorderable-list

```yaml
id: html-hard-accessible-drag-drop-reorderable-list
version: 1
language: html
engine: none
difficulty: hard
title: "Klavyeyle yeniden sıralanabilir erişilebilir liste (reorderable list aria-roledescription)"
prompt: |
  Kullanıcıların maddeleri fare ile tutup sürükleyerek sıralayabildiği bir yapılacaklar
  listesi hazırlıyorsunuz. Ancak bu yapının görme engelliler ve yalnızca klavye kullananlar
  için de tamamen çalışır olması gerekmektedir. Listenin özel bir sıralanabilir liste olduğunu
  ekran okuyucuya tanıtın, her maddenin o anki konumunu (örn: '1 / 5') ve klavye kısayollarını
  (Boşluk ile tut, yukarı/aşağı oklarla taşı, Enter ile bırak) anlatan yönergeleri bağlayın.
  Sıralama değiştiğinde sonucu duyuracak canlı bölgeyi ekleyin.
constraints:
  - "Listede 'aria-roledescription=\"sıralanabilir liste\"' veya benzeri açıklama bulunmalı"
  - "Her listede 'role=\"listitem\"' ve 'tabindex=\"0\"' bulunmalı"
  - "Klavye talimatları 'aria-describedby' ile öğelere bağlanmalı"
  - "Sıralama değişimlerini duyuran 'aria-live=\"polite\"' canlı bölgesi yer almalı"
concept_tags: [accessibility, lists, focus]
checklist_extra:
  - "Özel liste davranışı aria-roledescription ile açıklanmış mı?"
  - "Sıralama değişikliğini seslendiren canlı bölge kurulmuş mu?"
reference_solution_path: private/solutions/html-hard-accessible-drag-drop-reorderable-list.html
hint_ladder:
  1: "Standart bir HTML elemanının rolünün ekran okuyucu tarafından Türkçe özel bir terimle okunmasını sağlayan nitelik nedir?"
  2: "Öğe taşındığında yeni pozisyonunu ekran okuyucuya aktarmak için hangi dinamik bölge kullanılır?"
  3: "Bu ileri düzey erişilebilirlik yapısı 'klavye erişilebilir yeniden sıralama listesi (reorderable list)' olarak bilinir."
```

---

### html-hard-jsonld-organization-localbusiness

```yaml
id: html-hard-jsonld-organization-localbusiness
version: 1
language: html
engine: none
difficulty: hard
title: "Yerel işletme ve harita koordinatları şeması (JSON-LD LocalBusiness)"
prompt: |
  Bir restoran zincirinin şube sayfası için Google Haritalar ve yerel arama sonuçlarında
  (Google Maps / Local Pack) öne çıkmasını sağlayacak yapılandırılmış veriyi hazırlayın.
  JSON-LD formatında, Schema.org 'Restaurant' (veya 'LocalBusiness') türünü kullanarak;
  işletme adı, açık sokak adresi, coğrafi koordinatları (enlem ve boylam), telefon numarası
  ve haftalık açılış-kapanış saatlerini içeren eksiksiz bir blok oluşturun.
constraints:
  - "<script type='application/ld+json'> kullanılmalı"
  - "'@type': 'Restaurant' veya 'LocalBusiness' tanımlanmalı"
  - "'address' nesnesi (PostalAddress) ve 'geo' nesnesi (GeoCoordinates: latitude, longitude) bulunmalı"
  - "'openingHoursSpecification' dizisi altında haftalık çalışma saatleri tanımlanmalı"
concept_tags: [standards, semantics, performance]
checklist_extra:
  - "Coğrafi koordinatlar geo nesnesi altında doğru yazılmış mı?"
  - "Çalışma saatleri openingHoursSpecification ile yapılandırılmış mı?"
reference_solution_path: private/solutions/html-hard-jsonld-organization-localbusiness.html
hint_ladder:
  1: "Arama motorlarına fiziksel dükkan ve işletme bilgilerini aktaran ana Schema.org tipi nedir?"
  2: "Harita konumunu kesin olarak belirtmek için kullanılan enlem ve boylam nesnesi hangisidir?"
  3: "Bu yerel SEO şeması 'JSON-LD yerel işletme yapılandırılmış verisi (LocalBusiness Schema)' olarak bilinir."
```

---

### html-hard-responsive-image-focal-point-object-fit

```yaml
id: html-hard-responsive-image-focal-point-object-fit
version: 1
language: html
engine: none
difficulty: hard
title: "LCP optimizasyonlu yüksek öncelikli kahraman görseli (fetchpriority ve picture)"
prompt: |
  Bir haber sitesinin manşet sayfasındaki en büyük görsel (LCP elemanı) için ultra performanslı
  bir HTML yapısı kurun. Görselin sayfa yüklenirken tarayıcının ağ kuyruğunda diğer tüm kaynakların
  önüne geçmesi için en yüksek öncelikle çekilmesini sağlayın. Masaüstü ve mobil ekranlar için
  iki ayrı AVIF/WebP kaynağı tanımlayın. Düzen kaymasını (CLS) sıfıra indirmek amacıyla görselin
  özgün en-boy oranını (aspect-ratio) koruyan genişlik ve yükseklik değerlerini tanımlayın.
constraints:
  - "<picture> kapsayıcısı ve <source> elemanları kullanılmalı"
  - "<img> elemanında 'fetchpriority=\"high\"' niteliği bulunmalı"
  - "<img> elemanında 'loading=\"eager\"' yer almalı (lazy olmamalı)"
  - "Genişlik ve yükseklik (width ve height) piksel değerleri tanımlı olmalı"
concept_tags: [images, performance, standards]
checklist_extra:
  - "LCP kahraman görselinde loading='lazy' yerine eager mı kullanılmış?"
  - "Tarayıcıya kaynak önceliğini bildirmek için fetchpriority='high' eklenmiş mi?"
reference_solution_path: private/solutions/html-hard-responsive-image-focal-point-object-fit.html
hint_ladder:
  1: "Tarayıcının bir kaynağı ağ kuyruğunda en öne almasını sağlayan yeni HTML niteliği nedir?"
  2: "Ekranın en üstündeki kritik görselin gecikmeden hemen indirilmesi için loading niteliğine ne verilir?"
  3: "Bu performans optimizasyonu 'en büyük boyama görseli önceliklendirmesi (fetchpriority high LCP)' olarak bilinir."
```

---

### html-hard-dialog-showmodal-backdrop-keyboard

```yaml
id: html-hard-dialog-showmodal-backdrop-keyboard
version: 1
language: html
engine: none
difficulty: hard
title: "Odak kilitli ve kapatma olaylı yerel modal pencere (dialog modal trap)"
prompt: |
  Bir web uygulamasında kullanıcının hesap güvenliği ayarlarını değiştirdiği yerel bir modal
  iletişim kutusu kurgulayın. HTML5 dialog elemanını kullanarak, pencerenin arkasındaki içeriğin
  yardımcı teknolojiler ve klavye tarafından erişilemez hale gelmesini (inert davranışı) sağlayacak
  yapıyı kurun. Modal açıldığında odağın ilk girdi kutusuna otomatik gitmesini, pencere
  içinde kullanıcı Esc tuşuna bastığında tetiklenecek kapatma formunu ve modalın erişilebilir
  başlık/açıklama bağlantılarını yapılandırın.
constraints:
  - "<dialog> elemanında 'aria-labelledby' ve 'aria-describedby' bulunmalı"
  - "Modal içindeki ilk etkileşimli elemanda 'autofocus' bulunmalı"
  - "Modalı kapatmak için 'method=\"dialog\"' form yapısı yer almalı"
  - "Arka plan karartması için modern CSS ::backdrop hedeflenebilir yapıda olmalı"
concept_tags: [dialogs, accessibility, focus]
checklist_extra:
  - "İlk girdi kutusuna otomatik odaklanma için autofocus eklenmiş mi?"
  - "Kapatma eylemi method='dialog' ile ilişkilendirilmiş mi?"
reference_solution_path: private/solutions/html-hard-dialog-showmodal-backdrop-keyboard.html
hint_ladder:
  1: "Bir dialog açıldığında odağın doğrudan ilk öğeye düşmesini sağlayan HTML özniteliği nedir?"
  2: "Dialog elemanının arkasındaki karartma katmanını stillendiren CSS sözde elemanı nedir?"
  3: "Bu yerel modal yapısı 'odak kilitli yerel modal iletişim kutusu (HTML5 dialog modal)' olarak bilinir."
```

---

### html-hard-wai-aria-treegrid-hierarchical-table

```yaml
id: html-hard-wai-aria-treegrid-hierarchical-table
version: 1
language: html
engine: none
difficulty: hard
title: "Hiyerarşik açılır kapanır ağaç ızgarası (WAI-ARIA Treegrid Pattern)"
prompt: |
  Bir kurumsal bütçe raporunda departmanların, alt departmanların ve harcama kalemlerinin
  hem tablo sütunları (bütçe, harcanan, kalan) hem de açılıp kapanabilen bir hiyerarşik ağaç
  şeklinde sunulduğu bir Ağaç Izgarası (TreeGrid) tasarlıyorsunuz. W3C Treegrid deseni
  kurallarına göre; tablonun rolünü, açılır satırların derinlik seviyesini (level), kaçıncı
  kardeş öğe olduğunu ve açık/kapalı durumunu bildiren durum niteliklerini uygulayın.
constraints:
  - "Kapsayıcıda 'role=\"treegrid\"' bulunmalı"
  - "Satırlarda 'role=\"row\"', 'aria-level' ve 'aria-expanded' yer almalı"
  - "Açılır düğümün altındaki eleman sayısını bildiren 'aria-setsize' ve 'aria-posinset' bulunmalı"
  - "Hücrelerde 'role=\"gridcell\"' veya 'role=\"columnheader\"' yer almalı"
concept_tags: [tables, accessibility, focus]
checklist_extra:
  - "Hiyerarşik tablo için treegrid rolü atanmış mı?"
  - "Ağaç derinliği aria-level niteliği ile sayısal olarak belirtilmiş mi?"
reference_solution_path: private/solutions/html-hard-wai-aria-treegrid-hierarchical-table.html
hint_ladder:
  1: "Hem tablo sütunlarına hem de iç içe ağaç dallanmasına sahip karmaşık bileşenin ARIA rolü nedir?"
  2: "Bir satırın ağaç içindeki derinlik katmanını (1. seviye, 2. seviye vb.) bildiren nitelik hangisidir?"
  3: "Bu kurumsal veri bileşeni 'WAI-ARIA hiyerarşik ağaç ızgarası (treegrid pattern)' olarak bilinir."
```

---

### html-hard-wai-aria-breadcrumb-rich-snippets-hybrid

```yaml
id: html-hard-wai-aria-breadcrumb-rich-snippets-hybrid
version: 1
language: html
engine: none
difficulty: hard
title: "Hibrit ekmek kırıntısı navigasyonu ve arama şeması (Breadcrumb nav ve Microdata)"
prompt: |
  Bir e-ticaret sitesinde (Ana Sayfa > Elektronik > Bilgisayarlar > Dizüstü) gezinti yolunu
  hem yardımcı teknolojiler için tam erişilebilir kılın hem de Google arama sonuçlarında
  sayfa bağlantısının üstünde zengin ekmek kırıntısı URL'si olarak çıkmasını sağlayın.
  Aynı HTML yapısı üzerinde hem WAI-ARIA navigasyon standartlarını (`<nav>`, `aria-current="page"`)
  hem de Schema.org 'BreadcrumbList' ve 'ListItem' Microdata özniteliklerini (`itemscope`,
  `itemtype`, `itemprop="itemListElement"`, `itemprop="position"`) bir arada harmanlayın.
constraints:
  - "<nav aria-label='...'> içinde <ol itemscope itemtype='https://schema.org/BreadcrumbList'> bulunmalı"
  - "Her <li> içinde 'itemprop=\"itemListElement\"' ve 'itemtype=\"https://schema.org/ListItem\"' yer almalı"
  - "Öğe sıralaması için '<meta itemprop=\"position\" content=\"1\">' bulunmalı"
  - "Son öğede 'aria-current=\"page\"' yer almalı"
concept_tags: [navigation, semantics, accessibility]
checklist_extra:
  - "Aynı navigasyon yapısında hem ARIA erişilebilirliği hem Schema Microdata birleştirilmiş mi?"
  - "Her liste maddesinin sayısal position meta etiketi bulunuyor mu?"
reference_solution_path: private/solutions/html-hard-wai-aria-breadcrumb-rich-snippets-hybrid.html
hint_ladder:
  1: "Arama motorlarına ekmek kırıntısı sıralamasını bildiren Schema.org tipi nedir?"
  2: "Her bir ekmek kırıntısı basamağının sırasını gösteren Microdata meta özelliği hangisidir?"
  3: "Bu ikili entegrasyon 'hibrit ekmek kırıntısı gezinti ve arama şeması (BreadcrumbList Microdata)' olarak bilinir."
```

---

### html-hard-dynamic-live-region-status-polite-assertive

```yaml
id: html-hard-dynamic-live-region-status-polite-assertive
version: 1
language: html
engine: none
difficulty: hard
title: "İki kademeli dinamik canlı bölge mimarisi (Dual live region: polite ve assertive)"
prompt: |
  Büyük bir web uygulamasında sayfa geneline hizmet veren merkezi bir bildirim motoru
  tasarlıyorsunuz. Önemsiz arka plan güncellemelerinin (örneğin 'Taslak kaydedildi') kullanıcıyı
  bölmeden o anki okuma bittikten sonra sakin bir şekilde okunması, ancak kritik acil durumların
  (örneğin 'Oturumunuz 1 dakika içinde kapanacak!') kullanıcının yaptığı her şeyi keserek
  anında duyurulması gerekmektedir. Bu iki farklı bildirim tipini tek bir ekranda yöneten,
  ekran okuyuculardan görsel olarak gizlenmiş iki ayrı canlı bölge kapsayıcısını kurun.
constraints:
  - "Sakin bildirimler için 'aria-live=\"polite\"' ve 'role=\"status\"' kapsayıcısı yer almalı"
  - "Acil bildirimler için 'aria-live=\"assertive\"' ve 'role=\"alert\"' kapsayıcısı yer almalı"
  - "Her iki kapsayıcıda da 'aria-atomic=\"true\"' niteliği bulunmalı"
  - "Bölgeler görsel olarak gizli (sr-only sınıfı) fakat erişilebilir olmalı"
concept_tags: [accessibility, standards, focus]
checklist_extra:
  - "Polite ve assertive bölgeleri iki ayrı kapsayıcı olarak ayrıştırılmış mı?"
  - "Mesajların yarım kalmaması için aria-atomic='true' tanımlanmış mı?"
reference_solution_path: private/solutions/html-hard-dynamic-live-region-status-polite-assertive.html
hint_ladder:
  1: "Acil olan ve olmayan bildirimleri ekran okuyucuya iletirken kullanılan iki temel aria-live modu nedir?"
  2: "İçerik değiştiğinde eski ve yeni metnin birbirine karışmadan tek seferde okunması için ne yazılır?"
  3: "Bu mimari desen 'çift kademeli erişilebilir canlı bildirim bölgesi (dual live region)' olarak bilinir."
```

---

### html-hard-wai-aria-nested-disclosure-panels

```yaml
id: html-hard-wai-aria-nested-disclosure-panels
version: 1
language: html
engine: none
difficulty: hard
title: "Çok katmanlı iç içe açılır kapanır panel hiyerarşisi (nested disclosure)"
prompt: |
  Kapsamlı bir teknik dokümantasyon merkezinde, ana konuların altında alt başlıkların ve
  onların da altında detay maddelerinin yer aldığı üç düzeyli iç içe açılır/kapanır
  (nested disclosure) bir yapı kuruyorsunuz. Her düzeydeki başlık hiyerarşisini (h2, h3, h4)
  bozmadan koruyun. Her tetikleyici butonun yalnızca kendi doğrudan alt panelini açıp
  kapattığını belirten 'aria-controls' ve 'aria-expanded' durumlarını uygulayın; ayrıca
  panellerin ait oldukları başlıkları 'aria-labelledby' ile ilişkilendirin.
constraints:
  - "Başlık hiyerarşisi (<h2>, <h3> vb.) atlama yapılmadan korunmalı"
  - "Her tetikleyici butonda 'aria-expanded' ve ilgili panelin id'sini gösteren 'aria-controls' bulunmalı"
  - "Açılan panellerde 'role=\"region\"' ve tetikleyiciye işaret eden 'aria-labelledby' bulunmalı"
  - "İç içe en az iki seviye açılır panel yapısı yer almalı"
concept_tags: [accessibility, semantics, focus]
checklist_extra:
  - "Tetikleyici butonlar doğrudan başlık etiketlerinin içine mi yerleştirilmiş?"
  - "Her alt panel kendi tetikleyicisinin kimliğiyle aria-labelledby üzerinden eşleştirilmiş mi?"
reference_solution_path: private/solutions/html-hard-wai-aria-nested-disclosure-panels.html
hint_ladder:
  1: "Açılır panellerin birer anlamsal bölge olarak tanınması için hangi ARIA rolü atanır?"
  2: "İç içe panellerde başlık etiketlerinin derinlik sırası nasıl korunmalıdır?"
  3: "Bu hiyerarşik bileşen 'iç içe açılır kapanır panel mimarisi (nested disclosure pattern)' olarak bilinir."
```

---

### html-hard-form-multi-page-wizard-session

```yaml
id: html-hard-form-multi-page-wizard-session
version: 1
language: html
engine: none
difficulty: hard
title: "Oturum korumalı çok adımlı sihirbaz formu (multi-step form wizard)"
prompt: |
  Bir sigorta poliçesi hesaplama sürecinin 2. adımına (Araç Detayları) ait form sayfasını
  tasarlıyorsunuz. Sayfa yenilendiğinde veya sunucuya gönderim yapıldığında kullanıcının 1. adımda
  girdiği verilerin ve geçerli oturum belirtecinin kaybolmaması için gizli girdi alanları
  (hidden inputs) yerleştirin. Formun en üstünde adım göstergesi (stepper), form gövdesinde
  araç bilgileri alan grubu, altında ise hem 'Geri Dön (1. Adım)' hem de 'Devam Et (3. Adım)'
  eylem butonlarını içeren tam anlamsal formu kurgulayın.
constraints:
  - "<form method='post'> içinde CSRF ve önceki adım verileri için <input type='hidden'> alanları bulunmalı"
  - "Adım navigasyonu için 'aria-current=\"step\"' taşıyan sıralı liste yer almalı"
  - "Form alanları <fieldset> ve <legend> ile gruplanmalı"
  - "Geri ve İleri eylemleri anlamsal butonlar ile yapılandırılmalı"
concept_tags: [forms, security, navigation]
checklist_extra:
  - "Güvenlik token'ı ve oturum durumu için gizli girdi (input type hidden) kullanılmış mı?"
  - "Mevcut adım aria-current='step' ile net biçimde işaretlenmiş mi?"
reference_solution_path: private/solutions/html-hard-form-multi-page-wizard-session.html
hint_ladder:
  1: "Kullanıcıya gösterilmeden arka planda taşınması gereken durum verileri hangi input türünde saklanır?"
  2: "Sihirbaz adımlarında aktif adımı bildirmek için aria-current hangi değere ayarlanır?"
  3: "Bu aşamalı form deseni 'çok adımlı sihirbaz formu (multi-step wizard pattern)' olarak bilinir."
```

---

### html-hard-accessible-code-diff-viewer

```yaml
id: html-hard-accessible-code-diff-viewer
version: 1
language: html
engine: none
difficulty: hard
title: "Erişilebilir kod farkı ve değişiklik görüntüleyicisi (semantic code diff)"
prompt: |
  GitHub veya GitLab benzeri bir platformda iki kod sürümü arasındaki farkları gösteren bir
  satır içi fark (diff viewer) bileşeni oluşturun. Silinen satırlar kırmızı, eklenen satırlar
  yeşil arka planla gösterilecektir. Ancak renk körü veya görme engelli bir yazılımcının
  hangi satırın silindiğini ve hangi satırın eklendiğini yalnızca renge bağımlı olmadan
  anlayabilmesi için; eklenen içerikleri `<ins>`, silinen içerikleri `<del>` anlamsal etiketleri
  ile sarın ve ekran okuyucular için metinsel durum belirteçleri ekleyin.
constraints:
  - "Silinen satırlarda <del> etiketi kullanılmalı"
  - "Eklenen satırlarda <ins> etiketi kullanılmalı"
  - "Ekran okuyucular için gizli metinle (sr-only) 'Satır eklendi:', 'Satır silindi:' ifadeleri yer almalı"
  - "Kod parçası <pre><code> içinde anlamsal olarak korunmalı"
concept_tags: [semantics, accessibility, standards]
checklist_extra:
  - "Yalnızca CSS renklerine dayanmak yerine anlamsal ins ve del etiketleri kullanılmış mı?"
  - "Değişiklik türü ekran okuyucular için metinsel olarak açıkça duyurulmuş mu?"
reference_solution_path: private/solutions/html-hard-accessible-code-diff-viewer.html
hint_ladder:
  1: "HTML'de bir belgeden silinen metni anlamsal olarak temsil eden etiket nedir?"
  2: "Belgeye sonradan eklenen metinleri anlamsal olarak işaretleyen etiket hangisidir?"
  3: "Bu anlamsal fark yapısı 'erişilebilir kod farkı görüntüleyicisi (semantic diff ins and del)' olarak bilinir."
```

---

### html-hard-video-interactive-cue-chapters

```yaml
id: html-hard-video-interactive-cue-chapters
version: 1
language: html
engine: none
difficulty: hard
title: "Bölüm işaretleyicili ve interaktif fihristli video (video track chapters)"
prompt: |
  Bir saatlik uzun bir konferans konuşması videosunda kullanıcıların belirli konulara doğrudan
  atlayabilmesi için WebVTT bölümleme standardını uygulayın. Video içine bölümleri tanımlayan
  bir `<track>` etiketi bağlayın. Ayrıca oynatıcının hemen yanında veya altında, kullanıcıların
  tıklayarak doğrudan ilgili dakikaya gidebileceği, süre bilgisi ve bölüm başlığı içeren
  erişilebilir bir bölüm fihristi (bölüm menüsü) inşa edin.
constraints:
  - "<video controls> içinde '<track kind=\"chapters\" ...>' etiketi yer almalı"
  - "Bölüm parçasında 'srclang' ve kaynak .vtt dosya yolu bulunmalı"
  - "Bölüm menüsü bir <nav> ve anlamsal liste (ol veya ul) içinde yapılandırılmalı"
  - "Her bölüm maddesinde zaman bilgisi ve bölüm adı yer almalı"
concept_tags: [standards, accessibility, navigation]
checklist_extra:
  - "track etiketinin türü kind='chapters' olarak ayarlanmış mı?"
  - "Bölüm gezinme fihristi anlamsal bir nav etiketiyle çevrelenmiş mi?"
reference_solution_path: private/solutions/html-hard-video-interactive-cue-chapters.html
hint_ladder:
  1: "Videolarda bölümleri ve konu başlıklarını tanımlamak için track kind niteliğine ne yazılır?"
  2: "Video bölümlerini listeleyen gezinme menüsü hangi HTML5 etiketi içine alınmalıdır?"
  3: "Bu video standardı 'video bölüm işaretleyicisi ve fihristi (video track chapters)' olarak bilinir."
```

---

### html-hard-microdata-event-schedule

```yaml
id: html-hard-microdata-event-schedule
version: 1
language: html
engine: none
difficulty: hard
title: "Etkinlik ve bilet satış şeması (Microdata Event, Location ve Offer)"
prompt: |
  Bir teknoloji konferansının etkinlik bilet satış sayfasında, etkinliğin Google Etkinlikler
  (Google Events) arama panelinde tarih, saat, mekan ve bilet fiyatı ile birlikte doğrudan
  çıkmasını sağlayacak Microdata şemasını HTML elemanlarına giydirin. Konferansı 'Event'
  türü olarak tanımlayın; başlangıç ve bitiş tarihlerini makinece okunabilir `<time>` elemanlarıyla
  bağlayın; fiziksel mekan (Place) ve bilet fiyat teklifi (Offer) alt nesnelerini kurgulayın.
constraints:
  - "Ana blokta 'itemscope itemtype=\"https://schema.org/Event\"' bulunmalı"
  - "Tarihlerde '<time itemprop=\"startDate\" datetime=\"...\">' yer almalı"
  - "'itemprop=\"location\"' altında 'itemtype=\"https://schema.org/Place\"' bulunmalı"
  - "'itemprop=\"offers\"' altında 'itemtype=\"https://schema.org/Offer\"' ve fiyat bilgisi yer almalı"
concept_tags: [semantics, standards, performance]
checklist_extra:
  - "Tarih bilgileri ISO 8601 formatında time datetime etiketleriyle mi verilmiş?"
  - "Mekan ve teklif nesneleri iç içe itemscope yapılarıyla ayrıştırılmış mı?"
reference_solution_path: private/solutions/html-hard-microdata-event-schedule.html
hint_ladder:
  1: "Etkinlik ve konferansları arama motorlarına bildiren Schema.org kök türü nedir?"
  2: "Etkinlik mekanını ve adresini tanımlayan iç içe yer türü hangisidir?"
  3: "Bu yapılandırılmış veri entegrasyonu 'HTML5 etkinlik mikro verisi (Microdata Event schema)' olarak bilinir."
```

---

### html-hard-wai-aria-tabpanel-dynamic-lazyload

```yaml
id: html-hard-wai-aria-tabpanel-dynamic-lazyload
version: 1
language: html
engine: none
difficulty: hard
title: "Gecikmeli yüklenen sekmeli panel ve meşguliyet durumu (aria-busy tabpanel)"
prompt: |
  Bir analitik gösterge panelinde sekmeler arasında geçiş yapıldığında, seçilen sekmenin
  verileri sunucudan AJAX ile asenkron olarak indirilmektedir. Sekme tıklandığında içerik
  paneline henüz veri gelmemişken ekran okuyucunun içeriği yarım yamalak veya boş seslendirmesini
  engellemek; yükleme tamamlandığında ise yeni içeriğin eksiksiz okunmasını sağlamak için
  panelin yükleme halinde olduğunu bildiren durum niteliklerini ve iskelet (skeleton)
  yükleme göstergesini yapılandırın.
constraints:
  - "İçerik panelinde 'role=\"tabpanel\"' ve 'aria-labelledby' bulunmalı"
  - "Yükleme devam ederken panel üzerinde 'aria-busy=\"true\"' yer almalı"
  - "Panel bir canlı bölge veya 'aria-live=\"polite\"' özelliğine sahip olmalı"
  - "Yükleme durumunu açıklayan erişilebilir bir metin yer almalı"
concept_tags: [accessibility, focus, performance]
checklist_extra:
  - "Veri yüklenirken yardımcı teknolojileri bekletmek için aria-busy='true' kullanılmış mı?"
  - "Veri geldiğinde panelin okunabilmesi için canlı bölge özelliği sağlanmış mı?"
reference_solution_path: private/solutions/html-hard-wai-aria-tabpanel-dynamic-lazyload.html
hint_ladder:
  1: "Bir bölgenin o anda güncellendiğini ve okunmadan önce beklenmesi gerektiğini bildiren ARIA durumu nedir?"
  2: "Güncelleme bittiğinde içeriğin okunmasını sağlayan bölge niteliği nedir?"
  3: "Bu asenkron arayüz yönetimi 'gecikmeli yüklenen meşgul sekme paneli (aria-busy tabpanel)' olarak bilinir."
```

---

### html-hard-multi-language-bidirectional-text

```yaml
id: html-hard-multi-language-bidirectional-text
version: 1
language: html
engine: none
difficulty: hard
title: "Çift yönlü metin ve Arapça/İbranice alıntı izolasyonu (dir, bdi ve bdo)"
prompt: |
  Türkçe yazılmış bir kullanıcı yorumları sayfasında, kullanıcıların serbestçe yazdığı
  yorumlar yer almaktadır. Bazı yorumlar sağdan sola yazılan Arapça veya İbranice metinler
  içerirken, bazı yorumlar kullanıcı adı olarak her iki alfabeden karmaşık karakterler
  barındırmaktadır. Tarayıcının metin yönü algoritmasının (BiDi) ana sayfanın soldan sağa
  düzenini bozmasını engellemek için kullanıcı tarafından üretilen içeriği izole eden etiketi
  kullanın; ayrıca yönün zorunlu olarak tersine çevrilmesi gereken özel durumlar için yön
  geçersiz kılma etiketini uygulayın.
constraints:
  - "Kullanıcı girdisini yön karmaşasından izole etmek için <bdi> etiketi kullanılmalı"
  - "Yönün kesin olarak sağdan sola belirlendiği alanda 'dir=\"rtl\"' bulunmalı"
  - "Yön algoritmasını zorla ezmek (override) için <bdo dir='...'> etiketi kullanılmalı"
  - "Sayfa kökünde veya üst kapsayıcıda geçerli dil ve yön nitelikleri yer almalı"
concept_tags: [standards, semantics, accessibility]
checklist_extra:
  - "Bilinmeyen kullanıcı metinlerini izole etmek için bdi etiketi tercih edilmiş mi?"
  - "Zorunlu yön değişimi için bdo etiketi doğru dir değeriyle uygulanmış mı?"
reference_solution_path: private/solutions/html-hard-multi-language-bidirectional-text.html
hint_ladder:
  1: "Yazı yönü bilinmeyen dinamik kullanıcı metinlerini çevreleyen düzeni bozmaması için izole eden etiket nedir?"
  2: "Metin yönü algoritmasını açıkça geçersiz kılıp yönü zorlayan çift yönlü etiket hangisidir?"
  3: "Bu uluslararası metin standardı 'çift yönlü metin izolasyonu ve geçersiz kılma (bdi ve bdo)' olarak bilinir."
```

---

### html-hard-security-clear-site-data-meta

```yaml
id: html-hard-security-clear-site-data-meta
version: 1
language: html
engine: none
difficulty: hard
title: "Çıkış ekranında istemci verilerini temizleme bildirimi (Clear-Site-Data)"
prompt: |
  Bir internet bankacılığı uygulamasında kullanıcı 'Güvenli Çıkış' bağlantısına tıkladığında
  yönlendirildiği 'Oturum Başarıyla Kapatıldı' ekranını hazırlıyorsunuz. Ortak kullanılan
  bilgisayarlarda sonraki kullanıcının önceki oturumdan kalan hassas verilere ulaşmasını
  engellemek için, tarayıcının o köke ait tüm çerezleri (cookies), yerel depolama verilerini
  (storage) ve önbelleği (cache) temizlemesini emreden standart güvenlik başlığı yönergesini
  HTML `<head>` bölümüne meta etiket olarak ekleyin.
constraints:
  - "<meta http-equiv='Clear-Site-Data' ...> etiketi bulunmalı"
  - "content içinde '\"cache\"', '\"cookies\"', '\"storage\"' temizleme hedefleri tanımlanmalı"
  - "Hedef değerler tırnak içinde ve virgülle ayrılmış standart sözdizimine sahip olmalı"
  - "Sayfa kullanıcıya oturumun kapandığını bildiren erişilebilir bir mesaj içermeli"
concept_tags: [security, standards, performance]
checklist_extra:
  - "http-equiv değeri Clear-Site-Data olarak doğru girilmiş mi?"
  - "content içindeki değerler W3C standardına uygun çift tırnaklı formatta mı?"
reference_solution_path: private/solutions/html-hard-security-clear-site-data-meta.html
hint_ladder:
  1: "Tarayıcının bir web sitesine ait çerez, depolama ve önbelleğini sıfırlamasını sağlayan direktif nedir?"
  2: "Bu temizleme direktifinde tüm verileri silmek için content içine hangi anahtarlar yazılır?"
  3: "Bu oturum güvenliği standardı 'istemci verilerini temizleme başlığı (Clear-Site-Data)' olarak bilinir."
```

---

### html-hard-wai-aria-color-picker-palette

```yaml
id: html-hard-wai-aria-color-picker-palette
version: 1
language: html
engine: none
difficulty: hard
title: "Erişilebilir renk paleti seçim matrisi (accessible color swatch palette)"
prompt: |
  Bir e-ticaret giyim sayfasında veya grafik çizim aracında kullanıcının ürün rengini
  seçtiği bir renk paleti tasarlıyorsunuz. Ekranda yalnızca renkli küçük kareler (kutucuklar)
  görünmektedir. Görme engelli veya renk körü bir kullanıcının her kutucuğun hangi renk
  olduğunu (örneğin 'Gece Mavisi', 'Zümrüt Yeşili') duyabilmesini, bir seferde yalnızca tek bir
  rengin seçilebilmesini ve bileşenin klavye ok tuşlarıyla tek bir mantıksal grup olarak
  gezilebilmesini sağlayan radyo grubu ARIA deseniyle renk paletini inşa edin.
constraints:
  - "Kapsayıcıda 'role=\"radiogroup\"' ve açıklayıcı bir 'aria-label' bulunmalı"
  - "Her renk seçeneğinde 'role=\"radio\"' ve rengin adını veren 'aria-label' yer almalı"
  - "Seçili renkte 'aria-checked=\"true\"' ve 'tabindex=\"0\"' bulunmalı"
  - "Seçili olmayan renklerde 'aria-checked=\"false\"' ve 'tabindex=\"-1\"' olmalı"
concept_tags: [accessibility, focus, forms]
checklist_extra:
  - "Renk kutucukları anlamsal bir radyo grubu (radiogroup ve radio) olarak kurgulanmış mı?"
  - "Her kutucuğa renk adını aktaran açık bir aria-label atanmış mı?"
reference_solution_path: private/solutions/html-hard-wai-aria-color-picker-palette.html
hint_ladder:
  1: "Bir gruptan tek bir seçenek seçtiren özel görsel kutucukları modellemek için hangi ARIA rol kümesi kullanılır?"
  2: "Renk adını ekran okuyucuya tanıtmak için kutucuğa hangi etiketleme niteliği eklenir?"
  3: "Bu erişilebilir tasarım deseni 'erişilebilir renk paleti radyo grubu (accessible color swatch radiogroup)' olarak bilinir."
```

---

### html-hard-web-app-manifest-meta-integration

```yaml
id: html-hard-web-app-manifest-meta-integration
version: 1
language: html
engine: none
difficulty: hard
title: "İlerici web uygulaması meta ve bildirim entegrasyonu (PWA manifest meta)"
prompt: |
  Bir web sitesini mobil cihazlarda ana ekrana eklenebilen ve bağımsız bir mobil uygulama
  gibi açılan bir İlerici Web Uygulamasına (PWA) dönüştürmek istiyorsunuz. Tarayıcı adres çubuğu
  tema rengini belirleyen, mobil tarayıcının tam ekran uygulama modunda açılmasını sağlayan,
  iOS Safari için özel web uygulaması yetkilerini ve simgelerini tanımlayan, ayrıca web
  uygulama bildirim dosyasına (manifest.json) işaret eden standart `<head>` meta etiketlerini
  eksiksiz kurgulayın.
constraints:
  - "<link rel='manifest' href='...'> etiketi bulunmalı"
  - "<meta name='theme-color' content='...'> tanımlanmalı"
  - "iOS için <meta name='apple-mobile-web-app-capable' content='yes'> yer almalı"
  - "<link rel='apple-touch-icon' href='...'> simge referansı bulunmalı"
concept_tags: [standards, performance, images]
checklist_extra:
  - "Uygulama bildirim dosyası rel='manifest' ile bağlanmış mı?"
  - "Mobil tarayıcı arayüz rengi theme-color meta etiketiyle tanımlanmış mı?"
reference_solution_path: private/solutions/html-hard-web-app-manifest-meta-integration.html
hint_ladder:
  1: "Web uygulamasının simge, isim ve başlangıç ayarlarını tutan JSON dosyasını bağlayan link ilişkisi nedir?"
  2: "Mobil tarayıcıların üst çubuk rengini site temasıyla uyumlu yapan meta etiketi hangisidir?"
  3: "Bu mobil web standardı 'ilerici web uygulaması meta entegrasyonu (PWA manifest meta tags)' olarak bilinir."
```

---

### html-hard-wai-aria-roving-tabindex-radiogroup

```yaml
id: html-hard-wai-aria-roving-tabindex-radiogroup
version: 1
language: html
engine: none
difficulty: hard
title: "Özel tasarımlı erişilebilir radyo grubu (custom radiogroup roving tabindex)"
prompt: |
  Standart HTML radio girdilerinin stil kısıtlamalarını aşmak için tamamen özel `<div>` veya
  `<span>` elemanlarıyla tasarlanmış bir teslimat hızı seçicisi ('Standart Kargo', 'Hızlı Kargo',
  'Aynı Gün Teslimat') oluşturuyorsunuz. Bu görsel yapının klavye ve yardımcı teknolojiler
  nezdinde standart bir radyo butonu kümesiyle birebir aynı davranmasını sağlayın. Grup içinde
  yalnızca seçili olan seçeneğin Tab ile odak almasını, ok tuşlarıyla seçenekler arasında
  geçiş yapılabilmesini destekleyen WAI-ARIA radyo grubu semantiğini kurun.
constraints:
  - "Kapsayıcıda 'role=\"radiogroup\"' ve 'aria-labelledby' veya 'aria-label' bulunmalı"
  - "Her seçenekte 'role=\"radio\"' ve 'aria-checked' durumu bulunmalı"
  - "Yalnızca seçili olan seçenekte 'tabindex=\"0\"', diğerlerinde 'tabindex=\"-1\"' olmalı"
  - "Grup bir başlık veya açıklamayla ilişkilendirilmeli"
concept_tags: [accessibility, focus, forms]
checklist_extra:
  - "Özel radyo butonları için role='radio' atanmış mı?"
  - "Dolaşan odak sırası için seçili olmayanlara tabindex='-1' verilmiş mi?"
reference_solution_path: private/solutions/html-hard-wai-aria-roving-tabindex-radiogroup.html
hint_ladder:
  1: "Özel elemanlardan tek seçenekli bir seçim kümesi oluşturmak için hangi ARIA rol çifti kullanılır?"
  2: "Klavyeden turlarken radyo grubuna tek bir durakla girilmesini sağlayan indeksleme kuralı nedir?"
  3: "Bu özel form deseni 'WAI-ARIA özel radyo grubu deseni (radiogroup roving tabindex)' olarak bilinir."
```

---

### html-hard-jsonld-article-author-publisher

```yaml
id: html-hard-jsonld-article-author-publisher
version: 1
language: html
engine: none
difficulty: hard
title: "Yazar ve yayıncı logolu kurumsal makale şeması (JSON-LD NewsArticle)"
prompt: |
  Büyük bir haber ajansının makale sayfasında Google Haberler (Google News) ve arama motorları
  için en üst düzey yapılandırılmış veri entegrasyonu kurun. JSON-LD formatında 'NewsArticle'
  şeması oluşturun. Şema içinde; makale başlığı, yayınlanma ve güncellenme tarihleri, yazarın
  kişi (Person) olarak adı ve profil URL'si; yayıncı kurumun ise tüzel kişilik (Organization)
  olarak adı, resmi web sitesi ve arama motorlarının talep ettiği formatta logo görseli (ImageObject)
  iç içe nesneler şeklinde tanımlanmalıdır.
constraints:
  - "<script type='application/ld+json'> kullanılmalı"
  - "'@type': 'NewsArticle' kök tipi altında 'headline', 'datePublished', 'dateModified' bulunmalı"
  - "'author' nesnesi '@type': 'Person' olarak yapılandırılmalı"
  - "'publisher' nesnesi '@type': 'Organization' ve altında '@type': 'ImageObject' logoya sahip olmalı"
concept_tags: [standards, semantics, performance]
checklist_extra:
  - "Yayıncı kurum altında logo bir ImageObject olarak mı tanımlanmış?"
  - "Tarihler ISO 8601 standart dizgisi olarak biçimlendirilmiş mi?"
reference_solution_path: private/solutions/html-hard-jsonld-article-author-publisher.html
hint_ladder:
  1: "Haber siteleri için özel olarak tasarlanmış Schema.org makale alt türü hangisidir?"
  2: "Yayıncı kurumun logosunu arama motoruna bildirmek için hangi alt nesne tipi kullanılır?"
  3: "Bu kurumsal SEO şeması 'JSON-LD haber makalesi ve yayıncı kurumu şeması (NewsArticle schema)' olarak bilinir."
```

---

### html-hard-complex-survey-matrix-form

```yaml
id: html-hard-complex-survey-matrix-form
version: 1
language: html
engine: none
difficulty: hard
title: "Matris tipi anket değerlendirme formu (Likert scale matrix form)"
prompt: |
  Bir müşteri memnuniyeti anketinde, birden fazla ifadenin (örneğin 'Hizmet Hızı', 'Ürün Kalitesi',
  'Destek Ekibi İlgisi') sütunlarda yer alan 5 puanlık Likert ölçeğine (1: Kesinlikle Katılmıyorum ...
  5: Kesinlikle Katılıyorum) göre değerlendirildiği bir anket matrisi tasarlıyorsunuz.
  Görsel olarak tablo biçiminde sunulan bu yapıda, her satırın bağımsız bir soru grubu olduğunu
  ekran okuyucuların anlayabilmesi için her satırı anlamsal bir `<fieldset>` ve `<legend>` ile
  koruyun veya tablo başlıkları ile radyo butonlarını iki boyutlu erişilebilir etiketleme
  ile bağlayın.
constraints:
  - "Tablo veya form içinde her soru satırı ayrı bir radyo 'name' grubuna sahip olmalı"
  - "Her radyo butonunda satır başlığı ve sütun puanını birlikte aktaran 'aria-label' veya label bulunmalı"
  - "Sütun başlıkları <th> hücreleri olarak 'scope=\"col\"' taşımalı"
  - "Satır başlıkları <th> veya anlamsal etiket olarak tanımlanmalı"
concept_tags: [forms, tables, accessibility]
checklist_extra:
  - "Her satırdaki radyo butonları kendi satırına özgü bağımsız bir name grubunda mı?"
  - "Radyo butonu tek başına '3' demek yerine hem soruyu hem puanı aktaran bir etiketlemeye sahip mi?"
reference_solution_path: private/solutions/html-hard-complex-survey-matrix-form.html
hint_ladder:
  1: "Tablo görünümünde sunulan anket sorularında her satırın ayrı soru olması için inputlarda ne farklı olmalıdır?"
  2: "Sadece rakam olan radyo kutusunun hangi soruya ait olduğunu bildirmek için hangi ARIA niteliği kullanılır?"
  3: "Bu form mimarisi 'matris tipi anket değerlendirme formu (survey matrix Likert scale)' olarak bilinir."
```

---

### html-hard-form-client-side-instant-feedback

```yaml
id: html-hard-form-client-side-instant-feedback
version: 1
language: html
engine: none
difficulty: hard
title: "İstemci taraflı anlık girdi doğrulama geri bildirimi (instant field feedback)"
prompt: |
  Bir kullanıcı kayıt formundaki e-posta adresinin uygunluğunu kullanıcı yazmayı bitirdiği
  anda kontrol eden bir girdi alanı tasarlıyorsunuz. Girdi geçerli olduğunda yanında yeşil
  bir onay simgesi ve 'E-posta adresi geçerli', geçersiz olduğunda ise kırmızı çarpı simgesi ve
  'Lütfen geçerli bir e-posta girin' uyarısı belirmektedir. Bu görsel durum değişimlerinin
  ekran okuyucu kullanıcılarına odak kaybı yaşatmadan anında seslendirilmesini sağlayan
  canlı bölge, geçersizlik durumu ve açıklama bağlantılarını HTML üzerinde kurgulayın.
constraints:
  - "<input type='email'> üzerinde 'aria-invalid' durumu dinamik olarak yönetilebilir yapıda olmalı"
  - "Geri bildirim alanı 'aria-live=\"polite\"' canlı bölgesi olmalı"
  - "Girdi alanı geri bildirim alanına 'aria-describedby' ile bağlanmalı"
  - "Görsel simgeler (onay/çarpı) 'aria-hidden=\"true\"' ile gizlenip açıklama metinle verilmeli"
concept_tags: [forms, input-validation, accessibility]
checklist_extra:
  - "Geri bildirim mesajı canlı bölge içine yerleştirilmiş mi?"
  - "Görsel durum simgeleri ekran okuyuculardan gizlenerek metinsel açıklama öne çıkarılmış mı?"
reference_solution_path: private/solutions/html-hard-form-client-side-instant-feedback.html
hint_ladder:
  1: "Girdi alanındaki anlık durum değişikliklerini kullanıcıyı bölmeden duyuran canlı bölge nedir?"
  2: "Girdinin o anki geçerlilik durumunu yardımcı teknolojiye ileten temel ARIA niteliği nedir?"
  3: "Bu kullanıcı deneyimi yapısı 'anlık form doğrulama geri bildirimi (instant input validation feedback)' olarak bilinir."
```

---

### html-hard-speculation-rules-document-rules

```yaml
id: html-hard-speculation-rules-document-rules
version: 1
language: html
engine: none
difficulty: hard
title: "Belge düzeyi otomatik tahmin ve önceden oluşturma kuralları (Speculation Rules document_rules)"
prompt: |
  Geniş bir e-ticaret veya medya sitesinde tek tek tüm ürün linklerini JSON listesine elle
  yazmak yerine, modern web tarayıcısının sayfadaki belirli bağlantı desenlerini otomatik
  keşfetmesini (auto-discovery) istiyorsunuz. Belge düzeyinde kurallar (document_rules) kullanarak;
  sayfada href değeri '/urunler/' ile başlayan ve üzerinde 'no-prerender' sınıfı bulunmayan
  tüm bağlantıların fare üzerine gelindiğinde (kullanıcı etkileşimi sinyaliyle) arka planda
  önceden getirilmesini (prefetch) veya işlenmesini (prerender) sağlayan gelişmiş kural
  şemasını HTML içine yerleştirin.
constraints:
  - "<script type='speculationrules'> etiketi kullanılmalı"
  - "'prerender' veya 'prefetch' bloğu altında 'source': 'document' kuralı yer almalı"
  - "'where' koşulunda 'href_matches' veya 'selector_matches' filtreleri bulunmalı"
  - "'eagerness': 'moderate' veya 'conservative' etkileşim eşiği tanımlanmalı"
concept_tags: [performance, standards, links]
checklist_extra:
  - "Statik URL listesi yerine dinamik document_rules kuralı kurulmuş mu?"
  - "Tıklama niyetine göre yükleme yapmak için eagerness seviyesi belirtilmiş mi?"
reference_solution_path: private/solutions/html-hard-speculation-rules-document-rules.html
hint_ladder:
  1: "Speculation Rules API'sinde sayfadaki bağlantıları CSS seçicisi veya regex ile otomatik yakalayan kaynak türü nedir?"
  2: "Kullanıcının fareyle link üzerine gelmesini bekleyip öyle ön yükleme yaptıran eagerness değeri nedir?"
  3: "Bu ileri düzey tarayıcı önbellekleme standardı 'belge kurallı tahmin API'si (Speculation Rules document_rules)' olarak bilinir."
```

---

### html-hard-accessible-audio-visualizer-canvas

```yaml
id: html-hard-accessible-audio-visualizer-canvas
version: 1
language: html
engine: none
difficulty: hard
title: "Erişilebilir ses spektrumu görselleştiricisi (canvas ve canlı yedek tablo)"
prompt: |
  Bir ses düzenleme yazılımında veya müzik çalar arayüzünde, ses frekanslarını gerçek zamanlı
  olarak çizen bir tuval (canvas) spektrum grafiği oluşturuyorsunuz. Yalnızca piksellerden oluşan
  tuval elemanları doğası gereği görme engelliler ve ekran okuyucular için tamamen erişilemezdir.
  Tuvalin içinde ekran okuyucuların frekans aralıklarını (Bas, Orta, Tiz) ve desibel değerlerini
  duyabileceği bir yedek veri tablosu kurgulayın; tuvalin amacını anlatan bir erişilebilir isim
  tanımlayın ve ses verisi değiştikçe tablonun güncellendiğini bildiren canlı bölge niteliğini bağlayın.
constraints:
  - "<canvas> elemanında 'role=\"img\"' ve açıklayıcı 'aria-label' bulunmalı"
  - "<canvas> içinde ekran okuyucular için anlamsal bir <table> yedek içeriği yer almalı"
  - "Yedek tablo frekans bantlarını ve ses seviyelerini anlamsal <th> ve <td> ile listelemeli"
  - "Tablo kapsayıcısı veya tablo 'aria-live=\"polite\"' canlı bölgesi taşımalı"
concept_tags: [accessibility, tables, standards]
checklist_extra:
  - "Canvas içine yardımcı teknolojiler için anlamsal bir yedek tablo yerleştirilmiş mi?"
  - "Canvas rolü img ve açıklayıcı aria-label ile donatılmış mı?"
reference_solution_path: private/solutions/html-hard-accessible-audio-visualizer-canvas.html
hint_ladder:
  1: "Canvas elemanını bir grafik olarak tanıtmak için hangi WAI-ARIA rolü atanır?"
  2: "Piksel tabanlı çizimlerin erişilebilir yedeğini sunmak için canvas içine ne yazılır?"
  3: "Bu grafik erişilebilirlik deseni 'erişilebilir tuval veri yedeği (accessible canvas fallback table)' olarak bilinir."
```

---

