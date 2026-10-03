# CodeMentor AI — 200 CSS Sorusu

Bu belge, `docs/SORU_YAZIM_REHBERI.md` standartlarına uygun olarak hazırlanmış 200 adet CSS sorusunu içerir.
CSS stil ve mizanpaj dili olduğu için algoritmik karmaşıklık analizi içermez (`expected` alanı yer almaz); mizanpaj modelleri (Flexbox, Grid), duyarlı tasarım (responsive), yığın bağlamı (stacking context / z-index), seçici özgüllüğü (specificity), CSS değişkenleri (custom properties), erişilebilirlik ve performans optimizasyonlarına odaklanır.

---

## Soru Bankası Değerlendirmesi ve Pedagojik Kullanım Notu

Bu soru bankası teknik mülakatlar, frontend mühendisliği adayları ve web geliştiricileri için tasarlanmıştır:

1. **Yöntem Sızıntısı Olmayan Saf Mülakat Formatı:**
   - Soruların başlıklarında ve prompt metinlerinde doğrudan CSS özellik adları (ör. `display: flex`, `z-index`, `!important`) verilmemiştir.
   - Sorular adaya gerçek dünya tasarım ve mizanpaj problemlerini tanımlar; adayın problemi çözmek için doğru CSS kuralını kendisinin seçmesi beklenir.

2. **Kademeli İpucu Sistemi (Sokratik Mentörlük):**
   - Öğrenci veya aday zorlandığında mentör doğrudan kodu vermez; 3 basamaklı ipucu merdiveni (`hint_ladder`) ile önce problemi düşündürür, sonra kavram alanına yönlendirir, en son kavramın adını açıklar.

3. **Mizanpaj, Performans ve Erişilebilirlik Dengesi:**
   - Sorular yalnızca görsel biçimlendirmeyi değil; klavye odağı göstergeleri, kontrast, hareket azaltma (`prefers-reduced-motion`), GPU hızlandırmalı animasyonlar (`transform`/`opacity`) ve düzen kayması (CLS) önleme gibi mühendislik kriterlerini ölçer.

---

## 1. Çok Kolay (Very Easy) — 50 Soru

### css-veryeasy-box-sizing-border-box

```yaml
id: css-veryeasy-box-sizing-border-box
version: 1
language: css
engine: none
difficulty: very_easy
title: "Kutu modeli genişlik taşmasını engelleme"
prompt: |
  Bir e-ticaret sitesinde yan yana duracak iki adet ürün kartı tasarlıyorsunuz. Her iki karta
  da yüzde 50 genişlik tanımlayıp iç boşluk (padding) ve kenarlık (border) eklediğinizde,
  kartların toplam genişliği yüzde 100'ü aştığı için ikinci kart alt satıra kaymaktadır.
  Tüm sayfadaki elemanların genişlik hesaplamasına iç boşluk ve kenarlıkların dahil edilmesini
  sağlayan evrensel kutu modeli kuralını yazın.
constraints:
  - "Genişlik hesabı iç boşluk ve kenarlığı kapsayacak şekilde ayarlanmalı"
  - "Kural evrensel seçici veya kök eleman üzerinden tüm elemanlara uygulanmalı"
concept_tags: [layout, edge-cases]
checklist_extra:
  - "Varsayılan content-box yerine border-box modeli seçilmiş mi?"
  - "Evrensel seçici sözde elemanları da kapsayacak şekilde kurgulanmış mı?"
reference_solution_path: private/solutions/css-veryeasy-box-sizing-border-box.css
hint_ladder:
  1: "Tarayıcının bir elemanın genişliğine padding ve border eklemesini hangi özellik engeller?"
  2: "Kutu boyutlandırma modelini içeriğe göre değil kenarlığa göre hesaplatan değer nedir?"
  3: "Bu temel CSS kutu modeli kuralı 'border-box kutu boyutlandırması' olarak bilinir."
```

---

### css-veryeasy-text-color-contrast

```yaml
id: css-veryeasy-text-color-contrast
version: 1
language: css
engine: none
difficulty: very_easy
title: "Koyu zemin üzerinde okunabilir metin rengi"
prompt: |
  Koyu lacivert arka plana sahip bir duyuru kutusu içinde yer alan paragrafların okunabilirliğini
  sağlamak istiyorsunuz. Tarayıcının varsayılan siyah metin rengi koyu zemin üzerinde kaybolduğu
  için, WCAG kontrast kriterlerine uygun olarak metin rengini temiz, göz yormayan açık bir renge
  dönüştüren kuralı yazın.
constraints:
  - "Duyuru kutusu içindeki metin için açık bir yazı rengi tanımlanmalı"
  - "Kontrast oranı okunabilirlik sınırını karşılamalı"
concept_tags: [color, accessibility]
checklist_extra:
  - "Metin rengi için geçerli bir renk değeri kullanılmış mı?"
  - "Kontrast oranı koyu zemin üzerinde rahat okunuyor mu?"
reference_solution_path: private/solutions/css-veryeasy-text-color-contrast.css
hint_ladder:
  1: "CSS'te yazıların rengini değiştirmek için hangi temel özellik kullanılır?"
  2: "Koyu arka plan üzerinde yüksek kontrast sağlamak için renk değeri ne seçilmelidir?"
  3: "Bu temel tipografi kuralı 'metin rengi ve kontrast ayarı' olarak bilinir."
```

---

### css-veryeasy-font-family-fallback

```yaml
id: css-veryeasy-font-family-fallback
version: 1
language: css
engine: none
difficulty: very_easy
title: "Yedekli sistem yazı tipi ailesi tanımı"
prompt: |
  Web sitenizin gövde metinleri için birincil olarak modern bir tırnaksız yazı tipi belirleyin.
  Kullanıcının bilgisayarında bu yazı tipi yüklü değilse sırasıyla işletim sistemi genelindeki
  standart tırnaksız alternatiflere, en son çare olarak ise tarayıcının yerleşik genel tırnaksız
  yazı tipine düşmesini (fallback) sağlayan güvenli bir yazı tipi zinciri kurun.
constraints:
  - "En az üç kademeli bir yazı tipi öncelik listesi sunulmalı"
  - "Listenin sonunda genel tırnaksız kategori yer almalı"
  - "Boşluk içeren yazı tipi adları tırnak içine alınmalı"
concept_tags: [typography, maintainability]
checklist_extra:
  - "Zincirin sonunda genel sans-serif anahtar kelimesi yer alıyor mu?"
  - "Birden fazla kelimeden oluşan font adları çift tırnakla sarılmış mı?"
reference_solution_path: private/solutions/css-veryeasy-font-family-fallback.css
hint_ladder:
  1: "Metinlerin fontunu belirleyen ve virgülle alternatifler kabul eden özellik nedir?"
  2: "Özel yazı tipi bulunamazsa devreye girecek jenerik aile adı nedir?"
  3: "Bu tipografi zinciri 'yazı tipi ailesi yedekleme kuralı (font-family fallback)' olarak bilinir."
```

---

### css-veryeasy-line-height-proportions

```yaml
id: css-veryeasy-line-height-proportions
version: 1
language: css
engine: none
difficulty: very_easy
title: "Orantılı ve miras alınabilir satır yüksekliği"
prompt: |
  Bir blog yazısındaki uzun paragrafların satırları birbirine çok yakın olduğu için okuma
  güçlüğü yaşanmaktadır. Paragrafların satır aralığını ferahlatacak orantılı bir satır yüksekliği
  belirleyin. Alt başlıklara veya farklı boyutlardaki çocuk elemanlara miras kaldığında piksel
  kayması veya üst üste binme yapmaması için birimsiz (çarpan tabanlı) bir değer tercih edin.
constraints:
  - "Okunabilirliği artıran bir satır yüksekliği atanmalı"
  - "Piksel gibi sabit birimler yerine birimsiz oransal değer kullanılmalı"
concept_tags: [typography, accessibility]
checklist_extra:
  - "px yerine birimsiz bağıl çarpan (örn. 1.5 veya 1.6) kullanılmış mı?"
  - "Satır yüksekliği metin boyutuyla uyumlu ve ferah mı?"
reference_solution_path: private/solutions/css-veryeasy-line-height-proportions.css
hint_ladder:
  1: "Satırlar arasındaki dikey boşluğu yöneten CSS özelliği hangisidir?"
  2: "Font boyutu değiştiğinde satır yüksekliğinin otomatik ölçeklenmesi için birim nasıl yazılır?"
  3: "Bu tipografi standardı 'birimsiz satır yüksekliği (unitless line-height)' olarak bilinir."
```

---

### css-veryeasy-margin-auto-centering

```yaml
id: css-veryeasy-margin-auto-centering
version: 1
language: css
engine: none
difficulty: very_easy
title: "Sabit genişlikli ana konteyneri yatayda ortalama"
prompt: |
  Geniş ekranlı monitörlerde web sayfasının içeriğinin sonsuza kadar yayılmasını istemiyorsunuz.
  Gövdedeki ana içerik bloğuna maksimum 1200 piksel bir genişlik sınırı koyun ve bu bloğun
  ekranın tam ortasında konumlanmasını sağlayacak klasik dış boşluk dengesini kurun.
constraints:
  - "Elemana maksimum genişlik veya genişlik sınırı tanımlanmalı"
  - "Sağ ve sol dış boşluklar eşit paylaştırılarak yatayda ortalanmalı"
concept_tags: [centering, layout]
checklist_extra:
  - "Sağ ve sol margin değerleri auto olarak ayarlanmış mı?"
  - "Genişlik sınırı belirtilmeden ortalama yapılmaya çalışılmış mı?"
reference_solution_path: private/solutions/css-veryeasy-margin-auto-centering.css
hint_ladder:
  1: "Blok düzeyindeki bir kutuyu yatayda ortalamak için sağ ve sol dış boşluğa ne verilir?"
  2: "auto değerinin ortalama yapabilmesi için kutunun neye sahip olması şarttır?"
  3: "Bu klasik ortalama tekniği 'otomatik dış boşlukla blok ortalama (margin auto)' olarak bilinir."
```

---

### css-veryeasy-padding-spacing-box

```yaml
id: css-veryeasy-padding-spacing-box
version: 1
language: css
engine: none
difficulty: very_easy
title: "Kart içeriğine iç nefes payı kazandırma"
prompt: |
  Bir profil kartının içindeki metinler ve resimler kartın dış çizgilerine tamamen yapışmış
  durumdadır. Kartın içindeki içeriğin kenarlardan 24 piksel içeride durmasını ve dört bir
  yandan ferah bir boşluk kazanmasını sağlayan iç boşluk kuralını tanımlayın.
constraints:
  - "Kart elemanına her yönden eşit iç boşluk uygulanmalı"
  - "İçerik ile kart sınırları arasında istenen mesafe oluşmalı"
concept_tags: [layout, edge-cases]
checklist_extra:
  - "Dış boşluk (margin) yerine iç boşluk (padding) kullanılmış mı?"
  - "Dört yöne tek satırda veya tek özellikle değer verilmiş mi?"
reference_solution_path: private/solutions/css-veryeasy-padding-spacing-box.css
hint_ladder:
  1: "Bir kutunun kenarlığı ile içindeki içerik arasındaki mesafeyi hangi özellik belirler?"
  2: "Dört yöne birden eşit iç mesafe vermek için hangi anahtar kullanılır?"
  3: "Bu kutu modeli kuralı 'iç boşluk tanımlaması (padding)' olarak bilinir."
```

---

### css-veryeasy-border-subtle-card

```yaml
id: css-veryeasy-border-subtle-card
version: 1
language: css
engine: none
difficulty: very_easy
title: "Köşeleri yuvarlatılmış zarif kart çerçevesi"
prompt: |
  Bir ürün tanıtım kartını arka plandan zarif bir şekilde ayırmak istiyorsunuz. Kartın
  etrafına 1 piksel kalınlığında, açık gri tonunda düz bir çerçeve çizin ve kartın sert
  köşelerini modern bir görünüm için 8 piksel kavisle yumuşatın.
constraints:
  - "Kenarlık kalınlığı, stili ve rengi eksiksiz tanımlanmalı"
  - "Köşe kavis değeri tüm köşelere eşit uygulanmalı"
concept_tags: [layout, color]
checklist_extra:
  - "Kenarlık stili solid olarak açıkça belirtilmiş mi?"
  - "Köşeleri yuvarlatmak için border-radius kullanılmış mı?"
reference_solution_path: private/solutions/css-veryeasy-border-subtle-card.css
hint_ladder:
  1: "Bir elemanın etrafına çizgi çekmek için hangi birleşik özellik kullanılır?"
  2: "Kutunun sivri köşelerini dairesel olarak bükmek için hangi özellik atanır?"
  3: "Bu görsel biçimlendirme 'kenarlık ve köşe yuvarlatma (border ve border-radius)' olarak bilinir."
```

---

### css-veryeasy-link-underline-states

```yaml
id: css-veryeasy-link-underline-states
version: 1
language: css
engine: none
difficulty: very_easy
title: "Köprü alt çizgi ve fare üzerine gelme etkileşimi"
prompt: |
  Bir web sitesinin navigasyon çubuğundaki bağlantıların varsayılan mavi rengini ve altındaki
  çizgiyi kaldırarak sadeleştirin. Ancak kullanıcı fareyle bağlantının üzerine geldiğinde
  metnin altına ince bir çizgi ekleyerek ve rengini kurumsal renge dönüştürerek tıklanabilir
  olduğunu hissettiren etkileşim durumunu tanımlayın.
constraints:
  - "Varsayılan durumda metin süslemesi (alt çizgi) kaldırılmalı"
  - "Fare üzerine gelindiğinde (:hover durumunda) alt çizgi ve renk değişimi tetiklenmeli"
concept_tags: [focus, accessibility]
checklist_extra:
  - "Alt çizgiyi kaldırmak için text-decoration: none kullanılmış mı?"
  - "Hover durumu için doğru sözde sınıf (:hover) bağlanmış mı?"
reference_solution_path: private/solutions/css-veryeasy-link-underline-states.css
hint_ladder:
  1: "Bağlantıların altındaki çizgiyi kaldırmak için hangi metin özelliği kullanılır?"
  2: "Fare bir elemanın üzerindeyken stil uygulamak için hangi sözde sınıf eklenir?"
  3: "Bu köprü kuralı 'metin süslemesi ve hover durumu (text-decoration: hover)' olarak bilinir."
```

---

### css-veryeasy-list-bullet-style

```yaml
id: css-veryeasy-list-bullet-style
version: 1
language: css
engine: none
difficulty: very_easy
title: "Liste işaretlerini ve girintisini sıfırlama"
prompt: |
  Bir yatay navigasyon menüsü veya etiket listesi oluştururken standart HTML sırasız listesi
  (`<ul>`) kullanıyorsunuz. Tarayıcının varsayılan olarak listenin başına koyduğu yuvarlak siyah
  noktaları (bullet) kaldırın ve tarayıcının eklediği varsayılan sol iç/dış boşluk girintilerini
  sıfırlayın.
constraints:
  - "Liste madde işaretleri tamamen kaldırılmalı"
  - "Varsayılan liste iç boşluğu (padding) ve dış boşluğu (margin) sıfırlanmalı"
concept_tags: [layout, maintainability]
checklist_extra:
  - "Liste işaretini kaldırmak için list-style: none atanmış mı?"
  - "Tarayıcının varsayılan sol girintisi sıfırlanmış mı?"
reference_solution_path: private/solutions/css-veryeasy-list-bullet-style.css
hint_ladder:
  1: "Liste elemanlarının başındaki noktaları veya numaraları kapatan özellik nedir?"
  2: "Listenin sola doğru olan varsayılan girintisini kaldırmak için ne sıfırlanmalıdır?"
  3: "Bu stil sıfırlama kuralı 'liste stili temizleme (list-style reset)' olarak bilinir."
```

---

### css-veryeasy-image-max-width-fluid

```yaml
id: css-veryeasy-image-max-width-fluid
version: 1
language: css
engine: none
difficulty: very_easy
title: "Görsellerin ebeveyn dışına taşmasını engelleme"
prompt: |
  Mobil cihazlarda veya dar sütunlarda büyük çözünürlüklü fotoğraflar yerleştirildiğinde,
  görseller kendi doğal boyutlarında kaldıkları için kartın veya sayfanın dışına taşarak
  yatay kaydırma çubuğu oluşturmaktadır. Sayfadaki tüm görsellerin ebeveyn kapsayıcılarının
  genişliğini asla aşmamasını ve kendi en-boy oranlarını bozmadan küçülmesini sağlayan temel
  duyarlı görsel kuralını yazın.
constraints:
  - "Görsellerin azami genişliği ebeveynin sınırına eşitlenmeli"
  - "Doğal en-boy oranının bozulmaması için yükseklik orantılı ayarlanmalı"
concept_tags: [responsive, layout]
checklist_extra:
  - "width: 100% yerine küçük görselleri bozmayan max-width: 100% kullanılmış mı?"
  - "Yükseklik ezilmesini önlemek için height: auto verilmiş mi?"
reference_solution_path: private/solutions/css-veryeasy-image-max-width-fluid.css
hint_ladder:
  1: "Bir elemanın kapsayıcısından daha geniş olmasını engelleyen sınır özelliği nedir?"
  2: "Genişlik küçülürken görselin basıklaşmaması için yükseklik değerine ne yazılır?"
  3: "Bu temel duyarlı kural 'akışkan görsel kısıtı (fluid image max-width)' olarak bilinir."
```

---

### css-veryeasy-display-inline-block-pills

```yaml
id: css-veryeasy-display-inline-block-pills
version: 1
language: css
engine: none
difficulty: very_easy
title: "Satır içi rozetlere genişlik ve boşluk kazandırma"
prompt: |
  Bir makalenin altında yer alan kategori etiketlerini `<span>` elemanları olarak yazdınız.
  Ancak satır içi (inline) elemanlar oldukları için dikey iç boşluklar (padding) ve üst/alt
  mesafeler düzgün çalışmamakta, metin satırları birbirine girmektedir. Bu etiketlerin yan yana
  satır içi gibi akmasını ama aynı zamanda genişlik, yükseklik ve dikey boşlukları kabul eden
  bir kutu gibi davranmasını sağlayın.
constraints:
  - "Elemanlar yan yana akış özelliğini korurken kutu modeli özelliklerini de kabul etmeli"
  - "Dikey ve yatay iç boşluklar düzgün uygulanabilmeli"
concept_tags: [layout, edge-cases]
checklist_extra:
  - "Görünüm değeri olarak inline-block seçilmiş mi?"
  - "Dikey iç boşlukların diğer satırlara taşması engellenmiş mi?"
reference_solution_path: private/solutions/css-veryeasy-display-inline-block-pills.css
hint_ladder:
  1: "Hem satır içi yan yana duran hem de kutu özelliklerini kabul eden görünüm modu nedir?"
  2: "inline ile block özelliklerini birleştiren display değeri hangisidir?"
  3: "Bu mizanpaj kuralı 'satır içi blok görünümü (display inline-block)' olarak bilinir."
```

---

### css-veryeasy-text-align-center-hero

```yaml
id: css-veryeasy-text-align-center-hero
version: 1
language: css
engine: none
difficulty: very_easy
title: "Başlık ve açıklama metinlerini yatayda ortalama"
prompt: |
  Bir açılış sayfasının ana karşılama bölümünde (hero section) büyük bir başlık, altında
  açıklayıcı bir alt paragraf ve bir kayıt çağrısı yer almaktadır. Bu bölümün içindeki tüm
  satır içi ve metinsel içeriklerin kapsayıcının yatay merkezine hizalanmasını sağlayan
  metin hizalama kuralını yazın.
constraints:
  - "Kapsayıcı içindeki metin akışı yatayda merkeze hizalanmalı"
  - "Kural blok düzeyindeki kapsayıcıya atanmalı"
concept_tags: [centering, typography]
checklist_extra:
  - "Metin hizalama özelliği center olarak atanmış mı?"
  - "Kural metnin kendisine değil üst kapsayıcıya mı uygulanmış?"
reference_solution_path: private/solutions/css-veryeasy-text-align-center-hero.css
hint_ladder:
  1: "Bir blok içindeki metinlerin hizasını sağa, sola veya ortaya ayarlayan özellik nedir?"
  2: "Metinleri ortaya toplamak için bu özelliğe hangi değer verilir?"
  3: "Bu temel hizalama 'metin hizalama kuralı (text-align center)' olarak bilinir."
```

---

### css-veryeasy-cursor-pointer-clickable

```yaml
id: css-veryeasy-cursor-pointer-clickable
version: 1
language: css
engine: none
difficulty: very_easy
title: "Tıklanabilir eleman için el simgesi imleci"
prompt: |
  Özel olarak tasarladığınız bir buton veya açılır akordeon başlığı üzerine fare ile
  gelindiğinde, kullanıcının bunun tıklanabilir bir etkileşim elemanı olduğunu hemen
  anlayabilmesi için varsayılan ok imlecini standart el/parmak tıklama simgesine dönüştüren
  kuralı tanımlayın.
constraints:
  - "Elemanın üzerine gelindiğinde imleç tıklama sembolü göstermeli"
  - "Tüm tarayıcılarda standart tıklanabilirlik hissi verilmeli"
concept_tags: [focus, accessibility]
checklist_extra:
  - "İmleç tipi pointer olarak ayarlanmış mı?"
  - "Tıklanabilir buton veya kart için doğru seçici kullanılmış mı?"
reference_solution_path: private/solutions/css-veryeasy-cursor-pointer-clickable.css
hint_ladder:
  1: "Fare imlecinin şeklini değiştiren CSS özelliği nedir?"
  2: "Tıklanabilir köprülerdeki gibi el işaretini gösteren imleç değeri hangisidir?"
  3: "Bu arayüz kuralı 'tıklanabilir imleç göstergesi (cursor pointer)' olarak bilinir."
```

---

### css-veryeasy-hover-button-feedback

```yaml
id: css-veryeasy-hover-button-feedback
version: 1
language: css
engine: none
difficulty: very_easy
title: "Buton fare üzerine gelme renk geri bildirimi"
prompt: |
  Bir web sitesinin birincil eylem butonuna (mavi arka planlı) kullanıcı fare ile yaklaştığında,
  butonun etkileşime hazır olduğunu belli etmek istiyorsunuz. Fare butonun üzerine geldiğinde
  arka plan rengini daha koyu bir mavi tona dönüştüren ve pürüzsüz geçiş sağlayan kuralı
  tanımlayın.
constraints:
  - "Fare üzerine gelme durumu sözde sınıfı ile yakalanmalı"
  - "Arka plan rengi belirgin bir tonda koyulaşmalı"
concept_tags: [color, focus]
checklist_extra:
  - ":hover sözde sınıfı doğru bağlanmış mı?"
  - "Yeni arka plan rengi erişilebilir kontrastı koruyor mu?"
reference_solution_path: private/solutions/css-veryeasy-hover-button-feedback.css
hint_ladder:
  1: "Bir elemanın üzerine fare geldiğinde stil değiştiren sözde sınıf nedir?"
  2: "Butonun zemin rengini değiştirmek için hangi özellik güncellenir?"
  3: "Bu durum bildirimi 'buton hover renk geri bildirimi' olarak bilinir."
```

---

### css-veryeasy-active-button-press

```yaml
id: css-veryeasy-active-button-press
version: 1
language: css
engine: none
difficulty: very_easy
title: "Buton tıklanma anı basılma hissi"
prompt: |
  Kullanıcı butona fareyle sol tıkladığı ve farenin tuşunu henüz bırakmadığı o milisaniyelik
  anda, fiziksel bir butona basılmış hissi vermek istiyorsunuz. Tıklanma anını yakalayan
  sözde sınıfı kullanarak butonun rengini hafifçe daha da koyulaştıran kuralı yazın.
constraints:
  - "Elemanın aktif basılma anı doğru sözde sınıf ile hedeflenmeli"
  - "Basılma anında görsel geri bildirim oluşturulmalı"
concept_tags: [focus, maintainability]
checklist_extra:
  - "Tıklanma anı için :active sözde sınıfı kullanılmış mı?"
  - ":hover ile :active sözde sınıflarının sıralaması mantıklı mı?"
reference_solution_path: private/solutions/css-veryeasy-active-button-press.css
hint_ladder:
  1: "Bir butona tıklandığı anı temsil eden CSS sözde sınıfı hangisidir?"
  2: "Fare tuşuna basılı tutulurken aktifleşen durum belirteci nedir?"
  3: "Bu etkileşim kuralı 'aktif basılma durumu (:active pseudo-class)' olarak bilinir."
```

---

### css-veryeasy-focus-visible-outline

```yaml
id: css-veryeasy-focus-visible-outline
version: 1
language: css
engine: none
difficulty: very_easy
title: "Klavye kullanıcıları için belirgin odak halkası"
prompt: |
  Geliştiriciler sıklıkla estetik kaygılarla `outline: none` yazarak klavye kullanıcılarını
  sayfada kaybolmaya mahkum eder. Yalnızca klavyeden Tab tuşuyla odaklanan kullanıcılar için
  belirgin, 2 piksel kalınlığında ve elemanın dışından 2 piksel mesafeli duran modern
  odaklanma halkasını tanımlayın; fareyle tıklayan kullanıcılarda ise bu halkanın çıkmamasını sağlayın.
constraints:
  - "Modern odaklanma göstergesi yalnızca klavye odağında tetiklenmeli"
  - "Dış hat çizgisi ve elemandan ayrılma mesafesi tanımlanmalı"
concept_tags: [focus, accessibility]
checklist_extra:
  - ":focus yerine modern :focus-visible tercih edilmiş mi?"
  - "Çizginin elemana yapışmaması için outline-offset kullanılmış mı?"
reference_solution_path: private/solutions/css-veryeasy-focus-visible-outline.css
hint_ladder:
  1: "Yalnızca klavye odağını yakalayan modern sözde sınıf hangisidir?"
  2: "Odak çizgisinin elemanın sınırından biraz dışarıda durmasını sağlayan özellik nedir?"
  3: "Bu erişilebilirlik standardı 'klavye odak halkası (:focus-visible ve outline-offset)' olarak bilinir."
```

---

### css-veryeasy-opacity-disabled-state

```yaml
id: css-veryeasy-opacity-disabled-state
version: 1
language: css
engine: none
difficulty: very_easy
title: "Devre dışı bırakılmış eleman saydamlığı"
prompt: |
  Form henüz geçerli doldurulmadığında pasif durumda olan 'Gönder' butonunun tıklanamaz
  olduğunu görsel olarak kullanıcıya belli etmek istiyorsunuz. Devre dışı bırakılmış
  (`disabled`) butonun saydamlığını yüzde 50 seviyesine düşüren ve fare imlecini yasaklı/engelli
  işaretine dönüştüren kuralı yazın.
constraints:
  - "Devre dışı durum sözde sınıfı veya öznitelik seçicisi kullanılmalı"
  - "Saydamlık yarı yarıya azaltılmalı"
  - "İmleç engelli/yasaklı durumunu göstermeli"
concept_tags: [color, focus]
checklist_extra:
  - ":disabled sözde sınıfı kullanılmış mı?"
  - "İmleç için not-allowed değeri atanmış mı?"
reference_solution_path: private/solutions/css-veryeasy-opacity-disabled-state.css
hint_ladder:
  1: "Bir elemanın saydamlık derecesini ayarlayan özellik hangisidir?"
  2: "Tıklanamaz durumdaki imleç için cursor özelliğine hangi değer verilir?"
  3: "Bu durum tasarımı 'devre dışı saydamlık ve imleç kısıtı (disabled opacity)' olarak bilinir."
```

---

### css-veryeasy-letter-spacing-uppercase

```yaml
id: css-veryeasy-letter-spacing-uppercase
version: 1
language: css
engine: none
difficulty: very_easy
title: "Büyük harfli rozetlerde harf aralığı açma"
prompt: |
  Bir haber kartının en üstünde yer alan 'TEKNOLOJİ' veya 'EKONOMİ' kategori etiketleri
  tamamen büyük harflerle yazılmıştır. Büyük harfli kelimeler birbirine çok sıkışık
  göründüğü için okunabilirliği zayıflar. Bu etiketlerin harfleri arasındaki mesafeyi
  hafifçe açarak (örneğin 0.05em veya 1px) daha profesyonel ve okunaklı hale getirin.
constraints:
  - "Harfler arasındaki mesafe orantılı biçimde artırılmalı"
  - "Yalnızca ilgili kategori rozeti hedeflenmeli"
concept_tags: [typography, accessibility]
checklist_extra:
  - "Harf aralığını açmak için letter-spacing kullanılmış mı?"
  - "Değer aşırı abartılmadan okunabilir bir ölçüde mi tutulmuş?"
reference_solution_path: private/solutions/css-veryeasy-letter-spacing-uppercase.css
hint_ladder:
  1: "Metin içindeki harflerin birbirine olan uzaklığını belirleyen CSS özelliği nedir?"
  2: "Büyük harfli başlıklara ferahlık katmak için bu özelliğe pozitif bir değer nasıl verilir?"
  3: "Bu tipografi kuralı 'harf aralığı düzenlemesi (letter-spacing)' olarak bilinir."
```

---

### css-veryeasy-text-transform-capitalization

```yaml
id: css-veryeasy-text-transform-capitalization
version: 1
language: css
engine: none
difficulty: very_easy
title: "CSS ile metin büyük harf dönüştürme"
prompt: |
  Bir web sitesinin alt bilgi (footer) başlıklarının HTML içinde küçük veya karışık harflerle
  yazılmış olsa dahi ekranda her zaman tamamen BÜYÜK HARFLERLE görüntülenmesini istiyorsunuz.
  HTML içeriğini değiştirmeden, stil katmanı üzerinden metnin harf büyüklüğünü dönüştüren kuralı yazın.
constraints:
  - "Metin harfleri CSS aracılığıyla tamamen büyük harfe dönüştürülmeli"
  - "HTML metnine dokunulmadan stil ile çözülmeli"
concept_tags: [typography, maintainability]
checklist_extra:
  - "text-transform özelliği uppercase değeriyle atanmış mı?"
  - "HTML içeriğindeki orijinal metin korundu mu?"
reference_solution_path: private/solutions/css-veryeasy-text-transform-capitalization.css
hint_ladder:
  1: "Bir metnin harflerini büyük, küçük veya baş harfleri büyük yapan CSS özelliği nedir?"
  2: "Tüm karakterleri büyük harfe çevirmek için bu özelliğe hangi değer atanır?"
  3: "Bu metin biçimlendirme 'büyük harf dönüşümü (text-transform uppercase)' olarak bilinir."
```

---

### css-veryeasy-font-weight-hierarchy

```yaml
id: css-veryeasy-font-weight-hierarchy
version: 1
language: css
engine: none
difficulty: very_easy
title: "Tipografik görsel hiyerarşi ve kalınlık ayrımı"
prompt: |
  Bir makale sayfasında ana başlığın güçlü ve tok durması, gövde metninin ise standart
  okuma kalınlığında olması gerekmektedir. Başlık için sayısal olarak 700 (kalın/bold),
  paragraf metinleri için ise 400 (normal) ağırlığını tanımlayarak net bir görsel hiyerarşi kurun.
constraints:
  - "Başlık için sayısal kalınlık değeri 700 olarak tanımlanmalı"
  - "Paragraf için sayısal normal kalınlık değeri 400 olarak tanımlanmalı"
concept_tags: [typography, layout]
checklist_extra:
  - "font-weight özelliği sayısal değerlerle (700 ve 400) atanmış mı?"
  - "Başlık ve paragraf seçicileri ayrı ayrı hedeflenmiş mi?"
reference_solution_path: private/solutions/css-veryeasy-font-weight-hierarchy.css
hint_ladder:
  1: "Yazı tiplerinin et kalınlığını veya inceliğini belirleyen özellik hangisidir?"
  2: "Standart normal metin ve kalın metin için hangi yüzlük sayılar kullanılır?"
  3: "Bu tipografi temeli 'yazı tipi ağırlığı (font-weight)' olarak bilinir."
```

---

### css-veryeasy-background-color-page

```yaml
id: css-veryeasy-background-color-page
version: 1
language: css
engine: none
difficulty: very_easy
title: "Sayfa geneli sıcak arka plan tonu"
prompt: |
  Gözleri yoran saf parlak beyaz (`#ffffff`) yerine, tüm web sayfasının zeminine dinlendirici
  ve modern bir kırık beyaz / açık gri (`#f8fafc`) arka plan tonu tanımlayın. Bu rengin
  tüm sayfa tuvaline pürüzsüz uygulanması için sayfa gövdesini hedefleyin.
constraints:
  - "Sayfa gövdesine (body) açık gri/kırık beyaz zemin rengi atanmalı"
  - "Tüm sayfa yüksekliğini kapsayacak temel zemin oluşturulmalı"
concept_tags: [color, layout]
checklist_extra:
  - "Arka plan rengi body seçicisine tanımlanmış mı?"
  - "Renk değeri geçerli bir hex veya rgb kodu mu?"
reference_solution_path: private/solutions/css-veryeasy-background-color-page.css
hint_ladder:
  1: "Bir sayfanın veya kutunun zemin rengini değiştiren özellik nedir?"
  2: "Tüm sayfayı kapsayacak stil hangi ana HTML elemanına atanır?"
  3: "Bu temel stil 'gövde arka plan rengi (body background-color)' olarak bilinir."
```

---

### css-veryeasy-overflow-hidden-bounds

```yaml
id: css-veryeasy-overflow-hidden-bounds
version: 1
language: css
engine: none
difficulty: very_easy
title: "Yuvarlak kullanıcı avatarından taşan görseli kırpma"
prompt: |
  Kullanıcı profil kartında 64x64 piksel boyutunda tam yuvarlak bir avatar kutusu oluşturdunuz.
  İçine gelen kullanıcı fotoğrafı kare olduğu için yuvarlatılmış köşelerin dışına taşmakta
  ve yuvarlak görünümü bozmaktadır. Kapsayıcı kutunun dışına taşan tüm pikselleri maskeleyip
  kırparak kusursuz bir daire elde edin.
constraints:
  - "Kapsayıcı kutudan dışarı taşan içerik görünmez yapılmalı ve kırpılmalı"
  - "Köşe yuvarlatma kuralı ile uyumlu çalışmalı"
concept_tags: [layout, edge-cases]
checklist_extra:
  - "Taşmayı gizlemek için overflow: hidden kullanılmış mı?"
  - "Avatar kapsayıcısına yüzde 50 border-radius verilmiş mi?"
reference_solution_path: private/solutions/css-veryeasy-overflow-hidden-bounds.css
hint_ladder:
  1: "Bir kutunun sınırlarını aşan içeriği kırpan CSS özelliği nedir?"
  2: "Taşan kısımları tamamen gizlemek için overflow özelliğine hangi değer verilir?"
  3: "Bu kırpma tekniği 'taşma gizleme kuralı (overflow: hidden)' olarak bilinir."
```

---

### css-veryeasy-vertical-align-middle-icon

```yaml
id: css-veryeasy-vertical-align-middle-icon
version: 1
language: css
engine: none
difficulty: very_easy
title: "Metin yanındaki satır içi simgeyi dikeyde hizalama"
prompt: |
  Bir buton veya bağlantı metninin hemen yanında duran küçük bir satır içi simge (`<img>` veya `<svg>`)
  varsayılan olarak metnin taban çizgisine (baseline) oturduğu için metne göre aşağıda veya
  yukarıda kalmaktadır. Simgenin yanındaki metin satırının tam dikey merkezine oturmasını
  sağlayan satır içi dikey hizalama kuralını tanımlayın.
constraints:
  - "Satır içi elemanın dikey hizalaması metnin orta eksenine eşitlenmeli"
  - "Metin taban çizgisi uyumsuzluğu giderilmeli"
concept_tags: [layout, centering]
checklist_extra:
  - "vertical-align: middle kuralı simge elemanına uygulanmış mı?"
  - "Elemanın satır içi akışta kalması sağlandı mı?"
reference_solution_path: private/solutions/css-veryeasy-vertical-align-middle-icon.css
hint_ladder:
  1: "Satır içi (inline) elemanların birbiriyle dikey ilişkisini ayarlayan özellik nedir?"
  2: "Simgeyi metin satırının tam ortasına getirmek için hangi değer verilir?"
  3: "Bu hizalama 'satır içi dikey ortalama (vertical-align middle)' olarak bilinir."
```

---

### css-veryeasy-width-percentage-columns

```yaml
id: css-veryeasy-width-percentage-columns
version: 1
language: css
engine: none
difficulty: very_easy
title: "Yüzde tabanlı iki eşit sütun genişliği"
prompt: |
  Bir form alanında 'Ad' ve 'Soyad' girdi kutularının yan yana geldiğinde ekran genişliğinden
  bağımsız olarak her birinin satırın tam yarısını (%50) kaplamasını istiyorsunuz.
  Kutuların sabit pikselle kilitlenmeyip esnek bir şekilde ekranın yarısına oturmasını sağlayan
  genişlik kuralını yazın.
constraints:
  - "Her iki sütunun genişliği yüzde cinsinden tanımlanmalı"
  - "İki sütunun toplam genişliği satırın tamamını doldurmalı"
concept_tags: [responsive, layout]
checklist_extra:
  - "Genişlik değeri width: 50% olarak atanmış mı?"
  - "border-box ile kutuların taşması önlenmiş mi?"
reference_solution_path: private/solutions/css-veryeasy-width-percentage-columns.css
hint_ladder:
  1: "Bir elemanın genişliğini kapsayıcısına oranla belirlemek için hangi birim kullanılır?"
  2: "Tam yarı yarıya iki sütun oluşturmak için genişliğe ne yazılır?"
  3: "Bu esnek düzenleme 'yüzde tabanlı genişlik (percentage width)' olarak bilinir."
```

---

### css-veryeasy-height-full-viewport

```yaml
id: css-veryeasy-height-full-viewport
version: 1
language: css
engine: none
difficulty: very_easy
title: "Tüm ekran yüksekliğini kaplayan karşılama bölümü"
prompt: |
  Bir web sitesinin ana karşılama ekranının (hero section), kullanıcının ekran boyutu ne olursa
  olsun tarayıcı penceresinin dikey yüksekliğinin tamamını (%100) kaplamasını istiyorsunuz.
  Görsel alan yüksekliği birimini kullanarak bu bölümün tam ekran yüksekliğinde açılmasını sağlayın.
constraints:
  - "Yükseklik değeri tarayıcının görünür alan yüksekliğine (viewport) göre ayarlanmalı"
  - "İçerik daha uzun olduğunda taşmayı engellemek için minimum yükseklik tercih edilmeli"
concept_tags: [responsive, layout]
checklist_extra:
  - "vh veya modern vh/dvh birimi kullanılmış mı?"
  - "height yerine içerik taşmasına izin veren min-height tercih edilmiş mi?"
reference_solution_path: private/solutions/css-veryeasy-height-full-viewport.css
hint_ladder:
  1: "Tarayıcının görünür ekran yüksekliğini temsil eden CSS birimi nedir?"
  2: "Ekranın yüzde yüz yüksekliğini almak için 100 değerinin yanına hangi birim konur?"
  3: "Bu boyutlandırma kuralı 'görünür alan yüksekliği (viewport height min-height)' olarak bilinir."
```

---

### css-veryeasy-word-break-long-urls

```yaml
id: css-veryeasy-word-break-long-urls
version: 1
language: css
engine: none
difficulty: very_easy
title: "Uzun bağlantıların kart dışına taşmasını engelleme"
prompt: |
  Bir yorum alanında kullanıcının paylaştığı 150 karakterlik kesintisiz bir internet bağlantısı
  (URL) veya şifrelenmiş metin, boşluk içermediği için dar mobil kartın sağından dışarı fırlamakta
  ve ekranı bozmaktadır. Normalde bölünmeyen çok uzun kelimelerin kutu sınırına geldiğinde
  alt satıra kırılmasını sağlayan kuralı tanımlayın.
constraints:
  - "Uzun kesintisiz dizgiler kutu kenarında alt satıra kırılmalı"
  - "Yatay taşma çubuğu oluşması engellenmeli"
concept_tags: [typography, edge-cases]
checklist_extra:
  - "word-break: break-word veya overflow-wrap: break-word kullanılmış mı?"
  - "Kural metni barındıran elemana veya kapsayıcıya atanmış mı?"
reference_solution_path: private/solutions/css-veryeasy-word-break-long-urls.css
hint_ladder:
  1: "Boşluksuz uzun kelimelerin satır sonundan taşmasını engelleyen özellik nedir?"
  2: "Kelimeleri gerekirse harf ortasından kırmak için hangi değer verilir?"
  3: "Bu tipografi güvenliği 'kelime bölme ve satır sarma (overflow-wrap break-word)' olarak bilinir."
```

---

### css-veryeasy-white-space-nowrap-badge

```yaml
id: css-veryeasy-white-space-nowrap-badge
version: 1
language: css
engine: none
difficulty: very_easy
title: "Çok kelimeli durum rozetinin ikiye bölünmesini engelleme"
prompt: |
  Bir tabloda ürünün durumunu gösteren 'Stokta Var' veya 'Teslim Edildi' şeklinde küçük durum
  rozetleri yer almaktadır. Tablo sütunu daraldığında bu rozetin içindeki iki kelime alt alta
  kırılarak çirkin bir görüntü oluşturmaktadır. Rozet metninin hiçbir koşulda alt satıra
  geçmemesini, her zaman tek bir satırda kalmasını garanti eden kuralı yazın.
constraints:
  - "Metnin kelimeler arasından alt satıra kırılması engellenmeli"
  - "Rozet içeriği tek satır bütünlüğünü korumalı"
concept_tags: [typography, edge-cases]
checklist_extra:
  - "white-space özelliği nowrap olarak atanmış mı?"
  - "Rozet elemanının sınırları korunmuş mu?"
reference_solution_path: private/solutions/css-veryeasy-white-space-nowrap-badge.css
hint_ladder:
  1: "Bir metnin boşluklardan alt satıra kırılmasını kontrol eden özellik nedir?"
  2: "Metnin asla kırılmamasını sağlamak için bu özelliğe hangi değer verilir?"
  3: "Bu metin düzenleme 'satır kırılmasını önleme (white-space nowrap)' olarak bilinir."
```

---

### css-veryeasy-border-radius-pill-badge

```yaml
id: css-veryeasy-border-radius-pill-badge
version: 1
language: css
engine: none
difficulty: very_easy
title: "Kusursuz kapsül şeklinde oval rozet tasarımı"
prompt: |
  Bir e-ticaret sitesinde indirim oranını belirten rozetin kenarlarının hafif kavisli değil,
  tam bir ilaç kapsülü (pill) şeklinde iki ucu yarım daire olacak biçimde tasarlanması istenmektedir.
  Rozetin genişliği metne göre artsa bile her zaman kusursuz kapsül formunu korumasını sağlayan
  yüksek yarıçap kuralını yazın.
constraints:
  - "Rozet uçları tam dairesel kıvrıma sahip olmalı"
  - "Metin uzadığında köşelerin şekli bozulmamalı"
concept_tags: [layout, maintainability]
checklist_extra:
  - "Yüksek bir piksel değeri (örn. 9999px veya 50px) kullanılmış mı?"
  - "Yüzde 50 yerine elipsleşmeyi önleyen yüksek piksel tekniği tercih edilmiş mi?"
reference_solution_path: private/solutions/css-veryeasy-border-radius-pill-badge.css
hint_ladder:
  1: "Köşeleri yuvarlatan border-radius özelliğine çok büyük bir piksel değeri verilirse ne olur?"
  2: "Dikdörtgen kutuları elips yapmadan kapsül haline getiren değer taktiği nedir?"
  3: "Bu tasarım tekniği 'kapsül rozet yuvarlatması (pill shape border-radius)' olarak bilinir."
```

---

### css-veryeasy-box-shadow-subtle-elevation

```yaml
id: css-veryeasy-box-shadow-subtle-elevation
version: 1
language: css
engine: none
difficulty: very_easy
title: "Zarif kart derinliği ve alt gölge efekti"
prompt: |
  Açık renkli bir arka plan üzerinde duran beyaz kartın sayfadan hafifçe havaya kalkmış
  gibi durmasını istiyorsunuz. Kartın altına sert ve siyah bir leke yerine, aşağıya doğru
  4 piksel inen, 12 piksel bulanıklığa sahip ve hafif saydam siyah renkte zarif bir gölge ekleyin.
constraints:
  - "Yatay ve dikey kayma, bulanıklık yarıçapı ve renk tanımlanmalı"
  - "Gölge rengi saydam siyah (rgba) olarak ayarlanmalı"
concept_tags: [color, layout]
checklist_extra:
  - "box-shadow özelliği doğru parametre sırasıyla yazılmış mı?"
  - "Sert siyah yerine yumuşak rgba rengi tercih edilmiş mi?"
reference_solution_path: private/solutions/css-veryeasy-box-shadow-subtle-elevation.css
hint_ladder:
  1: "Kutulara dış veya iç gölge ekleyen CSS özelliği nedir?"
  2: "Gölgenin sertliğini kırıp yayılmasını sağlayan üçüncü parametre nedir?"
  3: "Bu görsel derinlik 'kutu gölgesi tanımlaması (box-shadow elevation)' olarak bilinir."
```

---

### css-veryeasy-color-rgb-alpha-backdrop

```yaml
id: css-veryeasy-color-rgb-alpha-backdrop
version: 1
language: css
engine: none
difficulty: very_easy
title: "Yarı saydam karartma katmanı rengi"
prompt: |
  Bir fotoğraf galerisinde görselin üzerinde beliren açıklama şeridinin arkasındaki resmi
  tamamen kapatmak istemiyorsunuz. Şeridin zeminine yüzde 60 opaklığa sahip siyah bir renk
  vererek, arkadaki görselin hafifçe görünmesini ama üzerindeki beyaz yazıların da net okunmasını
  sağlayan renk fonksiyonunu yazın.
constraints:
  - "Arka plan rengi alfa kanalı (saydamlık) içeren bir renk fonksiyonuyla tanımlanmalı"
  - "Yazıların okunabilirliği için yeterli karartma sağlanmalı"
concept_tags: [color, accessibility]
checklist_extra:
  - "rgba veya modern rgb(r g b / alpha) sözdizimi kullanılmış mı?"
  - "opacity özelliği yerine yalnızca arka planı saydam yapan renk mi seçilmiş?"
reference_solution_path: private/solutions/css-veryeasy-color-rgb-alpha-backdrop.css
hint_ladder:
  1: "Bir renge saydamlık derecesi (alfa) ekleyen renk modeli nedir?"
  2: "Bütün elemanı değil sadece arka planı yarı saydam yapmak için hangi özellik kullanılır?"
  3: "Bu renk tekniği 'alfa kanallı arka plan rengi (rgba background)' olarak bilinir."
```

---

### css-veryeasy-margin-collapsing-prevention

```yaml
id: css-veryeasy-margin-collapsing-prevention
version: 1
language: css
engine: none
difficulty: very_easy
title: "İç boşluk ile dikey dış boşluk çökmesini önleme"
prompt: |
  Bir bölüm (`<section>`) içerisindeki ilk başlığa üst dış boşluk (margin-top) verdiğinizde,
  bu boşluk bölümün içinde kalmak yerine bölümü de aşağı itmekte ve bölümün dışına taşmaktadır
  (margin collapsing). Bölüm kapsayıcısına minik bir iç boşluk ekleyerek veya uygun bir taşma
  kuralıyla çocuk elemanın dış boşluğunun ebeveyn sınırları içinde kalmasını sağlayın.
constraints:
  - "Ebeveyn ve ilk çocuk arasındaki dikey dış boşluk çökmesi engellenmeli"
  - "Çocuğun üst boşluğu bölüm içinde doğru mesafeyi üretmeli"
concept_tags: [layout, edge-cases]
checklist_extra:
  - "Çöküşü engellemek için ebeveyne padding veya overflow kuralı uygulanmış mı?"
  - "Görsel düzen bozulmadan dikey ritim korundu mu?"
reference_solution_path: private/solutions/css-veryeasy-margin-collapsing-prevention.css
hint_ladder:
  1: "Dikey dış boşlukların birbirinin içine geçmesi olayına ne ad verilir?"
  2: "Ebeveyn elemana 1px bile olsa padding verildiğinde bu boşluk birleşmesine ne olur?"
  3: "Bu mizanpaj çözümü 'dış boşluk çökmesi engelleme (margin collapsing prevention)' olarak bilinir."
```

---

### css-veryeasy-child-combinator-selector

```yaml
id: css-veryeasy-child-combinator-selector
version: 1
language: css
engine: none
difficulty: very_easy
title: "Yalnızca doğrudan çocuk liste elemanlarını hedefleme"
prompt: |
  İç içe geçmiş çok düzeyli bir menüde (`<ul>` içinde alt `<ul>`), en üst düzey menü
  elemanlarını yan yana dizmek istiyorsunuz. Ancak yazdığınız liste seçicisi yanlışlıkla
  alt açılır menünün içindeki tüm maddeleri de etkilemektedir. Yalnızca menünün doğrudan
  ilk düzey çocuklarını hedefleyen ve torunları etkilemeyen çocuk birleştirici seçiciyi yazın.
constraints:
  - "Yalnızca bir düzey altındaki doğrudan çocuk elemanlar seçilmeli"
  - "Daha derin alt menü maddeleri bu kuraldan etkilenmemeli"
concept_tags: [specificity, maintainability]
checklist_extra:
  - "Doğrudan çocuk birleştiricisi (>) kullanılmış mı?"
  - "Tüm torunları seçen boşluk seçicisi yerine kesin hiyerarşi kurulmuş mu?"
reference_solution_path: private/solutions/css-veryeasy-child-combinator-selector.css
hint_ladder:
  1: "CSS'te sadece bir alt basamaktaki öz çocukları seçmek için hangi sembol kullanılır?"
  2: "Boşluk ile büyüktür (>) işareti arasındaki fark nedir?"
  3: "Bu seçici türü 'doğrudan çocuk birleştiricisi (child combinator >)' olarak bilinir."
```

---

### css-veryeasy-adjacent-sibling-spacing

```yaml
id: css-veryeasy-adjacent-sibling-spacing
version: 1
language: css
engine: none
difficulty: very_easy
title: "Başlıktan hemen sonra gelen ilk paragrafa özel aralık"
prompt: |
  Bir edebi makalede, bölüm başlığından (`<h2>`) hemen sonra gelen ilk paragrafa özel bir üst
  boşluk tanımlamak istiyorsunuz; ancak başlığı takip etmeyen diğer normal paragrafların bu
  boşluğu almaması gerekmektedir. Bir elemanın hemen ardılı olan kardeşi hedefleyen seçiciyi yazın.
constraints:
  - "Yalnızca h2'nin hemen ardından gelen ilk paragraf seçilmeli"
  - "Diğer paragraflar bu kuraldan muaf tutulmalı"
concept_tags: [specificity, typography]
checklist_extra:
  - "Bitişik kardeş seçicisi (+) kullanılmış mı?"
  - "Genel kardeş seçicisi (~) ile karıştırılmadan tekil kardeş hedeflenmiş mi?"
reference_solution_path: private/solutions/css-veryeasy-adjacent-sibling-spacing.css
hint_ladder:
  1: "Bir elemanın hemen peşinden gelen ilk kardeş elemanı hangi sembolle seçeriz?"
  2: "h2 + p sözdizimi hangi paragrafları etkiler?"
  3: "Bu seçici türü 'bitişik kardeş seçicisi (adjacent sibling combinator +)' olarak bilinir."
```

---

### css-veryeasy-descendant-selector-scoped

```yaml
id: css-veryeasy-descendant-selector-scoped
version: 1
language: css
engine: none
difficulty: very_easy
title: "Kart içindeki başlıkları sayfadaki diğer başlıklardan yalıtma"
prompt: |
  Web sitesindeki tüm `<h3>` başlıkları 24 piksel boyuta sahiptir. Ancak yan sütunda (sidebar)
  yer alan kartların içindeki `<h3>` başlıklarının daha küçük (16 piksel) olması istenmektedir.
  Sayfa genelindeki ana stilleri bozmadan, sadece yan sütun kapsayıcısının içindeki başlıkları
  hedefleyen torun seçici kuralını yazın.
constraints:
  - "Kural yalnızca belirtilen kapsayıcı içindeki başlıkları etkilemeli"
  - "Sayfanın geri kalanındaki h3 başlıkları değişmeden kalmalı"
concept_tags: [specificity, maintainability]
checklist_extra:
  - "Kapsayıcı sınıfı ile eleman arasına boşluk konularak torun seçimi yapılmış mı?"
  - "Özgüllük gereksiz yere şişirilmeden amaca uygun scoped edilmiş mi?"
reference_solution_path: private/solutions/css-veryeasy-descendant-selector-scoped.css
hint_ladder:
  1: "Bir elemanın içinde herhangi bir derinlikteki çocukları seçmek için ne kullanılır?"
  2: "Kapsayıcı sınıfı ile hedef etiket arasına hangi ayıraç konur?"
  3: "Bu seçici türü 'torun seçicisi (descendant selector)' olarak bilinir."
```

---

### css-veryeasy-first-child-pseudo-class

```yaml
id: css-veryeasy-first-child-pseudo-class
version: 1
language: css
engine: none
difficulty: very_easy
title: "Yatay menüdeki ilk elemanın sol kenarlığını kaldırma"
prompt: |
  Yatay bir gezinti çubuğundaki menü öğelerinin arasına dikey birer çizgi (`border-left`)
  koydunuz. Ancak listenin en başındaki ilk elemanın solunda da çizgi belirmekte ve menünün
  dış çerçevesinde çirkin bir fazlalık oluşturmaktadır. Listenin yalnızca ilk çocuğunu
  hedefleyerek bu sol çizgiyi sıfırlayan sözde sınıfı yazın.
constraints:
  - "Yalnızca kardeşler arasındaki en baştaki ilk eleman hedeflenmeli"
  - "İlk elemanın sol kenarlığı kaldırılmalı, diğer elemanlarınki korunmalı"
concept_tags: [layout, specificity]
checklist_extra:
  - ":first-child sözde sınıfı kullanılmış mı?"
  - "Sol kenarlık border-left: none ile sıfırlanmış mı?"
reference_solution_path: private/solutions/css-veryeasy-first-child-pseudo-class.css
hint_ladder:
  1: "Bir kapsayıcı içindeki aynı türden ilk kardeşi seçen sözde sınıf nedir?"
  2: "En baştaki elemanın sol kenarlığını kapatmak için hangi sözde sınıf bağlanır?"
  3: "Bu seçici kuralı 'ilk çocuk seçicisi (:first-child pseudo-class)' olarak bilinir."
```

---

### css-veryeasy-last-child-pseudo-class

```yaml
id: css-veryeasy-last-child-pseudo-class
version: 1
language: css
engine: none
difficulty: very_easy
title: "Dikey listenin sonundaki ayraç çizgisini temizleme"
prompt: |
  Bir bildirim listesinde her bildirim maddesinin altında 1 piksel gri ayraç çizgisi
  (`border-bottom`) bulunmaktadır. Ancak listenin en altındaki son elemanın altındaki çizgi
  kartın alt kenarıyla çakışarak çift çizgi görüntüsü yaratmaktadır. Listenin yalnızca en son
  maddesini hedefleyerek bu alt kenarlığı kaldıran kuralı yazın.
constraints:
  - "Yalnızca listenin en son elemanı hedeflenmeli"
  - "Son elemanın alt kenarlığı kaldırılmalı, aradaki ayraçlar korunmalı"
concept_tags: [layout, specificity]
checklist_extra:
  - ":last-child sözde sınıfı kullanılmış mı?"
  - "border-bottom: none kuralı atanmış mı?"
reference_solution_path: private/solutions/css-veryeasy-last-child-pseudo-class.css
hint_ladder:
  1: "Kardeşler arasındaki en son elemanı seçmek için hangi sözde sınıf kullanılır?"
  2: "Listenin bitişindeki fazlalık çizgiyi silmek için ne yazılır?"
  3: "Bu seçici kuralı 'son çocuk seçicisi (:last-child pseudo-class)' olarak bilinir."
```

---

### css-veryeasy-nth-child-zebra-striping

```yaml
id: css-veryeasy-nth-child-zebra-striping
version: 1
language: css
engine: none
difficulty: very_easy
title: "Tablo satırlarında zebra çizgili ardışık arka plan"
prompt: |
  Çok satırlı bir finans tablosunda satırların birbiriyle karışmasını önlemek ve gözün satırları
  kolay takip etmesini sağlamak istiyorsunuz. Tablonun çift numaralı satırlarına (2, 4, 6...)
  hafif açık gri bir arka plan rengi tanımlayan dinamik formül seçicisini yazın.
constraints:
  - "Çift numaralı satırlar tek bir dinamik sözde sınıf ile hedeflenmeli"
  - "Tek numaralı satırların beyaz kalması sağlanmalı"
concept_tags: [layout, specificity]
checklist_extra:
  - ":nth-child(even) veya :nth-child(2n) kullanılmış mı?"
  - "Kural tbody içindeki tr satırlarına mı uygulanmış?"
reference_solution_path: private/solutions/css-veryeasy-nth-child-zebra-striping.css
hint_ladder:
  1: "Elemanları sıralarına ve matematiksel formüle göre seçen sözde sınıf hangisidir?"
  2: "Çift sıralı elemanları seçmek için bu sözde sınıfa hangi parametre yazılır?"
  3: "Bu tablo tekniği 'zebra satır renklendirmesi (:nth-child even)' olarak bilinir."
```

---

### css-veryeasy-not-pseudo-class-filter

```yaml
id: css-veryeasy-not-pseudo-class-filter
version: 1
language: css
engine: none
difficulty: very_easy
title: "Birincil eylem butonu hariç diğer tüm butonları seçme"
prompt: |
  Bir formun altında üç adet buton bulunmaktadır: 'Kaydet' (ana buton, `.btn-primary`),
  'Taslak Olarak Sakla' ve 'İptal'. Ana buton hariç diğer tüm ikincil butonlara şeffaf arka plan
  ve gri kenarlık vermek istiyorsunuz. Belirli bir sınıfı taşımayan elemanları filtreleyen
  olumsuzluk sözde sınıfını kullanarak bu kuralı yazın.
constraints:
  - "Belirtilen istisna sınıfı taşımayan butonlar hedeflenmeli"
  - "İstisna sınıfına sahip eleman bu kuraldan etkilenmemeli"
concept_tags: [specificity, maintainability]
checklist_extra:
  - ":not(.btn-primary) seçicisi kullanılmış mı?"
  - "İkincil stiller başarıyla uygulanmış mı?"
reference_solution_path: private/solutions/css-veryeasy-not-pseudo-class-filter.css
hint_ladder:
  1: "CSS'te 'bu kural şu sınıfa sahip olmayanlara uygulansın' demek için hangi filtre sözde sınıfı kullanılır?"
  2: "Hariç tutma parantezi içine ne yazılır?"
  3: "Bu seçici filtresi 'olumsuzluk seçicisi (:not pseudo-class)' olarak bilinir."
```

---

### css-veryeasy-attribute-selector-external

```yaml
id: css-veryeasy-attribute-selector-external
version: 1
language: css
engine: none
difficulty: very_easy
title: "Yeni sekmede açılan dış bağlantıları hedefleme"
prompt: |
  Web sitenizdeki köprüler arasında yeni tarayıcı sekmesinde açılan dış bağlantılar bulunmaktadır.
  Bu bağlantıların yanına stil vermek veya farklı bir renk atamak için, HTML kodunda
  `target="_blank"` niteliği taşıyan tüm `<a>` etiketlerini yakalayan öznitelik seçicisini yazın.
constraints:
  - "Yalnızca belirli hedef özniteliğine sahip bağlantılar seçilmeli"
  - "Site içi normal bağlantılar bu kuraldan etkilenmemeli"
concept_tags: [specificity, accessibility]
checklist_extra:
  - "Köşeli parantezli öznitelik seçicisi a[target='_blank'] kullanılmış mı?"
  - "Nitelik değeri tırnak içinde doğru belirtilmiş mi?"
reference_solution_path: private/solutions/css-veryeasy-attribute-selector-external.css
hint_ladder:
  1: "HTML etiketlerinin niteliklerine göre stil uygulamak için hangi parantez kullanılır?"
  2: "[target='_blank'] seçicisi hangi bağlantıları yakalar?"
  3: "Bu seçici türü 'öznitelik seçicisi (attribute selector)' olarak bilinir."
```

---

### css-veryeasy-visited-link-privacy

```yaml
id: css-veryeasy-visited-link-privacy
version: 1
language: css
engine: none
difficulty: very_easy
title: "Ziyaret edilmiş bağlantıların renk ayrımı"
prompt: |
  Bir arama sonuçları veya makale listesinde, kullanıcının daha önce tıkladığı bağlantıları
  henüz tıklamadıklarından görsel olarak ayırt edebilmesi kullanıcı deneyimi için kritiktir.
  Kullanıcının geçmişte ziyaret ettiği bağlantıların rengini hafif soluk bir mor tona dönüştüren
  güvenli geçmiş sözde sınıfını tanımlayın.
constraints:
  - "Ziyaret edilmiş bağlantı durumu sözde sınıfı kullanılmalı"
  - "Yalnızca gizlilik izinli renk özelliği güncellenmeli"
concept_tags: [color, accessibility]
checklist_extra:
  - ":visited sözde sınıfı kullanılmış mı?"
  - "Tarayıcı gizlilik kısıtlamalarına uygun şekilde yalnızca color mı değiştirilmiş?"
reference_solution_path: private/solutions/css-veryeasy-visited-link-privacy.css
hint_ladder:
  1: "Daha önce tıklanmış bağlantıları hedefleyen sözde sınıf hangisidir?"
  2: "Kullanıcı gizliliğini korumak için bu sözde sınıfta sadece hangi özelliklerin değişimine izin verilir?"
  3: "Bu bağlantı durumu 'ziyaret edilmiş köprü seçicisi (:visited)' olarak bilinir."
```

---

### css-veryeasy-display-none-toggle

```yaml
id: css-veryeasy-display-none-toggle
version: 1
language: css
engine: none
difficulty: very_easy
title: "Elemanı akıştan tamamen çıkarma ve gizleme"
prompt: |
  Sayfadaki bir uyarı kutusu kapatıldığında veya bir sekme pasifleştiğinde, bu elemanın
  ekranda görünmemesi ve sayfada hiçbir boşluk (yer) kaplamaması gerekmektedir. Elemanı
  hem görsel olarak gizleyen hem de belge mizanpaj akışından tamamen çıkaran yardımcı sınıfı yazın.
constraints:
  - "Eleman ekranda görünmez olmalı"
  - "Mizanpajda işgal ettiği tüm alan sıfırlanmalı"
concept_tags: [layout, maintainability]
checklist_extra:
  - "display: none kuralı kullanılmış mı?"
  - "visibility: hidden ile arasındaki alan işgali farkı gözetilmiş mi?"
reference_solution_path: private/solutions/css-veryeasy-display-none-toggle.css
hint_ladder:
  1: "Bir elemanı hem görünmez yapıp hem de kapladığı yeri tamamen yok eden özellik nedir?"
  2: "Elemanın sanki DOM'da hiç yokmuş gibi yer tutmamasını sağlayan değer hangisidir?"
  3: "Bu temel gizleme kuralı 'akıştan çıkarma ve gizleme (display: none)' olarak bilinir."
```

---

### css-veryeasy-visibility-hidden-reserve

```yaml
id: css-veryeasy-visibility-hidden-reserve
version: 1
language: css
engine: none
difficulty: very_easy
title: "Yerini koruyarak elemanı görünmez kılma"
prompt: |
  Bir form alanının yanında bir onay ikonu yer almaktadır. İkon henüz görünür olmadığında
  bile yanındaki form kutusunun zıplamasını veya yer değiştirmesini engellemek için, ikonun
  işgal ettiği alanı aynen koruyarak kendisini geçici olarak görünmez yapan kuralı yazın.
constraints:
  - "Eleman görsel olarak görünmez olmalı"
  - "Sayfa mizanpajında kapladığı fiziksel genişlik ve yükseklik korunmalı"
concept_tags: [layout, edge-cases]
checklist_extra:
  - "visibility: hidden özelliği tercih edilmiş mi?"
  - "display: none kullanılmayarak düzen zıplaması önlenmiş mi?"
reference_solution_path: private/solutions/css-veryeasy-visibility-hidden-reserve.css
hint_ladder:
  1: "Bir elemanı görünmez yaparken kapladığı boşluğu aynen koruyan özellik nedir?"
  2: "visibility özelliğine hangi değer verildiğinde eleman şeffaf bir boşluk gibi yer tutar?"
  3: "Bu mizanpaj koruma tekniği 'yer koruyarak gizleme (visibility: hidden)' olarak bilinir."
```

---

### css-veryeasy-reset-button-styles

```yaml
id: css-veryeasy-reset-button-styles
version: 1
language: css
engine: none
difficulty: very_easy
title: "Tarayıcı varsayılan buton stillerini sıfırlama"
prompt: |
  Özel tasarımlı bir ikon butonu oluşturmak için `<button>` etiketi kullandınız. Ancak tarayıcı
  butona gri degrade bir zemin, kalın bir kenarlık ve gereksiz iç boşluklar eklemiştir.
  Butonun tüm yerleşik tarayıcı zeminini şeffaf yapan, kenarlığını ve varsayılan dolgularını
  sıfırlayan temel sıfırlama kuralını yazın.
constraints:
  - "Arka plan şeffaf yapılmalı"
  - "Kenarlık tamamen kaldırılmalı"
  - "Yazı tipi miras alınmalı"
concept_tags: [maintainability, layout]
checklist_extra:
  - "background: transparent veya none atanmış mı?"
  - "border: none ile yerel kenarlık silinmiş mi?"
reference_solution_path: private/solutions/css-veryeasy-reset-button-styles.css
hint_ladder:
  1: "Tarayıcının butona koyduğu arka planı şeffaf yapmak için ne yazılır?"
  2: "Butonun çerçevesini kaldırmak için border özelliğine hangi değer atanır?"
  3: "Bu biçimlendirme temizliği 'buton stili sıfırlama (button reset)' olarak bilinir."
```

---

### css-veryeasy-input-placeholder-color

```yaml
id: css-veryeasy-input-placeholder-color
version: 1
language: css
engine: none
difficulty: very_easy
title: "Form yer tutucu metin rengini özelleştirme"
prompt: |
  Bir arama kutusunun içindeki ipucu metninin (`placeholder`), varsayılan koyu gri rengi
  yerine marka renk paletinize uygun açık duman tonunda (`#94a3b8`) görüntülenmesini istiyorsunuz.
  Girdi kutularının yer tutucu metinlerini hedefleyen standart sözde elemanı yazın.
constraints:
  - "Girdi elemanlarının yer tutucu metni sözde eleman ile hedeflenmeli"
  - "Belirtilen açık renk tonu tanımlanmalı"
concept_tags: [color, typography]
checklist_extra:
  - "Çift iki noktalı ::placeholder sözde elemanı kullanılmış mı?"
  - "Renk değeri okunabilirlik sınırları içinde mi?"
reference_solution_path: private/solutions/css-veryeasy-input-placeholder-color.css
hint_ladder:
  1: "Girdi kutularındaki ipucu yazısını hedefleyen CSS sözde elemanı nedir?"
  2: "::placeholder sözde elemanında yazı rengi hangi özellikle değiştirilir?"
  3: "Bu form stili 'yer tutucu metin özelleştirmesi (::placeholder pseudo-element)' olarak bilinir."
```

---

### css-veryeasy-selection-highlight-color

```yaml
id: css-veryeasy-selection-highlight-color
version: 1
language: css
engine: none
difficulty: very_easy
title: "Metin seçim vurgu rengini özelleştirme"
prompt: |
  Kullanıcı sayfadaki yazıları fare ile seçtiğinde (mavi tarama yaptığında), işletim sisteminin
  varsayılan parlak mavi seçimi yerine sitenizin temasına uygun sarı arka plan ve siyah yazı
  rengi belirmesini istiyorsunuz. Kullanıcı metin seçimini küresel olarak stilize eden sözde elemanı yazın.
constraints:
  - "Tüm sayfadaki metin seçimi durumu sözde eleman ile yakalanmalı"
  - "Seçim arka planı ve metin rengi tanımlanmalı"
concept_tags: [color, accessibility]
checklist_extra:
  - "::selection sözde elemanı doğru tanımlanmış mı?"
  - "Seçili metin ile zemin arasındaki kontrast yeterli mi?"
reference_solution_path: private/solutions/css-veryeasy-selection-highlight-color.css
hint_ladder:
  1: "Kullanıcının fareyle seçtiği metin alanını hedefleyen sözde eleman hangisidir?"
  2: "Seçili alanın zemin ve yazı rengini hangi sözde eleman altında değiştiririz?"
  3: "Bu stil kuralı 'metin seçimi vurgusu (::selection pseudo-element)' olarak bilinir."
```

---

### css-veryeasy-smooth-scrolling-root

```yaml
id: css-veryeasy-smooth-scrolling-root
version: 1
language: css
engine: none
difficulty: very_easy
title: "Sayfa içi bağlantılarda pürüzsüz kaydırma"
prompt: |
  Kullanıcı sayfanın üstündeki 'İletişim' bağlantısına tıkladığında, tarayıcının sayfanın
  altındaki `#iletisim` bölümüne bir anda küt diye zıplaması yerine ekranın pürüzsüz ve
  yumuşak bir şekilde aşağı doğru kaymasını (smooth scroll) sağlayan kök kuralı tanımlayın.
constraints:
  - "Pürüzsüz kaydırma davranışı kök elemana (`html`) uygulanmalı"
  - "Sayfa içi çapa atlamaları akıcı hale getirilmeli"
concept_tags: [animation, maintainability]
checklist_extra:
  - "scroll-behavior özelliği smooth olarak atanmış mı?"
  - "Kural html veya :root seçicisine mi uygulanmış?"
reference_solution_path: private/solutions/css-veryeasy-smooth-scrolling-root.css
hint_ladder:
  1: "Tarayıcının sayfa içi bağlantılara zıplamak yerine kayarak gitmesini sağlayan özellik nedir?"
  2: "scroll-behavior özelliğine hangi değer verildiğinde kayma yumuşak olur?"
  3: "Bu sayfa gezintisi 'pürüzsüz kaydırma davranışı (scroll-behavior: smooth)' olarak bilinir."
```

---

### css-veryeasy-user-select-none-toolbar

```yaml
id: css-veryeasy-user-select-none-toolbar
version: 1
language: css
engine: none
difficulty: very_easy
title: "Araç çubuğu butonlarında kazara metin seçimini önleme"
prompt: |
  Bir web uygulamasının üst araç çubuğundaki butonlara veya açılır menü başlıklarına kullanıcı
  hızlıca çift tıkladığında, butonların üzerindeki metinler mavi olarak seçilmekte ve çirkin
  bir görüntü oluşmaktadır. Bu etkileşimli kontrol elemanlarının üzerindeki metinlerin fare ile
  taranarak seçilmesini engelleyen kuralı yazın.
constraints:
  - "Eleman üzerindeki metin seçimi devre dışı bırakılmalı"
  - "Tıklanabilirlik ve etkileşim engellenmemeli"
concept_tags: [accessibility, maintainability]
checklist_extra:
  - "user-select özelliği none olarak ayarlanmış mı?"
  - "Butonun tıklanabilirliği korunmuş mu?"
reference_solution_path: private/solutions/css-veryeasy-user-select-none-toolbar.css
hint_ladder:
  1: "Kullanıcının bir metni fareyle tarayıp seçmesini engelleyen CSS özelliği nedir?"
  2: "Metin seçimini kapatmak için bu özelliğe hangi değer verilir?"
  3: "Bu arayüz kuralı 'kullanıcı metin seçimi engeli (user-select: none)' olarak bilinir."
```

---

### css-veryeasy-text-overflow-ellipsis-single

```yaml
id: css-veryeasy-text-overflow-ellipsis-single
version: 1
language: css
engine: none
difficulty: very_easy
title: "Taşan tek satırlık başlığı üç nokta ile kırpma"
prompt: |
  Bir müzik çaların alt çubuğunda şarkı adını gösteren tek satırlık bir alan bulunmaktadır.
  Şarkı adı çok uzun olduğunda metin alt satıra geçmemeli, çubuğun dışına taşmamalı ve
  sığmayan kısmın sonunda otomatik olarak üç nokta (...) belirmelidir. Bu klasik tek satır
  kırpma üçlüsünü tanımlayın.
constraints:
  - "Metin tek satırda kalmaya zorlanmalı"
  - "Taşan kısım gizlenmeli"
  - "Taşma ucuna üç nokta işareti eklenmeli"
concept_tags: [typography, edge-cases]
checklist_extra:
  - "white-space: nowrap, overflow: hidden ve text-overflow: ellipsis üçlüsü eksiksiz mi?"
  - "Genişlik sınırı olan bir elemana uygulanmış mı?"
reference_solution_path: private/solutions/css-veryeasy-text-overflow-ellipsis-single.css
hint_ladder:
  1: "Metnin sonuna üç nokta koymak için hangi üç özelliğin birlikte kullanılması şarttır?"
  2: "Taşan metni üç nokta ile bitiren özellik ve değer hangisidir?"
  3: "Bu tipografi deseni 'tek satır metin kırpma (text-overflow: ellipsis)' olarak bilinir."
```

---

### css-veryeasy-min-height-footer-stick

```yaml
id: css-veryeasy-min-height-footer-stick
version: 1
language: css
engine: none
difficulty: very_easy
title: "Az içerikli sayfalarda altbilgiyi alta sabitleme temeli"
prompt: |
  İçeriği çok az olan sayfalarda (örneğin boş sepet veya 404 sayfası), sayfa altbilgisi (footer)
  ekranın ortasına kadar yükselmekte ve altta çirkin bir boşluk kalmaktadır. Sayfa gövdesinin
  en az görünür ekran yüksekliği kadar uzamasını sağlayarak altbilginin ekranın en altına
  itilmesini kolaylaştıran temel dikey minimum sınır kuralını yazın.
constraints:
  - "Gövde elemanına ekran boyuna eşit minimum yükseklik verilmeli"
  - "İçerik uzadığında dikey kaydırmaya engel olunmamalı"
concept_tags: [layout, responsive]
checklist_extra:
  - "min-height: 100vh veya 100dvh kullanılmış mı?"
  - "Sabit height yerine esnek min-height tercih edilmiş mi?"
reference_solution_path: private/solutions/css-veryeasy-min-height-footer-stick.css
hint_ladder:
  1: "Bir sayfanın en az ekran kadar yüksek olmasını sağlayan minimum yükseklik kuralı nedir?"
  2: "height yerine min-height kullanmanın içerik uzadığında sağladığı avantaj nedir?"
  3: "Bu sayfa düzeni kuralı 'minimum ekran yüksekliği (min-height 100vh)' olarak bilinir."
```

---

### css-veryeasy-table-border-collapse

```yaml
id: css-veryeasy-table-border-collapse
version: 1
language: css
engine: none
difficulty: very_easy
title: "Tablo hücre çizgilerini tek hatta birleştirme"
prompt: |
  HTML'de bir veri tablosunun hücrelerine (`<td>`, `<th>`) 1 piksel kenarlık verdiğinizde,
  tarayıcı her hücrenin kenarlığını ayrı çizer ve aralarında boşluk bırakarak çift çizgi
  oluşturur. Tablonun tüm hücre çizgilerinin birbirinin içine geçerek tek ve net bir ızgara
  çizgisine dönüşmesini sağlayan tablo kuralını yazın.
constraints:
  - "Hücre kenarlıkları tek bir ortak çizgide birleştirilmeli"
  - "Hücreler arasındaki varsayılan boşluklar yok edilmeli"
concept_tags: [layout, edge-cases]
checklist_extra:
  - "border-collapse özelliği collapse değeriyle atanmış mı?"
  - "Kural doğrudan table elemanına mı uygulanmış?"
reference_solution_path: private/solutions/css-veryeasy-table-border-collapse.css
hint_ladder:
  1: "Tablo kenarlıklarının çift çizgi yerine tek çizgi olarak birleşmesini sağlayan özellik nedir?"
  2: "Ayrı kenarlık modelini (separate) birleşik modele çeviren değer hangisidir?"
  3: "Bu tablo standardı 'tablo kenarlık birleştirme (border-collapse: collapse)' olarak bilinir."
```

---

## 2. Kolay (Easy) — 50 Soru

### css-easy-flexbox-horizontal-navigation

```yaml
id: css-easy-flexbox-horizontal-navigation
version: 1
language: css
engine: none
difficulty: easy
title: "Yatay navigasyon çubuğu ve logo-menü dengesi"
prompt: |
  Bir web sitesinin üst başlığında (header) solda şirket logosu, sağda ise menü bağlantıları
  yer almaktadır. Bu iki elemanı yatay bir eksende yan yana dizin; logoyu en sola, menü
  bağlantılarını en sağa itecek şekilde aralarındaki boşluğu eşit dağıtın ve her iki elemanı
  dikey eksende tam ortalayın.
constraints:
  - "Elemanlar yatay tek bir satırda hizalanmalı"
  - "Logo sola, menü sağa yaslanacak şekilde aradaki boşluk maksimize edilmeli"
  - "Dikey eksende merkezleme sağlanmalı"
concept_tags: [layout, centering]
checklist_extra:
  - "display: flex ile ana eksen ve çapraz eksen hizalaması kurulmuş mu?"
  - "justify-content özelliği space-between olarak belirlenmiş mi?"
reference_solution_path: private/solutions/css-easy-flexbox-horizontal-navigation.css
hint_ladder:
  1: "Çocuk elemanları yan yana dizip aralarındaki boşluğu en uca itmek için hangi mizanpaj modeli kullanılır?"
  2: "İlk elemanı başa, son elemanı sona iten yatay dağıtım değeri nedir?"
  3: "Bu navigasyon deseni 'esnek kutu başlık mizanpajı (flexbox space-between)' olarak bilinir."
```

---

### css-easy-flexbox-vertical-centering

```yaml
id: css-easy-flexbox-vertical-centering
version: 1
language: css
engine: none
difficulty: easy
title: "Kart içindeki içeriği hem yatayda hem dikeyde ortalama"
prompt: |
  Bir karşılama kartının veya boş durum (empty state) kutusunun 400 piksel yüksekliği
  bulunmaktadır. Kutu içindeki illüstrasyon, başlık ve aksiyon butonunu barındıran içerik
  grubunu kutunun hem tam yatay merkezine hem de tam dikey merkezine kusursuz şekilde yerleştirin.
constraints:
  - "İçerik her iki eksende (yatay ve dikey) tam ortalanmalı"
  - "Elemanlar dikey kolon akışında alt alta durmalı"
concept_tags: [centering, layout]
checklist_extra:
  - "justify-content ve align-items özellikleri birlikte center yapılmış mı?"
  - "İçeriğin alt alta kalması için flex-direction: column düşünülmüş mü?"
reference_solution_path: private/solutions/css-easy-flexbox-vertical-centering.css
hint_ladder:
  1: "Esnek kutuda hem ana ekseni hem çapraz ekseni merkeze almak için hangi iki özellik kullanılır?"
  2: "Dikey eksende dizilim için esnek kutu yönü ne olmalıdır?"
  3: "Bu mizanpaj kuralı 'çift eksenli esnek merkezleme (flexbox center alignment)' olarak bilinir."
```

---

### css-easy-flexbox-gap-spacing

```yaml
id: css-easy-flexbox-gap-spacing
version: 1
language: css
engine: none
difficulty: easy
title: "Esnek liste elemanları arasına eşit mesafe koyma"
prompt: |
  Bir filtre çubuğunda yan yana dizilmiş 5 adet filtre butonu bulunmaktadır. Geçmişte butonların
  sağına dış boşluk (margin-right) verilip en sondakinden bu boşluğu silmek için karmaşık seçiciler
  kullanılırdı. Modern esnek kutu aralık özelliğini kullanarak, butonların kendi aralarına
  16 piksel boşluk ekleyin; en baştaki ve en sondaki elemanların dış kenarlara yapışık kalmasını sağlayın.
constraints:
  - "Elemanların yalnızca birbirleri arasındaki mesafesi eşitlenmeli"
  - "Dış sınır kenarlıklarında istenmeyen taşma payı oluşmamalı"
concept_tags: [layout, maintainability]
checklist_extra:
  - "margin hileleri yerine doğrudan gap özelliği kullanılmış mı?"
  - "Değer 16px veya eşdeğeri rem olarak atanmış mı?"
reference_solution_path: private/solutions/css-easy-flexbox-gap-spacing.css
hint_ladder:
  1: "Esnek kutu veya ızgara elemanlarının sadece birbirleri arasındaki boşluğu yöneten özellik nedir?"
  2: "Son çocuktan margin silme zahmetini ortadan kaldıran modern özellik hangisidir?"
  3: "Bu mizanpaj boşluğu 'esnek aralık tanımlaması (flexbox gap)' olarak bilinir."
```

---

### css-easy-flexbox-wrap-tags

```yaml
id: css-easy-flexbox-wrap-tags
version: 1
language: css
engine: none
difficulty: easy
title: "Taşan etiket rozetlerini alt satıra kırma"
prompt: |
  Bir blog yazısının altında 15 adet konu etiketi rozeti yer almaktadır. Kapsayıcı kutu
  daraldığında veya mobilde açıldığında rozetlerin tek satıra sıkışıp kutunun dışına fırlamasını
  engellemek istiyorsunuz. Sığmayan etiketlerin doğal bir şekilde alt satıra geçmesini ve
  satırlar arasında da 8 piksel boşluk kalmasını sağlayın.
constraints:
  - "Elemanlar tek satıra zorlanmamalı, gerektiğinde alt satırlara akmalı"
  - "Satırlar ve sütunlar arasında düzenli mesafe korunmalı"
concept_tags: [layout, responsive]
checklist_extra:
  - "flex-wrap: wrap kuralı tanımlanmış mı?"
  - "Hem yatay hem dikey aralık için gap verilmiş mi?"
reference_solution_path: private/solutions/css-easy-flexbox-wrap-tags.css
hint_ladder:
  1: "Esnek kutudaki elemanların sığmadığında alt satıra geçmesine izin veren özellik nedir?"
  2: "nowrap varsayılanını çok satırlı akışa çeviren değer hangisidir?"
  3: "Bu satır sarma kuralı 'esnek çok satırlı akış (flex-wrap: wrap)' olarak bilinir."
```

---

### css-easy-flexbox-grow-shrink-input

```yaml
id: css-easy-flexbox-grow-shrink-input
version: 1
language: css
engine: none
difficulty: easy
title: "Kalan boşluğu dolduran arama çubuğu ve sabit buton"
prompt: |
  Bir arama formunda solda bir metin kutusu, sağda ise 'Ara' butonu yan yana durmaktadır.
  Butonun genişliği içindeki metin kadar sabit kalmalı; metin girdi kutusu ise satırdaki
  kullanılabilir tüm boşluğu dinamik olarak doldurmalıdır. Esnek büyüme özelliğini kullanarak
  bu arama çubuğu dengesini kurun.
constraints:
  - "Girdi kutusu satırdaki tüm serbest alanı kaplayacak şekilde esnemeli"
  - "Buton kendi doğal genişliğini korumalı, ezilmemeli"
concept_tags: [layout, focus]
checklist_extra:
  - "Girdi kutusuna flex-grow: 1 veya flex: 1 atanmış mı?"
  - "Butonun ezilmesini önlemek için flex-shrink: 0 düşünülmüş mü?"
reference_solution_path: private/solutions/css-easy-flexbox-grow-shrink-input.css
hint_ladder:
  1: "Esnek bir elemanın satırdaki kalan tüm boş alanı kaplamasını sağlayan özellik nedir?"
  2: "flex-grow özelliğine hangi değer verildiğinde eleman serbest alanı emer?"
  3: "Bu esnek büyüme kuralı 'esnek alan doldurma (flex-grow: 1)' olarak bilinir."
```

---

### css-easy-flexbox-column-card-layout

```yaml
id: css-easy-flexbox-column-card-layout
version: 1
language: css
engine: none
difficulty: easy
title: "Kart altbilgisini en alta sabitleyen dikey esnek düzen"
prompt: |
  Bir ürün kartında görsel, ürün adı, değişken uzunlukta bir açıklama metni ve en altta
  'Satın Al' butonu bulunmaktadır. Açıklama metni kısa da olsa uzun da olsa, tüm kartların
  altındaki 'Satın Al' butonunun kartın en dibine yapışık ve aynı hizada durmasını istiyorsunuz.
  Dikey esnek kutu yönünü ve açıklama metninin kalan dikey alanı doldurmasını sağlayacak kuralı kurun.
constraints:
  - "Kart elemanı dikey esnek akışa sahip olmalı"
  - "Açıklama alanı veya buton esnekliği ile buton kartın dibine itilmeli"
concept_tags: [layout, positioning]
checklist_extra:
  - "flex-direction: column kullanılmış mı?"
  - "Açıklama metnine flex-grow: 1 veya butona margin-top: auto verilmiş mi?"
reference_solution_path: private/solutions/css-easy-flexbox-column-card-layout.css
hint_ladder:
  1: "Esnek kutuyu dikey olarak çalıştırmak için flex-direction ne olmalıdır?"
  2: "Dikey esnek kutuda bir elemanı en dibe itmek için margin-top: auto veya flex-grow nasıl kullanılır?"
  3: "Bu dikey mizanpaj deseni 'dikey esnek kart ve yapışık altbilgi (flex column sticky footer)' olarak bilinir."
```

---

### css-easy-grid-three-column-cards

```yaml
id: css-easy-grid-three-column-cards
version: 1
language: css
engine: none
difficulty: easy
title: "Üç eşit sütunlu modern kart ızgarası"
prompt: |
  Bir portföy vitrininde sergilenen projeleri yan yana 3 eşit sütun halinde dizmek istiyorsunuz.
  Geleneksel yüzdeli genişlik hesaplamaları yerine, modern CSS Grid şablon sütunlarını ve
  kesirli birim (fr) sistemini kullanarak aralarında 24 piksel boşluk olan 3 sütunlu ızgarayı kurun.
constraints:
  - "Kapsayıcı CSS Grid mizanpajı kullanmalı"
  - "Tam olarak 3 eşit genişlikte sütun tanımlanmalı"
  - "Sütunlar ve satırlar arasında 24 piksel boşluk bırakılmalı"
concept_tags: [layout, responsive]
checklist_extra:
  - "grid-template-columns: repeat(3, 1fr) veya 1fr 1fr 1fr kullanılmış mı?"
  - "Boşluklar için gap özelliği atanmış mı?"
reference_solution_path: private/solutions/css-easy-grid-three-column-cards.css
hint_ladder:
  1: "CSS Grid'de sütun sayısını ve genişliğini belirleyen ana özellik nedir?"
  2: "Eşit paylaşımlı sütunlar üretmek için kullanılan kesirli esnek birim hangisidir?"
  3: "Bu ızgara yapısı 'üç sütunlu grid şablonu (grid-template-columns 3fr)' olarak bilinir."
```

---

### css-easy-grid-auto-fit-minmax

```yaml
id: css-easy-grid-auto-fit-minmax
version: 1
language: css
engine: none
difficulty: easy
title: "Medyasorgusuz kendiliğinden duyarlı kart ızgarası"
prompt: |
  Hiç `@media` sorgusu yazmadan, ekran genişliğine göre kendiliğinden sütun sayısını ayarlayan
  akıllı bir ürün ızgarası tasarlayın. Kartların genişliği en az 280 piksel olmalı, ekranda
  yer kaldıkça satırı eşit dolduracak şekilde genişlemeli, yer kalmadığında ise otomatik olarak
  alt satıra geçmelidir.
constraints:
  - "Medya sorgusu kullanılmadan duyarlı sütun kırılımı sağlanmalı"
  - "Kartların asgari boyutu 280px, azami boyutu 1fr olmalı"
  - "Kapsayıcıyı otomatik dolduran auto-fit veya auto-fill yapısı kullanılmalı"
concept_tags: [layout, responsive]
checklist_extra:
  - "repeat(auto-fit, minmax(280px, 1fr)) formülü kurulmuş mı?"
  - "grid-template-columns üzerinde minmax fonksiyonu kullanılmış mı?"
reference_solution_path: private/solutions/css-easy-grid-auto-fit-minmax.css
hint_ladder:
  1: "CSS Grid'de sütunların ekrana göre otomatik sığmasını sağlayan repeat anahtar kelimesi nedir?"
  2: "Minimum ve maksimum sınırları birleştiren CSS matematik fonksiyonu hangisidir?"
  3: "Bu popüler duyarlı desen 'otomatik sığan minmax ızgarası (grid auto-fit minmax)' olarak bilinir."
```

---

### css-easy-grid-gap-matrix

```yaml
id: css-easy-grid-gap-matrix
version: 1
language: css
engine: none
difficulty: easy
title: "Satır ve sütun aralıklarını bağımsız boyutlandırma"
prompt: |
  Bir kontrol paneli arayüzünde kartlar bir ızgara düzeninde yerleşmektedir. Tasarım kurallarına
  göre sütunlar arasındaki yatay mesafenin ferah (32 piksel), satırlar arasındaki dikey
  mesafenin ise daha derli toplu (16 piksel) olması istenmektedir. İki yönlü aralık değerini
  tek bir birleşik kuralda tanımlayın.
constraints:
  - "Satır boşluğu 16px, sütun boşluğu 32px olarak ayarlanmalı"
  - "Aralıklar ızgara kapsayıcısına tanımlanmalı"
concept_tags: [layout, maintainability]
checklist_extra:
  - "gap özelliğine sırasıyla satır ve sütun değerleri (16px 32px) verilmiş mi?"
  - "row-gap ve column-gap ayrımı doğru anlaşılmış mı?"
reference_solution_path: private/solutions/css-easy-grid-gap-matrix.css
hint_ladder:
  1: "gap özelliğine iki farklı değer yazıldığında ilk değer neyi, ikinci değer neyi ifade eder?"
  2: "Satır ve sütun aralığını tek satırda nasıl ayırırız?"
  3: "Bu boşluk kuralı 'iki eksenli ızgara boşluğu (row-gap ve column-gap)' olarak bilinir."
```

---

### css-easy-position-relative-absolute-badge

```yaml
id: css-easy-position-relative-absolute-badge
version: 1
language: css
engine: none
difficulty: easy
title: "Kullanıcı profil fotoğrafının köşesine bildirim rozeti sabitleme"
prompt: |
  Dairesel bir kullanıcı profil fotoğrafının sağ üst köşesine kırmızı bir okunmamış bildirim
  sayacı rozeti (`<span>`) yerleştirmek istiyorsunuz. Profil fotoğrafı sayfada nereye kayarsa
  kaysın rozetin onun sağ üst köşesine kenetlenmiş kalmasını sağlayan ebeveyn-çocuk konumlandırma
  ilişkisini kurun.
constraints:
  - "Ebeveyn avatar kutusu konumlandırma referans noktası haline getirilmeli"
  - "Bildirim rozeti ebeveyne göre mutlak olarak sağ üste yerleştirilmeli"
concept_tags: [positioning, layout]
checklist_extra:
  - "Ebeveyne position: relative atanmış mı?"
  - "Rozete position: absolute ile top ve right koordinatları verilmiş mi?"
reference_solution_path: private/solutions/css-easy-position-relative-absolute-badge.css
hint_ladder:
  1: "Bir çocuğun mutlak (absolute) konumlanabilmesi için ebeveyninin hangi konuma sahip olması gerekir?"
  2: "Rozeti sağ üst köşeye oturtmak için hangi koordinat özellikleri sıfırlanır?"
  3: "Bu klasik konumlandırma ikilisi 'göreli ebeveyn ve mutlak çocuk (relative-absolute positioning)' olarak bilinir."
```

---

### css-easy-position-sticky-subnav

```yaml
id: css-easy-position-sticky-subnav
version: 1
language: css
engine: none
difficulty: easy
title: "Kaydırma sırasında ekranın tepesine yapışan alt menü"
prompt: |
  Bir dokümantasyon sayfasında ana başlığın altında bir konu fihristi alt menüsü bulunmaktadır.
  Sayfa aşağı kaydırılırken bu menü başlangıçta normal akışında yukarı doğru hareket etmeli,
  ancak ekranın tam tepesine (0 piksel) ulaştığında orada sabitlenip içerik altından akmaya
  devam etmelidir.
constraints:
  - "Eleman kaydırma eşiğine ulaştığında tepeye yapışmalı"
  - "Eşik noktası olarak tepe mesafesi (top) sıfır tanımlanmalı"
concept_tags: [positioning, layout]
checklist_extra:
  - "position: sticky kuralı kullanılmış mı?"
  - "Yapışma eşiği için top: 0 koordinatı verilmiş mi?"
reference_solution_path: private/solutions/css-easy-position-sticky-subnav.css
hint_ladder:
  1: "Hem normal akışta durup hem de kaydırma sınırında sabitlenen konum türü nedir?"
  2: "Yapışkan konumlandırmanın çalışması için hangi koordinat eşiğinin tanımlanması şarttır?"
  3: "Bu gezinme davranışı 'yapışkan konumlandırma (position: sticky)' olarak bilinir."
```

---

### css-easy-position-fixed-floating-action

```yaml
id: css-easy-position-fixed-floating-action
version: 1
language: css
engine: none
difficulty: easy
title: "Ekranın sağ altına kenetlenen yüzen destek butonu"
prompt: |
  Kullanıcı sayfanın neresinde olursa olsun (ister en üstte, ister en altta), ekran penceresinin
  sağ alt köşesinde her zaman sabit duran bir 'Canlı Destek' yüzen eylem butonu tasarlayın.
  Buton sayfa kaydırmasından etkilenmemeli, sağdan 24px ve alttan 24px mesafede asılı kalmalıdır.
constraints:
  - "Eleman görünür pencereye (viewport) göre sabitlenmeli"
  - "Sayfa kaydırıldığında ekrandaki yerini terk etmemeli"
  - "Sağ ve alt mesafeler 24 piksel olarak tanımlanmalı"
concept_tags: [positioning, layout]
checklist_extra:
  - "position: fixed kuralı kullanılmış mı?"
  - "bottom ve right koordinatları doğru atanmış mı?"
reference_solution_path: private/solutions/css-easy-position-fixed-floating-action.css
hint_ladder:
  1: "Doğrudan tarayıcı ekranına kenetlenen ve kaydırmayla hareket etmeyen konum türü hangisidir?"
  2: "Sağ alt köşeye mesafe koymak için hangi iki koordinat özelliği kullanılır?"
  3: "Bu yüzen buton kuralı 'sabit konumlandırma (position: fixed)' olarak bilinir."
```

---

### css-easy-css-variables-color-theme

```yaml
id: css-easy-css-variables-color-theme
version: 1
language: css
engine: none
difficulty: easy
title: "CSS değişkenleri ile yeniden kullanılabilir renk paleti"
prompt: |
  Bir web projesinde ana marka rengini (`#2563eb`) ve vurgu rengini (`#f59e0b`) onlarca
  farklı yerde elle yazmak yerine, sayfanın en üst kök elemanında iki adet özel CSS değişkeni
  olarak tanımlayın. Ardından bir butona bu değişkenleri tüketerek arka plan ve kenarlık rengi verin.
constraints:
  - "Değişkenler kök seçici (`:root`) altında tanımlanmalı"
  - "Değişken adları standart çift tire (`--`) ile başlamalı"
  - "Buton stilinde değişkenler `var()` fonksiyonuyla tüketilmeli"
concept_tags: [variables, color]
checklist_extra:
  - "--ana-renk gibi çift tireli özel özellikler oluşturulmuş mu?"
  - "Tüketim yerinde var(--degisken-adi) sözdizimi kullanılmış mı?"
reference_solution_path: private/solutions/css-easy-css-variables-color-theme.css
hint_ladder:
  1: "CSS'te özel değişken tanımlarken isimler hangi iki karakterle başlar?"
  2: "Tanımlanan değişkeni bir özellik değerinde kullanmak için hangi fonksiyon çağrılır?"
  3: "Bu modüler stil standardı 'CSS özel değişkenleri (custom properties var)' olarak bilinir."
```

---

### css-easy-css-variables-spacing-scale

```yaml
id: css-easy-css-variables-spacing-scale
version: 1
language: css
engine: none
difficulty: easy
title: "Değişken tabanlı tutarlı boşluk cetveli"
prompt: |
  Tasarım sisteminde tutarlılık sağlamak amacıyla küçük (`--space-sm: 8px`), orta (`--space-md: 16px`)
  ve büyük (`--space-lg: 24px`) boşluk ölçeklerini kök değişkenler olarak belirleyin. Bir kart
  bileşeninin iç boşluğunda büyük ölçeği, kartın altındaki paragraflar arası mesafede ise
  küçük ölçeği değişken fonksiyonlarıyla uygulayın.
constraints:
  - "Kök seviyesinde en az üç kademeli boşluk değişkeni tanımlanmalı"
  - "Bileşenler doğrudan piksel yazmak yerine bu değişkenleri tüketmeli"
concept_tags: [variables, maintainability]
checklist_extra:
  - "Değişkenler :root bloğunda mı tanımlanmış?"
  - "Kart ve paragraf stillerinde var() çağrıları doğru bağlanmış mı?"
reference_solution_path: private/solutions/css-easy-css-variables-spacing-scale.css
hint_ladder:
  1: "Proje genelinde ortak boşluk standartları oluşturmak için değişkenler nereye yazılır?"
  2: "Padding ve margin değerlerinde değişkenleri nasıl çağırırız?"
  3: "Bu tasarım sistemi kuralı 'CSS boşluk cetveli değişkenleri (spacing scale variables)' olarak bilinir."
```

---

### css-easy-transition-button-smooth

```yaml
id: css-easy-transition-button-smooth
version: 1
language: css
engine: none
difficulty: easy
title: "Buton durumlarında yumuşak geçiş animasyonu"
prompt: |
  Bir butona fareyle gelindiğinde (`:hover`) arka plan rengi değişmektedir. Ancak bu renk
  değişimi bir anda küt diye gerçekleştiği için sert ve kalitesiz görünmektedir. Arka plan
  rengi değişiminin 250 milisaniye içinde yumuşak ve akıcı bir şekilde gerçekleşmesini
  sağlayan geçiş kuralını tanımlayın.
constraints:
  - "Yalnızca değişen özellik (background-color) hedeflenmeli"
  - "Süre 200-300ms arasında belirlenmeli"
  - "Geçiş kuralı :hover içine değil ana buton stiline tanımlanmalı"
concept_tags: [animation, maintainability]
checklist_extra:
  - "transition: background-color 250ms ease kuralı ana seçiciye mi yazılmış?"
  - "Tüm özellikleri gereksiz yere geçişe sokan transition: all'dan kaçınılmış mı?"
reference_solution_path: private/solutions/css-easy-transition-button-smooth.css
hint_ladder:
  1: "Stil değişimlerinin zamana yayılarak yumuşak olmasını sağlayan özellik nedir?"
  2: "Farenin hem gelişte hem çıkışta akıcı çalışması için transition nereye yazılmalıdır?"
  3: "Bu etkileşim kuralı 'durum geçiş animasyonu (CSS transition)' olarak bilinir."
```

---

### css-easy-transform-card-hover-lift

```yaml
id: css-easy-transform-card-hover-lift
version: 1
language: css
engine: none
difficulty: easy
title: "Kart üzerine gelindiğinde yukarı doğru süzülme efekti"
prompt: |
  Kullanıcı bir ürün kartının üzerine fareyle geldiğinde, kartın sayfadan hafifçe 6 piksel
  yukarı doğru süzülmesini ve altındaki gölgenin derinleşmesini istiyorsunuz. Kartın etrafındaki
  diğer elemanların mizanpajını bozmadan ve performans kaybı yaratmadan bu yukarı yükselme
  hareketini sağlayan dönüşüm fonksiyonunu yazın.
constraints:
  - "Yükselme hareketi GPU dostu dönüşüm (transform) özelliğiyle yapılmalı"
  - "Yukarı doğru hareket için negatif dikey kayma uygulanmalı"
  - "Geçiş yumuşak bir transition ile desteklenmeli"
concept_tags: [animation, performance]
checklist_extra:
  - "top veya margin-top yerine transform: translateY(-6px) kullanılmış mı?"
  - "Kutu düzenini bozmayan donanım hızlandırmalı transform tercih edilmiş mi?"
reference_solution_path: private/solutions/css-easy-transform-card-hover-lift.css
hint_ladder:
  1: "Bir elemanı mizanpajı etkilemeden dikeyde kaydırmak için hangi CSS fonksiyonu kullanılır?"
  2: "Yukarı doğru hareket ettirmek için Y ekseninde pozitif mi negatif mi değer verilir?"
  3: "Bu mikro etkileşim 'kart yükselme efekti (transform translateY)' olarak bilinir."
```

---

### css-easy-transform-icon-rotate

```yaml
id: css-easy-transform-icon-rotate
version: 1
language: css
engine: none
difficulty: easy
title: "Açılır menü ok simgesini 180 derece döndürme"
prompt: |
  Bir akordeon veya açılır menü başlığının yanında aşağı bakan küçük bir ok simgesi vardır.
  Menü açıldığında (örneğin `.is-open` sınıfı eklendiğinde), bu ok simgesinin kendi merkezi
  etrafında pürüzsüzce dönerek yukarı bakmasını (180 derece dönüş) sağlayan dönüşüm kuralını yazın.
constraints:
  - "Açık durumda eleman 180 derece döndürülmeli"
  - "Dönüş hareketi akıcı bir süreyle gerçekleşmeli"
concept_tags: [animation, maintainability]
checklist_extra:
  - "transform: rotate(180deg) kuralı kullanılmış mı?"
  - "Geçişin görünmesi için transition tanımlanmış mı?"
reference_solution_path: private/solutions/css-easy-transform-icon-rotate.css
hint_ladder:
  1: "Bir elemanı açıyla döndüren CSS dönüşüm fonksiyonu hangisidir?"
  2: "Yarım tur tersine çevirmek için derece birimiyle ne yazılır?"
  3: "Bu gösterge animasyonu 'açısal simge döndürme (transform rotate)' olarak bilinir."
```

---

### css-easy-media-query-mobile-stack

```yaml
id: css-easy-media-query-mobile-stack
version: 1
language: css
engine: none
difficulty: easy
title: "Mobil ekranlarda iki sütunu alt alta düşürme"
prompt: |
  Masaüstü bilgisayarlarda yan yana duran iki sütunlu form veya kart düzeni, 768 pikselden
  daha dar tablet ve cep telefonu ekranlarında sıkışmaktadır. Ekran genişliği 768 pikselin
  altına indiğinde bu iki sütunu tam genişlikli olarak alt alta dizen standart medya sorgusu
  kuralını yazın.
constraints:
  - "768px kırılma noktası için medya sorgusu tanımlanmalı"
  - "Sütunlar dar ekranda yüzde 100 genişliğe çıkarak alt alta yerleşmeli"
concept_tags: [responsive, layout]
checklist_extra:
  - "@media (max-width: 767px) veya uygun bir eşik kullanılmış mı?"
  - "Mizanpaj yönü sütuna çevrilmiş mi?"
reference_solution_path: private/solutions/css-easy-media-query-mobile-stack.css
hint_ladder:
  1: "Ekran genişliğine göre farklı stiller çalıştırmayı sağlayan CSS kuralı nedir?"
  2: "768 pikselden küçük ekranları hedeflemek için hangi koşul parantezi yazılır?"
  3: "Bu duyarlı tasarım kuralı 'mobil kırılma noktası medya sorgusu (media query max-width)' olarak bilinir."
```

---

### css-easy-media-query-dark-mode

```yaml
id: css-easy-media-query-dark-mode
version: 1
language: css
engine: none
difficulty: easy
title: "İşletim sistemi karanlık mod tercihine uyum sağlama"
prompt: |
  Kullanıcının işletim sisteminde veya tarayıcısında 'Karanlık Mod' (Dark Mode) aktif olduğunda,
  web sitenizin otomatik olarak koyu bir arka plana ve açık bir yazı rengine bürünmesini
  sağlayın. Kullanıcının sistem renk tercihini dinleyen standart medya özelliğini kullanarak
  karanlık tema stillerini tanımlayın.
constraints:
  - "Kullanıcının sistem renk teması tercihi dinlenmeli"
  - "Koyu zemin ve açık metin renkleri tanımlanmalı"
concept_tags: [responsive, color]
checklist_extra:
  - "@media (prefers-color-scheme: dark) medya özelliği kullanılmış mı?"
  - "Kontrast koyu modda da okunabilir kalmış mı?"
reference_solution_path: private/solutions/css-easy-media-query-dark-mode.css
hint_ladder:
  1: "Kullanıcının cihazında karanlık temayı seçip seçmediğini kontrol eden medya sorgusu nedir?"
  2: "prefers-color-scheme özelliği hangi iki temel değeri alabilir?"
  3: "Bu modern erişilebilirlik özelliği 'karanlık mod medya tercihi (prefers-color-scheme: dark)' olarak bilinir."
```

---

### css-easy-accessible-visually-hidden

```yaml
id: css-easy-accessible-visually-hidden
version: 1
language: css
engine: none
difficulty: easy
title: "Görsel olarak gizli fakat ekran okuyucuya açık yardımcı sınıf"
prompt: |
  Bir simge butonunun ('Sepete Ekle') yanında sadece büyüteç veya sepet ikonu görünmektedir.
  Görme engelli ekran okuyucu kullanıcılarının bu butonu duyabilmesi için HTML'e bir `<span>`
  eklediniz. Ancak bu metnin ekranda görünmemesi, `display: none` yazıldığında ekran
  okuyuculardan da silinmemesi gerekmektedir. Metni görsel olarak 1 piksele kırparak gizleyen
  fakat erişilebilir bırakan evrensel yardımcı sınıfı (`.sr-only`) yazın.
constraints:
  - "Metin ekrandan tamamen gizlenmeli fakat ekran okuyucular tarafından okunabilmeli"
  - "`display: none` veya `visibility: hidden` kesinlikle kullanılmamalı"
  - "Kırpma (clip / clip-path) ve mutlak konumlandırma tekniği uygulanmalı"
concept_tags: [accessibility, maintainability]
checklist_extra:
  - "width: 1px, height: 1px ve clip: rect(0, 0, 0, 0) veya clip-path kullanılmış mı?"
  - "Ekran okuyucu akışını korumak için overflow: hidden eklenmiş mi?"
reference_solution_path: private/solutions/css-easy-accessible-visually-hidden.css
hint_ladder:
  1: "display: none kullanırsak ekran okuyucular metni okuyabilir mi?"
  2: "Metni 1 piksele indirip mutlak konumla ekran dışına taşımadan kırpma tekniği nedir?"
  3: "Bu kritik erişilebilirlik sınıfı 'görsel olarak gizleme sınıfı (sr-only / visually-hidden)' olarak bilinir."
```

---

### css-easy-image-object-fit-cover

```yaml
id: css-easy-image-object-fit-cover
version: 1
language: css
engine: none
difficulty: easy
title: "Sabit boyutlu kartta görselin ezilmesini önleme"
prompt: |
  Bir haber portalının kartlarında görsellere 100% genişlik ve 200 piksel sabit yükseklik
  verilmiştir. Farklı en-boy oranlarına sahip fotoğraflar bu kutuya girdiğinde basıklaşmakta,
  uzamakta ve insanların yüzleri orantısız şekilde ezilmektedir. Görselin doğal oranını koruyarak
  kutuyu tamamen doldurmasını ve gerekirse taşan kısımların kırpılmasını sağlayan kuralı tanımlayın.
constraints:
  - "Görselin en-boy oranı bozulmamalı ve basıklaşma engellenmeli"
  - "Görsel kutunun tamamını boşluk bırakmadan doldurmalı"
concept_tags: [layout, responsive]
checklist_extra:
  - "object-fit: cover özelliği atanmış mı?"
  - "Görselin odak merkezini korumak için object-position düşünüldü mü?"
reference_solution_path: private/solutions/css-easy-image-object-fit-cover.css
hint_ladder:
  1: "Görsellerin ve videoların sabit bir çerçeveye sığarken ezilmesini önleyen özellik nedir?"
  2: "Kutuyu tamamen kaplayıp taşan kısımları kırpan değer hangisidir?"
  3: "Bu medya kuralı 'nesne sığdırma orantısı (object-fit: cover)' olarak bilinir."
```

---

### css-easy-aspect-ratio-video-box

```yaml
id: css-easy-aspect-ratio-video-box
version: 1
language: css
engine: none
difficulty: easy
title: "Modern oran özelliğiyle 16'ya 9 video kutusu"
prompt: |
  Bir eğitim sayfasındaki video oynatıcı kutusunun genişliği mobilde ve masaüstünde esnek
  şekilde değişmektedir. Geçmişte `padding-top: 56.25%` hilesiyle yapılan geniş ekran (16:9)
  oranını, modern CSS yerel en-boy oranı özelliğini kullanarak tek satırda tanımlayın;
  video yüklenmeden önce düzen kaymasını (CLS) tamamen önleyin.
constraints:
  - "Kutu genişliği değiştikçe 16:9 oranını otomatik korumalı"
  - "Eski padding hilesi yerine modern CSS özelliği kullanılmalı"
concept_tags: [responsive, performance]
checklist_extra:
  - "aspect-ratio: 16 / 9 özelliği tanımlanmış mı?"
  - "Genişlik esnerken yükseklik bu orana göre otomatik hesaplanıyor mu?"
reference_solution_path: private/solutions/css-easy-aspect-ratio-video-box.css
hint_ladder:
  1: "Bir elemanın genişlik ve yükseklik oranını doğrudan sabitleyen modern CSS özelliği nedir?"
  2: "16'ya 9 standart video oranı bu özelliğe nasıl yazılır?"
  3: "Bu performans özelliği 'en-boy oranı sabitlemesi (aspect-ratio: 16 / 9)' olarak bilinir."
```

---

### css-easy-overflow-x-auto-scroll

```yaml
id: css-easy-overflow-x-auto-scroll
version: 1
language: css
engine: none
difficulty: easy
title: "Mobil uyumlu yatay kaydırmalı kart şeridi"
prompt: |
  Mobil ekranda ürün kartlarının alt alta dizilip sayfayı sonsuz uzatması yerine, kullanıcının
  parmağıyla sağa-sola kaydırabileceği yatay bir kart şeridi (carousel) tasarlayın. Kartların
  tek satırda yan yana durmasını sağlayın; kapsayıcı kutuya yalnızca yatayda kaydırma çubuğu
  ekleyin ve dikey taşmaları engelleyin.
constraints:
  - "Yalnızca yatay eksende kaydırma etkinleştirilmeli"
  - "Elemanlar alt satıra kırılmadan yatay hatta kalmalı"
concept_tags: [layout, responsive]
checklist_extra:
  - "overflow-x: auto veya scroll atanmış mı?"
  - "Dikey kaydırmayı engellemek için overflow-y: hidden düşünülmüş mü?"
reference_solution_path: private/solutions/css-easy-overflow-x-auto-scroll.css
hint_ladder:
  1: "Yalnızca yatay eksendeki taşmaları kaydırılabilir yapan özellik nedir?"
  2: "İçeriğin tek satırda kalması için esnek kutuda wrap özelliği nasıl olmalıdır?"
  3: "Bu kaydırma şeridi 'yatay kaydırılabilir kapsayıcı (overflow-x auto scroll)' olarak bilinir."
```

---

### css-easy-custom-checkbox-appearance

```yaml
id: css-easy-custom-checkbox-appearance
version: 1
language: css
engine: none
difficulty: easy
title: "Tarayıcı varsayılan onay kutusunu sıfırlayıp özelleştirme"
prompt: |
  HTML'in yerleşik `<input type="checkbox">` elemanının modası geçmiş işletim sistemi görünümünü
  kaldırıp, kendi özel marka renklerinize uygun 20x20 piksel boyutunda, yuvarlak köşeli modern
  bir onay kutusu tasarlamak istiyorsunuz. Tarayıcının yerel görsel çizimini tamamen kapatan
  ve kutuyu CSS ile biçimlendirilebilir kılan modern özelliği yazın.
constraints:
  - "İşletim sisteminin varsayılan form denetimi görünümü kapatılmalı"
  - "Eleman standart kutu modeli özellikleri (genişlik, yükseklik, kenarlık) ile çizilmeli"
concept_tags: [maintainability, accessibility]
checklist_extra:
  - "appearance: none kuralı uygulanmış mı?"
  - "Klavye erişilebilirliği ve :checked durumu korunmuş mu?"
reference_solution_path: private/solutions/css-easy-custom-checkbox-appearance.css
hint_ladder:
  1: "Tarayıcıların yerel buton ve girdi çizimlerini kapatan CSS özelliği nedir?"
  2: "Bu özelliğe none değeri verildiğinde onay kutusuna ne olur?"
  3: "Bu form stili sıfırlaması 'yerel görünümü kapatma (appearance: none)' olarak bilinir."
```

---

### css-easy-custom-radio-circle

```yaml
id: css-easy-custom-radio-circle
version: 1
language: css
engine: none
difficulty: easy
title: "Özel tasarımlı dairesel radyo butonu seçilme durumu"
prompt: |
  Bir abonelik paket seçimi formunda özel radyo butonları tasarlıyorsunuz. Radyo butonu
  seçildiğinde (`:checked`), dış halkanın kurumsal renge bürünmesini ve halkanın tam ortasında
  küçük dolu bir iç dairenin belirmesini istiyorsunuz. Radyo butonunun seçilme anını yakalayan
  sözde sınıfı kullanarak bu iç çekirdek görselini oluşturun.
constraints:
  - "Seçilme durumu `:checked` sözde sınıfı ile yakalanmalı"
  - "Seçili durumda iç çekirdek vurgusu oluşturulmalı"
concept_tags: [focus, accessibility]
checklist_extra:
  - ":checked sözde sınıfı doğru hedeflenmiş mi?"
  - "Görsel daire merkezlemesi düzgün yapılmış mı?"
reference_solution_path: private/solutions/css-easy-custom-radio-circle.css
hint_ladder:
  1: "Bir radyo butonu veya onay kutusu seçildiğinde aktifleşen sözde sınıf nedir?"
  2: "Seçili durumu gösteren stil hangi sözde sınıf üzerinden yazılır?"
  3: "Bu form etkileşimi 'seçili girdi durumu (:checked pseudo-class)' olarak bilinir."
```

---

### css-easy-focus-within-form-card

```yaml
id: css-easy-focus-within-form-card
version: 1
language: css
engine: none
difficulty: easy
title: "İçindeki girdi odaklandığında tüm form kartını vurgulama"
prompt: |
  Bir giriş formunda kullanıcı herhangi bir metin kutusuna (`<input>`) tıkladığında veya
  klavye ile odaklandığında, o girdiyi barındıran tüm ebeveyn kart çerçevesinin mavi bir
  parlama ve gölge kazanmasını istiyorsunuz. Bir elemanın herhangi bir çocuğu odak aldığında
  ebeveyne stil uygulayan güçlü sözde sınıfı yazın.
constraints:
  - "Ebeveyn kapsayıcı, içindeki herhangi bir eleman odaklandığında stillendirilmeli"
  - "Kullanıcı girdiden çıktığında vurgu otomatik kaybolmalı"
concept_tags: [focus, accessibility]
checklist_extra:
  - ":focus-within sözde sınıfı ebeveyne tanımlanmış mı?"
  - "Klavye ve fare odağında tutarlı çalışıyor mu?"
reference_solution_path: private/solutions/css-easy-focus-within-form-card.css
hint_ladder:
  1: "Bir kapsayıcının çocuklarından biri odaklandığında ebeveyne stil veren sözde sınıf nedir?"
  2: "Form kartının kendisini ışıldatmak için karta hangi sözde sınıf eklenir?"
  3: "Bu kapsayıcı odak kuralı 'iç odak durumu (:focus-within)' olarak bilinir."
```

---

### css-easy-has-pseudo-class-highlight

```yaml
id: css-easy-has-pseudo-class-highlight
version: 1
language: css
engine: none
difficulty: easy
title: "Seçili onay kutusu içeren kartın arka planını değiştirme"
prompt: |
  Bir fiyatlandırma tablosunda kullanıcının seçebileceği seçenek kartları vardır. Kartın içindeki
  onay kutusu işaretlendiğinde (`input:checked`), o kartın arka planının açık maviye dönmesini
  ve kenarlığının kalınlaşmasını istiyorsunuz. Hiçbir JavaScript kodu yazmadan, çocuk elemanın
  durumuna göre ebeveyn kartı seçen modern CSS ebeveyn seçicisini kullanın.
constraints:
  - "Çocuk elemanın durumuna göre ebeveyn kart stillendirilmeli"
  - "İşaretleme kalktığında ebeveyn eski stiline dönmeli"
concept_tags: [specificity, maintainability]
checklist_extra:
  - ":has(input:checked) sözdizimi kullanılmış mı?"
  - "Modern ebeveyn seçici doğru bağlanmış mı?"
reference_solution_path: private/solutions/css-easy-has-pseudo-class-highlight.css
hint_ladder:
  1: "CSS'te belirli bir çocuğu içeren ebeveyni seçmeyi sağlayan modern sözde sınıf hangisidir?"
  2: "İçinde seçili girdi olan kartı hedeflemek için :has() parantezine ne yazılır?"
  3: "Bu devrimsel seçici 'CSS ilişkisel ebeveyn seçicisi (:has pseudo-class)' olarak bilinir."
```

---

### css-easy-is-pseudo-class-grouping

```yaml
id: css-easy-is-pseudo-class-grouping
version: 1
language: css
engine: none
difficulty: easy
title: "Başlık seçicilerini tek satırda sadeleştirme"
prompt: |
  Bir makale, bir yan sütun ve bir altbilgi içindeki tüm `h1`, `h2` ve `h3` başlıklarının
  renklerini tek bir kuralla güncellemek istiyorsunuz. Dokuz satırlık upuzun ve tekrarlı
  seçici zincirleri yazmak yerine, modern gruplama sözde sınıfını kullanarak seçici kodunu
  kısa, okunabilir ve bakımı kolay hale getirin.
constraints:
  - "Tekrarlayan seçiciler modern gruplama sözde sınıfı ile birleştirilmeli"
  - "Kuralın okunabilirliği artırılmalı ve kod tekrarı önlenmeli"
concept_tags: [specificity, maintainability]
checklist_extra:
  - ":is(h1, h2, h3) gruplaması kullanılmış mı?"
  - "Seçici kodu sadeleştirilmiş mi?"
reference_solution_path: private/solutions/css-easy-is-pseudo-class-grouping.css
hint_ladder:
  1: "Birden çok seçiciyi parantez içinde virgülle birleştiren modern sözde sınıf nedir?"
  2: "article :is(h1, h2, h3) sözdizimi ne anlama gelir?"
  3: "Bu seçici sadeleştirmesi 'seçici eşleştirme grubu (:is pseudo-class)' olarak bilinir."
```

---

### css-easy-where-pseudo-class-zero-specificity

```yaml
id: css-easy-where-pseudo-class-zero-specificity
version: 1
language: css
engine: none
difficulty: easy
title: "Sıfır özgüllükle varsayılan sıfırlama stilleri yazma"
prompt: |
  Bir tasarım sistemi veya CSS sıfırlama (reset) katmanı hazırlıyorsunuz. Tüm butonlara ve
  girdilere temel stiller tanımlamak, ancak ileride geliştiricilerin bu stilleri ezmek istediğinde
  özgüllük (specificity) savaşına girmemesini istiyorsunuz. Tanımladığı kurallara tam olarak
  0 (sıfır) özgüllük puanı veren modern sözde sınıfı kullanarak varsayılan stilleri tanımlayın.
constraints:
  - "Tanımlanan kuralın özgüllük puanı kesinlikle sıfır (0) olmalı"
  - "Geliştiriciler tek bir sınıf yazarak bu stili kolayca ezebilmeli"
concept_tags: [specificity, maintainability]
checklist_extra:
  - ":where() sözde sınıfı kullanılmış mı?"
  - ":is() ile arasındaki özgüllük farkı doğru anlaşılmış mı?"
reference_solution_path: private/solutions/css-easy-where-pseudo-class-zero-specificity.css
hint_ladder:
  1: ":is() ile aynı çalışan ancak özgüllüğü daima 0 olan sözde sınıf hangisidir?"
  2: "CSS reset yazarken ezilmesi en kolay kuralı hangi sözde sınıfla kurarız?"
  3: "Bu sıfır özgüllük aracı 'sıfır özgüllüklü seçici (:where pseudo-class)' olarak bilinir."
```

---

### css-easy-line-clamp-multi-line-ellipsis

```yaml
id: css-easy-line-clamp-multi-line-ellipsis
version: 1
language: css
engine: none
difficulty: easy
title: "Çok satırlı makale özetini tam 3 satırda kırpma"
prompt: |
  Bir blog kartındaki makale özet paragrafı bazen 2 satır bazen 10 satır olabilmektedir.
  Tüm kartların eşit boyda kalması için metnin tam 3 satır görünmesini, 3. satırın sonunda
  otomatik olarak üç nokta (...) konularak metnin geri kalanının gizlenmesini sağlayan modern
  çok satırlı kırpma kuralını yazın.
constraints:
  - "Metin azami 3 satır olarak sınırlandırılmalı"
  - "Taşan metin gizlenmeli ve 3. satırın sonuna üç nokta eklenmeli"
concept_tags: [typography, edge-cases]
checklist_extra:
  - "-webkit-line-clamp: 3 ve line-clamp: 3 tanımlanmış mı?"
  - "display: -webkit-box ve -webkit-box-orient: vertical kuralları eksiksiz mi?"
reference_solution_path: private/solutions/css-easy-line-clamp-multi-line-ellipsis.css
hint_ladder:
  1: "Çok satırlı metinleri belirli bir satır sayısında kesen özellik nedir?"
  2: "line-clamp kuralının çalışması için hangi webkit kutu özellikleri gereklidir?"
  3: "Bu tipografi standardı 'çok satırlı metin kırpma (line-clamp)' olarak bilinir."
```

---

### css-easy-gradient-subtle-hero-bg

```yaml
id: css-easy-gradient-subtle-hero-bg
version: 1
language: css
engine: none
difficulty: easy
title: "İki renkli doğrusal degrade arka plan"
prompt: |
  Bir mobil uygulamanın karşılama ekranına derinlik katmak istiyorsunuz. Ekranın sol üst
  köşesinden sağ alt köşesine doğru (135 derece açıyla) koyu lacivertten gece mavisine
  pürüzsüzce geçiş yapan şık bir doğrusal renk geçişi (linear-gradient) arka planı oluşturun.
constraints:
  - "Doğrusal renk geçişi (linear-gradient) kullanılmalı"
  - "Geçiş açısı veya yönü 135 derece olarak belirlenmeli"
  - "İki renk durağı eksiksiz tanımlanmalı"
concept_tags: [color, layout]
checklist_extra:
  - "background-image veya background içinde linear-gradient fonksiyonu kullanılmış mı?"
  - "Açı değeri 135deg olarak belirtilmiş mi?"
reference_solution_path: private/solutions/css-easy-gradient-subtle-hero-bg.css
hint_ladder:
  1: "CSS'te iki renk arasında doğrusal geçiş yapan fonksiyon nedir?"
  2: "Açıyı derece cinsinden belirtmek için fonksiyona ilk parametre olarak ne yazılır?"
  3: "Bu görsel efekt 'doğrusal renk geçişi (linear-gradient)' olarak bilinir."
```

---

### css-easy-radial-gradient-vignette

```yaml
id: css-easy-radial-gradient-vignette
version: 1
language: css
engine: none
difficulty: easy
title: "Merkezden yayılan dairesel ışık efekti"
prompt: |
  Bir ürün vitrininde ortada duran spor ayakkabısının arkasında, merkezden dışa doğru yayılan
  dairesel bir aydınlatma efekti oluşturmak istiyorsunuz. Kartın merkezinde parlak beyaz bir
  noktadan başlayıp kenarlara doğru yumuşak griye açılan dairesel renk geçişini (radial-gradient) yazın.
constraints:
  - "Merkezden dışa yayılan dairesel renk geçişi kullanılmalı"
  - "Geçiş kartın tam merkezine odaklanmalı"
concept_tags: [color, centering]
checklist_extra:
  - "radial-gradient fonksiyonu kullanılmış mı?"
  - "Merkez noktası circle at center olarak kurgulanmış mı?"
reference_solution_path: private/solutions/css-easy-radial-gradient-vignette.css
hint_ladder:
  1: "Merkezden dairesel olarak dışarı açılan degrade fonksiyonu nedir?"
  2: "linear-gradient yerine dairesel geçiş için hangi fonksiyon çağrılır?"
  3: "Bu ışıklandırma kuralı 'dairesel renk geçişi (radial-gradient)' olarak bilinir."
```

---

### css-easy-clip-path-circle-avatar

```yaml
id: css-easy-clip-path-circle-avatar
version: 1
language: css
engine: none
difficulty: easy
title: "Kırpma yoluyla kusursuz dairesel görsel maskeleme"
prompt: |
  Kare formatındaki kullanıcı fotoğraflarını border-radius kullanmadan, modern geometrik
  kırpma yolu (clip-path) özelliğini kullanarak tam merkezden yüzde 50 yarıçaplı kusursuz
  bir daire şeklinde kesin.
constraints:
  - "Geometrik kırpma yolu fonksiyonu kullanılmalı"
  - "Daire şekli kutunun tam ortasına oturtulmalı"
concept_tags: [layout, performance]
checklist_extra:
  - "clip-path: circle(50% at center) veya eşdeğeri kullanılmış mı?"
  - "Donanım hızlandırmalı modern kırpma yöntemi seçilmiş mi?"
reference_solution_path: private/solutions/css-easy-clip-path-circle-avatar.css
hint_ladder:
  1: "Bir elemanı istenilen geometrik şekilde kesip maskeleyen CSS özelliği nedir?"
  2: "Daire şeklinde kırpmak için clip-path içine hangi şekil fonksiyonu yazılır?"
  3: "Bu görsel maskeleme 'kırpma yolu daire maskesi (clip-path circle)' olarak bilinir."
```

---

### css-easy-backdrop-filter-frosted-glass

```yaml
id: css-easy-backdrop-filter-frosted-glass
version: 1
language: css
engine: none
difficulty: easy
title: "Buzlu cam efektli yarı saydam başlık çubuğu"
prompt: |
  Sayfa aşağı kayarken sayfa içeriğinin üzerinden geçen yapışkan üst başlığın (header)
  arka planını yarı saydam yapın. Başlığın arkasında kalan metin ve görsellerin başlığın
  içinden buzlu cam gibi bulanık (blur) görünmesini sağlayan modern arka plan filtreleme kuralını yazın.
constraints:
  - "Başlık zemin rengi yarı saydam (rgba) olmalı"
  - "Başlığın arkasında kalan katman bulanıklaştırılmalı"
concept_tags: [color, layout]
checklist_extra:
  - "backdrop-filter: blur(10px) kuralı kullanılmış mı?"
  - "Normal filter ile backdrop-filter arasındaki fark gözetilmiş mi?"
reference_solution_path: private/solutions/css-easy-backdrop-filter-frosted-glass.css
hint_ladder:
  1: "Bir elemanın kendi içeriğini değil, hemen arkasında kalan katmanı bulanıklaştıran özellik nedir?"
  2: "Buzlu cam efekti için backdrop-filter içine hangi efekt fonksiyonu yazılır?"
  3: "Bu popüler cam tasarımı 'arka plan filtreleme buzlu cam efekti (backdrop-filter blur)' olarak bilinir."
```

---

### css-easy-column-count-newspaper

```yaml
id: css-easy-column-count-newspaper
version: 1
language: css
engine: none
difficulty: easy
title: "Gazete tarzı çok sütunlu metin akışı"
prompt: |
  Geniş ekranlarda uzun bir makale metninin tek bir satırda kilometrelerce uzamasını engellemek
  ve gazete/dergi sayfalarındaki gibi akıcı okunmasını sağlamak istiyorsunuz. Metin bloğunu
  yan yana iki eşit sütuna bölen ve sütunların arasına 32 piksel boşluk koyan CSS çoklu sütun
  kurallarını yazın.
constraints:
  - "Metin akışı otomatik olarak 2 sütuna paylaştırılmalı"
  - "Sütunlar arası boşluk 32 piksel olarak tanımlanmalı"
concept_tags: [typography, layout]
checklist_extra:
  - "column-count: 2 özelliği tanımlanmış mı?"
  - "Sütun aralığı için column-gap: 32px kullanılmış mı?"
reference_solution_path: private/solutions/css-easy-column-count-newspaper.css
hint_ladder:
  1: "Bir metin bloğunu gazete sütunları gibi bölüştüren CSS özelliği nedir?"
  2: "Sütun sayısını 2 yapmak için hangi kural atanır?"
  3: "Bu tipografi mizanpajı 'çoklu sütun metin düzeni (column-count)' olarak bilinir."
```

---

### css-easy-scroll-margin-top-offset

```yaml
id: css-easy-scroll-margin-top-offset
version: 1
language: css
engine: none
difficulty: easy
title: "Sabit başlık altında kalan çapa başlıklarını kurtarma"
prompt: |
  Web sitenizde 80 piksel yüksekliğinde sabit bir üst menü (`position: fixed`) vardır. Kullanıcı
  sayfa içi bağlantıya (örneğin `#bolum-2`) tıkladığında, ilgili başlık tam ekranın tepesine
  zıplamakta ve 80 piksellik menünün arkasında kalarak gizlenmektedir. Çapa hedeflenen başlığın
  ekran tepesinden 100 piksel aşağıda durmasını sağlayan modern kaydırma kenar boşluğunu tanımlayın.
constraints:
  - "Kaydırma hedefi başlığa üst kaydırma boşluğu atanmalı"
  - "Başlığın sabit menü altında kalması engellenmeli"
concept_tags: [positioning, maintainability]
checklist_extra:
  - "scroll-margin-top: 100px kuralı kullanılmış mı?"
  - "Eski görünmez eleman hileleri yerine modern kaydırma payı mı tercih edilmiş?"
reference_solution_path: private/solutions/css-easy-scroll-margin-top-offset.css
hint_ladder:
  1: "Sayfa içi bağlantılarda tarayıcının duracağı noktaya pay bırakan özellik nedir?"
  2: "Sabit başlığın yüksekliğini telafi etmek için hedefe hangi scroll özelliği verilir?"
  3: "Bu gezinme çözümü 'kaydırma hedefi kenar boşluğu (scroll-margin-top)' olarak bilinir."
```

---

### css-easy-counter-ordered-list

```yaml
id: css-easy-counter-ordered-list
version: 1
language: css
engine: none
difficulty: easy
title: "CSS sayaçları ile özel numaralı sıralı liste"
prompt: |
  Bir yemek tarifi adım listesinde, standart HTML numaraları yerine yuvarlak mavi rozetler
  içinde 'Adım 1', 'Adım 2' şeklinde özel numaralandırma yapmak istiyorsunuz. CSS sayaç (counter)
  mekanizmasını kullanarak; listede sayacı başlatan, her adımda sayacı bir artıran ve
  `::before` sözde elemanıyla bu numarayı rozet içine basan kuralları yazın.
constraints:
  - "Liste kapsayıcısında sayaç başlatılmalı"
  - "Her liste maddesinde sayaç birer artırılmalı"
  - "`::before` sözde elemanında `content: counter(...)` ile numara yazdırılmalı"
concept_tags: [maintainability, typography]
checklist_extra:
  - "counter-reset ve counter-increment kuralları doğru yerlere konmuş mu?"
  - "content içinde counter() fonksiyonu çağrılmış mı?"
reference_solution_path: private/solutions/css-easy-counter-ordered-list.css
hint_ladder:
  1: "CSS'te dinamik sayı saydırmak için kullanılan mekanizmanın adı nedir?"
  2: "Sayacı sıfırlayan ve her adımda artıran iki anahtar özellik hangileridir?"
  3: "Bu numaralandırma tekniği 'CSS otomatik sayaçları (counter-reset ve counter-increment)' olarak bilinir."
```

---

### css-easy-before-after-decorative-quote

```yaml
id: css-easy-before-after-decorative-quote
version: 1
language: css
engine: none
difficulty: easy
title: "Alıntı bloğuna dekoratif tırnak işareti ekleme"
prompt: |
  Bir alıntı kutusunun (`<blockquote>`) sol üst köşesine HTML'e fazladan etiket eklemeden,
  tamamen CSS sözde elemanları aracılığıyla devasa, soluk gri renkte bir tırnak işareti (“)
  yerleştirin. Sözde elemanın içerik özelliğini kullanarak bu dekorasyonu oluşturun.
constraints:
  - "`::before` sözde elemanı kullanılmalı"
  - "`content` özelliğinde tırnak karakteri tanımlanmalı"
  - "Alıntı metninin okunabilirliğini engellemeyecek şekilde konumlandırılmalı"
concept_tags: [typography, positioning]
checklist_extra:
  - "content özelliği boş bırakılmadan tırnak işareti atanmış mı?"
  - "Dekoratif amaçla mutlak konumlandırma düşünülmüş mü?"
reference_solution_path: private/solutions/css-easy-before-after-decorative-quote.css
hint_ladder:
  1: "Bir elemanın içeriğinden hemen önce sanal bir görsel katman ekleyen sözde eleman nedir?"
  2: "Sözde elemanın ekranda çizilebilmesi için hangi özelliğin mutlaka tanımlanması şarttır?"
  3: "Bu tipografi dekorasyonu 'sözde eleman içerik üretimi (::before content)' olarak bilinir."
```

---

### css-easy-pointer-events-none-icon

```yaml
id: css-easy-pointer-events-none-icon
version: 1
language: css
engine: none
difficulty: easy
title: "Arama kutusu simgesini tıklamaya karşı şeffaf kılma"
prompt: |
  Bir arama girdi kutusunun içine sağ tarafta duracak şekilde büyüteç ikonu yerleştirdiniz.
  Ancak kullanıcı arama çubuğunun sağ tarafına tıkladığında, tıklama büyüteç ikonuna denk
  gelmekte ve arama kutusu odak almamaktadır. İkonun fare tıklamalarını tamamen yok saymasını
  ve tıklamanın arkadaki girdi kutusuna geçmesini sağlayan kuralı yazın.
constraints:
  - "İkon elemanının fare etkileşimlerine tepki vermesi engellenmeli"
  - "Tıklama arkasındaki girdi kutusuna nüfuz etmeli"
concept_tags: [focus, edge-cases]
checklist_extra:
  - "pointer-events: none kuralı ikona uygulanmış mı?"
  - "Kullanıcının girdi kutusuna tıklama deneyimi iyileştirilmiş mi?"
reference_solution_path: private/solutions/css-easy-pointer-events-none-icon.css
hint_ladder:
  1: "Bir elemanın fare tıklamalarını ve işaretçi olaylarını görmezden gelmesini sağlayan özellik nedir?"
  2: "Tıklamanın elemanı delip arkaya geçmesi için pointer-events değerine ne verilir?"
  3: "Bu etkileşim kuralı 'işaretçi olaylarını yok sayma (pointer-events: none)' olarak bilinir."
```

---

### css-easy-resize-vertical-textarea

```yaml
id: css-easy-resize-vertical-textarea
version: 1
language: css
engine: none
difficulty: easy
title: "Metin alanının yatayda genişletilip mizanpajı bozmasını önleme"
prompt: |
  HTML'deki çok satırlı metin kutuları (`<textarea>`) varsayılan olarak kullanıcının sağ alt
  köşeden tutup hem yatay hem dikey çekmesine izin verir. Kullanıcı kutuyu yatayda çektiğinde
  tüm sayfa mizanpajı kırılmakta ve dışarı taşmaktadır. Kullanıcının kutuyu yalnızca dikeyde
  uzatabilmesini sağlayan, yatay genişletmeyi ise kesin olarak kilitleyen kuralı yazın.
constraints:
  - "Boyutlandırma yalnızca dikey eksenle sınırlandırılmalı"
  - "Yatay genişleme tamamen engellenmeli"
concept_tags: [layout, edge-cases]
checklist_extra:
  - "resize: vertical kuralı kullanılmış mı?"
  - "resize: none yerine kullanıcıya dikey esneklik tanınmış mı?"
reference_solution_path: private/solutions/css-easy-resize-vertical-textarea.css
hint_ladder:
  1: "Metin kutularının kullanıcı tarafından yeniden boyutlandırılmasını yöneten özellik nedir?"
  2: "Yalnızca yukarı-aşağı çekilmesine izin veren değer hangisidir?"
  3: "Bu form mizanpaj denetimi 'dikey boyutlandırma kısıtı (resize: vertical)' olarak bilinir."
```

---

### css-easy-overscroll-behavior-contain

```yaml
id: css-easy-overscroll-behavior-contain
version: 1
language: css
engine: none
difficulty: easy
title: "Modal kaydırma çubuğunun ana sayfayı kaydırmasını önleme"
prompt: |
  Açılan bir modal pencere veya yan çekmece (drawer) içinde uzun bir metin kaydırılmaktadır.
  Kullanıcı modalın sonuna ulaştığında kaydırmaya devam ederse, arka plandaki ana web sayfası
  da kaymaya başlamakta (scroll chaining) ve kullanıcı yerini kaybetmektedir. Modal içindeki
  kaydırmanın modal sınırları içinde hapsolmasını sağlayan kaydırma davranışı kuralını tanımlayın.
constraints:
  - "Kaydırma taşması ebeveyn sayfaya zincirlenmemeli"
  - "Kaydırma yalnızca aktif kutu içinde hapsedilmeli"
concept_tags: [layout, edge-cases]
checklist_extra:
  - "overscroll-behavior: contain kuralı atanmış mı?"
  - "Mobil cihazlarda sayfa yenileme tetiklenmesi engellenmiş mi?"
reference_solution_path: private/solutions/css-easy-overscroll-behavior-contain.css
hint_ladder:
  1: "Bir kutu bittiğinde kaydırma hareketinin arkadaki sayfaya geçmesini engelleyen özellik nedir?"
  2: "Kaydırma zincirini kırmak için overscroll-behavior özelliğine hangi değer verilir?"
  3: "Bu kaydırma izolasyonu 'kaydırma zinciri hapsetme (overscroll-behavior: contain)' olarak bilinir."
```

---

### css-easy-scroll-snap-mandatory

```yaml
id: css-easy-scroll-snap-mandatory
version: 1
language: css
engine: none
difficulty: easy
title: "Yatay fotoğraf galerisinde manyetik kart hizalama"
prompt: |
  Kullanıcının parmağıyla kaydırdığı bir fotoğraf şeridinde, fotoğrafların yarım yamalak
  ortada durmasını istemiyorsunuz. Kullanıcı kaydırmayı bıraktığı anda en yakın fotoğrafın
  manyetik bir şekilde ekranın sol kenarına tam oturmasını (snap) sağlayan CSS kaydırma
  kenetlenme kurallarını hem kapsayıcıya hem çocuk elemanlara tanımlayın.
constraints:
  - "Kapsayıcı yatay eksende zorunlu kenetlenme (mandatory snap) tanımlamalı"
  - "Çocuk elemanlar kenetlenme noktası olarak başlangıç çizgisine (start) kilitlenmeli"
concept_tags: [layout, responsive]
checklist_extra:
  - "Kapsayıcıda scroll-snap-type: x mandatory kullanılmış mı?"
  - "Kartlarda scroll-snap-align: start tanımlanmış mı?"
reference_solution_path: private/solutions/css-easy-scroll-snap-mandatory.css
hint_ladder:
  1: "Kaydırma bittiğinde sayfayı belirli noktalara kitleyen CSS özelliği nedir?"
  2: "Kapsayıcıya snap tipi verildikten sonra çocuklara hangi hizalama özelliği atanır?"
  3: "Bu manyetik kaydırma 'kaydırma kenetlenme sistemi (CSS scroll snap)' olarak bilinir."
```

---

### css-easy-prefers-reduced-motion-toggle

```yaml
id: css-easy-prefers-reduced-motion-toggle
version: 1
language: css
engine: none
difficulty: easy
title: "Hareket hassasiyeti olan kullanıcılar için animasyonları kapatma"
prompt: |
  Vestibüler bozukluğu veya hareket hassasiyeti olan kullanıcılar, işletim sistemlerinde
  'Hareketi Azalt' seçeneğini aktif etmektedir. Web sitenizdeki tüm pürüzsüz kaydırmaları
  ve dönme/zıplama animasyonlarını, bu tercihi açmış olan kullanıcılar için anında kapatan
  veya sürelerini sıfırlayan erişilebilirlik medya sorgusunu yazın.
constraints:
  - "Kullanıcının hareket azaltma tercihi medya sorgusuyla dinlenmeli"
  - "Animasyon ve geçiş süreleri sıfırlanmalı veya kapatılmalı"
concept_tags: [accessibility, animation]
checklist_extra:
  - "@media (prefers-reduced-motion: reduce) kullanılmış mı?"
  - "animation-duration ve transition-duration sıfırlanmış mı?"
reference_solution_path: private/solutions/css-easy-prefers-reduced-motion-toggle.css
hint_ladder:
  1: "Kullanıcının sistemindeki hareket azaltma ayarını kontrol eden medya sorgusu nedir?"
  2: "Hareket hassasiyeti olanlar için animasyonları iptal etmek üzere hangi değer dinlenir?"
  3: "Bu kritik erişilebilirlik standardı 'hareket azaltma medya sorgusu (prefers-reduced-motion)' olarak bilinir."
```

---

### css-easy-font-variant-numeric-tabular

```yaml
id: css-easy-font-variant-numeric-tabular
version: 1
language: css
engine: none
difficulty: easy
title: "Finans tablosunda rakamların alt alta hizalanması"
prompt: |
  Bir muhasebe tablosundaki para tutarlarında '1' rakamı dar, '8' rakamı geniş olduğu için
  alt alta gelen sayılar dalgalanmakta ve basamaklar birbirini tutmamaktadır. Yazı tipinin
  tüm rakamları eşit genişlikte bir kutu içinde çizmesini (daktilo rakamları gibi) sağlayarak
  finansal sütunların kusursuz hizalanmasını sağlayan tipografi kuralını yazın.
constraints:
  - "Rakamların genişlikleri eşit sütun formatına dönüştürülmeli"
  - "Farklı basamakların alt alta dikey hizası korunmalı"
concept_tags: [typography, layout]
checklist_extra:
  - "font-variant-numeric: tabular-nums kuralı atanmış mı?"
  - "Tablo sayısal hücreleri için doğru hedeflenmiş mi?"
reference_solution_path: private/solutions/css-easy-font-variant-numeric-tabular.css
hint_ladder:
  1: "Yazı tiplerindeki rakamların genişliğini eşitleyen OpenType CSS özelliği nedir?"
  2: "Tablolarda sayıların hizalanması için bu özelliğe hangi değer atanır?"
  3: "Bu finansal tipografi kuralı 'tablo rakamları hizalaması (font-variant-numeric: tabular-nums)' olarak bilinir."
```

---

### css-easy-accent-color-form-theme

```yaml
id: css-easy-accent-color-form-theme
version: 1
language: css
engine: none
difficulty: easy
title: "Yerleşik form kontrollerini tek satırda renklendirme"
prompt: |
  HTML'in standart onay kutuları (`checkbox`), radyo butonları (`radio`) ve aralık kaydırıcıları
  (`range`) varsayılan olarak mavi renkle çizilir. Hiç karmaşık stil sıfırlaması yapmadan,
  tarayıcının tüm bu yerleşik kontrolleri şirketinizin kurumsal mor renginde (`#7c3aed`)
  çizmesini sağlayan modern vurgu rengi özelliğini kök seviyesinde uygulayın.
constraints:
  - "Tüm yerel form etkileşim kontrollerinin vurgu rengi tek kuralda değiştirilmeli"
  - "Kural geniş tarayıcı desteğine sahip modern özellikle yazılmalı"
concept_tags: [color, accessibility]
checklist_extra:
  - "accent-color özelliği tanımlanmış mı?"
  - ":root veya form seçicisine mi uygulanmış?"
reference_solution_path: private/solutions/css-easy-accent-color-form-theme.css
hint_ladder:
  1: "Tarayıcının yerel onay ve radyo kutularını renklendiren modern CSS özelliği nedir?"
  2: "Tek satırda form kontrollerine marka rengi atamak için ne yazılır?"
  3: "Bu pratik form kuralı 'vurgu rengi tanımlaması (accent-color)' olarak bilinir."
```

---

### css-easy-color-scheme-dark-light

```yaml
id: css-easy-color-scheme-dark-light
version: 1
language: css
engine: none
difficulty: easy
title: "Tarayıcı kaydırma çubukları ve kontrollerine karanlık tema bildirme"
prompt: |
  Karanlık temaya sahip bir sayfada, tarayıcının varsayılan kaydırma çubukları (scrollbar)
  ve form elemanları parlak beyaz renkle parlayarak göz almaktadır. Tarayıcıya sitenizin
  hem açık hem koyu temayı desteklediğini bildiren ve sistem kaydırma çubuklarının da
  otomatik olarak koyu renge bürünmesini sağlayan kök renk şeması kuralını tanımlayın.
constraints:
  - "Sayfa kökünde açık ve koyu tema desteği beyan edilmeli"
  - "Tarayıcının dahili arayüz elemanlarının temaya uyumu sağlanmalı"
concept_tags: [color, maintainability]
checklist_extra:
  - "color-scheme: dark light veya light dark kuralı tanımlanmış mı?"
  - ":root veya html elemanına mı atanmış?"
reference_solution_path: private/solutions/css-easy-color-scheme-dark-light.css
hint_ladder:
  1: "Tarayıcının kaydırma çubuğu gibi yerleşik parçalarını temaya uyduran özellik nedir?"
  2: "Kök elemana karanlık ve aydınlık desteği bildirmek için hangi değerler verilir?"
  3: "Bu sistem kuralı 'renk şeması bildirimi (color-scheme)' olarak bilinir."
```

---

### css-easy-hyphens-auto-justified

```yaml
id: css-easy-hyphens-auto-justified
version: 1
language: css
engine: none
difficulty: easy
title: "İki yana yaslı metinlerde otomatik tireleme"
prompt: |
  Dar bir gazete sütununda metinler iki yana yaslandığında (`text-align: justify`), uzun kelimeler
  alt satıra geçtiği için satır aralarında nehir gibi çirkin devasa boşluklar oluşmaktadır.
  Tarayıcının dil kurallarına uygun olarak kelimeleri hecelerinden otomatik tire ile (-)
  bölmesini sağlayan tireleme kuralını tanımlayın.
constraints:
  - "Kelimeler satır sonunda otomatik olarak hecelere ayrılarak tirelenmeli"
  - "İki yana yaslı metindeki orantısız boşluklar giderilmeli"
concept_tags: [typography, edge-cases]
checklist_extra:
  - "hyphens: auto kuralı kullanılmış mı?"
  - "HTML lang niteliğiyle uyumlu çalıştığı gözetilmiş mi?"
reference_solution_path: private/solutions/css-easy-hyphens-auto-justified.css
hint_ladder:
  1: "Kelimelerin satır sonunda otomatik olarak heceleme çizgisiyle bölünmesini sağlayan özellik nedir?"
  2: "Tarayıcının sözlüğüne göre tireleme yapması için hyphens özelliğine ne yazılır?"
  3: "Bu tipografi optimizasyonu 'otomatik tireleme (hyphens: auto)' olarak bilinir."
```

---

### css-easy-caret-color-custom

```yaml
id: css-easy-caret-color-custom
version: 1
language: css
engine: none
difficulty: easy
title: "Metin girdi imlecinin yanıp sönen rengini özelleştirme"
prompt: |
  Bir lüks marka web sitesindeki arama kutusuna tıklandığında yanıp sönen dikey metin imlecinin
  (caret), tarayıcının standart siyah rengi yerine markanın altın sarısı (`#d97706`) renginde
  yanıp sönmesini sağlayan kuralı tanımlayın.
constraints:
  - "Metin yazma imlecinin rengi marka rengine dönüştürülmeli"
  - "Girdi içindeki harflerin rengi bu kuraldan etkilenmemeli"
concept_tags: [color, focus]
checklist_extra:
  - "caret-color özelliği tanımlanmış mı?"
  - "Normal color özelliği ile karıştırılmadan yalnızca imleç mi hedeflenmiş?"
reference_solution_path: private/solutions/css-easy-caret-color-custom.css
hint_ladder:
  1: "Metin kutusunda yanıp sönen dikey yazma çizgisinin rengini değiştiren özellik nedir?"
  2: "Yazı rengini bozmadan sadece imleci renklendiren anahtar kelime nedir?"
  3: "Bu form stili 'metin imleci rengi (caret-color)' olarak bilinir."
```

---

### css-easy-z-index-dropdown-layer

```yaml
id: css-easy-z-index-dropdown-layer
version: 1
language: css
engine: none
difficulty: easy
title: "Açılır menünün kartların arkasında kalmasını önleme"
prompt: |
  Bir üst menüdeki 'Kategoriler' butonuna tıklandığında açılan alt menü listesi, hemen altta
  duran ürün afişinin ve butonların arkasında kalarak tıklanamaz hale gelmektedir. Açılır
  menünün katman derinliğini artırarak sayfadaki tüm normal içeriklerin üzerinde yüzecek
  şekilde görüntülenmesini sağlayan konumlandırma ve katman sırası kuralını yazın.
constraints:
  - "Eleman katman sıralamasında üst seviyeye çıkarılmalı"
  - "Katman kuralının çalışması için uygun konumlandırma (position) tanımlanmalı"
concept_tags: [stacking-context, positioning]
checklist_extra:
  - "z-index değeri atanmış mı?"
  - "z-index'in çalışabilmesi için static olmayan bir position verilmiş mi?"
reference_solution_path: private/solutions/css-easy-z-index-dropdown-layer.css
hint_ladder:
  1: "Elemanların Z ekseninde (derinlikte) hangisinin üstte duracağını belirleyen özellik nedir?"
  2: "z-index özelliğinin çalışabilmesi için elemanın hangi konumda olmaması şarttır?"
  3: "Bu katmanlama kuralı 'katman önceliği (z-index layering)' olarak bilinir."
```

---

### css-easy-isolation-isolate-stack

```yaml
id: css-easy-isolation-isolate-stack
version: 1
language: css
engine: none
difficulty: easy
title: "Bileşen içi katmanları dış dünyadan izole etme"
prompt: |
  Bir kart bileşeni içinde rozetler ve resimler için `z-index: 1`, `z-index: 2` gibi katmanlar
  kullandınız. Ancak bu z-index değerleri sayfanın dışındaki diğer elemanlarla yarışa girmekte
  ve kart sayfa menülerinin üzerine taşmaktadır. Kartın içinde yeni bir yerel yığınlama bağlamı
  (stacking context) yaratarak iç katmanları kart içine hapseden modern yalıtım özelliğini yazın.
constraints:
  - "Bileşen için yeni ve bağımsız bir yığınlama bağlamı oluşturulmalı"
  - "Hileli z-index veya transform kuralları yerine modern yalıtım özelliği tercih edilmeli"
concept_tags: [stacking-context, edge-cases]
checklist_extra:
  - "isolation: isolate kuralı kullanılmış mı?"
  - "Kart içi katmanların dış dünyaya sızması engellenmiş mi?"
reference_solution_path: private/solutions/css-easy-isolation-isolate-stack.css
hint_ladder:
  1: "Bir elemana hiçbir hile yapmadan doğrudan yeni bir stacking context açan modern özellik nedir?"
  2: "z-index savaşlarını bileşen sınırlarında kesmek için isolation özelliğine ne yazılır?"
  3: "Bu modern mimari kuralı 'katman yalıtımı (isolation: isolate)' olarak bilinir."
```

---

## 3. Orta (Medium) — 50 Soru

### css-medium-grid-template-areas-dashboard

```yaml
id: css-medium-grid-template-areas-dashboard
version: 1
language: css
engine: none
difficulty: medium
title: "İsimlendirilmiş ızgara alanlarıyla kontrol paneli mizanpajı"
prompt: |
  Karmaşık bir kurumsal kontrol paneli (dashboard) tasarlıyorsunuz. Sayfada üst başlık (header),
  sol navigasyon menüsü (sidebar), ana içerik akışı (main) ve sağda iki küçük widget alanı
  yer almaktadır. Sayısal sütun indeksleri yerine, CSS Grid'in görsel şablon alanları
  özelliğini kullanarak ekran düzenini haritalandıran ve kodun okunabilirliğini artıran
  mizanpajı kurun.
constraints:
  - "İsimlendirilmiş ızgara alanları (grid-template-areas) kullanılmalı"
  - "Bileşenler ilgili ızgara alanlarına (grid-area) atanmalı"
  - "Bölümler arasında 20 piksel boşluk bırakılmalı"
concept_tags: [layout, maintainability]
checklist_extra:
  - "grid-template-areas dizgisi görsel mizanpajı net yansıtıyor mu?"
  - "Her ana bölüme grid-area ile isim verilmiş mi?"
reference_solution_path: private/solutions/css-medium-grid-template-areas-dashboard.css
hint_ladder:
  1: "CSS Grid'de sütun ve satırlara isim verip ASCII çizimi gibi haritalandıran özellik nedir?"
  2: "grid-template-areas içinde tırnaklı satır blokları nasıl tanımlanır?"
  3: "Bu gelişmiş ızgara mimarisi 'isimlendirilmiş ızgara alanları (grid-template-areas)' olarak bilinir."
```

---

### css-medium-fluid-typography-clamp

```yaml
id: css-medium-fluid-typography-clamp
version: 1
language: css
engine: none
difficulty: medium
title: "Akışkan ve kesintisiz ölçeklenen başlık boyutu"
prompt: |
  Bir web sitesinin ana başlığının dar mobil ekranlarda en az 24 piksel, devasa 4K ekranlarda
  ise en fazla 64 piksel olması; bu iki sınır arasında ise ekran genişliğine göre orantılı,
  kesintisiz ve pürüzsüz bir şekilde akışkan olarak büyümesi istenmektedir. Onlarca medya
  sorgusu yazmak yerine, modern CSS sınırlandırma matematik fonksiyonunu kullanarak tek
  satırda bu akışkan tipografiyi uygulayın.
constraints:
  - "Minimum sınır, ideal dinamik değer ve maksimum sınır tek fonksiyonda birleştirilmeli"
  - "Medya sorgusu yazılmadan kesintisiz akışkan ölçeklenme sağlanmalı"
concept_tags: [typography, responsive]
checklist_extra:
  - "clamp(min, val, max) matematik fonksiyonu kullanılmış mı?"
  - "İdeal değer için viewport birimi (vw) ve rem kombinasyonu tercih edilmiş mi?"
reference_solution_path: private/solutions/css-medium-fluid-typography-clamp.css
hint_ladder:
  1: "Bir değeri alt ve üst sınırlar arasında esneten modern CSS matematik fonksiyonu nedir?"
  2: "clamp fonksiyonunun ikinci parametresine dinamik büyüme için hangi birim yazılır?"
  3: "Bu tipografi formülü 'akışkan tipografi (fluid typography clamp)' olarak bilinir."
```

---

### css-medium-container-query-card

```yaml
id: css-medium-container-query-card
version: 1
language: css
engine: none
difficulty: medium
title: "Kendi genişliğine göre biçim değiştiren duyarlı bileşen"
prompt: |
  Bir ürün kartı hem dar yan sütunda (sidebar) hem de geniş ana içerik alanında kullanılmaktadır.
  Kartın biçimi ekran genişliğine göre değil, içine konulduğu kapsayıcının genişliğine göre
  şekillenmelidir. Kapsayıcısı 450 pikselden dar olduğunda dikey sütun, 450 pikselden geniş
  olduğunda ise yatay kart düzenine geçen modern kapsayıcı sorgusu (Container Queries) kuralını kurun.
constraints:
  - "Ebeveyn eleman kapsayıcı bağlamı (container-type: inline-size) olarak tanımlanmalı"
  - "Bileşenin iç mizanpajı `@container` sorgusu ile yönetilmeli"
concept_tags: [responsive, layout]
checklist_extra:
  - "container-type: inline-size kuralı ebeveyne atanmış mı?"
  - "@media yerine modern @container sorgusu kullanılmış mı?"
reference_solution_path: private/solutions/css-medium-container-query-card.css
hint_ladder:
  1: "Bileşenleri ekran genişliği yerine kendi ebeveynlerinin genişliğine göre uyarlayan yeni nesil sorgu nedir?"
  2: "Ebeveyni bir kapsayıcı sorgusu hedefi yapmak için hangi özellik atanır?"
  3: "Bu modüler tasarım standardı 'kapsayıcı sorguları (CSS Container Queries)' olarak bilinir."
```

---

### css-medium-cascade-layers-organization

```yaml
id: css-medium-cascade-layers-organization
version: 1
language: css
engine: none
difficulty: medium
title: "CSS basamak katmanları ile mimari özgüllük yönetimi"
prompt: |
  Büyük ölçekli bir projede üçüncü taraf stil kütüphaneleri, bileşen stilleri ve yardımcı
  (utility) sınıflar birbirini ezmekte ve özgüllük (specificity) kaosu yaşanmaktadır.
  Stillerin öncelik sırasını seçici ağırlıklarına bırakmadan; sırasıyla `reset`, `components`
  ve `utilities` adında üç basamak katmanı (Cascade Layers) oluşturun ve yardımcı sınıfların
  diğer tüm stilleri her zaman doğal olarak ezebilmesini sağlayın.
constraints:
  - "`@layer` yönergesi ile açık bir katman öncelik sırası tanımlanmalı"
  - "Stiller ilgili katman blokları içine dağıtılmalı"
  - "Özgüllük puanı düşük olsa bile üst katmanın önceliği korunmalı"
concept_tags: [specificity, maintainability]
checklist_extra:
  - "@layer reset, components, utilities ön beyanı yapılmış mı?"
  - "Katman hiyerarşisi doğru sırada oluşturulmuş mu?"
reference_solution_path: private/solutions/css-medium-cascade-layers-organization.css
hint_ladder:
  1: "CSS stillerini mantıksal öncelik katmanlarına ayıran modern yönerge hangisidir?"
  2: "@layer kuralında katmanların öncelik sırası nasıl belirlenir?"
  3: "Bu mimari standart 'CSS basamak katmanları (Cascade Layers)' olarak bilinir."
```

---

### css-medium-subgrid-aligned-cards

```yaml
id: css-medium-subgrid-aligned-cards
version: 1
language: css
engine: none
difficulty: medium
title: "Kart satırları arasında kusursuz başlık ve buton hizalaması"
prompt: |
  Yan yana duran üç ürün kartında başlıklar, açıklamalar ve 'Satın Al' butonları yer almaktadır.
  Bir kartın başlığı veya açıklaması 3 satır uzadığında, diğer kartlardaki butonlar yukarıda
  kalmakta ve yatay hiza bozulmaktadır. Üst ızgaranın satır çizgilerini kartların kendi
  içine miras almasını sağlayan CSS Subgrid özelliğini kullanarak, tüm kartların başlık, gövde
  ve butonlarının satır bazında birbirine kilitlenmesini sağlayın.
constraints:
  - "Kart kapsayıcısı üst ızgaranın satırlarını miras almalı"
  - "`grid-template-rows: subgrid` özelliği kullanılmalı"
  - "Farklı uzunluktaki içeriklerde bile kardeş kartların butonları aynı yatay çizgide hizalanmalı"
concept_tags: [layout, edge-cases]
checklist_extra:
  - "grid-template-rows değeri subgrid olarak atanmış mı?"
  - "Kartın grid satır aralığı üst ızgaraya bağlanmış mı?"
reference_solution_path: private/solutions/css-medium-subgrid-aligned-cards.css
hint_ladder:
  1: "Bir ızgara elemanının kendi çocuklarını ebeveyn ızgaranın çizgilerine hizalayan özellik nedir?"
  2: "grid-template-rows özelliğine hangi değer verildiğinde satırlar ebeveynle senkronize olur?"
  3: "Bu gelişmiş ızgara tekniği 'alt ızgara hizalaması (CSS Subgrid)' olarak bilinir."
```

---

### css-medium-css-nesting-component

```yaml
id: css-medium-css-nesting-component
version: 1
language: css
engine: none
difficulty: medium
title: "Yerel CSS iç içe geçme sözdizimi ile modüler kart"
prompt: |
  Sass veya PostCSS benzeri ön işlemcilere ihtiyaç duymadan, modern tarayıcıların desteklediği
  yerel CSS İç İçe Geçme (Native CSS Nesting) özelliğini kullanarak bir kart bileşeni stillendirin.
  `.card` sınıfı altında kart başlığını, kart görselini, kartın `:hover` durumunu ve kartın
  içindeki butonun odak durumunu ampersand (`&`) ebeveyn seçicisini kullanarak modüler tek
  bir blok halinde yazın.
constraints:
  - "Yerel CSS nesting sözdizimi kullanılmalı"
  - "Ebeveyn seçici (`&`) ile hover ve odak durumları bağlanmalı"
  - "Çocuk elemanlar ebeveyn bloğunun içine gömülmeli"
concept_tags: [maintainability, specificity]
checklist_extra:
  - "Harici derleyici olmadan standart CSS nesting kuralları uygulanmış mı?"
  - "&:hover sözdizimi doğru yapılandırılmış mı?"
reference_solution_path: private/solutions/css-medium-css-nesting-component.css
hint_ladder:
  1: "Modern CSS'te stilleri Sass gibi iç içe yazmayı sağlayan yerel özellik nedir?"
  2: "İç içe blokta geçerli ebeveyn seçiciyi temsil eden sembol hangisidir?"
  3: "Bu modern yazım standardı 'yerel CSS iç içe geçme (Native CSS Nesting)' olarak bilinir."
```

---

### css-medium-keyframes-spinner-loader

```yaml
id: css-medium-keyframes-spinner-loader
version: 1
language: css
engine: none
difficulty: medium
title: "Kesintisiz 360 derece dönen yükleme göstergesi"
prompt: |
  Bir veri yükleme anında ekranda beliren 40x40 piksel boyutunda dairesel bir yükleme halkası
  (spinner) tasarlayın. Halkanın üç kenarı açık gri, bir kenarı ise mavi renkte olsun.
  CSS anahtar kareleri (`@keyframes`) ile halkanın kendi ekseni etrafında 0 dereceden
  360 dereceye doğru sonsuz döngüde, doğrusal (linear) hızla takılmadan dönmesini sağlayan
  animasyon kuralını yazın.
constraints:
  - "`@keyframes` ile 0'dan 360 dereceye dönüş tanımlanmalı"
  - "Animasyon hızı doğrusal (linear) ve döngüsü sonsuz (infinite) olmalı"
  - "Donanım hızlandırmalı transform fonksiyonu kullanılmalı"
concept_tags: [animation, performance]
checklist_extra:
  - "animation: spin 1s linear infinite kuralı eksiksiz mi?"
  - "@keyframes bloğunda transform: rotate(360deg) doğru yazılmış mı?"
reference_solution_path: private/solutions/css-medium-keyframes-spinner-loader.css
hint_ladder:
  1: "CSS'te özel kare kare animasyon üretmeyi sağlayan kural bloğu nedir?"
  2: "Dönüşün hiç yavaşlamadan sabit hızla devam etmesi için hangi zamanlama fonksiyonu kullanılır?"
  3: "Bu yükleme bileşeni 'anahtar kareli dönme animasyonu (@keyframes spinner)' olarak bilinir."
```

---

### css-medium-keyframes-skeleton-shimmer

```yaml
id: css-medium-keyframes-skeleton-shimmer
version: 1
language: css
engine: none
difficulty: medium
title: "İskelet yükleme kartında akan ışık efekti"
prompt: |
  YouTube ve Facebook benzeri platformlarda içerik yüklenirken gösterilen gri iskelet kartlarının
  üzerinden soldan sağa doğru akan hafif beyaz bir parlama (shimmer) efekti tasarlayın.
  Geniş açılı bir doğrusal degrade arka plan oluşturun ve `@keyframes` animasyonu ile bu
  arka planın yatay konumunu kaydırarak kesintisiz akan bir ışık yansıması elde edin.
constraints:
  - "Doğrusal renk geçişi içeren arka plan tanımlanmalı"
  - "`@keyframes` ile arka plan yatay konumu (background-position) kaydırılmalı"
  - "Animasyon sonsuz döngüde akıcı çalışmalı"
concept_tags: [animation, color]
checklist_extra:
  - "Arka plan boyutu kapsayıcıdan geniş (örn. 200%) tutulmuş mu?"
  - "Animasyon zamanlaması ve yönü akıcı mı?"
reference_solution_path: private/solutions/css-medium-keyframes-skeleton-shimmer.css
hint_ladder:
  1: "İskelet ekranlarda ışık akması efekti üretmek için hangi arka plan özelliği hareket ettirilir?"
  2: "background-position değerini yüzde 200'den eksi 200'e kaydırmak ne hissi verir?"
  3: "Bu yükleme arayüzü 'iskelet parlama animasyonu (skeleton shimmer animation)' olarak bilinir."
```

---

### css-medium-dual-ring-accessible-focus

```yaml
id: css-medium-dual-ring-accessible-focus
version: 1
language: css
engine: none
difficulty: medium
title: "Her zeminde görünür çift halkalı erişilebilir odak göstergesi"
prompt: |
  Koyu renkli zeminlerde siyah odak çizgileri, açık renkli zeminlerde ise beyaz odak çizgileri
  görünmez hale gelir. Buton veya bağlantı klavyeyle odaklandığında, hem açık hem koyu renkli
  tüm arka planlarda daima kontrastını koruyan, içte beyaz bir boşluk halkası dışta ise
  koyu mavi bir çerçeve oluşturan çift katmanlı erişilebilir odak halkasını (dual-ring focus) tasarlayın.
constraints:
  - "Odak göstergesi hem açık hem koyu zeminlerde yüksek kontrast sağlamalı"
  - "`outline` ve `box-shadow` veya `outline-offset` kombinasyonu kullanılmalı"
  - "Yalnızca klavye odağında (`:focus-visible`) aktifleşmeli"
concept_tags: [focus, accessibility]
checklist_extra:
  - "Çift katmanlı kontrast oluşturulmuş mu?"
  - ":focus-visible kullanılarak fare tıklamasında gereksiz parlaması engellenmiş mi?"
reference_solution_path: private/solutions/css-medium-dual-ring-accessible-focus.css
hint_ladder:
  1: "Bir odak çizgisinin arkasına ikinci bir zıt renk halkası eklemenin en pratik CSS yolu nedir?"
  2: "outline ile box-shadow birlikte kullanıldığında nasıl bir odak halkası elde edilir?"
  3: "Bu yüksek kontrastlı desen 'çift halkalı erişilebilir odak göstergesi (dual-ring focus)' olarak bilinir."
```

---

### css-medium-holy-grail-layout

```yaml
id: css-medium-holy-grail-layout
version: 1
language: css
engine: none
difficulty: medium
title: "Modern Kutsal Kase sayfa mizanpajı"
prompt: |
  Web tasarımının klasik 'Holy Grail' mizanpajını kurun: En üstte sabit başlık, en altta
  altbilgi; ortada ise solda navigasyon menüsü (200px), ortada esnek ana içerik alanı (1fr)
  ve sağda ek bilgiler paneli (200px). CSS Grid kullanarak bu yapıyı kurun; sayfa içeriği
  az olsa dahi altbilginin ekranın dibine yapışmasını sağlayın.
constraints:
  - "CSS Grid ile 3 sütunlu ve 3 satırlı mizanpaj tanımlanmalı"
  - "Orta içerik esnek büyüme göstermeli, yan sütunlar sabit kalmalı"
  - "Tüm sayfa yüksekliği en az 100vh olmalı"
concept_tags: [layout, responsive]
checklist_extra:
  - "grid-template-rows: auto 1fr auto düzeni kurulmuş mu?"
  - "grid-template-columns: 200px 1fr 200px yapısı doğru mu?"
reference_solution_path: private/solutions/css-medium-holy-grail-layout.css
hint_ladder:
  1: "Üst, alt ve 3 sütunlu orta gövdeden oluşan klasik sayfa düzenine webde ne ad verilir?"
  2: "CSS Grid ile satırları başlık, esnek gövde ve altbilgi şeklinde bölmek için ne yazılır?"
  3: "Bu mimari 'Kutsal Kase mizanpajı (Holy Grail layout)' olarak bilinir."
```

---

### css-medium-sticky-table-header-first-column

```yaml
id: css-medium-sticky-table-header-first-column
version: 1
language: css
engine: none
difficulty: medium
title: "Büyük tabloda hem başlık satırını hem ilk sütunu sabitleme"
prompt: |
  Yüzlerce satır ve onlarca sütun içeren geniş bir finans tablosunda, kullanıcı hem aşağı
  hem sağa doğru kaydırma yapmaktadır. Sayfa kaydırıldıkça tablonun en üst başlık satırının
  (`<thead>`) yukarıda sabit kalmasını; aynı zamanda sağa kaydırıldığında ise ürün isimlerini
  içeren ilk sütunun (`<th>` / ilk `<td>`) solda yapışık kalarak donmasını (freeze column)
  sağlayan çift yönlü yapışkan konumlandırmayı kurun.
constraints:
  - "Üst başlık hücreleri dikeyde (`top: 0`) sabitlenmeli"
  - "İlk sütun hücreleri yatayda (`left: 0`) sabitlenmeli"
  - "Sol üst köşe hücresi iki yapışmanın da üstünde duracak z-index derinliğine sahip olmalı"
concept_tags: [positioning, stacking-context]
checklist_extra:
  - "position: sticky kuralları hem th hem ilk sütun için doğru koordinatlarla verilmiş mi?"
  - "Sol üst köşe çakışması z-index ile çözülmüş mü?"
reference_solution_path: private/solutions/css-medium-sticky-table-header-first-column.css
hint_ladder:
  1: "Tablo başlıklarını kaydırma sırasında dondurmak için hücrelere hangi konum verilir?"
  2: "İlk sütunu dondurmak için left: 0 değeri hangi hücrelere atanır?"
  3: "Bu gelişmiş tablo deseni 'çift eksenli yapışkan tablo (sticky header and frozen column)' olarak bilinir."
```

---

### css-medium-mask-image-gradient-fade

```yaml
id: css-medium-mask-image-gradient-fade
version: 1
language: css
engine: none
difficulty: medium
title: "Kaydırma kutusu dibinde degrade silinme efekti"
prompt: |
  Bir kullanıcı sözleşmesi veya bildirim listesi kutusunda metin aşağıya doğru devam etmektedir.
  Kutunun alt kenarındaki metinlerin küt diye sert bir çizgiyle kesilmesi yerine, dibe doğru
  şeffaflaşarak tatlı bir şekilde silinmesini (fade out) istiyorsunuz. Kutunun üzerine beyaz
  katman koymak yerine, arka plan rengi ne olursa olsun çalışan CSS maskeleme özelliğini kullanın.
constraints:
  - "Maskeleme görüntüsü doğrusal degrade ile oluşturulmalı"
  - "Kutunun üst kısmı tam opak, en alt kısmı tam şeffaf olmalı"
concept_tags: [layout, performance]
checklist_extra:
  - "mask-image veya -webkit-mask-image kullanılmış mı?"
  - "linear-gradient(to bottom, black 80%, transparent 100%) mantığı uygulanmış mı?"
reference_solution_path: private/solutions/css-medium-mask-image-gradient-fade.css
hint_ladder:
  1: "Bir elemanın belirli bölgelerini şeffaflaştırarak maskeleyen CSS özelliği nedir?"
  2: "Dibe doğru görünmezlik sağlamak için mask-image içine hangi fonksiyon yazılır?"
  3: "Bu görsel efekt 'degrade maskeleme silinmesi (mask-image gradient fade)' olarak bilinir."
```

---

### css-medium-clip-path-diagonal-section

```yaml
id: css-medium-clip-path-diagonal-section
version: 1
language: css
engine: none
difficulty: medium
title: "Çokgen kırpma ile eğik bölge ayracı tasarımı"
prompt: |
  Bir web sitesinin karşılama bölümü ile ürünler bölümü arasındaki yatay düz çizgiyi kaldırıp,
  modern açılı bir eğim (diyagonal çizgi) kazandırmak istiyorsunuz. Hiçbir SVG veya görsel
  dosyası kullanmadan, tamamen CSS çokgen kırpma fonksiyonu ile bölümün alt köşesini
  açılı kesen kuralı yazın.
constraints:
  - "`clip-path: polygon(...)` fonksiyonu kullanılmalı"
  - "Dört köşe koordinatı açı oluşturacak şekilde tanımlanmalı"
concept_tags: [layout, performance]
checklist_extra:
  - "polygon koordinatları geçerli yüzde değerleriyle mi verilmiş?"
  - "Gereksiz DOM elemanı oluşturulmadan doğrudan bölüme mi uygulanmış?"
reference_solution_path: private/solutions/css-medium-clip-path-diagonal-section.css
hint_ladder:
  1: "CSS'te bir kutuyu çokgen köşeleriyle kesip şekillendiren kırpma fonksiyonu nedir?"
  2: "Alt kenarı eğik kesmek için dördüncü köşe koordinatı nasıl ayarlanır?"
  3: "Bu tasarım tekniği 'açılı çokgen bölüm ayracı (clip-path diagonal section)' olarak bilinir."
```

---

### css-medium-custom-range-slider-styling

```yaml
id: css-medium-custom-range-slider-styling
version: 1
language: css
engine: none
difficulty: medium
title: "Aralık kaydırıcı çubuğu ve tutamacını özelleştirme"
prompt: |
  Bir ses veya fiyat aralığı seçici (`<input type="range">`) bileşenini özel olarak stilize edin.
  Tarayıcının varsayılan ray çizgisini 6 piksel yüksekliğinde açık gri bir şeride çevirin;
  kaydırıcı tutamacını (thumb) ise 24x24 piksel boyutunda, mavi renkli, beyaz kenarlıklı
  ve gölgeli modern bir düğmeye dönüştürün.
constraints:
  - "Tarayıcı varsayılan ray ve tutamaç çizimi sıfırlanmalı"
  - "Tutamaç sözde elemanları (WebKit ve Mozilla için) tanımlanmalı"
concept_tags: [maintainability, accessibility]
checklist_extra:
  - "::-webkit-slider-thumb ve ::-moz-range-thumb hedeflenmiş mi?"
  - "appearance: none uygulanmış mı?"
reference_solution_path: private/solutions/css-medium-custom-range-slider-styling.css
hint_ladder:
  1: "Aralık kaydırıcının tutamacını hedefleyen tarayıcı sözde elemanları nelerdir?"
  2: "Kendi stilimizi çizebilmek için önce appearance özelliğine ne yazılır?"
  3: "Bu form özelleştirmesi 'kaydırıcı tutamaç ve ray stili (custom range slider)' olarak bilinir."
```

---

### css-medium-staggered-list-animation

```yaml
id: css-medium-staggered-list-animation
version: 1
language: css
engine: none
difficulty: medium
title: "Kademeli gecikmeli liste giriş animasyonu"
prompt: |
  Bir menü veya bildirim listesi açıldığında, listedeki maddelerin hepsinin aynı anda değil;
  sırayla, birbiri ardına (kademeli / staggered) hafifçe aşağıdan yukarı kayarak belirmesini
  istiyorsunuz. Her liste maddesine tek tek sınıf yazmak yerine, CSS değişkeni (`--i`) ile
  hesaplanan gecikme süresini (`calc(var(--i) * 100ms)`) kullanan tek ve modüler bir
  animasyon kuralı yazın.
constraints:
  - "Her elemanın gecikme süresi CSS değişkeni ve `calc()` ile hesaplanmalı"
  - "Elemanlar saydamlıktan opaka ve aşağıdan yukarıya doğru kaymalı"
concept_tags: [animation, variables]
checklist_extra:
  - "animation-delay içinde calc(var(--i) * 100ms) formülü kullanılmış mı?"
  - "Başlangıç durumu için opacity ve transform hazırlanmış mı?"
reference_solution_path: private/solutions/css-medium-staggered-list-animation.css
hint_ladder:
  1: "Animasyon gecikmesini her eleman için dinamik kılmak adına hangi fonksiyon ikilisi kullanılır?"
  2: "Elemanların sırayla peş peşe akması tekniğine ne ad verilir?"
  3: "Bu mikro etkileşim 'kademeli animasyon gecikmesi (staggered animation delay)' olarak bilinir."
```

---

### css-medium-mix-blend-mode-contrast-text

```yaml
id: css-medium-mix-blend-mode-contrast-text
version: 1
language: css
engine: none
difficulty: medium
title: "Yarı siyah yarı beyaz zemin üzerinde kendini tersleyen metin"
prompt: |
  Sanatsal bir poster tasarımında ekran dikey olarak tam ortadan ikiye bölünmüştür; sol tarafı
  simsiyah, sağ tarafı ise bembeyazdır. Bu iki bölgenin tam ortasında duran büyük bir başlığın,
  siyah zemine denk gelen harflerinin beyaz, beyaz zemine denk gelen harflerinin ise otomatik
  olarak siyah olmasını sağlayan CSS karışım modu kuralını uygulayın.
constraints:
  - "Metin rengi altındaki zeminin zıddına otomatik dönüşmeli"
  - "CSS katman karışım modu (blend mode) özelliği kullanılmalı"
concept_tags: [color, edge-cases]
checklist_extra:
  - "mix-blend-mode: difference kuralı kullanılmış mı?"
  - "Metin rengi saf beyaz olarak tanımlanmış mı?"
reference_solution_path: private/solutions/css-medium-mix-blend-mode-contrast-text.css
hint_ladder:
  1: "Bir elemanın piksellerini arkasındaki zemin pikselleriyle matematiksel olarak harmanlayan özellik nedir?"
  2: "Arkadaki rengi tam tersine çeviren (invert eden) karışım modu hangisidir?"
  3: "Bu tipografik efekt 'karışım moduyla zıt renk dönüşümü (mix-blend-mode difference)' olarak bilinir."
```

---

### css-medium-dialog-backdrop-animation

```yaml
id: css-medium-dialog-backdrop-animation
version: 1
language: css
engine: none
difficulty: medium
title: "Yerel modal arka plan karartmasını ve pencereyi canlandırma"
prompt: |
  HTML5 `<dialog>` elemanı açıldığında (`showModal()`), arkasındaki koyu karartma perdesinin
  (`::backdrop`) ve modal pencerenin kendisinin ani bir parlama yerine, 300 milisaniye içinde
  yumuşakça belirip hafifçe büyüyerek ekrana gelmesini sağlayın.
constraints:
  - "Modal arka plan karartması `::backdrop` sözde elemanı üzerinden stillendirilmeli"
  - "Açılış animasyonu saydamlık ve hafif ölçekleme içermeli"
concept_tags: [animation, positioning]
checklist_extra:
  - "dialog::backdrop sözde elemanı hedeflenmiş mi?"
  - "Açılış için opacity ve transform animasyonu tanımlanmış mı?"
reference_solution_path: private/solutions/css-medium-dialog-backdrop-animation.css
hint_ladder:
  1: "Yerleşik dialog penceresinin arkasındaki karartma katmanını seçen CSS sözde elemanı nedir?"
  2: "Modalın arkasını flu ve saydam yapmak için ::backdrop üzerinde hangi kurallar çalışır?"
  3: "Bu modal tasarımı 'iletişim kutusu perde animasyonu (dialog ::backdrop)' olarak bilinir."
```

---

### css-medium-print-stylesheet-optimization

```yaml
id: css-medium-print-stylesheet-optimization
version: 1
language: css
engine: none
difficulty: medium
title: "Yazıcı çıktısı için optimize edilmiş yazdırma stilleri"
prompt: |
  Kullanıcı sayfayı yazıcıdan veya 'PDF Olarak Kaydet' seçeneğiyle yazdırmak istediğinde;
  sayfadaki gezinme menüsünü ve reklamları gizleyen, gereksiz renk tüketimini önlemek için
  yazıları saf siyaha çeken ve makale paragraflarının sayfa bölünmesinde ortadan ikiye
  kesilmesini engelleyen baskı medya sorgusu kurallarını yazın.
constraints:
  - "`@media print` bloğu içinde tanımlanmalı"
  - "Navigasyon ve reklamlar `display: none` ile gizlenmeli"
  - "Paragrafların sayfa ortasından bölünmesini engelleyen kural eklenmeli"
concept_tags: [responsive, maintainability]
checklist_extra:
  - "break-inside: avoid veya page-break-inside: avoid kullanılmış mı?"
  - "Yazıcı için gereksiz arayüz parçaları gizlenmiş mi?"
reference_solution_path: private/solutions/css-medium-print-stylesheet-optimization.css
hint_ladder:
  1: "Yalnızca yazıcıya gönderildiğinde çalışan CSS medya sorgusu türü nedir?"
  2: "Bir metin bloğunun iki A4 sayfası arasına denk gelip bölünmesini engelleyen özellik nedir?"
  3: "Bu yazdırma optimizasyonu 'yazıcı medya sorgusu kuralları (@media print)' olarak bilinir."
```

---

### css-medium-theme-toggle-data-attribute

```yaml
id: css-medium-theme-toggle-data-attribute
version: 1
language: css
engine: none
difficulty: medium
title: "Öznitelik tabanlı açık ve koyu tema motoru"
prompt: |
  Bir web uygulamasında kullanıcının manuel olarak tema değiştirebilmesi için HTML kök
  etiketine `data-theme="dark"` özniteliği eklenmektedir. Kök değişkenleri (`--bg-color`,
  `--text-color`, `--card-bg`) varsayılan açık tema değerleriyle tanımlayın; ardından
  `[data-theme="dark"]` seçicisi altında bu değişkenleri koyu tema karşılıklarıyla ezerek
  anında tüm sitenin temasını değiştiren yapıyı kurun.
constraints:
  - "Renkler CSS değişkenleri üzerinden yönetilmeli"
  - "Karanlık tema `[data-theme='dark']` seçicisiyle değişkenleri yeniden tanımlamalı"
  - "Sayfa gövdesi ve kartlar doğrudan değişkenleri tüketmeli"
concept_tags: [variables, color]
checklist_extra:
  - "Değişkenler :root ve [data-theme='dark'] altında mı tanımlanmış?"
  - "Tek bir öznitelik değişimiyle tüm renkler otomatik güncelleniyor mu?"
reference_solution_path: private/solutions/css-medium-theme-toggle-data-attribute.css
hint_ladder:
  1: "Tema yönetiminde renkleri tek merkezden değiştirmek için hangi CSS özelliği kullanılır?"
  2: "HTML'deki data-theme özniteliğini CSS seçicisi olarak nasıl hedefleriz?"
  3: "Bu tema mimarisi 'öznitelik tabanlı tema motoru (data-theme CSS variables)' olarak bilinir."
```

---

### css-medium-grid-dense-packing

```yaml
id: css-medium-grid-dense-packing
version: 1
language: css
engine: none
difficulty: medium
title: "Boşlukları geriye dönük dolduran yoğun ızgara akışı"
prompt: |
  Bir fotoğraf galerisinde bazı fotoğraflar 2 sütun veya 2 satır yer kaplamaktadır. Standart
  CSS ızgarasında büyük bir fotoğraf sığmadığında alt satıra geçmekte ve geride çirkin boş
  delikler bırakmaktadır. Izgara algoritmasına geride kalan boşlukları daha küçük fotoğraflarla
  geriye dönük olarak doldurmasını (dense packing) emreden kuralı tanımlayın.
constraints:
  - "Izgarada boşluk bırakmayan yoğun otomatik akış kuralı tanımlanmalı"
  - "Görseller boş kalan hücrelere akıllıca yerleştirilmeli"
concept_tags: [layout, edge-cases]
checklist_extra:
  - "grid-auto-flow: dense veya row dense kullanılmış mı?"
  - "Farklı span değerlerine sahip elemanların delikleri doldurması sağlandı mı?"
reference_solution_path: private/solutions/css-medium-grid-dense-packing.css
hint_ladder:
  1: "CSS Grid'in elemanları yerleştirirken boşluk gördüğünde arkadaki küçük elemanı oraya çekmesini sağlayan değer nedir?"
  2: "grid-auto-flow özelliğine hangi anahtar kelime eklenir?"
  3: "Bu ızgara optimizasyonu 'yoğun ızgara akışı (grid-auto-flow: dense)' olarak bilinir."
```

---

### css-medium-scroll-driven-reading-progress

```yaml
id: css-medium-scroll-driven-reading-progress
version: 1
language: css
engine: none
difficulty: medium
title: "Kaydırmaya duyarlı saf CSS okuma ilerleme çubuğu"
prompt: |
  Bir makale sayfasının en tepesinde duran 4 piksel kalınlığındaki kırmızı çizgi, kullanıcı
  sayfayı aşağı kaydırdıkça soldan sağa doğru yüzde 0'dan yüzde 100 genişliğe uzamalıdır.
  Hiç JavaScript scroll dinleyicisi yazmadan, modern tarayıcıların desteklediği Kaydırma
  Güdümlü Animasyon (Scroll-driven Animations) standardıyla bu ilerleme çubuğunu kurun.
constraints:
  - "JavaScript olmadan tamamen CSS animasyonu ile çözülmeli"
  - "Animasyon zaman çizelgesi sayfa kaydırmasına (`animation-timeline: scroll()`) bağlanmalı"
  - "Genişlik veya ölçekleme 0'dan 1'e doğru ilerlemeli"
concept_tags: [animation, performance]
checklist_extra:
  - "animation-timeline: scroll() özelliği kullanılmış mı?"
  - "Donanım hızlandırmalı transform: scaleX() tercih edilmiş mi?"
reference_solution_path: private/solutions/css-medium-scroll-driven-reading-progress.css
hint_ladder:
  1: "CSS animasyonunu zamana değil sayfa kaydırma mesafesine bağlayan modern özellik nedir?"
  2: "animation-timeline özelliğine hangi kaydırma fonksiyonu verilir?"
  3: "Bu yeni nesil web standardı 'kaydırma güdümlü animasyon (Scroll-driven Animation)' olarak bilinir."
```

---

### css-medium-scroll-snap-header-sync

```yaml
id: css-medium-scroll-snap-header-sync
version: 1
language: css
engine: none
difficulty: medium
title: "Manyetik slayt geçişinde orta eksen kenetlenmesi"
prompt: |
  Kullanıcının kartları kaydırdığı bir mobil tanıtım vitrininde, her kartın sol kenara değil,
  tam ekranın yatay merkezine kilitlenmesini istiyorsunuz. Hem kapsayıcıda hem kartlarda
  merkez odaklı manyetik kenetlenme kurallarını kurun ve kaydırma bittiğinde kartın ekranda
  ortalanmış kalmasını sağlayın.
constraints:
  - "Yatay eksende zorunlu kenetlenme tanımlanmalı"
  - "Kenetlenme hizalaması merkez (center) olarak ayarlanmalı"
concept_tags: [layout, centering]
checklist_extra:
  - "scroll-snap-align: center kuralı kartlara uygulanmış mı?"
  - "scroll-snap-type: x mandatory kapsayıcıda aktif mi?"
reference_solution_path: private/solutions/css-medium-scroll-snap-header-sync.css
hint_ladder:
  1: "Kaydırma bittiğinde kartın ekranın tam ortasına oturmasını sağlayan snap hizalama değeri nedir?"
  2: "scroll-snap-align özelliğine start yerine ne yazılır?"
  3: "Bu hizalama kuralı 'merkezi kaydırma kenetlenmesi (scroll-snap-align: center)' olarak bilinir."
```

---

### css-medium-calc-mixed-units-banner

```yaml
id: css-medium-calc-mixed-units-banner
version: 1
language: css
engine: none
difficulty: medium
title: "Kısıtlı konteyner içinden tüm ekrana taşan tam genişlikli şerit"
prompt: |
  Sayfanız maksimum 1000 piksel genişliğinde ortalanmış bir konteyner içindedir. Ancak bu
  konteynerin tam ortasındaki bir kampanya şeridinin, kapsayıcısından taşarak tarayıcı
  ekranının sol kenarından sağ kenarına kadar tam ekran genişliğinde (%100 viewport) yayılmasını
  istiyorsunuz. HTML yapısını bozmadan, `calc()` matematik fonksiyonu ve negatif kenar
  boşluklarıyla bu tam genişlik taşmasını (full-bleed breakout) kurun.
constraints:
  - "Genişlik 100vw olarak ayarlanmalı"
  - "Kapsayıcının sol sınırını sıfırlamak için negatif margin ve calc formülü kullanılmalı"
concept_tags: [layout, responsive]
checklist_extra:
  - "margin-left: calc(50% - 50vw) veya eşdeğer taşma formülü uygulanmış mı?"
  - "Yatay kaydırma çubuğu taşması kontrol altında mı?"
reference_solution_path: private/solutions/css-medium-calc-mixed-units-banner.css
hint_ladder:
  1: "Kısıtlı bir kutunun içinden tam ekran genişliğine fırlamak için hangi negatif margin formülü kullanılır?"
  2: "50vw ile yüzde 50 arasındaki farkı hesaplayan fonksiyon nedir?"
  3: "Bu mizanpaj hilesi 'tam genişlikli şerit kırılması (full-bleed breakout calc)' olarak bilinir."
```

---

### css-medium-conic-gradient-pie-chart

```yaml
id: css-medium-conic-gradient-pie-chart
version: 1
language: css
engine: none
difficulty: medium
title: "Koni biçimli renk geçişiyle pasta grafik göstergesi"
prompt: |
  Bir analiz panelinde kullanıcının depolama doluluk oranını (yüzde 70 dolu, yüzde 30 boş)
  gösteren dairesel bir pasta grafik oluşturacaksınız. SVG veya canvas kullanmadan, yalnızca
  CSS koni biçimli renk geçişi (conic-gradient) fonksiyonunu kullanarak yüzde 70'i mavi,
  kalan yüzde 30'u gri olan dairesel bir pasta grafiği tek bir `<div>` üzerinde çizin.
constraints:
  - "Koni biçimli renk geçişi (`conic-gradient`) fonksiyonu kullanılmalı"
  - "Yüzde 70 renk durağı ve geçiş noktası tanımlanmalı"
  - "Kutu tam yuvarlak (`border-radius: 50%`) olmalı"
concept_tags: [color, layout]
checklist_extra:
  - "conic-gradient(#2563eb 0% 70%, #e2e8f0 70% 100%) mantığı kurulmuş mu?"
  - "border-radius: 50% ile daireye dönüştürülmüş mü?"
reference_solution_path: private/solutions/css-medium-conic-gradient-pie-chart.css
hint_ladder:
  1: "Merkez etrafında saat yönünde dönerek pasta dilimleri oluşturan CSS degrade fonksiyonu nedir?"
  2: "linear ve radial dışında açısal konik geçiş yapan fonksiyon hangisidir?"
  3: "Bu grafik tekniği 'konik renk geçişiyle pasta grafik (conic-gradient pie chart)' olarak bilinir."
```

---

### css-medium-text-shadow-glow-contrast

```yaml
id: css-medium-text-shadow-glow-contrast
version: 1
language: css
engine: none
difficulty: medium
title: "Karışık fotoğraflar üzerinde beyaz metin okunurluğunu kurtarma"
prompt: |
  Bir kahraman afişinde arka plandaki fotoğrafın bazı yerleri bembeyaz kar, bazı yerleri ise
  koyu dağ manzarasıdır. Üzerindeki beyaz başlık yazısı açık renkli bölgelere denk geldiğinde
  tamamen kaybolmaktadır. Arka plana yapay koyu bir kutu koymak yerine, metnin arkasına
  çok katmanlı yumuşak bir gölge (`text-shadow`) vererek metnin her pikselde kusursuz
  okunmasını sağlayan tipografik kontrast kuralını yazın.
constraints:
  - "Metin gölgesi özelliği (`text-shadow`) kullanılmalı"
  - "Yumuşak ve yaygın bir gölge için bulanıklık yarıçapı dengelenmeli"
  - "Metin okunabilirlik kontrastı garanti altına alınmalı"
concept_tags: [typography, color]
checklist_extra:
  - "text-shadow üzerinde saydam siyah (rgba) kullanılmış mı?"
  - "Gölge metnin doğallığını bozmadan okunurluk sağlıyor mu?"
reference_solution_path: private/solutions/css-medium-text-shadow-glow-contrast.css
hint_ladder:
  1: "Yazıların arkasına gölge ekleyen CSS özelliği hangisidir?"
  2: "Fotoğraf üzerinde beyaz yazıyı kurtarmak için metin gölgesine hangi renk verilir?"
  3: "Bu tipografi güvenliği 'metin gölgesiyle kontrast koruma (text-shadow contrast)' olarak bilinir."
```

---

### css-medium-custom-scrollbar-themed

```yaml
id: css-medium-custom-scrollbar-themed
version: 1
language: css
engine: none
difficulty: medium
title: "Modern ve tarayıcı uyumlu özel kaydırma çubuğu"
prompt: |
  Bir web uygulamasının koyu renkli mesajlaşma panelinde, tarayıcının kalın ve gri renkli
  varsayılan kaydırma çubuğu çok çirkin durmaktadır. Hem W3C standart kaydırma çubuğu
  özelliklerini (`scrollbar-width`, `scrollbar-color`) hem de WebKit sözde elemanlarını
  kullanarak; ince, yuvarlak köşeli ve koyu lacivert temaya uygun şık bir kaydırma çubuğu tasarlayın.
constraints:
  - "Standart W3C `scrollbar-width: thin` ve `scrollbar-color` tanımlanmalı"
  - "WebKit tarayıcılar için genişlik ve tutamaç (thumb) stili desteklenmeli"
concept_tags: [maintainability, color]
checklist_extra:
  - "Hem standart özellikler hem webkit sözde elemanları birlikte düşünülmüş mü?"
  - "Kaydırma tutamacına yuvarlak köşe verilmiş mi?"
reference_solution_path: private/solutions/css-medium-custom-scrollbar-themed.css
hint_ladder:
  1: "W3C standardında kaydırma çubuğu kalınlığını ve rengini belirleyen modern iki özellik nedir?"
  2: "Chrome ve Safari'de kaydırma çubuğunu stillendiren sözde eleman öneki nedir?"
  3: "Bu arayüz kuralı 'özel kaydırma çubuğu tasarımı (custom scrollbar)' olarak bilinir."
```

---

### css-medium-checkbox-toggle-switch

```yaml
id: css-medium-checkbox-toggle-switch
version: 1
language: css
engine: none
difficulty: medium
title: "Saf CSS ile kayan düğmeli açma/kapama anahtarı"
prompt: |
  Standart bir `<input type="checkbox">` elemanını ve yanındaki `<label>` etiketini kullanarak,
  hiç JavaScript kullanmadan modern bir mobil açma/kapama sürgüsü (toggle switch) tasarlayın.
  Kullanıcı tıkladığında (`:checked`), anahtarın içindeki dairesel beyaz topun sağa doğru
  yumuşak bir geçişle kaymasını ve arka planın gri renkten yeşile dönmesini sağlayın.
constraints:
  - "Girdi elemanı gizlenmeli ancak klavye erişilebilirliği korunmalı"
  - "Seçili durumda dairesel buton `transform: translateX(...)` ile sağa kaymalı"
  - "Arka plan rengi yumuşak bir geçişle değişmeli"
concept_tags: [animation, accessibility]
checklist_extra:
  - "input:checked + label yapısı veya benzeri kardeş seçicisi kurulmuş mu?"
  - "Kayan daire için transform ve transition kullanılmış mı?"
reference_solution_path: private/solutions/css-medium-checkbox-toggle-switch.css
hint_ladder:
  1: "Bir onay kutusunun işaretli olup olmamasına göre yanındaki etiketi stillendiren seçici nedir?"
  2: "Düğmeyi sağa kaydırmak için hangi CSS dönüşüm fonksiyonu tercih edilir?"
  3: "Bu popüler form bileşeni 'saf CSS geçiş anahtarı (CSS toggle switch)' olarak bilinir."
```

---

### css-medium-hover-zoom-image-contained

```yaml
id: css-medium-hover-zoom-image-contained
version: 1
language: css
engine: none
difficulty: medium
title: "Kart sınırından taşmadan görsel yakınlaştırma efekti"
prompt: |
  Bir e-ticaret kartının üzerine fareyle gelindiğinde, ürün fotoğrafının yüzde 10 oranında
  hafifçe büyümesini (`scale(1.1)`) istiyorsunuz. Ancak fotoğraf büyürken kartın köşelerinden
  dışarı taşmamalı, kartın sınırları içinde pürüzsüzce büyüyüp küçülmelidir.
constraints:
  - "Kart kapsayıcısı taşan kısımları kırpmalı (`overflow: hidden`)"
  - "Görsel `:hover` anında `transform: scale(...)` ile büyütülmeli"
  - "Büyüme hareketi akıcı bir geçiş (transition) süresine sahip olmalı"
concept_tags: [animation, layout]
checklist_extra:
  - "Ebeveynde overflow: hidden kuralı unutulmamış mı?"
  - "Görselde transform: scale(1.1) ve transition tanımlı mı?"
reference_solution_path: private/solutions/css-medium-hover-zoom-image-contained.css
hint_ladder:
  1: "Bir elemanın büyürken kendi sınırlarını aşmasını engelleyen ebeveyn özelliği nedir?"
  2: "Görseli orantılı olarak büyüten donanım dostu transform fonksiyonu hangisidir?"
  3: "Bu mikro etkileşim 'sınırlı görsel yakınlaştırma efekti (contained hover zoom)' olarak bilinir."
```

---

### css-medium-sidebar-toggle-offcanvas

```yaml
id: css-medium-sidebar-toggle-offcanvas
version: 1
language: css
engine: none
difficulty: medium
title: "Ekran dışından kayarak gelen yan çekmece menü"
prompt: |
  Mobil cihazlarda sol taraftan kayarak açılan bir yan çekmece (off-canvas drawer) menü
  tasarlayın. Menü kapalıyken ekranın sol tarafında tamamen görünmez olmalı (`translateX(-100%)`),
  aktif olduğunda (`.is-open` sınıfı aldığında) ise donanım hızlandırmalı bir animasyonla
  orijinal konumuna (`translateX(0)`) yumuşakça kaymalıdır.
constraints:
  - "Gizleme ve açılma işlemi `transform: translateX` ile yapılmalı (left/margin kullanılmamalı)"
  - "Kayma hareketi 300ms yumuşak bir geçiş süresine sahip olmalı"
  - "Menü tüm ekran yüksekliğini kaplamalı ve en üst katmanda durmalı"
concept_tags: [positioning, animation]
checklist_extra:
  - "left yerine GPU hızlandırmalı transform: translateX(-100%) kullanılmış mı?"
  - "z-index ile sayfanın en üstünde durması sağlanmış mı?"
reference_solution_path: private/solutions/css-medium-sidebar-toggle-offcanvas.css
hint_ladder:
  1: "Bir yan menüyü performanslı bir şekilde ekranın dışına itmek için hangi CSS fonksiyonu kullanılır?"
  2: "left özelliğini canlandırmak ile transform'u canlandırmak arasındaki performans farkı nedir?"
  3: "Bu mobil navigasyon kalıbı 'kayan çekmece menü (off-canvas drawer)' olarak bilinir."
```

---

### css-medium-button-loading-state-spinner

```yaml
id: css-medium-button-loading-state-spinner
version: 1
language: css
engine: none
difficulty: medium
title: "Yükleniyor durumundaki butonda metni gizleyip çark gösterme"
prompt: |
  Kullanıcı 'Ödemeyi Tamamla' butonuna bastığında butona `.is-loading` sınıfı eklenmektedir.
  Bu durumda butonun boyutunun zıplamasını engellemek için butonun içindeki metni görünmez
  yapın (`color: transparent`), butonun tam ortasında ise dönen bir yükleme çarkını
  `::after` sözde elemanı ve animasyon ile ortaya çıkarın.
constraints:
  - "Buton metni şeffaf yapılarak butonun orijinal genişliği korunmalı"
  - "Yükleme çarkı `::after` sözde elemanıyla oluşturulup tam merkeze yerleştirilmeli"
  - "Çark kesintisiz dönme animasyonuna sahip olmalı"
concept_tags: [animation, focus]
checklist_extra:
  - "Metin display: none yapılmayarak butonun küçülmesi önlenmiş mi?"
  - "::after simgesi tam ortaya mutlak konumlandırılmış mı?"
reference_solution_path: private/solutions/css-medium-button-loading-state-spinner.css
hint_ladder:
  1: "Butonun genişliği küçülmesin ama yazısı görünmesin diye renk ne yapılır?"
  2: "Butonun içine harici div koymadan yükleme çarkı eklemenin yolu hangi sözde elemandır?"
  3: "Bu durum tasarımı 'buton yükleniyor çarkı durumu (button loading state)' olarak bilinir."
```

---

### css-medium-table-responsive-stacked-labels

```yaml
id: css-medium-table-responsive-stacked-labels
version: 1
language: css
engine: none
difficulty: medium
title: "Mobilde kartlara dönüşen duyarlı veri tablosu"
prompt: |
  Geniş ekranlarda normal bir veri tablosu olarak duran tablonun, 640 pikselden dar mobil
  ekranlarda yatay kaydırma çubuğu çıkarmak yerine her satırının bağımsız bir karta dönüşmesini
  sağlayın. `display: block` ile satır ve hücreleri alt alta dizin; hücrelerin solunda ise
  HTML'deki `data-label` özniteliğini okuyarak sütun adını yazdıran CSS kuralını kurun.
constraints:
  - "Mobil ekranda `tr`, `td` ve `th` elemanları blok düzene geçmeli"
  - "Hücre başlıkları `td::before` içinde `content: attr(data-label)` ile dinamik yazdırılmalı"
concept_tags: [responsive, layout]
checklist_extra:
  - "attr(data-label) fonksiyonu kullanılmış mı?"
  - "Masaüstünde normal tablo görünümü korunmuş mu?"
reference_solution_path: private/solutions/css-medium-table-responsive-stacked-labels.css
hint_ladder:
  1: "CSS sözde elemanında bir HTML özniteliğinin değerini yazdırmak için hangi fonksiyon kullanılır?"
  2: "Tablo hücrelerini alt alta kart dizilimine sokmak için display değerine ne verilir?"
  3: "Bu duyarlı tablo deseni 'yığılmış kart tablo dönüşümü (responsive stacked table)' olarak bilinir."
```

---

### css-medium-breadcrumbs-separator-styling

```yaml
id: css-medium-breadcrumbs-separator-styling
version: 1
language: css
engine: none
difficulty: medium
title: "Ekmek kırıntısı menüsüne CSS ile ayraç ekleme"
prompt: |
  Bir ekmek kırıntısı (breadcrumbs) gezinti yolunda, sayfalar arasına eğik çizgi (/) veya
  büyüktür (>) işaretini HTML içine elle yazmak ekran okuyucuların kafasını karıştırır.
  HTML kodunu temiz tutarak, her liste maddesinin arasına tamamen CSS `::after` sözde elemanı
  aracılığıyla şık bir ayraç işareti ekleyin; listenin en son elemanından sonra ayraç çıkmasını engelleyin.
constraints:
  - "Ayraç işaretleri `::after` sözde elemanı ile oluşturulmalı"
  - "Listenin sonuncu elemanında ayraç gizlenmeli (`:last-child`)"
concept_tags: [maintainability, layout]
checklist_extra:
  - "content: '/' veya content: '>' tanımlanmış mı?"
  - ":last-child::after seçicisiyle son ayraç silinmiş mi?"
reference_solution_path: private/solutions/css-medium-breadcrumbs-separator-styling.css
hint_ladder:
  1: "HTML'i kirletmeden iki bağlantı arasına ayraç koymanın en anlamsal yolu nedir?"
  2: "En sondaki gereksiz ayracı silmek için hangi sözde sınıf kombinasyonu yazılır?"
  3: "Bu navigasyon stili 'sözde elemanlı ekmek kırıntısı ayracı (breadcrumbs separator)' olarak bilinir."
```

---

### css-medium-tooltip-balloon-positioning

```yaml
id: css-medium-tooltip-balloon-positioning
version: 1
language: css
engine: none
difficulty: medium
title: "Saf CSS ile oklu ipucu balonu tasarımı"
prompt: |
  Bir butonun üzerine gelindiğinde veya klavyeyle odaklanıldığında butonun tam üstünde beliren
  küçük bir ipucu balonu (tooltip) tasarlayın. İpucunun gövdesini ve altına sarkan minik üçgen
  okunu JavaScript olmadan, butonun `data-tooltip` özniteliğini okuyan `::before` ve `::after`
  sözde elemanlarıyla oluşturun.
constraints:
  - "Balon metni `content: attr(data-tooltip)` ile üretilmeli"
  - "Üçgen ok işareti CSS kenarlık hilesiyle çizilmeli"
  - "Yalnızca `:hover` ve `:focus-visible` anlarında görünür olmalı"
concept_tags: [positioning, focus]
checklist_extra:
  - "Hem fare hem klavye odağında ipucunun açılması sağlanmış mı?"
  - "Üçgen ok için border şeffaflık tekniği uygulanmış mı?"
reference_solution_path: private/solutions/css-medium-tooltip-balloon-positioning.css
hint_ladder:
  1: "CSS ile üçgen ok çizmek için şeffaf kenarlıklar (transparent borders) nasıl kullanılır?"
  2: "İpucunun metnini HTML'den dinamik çekmek için hangi CSS fonksiyonu yazılır?"
  3: "Bu arayüz bileşeni 'saf CSS oklu ipucu balonu (CSS tooltip balloon)' olarak bilinir."
```

---

### css-medium-form-floating-label-peer

```yaml
id: css-medium-form-floating-label-peer
version: 1
language: css
engine: none
difficulty: medium
title: "Kayan etiketli animasyonlu girdi alanı"
prompt: |
  Girdi kutusu boşken içinde yer tutucu gibi duran etiket metninin (`<label>`), kullanıcı kutuya
  tıkladığında veya kutuya yazı yazdığında yukarı doğru küçülerek girdi kutusunun üst kenarına
  tünemesini (floating label) sağlayın. Bu animasyonu kardeş seçicileri (`+`) ve `:focus` /
  `:not(:placeholder-shown)` durumlarını kullanarak kurgulayın.
constraints:
  - "Girdi odaklandığında etiket yukarı kaymalı ve boyutu küçülmeli"
  - "Girdide metin varken kullanıcı odaktan çıksa bile etiket yukarıda kalmalı"
  - "Hareket pürüzsüz bir `transform` geçişiyle yapılmalı"
concept_tags: [animation, focus]
checklist_extra:
  - "input:focus + label ve input:not(:placeholder-shown) + label kullanılmış mı?"
  - "Etiketin yukarı çıkışı translateY ve scale ile mi canlandırılmış?"
reference_solution_path: private/solutions/css-medium-form-floating-label-peer.css
hint_ladder:
  1: "Bir girdide metin olup olmadığını CSS ile anlamanın standart hilesi nedir?"
  2: "placeholder-shown sözde sınıfının değili (:not) neyi ifade eder?"
  3: "Bu modern form deseni 'kayan etiket animasyonu (floating label pattern)' olarak bilinir."
```

---

### css-medium-card-flip-3d-perspective

```yaml
id: css-medium-card-flip-3d-perspective
version: 1
language: css
engine: none
difficulty: medium
title: "Üç boyutlu dönerek arkasını gösteren kart efekti"
prompt: |
  Kullanıcı bir oyun kartının veya kartvizitin üzerine geldiğinde, kartın Y ekseni etrafında
  180 derece dönerek arka yüzünü göstermesini sağlayın. Kartın gerçekçi bir 3D derinlikte
  dönmesi için ebeveyne perspektif verin; kartın ön ve arka yüzlerinin sırt sırta durması
  için arka yüz gizleme kuralını tanımlayın.
constraints:
  - "Kapsayıcıya `perspective` derinliği atanmalı"
  - "Dönen gövdeye `transform-style: preserve-3d` verilmeli"
  - "Ters dönen yüzün arkasının görünmemesi için `backface-visibility: hidden` kullanılmalı"
concept_tags: [animation, positioning]
checklist_extra:
  - "preserve-3d kuralı doğru elemana atanmış mı?"
  - "backface-visibility: hidden her iki yüze de tanımlanmış mı?"
reference_solution_path: private/solutions/css-medium-card-flip-3d-perspective.css
hint_ladder:
  1: "CSS'te 3D animasyonların düzleşmesini engelleyip derinliği koruyan özellik nedir?"
  2: "Bir elemanın arkası döndüğünde ters görüntüsünü gizleyen özellik hangisidir?"
  3: "Bu üç boyutlu efekt '3D kart çevirme animasyonu (3D card flip perspective)' olarak bilinir."
```

---

### css-medium-gradient-border-card

```yaml
id: css-medium-gradient-border-card
version: 1
language: css
engine: none
difficulty: medium
title: "Renkli degrade kenarlıklı modern kart"
prompt: |
  Koyu renkli bir web sitesindeki özel bir kartın etrafına mor ve pembe renklerden oluşan
  canlı bir degrade kenarlık çizmek istiyorsunuz. Standart `border-color` özelliği doğrudan
  degrade kabul etmediği için, arka plan kırpma (`background-clip`) veya sözde eleman maskeleme
  tekniğini kullanarak içi koyu, kenarlığı ise degrade parlayan kartı oluşturun.
constraints:
  - "Kenarlık çok renkli bir degrade geçişine sahip olmalı"
  - "Kartın iç gövdesi kendi bağımsız koyu zemin rengini korumalı"
concept_tags: [color, layout]
checklist_extra:
  - "background-clip veya border-image tekniği doğru uygulanmış mı?"
  - "İçerik alanı ile kenarlık degrade rengi birbirine karışmadan ayrışmış mı?"
reference_solution_path: private/solutions/css-medium-gradient-border-card.css
hint_ladder:
  1: "CSS'te bir kutunun kenarlığına degrade vermek için hangi arka plan hilesi kullanılır?"
  2: "background-clip özelliğinde padding-box ve border-box nasıl birlikte çalışır?"
  3: "Bu görsel tasarım 'degrade kenarlık tekniği (gradient border card)' olarak bilinir."
```

---

### css-medium-multi-step-wizard-indicator

```yaml
id: css-medium-multi-step-wizard-indicator
version: 1
language: css
engine: none
difficulty: medium
title: "Çok adımlı sihirbaz bağlantı çizgileri ve aşama halkaları"
prompt: |
  Bir sipariş takip ekranında 4 adımlı bir süreç çubuğu yer almaktadır (Sipariş Alındı,
  Hazırlanıyor, Kargoda, Teslim Edildi). Numaralı adımların arasına gri bağlantı çizgileri
  yerleştirin; tamamlanmış adımları yeşil renge boyayın ve aradaki bağlantı çizgisinin de
  yeşile dönmesini sağlayacak esnek kutu ve sözde eleman mimarisini kurun.
constraints:
  - "Adımlar yatay esnek kutuda eşit aralıklarla dizilmeli"
  - "Adımlar arasındaki çizgiler `::before` veya `::after` ile çizilmeli"
  - "Aktif ve tamamlanmış adımların durum sınıfları renkleri değiştirmeli"
concept_tags: [layout, animation]
checklist_extra:
  - "Bağlantı çizgileri esnek şekilde adımların arasını dolduruyor mu?"
  - "Son adımdan sonra taşan gereksiz çizgi engellenmiş mi?"
reference_solution_path: private/solutions/css-medium-multi-step-wizard-indicator.css
hint_ladder:
  1: "Adım halkaları arasına dinamik bağlantı çizgisi çekmek için hangi sözde eleman kullanılır?"
  2: "Tamamlanan adımların çizgisini yeşil yapmak için durum sınıfları nasıl kurgulanır?"
  3: "Bu navigasyon bileşeni 'aşama göstergesi bağlantı çizgileri (step wizard indicator)' olarak bilinir."
```

---

### css-medium-typing-text-animation

```yaml
id: css-medium-typing-text-animation
version: 1
language: css
engine: none
difficulty: medium
title: "Daktilo tarzı harf harf yazılma ve imleç kırpışması"
prompt: |
  Bir yazılım geliştirici portföyünün girişinde 'Full-Stack Developer' unvanının daktilodan
  çıkıyormuş gibi harf harf ekrana yazılmasını ve cümlenin sonunda bir dikey imlecin yanıp
  sönmesini istiyorsunuz. Eşaralıklı (monospace) bir font kullanarak, `ch` karakter birimi,
  `steps()` zamanlama fonksiyonu ve `@keyframes` ile bu daktilo animasyonunu kurun.
constraints:
  - "Yazı genişliği harf sayısı kadar basamaklı (`steps(...)`) olarak açılmalı"
  - "İmleç yanıp sönmesi için ayrı bir `@keyframes` tanımlanmalı"
  - "Yazı taşmaları `overflow: hidden` ile gizlenmeli"
concept_tags: [animation, typography]
checklist_extra:
  - "steps(N) zamanlama fonksiyonu karakter sayısıyla eşleşiyor mu?"
  - "Harf genişliği ölçümü için ch birimi kullanılmış mı?"
reference_solution_path: private/solutions/css-medium-typing-text-animation.css
hint_ladder:
  1: "Animasyonun akıcı değil tık tık basamaklı ilerlemesini sağlayan zamanlama fonksiyonu nedir?"
  2: "Genişliği karakter adedine göre tam hesaplamak için hangi CSS birimi kullanılır?"
  3: "Bu klasik efekt 'CSS daktilo yazma animasyonu (typewriter steps animation)' olarak bilinir."
```

---

### css-medium-accordion-details-transition

```yaml
id: css-medium-accordion-details-transition
version: 1
language: css
engine: none
difficulty: medium
title: "Yerel açılır kapanır detay etiketini yumuşak geçişle açma"
prompt: |
  HTML'in yerleşik `<details>` ve `<summary>` elemanları varsayılan olarak tıklandığında içeriği
  küt diye aniden açar. Modern CSS ızgara hilesi (`grid-template-rows: 0fr` dan `1fr` e geçiş)
  veya modern geçiş özellikleri kullanarak, açılan içeriğin yüksekliğinin sıfırdan otomatik
  yüksekliğe yumuşak ve akıcı bir şekilde açılarak aşağı inmesini sağlayın.
constraints:
  - "İçerik yüksekliği geçişi küt açılma yerine yumuşak olmalı"
  - "CSS Grid `0fr` / `1fr` satır geçiş tekniği veya interpolate-size kullanılmalı"
concept_tags: [animation, layout]
checklist_extra:
  - "grid-template-rows: 0fr ve 1fr tekniği doğru uygulanmış mı?"
  - "İçerik taşmasını önlemek için overflow: hidden eklenmiş mi?"
reference_solution_path: private/solutions/css-medium-accordion-details-transition.css
hint_ladder:
  1: "Otomatik yüksekliğe (height: auto) sahip içerikleri CSS ile canlandırmanın ızgara çözümü nedir?"
  2: "0fr ile 1fr arasında geçiş yapmak içeriği nasıl açar?"
  3: "Bu animasyon tekniği 'otomatik yükseklik ızgara geçişi (grid 0fr 1fr transition)' olarak bilinir."
```

---

### css-medium-badge-overlapping-avatars

```yaml
id: css-medium-badge-overlapping-avatars
version: 1
language: css
engine: none
difficulty: medium
title: "Üst üste binen grup kullanıcı avatarları kümesi"
prompt: |
  Bir projede çalışan 4 ekip üyesinin profil fotoğraflarını, popüler uygulamalardaki gibi
  birbirinin üzerine hafifçe binecek şekilde (yarı üst üste) dizin. Her avatarın etrafında
  arkadaki avatardan ayıran 2 piksel beyaz bir boşluk sınırı olsun; en sağda ise '+3'
  şeklinde kalan üyeleri gösteren dairesel bir sayaç rozeti yer alsın.
constraints:
  - "Avatarlar birbirinin üzerine binecek şekilde negatif dış boşluk ile sıralanmalı"
  - "Avatarların birbiriyle karışmasını önlemek için beyaz kenarlık tanımlanmalı"
  - "Yığın sırası (z-index) veya doğal akış doğru kurgulanmalı"
concept_tags: [layout, stacking-context]
checklist_extra:
  - "Negatif margin-left veya margin-right kullanılmış mı?"
  - "Beyaz kenarlık ile avatarların çakışma hatları temiz ayrılmış mı?"
reference_solution_path: private/solutions/css-medium-badge-overlapping-avatars.css
hint_ladder:
  1: "Elemanların yatayda birbirinin üzerine geçmesini sağlayan boşluk yöntemi nedir?"
  2: "Kutu kenarlığı ile alttaki fotoğrafı kesmek için ne tanımlanır?"
  3: "Bu arayüz deseni 'üst üste binen avatarlar yığını (avatar stack overlap)' olarak bilinir."
```

---

### css-medium-dynamic-aspect-ratio-masonry

```yaml
id: css-medium-dynamic-aspect-ratio-masonry
version: 1
language: css
engine: none
difficulty: medium
title: "Pinterest tarzı akıcı duvar mizanpajı"
prompt: |
  Pinterest benzeri bir görsel platformunda farklı dikey uzunluklara sahip görselleri
  sergiliyorsunuz. Standart ızgaralarda alt alta gelen görseller arasında oluşan çirkin
  boşlukları engellemek için, CSS çoklu sütun (column-count) özelliğini kullanarak görsellerin
  duvar gibi birbirinin peşi sıra aşağı aktığı ve kartların sütunlar arasında ortadan
  bölünmediği bir duvar (masonry) mizanpajı kurun.
constraints:
  - "`column-count` ile çoklu sütun yapısı kurulmalı"
  - "Kartların sütun sınırında bölünmesini engellemek için `break-inside: avoid` kullanılmalı"
  - "Sütun aralıkları ve kart alt boşlukları eşitlenmeli"
concept_tags: [layout, responsive]
checklist_extra:
  - "break-inside: avoid tanımlanmış mı?"
  - "Kartların dikeyde birbirine yapışması önlenmiş mi?"
reference_solution_path: private/solutions/css-medium-dynamic-aspect-ratio-masonry.css
hint_ladder:
  1: "Görsellerin gazete gibi dikey akıp birbirini takip etmesini sağlayan CSS özelliği nedir?"
  2: "Bir kartın iki sütun arasında parçalanmasını önleyen kural hangisidir?"
  3: "Bu akıcı mizanpaj 'CSS sütun tabanlı duvar düzeni (CSS column masonry)' olarak bilinir."
```

---

### css-medium-content-visibility-auto

```yaml
id: css-medium-content-visibility-auto
version: 1
language: css
engine: none
difficulty: medium
title: "Ekran dışı bölümleri işlemeyerek açılış hızını artırma"
prompt: |
  Binlerce ürünün veya uzun bir haber akışının listelendiği devasa bir sayfada, tarayıcı
  sayfa ilk açıldığında henüz ekranın çok aşağısında kalan ve kullanıcının görmediği
  yüzlerce bölümü de DOM'da çizmeye çalışarak işlemciyi kilitlemektedir. Ekran dışındaki
  bölümlerin çizim ve mizanpaj hesaplamalarını kullanıcı oraya kaydırana kadar atlayan
  modern performans özelliğini uygulayın.
constraints:
  - "`content-visibility: auto` kuralı uygulanmalı"
  - "Kaydırma çubuğunun zıplamasını engellemek için `contain-intrinsic-size` tanımlanmalı"
concept_tags: [performance, layout]
checklist_extra:
  - "content-visibility: auto kuralı kullanılmış mı?"
  - "Tahmini yükseklik için contain-intrinsic-size verilmiş mi?"
reference_solution_path: private/solutions/css-medium-content-visibility-auto.css
hint_ladder:
  1: "Ekran dışında kalan elemanların rendering maliyetini sıfırlayan yeni nesil özellik nedir?"
  2: "Bu özellik etkinken sayfa kaydırma çubuğunun doğru boyutta kalması için hangi tahmini boyut atanır?"
  3: "Bu kritik render optimizasyonu 'içerik görünürlük performans kuralı (content-visibility: auto)' olarak bilinir."
```

---

### css-medium-font-display-swap-foit

```yaml
id: css-medium-font-display-swap-foit
version: 1
language: css
engine: none
difficulty: medium
title: "Görünmez metin parlamasını önleyen yazı tipi yükleme kuralı"
prompt: |
  Özel bir web yazı tipi (`@font-face`) sunucudan indirilirken, tarayıcı yazı tipi inene kadar
  yazıları ekranda tamamen görünmez kılmakta (Flash of Invisible Text - FOIT) ve ziyaretçiler
  3 saniye boyunca boş ekran görmektedir. Yazı tipi inene kadar sistemin varsayılan fontunu
  anında gösteren, font indiğinde ise pürüzsüzce değiştiren yazı tipi görüntüleme kuralını tanımlayın.
constraints:
  - "`@font-face` bloğu içinde tanımlanmalı"
  - "Görünmez metin engellenmeli ve hemen yedek font çizilmeli"
concept_tags: [performance, typography]
checklist_extra:
  - "font-display: swap kuralı kullanılmış mı?"
  - "LCP ve Core Web Vitals ölçümlerine katkısı düşünülmüş mü?"
reference_solution_path: private/solutions/css-medium-font-display-swap-foit.css
hint_ladder:
  1: "Web yazı tipi indirilirken tarayıcının metni gizlemesini engelleyen kural nedir?"
  2: "Font inene kadar sistem fontunu gösterip inince takas eden değer hangisidir?"
  3: "Bu performans standardı 'yazı tipi takas görüntülemesi (font-display: swap)' olarak bilinir."
```

---

### css-medium-scroll-padding-top-anchor

```yaml
id: css-medium-scroll-padding-top-anchor
version: 1
language: css
engine: none
difficulty: medium
title: "Kapsayıcı düzeyinde kaydırma ofseti yönetimi"
prompt: |
  Her başlığa tek tek `scroll-margin-top` yazmak yerine, sayfadaki 70 piksel yüksekliğindeki
  sabit başlığı telafi etmek için doğrudan sayfa köküne veya kaydırma kapsayıcısına üstten
  kaydırma iç boşluğu tanımlayın. Sayfa içi tüm çapa atlamalarının otomatik olarak bu boşluğu
  hesaba katmasını sağlayın.
constraints:
  - "Kural kök veya ana kaydırma kapsayıcısına atanmalı"
  - "Tüm sayfa içi çapa atlamaları bu payı otomatik almalı"
concept_tags: [positioning, maintainability]
checklist_extra:
  - "scroll-padding-top: 70px kuralı html seçicisine tanımlanmış mı?"
  - "scroll-margin ile scroll-padding arasındaki ebeveyn-çocuk farkı gözetilmiş mi?"
reference_solution_path: private/solutions/css-medium-scroll-padding-top-anchor.css
hint_ladder:
  1: "Kaydırma kapsayıcısının durma bölgesine küresel iç pay bırakan özellik nedir?"
  2: "Tüm sayfa bağlantılarını tek merkezden ofsetlemek için nereye uygulanır?"
  3: "Bu global kaydırma kuralı 'kaydırma kapsayıcı iç payı (scroll-padding-top)' olarak bilinir."
```

---

### css-medium-animation-fill-mode-retain

```yaml
id: css-medium-animation-fill-mode-retain
version: 1
language: css
engine: none
difficulty: medium
title: "Animasyon bittiğinde son karedeki stili koruma"
prompt: |
  Bir bildirim kartı ekrana gelirken sıfır saydamlıktan tam opaklığa çıkmakta ve 20 piksel
  aşağı kaymaktadır. Ancak animasyon süresi bittiği anda eleman bir anda ilk haline geri
  fırlamakta ve kaybolmaktadır. Animasyon tamamlandığında son karenin (`to` veya `100%`)
  özelliklerinin eleman üzerinde kalıcı olarak korunmasını sağlayan dolgu modu kuralını yazın.
constraints:
  - "Animasyon bittiğinde başa dönmemeli, ulaştığı son durumda sabit kalmalı"
  - "Doğru animasyon dolgu kuralı tanımlanmalı"
concept_tags: [animation, maintainability]
checklist_extra:
  - "animation-fill-mode: forwards atanmış mı?"
  - "both veya forwards kullanımı doğru analiz edilmiş mi?"
reference_solution_path: private/solutions/css-medium-animation-fill-mode-retain.css
hint_ladder:
  1: "Bir CSS animasyonu bittiğinde son karenin stillerini elemanın üzerinde tutan özellik nedir?"
  2: "İleriye doğru son durumu dondurmak için fill-mode özelliğine ne yazılır?"
  3: "Bu animasyon kuralı 'animasyon son durumunu koruma (animation-fill-mode: forwards)' olarak bilinir."
```

---

### css-medium-focus-trap-overlay-dim

```yaml
id: css-medium-focus-trap-overlay-dim
version: 1
language: css
engine: none
difficulty: medium
title: "Açık modal arkasındaki içeriği görsel olarak susturma"
prompt: |
  Bir modal açıldığında, sayfa arkasındaki içeriklerin kullanıcının dikkatini dağıtmasını
  engellemek istiyorsunuz. Modal arkasındaki ana içerik kapsayıcısına bir karartma ve
  hafif bir flu efekti (bulanıklık) uygulayarak, kullanıcının görsel algısının tamamen
  aktif pencereye kilitlenmesini sağlayan durum kuralını yazın.
constraints:
  - "Arka plan içeriği hafif grileşmeli ve saydamlaşmalı"
  - "Arka plana `filter: blur(...)` bulanıklık efekti uygulanmalı"
concept_tags: [color, focus]
checklist_extra:
  - "Arka plan için filter: blur(4px) veya benzeri kullanılmış mı?"
  - "Modalın kendisi bu bulanıklıktan hariç tutulmuş mu?"
reference_solution_path: private/solutions/css-medium-focus-trap-overlay-dim.css
hint_ladder:
  1: "Bir elemanın görsel netliğini dağıtıp puslu hale getiren CSS filtresi nedir?"
  2: "Modal açıkken arka sayfayı pasifleştirmek için hangi filtre kombinasyonu yazılır?"
  3: "Bu görsel odak tekniği 'arka plan susturma bulanıklığı (focus overlay blur)' olarak bilinir."
```

---

### css-medium-text-wrap-balance-headlines

```yaml
id: css-medium-text-wrap-balance-headlines
version: 1
language: css
engine: none
difficulty: medium
title: "Başlıklarda tek kalan yetim kelimeleri önleme"
prompt: |
  Büyük bir gazete başlığında ilk satır dopdolu iken, ikinci satıra yalnızca tek bir kelime
  düşmekte (yetim kelime / typographic orphan) ve çirkin bir boşluk yaratmaktadır.
  Modern tarayıcıların başlık satırlarını dengeli iki eşit parçaya bölmesini sağlayan modern
  metin sarma dengeleme özelliğini tanımlayın.
constraints:
  - "Başlık satırlarının kelime uzunlukları otomatik dengelenmeli"
  - "Son satırda tek kelime kalması engellenmeli"
concept_tags: [typography, responsive]
checklist_extra:
  - "text-wrap: balance kuralı tanımlanmış mı?"
  - "Gövde metinleri yerine performans açısından sadece başlıklara mı uygulanmış?"
reference_solution_path: private/solutions/css-medium-text-wrap-balance-headlines.css
hint_ladder:
  1: "Başlıklardaki satır uzunluklarını birbirine eşitleyip yetim kelimeyi önleyen yeni özellik nedir?"
  2: "text-wrap özelliğine dengeli dağıtım için hangi değer verilir?"
  3: "Bu modern tipografi standardı 'metin satır dengelemesi (text-wrap: balance)' olarak bilinir."
```

---

### css-medium-color-mix-functional-shades

```yaml
id: css-medium-color-mix-functional-shades
version: 1
language: css
engine: none
difficulty: medium
title: "Modern renk karıştırma fonksiyonu ile dinamik ton üretme"
prompt: |
  Tasarım sisteminizdeki ana marka renginden (`var(--brand)`) otomatik olarak yüzde 15 siyah
  karıştırılmış bir `:hover` rengi ve yüzde 90 beyaz karıştırılmış açık bir arka plan rengi
  türetmek istiyorsunuz. Yeni renk kodları uydurmak yerine, modern CSS yerel renk karıştırma
  fonksiyonunu kullanarak dinamik renk varyasyonları oluşturun.
constraints:
  - "`color-mix()` fonksiyonu kullanılmalı"
  - "Renk uzayı olarak `in srgb` tanımlanmalı"
  - "Mevcut bir değişkenden yüzdelik karışımla yeni ton üretilmeli"
concept_tags: [color, variables]
checklist_extra:
  - "color-mix(in srgb, var(--brand), black 15%) sözdizimi doğru mu?"
  - "Renk uzayı parametresi unutulmamış mı?"
reference_solution_path: private/solutions/css-medium-color-mix-functional-shades.css
hint_ladder:
  1: "CSS'te iki rengi belirli yüzdelerle birbirine katan yerel fonksiyon nedir?"
  2: "color-mix fonksiyonunda ilk parametre olarak hangi renk uzayı belirtilir?"
  3: "Bu yeni nesil renk standardı 'CSS renk karıştırma fonksiyonu (color-mix)' olarak bilinir."
```

---

### css-medium-initial-letter-drop-cap

```yaml
id: css-medium-initial-letter-drop-cap
version: 1
language: css
engine: none
difficulty: medium
title: "Roman ve dergi tarzı büyük başlangıç harfi"
prompt: |
  Bir edebi dergi makalesinin ilk paragrafındaki ilk harfin, 3 satır yüksekliğinde devasa bir
  başlangıç harfi (drop-cap) olarak basılmasını ve sonraki satırların bu harfin etrafından
  akmasını istiyorsunuz. Eski float hileleri yerine, modern CSS başlangıç harfi özelliğini
  `::first-letter` sözde elemanı üzerinde uygulayın.
constraints:
  - "`::first-letter` sözde elemanı hedeflenmeli"
  - "Harf 3 satır yüksekliğini kaplayacak şekilde boyutlandırılmalı"
concept_tags: [typography, layout]
checklist_extra:
  - "initial-letter: 3 veya -webkit-initial-letter kullanılmış mı?"
  - "Eski float hileleri yerine modern özellik tercih edilmiş mi?"
reference_solution_path: private/solutions/css-medium-initial-letter-drop-cap.css
hint_ladder:
  1: "İlk harfin kaç satır büyüklüğünde olacağını belirten modern CSS özelliği nedir?"
  2: "Paragrafın ilk harfini seçen sözde eleman hangisidir?"
  3: "Bu edebi tipografi standardı 'büyük başlangıç harfi (initial-letter drop-cap)' olarak bilinir."
```

---

### css-medium-scroll-driven-header-shrink

```yaml
id: css-medium-scroll-driven-header-shrink
version: 1
language: css
engine: none
difficulty: medium
title: "Sayfa kaydırıldıkça küçülen dinamik başlık"
prompt: |
  Kullanıcı sayfayı aşağı kaydırmaya başladığı anda, sabit üst başlığın yüksekliğinin
  100 pikselden 60 piksele inmesini ve arka planının hafifçe bulanıklaşıp gölge kazanmasını
  istiyorsunuz. Bu etkileşimi tek bir satır JavaScript yazmadan, sayfa kaydırma aralığına
  bağlanan CSS kaydırma zaman çizelgesi animasyonu ile gerçekleştirin.
constraints:
  - "Animasyon sayfa kaydırma mesafesine (`scroll()`) bağlanmalı"
  - "Başlık yüksekliği veya iç dolgusu kaydırmayla birlikte küçülmeli"
concept_tags: [animation, positioning]
checklist_extra:
  - "animation-timeline: scroll(root) kullanılmış mı?"
  - "Kaydırma eşiğine göre yükseklik değişimi yumuşak mı?"
reference_solution_path: private/solutions/css-medium-scroll-driven-header-shrink.css
hint_ladder:
  1: "Bir başlığı sayfa kaydırmasıyla orantılı küçültmek için hangi modern animasyon özelliği kullanılır?"
  2: "animation-range veya keyframes ile kaydırma mesafesi nasıl eşleştirilir?"
  3: "Bu dinamik başlık 'kaydırma kontrollü küçülen başlık (scroll-driven shrinking header)' olarak bilinir."
```

---

## 4. Zor (Hard) — 50 Soru

### css-hard-registered-property-gradient-animation

```yaml
id: css-hard-registered-property-gradient-animation
version: 1
language: css
engine: none
difficulty: hard
title: "Kayıtlı özel özellik ile pürüzsüz degrade renk animasyonu"
prompt: |
  Normalde CSS'te `background-image: linear-gradient(...)` özellikleri doğrudan animasyona
  sokulamaz; renkler arasında yumuşak geçiş yapılamaz ve tarayıcı küt geçiş yapar. Modern CSS
  Houdini `@property` kuralını kullanarak, açıyı veya renk durağı yüzdesini resmi olarak tip
  güvenlikli (`<angle>` veya `<percentage>`) bir CSS değişkeni olarak tarayıcıya tescil edin
  ve bu değişken üzerinden pürüzsüzce dönen bir degrade animasyonu inşa edin.
constraints:
  - "`@property` yönergesi ile tür sözdizimi (`syntax`) tanımlanmalı"
  - "`inherits` ve `initial-value` parametreleri eksiksiz girilmeli"
  - "`@keyframes` ile tescillenen bu özel değişken üzerinden akıcı animasyon çalıştırılmalı"
concept_tags: [variables, animation, performance]
checklist_extra:
  - "@property bloğunda syntax: '<angle>' veya '<percentage>' tanımlanmış mı?"
  - "Animasyon doğrudan gradient yerine tescilli değişkene mi uygulanmış?"
reference_solution_path: private/solutions/css-hard-registered-property-gradient-animation.css
hint_ladder:
  1: "CSS değişkenlerine veri türü atayarak animasyona sokulabilmelerini sağlayan Houdini kuralı nedir?"
  2: "Degrade açısını veya rengini canlandırmak için @property kuralında hangi syntax tipi kullanılır?"
  3: "Bu ileri düzey animasyon standardı 'tescilli CSS özelliği animasyonu (@property gradient)' olarak bilinir."
```

---

### css-hard-view-transitions-hero-morph

```yaml
id: css-hard-view-transitions-hero-morph
version: 1
language: css
engine: none
difficulty: hard
title: "Görsel geçiş API'si ile karttan tam ekrana dönüşüm"
prompt: |
  Kullanıcı bir ürün kartına tıkladığında, karttaki küçük fotoğrafın detay sayfasındaki
  devasa kahraman (hero) afişine pürüzsüzce büyüyerek dönüşmesini (morphing) istiyorsunuz.
  Modern Görünüm Geçişleri (View Transitions API) standardının CSS tarafındaki `view-transition-name`
  özelliğini kullanarak, iki farklı sayfadaki iki bağımsız görseli birbirine bağlayan ve
  aralarındaki büyüme geçişini özelleştiren CSS kurallarını yazın.
constraints:
  - "Her iki durumdaki ilgili elemana benzersiz `view-transition-name` atanmalı"
  - "`::view-transition-old` ve `::view-transition-new` sözde elemanları üzerinden animasyon süresi özelleştirilmeli"
  - "Geçiş donanım hızlandırmalı transform akıcılığında olmalı"
concept_tags: [animation, performance]
checklist_extra:
  - "view-transition-name değeri benzersiz bir kimlik olarak tanımlanmış mı?"
  - "Eski ve yeni durum sözde elemanları doğru hedeflenmiş mi?"
reference_solution_path: private/solutions/css-hard-view-transitions-hero-morph.css
hint_ladder:
  1: "Sayfalar veya durumlar arası eleman dönüşümlerini sağlayan yeni web standardı özelliği nedir?"
  2: "İki elemanın aynı görsel parça olduğunu tarayıcıya bildiren geçiş adı özelliği hangisidir?"
  3: "Bu yeni nesil geçiş teknolojisi 'görünüm geçişleri adı eşleştirmesi (view-transition-name)' olarak bilinir."
```

---

### css-hard-trigonometric-circular-menu

```yaml
id: css-hard-trigonometric-circular-menu
version: 1
language: css
engine: none
difficulty: hard
title: "Trigonometrik fonksiyonlarla dairesel saat menüsü"
prompt: |
  Bir akıllı saat veya oyun arayüzünde, merkezdeki düğmenin etrafında tam bir çember oluşturacak
  şekilde 8 adet menü butonunu radyal olarak dizin. Butonları tek tek elle piksel hesaplayarak
  değil; modern CSS matematik fonksiyonları olan `cos()` ve `sin()` yardımıyla, her butonun
  açısına göre (`calc(cos(var(--aci)) * var(--yaricap))`) kusursuz bir çember rotasına
  oturtan matematiksel mizanpajı kurun.
constraints:
  - "`cos()` ve `sin()` yerel trigonometri fonksiyonları kullanılmalı"
  - "Açı ve yarıçap değişkenlerle dinamik hesaplanmalı"
  - "Elemanlar çember yayında eşit açılarla (45 derece adımlarla) dağıtılmalı"
concept_tags: [layout, centering, variables]
checklist_extra:
  - "Trigonometrik fonksiyonlar transform: translate(...) içinde doğru kullanılmış mı?"
  - "Açı birimleri deg veya rad cinsinden formüle edilmiş mi?"
reference_solution_path: private/solutions/css-hard-trigonometric-circular-menu.css
hint_ladder:
  1: "CSS'te dairesel koordinat hesaplamayı sağlayan matematiksel fonksiyon ikilisi nedir?"
  2: "X ve Y ekseni konumlarını çember yayında hesaplamak için cos ve sin nasıl birleştirilir?"
  3: "Bu ileri düzey matematiksel mizanpaj 'CSS trigonometrik dairesel yerleşim (cos ve sin)' olarak bilinir."
```

---

### css-hard-forced-colors-high-contrast

```yaml
id: css-hard-forced-colors-high-contrast
version: 1
language: css
engine: none
difficulty: hard
title: "Windows yüksek karşıtlık modunda sistem renklerine uyum"
prompt: |
  Az gören kullanıcılar Windows Yüksek Karşıtlık Modunu (High Contrast Mode) açtığında,
  web sitenizdeki özel kart kenarlıkları, renkli rozetler ve butonlar görünmez hale gelebilir.
  `@media (forced-colors: active)` medya özelliğini dinleyerek; sistemin zorunlu renk paletine
  saygı duyan, buton ve odak göstergelerini işletim sisteminin `ButtonText`, `Highlight` ve
  `CanvasText` sistem renkleriyle yeniden çizdiren tam erişilebilir kural kümesini yazın.
constraints:
  - "`@media (forced-colors: active)` medya bloğu kullanılmalı"
  - "Görünmez olan kenarlıklar `CanvasText` veya `Highlight` sistem renkleriyle çizilmeli"
  - "Gerektiğinde `forced-color-adjust: none` kuralı yalnızca kritik simgeler için kontrollü kullanılmalı"
concept_tags: [accessibility, color]
checklist_extra:
  - "forced-colors: active medya özelliği doğru kurgulanmış mı?"
  - "Sistem renk anahtar kelimeleri (ButtonText, Canvas vb.) kullanılmış mı?"
reference_solution_path: private/solutions/css-hard-forced-colors-high-contrast.css
hint_ladder:
  1: "İşletim sisteminin yüksek karşıtlık modunu algılayan standart CSS medya sorgusu nedir?"
  2: "Bu modda renk atamak için kullanılan işletim sistemi renk değişkenlerine ne ad verilir?"
  3: "Bu kritik erişilebilirlik standardı 'zorunlu renkler yüksek karşıtlık uyumu (forced-colors mode)' olarak bilinir."
```

---

### css-hard-composite-only-performance-optimizations

```yaml
id: css-hard-composite-only-performance-optimizations
version: 1
language: css
engine: none
difficulty: hard
title: "Sıfır yeniden çizim maliyetli 60 FPS mikro animasyon"
prompt: |
  Kullanıcı bir kartın üzerine geldiğinde veya bir paneli sürüklediğinde, tarayıcının Yeniden
  Düzenleme (Layout / Reflow) ve Yeniden Boyama (Paint) aşamalarını tetiklemesini kesinlikle
  engellemelisiniz. Yalnızca GPU Kompozit (Composite-only) katmanında çalışan özellikleri
  kullanarak, `will-change` bildirimini doğru yaşam döngüsüyle bağlayan ve düşük donanımlı
  mobil cihazlarda dahi takılmadan 60 FPS çalışan kart animasyonunu yazın.
constraints:
  - "Animasyon yalnızca `transform` ve `opacity` özellikleri üzerinden yürütülmeli"
  - "`top`, `left`, `width`, `height`, `margin` gibi Layout tetikleyici özellikler kesinlikle canlandırılmamalı"
  - "GPU katman hazırlığı için `will-change` doğru özelliklerle tanımlanmalı"
concept_tags: [performance, animation]
checklist_extra:
  - "Yalnızca donanım hızlandırmalı composite özellikleri mi kullanılmış?"
  - "will-change aşırıya kaçmadan hedeflenen özelliklerle mi sınırlandırılmış?"
reference_solution_path: private/solutions/css-hard-composite-only-performance-optimizations.css
hint_ladder:
  1: "Tarayıcıda layout ve paint aşamalarını atlayıp doğrudan GPU'da çalışan iki özellik nedir?"
  2: "Tarayıcıya bir elemanın yakında hareket edeceğini önceden bildiren optimizasyon özelliği hangisidir?"
  3: "Bu performans mühendisliği kuralı 'kompozit katmanı animasyon optimizasyonu (composite-only will-change)' olarak bilinir."
```

---

### css-hard-container-style-queries

```yaml
id: css-hard-container-style-queries
version: 1
language: css
engine: none
difficulty: hard
title: "Kapsayıcı stil sorguları ile akıllı tema adaptasyonu"
prompt: |
  Bir kart bileşeninin, içine düştüğü ebeveyn bölümün CSS değişkeni değerine göre stilini
  otomatik değiştirmesini istiyorsunuz. Boyut sorgularından farklı olarak, modern CSS
  Kapsayıcı Stil Sorguları (`@container style(...)`) standardını kullanarak; ebeveynde
  `--tema: premium` tanımlıysa kartın altın yaldızlı çerçeveye bürünmesini sağlayan
  yeni nesil stil sorgusu kuralını yazın.
constraints:
  - "`@container style(--degisken: deger)` sözdizimi kullanılmalı"
  - "Bileşen ebeveynin değişken durumuna göre stillenmeli"
concept_tags: [variables, maintainability]
checklist_extra:
  - "@container style(...) fonksiyonu doğru yapılandırılmış mı?"
  - "Boyut sorgusu ile stil sorgusu arasındaki ayrım gözetilmiş mi?"
reference_solution_path: private/solutions/css-hard-container-style-queries.css
hint_ladder:
  1: "Kapsayıcının genişliğine değil, üzerindeki bir CSS değişkenine göre tetiklenen sorgu nedir?"
  2: "@container sorgusuna stil denetimi eklemek için hangi anahtar kelime yazılır?"
  3: "Bu ileri düzey CSS özelliği 'kapsayıcı stil sorguları (@container style queries)' olarak bilinir."
```

---

### css-hard-scroll-driven-view-timeline-reveal

```yaml
id: css-hard-scroll-driven-view-timeline-reveal
version: 1
language: css
engine: none
difficulty: hard
title: "Görüş alanına girdikçe beliren kaydırma animasyonu"
prompt: |
  Bir açılış sayfasında aşağı doğru inildikçe, her bir ürün kartının ekranın altına girdiği
  anda şeffaf ve küçük başlayıp, ekranın ortasına ulaştığında tam boyutuna ve tam opaklığına
  ulaşmasını istiyorsunuz. IntersectionObserver JavaScript API'sine ihtiyaç duymadan,
  tamamen CSS Görüş Alanı Zaman Çizelgesi (`view-timeline`) ve `animation-range` özelliklerini
  kullanarak bu girişi canlandırın.
constraints:
  - "`view-timeline` veya yerel `view()` fonksiyonu kullanılmalı"
  - "`animation-range: entry` veya `cover` aralığı tanımlanmalı"
  - "Sayfa kaydırmasıyla birebir senkronize çalışan transform ve opacity animasyonu kurulmalı"
concept_tags: [animation, performance]
checklist_extra:
  - "animation-timeline: view() veya adlandırılmış view-timeline kullanılmış mı?"
  - "Görüş alanına giriş eşiği animation-range ile sınırlandırılmış mı?"
reference_solution_path: private/solutions/css-hard-scroll-driven-view-timeline-reveal.css
hint_ladder:
  1: "Bir elemanın tam olarak ekrana girdiği anı takip eden CSS kaydırma zaman çizelgesi nedir?"
  2: "Animasyonun eleman ekranın altından girerken başlayıp bitmesini sağlayan aralık kuralı nedir?"
  3: "Bu modern animasyon standardı 'görüş alanı zaman çizelgesi (view-timeline ve animation-range)' olarak bilinir."
```

---

### css-hard-subgrid-nested-data-alignment

```yaml
id: css-hard-subgrid-nested-data-alignment
version: 1
language: css
engine: none
difficulty: hard
title: "İç içe geçmiş form alanlarında iki boyutlu alt ızgara senkronizasyonu"
prompt: |
  İç içe geçmiş alan grupları (`<fieldset>` içinde alt `<fieldset>`) içeren karmaşık bir
  kurumsal kayıt formunda, tüm etiketlerin (`<label>`) ve girdi kutularının (`<input>`),
  hangi derinlikte olursa olsun en dıştaki ana ızgaranın sütun çizgilerine kusursuz şekilde
  oturmasını istiyorsunuz. Hem yatay hem dikey sütunları alt basamaklara kesintisiz aktaran
  çift yönlü Subgrid mimarisini uygulayın.
constraints:
  - "Üst form kapsayıcısında çok sütunlu CSS Grid kurulmalı"
  - "Alt alan gruplarında `grid-template-columns: subgrid` kullanılmalı"
  - "Farklı hiyerarşideki etiketlerin sol ve sağ sınırları pikseli pikseline hizalanmalı"
concept_tags: [layout, focus]
checklist_extra:
  - "grid-template-columns: subgrid kuralı iç içe fieldset elemanlarına aktarılmış mı?"
  - "Derin hiyerarşide mizanpaj sapması önlenmiş mi?"
reference_solution_path: private/solutions/css-hard-subgrid-nested-data-alignment.css
hint_ladder:
  1: "İç içe elemanların ebeveyn sütun çizgilerini aynen kullanmasını sağlayan özellik nedir?"
  2: "Sütun genişliklerini en dış formdan miras almak için subgrid nereye yazılır?"
  3: "Bu mimari form hizalaması 'iç içe alt ızgara senkronizasyonu (nested subgrid)' olarak bilinir."
```

---

### css-hard-mobile-dynamic-viewport-units

```yaml
id: css-hard-mobile-dynamic-viewport-units
version: 1
language: css
engine: none
difficulty: hard
title: "Mobil adres çubuğu açılıp kapandığında düzen zıplamasını önleme"
prompt: |
  Mobil Safari ve Chrome'da kullanıcı sayfayı kaydırdıkça tarayıcının üst ve alt adres çubukları
  küçülmekte veya kaybolmaktadır. Klasik `100vh` kullanıldığında, altbilgi butonları adres
  çubuğunun arkasında kalmakta veya zıplama yapmaktadır. Dinamik ekran yüksekliği (`dvh`),
  küçük ekran yüksekliği (`svh`) ve büyük ekran yüksekliği (`lvh`) birimlerini duruma uygun
  kullanarak, mobil ekranlarda kusursuz sabit ekran yüksekliği dengesini kurun.
constraints:
  - "Klasik vh yerine yeni nesil dinamik görünür alan birimleri (`dvh` veya `svh`) kullanılmalı"
  - "Mobil adres çubuğu hareketlerinde sayfa içeriğinin butonları ezmesi önlenmeli"
concept_tags: [responsive, edge-cases]
checklist_extra:
  - "100dvh veya 100svh birimi doğru seçilmiş mi?"
  - "Eski tarayıcılar için yedek 100vh kuralı düşünülmüş mü?"
reference_solution_path: private/solutions/css-hard-mobile-dynamic-viewport-units.css
hint_ladder:
  1: "Mobil tarayıcılarda adres çubuğunun değişimini anlık hesaba katan dinamik ekran birimi nedir?"
  2: "En küçük ve en büyük ekran yüksekliklerini temsil eden svh ve lvh ne anlama gelir?"
  3: "Bu mobil mizanpaj standardı 'dinamik görünür alan birimleri (dynamic viewport units dvh)' olarak bilinir."
```

---

### css-hard-svg-clipping-path-complex-mask

```yaml
id: css-hard-svg-clipping-path-complex-mask
version: 1
language: css
engine: none
difficulty: hard
title: "Vektörel SVG yolu ile karmaşık organik görsel maskeleme"
prompt: |
  Bir yaratıcı ajans sitesinde, dikdörtgen bir tanıtım videosunu standart geometrik şekillerle
  değil; tasarımcının çizdiği organik, dalgalı ve sıvımsı (blob) bir SVG kırpma yoluyla
  kesmek istiyorsunuz. Sayfadaki inline SVG içinde yer alan `<clipPath id="sivi-maske">`
  yolunu CSS `clip-path` özelliği ile video elemanına bağlayarak duyarlı vektörel maskelemeyi uygulayın.
constraints:
  - "CSS `clip-path` özelliği `url(#id)` sözdizimiyle vektörel yola bağlanmalı"
  - "Görsel veya video ekran boyutu değiştikçe maske sınırlarına uyum sağlamalı"
concept_tags: [performance, layout]
checklist_extra:
  - "clip-path: url(#sivi-maske) sözdizimi doğru bağlanmış mı?"
  - "SVG clipPathUnits='objectBoundingBox' uyumu gözetilmiş mi?"
reference_solution_path: private/solutions/css-hard-svg-clipping-path-complex-mask.css
hint_ladder:
  1: "CSS ile bir elemanı harici bir SVG kırpma yoluna bağlamak için hangi fonksiyon yazılır?"
  2: "clip-path özelliğine bir SVG kimliği nasıl referans verilir?"
  3: "Bu gelişmiş maskeleme 'SVG referanslı kırpma yolu (clip-path url mask)' olarak bilinir."
```

---

### css-hard-specificity-layer-migration

```yaml
id: css-hard-specificity-layer-migration
version: 1
language: css
engine: none
difficulty: hard
title: "Ünlem işaretli kuralları sıfırlayarak katmanlı mimariye göç"
prompt: |
  Eski bir kod tabanında her yere `!important` serpiştirilmiş ve yeni stiller eklenemez hale
  gelmiştir. Tüm `!important` ifadelerini temizleyin; CSS Basamak Katmanları (`@layer`) mimarisini
  kullanarak sırasıyla üçüncü taraf kütüphaneyi, ana tema stillerini ve özel bileşenleri
  kendi katmanlarına ayırın; hiçbir özgüllük savaşına girmeden en spesifik kuralın en üst
  katmandan gelmesini sağlayın.
constraints:
  - "Hiçbir `!important` ifadesi kullanılmamalı"
  - "`@layer` hiyerarşisi ile stil öncelikleri mimari olarak çözülmeli"
  - "Seçici özgüllük puanları yerine katman sırası belirleyici olmalı"
concept_tags: [specificity, maintainability]
checklist_extra:
  - "Tüm !important ifadeleri temizlenmiş mi?"
  - "Katman öncelik sırası doğru kurgulanmış mı?"
reference_solution_path: private/solutions/css-hard-specificity-layer-migration.css
hint_ladder:
  1: "CSS'te !important kullanımını tamamen gereksiz kılan modern mimari özellik nedir?"
  2: "Katmanların hangisinin üstün geleceğini belirleyen kural sırası nasıl yazılır?"
  3: "Bu mimari refaktör 'basamak katmanları ile özgüllük yönetimi (@layer refactoring)' olarak bilinir."
```

---

### css-hard-parallax-scroll-pure-css

```yaml
id: css-hard-parallax-scroll-pure-css
version: 1
language: css
engine: none
difficulty: hard
title: "Saf CSS 3D derinlik ile sıfır gecikmeli paralaks kaydırma"
prompt: |
  JavaScript scroll olaylarının sebep olduğu titreme ve gecikmeler olmadan, tamamen CSS
  3D dönüşüm ve perspektif matematiğini kullanarak bir paralaks kaydırma (parallax scrolling)
  sahnesi inşa edin. Kapsayıcıya `perspective` verin; arka plan görselini Z ekseninde geriye
  itip (`translateZ(-1px)`) ölçekleyerek ön plandaki metinlerin arkasındaki resimden daha
  hızlı akmasını sağlayın.
constraints:
  - "JavaScript kullanılmadan tamamen CSS 3D ile çözülmeli"
  - "Kapsayıcıda `perspective` ve `overflow-y: auto` tanımlanmalı"
  - "Paralaks katmanı `translateZ` ve `scale` dengesiyle kurulmalı"
concept_tags: [positioning, animation, performance]
checklist_extra:
  - "perspective ve transform: translateZ(-1px) scale(2) dengesi kurulmuş mu?"
  - "Tarayıcının kaydırma performansı GPU hızlandırmasında mı?"
reference_solution_path: private/solutions/css-hard-parallax-scroll-pure-css.css
hint_ladder:
  1: "Saf CSS ile paralaks derinliği oluşturmak için hangi 3D dönüşüm özelliği kullanılır?"
  2: "Bir nesneyi Z ekseninde geriye ittiğimizde küçülmesini engellemek için ne ile dengeleriz?"
  3: "Bu performanslı görsel efekt 'saf CSS 3D paralaks kaydırma (pure CSS 3D parallax)' olarak bilinir."
```

---

### css-hard-sprite-sheet-character-animation

```yaml
id: css-hard-sprite-sheet-character-animation
version: 1
language: css
engine: none
difficulty: hard
title: "Oyun karakteri yürüme döngüsü sprite animasyonu"
prompt: |
  Tek bir görsel dosyasında yan yana dizilmiş 8 kareden oluşan bir piksel oyun karakteri
  yürüme şeridi (sprite sheet) bulunmaktadır. Animasyonun kareler arasında bulanık kayma
  yapmadan, tam bir çizgi film veya arcade oyunu gibi küt küt basamaklı adımlarla oynamasını
  sağlayan `steps(8)` zamanlama fonksiyonunu ve arka plan yatay pozisyon animasyonunu yazın.
constraints:
  - "`animation-timing-function: steps(8)` kuralı kullanılmalı"
  - "Arka plan yatay pozisyonu 0'dan eksi toplam genişliğe kadar ötelenmeli"
  - "Kareler arası pürüzsüz geçiş engellenmeli, keskin piksel atlaması sağlanmalı"
concept_tags: [animation, performance]
checklist_extra:
  - "steps(8) zamanlama fonksiyonu tanımlanmış mı?"
  - "Görsel bulanıklığını önlemek için image-rendering: pixelated düşünülmüş mü?"
reference_solution_path: private/solutions/css-hard-sprite-sheet-character-animation.css
hint_ladder:
  1: "Sprite sheet animasyonlarında karelerin birbirine karışmasını önleyen adım fonksiyonu nedir?"
  2: "8 kareli bir animasyonu kare kare oynatmak için timing fonksiyonuna ne yazılır?"
  3: "Bu oyun arayüzü tekniği 'adımlı sprite animasyonu (steps timing sprite animation)' olarak bilinir."
```

---

### css-hard-custom-focus-indicator-forced-colors

```yaml
id: css-hard-custom-focus-indicator-forced-colors
version: 1
language: css
engine: none
difficulty: hard
title: "Yüksek karşıtlık modunda kaybolmayan özel odak göstergesi"
prompt: |
  Gelişmiş bir web portalında butonların odak durumunu özel bir `box-shadow` ve arka plan
  gradyanı ile parlatıyorsunuz. Ancak Windows Yüksek Karşıtlık Modunda işletim sistemi tüm
  box-shadow ve arka plan gradyanlarını tamamen sildiği için buton odaklandığında hiçbir şey
  görünmemektedir. Hem normal modda özel stilinizi koruyan hem de yüksek karşıtlık modunda
  şeffaf bir `outline` hilesiyle sistem odağını zorunlu kılan kuralı kurun.
constraints:
  - "Normal modda görsel gölge ve parlamalar korunmalı"
  - "Yüksek karşıtlık modunda `outline: 2px solid transparent` ile sistem çizgisinin belirmesi sağlanmalı"
  - "Tüm erişilebilirlik standartları garanti altına alınmalı"
concept_tags: [focus, accessibility]
checklist_extra:
  - "outline: 2px solid transparent hilesi uygulanmış mı?"
  - "Forced-colors modunda sistemin outline'ı görünür renge boyaması sağlandı mı?"
reference_solution_path: private/solutions/css-hard-custom-focus-indicator-forced-colors.css
hint_ladder:
  1: "Normal modda şeffaf durup yüksek karşıtlık modunda sistem rengiyle parlayan özellik nedir?"
  2: "box-shadow yerine forced-colors modunda çalışan temel odak çizgisi hangisidir?"
  3: "Bu erişilebilirlik çözümü 'şeffaf dış hat odak güvencesi (transparent outline focus)' olarak bilinir."
```

---

### css-hard-color-contrast-dynamic-palette

```yaml
id: css-hard-color-contrast-dynamic-palette
version: 1
language: css
engine: none
difficulty: hard
title: "Gelişmiş renk uzayı ile algısal olarak eşit renk paleti"
prompt: |
  Geleneksel sRGB ve HSL renk modelleri insan gözünün parlaklık algısını (perceptual uniformity)
  doğru yansıtmaz (örneğin saf mavi ile saf sarı aynı açık değerde bile bambaşka parlaklıkta görünür).
  Modern `oklch()` renk uzayını kullanarak, algısal olarak eşit parlaklık (lightness) ve
  kroma (chroma) değerlerine sahip, insan gözüne kusursuz dengeli gelen 5 farklı renk tonundan
  oluşan modern bir tasarım sistemi paleti oluşturun.
constraints:
  - "`oklch()` renk uzayı fonksiyonu kullanılmalı"
  - "Renklerin algısal parlaklık (L) parametresi sabit tutulmalı"
  - "Yalnızca ton açısı (Hue) değiştirilerek tutarlı palet türetilmeli"
concept_tags: [color, variables]
checklist_extra:
  - "oklch(L C H) sözdizimi doğru parametrelerle kurulmuş mu?"
  - "Algısal parlaklık eşitliği sağlanmış mı?"
reference_solution_path: private/solutions/css-hard-color-contrast-dynamic-palette.css
hint_ladder:
  1: "İnsan gözünün ışık algısına göre tasarlanmış en yeni CSS renk uzayı hangisidir?"
  2: "oklch fonksiyonunda renk tonunu değiştirmek için hangi açı parametresi kullanılır?"
  3: "Bu modern renk standardı 'algısal renk uzayı paleti (OKLCH color space)' olarak bilinir."
```

---

### css-hard-grid-overlapping-hero-layers

```yaml
id: css-hard-grid-overlapping-hero-layers
version: 1
language: css
engine: none
difficulty: hard
title: "CSS Grid ile asimetrik çakışan kahraman katmanları"
prompt: |
  Bir moda dergisi ana sayfasında devasa bir fotoğraf, üzerine binen yarı saydam renkli
  bir metin kutusu ve köşesinde duran yuvarlak bir indirim rozeti bulunmaktadır. Eski
  `position: absolute` hileleri yerine, tüm bu elemanları tek bir CSS Grid içine yerleştirip
  aynı satır ve sütun çizgilerini paylaşmalarını (`grid-column: 2 / 5`, `grid-row: 1 / 3`)
  sağlayarak esnek ve kırılmayan asimetrik bir çakışma mizanpajı kurun.
constraints:
  - "Farklı elemanlar aynı ızgara hücre çizgilerini paylaşmalı"
  - "`position: absolute` kullanılmadan CSS Grid üst üste binmesi sağlanmalı"
  - "Katman derinliği için z-index yönetilmeli"
concept_tags: [layout, stacking-context]
checklist_extra:
  - "Birden fazla eleman aynı grid-column ve grid-row aralığına atanmış mı?"
  - "Mizanpaj responsive esnekliğe uygun mu?"
reference_solution_path: private/solutions/css-hard-grid-overlapping-hero-layers.css
hint_ladder:
  1: "CSS Grid'de birden fazla elemanı üst üste bindirmek için çizgiler nasıl paylaşılır?"
  2: "absolute position kullanmadan katman oluşturmanın ızgara yolu nedir?"
  3: "Bu asimetrik düzenleme 'ızgara hücre çakışması (overlapping grid items)' olarak bilinir."
```

---

### css-hard-nested-sticky-parent-boundary

```yaml
id: css-hard-nested-sticky-parent-boundary
version: 1
language: css
engine: none
difficulty: hard
title: "Kendi bölümünün sonuna kadar yapışık kalıp sonra çözülen yan panel"
prompt: |
  Uzun bir blog makalesinin solunda yer alan sosyal paylaşım butonları şeridi, sayfa kaydırılırken
  tepeye yapışmalıdır (`position: sticky`). Ancak makale bittiğinde ve altındaki yorumlar bölümüne
  geçildiğinde bu şerit aşağı akmaya devam etmemeli; yalnızca makale bölümünün (`<article>`)
  sınırları içinde yapışık kalıp makalenin bittiği alt sınırda takılıp durmalıdır.
constraints:
  - "Yapışkan elemanın yapışma ömrü doğrudan ebeveyn sınırıyla kısıtlanmalı"
  - "Ebeveyn elemanın yüksekliği boyunca yapışık kalıp alt sınırda durması sağlanmalı"
  - "Ebeveynde yapışmayı bozan `overflow: hidden` hatasından kaçınılmalı"
concept_tags: [positioning, edge-cases]
checklist_extra:
  - "Ebeveyn kapsayıcı yapışkan elemandan daha yüksek mi?"
  - "Ebeveynde sticky'yi öldüren overflow kuralları engellenmiş mi?"
reference_solution_path: private/solutions/css-hard-nested-sticky-parent-boundary.css
hint_ladder:
  1: "Bir position: sticky elemanının kayabileceği azami mesafe ne ile sınırlıdır?"
  2: "Ebeveyn kutunun bittiği yerde sticky elemanın durması nasıl gerçekleşir?"
  3: "Bu konumlandırma kuralı 'ebeveyn sınırlı yapışkan mizanpaj (bounded sticky container)' olarak bilinir."
```

---

### css-hard-css-marquee-infinite-ticker

```yaml
id: css-hard-css-marquee-infinite-ticker
version: 1
language: css
engine: none
difficulty: hard
title: "Kesintisiz ve takılmasız sonsuz kayan haber bandı"
prompt: |
  Bir borsa veya spor sitesinin en üstünde duran döviz kurları bandının, soldan sağa doğru
  hiç duraksamadan ve sıçrama yapmadan sonsuz bir döngüde akmasını sağlayın. İki kopya metin
  bloğunu yan yana esnek kutuya koyun; `@keyframes` ile genişliğin tam yüzde 50'si kadar
  (`translateX(-50%)`) kaydırıp anında başa dönen, GPU dostu ve takılmasız sonsuz şeridi kurun.
constraints:
  - "Sıçrama veya boşluk oluşmadan kesintisiz sonsuz döngü kurulmalı"
  - "Dönüşüm yalnızca `transform: translateX` ile donanım hızlandırmalı yapılmalı"
  - "Kullanıcı fareyle üzerine geldiğinde akış duraklatılabilmeli (`animation-play-state: paused`)"
concept_tags: [animation, performance]
checklist_extra:
  - "translateX(-50%) matematiği ile kusursuz döngü sağlanmış mı?"
  - "Hover anında animation-play-state: paused kuralı eklenmiş mi?"
reference_solution_path: private/solutions/css-hard-css-marquee-infinite-ticker.css
hint_ladder:
  1: "Kayan şeridin dikişsiz sonsuz döngü yapması için genişliğin yüzde kaçı kaydırılmalıdır?"
  2: "Kullanıcı okurken kayan bandı duraklatmak için hangi CSS özelliği kullanılır?"
  3: "Bu dinamik bileşen 'kesintisiz kayan haber bandı (infinite marquee ticker)' olarak bilinir."
```

---

### css-hard-fluid-modular-scale-ratio

```yaml
id: css-hard-fluid-modular-scale-ratio
version: 1
language: css
engine: none
difficulty: hard
title: "Matematiksel modüler oranlı akışkan tipografi sistemi"
prompt: |
  Bir tasarım sisteminde tüm başlıkların (`h1`, `h2`, `h3`, `h4`) ve gövde metinlerinin
  altın oran veya gümüş oran gibi matematiksel bir modüler ölçek çarpanı (`--ratio: 1.25`)
  üzerinden türetilmesini istiyorsunuz. Kök değişkende tanımlanan taban boyut ve oran üzerinden,
  CSS `calc()` ve `pow()` fonksiyonlarını kullanarak her başlık seviyesinin boyutunu
  otomatik hesaplayan modüler tipografi motorunu yazın.
constraints:
  - "Tipografi ölçeği CSS değişkenleri ve matematik fonksiyonlarıyla hesaplanmalı"
  - "Her başlık boyutu taban boyut ve oranın kuvveti olarak türetilmeli"
concept_tags: [typography, variables]
checklist_extra:
  - "calc() içinde oran çarpanları doğru formüle edilmiş mi?"
  - "Başlık hiyerarşisi matematiksel olarak tutarlı mı?"
reference_solution_path: private/solutions/css-hard-fluid-modular-scale-ratio.css
hint_ladder:
  1: "Başlık boyutlarını bir oranın katları şeklinde türetme metodolojisine ne ad verilir?"
  2: "CSS değişkenleriyle taban boyut ve oran nasıl matematiksel olarak birleştirilir?"
  3: "Bu tipografi mimarisi 'modüler ölçekli tipografi motoru (modular scale typography)' olarak bilinir."
```

---

### css-hard-interactive-card-3d-tilt-lighting

```yaml
id: css-hard-interactive-card-3d-tilt-lighting
version: 1
language: css
engine: none
difficulty: hard
title: "3D dinamik eğim ve fare takip eden parlama yansıması"
prompt: |
  Apple TV kartlarındaki gibi, fare kartın köşelerine yaklaştıkça kartın hafifçe o yöne
  doğru 3D eğildiği ve üzerinde dairesel bir ışık parlamasının gezindiği bir mikro etkileşim
  kurgulayın. CSS değişkenleri (`--mouse-x`, `--mouse-y`) üzerinden beslenen `radial-gradient`
  maskesi ve `rotateX`/`rotateY` dönüşümlerini pürüzsüzce birleştiren kart stilini yazın.
constraints:
  - "Kart 3D perspektif alanında açılı olarak dönebilmeli"
  - "Işık parlaması CSS değişkenleriyle konumlanan dairesel degrade ile çizilmeli"
  - "Geçişler GPU hızlandırmalı transform üzerinden yürütülmeli"
concept_tags: [animation, color, positioning]
checklist_extra:
  - "rotateX ve rotateY açıları perspektif içinde dengelenmiş mi?"
  - "Parlama katmanı mix-blend-mode veya saydamlıkla desteklenmiş mi?"
reference_solution_path: private/solutions/css-hard-interactive-card-3d-tilt-lighting.css
hint_ladder:
  1: "Bir elemanı X ve Y eksenlerinde eğerek 3D hissi vermek için hangi transform fonksiyonları kullanılır?"
  2: "Dinamik ışık yansımasını kart üzerinde gezdirmek için hangi degrade fonksiyonu değişkene bağlanır?"
  3: "Bu ileri düzey mikro etkileşim '3D kart eğilme ve dinamik ışık efekti (3D tilt and glare)' olarak bilinir."
```

---

### css-hard-masonry-native-grid-specification

```yaml
id: css-hard-masonry-native-grid-specification
version: 1
language: css
engine: none
difficulty: hard
title: "Gelecek nesil yerel CSS Grid duvar mizanpajı beyanı"
prompt: |
  Geleneksel column-count hileleri yerine, W3C CSS Grid Seviye 3 taslağında yer alan ve
  doğrudan ızgara satırlarını otomatik tuğla gibi ören yerel `grid-template-rows: masonry`
  standardını uygulayın. Bu özelliği destekleyen modern tarayıcılarda doğrudan yerel masonry
  çalıştıran, desteklemeyen tarayıcılarda ise esnek çok sütunlu düzene düşen `@supports`
  kural mimarisini kurun.
constraints:
  - "`@supports (grid-template-rows: masonry)` sorgusu kullanılmalı"
  - "Destekleyen ortamda yerel masonry ızgarası aktifleşmeli"
  - "Desteklemeyen ortam için yedek fallback düzeni sağlanmalı"
concept_tags: [layout, maintainability]
checklist_extra:
  - "grid-template-rows: masonry kuralı doğru şartlandırılmış mı?"
  - "@supports ile özellik algılama başarıyla kurulmuş mu?"
reference_solution_path: private/solutions/css-hard-masonry-native-grid-specification.css
hint_ladder:
  1: "Gelecekte CSS Grid'e doğrudan tuğla duvar mizanpajı ekleyecek olan satır değeri nedir?"
  2: "Bir tarayıcının bu özelliği destekleyip desteklemediğini denetleyen CSS kuralı nedir?"
  3: "Bu yeni nesil mizanpaj kuralı 'yerel ızgara duvar mizanpajı (native grid masonry)' olarak bilinir."
```

---

### css-hard-accessible-accordion-independent-height

```yaml
id: css-hard-accessible-accordion-independent-height
version: 1
language: css
engine: none
difficulty: hard
title: "Bilinmeyen dinamik yükseklikli akordeon paneli açılış geçişi"
prompt: |
  Bir akordeon panelinin içinde 1 satır da metin olabilir, 20 satırlık dev bir tablo da
  olabilir. `max-height: 1000px` gibi sahte hileler animasyon hızını bozmakta ve gecikme
  yaratmaktadır. Modern CSS Grid `grid-template-rows` tekniğini (`0fr` dan `1fr` e geçiş)
  veya `calc-size(auto)` desteğini kullanarak; içeriğin gerçek yüksekliğini bilmeden,
  tamamen doğal yüksekliği kadar pürüzsüz açılıp kapanan kusursuz akordeon stilini kurun.
constraints:
  - "Sabit veya yapay max-height hileleri kullanılmamalı"
  - "CSS Grid `grid-template-rows: 0fr` -> `1fr` animasyonu veya modern geçiş kullanılmalı"
  - "İçerik taşması `overflow: hidden` ile gizlenmeli"
concept_tags: [animation, layout]
checklist_extra:
  - "0fr'dan 1fr'a geçiş transition ile bağlanmış mı?"
  - "İçerik kutusu min-height: 0 kuralına sahip mi?"
reference_solution_path: private/solutions/css-hard-accessible-accordion-independent-height.css
hint_ladder:
  1: "Yüksekliği belirsiz içerikleri pürüzsüz açmanın modern CSS Grid formülü nedir?"
  2: "0fr satır yüksekliğinin sıfırlanabilmesi için içindeki elemana hangi min-height verilmelidir?"
  3: "Bu gelişmiş animasyon deseni 'belirsiz yükseklik ızgara geçişi (grid 0fr-1fr accordion)' olarak bilinir."
```

---

### css-hard-popover-api-backdrop-anchor

```yaml
id: css-hard-popover-api-backdrop-anchor
version: 1
language: css
engine: none
difficulty: hard
title: "Yerel Popover elemanı ve üst katman perde stillendirmesi"
prompt: |
  HTML'in yerleşik Popover API'si ile açılan bir bildirim kutusunu (`popover` öznitelikli)
  ve onun tarayıcının en üst katmanında (Top Layer) yarattığı karartma perdesini (`::backdrop`)
  CSS ile stillendirin. Popover açıldığında üst katmandaki perdenin yumuşakça kararmasını
  ve popover kutusunun `:popover-open` sözde sınıfı üzerinden canlanarak ekrana gelmesini sağlayın.
constraints:
  - "`:popover-open` sözde sınıfı üzerinden açılış stilleri tanımlanmalı"
  - "`::backdrop` sözde elemanı üzerinden arka plan perdesi canlandırılmalı"
  - "En üst katman (Top Layer) z-index bağımsızlığı gözetilmeli"
concept_tags: [positioning, animation]
checklist_extra:
  - ":popover-open sözde sınıfı doğru kullanılmış mı?"
  - "popover::backdrop perdesi canlandırılmış mı?"
reference_solution_path: private/solutions/css-hard-popover-api-backdrop-anchor.css
hint_ladder:
  1: "Yerleşik Popover API'sinde kutunun açık olduğunu gösteren modern sözde sınıf nedir?"
  2: "Popover elemanının arkasındaki karartma perdesini hangi sözde eleman stillendirir?"
  3: "Bu yeni nesil arayüz standardı 'Popover API ve perde stillendirmesi (:popover-open ::backdrop)' olarak bilinir."
```

---

### css-hard-anchor-positioning-dropdown

```yaml
id: css-hard-anchor-positioning-dropdown
version: 1
language: css
engine: none
difficulty: hard
title: "CSS Çapa Konumlandırma API'si ile serbest açılır menü"
prompt: |
  Bir menü butonuna tıklandığında açılan menü kutusunun, DOM ağacında butonun içinde
  olmasına gerek kalmadan (örneğin sayfanın en sonunda `<body>` altında dursa bile),
  modern CSS Çapa Konumlandırma (Anchor Positioning) standardıyla butonun tam altına
  kenetlenmesini sağlayın. Butona `anchor-name`, menüye ise `position-anchor` atayarak bu
  çapa bağlantısını kurun.
constraints:
  - "Tetikleyici butonda `anchor-name: --buton-capasi` tanımlanmalı"
  - "Açılan menüde `position-anchor: --buton-capasi` ile hedef bağlanmalı"
  - "Konumlandırma `anchor(...)` fonksiyonu ile butonun altına kilitlenmeli"
concept_tags: [positioning, maintainability]
checklist_extra:
  - "anchor-name çift tireli bir isimle tescil edilmiş mi?"
  - "position: absolute eleman anchor() fonksiyonuyla mı hizalanmış?"
reference_solution_path: private/solutions/css-hard-anchor-positioning-dropdown.css
hint_ladder:
  1: "DOM'da uzakta duran iki elemanı CSS ile birbirine bağlayıp konumlandıran yeni API nedir?"
  2: "Hedef elemanın alt kenarını referans almak için top özelliğinde hangi fonksiyon çağrılır?"
  3: "Bu devrimsel konumlandırma standardı 'CSS çapa konumlandırması (Anchor Positioning API)' olarak bilinir."
```

---

### css-hard-light-dark-system-ui-sync

```yaml
id: css-hard-light-dark-system-ui-sync
version: 1
language: css
engine: none
difficulty: hard
title: "Modern light-dark fonksiyonu ile deklaratif tema sistemi"
prompt: |
  Medya sorguları veya seçici çoğaltmaları yapmadan, modern CSS `light-dark()` fonksiyonunu
  kullanarak tek satırda hem açık hem koyu renkleri yöneten bir tasarım sistemi kurun.
  Kök elemana `color-scheme: light dark` beyan edin; kart arka planını `light-dark(#ffffff, #0f172a)`
  ve metin rengini `light-dark(#0f172a, #f8fafc)` şeklinde deklaratif olarak tanımlayın.
constraints:
  - "Kök seviyesinde `color-scheme: light dark` tanımlanmalı"
  - "Renkler `light-dark(açıkRenk, koyuRenk)` fonksiyonuyla atanmalı"
  - "Ayrı medya sorgusu yazmadan tarayıcı renk şemasına tam uyum sağlanmalı"
concept_tags: [color, variables]
checklist_extra:
  - "light-dark() fonksiyonu doğru parametrelerle kullanılmış mı?"
  - "color-scheme beyanı kök elemana atanmış mı?"
reference_solution_path: private/solutions/css-hard-light-dark-system-ui-sync.css
hint_ladder:
  1: "CSS'te açık ve koyu tema renklerini tek fonksiyonda virgülle ayıran yeni özellik nedir?"
  2: "light-dark fonksiyonunun çalışabilmesi için sayfada hangi özelliğin açık olması şarttır?"
  3: "Bu yeni nesil renk sistemi 'deklaratif tema fonksiyonu (light-dark color function)' olarak bilinir."
```

---

### css-hard-multi-column-balancing-spans

```yaml
id: css-hard-multi-column-balancing-spans
version: 1
language: css
engine: none
difficulty: hard
title: "Sütunları aşan manşet ve dengeli çoklu sütun sonu"
prompt: |
  Bir dergi makalesi 3 sütunlu metin düzeninde akmaktadır. Makalenin ortasında yer alan
  önemli bir alıntı kutusunun tüm 3 sütunu birden enlemesine kesip boydan boya geçmesini
  (`column-span: all`), ardından alttaki metnin kalan sütunlara dengeli ve eşit yükseklikte
  dağılarak akmasını sağlayan gelişmiş tipografi mizanpajını yazın.
constraints:
  - "Bölüm içinde `column-count: 3` çoklu sütun yapısı kurulmalı"
  - "Araya giren vurgu kutusu `column-span: all` ile tüm sütunları aşmalı"
  - "Sütun bitişleri dengeli yükseklikte kapanmalı"
concept_tags: [typography, layout]
checklist_extra:
  - "column-span: all kuralı uygulanmış mı?"
  - "Sütun akışı manşetin altından sorunsuz devam ediyor mu?"
reference_solution_path: private/solutions/css-hard-multi-column-balancing-spans.css
hint_ladder:
  1: "Çok sütunlu bir metnin ortasındaki bir başlığın tüm sütunları tek satırda yarmasını sağlayan özellik nedir?"
  2: "column-span özelliğine hangi değer verildiğinde eleman tüm sütunları kaplar?"
  3: "Bu gazete mizanpajı 'tüm sütunları aşan başlık düzeni (column-span: all)' olarak bilinir."
```

---

### css-hard-advanced-blend-mode-photo-duotone

```yaml
id: css-hard-advanced-blend-mode-photo-duotone
version: 1
language: css
engine: none
difficulty: hard
title: "Çift tonlu sanatsal albüm kapağı renk filtreleme"
prompt: |
  Spotify tarzı iki tonlu (duotone) sanatsal bir görsel efekti oluşturun. Bir fotoğrafı
  gri tonlamaya (`filter: grayscale(100%)`) çevirin; üzerine binen yarı saydam renkli
  katmanlarla `mix-blend-mode: multiply` ve `mix-blend-mode: screen` harmanlama modlarını
  kullanarak, fotoğrafın açık alanlarını sarıya, koyu alanlarını ise laciverte dönüştüren
  fotoğraf filtreleme mimarisini kurun.
constraints:
  - "Görsel desatüre edilmeli veya gri tonlamaya çekilmeli"
  - "Çift katmanlı karışım modları (`multiply`, `screen` vb.) kullanılmalı"
  - "Fotoğraf iki zıt rengin tonlarıyla sanatsal olarak yeniden renklendirilmeli"
concept_tags: [color, performance]
checklist_extra:
  - "mix-blend-mode veya background-blend-mode doğru uygulanmış mı?"
  - "Duotone renk geçişi net ve sanatsal duruyor mu?"
reference_solution_path: private/solutions/css-hard-advanced-blend-mode-photo-duotone.css
hint_ladder:
  1: "Bir fotoğrafı iki karşıt renk tonuna boyama efektine ne ad verilir?"
  2: "Açık ve koyu pikselleri farklı renk katmanlarıyla harmanlayan CSS özelliği nedir?"
  3: "Bu görsel efekt 'çift tonlu karışım modu filtresi (duotone blend mode)' olarak bilinir."
```

---

### css-hard-smooth-height-interpolate-size

```yaml
id: css-hard-smooth-height-interpolate-size
version: 1
language: css
engine: none
difficulty: hard
title: "Yerel otomatik boyut enterpolasyonu ile sınırsız yükseklik geçişi"
prompt: |
  Yıllardır CSS'in en büyük eksikliği olan `height: 0` dan `height: auto` değerine doğrudan
  geçiş yapılamaması sorunu, modern CSS `interpolate-size: allow-keywords` özelliği ile
  çözülmüştür. Kök düzeyinde veya bileşende bu özelliği açarak, bir kutunun yüksekliğini
  hiçbir ızgara veya JavaScript hilesi olmadan doğrudan sıfırdan `auto` değerine yumuşakça
  açan son teknoloji geçiş kuralını tanımlayın.
constraints:
  - "`interpolate-size: allow-keywords` özelliği tanımlanmalı"
  - "`height` özelliği doğrudan `0` ile `auto` arasında transition ile canlandırılmalı"
  - "Modern web platformu standardına tam uyum sağlanmalı"
concept_tags: [animation, layout]
checklist_extra:
  - "interpolate-size kuralı doğru tanımlanmış mı?"
  - "Doğrudan height: auto geçişi sağlanmış mı?"
reference_solution_path: private/solutions/css-hard-smooth-height-interpolate-size.css
hint_ladder:
  1: "CSS'te auto anahtar kelimesinin animasyonlarda hesaplanmasını sağlayan en yeni özellik nedir?"
  2: "interpolate-size özelliğine hangi değer verildiğinde auto bir sayı gibi enterpole edilir?"
  3: "Bu çığır açan CSS standardı 'otomatik boyut enterpolasyonu (interpolate-size allow-keywords)' olarak bilinir."
```

---

### css-hard-scroll-driven-carousel-dots-sync

```yaml
id: css-hard-scroll-driven-carousel-dots-sync
version: 1
language: css
engine: none
difficulty: hard
title: "Kaydırma konumuna kilitli akıllı sayfalama noktaları"
prompt: |
  Yatay bir fotoğraf kaydırıcısında alt kısımdaki sayfalama noktalarından (dots), o anda
  ekranda hangi fotoğraf duruyorsa o noktanın aktifleşip büyümesini istiyorsunuz. Hiç
  JavaScript kaydırma dinleyicisi yazmadan; her kartın görüş alanına girişini izleyen
  `view-timeline` ve `animation-timeline` kurallarıyla, ilgili navigasyon noktasını
  kaydırmayla eş zamanlı olarak genişleten ve renklendiren saf CSS çözümünü kurun.
constraints:
  - "JavaScript olmadan tamamen kaydırma zaman çizelgesiyle yönetilmeli"
  - "Her fotoğraf kendi `view-timeline` referansına sahip olmalı"
  - "Sayfalama göstergeleri ilgili kartın görünürlük aralığına bağlanmalı"
concept_tags: [animation, positioning]
checklist_extra:
  - "Adlandırılmış view-timeline-name kullanılmış mı?"
  - "Noktalar ilgili zaman çizelgesine bağlanmış mı?"
reference_solution_path: private/solutions/css-hard-scroll-driven-carousel-dots-sync.css
hint_ladder:
  1: "Bir elemanın kaydırma durumunu sayfadaki başka bir göstergeye bağlayan CSS özelliği nedir?"
  2: "view-timeline-name ile isimlendirilen zaman çizelgesi başka bir elemana nasıl bağlanır?"
  3: "Bu gelişmiş etkileşim 'kaydırma zaman çizelgeli sayfalama senkronizasyonu (scroll-driven carousel sync)' olarak bilinir."
```

---

### css-hard-nested-perspective-origami-fold

```yaml
id: css-hard-nested-perspective-origami-fold
version: 1
language: css
engine: none
difficulty: hard
title: "İç içe katlanan origami broşür 3D açılma animasyonu"
prompt: |
  Üç panelli bir basılı broşürün ekranda birbiri ardına katlanarak açıldığı bir 3D origami
  animasyonu inşa edin. Her panelin bir önceki panelin kenarına menteşelenmesi (`transform-origin: left`),
  `preserve-3d` bağlamının çocuklara kesintisiz aktarılması ve panellerin sırayla farklı
  açılardan (eksi 120 dereceden sıfıra) dönerek broşürü tamamlamasını sağlayan hiyerarşik
  3D dönüşüm zincirini kurun.
constraints:
  - "`transform-style: preserve-3d` hiyerarşi boyunca korunmalı"
  - "Dönüş menteşeleri `transform-origin` ile kenarlara kilitlenmeli"
  - "Paneller birbirine göre sırayla açılan 3D dönüşüm açılarına sahip olmalı"
concept_tags: [animation, positioning]
checklist_extra:
  - "transform-origin: left veya right doğru atanmış mı?"
  - "İç içe 3D katmanlar düzleşmeden (flattening olmadan) korunmuş mu?"
reference_solution_path: private/solutions/css-hard-nested-perspective-origami-fold.css
hint_ladder:
  1: "Bir elemanın menteşe gibi belirli bir kenardan dönmesini sağlayan özellik nedir?"
  2: "İç içe 3D elemanların düzleşmesini engelleyen kural hangisidir?"
  3: "Bu karmaşık 3D animasyon 'origami katlanma zinciri (nested preserve-3d origami fold)' olarak bilinir."
```

---

### css-hard-print-multi-page-table-repeating-header

```yaml
id: css-hard-print-multi-page-table-repeating-header
version: 1
language: css
engine: none
difficulty: hard
title: "Çok sayfalı baskıda tablo başlığını her sayfada tekrarlama"
prompt: |
  Bir muhasebe raporu yazıcıya gönderildiğinde 5 sayfa A4 tutmaktadır. Standart ayarlarda
  tablonun başlıkları (`<thead>`) yalnızca ilk sayfada çıkmakta, sonraki sayfalarda kullanıcı
  sütunların ne olduğunu görememektedir. Tablo başlıklarının her basılan sayfanın tepesinde
  otomatik olarak tekrar yazdırılmasını sağlayan ve satırların sayfa sınırında ortadan
  kesilmesini engelleyen profesyonel yazdırma kuralını kurun.
constraints:
  - "`@media print` altında `thead` için sayfa başı tekrarlama kuralı tanımlanmalı"
  - "Tablo satırlarının sayfa sınırında bölünmesi engellenmeli (`break-inside: avoid`)"
  - "Kenar boşlukları `@page` kuralı ile optimize edilmeli"
concept_tags: [responsive, maintainability]
checklist_extra:
  - "thead için display: table-header-group kullanılmış mı?"
  - "tr için break-inside: avoid tanımlanmış mı?"
reference_solution_path: private/solutions/css-hard-print-multi-page-table-repeating-header.css
hint_ladder:
  1: "Baskıda tablo başlığının her sayfanın başında çıkmasını sağlayan display değeri nedir?"
  2: "Yazıcı kenar boşluklarını belirlemek için hangi özel at-rule kullanılır?"
  3: "Bu baskı mimarisi 'tekrarlanan baskı tablo başlığı (print table-header-group @page)' olarak bilinir."
```

---

### css-hard-dynamic-shadow-elevation-system

```yaml
id: css-hard-dynamic-shadow-elevation-system
version: 1
language: css
engine: none
difficulty: hard
title: "Çok katmanlı fiziksel gölge derinlik hiyerarşisi"
prompt: |
  Tek bir sert `box-shadow` yerine, gerçek dünyadaki ortam ışığını (ambient light) ve doğrudan
  ışık kaynağını taklit eden iki katmanlı fiziksel gölge formülü geliştirin. Tasarım sisteminizde
  seviye 1, seviye 2 ve seviye 3 yükseklikler için; biri yayvan ve soluk, diğeri ise yönlü
  ve koyu olan iki gölge katmanını CSS değişkenleriyle birleştiren derinlik sistemini kurun.
constraints:
  - "Her gölge seviyesi en az iki bağımsız gölge katmanından (virgülle ayrılmış) oluşmalı"
  - "Gölge parametreleri CSS değişkenleri üzerinden modüler yönetilmeli"
  - "Doğal fiziksel ışık hissi oluşturulmalı"
concept_tags: [variables, color]
checklist_extra:
  - "İki katmanlı (ortam + yönlü) gölge ayrımı yapılmış mı?"
  - "Gölge derinlikleri mantıksal bir yükseklik hiyerarşisi oluşturuyor mu?"
reference_solution_path: private/solutions/css-hard-dynamic-shadow-elevation-system.css
hint_ladder:
  1: "Gerçekçi gölgeler oluşturmak için box-shadow özelliğine virgülle kaç katman eklenir?"
  2: "Gölgenin biri yayvan ortam ışığı, diğeri yönlü ışık olacak şekilde nasıl dengelenir?"
  3: "Bu tasarım sistemi standardı 'katmanlı fiziksel gölge derinliği (layered elevation shadows)' olarak bilinir."
```

---

### css-hard-text-decoration-thickness-offset

```yaml
id: css-hard-text-decoration-thickness-offset
version: 1
language: css
engine: none
difficulty: hard
title: "Karakter bacaklarını kesmeyen editoryal bağlantı alt çizgisi"
prompt: |
  Geleneksel web sitelerinde bağlantı alt çizgileri 'p', 'y', 'g' gibi harflerin sarkan
  bacaklarının tam üzerinden geçerek çirkin bir karalama görüntüsü yaratır. Modern CSS
  özelliklerini kullanarak; metinden 4 piksel aşağıda duran, 2 piksel kalınlığında,
  harflerin sarkan bacaklarına geldiğinde akıllıca kesilip boşluk bırakan (ink skipping)
  şık bir editoryal alt çizgi stili oluşturun.
constraints:
  - "Alt çizgi mesafesi `text-underline-offset` ile açılmalı"
  - "Çizgi kalınlığı `text-decoration-thickness` ile ayarlanmalı"
  - "Harf bacaklarında çizginin kesilmesi `text-decoration-skip-ink: auto` ile sağlanmalı"
concept_tags: [typography, accessibility]
checklist_extra:
  - "text-underline-offset ve text-decoration-thickness kullanılmış mı?"
  - "text-decoration-skip-ink özelliği tanımlanmış mı?"
reference_solution_path: private/solutions/css-hard-text-decoration-thickness-offset.css
hint_ladder:
  1: "Alt çizginin metne olan mesafesini açan modern CSS özelliği nedir?"
  2: "Alt çizginin harf bacaklarının üstünü çizmesini engelleyen özellik hangisidir?"
  3: "Bu tipografi inceliği 'mürekkep atlamalı alt çizgi (text-underline-offset skip-ink)' olarak bilinir."
```

---

### css-hard-glassmorphism-multi-layer-blur

```yaml
id: css-hard-glassmorphism-multi-layer-blur
version: 1
language: css
engine: none
difficulty: hard
title: "Çok katmanlı ışık yansımalı cam tasarımı"
prompt: |
  Gelişmiş bir 'Glassmorphism' modal penceresi inşa edin. Pencerenin arkasındaki zemini
  bulanıklaştıran `backdrop-filter` kuralının yanı sıra; camın üst kenarından vuran beyaz
  ışık parlamasını temsil eden yarı saydam kenarlık geçişini ve camın kendi yüzeyindeki
  hafif gürültü/doygunluk artışını (`backdrop-filter: saturate(180%) blur(20px)`) birleştiren
  lüks cam bileşeni oluşturun.
constraints:
  - "Çoklu arka plan filtresi (`blur` ve `saturate`) birleştirilmeli"
  - "Cam kenarı ışık yansıması için yarı saydam geçişli kenarlık tanımlanmalı"
  - "Yüksek kontrast ve erişilebilir metin okunabilirliği garanti edilmeli"
concept_tags: [color, layout]
checklist_extra:
  - "backdrop-filter içinde hem blur hem saturate kullanılmış mı?"
  - "Camın kenarlığı saydam beyaz degrade ile aydınlatılmış mı?"
reference_solution_path: private/solutions/css-hard-glassmorphism-multi-layer-blur.css
hint_ladder:
  1: "Buzlu cam tasarımında renklerin solmasını önlemek için blur yanına hangi filtre eklenir?"
  2: "Camın üst köşesindeki parlaklığı vermek için kenarlık nasıl renklendirilir?"
  3: "Bu popüler arayüz stili 'çok katmanlı cam morfolojisi (advanced glassmorphism)' olarak bilinir."
```

---

### css-hard-aspect-ratio-art-direction-grid

```yaml
id: css-hard-aspect-ratio-art-direction-grid
version: 1
language: css
engine: none
difficulty: hard
title: "Katı geometrik oranları koruyan duyarlı fotoğraf mozaiği"
prompt: |
  Bir fotoğraf ajansı için mozaik ızgara tasarlıyorsunuz. İlk fotoğraf devasa bir kare
  (1:1), yanındaki iki fotoğraf yatay dikdörtgen (16:9), altındaki diğer fotoğraflar ise
  dikey portre (3:4) formatında olmalıdır. Ekran boyutu değiştikçe hiçbir fotoğrafın oranının
  bozulmamasını, boşluk bırakmadan birbirine kenetlenmesini sağlayan CSS Grid ve `aspect-ratio`
  mimarisini kurun.
constraints:
  - "Farklı elemanlara özel `aspect-ratio` oranları atanmalı"
  - "Izgarada `grid-auto-flow: dense` ile boşluksuz kenetlenme sağlanmalı"
  - "Görseller `object-fit: cover` ile kutuyu tam doldurmalı"
concept_tags: [layout, responsive]
checklist_extra:
  - "Farklı en-boy oranları doğru elemanlara atanmış mı?"
  - "object-fit: cover ile ezilme engellenmiş mi?"
reference_solution_path: private/solutions/css-hard-aspect-ratio-art-direction-grid.css
hint_ladder:
  1: "Bir ızgaradaki hücrelerin kendi özel geometrik oranlarını korumasını sağlayan özellik nedir?"
  2: "Farklı oranlardaki kartların boşluk bırakmadan oturması için ızgara akışına ne yazılır?"
  3: "Bu medya mizanpajı 'geometrik mozaik ızgara düzeni (aspect-ratio mosaic grid)' olarak bilinir."
```

---

### css-hard-accessible-custom-tabs-keyboard-focus

```yaml
id: css-hard-accessible-custom-tabs-keyboard-focus
version: 1
language: css
engine: none
difficulty: hard
title: "Tam erişilebilir sekmeli içerik gezinme ve odak göstergesi"
prompt: |
  WAI-ARIA tablist standardına göre hazırlanmış üç sekmeli bir içerik alanını stillendirin.
  Seçili sekmenin (`[aria-selected="true"]`) altına hareketli bir mavi gösterge çizgisi
  çekin; klavye ile odaklanıldığında sekmenin etrafında yüksek kontrastlı bir odak halkası
  oluşturun; pasif sekmelerin ise şeffaf ve gri kalarak erişilebilir kontrast sınırını
  korumasını sağlayın.
constraints:
  - "Durum stilleri `[aria-selected='true']` özniteliği üzerinden bağlanmalı"
  - "Klavye odağı `:focus-visible` ile yüksek kontrastlı çizilmeli"
  - "Aktif sekme alt çizgisi veya arka planı pürüzsüz geçişe sahip olmalı"
concept_tags: [focus, accessibility]
checklist_extra:
  - "aria-selected öznitelik seçicisi kullanılmış mı?"
  - "Klavye odağı için belirgin outline sağlanmış mı?"
reference_solution_path: private/solutions/css-hard-accessible-custom-tabs-keyboard-focus.css
hint_ladder:
  1: "Erişilebilir sekmelerde aktif sekmeyi seçmek için hangi ARIA özniteliği kullanılır?"
  2: "Sekmenin seçilme durumunu gösteren alt çizgiyi CSS ile nasıl canlandırırız?"
  3: "Bu bileşen stili 'erişilebilir sekme çubuğu tasarımı (accessible tablist styling)' olarak bilinir."
```

---

### css-hard-dynamic-badge-counter-clamp

```yaml
id: css-hard-dynamic-badge-counter-clamp
version: 1
language: css
engine: none
difficulty: hard
title: "Tek basamakta daire, çift basamakta kapsüle esneyen sayaç"
prompt: |
  Bir sepet veya bildirim sayacı rozeti tek basamaklı bir sayı içerdiğinde (`3` gibi)
  kusursuz bir daire (20x20 piksel) olmalıdır. Sayı iki veya üç basamağa çıktığında (`99+` gibi)
  ise kutu elipsleşmemeli veya bozulmamalı; doğal bir şekilde yatayda genişleyerek kusursuz
  bir kapsül (pill) formuna dönüşmelidir. `min-width` ve yüksek `border-radius` dengesini kurun.
constraints:
  - "Tek karakterde tam dairesel oran korunmalı"
  - "İçerik uzadığında yatayda kapsül şeklinde esnemeli"
  - "İç boşluk ve merkezleme bozulmamalı"
concept_tags: [layout, centering]
checklist_extra:
  - "min-width ve min-height eşitlenmiş mi?"
  - "border-radius: 9999px veya yüzde 50 dengesi kurulmuş mu?"
reference_solution_path: private/solutions/css-hard-dynamic-badge-counter-clamp.css
hint_ladder:
  1: "Bir kutunun tek harfte daire kalıp metin uzadıkça kapsül olmasını sağlayan minimum genişlik kuralı nedir?"
  2: "Kutu içeriği ortalamak için esnek merkezleme nasıl uygulanır?"
  3: "Bu dinamik bileşen 'akıllı esneyen sayaç rozeti (dynamic pill badge)' olarak bilinir."
```

---

### css-hard-css-tree-branch-connector-lines

```yaml
id: css-hard-css-tree-branch-connector-lines
version: 1
language: css
engine: none
difficulty: hard
title: "Organizasyon şeması ağaç dalları bağlantı çizgileri"
prompt: |
  İç içe geçmiş hiyerarşik bir organizasyon şemasında veya dosya ağacında (`<ul>` içinde alt `<ul>`),
  her bir alt elemanın ebeveynine dikey ve yatay gri ince çizgilerle bağlı olduğunu gösteren
  bir ağaç yapısı kurun. Görsel resimler kullanmadan, yalnızca liste maddelerinin `::before`
  ve `::after` sözde elemanlarına kenarlık (`border-left`, `border-bottom`) vererek bu
  organik bağlantı dallarını çizin.
constraints:
  - "Bağlantı çizgileri tamamen CSS sözde elemanları ile oluşturulmalı"
  - "Dikey çizgi ebeveynden inmeli, yatay çizgi alt elemana uzanmalı"
  - "Son çocuğun altından aşağıya doğru taşan fazla çizgi kesilmeli"
concept_tags: [layout, maintainability]
checklist_extra:
  - "::before ve ::after ile dikey ve yatay kenarlıklar çekilmiş mi?"
  - ":last-child seçicisi ile fazla dikey çizgi sıfırlanmış mı?"
reference_solution_path: private/solutions/css-hard-css-tree-branch-connector-lines.css
hint_ladder:
  1: "İç içe listeleri klasör ağacı gibi birbirine bağlayan çizgiler hangi sözde elemanlarla çizilir?"
  2: "Sonuncu elemandan sonra dikey çizginin uzamasını engellemek için ne yapılır?"
  3: "Bu hiyerarşik mizanpaj 'CSS ağaç bağlantı çizgileri (tree view connector lines)' olarak bilinir."
```

---

### css-hard-infinite-canvas-draggable-panning

```yaml
id: css-hard-infinite-canvas-draggable-panning
version: 1
language: css
engine: none
difficulty: hard
title: "Figma tarzı sonsuz noktalı ızgara arka plan deseni"
prompt: |
  Figma veya Miro benzeri sonsuz tuval (infinite canvas) uygulamalarında görülen, 24 piksel
  aralıklarla tekrarlanan gri noktalardan oluşan bir tuval arka planı tasarlayın. Görsel
  dosyası indirmeden; tamamen iki yönlü `radial-gradient` ve `background-size` kullanarak,
  yüksek çözünürlüklü Retina ekranlarda bile bulanıklaşmayan keskin noktalı ızgara desenini kurun.
constraints:
  - "Noktalar dairesel renk geçişi (`radial-gradient`) ile çizilmeli"
  - "`background-size: 24px 24px` ile ızgara döngüsü oluşturulmalı"
  - "Pikseller keskin ve hafif saydam gri renkte olmalı"
concept_tags: [color, performance]
checklist_extra:
  - "radial-gradient(#94a3b8 1px, transparent 1px) deseni kurulmuş mu?"
  - "background-size ile 24px ızgara adımı eşitlenmiş mi?"
reference_solution_path: private/solutions/css-hard-infinite-canvas-draggable-panning.css
hint_ladder:
  1: "CSS'te resim kullanmadan tekrarlayan nokta deseni oluşturmak için hangi degrade kullanılır?"
  2: "Noktaların aralığını belirlemek için hangi arka plan özelliği ayarlanır?"
  3: "Bu tuval deseni 'noktalı ızgara arka plan deseni (dot grid canvas)' olarak bilinir."
```

---

### css-hard-multi-layer-clip-path-reveal

```yaml
id: css-hard-multi-layer-clip-path-reveal
version: 1
language: css
engine: none
difficulty: hard
title: "Geometrik çokgen açılma geçiş animasyonu"
prompt: |
  Yeni bir içerik sahnesi yüklenirken, ekranın ortasından dışarı doğru açılan bir elmas
  veya çokgen formunda bir kırpma yolu animasyonu kurgulayın. `@keyframes` içinde `clip-path: polygon(...)`
  koordinatlarını kapalı bir noktadan tüm ekranı kapsayan devasa bir alana doğru büyüterek,
  sayfanın geometrik bir prizma gibi açılmasını sağlayan dönüşüm kuralını yazın.
constraints:
  - "Açılış animasyonu `clip-path: polygon(...)` üzerinden yürütülmeli"
  - "Başlangıçta koordinatlar merkezde kapalı, sonda tüm ekranı açmalı"
  - "Animasyon süresi ve zamanlaması akıcı olmalı"
concept_tags: [animation, performance]
checklist_extra:
  - "polygon köşe sayısı başlangıç ve bitiş karelerinde eşit tutulmuş mu?"
  - "Donanım hızlandırmalı modern kırpma geçişi sağlanmış mı?"
reference_solution_path: private/solutions/css-hard-multi-layer-clip-path-reveal.css
hint_ladder:
  1: "Bir elemanın geometrik bir maskeyle açılarak belirmesini sağlayan animasyon kuralı nedir?"
  2: "polygon animasyonlarında ara kare geçişinin bozulmaması için nokta sayısı nasıl olmalıdır?"
  3: "Bu sahne geçişi 'çokgen kırpma yoluyla sahne açılışı (clip-path polygon reveal)' olarak bilinir."
```

---

### css-hard-form-field-validation-icons-css

```yaml
id: css-hard-form-field-validation-icons-css
version: 1
language: css
engine: none
difficulty: hard
title: "İstemci tarafı doğrulama durumunda dinamik onay ikonu"
prompt: |
  HTML5 yerel doğrulama kurallarına göre bir girdi kutusu doğru doldurulduğunda (`:valid`),
  kutunun sağ içinde yeşil bir tik işareti belirmeli; geçersiz doldurulduğunda (`:user-invalid`)
  ise kırmızı bir çarpı işareti çıkmalıdır. JavaScript kullanmadan, kutunun durum sözde sınıflarını
  ve arka plan SVG veri şemasını (`background-image: url("data:image/svg+xml...")`) kullanarak
  bu dinamik doğrulama ikonlarını entegre edin.
constraints:
  - "Durumlar `:valid` ve `:user-invalid` sözde sınıfları ile yakalanmalı"
  - "İkonlar arka plan SVG görseli olarak sağa konumlandırılmalı"
  - "Metnin ikonun altına girmemesi için sağ iç boşluk (`padding-right`) bırakılmalı"
concept_tags: [focus, accessibility]
checklist_extra:
  - "Kullanıcı etkileşimi öncesi kırmızı yanmasını önlemek için :user-invalid düşünülmüş mü?"
  - "Sağ iç boşluk ikon genişliği kadar açılmış mı?"
reference_solution_path: private/solutions/css-hard-form-field-validation-icons-css.css
hint_ladder:
  1: "Kullanıcı bir formu hatalı doldurup çıktığında aktifleşen modern doğrulama sözde sınıfı nedir?"
  2: "Girdi kutusunun içine CSS ile vektörel ikon gömmenin en pratik yolu nedir?"
  3: "Bu form etkileşimi 'CSS dinamik girdi doğrulama ikonları (:user-invalid SVG icon)' olarak bilinir."
```

---

### css-hard-curved-text-svg-css-sync

```yaml
id: css-hard-curved-text-svg-css-sync
version: 1
language: css
engine: none
difficulty: hard
title: "Dairesel rozet etrafında dönen dairesel yazı"
prompt: |
  Tasarım ödülü rozetlerinde sıklıkla görülen, bir dairenin yayını takip eden dairesel bir
  yazının kendi merkezi etrafında yavaşça ve kesintisiz döndüğü bir bileşen oluşturun.
  SVG `<textPath>` ile eğriye oturtulmuş metnin CSS `transform: rotate` ve `transform-origin: center`
  animasyonu ile takılmadan sonsuz döngüde dönmesini sağlayan kuralı yazın.
constraints:
  - "Dönüş hareketi tam merkez (`transform-origin: center`) ekseninde olmalı"
  - "Animasyon sonsuz (`infinite`) ve doğrusal (`linear`) zamanlamada dönmeli"
  - "Dairesel yazı okunurluğu korunmalı"
concept_tags: [animation, typography]
checklist_extra:
  - "transform-origin: center tanımlanmış mı?"
  - "SVG metin yolu ile CSS animasyonu uyumlu mu?"
reference_solution_path: private/solutions/css-hard-curved-text-svg-css-sync.css
hint_ladder:
  1: "Dairesel bir metni kendi ortasında döndürmek için transform-origin ne olmalıdır?"
  2: "Yazının kesintisiz dönmesi için hangi animasyon parametreleri eşleştirilir?"
  3: "Bu görsel efekt 'dönen dairesel metin rozeti (rotating curved text badge)' olarak bilinir."
```

---

### css-hard-hardware-accelerated-glow-filter

```yaml
id: css-hard-hardware-accelerated-glow-filter
version: 1
language: css
engine: none
difficulty: hard
title: "GPU dostu titremeyen neon parlama animasyonu"
prompt: |
  Karanlık temalı bir oyunda neon mavi parlayan bir buton tasarlıyorsunuz. `box-shadow`
  ile yapılan parlamalar her karede CPU üzerinde ağır rasterizasyon maliyeti yarattığı için
  mobil cihazlarda pili tüketir ve kasar. Çok katmanlı `drop-shadow` filtresi ve donanım
  hızlandırmalı opaklık geçişleriyle, yüksek performanslı ve akıcı bir neon nefes alma
  (pulse) parlaması inşa edin.
constraints:
  - "Ağır box-shadow animasyonları yerine GPU dostu filtreleme tekniği kullanılmalı"
  - "Parlama `@keyframes` ile nefes alır gibi (pulse) büyüyüp küçülmeli"
  - "Erişilebilirlik için hareket azaltma tercihi kontrol edilmeli"
concept_tags: [animation, performance]
checklist_extra:
  - "filter: drop-shadow(...) tekniği kullanılmış mı?"
  - "Pre-rendered katman opacity ile canlandırılarak performans garanti edilmiş mi?"
reference_solution_path: private/solutions/css-hard-hardware-accelerated-glow-filter.css
hint_ladder:
  1: "Kutu gölgesine göre daha estetik ve alfa şeffaflığına uyan filtreleme gölgesi nedir?"
  2: "Ağır gölge hesaplamalarını her karede çalıştırmak yerine opaklık ile açıp kapama hilesi nedir?"
  3: "Bu görsel performans deseni 'GPU hızlandırmalı neon parlama efekti (hardware-accelerated glow)' olarak bilinir."
```

---

### css-hard-nested-subgrid-financial-statement

```yaml
id: css-hard-nested-subgrid-financial-statement
version: 1
language: css
engine: none
difficulty: hard
title: "Üç kademeli hiyerarşik finansal bilanço alt ızgarası"
prompt: |
  Bir holdingin konsolide mali tablosunda Ana Faaliyet > Bölge > Departman şeklinde 3 kademeli
  iç içe hiyerarşi bulunmaktadır. Her alt seviye HTML'de ayrı bir kapsayıcı blok içinde
  olmasına rağmen; sütun başlıkları (Gelir, Gider, Net Kar, Büyüme Oranı) en dıştaki ana
  ızgara sütunlarıyla pikseli pikseline aynı hizada durmalıdır. Üçüncü seviyeye kadar alt
  ızgara aktarımı sağlayan tam subgrid hiyerarşisini kurun.
constraints:
  - "En dışta ana sütun oranları tanımlanmalı"
  - "Ara seviyelerde ve en alt seviyede `grid-template-columns: subgrid` zinciri kurulmalı"
  - "Farklı girintilere rağmen tüm finansal sütunların dikey çizgileri örtüşmeli"
concept_tags: [layout, maintainability]
checklist_extra:
  - "Subgrid zinciri aradaki ebeveynler atlanmadan aktarılmış mı?"
  - "Tablo hiyerarşisinde sütun sapmaları giderilmiş mi?"
reference_solution_path: private/solutions/css-hard-nested-subgrid-financial-statement.css
hint_ladder:
  1: "İç içe geçmiş birden fazla kutunun en üstteki ızgara çizgilerini paylaşması için ne yapılır?"
  2: "Subgrid kuralı zincirleme olarak alt basamaklara nasıl aktarılır?"
  3: "Bu kurumsal mizanpaj 'üç kademeli alt ızgara zinciri (multi-level subgrid hierarchy)' olarak bilinir."
```

---

### css-hard-contrast-mode-svg-icon-fill

```yaml
id: css-hard-contrast-mode-svg-icon-fill
version: 1
language: css
engine: none
difficulty: hard
title: "Satır içi SVG simgelerinin sistem renkleriyle otomatik uyumu"
prompt: |
  Bir butonun içindeki satır içi SVG simgesinin dolgu rengi (`fill`), normal modda butonun
  metin rengiyle aynı olmalıdır. Kullanıcı işletim sisteminde yüksek karşıtlık moduna geçtiğinde
  veya metin rengi değiştiğinde, SVG simgesinin de hiçbir ek kural yazmadan otomatik olarak
  üst metin rengini miras almasını (`currentColor`) sağlayan renk miras alma kuralını yazın.
constraints:
  - "SVG dolgu ve çizgi özellikleri `currentColor` anahtar kelimesine bağlanmalı"
  - "Üst elemanın metin rengi değiştikçe ikon rengi otomatik güncellenmeli"
concept_tags: [color, accessibility]
checklist_extra:
  - "fill: currentColor ve stroke: currentColor kullanılmış mı?"
  - "Yüksek karşıtlık modunda sistem metin rengine otomatik uyum sağlandı mı?"
reference_solution_path: private/solutions/css-hard-contrast-mode-svg-icon-fill.css
hint_ladder:
  1: "CSS'te o anki geçerli metin rengini temsil eden sihirli anahtar kelime nedir?"
  2: "SVG ikonlarının üst yazı rengiyle senkronize olması için fill değerine ne yazılır?"
  3: "Bu erişilebilir renk kuralı 'akıllı renk mirası (currentColor)' olarak bilinir."
```

---

### css-hard-custom-scroll-driven-coverflow

```yaml
id: css-hard-custom-scroll-driven-coverflow
version: 1
language: css
engine: none
difficulty: hard
title: "3D albüm kapağı akışı kaydırma animasyonu"
prompt: |
  Apple Coverflow tarzında, kullanıcı yatayda kaydırdıkça ortadaki albüm kapağının düz durduğu,
  sağdaki ve soldaki albüm kapaklarının ise Y ekseni etrafında 45 derece dönerek arkaya doğru
  küçüldüğü 3D bir albüm vitrini tasarlayın. Bu karmaşık dönüşümü tamamen CSS `view-timeline`
  ve `animation-range` ile bağlayarak, kartın ekran ortasına olan mesafesine göre açısını
  değiştiren saf CSS kuralını kurun.
constraints:
  - "3D dönüşüm açısı (`rotateY`) kaydırma konumuna bağlanmalı"
  - "`view-timeline: --kart inline` ve `animation-timeline` kullanılmalı"
  - "Kapsayıcıda 3D derinlik (`perspective`) tanımlanmalı"
concept_tags: [animation, positioning, performance]
checklist_extra:
  - "rotateY açısı kaydırma ekseninde merkezden geçişe göre formüle edilmiş mi?"
  - "perspective tanımlanarak 3D derinlik hissi verilmiş mi?"
reference_solution_path: private/solutions/css-hard-custom-scroll-driven-coverflow.css
hint_ladder:
  1: "Kaydırılan bir elemanın ekrandaki konumuna göre 3D dönmesini sağlayan animasyon zaman çizelgesi nedir?"
  2: "Ortada düz, kenarlarda açılı duran albüm kapağı animasyonuna ne ad verilir?"
  3: "Bu ileri düzey galeri 'kaydırma güdümlü 3D albüm akışı (scroll-driven coverflow)' olarak bilinir."
```

---

### css-hard-fluid-line-height-dynamic-proportions

```yaml
id: css-hard-fluid-line-height-dynamic-proportions
version: 1
language: css
engine: none
difficulty: hard
title: "Yazı boyutu büyüdükçe daralan ters orantılı satır yüksekliği"
prompt: |
  Tipografi kurallarına göre, yazı boyutu büyüdükçe (örneğin devasa başlıklarda) satır yüksekliği
  çarpanının küçülmesi (1.5 yerine 1.1 olması); küçük metinlerde ise satır yüksekliği çarpanının
  büyümesi (1.6 olması) gerekir. Başlık boyutu mobilden masaüstüne `clamp()` ile akışkan
  büyürken, satır yüksekliğinin bu büyümenin tersine daralmasını sağlayan dinamik matematiksel
  satır yüksekliği formülünü kurun.
constraints:
  - "Yazı boyutu büyüdükçe satır yüksekliği oransal olarak daralmalı"
  - "Matematiksel bağıntı `calc()` ve `clamp()` ile kurulmalı"
  - "Dev ekranlarda başlık satırlarının birbirinden kopması engellenmeli"
concept_tags: [typography, responsive]
checklist_extra:
  - "Satır yüksekliği yazı boyutuyla ters orantılı formüle edilmiş mi?"
  - "Hem mobilde hem masaüstünde ideal tipografik ritim korunmuş mu?"
reference_solution_path: private/solutions/css-hard-fluid-line-height-dynamic-proportions.css
hint_ladder:
  1: "Büyük başlıklarda satır aralığının açılmasını önlemek için hangi tipografi kuralı uygulanır?"
  2: "Yazı boyutuyla ters orantılı satır aralığı hesaplamak için calc formülü nasıl kurulur?"
  3: "Bu ileri tipografi tekniği 'ters orantılı akışkan satır yüksekliği (fluid proportional line-height)' olarak bilinir."
```

---

### css-hard-css-logical-properties-rtl-ltr-mirror

```yaml
id: css-hard-css-logical-properties-rtl-ltr-mirror
version: 1
language: css
engine: none
difficulty: hard
title: "Çift yönlü diller için mantıksal özelliklerle ayna mizanpajı"
prompt: |
  Arapça ve İbranice gibi sağdan sola (RTL) okunan diller için ayrı bir stil dosyası yazma
  dönemini kapatın. Geleneksel `left`, `right`, `margin-left`, `padding-right` fiziksel
  yönleri yerine; `margin-inline-start`, `padding-inline-end`, `inset-inline-start` gibi
  modern CSS Mantıksal Özelliklerini (Logical Properties) kullanarak sayfa yönü `dir="rtl"`
  olduğunda otomatik olarak aynalanan evrensel bir kart bileşeni tasarlayın.
constraints:
  - "Hiçbir fiziksel yön özelliği (`left`, `right`, `margin-left` vb.) kullanılmamalı"
  - "Tüm yönler `inline-start`, `inline-end`, `block-start`, `block-end` mantıksal terimleriyle tanımlanmalı"
  - "Sayfa yönü değiştiğinde düzen otomatik olarak kusursuz aynalanmalı"
concept_tags: [layout, responsive, maintainability]
checklist_extra:
  - "margin-inline ve padding-inline mantıksal özellikleri eksiksiz kullanılmış mı?"
  - "dir='rtl' durumunda sıfır kod değişikliğiyle ayna mizanpaj elde ediliyor mu?"
reference_solution_path: private/solutions/css-hard-css-logical-properties-rtl-ltr-mirror.css
hint_ladder:
  1: "Fiziksel sol ve sağ yerine metin yönüne göre otomatik uyum sağlayan CSS özellik ailesi nedir?"
  2: "margin-left yerine metnin başlangıç kenarını temsil eden mantıksal özellik hangisidir?"
  3: "Bu uluslararasılaşma standardı 'CSS mantıksal özellikleri (CSS Logical Properties)' olarak bilinir."
```

---

### css-hard-stateful-interactive-rating-stars

```yaml
id: css-hard-stateful-interactive-rating-stars
version: 1
language: css
engine: none
difficulty: hard
title: "Saf CSS ile ters kardeş seçicili etkileşimli yıldız puanlama"
prompt: |
  Bir e-ticaret yorum formunda 5 yıldızlı bir puanlama bileşeni tasarlayın. Kullanıcı 4. yıldızın
  üzerine geldiğinde, 1, 2, 3 ve 4. yıldızların hepsinin aynı anda sarı renge boyanması gerekir.
  CSS'te geriye doğru kardeş seçici olmadığı için, yıldızları HTML'de tersten sıralayıp
  CSS'te `flex-direction: row-reverse` ile doğru yöne çeviren ve genel kardeş seçicisi (`~`)
  ile farenin altındaki tüm yıldızları parlatan saf CSS hilesini kurun.
constraints:
  - "JavaScript olmadan tamamen CSS seçicileriyle puanlama animasyonu yapılmalı"
  - "Ters esnek kutu (`row-reverse`) ve genel kardeş seçicisi (`~`) kombinasyonu kurulmalı"
  - "Klavyeyle radyo butonları seçildiğinde seçili puan görsel olarak kilitlenmeli"
concept_tags: [focus, accessibility]
checklist_extra:
  - "row-reverse ile görsel sıra kullanıcıya doğru yansıtılmış mı?"
  - "~ kardeş seçicisi hover ve checked durumlarında doğru çalışıyor mu?"
reference_solution_path: private/solutions/css-hard-stateful-interactive-rating-stars.css
hint_ladder:
  1: "CSS'te sadece sonraki kardeşler seçilebildiğine göre önceki yıldızları boyama hilesi nedir?"
  2: "HTML'de tersten yazıp ekranda soldan sağa dizmek için hangi esnek kutu yönü kullanılır?"
  3: "Bu klasik CSS hilesi 'ters kardeş seçicili yıldız puanlama (row-reverse sibling star rating)' olarak bilinir."
```

---

### css-hard-stacked-cards-sticky-deck

```yaml
id: css-hard-stacked-cards-sticky-deck
version: 1
language: css
engine: none
difficulty: hard
title: "Kaydırma sırasında üst üste yığılan iskambil destesi kartları"
prompt: |
  Bir portföy vitrininde 4 adet büyük proje kartı aşağı doğru kaydırılmaktadır. Her kart
  ekranın tepesine ulaştığında (`top: 10vh`) orada sabitlenmeli; arkadan gelen bir sonraki
  kart ise önceki kartın üzerine kayarak binmeli ve önceki kart hafifçe arkaya doğru küçülmelidir
  (iskambil destesi efekti). Yapışkan konumlandırma, z-index derinliği ve kaydırma zaman çizelgesiyle
  bu destelenen kartlar sahnesini inşa edin.
constraints:
  - "Kartlar ardışık yapışkan konumlara sahip olmalı"
  - "Her sonraki kart bir öncekinin üstüne binerek yığılmalı"
  - "Üst üste binen kartlar z-index hiyerarşisiyle doğru sıralanmalı"
concept_tags: [positioning, stacking-context, animation]
checklist_extra:
  - "position: sticky ve top mesafeleri doğru kademelendirilmiş mi?"
  - "Kartların üst üste binmesi z-index ile yönetilmiş mi?"
reference_solution_path: private/solutions/css-hard-stacked-cards-sticky-deck.css
hint_ladder:
  1: "Sayfa kaydırıldıkça kartların birbiri üzerine iskambil destesi gibi binmesi hangi konumlandırmayla yapılır?"
  2: "Her kartın bir öncekinin üstünü örtmesi için katman sırası nasıl kurgulanır?"
  3: "Bu popüler açılış sayfası efekti 'yığılan yapışkan kart destesi (stacked sticky cards)' olarak bilinir."
```

---

