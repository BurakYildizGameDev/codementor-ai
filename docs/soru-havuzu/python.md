# CodeMentor AI — 200 Python Sorusu

Bu belge, `docs/SORU_YAZIM_REHBERI.md` standartlarına uygun olarak hazırlanmış 200 adet Python sorusunu içerir.
Tüm sorular; başlık, prompt, kısıtlar, karmaşıklık beklentisi, kavram etiketleri, kontrol listesi soruları ve üç kademeli ipucu merdivenini barındıran tam YAML şemasında sunulmuştur.

---

## Soru Bankası Değerlendirmesi ve Pedagojik Kullanım Notu

Bu soru bankası; yazılım mühendisliği teknik iş mülakatları (FAANG/Big Tech ve kurumsal şirket kodlama sınavları), bilgisayar mühendisliği öğrencileri ve ileri düzey Python geliştiricileri için tasarlanmıştır:

1. **Öğrenciler ve Temel Düzey İçin:**
   - Çok Kolay ve Kolay bölümler (1 - 100); temel veri yapıları (listeler, sözlükler, kümeler, dizgiler), sınır durumlar (boş girdi, tek eleman, negatif sayılar), döngüler ve Python yerleşik metotlarının doğru kullanımını pekiştirir.
   - Her soruda bellek ve zaman karmaşıklığı (`expected: time, space`) zorunlu tutularak öğrenciye ilk günden Big-O analizi alışkanlığı kazandırılır.

2. **İş Mülakatları ve İleri Düzey İçin:**
   - Orta ve Zor bölümler (101 - 200); İki İşaretçi (Two Pointers), Kayan Pencere (Sliding Window), Dinamik Programlama, Graf Gezinimleri (BFS/DFS, Dijkstra, Tarjan Köprüleri), Ağaçlar ve Sistem Tasarımı seviyesinde veri yapıları (LFU/LRU Cache, Trie, Token Bucket Rate Limiter, Monotonik Yığın) içerir.
   - **Mülakat Kullanımı:** Gerçek bir mülakat simülasyonunda adaya veri yapısının veya algoritmanın adı (örn. "Trie", "Tarjan", "Token Bucket") doğrudan söylenmemeli; yalnızca `prompt` metnindeki gereksinim ve karmaşıklık kısıtları verilerek adayın uygun algoritmayı kendisinin seçmesi beklenmelidir.

### Kapsam ve İstatistikler
- **Toplam Soru:** 200 adet (50 Çok Kolay, 50 Kolay, 50 Orta, 50 Zor)
- **Konsept Dağılımı:** Performans/Big-O (113), Algoritmik Tasarım (104), Sınır Durumları (91), Veri Yapıları (85), Metin/Dizgi İşleme (65), Hash Haritaları (31), Graf/Ağaçlar (18), İstisna & Hata Yönetimi (18).
- **Tip Güvenliği ve Standart:** PEP 484/585 tip ipuçları, Python 3.12+ standartları, saf algoritmik düşünce (harici kütüphane bağımlılığı yok).

---

## 1. Çok Kolay (Very Easy) — 50 Soru

### py-veryeasy-even-count

```yaml
id: py-veryeasy-even-count
version: 1
language: python
engine: none
difficulty: very_easy
title: "Pozitif çift sayıların adedi"
prompt: |
  Verilen tamsayı listesinde bulunan pozitif ve çift sayıların adedini döndüren
  `count_positive_evens(numbers: list[int]) -> int` fonksiyonunu yazın. Liste boş
  olabilir veya yalnızca negatif sayılar içerebilir; bu durumlarda 0 dönmelidir.
  Sıfır sayısı pozitif kabul edilmez.
constraints:
  - "Liste uzunluğu n için çalışma süresi O(n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "Boş liste durumunda 0 döndürülmeli"
expected:
  time: { count_positive_evens: "n" }
  space: "1"
concept_tags: [boundary-conditions, edge-cases]
checklist_extra:
  - "Sıfır sayısı pozitif sayı gibi sayılıp sonuca dahil ediliyor mu?"
  - "Negatif çift sayılar koşulu yanlışlıkla sağlıyor mu?"
reference_solution_path: private/solutions/py-veryeasy-even-count.py
hint_ladder:
  1: "Sayıyı incelerken hem 0'dan büyük olma hem de 2'ye tam bölünme şartını nasıl sınıyorsun?"
  2: "Sıfır çift bir sayıdır ancak pozitif midir; koşulunda sıfır için ayrı bir durum oluşuyor mu?"
  3: "Bu durum 'bileşik mantıksal koşul ve sınır değeri denetimi' olarak bilinir."
```

### py-veryeasy-celsius-to-fahrenheit

```yaml
id: py-veryeasy-celsius-to-fahrenheit
version: 1
language: python
engine: none
difficulty: very_easy
title: "Sıcaklık birim dönüşümü"
prompt: |
  Celsius cinsinden verilen sıcaklık değerini Fahrenheit birimine çeviren
  `celsius_to_fahrenheit(celsius: float) -> float` fonksiyonunu yazın. Formül:
  F = C * (9 / 5) + 32 şeklindedir. Mutlak sıfır noktasının altındaki (-273.15 altı)
  değerler fiziksel olarak geçersizdir ve bu durumda ValueError fırlatılmalıdır.
constraints:
  - "Geçersiz sıcaklıklarda (-273.15 altı) ValueError fırlatılmalı"
  - "Çalışma süresi ve bellek O(1) olmalı"
expected:
  time: { celsius_to_fahrenheit: "1" }
  space: "1"
concept_tags: [floating-point, exceptions, input-validation]
checklist_extra:
  - "Tamsayı bölmesi yapılarak kesirli katsayı kayba uğruyor mu?"
  - "Mutlak sıfır sınırında tam eşitlik durumu doğru kabul ediliyor mu?"
reference_solution_path: private/solutions/py-veryeasy-celsius-to-fahrenheit.py
hint_ladder:
  1: "Girdi mutlak sıfırdan küçük olduğunda fonksiyon ne üretiyor?"
  2: "Bölme işleminde tamsayı bölmesi mi yoksa kayan noktalı bölme mi kullanıyorsun?"
  3: "Bu yaklaşım 'girdi doğrulama ve kayan nokta duyarlılığı' olarak bilinir."
```

### py-veryeasy-string-length-check

```yaml
id: py-veryeasy-string-length-check
version: 1
language: python
engine: none
difficulty: very_easy
title: "Kullanıcı adı uzunluk denetimi"
prompt: |
  Kullanıcı adı metninin belirlenen minimum ve maksimum karakter sınırları içinde olup
  olmadığını denetleyen `is_valid_username_length(username: str, min_len: int, max_len: int) -> bool`
  fonksiyonunu yazın. Sınır değerler dahildir. Kullanıcı adı None veya sınırlar tutarsız
  (min_len > max_len veya negatif) ise False dönmelidir.
constraints:
  - "None girdisinde çökme yaşanmamalı ve False dönmeli"
  - "Zaman karmaşıklığı O(1) olmalı"
expected:
  time: { is_valid_username_length: "1" }
  space: "1"
concept_tags: [boundary-conditions, edge-cases, strings]
checklist_extra:
  - "username None geldiğinde len() çağrısı TypeError fırlatıyor mu?"
  - "min_len veya max_len negatif geldiğinde beklenmeyen bir kabul oluşuyor mu?"
reference_solution_path: private/solutions/py-veryeasy-string-length-check.py
hint_ladder:
  1: "Karakter dizisi parametresi None olduğunda uzunluk fonksiyonunu çağırmadan önce ne yapıyorsun?"
  2: "Alt sınır üst sınırdan büyük verildiğinde aralık denetimi ne sonuç veriyor?"
  3: "Bu denetim 'savunmacı programlama ve kısa devre mantıksal değerlendirme' olarak bilinir."
```

### py-veryeasy-positive-sum

```yaml
id: py-veryeasy-positive-sum
version: 1
language: python
engine: none
difficulty: very_easy
title: "Pozitif sayıların toplamı"
prompt: |
  Verilen tamsayı listesindeki sadece pozitif (sıfırdan büyük) sayıların toplamını
  hesaplayan `sum_positives(numbers: list[int]) -> int` fonksiyonunu yazın. Liste boşsa
  veya hiç pozitif sayı yoksa 0 döndürülmelidir. Liste binlerce eleman içerebilir.
constraints:
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
  - "Bellek kullanımı O(1) olmalı"
expected:
  time: { sum_positives: "n" }
  space: "1"
concept_tags: [boundary-conditions, performance]
checklist_extra:
  - "Sıfır sayısı toplama etki etmese de koşulda fazladan işlem yaratıyor mu?"
  - "Liste oluşturulup bellekte gereksiz kopyalama yapılıyor mu?"
reference_solution_path: private/solutions/py-veryeasy-positive-sum.py
hint_ladder:
  1: "Her elemanı gezerken negatif sayıları nasıl atlıyorsun?"
  2: "Toplamı biriktirirken yeni bir liste mi üretiyorsun yoksa tek bir sayaç değişkeni mi tutuyorsun?"
  3: "Bu yöntem 'akümülatör deseni ile yerinde toplama' olarak bilinir."
```

### py-veryeasy-find-min

```yaml
id: py-veryeasy-find-min
version: 1
language: python
engine: none
difficulty: very_easy
title: "Listedeki en küçük değer"
prompt: |
  Bir tamsayı listesindeki en küçük sayıyı döndüren `find_minimum(numbers: list[int]) -> int | None`
  fonksiyonunu yazın. Liste boş olduğunda None dönmelidir. Hazır sıralama veya arama
  fonksiyonları yerine listeyi tek geçişte inceleyin.
constraints:
  - "Liste n elemanlı olduğunda çalışma süresi O(n) olmalı"
  - "Boş liste durumunda None döndürülmeli"
expected:
  time: { find_minimum: "n" }
  space: "1"
concept_tags: [boundary-conditions, edge-cases]
checklist_extra:
  - "İlk minimum adayını 0 gibi sabit bir sayı seçmek tümü pozitif veya tümü negatif listelerde hataya yol açıyor mu?"
  - "Boş listede ilk indekse erişim IndexError veriyor mu?"
reference_solution_path: private/solutions/py-veryeasy-find-min.py
hint_ladder:
  1: "Başlangıçta en küçük kabul ettiğin değeri neye göre belirliyorsun?"
  2: "Listedeki tüm elemanlar negatif olduğunda 0 başlangıç değeri ne sonuç doğurur?"
  3: "Bu yaklaşım 'ilk eleman ile başlatılan doğrusal arama (linear scan)' olarak bilinir."
```

### py-veryeasy-is-divisible

```yaml
id: py-veryeasy-is-divisible
version: 1
language: python
engine: none
difficulty: very_easy
title: "İki sayıya ortak bölünebilme"
prompt: |
  Bir tamsayının verilen iki bölene de kalansız bölünüp bölünmediğini kontrol eden
  `is_divisible_by_both(number: int, divisor_a: int, divisor_b: int) -> bool`
  fonksiyonunu yazın. Bölenlerden herhangi biri sıfır olduğunda ZeroDivisionError
  meydana gelmemeli, False döndürülmelidir.
constraints:
  - "Bölen sıfır olduğunda istisna fırlatılmamalı ve False dönmeli"
  - "Zaman ve alan karmaşıklığı O(1) olmalı"
expected:
  time: { is_divisible_by_both: "1" }
  space: "1"
concept_tags: [boundary-conditions, edge-cases, error-handling]
checklist_extra:
  - "divisor_a veya divisor_b sıfır olduğunda modulo işlemi yapılmadan önce kontrol ediliyor mu?"
  - "Negatif bölenlerde kalan hesabı doğru değerlendiriliyor mu?"
reference_solution_path: private/solutions/py-veryeasy-is-divisible.py
hint_ladder:
  1: "Bölme ya da kalan işlemi yapmadan önce bölenlerin sıfır olup olmadığını nasıl sınıyorsun?"
  2: "Python'da 0 ile modulo işlemine kalkışıldığında hangi hata üretilir?"
  3: "Bu durum 'sıfıra bölme güvenliği (zero-division guard)' olarak bilinir."
```

### py-veryeasy-first-last-same

```yaml
id: py-veryeasy-first-last-same
version: 1
language: python
engine: none
difficulty: very_easy
title: "İlk ve son karakter eşitliği"
prompt: |
  Verilen metnin ilk ve son karakterlerinin büyük/küçük harf duyarsız olarak aynı olup
  olmadığını kontrol eden `has_matching_ends(text: str) -> bool` fonksiyonunu yazın.
  Metin boş olduğunda veya tek karakterden oluştuğunda ne dönmesi gerektiğini belirleyin:
  boş metin için False, tek karakter için True dönmelidir.
constraints:
  - "Boş metin girdisinde IndexError fırlatılmamalı"
  - "Karakter karşılaştırması büyük/küçük harf duyarsız olmalı"
  - "Zaman karmaşıklığı O(1) olmalı"
expected:
  time: { has_matching_ends: "1" }
  space: "1"
concept_tags: [strings, edge-cases, boundary-conditions]
checklist_extra:
  - "Boş metin geldiğinde text[0] erişimi çökmeye neden oluyor mu?"
  - "Karakterlerin büyük/küçük harf dönüşümü doğru uygulanıyor mu?"
reference_solution_path: private/solutions/py-veryeasy-first-last-same.py
hint_ladder:
  1: "Metin sıfır uzunlukta olduğunda indeksleme yapmadan önce bir kontrolün var mı?"
  2: "'A' ile 'a' harflerinin eşleştiğinden nasıl emin olabilirsin?"
  3: "Bu yöntem 'sınır denetimi ve harf normalizasyonu (case folding)' olarak bilinir."
```

### py-veryeasy-clamp-number

```yaml
id: py-veryeasy-clamp-number
version: 1
language: python
engine: none
difficulty: very_easy
title: "Sayıyı aralıkta sınırlama"
prompt: |
  Verilen bir sayıyı belirlenen alt ve üst sınırlar arasında tutan
  `clamp(value: float, lower: float, upper: float) -> float` fonksiyonunu yazın.
  Değer alt sınırdan küçükse alt sınır, üst sınırdan büyükse üst sınır, aralıktaysa
  kendisi dönmelidir. Eğer lower > upper ise ValueError fırlatılmalıdır.
constraints:
  - "lower > upper olduğunda ValueError fırlatılmalı"
  - "Zaman ve bellek karmaşıklığı O(1) olmalı"
expected:
  time: { clamp: "1" }
  space: "1"
concept_tags: [boundary-conditions, exceptions, input-validation]
checklist_extra:
  - "lower ve upper eşit olduğunda fonksiyon doğru değeri veriyor mu?"
  - "Geçersiz aralık girdisi istisna fırlatmak yerine hatalı sonuç üretiyor mu?"
reference_solution_path: private/solutions/py-veryeasy-clamp-number.py
hint_ladder:
  1: "Alt sınırın üst sınırdan büyük gelmesi durumunda fonksiyonun ne yapması gerekiyor?"
  2: "Koşullu ifadelerin sıralaması sınırların kesişimini doğru yansıtıyor mu?"
  3: "Bu işlem 'değer aralığı kırpma (clamping)' olarak bilinir."
```

### py-veryeasy-count-vowels

```yaml
id: py-veryeasy-count-vowels
version: 1
language: python
engine: none
difficulty: very_easy
title: "Metindeki sesli harf sayısı"
prompt: |
  Bir metin içindeki İngilizce sesli harflerin (a, e, i, o, u) toplam adedini döndüren
  `count_vowels(text: str) -> int` fonksiyonunu yazın. Büyük ve küçük harfler eşit
  sayılmalıdır. Metin boşsa 0 dönmelidir.
constraints:
  - "n karakterli metin için çalışma süresi O(n) olmalı"
  - "Ekstra bellek O(1) olmalı"
expected:
  time: { count_vowels: "n" }
  space: "1"
concept_tags: [strings, boundary-conditions]
checklist_extra:
  - "Büyük harfle yazılmış sesli harfler (örneğin 'A') atlanıyor mu?"
  - "Her karakter denetiminde gereksiz yeni nesneler oluşturuluyor mu?"
reference_solution_path: private/solutions/py-veryeasy-count-vowels.py
hint_ladder:
  1: "Harfleri kontrol etmeden önce büyük/küçük harf ayrımını nasıl ortadan kaldırıyorsun?"
  2: "Sesli harf kümesinde arama yaparken hangi veri tipini kullanmak sabit süre sağlar?"
  3: "Bu işlem 'küme üyeliği ile doğrusal metin tarama' olarak bilinir."
```

### py-veryeasy-repeat-string

```yaml
id: py-veryeasy-repeat-string
version: 1
language: python
engine: none
difficulty: very_easy
title: "Metin çoğaltıcı"
prompt: |
  Verilen bir metni count kez art arda ekleyerek yeni bir metin oluşturan
  `repeat_string(text: str, count: int) -> str` fonksiyonunu yazın. count sıfır veya
  negatifse boş metin dönmelidir. text boşsa boş metin dönmelidir.
constraints:
  - "count <= 0 durumunda boş metin dönmeli"
  - "Sonuç metninin uzunluğu k = len(text) * count olmak üzere çalışma süresi O(k) olmalı"
expected:
  time: { repeat_string: "k" }
  space: "k"
concept_tags: [strings, boundary-conditions]
checklist_extra:
  - "Negatif count değerlerinde döngü sonsuz veya hatalı davranıyor mu?"
  - "Döngü içinde ardışık string birleştirmesi gereksiz bellek kopyalaması yapıyor mu?"
reference_solution_path: private/solutions/py-veryeasy-repeat-string.py
hint_ladder:
  1: "Çoğaltma katsayısı negatif veya sıfır geldiğinde döngüye girmeden ne döndürebilirsin?"
  2: "Python'da metinleri çarpma işlemi veya birleştirme işlemi bellekte nasıl yer ayırır?"
  3: "Bu işlem 'dizgi yineleme ve sınır kontrolü' olarak bilinir."
```

### py-veryeasy-absolute-diff

```yaml
id: py-veryeasy-absolute-diff
version: 1
language: python
engine: none
difficulty: very_easy
title: "İki sayının mutlak farkı"
prompt: |
  İki tamsayı arasındaki mutlak farkı hesaplayan `absolute_difference(a: int, b: int) -> int`
  fonksiyonunu yazın. Dahili `abs()` fonksiyonunu kullanmadan, yalnızca temel karşılaştırma
  ve aritmetik operatörler kullanarak çözün.
constraints:
  - "Dahili abs fonksiyonu kullanılmamalı"
  - "Zaman ve alan karmaşıklığı O(1) olmalı"
expected:
  time: { absolute_difference: "1" }
  space: "1"
concept_tags: [boundary-conditions, design]
checklist_extra:
  - "Sayılar eşit olduğunda farkın 0 çıktığı doğrulanıyor mu?"
  - "b > a olduğunda negatif sonuç üretilmeden doğru çıkarma yapılıyor mu?"
reference_solution_path: private/solutions/py-veryeasy-absolute-diff.py
hint_ladder:
  1: "İlk sayı ikincisinden küçük olduğunda hangi sırayla çıkarma yapmalısın?"
  2: "İki sayının büyüklük ilişkisini basit bir koşul ifadesiyle nasıl belirlersin?"
  3: "Bu mantık 'koşullu çıkarma ile mutlak değer hesabı' olarak bilinir."
```

### py-veryeasy-all-positive

```yaml
id: py-veryeasy-all-positive
version: 1
language: python
engine: none
difficulty: very_easy
title: "Tüm elemanlar pozitif mi"
prompt: |
  Verilen tamsayı listesindeki tüm sayıların sıfırdan büyük olup olmadığını denetleyen
  `are_all_positive(numbers: list[int]) -> bool` fonksiyonunu yazın. Boş liste durumunda
  matematiksel doğruluk gereği True dönmelidir. Negatif veya sıfır bir eleman görüldüğü
  anda liste taranmaya devam edilmemelidir.
constraints:
  - "Negatif veya sıfır eleman bulunduğunda erken çıkış yapılmalı"
  - "Boş liste için True dönmeli"
  - "En kötü durumda n eleman için O(n) süre, O(1) bellek olmalı"
expected:
  time: { are_all_positive: "n" }
  space: "1"
concept_tags: [boundary-conditions, edge-cases, performance]
checklist_extra:
  - "Boş liste için yanlışlıkla False dönüyor mu?"
  - "İlk eleman negatif olduğunda bile listenin tamamı taranıyor mu?"
reference_solution_path: private/solutions/py-veryeasy-all-positive.py
hint_ladder:
  1: "Şartı bozan tek bir eleman gördüğün anda fonksiyonu hemen sonlandırabilir misin?"
  2: "Boş bir kümedeki tüm elemanların bir koşulu sağlaması mantıkta ne anlama gelir?"
  3: "Bu mantık 'kısa devre değerlendirmeli evrensel niceleme (vacuous truth)' olarak bilinir."
```

### py-veryeasy-safe-divide

```yaml
id: py-veryeasy-safe-divide
version: 1
language: python
engine: none
difficulty: very_easy
title: "Güvenli bölme işlemi"
prompt: |
  İki sayıyı birbirine bölen, ancak payda sıfır olduğunda çökmeden varsayılan bir değer
  döndüren `safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float`
  fonksiyonunu yazın. Payda sıfır olduğunda default parametresi dönmelidir.
constraints:
  - "Sıfıra bölme hatası yaşanmamalı"
  - "Zaman ve alan karmaşıklığı O(1) olmalı"
expected:
  time: { safe_divide: "1" }
  space: "1"
concept_tags: [floating-point, edge-cases, error-handling]
checklist_extra:
  - "denominator sıfır olduğunda istisna yakalanıyor veya önceden denetleniyor mu?"
  - "Kayan noktalı sayılarda çok küçük değerler ile tam sıfır doğru ayırt ediliyor mu?"
reference_solution_path: private/solutions/py-veryeasy-safe-divide.py
hint_ladder:
  1: "Bölme işlemine girmeden önce bölenin değerini kontrol ediyor musun?"
  2: "Hata fırlatmak yerine güvenli bir yedek değer döndürmek için ne kullanabilirsin?"
  3: "Bu desen 'güvenli bölme ve varsayılan geri dönüş (safe division fallback)' olarak bilinir."
```

### py-veryeasy-greeting-message

```yaml
id: py-veryeasy-greeting-message
version: 1
language: python
engine: none
difficulty: very_easy
title: "Kişiselleştirilmiş selamlama mesajı"
prompt: |
  Verilen isim ve unvan bilgilerini kullanarak `format_greeting(name: str, title: str | None = None) -> str`
  fonksiyonunu yazın. Unvan verilmişse 'Sayın {title} {name}', verilmemişse veya boşluktan
  oluşuyorsa 'Merhaba {name}' biçiminde metin üretmelidir. İsim başında veya sonundaki
  gereksiz boşluklar temizlenmelidir. İsim boşsa ValueError fırlatılmalıdır.
constraints:
  - "İsim boş veya sadece boşluklardan oluştuğunda ValueError fırlatılmalı"
  - "Karakter dizisi birleştirmede verimli metin biçimlendirme kullanılmalı"
expected:
  time: { format_greeting: "1" }
  space: "1"
concept_tags: [strings, input-validation, exceptions]
checklist_extra:
  - "İsim yalnızca boşluk içerdiğinde strip() denetimi yapılıyor mu?"
  - "title parametresi None olduğunda metne 'None' sözcüğü sızıyor mu?"
reference_solution_path: private/solutions/py-veryeasy-greeting-message.py
hint_ladder:
  1: "İsmin geçerli olup olmadığını boşlukları ayıkladıktan sonra nasıl kontrol edersin?"
  2: "Unvanın None olup olmadığını f-string içinde nasıl ayırt edebilirsin?"
  3: "Bu işlem 'metin temizleme ve koşullu dizgi biçimlendirme' olarak bilinir."
```

### py-veryeasy-square-list

```yaml
id: py-veryeasy-square-list
version: 1
language: python
engine: none
difficulty: very_easy
title: "Listedeki sayıların kareleri"
prompt: |
  Verilen tamsayı listesindeki her sayının karesini alarak yeni bir liste döndüren
  `square_elements(numbers: list[int]) -> list[int]` fonksiyonunu yazın. Orijinal liste
  değiştirilmemelidir. Liste boşsa boş liste dönmelidir.
constraints:
  - "Orijinal girdi listesi üzerinde değişiklik yapılmamalı (mutasyon olmamalı)"
  - "n elemanlı liste için çalışma süresi O(n), ek bellek O(n) olmalı"
expected:
  time: { square_elements: "n" }
  space: "n"
concept_tags: [data-structures, design]
checklist_extra:
  - "Girdi parametresi olan liste yerinde (in-place) değiştiriliyor mu?"
  - "Döngü veya liste üreteci yeni bir liste tahsis ediyor mu?"
reference_solution_path: private/solutions/py-veryeasy-square-list.py
hint_ladder:
  1: "Fonksiyondan dönen listeyi oluştururken orijinal listeyi korumak için ne yapıyorsun?"
  2: "Tüm elemanlara aynı aritmetik işlemi uygulayarak yeni koleksiyon üretmenin en yalın yolu nedir?"
  3: "Bu yaklaşım 'saf fonksiyon ve liste dönüşümü (mapping)' olarak bilinir."
```

### py-veryeasy-last-element

```yaml
id: py-veryeasy-last-element
version: 1
language: python
engine: none
difficulty: very_easy
title: "Listenin son elemanı"
prompt: |
  Bir listenin son elemanını güvenle döndüren `get_last_element(items: list[int], default: int = -1) -> int`
  fonksiyonunu yazın. Liste boş olduğunda IndexError fırlatılmamalı, default parametresi
  dönmelidir. Liste tek bir eleman içeriyorsa o eleman dönmelidir.
constraints:
  - "Boş listede IndexError fırlatılmamalı"
  - "Zaman ve alan karmaşıklığı O(1) olmalı"
expected:
  time: { get_last_element: "1" }
  space: "1"
concept_tags: [boundary-conditions, edge-cases]
checklist_extra:
  - "Liste uzunluğu 0 olduğunda items[-1] erişimi engelleniyor mu?"
  - "Listenin son elemanı kopyalanmadan doğrudan mı erişiliyor?"
reference_solution_path: private/solutions/py-veryeasy-last-element.py
hint_ladder:
  1: "Liste boşken son elemana erişmeye çalışırsan hangi hata fırlatılır?"
  2: "Listenin dolu olup olmadığını en hızlı nasıl test edebilirsin?"
  3: "Bu yaklaşım 'koleksiyon boşluk denetimi ve güvenli indeksleme' olarak bilinir."
```

### py-veryeasy-string-contains-digit

```yaml
id: py-veryeasy-string-contains-digit
version: 1
language: python
engine: none
difficulty: very_easy
title: "Metinde rakam varlığı denetimi"
prompt: |
  Bir metnin içinde en az bir adet rakam ('0'-'9') bulunup bulunmadığını kontrol eden
  `contains_digit(text: str) -> bool` fonksiyonunu yazın. İlk rakamla karşılaşıldığı
  anda metnin geri kalanı incelenmemelidir. Metin boşsa False dönmelidir.
constraints:
  - "İlk rakam bulunduğunda erken çıkış yapılmalı"
  - "n karakterli metin için en kötü durumda süre O(n), alan O(1) olmalı"
expected:
  time: { contains_digit: "n" }
  space: "1"
concept_tags: [strings, performance, edge-cases]
checklist_extra:
  - "İlk rakam bulunduktan sonra metnin sonuna kadar taranmaya devam ediliyor mu?"
  - "Karakterin rakam olup olmadığı yerleşik yöntemlerle mi kontrol ediliyor?"
reference_solution_path: private/solutions/py-veryeasy-string-contains-digit.py
hint_ladder:
  1: "Bir rakam bulduğunda döngüyü sürdürmenin bir anlamı var mı?"
  2: "Karakterlerin sayısal karakter olup olmadığını test eden yerleşik dize metodu nedir?"
  3: "Bu yöntem 'erken sonlandırmalı doğrusal arama (early exit)' olarak bilinir."
```

### py-veryeasy-max-of-three

```yaml
id: py-veryeasy-max-of-three
version: 1
language: python
engine: none
difficulty: very_easy
title: "Üç sayının en büyüğü"
prompt: |
  Verilen üç tamsayıdan en büyük olanı bulan `max_of_three(a: int, b: int, c: int) -> int`
  fonksiyonunu yazın. Dahili `max()` fonksiyonunu kullanmadan, yalnızca karşılaştırma
  mantığıyla çözün. Tüm sayılar birbirine eşit olduğunda da doğru değer dönmelidir.
constraints:
  - "Dahili max() fonksiyonu kullanılmamalı"
  - "Zaman ve alan karmaşıklığı O(1) olmalı"
expected:
  time: { max_of_three: "1" }
  space: "1"
concept_tags: [boundary-conditions, design]
checklist_extra:
  - "İki veya üç sayının birbirine eşit olması durumunda yanlış dal çalışıyor mu?"
  - "Karşılaştırma mantığı gereksiz dallanmalar içeriyor mu?"
reference_solution_path: private/solutions/py-veryeasy-max-of-three.py
hint_ladder:
  1: "İlk olarak birinci ve ikinci sayıyı karşılaştırıp bir geçici lider belirleyebilir misin?"
  2: "Belirlediğin lideri üçüncü sayıyla karşılaştırmak kaç adım gerektirir?"
  3: "Bu yöntem 'sıralı eleme ile en büyük eleman seçimi' olarak bilinir."
```

### py-veryeasy-count-occurrences

```yaml
id: py-veryeasy-count-occurrences
version: 1
language: python
engine: none
difficulty: very_easy
title: "Belirli bir elemanın frekansı"
prompt: |
  Bir listede aranan değerin kaç kez geçtiğini sayan `count_occurrences(items: list[int], target: int) -> int`
  fonksiyonunu yazın. Listenin yerleşik `count` metodunu kullanmadan, kendi döngünüzle
  çözün. Liste boşsa 0 dönmelidir.
constraints:
  - "Listenin yerleşik .count() metodu kullanılmamalı"
  - "n elemanlı liste için çalışma süresi O(n), alan O(1) olmalı"
expected:
  time: { count_occurrences: "n" }
  space: "1"
concept_tags: [boundary-conditions, performance]
checklist_extra:
  - "Aranan eleman listede hiç bulunmadığında sayaç 0 dönüyor mu?"
  - "Döngü içinde yeni liste veya veri yapısı oluşturuluyor mu?"
reference_solution_path: private/solutions/py-veryeasy-count-occurrences.py
hint_ladder:
  1: "Her elemanı gezerken aranan hedefle eşitliğini nasıl test ediyorsun?"
  2: "Eşitlik sağlandığında bir tamsayı sayacı artırmak ne kadar ek alan gerektirir?"
  3: "Bu işlem 'sayaç akümülasyonu ile doğrusal tarama' olarak bilinir."
```

### py-veryeasy-is-empty-or-whitespace

```yaml
id: py-veryeasy-is-empty-or-whitespace
version: 1
language: python
engine: none
difficulty: very_easy
title: "Boşluk veya boş metin denetimi"
prompt: |
  Bir metnin boş veya tamamen görünmez boşluk karakterlerinden (boşluk, tab, yeni satır)
  oluşup oluşmadığını denetleyen `is_blank(text: str | None) -> bool` fonksiyonunu yazın.
  Girdi None ise True dönmelidir. Metin en az bir görünür karakter içeriyorsa False dönmelidir.
constraints:
  - "None girdisinde AttributeError fırlatılmamalı ve True dönmeli"
  - "Metin uzunluğu n için süre en kötü durumda O(n), alan O(1) olmalı"
expected:
  time: { is_blank: "n" }
  space: "1"
concept_tags: [strings, edge-cases, input-validation]
checklist_extra:
  - "text None olduğunda strip() çağrısı yapılmaya çalışılıyor mu?"
  - "Tab ('\\t') ve yeni satır ('\\n') karakterleri boşluk olarak algılanıyor mu?"
reference_solution_path: private/solutions/py-veryeasy-is-empty-or-whitespace.py
hint_ladder:
  1: "Parametre None ise dize metotlarını çağırmadan önce ne döndürmelisin?"
  2: "Metnin başındaki ve sonundaki tüm boşlukları temizlediğinde geriye ne kalıyor?"
  3: "Bu kontrol 'boşluk budama ve boş dize denetimi (blank string validation)' olarak bilinir."
```

### py-veryeasy-filter-greater

```yaml
id: py-veryeasy-filter-greater
version: 1
language: python
engine: none
difficulty: very_easy
title: "Eşik değerden büyük sayıları filtreleme"
prompt: |
  Verilen tamsayı listesinde belirli bir eşik değerden (`threshold`) kesinlikle büyük
  olan sayıları sırasını koruyarak yeni bir listede toplayan
  `filter_greater_than(numbers: list[int], threshold: int) -> list[int]` fonksiyonunu yazın.
  Hiçbir sayı eşiği aşmıyorsa boş liste dönmelidir. Orijinal liste değiştirilmemelidir.
constraints:
  - "Orijinal liste değiştirilmemeli"
  - "n elemanlı liste için süre O(n), dönen liste için alan en fazla O(n) olmalı"
expected:
  time: { filter_greater_than: "n" }
  space: "n"
concept_tags: [boundary-conditions, data-structures]
checklist_extra:
  - "Eşik değere tam eşit olan sayılar (büyük-eşit yerine) yanlışlıkla dahil ediliyor mu?"
  - "Orijinal listedeki göreli eleman sırası bozuluyor mu?"
reference_solution_path: private/solutions/py-veryeasy-filter-greater.py
hint_ladder:
  1: "Büyüktür (>) ile büyük eşittir (>=) arasındaki farkı koruyor musun?"
  2: "Yeni listeyi oluştururken elemanları hangi sırayla ekliyorsun?"
  3: "Bu işlem 'koşullu filtreleme ve liste inşası' olarak bilinir."
```

### py-veryeasy-multiply-elements

```yaml
id: py-veryeasy-multiply-elements
version: 1
language: python
engine: none
difficulty: very_easy
title: "Listedeki sayıların çarpımı"
prompt: |
  Bir tamsayı listesindeki tüm elemanların çarpımını döndüren
  `product_of_list(numbers: list[int]) -> int` fonksiyonunu yazın. Liste boş olduğunda
  çarpımsal birim eleman olan 1 dönmelidir. Eğer listede sıfır varsa sonuç hemen 0
  olarak döndürülmeli, gereksiz işlemler sürdürülmemelidir.
constraints:
  - "Sıfır elemanı görüldüğünde çarpım döngüsü sonlandırılmalı"
  - "Boş liste için 1 dönmeli"
  - "n eleman için süre en kötü durumda O(n), alan O(1) olmalı"
expected:
  time: { product_of_list: "n" }
  space: "1"
concept_tags: [boundary-conditions, performance, edge-cases]
checklist_extra:
  - "0 elemanı görüldüğünde döngü erken bitiriliyor mu?"
  - "Boş liste durumunda 0 yerine 1 dönmesi sağlandı mı?"
reference_solution_path: private/solutions/py-veryeasy-multiply-elements.py
hint_ladder:
  1: "Çarpma işleminde başlangıç değeri (etkisiz eleman) olarak ne seçilmelidir?"
  2: "Listedeki herhangi bir sayı 0 olduğunda geriye kalan çarpmaların bir önemi kalır mı?"
  3: "Bu mantık 'çarpımsal birim eleman ve sıfır yutan eleman ile erken çıkış' olarak bilinir."
```

### py-veryeasy-swap-pair

```yaml
id: py-veryeasy-swap-pair
version: 1
language: python
engine: none
difficulty: very_easy
title: "İkili demet elemanlarını yer değiştirme"
prompt: |
  İki elemandan oluşan bir demetin (tuple) elemanlarının yerini değiştiren
  `swap_pair(pair: tuple[int, int]) -> tuple[int, int]` fonksiyonunu yazın.
  Örneğin (1, 2) verildiğinde (2, 1) dönmelidir.
constraints:
  - "Zaman ve alan karmaşıklığı O(1) olmalı"
  - "Dönen değer yeni bir tuple olmalı"
expected:
  time: { swap_pair: "1" }
  space: "1"
concept_tags: [data-structures, design]
checklist_extra:
  - "Tuple'ın değişmez (immutable) yapısına aykırı bir atama deneniyor mu?"
  - "Demet paketleme/çözme (unpacking) hatasız uygulanıyor mu?"
reference_solution_path: private/solutions/py-veryeasy-swap-pair.py
hint_ladder:
  1: "Bir demetin elemanlarını iki değişkene aynı anda nasıl atayabilirsin?"
  2: "Elde ettiğin değişkenleri ters sırada yeni bir demet olarak nasıl paketlersin?"
  3: "Bu işlem 'demet çözme ve paketleme (tuple unpacking)' olarak bilinir."
```

### py-veryeasy-remove-negative

```yaml
id: py-veryeasy-remove-negative
version: 1
language: python
engine: none
difficulty: very_easy
title: "Negatif sayıları ayıklama"
prompt: |
  Bir tamsayı listesinde bulunan negatif sayıları ayıklayarak yalnızca sıfır ve pozitif
  sayılardan oluşan yeni bir liste döndüren `remove_negatives(numbers: list[int]) -> list[int]`
  fonksiyonunu yazın. Orijinal liste bozulmamalıdır.
constraints:
  - "Girdi listesi değiştirilmemeli"
  - "n elemanlı liste için çalışma süresi O(n), ek bellek O(n) olmalı"
expected:
  time: { remove_negatives: "n" }
  space: "n"
concept_tags: [data-structures, boundary-conditions]
checklist_extra:
  - "0 sayısı negatif sayılmayıp sonuca dahil ediliyor mu?"
  - "Orijinal listeden eleman silinmeye çalışılarak döngü indeksi bozuluyor mu?"
reference_solution_path: private/solutions/py-veryeasy-remove-negative.py
hint_ladder:
  1: "Bir listeyi döngüyle gezerken aynı anda içinden eleman silmek neden tehlikelidir?"
  2: "İstenen şartı sağlayan elemanları yeni bir listeye eklemek bu sorunu nasıl çözer?"
  3: "Bu yaklaşım 'koleksiyon mutasyonu yerine yeni koleksiyon üretimi' olarak bilinir."
```

### py-veryeasy-is-in-range

```yaml
id: py-veryeasy-is-in-range
version: 1
language: python
engine: none
difficulty: very_easy
title: "Aralık dahilinde olma kontrolü"
prompt: |
  Verilen sayının `start` ve `end` sınırları arasında olup olmadığını denetleyen
  `is_in_range(value: float, start: float, end: float, inclusive: bool = True) -> bool`
  fonksiyonunu yazın. `inclusive` True olduğunda sınırlar dahil, False olduğunda hariç
  tutulmalıdır. Eğer start > end ise sınırlar otomatik olarak yer değiştirmelidir.
constraints:
  - "start > end durumunda sınırlar düzeltilmeli"
  - "Zaman ve alan karmaşıklığı O(1) olmalı"
expected:
  time: { is_in_range: "1" }
  space: "1"
concept_tags: [boundary-conditions, edge-cases]
checklist_extra:
  - "start > end geldiğinde kontrol başarısız mı oluyor yoksa sınırlar normalize ediliyor mu?"
  - "inclusive bayrağı eşitlik durumunu doğru yönetiyor mu?"
reference_solution_path: private/solutions/py-veryeasy-is-in-range.py
hint_ladder:
  1: "Başlangıç sınırı bitiş sınırından büyükse ikisinin yerini nasıl değiştirebilirsin?"
  2: "Eşitlik durumunu bayrağın değerine göre nasıl tek bir mantık ifadesine bağlarsın?"
  3: "Bu yaklaşım 'sınır normalizasyonu ve parametrik aralık testi' olarak bilinir."
```

### py-veryeasy-sum-range

```yaml
id: py-veryeasy-sum-range
version: 1
language: python
engine: none
difficulty: very_easy
title: "Aralıktaki tamsayıların toplamı"
prompt: |
  `a` ve `b` tamsayıları (dahil) arasındaki tüm tamsayıların toplamını hesaplayan
  `sum_range(a: int, b: int) -> int` fonksiyonunu yazın. Eğer a > b ise fonksiyon
  yine de iki sayı arasındaki toplamı bulmalıdır (örneğin a=5, b=2 için 2+3+4+5).
  İşlemi bir döngüde dönmek yerine matematiksel toplam formülüyle O(1) zamanda çözün.
constraints:
  - "Çalışma süresi O(1) olmalı (döngü kullanılmamalı)"
  - "Bellek kullanımı O(1) olmalı"
expected:
  time: { sum_range: "1" }
  space: "1"
concept_tags: [performance, design, boundary-conditions]
checklist_extra:
  - "a > b olduğunda formülün negatif sonuç üretmesi engelleniyor mu?"
  - "Eleman adedi hesaplanırken sınır farkına +1 ekleniyor mu?"
reference_solution_path: private/solutions/py-veryeasy-sum-range.py
hint_ladder:
  1: "a ve b arasındaki eleman sayısı formülünde (b - a + 1) terimini nasıl kullanırsın?"
  2: "Ardışık tamsayıların toplamı formülü Gauss toplamıyla nasıl ifade edilir?"
  3: "Bu yöntem 'aritmetik dizi toplam formülü ile sabit zamanlı hesaplama' olarak bilinir."
```

### py-veryeasy-capitalize-word

```yaml
id: py-veryeasy-capitalize-word
version: 1
language: python
engine: none
difficulty: very_easy
title: "İlk harfi büyütme"
prompt: |
  Verilen tek bir kelimenin yalnızca ilk harfini büyük, geri kalan harflerini küçük
  yapan `capitalize_word(word: str) -> str` fonksiyonunu yazın. Metin boşsa boş metin
  dönmelidir. İlk karakter harf değilse (örneğin rakam veya noktalama) hata vermemeli,
  kalan karakterler yine küçültülmelidir.
constraints:
  - "Boş metinde IndexError fırlatılmamalı"
  - "Kelime uzunluğu n için süre O(n), alan O(n) olmalı"
expected:
  time: { capitalize_word: "n" }
  space: "n"
concept_tags: [strings, boundary-conditions, edge-cases]
checklist_extra:
  - "Metin boş olduğunda word[0] ifadesi çökme yaratıyor mu?"
  - "İlk karakter dışındaki harflerin küçük harfe çevrildiği test ediliyor mu?"
reference_solution_path: private/solutions/py-veryeasy-capitalize-word.py
hint_ladder:
  1: "Metin boşken indeksleme yapmadan önce uzunluk denetimi yapıyor musun?"
  2: "İlk karakteri büyük yapıp kalanı küçük yapmak için dilimleme (slicing) nasıl kullanılır?"
  3: "Bu işlem 'dize dilimleme ve harf kasası dönüşümü' olarak bilinir."
```

### py-veryeasy-has-duplicates-pair

```yaml
id: py-veryeasy-has-duplicates-pair
version: 1
language: python
engine: none
difficulty: very_easy
title: "Yan yana eşit iki eleman denetimi"
prompt: |
  Bir listede ardışık (yan yana) duran iki elemanın birbirine eşit olup olmadığını
  denetleyen `has_adjacent_duplicates(items: list[int]) -> bool` fonksiyonunu yazın.
  Böyle bir ikili bulunur bulunmaz True dönülmeli ve arama sonlandırılmalıdır. Liste
  boş veya tek elemanlıysa False dönmelidir.
constraints:
  - "Eşit ikili bulunduğunda erken çıkış yapılmalı"
  - "Liste n elemanlı olduğunda en kötü durumda süre O(n), alan O(1) olmalı"
expected:
  time: { has_adjacent_duplicates: "n" }
  space: "1"
concept_tags: [boundary-conditions, edge-cases, performance]
checklist_extra:
  - "Son elemana gelindiğinde i+1 indeksi IndexError oluşturuyor mu?"
  - "0 veya 1 elemanlı listelerde döngüye girmeden False dönülüyor mu?"
reference_solution_path: private/solutions/py-veryeasy-has-duplicates-pair.py
hint_ladder:
  1: "Listenin n-1'inci indeksine ulaştığında sonraki indekse erişmeye çalışırsan ne olur?"
  2: "İkili karşılaştırmayı yaparken döngü sınırını nasıl ayarlamalısın?"
  3: "Bu yaklaşım 'komşu indeks denetimi ve sınır korumalı döngü' olarak bilinir."
```

### py-veryeasy-calculate-discount

```yaml
id: py-veryeasy-calculate-discount
version: 1
language: python
engine: none
difficulty: very_easy
title: "İndirimli fiyat hesaplama"
prompt: |
  Orijinal fiyat ve indirim yüzdesi verildiğinde ödenecek tutarı hesaplayan
  `apply_discount(price: float, discount_percent: float) -> float` fonksiyonunu yazın.
  İndirim yüzdesi 0 ile 100 arasında olmalıdır; bu aralık dışındaysa ValueError
  fırlatılmalıdır. Fiyat negatifse yine ValueError fırlatılmalıdır.
constraints:
  - "Geçersiz yüzde veya negatif fiyatta ValueError fırlatılmalı"
  - "Zaman ve alan karmaşıklığı O(1) olmalı"
expected:
  time: { apply_discount: "1" }
  space: "1"
concept_tags: [floating-point, exceptions, input-validation]
checklist_extra:
  - "discount_percent 100 olduğunda sonucun tam 0.0 çıktığı test ediliyor mu?"
  - "Geçersiz değerlerde hata fırlatmak yerine hatalı sayı mı dönüyor?"
reference_solution_path: private/solutions/py-veryeasy-calculate-discount.py
hint_ladder:
  1: "Girdilerin geçerli aralıkta olup olmadığını hesaplamadan önce nasıl denetlersin?"
  2: "Yüzde indirimini fiyattan düşerken formülü nasıl kurarsın?"
  3: "Bu işlem 'ön koşul denetimi ve oransal indirim hesabı' olarak bilinir."
```

### py-veryeasy-is-leap-year

```yaml
id: py-veryeasy-is-leap-year
version: 1
language: python
engine: none
difficulty: very_easy
title: "Artık yıl belirleme"
prompt: |
  Verilen bir yılın Gregoryen takvimine göre artık yıl olup olmadığını denetleyen
  `is_leap_year(year: int) -> bool` fonksiyonunu yazın. Kural: Yıl 4'e tam bölünmeli,
  ancak 100'e tam bölünen yıllar 400'e de tam bölünmüyorsa artık yıl sayılmaz. Yıl
  pozitif bir sayı değilse ValueError fırlatılmalıdır.
constraints:
  - "year <= 0 durumunda ValueError fırlatılmalı"
  - "Zaman ve alan karmaşıklığı O(1) olmalı"
expected:
  time: { is_leap_year: "1" }
  space: "1"
concept_tags: [boundary-conditions, exceptions, design]
checklist_extra:
  - "1900 gibi 100'e bölünüp 400'e bölünmeyen yıllar artık yıl sayılıyor mu?"
  - "2000 gibi 400'e bölünen yıllar doğru belirleniyor mu?"
reference_solution_path: private/solutions/py-veryeasy-is-leap-year.py
hint_ladder:
  1: "100'ün katı olan yılların durumunu genel 4'e bölünme kuralından nasıl ayırırsın?"
  2: "400'e tam bölünebilme şartını mantıksal ifadenin neresine yerleştirmelisin?"
  3: "Bu mantık 'katmanlı bölünebilme kuralları ve artık yıl algoritması' olarak bilinir."
```

### py-veryeasy-find-first-negative

```yaml
id: py-veryeasy-find-first-negative
version: 1
language: python
engine: none
difficulty: very_easy
title: "İlk negatif sayının indeksi"
prompt: |
  Bir tamsayı listesinde ilk karşılaşılan negatif sayının indeksini döndüren
  `find_first_negative_index(numbers: list[int]) -> int` fonksiyonunu yazın.
  Eğer listede hiç negatif sayı yoksa veya liste boşsa -1 dönmelidir.
  Negatif sayı bulunduğu anda arama sonlandırılmalıdır.
constraints:
  - "İlk negatif sayı bulunduğunda döngü sonlandırılmalı"
  - "Negatif sayı bulunamadığında -1 dönmeli"
  - "n elemanlı liste için en kötü durumda süre O(n), alan O(1) olmalı"
expected:
  time: { find_first_negative_index: "n" }
  space: "1"
concept_tags: [boundary-conditions, performance, edge-cases]
checklist_extra:
  - "Negatif sayı bulunduktan sonra liste taranmaya devam ediliyor mu?"
  - "Sıfır sayısı negatif kabul ediliyor mu?"
reference_solution_path: private/solutions/py-veryeasy-find-first-negative.py
hint_ladder:
  1: "Elemanları indeksleriyle birlikte gezinmek için hangi yerleşik fonksiyonu kullanırsın?"
  2: "Şartı sağlayan ilk elemanı gördüğün an indeksi nasıl doğrudan döndürürsün?"
  3: "Bu yöntem 'numaralandırılmış döngü ile erken çıkışlı doğrusal arama' olarak bilinir."
```

### py-veryeasy-pad-left

```yaml
id: py-veryeasy-pad-left
version: 1
language: python
engine: none
difficulty: very_easy
title: "Metni soldan doldurma"
prompt: |
  Verilen bir metni belirlenen toplam uzunluğa (`width`) ulaşana kadar sol tarafına
  dolgu karakteri (`fill_char`) ekleyen `pad_left(text: str, width: int, fill_char: str = ' ') -> str`
  fonksiyonunu yazın. Metin zaten bu uzunlukta veya daha uzunsa aynen dönmelidir.
  `fill_char` tam olarak bir karakterden oluşmalıdır, aksi halde ValueError fırlatılmalıdır.
constraints:
  - "len(fill_char) != 1 durumunda ValueError fırlatılmalı"
  - "width <= len(text) ise metin değiştirilmeden dönmeli"
  - "Hedef uzunluk w = max(len(text), width) için süre ve alan O(w) olmalı"
expected:
  time: { pad_left: "w" }
  space: "w"
concept_tags: [strings, input-validation, exceptions]
checklist_extra:
  - "Dolgu karakteri olarak birden çok karakter girildiğinde denetleniyor mu?"
  - "Döngü ile tek tek karakter eklenerek karesel kopyalama mı yapılıyor?"
reference_solution_path: private/solutions/py-veryeasy-pad-left.py
hint_ladder:
  1: "Dolgu karakterinin tek bir karakter olduğunu fonksiyonun başında nasıl kontrol edersin?"
  2: "Eksik kalan karakter sayısını hesaplayıp dolgu karakterini bir kerede çoğaltabilir misin?"
  3: "Bu işlem 'sol dolgu (left padding) ve dize boyutu tamamlama' olarak bilinir."
```

### py-veryeasy-count-booleans

```yaml
id: py-veryeasy-count-booleans
version: 1
language: python
engine: none
difficulty: very_easy
title: "True değerlerinin sayısı"
prompt: |
  Boole ve tamsayı değerlerinden oluşan karışık bir listede tam olarak boole türünde
  ve değeri `True` olan elemanların adedini döndüren `count_exact_trues(items: list[object]) -> int`
  fonksiyonunu yazın. Python'da `bool` sınıfı `int` sınıfının alt sınıfı olduğundan,
  `1` sayısı kesinlikle True sayılmamalıdır; türün bizzat `bool` olduğu denetlenmelidir.
constraints:
  - "Tamsayı 1 değeri True olarak sayılmamalı"
  - "n elemanlı liste için süre O(n), alan O(1) olmalı"
expected:
  time: { count_exact_trues: "n" }
  space: "1"
concept_tags: [edge-cases, design]
checklist_extra:
  - "x is True veya type(x) is bool denetimi yerine x == True kullanılarak 1 sayısı da sayılıyor mu?"
  - "None ve False değerleri sayacı etkiliyor mu?"
reference_solution_path: private/solutions/py-veryeasy-count-booleans.py
hint_ladder:
  1: "Python'da True == 1 eşitliği doğru mudur? Değer eşitliği yerine kimlik veya tip kontrolü nasıl yapılır?"
  2: "Bir nesnenin tam olarak bool sınıfından olduğunu nasıl doğrularsın?"
  3: "Bu ayrım 'tür duyarlı eşitlik ve Python tip hiyerarşisi (bool/int alt sınıflandırması)' olarak bilinir."
```

### py-veryeasy-second-element

```yaml
id: py-veryeasy-second-element
version: 1
language: python
engine: none
difficulty: very_easy
title: "Listenin ikinci elemanı"
prompt: |
  Bir tamsayı listesinin ikinci elemanını döndüren `get_second_element(items: list[int]) -> int | None`
  fonksiyonunu yazın. Liste iki elemandan az eleman içeriyorsa IndexError fırlatılmamalı,
  None dönmelidir.
constraints:
  - "İkiden az elemanlı listelerde IndexError fırlatılmamalı ve None dönmeli"
  - "Zaman ve alan karmaşıklığı O(1) olmalı"
expected:
  time: { get_second_element: "1" }
  space: "1"
concept_tags: [boundary-conditions, edge-cases]
checklist_extra:
  - "Liste uzunluğu 1 olduğunda items[1] erişimi IndexError üretiyor mu?"
  - "Listenin boyutu kontrol edilmeden doğrudan indeksleme mi yapılıyor?"
reference_solution_path: private/solutions/py-veryeasy-second-element.py
hint_ladder:
  1: "İkinci elemana erişmek için indeks değeri kaçtır?"
  2: "Listenin en az iki elemanı olduğunu indekse dokunmadan önce nasıl teyit edersin?"
  3: "Bu işlem 'güvenli indeksleme ve sınır koşulu denetimi' olarak bilinir."
```

### py-veryeasy-is-single-digit

```yaml
id: py-veryeasy-is-single-digit
version: 1
language: python
engine: none
difficulty: very_easy
title: "Tek basamaklı sayı denetimi"
prompt: |
  Verilen bir tamsayının pozitif veya negatif tek basamaklı bir sayı olup olmadığını
  denetleyen `is_single_digit(number: int) -> bool` fonksiyonunu yazın. -9 ile 9
  arasındaki tüm sayılar (sınırlar dahil) tek basamaklı kabul edilmelidir.
constraints:
  - "-9 ve 9 sınır değerleri True dönmeli"
  - "Zaman ve alan karmaşıklığı O(1) olmalı"
expected:
  time: { is_single_digit: "1" }
  space: "1"
concept_tags: [boundary-conditions, edge-cases]
checklist_extra:
  - "Negatif tek basamaklı sayılar (-5 gibi) iki basamaklı mı sayılıyor?"
  - "Sayı metne çevrilerek eksi işareti yüzünden basamak sayısı yanlış mı hesaplanıyor?"
reference_solution_path: private/solutions/py-veryeasy-is-single-digit.py
hint_ladder:
  1: "Sayıyı metne çevirip uzunluğunu alırsan negatif sayılardaki '-' işareti uzunluğu nasıl etkiler?"
  2: "Aritmetik karşılaştırma ile sayının -9 ve 9 arasında olduğunu doğrudan nasıl sınarsın?"
  3: "Bu yöntem 'sayısal aralık karşılaştırması ile basamak denetimi' olarak bilinir."
```

### py-veryeasy-reverse-two-words

```yaml
id: py-veryeasy-reverse-two-words
version: 1
language: python
engine: none
difficulty: very_easy
title: "İki kelimeli metni tersine çevirme"
prompt: |
  Tam olarak iki kelimeden oluşan bir metnin kelimelerinin sırasını değiştiren
  `swap_two_words(phrase: str) -> str` fonksiyonunu yazın. Örneğin 'Ali Veli' verildiğinde
  'Veli Ali' dönmelidir. Metin iki kelimeden oluşmuyorsa (tek kelime veya üçten fazla)
  ValueError fırlatılmalıdır. Aradaki fazla boşluklar tek bir boşluğa indirgenmelidir.
constraints:
  - "Metin tam olarak iki kelime içermiyorsa ValueError fırlatılmalı"
  - "Kelimelerin uzunluğu n için süre ve alan O(n) olmalı"
expected:
  time: { swap_two_words: "n" }
  space: "n"
concept_tags: [strings, exceptions, parsing]
checklist_extra:
  - "Metin tek kelimeden oluştuğunda IndexError yerine ValueError fırlatılıyor mu?"
  - "Birden fazla boşluk içeren metinlerde parçalama işlemi doğru çalışıyor mu?"
reference_solution_path: private/solutions/py-veryeasy-reverse-two-words.py
hint_ladder:
  1: "Metni kelimelerine ayırdığında elde ettiğin listenin uzunluğunu nasıl doğrularsın?"
  2: "Elde edilen iki kelimeyi aralarında tek bir boşluk olacak şekilde nasıl birleştirirsin?"
  3: "Bu işlem 'metin parçalama, boyut doğrulama ve yeniden biçimlendirme' olarak bilinir."
```

### py-veryeasy-sum-even-indexed

```yaml
id: py-veryeasy-sum-even-indexed
version: 1
language: python
engine: none
difficulty: very_easy
title: "Çift indeksli elemanların toplamı"
prompt: |
  Bir tamsayı listesinde çift numaralı indekslerde (0, 2, 4...) bulunan elemanların
  toplamını hesaplayan `sum_even_indices(numbers: list[int]) -> int` fonksiyonunu yazın.
  Liste boşsa 0 dönmelidir. Tek elemanlı listede yalnızca o elemanın değeri dönmelidir.
constraints:
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
expected:
  time: { sum_even_indices: "n" }
  space: "1"
concept_tags: [boundary-conditions, performance]
checklist_extra:
  - "Döngü 2'şer adımla ilerlemek yerine tüm elemanları gezip tek tek modulo mu alıyor?"
  - "Boş liste durumunda döngü hatasız 0 üretiyor mu?"
reference_solution_path: private/solutions/py-veryeasy-sum-even-indexed.py
hint_ladder:
  1: "Döngü kurarken adım büyüklüğünü (step) 2 yaparak sadece çift indeksleri nasıl ziyaret edersin?"
  2: "Her adımda indeks modunu almak yerine doğrudan doğru indekslere atlamak süreyi nasıl etkiler?"
  3: "Bu işlem 'adımlı aralık döngüsü (strided iteration)' olarak bilinir."
```

### py-veryeasy-replace-char

```yaml
id: py-veryeasy-replace-char
version: 1
language: python
engine: none
difficulty: very_easy
title: "Belirli karakteri değiştirme"
prompt: |
  Bir metin içindeki hedef karakteri (`old_char`) yeni bir karakterle (`new_char`)
  değiştiren `replace_character(text: str, old_char: str, new_char: str) -> str`
  fonksiyonunu yazın. Metnin yerleşik `.replace()` metodunu kullanmadan, kendi döngünüzle
  çözün. Metin boşsa boş metin dönmelidir.
constraints:
  - "Dahili .replace() metodu kullanılmamalı"
  - "n karakterli metin için süre O(n), alan O(n) olmalı"
expected:
  time: { replace_character: "n" }
  space: "n"
concept_tags: [strings, design]
checklist_extra:
  - "Döngüde str birleştirme (s += c) yapılarak karesel bellek kopyalaması yapılıyor mu?"
  - "Karakterlerin bir liste toplanıp en sonda birleştirilmesi tercih edildi mi?"
reference_solution_path: private/solutions/py-veryeasy-replace-char.py
hint_ladder:
  1: "Her adımda yeni bir string oluşturmak yerine karakterleri bir listede biriktirip sonda birleştirmek neden daha hızlıdır?"
  2: "Eşleşen karakter gördüğünde listeye neyi eklemelisin?"
  3: "Bu desen 'dizgi oluşturucu (list of characters to join) deseni' olarak bilinir."
```

### py-veryeasy-list-is-sorted-pair

```yaml
id: py-veryeasy-list-is-sorted-pair
version: 1
language: python
engine: none
difficulty: very_easy
title: "İki elemanlı liste sıralı mı"
prompt: |
  İki tamsayıdan oluşan bir listenin küçükten büyüğe sıralı olup olmadığını
  (ilk eleman <= ikinci eleman) denetleyen `is_pair_sorted(pair: list[int]) -> bool`
  fonksiyonunu yazın. Liste tam olarak iki elemandan oluşmuyorsa ValueError fırlatılmalıdır.
constraints:
  - "Liste uzunluğu 2 değilse ValueError fırlatılmalı"
  - "Zaman ve alan karmaşıklığı O(1) olmalı"
expected:
  time: { is_pair_sorted: "1" }
  space: "1"
concept_tags: [boundary-conditions, exceptions, input-validation]
checklist_extra:
  - "İki eleman eşit olduğunda (örneğin [3, 3]) True döndüğü doğrulanıyor mu?"
  - "Liste uzunluğu 2'den farklı olduğunda doğru istisna fırlatılıyor mu?"
reference_solution_path: private/solutions/py-veryeasy-list-is-sorted-pair.py
hint_ladder:
  1: "Listenin uzunluğunu karşılaştırmadan önce nasıl doğrularsın?"
  2: "Eşit elemanlar sıralı kabul edilir mi? Hangi operatörü kullanmalısın?"
  3: "Bu denetim 'ön koşul doğrulaması ve zayıf sıralama karşılaştırması' olarak bilinir."
```

### py-veryeasy-tax-calculator

```yaml
id: py-veryeasy-tax-calculator
version: 1
language: python
engine: none
difficulty: very_easy
title: "KDV ve vergi tutarı hesabı"
prompt: |
  Net tutar ve vergi oranı verildiğinde hesaplanan vergi tutarını ve toplam tutarı
  bir demet olarak döndüren `calculate_tax(net_amount: float, tax_rate: float) -> tuple[float, float]`
  fonksiyonunu yazın. Geriye (vergi_tutari, toplam_tutar) dönmelidir. Tutar veya oran
  negatifse ValueError fırlatılmalıdır.
constraints:
  - "Negatif tutar veya oranda ValueError fırlatılmalı"
  - "Zaman ve alan karmaşıklığı O(1) olmalı"
expected:
  time: { calculate_tax: "1" }
  space: "1"
concept_tags: [floating-point, exceptions, input-validation]
checklist_extra:
  - "Vergi oranı sıfır olduğunda verginin 0.0 ve toplamın net tutara eşit olduğu teyit edildi mi?"
  - "Negatif parametreler doğru şekilde engelleniyor mu?"
reference_solution_path: private/solutions/py-veryeasy-tax-calculator.py
hint_ladder:
  1: "Parametrelerin sıfırdan küçük olup olmadığını hesaplama öncesinde nasıl denetlersin?"
  2: "Vergi tutarını bulduktan sonra toplam tutara nasıl ulaşırsın?"
  3: "Bu işlem 'girdi doğrulama ve demet olarak çoklu değer döndürme' olarak bilinir."
```

### py-veryeasy-count-spaces

```yaml
id: py-veryeasy-count-spaces
version: 1
language: python
engine: none
difficulty: very_easy
title: "Metindeki boşluk sayısı"
prompt: |
  Verilen metin içindeki standart boşluk (' ') karakterlerinin sayısını döndüren
  `count_spaces(text: str) -> int` fonksiyonunu yazın. Sekme ('\\t') veya yeni satır ('\\n')
  karakterleri sayılmamalı, yalnızca ' ' karakteri sayılmalıdır. Metin boşsa 0 dönmelidir.
constraints:
  - "Yalnızca ' ' karakteri sayılmalı"
  - "n karakterli metin için süre O(n), ek bellek O(1) olmalı"
expected:
  time: { count_spaces: "n" }
  space: "1"
concept_tags: [strings, boundary-conditions]
checklist_extra:
  - "Sekme veya satır sonu gibi diğer boşluk karakterleri yanlışlıkla sayılıyor mu?"
  - "Döngü ek bellek kullanmadan tek bir sayaçla mı çalışıyor?"
reference_solution_path: private/solutions/py-veryeasy-count-spaces.py
hint_ladder:
  1: "Genel boşluk denetimi yerine birebir ' ' karakteriyle eşitlik kontrolü yapıyor musun?"
  2: "Metni döngüyle tararken sayaç mantığını nasıl kurarsın?"
  3: "Bu işlem 'kesin karakter eşleştirme ile doğrusal sayaç' olarak bilinir."
```

### py-veryeasy-sign-of-number

```yaml
id: py-veryeasy-sign-of-number
version: 1
language: python
engine: none
difficulty: very_easy
title: "Sayının işareti"
prompt: |
  Verilen bir sayının işaretini belirleyen `get_sign(number: float) -> int` fonksiyonunu yazın:
  sayı pozitifse 1, negatifse -1, sıfırsa 0 döndürmelidir.
constraints:
  - "Zaman ve alan karmaşıklığı O(1) olmalı"
  - "Dönüş değeri kesinlikle tamsayı (-1, 0, 1) olmalı"
expected:
  time: { get_sign: "1" }
  space: "1"
concept_tags: [boundary-conditions, design]
checklist_extra:
  - "0.0 değeri verildiğinde tam 0 dönüyor mu?"
  - "Dallanma koşulları tüm durumları kapsıyor mu?"
reference_solution_path: private/solutions/py-veryeasy-sign-of-number.py
hint_ladder:
  1: "Sayının sıfırla ilişkisini üç farklı durumda nasıl ele alırsın?"
  2: "Koşullu if-elif-else yapısı eksiksiz kuruldu mu?"
  3: "Bu işlem 'işaret fonksiyonu (signum/sgn)' olarak bilinir."
```

### py-veryeasy-ends-with-dot

```yaml
id: py-veryeasy-ends-with-dot
version: 1
language: python
engine: none
difficulty: very_easy
title: "Cümle noktayla bitiyor mu"
prompt: |
  Verilen bir metnin son karakterinin nokta ('.') olup olmadığını kontrol eden
  `ends_with_dot(sentence: str) -> bool` fonksiyonunu yazın. Metin boşsa IndexError
  fırlatılmamalı ve False dönmelidir.
constraints:
  - "Boş metin durumunda False dönmeli"
  - "Zaman ve alan karmaşıklığı O(1) olmalı"
expected:
  time: { ends_with_dot: "1" }
  space: "1"
concept_tags: [strings, boundary-conditions, edge-cases]
checklist_extra:
  - "Boş metinde sentence[-1] çağrısı yapılmaya çalışılıyor mu?"
  - "Metnin yerleşik metodu veya güvenli indeksleme mi tercih edildi?"
reference_solution_path: private/solutions/py-veryeasy-ends-with-dot.py
hint_ladder:
  1: "Metin boş olduğunda son karaktere erişmeye kalkışırsan ne olur?"
  2: "Metnin boş olmadığını doğrulamak veya yerleşik son ek kontrolünü kullanmak nasıl güvence sağlar?"
  3: "Bu yaklaşım 'son ek doğrulaması ve boş dize güvenliği' olarak bilinir."
```

### py-veryeasy-merge-two-tuples

```yaml
id: py-veryeasy-merge-two-tuples
version: 1
language: python
engine: none
difficulty: very_easy
title: "İki demeti birleştirme"
prompt: |
  İki tamsayı demetini (tuple) sırasıyla birleştirerek tek bir demet haline getiren
  `merge_tuples(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]` fonksiyonunu yazın.
  Demetlerden biri veya ikisi birden boş olabilir.
constraints:
  - "Girdi demetlerinin toplam uzunluğu n = len(a) + len(b) için süre O(n), alan O(n) olmalı"
  - "Sonuç nesnesi yeni bir demet olmalı"
expected:
  time: { merge_tuples: "n" }
  space: "n"
concept_tags: [data-structures, boundary-conditions]
checklist_extra:
  - "Demetlerden biri boş olduğunda diğeri hatasız yeni demet olarak dönüyor mu?"
  - "Demetlerin değiştirilemez yapısına uygun birleştirme mi yapıldı?"
reference_solution_path: private/solutions/py-veryeasy-merge-two-tuples.py
hint_ladder:
  1: "Python'da iki demeti birleştiren operatör hangisidir?"
  2: "Boş demet ile dolu bir demet birleştiğinde ne oluşur?"
  3: "Bu işlem 'değişmez dizi birleştirme (tuple concatenation)' olarak bilinir."
```

### py-veryeasy-is-palindrome-word

```yaml
id: py-veryeasy-is-palindrome-word
version: 1
language: python
engine: none
difficulty: very_easy
title: "Basit palindrom kelime kontrolü"
prompt: |
  Verilen tek bir kelimenin tersten okunuşuyla aynı olup olmadığını büyük/küçük harf
  farkını gözetmeksizin denetleyen `is_simple_palindrome(word: str) -> bool` fonksiyonunu yazın.
  Boş metin veya tek harfli kelimeler palindrom kabul edilmelidir (True dönmelidir).
constraints:
  - "Büyük/küçük harf duyarsız olmalı"
  - "n karakterli kelime için süre O(n), alan O(n) olmalı"
expected:
  time: { is_simple_palindrome: "n" }
  space: "n"
concept_tags: [strings, boundary-conditions]
checklist_extra:
  - "'Radar' gibi büyük ve küçük harf karışık kelimeler doğru değerlendiriliyor mu?"
  - "Boş metin durumunda True dönüyor mu?"
reference_solution_path: private/solutions/py-veryeasy-is-palindrome-word.py
hint_ladder:
  1: "Karşılaştırmadan önce kelimenin tüm harflerini aynı harf büyüklüğüne getirdin mi?"
  2: "Bir metnin tersini dilimleme (slicing) yöntemiyle nasıl elde edersin?"
  3: "Bu kontrol 'harf büyüklüğü normalizasyonu ve dize ters çevirme ile palindrom testi' olarak bilinir."
```

### py-veryeasy-clamp-percentage

```yaml
id: py-veryeasy-clamp-percentage
version: 1
language: python
engine: none
difficulty: very_easy
title: "Yüzde değerini 0-100 arasında sabitleme"
prompt: |
  Kullanıcıdan veya sensörden gelen yüzde değerini 0.0 ile 100.0 aralığına sabitleyen
  `clamp_percentage(value: float) -> float` fonksiyonunu yazın. Değer 0'dan küçükse 0.0,
  100'den büyükse 100.0, aralıktaysa kendisi dönmelidir.
constraints:
  - "Zaman ve alan karmaşıklığı O(1) olmalı"
  - "Sonuç float türünde olmalı"
expected:
  time: { clamp_percentage: "1" }
  space: "1"
concept_tags: [floating-point, boundary-conditions]
checklist_extra:
  - "0.0 ve 100.0 sınır değerleri tam olarak korunuyor mu?"
  - "Girdi tamsayı olduğunda dönüş float olarak sağlanıyor mu?"
reference_solution_path: private/solutions/py-veryeasy-clamp-percentage.py
hint_ladder:
  1: "Sayıyı önce alt sınırdan küçük mü diye test edip ardından üst sınırı kontrol edebilir misin?"
  2: "Python'da min ve max fonksiyonlarının bileşimiyle bu aralığı nasıl ifade edersin?"
  3: "Bu işlem 'alt ve üst sınır kırpma (boundary clamping)' olarak bilinir."
```

### py-veryeasy-remove-first-and-last

```yaml
id: py-veryeasy-remove-first-and-last
version: 1
language: python
engine: none
difficulty: very_easy
title: "İlk ve son karakteri atma"
prompt: |
  Verilen metnin ilk ve son karakterini atarak ortada kalan kısmı döndüren
  `remove_ends(text: str) -> str` fonksiyonunu yazın. Metin 2 veya daha az karakterden
  oluşuyorsa boş metin dönmelidir.
constraints:
  - "Metin uzunluğu <= 2 olduğunda boş metin dönmeli"
  - "n karakterli metin için süre O(n), alan O(n) olmalı"
expected:
  time: { remove_ends: "n" }
  space: "n"
concept_tags: [strings, boundary-conditions, edge-cases]
checklist_extra:
  - "Tek karakterli metinde dilimleme sonucunda beklenmeyen bir karakter kalıyor mu?"
  - "Boş metin girdiğinde IndexError önlendi mi?"
reference_solution_path: private/solutions/py-veryeasy-remove-first-and-last.py
hint_ladder:
  1: "Metin iki veya daha az karaktere sahip olduğunda geriye ne kalmalıdır?"
  2: "Python dize dilimlemesinde başlangıç ve bitiş indekslerini 1 ve -1 olarak belirlemek ne sağlar?"
  3: "Bu işlem 'dize kırpma dilimlemesi (string slice trimming)' olarak bilinir."
```

### py-veryeasy-calculate-bmi

```yaml
id: py-veryeasy-calculate-bmi
version: 1
language: python
engine: none
difficulty: very_easy
title: "Vücut kitle indeksi"
prompt: |
  Kilo (kg) ve boy (metre) değerlerini alarak vücut kitle indeksini (VKİ = kilo / (boy * boy))
  hesaplayan `calculate_bmi(weight_kg: float, height_m: float) -> float` fonksiyonunu yazın.
  Kilo veya boy sıfır veya negatifse ValueError fırlatılmalıdır.
constraints:
  - "weight_kg <= 0 veya height_m <= 0 durumunda ValueError fırlatılmalı"
  - "Zaman ve alan karmaşıklığı O(1) olmalı"
expected:
  time: { calculate_bmi: "1" }
  space: "1"
concept_tags: [floating-point, exceptions, input-validation]
checklist_extra:
  - "Boy sıfır olduğunda ZeroDivisionError yerine ValueError fırlatılıyor mu?"
  - "Formülde boyun karesi doğru alınıyor mu?"
reference_solution_path: private/solutions/py-veryeasy-calculate-bmi.py
hint_ladder:
  1: "Boy veya kilonun geçersizliğini bölme işlemine girmeden önce nasıl denetlersin?"
  2: "Bölme paydasında boyun karesini hesaplarken parantez önceliğine dikkat ettin mi?"
  3: "Bu işlem 'ön koşul doğrulaması ve formülsel metrik hesabı' olarak bilinir."
```

### py-veryeasy-count-uppercase

```yaml
id: py-veryeasy-count-uppercase
version: 1
language: python
engine: none
difficulty: very_easy
title: "Büyük harf sayısı"
prompt: |
  Bir metin içinde yer alan büyük harflerin toplam sayısını döndüren
  `count_uppercase_letters(text: str) -> int` fonksiyonunu yazın. Rakamlar, boşluklar
  ve noktalama işaretleri sayılmamalıdır. Metin boşsa 0 dönmelidir.
constraints:
  - "Rakam veya semboller büyük harf gibi sayılmamalı"
  - "n karakterli metin için süre O(n), alan O(1) olmalı"
expected:
  time: { count_uppercase_letters: "n" }
  space: "1"
concept_tags: [strings, boundary-conditions]
checklist_extra:
  - "Karakterin hem harf hem büyük olduğunu doğrulayan yöntem kullanılıyor mu?"
  - "Döngüde sayaç dışında gereksiz veri yapıları açılıyor mu?"
reference_solution_path: private/solutions/py-veryeasy-count-uppercase.py
hint_ladder:
  1: "Python'da bir karakterin büyük harf olup olmadığını sınayan dize metodu hangisidir?"
  2: "Metin üzerinde tek bir döngü kurup sayaç artırmak yeterli midir?"
  3: "Bu işlem 'karakter yükseklik sınaması ile doğrusal sayım' olarak bilinir."
```

### py-veryeasy-all-equal-three

```yaml
id: py-veryeasy-all-equal-three
version: 1
language: python
engine: none
difficulty: very_easy
title: "Üç sayının eşitliği"
prompt: |
  Verilen üç tamsayının üçünün de birbirine eşit olup olmadığını denetleyen
  `are_three_equal(a: int, b: int, c: int) -> bool` fonksiyonunu yazın.
  Yalnızca ikisi eşitse False dönmelidir.
constraints:
  - "Zaman ve alan karmaşıklığı O(1) olmalı"
  - "Sadece üçü de eşit olduğunda True dönmeli"
expected:
  time: { are_three_equal: "1" }
  space: "1"
concept_tags: [boundary-conditions, design]
checklist_extra:
  - "a == b ve b == c zincirleme karşılaştırması doğru çalışıyor mu?"
  - "a == b == c ifadesi kısa devre ve eşitlik mantığını karşılıyor mu?"
reference_solution_path: private/solutions/py-veryeasy-all-equal-three.py
hint_ladder:
  1: "Birinci sayının ikinciye, ikincinin de üçüncüye eşit olduğunu tek bir mantıksal ifadede nasıl yazarsın?"
  2: "Python'un zincirleme karşılaştırma (chained comparison) sözdizimini duydun mu?"
  3: "Bu mantık 'zincirleme eşitlik denetimi (transitive equality)' olarak bilinir."
```
---

## 2. Kolay (Easy) — 50 Soru

### py-easy-remove-duplicates-order

```yaml
id: py-easy-remove-duplicates-order
version: 1
language: python
engine: none
difficulty: easy
title: "Sırayı koruyarak tekrarları kaldırma"
prompt: |
  Bir tamsayı listesinde bulunan tekrar eden elemanları, elemanların ilk görülme
  sırasını kesinlikle bozmadan temizleyen `deduplicate_keep_order(items: list[int]) -> list[int]`
  fonksiyonunu yazın. Liste on binlerce eleman içerebilir. İç içe döngülerle karesel sürede
  arama yapmak yerine, daha önce görülen elemanları sabit sürede sorgulayabileceğiniz bir
  yapı ile doğrusal sürede çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
  - "Ek bellek kullanımı O(n) olmalı"
  - "Elemanların orijinal göreli sırası korunmalı"
expected:
  time: { deduplicate_keep_order: "n" }
  space: "n"
concept_tags: [hashing, data-structures, performance]
checklist_extra:
  - "Her eleman için listede 'in' araması yapılarak O(n^2) karmaşıklığa düşülüyor mu?"
  - "Görülen elemanları kaydetmek için küme (set) kullanılıyor mu?"
reference_solution_path: private/solutions/py-easy-remove-duplicates-order.py
hint_ladder:
  1: "Yeni bir elemanın daha önce eklenip eklenmediğini listede ararsan arama süresi ne olur?"
  2: "Daha önce ziyaret edilen elemanları O(1) sürede kontrol edebileceğin veri yapısı hangisidir?"
  3: "Bu yöntem 'ziyaret kümesi ile sıra korumalı tekilleştirme (hash set deduplication)' olarak bilinir."
```

### py-easy-anagram-check

```yaml
id: py-easy-anagram-check
version: 1
language: python
engine: none
difficulty: easy
title: "İki kelimenin anagram kontrolü"
prompt: |
  Verilen iki metnin birbirinin anagramı (harfleri ve frekansları birebir aynı, ancak
  sırası farklı veya aynı) olup olmadığını kontrol eden `is_anagram(s1: str, s2: str) -> bool`
  fonksiyonunu yazın. Boşluklar ve büyük/küçük harf farkı yok sayılmalıdır. Metinler
  yüz binlerce karakter uzunluğunda olabilir; bu nedenle sıralama tabanlı O(n log n)
  çözüm yerine karakter sayımı tabanlı O(n) sürede çalışan bir yöntem tercih edilmelidir.
constraints:
  - "Karakter sayıları n ve m için n == m iken çalışma süresi O(n) olmalı"
  - "Büyük/küçük harf ve boşluklar duyarsız olmalı"
  - "Ekstra bellek karakter alfabesi boyutuyla sınırlı O(1) olmalı"
expected:
  time: { is_anagram: "n" }
  space: "1"
concept_tags: [hashing, strings, performance]
checklist_extra:
  - "Metinler n log n süreli sort() işlemine tabi tutuluyor mu?"
  - "Karakterlerin frekans farkları kontrol edilirken negatif veya artık sayılar kalıyor mu?"
reference_solution_path: private/solutions/py-easy-anagram-check.py
hint_ladder:
  1: "İki metnin uzunlukları harf harf sayılmadan önce farklı çıkarsa hemen karar verebilir misin?"
  2: "Her iki metindeki harf sayılarını bir tabloda artırıp azaltarak tek geçişte nasıl doğrularsın?"
  3: "Bu yaklaşım 'karakter frekans sayımı ile anagram doğrulaması' olarak bilinir."
```

### py-easy-char-frequency

```yaml
id: py-easy-char-frequency
version: 1
language: python
engine: none
difficulty: easy
title: "Karakter frekans tablosu"
prompt: |
  Verilen bir metindeki her karakterin kaç kez geçtiğini gösteren bir sözlük oluşturan
  `build_frequency_map(text: str) -> dict[str, int]` fonksiyonunu yazın. Metin boşsa
  boş sözlük dönmelidir. Standart hazır sayaç kütüphanelerini içe aktarmadan kendi
  döngünüzle çözün.
constraints:
  - "n karakterli metin için çalışma süresi O(n) olmalı"
  - "Harici kütüphane veya koleksiyon modülü içe aktarılmamalı"
  - "Ek bellek alfabetik karakter sayısı k için O(k) olmalı"
expected:
  time: { build_frequency_map: "n" }
  space: "k"
concept_tags: [hashing, strings, data-structures]
checklist_extra:
  - "Sözlükte henüz bulunmayan bir anahtara doğrudan erişim KeyError üretiyor mu?"
  - "Döngü içinde text.count(c) çağrılarak karesel maliyet yaratılıyor mu?"
reference_solution_path: private/solutions/py-easy-char-frequency.py
hint_ladder:
  1: "Her karakter için tüm metni baştan saymak yerine tek bir döngüde sözlüğü nasıl güncellersin?"
  2: "Sözlükte anahtar yoksa varsayılan 0 değerini almak için sözlüğün hangi yöntemini kullanırsın?"
  3: "Bu desen 'sözlük tabanlı frekans haritası çıkarma (histogramming)' olarak bilinir."
```

### py-easy-merge-sorted-lists

```yaml
id: py-easy-merge-sorted-lists
version: 1
language: python
engine: none
difficulty: easy
title: "İki sıralı listeyi birleştirme"
prompt: |
  Küçükten büyüğe sıralı iki tamsayı listesini alıp yine sıralı tek bir liste halinde
  birleştiren `merge_sorted(a: list[int], b: list[int]) -> list[int]` fonksiyonunu yazın.
  İki listeyi uç uca ekleyip yeniden sort() çağırmak O((n+m) log(n+m)) sürer; oysa
  sıralı olmaları avantajını kullanarak iki işaretçi yardımıyla O(n + m) sürede birleştirin.
  n ve m listelerin eleman sayılarıdır.
constraints:
  - "n ve m elemanlı listeler için çalışma süresi O(n + m) olmalı"
  - "Dahili .sort() veya sorted() kullanılmamalı"
  - "Ek bellek sonuç listesi için O(n + m) olmalı"
expected:
  time: { merge_sorted: "n + m" }
  space: "n + m"
concept_tags: [data-structures, performance, boundary-conditions]
checklist_extra:
  - "Listelerden biri diğerinden önce tükendiğinde kalan elemanlar aktarılıyor mu?"
  - "Liste başından pop(0) yapılarak kaydırma maliyeti oluşturuluyor mu?"
reference_solution_path: private/solutions/py-easy-merge-sorted-lists.py
hint_ladder:
  1: "Her iki listenin başında iki ayrı indeks tutup küçük olanı seçerek ilerleyebilir misin?"
  2: "Bir liste bittiğinde diğer listenin geri kalan dilimini sonuca doğrudan nasıl eklersin?"
  3: "Bu algoritma 'iki işaretçili sıralı dizi birleştirme (two-pointer merge)' olarak bilinir."
```

### py-easy-find-missing-number

```yaml
id: py-easy-find-missing-number
version: 1
language: python
engine: none
difficulty: easy
title: "Dizideki eksik sayıyı bulma"
prompt: |
  0'dan n'e kadar olan tamsayıları içeren fakat içlerinden tam olarak bir tanesinin
  eksik olduğu n elemanlı bir liste verilmiştir. Eksik olan sayıyı bulan
  `find_missing_number(numbers: list[int]) -> int` fonksiyonunu yazın. Liste sıralı
  olmak zorunda değildir. Sıralama yapmadan ve ek bellek kullanmadan O(n) zaman ve
  O(1) alanda çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "Sıralama fonksiyonları kullanılmamalı"
expected:
  time: { find_missing_number: "n" }
  space: "1"
concept_tags: [boundary-conditions, performance, design]
checklist_extra:
  - "Eksik eleman 0 veya n olduğunda formül doğru sonucu veriyor mu?"
  - "Ekstra bir küme veya liste açılarak bellek kısıtı ihlal ediliyor mu?"
reference_solution_path: private/solutions/py-easy-find-missing-number.py
hint_ladder:
  1: "0'dan n'e kadar olan sayıların beklenen matematiksel toplamı nedir?"
  2: "Beklenen toplamdan listedeki sayıların gerçek toplamını çıkarırsan geriye ne kalır?"
  3: "Bu yöntem 'Gauss toplam farkı ile eksik eleman tespiti' olarak bilinir."
```

### py-easy-is-rotation

```yaml
id: py-easy-is-rotation
version: 1
language: python
engine: none
difficulty: easy
title: "Metin döndürme kontrolü"
prompt: |
  İki metin verildiğinde, ikincisinin birincisinin dairesel olarak döndürülmüş hali
  (örneğin 'merhaba' ve 'habamer') olup olmadığını kontrol eden
  `is_string_rotation(s1: str, s2: str) -> bool` fonksiyonunu yazın. İki metin de boşsa
  True dönmelidir. Uzunlukları farklıysa False dönmelidir.
constraints:
  - "Uzunlukları farklı dizgiler için hemen False dönmeli"
  - "n karakterli dizgiler için süre O(n), alan O(n) olmalı"
expected:
  time: { is_string_rotation: "n" }
  space: "n"
concept_tags: [strings, boundary-conditions, edge-cases]
checklist_extra:
  - "Uzunlukları eşit olmayan metinlerde gereksiz arama yapılıyor mu?"
  - "Boş metinlerin birbirinin dönüşü olduğu doğru değerlendiriliyor mu?"
reference_solution_path: private/solutions/py-easy-is-rotation.py
hint_ladder:
  1: "Bir metni kendisiyle birleştirip iki katına çıkarırsan (s1 + s1) içinde tüm olası dönüşler yer alır mı?"
  2: "s2'nin bu birleştirilmiş metin içinde bir alt metin olup olmadığını kontrol etmek yeterli midir?"
  3: "Bu teknik 'çift dize birleştirme ile dairesel döndürme doğrulaması' olarak bilinir."
```

### py-easy-common-elements

```yaml
id: py-easy-common-elements
version: 1
language: python
engine: none
difficulty: easy
title: "İki listenin ortak elemanları"
prompt: |
  Verilen iki tamsayı listesinde ortak olarak bulunan benzersiz elemanları bir liste
  olarak döndüren `find_common_elements(a: list[int], b: list[int]) -> list[int]`
  fonksiyonunu yazın. Sonuç listesindeki elemanlar benzersiz olmalı, tekrar etmemelidir.
  Her iki listenin uzunlukları n ve m olmak üzere O(n + m) sürede çalışmalıdır.
constraints:
  - "n ve m elemanlı listeler için çalışma süresi O(n + m) olmalı"
  - "Sonuç listesinde hiçbir eleman birden fazla yer almamalı"
expected:
  time: { find_common_elements: "n + m" }
  space: "n + m"
concept_tags: [hashing, data-structures, performance]
checklist_extra:
  - "İç içe döngü ile a'daki her eleman b'de aranarak O(n*m) süreye çıkılıyor mu?"
  - "Sonuç listesinde mükerrer elemanlar temizleniyor mu?"
reference_solution_path: private/solutions/py-easy-common-elements.py
hint_ladder:
  1: "Listelerden birini kümeye (set) dönüştürmek diğer listenin elemanlarını ararken ne kazandırır?"
  2: "Küme kesişim işlemi iki koleksiyon arasındaki ortaklığı nasıl tek adımda bulur?"
  3: "Bu işlem 'küme kesişimi ile doğrusal zamanlı ortak eleman bulma' olarak bilinir."
```

### py-easy-string-compression-rle

```yaml
id: py-easy-string-compression-rle
version: 1
language: python
engine: none
difficulty: easy
title: "Basit uzunluk kodlama sıkıştırması"
prompt: |
  Yalnızca harflerden oluşan bir metni ardışık tekrar sayılarıyla sıkıştıran
  `compress_string(text: str) -> str` fonksiyonunu yazın. Örneğin 'aabcccccaaa' verildiğinde
  'a2b1c5a3' dönmelidir. Eğer sıkıştırılmış metin orijinal metinden kısa değilse orijinal
  metin dönmelidir. Metin boşsa boş metin dönmelidir.
constraints:
  - "n karakterli metin için çalışma süresi O(n) olmalı"
  - "Döngüde string birleştirmek yerine liste biriktirip join kullanılmalı"
expected:
  time: { compress_string: "n" }
  space: "n"
concept_tags: [strings, performance, boundary-conditions]
checklist_extra:
  - "Döngü bittiğinde son karakter grubu sıkıştırmaya eklenmeden unutuluyor mu?"
  - "Sıkıştırılmış metin orijinalden daha uzun veya eşit olduğunda orijinal metin mi dönüyor?"
reference_solution_path: private/solutions/py-easy-string-compression-rle.py
hint_ladder:
  1: "Karakter dizisi üzerinde ilerlerken bir önceki karakterin sayacını ne zaman sıfırlayıp kaydetmelisin?"
  2: "Döngü bittiğinde elde kalan son karakter grubunu listeye eklemeyi hatırladın mı?"
  3: "Bu algoritma 'çalışma uzunluğu kodlaması (run-length encoding - RLE)' olarak bilinir."
```

### py-easy-group-by-parity

```yaml
id: py-easy-group-by-parity
version: 1
language: python
engine: none
difficulty: easy
title: "Sayıları tek ve çift olarak gruplama"
prompt: |
  Bir tamsayı listesindeki sayıları tekler ve çiftler olarak ayıran ve bir sözlük
  halinde `{'even': [...], 'odd': [...]}` döndüren `separate_parity(numbers: list[int]) -> dict[str, list[int]]`
  fonksiyonunu yazın. Orijinal listedeki göreli sıralar korunmalıdır. Liste boşsa her iki
  anahtarın değeri boş liste olmalıdır.
constraints:
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
  - "Orijinal eleman sırası bozulmamalı"
  - "Ek bellek O(n) olmalı"
expected:
  time: { separate_parity: "n" }
  space: "n"
concept_tags: [data-structures, boundary-conditions]
checklist_extra:
  - "Negatif sayılarda çift/tek kontrolü doğru çalışıyor mu?"
  - "Sıfır sayısı 'even' listesine dahil ediliyor mu?"
reference_solution_path: private/solutions/py-easy-group-by-parity.py
hint_ladder:
  1: "Her sayıyı gezerken ikiye bölümünden kalana göre iki listeden birine nasıl yönlendirirsin?"
  2: "Tek bir geçişte her iki listeyi aynı anda doldurabilir misin?"
  3: "Bu işlem 'koşullu sepetleme (bucketing by predicate)' olarak bilinir."
```

### py-easy-second-largest

```yaml
id: py-easy-second-largest
version: 1
language: python
engine: none
difficulty: easy
title: "Listedeki en büyük ikinci eleman"
prompt: |
  Bir tamsayı listesinde bulunan birbirinden farklı en büyük ikinci sayıyı döndüren
  `find_second_largest(numbers: list[int]) -> int | None` fonksiyonunu yazın. Eğer listede
  ikiden az farklı sayı varsa None dönmelidir. Listeyi sıralamadan (sort kullanmadan),
  tek bir geçişte O(n) zamanda ve O(1) alanda çözün.
constraints:
  - "Dahili sıralama (.sort() veya sorted()) kullanılmamalı"
  - "Tüm elemanlar eşitse veya ikiden az farklı eleman varsa None dönmeli"
  - "n elemanlı liste için süre O(n), alan O(1) olmalı"
expected:
  time: { find_second_largest: "n" }
  space: "1"
concept_tags: [boundary-conditions, performance, edge-cases]
checklist_extra:
  - "En büyük eleman tekrar ettiğinde (örneğin [10, 10, 5]) ikinci en büyük olarak 10 mu seçiliyor?"
  - "Başlangıç değerleri olarak 0 seçilip negatif sayılarda mantık çöküyor mu?"
reference_solution_path: private/solutions/py-easy-second-largest.py
hint_ladder:
  1: "En büyük (first) ve ikinci en büyük (second) için başlangıçta None değerini tutmak neden güvenlidir?"
  2: "Yeni bir sayı en büyükten büyük olduğunda second değerine ne atanmalıdır?"
  3: "Bu algoritma 'çift değişken takibi ile tek geçişli sıra istatistiği' olarak bilinir."
```

### py-easy-valid-parentheses-simple

```yaml
id: py-easy-valid-parentheses-simple
version: 1
language: python
engine: none
difficulty: easy
title: "Basit parantez dizisi dengesi"
prompt: |
  Yalnızca '(' ve ')' karakterlerinden oluşan bir metnin parantez dengesinin geçerli
  olup olmadığını denetleyen `is_valid_simple_parentheses(s: str) -> bool` fonksiyonunu
  yazın. Her açılan parantez mutlaka kapanmalı ve hiçbir zaman kapatma parantezi
  açılmamış bir parantezden önce gelmemelidir. Boş metin geçerli kabul edilir (True).
constraints:
  - "Kapatma parantezi sayısı hiçbir anda açma parantezi sayısını aşmamalı"
  - "n karakterli metin için süre O(n), ek alan O(1) olmalı"
expected:
  time: { is_valid_simple_parentheses: "n" }
  space: "1"
concept_tags: [strings, boundary-conditions, performance]
checklist_extra:
  - "Sayaç döngü sırasında negatif değere indiğinde erken çıkış yapılıyor mu?"
  - "Döngü sonunda sayaç sıfırdan farklı kaldığında False dönüyor mu?"
reference_solution_path: private/solutions/py-easy-valid-parentheses-simple.py
hint_ladder:
  1: "Tek tip parantez varken tam bir yığın (stack) yapısı yerine sadece bir tamsayı sayacı kullanabilir misin?"
  2: "Sayacın sıfırın altına düşmesi ne anlama gelir?"
  3: "Bu yöntem 'denge sayacı ile parantez geçerliliği (balance counter)' olarak bilinir."
```

### py-easy-find-single-number

```yaml
id: py-easy-find-single-number
version: 1
language: python
engine: none
difficulty: easy
title: "Tekil kalan sayıyı bulma"
prompt: |
  Bir elemanı hariç tüm elemanlarının tam olarak iki kez tekrar ettiği bir tamsayı listesi
  verilmiştir. Tekrar etmeyen tek sayıyı bulan `find_single_number(numbers: list[int]) -> int`
  fonksiyonunu yazın. Ekstra bir liste veya sözlük açmadan, O(n) zaman ve O(1) sabit
  ek bellek kullanarak çözün.
constraints:
  - "Çalışma süresi O(n) olmalı"
  - "Ek bellek kullanımı kesinlikle O(1) olmalı (sözlük/küme kullanılmamalı)"
expected:
  time: { find_single_number: "n" }
  space: "1"
concept_tags: [performance, design]
checklist_extra:
  - "Ekstra bellek tahsis edilerek O(n) bellek kısıtı çiğneniyor mu?"
  - "Bit düzeyinde XOR operatörü (^) doğru akümüle ediliyor mu?"
reference_solution_path: private/solutions/py-easy-find-single-number.py
hint_ladder:
  1: "Bir sayıyı kendisiyle XOR işlemine sokarsan sonuç ne olur?"
  2: "0 ile bir sayıyı XOR işlemine sokarsan ne elde edersin?"
  3: "Bu teknik 'bit düzeyinde XOR toplamı ile eşsiz eleman tespiti' olarak bilinir."
```

### py-easy-title-case-words

```yaml
id: py-easy-title-case-words
version: 1
language: python
engine: none
difficulty: easy
title: "Kelimelerin ilk harflerini büyütme"
prompt: |
  Bir cümledeki tüm kelimelerin yalnızca ilk harfini büyük, diğer harflerini küçük
  harfe dönüştüren `to_title_case(sentence: str) -> str` fonksiyonunu yazın. Kelimeler
  arasındaki birden fazla boşluk korunmalı veya tek boşluğa indirgenmesi yerine orijinal
  boşluk yapısına saygı duyulmalıdır. Metin boşsa boş metin dönmelidir.
constraints:
  - "n karakterli metin için çalışma süresi O(n) olmalı"
  - "Ekstra bellek O(n) olmalı"
expected:
  time: { to_title_case: "n" }
  space: "n"
concept_tags: [strings, parsing, boundary-conditions]
checklist_extra:
  - "Aralardaki birden çok boşluk veya sekme karakteri kayba uğruyor mu?"
  - "Kelimelerin ikinci ve sonraki harfleri küçük harfe çevriliyor mu?"
reference_solution_path: private/solutions/py-easy-title-case-words.py
hint_ladder:
  1: "Kelimeleri ayırırken boşlukları korumak için metni karakter karakter tarayabilir misin?"
  2: "Bir harfin kelime başı olduğunu önceki karakterin boşluk olup olmamasından nasıl anlarsın?"
  3: "Bu algoritma 'durum makinesi mantığıyla başlık dönüşümü (title casing)' olarak bilinir."
```

### py-easy-reverse-vowels

```yaml
id: py-easy-reverse-vowels
version: 1
language: python
engine: none
difficulty: easy
title: "Yalnızca sesli harfleri ters çevirme"
prompt: |
  Verilen bir metindeki sessiz harflerin ve diğer karakterlerin konumunu korurken,
  yalnızca sesli harflerin (a, e, i, o, u hem büyük hem küçük) kendi aralarındaki sırasını
  tersine çeviren `reverse_vowels(text: str) -> str` fonksiyonunu yazın. Örneğin
  'merhaba' verildiğinde 'marhabe' dönmelidir. İki işaretçi yardımıyla O(n) sürede çözün.
constraints:
  - "n karakterli metin için çalışma süresi O(n) olmalı"
  - "Büyük ve küçük tüm sesli harfler kapsanmalı"
  - "Ek bellek O(n) olmalı"
expected:
  time: { reverse_vowels: "n" }
  space: "n"
concept_tags: [strings, performance, boundary-conditions]
checklist_extra:
  - "İşaretçiler birbirini geçtiğinde döngü güvenle sonlanıyor mu?"
  - "Metinde hiç sesli harf olmadığında metin aynen korunuyor mu?"
reference_solution_path: private/solutions/py-easy-reverse-vowels.py
hint_ladder:
  1: "Metnin başından ve sonundan iki işaretçi başlatıp sesli harf bulana kadar ilerletebilir misin?"
  2: "İki işaretçi de sesli harfe denk geldiğinde karakterlerin yerini nasıl değiştirirsin?"
  3: "Bu yöntem 'iki uçtan yaklaşan iki işaretçi tekniği (two pointers)' olarak bilinir."
```

### py-easy-matrix-diagonal-sum

```yaml
id: py-easy-matrix-diagonal-sum
version: 1
language: python
engine: none
difficulty: easy
title: "Kare matrisin köşegen toplamı"
prompt: |
  n x n boyutunda bir tamsayı kare matrisi verildiğinde, birincil (sol üstten sağ alta)
  ve ikincil (sağ üstten sol alta) köşegenler üzerindeki elemanların toplamını hesaplayan
  `diagonal_sum(matrix: list[list[int]]) -> int` fonksiyonunu yazın. İki köşegenin
  kesiştiği merkez eleman (n tek sayı ise) toplama yalnızca bir kez dahil edilmelidir.
constraints:
  - "n x n matris için çalışma süresi O(n) olmalı (iç içe iki döngü kullanılmamalı)"
  - "Ek bellek kullanımı O(1) olmalı"
  - "Merkez eleman tek sayı boyutlu matrislerde çift sayılmamalı"
expected:
  time: { diagonal_sum: "n" }
  space: "1"
concept_tags: [data-structures, performance, boundary-conditions]
checklist_extra:
  - "İç içe iki döngü kurularak O(n^2) gereksiz tarama yapılıyor mu?"
  - "n tek olduğunda tam ortadaki eleman iki kez mi toplanıyor?"
reference_solution_path: private/solutions/py-easy-matrix-diagonal-sum.py
hint_ladder:
  1: "Her i satırında birincil ve ikincil köşegen elemanlarının sütun indeksleri formülle nedir?"
  2: "i == n - 1 - i olduğunda aynı elemana mı denk gelinir; bu durumu nasıl telafi edersin?"
  3: "Bu yaklaşım 'doğrusal matris köşegen taraması ve kesişim tekilleştirmesi' olarak bilinir."
```

### py-easy-majority-element-simple

```yaml
id: py-easy-majority-element-simple
version: 1
language: python
engine: none
difficulty: easy
title: "Çoğunluk elemanı"
prompt: |
  n elemanlı bir tamsayı listesinde n // 2 defadan daha fazla tekrar eden bir çoğunluk
  elemanının kesinlikle var olduğu garanti edilmiştir. Bu çoğunluk elemanını bulan
  `majority_element(numbers: list[int]) -> int` fonksiyonunu yazın. Ekstra bellek
  açmadan O(n) zaman ve O(1) alanda çalışmalıdır.
constraints:
  - "Çalışma süresi O(n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
expected:
  time: { majority_element: "n" }
  space: "1"
concept_tags: [performance, design]
checklist_extra:
  - "Sözlük açılarak O(n) ek alan kullanılıyor mu?"
  - "Sayaç sıfıra düştüğünde aday eleman doğru güncelleniyor mu?"
reference_solution_path: private/solutions/py-easy-majority-element-simple.py
hint_ladder:
  1: "Bir aday ve bir sayaç tutarak, aynı sayı geldiğinde sayacı artırıp farklı sayıda azaltsan ne olur?"
  2: "Çoğunluk elemanının sayısı diğer tüm elemanların toplamından fazlaysa sayaç sonunda hangi elemanı işaret eder?"
  3: "Bu algoritma 'Boyer-Moore çoğunluk oylama algoritması (voting algorithm)' olarak bilinir."
```

### py-easy-move-zeroes

```yaml
id: py-easy-move-zeroes
version: 1
language: python
engine: none
difficulty: easy
title: "Sıfırları sona taşıma"
prompt: |
  Bir tamsayı listesindeki tüm sıfırları listenin sonuna taşıyan, ancak sıfır olmayan
  elemanların göreli sırasını kesinlikle koruyan `move_zeroes_in_place(numbers: list[int]) -> None`
  fonksiyonunu yazın. Fonksiyon yeni bir liste oluşturmamalı, işlemi doğrudan orijinal
  liste üzerinde (in-place) O(n) zaman ve O(1) alanda gerçekleştirmelidir.
constraints:
  - "Yeni liste oluşturulmamalı; işlem liste üzerinde yerinde (in-place) yapılmalı"
  - "n elemanlı liste için çalışma süresi O(n), ek alan O(1) olmalı"
  - "Sıfır olmayan elemanların sırası değişmemeli"
expected:
  time: { move_zeroes_in_place: "n" }
  space: "1"
concept_tags: [data-structures, performance, boundary-conditions]
checklist_extra:
  - "numbers.remove(0) veya pop() döngüde kullanılarak her adımda O(n) kaydırma yapılıyor mu?"
  - "Yazma işaretçisi sıfır olmayan tüm elemanlar bittiğinde kalan indekslere sıfır yazıyor mu?"
reference_solution_path: private/solutions/py-easy-move-zeroes.py
hint_ladder:
  1: "Sıfır olmayan bir eleman gördüğünde onu listenin en başındaki ilk uygun boşluğa nasıl yazarsın?"
  2: "Tüm sıfır olmayanlar yazıldıktan sonra geriye kalan indeksleri neyle doldurmalısın?"
  3: "Bu yöntem 'iki işaretçi ile yerinde sıkıştırma ve doldurma' olarak bilinir."
```

### py-easy-palindrome-sentence

```yaml
id: py-easy-palindrome-sentence
version: 1
language: python
engine: none
difficulty: easy
title: "Cümle düzeyinde palindrom denetimi"
prompt: |
  Verilen bir cümlenin noktalama işaretleri ve boşlukları yok sayıldığında ve tüm harfler
  küçük kabul edildiğinde palindrom olup olmadığını denetleyen
  `is_sentence_palindrome(sentence: str) -> bool` fonksiyonunu yazın. Örneğin
  'Ey Edip, Adana\'da pide ye!' bir palindromdur. Ekstra temizlenmiş bir string kopyalamadan,
  iki işaretçi ile O(n) zamanda ve O(1) ek alanda çözün.
constraints:
  - "Alfanümerik olmayan karakterler atlanmalı"
  - "Büyük/küçük harf duyarsız olmalı"
  - "Ek bellek kullanımı O(1) olmalı (yeni dize oluşturulmamalı)"
expected:
  time: { is_sentence_palindrome: "n" }
  space: "1"
concept_tags: [strings, performance, boundary-conditions]
checklist_extra:
  - "Tüm harfleri temizleyip yeni bir dize oluşturarak O(n) ek alan kullanılıyor mu?"
  - "İşaretçiler alfanümerik olmayan karakterleri geçerken birbirini aşma kontrolü yapılıyor mu?"
reference_solution_path: private/solutions/py-easy-palindrome-sentence.py
hint_ladder:
  1: "Metnin başından ve sonundan ilerlerken alfanümerik olmayan karakterleri işaretçiyi kaydırarak atlayabilir misin?"
  2: "İki tarafta da geçerli bir harfe ulaşıldığında küçük harf karşılaştırması nasıl yapılır?"
  3: "Bu yöntem 'yerinde iki işaretçili alfanümerik filtreleme ve palindrom testi' olarak bilinir."
```

### py-easy-list-chunking

```yaml
id: py-easy-list-chunking
version: 1
language: python
engine: none
difficulty: easy
title: "Listeyi sabit boyutlu parçalara bölme"
prompt: |
  Bir tamsayı listesini belirtilen `chunk_size` boyutundaki alt listelere bölen
  `chunk_list(items: list[int], chunk_size: int) -> list[list[int]]` fonksiyonunu yazın.
  Listenin son parçası `chunk_size`'dan daha az eleman içerebilir. `chunk_size` sıfır veya
  negatifse ValueError fırlatılmalıdır. Liste boşsa boş liste dönmelidir.
constraints:
  - "chunk_size <= 0 durumunda ValueError fırlatılmalı"
  - "n elemanlı liste için süre O(n), alan O(n) olmalı"
expected:
  time: { chunk_list: "n" }
  space: "n"
concept_tags: [data-structures, exceptions, input-validation]
checklist_extra:
  - "Son parça chunk_size boyutuna tam bölünmediğinde eksik elemanlar kayboluyor mu?"
  - "Döngü chunk_size adımlarıyla atlamak yerine tek tek eleman mı kopyalıyor?"
reference_solution_path: private/solutions/py-easy-list-chunking.py
hint_ladder:
  1: "Python range fonksiyonunda adım büyüklüğü (step) belirleyerek başlangıç indekslerini nasıl üretirsin?"
  2: "Her adımda listeyi `items[i:i + chunk_size]` dilimlemesiyle almak ne sağlar?"
  3: "Bu desen 'diziyi sabit aralıklı dilimleme ile parçalama (chunking/batching)' olarak bilinir."
```

### py-easy-count-occurrences-dict

```yaml
id: py-easy-count-occurrences-dict
version: 1
language: python
engine: none
difficulty: easy
title: "Eleman tekrar sayıları"
prompt: |
  Bir tamsayı listesindeki her bir sayının kaç defa geçtiğini hesaplayıp sayı ve adet
  çiftlerinden oluşan bir sözlük döndüren `count_frequencies(numbers: list[int]) -> dict[int, int]`
  fonksiyonunu yazın. Dahili Counter sınıfını kullanmadan, doğrudan sözlük işlemleriyle
  O(n) sürede çözün.
constraints:
  - "collections.Counter veya harici araçlar kullanılmamalı"
  - "n elemanlı liste için süre O(n), benzersiz k eleman için alan O(k) olmalı"
expected:
  time: { count_frequencies: "n" }
  space: "k"
concept_tags: [hashing, data-structures, performance]
checklist_extra:
  - "Anahtar bulunamadığında KeyError oluşmaması için dict.get() kullanıldı mı?"
  - "Her eleman için listede baştan count() çağrılarak O(n^2) karmaşıklığa yol açılıyor mu?"
reference_solution_path: private/solutions/py-easy-count-occurrences-dict.py
hint_ladder:
  1: "Listeyi tek bir döngüyle gezerken her sayıyı sözlük anahtarı olarak nasıl kaydedersin?"
  2: "Sözlükte anahtar varsa değerini 1 artırıp yoksa 1 ile başlatmayı nasıl tek satırda yazarsın?"
  3: "Bu yaklaşım 'karma tablosu akümülatörü ile frekans sayımı' olarak bilinir."
```

### py-easy-first-non-repeating-char

```yaml
id: py-easy-first-non-repeating-char
version: 1
language: python
engine: none
difficulty: easy
title: "İlk tekrar etmeyen karakter"
prompt: |
  Bir metin içinde yalnızca bir kez geçen ilk karakteri bulan
  `first_unique_character(s: str) -> str | None` fonksiyonunu yazın. Tekrar etmeyen
  karakter yoksa veya metin boşsa None dönmelidir. n karakterli metin için O(n^2)
  süreli iç içe aramalar yerine, iki geçişli bir algoritmayla O(n) sürede çözün.
constraints:
  - "n karakterli metin için çalışma süresi O(n) olmalı"
  - "Hiç benzersiz karakter yoksa None dönmeli"
  - "Ekstra bellek alfabetik karakter sayısı k için O(k) olmalı"
expected:
  time: { first_unique_character: "n" }
  space: "k"
concept_tags: [strings, hashing, performance]
checklist_extra:
  - "Her karakter için s.count(c) çağrılarak n*n tarama yapılıyor mu?"
  - "İlk geçişte frekanslar çıkarılıp ikinci geçişte ilk frekansı 1 olan eleman seçiliyor mu?"
reference_solution_path: private/solutions/py-easy-first-non-repeating-char.py
hint_ladder:
  1: "İlk turda tüm karakterlerin sayısını bir sözlükte toplarsan ikinci turda ne yapabilirsin?"
  2: "İkinci turda metni baştan sona tarayıp sözlükteki sayısı 1 olan ilk karakteri gördüğün an ne dönersin?"
  3: "Bu desen 'iki geçişli frekans sorgulaması (two-pass hash map scan)' olarak bilinir."
```

### py-easy-is-monotonic

```yaml
id: py-easy-is-monotonic
version: 1
language: python
engine: none
difficulty: easy
title: "Monoton liste denetimi"
prompt: |
  Bir tamsayı listesinin monoton olup olmadığını (tamamen artan veya tamamen azalan)
  denetleyen `is_monotonic(numbers: list[int]) -> bool` fonksiyonunu yazın. Ardışık
  elemanların birbirine eşit olması monotonluğu bozmaz. Boş veya tek elemanlı listeler
  monoton kabul edilmelidir. Tek bir geçişte O(n) zaman ve O(1) alanda çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
expected:
  time: { is_monotonic: "n" }
  space: "1"
concept_tags: [boundary-conditions, performance, design]
checklist_extra:
  - "Hem artış hem azalış bayrağını takip eden bir mantık kuruldu mu?"
  - "Aynı anda hem artan hem azalan bir adım görüldüğünde hemen False dönülüyor mu?"
reference_solution_path: private/solutions/py-easy-is-monotonic.py
hint_ladder:
  1: "Başlangıçta listenin hem artan hem azalan olabileceğini varsayabilir misin?"
  2: "Bir adımda bir önceki elemandan küçük, başka bir adımda büyük bir eleman gördüğünde ne olur?"
  3: "Bu yöntem 'çift durum bayrağı ile tek geçişli monotonluk analizi' olarak bilinir."
```

### py-easy-intersection-unique

```yaml
id: py-easy-intersection-unique
version: 1
language: python
engine: none
difficulty: easy
title: "İki listenin tekil kesişimi"
prompt: |
  İki tamsayı listesinde ortak olan elemanları, sonuç listesinde her eleman en fazla
  bir kez yer alacak şekilde döndüren `unique_intersection(nums1: list[int], nums2: list[int]) -> list[int]`
  fonksiyonunu yazın. Listelerin uzunlukları n ve m olmak üzere O(n + m) sürede çalışmalıdır.
constraints:
  - "n ve m elemanlı listeler için süre O(n + m) olmalı"
  - "Sonuç listesinde mükerrer eleman bulunmamalı"
expected:
  time: { unique_intersection: "n + m" }
  space: "n + m"
concept_tags: [hashing, data-structures, boundary-conditions]
checklist_extra:
  - "Sonuç listesinde eleman tekrarı engellendi mi?"
  - "Kümeye dönüştürme işlemiyle arama süresi O(1)'e çekildi mi?"
reference_solution_path: private/solutions/py-easy-intersection-unique.py
hint_ladder:
  1: "Her iki listeyi de küme (set) haline getirdiğinde kesişim operatörü ne döndürür?"
  2: "Elde ettiğin kümeyi tekrar listeye dönüştürmek kaç adım sürer?"
  3: "Bu işlem 'küme tabanlı tekil kesişim (set intersection)' olarak bilinir."
```

### py-easy-find-pivot-index

```yaml
id: py-easy-find-pivot-index
version: 1
language: python
engine: none
difficulty: easy
title: "Denge indeksi (pivot) bulma"
prompt: |
  Bir tamsayı listesinde, solundaki sayıların toplamının sağındaki sayıların toplamına
  eşit olduğu en küçük indeksi (denge noktası) döndüren `find_pivot_index(numbers: list[int]) -> int`
  fonksiyonunu yazın. Listenin dışındaki elemanların toplamı 0 kabul edilir. Böyle bir
  indeks yoksa -1 dönmelidir. Her indeks için sağı ve solu baştan toplamak yerine, toplam
  sayıdan faydalanarak O(n) zamanda çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
expected:
  time: { find_pivot_index: "n" }
  space: "1"
concept_tags: [performance, boundary-conditions, design]
checklist_extra:
  - "Her adımda dilimleme (slice sum) yapılarak O(n^2) maliyet yaratılıyor mu?"
  - "Sağdaki toplam: toplam - sol_toplam - mevcut_eleman ilişkisi kullanılıyor mu?"
reference_solution_path: private/solutions/py-easy-find-pivot-index.py
hint_ladder:
  1: "Döngüye başlamadan önce listenin genel toplamını bir kez hesaplayabilir misin?"
  2: "İlerlerken sol toplamı biriktirirsen, sağ toplamı genel toplamdan nasıl anında çıkarırsın?"
  3: "Bu yöntem 'toplam farkı ile tek geçişli denge noktası tespiti' olarak bilinir."
```

### py-easy-hamming-distance

```yaml
id: py-easy-hamming-distance
version: 1
language: python
engine: none
difficulty: easy
title: "İki metin arasındaki Hamming mesafesi"
prompt: |
  Eşit uzunluktaki iki metin arasında karşılıklı farklı olan karakterlerin sayısını
  hesaplayan `hamming_distance(s1: str, s2: str) -> int` fonksiyonunu yazın. Metinlerin
  uzunlukları eşit değilse ValueError fırlatılmalıdır.
constraints:
  - "len(s1) != len(s2) durumunda ValueError fırlatılmalı"
  - "n karakterli dizgiler için süre O(n), alan O(1) olmalı"
expected:
  time: { hamming_distance: "n" }
  space: "1"
concept_tags: [strings, exceptions, input-validation]
checklist_extra:
  - "Uzunlukları eşit olmayan metinlerde IndexError yerine ValueError fırlatılıyor mu?"
  - "Döngü iki dizeyi paralel olarak tek geçişte inceliyor mu?"
reference_solution_path: private/solutions/py-easy-hamming-distance.py
hint_ladder:
  1: "İki dizeyi karşılıklı eşleştirmek için Python'ın zip fonksiyonunu nasıl kullanırsın?"
  2: "Karakterlerin birbirine eşit olmadığı durumları sayan bir sayaç nasıl kurgulanır?"
  3: "Bu metrik 'farklılaşan karakter sayısı ve Hamming mesafesi' olarak bilinir."
```

### py-easy-filter-dict-by-value

```yaml
id: py-easy-filter-dict-by-value
version: 1
language: python
engine: none
difficulty: easy
title: "Sözlüğü değere göre filtreleme"
prompt: |
  Bir anahtar-değer sözlüğünde değerleri belirli bir eşik değerden (`min_value`)
  büyük veya eşit olan çiftleri seçerek yeni bir sözlük döndüren
  `filter_dict_by_min_value(data: dict[str, int], min_value: int) -> dict[str, int]`
  fonksiyonunu yazın. Orijinal sözlük değiştirilmemelidir.
constraints:
  - "Orijinal sözlük mutasyona uğramamalı"
  - "n elemanlı sözlük için çalışma süresi O(n), alan O(n) olmalı"
expected:
  time: { filter_dict_by_min_value: "n" }
  space: "n"
concept_tags: [hashing, data-structures, design]
checklist_extra:
  - "Döngü sırasında orijinal sözlükten del ile eleman silinerek RuntimeError alınıyor mu?"
  - "Sözlük üreteci (dict comprehension) ile yeni sözlük üretildi mi?"
reference_solution_path: private/solutions/py-easy-filter-dict-by-value.py
hint_ladder:
  1: "Bir sözlüğü döngüyle gezerken aynı anda içinden eleman silmek neden hataya yol açar?"
  2: "Sözlük üreteci sözdizimi ile koşulu sağlayan anahtar-değer çiftlerini nasıl toplarsın?"
  3: "Bu işlem 'sözlük üreteci ile değişmez filtreleme (dictionary comprehension)' olarak bilinir."
```

### py-easy-running-sum

```yaml
id: py-easy-running-sum
version: 1
language: python
engine: none
difficulty: easy
title: "Kümülatif toplam dizisi"
prompt: |
  Bir tamsayı listesi verildiğinde, her i indeksindeki elemanın 0'dan i'ye kadar olan
  tüm elemanların toplamına eşit olduğu yeni bir liste döndüren
  `running_sum(numbers: list[int]) -> list[int]` fonksiyonunu yazın. Her adımda listenin
  başından o ana kadar olan kısmı yeniden toplamak O(n^2) süreceğinden, önceki toplamı
  biriktirerek O(n) sürede çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
  - "Ek bellek dönen liste için O(n) olmalı"
expected:
  time: { running_sum: "n" }
  space: "n"
concept_tags: [performance, data-structures, design]
checklist_extra:
  - "Her adımda sum(numbers[:i+1]) çağrılarak karesel süreye düşülüyor mu?"
  - "Önceki adımın kümülatif toplamı bir akümülatör değişkeninde tutuluyor mu?"
reference_solution_path: private/solutions/py-easy-running-sum.py
hint_ladder:
  1: "Mevcut elemanın kümülatif toplamı, bir önceki kümülatif toplama ne eklenerek bulunur?"
  2: "Tüm dilimi baştan toplamak yerine tek bir toplama işlemiyle ilerleyebilir misin?"
  3: "Bu dizi yapısı 'ön ek toplamı (prefix sum)' olarak bilinir."
```

### py-easy-is-subsequence

```yaml
id: py-easy-is-subsequence
version: 1
language: python
engine: none
difficulty: easy
title: "Alt dizi (subsequence) denetimi"
prompt: |
  `s` metninin `t` metninin bir alt dizisi olup olmadığını denetleyen
  `is_subsequence(s: str, t: str) -> bool` fonksiyonunu yazın. Bir alt dizi, orijinal
  metindeki karakterlerin sırası bozulmadan, bazı karakterlerin silinmesiyle elde edilen
  yeni metindir. Boş metin s her zaman alt dizidir. İki işaretçi kullanarak O(len(t))
  sürede çözün.
constraints:
  - "s uzunluğu n, t uzunluğu m iken çalışma süresi O(m) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
expected:
  time: { is_subsequence: "m" }
  space: "1"
concept_tags: [strings, performance, boundary-conditions]
checklist_extra:
  - "s metninin sonuna ulaşıldığında hemen True dönerek erken çıkış yapılıyor mu?"
  - "t metni bitmesine rağmen s tamamlanamadığında False dönüyor mu?"
reference_solution_path: private/solutions/py-easy-is-subsequence.py
hint_ladder:
  1: "s ve t üzerinde iki ayrı işaretçi tutarak t'de eşleşen her harfte s işaretçisini 1 artırabilir misin?"
  2: "s işaretçisi s'nin uzunluğuna ulaştığında bu neyi kanıtlar?"
  3: "Bu yöntem 'açgözlü iki işaretçi ile alt dizi doğrulaması' olarak bilinir."
```

### py-easy-flatten-shallow-list

```yaml
id: py-easy-flatten-shallow-list
version: 1
language: python
engine: none
difficulty: easy
title: "Tek kademe iç içe listeyi düzleştirme"
prompt: |
  Listelerden oluşan bir listeyi tek bir düz liste haline getiren
  `flatten_shallow(nested: list[list[int]]) -> list[int]` fonksiyonunu yazın. Yalnızca
  bir kademe derinlik düzleştirilmelidir. Boş alt listeler atlanmalıdır. Toplam eleman
  sayısı n için O(n) zamanda çözün.
constraints:
  - "Toplam n eleman için çalışma süresi O(n) olmalı"
  - "Sonuç listesi için ek bellek O(n) olmalı"
expected:
  time: { flatten_shallow: "n" }
  space: "n"
concept_tags: [data-structures, design]
checklist_extra:
  - "Döngüde result = result + sublist yapılarak her adımda listenin kopyalanması önlendi mi?"
  - "İç içe liste üreteci veya extend metodu doğru kullanıldı mı?"
reference_solution_path: private/solutions/py-easy-flatten-shallow-list.py
hint_ladder:
  1: "Bir listeye başka bir listenin tüm elemanlarını topluca eklemek için hangi metot kullanılır?"
  2: "+ operatörü ile liste birleştirmek neden her adımda yeni bir liste oluşturur?"
  3: "Bu işlem 'liste uzatma ve sığ düzleştirme (shallow flattening)' olarak bilinir."
```

### py-easy-max-consecutive-ones

```yaml
id: py-easy-max-consecutive-ones
version: 1
language: python
engine: none
difficulty: easy
title: "Ardışık 1'lerin azami uzunluğu"
prompt: |
  Yalnızca 0 ve 1 sayılarından oluşan bir listede art arda gelen en uzun 1 dizisinin
  uzunluğunu bulan `max_consecutive_ones(nums: list[int]) -> int` fonksiyonunu yazın.
  Liste hiç 1 içermiyorsa 0 dönmelidir. Tek bir geçişte O(n) zaman ve O(1) alanda çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
expected:
  time: { max_consecutive_ones: "n" }
  space: "1"
concept_tags: [boundary-conditions, performance, design]
checklist_extra:
  - "Liste 1 ile bittiğinde son sayaç en yüksek değerle karşılaştırılmadan atlanıyor mu?"
  - "0 görüldüğünde anlık sayaç sıfırlanıyor mu?"
reference_solution_path: private/solutions/py-easy-max-consecutive-ones.py
hint_ladder:
  1: "Bir anlık sayaç ve bir de şimdiye kadar görülen en büyük sayacı tutabilir misin?"
  2: "0 geldiğinde anlık sayacı sıfırlamadan önce en büyük sayacı güncelliyor musun?"
  3: "Bu teknik 'kayar sayaç ile ardışık seri takibi' olarak bilinir."
```

### py-easy-count-words-frequency

```yaml
id: py-easy-count-words-frequency
version: 1
language: python
engine: none
difficulty: easy
title: "Metindeki kelimelerin frekans dağılımı"
prompt: |
  Bir cümledeki kelimelerin kaçar defa geçtiğini bulan `word_frequency_map(text: str) -> dict[str, int]`
  fonksiyonunu yazın. Kelimeler boşluklara göre ayrılmalı, noktalama işaretleri temizlenmeli
  ve büyük/küçük harf farkı kaldırılmalıdır. Harici sayaç modülleri kullanılmamalıdır.
constraints:
  - "Kelimeler küçük harfe dönüştürülmeli"
  - "n kelimeli metin için çalışma süresi O(n), alan O(n) olmalı"
expected:
  time: { word_frequency_map: "n" }
  space: "n"
concept_tags: [strings, hashing, parsing]
checklist_extra:
  - "Noktalama işaretleri kelimelerin parçası olarak kalıyor mu?"
  - "Büyük harfle başlayan kelimeler küçük harflilerle birleşiyor mu?"
reference_solution_path: private/solutions/py-easy-count-words-frequency.py
hint_ladder:
  1: "Metni kelimelere bölmeden önce noktalama işaretlerini ve harf büyüklüğünü nasıl normalize edersin?"
  2: "Kelimeleri bir sözlükte toplarken her kelime için sayacı nasıl artırırsın?"
  3: "Bu süreç 'metin normalizasyonu ve sözlük frekans eşlemesi' olarak bilinir."
```

### py-easy-caesar-cipher

```yaml
id: py-easy-caesar-cipher
version: 1
language: python
engine: none
difficulty: easy
title: "Sezar şifreleme"
prompt: |
  Verilen metindeki yalnızca İngilizce harfleri belirtilen `shift` miktarı kadar alfabede
  kaydıran `caesar_cipher(text: str, shift: int) -> str` fonksiyonunu yazın. Büyük harfler
  büyük harfe, küçük harfler küçük harfe dönüşmelidir. Sayılar, boşluklar ve noktalama
  işaretleri aynen korunmalıdır. `shift` negatif veya 26'dan büyük olabilir.
constraints:
  - "shift % 26 normalizasyonu uygulanmalı"
  - "Harf dışı karakterler değiştirilmemeli"
  - "n karakterli metin için süre O(n), alan O(n) olmalı"
expected:
  time: { caesar_cipher: "n" }
  space: "n"
concept_tags: [strings, boundary-conditions, design]
checklist_extra:
  - "shift 26'dan büyük veya negatif olduğunda modulo aritmetiği doğru işliyor mu?"
  - "Büyük harfler alfabe sonundan dönüp 'A'ya sarıyor mu?"
reference_solution_path: private/solutions/py-easy-caesar-cipher.py
hint_ladder:
  1: "Kaydırma miktarını 0-25 aralığına çekmek için hangi matematiksel operatörü kullanırsın?"
  2: "Bir harfin alfabedeki sırasını bulmak için ord() ve chr() fonksiyonları nasıl eşleştirilir?"
  3: "Bu dönüşüm 'modüler aritmetik ile harf kaydırma şifrelemesi' olarak bilinir."
```

### py-easy-square-sorted-array

```yaml
id: py-easy-square-sorted-array
version: 1
language: python
engine: none
difficulty: easy
title: "Sıralı dizinin karelerini sıralı döndürme"
prompt: |
  Küçükten büyüğe sıralı, içinde negatif sayılar da bulunabilen bir tamsayı listesi
  verilmiştir. Her elemanın karesini alıp yine sıralı tek bir liste olarak döndüren
  `sorted_squares(numbers: list[int]) -> list[int]` fonksiyonunu yazın. Kareleri alıp
  `sort()` çağırmak O(n log n) sürer; iki işaretçi tekniğiyle O(n) sürede çözün.
constraints:
  - "Çalışma süresi O(n) olmalı (dahili sıralama kullanılmamalı)"
  - "Ek bellek sonuç listesi için O(n) olmalı"
expected:
  time: { sorted_squares: "n" }
  space: "n"
concept_tags: [performance, data-structures, design]
checklist_extra:
  - "Kareleri alıp sonradan sort() çağrılarak n log n karmaşıklığa çıkılıyor mu?"
  - "Listenin iki ucundan kareleri karşılaştırıp sonuç listesini sondan başa dolduran iki işaretçi kurgulandı mı?"
reference_solution_path: private/solutions/py-easy-square-sorted-array.py
hint_ladder:
  1: "Negatif sayıların kareleri büyük olabileceğinden en büyük kareler dizinin neresinde yer alır?"
  2: "İki uçtaki elemanların mutlak değerlerini karşılaştırıp büyük olanı yeni dizinin sonuna yazabilir misin?"
  3: "Bu teknik 'çift uçlu işaretçi ile ters yönde sıralı dizi doldurma' olarak bilinir."
```

### py-easy-invert-dictionary

```yaml
id: py-easy-invert-dictionary
version: 1
language: python
engine: none
difficulty: easy
title: "Sözlük anahtar ve değerlerini ters çevirme"
prompt: |
  Bir sözlükteki anahtarları değer, değerleri anahtar yapan yeni bir sözlük döndüren
  `invert_unique_dict(d: dict[str, int]) -> dict[int, str]` fonksiyonunu yazın.
  Sözlükteki değerlerin benzersiz olduğu garanti edilmiştir. Orijinal sözlük
  değiştirilmemelidir.
constraints:
  - "Orijinal sözlük mutasyona uğramamalı"
  - "n elemanlı sözlük için çalışma süresi O(n), alan O(n) olmalı"
expected:
  time: { invert_unique_dict: "n" }
  space: "n"
concept_tags: [hashing, data-structures, design]
checklist_extra:
  - "Orijinal sözlük boş olduğunda boş sözlük dönüyor mu?"
  - "Sözlük üreteci ile tersine çevirme temiz bir biçimde yapıldı mı?"
reference_solution_path: private/solutions/py-easy-invert-dictionary.py
hint_ladder:
  1: "Sözlüğün .items() metodunu kullanarak (k, v) çiftlerini nasıl tersine çevirirsin?"
  2: "Tersine çevrilen çiftlerle yeni bir sözlük kurmak için sözlük üreteci nasıl yazılır?"
  3: "Bu işlem 'anahtar-değer tersleme (dictionary inversion)' olarak bilinir."
```

### py-easy-count-vowel-consonant-ratio

```yaml
id: py-easy-count-vowel-consonant-ratio
version: 1
language: python
engine: none
difficulty: easy
title: "Sesli ve sessiz harf sayısı oranı"
prompt: |
  Bir metindeki İngilizce sesli harf sayısının sessiz harf sayısına oranını hesaplayan
  `vowel_to_consonant_ratio(text: str) -> float | None` fonksiyonunu yazın. Harf dışındaki
  karakterler hesaba katılmamalıdır. Hiç sessiz harf yoksa (sıfıra bölme durumunda)
  None dönmelidir.
constraints:
  - "Sessiz harf sayısı sıfır olduğunda None dönmeli"
  - "n karakterli metin için süre O(n), alan O(1) olmalı"
expected:
  time: { vowel_to_consonant_ratio: "n" }
  space: "1"
concept_tags: [strings, floating-point, edge-cases]
checklist_extra:
  - "Sessiz harf 0 iken ZeroDivisionError fırlatılmadan None dönüyor mu?"
  - "Harf olmayan rakam ve noktalama işaretleri sessiz harf sayılıyor mu?"
reference_solution_path: private/solutions/py-easy-count-vowel-consonant-ratio.py
hint_ladder:
  1: "Bir karakterin harf olup olmadığını nasıl denetlersin?"
  2: "Bölme işlemi yapmadan önce paydanın sıfır olup olmadığını nasıl kontrol edersin?"
  3: "Bu yaklaşım 'karakter sınıflandırması ve sıfıra bölme koruması' olarak bilinir."
```

### py-easy-find-difference-element

```yaml
id: py-easy-find-difference-element
version: 1
language: python
engine: none
difficulty: easy
title: "İki metin arasındaki eklenen karakter"
prompt: |
  `s` metninin karakterleri karıştırılıp içine rastgele bir ek karakter eklenerek `t`
  metni oluşturulmuştur. Eklenen bu tek karakteri bulan `find_added_character(s: str, t: str) -> str`
  fonksiyonunu yazın. Sıralama yapmadan, karakterlerin sayısal ASCII değerlerinden ya da
  XOR mantığından yararlanarak O(len(t)) sürede çözün.
constraints:
  - "Sıralama yapılmamalı; süre O(len(t)) olmalı"
  - "Ek bellek O(1) olmalı"
expected:
  time: { find_added_character: "n" }
  space: "1"
concept_tags: [strings, performance, design]
checklist_extra:
  - "İki metin sıralanıp O(n log n) sürece çıkılıyor mu?"
  - "ASCII karakter kodlarının toplam farkı veya XOR yöntemi kullanıldı mı?"
reference_solution_path: private/solutions/py-easy-find-difference-element.py
hint_ladder:
  1: "t metnindeki tüm karakterlerin ord() toplamından s metnindekileri çıkarırsan ne elde edersin?"
  2: "Elde ettiğin tamsayı farkını chr() ile karaktere nasıl dönüştürürsün?"
  3: "Bu teknik 'ASCII toplam farkı ile fazlalık karakter tespiti' olarak bilinir."
```

### py-easy-longest-common-prefix-simple

```yaml
id: py-easy-longest-common-prefix-simple
version: 1
language: python
engine: none
difficulty: easy
title: "Kelimelerde en uzun ortak ön ek"
prompt: |
  Verilen bir metin listesindeki tüm kelimelerin paylaştığı en uzun ortak ön eki
  (başlangıç harflerini) bulan `longest_common_prefix(words: list[str]) -> str`
  fonksiyonunu yazın. Ortak ön ek yoksa veya liste boşsa boş metin dönmelidir.
  n kelime sayısı ve m en kısa kelimenin uzunluğu olmak üzere O(n * m) zamanda çözün.
constraints:
  - "Liste boşken boş metin dönmeli"
  - "n kelime ve m karakter için çalışma süresi O(n * m) olmalı"
expected:
  time: { longest_common_prefix: "n*m" }
  space: "m"
concept_tags: [strings, boundary-conditions, edge-cases]
checklist_extra:
  - "Kelimelerden biri diğerinden daha kısa olduğunda IndexError önlendi mi?"
  - "Kelimelerden biri boş metin ise hemen boş metin dönülüyor mu?"
reference_solution_path: private/solutions/py-easy-longest-common-prefix-simple.py
hint_ladder:
  1: "İlk kelimenin harflerini tek tek diğer tüm kelimelerle aynı indekste karşılaştırabilir misin?"
  2: "Herhangi bir kelime bittiğinde veya harf uyuşmadığında o ana kadar biriken ön eki nasıl döndürürsün?"
  3: "Bu algoritma 'düşey karakter taraması ile ortak ön ek bulma (vertical scanning)' olarak bilinir."
```

### py-easy-symmetric-difference

```yaml
id: py-easy-symmetric-difference
version: 1
language: python
engine: none
difficulty: easy
title: "İki listenin simetrik farkı"
prompt: |
  İki tamsayı listesinde bulunan, ancak her ikisinde birden bulunmayan (yalnızca birinde
  olan) elemanları tekilleştirilmiş bir liste olarak döndüren
  `symmetric_difference_list(a: list[int], b: list[int]) -> list[int]` fonksiyonunu yazın.
  n ve m listelerin eleman sayıları olmak üzere O(n + m) sürede çalışmalıdır.
constraints:
  - "n ve m elemanlı listeler için süre O(n + m) olmalı"
  - "Sonuç listesinde mükerrer eleman yer almamalı"
expected:
  time: { symmetric_difference_list: "n + m" }
  space: "n + m"
concept_tags: [hashing, data-structures, design]
checklist_extra:
  - "İki listede de olan ortak elemanlar sonuca yanlışlıkla sızıyor mu?"
  - "Kümelerin simetrik fark operatörü (^) tercih edildi mi?"
reference_solution_path: private/solutions/py-easy-symmetric-difference.py
hint_ladder:
  1: "Kümelerde yalnızca bir kümede bulunan elemanları veren işlem hangisidir?"
  2: "(A - B) birleşim (B - A) ifadesini Python set operatörleriyle nasıl tek adımda yazarsın?"
  3: "Bu işlem 'kümelerin simetrik farkı (symmetric difference)' olarak bilinir."
```

### py-easy-pascals-triangle-row

```yaml
id: py-easy-pascals-triangle-row
version: 1
language: python
engine: none
difficulty: easy
title: "Pascal üçgeninin k. satırı"
prompt: |
  Pascal üçgeninin 0 tabanlı indekslenen `k`'ıncı satırını bir tamsayı listesi olarak
  üreten `get_pascals_triangle_row(k: int) -> list[int]` fonksiyonunu yazın. Örneğin
  k = 0 için [1], k = 3 için [1, 3, 3, 1] dönmelidir. k negatifse ValueError fırlatılmalıdır.
  Bir önceki satırı kullanarak adım adım O(k^2) zaman ve O(k) ek bellekle hesaplayın.
constraints:
  - "k < 0 durumunda ValueError fırlatılmalı"
  - "Ek bellek kullanımı O(k) olmalı"
  - "Çalışma süresi O(k^2) olmalı"
expected:
  time: { get_pascals_triangle_row: "k^2" }
  space: "k"
concept_tags: [data-structures, exceptions, design]
checklist_extra:
  - "Tüm üçgeni bellekte tutarak O(k^2) gereksiz bellek harcanıyor mu?"
  - "Yalnızca önceki satırı güncelleyerek O(k) alan içinde kalındı mı?"
reference_solution_path: private/solutions/py-easy-pascals-triangle-row.py
hint_ladder:
  1: "Bir satırdaki her eleman, bir önceki satırın hangi iki komşu elemanının toplamıdır?"
  2: "Tüm üçgeni bellekte tutmak yerine sadece önceki satırı elinde tutmak yeterli midir?"
  3: "Bu hesaplama 'Pascal satırı dinamik inşası ve alan optimizasyonu' olarak bilinir."
```

### py-easy-truncate-words

```yaml
id: py-easy-truncate-words
version: 1
language: python
engine: none
difficulty: easy
title: "Metni kelime sınırından kırpma"
prompt: |
  Bir metni en fazla `k` adet kelime içerecek şekilde kırpan ve eğer metin kırpıldıysa
  sonuna '...' ekleyen `truncate_by_words(text: str, k: int) -> str` fonksiyonunu yazın.
  Metin zaten k veya daha az kelimeden oluşuyorsa sonuna üç nokta eklenmemeli, orijinal
  hali dönmelidir. k <= 0 ise ve metin boş değilse yalnızca '...' dönmelidir.
constraints:
  - "Metin kısaltılmadıysa '...' eklenmemeli"
  - "n kelimeli metin için çalışma süresi O(n), alan O(n) olmalı"
expected:
  time: { truncate_by_words: "n" }
  space: "n"
concept_tags: [strings, boundary-conditions, parsing]
checklist_extra:
  - "Kelimelerin sayısı k'ya eşit olduğunda gereksiz '...' ekleniyor mu?"
  - "Metin boş olduğunda doğru şekilde boş metin dönüyor mu?"
reference_solution_path: private/solutions/py-easy-truncate-words.py
hint_ladder:
  1: "Metni kelimelerine ayırdıktan sonra listenin uzunluğu ile k'yı nasıl karşılaştırırsın?"
  2: "İlk k kelimeyi alıp aralarına boşluk koyarak birleştirmek için ne kullanırsın?"
  3: "Bu işlem 'kelime sınırında dize kısaltma (word-aware truncation)' olarak bilinir."
```

### py-easy-find-all-duplicates

```yaml
id: py-easy-find-all-duplicates
version: 1
language: python
engine: none
difficulty: easy
title: "Listede yinelenen elemanları bulma"
prompt: |
  Bir tamsayı listesinde birden fazla kez geçen tüm sayıları tekilleştirilmiş bir liste
  olarak döndüren `find_duplicates(numbers: list[int]) -> list[int]` fonksiyonunu yazın.
  Sayıların sonuçtaki sırası önemli değildir. n elemanlı liste için O(n) zamanda ve
  O(n) ek bellekle çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
  - "Sonuç listesinde her yinelenen sayı yalnızca bir kez bulunmalı"
expected:
  time: { find_duplicates: "n" }
  space: "n"
concept_tags: [hashing, data-structures, performance]
checklist_extra:
  - "3 kez geçen bir sayı sonuç listesine iki kez ekleniyor mu?"
  - "Görülenler ve tekrarlananlar için iki ayrı küme yapısı düşünüldü mü?"
reference_solution_path: private/solutions/py-easy-find-all-duplicates.py
hint_ladder:
  1: "Bir sayıyı ilk kez gördüğünde bir kümeye, ikinci kez gördüğünde sonuç kümesine atabilir misin?"
  2: "Sonuçları kümede tutmak üç veya daha fazla tekrarda mükerrer kaydı nasıl engeller?"
  3: "Bu yaklaşım 'çift küme ile tekrar eden eleman ayrıştırması' olarak bilinir."
```

### py-easy-is-power-of-two

```yaml
id: py-easy-is-power-of-two
version: 1
language: python
engine: none
difficulty: easy
title: "Sayının ikinin kuvveti olup olmadığı"
prompt: |
  Pozitif bir tamsayının 2'nin bir kuvveti (1, 2, 4, 8, 16...) olup olmadığını kontrol eden
  `is_power_of_two(n: int) -> bool` fonksiyonunu yazın. n sıfır veya negatifse False
  dönmelidir. Döngü kurmadan, ikili sistemdeki bit özelliklerinden faydalanarak
  O(1) sürede çözün.
constraints:
  - "Döngü veya özyineleme kullanılmamalı; O(1) zamanda çalışmalı"
  - "n <= 0 değerlerinde False dönmeli"
expected:
  time: { is_power_of_two: "1" }
  space: "1"
concept_tags: [boundary-conditions, design, performance]
checklist_extra:
  - "n <= 0 sınır durumlarında n & (n - 1) denetimi kısa devre ile korunuyor mu?"
  - "Döngü ile sürekli 2'ye bölmek yerine bit işlemi tercih edildi mi?"
reference_solution_path: private/solutions/py-easy-is-power-of-two.py
hint_ladder:
  1: "İkinin kuvveti olan bir sayının ikilik (binary) gösteriminde kaç tane 1 biti bulunur?"
  2: "n sayısından 1 çıkarıp n ile 'VE' (&) işlemine sokarsan ne elde edersin?"
  3: "Bu yöntem 'bit manipülasyonu ile ikinin kuvveti sınaması (n & (n - 1) == 0)' olarak bilinir."
```

### py-easy-reverse-words-in-sentence

```yaml
id: py-easy-reverse-words-in-sentence
version: 1
language: python
engine: none
difficulty: easy
title: "Cümledeki kelimelerin sırasını tersine çevirme"
prompt: |
  Bir cümledeki kelimelerin sırasını tersine çeviren, ancak kelimelerin kendi harf
  sırasını koruyan `reverse_words(sentence: str) -> str` fonksiyonunu yazın.
  Örneğin 'gökyüzü masmavi bugün' verildiğinde 'bugün masmavi gökyüzü' dönmelidir.
  Baştaki, sondaki veya aradaki fazla boşluklar temizlenmeli ve kelimeler arasında
  yalnızca tek bir boşluk kalmalıdır.
constraints:
  - "n kelimeli metin için çalışma süresi O(n), alan O(n) olmalı"
  - "Fazla boşluklar tek boşluğa normalize edilmeli"
expected:
  time: { reverse_words: "n" }
  space: "n"
concept_tags: [strings, parsing, design]
checklist_extra:
  - "Metin başında ve sonundaki boşluklar temizleniyor mu?"
  - "Kelimeleri ayırmak için split() parametresiz kullanılarak ardışık boşluklar yutuldu mu?"
reference_solution_path: private/solutions/py-easy-reverse-words-in-sentence.py
hint_ladder:
  1: "Python'da split() fonksiyonunu parametresiz çağırmak boşlukları nasıl ele alır?"
  2: "Elde edilen kelime listesini tersine çevirip aralarına boşluk koyarak nasıl birleştirirsin?"
  3: "Bu işlem 'dizge parçalama, liste tersleme ve birleştirme' olarak bilinir."
```

### py-easy-range-overlap

```yaml
id: py-easy-range-overlap
version: 1
language: python
engine: none
difficulty: easy
title: "İki sayı aralığının çakışması"
prompt: |
  [start1, end1] ve [start2, end2] şeklinde verilen iki kapalı sayı aralığının ortak
  en az bir noktada çakışıp çakışmadığını denetleyen
  `do_ranges_overlap(r1: tuple[int, int], r2: tuple[int, int]) -> bool` fonksiyonunu yazın.
  Uç noktaların birbirine değmesi (örneğin [1, 5] ve [5, 10]) çakışma kabul edilmelidir.
constraints:
  - "Zaman ve alan karmaşıklığı O(1) olmalı"
  - "Uç nokta temasları True dönmeli"
expected:
  time: { do_ranges_overlap: "1" }
  space: "1"
concept_tags: [boundary-conditions, design]
checklist_extra:
  - "Birinci aralığın ikincinin tamamen içinde kaldığı durum doğru değerlendiriliyor mu?"
  - "Aralıkların çakışmama koşulu (end1 < start2 or end2 < start1) tersine çevrildi mi?"
reference_solution_path: private/solutions/py-easy-range-overlap.py
hint_ladder:
  1: "İki aralığın kesinlikle çakışmadığı iki durumu düşün: biri tamamen diğerinin solundaysa ne olur?"
  2: "Çakışmama durumunun mantıksal değilini (NOT) alarak çakışmayı nasıl ifade edersin?"
  3: "Bu kontrol 'aralık kesişim testi (interval overlap test)' olarak bilinir."
```

### py-easy-sum-of-digits

```yaml
id: py-easy-sum-of-digits
version: 1
language: python
engine: none
difficulty: easy
title: "Basamaklar toplamı"
prompt: |
  Verilen bir tamsayının tüm basamaklarının sayısal toplamını hesaplayan
  `sum_of_digits(n: int) -> int` fonksiyonunu yazın. Sayı negatifse eksi işareti yok
  sayılmalı ve mutlak değerinin basamakları toplanmalıdır. Örneğin -123 için 1+2+3 = 6
  dönmelidir. Metne dönüştürmek yerine matematiksel bölme ve kalan işlemleriyle çözün.
constraints:
  - "Dizeye dönüştürme (str(n)) kullanılmamalı"
  - "Basamak sayısı d = log10(|n|) için süre O(d), alan O(1) olmalı"
expected:
  time: { sum_of_digits: "d" }
  space: "1"
concept_tags: [boundary-conditions, design]
checklist_extra:
  - "n negatif olduğunda sonsuz döngü veya negatif kalan oluşması engellendi mi?"
  - "n = 0 durumunda döngü hatasız 0 veriyor mu?"
reference_solution_path: private/solutions/py-easy-sum-of-digits.py
hint_ladder:
  1: "Bir sayının son basamağını 10'a göre kalan (% 10) alarak nasıl elde edersin?"
  2: "Sayının son basamağını atmak için 10'a tamsayı bölmesi (// 10) nasıl kullanılır?"
  3: "Bu işlem 'aritmetik basamak ayrıştırma (digit extraction by modulo)' olarak bilinir."
```

### py-easy-key-with-max-value

```yaml
id: py-easy-key-with-max-value
version: 1
language: python
engine: none
difficulty: easy
title: "Sözlükte en büyük değere sahip anahtar"
prompt: |
  Bir anahtar-sayısal değer sözlüğünde en büyük değere sahip olan anahtarı döndüren
  `key_with_max_value(data: dict[str, int]) -> str | None` fonksiyonunu yazın. Sözlük
  boşsa None dönmelidir. Birden fazla anahtar aynı maksimum değere sahipse alfabetik
  olarak ilk gelen anahtar seçilmelidir.
constraints:
  - "Boş sözlük için None dönmeli"
  - "Eşitlik durumunda alfabetik olarak en küçük anahtar dönmeli"
  - "n elemanlı sözlük için çalışma süresi O(n), alan O(1) olmalı"
expected:
  time: { key_with_max_value: "n" }
  space: "1"
concept_tags: [hashing, boundary-conditions, design]
checklist_extra:
  - "Eşitlik durumunda alfabetik öncelik kriteri atlanıyor mu?"
  - "Boş sözlük kontrolü yapılmadan max() çağrılıp ValueError fırlatılıyor mu?"
reference_solution_path: private/solutions/py-easy-key-with-max-value.py
hint_ladder:
  1: "Sözlük boş olduğunda hata almamak için fonksiyonun başında ne kontrolü yapmalısın?"
  2: "Değer büyük olduğunda veya değer eşitken anahtar alfabetik küçük olduğunda adayı nasıl güncellersin?"
  3: "Bu mantık 'bileşik öncelikli doğrusal arama (custom comparator scan)' olarak bilinir."
```

### py-easy-transpose-2x2-matrix

```yaml
id: py-easy-transpose-2x2-matrix
version: 1
language: python
engine: none
difficulty: easy
title: "Matris transpozu"
prompt: |
  r satır ve c sütundan oluşan bir tamsayı matrisinin transpozunu (satır ve sütunların
  yer değiştirdiği c x r boyutlu matris) hesaplayan `transpose_matrix(matrix: list[list[int]]) -> list[list[int]]`
  fonksiyonunu yazın. Matris boşsa boş liste dönmelidir.
constraints:
  - "r satır ve c sütun için süre O(r * c), ek alan O(r * c) olmalı"
  - "Orijinal matris bozulmamalı"
expected:
  time: { transpose_matrix: "r*c" }
  space: "r*c"
concept_tags: [data-structures, design, boundary-conditions]
checklist_extra:
  - "Boş liste veya boş satır ([[]]) durumlarında IndexError önlendi mi?"
  - "Döngü veya liste üreteci satır ve sütun indislerini doğru takas ediyor mu?"
reference_solution_path: private/solutions/py-easy-transpose-2x2-matrix.py
hint_ladder:
  1: "Yeni matrisin i'inci satır j'inci sütunundaki eleman orijinal matrisin neresinden gelir?"
  2: "Python'da zip(*matrix) sözdizimi satır ve sütunları dönüştürmede nasıl kullanılır?"
  3: "Bu işlem 'matris devriği alma (matrix transposition)' olarak bilinir."
```

### py-easy-remove-element-in-place

```yaml
id: py-easy-remove-element-in-place
version: 1
language: python
engine: none
difficulty: easy
title: "Belirli bir değeri dizide yerinde eleme"
prompt: |
  Bir tamsayı listesi ve hedef değer verildiğinde, hedef değere eşit olan tüm elemanları
  liste üzerinde yerinde (in-place) kaldırıp geriye kalan geçerli eleman sayısını
  döndüren `remove_element_in_place(nums: list[int], val: int) -> int` fonksiyonunu yazın.
  Listenin ilk k elemanı hedef dışındaki sayılardan oluşmalıdır. Ekstra liste açmadan
  O(n) zaman ve O(1) alanda çalışmalıdır.
constraints:
  - "Yeni bir liste oluşturulmamalı; yerinde değiştirilmeli"
  - "n elemanlı liste için süre O(n), alan O(1) olmalı"
expected:
  time: { remove_element_in_place: "n" }
  space: "1"
concept_tags: [data-structures, performance, boundary-conditions]
checklist_extra:
  - "Her eleman silindiğinde nums.remove() çağrılarak O(n^2) kaydırma yapılıyor mu?"
  - "Yazma işaretçisi ile iki işaretçi yaklaşımı uygulandı mı?"
reference_solution_path: private/solutions/py-easy-remove-element-in-place.py
hint_ladder:
  1: "Okuma ve yazma için iki ayrı indeks tutup hedef olmayanları yazma indeksine yazabilir misin?"
  2: "Yazma indeksi her başarılı yazmada 1 artarsa döngü sonunda neyi gösterir?"
  3: "Bu yöntem 'hızlı ve yavaş işaretçi ile yerinde eleman filtreleme' olarak bilinir."
```

### py-easy-generate-acronym

```yaml
id: py-easy-generate-acronym
version: 1
language: python
engine: none
difficulty: easy
title: "Metinden kısaltma (akronim) üretme"
prompt: |
  Verilen bir başlıktaki her kelimenin ilk harfini alarak büyük harfli bir kısaltma
  (örneğin 'As Soon As Possible' için 'ASAP') üreten `generate_acronym(phrase: str) -> str`
  fonksiyonunu yazın. Birden fazla boşluk içeren metinlerde fazlalık boşluklar atlanmalıdır.
  Metin boşsa veya harf içermiyorsa boş metin dönmelidir.
constraints:
  - "n kelimeli metin için çalışma süresi O(n), alan O(n) olmalı"
  - "Tüm harfler büyük harfe dönüştürülmeli"
expected:
  time: { generate_acronym: "n" }
  space: "n"
concept_tags: [strings, parsing, boundary-conditions]
checklist_extra:
  - "split() kullanılarak boş kelimeler ve ardışık boşluklar temizlendi mi?"
  - "Kısaltma oluşturulurken liste toplanıp join ile mi birleştirildi?"
reference_solution_path: private/solutions/py-easy-generate-acronym.py
hint_ladder:
  1: "Metni kelimelere böldükten sonra her kelimenin ilk karakterine nasıl erişirsin?"
  2: "Bu karakterleri büyük harfe çevirip aralarında boşluk olmadan nasıl birleştirirsin?"
  3: "Bu işlem 'akronim türetme ve baş harf birleştirme' olarak bilinir."
```

### py-easy-detect-capital-use

```yaml
id: py-easy-detect-capital-use
version: 1
language: python
engine: none
difficulty: easy
title: "Büyük harf kullanım kuralı denetimi"
prompt: |
  Bir kelimenin büyük harf kullanımının kurallara uygun olup olmadığını denetleyen
  `detect_capital_use(word: str) -> bool` fonksiyonunu yazın. Geçerli durumlar:
  1) Tüm harfleri büyük ('USA'), 2) Tüm harfleri küçük ('leetcode'), 3) Yalnızca ilk harfi
  büyük ('Google'). Bunların dışındaki tüm durumlar (örneğin 'FlaG') False dönmelidir.
  Kelime boşsa True dönmelidir.
constraints:
  - "n karakterli kelime için çalışma süresi O(n), alan O(1) olmalı"
  - "Her üç geçerli durum da doğru değerlendirilmeli"
expected:
  time: { detect_capital_use: "n" }
  space: "1"
concept_tags: [strings, boundary-conditions, design]
checklist_extra:
  - "Tek karakterli kelimelerde (örneğin 'A' veya 'a') doğru çalışıyor mu?"
  - "Kelimeyi birden çok kez taramak yerine tek bir geçişte büyük harf sayısı sayılarak mı çözüldü?"
reference_solution_path: private/solutions/py-easy-detect-capital-use.py
hint_ladder:
  1: "Kelimenin tamamındaki büyük harf sayısını ve ilk harfin büyük olup olmadığını sayarsan ne elde edersin?"
  2: "Büyük harf sayısı 0 ise, n ise ya da 1 olup ilk harfse kural sağlanır mı?"
  3: "Bu denetim 'sayım temelli dize kuralı sınıflandırması' olarak bilinir."
```

---

## 3. Orta (Medium) — 50 Soru

### py-medium-longest-substring-k-distinct

```yaml
id: py-medium-longest-substring-k-distinct
version: 1
language: python
engine: none
difficulty: medium
title: "En fazla k farklı karakter içeren en uzun alt metin"
prompt: |
  Bir metin ve `k` pozitif tamsayısı verildiğinde, içerisinde en fazla `k` adet farklı
  karakter barındıran en uzun kesintisiz alt metnin uzunluğunu bulan
  `length_of_longest_substring_k_distinct(s: str, k: int) -> int` fonksiyonunu yazın.
  k sıfırsa veya metin boşsa 0 dönmelidir. Metin yüz binlerce karakter içerebileceğinden,
  tüm alt metinleri karesel sürede üretmek yerine kayan pencere yaklaşımıyla O(len(s))
  sürede çözün.
constraints:
  - "n = len(s) karakterli metin için çalışma süresi O(n) olmalı"
  - "Ek bellek kullanımı farklı karakter sayısı k için O(k) olmalı"
  - "k <= 0 durumunda 0 dönmeli"
expected:
  time: { length_of_longest_substring_k_distinct: "n" }
  space: "k"
concept_tags: [strings, performance, hashing, boundary-conditions]
checklist_extra:
  - "Penceredeki farklı karakter sayısı k'yı aştığında sol sınır tek adımda mı yoksa döngüyle mi daraltılıyor?"
  - "Karakter sayısı 0'a inen harf sözlükten silinerek len(dict) <= k dengesi korunuyor mu?"
reference_solution_path: private/solutions/py-medium-longest-substring-k-distinct.py
hint_ladder:
  1: "Pencereye yeni bir karakter eklediğinde farklı karakter sayısı k'yı aşarsa sol sınırı nereye kadar çekmelisin?"
  2: "Sözlükte tuttuğun frekans değeri sıfıra düştüğünde anahtarı sözlükten tamamen kaldırmazsan ne olur?"
  3: "Bu yöntem 'dinamik genişleyip daralan kayan pencere (sliding window with hash map)' olarak bilinir."
```

### py-medium-binary-search-rotated

```yaml
id: py-medium-binary-search-rotated
version: 1
language: python
engine: none
difficulty: medium
title: "Döndürülmüş sıralı listede arama"
prompt: |
  Küçükten büyüğe sıralı ve elemanları benzersiz bir tamsayı listesi, bilinmeyen bir
  pivot indeksinden dairesel olarak döndürülmüştür (örneğin [4, 5, 6, 7, 0, 1, 2]).
  Bu listede verilen `target` değerini arayan ve bulunursa indeksini, bulunamazsa -1
  döndüren `search_rotated_array(nums: list[int], target: int) -> int` fonksiyonunu yazın.
  Doğrusal tarama yerine, her adımda arama aralığını yarıya indiren O(log n) süreli
  bir algoritma tasarlayın.
constraints:
  - "n elemanlı liste için çalışma süresi kesinlikle O(log n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "Aranan eleman bulunamazsa -1 dönmeli"
expected:
  time: { search_rotated_array: "log n" }
  space: "1"
concept_tags: [performance, boundary-conditions, design]
checklist_extra:
  - "Diziyi doğrusal gezerek O(n) maliyete çıkılıyor mu?"
  - "Orta noktanın solunun mu yoksa sağının mı sıralı olduğu tespit edilerek hedef o aralıkta mı aranıyor?"
reference_solution_path: private/solutions/py-medium-binary-search-rotated.py
hint_ladder:
  1: "Orta elemanı seçtiğinde sol yarım ile sağ yarımdan en az birinin kesinlikle düzgün sıralı olduğunu fark ettin mi?"
  2: "Sıralı olan yarıma bakarak hedefin o aralığa düşüp düşmediğini sabit sürede nasıl anlarsın?"
  3: "Bu algoritma 'değiştirilmiş ikili arama (modified binary search on rotated array)' olarak bilinir."
```

### py-medium-merge-intervals

```yaml
id: py-medium-merge-intervals
version: 1
language: python
engine: none
difficulty: medium
title: "Kesişen aralıkları birleştirme"
prompt: |
  Her biri [başlangıç, bitiş] şeklinde tanımlanmış aralıklardan oluşan bir liste
  verilmiştir. Birbiriyle kesişen veya birbirine teğet olan tüm aralıkları birleştirerek
  yeni bir aralık listesi döndüren `merge_overlapping_intervals(intervals: list[list[int]]) -> list[list[int]]`
  fonksiyonunu yazın. Girdi listesi boş olabilir. n adet aralık için O(n log n) zamanda çözün.
constraints:
  - "n aralık için çalışma süresi O(n log n) olmalı"
  - "Birbiriyle temas eden uç noktalar (ör. [1, 4] ve [4, 5]) birleştirilmeli"
  - "Ek bellek dönen liste için O(n) olmalı"
expected:
  time: { merge_overlapping_intervals: "n log n" }
  space: "n"
concept_tags: [data-structures, performance, boundary-conditions]
checklist_extra:
  - "Aralıklar başlangıç noktalarına göre sıralanmadan birleştirilmeye çalışılıyor mu?"
  - "Mevcut aralığın bitişi sonraki aralığın başlangıcından büyük veya eşit olduğunda bitiş noktası max() ile güncelleniyor mu?"
reference_solution_path: private/solutions/py-medium-merge-intervals.py
hint_ladder:
  1: "Aralıkları önce başlangıç değerlerine göre küçükten büyüğe sıralarsan ne kolaylaşır?"
  2: "Bir aralığın başlangıcı bir önceki aralığın bitişinden küçük veya eşitse iki aralığı nasıl kaynaştırırsın?"
  3: "Bu yöntem 'sıralama sonrası doğrusal aralık birleştirme (interval merging)' olarak bilinir."
```

### py-medium-daily-temperatures

```yaml
id: py-medium-daily-temperatures
version: 1
language: python
engine: none
difficulty: medium
title: "Daha sıcak bir gün için bekleme süresi"
prompt: |
  Günlük sıcaklık ölçümlerini içeren bir tamsayı listesi verilmiştir. Her gün için,
  o günden sonra daha sıcak bir havanın görüleceği ilk güne kadar kaç gün beklenmesi
  gerektiğini hesaplayan `daily_temperatures(temperatures: list[int]) -> list[int]`
  fonksiyonunu yazın. Gelecekte daha sıcak bir gün yoksa o gün için 0 yazılmalıdır.
  Her gün için ileriye doğru tarama yapmak O(n^2) süreceğinden, listenin uzunluğu n
  olmak üzere O(n) zamanda ve O(n) ek bellekle çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
  - "İç içe karesel döngüler kullanılmamalı"
  - "Ek bellek kullanımı O(n) olmalı"
expected:
  time: { daily_temperatures: "n" }
  space: "n"
concept_tags: [data-structures, performance, design]
checklist_extra:
  - "Her gün için sonraki günleri iç içe döngüyle tarayarak O(n^2) karmaşıklığa mı düşülüyor?"
  - "İndeksleri saklayan azalan bir yığın yapısı kuruldu mu?"
reference_solution_path: private/solutions/py-medium-daily-temperatures.py
hint_ladder:
  1: "Daha sıcak gününü henüz bulamamış günlerin indekslerini bir veri yapısında bekletebilir misin?"
  2: "Yeni gelen gün bekleyen günlerden sıcak olduğunda bekleyenleri sırayla çıkarıp aradaki gün farkını nasıl yazarsın?"
  3: "Bu veri yapısı deseni 'monotonik azalan yığın (monotonic stack)' olarak bilinir."
```

### py-medium-group-anagrams

```yaml
id: py-medium-group-anagrams
version: 1
language: python
engine: none
difficulty: medium
title: "Anagram kelimeleri gruplama"
prompt: |
  Kelimelerden oluşan bir liste verildiğinde, birbirinin anagramı olan kelimeleri aynı
  grup içinde toplayarak bir liste listesi döndüren `group_anagrams(words: list[str]) -> list[list[str]]`
  fonksiyonunu yazın. Grupların ve grup içindeki kelimelerin sıralaması önemli değildir.
  n kelime ve her kelimenin ortalama uzunluğu k olmak üzere, harf frekanslarını anahtar
  alarak O(n * k) sürede veya sıralama anahtarı ile O(n * k log k) sürede çözün.
constraints:
  - "n kelime ve en fazla k karakter için çalışma süresi en fazla O(n * k log k) olmalı"
  - "Boş liste verildiğinde boş liste dönmeli"
  - "Ek bellek O(n * k) olmalı"
expected:
  time: { group_anagrams: "n*k" }
  space: "n*k"
concept_tags: [hashing, strings, data-structures]
checklist_extra:
  - "Sözlük anahtarı olarak değiştirilebilir (mutable) bir liste kullanılmaya çalışılıp TypeError alınıyor mu?"
  - "Karakterlerin sayım demeti (tuple) veya sıralı hali anahtar olarak hash ediliyor mu?"
reference_solution_path: private/solutions/py-medium-group-anagrams.py
hint_ladder:
  1: "Birbirinin anagramı olan tüm kelimelerin ortak olarak paylaşacağı değişmez (hashable) bir imza ne olabilir?"
  2: "Sözlükte bu imzayı anahtar, o imzaya uyan kelimelerin listesini değer olarak tutarsan gruplama nasıl tamamlanır?"
  3: "Bu yöntem 'kanonik imza ile karma tablosunda gruplama (canonical representation hash grouping)' olarak bilinir."
```

### py-medium-spiral-matrix

```yaml
id: py-medium-spiral-matrix
version: 1
language: python
engine: none
difficulty: medium
title: "Matrisi spiral sırada gezme"
prompt: |
  m x n boyutunda bir matris verildiğinde, matrisin tüm elemanlarını dıştan içe doğru
  saat yönünde spiral bir sırada ziyaret ederek tek bir liste olarak döndüren
  `spiral_order(matrix: list[list[int]]) -> list[int]` fonksiyonunu yazın. Matris
  boşsa boş liste dönmelidir. Satır sayısı m ve sütun sayısı n olmak üzere tam olarak
  m * n adet eleman ziyaret edilmeli, hiçbir eleman atlanmamalı veya iki kez eklenmemelidir.
constraints:
  - "m satır ve n sütun için çalışma süresi O(m * n) olmalı"
  - "Ek bellek sonuç listesi hariç O(1) olmalı"
expected:
  time: { spiral_order: "m*n" }
  space: "1"
concept_tags: [data-structures, boundary-conditions, design]
checklist_extra:
  - "Tek satırlı veya tek sütunlu matrislerde sınırların birbirini geçmesi durumunda eleman tekrarı oluyor mu?"
  - "Üst, alt, sol ve sağ sınırlar her turda doğru daraltılıyor mu?"
reference_solution_path: private/solutions/py-medium-spiral-matrix.py
hint_ladder:
  1: "Matrisin dört kenarını temsil eden dört sınır değişkeni (top, bottom, left, right) tutabilir misin?"
  2: "Her kenarı gezdikten sonra ilgili sınırı bir birim içeri çekip sınırların çakışıp çakışmadığını nasıl denetlersin?"
  3: "Bu teknik 'sınır daraltmalı spiral ızgara simülasyonu' olarak bilinir."
```

### py-medium-three-sum

```yaml
id: py-medium-three-sum
version: 1
language: python
engine: none
difficulty: medium
title: "Toplamı sıfır olan benzersiz üçlüler"
prompt: |
  Bir tamsayı listesinde toplamları tam olarak 0 olan birbirinden farklı tüm [a, b, c]
  üçlülerini bulan `three_sum(nums: list[int]) -> list[list[int]]` fonksiyonunu yazın.
  Sonuç kümesinde aynı sayı üçlüsü birden fazla yer almamalıdır. Üç iç içe döngüyle
  O(n^3) arama yapmak yerine, listeyi sıralayıp iki işaretçi tekniğiyle O(n^2) sürede çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(n^2) olmalı"
  - "Sonuçta tekrar eden üçlüler bulunmamalı"
  - "Ek bellek sıralama ve sonuç hariç O(1) olmalı"
expected:
  time: { three_sum: "n^2" }
  space: "n"
concept_tags: [performance, data-structures, design]
checklist_extra:
  - "Üç iç içe döngüyle O(n^3) kaba kuvvet mi uygulanıyor?"
  - "Mükerrer üçlüleri önlemek için sıralı dizide ardışık aynı sayılar atlanıyor mu?"
reference_solution_path: private/solutions/py-medium-three-sum.py
hint_ladder:
  1: "Listeyi küçükten büyüğe sıraladıktan sonra ilk elemanı sabitleyip kalan iki sayıyı nasıl ararsın?"
  2: "İki işaretçi ile arama yaparken toplam sıfırdan küçükse solu, büyükse sağı nasıl kaydırırsın?"
  3: "Bu klasik algoritma 'sıralama ve iki işaretçili 3-toplam (three pointers on sorted array)' olarak bilinir."
```

### py-medium-container-with-most-water

```yaml
id: py-medium-container-with-most-water
version: 1
language: python
engine: none
difficulty: medium
title: "En çok su tutan kap"
prompt: |
  n adet negatif olmayan tamsayıdan oluşan bir yükseklik listesi verilmiştir. Her bir
  eleman (i, height[i]) noktasında dikey bir çizgiyi temsil eder. İki çizgi ve x ekseni
  arasında tutulabilecek maksimum su miktarını hesaplayan `max_area(height: list[int]) -> int`
  fonksiyonunu yazın. Su alanı, iki çizgi arasındaki taban genişliği ile kısa olan çizginin
  yüksekliğinin çarpımıdır. Tüm ikilileri denemek O(n^2) süreceğinden, listenin iki ucundan
  başlayan iki işaretçi ile O(n) sürede ve O(1) ek bellekle çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
expected:
  time: { max_area: "n" }
  space: "1"
concept_tags: [performance, design, boundary-conditions]
checklist_extra:
  - "Tüm olası ikilileri kontrol eden iç içe döngüler kuruldu mu?"
  - "İki işaretçiden daha kısa olanı içeri doğru kaydırılarak potansiyel artış arandı mı?"
reference_solution_path: private/solutions/py-medium-container-with-most-water.py
hint_ladder:
  1: "Alanı belirleyen kısıtlayıcı faktör iki çizgiden hangisinin boyudur?"
  2: "Genişlik her adımda daralırken alanı artırmanın tek yolu daha uzun bir dikey çizgi bulmak mıdır?"
  3: "Bu yaklaşım 'açgözlü iki işaretçi daraltması (greedy two-pointer)' olarak bilinir."
```

### py-medium-subarray-sum-equals-k

```yaml
id: py-medium-subarray-sum-equals-k
version: 1
language: python
engine: none
difficulty: medium
title: "Toplamı hedefe eşit kesintisiz alt dizi sayısı"
prompt: |
  Bir tamsayı listesi ve hedef tamsayı `k` verildiğinde, elemanlarının toplamı tam olarak
  `k`'ya eşit olan kesintisiz alt dizilerin toplam sayısını döndüren
  `subarray_sum_equals_k(nums: list[int], k: int) -> int` fonksiyonunu yazın. Listede
  negatif sayılar da bulunabilir. Tüm alt dizileri toplayarak O(n^2) zaman harcamak yerine,
  kümülatif ön ek toplamlarının frekansını bir sözlükte saklayarak O(n) sürede çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
  - "Ek bellek kullanımı O(n) olmalı"
expected:
  time: { subarray_sum_equals_k: "n" }
  space: "n"
concept_tags: [hashing, performance, design]
checklist_extra:
  - "İç içe iki döngü ile alt dizi toplamları hesaplanarak O(n^2) yapılıyor mu?"
  - "Sözlüğe başlangıçta {0: 1} değeri eklenerek en baştan başlayan toplamlar yakalanıyor mu?"
reference_solution_path: private/solutions/py-medium-subarray-sum-equals-k.py
hint_ladder:
  1: "Şu anki kümülatif toplam `current_sum` ise, toplamı k olan bir alt dizi için geçmişte hangi toplamın görülmüş olması gerekir?"
  2: "`current_sum - k` değerinin daha önce kaç kez oluştuğunu bir sözlükten O(1) sürede nasıl sorgularsın?"
  3: "Bu teknik 'ön ek toplamı ve karma tablosu farkı (prefix sum frequency map)' olarak bilinir."
```

### py-medium-longest-consecutive-sequence

```yaml
id: py-medium-longest-consecutive-sequence
version: 1
language: python
engine: none
difficulty: medium
title: "Sırasız listede en uzun ardışık sayı dizisi"
prompt: |
  Sıralı olmayan bir tamsayı listesinde bulunan ve ardışık sayılardan oluşan en uzun
  dizinin eleman sayısını bulan `longest_consecutive(nums: list[int]) -> int` fonksiyonunu
  yazın. Örneğin [100, 4, 200, 1, 3, 2] için en uzun ardışık dizi [1, 2, 3, 4] olup
  uzunluğu 4'tür. Sıralama yapmak O(n log n) süreceğinden, bir küme yapısından
  faydalanarak O(n) zamanda çözün.
constraints:
  - "Dahili sıralama kullanılmamalı; süre O(n) olmalı"
  - "Ek bellek kullanımı O(n) olmalı"
  - "Boş liste durumunda 0 dönmeli"
expected:
  time: { longest_consecutive: "n" }
  space: "n"
concept_tags: [hashing, performance, design]
checklist_extra:
  - "Dizi sıralanarak O(n log n) kuralı çiğneniyor mu?"
  - "Bir sayının sadece bir dizinin başlangıcı olup olmadığı (num - 1 kümede yoksa) kontrol edilerek gereksiz tekrarlar önlendi mi?"
reference_solution_path: private/solutions/py-medium-longest-consecutive-sequence.py
hint_ladder:
  1: "Tüm sayıları bir kümeye atarsan, bir sayının ardışık bir serinin başlangıcı olduğunu nasıl anlarsın?"
  2: "Eğer `x - 1` kümede yoksa `x` serinin ilk sayısıdır; peki `x + 1`, `x + 2` diye kümeyi sorgulamak toplam kaç adım sürer?"
  3: "Bu yöntem 'küme ile dizi başı filtreleme ve doğrusal ardışık zincir arama' olarak bilinir."
```

### py-medium-validate-binary-search-tree

```yaml
id: py-medium-validate-binary-search-tree
version: 1
language: python
engine: none
difficulty: medium
title: "İkili arama ağacı geçerliliği"
prompt: |
  Düğümleri `{'val': int, 'left': node | None, 'right': node | None}` biçiminde sözlüklerle
  temsil edilen bir ikili ağacın geçerli bir İkili Arama Ağacı (BST) olup olmadığını
  denetleyen `is_valid_bst(root: dict[str, object] | None) -> bool` fonksiyonunu yazın.
  Kural: Bir düğümün sol alt ağacındaki tüm düğümler o düğümden küçük, sağ alt ağacındaki
  tüm düğümler ise kesinlikle o düğümden büyük olmalıdır (yalnızca doğrudan çocukları
  karşılaştırmak yetersizdir). Ağacın derinliği h ve düğüm sayısı n için O(n) zamanda çözün.
constraints:
  - "Tüm alt ağaç kısıtları doğrulanmalı (sadece ebeveyn-çocuk kontrolü yetmez)"
  - "n düğüm için çalışma süresi O(n), çağrı yığını O(h) olmalı"
expected:
  time: { is_valid_bst: "n" }
  space: "h"
concept_tags: [graphs, data-structures, design]
checklist_extra:
  - "Yalnızca sol çocuk < kök ve sağ çocuk > kök denetlenerek torunların sınır ihlali gözden kaçıyor mu?"
  - "Özyinelemede her düğüm için geçerli bir (min_val, max_val) aralığı taşınıyor mu?"
reference_solution_path: private/solutions/py-medium-validate-binary-search-tree.py
hint_ladder:
  1: "Sol alt ağaca inerken üst sınırın, sağ alt ağaca inerken alt sınırın nasıl güncellendiğini düşündün mü?"
  2: "Her düğümün değerinin (alt_sinir, ust_sinir) açık aralığında kalıp kalmadığını özyinelemeyle nasıl sınarsın?"
  3: "Bu algoritma 'aralık kısıtlı derinlik öncelikli arama ile BST doğrulaması' olarak bilinir."
```

### py-medium-clone-graph-nodes

```yaml
id: py-medium-clone-graph-nodes
version: 1
language: python
engine: none
difficulty: medium
title: "Graf düğümlerini derinlemesine kopyalama"
prompt: |
  Yönsüz ve bağlantılı bir grafın bir düğümü verilmiştir. Düğümler `{'val': int, 'neighbors': list[node]}`
  yapısındadır. Bu grafın birebir aynı bağlantılara sahip derin kopyasını (clone) oluşturan
  ve başlangıç düğümünün kopyasını döndüren `clone_graph(node: dict[str, object] | None) -> dict[str, object] | None`
  fonksiyonunu yazın. Döngüsel bağlantılar sonsuz döngüye yol açmamalıdır. V düğüm ve E kenar
  için O(V + E) sürede çalışmalıdır.
constraints:
  - "Döngüsel graflarda sonsuz döngü yaşanmamalı"
  - "Orijinal graf nesneleri üzerinde mutasyon yapılmamalı"
  - "V düğüm ve E kenar için süre O(V + E), alan O(V) olmalı"
expected:
  time: { clone_graph: "V + E" }
  space: "V"
concept_tags: [graphs, data-structures, hashing]
checklist_extra:
  - "Daha önce kopyalanmış düğümler bir eşleme sözlüğünde tutulup tekrar kopyalanması önlendi mi?"
  - "Graf boş (None) olduğunda hatasız None dönüyor mu?"
reference_solution_path: private/solutions/py-medium-clone-graph-nodes.py
hint_ladder:
  1: "Daha önce klonladığın düğümleri orijinal düğüm kimliğine göre bir sözlükte nasıl eşleştirirsin?"
  2: "Bir komşuyu gezerken zaten kopyalanmışsa yeni düğüm üretmek yerine mevcut kopyayı listeye nasıl bağlarsın?"
  3: "Bu desen 'ziyaret sözlüğü ile graf derin kopyalama (deep copy via traversal)' olarak bilinir."
```

### py-medium-coin-change-fewest

```yaml
id: py-medium-coin-change-fewest
version: 1
language: python
engine: none
difficulty: medium
title: "En az madeni para ile tutar oluşturma"
prompt: |
  Farklı değerlerdeki madeni paraların listesi (`coins`) ve hedef bir `amount` tutarı
  verilmiştir. Bu tutarı oluşturmak için gereken en az madeni para sayısını hesaplayan
  `coin_change_min(coins: list[int], amount: int) -> int` fonksiyonunu yazın. Her madeni
  paradan sınırsız sayıda kullanılabilir. Verilen paralarla bu tutar oluşturulamıyorsa
  -1 dönmelidir. Açgözlü (greedy) yaklaşım her zaman optimum vermeyeceğinden, dinamik
  programlama ile O(n * amount) sürede çözün. n madeni para çeşidi sayısıdır.
constraints:
  - "amount == 0 durumunda 0 dönmeli"
  - "Çözüm yoksa -1 dönmeli"
  - "n para türü ve m = amount için süre O(n * m), ek alan O(m) olmalı"
expected:
  time: { coin_change_min: "n*m" }
  space: "m"
concept_tags: [performance, data-structures, design]
checklist_extra:
  - "Açgözlü yaklaşımla en büyük parayı seçip suboptimal veya hatalı sonuca mı düşülüyor?"
  - "DP tablosu sonsuz değerle başlatılıp min() fonksiyonuyla doğru gevşetildi mi?"
reference_solution_path: private/solutions/py-medium-coin-change-fewest.py
hint_ladder:
  1: "0'dan hedefe kadar olan her ara tutar için gereken en az para sayısını bir dizide tutabilir misin?"
  2: "i tutarına ulaşmak için elindeki her bozuk para c için dp[i - c] + 1 değerini nasıl değerlendirirsin?"
  3: "Bu klasik problem 'aşağıdan yukarıya dinamik programlama ile madeni para değişimi' olarak bilinir."
```

### py-medium-word-break-simple

```yaml
id: py-medium-word-break-simple
version: 1
language: python
engine: none
difficulty: medium
title: "Metnin sözlük kelimeleriyle bölünebilirliği"
prompt: |
  Bir metin ve kelimelerden oluşan bir sözlük listesi (`word_dict`) verilmiştir.
  Metnin, sözlükte yer alan kelimelerin bir veya daha fazlasının ardışık birleşimiyle
  tamamen oluşturulup oluşturulamayacağını denetleyen `can_word_break(s: str, word_dict: list[str]) -> bool`
  fonksiyonunu yazın. Aynı sözlük kelimesi birden çok kez kullanılabilir.
  n = len(s) olmak üzere O(n^2) sürede çalışan dinamik programlama tablosu tasarlayın.
constraints:
  - "Sözlük kelimeleri küme yapısına dönüştürülerek O(1) sürede aranmalı"
  - "n karakterli metin için çalışma süresi O(n^2), alan O(n) olmalı"
expected:
  time: { can_word_break: "n^2" }
  space: "n"
concept_tags: [strings, performance, hashing, design]
checklist_extra:
  - "Saf özyineleme ile aynı alt problemleri tekrar tekrar çözüp üstel O(2^n) süreye mi çıkılıyor?"
  - "dp[i] değeri metnin ilk i karakterinin parçalanabilirliğini doğru temsil ediyor mu?"
reference_solution_path: private/solutions/py-medium-word-break-simple.py
hint_ladder:
  1: "Metnin ilk i karakterinin geçerli parçalara bölünebildiğini bir boole dizisinde tutabilir misin?"
  2: "0'dan i'ye kadar bir j indeksi seçtiğinde, dp[j] True ise ve s[j:i] sözlükte varsa dp[i] ne olur?"
  3: "Bu algoritma '1B dinamik programlama ile dize ayrıştırma (word break DP)' olarak bilinir."
```

### py-medium-top-k-frequent-elements

```yaml
id: py-medium-top-k-frequent-elements
version: 1
language: python
engine: none
difficulty: medium
title: "En sık geçen k eleman"
prompt: |
  Bir tamsayı listesinde en yüksek frekansa sahip `k` adet elemanı bir liste olarak
  döndüren `top_k_frequent(nums: list[int], k: int) -> list[int]` fonksiyonunu yazın.
  Cevabın benzersiz olduğu garanti edilmiştir. Listeyi frekanslarına göre sıralamak
  O(n log n) sürer; kova sıralaması (bucket sort) mantığından yararlanarak O(n) doğrusal
  zamanda ve O(n) ek bellekle çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
  - "Ek bellek kullanımı O(n) olmalı"
  - "Dahili tam sıralama (.sort() / sorted()) kullanılmamalı"
expected:
  time: { top_k_frequent: "n" }
  space: "n"
concept_tags: [hashing, data-structures, performance]
checklist_extra:
  - "Elemanları frekanslarına göre sıralayıp O(n log n) sürece mi çıkılıyor?"
  - "Frekansı indeks alan bir kova listesi (buckets[freq]) kuruldu mu?"
reference_solution_path: private/solutions/py-medium-top-k-frequent-elements.py
hint_ladder:
  1: "Bir sayının frekansı en fazla listenin uzunluğu n kadar olabilir mi?"
  2: "İndeksi frekans olan n + 1 boyutunda bir kova listesi tutup elemanları frekanslarına göre bu kovalara dizebilir misin?"
  3: "Bu yöntem 'kova sıralaması ile en sık eleman seçimi (bucket sort)' olarak bilinir."
```

### py-medium-product-except-self

```yaml
id: py-medium-product-except-self
version: 1
language: python
engine: none
difficulty: medium
title: "Kendisi hariç diğer elemanların çarpımı"
prompt: |
  n elemanlı bir tamsayı listesi verildiğinde, her i indeksi için o eleman hariç diğer
  tüm elemanların çarpımına eşit yeni bir liste döndüren `product_except_self(nums: list[int]) -> list[int]`
  fonksiyonunu yazın. Bölme operatörünü (/) kesinlikle kullanmayın. Liste sıfırlar
  içerebilir. Çözüm O(n) zamanda çalışmalı ve sonuç listesi hariç O(1) ek alan kullanmalıdır.
constraints:
  - "Bölme işlemi (/) kesinlikle kullanılmamalı"
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
  - "Sonuç listesi dışında ek bellek O(1) olmalı"
expected:
  time: { product_except_self: "n" }
  space: "1"
concept_tags: [performance, design, boundary-conditions]
checklist_extra:
  - "Bölme işlemi kullanılarak sıfır içeren durumlarda ZeroDivisionError alınıyor mu?"
  - "Sol çarpımlar ve sağ çarpımlar tek bir sonuç dizisi üzerinde iki geçişte biriktirildi mi?"
reference_solution_path: private/solutions/py-medium-product-except-self.py
hint_ladder:
  1: "Bir elemanın solundaki tüm sayıların çarpımını bir geçişte sonuç dizisine yazabilir misin?"
  2: "İkinci geçişte sağdan sola gelirken sağdaki çarpımları tek bir değişkende biriktirip sonuçla çarparsan ne elde edersin?"
  3: "Bu algoritma 'çift geçişli ön ek ve son ek çarpım akümülasyonu' olarak bilinir."
```

### py-medium-find-kth-largest

```yaml
id: py-medium-find-kth-largest
version: 1
language: python
engine: none
difficulty: medium
title: "Dizideki k. en büyük eleman"
prompt: |
  Sırasız bir tamsayı listesinde sıralandığında `k`'ıncı en büyük olacak sayıyı bulan
  `find_kth_largest(nums: list[int], k: int) -> int` fonksiyonunu yazın. Listeyi tamamen
  sıralamak O(n log n) sürer; bunun yerine boyutu k ile sınırlı bir öncelik kuyruğu
  (min-heap) kullanarak O(n log k) sürede ya da hızlı seçimle (quickselect) ortalama O(n)
  sürede çözün.
constraints:
  - "n eleman ve k için süre O(n log k) veya ortalama O(n) olmalı"
  - "Tüm diziyi sort() ile sıralamaktan kaçınılmalı"
  - "Ek bellek en fazla O(k) olmalı"
expected:
  time: { find_kth_largest: "n log k" }
  space: "k"
concept_tags: [data-structures, performance, design]
checklist_extra:
  - "Bütün dizi sort() edilip O(n log n) süre harcanıyor mu?"
  - "Öncelikli kuyruk boyutu k'yı aştığında en küçük eleman çıkarılıyor mu?"
reference_solution_path: private/solutions/py-medium-find-kth-largest.py
hint_ladder:
  1: "Boyutu k olan bir min-heap yapısında her an en büyük k elemanı tutabilir misin?"
  2: "Listenin tüm elemanları geçtikten sonra bu k boyutlu min-heap'in tepesindeki eleman neyi temsil eder?"
  3: "Bu teknik 'k-boyutlu min-heap ile sıra istatistiği seçimi' olarak bilinir."
```

### py-medium-decode-string-brackets

```yaml
id: py-medium-decode-string-brackets
version: 1
language: python
engine: none
difficulty: medium
title: "Parantezli kodlanmış metni açma"
prompt: |
  `k[metin]` biçiminde kodlanmış bir dizeyi açarak orijinal metni üreten
  `decode_string(s: str) -> str` fonksiyonunu yazın. Kural: Köşeli parantez içindeki metin
  tam olarak `k` kez tekrarlanır. Kodlamalar iç içe olabilir (örneğin '3[a2[c]]' ->
  'accaccacc'). k değeri çok basamaklı bir sayı olabilir. Bir yığın (stack) yapısı
  kullanarak O(çıktı_uzunluğu) sürede çözün.
constraints:
  - "İç içe parantezler doğru sırayla açılmalı"
  - "Çok basamaklı sayılar (örneğin '10[a]') doğru ayrıştırılmalı"
  - "Çıktı uzunluğu m için çalışma süresi O(m), yığın alanı O(m) olmalı"
expected:
  time: { decode_string: "m" }
  space: "m"
concept_tags: [strings, data-structures, parsing]
checklist_extra:
  - "Ardışık rakamlar birleştirilmeyip tek basamaklı mı varsayılıyor?"
  - "'[' görüldüğünde mevcut dize ve sayı yığına itilip ']' görüldüğünde geri çekiliyor mu?"
reference_solution_path: private/solutions/py-medium-decode-string-brackets.py
hint_ladder:
  1: "Yeni bir '[' ile karşılaştığında o ana kadar biriken dizeyi ve sayıyı bir yığına atıp sıfırlayabilir misin?"
  2: "']' karakteri geldiğinde yığından önceki dizeyi ve çarpanı çıkarıp mevcut parçayı kaç kez tekrarlamalısın?"
  3: "Bu algoritma 'yığın tabanlı bağlam saklama ile iç içe ifade açma' olarak bilinir."
```

### py-medium-min-stack

```yaml
id: py-medium-min-stack
version: 1
language: python
engine: none
difficulty: medium
title: "O(1) sürede minimum veren yığın sınıfı"
prompt: |
  Standart yığın işlemleri olan `push(val: int)`, `pop() -> int`, `top() -> int` metodlarına
  ek olarak yığındaki en küçük elemanı anında döndüren `get_min() -> int` metodunu
  destekleyen bir `MinStack` sınıfı tasarlayın. Tüm işlemler en kötü durumda kesinlikle
  O(1) zaman karmaşıklığında çalışmalıdır. Boş yığında pop, top veya get_min çağrılırsa
  IndexError fırlatılmalıdır.
constraints:
  - "Tüm dört işlem (push, pop, top, get_min) O(1) zamanda çalışmalı"
  - "Boş yığında IndexError fırlatılmalı"
  - "Ek bellek n eleman için O(n) olmalı"
expected:
  time: { push: "1", pop: "1", top: "1", get_min: "1" }
  space: "n"
concept_tags: [data-structures, design, exceptions]
checklist_extra:
  - "get_min çağrıldığında yığın taranarak O(n) süreye mi çıkılıyor?"
  - "Her elemanla birlikte o anki minimum değeri de yığına kaydeden çift yığın yaklaşımı uygulandı mı?"
reference_solution_path: private/solutions/py-medium-min-stack.py
hint_ladder:
  1: "Her elemanı yığına iterken, o eleman itildikten sonraki geçerli minimumu da paralel bir yığında saklayabilir misin?"
  2: "Bir eleman pop edildiğinde minimum takip yığınından da bir eleman çıkarmak minimumun tutarlılığını nasıl korur?"
  3: "Bu tasarım 'yardımcı minimum yığını ile O(1) arama mimarisi' olarak bilinir."
```

### py-medium-rotate-array-k

```yaml
id: py-medium-rotate-array-k
version: 1
language: python
engine: none
difficulty: medium
title: "Diziyi k adım sağa döndürme"
prompt: |
  n elemanlı bir tamsayı listesini `k` adım sağa dairesel olarak döndüren
  `rotate_array_in_place(nums: list[int], k: int) -> None` fonksiyonunu yazın.
  İşlem doğrudan orijinal liste üzerinde yerinde (in-place) gerçekleştirilmeli,
  yeni bir liste oluşturulmamalıdır. k, n'den büyük olabilir. O(n) zaman ve O(1) ek
  alan karmaşıklığında çözün.
constraints:
  - "k %= len(nums) normalizasyonu yapılmalı"
  - "Yeni liste tahsis edilmemeli; ek bellek O(1) olmalı"
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
expected:
  time: { rotate_array_in_place: "n" }
  space: "1"
concept_tags: [data-structures, performance, boundary-conditions]
checklist_extra:
  - "nums = nums[-k:] + nums[:-k] yapılarak yeni liste tahsis edilip in-place kısıtı bozuluyor mu?"
  - "Tüm diziyi ters çevirip, ardından ilk k ve kalan n-k elemanı ayrı ayrı ters çeviren yöntem kullanıldı mı?"
reference_solution_path: private/solutions/py-medium-rotate-array-k.py
hint_ladder:
  1: "Dizinin tamamını ters çevirirsen elemanların konumları hedefe nasıl yaklaşır?"
  2: "İlk k elemanı kendi içinde ve kalan elemanları kendi içinde tekrar ters çevirirsen doğru sıralama oluşur mu?"
  3: "Bu algoritma 'üç aşamalı ters çevirme ile yerinde dizi döndürme (reversal algorithm)' olarak bilinir."
```

### py-medium-permutations-recursive

```yaml
id: py-medium-permutations-recursive
version: 1
language: python
engine: none
difficulty: medium
title: "Benzersiz elemanların tüm permütasyonları"
prompt: |
  Tümü birbirinden farklı tamsayılardan oluşan bir liste verildiğinde, bu sayıların
  tüm olası permütasyonlarını bir liste listesi olarak döndüren
  `generate_permutations(nums: list[int]) -> list[list[int]]` fonksiyonunu yazın.
  itertools kütüphanesini içe aktarmadan, geri izleme (backtracking) veya özyineleme
  ile kendiniz kodlayın. n elemanlı liste için n! adet permütasyon üretilmelidir.
constraints:
  - "itertools modülü kullanılmamalı"
  - "n elemanlı liste için çalışma süresi O(n * n!) olmalı"
  - "Sonuç listesi tüm geçerli permütasyonları içermeli"
expected:
  time: { generate_permutations: "n*n!" }
  space: "n"
concept_tags: [design, data-structures, performance]
checklist_extra:
  - "Oluşturulan ara permütasyon listeleri sonuca kopyalanmadan referansıyla eklenip bozuluyor mu?"
  - "Geri izleme adımında ziyaret edilen eleman geri çıkarılıyor (backtrack ediliyor) mu?"
reference_solution_path: private/solutions/py-medium-permutations-recursive.py
hint_ladder:
  1: "Bir sayıyı mevcut yola ekleyip özyinelemeli çağırdıktan sonra o sayıyı yoldan çıkarmayı (pop) unutmaman neden kritiktir?"
  2: "Mevcut yolun boyutu girdi listesinin boyutuna eşit olduğunda yeni bir kopya oluşturup sonuçlara nasıl eklersin?"
  3: "Bu yöntem 'durum uzayı ağacında geri izleme (backtracking)' olarak bilinir."
```

### py-medium-subsets-powerset

```yaml
id: py-medium-subsets-powerset
version: 1
language: python
engine: none
difficulty: medium
title: "Kümenin tüm alt kümeleri (Kuvvet kümesi)"
prompt: |
  Benzersiz tamsayılardan oluşan bir liste verildiğinde, bu listenin oluşturabileceği
  tüm olası alt kümeleri (kuvvet kümesini) döndüren `generate_subsets(nums: list[int]) -> list[list[int]]`
  fonksiyonunu yazın. Boş küme ve kümenin kendisi de sonuca dahil edilmelidir.
  n elemanlı bir kümenin 2^n adet alt kümesi vardır. O(n * 2^n) zamanda ve bellekte çözün.
constraints:
  - "Sonuçta tam olarak 2^n adet alt küme bulunmalı"
  - "n eleman için çalışma süresi O(n * 2^n) olmalı"
expected:
  time: { generate_subsets: "n*2^n" }
  space: "n"
concept_tags: [design, data-structures, boundary-conditions]
checklist_extra:
  - "Boş alt küme ([]) sonuca dahil ediliyor mu?"
  - "Her eleman için 'bu elemanı dahil et veya etme' ikili seçim mantığı kurgulandı mı?"
reference_solution_path: private/solutions/py-medium-subsets-powerset.py
hint_ladder:
  1: "Her adımda sıradaki elemanı mevcut tüm alt kümelere ekleyerek alt kümeler listesini iki katına çıkarabilir misin?"
  2: "Geri izleme ile her eleman için 'dahil et' ve 'etme' dallarını nasıl oluşturursun?"
  3: "Bu işlem 'kuvvet kümesi inşası (powerset generation)' olarak bilinir."
```

### py-medium-letter-combinations-phone

```yaml
id: py-medium-letter-combinations-phone
version: 1
language: python
engine: none
difficulty: medium
title: "Telefon tuş takımı harf kombinasyonları"
prompt: |
  2-9 arasındaki rakamlardan oluşan bir metin verildiğinde, eski telefon tuş takımında
  bu rakamların karşılık geldiği harflerle oluşturulabilecek tüm olası harf kombinasyonlarını
  döndüren `letter_combinations(digits: str) -> list[str]` fonksiyonunu yazın.
  Örneğin '23' için ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf'] dönmelidir.
  digits boşsa boş liste dönmelidir. Rakam uzunluğu n için O(4^n) sürede çalışmalıdır.
constraints:
  - "digits boş metin olduğunda boş liste dönmeli"
  - "n basamaklı girdi için süre O(4^n), alan O(n) olmalı"
expected:
  time: { letter_combinations: "4^n" }
  space: "n"
concept_tags: [strings, design, data-structures]
checklist_extra:
  - "digits boşken [''] gibi boş dize içeren tek elemanlı liste mi dönüyor?"
  - "7 ve 9 tuşlarının 4 harf içerdiği durum harita tablosunda doğru tanımlandı mı?"
reference_solution_path: private/solutions/py-medium-letter-combinations-phone.py
hint_ladder:
  1: "Her rakamı temsil eden harfleri bir sözlükte nasıl saklarsın?"
  2: "İlk rakamın her bir harfi için ikinci rakamın harflerini özyinelemeyle nasıl birleştirirsin?"
  3: "Bu yöntem 'kartezyen çarpım geri izleme ağacı (backtracking combinations)' olarak bilinir."
```

### py-medium-number-of-islands

```yaml
id: py-medium-number-of-islands
version: 1
language: python
engine: none
difficulty: medium
title: "İki boyutlu ızgarada ada sayısı"
prompt: |
  '1' (kara) ve '0' (su) karakterlerinden oluşan m x n boyutunda iki boyutlu bir ızgara
  verilmiştir. Karaların yatay veya dikey olarak birbirine bağlanmasıyla oluşan bağımsız
  ada sayısını hesaplayan `num_islands(grid: list[list[str]]) -> int` fonksiyonunu yazın.
  Çapraz bağlantılar kara sayılmaz. Ziyaret edilen karaları işaretleyerek O(m * n) zamanda
  ve O(m * n) yığın belleğinde çözün.
constraints:
  - "m satır ve n sütun için çalışma süresi O(m * n) olmalı"
  - "Yalnızca yatay ve dikey komşuluklar ada bağlantısı sayılmalı"
  - "Ziyaret edilen hücreler tekrar işlenmemeli"
expected:
  time: { num_islands: "m*n" }
  space: "m*n"
concept_tags: [graphs, data-structures, design]
checklist_extra:
  - "Çapraz komşuluklar yanlışlıkla aynı ada sayılıyor mu?"
  - "Ziyaret edilen hücreler '0' ile değiştirilerek veya ziyaret kümesine alınarak sonsuz döngü engellendi mi?"
reference_solution_path: private/solutions/py-medium-number-of-islands.py
hint_ladder:
  1: "'1' gördüğün her hücreden başlayarak ona bağlı tüm komşu '1'leri gezen bir arama fonksiyonu yazabilir misin?"
  2: "Geçtiğin '1' hücrelerini '0' yaparak ya da kaydederek aynı adayı bir daha saymaktan nasıl kaçınırsın?"
  3: "Bu algoritma 'bağlantılı bileşen sayımı için ızgara DFS/BFS (connected components flood fill)' olarak bilinir."
```

### py-medium-set-matrix-zeroes

```yaml
id: py-medium-set-matrix-zeroes
version: 1
language: python
engine: none
difficulty: medium
title: "Matriste sıfır içeren satır ve sütunları sıfırlama"
prompt: |
  m x n boyutunda bir tamsayı matrisinde bir eleman 0 ise, o elemanın bulunduğu satır
  ve sütundaki tüm elemanları 0 yapan `set_matrix_zeroes(matrix: list[list[int]]) -> None`
  fonksiyonunu yazın. İşlem yerinde (in-place) yapılmalıdır. Ekstra m + n boyutunda
  liste veya küme açmak yerine, matrisin ilk satır ve ilk sütununu işaretçi olarak
  kullanarak O(1) ek alan karmaşıklığında çözün.
constraints:
  - "Ek bellek kullanımı kesinlikle O(1) olmalı"
  - "m x n matris için çalışma süresi O(m * n) olmalı"
  - "Sonradan sıfır yapılan hücreler yeni sıfırlar tetiklememeli"
expected:
  time: { set_matrix_zeroes: "m*n" }
  space: "1"
concept_tags: [data-structures, performance, design]
checklist_extra:
  - "O(m*n) veya O(m+n) ekstra bellek ayrılarak O(1) bellek şartı bozuluyor mu?"
  - "İlk satır ve ilk sütunun kendisinde baştan sıfır olup olmadığı iki ayrı bayrakla tutuldu mu?"
reference_solution_path: private/solutions/py-medium-set-matrix-zeroes.py
hint_ladder:
  1: "Matrisin ilk satırını ve ilk sütununu hangi satır ve sütunların sıfırlanacağını tutan bayraklar gibi kullanabilir misin?"
  2: "İlk satır ve sütunun kendilerinin sıfırlanıp sıfırlanmayacağını ayrı iki değişkende saklamak neden şarttır?"
  3: "Bu teknik 'matris sınırlarını durum göstergesi olarak kullanan O(1) alan algoritması' olarak bilinir."
```

### py-medium-sort-colors-dutch-flag

```yaml
id: py-medium-sort-colors-dutch-flag
version: 1
language: python
engine: none
difficulty: medium
title: "Üç renkli diziyi tek geçişte sıralama"
prompt: |
  Yalnızca 0 (kırmızı), 1 (beyaz) ve 2 (mavi) değerlerinden oluşan bir tamsayı listesini,
  aynı renkler yan yana gelecek şekilde (0'lar başta, 1'ler ortada, 2'ler sonda) yerinde
  sıralayan `sort_colors_in_place(nums: list[int]) -> None` fonksiyonunu yazın.
  Dahili `.sort()` fonksiyonunu kullanmayın ve iki geçişli sayma sıralaması yerine,
  üç işaretçi ile tek bir geçişte O(n) zaman ve O(1) ek alanda çözün.
constraints:
  - "Dahili sıralama fonksiyonları kullanılmamalı"
  - "Tek bir geçişte (one-pass) tamamlanmalı"
  - "Ek bellek O(1) olmalı"
expected:
  time: { sort_colors_in_place: "n" }
  space: "1"
concept_tags: [data-structures, performance, design]
checklist_extra:
  - "İki geçişli sayma (sayıları sayıp sonra üzerine yazma) mı yapılıyor?"
  - "Üç işaretçi (low, mid, high) mantığı doğru takaslarla kurgulandı mı?"
reference_solution_path: private/solutions/py-medium-sort-colors-dutch-flag.py
hint_ladder:
  1: "0'ların bitiş sınırını (low), 2'lerin başlangıç sınırını (high) ve taranan indeksi (mid) tutabilir misin?"
  2: "mid konumunda 0 gördüğünde low ile, 2 gördüğünde high ile takas edip işaretçileri nasıl güncellersin?"
  3: "Bu klasik algoritma 'Hollanda Milli Bayrağı problemi (Dutch National Flag problem)' olarak bilinir."
```

### py-medium-search-2d-matrix

```yaml
id: py-medium-search-2d-matrix
version: 1
language: python
engine: none
difficulty: medium
title: "İki boyutlu sıralı matriste arama"
prompt: |
  m x n boyutunda bir tamsayı matrisi verilmiştir. Bu matriste her satır soldan sağa
  artan sırada sıralıdır ve her satırın ilk elemanı bir önceki satırın son elemanından
  büyüktür. Verilen bir `target` değerinin matriste olup olmadığını denetleyen
  `search_matrix(matrix: list[list[int]], target: int) -> bool` fonksiyonunu yazın.
  Tüm matrisi tek boyutlu bir dizi gibi hayal ederek O(log(m * n)) süreli ikili arama
  ile çözün.
constraints:
  - "m satır ve n sütun için çalışma süresi O(log(m * n)) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
expected:
  time: { search_matrix: "log(m*n)" }
  space: "1"
concept_tags: [performance, design, boundary-conditions]
checklist_extra:
  - "Doğrusal olarak satır satır taranarak O(m*n) sürece mi çıkılıyor?"
  - "Tek boyutlu indeks idx için satır = idx // n ve sütun = idx % n dönüşümü doğru yapıldı mı?"
reference_solution_path: private/solutions/py-medium-search-2d-matrix.py
hint_ladder:
  1: "m x n elemanlı bir matrisi 0'dan m*n - 1'e kadar sanal tek boyutlu bir dizi gibi görebilir misin?"
  2: "Herhangi bir ortanca indeksin matristeki [satır][sütun] karşılığını // ve % işlemleriyle nasıl hesaplarsın?"
  3: "Bu teknik 'sanal matris düzleştirme ile ikili arama (virtual flattened binary search)' olarak bilinir."
```

### py-medium-longest-palindromic-substring

```yaml
id: py-medium-longest-palindromic-substring
version: 1
language: python
engine: none
difficulty: medium
title: "En uzun palindromik alt metin"
prompt: |
  Verilen bir metin içindeki en uzun palindromik alt metni bulan
  `longest_palindromic_substring(s: str) -> str` fonksiyonunu yazın. Birden fazla aynı
  uzunlukta palindrom varsa herhangi biri döndürülebilir. Metin tek karakterden oluşuyorsa
  o karakter dönmelidir. Tüm olası alt metinleri test etmek O(n^3) sürer; her merkezi
  dışa doğru genişleterek O(n^2) zamanda ve O(1) ek alanda çözün.
constraints:
  - "n karakterli metin için çalışma süresi en fazla O(n^2) olmalı"
  - "Ek bellek kullanımı O(1) olmalı (dilimleme dışında)"
expected:
  time: { longest_palindromic_substring: "n^2" }
  space: "1"
concept_tags: [strings, performance, boundary-conditions]
checklist_extra:
  - "Yalnızca tek uzunluklu (merkezi tek harf olan) palindromlar mı denetleniyor?"
  - "Çift uzunluklu ('abba' gibi) palindromlar için iki harfli merkezler de test edildi mi?"
reference_solution_path: private/solutions/py-medium-longest-palindromic-substring.py
hint_ladder:
  1: "Palindromların merkezleri ya tek bir karakter (tek uzunluk) ya da iki ardışık karakter (çift uzunluk) olabilir mi?"
  2: "Olası 2n - 1 merkezin her birinden sola ve sağa doğru harfler eşit olduğu sürece genişleyebilir misin?"
  3: "Bu yöntem 'merkezden dışa doğru genişleyerek palindrom bulma (expand around centers)' olarak bilinir."
```

### py-medium-peak-element

```yaml
id: py-medium-peak-element
version: 1
language: python
engine: none
difficulty: medium
title: "Dizideki tepe noktayı bulma"
prompt: |
  Bir tepe eleman (peak element), komşularından kesinlikle büyük olan elemandır.
  Verilen bir tamsayı listesinde herhangi bir tepe elemanın indeksini döndüren
  `find_peak_element(nums: list[int]) -> int` fonksiyonunu yazın. Liste sınırlarının dışı
  -sonsuz kabul edilir. Birden fazla tepe varsa herhangi birinin indeksi geçerlidir.
  Doğrusal tarama yerine, ikili arama prensibiyle O(log n) zamanda çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(log n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
expected:
  time: { find_peak_element: "log n" }
  space: "1"
concept_tags: [performance, boundary-conditions, design]
checklist_extra:
  - "Dizi baştan sona taranarak O(n) süreye mi düşülüyor?"
  - "nums[mid] < nums[mid + 1] olduğunda tepenin kesinlikle sağ yarıda olduğu mantığı kuruldu mu?"
reference_solution_path: private/solutions/py-medium-peak-element.py
hint_ladder:
  1: "Eğer ortanca eleman bir sağındaki elemandan küçükse, sağ tarafta en az bir tepe noktası bulunması neden garantidir?"
  2: "İkili arama mantığını sıralı olmayan bir dizide eğim (türev) yönüne göre nasıl kullanırsın?"
  3: "Bu yaklaşım 'eğim yönü takipli ikili arama ile tepe tespiti' olarak bilinir."
```

### py-medium-jump-game-can-reach

```yaml
id: py-medium-jump-game-can-reach
version: 1
language: python
engine: none
difficulty: medium
title: "Zıplama oyununda son indekse ulaşabilirlik"
prompt: |
  Her elemanının o konumdan yapılabilecek maksimum zıplama mesafesini gösterdiği bir
  tamsayı listesi verilmiştir. Başlangıç noktası 0. indeks olduğuna göre, son indekse
  ulaşmanın mümkün olup olmadığını denetleyen `can_jump(nums: list[int]) -> bool`
  fonksiyonunu yazın. n elemanlı liste için dinamik programlama O(n^2) sürer;
  açgözlü (greedy) yaklaşımla ulaşılabilecek en uzak mesafeyi takip ederek O(n) sürede
  ve O(1) ek bellekle çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
expected:
  time: { can_jump: "n" }
  space: "1"
concept_tags: [performance, design, boundary-conditions]
checklist_extra:
  - "İç içe döngülerle O(n^2) zıplama simülasyonu mu yapılıyor?"
  - "Mevcut indeks o ana kadar erişilebilen maksimum menzili aştığında hemen False dönülüyor mu?"
reference_solution_path: private/solutions/py-medium-jump-game-can-reach.py
hint_ladder:
  1: "Her adımda şu ana kadar zıplanabilecek en uzak indeksi (`max_reachable`) güncelleyebilir misin?"
  2: "Eğer bir i indeksine geldiğinde i > max_reachable ise bu konuma asla varılamayacağı anlamına gelmez mi?"
  3: "Bu yöntem 'açgözlü erişim menzili takibi (greedy reachability)' olarak bilinir."
```

### py-medium-gas-station-circuit

```yaml
id: py-medium-gas-station-circuit
version: 1
language: python
engine: none
difficulty: medium
title: "Dairesel benzin istasyonu turu"
prompt: |
  Dairesel bir rota üzerinde n adet benzin istasyonu bulunmaktadır. i. istasyonda
  alınabilecek yakıt `gas[i]`, bir sonraki istasyona gitmek için gereken yakıt `cost[i]`
  olarak verilmiştir. Deponuz başlangıçta boşken, tüm rotayı saat yönünde tam bir tur
  atabilecek başlangıç istasyonunun indeksini döndüren `can_complete_circuit(gas: list[int], cost: list[int]) -> int`
  fonksiyonunu yazın. Çözüm varsa tek bir benzersiz istasyondur, tur tamamlanamıyorsa
  -1 dönmelidir. O(n) zamanda ve O(1) alanda çözün.
constraints:
  - "Toplam yakıt toplam maliyetten azsa hemen -1 dönmeli"
  - "n istasyon için süre O(n), alan O(1) olmalı"
expected:
  time: { can_complete_circuit: "n" }
  space: "1"
concept_tags: [performance, design, boundary-conditions]
checklist_extra:
  - "Her istasyondan başlayarak karesel O(n^2) simülasyon mu yapılıyor?"
  - "Mevcut depodaki yakıt negatif olduğunda başlangıç noktası bir sonraki istasyona kaydırılıyor mu?"
reference_solution_path: private/solutions/py-medium-gas-station-circuit.py
hint_ladder:
  1: "Listenin tamamındaki toplam gaz toplam maliyetten azsa herhangi bir çözümün bulunması mümkün müdür?"
  2: "A noktasından yola çıkıp B noktasında yakıtın biterse, A ile B arasındaki hiçbir noktanın çözüm olamayacağını fark ettin mi?"
  3: "Bu yaklaşım 'kümülatif yakıt açığı ile tek geçişli başlangıç noktası tespiti' olarak bilinir."
```

### py-medium-flatten-nested-iterator

```yaml
id: py-medium-flatten-nested-iterator
version: 1
language: python
engine: none
difficulty: medium
title: "İç içe listeleri bellek dostu jeneratörle düzleştirme"
prompt: |
  Tamsayılar ve keyfi derinlikte iç içe geçmiş listelerden oluşan karmaşık bir veri yapısını
  tüm elemanlarını düz bir sırada teker teker üreten `flatten_generator(nested: list[object]) -> Iterator[int]`
  jeneratör fonksiyonunu yazın. Tüm yapıyı önceden hafızada düz bir listeye açmak yerine,
  `yield` ve `yield from` kullanarak talep edildikçe (lazy evaluation) eleman üretmelidir.
  Toplam n tamsayı için O(n) zamanda ve en fazla yuvalanma derinliği d kadar ek alanda çalışmalıdır.
constraints:
  - "Tüm veriyi önceden belleğe alan düz bir liste tahsis edilmemeli; jeneratör olmalı"
  - "Toplam n tamsayı için süre O(n), çağrı yığını O(d) olmalı"
expected:
  time: { flatten_generator: "n" }
  space: "d"
concept_tags: [data-structures, design, exceptions]
checklist_extra:
  - "Tüm elemanlar bellekte yeni bir listeye toplanıp mı döndürülüyor?"
  - "Python'un yield from sözdizimi özyinelemeli alt jeneratörler için kullanıldı mı?"
reference_solution_path: private/solutions/py-medium-flatten-nested-iterator.py
hint_ladder:
  1: "Bir elemanın liste mi yoksa tamsayı mı olduğunu isinstance ile nasıl kontrol edersin?"
  2: "Eğer eleman bir listeyse yield from ile fonksiyonu kendisine özyinelemeli olarak nasıl bağlarsın?"
  3: "Bu yapı 'özyinelemeli jeneratör ile tembel düzleştirme (recursive lazy generator)' olarak bilinir."
```

### py-medium-task-scheduler

```yaml
id: py-medium-task-scheduler
version: 1
language: python
engine: none
difficulty: medium
title: "Soğuma süreli görev planlayıcı"
prompt: |
  Harflerle temsil edilen bir görev listesi ve aynı iki görevin tekrar çalışabilmesi için
  arada geçmesi gereken minimum bekleme (soğuma) aralığı `n` verilmiştir. CPU her birim
  zamanda ya bir görev yürütür ya da boşta (idle) bekler. Tüm görevlerin tamamlanması
  için gereken en az toplam birim zamanı hesaplayan `least_interval(tasks: list[str], n: int) -> int`
  fonksiyonunu yazın. Görevleri tek tek simüle etmek yerine matematiksel frekans
  analiziyle O(len(tasks)) zamanda çözün.
constraints:
  - "m = len(tasks) için çalışma süresi O(m) olmalı"
  - "Ek bellek görev alfabesi boyutuyla sınırlı O(1) olmalı"
expected:
  time: { least_interval: "m" }
  space: "1"
concept_tags: [performance, design, hashing]
checklist_extra:
  - "Adım adım zaman simülasyonu yapılarak gereksiz karmaşıklığa mı giriliyor?"
  - "En yüksek frekansa sahip görevin oluşturduğu boşluklar ve maksimum formülü kullanıldı mı?"
reference_solution_path: private/solutions/py-medium-task-scheduler.py
hint_ladder:
  1: "En sık tekrar eden görev diğerlerinden daha fazla boşluk (idle) zorunluluğu doğurmaz mı?"
  2: "Maksimum frekans k ise, (k - 1) adet boşluk bloğunun her birine n görev yerleştirme hesabını nasıl yaparsın?"
  3: "Bu yaklaşım 'frekans tavanı ile blok bazlı görev zamanlama' olarak bilinir."
```

### py-medium-interval-intersection

```yaml
id: py-medium-interval-intersection
version: 1
language: python
engine: none
difficulty: medium
title: "İki sıralı aralık listesinin kesişimi"
prompt: |
  Her biri kendi içinde ayrık ve küçükten büyüğe sıralı iki kapalı aralık listesi
  verilmiştir. Bu iki listenin kesişimini oluşturan tüm aralıkları yeni bir liste olarak
  döndüren `interval_intersection(first_list: list[list[int]], second_list: list[list[int]]) -> list[list[int]]`
  fonksiyonunu yazın. Kesişmeyen aralıklar atlanmalı, tek bir noktada temas eden aralıklar
  [x, x] biçiminde dahil edilmelidir. n ve m listelerin eleman sayıları olmak üzere iki
  işaretçi ile O(n + m) sürede çözün.
constraints:
  - "n ve m elemanlı listeler için çalışma süresi O(n + m) olmalı"
  - "Ek bellek sonuç listesi hariç O(1) olmalı"
expected:
  time: { interval_intersection: "n + m" }
  space: "1"
concept_tags: [data-structures, performance, boundary-conditions]
checklist_extra:
  - "İki aralığın kesişim başlangıcı max(start1, start2) ve bitişi min(end1, end2) olarak doğru alındı mı?"
  - "İşaretçilerden hangisinin bir sonrakine geçeceği (bitişi daha küçük olan) doğru belirlendi mi?"
reference_solution_path: private/solutions/py-medium-interval-intersection.py
hint_ladder:
  1: "İki aralığın kesişiminin geçerli olması için başlangıç <= bitiş şartı nasıl test edilir?"
  2: "İki aralıktan hangisinin daha önce bittiğine bakarak o listenin işaretçisini 1 artırabilir misin?"
  3: "Bu yöntem 'sıralı aralıklarda iki işaretçi ile kesişim taraması' olarak bilinir."
```

### py-medium-string-to-integer-atoi

```yaml
id: py-medium-string-to-integer-atoi
version: 1
language: python
engine: none
difficulty: medium
title: "Metni güvenli tamsayıya çevirme"
prompt: |
  C standart kütüphanesindeki atoi fonksiyonuna benzer şekilde, bir metni tamsayıya
  dönüştüren `my_atoi(s: str) -> int` fonksiyonunu yazın. Kurallar: 1) Baştaki tüm
  boşlukları atla, 2) Opsiyonel '+' veya '-' işaretini oku, 3) Rakamlar bittiğinde
  veya geçersiz karakter geldiğinde dur, 4) Elde edilen sayı 32-bit işaretli tamsayı
  aralığını [-2^31, 2^31 - 1] aşıyorsa sınır değere sabitle, 5) Hiç rakam okunamazsa 0 dön.
constraints:
  - "32-bit tamsayı taşma sınırları [-2147483648, 2147483647] uygulanmalı"
  - "n karakterli metin için çalışma süresi O(n), alan O(1) olmalı"
expected:
  time: { my_atoi: "n" }
  space: "1"
concept_tags: [strings, parsing, boundary-conditions, design]
checklist_extra:
  - "Sayı olmayan karakter görüldüğünde döngü sonlandırılmayıp hata mı veriyor?"
  - "Taşma sınırları kırpma mantığı ile doğru sabitlendi mi?"
reference_solution_path: private/solutions/py-medium-string-to-integer-atoi.py
hint_ladder:
  1: "Karakter dizisi üzerinde baştan ilerlerken boşlukları ve işareti sırayla nasıl geçersin?"
  2: "Rakam okurken toplam sayıyı `toplam = toplam * 10 + rakam` şeklinde nasıl inşa edersin?"
  3: "Bu süreç 'durum makinesi ile dize tamsayı ayrıştırma (atoi parsing)' olarak bilinir."
```

### py-medium-valid-sudoku-board

```yaml
id: py-medium-valid-sudoku-board
version: 1
language: python
engine: none
difficulty: medium
title: "9x9 Sudoku tahtasının geçerliliği"
prompt: |
  9x9 boyutunda kısmen doldurulmuş bir Sudoku tahtasının kurallara göre geçerli olup
  olmadığını denetleyen `is_valid_sudoku(board: list[list[str]]) -> bool` fonksiyonunu
  yazın. Boş hücreler '.' ile gösterilmiştir. Kurallar: Her satır, her sütun ve her 3x3'lük
  dokuz alt kutu 1-9 arasındaki rakamları en fazla birer kez içerebilir. Sudoku'nun
  çözülebilir olup olmadığını değil, mevcut tahtada kural ihlali olup olmadığını denetleyin.
constraints:
  - "Tahta 9x9 sabit boyuttadır; süre O(1) ve alan O(1) olmalı"
  - "Her satır, sütun ve 3x3 kutu için tekrar kontrolü yapılmalı"
expected:
  time: { is_valid_sudoku: "1" }
  space: "1"
concept_tags: [data-structures, hashing, design]
checklist_extra:
  - "3x3 kutuların indeks formülü (r // 3, c // 3) doğru hesaplandı mı?"
  - "Boşluk '.' karakterleri rakam gibi değerlendirilmeyip atlandı mı?"
reference_solution_path: private/solutions/py-medium-valid-sudoku-board.py
hint_ladder:
  1: "Satırlar için 9, sütunlar için 9 ve 3x3 bloklar için 9 ayrı küme tutabilir misin?"
  2: "Bir rakam gördüğünde bu üç kümeden herhangi birinde zaten var olup olmadığını nasıl kontrol edersin?"
  3: "Bu işlem 'küme tabanlı ızgara kısıt doğrulaması' olarak bilinir."
```

### py-medium-course-schedule-cycle

```yaml
id: py-medium-course-schedule-cycle
version: 1
language: python
engine: none
difficulty: medium
title: "Ders ön koşulları ve döngü tespiti"
prompt: |
  Toplam `num_courses` adet ders (0 ile num_courses - 1 arasında numaralı) ve
  [ders, on_kosul] çiftlerinden oluşan bir `prerequisites` listesi verilmiştir. Tüm dersleri
  tamamlamanın mümkün olup olmadığını (ön koşul grafında döngü olup olmadığını) denetleyen
  `can_finish_courses(num_courses: int, prerequisites: list[list[int]]) -> bool` fonksiyonunu
  yazın. Döngü varsa dersler tamamlanamaz (False). V ders ve E ön koşul için O(V + E) sürede çözün.
constraints:
  - "V = num_courses ve E = len(prerequisites) için süre O(V + E) olmalı"
  - "Yönlü grafta döngü tespit edilmeli"
  - "Ek bellek O(V + E) olmalı"
expected:
  time: { can_finish_courses: "V + E" }
  space: "V + E"
concept_tags: [graphs, data-structures, performance]
checklist_extra:
  - "Graf üzerinde DFS yaparken ziyaret durumları (ziyaret edilmedi, ziyaret ediliyor, tamamlandı) 3 renkle ayrıldı mı?"
  - "Kahn algoritması ile giriş dereceleri (in-degree) ve BFS kuyruğu kullanıldı mı?"
reference_solution_path: private/solutions/py-medium-course-schedule-cycle.py
hint_ladder:
  1: "Her dersin kaç adet ön koşulu olduğunu gösteren bir 'giriş derecesi' (in-degree) listesi tutabilir misin?"
  2: "Ön koşulu olmayan dersleri bir kuyruğa alıp tamamladıkça diğer derslerin ön koşul sayısını nasıl azaltırsın?"
  3: "Bu yöntem 'Kahn algoritması ile topolojik sıralama ve döngü tespiti' olarak bilinir."
```

### py-medium-unique-paths-grid

```yaml
id: py-medium-unique-paths-grid
version: 1
language: python
engine: none
difficulty: medium
title: "Izgarada sol üstten sağ alta benzersiz yollar"
prompt: |
  m x n boyutunda bir ızgaranın sol üst köşesinden (0, 0) başlayıp sağ alt köşesine
  (m - 1, n - 1) gitmek isteyen bir robot her adımda yalnızca sağa veya aşağı hareket
  edebilir. Robotun hedef noktaya ulaşabileceği toplam benzersiz yol sayısını hesaplayan
  `unique_paths(m: int, n: int) -> int` fonksiyonunu yazın. m x n boyutlu tam tablo yerine
  yalnızca tek bir satır tutarak O(m * n) zaman ve O(n) ek alanla çözün.
constraints:
  - "Çalışma süresi O(m * n) olmalı"
  - "Ek bellek kullanımı yalnızca O(min(m, n)) olmalı"
expected:
  time: { unique_paths: "m*n" }
  space: "n"
concept_tags: [performance, design, data-structures]
checklist_extra:
  - "m x n boyutunda gereksiz büyük matris oluşturulup bellek harcanıyor mu?"
  - "dp[j] = dp[j] + dp[j - 1] formülü ile tek bir satır üzerinde dinamik güncelleme yapıldı mı?"
reference_solution_path: private/solutions/py-medium-unique-paths-grid.py
hint_ladder:
  1: "Bir hücreye yalnızca üstünden ve solundan gelinebileceğine göre o hücreye çıkan yol sayısı neye eşittir?"
  2: "Tüm ızgarayı tutmak yerine sadece bir önceki satırın değerlerini tutmak yeterli midir?"
  3: "Bu teknik 'alan optimize edilmiş ızgara dinamik programlaması' olarak bilinir."
```

### py-medium-minimum-path-sum

```yaml
id: py-medium-minimum-path-sum
version: 1
language: python
engine: none
difficulty: medium
title: "Izgarada minimum maliyetli yol toplamı"
prompt: |
  Negatif olmayan sayılarla dolu m x n boyutunda bir ızgarada, sol üstten sağ alta kadar
  olan bir yolda geçtiği hücrelerdeki sayıların toplamını minimize eden yolun toplam
  değerini hesaplayan `min_path_sum(grid: list[list[int]]) -> int` fonksiyonunu yazın.
  Robot yalnızca sağa ve aşağı hareket edebilir. m x n hücre sayısı için O(m * n) zamanda
  ve O(1) ek alan (ızgara üzerinde yerinde güncelleyerek) ile çözün.
constraints:
  - "m satır ve n sütun için çalışma süresi O(m * n) olmalı"
  - "Ek bellek matris üzerinde yerinde güncellenerek O(1) olmalı"
expected:
  time: { min_path_sum: "m*n" }
  space: "1"
concept_tags: [data-structures, performance, design]
checklist_extra:
  - "İlk satır ve ilk sütunun kümülatif toplamları doğru başlatıldı mı?"
  - "grid[i][j] hücresi min(üst, sol) + kendisi formülüyle doğru güncelleniyor mu?"
reference_solution_path: private/solutions/py-medium-minimum-path-sum.py
hint_ladder:
  1: "Bir hücreye ulaşmanın minimum maliyeti, o hücrenin kendi değeri ile üst ve sol hücrelerin minimumunun toplamı mıdır?"
  2: "İlk satır yalnızca soldan, ilk sütun yalnızca üstten gelebileceğine göre sınırları nasıl doldurursun?"
  3: "Bu algoritma 'yerinde dinamik programlama ile en düşük maliyetli yol hesabı' olarak bilinir."
```

### py-medium-combination-sum-target

```yaml
id: py-medium-combination-sum-target
version: 1
language: python
engine: none
difficulty: medium
title: "Toplamı hedefe eşit kombinasyonlar"
prompt: |
  Birbirinden farklı pozitif tamsayılardan oluşan bir `candidates` listesi ve bir `target`
  sayısı verilmiştir. Toplamı tam olarak hedefe eşit olan tüm benzersiz kombinasyonları
  listeleyen `combination_sum(candidates: list[int], target: int) -> list[list[int]]`
  fonksiyonunu yazın. Aynı sayı sınırsız sayıda seçilebilir. Kombinasyonların sırası
  önemli değildir, ancak mükerrer kombinasyonlar (örneğin [2, 2, 3] ve [3, 2, 2])
  sonuçta tek bir kez yer almalıdır.
constraints:
  - "Aynı kombinasyon farklı sıralarla birden fazla dönmemeli"
  - "Geri izleme arama uzayında adaylar sıralanarak budama yapılmalı"
expected:
  time: { combination_sum: "2^t" }
  space: "t"
concept_tags: [design, data-structures, performance]
checklist_extra:
  - "Mükerrer kombinasyonları engellemek için geri izlemede başlangıç indeksi ileriye doğru sınırlandı mı?"
  - "Kalan hedef sıfırın altına düştüğünde arama erken sonlandırılıyor mu?"
reference_solution_path: private/solutions/py-medium-combination-sum-target.py
hint_ladder:
  1: "Bir sayıyı birden çok kez kullanabilmek için özyinelemeli çağrıda indeksi artırmadan aynı indekste kalabilir misin?"
  2: "Kalan hedefi aşan sayıları denememek için adayları önceden sıralamak ne kazandırır?"
  3: "Bu yöntem 'budamalı geri izleme ile sınırsız kombinasyon toplamı' olarak bilinir."
```

### py-medium-simplify-path-unix

```yaml
id: py-medium-simplify-path-unix
version: 1
language: python
engine: none
difficulty: medium
title: "Unix dosya yolunu sadeleştirme"
prompt: |
  Bir Unix dosya yolunu mutlak ve sadeleştirilmiş kanonik yola dönüştüren
  `simplify_path(path: str) -> str` fonksiyonunu yazın. Kurallar: 1) Tek nokta '.' mevcut
  dizini temsil eder ve atlanır, 2) Çift nokta '..' bir üst dizine çıkar, 3) Birden fazla
  ardışık eğik çizgi '//' tek eğik çizgiye indirgenir, 4) Sonuç her zaman '/' ile başlamalı
  ve kök dizin hariç sonunda '/' bulunmamalıdır. Bir yığın kullanarak O(n) sürede çözün.
constraints:
  - "n karakterli yol için çalışma süresi O(n), yığın belleği O(n) olmalı"
  - "Kök dizindeyken '..' gelirse kök dizinde kalınmalı"
expected:
  time: { simplify_path: "n" }
  space: "n"
concept_tags: [strings, data-structures, parsing]
checklist_extra:
  - "Kök dizindeyken '..' geldiğinde yığından pop yapılarak IndexError alınıyor mu?"
  - "Yol '/' ile parçalandığında boşluk ve '.' parçaları atlandı mı?"
reference_solution_path: private/solutions/py-medium-simplify-path-unix.py
hint_ladder:
  1: "Yolu '/' karakterine göre parçalara böldüğünde eline geçen dizin adlarını bir yığına nasıl eklersin?"
  2: "'..' gördüğünde yığın boş değilse en üstteki dizini nasıl çıkarırsın?"
  3: "Bu işlem 'yığın tabanlı dosya yolu kanonikleştirmesi (canonical path simplification)' olarak bilinir."
```

### py-medium-maximum-product-subarray

```yaml
id: py-medium-maximum-product-subarray
version: 1
language: python
engine: none
difficulty: medium
title: "Maksimum çarpımlı alt dizi"
prompt: |
  Bir tamsayı listesi verildiğinde, elemanlarının çarpımı en büyük olan kesintisiz alt
  dizinin çarpım değerini bulan `max_product_subarray(nums: list[int]) -> int`
  fonksiyonunu yazın. Listede negatif sayılar ve sıfır bulunabilir. Negatif iki sayının
  çarpımının pozitif olabileceğini hesaba katarak, her adımda hem maksimum hem de
  minimum çarpımı izleyen dinamik bir mantıkla O(n) zamanda ve O(1) alanda çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
expected:
  time: { max_product_subarray: "n" }
  space: "1"
concept_tags: [performance, design, boundary-conditions]
checklist_extra:
  - "Yalnızca maksimum çarpım takip edilerek negatif sayıların çarpımı kaçırılıyor mu?"
  - "Sayı negatif olduğunda anlık maksimum ve minimum değişkenlerinin yer değiştirmesi sağlandı mı?"
reference_solution_path: private/solutions/py-medium-maximum-product-subarray.py
hint_ladder:
  1: "Negatif bir sayıyla karşılaştığında elindeki minimum değer en büyük pozitife dönüşebilir mi?"
  2: "Her adımda hem şimdiye kadarki en büyük çarpımı hem de en küçük (en negatif) çarpımı nasıl güncellersin?"
  3: "Bu yöntem 'çift uçlu ekstremum takibi ile alt dizi dinamik programlaması' olarak bilinir."
```

### py-medium-house-robber-max

```yaml
id: py-medium-house-robber-max
version: 1
language: python
engine: none
difficulty: medium
title: "Komşu evleri soymadan maksimum kazanç"
prompt: |
  Bir sokaktaki her evin içinde bulunan para miktarlarını temsil eden bir liste
  verilmiştir. Yan yana iki ev aynı gece soyulursa alarm çalmaktadır. Alarmı tetiklemeden
  soyulabilecek maksimum para miktarını hesaplayan `rob_houses(nums: list[int]) -> int`
  fonksiyonunu yazın. Liste boşsa 0 dönmelidir. n ev için O(n) zamanda ve O(1) ek
  bellekle çözün.
constraints:
  - "n ev için çalışma süresi O(n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı (liste açılmamalı)"
expected:
  time: { rob_houses: "n" }
  space: "1"
concept_tags: [performance, design, boundary-conditions]
checklist_extra:
  - "O(n) boyutlu tam DP dizisi tutularak bellek kısıtı ihmal ediliyor mu?"
  - "Önceki iki evin maksimum kazançlarını iki değişken ile devretme mantığı kuruldu mu?"
reference_solution_path: private/solutions/py-medium-house-robber-max.py
hint_ladder:
  1: "Bir i evine geldiğinde iki seçeneğin vardır: bu evi soyup i-2'deki kazancı eklemek ya da bu evi atlayıp i-1'deki kazancı korumak."
  2: "Bu kararı vermek için geçmişteki yalnızca son iki maksimum değeri tutmak yeterli midir?"
  3: "Bu klasik problem 'alan optimize edilmiş 1B dinamik programlama' olarak bilinir."
```

### py-medium-find-min-rotated-sorted

```yaml
id: py-medium-find-min-rotated-sorted
version: 1
language: python
engine: none
difficulty: medium
title: "Döndürülmüş sıralı listede minimum elemanı bulma"
prompt: |
  Küçükten büyüğe sıralı ve elemanları benzersiz bir liste bilinmeyen bir pivot
  noktasından döndürülmüştür (örneğin [3, 4, 5, 1, 2]). Bu listenin en küçük elemanını
  bulan `find_min_rotated(nums: list[int]) -> int` fonksiyonunu yazın. Doğrusal tarama
  O(n) sürer; ikili arama prensibiyle O(log n) sürede ve O(1) ek alanda çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(log n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
expected:
  time: { find_min_rotated: "log n" }
  space: "1"
concept_tags: [performance, boundary-conditions, design]
checklist_extra:
  - "Doğrusal tarama veya min() fonksiyonu kullanılarak O(n) mi yapılıyor?"
  - "nums[mid] > nums[right] iken minimumun kesinlikle sağ tarafta olduğu mantığı işletildi mi?"
reference_solution_path: private/solutions/py-medium-find-min-rotated-sorted.py
hint_ladder:
  1: "Orta elemanı listenin en sağındaki elemanla karşılaştırırsan, ortanca sağdakinden büyükse kırılma noktası nerede kalır?"
  2: "Ortanca sağdakinden küçük veya eşitse aramanın sağ sınırını ortaya nasıl çekersin?"
  3: "Bu teknik 'kırılma noktası odaklı ikili arama' olarak bilinir."
```

### py-medium-longest-repeating-char-replacement

```yaml
id: py-medium-longest-repeating-char-replacement
version: 1
language: python
engine: none
difficulty: medium
title: "Karakter değiştirerek en uzun tekdüze alt metin"
prompt: |
  Yalnızca büyük İngilizce harflerden oluşan bir metin ve bir `k` tamsayısı verilmiştir.
  Metindeki en fazla `k` adet karakteri istediğiniz başka bir harfle değiştirme hakkınız
  vardır. Bu işlem sonucunda elde edilebilecek yalnızca aynı harften oluşan en uzun
  alt metnin uzunluğunu döndüren `character_replacement(s: str, k: int) -> int`
  fonksiyonunu yazın. n karakterli metin için kayan pencere yöntemiyle O(n) sürede çözün.
constraints:
  - "n karakterli metin için çalışma süresi O(n) olmalı"
  - "Ek bellek 26 harflik frekans tablosu için O(1) olmalı"
expected:
  time: { character_replacement: "n" }
  space: "1"
concept_tags: [strings, performance, hashing]
checklist_extra:
  - "Pencere boyutu - penceredeki en sık harf sayısı > k olduğunda pencere sol sınırından daraltılıyor mu?"
  - "Her adımda harita baştan taranmadan maksimum frekans değişkeni canlı güncelleniyor mu?"
reference_solution_path: private/solutions/py-medium-longest-repeating-char-replacement.py
hint_ladder:
  1: "Bir penceredeki tüm karakterleri aynı yapmak için değiştirilmesi gereken harf sayısı nedir? (Pencere boyutu - en sık harf sayısı)."
  2: "Bu fark k'dan büyük olduğu anda pencerenin sol kenarını bir birim kaydırmak yeterli midir?"
  3: "Bu yöntem 'azami frekans kısıtlı kayan pencere (sliding window with max frequency)' olarak bilinir."
```

### py-medium-insert-interval

```yaml
id: py-medium-insert-interval
version: 1
language: python
engine: none
difficulty: medium
title: "Sıralı aralık listesine yeni aralık ekleme"
prompt: |
  Başlangıç noktalarına göre sıralı ve birbiriyle kesişmeyen aralıklardan oluşan bir
  `intervals` listesi ve yeni bir `new_interval` verilmiştir. Yeni aralığı listeye
  doğru konuma ekleyen ve varsa oluşan tüm kesişimleri birleştirerek yine sıralı bir
  aralık listesi döndüren `insert_interval(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]`
  fonksiyonunu yazın. Tek geçişte O(n) zamanda çözün.
constraints:
  - "n aralık için çalışma süresi O(n) olmalı"
  - "Dahili sıralama kullanılmamalı"
  - "Ek bellek dönen liste için O(n) olmalı"
expected:
  time: { insert_interval: "n" }
  space: "n"
concept_tags: [data-structures, performance, boundary-conditions]
checklist_extra:
  - "Yeni aralık tüm aralıklardan önce veya sonra geldiğinde IndexError önlendi mi?"
  - "Kesişen tüm aralıklar tek bir aralıkta birleştirilip sonraki kesişmeyenler eklendi mi?"
reference_solution_path: private/solutions/py-medium-insert-interval.py
hint_ladder:
  1: "Yeni aralıktan tamamen önce biten aralıkları doğrudan sonuca ekleyebilir misin?"
  2: "Yeni aralıkla kesişenlerin başlangıcını min, bitişini max ile birleştirip kalanları ne zaman eklersin?"
  3: "Bu algoritma 'üç aşamalı doğrusal aralık yerleştirme ve birleştirme' olarak bilinir."
```

### py-medium-custom-sort-string

```yaml
id: py-medium-custom-sort-string
version: 1
language: python
engine: none
difficulty: medium
title: "Özel harf önceliğine göre metin sıralama"
prompt: |
  Karakterlerin öncelik sırasını belirleyen `order` metni ve sıralanacak `s` metni
  verilmiştir. `s` metnindeki tüm karakterleri `order` metninde geçen öncelik sırasına göre
  yeniden dizen `custom_sort_string(order: str, s: str) -> str` fonksiyonunu yazın.
  `order` içinde geçmeyen karakterler sonucun sonuna herhangi bir sırada eklenebilir.
  Sıralama fonksiyonu kullanmadan, frekans sayımı ile O(len(order) + len(s)) sürede çözün.
constraints:
  - "Dahili .sort() veya sorted() kullanılmamalı"
  - "n = len(s) ve m = len(order) için süre O(n + m), alan O(n) olmalı"
expected:
  time: { custom_sort_string: "n + m" }
  space: "n"
concept_tags: [strings, hashing, performance]
checklist_extra:
  - "order içinde bulunmayan artık karakterler unutuluyor mu?"
  - "Frekans tablosu kullanılarak karakterler adetleri kadar sonuca eklendi mi?"
reference_solution_path: private/solutions/py-medium-custom-sort-string.py
hint_ladder:
  1: "s metnindeki her harfin frekansını bir sözlükte saydıktan sonra order'daki harfleri sırayla nasıl tüketirsin?"
  2: "order bittiğinde sözlükte geriye kalan harfleri sonucun sonuna nasıl eklersin?"
  3: "Bu teknik 'özel alfabe eşlemeli sayma sıralaması (custom order counting sort)' olarak bilinir."
```

### py-medium-reorganize-string

```yaml
id: py-medium-reorganize-string
version: 1
language: python
engine: none
difficulty: medium
title: "Aynı harfler yan yana gelmeyecek şekilde dizme"
prompt: |
  Verilen bir metnin harflerini, hiçbir iki aynı harf yan yana gelmeyecek biçimde yeniden
  düzenleyen `reorganize_string(s: str) -> str` fonksiyonunu yazın. Böyle bir dizilim
  mümkün değilse boş metin dönmelidir. En sık geçen harfin sayısı (len(s) + 1) // 2'den
  fazla ise dizilimin imkansız olduğunu göz önünde bulundurarak O(n) zamanda veya max-heap
  ile O(n log k) zamanda çözün.
constraints:
  - "Olası değilse boş metin dönmeli"
  - "n karakterli metin ve k alfabetik çeşitlilik için süre O(n log k), alan O(n) olmalı"
expected:
  time: { reorganize_string: "n" }
  space: "n"
concept_tags: [strings, hashing, data-structures, design]
checklist_extra:
  - "Mümkün olmayan durumlarda (en sık harf > (n+1)//2) erkenden boş dize dönüldü mü?"
  - "Açgözlü yaklaşımla en sık harfler tek ve çift indekslere serpiştirildi mi?"
reference_solution_path: private/solutions/py-medium-reorganize-string.py
hint_ladder:
  1: "En çok tekrar eden harf dizinin yarısından fazlasını kaplıyorsa yan yana gelmemeleri mümkün müdür?"
  2: "Önce en sık harfi dizinin çift indekslerine (0, 2, 4...) doldurup ardından kalan harfleri yerleştirirsen ne olur?"
  3: "Bu yöntem 'açgözlü çift adımlı frekans yerleşimi (interleaving placement)' olarak bilinir."
```

### py-medium-safe-file-line-counter

```yaml
id: py-medium-safe-file-line-counter
version: 1
language: python
engine: none
difficulty: medium
title: "Büyük dosyalarda güvenli satır ve kelime sayımı"
prompt: |
  Belirtilen dosya yolundaki bir metin dosyasını açıp toplam satır ve kelime sayısını
  bir demet `(satir_sayisi, kelime_sayisi)` olarak döndüren
  `count_file_metrics(filepath: str) -> tuple[int, int]` fonksiyonunu yazın. Dosya
  gigabaytlarca boyutta olabileceğinden `file.read()` veya `file.readlines()` ile tüm
  içeriği tek seferde belleğe yüklemek yasaktır; akış (streaming) halinde satır satır
  okunmalıdır. Dosya bulunamazsa FileNotFoundError fırlatılmalıdır.
constraints:
  - "Dosyanın tamamı belleğe okunmamalı; bellek O(1) olmalı"
  - "Kaynaklar with bloğu ile yönetilmeli"
  - "n satırlı dosya için süre O(n) olmalı"
expected:
  time: { count_file_metrics: "n" }
  space: "1"
concept_tags: [files, resources, exceptions, performance]
checklist_extra:
  - "readlines() çağrılarak tüm dosya tek seferde belleğe mi çekiliyor?"
  - "with bloğu kullanılarak hata durumunda da dosya tanıtıcısının kapanması güvenceye alındı mı?"
reference_solution_path: private/solutions/py-medium-safe-file-line-counter.py
hint_ladder:
  1: "Python'da bir dosya nesnesini for döngüsüne verdiğinde satırları belleği şişirmeden nasıl gezer?"
  2: "Her satırın kelimelerini split() ile sayıp sayaçları O(1) ek bellekte nasıl güncellersin?"
  3: "Bu desen 'akış tabanlı dosya işleme ve bağlam yöneticisi (streaming with context manager)' olarak bilinir."
```

### py-medium-time-based-key-value

```yaml
id: py-medium-time-based-key-value
version: 1
language: python
engine: none
difficulty: medium
title: "Zaman damgalı anahtar-değer deposu"
prompt: |
  Belirli bir zaman damgasıyla (`timestamp`) değer kaydedebilen ve sorgulandığında o zaman
  damgasına eşit ya da ondan küçük en yakın değerin sonucunu getiren bir `TimeMap` sınıfı
  tasarlayın. Metotlar: `set_val(key: str, value: str, timestamp: int) -> None` ve
  `get_val(key: str, timestamp: int) -> str`. Zaman damgaları set_val çağrılarında artan
  sırada gelir. Uygun bir zaman damgası yoksa get_val boş dize dönmelidir. get_val
  işlemi ikili arama kullanarak O(log n) sürede çalışmalıdır.
constraints:
  - "get_val işlemi O(log n) sürede çalışmalı"
  - "set_val işlemi O(1) amortize sürede çalışmalı"
  - "Uygun değer bulunamadığında boş metin dönmeli"
expected:
  time: { set_val: "1*", get_val: "log n" }
  space: "n"
concept_tags: [data-structures, hashing, performance, design]
checklist_extra:
  - "get_val metodunda tüm liste taranarak O(n) mi yapılıyor?"
  - "Zaman damgası sıralı listesinde ikili arama (bisect) ile en büyük <= timestamp bulundu mu?"
reference_solution_path: private/solutions/py-medium-time-based-key-value.py
hint_ladder:
  1: "Her anahtar için (timestamp, value) ikililerini saklayan sıralı bir liste tutabilir misin?"
  2: "Aranan timestamp değerinden küçük veya eşit olan en sağdaki elemanı ikili aramayla nasıl bulursun?"
  3: "Bu yapı 'zaman serisi anahtar-değer eşlemesi ve ikili arama ile en yakın geçmiş sorgusu' olarak bilinir."
```

---

## 4. Zor (Hard) — 50 Soru

### py-hard-median-two-sorted-arrays

```yaml
id: py-hard-median-two-sorted-arrays
version: 1
language: python
engine: none
difficulty: hard
title: "İki sıralı dizinin medyanı"
prompt: |
  Küçükten büyüğe sıralı m ve n elemanlı iki tamsayı listesi verilmiştir. Bu iki listenin
  tüm elemanları birleştirildiğinde oluşacak sıralı kümenin medyan değerini hesaplayan
  `find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float` fonksiyonunu yazın.
  İki listeyi birleştirip sıralamak O((m+n) log(m+n)) veya iki işaretçi ile taramak
  O(m + n) sürecektir. Kısa olan m elemanlı dizi üzerinde ikili arama bölmesi yaparak kesinlikle
  O(log m) zamanında ve O(1) ek alanda çözün.
constraints:
  - "Çalışma süresi kesinlikle O(log m) olmalı (m <= n kısa dizi ikili arama)"
  - "Ek bellek kullanımı O(1) olmalı (birleştirilmiş dizi oluşturulmamalı)"
  - "Toplam eleman sayısı çift olduğunda ortadaki iki sayının aritmetik ortalaması dönmeli"
expected:
  time: { find_median_sorted_arrays: "log m" }
  space: "1"
concept_tags: [performance, boundary-conditions, design]
checklist_extra:
  - "Diziler birleştirilerek O(m + n) süre veya ek bellek kullanılıyor mu?"
  - "Kısa olan dizi üzerinde bölme noktası aranırken sol ve sağ sınırların kesişim koşulu (L1 <= R2 and L2 <= R1) doğru kuruldu mu?"
reference_solution_path: private/solutions/py-hard-median-two-sorted-arrays.py
hint_ladder:
  1: "Birleştirilmiş diziyi iki eşit sol ve sağ yarıya bölecek kesim noktalarını her iki dizide aynı anda düşünebilir misin?"
  2: "Kısa dizi üzerinde bir kesim noktası seçtiğinde, uzun dizideki kesim noktası otomatik olarak (m + n + 1) // 2 - cut1 formülüyle belirlenir mi?"
  3: "Bu algoritma 'iki sıralı dizide ikili arama ile medyan bölmesi' olarak bilinir."
```

### py-hard-trapping-rain-water

```yaml
id: py-hard-trapping-rain-water
version: 1
language: python
engine: none
difficulty: hard
title: "Yağmur suyu birikintisi hesaplama"
prompt: |
  n adet negatif olmayan tamsayıdan oluşan bir yükseklik haritası verilmiştir. Yağmur
  sonrasında bu yükseklik blokları arasında hapsolabilecek toplam su hacmini hesaplayan
  `trap_rain_water(height: list[int]) -> int` fonksiyonunu yazın. Her çubuğun genişliği
  1 birimdir. Her sütun için sol ve sağ maksimumları aramak O(n^2) sürer; iki işaretçi
  veya monotonik yığın yöntemiyle O(n) sürede ve O(1) ek bellekle çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "Boş veya ikiden az elemanlı listelerde 0 dönmeli"
expected:
  time: { trap_rain_water: "n" }
  space: "1"
concept_tags: [performance, design, boundary-conditions]
checklist_extra:
  - "Sol ve sağ maksimum dizileri ayrı listelerde tutularak O(n) bellek harcanıyor mu?"
  - "İki uçtan yaklaşan işaretçilerden küçük olan tarafın maksimumunu güncelleyip farkı toplayan O(1) alan yaklaşımı tercih edildi mi?"
reference_solution_path: private/solutions/py-hard-trapping-rain-water.py
hint_ladder:
  1: "Herhangi bir sütunda biriken su, o sütunun solundaki en yüksek ve sağındaki en yüksek engellerin minimumundan sütunun kendi boyunun çıkarılması mıdır?"
  2: "Sol tarafın tepe noktası sağ tarafın tepe noktasından küçükse, su miktarını sadece sol tepenin belirlediğini fark ettin mi?"
  3: "Bu teknik 'çift uçlu iki işaretçi ile yerinde su birikintisi hesabı' olarak bilinir."
```

### py-hard-merge-k-sorted-lists

```yaml
id: py-hard-merge-k-sorted-lists
version: 1
language: python
engine: none
difficulty: hard
title: "k adet sıralı listeyi tek bir sıralı listede birleştirme"
prompt: |
  Her biri küçükten büyüğe sıralı `k` adet tamsayı listesi verilmiştir. Bu listelerin
  tüm elemanlarını birleştirerek yine küçükten büyüğe sıralı tek bir liste döndüren
  `merge_k_sorted(lists: list[list[int]]) -> list[int]` fonksiyonunu yazın. Toplam eleman
  sayısı N ve liste adedi k olsun. Listeleri ikişer ikişer birleştirmek O(N * k) sürer;
  bir öncelik kuyruğu (min-heap) kullanarak her an k adet listenin en küçük baş elemanlarını
  yarıştırın ve O(N log k) sürede çözün.
constraints:
  - "Toplam N eleman ve k liste için çalışma süresi O(N log k) olmalı"
  - "Ek bellek öncelik kuyruğu boyutu için O(k) olmalı"
  - "Boş alt listeler doğru atlanmalı"
expected:
  time: { merge_k_sorted: "N log k" }
  space: "k"
concept_tags: [data-structures, performance, boundary-conditions]
checklist_extra:
  - "Tüm listeler tek bir büyük listede toplanıp sort() çağrılarak O(N log N) mi yapılıyor?"
  - "Öncelik kuyruğunda elemanla birlikte hangi listeden geldiği bilgisi (değer, liste_idx, eleman_idx) tutuldu mu?"
reference_solution_path: private/solutions/py-hard-merge-k-sorted-lists.py
hint_ladder:
  1: "k adet listenin en başındaki ilk elemanları bir min-heap içine atarsan tepedeki eleman neyi verir?"
  2: "Tepedeki elemanı sonuca ekleyip o listenin bir sonraki elemanını heap'e iterken heap boyutu kaçı aşmaz?"
  3: "Bu algoritma 'k-yollu birleştirmeli öncelik kuyruğu (k-way merge with min-heap)' olarak bilinir."
```

### py-hard-lfu-cache

```yaml
id: py-hard-lfu-cache
version: 1
language: python
engine: none
difficulty: hard
title: "En az sıklıkla kullanılanı atan önbellek (LFU Cache)"
prompt: |
  Belirli bir `capacity` kapasitesine sahip En Az Sıklıkla Kullanılan (LFU - Least Frequently Used)
  veri yapısını sağlayan bir `LFUCache` sınıfı tasarlayın. Metotlar: `get(key: int) -> int`
  ve `put(key: int, value: int) -> None`. get işlemi anahtar varsa değerini döner ve kullanım
  sıklığını 1 artırır; yoksa -1 döner. put işlemi yeni eleman ekler veya günceller; kapasite
  dolduğunda en düşük frekansa sahip anahtarı eler. Eşitlik durumunda en uzun süredir
  erişilmemiş olan (LRU) elenmelidir. Her iki işlem de O(1) zamanda çalışmalıdır.
constraints:
  - "get ve put işlemleri O(1) zamanda çalışmalı"
  - "Aynı frekanstaki anahtarlar arasında LRU kuralı işletilmeli"
  - "capacity <= 0 durumunda put işlemi hiçbir şey eklememeli"
expected:
  time: { get: "1", put: "1" }
  space: "n"
concept_tags: [data-structures, design, performance]
checklist_extra:
  - "Minimum frekans takibi ve frekans-bağlı liste eşlemeleri O(1) sürede güncelleniyor mu?"
  - "Bir anahtarın frekansı arttığında eski frekans listesinden silinip yeni frekans listesine taşınıyor mu?"
reference_solution_path: private/solutions/py-hard-lfu-cache.py
hint_ladder:
  1: "Her frekans değeri için o frekansa sahip anahtarları eklenme sırasıyla tutan çift bağlı listeler (veya sıralı sözlükler) tasarlayabilir misin?"
  2: "O anki genel minimum frekansı (min_freq) tek bir tamsayı değişkeninde nasıl canlı tutarsın?"
  3: "Bu veri yapısı mimarisi 'çift karma tablosu ve frekans bağlı listesi ile LFU önbelleği' olarak bilinir."
```

### py-hard-sliding-window-maximum

```yaml
id: py-hard-sliding-window-maximum
version: 1
language: python
engine: none
difficulty: hard
title: "Kayan pencerede her anın maksimumu"
prompt: |
  Bir tamsayı listesi ve `k` boyutunda bir kayan pencere verilmiştir. Pencere listenin
  en solundan en sağına doğru her adımda bir eleman kaymaktadır. Her pencere konumunda
  pencere içindeki en büyük elemandan oluşan bir liste döndüren
  `max_sliding_window(nums: list[int], k: int) -> list[int]` fonksiyonunu yazın.
  Her adımda pencereyi max() ile taramak O(n * k) sürer; monotonik bir çift uçlu
  kuyruk (deque) yardımıyla O(n) zamanda ve O(k) ek bellekle çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
  - "Ek bellek kullanımı O(k) olmalı"
  - "Pencere dışına çıkan eski indeksler kuyruktan atılmalı"
expected:
  time: { max_sliding_window: "n" }
  space: "k"
concept_tags: [data-structures, performance, design]
checklist_extra:
  - "Her adımda max(nums[i:i+k]) çağrılarak O(n * k) kaba kuvvet mi uygulanıyor?"
  - "Kuyruğun başında daima o anki pencerenin maksimum elemanının indeksi tutuldu mu?"
reference_solution_path: private/solutions/py-hard-sliding-window-maximum.py
hint_ladder:
  1: "Yeni gelen bir sayı kuyrukta kendisinden önce duran daha küçük sayılardan sonra geleceğine göre, o küçük sayıların bir daha maksimum olma şansı kalır mı?"
  2: "Kuyrukta elemanların kendileri yerine indekslerini saklayıp pencere sınırını aşanları soldan nasıl elersin?"
  3: "Bu algoritma 'monotonik azalan çift uçlu kuyruk ile kayan pencere maksimumu' olarak bilinir."
```

### py-hard-word-ladder-shortest

```yaml
id: py-hard-word-ladder-shortest
version: 1
language: python
engine: none
difficulty: hard
title: "Kelime merdiveni en kısa dönüşüm zinciri"
prompt: |
  `begin_word`, `end_word` ve bir kelime listesi `word_list` verilmiştir. Başlangıç
  kelimesinden bitiş kelimesine her adımda yalnızca tek bir harf değiştirerek ve oluşan
  her ara kelimenin `word_list` içinde yer alması şartıyla ulaşılabilecek en kısa dönüşüm
  zincirindeki kelime sayısını hesaplayan `ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int`
  fonksiyonunu yazın. Dönüşüm mümkün değilse 0 dönmelidir. Kelime sayısı n ve kelime
  uzunluğu m olsun. Tek yönlü BFS yerine, her iki uçtan arama yapan iki yönlü BFS
  (bidirectional BFS) ile çok daha küçük bir arama uzayında çözün.
constraints:
  - "end_word sözlükte yoksa hemen 0 dönmeli"
  - "n kelime ve m karakter için çalışma süresi O(n * m^2) olmalı"
  - "Ek bellek sözlük ve kuyruklar için O(n * m) olmalı"
expected:
  time: { ladder_length: "n*m^2" }
  space: "n*m"
concept_tags: [graphs, performance, hashing, strings]
checklist_extra:
  - "Kelime karşılaştırmalarında iç içe döngülerle O(n^2 * m) süreye mi çıkılıyor?"
  - "Aynı anda hem baştan hem sondan ilerleyip kesişim noktasını arayan iki yönlü BFS tercih edildi mi?"
reference_solution_path: private/solutions/py-hard-word-ladder-shortest.py
hint_ladder:
  1: "Aramayı hem başlangıç kelimesinden ileriye hem de bitiş kelimesinden geriye doğru aynı anda başlatırsan ne olur?"
  2: "Her adımda daha az elemana sahip olan yönü genişletmek arama uzayını nasıl daraltır?"
  3: "Bu algoritma 'iki yönlü genişlik öncelikli arama (bidirectional BFS)' olarak bilinir."
```

### py-hard-regular-expression-matching

```yaml
id: py-hard-regular-expression-matching
version: 1
language: python
engine: none
difficulty: hard
title: "Nokta ve yıldız içeren düzenli ifade eşleştirici"
prompt: |
  Bir metin `s` ve bir desen `p` verilmiştir. Desende '.' herhangi bir tek karakterle
  eşleşir; '*' ise kendinden hemen önce gelen karakterin sıfır veya daha fazla kez
  tekrarlanması anlamına gelir. Desen tüm metinle tam olarak eşleşiyor mu denetleyen
  `is_match_regex(s: str, p: str) -> bool` fonksiyonunu yazın. re modülünü kullanmayın.
  İki boyutlu bir dinamik programlama tablosu tasarlayarak O(len(s) * len(p)) zamanda
  ve bellekte çözün.
constraints:
  - "Harici re modülü kesinlikle kullanılmamalı"
  - "n = len(s) ve m = len(p) için çalışma süresi O(n * m), alan O(n * m) olmalı"
  - "'*' karakterinin sıfır eşleşme durumu (karakteri yok sayma) doğru modellenmeli"
expected:
  time: { is_match_regex: "n*m" }
  space: "n*m"
concept_tags: [strings, performance, design]
checklist_extra:
  - "Özyineleme memoize edilmeden kullanılarak üstel O(2^(n+m)) patlamaya mı yol açılıyor?"
  - "'*' durumunda: sıfır eşleşme dp[i][j - 2] ve bir eşleşme dp[i - 1][j] dalları doğru bağlandı mı?"
reference_solution_path: private/solutions/py-hard-regular-expression-matching.py
hint_ladder:
  1: "Bir '*' karakteri gördüğünde, önceki karakteri hiç kullanmama seçeneği tablodaki hangi hücreye bakar?"
  2: "Eğer metindeki karakter desenle eşleşiyorsa '*' karakteri sayesinde metinde bir önceki karaktere nasıl geri dönersin?"
  3: "Bu yöntem '2B dinamik programlama ile düzenli ifade (regex) durum geçişi' olarak bilinir."
```

### py-hard-edit-distance-levenshtein

```yaml
id: py-hard-edit-distance-levenshtein
version: 1
language: python
engine: none
difficulty: hard
title: "Levenshtein düzenleme mesafesi"
prompt: |
  `word1` kelimesini `word2` kelimesine dönüştürmek için gereken minimum işlem sayısını
  (ekleme, silme, değiştirme) hesaplayan `min_edit_distance(word1: str, word2: str) -> int`
  fonksiyonunu yazın. n = len(word1) ve m = len(word2) olmak üzere, standart O(n * m)
  tablo alanını yalnızca iki satır tutarak O(min(n, m)) ek alana düşürün.
constraints:
  - "Çalışma süresi O(n * m) olmalı"
  - "Ek bellek kullanımı yalnızca O(min(n, m)) olmalı (tüm matris saklanmamalı)"
  - "Ekleme, silme ve değiştirme maliyetleri 1 birim kabul edilmeli"
expected:
  time: { min_edit_distance: "n*m" }
  space: "m"
concept_tags: [strings, performance, design]
checklist_extra:
  - "n x m boyutlu tüm matris bellekte tutularak O(n * m) alan mı harcanıyor?"
  - "Harfler eşit olduğunda köşegen maliyetin (ek maliyetsiz) devredilmesi sağlandı mı?"
reference_solution_path: private/solutions/py-hard-edit-distance-levenshtein.py
hint_ladder:
  1: "Mevcut hücreyi hesaplamak için yalnızca bir önceki satırın değerlerine ihtiyaç duyduğunu fark ettin mi?"
  2: "İki dizi tutup satırlar arasında geçiş yaparak bellek kullanımını nasıl tek bir satır boyutuna indirirsin?"
  3: "Bu algoritma 'alan optimize edilmiş Levenshtein dinamik programlaması' olarak bilinir."
```

### py-hard-dijkstra-network-delay

```yaml
id: py-hard-dijkstra-network-delay
version: 1
language: python
engine: none
difficulty: hard
title: "Ağ gecikmesi ve ağırlıklı en kısa yol"
prompt: |
  1'den n'e kadar etiketlenmiş n adet ağ düğümü ve [kaynak, hedef, gecikme_suresi]
  üçlülerinden oluşan bir `times` listesi verilmiştir. Sinyal `k` düğümünden gönderildiğinde,
  ağdaki tüm düğümlerin sinyali alması için gereken minimum toplam süreyi hesaplayan
  `network_delay_time(times: list[list[int]], n: int, k: int) -> int` fonksiyonunu yazın.
  Tüm düğümlere ulaşılamıyorsa -1 dönmelidir. Min-heap tabanlı Dijkstra algoritması
  kullanarak V düğüm ve E kenar için O((V + E) log V) sürede çözün.
constraints:
  - "Negatif ağırlık içermeyen yönlü grafta en kısa yol hesaplanmalı"
  - "V düğüm ve E kenar için çalışma süresi O((V + E) log V) olmalı"
  - "Tüm düğümlere ulaşılamazsa -1 dönmeli"
expected:
  time: { network_delay_time: "E log V" }
  space: "V + E"
concept_tags: [graphs, performance, data-structures]
checklist_extra:
  - "Kuyruktan çekilen mesafe o ana kadar bulunan en kısa mesafeden büyükse atlanıyor mu?"
  - "En sonda tüm düğümlerin mesafelerinin maksimumu doğru alınıp ulaşılamayan varsa -1 dönüldü mü?"
reference_solution_path: private/solutions/py-hard-dijkstra-network-delay.py
hint_ladder:
  1: "Bir min-heap içinde (o_ana_kadarki_sure, dugum) çiftlerini saklayarak her adımda en yakın düğümü nasıl seçersin?"
  2: "Bir düğüme daha kısa bir yolla ulaştığında o düğümün komşularını gevşetme (relaxation) işlemi nasıl yapılır?"
  3: "Bu algoritma 'öncelikli kuyruk (min-heap) ile optimize edilmiş Dijkstra algoritması' olarak bilinir."
```

### py-hard-alien-dictionary

```yaml
id: py-hard-alien-dictionary
version: 1
language: python
engine: none
difficulty: hard
title: "Yabancı dil sözlük sırasından alfabe çıkarımı"
prompt: |
  Bilinmeyen bir dilde alfabetik sıraya göre dizilmiş kelimelerden oluşan bir liste
  verilmiştir. Bu dildeki harflerin geçerli alfabe öncelik sırasını belirleyen
  `alien_order(words: list[str]) -> str` fonksiyonunu yazın. Eğer sıralama geçersizse
  veya döngü içeriyorsa boş dize dönmelidir. Birden fazla geçerli sıra varsa herhangi
  biri dönebilir. Ardışık kelimelerin ilk farklılaşan harflerinden yönlü kenarlar kurarak
  ve topolojik sıralama uygulayarak O(toplam_karakter_sayisi) sürede çözün.
constraints:
  - "Bir kelime kendinden sonra gelen kelimenin ön eki ise ve daha uzunsa (ör. ['abc', 'ab']) hemen boş dize dönmeli"
  - "Döngü tespit edildiğinde boş dize dönmeli"
  - "Tüm benzersiz harfler sonuçta yer almalı"
expected:
  time: { alien_order: "C" }
  space: "V + E"
concept_tags: [graphs, strings, data-structures, parsing]
checklist_extra:
  - "Ön ek hatası (uzun kelimenin kısa ön ekten önce gelmesi) kontrol edildi mi?"
  - "Topolojik sıralama çıktısının boyutu toplam benzersiz harf sayısına eşit mi diye döngü testi yapıldı mı?"
reference_solution_path: private/solutions/py-hard-alien-dictionary.py
hint_ladder:
  1: "Ardışık iki kelimeyi karşılaştırırken farklılaşan ilk karakter çifti hangi harfin hangisinden önce geldiğini gösterir?"
  2: "Bu harf bağımlılıklarından bir yönlü graf kurup topolojik sıralamayla harfleri nasıl dizersin?"
  3: "Bu yöntem 'sözlük sıralamasından graf çıkarımı ve topolojik sıralama' olarak bilinir."
```

### py-hard-longest-valid-parentheses

```yaml
id: py-hard-longest-valid-parentheses
version: 1
language: python
engine: none
difficulty: hard
title: "En uzun geçerli parantez alt dizisi"
prompt: |
  Yalnızca '(' ve ')' karakterlerinden oluşan bir metinde, parantez dengesi kuralına
  tamamen uyan en uzun kesintisiz alt metnin uzunluğunu bulan
  `longest_valid_parentheses(s: str) -> int` fonksiyonunu yazın. Örneğin ')()())' için
  en uzun geçerli alt metin '()' olup uzunluğu 4'tür. Tüm alt metinleri denemek O(n^3)
  sürer; bir yığın indeks takibiyle O(n) zamanda ve O(n) alanda ya da çift geçişli
  sayaçla O(n) zaman ve O(1) alanda çözün.
constraints:
  - "n karakterli metin için çalışma süresi O(n) olmalı"
  - "Ek bellek en fazla O(n) olmalı"
  - "Geçerli alt dize kesintisiz olmalı"
expected:
  time: { longest_valid_parentheses: "n" }
  space: "n"
concept_tags: [strings, data-structures, performance]
checklist_extra:
  - "Yığına başlangıç referansı olarak -1 indeksi atıldı mı?"
  - "Kapatma parantezi geldiğinde yığından eleman çekilip yığın boşsa o anki indeks yeni taban olarak kaydediliyor mu?"
reference_solution_path: private/solutions/py-hard-longest-valid-parentheses.py
hint_ladder:
  1: "Yığına karakterler yerine indeksleri atarsan, geçerli bir parantez kapandığında uzunluğu indeks farkıyla nasıl bulursun?"
  2: "Yığının en altında daima 'en son geçerli olmayan sınırın indeksi' tutulursa her pop sonrasında uzunluk ne olur?"
  3: "Bu yöntem 'indeks tabanlı yığın ile en uzun geçerli parantez tespiti' olarak bilinir."
```

### py-hard-largest-rectangle-histogram

```yaml
id: py-hard-largest-rectangle-histogram
version: 1
language: python
engine: none
difficulty: hard
title: "Histogramdaki en büyük dikdörtgen alanı"
prompt: |
  Her sütununun genişliği 1 birim olan bir histogram çubuk yükseklikleri listesi
  verilmiştir. Bu histogram içinde oluşturulabilecek en büyük dikdörtgenin alanını
  hesaplayan `largest_rectangle_area(heights: list[int]) -> int` fonksiyonunu yazın.
  Her sütun çiftini denemek O(n^2) sürer; monotonik artan bir yığın yardımıyla her
  çubuğun kendisini en kısa kabul eden maksimum sol ve sağ sınırlarını belirleyerek
  O(n) sürede ve O(n) ek bellekle çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
  - "Ek bellek kullanımı O(n) olmalı"
expected:
  time: { largest_rectangle_area: "n" }
  space: "n"
concept_tags: [data-structures, performance, design]
checklist_extra:
  - "Dizi sonuna 0 yüksekliğinde yapay bir eleman eklenerek yığındaki kalan elemanların boşaltılması sağlandı mı?"
  - "Yığından çıkarılan çubuğun genişliği (sağ_indeks - sol_indeks - 1) formülüyle doğru hesaplandı mı?"
reference_solution_path: private/solutions/py-hard-largest-rectangle-histogram.py
hint_ladder:
  1: "Bir çubuğu yükseklik olarak kabul eden en geniş dikdörtgen nereye kadar uzanabilir? (Kendinden kısa ilk sol ve sağ çubuklara kadar)."
  2: "Yığında artan sırada çubuk indeksleri tutarsan, daha kısa bir çubuk gördüğünde yığındakileri pop edip alanlarını nasıl hesaplarsın?"
  3: "Bu klasik algoritma 'monotonik artan yığın ile histogram alan optimizasyonu' olarak bilinir."
```

### py-hard-maximal-rectangle-binary-matrix

```yaml
id: py-hard-maximal-rectangle-binary-matrix
version: 1
language: python
engine: none
difficulty: hard
title: "İkili matriste 1'lerden oluşan en büyük dikdörtgen"
prompt: |
  '0' ve '1'lerden oluşan m x n boyutunda bir matris verilmiştir. Yalnızca '1'lerden
  oluşan en büyük dikdörtgenin alanını hesaplayan `maximal_rectangle(matrix: list[list[str]]) -> int`
  fonksiyonunu yazın. Matris boşsa 0 dönmelidir. Her satırı kümülatif yüksekliklerden
  oluşan bir histogram tabanı gibi düşünerek, histogramda maksimum alan algoritmasını
  her satır için çağırın ve O(m * n) zamanda çözün.
constraints:
  - "m satır ve n sütun için çalışma süresi O(m * n) olmalı"
  - "Ek bellek kullanımı tek bir satır boyutu olan O(n) olmalı"
expected:
  time: { maximal_rectangle: "m*n" }
  space: "n"
concept_tags: [data-structures, performance, design]
checklist_extra:
  - "Hücrede '0' görüldüğünde o sütunun histogram yüksekliği sıfırlanıyor mu?"
  - "Her satır güncellendikten sonra monotonik yığın fonksiyonu çağrılıyor mu?"
reference_solution_path: private/solutions/py-hard-maximal-rectangle-binary-matrix.py
hint_ladder:
  1: "Matrisin her bir satırını yer seviyesi kabul edip yukarıya doğru uzanan ardışık '1'leri sütun yükseklikleri yapabilir misin?"
  2: "Elde edilen bu dinamik histogram dizisini bir önceki sorudaki O(n) alan algoritmasıyla çözersen toplam süre ne olur?"
  3: "Bu teknik 'dinamik histogram dönüşümü ile matriste maksimum dikdörtgen tespiti' olarak bilinir."
```

### py-hard-trie-prefix-tree

```yaml
id: py-hard-trie-prefix-tree
version: 1
language: python
engine: none
difficulty: hard
title: "Ön ek ağacı (Trie) tasarımı"
prompt: |
  Kelimeleri verimli bir şekilde saklayan ve ön ek sorguları yapabilen bir `Trie`
  sınıfı tasarlayın. Desteklenecek metotlar: 1) `insert(word: str) -> None`: Kelimeyi ağaca ekler,
  2) `search(word: str) -> bool`: Kelime ağaçta tam olarak varsa True döner,
  3) `starts_with(prefix: str) -> bool`: Ağaçta bu ön ekle başlayan en az bir kelime varsa
  True döner. Her üç işlem de aranan kelimenin uzunluğu m için O(m) sürede çalışmalıdır.
constraints:
  - "insert, search ve starts_with işlemleri O(m) zamanda çalışmalı (m = kelime uzunluğu)"
  - "Düğümlerde kelime sonunu belirten bir bayrak (is_end) tutulmalı"
  - "Boşluk veya geçersiz aramalarda KeyError fırlatılmamalı"
expected:
  time: { insert: "m", search: "m", starts_with: "m" }
  space: "n*m"
concept_tags: [data-structures, design, strings]
checklist_extra:
  - "starts_with ile search ayrımı (kelime sonu bayrağı kontrolü) doğru yapıldı mı?"
  - "Her düğümde çocukları tutmak için sözlük yapısı kullanıldı mı?"
reference_solution_path: private/solutions/py-hard-trie-prefix-tree.py
hint_ladder:
  1: "Her düğümde karakterlerden sonraki düğümlere giden bir sözlük ve bir kelime_sonu mu (boolean) bayrağı tutabilir misin?"
  2: "Arama yaparken harf harf ilerleyip düğüm biterse durmak, harfler bitince de bayrağı kontrol etmek yeterli midir?"
  3: "Bu veri yapısı 'ön ek ağacı (Trie / prefix tree)' olarak bilinir."
```

### py-hard-word-search-grid-trie

```yaml
id: py-hard-word-search-grid-trie
version: 1
language: python
engine: none
difficulty: hard
title: "Izgarada sözlükteki tüm kelimeleri bulma"
prompt: |
  m x n boyutunda harflerden oluşan bir tahta ve bir `words` kelime listesi verilmiştir.
  Tahta üzerinde yatay ve dikey komşu hücrelerde gezinerek oluşturulabilecek tüm
  kelimeleri bulan `find_words_in_board(board: list[list[str]], words: list[str]) -> list[str]`
  fonksiyonunu yazın. Bir hücre aynı kelime içinde iki kez kullanılamaz. Her kelime için
  baştan DFS yapmak yerine, kelimeleri bir Trie ağacında toplayıp ızgara üzerinde tek bir
  budamalı DFS gezintisi ile çözün.
constraints:
  - "Kelimeler Trie yapısına eklenerek arama uzayı budanmalı"
  - "Bulunan kelimeler Trie'den silinerek veya tekilleştirilerek mükerrer sonuç engellenmeli"
  - "Ziyaret edilen hücreler geçici işaretlenip geri dönüşte (backtrack) eski haline getirilmeli"
expected:
  time: { find_words_in_board: "m*n*4^L" }
  space: "W*L"
concept_tags: [graphs, strings, data-structures, design]
checklist_extra:
  - "Her kelime için tahta baştan taranarak kaba kuvvet O(K * m * n * 4^L) mi yapılıyor?"
  - "Hücre ziyaret işareti '#' ile yapılıp geri izlemede orijinal karaktere döndürüldü mü?"
reference_solution_path: private/solutions/py-hard-word-search-grid-trie.py
hint_ladder:
  1: "Aranan kelimelerin tamamını bir Trie ağacına eklersen, ızgarada bir harfe bastığında Trie'de o harfin çocuğu yoksa aramayı hemen kesebilir misin?"
  2: "Trie'de kelime sonuna ulaştığında kelimeyi sonuç listesine ekleyip Trie'den temizlemek neden faydalıdır?"
  3: "Bu algoritma 'Trie destekli geri izleme ile ızgarada çoklu kelime arama' olarak bilinir."
```

### py-hard-minimum-window-substring

```yaml
id: py-hard-minimum-window-substring
version: 1
language: python
engine: none
difficulty: hard
title: "Hedef karakterleri içeren en küçük alt metin"
prompt: |
  İki metin `s` ve `t` verilmiştir. `s` içinde `t`'deki tüm karakterleri (tekrarlarıyla
  birlikte) kapsayan en kısa kesintisiz alt metni bulan `min_window(s: str, t: str) -> str`
  fonksiyonunu yazın. Böyle bir alt metin yoksa boş metin dönmelidir. Tüm alt metinleri
  denemek O(n^2) sürer; kayan pencere ve eşleşen karakter sayacı ile O(len(s) + len(t))
  sürede çözün.
constraints:
  - "n = len(s) ve m = len(t) için çalışma süresi O(n + m) olmalı"
  - "Ek bellek karakter kümesi boyutu için O(1) olmalı"
  - "Tekrarlı karakter sayıları tam olarak karşılanmalı"
expected:
  time: { min_window: "n + m" }
  space: "1"
concept_tags: [strings, performance, hashing, boundary-conditions]
checklist_extra:
  - "Pencere t'nin tüm şartlarını sağladığında sol kenar daraltılarak minimum boyut aranıyor mu?"
  - "Karakterlerin hedef frekansları tek tek tüm sözlük karşılaştırılarak O(26) gecikmeyle mi yapılıyor yoksa bir 'eşleşen_tur' sayacıyla mı takip ediliyor?"
reference_solution_path: private/solutions/py-hard-minimum-window-substring.py
hint_ladder:
  1: "Sağ işaretçiyi ilerletip hedef harfleri toplarken, gereken tüm harfler sağlandığında sol işaretçiyi nereye kadar çekebilirsin?"
  2: "Sol kenarı ilerletirken pencereden çıkan harf hedef şartını bozduğu an pencereyi tekrar sağdan genişletmek ne sağlar?"
  3: "Bu algoritma 'değişken boyutlu kayan pencere ile minimum kapsayan alt dize (minimum window substring)' olarak bilinir."
```

### py-hard-burst-balloons-max-coins

```yaml
id: py-hard-burst-balloons-max-coins
version: 1
language: python
engine: none
difficulty: hard
title: "Balon patlatma maksimum altın oyunu"
prompt: |
  n adet balonun üzerinde yazan sayıları temsil eden bir tamsayı listesi `nums` verilmiştir.
  i. balonu patlattığınızda `nums[i-1] * nums[i] * nums[i+1]` kadar altın kazanırsınız.
  Dizi sınırlarının dışındaki komşular 1 kabul edilir. Balonları doğru sırada patlatarak
  kazanılabilecek maksimum altın miktarını hesaplayan `max_coins(nums: list[int]) -> int`
  fonksiyonunu yazın. Patlatma işlemi komşulukları değiştirdiğinden, tersten düşünerek
  (en son patlayacak balona göre) aralık dinamik programlamasıyla O(n^3) zamanda çözün.
constraints:
  - "n eleman için çalışma süresi O(n^3), bellek O(n^2) olmalı"
  - "Sınırlar için dizinin başına ve sonuna 1 değerleri eklenmeli"
expected:
  time: { max_coins: "n^3" }
  space: "n^2"
concept_tags: [performance, design, data-structures]
checklist_extra:
  - "İlk patlayan balona göre düşünüp alt problemlerin birbirine bağımlı hale gelmesi tuzağına düşüldü mü?"
  - "Bir (left, right) aralığında EN SON patlayacak balon k seçilerek bağımsız alt problemler kuruldu mu?"
reference_solution_path: private/solutions/py-hard-burst-balloons-max-coins.py
hint_ladder:
  1: "İlk patlatılan balon yerine, o aralıkta en son patlatılan balonu seçersen sol ve sağ alt problemlerin komşuları sabit kalır mı?"
  2: "Aralık uzunluğu 1'den n'e kadar artırılarak dp[left][right] tablosu nasıl doldurulur?"
  3: "Bu yöntem 'tersine kurgulanan aralık dinamik programlaması (interval DP)' olarak bilinir."
```

### py-hard-serialize-deserialize-binary-tree

```yaml
id: py-hard-serialize-deserialize-binary-tree
version: 1
language: python
engine: none
difficulty: hard
title: "İkili ağacı dizgeye serileştirme ve geri yükleme"
prompt: |
  Bir ikili ağacı bir metne serileştiren (serialize) ve bu metni tekrar orijinal ikili
  ağaç yapısına dönüştüren (deserialize) iki fonksiyon yazın: `serialize(root) -> str`
  ve `deserialize(data: str) -> Node | None`. Düğümler `{'val': int, 'left': ..., 'right': ...}`
  biçimindedir. Boş düğümler '#' veya 'None' ile temsil edilebilir. Ağaçtaki düğüm sayısı n
  için her iki işlem de doğrusal O(n) zamanda ve O(n) alanda çalışmalıdır.
constraints:
  - "serialize ve deserialize işlemleri O(n) zamanda çalışmalı"
  - "Ağaç yapısı ve değerler birebir aslına uygun geri yüklenmeli"
  - "Öncelikli dolaşma (preorder) veya seviye dolaşması (BFS) kullanılmalı"
expected:
  time: { serialize: "n", deserialize: "n" }
  space: "n"
concept_tags: [graphs, data-structures, strings, parsing]
checklist_extra:
  - "Boş düğümler serileştirme dizesinde işaretlenmeyip yapısal bilgi kayba uğruyor mu?"
  - "Geri yüklemede yineleyici (iterator) kullanılarak dizge tek geçişte O(n) sürede tüketildi mi?"
reference_solution_path: private/solutions/py-hard-serialize-deserialize-binary-tree.py
hint_ladder:
  1: "Ağacı preorder (kök, sol, sağ) şeklinde gezip boş düğümlere özel bir ayraç koyarak metne çevirebilir misin?"
  2: "Geri yüklerken metni parçalayıp bir kuyruk veya yineleyici üzerinden sıradaki elemanı çekerek kökü ve alt çocukları özyinelemeyle nasıl kurarsın?"
  3: "Bu işlem 'preorder dolaşma ile ağaç serileştirme ve seriden çıkarma (tree serialization)' olarak bilinir."
```

### py-hard-course-schedule-order

```yaml
id: py-hard-course-schedule-order
version: 1
language: python
engine: none
difficulty: hard
title: "Ders ön koşulları tam tamamlama sırası"
prompt: |
  `num_courses` adet ders ve `prerequisites` listesi verilmiştir. Tüm dersleri alabilmek
  için izlenmesi gereken geçerli bir ders sıralamasını liste olarak döndüren
  `find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]` fonksiyonunu
  yazın. Eğer dersleri tamamlamak imkansızsa (döngü varsa) boş liste dönmelidir.
  Birden fazla geçerli sıra varsa herhangi biri döndürülebilir. V ders ve E ön koşul
  için Kahn algoritması veya DFS ile O(V + E) sürede çözün.
constraints:
  - "Döngü varsa boş liste dönmeli"
  - "V ders ve E ön koşul için süre O(V + E), alan O(V + E) olmalı"
  - "Tüm dersler sıralamada yer almalı"
expected:
  time: { find_order: "V + E" }
  space: "V + E"
concept_tags: [graphs, data-structures, performance]
checklist_extra:
  - "Döngü durumunda eksik ders listesi mi dönülüyor yoksa kesinlikle boş liste mi dönülüyor?"
  - "Kahn algoritmasında kuyruktan çıkan her ders sonuç listesine eklenip komşuların giriş dereceleri azaltıldı mı?"
reference_solution_path: private/solutions/py-hard-course-schedule-order.py
hint_ladder:
  1: "Giriş derecesi (in-degree) 0 olan dersleri bir kuyruğa alıp işledikçe komşu derslerin derecesini nasıl azaltırsın?"
  2: "Sonuç listesinin uzunluğu num_courses'a eşit değilse bu ne anlama gelir?"
  3: "Bu algoritma 'giriş derecesi kuyruğu ile topolojik sıralama (Kahn algorithm)' olarak bilinir."
```

### py-hard-min-cost-connect-all-points

```yaml
id: py-hard-min-cost-connect-all-points
version: 1
language: python
engine: none
difficulty: hard
title: "Noktaları minimum kabloyla bağlama (Minimum Kapsayan Ağaç)"
prompt: |
  2 boyutlu düzlemde n adet noktanın koordinatları verilmiştir. İki nokta [xi, yi] ve
  [xj, yj] arasındaki bağlantı maliyeti Manhattan mesafesidir (|xi - xj| + |yi - yj|).
  Tüm noktaları birbirine bağlayan ve toplam maliyeti en küçük olan ağın (Minimum Spanning Tree)
  maliyetini hesaplayan `min_cost_connect_points(points: list[list[int]]) -> int`
  fonksiyonunu yazın. Nokta sayısı n için Prim veya Kruskal algoritması kullanarak
  O(n^2) veya O(n^2 log n) sürede çözün.
constraints:
  - "n nokta için çalışma süresi en fazla O(n^2 log n) olmalı"
  - "Ek bellek kullanımı O(n^2) olmalı"
expected:
  time: { min_cost_connect_points: "n^2" }
  space: "n"
concept_tags: [graphs, performance, data-structures]
checklist_extra:
  - "Tüm kenarları önceden üretip hafızayı şişirmek yerine her adımda en yakın noktayı güncelleyen Prim algoritması düşünüldü mü?"
  - "Ziyaret edilen noktalar bir kümede toplanıp n noktaya ulaşıldığında döngü bitirildi mi?"
reference_solution_path: private/solutions/py-hard-min-cost-connect-all-points.py
hint_ladder:
  1: "Her adımda ağaca dahil edilmiş noktalar kümesine en yakın olan yeni noktayı açgözlü olarak nasıl seçersin?"
  2: "Prim algoritmasında min-heap veya O(n) doğrusal dizi araması ile her adımda en ucuz kenarı nasıl çekersin?"
  3: "Bu klasik problem 'yoğun graflarda Prim algoritması ile minimum kapsayan ağaç (MST)' olarak bilinir."
```

### py-hard-n-queens-valid-placements

```yaml
id: py-hard-n-queens-valid-placements
version: 1
language: python
engine: none
difficulty: hard
title: "N-Vezir tahtası geçerli yerleşimleri"
prompt: |
  n x n boyutundaki bir satranç tahtasına n adet veziri hiçbir vezirin birbirini tehdit
  etmeyeceği (aynı satır, sütun veya çaprazda olmayacak) şekilde yerleştiren tüm geçerli
  çözümleri döndüren `solve_n_queens(n: int) -> list[list[str]]` fonksiyonunu yazın.
  Her çözüm tahtayı temsil eden n adet dizeden oluşmalı, vezirler 'Q', boş kareler '.'
  ile gösterilmelidir. Sütun ve çapraz tehditlerini O(1) sürede denetleyen kümelerle
  budamalı geri izleme yaparak çözün.
constraints:
  - "Vezirlerin çapraz tehditleri (r - c ve r + c) kümelerle O(1) sürede doğrulanmalı"
  - "n için geçerli tüm çözümler listelenmeli"
expected:
  time: { solve_n_queens: "n!" }
  space: "n"
concept_tags: [design, data-structures, performance]
checklist_extra:
  - "Çapraz kontrolleri için her adımda tüm tahta taranarak gereksiz karesel kontrol yapılıyor mu?"
  - "Ana çapraz (r - c) ve ikincil çapraz (r + c) için iki ayrı küme tutuldu mu?"
reference_solution_path: private/solutions/py-hard-n-queens-valid-placements.py
hint_ladder:
  1: "Aynı çaprazda bulunan karelerin satır ve sütun indislerinin farkı (r - c) veya toplamı (r + c) sabit midir?"
  2: "Bu fark ve toplamları birer kümede tutarak bir karenin tehdit altında olup olmadığını O(1) sürede nasıl anlarsın?"
  3: "Bu yöntem 'çapraz hash takibi ile N-Vezir geri izleme algoritması' olarak bilinir."
```

### py-hard-binary-tree-maximum-path-sum

```yaml
id: py-hard-binary-tree-maximum-path-sum
version: 1
language: python
engine: none
difficulty: hard
title: "İkili ağaçta maksimum yol toplamı"
prompt: |
  Düğümleri `{'val': int, 'left': ..., 'right': ...}` biçiminde tanımlanmış bir ikili
  ağaçta, herhangi iki düğüm arasında uzanan ve her düğümden en fazla bir kez geçen bir
  yoldaki düğüm değerlerinin toplamının alabileceği maksimum değeri hesaplayan
  `max_path_sum(root: dict[str, object] | None) -> int` fonksiyonunu yazın. Yolun kökten
  geçmesi zorunlu değildir ve düğüm değerleri negatif olabilir. Post-order DFS dolaşmasıyla
  O(n) sürede ve O(h) yığın alanında çözün.
constraints:
  - "Tüm düğüm değerleri negatif olduğunda en az bir düğüm seçilmeli (en büyük negatif dönmeli)"
  - "n düğüm için çalışma süresi O(n), çağrı yığını O(h) olmalı"
expected:
  time: { max_path_sum: "n" }
  space: "h"
concept_tags: [graphs, performance, boundary-conditions, design]
checklist_extra:
  - "Alt ağaçtan gelen kazanç negatif olduğunda max(0, gain) ile budanmayıp sonuca zarar veriyor mu?"
  - "Bir düğüm ebeveynine yalnızca tek bir kolun (sol veya sağ) maksimumunu döndürürken global maksimumu her iki kolun toplamıyla güncelliyor mu?"
reference_solution_path: private/solutions/py-hard-binary-tree-maximum-path-sum.py
hint_ladder:
  1: "Bir düğüm kendi ebeveynine giden yola hem sol hem sağ çocuğunu aynı anda dahil edebilir mi? (Hayır, yol çatallanamaz)."
  2: "Fakat o düğümü tepe noktası kabul eden bir yol için `sol_kazanc + dugum.val + sag_kazanc` global rekoru kırabilir mi?"
  3: "Bu algoritma 'aşağıdan yukarıya post-order DFS ile ağaçta maksimum yol kazancı hesabı' olarak bilinir."
```

### py-hard-count-smaller-numbers-after-self

```yaml
id: py-hard-count-smaller-numbers-after-self
version: 1
language: python
engine: none
difficulty: hard
title: "Kendinden sonra gelen küçük elemanların sayısı"
prompt: |
  Bir tamsayı listesi `nums` verildiğinde, her `nums[i]` elemanı için o elemanın sağında
  kalan ve kendisinden kesinlikle daha küçük olan elemanların sayısını hesaplayıp bir
  liste olarak döndüren `count_smaller_after(nums: list[int]) -> list[int]` fonksiyonunu
  yazın. Her eleman için sağı taramak O(n^2) sürer; birleştirmeli sıralama (merge sort)
  esnasında elemanların indekslerini takip ederek ya da Fenwick ağacı ile O(n log n)
  sürede çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(n log n) olmalı"
  - "İç içe karesel döngüler kullanılmamalı"
  - "Ek bellek kullanımı O(n) olmalı"
expected:
  time: { count_smaller_after: "n log n" }
  space: "n"
concept_tags: [data-structures, performance, design]
checklist_extra:
  - "Sıralama sırasında sayıların orijinal indekslerini kaybetmemek için (sayı, indeks) çiftleri kullanıldı mı?"
  - "Merge sort birleştirmesinde sağ yarıdan sol yarıya geçen eleman sayısı sol elemanın sayacına eklendi mi?"
reference_solution_path: private/solutions/py-hard-count-smaller-numbers-after-self.py
hint_ladder:
  1: "Birleştirmeli sıralamada sol yarıdaki bir eleman sağ yarıdaki bir elemandan büyükse, sağdaki eleman sola ne zaman atlar?"
  2: "Sağ yarıdan çekilen her küçük eleman, sol yarıda bekleyen o anki elemandan daha küçük bir sayının sağda yer aldığını kanıtlamaz mı?"
  3: "Bu teknik 'birleştirmeli sıralama modifikasyonu ile ters sıra (inversion) sayımı' olarak bilinir."
```

### py-hard-sudoku-solver

```yaml
id: py-hard-sudoku-solver
version: 1
language: python
engine: none
difficulty: hard
title: "Sudoku tahtası çözücü"
prompt: |
  9x9 boyutunda kısmen doldurulmuş bir Sudoku tahtasını doğrudan üzerinde (in-place)
  çözerek tamamlayan `solve_sudoku(board: list[list[str]]) -> None` fonksiyonunu yazın.
  Boş hücreler '.' ile gösterilmiştir. Çözümün kesinlikle tek ve var olduğu garanti
  edilmiştir. Satır, sütun ve 3x3 kutu kısıtlarını sağlayan geçerli rakamları deneyen
  ve çıkmaza girdiğinde geri adım atan budamalı bir geri izleme (backtracking) algoritması
  tasarlayın.
constraints:
  - "Tahta yerinde (in-place) güncellenmeli"
  - "Geri izlemede her boş hücreye yalnızca kuralı sağlayan 1-9 rakamları denenmeli"
  - "Çözüm bulunduğunda arama hemen sonlandırılmalı"
expected:
  time: { solve_sudoku: "9^b" }
  space: "1"
concept_tags: [design, data-structures, hashing]
checklist_extra:
  - "Bir rakamın satır, sütun ve 3x3 kutuda var olup olmadığını denetleyen yardımcı fonksiyon yazıldı mı?"
  - "Geri izleme adımı başarısız olduğunda hücre tekrar '.' yapılarak geri alındı mı?"
reference_solution_path: private/solutions/py-hard-sudoku-solver.py
hint_ladder:
  1: "İlk boş hücreyi bulup oraya 1'den 9'a kadar geçerli bir rakam koymayı deneyebilir misin?"
  2: "Eğer sonraki boş hücreler için çözüm bulunamazsa koyduğun rakamı geri silip bir sonraki rakamı nasıl denersin?"
  3: "Bu algoritma 'kısıt doyurma ve geri izleme ile Sudoku çözümü (backtracking constraint satisfaction)' olarak bilinir."
```

### py-hard-subarrays-with-k-different-integers

```yaml
id: py-hard-subarrays-with-k-different-integers
version: 1
language: python
engine: none
difficulty: hard
title: "Tam olarak k farklı tamsayı içeren alt diziler"
prompt: |
  Bir tamsayı listesi ve pozitif bir `k` tamsayısı verilmiştir. İçerisinde tam olarak `k`
  adet farklı tamsayı barındıran kesintisiz alt dizilerin sayısını hesaplayan
  `subarrays_with_k_distinct(nums: list[int], k: int) -> int` fonksiyonunu yazın.
  Doğrudan 'tam k' koşulunu kayan pencereyle izlemek zordur; bu nedenle
  `tam_k = en_fazla(k) - en_fazla(k - 1)` matematiksel dönüşümünü kullanarak,
  kayan pencereyle iki geçişte O(n) sürede ve O(k) ek bellekle çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(n) olmalı"
  - "Ek bellek frekans tablosu için O(k) olmalı"
  - "tam_k = at_most(k) - at_most(k - 1) formülü uygulanmalı"
expected:
  time: { subarrays_with_k_distinct: "n" }
  space: "k"
concept_tags: [performance, design, hashing]
checklist_extra:
  - "Kayan pencere ile doğrudan 'tam k' aranırken sol kenarın ne zaman kaydırılacağı belirsizliğine düşüldü mü?"
  - "'En fazla k farklı sayı içeren alt dizi sayısı' fonksiyonu yazılarak iki kez çağrıldı mı?"
reference_solution_path: private/solutions/py-hard-subarrays-with-k-different-integers.py
hint_ladder:
  1: "Bir pencerede en fazla k farklı sayı varken, sağ ucu sabit tutup oluşturulabilecek alt dizi sayısı pencerenin uzunluğu kadar mıdır?"
  2: "'En fazla k farklı' kümesinden 'en fazla k-1 farklı' kümesini çıkarırsan geriye ne kalır?"
  3: "Bu yaklaşım 'en fazla k dönüşümü ile tam k elemanlı kayan pencere hesabı' olarak bilinir."
```

### py-hard-longest-increasing-path-matrix

```yaml
id: py-hard-longest-increasing-path-matrix
version: 1
language: python
engine: none
difficulty: hard
title: "Matriste kesinlikle artan en uzun yol"
prompt: |
  m x n boyutunda bir tamsayı matrisi verilmiştir. Herhangi bir hücreden başlayıp komşu
  (yukarı, aşağı, sol, sağ) hücrelere hareket ederek yalnızca değerlerin kesinlikle arttığı
  bir rota çizilecektir. Bu rotanın içerebileceği maksimum hücre sayısını hesaplayan
  `longest_increasing_path(matrix: list[list[int]]) -> int` fonksiyonunu yazın.
  Aynı yolları tekrar hesaplamamak için her hücreden başlayan en uzun yolu bir tabloda
  saklayarak (memoization) DFS ile O(m * n) zamanda ve O(m * n) alanda çözün.
constraints:
  - "m satır ve n sütun için çalışma süresi O(m * n) olmalı"
  - "Ek bellek memoization tablosu için O(m * n) olmalı"
  - "Döngü oluşamayacağı (kesin artış kuralı) göz önünde bulundurulmalı"
expected:
  time: { longest_increasing_path: "m*n" }
  space: "m*n"
concept_tags: [graphs, performance, design, data-structures]
checklist_extra:
  - "Hücreler için daha önce hesaplanan en uzun yol memoize edilmeyip üstel süreye mi çıkılıyor?"
  - "Komşuya geçiş şartı matrix[yeni_r][yeni_c] > matrix[r][c] doğru denetlendi mi?"
reference_solution_path: private/solutions/py-hard-longest-increasing-path-matrix.py
hint_ladder:
  1: "Her adımda sayılar kesinlikle büyümek zorunda olduğuna göre bu graf üzerinde bir döngü oluşması mümkün müdür? (Yönlü Döngüsüz Graf - DAG)."
  2: "Bir hücreden başlayabilecek en uzun yolu bir kez hesaplayıp memo tablosuna kaydedersen her hücreye kaç kez girersin?"
  3: "Bu yöntem 'matriste önbellekli derinlik öncelikli arama (memoized DFS on DAG)' olarak bilinir."
```

### py-hard-critical-connections-bridges

```yaml
id: py-hard-critical-connections-bridges
version: 1
language: python
engine: none
difficulty: hard
title: "Ağdaki kritik bağlantıları (köprüleri) bulma"
prompt: |
  n adet sunucu (0'dan n-1'e kadar) ve aralarındaki çift yönlü bağlantılardan oluşan
  bir ağ verilmiştir. Kaldırıldığında ağın iki veya daha fazla bağımsız parçaya bölünmesine
  neden olan tüm kritik bağlantıları (köprüleri) bir liste olarak döndüren
  `critical_connections(n: int, connections: list[list[int]]) -> list[list[int]]`
  fonksiyonunu yazın. Her kenarı tek tek silip bağlantıyı test etmek O(E * (V + E)) sürer;
  Tarjan'ın köprü bulma algoritması ile tek bir DFS geçişinde O(V + E) sürede çözün.
constraints:
  - "V = n ve E = len(connections) için çalışma süresi O(V + E) olmalı"
  - "Ek bellek graf ve derinlik dizileri için O(V + E) olmalı"
  - "Yönsüz graftaki geri kenarlar (back-edges) ebeveyn hariç doğru ayrıştırılmalı"
expected:
  time: { critical_connections: "V + E" }
  space: "V + E"
concept_tags: [graphs, performance, design]
checklist_extra:
  - "Her kenarı tek tek silip grafı test eden O(E^2) kaba kuvvet yöntemi mi uygulandı?"
  - "Tarjan algoritmasındaki keşif zamanı (disc) ve en düşük erişim zamanı (low) dizileri doğru tutuldu mu?"
reference_solution_path: private/solutions/py-hard-critical-connections-bridges.py
hint_ladder:
  1: "Bir düğümün komşusuna giden kenar köprü değilse, o komşunun atalarına uzanan alternatif bir 'geri kenar' (back edge) var mıdır?"
  2: "low[v] > disc[u] koşulu sağlandığında (v'den u'nun atalarına giden hiçbir yol yoksa) (u, v) kenarı ne olur?"
  3: "Bu algoritma 'Tarjan'ın derinlik öncelikli arama ile köprü bulma algoritması' olarak bilinir."
```

### py-hard-wildcard-matching

```yaml
id: py-hard-wildcard-matching
version: 1
language: python
engine: none
difficulty: hard
title: "Joker karakterli metin eşleştirme"
prompt: |
  Bir metin `s` ve bir desen `p` verilmiştir. Desende '?' herhangi bir tek karakterle
  eşleşir; '*' ise herhangi bir karakter dizisiyle (boş dizi dahil) eşleşir. Desen tüm
  metinle tam olarak örtüşüyor mu denetleyen `is_match_wildcard(s: str, p: str) -> bool`
  fonksiyonunu yazın. re modülünü kullanmayın. Dinamik programlama veya açgözlü iki
  işaretçi yaklaşımıyla O(len(s) * len(p)) sürede çözün.
constraints:
  - "re kütüphanesi kullanılmamalı"
  - "n = len(s) ve m = len(p) için süre O(n * m) veya açgözlü yöntemle ortalama O(n), alan O(m) olmalı"
  - "'*' karakterinin boş metinle eşleşebilme kuralı doğru uygulanmalı"
expected:
  time: { is_match_wildcard: "n*m" }
  space: "m"
concept_tags: [strings, design, performance]
checklist_extra:
  - "Desenin başındaki ardışık '*' karakterlerinin boş dizeyle eşleşmesi gözden kaçıyor mu?"
  - "Dinamik programlama tablosu tek boyutlu diziye indirgenerek bellek optimize edildi mi?"
reference_solution_path: private/solutions/py-hard-wildcard-matching.py
hint_ladder:
  1: "'*' karakteri metindeki 0 karakterle eşleşirse dp[i][j - 1] hücresine, 1 veya daha fazla karakterle eşleşirse dp[i - 1][j] hücresine mi bakar?"
  2: "'?' karakteri ise sadece metin ve desenin önceki karakterlerinin eşleşmiş olmasını (dp[i - 1][j - 1]) mı gerektirir?"
  3: "Bu yöntem 'joker karakterler için 2B dinamik programlama geçişi' olarak bilinir."
```

### py-hard-expression-add-operators

```yaml
id: py-hard-expression-add-operators
version: 1
language: python
engine: none
difficulty: hard
title: "Rakamlar arasına operatör ekleyerek hedefe ulaşma"
prompt: |
  Yalnızca rakamlardan oluşan bir `num` metni ve bir `target` tamsayısı verilmiştir.
  Rakamların arasına ikili '+', '-' veya '*' operatörlerini ekleyerek sonucu `target`
  değerine eşit kılan tüm geçerli matematiksel ifadeleri döndüren
  `add_operators(num: str, target: int) -> list[str]` fonksiyonunu yazın. Sayılar başında
  gereksiz sıfır içeremez (örneğin '05' geçersizdir). Çarpma işleminin işlem önceliğini
  doğru yöneterek geri izleme (backtracking) ile çözün.
constraints:
  - "'0' ile başlayan çok basamaklı sayılar elenmeli"
  - "Çarpma işlemi önceliği için önceki terim takip edilmeli"
  - "Tüm olası ifadeler geri izleme ile taranmalı"
expected:
  time: { add_operators: "4^n" }
  space: "n"
concept_tags: [strings, design, performance, parsing]
checklist_extra:
  - "eval() fonksiyonu kullanılarak performans ve güvenlik açığı yaratılıyor mu?"
  - "Çarpma operatöründe önceki eklenen terim çıkarılıp (mevcut_toplam - onceki + onceki * yeni) şeklinde öncelik düzeltildi mi?"
reference_solution_path: private/solutions/py-hard-expression-add-operators.py
hint_ladder:
  1: "Önceki işlemin '*' olduğu durumda işlem önceliğini korumak için son eklenen terimi geri izlemede parametre olarak taşımak neden gerekir?"
  2: "Bir basamak 0 olduğunda o sayıdan sonra gelen rakamlarla birleştirip '03' gibi sayılar oluşturmaktan nasıl kaçınırsın?"
  3: "Bu algoritma 'işlem önceliği takipli geri izleme ile ifade üretimi' olarak bilinir."
```

### py-hard-palindrome-partitioning-min-cuts

```yaml
id: py-hard-palindrome-partitioning-min-cuts
version: 1
language: python
engine: none
difficulty: hard
title: "Palindromik parçalama için minimum kesim sayısı"
prompt: |
  Verilen bir metni, elde edilen her bir alt parçası palindrom olacak şekilde bölmek
  istiyoruz. Bunun için yapılması gereken minimum kesim sayısını hesaplayan
  `min_cut_palindrome(s: str) -> int` fonksiyonunu yazın. Örneğin 'aab' metni 'aa' ve 'b'
  olarak bölünürse tek bir kesim yeterlidir (sonuç 1). Metin zaten palindromsa 0 dönmelidir.
  n = len(s) olmak üzere O(n^2) zamanda ve O(n) alanda çalışan dinamik programlama tasarlayın.
constraints:
  - "n karakterli metin için çalışma süresi O(n^2) olmalı"
  - "Ek bellek kullanımı O(n^2) veya O(n) olmalı"
expected:
  time: { min_cut_palindrome: "n^2" }
  space: "n"
concept_tags: [strings, performance, design]
checklist_extra:
  - "Tüm alt metinlerin palindromluğunu her seferinde baştan test ederek O(n^3) süreye mi çıkılıyor?"
  - "Önceden bir palindrom tablosu hazırlanarak veya merkezden genişleyerek O(n^2) süreye inildi mi?"
reference_solution_path: private/solutions/py-hard-palindrome-partitioning-min-cuts.py
hint_ladder:
  1: "dp[i] değerini s[0:i] metninin minimum kesim sayısı olarak tanımlarsan, s[j:i] palindrom olduğunda dp[i] ne olur?"
  2: "Eğer s[0:i] tamamen bir palindromsa bu parça için hiç kesim gerekir mi (0 kesim)?"
  3: "Bu problem '1B dinamik programlama ve palindrom tablosu ile minimum kesim analizi' olarak bilinir."
```

### py-hard-first-missing-positive

```yaml
id: py-hard-first-missing-positive
version: 1
language: python
engine: none
difficulty: hard
title: "İlk eksik pozitif sayıyı bulma"
prompt: |
  Sırasız bir tamsayı listesinde bulunmayan en küçük pozitif tamsayıyı (1, 2, 3...)
  bulan `first_missing_positive(nums: list[int]) -> int` fonksiyonunu yazın. Listeyi
  sıralamak O(n log n), küme açmak O(n) ek bellek gerektirir. Döngüsel yer değiştirme
  (cyclic sort) mantığıyla her pozitif sayıyı kendi indeksine (x sayısı nums[x - 1] indeksine)
  taşıyarak O(n) zamanda ve kesinlikle O(1) ek bellekte çözün.
constraints:
  - "Çalışma süresi kesinlikle O(n) olmalı"
  - "Ek bellek kullanımı kesinlikle O(1) olmalı (liste yerinde düzenlenmeli)"
  - "Negatif sayılar ve sıfır göz ardı edilmeli"
expected:
  time: { first_missing_positive: "n" }
  space: "1"
concept_tags: [performance, design, boundary-conditions]
checklist_extra:
  - "Küme veya sözlük açılarak O(n) bellek kısıtı ihlal ediliyor mu?"
  - "nums[i] elemanı 1 ile n arasında olduğu sürece nums[nums[i] - 1] ile doğru takas ediliyor mu?"
reference_solution_path: private/solutions/py-hard-first-missing-positive.py
hint_ladder:
  1: "n elemanlı bir dizide aranan ilk eksik pozitif sayı en fazla n + 1 olabilir mi?"
  2: "Her geçerli x sayısını dizinin x - 1'inci indeksine yerleştirirsen, diziyi taradığında indeksine uymayan ilk sayı neyi verir?"
  3: "Bu algoritma 'döngüsel yerleştirme ile O(1) alanda eksik pozitif tespiti (cyclic sort)' olarak bilinir."
```

### py-hard-skyline-problem

```yaml
id: py-hard-skyline-problem
version: 1
language: python
engine: none
difficulty: hard
title: "Binaların gökyüzü silüetini çıkarma"
prompt: |
  Düz bir zemin üzerinde duran binaların [sol, sağ, yükseklik] üçlülerinden oluşan bir
  liste verilmiştir. Bu binaların dış hatlarını oluşturan silüetin köşe noktalarını
  [x, y] koordinatları olarak döndüren `get_skyline(buildings: list[list[int]]) -> list[list[int]]`
  fonksiyonunu yazın. Silüet noktaları x ekseninde sıralı olmalı ve ardışık yatay çizgiler
  birleştirilmelidir. Süpürme çizgisi (sweep-line) algoritması ve max-heap kullanarak
  n bina için O(n log n) zamanda çözün.
constraints:
  - "n bina için çalışma süresi O(n log n) olmalı"
  - "Aynı x noktasında birden fazla bina başladığında/bittiğinde olay sıralaması doğru yönetilmeli"
  - "Ek bellek yığın için O(n) olmalı"
expected:
  time: { get_skyline: "n log n" }
  space: "n"
concept_tags: [data-structures, performance, design]
checklist_extra:
  - "Aynı x konumunda birden çok olay çakıştığında (örneğin iki bina başlangıcı) sıralama kuralları doğru işletildi mi?"
  - "Max-heap'ten süresi dolmuş binaların tembel (lazy) olarak silinmesi sağlandı mı?"
reference_solution_path: private/solutions/py-hard-skyline-problem.py
hint_ladder:
  1: "Her binayı iki kritik olaya ayırabilir misin: sol sınırda bir yükselme olayı, sağ sınırda bir düşme olayı."
  2: "Soldan sağa süpürürken aktif binaların yüksekliklerini bir max-heap'te tutarsan o anki en tepe nokta değiştiğinde yeni silüet noktası nasıl oluşur?"
  3: "Bu teknik 'süpürme çizgisi ve öncelikli kuyruk ile silüet tespiti (sweep-line algorithm)' olarak bilinir."
```

### py-hard-basic-calculator-nested

```yaml
id: py-hard-basic-calculator-nested
version: 1
language: python
engine: none
difficulty: hard
title: "Parantez ve öncelik içeren matematiksel ifade hesaplayıcı"
prompt: |
  Rakamlar, '+', '-', '(', ')' ve boşluk karakterleri içeren geçerli bir matematiksel
  ifadeyi değerlendiren `calculate_expression(s: str) -> int` fonksiyonunu yazın.
  eval() fonksiyonunu kullanmayın. Parantezlerin iç içe olabileceğini ve parantez
  önündeki '-' işaretinin içerideki tüm terimlerin işaretini değiştireceğini göz önünde
  bulundurarak, bir yığın yardımıyla O(len(s)) zamanda ve O(len(s)) alanda çözün.
constraints:
  - "eval() veya harici yorumlayıcı kullanılmamalı"
  - "n karakterli ifade için çalışma süresi O(n), yığın belleği O(n) olmalı"
  - "Çok basamaklı sayılar ve parantezli işaret değişimleri doğru hesaplanmalı"
expected:
  time: { calculate_expression: "n" }
  space: "n"
concept_tags: [strings, data-structures, parsing]
checklist_extra:
  - "'(' açıldığında o anki kümülatif toplam ve işaret yığına aktarılıyor mu?"
  - "')' kapandığında parantez içi toplamı parantez dışındaki işaret ve toplamla birleştiriliyor mu?"
reference_solution_path: private/solutions/py-hard-basic-calculator-nested.py
hint_ladder:
  1: "Parantez içine girerken o ana kadar hesaplanan toplamı ve geçerli işareti bir yığına atıp sıfırdan başlayabilir misin?"
  2: "Parantez bittiğinde elde ettiğin parantez içi sonucu yığından çektiğin işaretle çarpıp önceki toplama nasıl eklersin?"
  3: "Bu yöntem 'işaret yığını ile iç içe aritmetik ifade ayrıştırma' olarak bilinir."
```

### py-hard-minimum-window-subsequence

```yaml
id: py-hard-minimum-window-subsequence
version: 1
language: python
engine: none
difficulty: hard
title: "Alt diziyi kapsayan en kısa kesintisiz aralık"
prompt: |
  İki metin `s1` ve `s2` verilmiştir. `s1` içinde `s2`'yi bir alt dizi (subsequence)
  olarak barındıran en kısa kesintisiz alt metni döndüren `min_window_subsequence(s1: str, s2: str) -> str`
  fonksiyonunu yazın. Böyle bir aralık yoksa boş metin dönmelidir. Eşit uzunlukta birden
  fazla aralık varsa en solda başlayanı seçilmelidir. İleriye doğru eşleştirip geriye
  doğru pencereyi sıkarak O(len(s1) * len(s2)) sürede ve O(1) ek bellekte çözün.
constraints:
  - "n = len(s1) ve m = len(s2) için çalışma süresi O(n * m) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "Eşitlik durumunda en soldaki indeks tercih edilmeli"
expected:
  time: { min_window_subsequence: "n*m" }
  space: "1"
concept_tags: [strings, performance, boundary-conditions]
checklist_extra:
  - "s2 eşleştiğinde sol sınır ileriye doğru gevşek mi bırakılıyor?"
  - "s2'nin son karakteri bulunduğunda s2 üzerinden geriye doğru taranarak s1'deki başlangıç noktası sıkıştırıldı mı?"
reference_solution_path: private/solutions/py-hard-minimum-window-subsequence.py
hint_ladder:
  1: "s1 üzerinde ilerleyip s2'nin tüm karakterlerini sırayla eşleştirdiğinde bir geçerli pencere bulursun."
  2: "Bu pencerenin başlangıç noktasını daraltmak için s2'yi sondan başa doğru s1 üzerinde ters yönde tarayabilir misin?"
  3: "Bu teknik 'çift yönlü tarama ile alt dizi pencere sıkıştırması' olarak bilinir."
```

### py-hard-stream-median-finder

```yaml
id: py-hard-stream-median-finder
version: 1
language: python
engine: none
difficulty: hard
title: "Sürekli veri akışında dinamik medyan bulucu"
prompt: |
  Sürekli sayıların eklendiği bir veri akışında her an medyanı hesaplayabilen bir
  `MedianFinder` sınıfı tasarlayın. Metotlar: `add_num(num: int) -> None` ve
  `find_median() -> float`. Sayıları her seferinde sıralamak O(n log n) süreceğinden;
  küçük yarıyı tutan bir max-heap ve büyük yarıyı tutan bir min-heap ile iki tepeyi
  dengede tutarak `add_num` işlemini O(log n), `find_median` işlemini O(1) sürede yapın.
constraints:
  - "add_num işlemi O(log n) sürede çalışmalı"
  - "find_median işlemi kesinlikle O(1) sürede çalışmalı"
  - "İki heap arasındaki eleman sayısı farkı en fazla 1 olmalı"
expected:
  time: { add_num: "log n", find_median: "1" }
  space: "n"
concept_tags: [data-structures, performance, design]
checklist_extra:
  - "find_median çağrıldığında liste sıralanarak O(n log n) süre harcanıyor mu?"
  - "Max-heap Python'da sayıları negatifle çarparak doğru simüle edildi mi?"
reference_solution_path: private/solutions/py-hard-stream-median-finder.py
hint_ladder:
  1: "Sayıların küçük yarısını bir max-heap'te, büyük yarısını bir min-heap'te tutarsan medyan daima bu iki heap'in tepesinde yer almaz mı?"
  2: "Yeni sayı eklerken iki heap arasındaki boyut farkını en fazla 1 olacak şekilde nasıl dengelersin?"
  3: "Bu veri yapısı 'çift dengeli heap ile dinamik medyan takibi' olarak bilinir."
```

### py-hard-bus-routes-min-transfers

```yaml
id: py-hard-bus-routes-min-transfers
version: 1
language: python
engine: none
difficulty: hard
title: "En az aktarmayla otobüs rotası bulma"
prompt: |
  Her bir elemanı bir otobüsün dairesel olarak uğradığı durakları gösteren bir `routes`
  listesi verilmiştir. Bir yolcu `source` durağından `target` durağına gitmek istemektedir.
  Hedefe ulaşmak için binilmesi gereken minimum otobüs sayısını (aktarma sayısı + 1)
  hesaplayan `num_buses_to_destination(routes: list[list[int]], source: int, target: int) -> int`
  fonksiyonunu yazın. Yolculuk imkansızsa -1 dönmelidir. Başlangıç ve hedef aynıysa 0
  dönmelidir. Duraklar yerine otobüs hatlarını düğüm kabul eden bir BFS ile O(toplam_durak)
  sürede çözün.
constraints:
  - "source == target durumunda 0 dönmeli"
  - "Hedefe ulaşılamazsa -1 dönmeli"
  - "Aynı otobüs hattı birden çok kez ziyaret edilmemeli"
expected:
  time: { num_buses_to_destination: "N" }
  space: "N"
concept_tags: [graphs, performance, hashing]
checklist_extra:
  - "Duraklar arasında tek tek gezilerek milyonlarca durum içeren yavaş bir graf mı kuruluyor?"
  - "Her duraktan hangi otobüs hatlarının geçtiğini eşleyen bir sözlük ile hatlar arası BFS kuruldu mu?"
reference_solution_path: private/solutions/py-hard-bus-routes-min-transfers.py
hint_ladder:
  1: "Aramayı durak durak gezmek yerine 'otobüsten otobüse aktarma' seviyesine çıkarabilir misin?"
  2: "Bir durağa ulaştığında o duraktan geçen tüm otobüsleri kuyruğa alıp bir otobüse bindiğinde o hattın tüm duraklarını tek hamlede gezmek ne kazandırır?"
  3: "Bu algoritma 'iki parçalı aktarma grafında genişlik öncelikli arama (bus route BFS)' olarak bilinir."
```

### py-hard-design-rate-limiter-token-bucket

```yaml
id: py-hard-design-rate-limiter-token-bucket
version: 1
language: python
engine: none
difficulty: hard
title: "Jeton kovası (Token Bucket) hız sınırlayıcı tasarımı"
prompt: |
  API isteklerini sınırlamak için Jeton Kovası (Token Bucket) algoritmasını uygulayan
  bir `TokenBucketRateLimiter` sınıfı tasarlayın. Parametreler: `capacity` (maksimum jeton)
  ve `refill_rate` (saniyede eklenen jeton sayısı). Metot: `allow_request(tokens: int = 1, current_time: float = ...) -> bool`.
  Arka planda çalışan bir sayaç iş parçacığı çalıştırmadan (thread çalıştırmadan),
  istek anındaki zaman farkı ile biriken jetonları O(1) zamanda tembel (lazy) hesaplayarak
  istek için yeterli jeton varsa tüketip True, yoksa False dönmelidir.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Arka plan iş parçacığı (threading) kullanılmamalı; tembel zaman farkı hesabı yapılmalı"
  - "Jeton miktarı hiçbir zaman capacity değerini aşmamalı"
expected:
  time: { allow_request: "1" }
  space: "1"
concept_tags: [design, performance, floating-point]
checklist_extra:
  - "Sürekli çalışan arka plan döngüsü açılarak CPU kaynağı tüketiliyor mu?"
  - "İki istek arasındaki delta_time ile üretilen jeton sayısı hesaplanıp kova kapasitesi min() ile sınırlandı mı?"
reference_solution_path: private/solutions/py-hard-design-rate-limiter-token-bucket.py
hint_ladder:
  1: "Geçen süreyi her saniye saymak yerine, sadece istek geldiği anda `gecen_sure * refill_rate` formülüyle eklenen jetonu hesaplayabilir misin?"
  2: "Yeni jetonları ekledikten sonra kova kapasitesini aşmayacak şekilde sınırlandırıp talep edilen jeton düşülebiliyor mu?"
  3: "Bu desen 'tembel yenilemeli jeton kovası algoritması (lazy refill token bucket)' olarak bilinir."
```

### py-hard-custom-lru-ttl-cache

```yaml
id: py-hard-custom-lru-ttl-cache
version: 1
language: python
engine: none
difficulty: hard
title: "Zaman aşımı ve LRU destekli gelişmiş önbellek"
prompt: |
  Hem kapasite sınırı (LRU) hem de her anahtar için yaşam süresi (TTL - Time To Live)
  destekleyen bir `TTLCache` sınıfı tasarlayın. Metotlar: `set(key: str, value: object, ttl_seconds: float, current_time: float) -> None`
  ve `get(key: str, current_time: float) -> object | None`. Süresi dolmuş anahtarlara
  erişildiğinde None dönmeli ve anahtar bellekten silinmelidir. Kapasite dolduğunda
  süresi dolmamış anahtarlar arasından en eski erişilen (LRU) atılmalıdır.
  Her iki işlem de O(1) sürede çalışmalıdır.
constraints:
  - "get ve set işlemleri O(1) amortize sürede çalışmalı"
  - "Süresi dolmuş anahtarlar derhal geçersiz sayılmalı"
  - "Kapasite aşımında LRU prensibi geçerli olmalı"
expected:
  time: { set: "1*", get: "1" }
  space: "n"
concept_tags: [data-structures, design, performance]
checklist_extra:
  - "Tüm anahtarları tarayarak süresi geçmişleri temizlemeye çalışan O(n) döngüler kuruldu mu?"
  - "get anında zaman aşımı kontrolü yapılıp çift bağlı listeden O(1) çıkarma uygulandı mı?"
reference_solution_path: private/solutions/py-hard-custom-lru-ttl-cache.py
hint_ladder:
  1: "Her düğümde anahtar, değer ve son kullanma zaman damgasını (expiry) saklayabilir misin?"
  2: "get çağrıldığında o anki zaman damgası son kullanma tarihini geçmişse düğümü sözlükten ve listeden O(1) sürede nasıl kaldırırsın?"
  3: "Bu yapı 'tembel temizlemeli çift bağlı liste ve sözlük ile TTL-LRU önbelleği' olarak bilinir."
```

### py-hard-shortest-palindrome-kmp

```yaml
id: py-hard-shortest-palindrome-kmp
version: 1
language: python
engine: none
difficulty: hard
title: "Başa en az karakter ekleyerek palindrom oluşturma"
prompt: |
  Bir metnin başına en az sayıda karakter ekleyerek elde edilebilecek en kısa palindromik
  metni oluşturan `shortest_palindrome(s: str) -> str` fonksiyonunu yazın.
  Metin boşsa boş metin dönmelidir. Orijinal metnin başından başlayan en uzun palindromik
  ön eki bulmak için metin ters çevirme ve KMP (Knuth-Morris-Pratt) algoritmasının
  ön ek fonksiyonundan (pi tablosu) yararlanarak O(len(s)) sürede çözün.
constraints:
  - "n = len(s) için çalışma süresi O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Yalnızca metnin başına karakter eklenmeli"
expected:
  time: { shortest_palindrome: "n" }
  space: "n"
concept_tags: [strings, performance, design]
checklist_extra:
  - "Karesel O(n^2) sürede tüm ön eklerin palindromluğu baştan mı test ediliyor?"
  - "s + '#' + rev(s) birleştirilerek KMP pi tablosu hesaplandı mı?"
reference_solution_path: private/solutions/py-hard-shortest-palindrome-kmp.py
hint_ladder:
  1: "Metnin başından başlayan en uzun palindromu bulursan, kalan son kısmı ters çevirip başa eklemek en kısa palindromu vermez mi?"
  2: "`s + '#' + s[::-1]` birleşik dizisinin en uzun ön ek-son ek eşleşmesini (KMP LPS tablosunun son değeri) hesaplarsan bu değer neye karşılık gelir?"
  3: "Bu teknik 'KMP ön ek fonksiyonu (LPS table) ile en uzun palindromik ön ek bulma' olarak bilinir."
```

### py-hard-longest-increasing-subsequence-nlogn

```yaml
id: py-hard-longest-increasing-subsequence-nlogn
version: 1
language: python
engine: none
difficulty: hard
title: "En uzun artan alt dizinin uzunluğu (O(n log n))"
prompt: |
  Bir tamsayı listesinde bulunan ve elemanları kesinlikle artan sırada olan en uzun
  alt dizinin (kesintisiz olması gerekmez) uzunluğunu bulan `length_of_lis(nums: list[int]) -> int`
  fonksiyonunu yazın. Klasik dinamik programlama O(n^2) sürer; 'sabır sıralaması' (patience sorting)
  mantığıyla her adımda uygun desteyi ikili arama ile bularak O(n log n) zamanda ve
  O(n) ek bellekte çözün.
constraints:
  - "n elemanlı liste için çalışma süresi kesinlikle O(n log n) olmalı"
  - "Dahili bisect modülü veya kendi ikili arama fonksiyonunuz kullanılabilir"
  - "Ek bellek kullanımı O(n) olmalı"
expected:
  time: { length_of_lis: "n log n" }
  space: "n"
concept_tags: [performance, data-structures, design]
checklist_extra:
  - "O(n^2) süreli çift döngülü dinamik programlama mı uygulandı?"
  - "Her x elemanı için mevcut artan dizideki ilk >= x konumu ikili aramayla bulunup üzerine yazıldı mı?"
reference_solution_path: private/solutions/py-hard-longest-increasing-subsequence-nlogn.py
hint_ladder:
  1: "Her uzunluktaki artan alt dizinin bitebileceği en küçük son elemanı tutan dinamik bir `tails` dizisi oluşturabilir misin?"
  2: "Yeni gelen sayıyı bu sıralı `tails` dizisinde ikili aramayla doğru yerine yerleştirirsen dizinin boyutu neyi temsil eder?"
  3: "Bu algoritma 'sabır sıralaması ve ikili arama ile en uzun artan alt dizi (LIS O(n log n))' olarak bilinir."
```

### py-hard-reconstruct-itinerary-eulerian

```yaml
id: py-hard-reconstruct-itinerary-eulerian
version: 1
language: python
engine: none
difficulty: hard
title: "Uçak biletlerinden Euler rotası kurma"
prompt: |
  [kalkış, varış] havalimanı kodlarından oluşan bir uçak biletleri listesi verilmiştir.
  Yolculuk daima 'JFK' havalimanından başlamalı ve tüm biletler tam olarak bir kez
  kullanılmalıdır. Birden fazla geçerli rota varsa alfabetik olarak en küçük havalimanı
  kodunu tercih eden rotayı bir liste olarak döndüren `find_itinerary(tickets: list[list[int]]) -> list[str]`
  fonksiyonunu yazın. Yönlü grafta bir Euler yolu bulmak için Hierholzer algoritmasını
  kullanarak E bilet için O(E log E) sürede çözün.
constraints:
  - "Yolculuk kesinlikle 'JFK' noktasından başlamalı"
  - "Tüm biletler tam olarak bir kez kullanılmalı"
  - "Eşitlik durumunda alfabetik küçük sıra seçilmeli"
expected:
  time: { find_itinerary: "E log E" }
  space: "E"
concept_tags: [graphs, performance, data-structures]
checklist_extra:
  - "Kör düğümlerde sıkışıp tüm biletleri tüketememe durumunu Hierholzer algoritmasının post-order tersleme mantığı çözüyor mu?"
  - "Komşuluk listesinde hedefler alfabetik sıralı tutulup tüketildikçe çıkarıldı mı?"
reference_solution_path: private/solutions/py-hard-reconstruct-itinerary-eulerian.py
hint_ladder:
  1: "Her havalimanından gidilebilecek yerleri alfabetik sıralı bir öncelik kuyruğunda veya listede tutabilir misin?"
  2: "Bir düğümden gidilecek başka bilet kalmadığında o düğümü rotanın sonuna ekleyip geri dönersen rota nasıl tamamlanır?"
  3: "Bu yöntem 'yönlü grafta Hierholzer algoritması ile Euler yolu bulma' olarak bilinir."
```

### py-hard-partition-equal-subset-sum-space-optimized

```yaml
id: py-hard-partition-equal-subset-sum-space-optimized
version: 1
language: python
engine: none
difficulty: hard
title: "Eşit toplamlı iki alt kümeye bölünebilirlik"
prompt: |
  Yalnızca pozitif tamsayılardan oluşan n elemanlı bir liste verilmiştir. Bu listenin elemanlarının,
  toplamları birbirine tam olarak eşit iki ayrık alt kümeye bölünüp bölünemeyeceğini
  denetleyen `can_partition(nums: list[int]) -> bool` fonksiyonunu yazın. Toplam sayı
  tek ise ikiye bölünemez (False). Hedef toplam // 2 olan s değeri için 0/1 Knapsack mantığını
  kullanarak, 2B matris yerine tek boyutlu bir boole dizisi ile O(n * s) zamanda
  ve O(s) alanda çözün.
constraints:
  - "Genel toplam tek sayı ise hemen False dönmeli"
  - "Ek bellek kullanımı kesinlikle O(s) olmalı (tek boyutlu dizi)"
  - "Her eleman yalnızca bir kez seçilebileceği için dizi tersten taranmalı"
expected:
  time: { can_partition: "n * s" }
  space: "s"
concept_tags: [performance, design, data-structures]
checklist_extra:
  - "Tek boyutlu dizi soldan sağa taranarak aynı eleman aynı adımda birden çok kez mi kullanılıyor?"
  - "Diziyi sağdan sola tarayarak 0/1 sırt çantası kısıtı korundu mu?"
reference_solution_path: private/solutions/py-hard-partition-equal-subset-sum-space-optimized.py
hint_ladder:
  1: "Eğer tüm sayıların toplamı S ise, problem 'toplamı S // 2 olan bir alt küme var mıdır' sorusuna dönüşmez mi?"
  2: "Bir boolean dizisinde dp[j], toplamı j olan bir alt küme oluşturulabiliyorsa True tutulabilir mi?"
  3: "Bu algoritma 'alan optimize edilmiş 0/1 sırt çantası dinamik programlaması' olarak bilinir."
```

### py-hard-decode-ways-num-strings

```yaml
id: py-hard-decode-ways-num-strings
version: 1
language: python
engine: none
difficulty: hard
title: "Şifrelenmiş sayı dizesinin farklı çözülme yolları"
prompt: |
  'A' -> "1", 'B' -> "2" ... 'Z' -> "26" şeklinde harflere karşılık gelen bir rakam
  metni `s` verilmiştir. Bu metnin kaç farklı şekilde harflere dönüştürülebileceğini
  hesaplayan `num_decodings(s: str) -> int` fonksiyonunu yazın. Metin '0' ile başlıyorsa
  veya geçerli bir harfe denk gelmeyen '0'lar varsa 0 dönmelidir. n = len(s) olmak üzere,
  tüm DP dizisini açmak yerine yalnızca son iki durumu tutarak O(n) zaman ve O(1) ek
  alanda çözün.
constraints:
  - "n karakterli metin için çalışma süresi O(n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "'0' ile başlayan geçersiz basamaklar 0 yol üretmeli"
expected:
  time: { num_decodings: "n" }
  space: "1"
concept_tags: [strings, performance, boundary-conditions, design]
checklist_extra:
  - "Metin içinde '30' veya '00' gibi çözülemeyen ikililer geldiğinde sonuç sıfıra düşürülüyor mu?"
  - "Yalnızca önceki iki adımın sonuçları iki değişken ile takip edildi mi?"
reference_solution_path: private/solutions/py-hard-decode-ways-num-strings.py
hint_ladder:
  1: "Son rakam 1-9 arasındaysa tek basamak olarak çözülebilir mi? (Önceki adımdan gelen yollar)."
  2: "Son iki rakam 10-26 arasındaysa iki basamak olarak çözülebilir mi? (İki önceki adımdan gelen yollar)."
  3: "Bu hesaplama 'Fibonacci benzeri durum geçişi ile dize kod çözme dinamik programlaması' olarak bilinir."
```

### py-hard-design-in-memory-file-system

```yaml
id: py-hard-design-in-memory-file-system
version: 1
language: python
engine: none
difficulty: hard
title: "Bellek içi dosya sistemi tasarımı"
prompt: |
  Bellek üzerinde hiyerarşik bir dosya sistemi simüle eden `FileSystem` sınıfı tasarlayın.
  Desteklenecek metotlar: 1) `ls(path: str) -> list[str]`: Dizinse içindeki dosya/klasör
  isimlerini alfabetik sıralı döner, dosyaysa yalnızca dosya adını döner,
  2) `mkdir(path: str) -> None`: Olmayan tüm ara dizinlerle birlikte dizin oluşturur,
  3) `add_content_to_file(file_path: str, content: str) -> None`: Dosya yoksa oluşturup
  yazar, varsa içeriği sonuna ekler, 4) `read_content_from_file(file_path: str) -> str`:
  Dosya içeriğini döndürür. Dizin hiyerarşisini bir Trie yapısıyla modelleyin.
constraints:
  - "ls işlemi alfabetik sıralı liste dönmeli"
  - "mkdir ara dizinleri otomatik oluşturmalı (mkdir -p mantığı)"
  - "add_content var olan dosyanın sonuna ekleme yapmalı"
expected:
  time: { ls: "m + k log k", mkdir: "m", add_content_to_file: "m + c", read_content_from_file: "m" }
  space: "n"
concept_tags: [data-structures, design, strings, files]
checklist_extra:
  - "ls komutu dosya yolu aldığında yalnızca o dosyanın adını tek elemanlı liste olarak veriyor mu?"
  - "Dizin düğümleri ile dosya düğümleri arasındaki ayrım temiz bir veri yapısıyla kuruldu mu?"
reference_solution_path: private/solutions/py-hard-design-in-memory-file-system.py
hint_ladder:
  1: "Dosya ve dizinleri bir ağacın düğümleri olarak tasarlayıp yolları '/' karakterine göre bölebilir misin?"
  2: "Bir düğümün dosya olup olmadığını bir bayrakla belirtip dosya içeriğini bir dizgede nasıl saklarsın?"
  3: "Bu mimari 'Trie tabanlı bellek içi sanal dosya sistemi (virtual in-memory file system)' olarak bilinir."
```

### py-hard-concurrency-async-worker-pool

```yaml
id: py-hard-concurrency-async-worker-pool
version: 1
language: python
engine: none
difficulty: hard
title: "Sınırlı eşzamanlılığa sahip asenkron görev havuzu"
prompt: |
  Python'ın `asyncio` kütüphanesini kullanarak, verilen bir asenkron görev listesini
  aynı anda en fazla `max_concurrency` adet eşzamanlı iş parçacığıyla yürüten
  `run_with_concurrency_limit(tasks: list[Callable[[], Awaitable[T]]], max_concurrency: int) -> list[T]`
  fonksiyonunu yazın. Görevlerin tamamlanma sırası ne olursa olsun, dönen liste orijinal
  görev sırasına birebir sadık kalmalıdır. `asyncio.Semaphore` ve `asyncio.gather`
  kullanarak kaynakları tüketmeden çözün.
constraints:
  - "Aynı anda çalışan asenkron görev sayısı kesinlikle max_concurrency değerini aşmamalı"
  - "Sonuç listesindeki eleman sırası girdi görev sırasıyla aynı olmalı"
  - "Kaynak yönetimi asyncio bağlam yöneticisi ile yapılmalı"
expected:
  time: { run_with_concurrency_limit: "n" }
  space: "n"
concept_tags: [design, performance, resources]
checklist_extra:
  - "Eşzamanlılık sınırı olmadan tüm görevler aynı anda başlatılıp bellek veya soket taşması yaşanıyor mu?"
  - "asyncio.Semaphore bağlamı (async with) doğru kullanıldı mı?"
reference_solution_path: private/solutions/py-hard-concurrency-async-worker-pool.py
hint_ladder:
  1: "Aynı anda yürütülebilecek görev sayısını sınırlandırmak için hangi asyncio senkronizasyon ilkelini kullanırsın?"
  2: "Her görevi bir sarmalayıcı (wrapper) içine alıp semafor koruması altında çalıştırmak eşzamanlılığı nasıl sınırlar?"
  3: "Bu desen 'asenkron semafor ile çalışan havuzu (async worker pool with semaphore)' olarak bilinir."
```

### py-hard-memoize-with-cache-expiry

```yaml
id: py-hard-memoize-with-cache-expiry
version: 1
language: python
engine: none
difficulty: hard
title: "Süre ve boyut sınırlı önbellek dekoratörü"
prompt: |
  Herhangi bir fonksiyonun dönüş değerini belirlenen `ttl_seconds` süresi ve `maxsize`
  kapasitesiyle önbelleğe alan bir `@memoize_with_ttl(ttl_seconds: float, maxsize: int = 128)`
  dekoratörü yazın. `functools.wraps` kullanılmalıdır. Fonksiyonun çağrı argümanları
  (args ve kwargs) anahtar olarak kullanılmalıdır. Önbellek dolduğunda en eski erişilen
  (LRU) anahtar elenmeli; süresi dolan değerler ise yeniden hesaplanmalıdır.
constraints:
  - "functools.wraps ile orijinal fonksiyon metadatası korunmalı"
  - "Değişken keyword argümanları hash edilebilir demetlere dönüştürülmeli"
  - "Kapasite aşımında LRU çıkarma kuralı işletilmeli"
expected:
  time: { wrapper: "1*" }
  space: "n"
concept_tags: [design, performance, mutable-default]
checklist_extra:
  - "Sözlük gibi değiştirilebilir (mutable) argümanlar hash edilemediğinde TypeError alınıyor mu?"
  - "Süresi dolmuş önbellek girdisi yenilenerek fonksiyonun tekrar çalıştırılması sağlandı mı?"
reference_solution_path: private/solutions/py-hard-memoize-with-cache-expiry.py
hint_ladder:
  1: "Fonksiyonun çağrıldığı args ve kwargs ikilisini değişmez (immutable) ve hash edilebilir tek bir anahtar haline nasıl getirirsin?"
  2: "Önbellekte tuttuğun değerin yanına o anki zaman damgasını ekleyip erişim anında süreyi nasıl denetlersin?"
  3: "Bu desen 'zaman aşımı ve boyut sınırlandırmalı LRU fonksiyon dekoratörü' olarak bilinir."
```

### py-hard-tree-ancestor-binary-lifting

```yaml
id: py-hard-tree-ancestor-binary-lifting
version: 1
language: python
engine: none
difficulty: hard
title: "Ağaçta k. atayı logaritmik sürede sorgulama (Binary Lifting)"
prompt: |
  n düğümlü bir ağaçta her düğümün ebeveynini içeren bir `parent` listesi verilmiştir
  (kökün ebeveyni -1'dir). Bir düğümün `k` adım yukarıdaki atasını sorgulayan bir
  `TreeAncestor` sınıfı tasarlayın. Metot: `get_kth_ancestor(node: int, k: int) -> int`.
  Böyle bir ata yoksa -1 dönmelidir. Her sorguda k adım yukarı tırmanmak O(k) sürer;
  başlangıçta her düğümün 2^j'inci atalarını önceden hesaplayarak (Binary Lifting)
  sorguyu O(log k) sürede yanıtlayın.
constraints:
  - "Başlangıç ön hazırlığı (precomputation) O(n log n) zamanda tamamlanmalı"
  - "get_kth_ancestor sorgusu O(log k) zamanda çalışmalı"
  - "Ek bellek tablosu O(n log n) olmalı"
expected:
  time: { get_kth_ancestor: "log k" }
  space: "n log n"
concept_tags: [graphs, performance, data-structures, design]
checklist_extra:
  - "Her sorguda adım adım ebeveyne çıkılarak O(k) kaba kuvvet mi uygulanıyor?"
  - "k sayısının ikili bitleri (k & (1 << j)) taranarak 2'nin kuvveti adımlarla zıplama yapıldı mı?"
reference_solution_path: private/solutions/py-hard-tree-ancestor-binary-lifting.py
hint_ladder:
  1: "Bir düğümün 2^(j+1)'inci atası, o düğümün 2^j'inci atasının 2^j'inci atası mıdır?"
  2: "k sayısını 2'nin kuvvetlerinin toplamı olarak ikilik tabanda açıp ilgili kuvvetler kadar yukarı sıçrayabilir misin?"
  3: "Bu algoritma 'ikili kuvvet atlama tekniği (binary lifting)' olarak bilinir."
```

### py-hard-maximum-frequency-stack

```yaml
id: py-hard-maximum-frequency-stack
version: 1
language: python
engine: none
difficulty: hard
title: "En yüksek frekanslı elemanı çıkaran yığın (FreqStack)"
prompt: |
  En sık tekrar eden elemanı pop eden bir `FreqStack` sınıfı tasarlayın. Metotlar:
  `push(val: int) -> None` ve `pop() -> int`. Eğer en yüksek frekansa sahip birden fazla
  eleman varsa, bu elemanlar arasından yığına en son eklenmiş olan (LIFO) çıkarılmalıdır.
  Her iki işlem de en kötü durumda kesinlikle O(1) zamanda çalışmalıdır. Öncelik
  kuyruğu (heap) kullanmak O(log n) sürer; frekans-yığın eşleme sözlüğü ile O(1)'de çözün.
constraints:
  - "push ve pop işlemleri kesinlikle O(1) zamanda çalışmalı"
  - "Eşit frekans durumunda son eklenen eleman (LIFO kuralı) pop edilmeli"
  - "Ek bellek n eleman için O(n) olmalı"
expected:
  time: { push: "1", pop: "1" }
  space: "n"
concept_tags: [data-structures, performance, design]
checklist_extra:
  - "Heap kullanılarak O(log n) karmaşıklığa mı çıkılıyor?"
  - "Her frekans değeri için bir yığın (group[freq] = list) tutulup pop anında maksimum frekans yığınından eleman çekildi mi?"
reference_solution_path: private/solutions/py-hard-maximum-frequency-stack.py
hint_ladder:
  1: "Her elemanın frekansını sayan bir sözlüğe ek olarak, her frekans seviyesi için elemanları saklayan bir yığın sözlüğü tutabilir misin?"
  2: "Bir sayı 3. kez eklendiğinde hem frekans 1, hem 2, hem de 3 yığınında yer alması pop işlemini nasıl kolaylaştırır?"
  3: "Bu veri yapısı mimarisi 'frekans seviyeli yığın gruplaması (frequency-to-stack mapping)' olarak bilinir."
```

### py-hard-count-of-range-sum

```yaml
id: py-hard-count-of-range-sum
version: 1
language: python
engine: none
difficulty: hard
title: "Toplamı aralıkta kalan alt dizilerin sayısı"
prompt: |
  Bir tamsayı listesi ve [lower, upper] kapalı aralığı verilmiştir. Elemanlarının toplamı
  `lower` ile `upper` arasında (dahil) kalan kesintisiz alt dizilerin sayısını hesaplayan
  `count_range_sum(nums: list[int], lower: int, upper: int) -> int` fonksiyonunu yazın.
  Bütün alt dizi toplamlarını hesaplamak O(n^2) sürer; ön ek toplamları üzerinde
  birleştirmeli sıralama (merge sort) uygulayarak O(n log n) sürede çözün.
constraints:
  - "n elemanlı liste için çalışma süresi O(n log n) olmalı"
  - "Ek bellek kullanımı O(n) olmalı"
  - "Alt dizi toplamı büyük sayılarda taşma yapmadan doğru hesaplanmalı"
expected:
  time: { count_range_sum: "n log n" }
  space: "n"
concept_tags: [performance, design, data-structures]
checklist_extra:
  - "İç içe iki döngü ile O(n^2) sürede mi çözülüyor?"
  - "Ön ek toplamları dizisi oluşturulup merge sort birleştirme adımında aralık koşulu iki işaretçi ile sayıldı mı?"
reference_solution_path: private/solutions/py-hard-count-of-range-sum.py
hint_ladder:
  1: "Alt dizi toplamı S(i, j) = prefix[j] - prefix[i] formülüyle ifade edildiğinde şart `lower <= prefix[j] - prefix[i] <= upper` olur mu?"
  2: "Merge sort sırasında sol ve sağ yarı sıralıyken, sağdaki her eleman için aralığa uyan sol elemanları iki işaretçiyle O(n) sürede nasıl sayarsın?"
  3: "Bu teknik 'birleştirmeli sıralama böl ve yönet ile aralık toplamı sayımı' olarak bilinir."
```

### py-hard-alien-order-resolver

```yaml
id: py-hard-alien-order-resolver
version: 1
language: python
engine: none
difficulty: hard
title: "Çok dilli sözlükten tam alfabe topolojik sıralaması"
prompt: |
  Bilinmeyen bir dilde sıralanmış kelime listesinden yola çıkarak harflerin tek ve tutarlı
  bir global sıralamasını üreten `resolve_alien_alphabet(words: list[str]) -> str`
  fonksiyonunu yazın. Grafta döngü varsa veya bir kelime kendisinden sonra gelen kelimenin
  ön eki olmasına rağmen daha uzunsa (örneğin ['apple', 'app']) sıralama imkansızdır ve
  boş dize dönmelidir. Graf düğümlerini renk kodlarıyla (beyaz, gri, siyah) takip eden
  bir DFS döngü tespiti ve ters post-order sıralamayla O(toplam_karakter) sürede çözün.
constraints:
  - "Ön ek ihlali durumlarında hemen boş dize dönmeli"
  - "Döngü tespit edildiğinde boş dize dönmeli"
  - "C = toplam karakter sayısı için süre O(C), alan O(V + E) olmalı"
expected:
  time: { resolve_alien_alphabet: "C" }
  space: "V + E"
concept_tags: [graphs, strings, data-structures, design]
checklist_extra:
  - "DFS sırasında gri (ziyaret edilmekte olan) bir düğüme tekrar gelinmesi döngü olarak yakalandı mı?"
  - "Tüm harfler ziyaret edildikten sonra sonuç ters çevrilerek topolojik sıra oluşturuldu mu?"
reference_solution_path: private/solutions/py-hard-alien-order-resolver.py
hint_ladder:
  1: "DFS sırasında bir düğümün durumunu üç renkle (0: işlenmedi, 1: yığında, 2: tamamlandı) tutmak döngüleri nasıl yakalar?"
  2: "Bir harfin komşuları tamamen bittiğinde o harfi sonuç listesine ekleyip en sonda listeyi ters çevirmek neyi verir?"
  3: "Bu algoritma 'üç renkli DFS ile döngü tespiti ve ters post-order topolojik sıralama' olarak bilinir."
```

---
