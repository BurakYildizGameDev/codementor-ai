# CodeMentor AI — 200 C++ Sorusu

Bu belge, `docs/SORU_YAZIM_REHBERI.md` standartlarına uygun olarak hazırlanmış 200 adet C++ programlama dili sorusunu içerir.
C++ dili modern sistem ve nesne yönelimli programlama dili olduğu için; RAII ve kaynak yönetimi (Rule of Zero/Three/Five), akıllı işaretçiler (unique_ptr, shared_ptr, weak_ptr), taşıma semantiği (move semantics, std::move, rvalue), const doğruluğu (const-correctness), eşzamanlılık (threads, mutex, condition_variable, atomics), veri yapıları ve algoritmik zaman/alan karmaşıklığı (`expected: time, space`) odaklı hazırlanmıştır.

---

## Soru Bankası Değerlendirmesi ve Pedagojik Kullanım Notu

Bu soru bankası teknik iş mülakatları, modern sistem mühendisleri ve bilgisayar bilimleri öğrencileri için tasarlanmıştır:

1. **Sokratik ve Mülakat Odaklı Yapı (Yöntem Sızıntısı Yok):**
   - Başlıklarda ve soru metinlerinde doğrudan kütüphane fonksiyon veya sınıf adları (ör. `std::vector`, `std::unique_ptr`, `std::move`, `std::copy`) yöntem sızıntısı oluşturacak biçimde verilmemiştir.
   - Adaya problem ve bellek modeli aktarılır; adayın uygun modern C++ standardını (C++17/C++20), RAII yapısını ve veri yapılarını kendisinin seçmesi beklenir.

2. **Sıkı Karmaşıklık ve Bellek Analizi (`expected`):**
   - Tüm sorularda zaman (`time`) ve alan (`space`) karmaşıklıkları Big-O notasyonuyla tanımlanmıştır.
   - Tanımlanan her karmaşıklık değişkeni (n, m, k) prompt ve kısıtlar içinde açık bir kelime olarak karşılık bulur.

3. **C++ Standartları Uyumu:**
   - Sorular ISO/IEC C++20 standardına uygun, derleyici uyarısı üretmeyecek, istisna güvenli (exception safety) ve tanımsız davranışlardan (UB) arındırılmış modern C++ programlama disiplinini ölçer.

---

## 1. Çok Kolay (Very Easy) — 50 Soru

---

### cpp-veryeasy-accumulate-elements

```yaml
id: cpp-veryeasy-accumulate-elements
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Vektördeki tamsayıların toplamını hesaplama"
prompt: |
  n elemanlı bir tamsayı vektöründeki tüm değerlerin toplamını hesaplayan `long long sum_elements(const std::vector<int>& vec)` fonksiyonunu yazın. Vektör boş olduğunda 0 dönmelidir. n vektörün eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Referans const ile geçilmeli"
expected:
  time: { sum_elements: "n" }
  space: "1"
concept_tags: [data-structures, const-correctness]
checklist_extra:
  - "Vektör kopyalanmadan const referansla alınmış mı?"
  - "Toplama işlemi taşmayı önlemek için 64-bit biriktiricide tutulmuş mu?"
reference_solution_path: private/solutions/cpp-veryeasy-accumulate-elements.cpp
hint_ladder:
  1: "Vektörü kopyalamadan const referansla alıp aralık tabanlı for döngüsüyle gezebilirsiniz."
  2: "Elemanları toplarken int sınırlarını aşmamak için long long türünde bir sayaç kullanın."
  3: "Bu işlem 'vektör elemanlarını toplama (vector accumulation)' olarak bilinir."
```

---

### cpp-veryeasy-find-maximum

```yaml
id: cpp-veryeasy-find-maximum
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Vektördeki en büyük elemanı bulma"
prompt: |
  n elemanlı boş olmayan bir tamsayı vektöründeki maksimum değeri bulan `int find_max_element(const std::vector<int>& vec)` fonksiyonunu yazın. n vektörün eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Vektör const referansla alınmalıdır"
expected:
  time: { find_max_element: "n" }
  space: "1"
concept_tags: [data-structures, const-correctness]
checklist_extra:
  - "Maksimum aday ilk elemandan başlatılmış mı?"
  - "Vektör gereksiz yere kopyalanmamış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-find-maximum.cpp
hint_ladder:
  1: "İlk elemanı en büyük kabul ederek başlayın."
  2: "Kalan elemanları tek döngüde tarayıp daha büyük bir değer gördükçe adayı güncelleyin."
  3: "Bu temel arama 'maksimum elemanı bulma (find maximum element)' olarak bilinir."
```

---

### cpp-veryeasy-count-matches

```yaml
id: cpp-veryeasy-count-matches
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Vektörde hedef değere eşit eleman sayısını bulma"
prompt: |
  n elemanlı tamsayı vektöründe target değerine eşit kaç eleman olduğunu sayan `size_t count_matches(const std::vector<int>& vec, int target)` fonksiyonunu yazın. n vektörün eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "const referans kullanılmalı"
expected:
  time: { count_matches: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Vektörün kopyalanması önlenmiş mi?"
  - "Sayaç size_t türünde artırılmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-count-matches.cpp
hint_ladder:
  1: "Döngü ile vektörün tüm elemanlarını gezin."
  2: "target değerine eşit her elemanda sayacı bir artırın."
  3: "Bu algoritma 'koşullu eleman sayımı (count matches)' olarak bilinir."
```

---

### cpp-veryeasy-string-reverse

```yaml
id: cpp-veryeasy-string-reverse
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Karakter dizisini yerinde tersine çevirme"
prompt: |
  n karakterli bir std::string nesnesini ek bellek ayırmadan yerinde tersine çeviren `void reverse_string_inplace(std::string& str)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "İki işaretçi veya indeks kullanılmalıdır"
expected:
  time: { reverse_string_inplace: "n" }
  space: "1"
concept_tags: [strings, copies]
checklist_extra:
  - "Yeni bir dizgi oluşturulmadan yerinde takas yapılmış mı?"
  - "str referansla alınmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-string-reverse.cpp
hint_ladder:
  1: "Dizginin başına ve sonuna iki indeks yerleştirin."
  2: "İndeksler karşılaşana kadar karakterleri takas edip birbirine yaklaştırın."
  3: "Bu algoritma 'yerinde dizgi ters çevirme (in-place string reversal)' olarak bilinir."
```

---

### cpp-veryeasy-is-palindrome

```yaml
id: cpp-veryeasy-is-palindrome
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Metnin palindrom olduğunu iki indeksle denetleme"
prompt: |
  Karakter dizisinin baştan ve sondan okunuşunun aynı olup olmadığını std::string_view kullanarak kopyalama yapmadan denetleyen `bool is_palindrome(std::string_view str)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "string_view ile sıfır kopya sağlanmalıdır"
expected:
  time: { is_palindrome: "n" }
  space: "1"
concept_tags: [strings, copies]
checklist_extra:
  - "std::string_view kullanılarak kopyalama engellenmiş mi?"
  - "Eşleşmeyen ilk karakterde erken çıkış yapılmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-is-palindrome.cpp
hint_ladder:
  1: "Metnin başından ve sonundan karakterleri karşılaştırın."
  2: "Uyuşmazlık gördüğünüz anda false dönün, ortaya kadar gelirseniz true dönün."
  3: "Bu algoritma 'çift indeksli palindrom denetimi (two-pointer palindrome check)' olarak bilinir."
```

---

### cpp-veryeasy-filter-even

```yaml
id: cpp-veryeasy-filter-even
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Vektördeki çift sayıları yeni vektöre aktarma"
prompt: |
  n elemanlı tamsayı vektöründeki çift sayıları sırasını koruyarak yeni bir vektörde döndüren `std::vector<int> filter_even_numbers(const std::vector<int>& vec)` fonksiyonunu yazın. n eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(k) olmalı (k çift sayı adedi)"
  - "const referans kullanılmalıdır"
expected:
  time: { filter_even_numbers: "n" }
  space: "k"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Girdi vektörü const referansla korunmuş mu?"
  - "Çift sayılar doğru modül ile tespit edilmiş mi?"
reference_solution_path: private/solutions/cpp-veryeasy-filter-even.cpp
hint_ladder:
  1: "Sonuç için boş bir vektör oluşturun."
  2: "Girdi vektöründeki her sayıyı test edip çift olanları push_back ile sonuca ekleyin."
  3: "Bu filtreleme 'çift sayıları ayıklama (even number filtering)' olarak bilinir."
```

---

### cpp-veryeasy-string-length

```yaml
id: cpp-veryeasy-string-length
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Metin görünümünün karakter uzunluğunu hesaplama"
prompt: |
  Verilen bir metin görünümünün karakter sayısını hesaplayan `size_t get_text_length(std::string_view text)` fonksiyonunu yazın. n karakter sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "string_view parametre olarak değerle geçilmelidir"
expected:
  time: { get_text_length: "1" }
  space: "1"
concept_tags: [strings, copies]
checklist_extra:
  - "std::string_view hafif bir sarmalayıcı olarak değerle geçilmiş mi?"
  - "Döngü kurmadan doğrudan uzunluk okunmuş mu?"
reference_solution_path: private/solutions/cpp-veryeasy-string-length.cpp
hint_ladder:
  1: "std::string_view boyutu önceden bilinen bir tampon işaretçisi ve uzunluk çiftidir."
  2: "text.size() veya text.length() fonksiyonunu doğrudan döndürün."
  3: "Bu işlem 'metin görünümü uzunluk sorgusu (string view size query)' olarak bilinir."
```

---

### cpp-veryeasy-check-sorted

```yaml
id: cpp-veryeasy-check-sorted
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Vektörün küçükten büyüğe sıralı olduğunu denetleme"
prompt: |
  n elemanlı bir tamsayı vektörünün her elemanının bir öncekinden büyük veya eşit olduğunu denetleyen `bool is_sorted_vector(const std::vector<int>& vec)` fonksiyonunu yazın. n vektörün eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı en kötü durumda O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "n < 2 için true dönmelidir"
expected:
  time: { is_sorted_vector: "n" }
  space: "1"
concept_tags: [data-structures, const-correctness]
checklist_extra:
  - "Sıralamayı bozan ilk ikilide erken çıkış yapılmış mı?"
  - "Vektör const referansla alınmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-check-sorted.cpp
hint_ladder:
  1: "1. indeksten n-1. indekse kadar döngü kurun."
  2: "vec[i] < vec[i-1] olduğu an hemen false dönün."
  3: "Bu denetim 'vektör sıralılık doğrulaması (is-sorted verification)' olarak bilinir."
```

---

### cpp-veryeasy-linear-search

```yaml
id: cpp-veryeasy-linear-search
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Vektörde doğrusal arama yaparak ilk indeksi bulma"
prompt: |
  n elemanlı tamsayı vektöründe target değerini arayan ve ilk bulunduğu indeksi döndüren, yoksa -1 dönen `int find_first_index(const std::vector<int>& vec, int target)` fonksiyonunu yazın. n eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Bulunduğu anda erken çıkış yapılmalıdır"
expected:
  time: { find_first_index: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "İndeks dönüşünde int türü kullanılarak -1 durumu desteklenmiş mi?"
  - "Gereksiz kopyalama engellenmiş mi?"
reference_solution_path: private/solutions/cpp-veryeasy-linear-search.cpp
hint_ladder:
  1: "0'dan n-1'e kadar tüm indeksleri sırayla ziyaret edin."
  2: "Hedef değerle eşleşen ilk elemanda mevcut indeksi döndürün."
  3: "Bu arama yöntemi 'doğrusal arama (linear search)' olarak bilinir."
```

---

### cpp-veryeasy-min-max-pair

```yaml
id: cpp-veryeasy-min-max-pair
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Vektördeki en küçük ve en büyük değerleri çift olarak döndürme"
prompt: |
  n elemanlı boş olmayan bir tamsayı vektörünü tek geçişte tarayarak hem minimum hem maksimum değeri std::pair içinde döndüren `std::pair<int, int> get_min_max(const std::vector<int>& vec)` fonksiyonunu yazın. n vektör boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) tek geçiş olmalı"
  - "Ek bellek O(1) olmalı"
  - "pair.first min, pair.second max olmalıdır"
expected:
  time: { get_min_max: "n" }
  space: "1"
concept_tags: [data-structures, const-correctness]
checklist_extra:
  - "Tek döngüde hem min hem max güncellenmiş mi?"
  - "İlk eleman başlangıç değeri olarak atanmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-min-max-pair.cpp
hint_ladder:
  1: "Başlangıçta min ve max değişkenlerini vec[0] değerine eşitleyin."
  2: "Kalan elemanları tek bir döngüde gezerek her ikisini güncelleyin ve std::make_pair ile döndürün."
  3: "Bu algoritma 'tek geçişte uç değer çifti bulma (min-max pair)' olarak bilinir."
```

---

### cpp-veryeasy-clamp-vector

```yaml
id: cpp-veryeasy-clamp-vector
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Vektör elemanlarını sınırlar arasına sıkıştırma"
prompt: |
  n elemanlı tamsayı vektöründeki her bir değeri low ve high sınırları arasında kalacak şekilde yerinde güncelleyen `void clamp_elements(std::vector<int>& vec, int low, int high)` fonksiyonunu yazın. n vektörün eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "vec değiştirilebilir referansla alınmalıdır"
expected:
  time: { clamp_elements: "n" }
  space: "1"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "low > high geçersiz aralık durumu güvenle elenmiş mi?"
  - "Her eleman yerinde güncellenmiş mi?"
reference_solution_path: private/solutions/cpp-veryeasy-clamp-vector.cpp
hint_ladder:
  1: "Vektör elemanlarını referansla döngüye sokun (auto& x : vec)."
  2: "std::clamp veya if koşulları ile x değerini sınırlar arasına çekin."
  3: "Bu sınırlandırma işlemi 'vektör değerlerini kırpma (vector clamping)' olarak bilinir."
```

---

### cpp-veryeasy-count-vowels

```yaml
id: cpp-veryeasy-count-vowels
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Dizgideki sesli harflerin adedini hesaplama"
prompt: |
  Verilen bir metindeki İngilizce sesli harflerin (a, e, i, o, u, A, E, I, O, U) toplam sayısını hesaplayan `size_t count_vowel_letters(std::string_view text)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "string_view kullanılmalıdır"
expected:
  time: { count_vowel_letters: "n" }
  space: "1"
concept_tags: [strings, copies]
checklist_extra:
  - "string_view ile kopyasız tarama yapılmış mı?"
  - "Büyük ve küçük harfler doğru hesaba katılmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-count-vowels.cpp
hint_ladder:
  1: "Metindeki her karakteri bir döngüde inceleyin."
  2: "Karakter sesli harfler kümesindeyse sayacı bir artırın."
  3: "Bu algoritma 'sesli harf sayımı (vowel counting)' olarak bilinir."
```

---

### cpp-veryeasy-prefix-check

```yaml
id: cpp-veryeasy-prefix-check
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Metnin verilen önek ile başladığını denetleme"
prompt: |
  str metninin prefix ile başlayıp başlamadığını denetleyen `bool has_prefix(std::string_view str, std::string_view prefix)` fonksiyonunu yazın. m önek uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(m) olmalı"
  - "Ek bellek O(1) olmalı"
  - "prefix str'den uzunsa false dönmelidir"
expected:
  time: { has_prefix: "m" }
  space: "1"
concept_tags: [strings, copies]
checklist_extra:
  - "Uzunluk karşılaştırması başta yapılmış mı?"
  - "Karakterler eşleşmediği an döngüden çıkılmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-prefix-check.cpp
hint_ladder:
  1: "Önek uzunluğu metin uzunluğundan büyükse doğrudan false dönün."
  2: "Önek karakterlerini metnin başıyla eşzamanlı karşılaştırın."
  3: "Bu kontrol 'önek doğrulaması (prefix matching)' olarak bilinir."
```

---

### cpp-veryeasy-suffix-check

```yaml
id: cpp-veryeasy-suffix-check
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Metnin verilen sonek ile bittiğini denetleme"
prompt: |
  str metninin suffix ile bitip bitmediğini denetleyen `bool has_suffix(std::string_view str, std::string_view suffix)` fonksiyonunu yazın. m sonek uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(m) olmalı"
  - "Ek bellek O(1) olmalı"
  - "suffix str'den uzunsa false dönmelidir"
expected:
  time: { has_suffix: "m" }
  space: "1"
concept_tags: [strings, copies]
checklist_extra:
  - "Boyut kontrolü (suffix.size() <= str.size()) yapılmış mı?"
  - "str sonundan geriye doğru karşılaştırma yapılmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-suffix-check.cpp
hint_ladder:
  1: "Sonek metinden uzunsa false dönün."
  2: "Metnin sonundan m karakterlik parçayı sonek ile karşılaştırın."
  3: "Bu kontrol 'sonek doğrulaması (suffix matching)' olarak bilinir."
```

---

### cpp-veryeasy-to-lower-copy

```yaml
id: cpp-veryeasy-to-lower-copy
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Metindeki harfleri küçülterek yeni metin üretme"
prompt: |
  Verilen bir metindeki tüm büyük İngilizce harfleri küçük harfe dönüştürerek yeni bir std::string olarak döndüren `std::string to_lower_copy(std::string_view text)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı (yeni dizgi)"
  - "std::tolower kullanılabilir"
expected:
  time: { to_lower_copy: "n" }
  space: "n"
concept_tags: [strings, performance]
checklist_extra:
  - "Yeni metin için reserve ile ön tahsis yapılmış mı?"
  - "Karakter dönüşümleri unsigned char ile güvenli yapılmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-to-lower-copy.cpp
hint_ladder:
  1: "Yeni bir std::string oluşturup boyutunu text.size() kadar rezerve edin."
  2: "Her karakterin tolower karşılığını yeni metne ekleyin."
  3: "Bu işlem 'küçük harfe dönüştürme (lowercase copy)' olarak bilinir."
```

---

### cpp-veryeasy-to-upper-inplace

```yaml
id: cpp-veryeasy-to-upper-inplace
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Metindeki harfleri yerinde büyük harfe dönüştürme"
prompt: |
  std::string nesnesindeki tüm küçük harfleri yerinde büyük harfe dönüştüren `void to_upper_inplace(std::string& text)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "Metin değiştirilebilir referansla alınmalıdır"
expected:
  time: { to_upper_inplace: "n" }
  space: "1"
concept_tags: [strings, copies]
checklist_extra:
  - "Yeni bellek tahsisi yapılmadan yerinde güncellenmiş mi?"
  - "Döngü referans ile (char& c : text) kurulmuş mu?"
reference_solution_path: private/solutions/cpp-veryeasy-to-upper-inplace.cpp
hint_ladder:
  1: "Aralık tabanlı döngüde karakterleri referansla alın."
  2: "std::toupper fonksiyonunu uygulayarak karakteri yerinde güncelleyin."
  3: "Bu işlem 'yerinde büyük harfe çevirme (in-place uppercase conversion)' olarak bilinir."
```

---

### cpp-veryeasy-dot-product

```yaml
id: cpp-veryeasy-dot-product
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "İki tamsayı vektörünün iç çarpımını hesaplama (C++)"
prompt: |
  n elemanlı iki tamsayı vektörünün iç çarpımını (dot product) hesaplayan `long long vector_dot_product(const std::vector<int>& a, const std::vector<int>& b)` fonksiyonunu yazın. n vektörlerin eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Çarpım toplamı 64-bit tamsayıda biriktirilmelidir"
expected:
  time: { vector_dot_product: "n" }
  space: "1"
concept_tags: [data-structures, const-correctness]
checklist_extra:
  - "Vektör boyutlarının eşitliği kontrol edilmiş mi?"
  - "32-bit taşmasını önlemek için elemanlar çarpmadan önce long long'a dönüştürülmüş mü?"
reference_solution_path: private/solutions/cpp-veryeasy-dot-product.cpp
hint_ladder:
  1: "Döngüde i = 0'dan n-1'e kadar a[i] ve b[i] çarpımlarını toplayın."
  2: "Çarpmadan önce statik tür dönüşümüyle tamsayı taşmasını önleyin."
  3: "Bu vektör işlemi 'iç çarpım (dot product)' olarak bilinir."
```

---

### cpp-veryeasy-remove-negative

```yaml
id: cpp-veryeasy-remove-negative
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Vektördeki negatif sayıları yerinde temizleme"
prompt: |
  n elemanlı bir tamsayı vektöründeki sıfırdan küçük sayıları yerinde silen `void remove_negatives(std::vector<int>& vec)` fonksiyonunu yazın. n vektör boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Erase-remove deyimi veya iki indeks kullanılabilir"
expected:
  time: { remove_negatives: "n" }
  space: "1"
concept_tags: [data-structures, iterator-invalidation]
checklist_extra:
  - "Eleman silinirken iterator geçersizleşmesi hatası önlenmiş mi?"
  - "std::erase_if veya iki işaretçi ile O(n) sağlanmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-remove-negative.cpp
hint_ladder:
  1: "İki indeks tutarak pozitif sayıları başa yazabilir ya da std::erase_if kullanabilirsiniz."
  2: "İç içe döngüde erase çağırmak O(n^2) olacağından tek geçişte temizleyin."
  3: "Bu filtreleme 'vektörden yerinde eleman silme (in-place vector filtering)' olarak bilinir."
```

---

### cpp-veryeasy-replace-char

```yaml
id: cpp-veryeasy-replace-char
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Metinde geçen belirli karakterleri başka karakterle değiştirme"
prompt: |
  std::string içindeki tüm old_ch karakterlerini yerinde new_ch ile değiştiren `void replace_characters(std::string& str, char old_ch, char new_ch)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "str referansla alınmalıdır"
expected:
  time: { replace_characters: "n" }
  space: "1"
concept_tags: [strings, copies]
checklist_extra:
  - "Karakterler referansla taranmış mı?"
  - "Yeni bellek tahsisi engellenmiş mi?"
reference_solution_path: private/solutions/cpp-veryeasy-replace-char.cpp
hint_ladder:
  1: "Dizgideki her karakteri referansla dolaşın."
  2: "Karakter old_ch ile eşleştiğinde new_ch değerini atayın."
  3: "Bu işlem 'yerinde karakter değiştirme (in-place character replace)' olarak bilinir."
```

---

### cpp-veryeasy-is-numeric

```yaml
id: cpp-veryeasy-is-numeric
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Metnin yalnızca rakamlardan oluştuğunu denetleme"
prompt: |
  Verilen bir metin görünümünün yalnızca '0'-'9' arasındaki rakamlardan oluştuğunu denetleyen `bool is_all_digits(std::string_view str)` fonksiyonunu yazın. Boş metin için false dönmelidir. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Boş metin kontrolü yapılmalıdır"
expected:
  time: { is_all_digits: "n" }
  space: "1"
concept_tags: [strings, edge-cases]
checklist_extra:
  - "Boş metin durumu false olarak elenmiş mi?"
  - "Rakam olmayan ilk karakterde erken çıkış yapılmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-is-numeric.cpp
hint_ladder:
  1: "str boşsa hemen false dönün."
  2: "Her karakter için std::isdigit denetimi yapın, false olduğu an çıkın."
  3: "Bu doğrulama 'sayısal karakter denetimi (numeric string check)' olarak bilinir."
```

---

### cpp-veryeasy-count-words

```yaml
id: cpp-veryeasy-count-words
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Boşluklarla ayrılmış sözcük sayısını bulma (C++)"
prompt: |
  Bir metin görünümündeki boşluklarla ayrılmış sözcüklerin toplam adedini hesaplayan `size_t count_words(std::string_view text)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Ardışık boşluklar tek sayılmalıdır"
expected:
  time: { count_words: "n" }
  space: "1"
concept_tags: [strings, copies]
checklist_extra:
  - "Bir sözcük içinde olup olunmadığı bayrakla takip edilmiş mi?"
  - "Metin başı ve sonundaki boşluklar doğru elenmiş mi?"
reference_solution_path: private/solutions/cpp-veryeasy-count-words.cpp
hint_ladder:
  1: "Şu anda bir sözcük içinde olup olmadığınızı tutan bir boole değişkeni kullanın."
  2: "Boşluktan harfe geçilen her noktada sözcük sayacını bir artırın."
  3: "Bu algoritma 'sözcük sayacı durum takibi (word counting state)' olarak bilinir."
```

---

### cpp-veryeasy-matrix-diagonal-sum

```yaml
id: cpp-veryeasy-matrix-diagonal-sum
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Kare matrisin asal köşegen toplamını hesaplama"
prompt: |
  n x n boyutundaki bir kare matrisin asal köşegenindeki (i == j) elemanların toplamını hesaplayan `long long diagonal_sum(const std::vector<std::vector<int>>& mat)` fonksiyonunu yazın. n matris satır ve sütun boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Tek döngü kurulmalıdır"
expected:
  time: { diagonal_sum: "n" }
  space: "1"
concept_tags: [data-structures, const-correctness]
checklist_extra:
  - "İç içe iki döngü kurmak yerine tek döngü kurulmuş mu?"
  - "Toplam long long biriktiricide tutulmuş mu?"
reference_solution_path: private/solutions/cpp-veryeasy-matrix-diagonal-sum.cpp
hint_ladder:
  1: "0'dan n-1'e kadar tek bir döngüde mat[i][i] elemanlarını toplayın."
  2: "İç içe iki döngü kurmaktan kaçınarak O(n) karmaşıklığını koruyun."
  3: "Bu matris işlemi 'asal köşegen toplamı (matrix diagonal sum)' olarak bilinir."
```

---

### cpp-veryeasy-swap-references

```yaml
id: cpp-veryeasy-swap-references
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "İki tamsayı referansının değerlerini takas etme"
prompt: |
  İki tamsayı referansının gösterdiği değerleri yer değiştiren `void swap_values(int& a, int& b)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "std::move veya geçici değişken kullanılabilir"
expected:
  time: { swap_values: "1" }
  space: "1"
concept_tags: [move-semantics, const-correctness]
checklist_extra:
  - "Geçici bir değişkenle veri kaybı olmadan takas yapılmış mı?"
  - "Referans parametreleri doğru bağlanmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-swap-references.cpp
hint_ladder:
  1: "Bir geçici değişkende a'nın değerini saklayın."
  2: "a'ya b'yi, b'ye ise saklanan geçici değeri atayın."
  3: "Bu temel işlem 'referans ile değer takası (reference swap)' olarak bilinir."
```

---

### cpp-veryeasy-scale-vector

```yaml
id: cpp-veryeasy-scale-vector
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Vektördeki tüm elemanları bir katsayı ile yerinde çarpma"
prompt: |
  n elemanlı tamsayı vektöründeki her bir elemanı factor değeriyle yerinde çarpan `void scale_vector(std::vector<int>& vec, int factor)` fonksiyonunu yazın. n vektörün eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "vec değiştirilebilir referansla alınmalıdır"
expected:
  time: { scale_vector: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Döngü referansla (for (int& x : vec)) kurulmuş mu?"
  - "Gereksiz kopyalama önlenmiş mi?"
reference_solution_path: private/solutions/cpp-veryeasy-scale-vector.cpp
hint_ladder:
  1: "Vektör elemanlarını referansla gezin."
  2: "Her elemanı factor ile çarparak güncelleyin (x *= factor)."
  3: "Bu işlem 'vektör ölçekleme (vector scaling)' olarak bilinir."
```

---

### cpp-veryeasy-absolute-diff-sum

```yaml
id: cpp-veryeasy-absolute-diff-sum
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Ardışık elemanlar arasındaki mutlak farkların toplamını bulma"
prompt: |
  n elemanlı bir tamsayı vektöründe ardışık komşu elemanlar arasındaki mutlak farkların (|vec[i] - vec[i-1]|) toplamını hesaplayan `long long consecutive_diffs(const std::vector<int>& vec)` fonksiyonunu yazın. n eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "n < 2 için 0 dönmelidir"
expected:
  time: { consecutive_diffs: "n" }
  space: "1"
concept_tags: [data-structures, const-correctness]
checklist_extra:
  - "std::abs kullanılarak mutlak fark doğru alınmış mı?"
  - "Toplama 64-bit tamsayıda yapılmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-absolute-diff-sum.cpp
hint_ladder:
  1: "1. indeksten n-1. indekse kadar döngü kurun."
  2: "std::abs(vec[i] - vec[i-1]) değerlerini biriktiriciye ekleyin."
  3: "Bu hesaplama 'ardışık farklar toplamı (sum of consecutive differences)' olarak bilinir."
```

---

### cpp-veryeasy-find-second-largest

```yaml
id: cpp-veryeasy-find-second-largest
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Vektördeki en büyük ikinci farklı değeri bulma"
prompt: |
  n elemanlı bir tamsayı vektöründeki en büyük ikinci farklı değeri std::optional içinde döndüren `std::optional<int> find_second_largest(const std::vector<int>& vec)` fonksiyonunu yazın. Yeterli farklı eleman yoksa std::nullopt dönmelidir. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) tek geçiş olmalı (sıralama yapılamaz)"
  - "Ek bellek O(1) olmalı"
  - "Vektör const referansla alınmalıdır"
expected:
  time: { find_second_largest: "n" }
  space: "1"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "Tüm elemanlar eşit olduğunda std::nullopt dönülmüş mü?"
  - "Sıralama yapılmadan tek döngüde çözülmüş mü?"
reference_solution_path: private/solutions/cpp-veryeasy-find-second-largest.cpp
hint_ladder:
  1: "En büyük ve ikinci en büyük için iki ayrı std::optional veya başlangıç değişkeni tutun."
  2: "Vektörü tek geçişte tarayarak adayları güncelleyin."
  3: "Bu algoritma 'tek geçişte ikinci en büyük elemanı bulma (second largest element)' olarak bilinir."
```

---

### cpp-veryeasy-vector-mean

```yaml
id: cpp-veryeasy-vector-mean
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Tamsayı vektörünün aritmetik ortalamasını hesaplama"
prompt: |
  n elemanlı tamsayı vektörünün aritmetik ortalamasını double türünde hesaplayan `double calculate_mean(const std::vector<int>& vec)` fonksiyonunu yazın. Vektör boşsa 0.0 dönmelidir. n eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Tamsayı bölmesi yerine kayan noktalı bölme yapılmalıdır"
expected:
  time: { calculate_mean: "n" }
  space: "1"
concept_tags: [integer-division, const-correctness]
checklist_extra:
  - "Toplam double'a dönüştürülerek tamsayı bölmesi kesilmesi önlenmiş mi?"
  - "Boş vektörde sıfıra bölme engellenmiş mi?"
reference_solution_path: private/solutions/cpp-veryeasy-vector-mean.cpp
hint_ladder:
  1: "Vektör boşsa hemen 0.0 dönün."
  2: "Elemanları long long biriktiricide toplayıp static_cast<double>(sum) / vec.size() ile bölün."
  3: "Bu istatistiksel hesap 'aritmetik ortalama hesaplama (mean calculation)' olarak bilinir."
```

---

### cpp-veryeasy-remove-duplicates-sorted

```yaml
id: cpp-veryeasy-remove-duplicates-sorted
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Sıralı vektördeki yinelenen elemanları yerinde temizleme"
prompt: |
  Küçükten büyüğe sıralı n elemanlı bir tamsayı vektöründeki yinelenen elemanları yerinde temizleyen `void remove_adjacent_duplicates(std::vector<int>& vec)` fonksiyonunu yazın. n vektörün eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "std::unique ve erase deyimi kullanılabilir"
expected:
  time: { remove_adjacent_duplicates: "n" }
  space: "1"
concept_tags: [data-structures, iterator-invalidation]
checklist_extra:
  - "std::unique sonrası kalan fazlalıklar erase ile silinmiş mi?"
  - "Boş vektör kontrolü yapılmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-remove-duplicates-sorted.cpp
hint_ladder:
  1: "std::unique fonksiyonunu kullanarak benzersiz elemanları vektörün başına toplayın."
  2: "Dönen iterator ile vec.end() arasını vec.erase ile silin."
  3: "Bu deyim 'sıralı dizide tekleştirme (erase-unique idiom)' olarak bilinir."
```

---

### cpp-veryeasy-left-rotate-one

```yaml
id: cpp-veryeasy-left-rotate-one
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Vektör elemanlarını bir adım sola kaydırma"
prompt: |
  n elemanlı bir tamsayı vektörünün tüm elemanlarını bir adım sola kaydıran ve ilk elemanı sona taşıyan `void rotate_left_once(std::vector<int>& vec)` fonksiyonunu yazın. n vektör boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "std::rotate kullanılabilir"
expected:
  time: { rotate_left_once: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "n <= 1 durumlarında işlem yapılmaması sağlanmış mı?"
  - "std::rotate ile O(n) sürede yerinde kaydırılmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-left-rotate-one.cpp
hint_ladder:
  1: "Vektör boş veya 1 elemanlıysa doğrudan dönün."
  2: "std::rotate(vec.begin(), vec.begin() + 1, vec.end()) çağrısıyla elemanları sola döndürün."
  3: "Bu işlem 'vektörü sola döndürme (left rotate by one)' olarak bilinir."
```

---

### cpp-veryeasy-fill-range

```yaml
id: cpp-veryeasy-fill-range
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Vektörü ardışık sayılarla doldurma"
prompt: |
  Boyutu önceden n olarak ayrılmış bir tamsayı vektörünü start değerinden başlayarak birer artan ardışık sayılarla dolduran `void fill_consecutive(std::vector<int>& vec, int start)` fonksiyonunu yazın. n vektör boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "std::iota kullanılabilir"
expected:
  time: { fill_consecutive: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Vektörün mevcut boyutu n korunmuş mu?"
  - "Elemanlar ardışık artırılarak doldurulmuş mu?"
reference_solution_path: private/solutions/cpp-veryeasy-fill-range.cpp
hint_ladder:
  1: "std::iota(vec.begin(), vec.end(), start) fonksiyonunu çağırın."
  2: "Vektörün tüm hücreleri sırayla start, start+1, ... ile doldurulacaktır."
  3: "Bu algoritma 'ardışık tamsayı doldurma (iota range fill)' olarak bilinir."
```

---

### cpp-veryeasy-count-greater-than

```yaml
id: cpp-veryeasy-count-greater-than
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Vektörde eşik değerinden büyük elemanları sayma"
prompt: |
  n elemanlı bir tamsayı vektöründe threshold değerinden kesinlikle büyük olan eleman sayısını bulan `size_t count_greater_than(const std::vector<int>& vec, int threshold)` fonksiyonunu yazın. n vektörün eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "std::count_if kullanılabilir"
expected:
  time: { count_greater_than: "n" }
  space: "1"
concept_tags: [data-structures, const-correctness]
checklist_extra:
  - "Lambda ifadesiyle koşullu sayım yapılmış mı?"
  - "const referans kullanılmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-count-greater-than.cpp
hint_ladder:
  1: "std::count_if algoritmasını ve [threshold](int x){ return x > threshold; } lambdasını kullanın."
  2: "Koşulu sağlayan elemanların adedini doğrudan döndürün."
  3: "Bu işlem 'koşullu filtreleme sayımı (conditional count_if)' olarak bilinir."
```

---

### cpp-veryeasy-is-all-positive

```yaml
id: cpp-veryeasy-is-all-positive
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Vektördeki tüm elemanların pozitif olduğunu denetleme"
prompt: |
  n elemanlı bir tamsayı vektöründeki tüm elemanların sıfırdan büyük olup olmadığını denetleyen `bool all_positive(const std::vector<int>& vec)` fonksiyonunu yazın. Boş vektör için true dönmelidir. n eleman adedidir.
constraints:
  - "Zaman karmaşıklığı en kötü durumda O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "std::all_of kullanılabilir"
expected:
  time: { all_positive: "n" }
  space: "1"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "İlk negatif veya sıfır elemanda erken çıkış yapılmış mı?"
  - "Boş vektörde true dönülmüş mü?"
reference_solution_path: private/solutions/cpp-veryeasy-is-all-positive.cpp
hint_ladder:
  1: "std::all_of algoritmasını [](int x){ return x > 0; } yüklemiyle çağırın."
  2: "Koşulu sağlamayan bir eleman görüldüğü anda erken dönülecektir."
  3: "Bu algoritma 'evrensel doğrulama (all_of predicate check)' olarak bilinir."
```

---

### cpp-veryeasy-split-by-char

```yaml
id: cpp-veryeasy-split-by-char
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Metni belirli bir ayraç karaktere göre parçalama"
prompt: |
  Verilen bir metin görünümünü delim karakterine göre parçalara ayırıp std::vector<std::string> olarak döndüren `std::vector<std::string> split_char(std::string_view text, char delim)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı (parçalar)"
  - "std::string_view üzerinden ayrıştırma yapılmalı"
expected:
  time: { split_char: "n" }
  space: "n"
concept_tags: [strings, performance]
checklist_extra:
  - "Karakterler tek tek kopyalanmadan alt dizgi indeksleriyle mi parçalanmış?"
  - "Son parça listeye eklenmiş mi?"
reference_solution_path: private/solutions/cpp-veryeasy-split-by-char.cpp
hint_ladder:
  1: "İki indeks tutarak delim karakterlerini arayın."
  2: "Her ayraçta text.substr ile parçayı alıp sonuç vektörüne push_back yapın."
  3: "Bu metin işlemi 'karakter ayracı ile bölme (string split by char)' olarak bilinir."
```

---

### cpp-veryeasy-join-strings

```yaml
id: cpp-veryeasy-join-strings
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Dizgi listesini ayraçla tek metinde birleştirme"
prompt: |
  n adet metin içeren parçalar vektörünü aralarına delim ayracını koyarak tek bir std::string halinde birleştiren `std::string join_strings(const std::vector<std::string>& parts, std::string_view delim)` fonksiyonunu yazın. n parça sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı (birleştirilmiş metin)"
  - "reserve ile ön tahsis yapılmalıdır"
expected:
  time: { join_strings: "n" }
  space: "n"
concept_tags: [strings, performance]
checklist_extra:
  - "Toplam uzunluk hesaplanıp reserve çağrılmış mı?"
  - "Son elemandan sonra fazladan ayraç konulması engellenmiş mi?"
reference_solution_path: private/solutions/cpp-veryeasy-join-strings.cpp
hint_ladder:
  1: "Tüm parçaların ve aradaki ayraçların toplam uzunluğunu hesaplayıp reserve çağırın."
  2: "Parçaları sırayla ekleyip aralarına delim yerleştirin."
  3: "Bu metin işlemi 'metin listesini birleştirme (string join)' olarak bilinir."
```

---

### cpp-veryeasy-repeat-string

```yaml
id: cpp-veryeasy-repeat-string
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Metni belirtilen k sayısı kadar ardışık çoğaltma"
prompt: |
  Verilen text metnini k kez ardışık tekrarlayan yeni bir std::string üreten `std::string repeat_text(std::string_view text, size_t k)` fonksiyonunu yazın. k tekrar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(k) olmalı"
  - "Ek bellek O(k) olmalı"
  - "reserve ile tek tahsis yapılmalıdır"
expected:
  time: { repeat_text: "k" }
  space: "k"
concept_tags: [strings, performance]
checklist_extra:
  - "text.size() * k kadar ön tahsis yapılmış mı?"
  - "Döngüde append çağrılarak verimli eklenmiş mi?"
reference_solution_path: private/solutions/cpp-veryeasy-repeat-string.cpp
hint_ladder:
  1: "Yeni bir std::string oluşturup kapasitesini text.size() * k olarak rezerve edin."
  2: "k defa döngüde result.append(text) çağırın."
  3: "Bu işlem 'metin tekrarlama (string repetition)' olarak bilinir."
```

---

### cpp-veryeasy-find-char-index

```yaml
id: cpp-veryeasy-find-char-index
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Karakterin metin içinde ilk görüldüğü indeksi bulma"
prompt: |
  Metin görünümünde ch karakterinin ilk geçtiği konumu std::optional<size_t> olarak döndüren `std::optional<size_t> find_char(std::string_view text, char ch)` fonksiyonunu yazın. Bulunamazsa std::nullopt dönmelidir. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "string_view::find kullanılabilir"
expected:
  time: { find_char: "n" }
  space: "1"
concept_tags: [strings, const-correctness]
checklist_extra:
  - "std::string_view::npos durumu std::nullopt'a dönüştürülmüş mü?"
  - "Kopyalama yapılmadan aranmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-find-char-index.cpp
hint_ladder:
  1: "size_t pos = text.find(ch) çağrısını yapın."
  2: "pos != std::string_view::npos ise pos döndürün, aksi halde std::nullopt dönün."
  3: "Bu işlem 'karakter indeksi arama (character find)' olarak bilinir."
```

---

### cpp-veryeasy-clamp-scalar

```yaml
id: cpp-veryeasy-clamp-scalar
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Tekil tamsayı değerini sınırlar arasına sıkıştırma"
prompt: |
  Verilen val değerini low ve high sınırları arasında tutan `int clamp_scalar(int val, int low, int high)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "std::clamp veya koşullarla çözülmeli"
expected:
  time: { clamp_scalar: "1" }
  space: "1"
concept_tags: [edge-cases, const-correctness]
checklist_extra:
  - "val < low ise low, val > high ise high döndürülmüş mü?"
  - "low <= high kabulü gözetilmiş mi?"
reference_solution_path: private/solutions/cpp-veryeasy-clamp-scalar.cpp
hint_ladder:
  1: "std::clamp(val, low, high) fonksiyonunu çağırın ya da koşul ifadeleriyle değeri sınırlandırın."
  2: "Değer sınırların dışındaysa ilgili sınıra yuvarlanır."
  3: "Bu matematiksel işlem 'skaler değer kırpma (scalar clamping)' olarak bilinir."
```

---

### cpp-veryeasy-are-vectors-equal

```yaml
id: cpp-veryeasy-are-vectors-equal
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "İki vektörün elemanlarının birebir eşitliğini sınama"
prompt: |
  n elemanlı iki tamsayı vektörünün hem boyut hem de aynı sıradaki elemanlar bakımından eşit olup olmadığını denetleyen `bool compare_vectors(const std::vector<int>& a, const std::vector<int>& b)` fonksiyonunu yazın. n vektörün boyutudur.
constraints:
  - "Zaman karmaşıklığı en kötü durumda O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Boyutlar farklıysa hemen false dönmelidir"
expected:
  time: { compare_vectors: "n" }
  space: "1"
concept_tags: [data-structures, const-correctness]
checklist_extra:
  - "Boyut farkı başta elenmiş mi?"
  - "const referans kullanılmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-are-vectors-equal.cpp
hint_ladder:
  1: "a.size() != b.size() ise doğrudan false dönün."
  2: "std::equal(a.begin(), a.end(), b.begin()) veya == operatörü ile elemanları karşılaştırın."
  3: "Bu denetim 'vektör eşitlik karşılaştırması (vector equality comparison)' olarak bilinir."
```

---

### cpp-veryeasy-vector-product

```yaml
id: cpp-veryeasy-vector-product
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Vektördeki tüm tamsayıların çarpımını hesaplama"
prompt: |
  n elemanlı bir tamsayı vektöründeki tüm elemanların çarpımını hesaplayan `long long product_elements(const std::vector<int>& vec)` fonksiyonunu yazın. Vektör boşsa 1 dönmelidir. n eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Boş vektör için 1 dönmelidir"
expected:
  time: { product_elements: "n" }
  space: "1"
concept_tags: [data-structures, const-correctness]
checklist_extra:
  - "Başlangıç değeri 1 olarak atanmış mı?"
  - "64-bit tamsayı biriktirici kullanılmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-vector-product.cpp
hint_ladder:
  1: "Çarpım biriktiricisini 1LL ile başlatın."
  2: "Döngüde her elemanla çarpıp sonucu döndürün."
  3: "Bu işlem 'vektör elemanları çarpımı (vector product accumulation)' olarak bilinir."
```

---

### cpp-veryeasy-count-odds

```yaml
id: cpp-veryeasy-count-odds
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Vektördeki tek sayıların toplam sayısını bulma"
prompt: |
  n elemanlı tamsayı vektöründeki tek sayıların adedini bulan `size_t count_odd_numbers(const std::vector<int>& vec)` fonksiyonunu yazın. n vektörün boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Negatif tek sayılar doğru modül ile yönetilmelidir"
expected:
  time: { count_odd_numbers: "n" }
  space: "1"
concept_tags: [data-structures, const-correctness]
checklist_extra:
  - "Negatif sayılarda (x % 2 != 0) koşulu doğru çalışıyor mu?"
  - "const referans kullanılmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-count-odds.cpp
hint_ladder:
  1: "Döngü ile vektör elemanlarını tarayın."
  2: "x % 2 != 0 veya x & 1 koşulunu sağlayan elemanlarda sayacı artırın."
  3: "Bu algoritma 'tek sayıların sayımı (odd number counting)' olarak bilinir."
```

---

### cpp-veryeasy-strip-whitespace

```yaml
id: cpp-veryeasy-strip-whitespace
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Metnin başındaki ve sonundaki boşlukları kırpma"
prompt: |
  Verilen bir metin görünümünün başında ve sonunda yer alan boşluk karakterlerini (' ', '\t', '\r', '\n') kopyalama yapmadan kırparak alt görünüm döndüren `std::string_view trim_whitespace(std::string_view str)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Sıfır kopyalı string_view döndürülmelidir"
expected:
  time: { trim_whitespace: "n" }
  space: "1"
concept_tags: [strings, copies]
checklist_extra:
  - "Tamamen boşluktan oluşan metinler için boş string_view dönülmüş mü?"
  - "remove_prefix ve remove_suffix doğru kullanılmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-strip-whitespace.cpp
hint_ladder:
  1: "Metnin başından ilk boşluk olmayan karakteri (first non-space) bulun ve remove_prefix uygulayın."
  2: "Sondan ilk boşluk olmayan karakteri bulup remove_suffix uygulayın."
  3: "Bu metin temizliği 'metin başı ve sonu boşluk budama (string_view trimming)' olarak bilinir."
```

---

### cpp-veryeasy-reverse-words

```yaml
id: cpp-veryeasy-reverse-words
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Cümledeki her bir sözcüğü kendi içinde ters çevirme"
prompt: |
  Boşluklarla ayrılmış sözcükler içeren bir cümledeki sözcüklerin sırasını değiştirmeden her bir sözcüğü kendi içinde tersine çeviren `std::string reverse_words(std::string_view sentence)` fonksiyonunu yazın. n cümlenin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "std::reverse kullanılabilir"
expected:
  time: { reverse_words: "n" }
  space: "n"
concept_tags: [strings, performance]
checklist_extra:
  - "Cümlenin kopyası alınıp sözcük sözcük std::reverse uygulanmış mı?"
  - "Ardışık boşluklar korunmuş mu?"
reference_solution_path: private/solutions/cpp-veryeasy-reverse-words.cpp
hint_ladder:
  1: "Cümleyi bir std::string olarak kopyalayın."
  2: "Boşluklarla sınırlandırılmış her bir sözcük aralığını std::reverse ile ters çevirin."
  3: "Bu algoritma 'sözcükleri kendi içinde ters çevirme (reverse words in sentence)' olarak bilinir."
```

---

### cpp-veryeasy-merge-alternating

```yaml
id: cpp-veryeasy-merge-alternating
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "İki eşit boyutlu vektörün elemanlarını harmanlama"
prompt: |
  n elemanlı iki tamsayı vektörünün elemanlarını bir a'dan bir b'den olacak şekilde sırayla harmanlayarak 2n boyutlu yeni bir vektör üreten `std::vector<int> zip_merge(const std::vector<int>& a, const std::vector<int>& b)` fonksiyonunu yazın. n her bir vektörün eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "reserve(2 * n) çağrılmalıdır"
expected:
  time: { zip_merge: "n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Sonuç vektörünün kapasitesi 2 * n olarak önceden ayrılmış mı?"
  - "Elemanlar doğru sırayla eklenmiş mi?"
reference_solution_path: private/solutions/cpp-veryeasy-merge-alternating.cpp
hint_ladder:
  1: "Sonuç vektörü için reserve(2 * n) çağırın."
  2: "0'dan n-1'e kadar her adımda sırasıyla a[i] ve b[i] değerlerini ekleyin."
  3: "Bu işlem 'vektörleri almaşık birleştirme (alternating zip merge)' olarak bilinir."
```

---

### cpp-veryeasy-first-difference-index

```yaml
id: cpp-veryeasy-first-difference-index
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "İki dizginin farklılaştığı ilk karakter indeksini bulma"
prompt: |
  İki metin görünümünü baştan sona karşılaştırarak ilk farklı karakterin indeksini std::optional<size_t> olarak döndüren `std::optional<size_t> first_mismatch(std::string_view a, std::string_view b)` fonksiyonunu yazın. Metinler tamamen aynıysa veya biri diğerinin önekiyse std::nullopt dönmelidir. n kısa metnin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "std::mismatch kullanılabilir"
expected:
  time: { first_mismatch: "n" }
  space: "1"
concept_tags: [strings, copies]
checklist_extra:
  - "std::mismatch ile iki aralık karşılaştırılmış mı?"
  - "Önek olma durumu doğru yönetilmiş mi?"
reference_solution_path: private/solutions/cpp-veryeasy-first-difference-index.cpp
hint_ladder:
  1: "Kısa olan metnin sonuna kadar karakterleri eşzamanlı kıyaslayın."
  2: "Farklılaşan ilk karakter indeksini bulunca döndürün."
  3: "Bu karşılaştırma 'ilk uyumsuzluk indeksi bulma (first mismatch index)' olarak bilinir."
```

---

### cpp-veryeasy-count-subsequence-chars

```yaml
id: cpp-veryeasy-count-subsequence-chars
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Metinde hedef karakter çiftinin ardışık geçiş sayısını sayma"
prompt: |
  Bir metin görünümünde c1 ve c2 karakterlerinin yan yana (c1 ardından c2) kaç kez geçtiğini sayan `size_t count_adjacent_pairs(std::string_view text, char c1, char c2)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "n < 2 için 0 dönmelidir"
expected:
  time: { count_adjacent_pairs: "n" }
  space: "1"
concept_tags: [strings, const-correctness]
checklist_extra:
  - "Sınır aşımı olmadan text[i] ve text[i+1] taranmış mı?"
  - "const referans veya string_view kullanılmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-count-subsequence-chars.cpp
hint_ladder:
  1: "0'dan text.size() - 2'ye kadar döngü kurun."
  2: "text[i] == c1 ve text[i+1] == c2 olduğu her durumda sayacı bir artırın."
  3: "Bu algoritma 'ardışık karakter çifti sayımı (adjacent pair counting)' olarak bilinir."
```

---

### cpp-veryeasy-is-subvector

```yaml
id: cpp-veryeasy-is-subvector
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Vektörün kesintisiz alt dizisi olduğunu denetleme"
prompt: |
  small vektörünün (m elemanlı) big vektörünün (n elemanlı) kesintisiz bir alt dizisi olup olmadığını denetleyen `bool is_subsegment(const std::vector<int>& big, const std::vector<int>& small)` fonksiyonunu yazın. Boş small her zaman alt dizidir. n büyük ve m küçük vektör boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(1) olmalı"
  - "std::search kullanılabilir"
expected:
  time: { is_subsegment: "n*m" }
  space: "1"
concept_tags: [data-structures, const-correctness]
checklist_extra:
  - "small boş olduğunda true dönülmüş mü?"
  - "std::search veya iç içe döngü sınırları aşmayacak şekilde kurulmuş mu?"
reference_solution_path: private/solutions/cpp-veryeasy-is-subvector.cpp
hint_ladder:
  1: "small boşsa true dönün."
  2: "std::search(big.begin(), big.end(), small.begin(), small.end()) != big.end() sonucunu döndürün."
  3: "Bu arama 'kesintisiz alt vektör denetimi (subsegment search)' olarak bilinir."
```

---

### cpp-veryeasy-generate-squares

```yaml
id: cpp-veryeasy-generate-squares
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Ardışık tamsayıların karelerini içeren vektör üretme"
prompt: |
  1'den n'e kadar olan tamsayıların karelerini (1, 4, 9, ...) içeren bir std::vector<long long> üreten `std::vector<long long> generate_squares(size_t n)` fonksiyonunu yazın. n tamsayı adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "reserve ile kapasite baştan ayrılmalıdır"
expected:
  time: { generate_squares: "n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "reserve(n) çağrılarak yeniden tahsisler engellenmiş mi?"
  - "64-bit kare hesabı yapılmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-generate-squares.cpp
hint_ladder:
  1: "Sonuç vektörü için result.reserve(n) çağırın."
  2: "1'den n'e kadar her sayı için 1LL * i * i değerini vektöre ekleyin."
  3: "Bu işlem 'kareler dizisi üretimi (squares sequence generation)' olarak bilinir."
```

---

### cpp-veryeasy-binary-to-int

```yaml
id: cpp-veryeasy-binary-to-int
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "İkilik tabandaki metin dizisini tamsayıya dönüştürme"
prompt: |
  Yalnızca '0' ve '1' karakterlerinden oluşan bir metin görünümünü işaretsiz tamsayıya (unsigned int) dönüştüren `unsigned int parse_binary(std::string_view bin_str)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Bit kaydırma operatörleri kullanılabilir"
expected:
  time: { parse_binary: "n" }
  space: "1"
concept_tags: [strings, performance]
checklist_extra:
  - "result = (result << 1) | (c - '0') bit kaydırması yapılmış mı?"
  - "string_view ile kopyasız işlenmiş mi?"
reference_solution_path: private/solutions/cpp-veryeasy-binary-to-int.cpp
hint_ladder:
  1: "result değişkenini 0 ile başlatın."
  2: "Her karakter için (result << 1) | (c - '0') işlemi uygulayarak bitleri sola kaydırın."
  3: "Bu dönüşüm 'ikilik metin ayrıştırma (binary string parsing)' olarak bilinir."
```

---

### cpp-veryeasy-diff-vectors

```yaml
id: cpp-veryeasy-diff-vectors
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "İki vektörün karşılıklı eleman farklarından yeni vektör oluşturma"
prompt: |
  n elemanlı iki tamsayı vektörünün karşılıklı elemanlarının farkını (a[i] - b[i]) hesaplayarak yeni bir vektör döndüren `std::vector<int> elementwise_diff(const std::vector<int>& a, const std::vector<int>& b)` fonksiyonunu yazın. n vektörün boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "reserve(n) kullanılmalıdır"
expected:
  time: { elementwise_diff: "n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Sonuç vektörüne reserve(n) yapılmış mı?"
  - "const referanslar kullanılmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-diff-vectors.cpp
hint_ladder:
  1: "Sonuç için n boyutunda kapasite ayırın."
  2: "Her indeks için a[i] - b[i] değerini ekleyin."
  3: "Bu vektör işlemi 'eleman bazında çıkarma (elementwise difference)' olarak bilinir."
```

---

### cpp-veryeasy-check-palindrome-numbers

```yaml
id: cpp-veryeasy-check-palindrome-numbers
version: 1
language: cpp
engine: none
difficulty: very_easy
title: "Tamsayı vektörünün simetrik olduğunu sınama"
prompt: |
  n elemanlı bir tamsayı vektörünün baştan ve sondan okunuşunun aynı (simetrik) olup olmadığını iki işaretçiyle denetleyen `bool is_symmetric_vector(const std::vector<int>& vec)` fonksiyonunu yazın. n vektörün eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "const referans kullanılmalıdır"
expected:
  time: { is_symmetric_vector: "n" }
  space: "1"
concept_tags: [data-structures, const-correctness]
checklist_extra:
  - "Sol ve sağ indeksler merkeze doğru ilerletilmiş mi?"
  - "Uyuşmazlık anında erken çıkış yapılmış mı?"
reference_solution_path: private/solutions/cpp-veryeasy-check-palindrome-numbers.cpp
hint_ladder:
  1: "Biri başta diğeri sonda iki indeks tutun."
  2: "İndeksler birbirine yaklaşırken elemanları karşılaştırın, uyuşmazlık varsa false dönün."
  3: "Bu algoritma 'vektör simetri denetimi (symmetric vector check)' olarak bilinir."
```

---


---

## 2. Kolay (Easy) — 50 Soru

---

### cpp-easy-custom-resource-raii

```yaml
id: cpp-easy-custom-resource-raii
version: 1
language: cpp
engine: none
difficulty: easy
title: "Dosya tanımlayıcısını kapsülleyen RAII sarmalayıcısı"
prompt: |
  Bir işletim sistemi dosya tanımlayıcısını (file descriptor int fd) yapıcıda devralan ve nesne kapsamdan çıktığında yıkıcıda otomatik kapatan `class FileDescriptor` RAII sınıfını yazın. Kopya işlemleri silinmeli, taşıma desteklenmelidir.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Kopya işlemleri delete edilmeli"
expected:
  time: { FileDescriptor: "1" }
  space: "1"
concept_tags: [raii, ownership]
checklist_extra:
  - "Yıkıcıda fd geçerliyse close() çağrılmış mı?"
  - "Taşıma yapıcısında taşınan nesnenin fd değeri -1 yapılmış mı?"
reference_solution_path: private/solutions/cpp-easy-custom-resource-raii.cpp
hint_ladder:
  1: "Yapıcıda fd değerini bir üye değişkene atayın."
  2: "Yıkıcıda fd != -1 ise kapatma fonksiyonunu çağırıp kaynağı otomatik serbest bırakın."
  3: "Bu C++ kaynak yönetim paradigması 'kaynak edinimi başlatmadır (RAII idiom)' olarak bilinir."
```

---

### cpp-easy-unique-ownership-wrap

```yaml
id: cpp-easy-unique-ownership-wrap
version: 1
language: cpp
engine: none
difficulty: easy
title: "Dinamik nesneyi tekil sahiplik sarmalayıcısına alma"
prompt: |
  Verilen id parametresiyle dinamik bir Widget nesnesi oluşturup tekil sahiplik garantisiyle döndüren `std::unique_ptr<Widget> create_widget(int id)` fabrika fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "std::make_unique kullanılmalıdır"
expected:
  time: { create_widget: "1" }
  space: "1"
concept_tags: [smart-pointers, ownership]
checklist_extra:
  - "std::make_unique ile istisna güvenli tahsis yapılmış mı?"
  - "Çıplak new kullanımından kaçınılmış mı?"
reference_solution_path: private/solutions/cpp-easy-unique-ownership-wrap.cpp
hint_ladder:
  1: "Çıplak new yerine std::make_unique<Widget>(id) çağrısı yapın."
  2: "Dönen nesne kapsam dışına çıktığında belleği otomatik temizleyecektir."
  3: "Bu bellek yönetimi 'tekil sahiplikli akıllı işaretçi (unique pointer ownership)' olarak bilinir."
```

---

### cpp-easy-move-constructor-demo

```yaml
id: cpp-easy-move-constructor-demo
version: 1
language: cpp
engine: none
difficulty: easy
title: "Dinamik tampon taşıyan sınıf için taşıma yapıcı tanımlama"
prompt: |
  Dinamik bir tamsayı dizisi ve boyutunu tutan `class DynamicBuffer` sınıfı için kaynakları kopyalamak yerine sahipliğini çalan taşıma yapıcısını (move constructor) ve noexcept niteleyicisini uygulayın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "noexcept belirtilmeli"
expected:
  time: { DynamicBuffer: "1" }
  space: "1"
concept_tags: [move-semantics, rule-of-five]
checklist_extra:
  - "Taşınan nesnenin işaretçisi nullptr yapılmış mı?"
  - "Taşıma yapıcı noexcept olarak bildirilmiş mi?"
reference_solution_path: private/solutions/cpp-easy-move-constructor-demo.cpp
hint_ladder:
  1: "Diğer nesnenin data_ ve size_ alanlarını mevcut nesneye kopyalayın."
  2: "Diğer nesnenin işaretçisini nullptr ve boyutunu 0 yaparak çift serbest bırakmayı (double-free) önleyin."
  3: "Bu C++ optimizasyonu 'taşıma yapıcısı (move constructor)' olarak bilinir."
```

---

### cpp-easy-const-member-inspect

```yaml
id: cpp-easy-const-member-inspect
version: 1
language: cpp
engine: none
difficulty: easy
title: "Değiştirici olmayan üye fonksiyonları const ile işaretleme"
prompt: |
  Bir metin görünümü saklayan ve metnin uzunluğunu sorgulayan get_length() ile metni döndüren get_text() üye fonksiyonlarını const doğruluğuna uygun olarak tanımlayan `class ReadOnlyView` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Üye fonksiyonlar const niteleyicisi almalıdır"
expected:
  time: { ReadOnlyView: "1" }
  space: "1"
concept_tags: [const-correctness, performance]
checklist_extra:
  - "Sınıf durumunu değiştirmeyen fonksiyonlar const bildirilmiş mi?"
  - "const nesneler üzerinden bu fonksiyonlar çağrılabiliyor mu?"
reference_solution_path: private/solutions/cpp-easy-const-member-inspect.cpp
hint_ladder:
  1: "Üye fonksiyon tanımının sonuna const anahtar sözcüğünü ekleyin."
  2: "Böylece const referansla erişilen nesneler üzerinden de bu fonksiyonların çağrılmasına olanak sağlayın."
  3: "Bu tasarım kuralı 'const doğruluğu (const correctness)' olarak bilinir."
```

---

### cpp-easy-hash-map-word-frequency

```yaml
id: cpp-easy-hash-map-word-frequency
version: 1
language: cpp
engine: none
difficulty: easy
title: "Metindeki sözcüklerin sıklıklarını karma tablosunda sayma"
prompt: |
  Boşluklarla ayrılmış sözcükler içeren bir metin görünümündeki her bir sözcüğün frekansını hesaplayan `std::unordered_map<std::string, size_t> word_frequencies(std::string_view text)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "std::unordered_map kullanılmalıdır"
expected:
  time: { word_frequencies: "n" }
  space: "n"
concept_tags: [hash-map, data-structures]
checklist_extra:
  - "Sözcükler string_view ile parçalanıp haritaya eklenirken kopyalanmış mı?"
  - "Ortalama O(1) karma erişimi sağlanmış mı?"
reference_solution_path: private/solutions/cpp-easy-hash-map-word-frequency.cpp
hint_ladder:
  1: "Metni boşluklara göre sözcük sözcük tarayın."
  2: "Her sözcük için freq_map[word]++ ifadesiyle frekansı artırın."
  3: "Bu algoritma 'karma tablosu ile frekans sayımı (hash map word frequency)' olarak bilinir."
```

---

### cpp-easy-safe-integer-division

```yaml
id: cpp-easy-safe-integer-division
version: 1
language: cpp
engine: none
difficulty: easy
title: "Tamsayı bölmesinde sıfıra bölme ve taşmayı önleme"
prompt: |
  İki işaretli tamsayının bölme sonucunu hesaplayan, bölen 0 ise veya INT_MIN / -1 taşması oluşursa std::nullopt döndüren `std::optional<int> safe_divide(int a, int b)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "INT_MIN / -1 taşması kontrol edilmelidir"
expected:
  time: { safe_divide: "1" }
  space: "1"
concept_tags: [integer-division, edge-cases]
checklist_extra:
  - "b == 0 durumu kontrol edilmiş mi?"
  - "a == INT_MIN ve b == -1 taşma durumu std::nullopt ile elenmiş mi?"
reference_solution_path: private/solutions/cpp-easy-safe-integer-division.cpp
hint_ladder:
  1: "b == 0 ise doğrudan std::nullopt dönün."
  2: "a == std::numeric_limits<int>::min() ve b == -1 durumunda taşmayı önlemek için std::nullopt dönün."
  3: "Bu kontrol 'güvenli tamsayı bölmesi (safe integer division)' olarak bilinir."
```

---

### cpp-easy-binary-search-vector

```yaml
id: cpp-easy-binary-search-vector
version: 1
language: cpp
engine: none
difficulty: easy
title: "Sıralı vektörde ikili aramayla değerin indeksini bulma"
prompt: |
  Küçükten büyüğe sıralı n elemanlı bir tamsayı vektöründe target değerini ikili aramayla arayan ve indeksini std::optional içinde döndüren `std::optional<size_t> binary_search_index(const std::vector<int>& vec, int target)` fonksiyonunu yazın. n vektörün boyutudur.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Orta nokta hesabı taşmasız (low + (high - low) / 2) yapılmalı"
expected:
  time: { binary_search_index: "log n" }
  space: "1"
concept_tags: [data-structures, const-correctness]
checklist_extra:
  - "Orta nokta hesabında tamsayı taşması engellenmiş mi?"
  - "Bulunamadığında std::nullopt dönülmüş mü?"
reference_solution_path: private/solutions/cpp-easy-binary-search-vector.cpp
hint_ladder:
  1: "low ve high indeksleri ile arama aralığını belirleyin."
  2: "mid = low + (high - low) / 2 formülüyle orta noktayı bulup aralığı yarıya indirin."
  3: "Bu algoritma 'ikili arama algoritması (binary search)' olarak bilinir."
```

---

### cpp-easy-two-sum-hash

```yaml
id: cpp-easy-two-sum-hash
version: 1
language: cpp
engine: none
difficulty: easy
title: "Vektörde toplamı hedefe eşit iki indeksi karma tablosuyla bulma"
prompt: |
  n elemanlı bir tamsayı vektöründe toplamları target değerine eşit olan iki elemanın indeks çiftini karma haritası kullanarak O(n) sürede bulan `std::optional<std::pair<size_t, size_t>> two_sum_hash(const std::vector<int>& vec, int target)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "std::unordered_map kullanılmalıdır"
expected:
  time: { two_sum_hash: "n" }
  space: "n"
concept_tags: [hash-map, data-structures]
checklist_extra:
  - "target - vec[i] değeri haritada aranmış mı?"
  - "Aynı elemanın iki kez kullanılması engellenmiş mi?"
reference_solution_path: private/solutions/cpp-easy-two-sum-hash.cpp
hint_ladder:
  1: "Vektörü gezerken her eleman için aranan tamamlayıcıyı (target - vec[i]) karma haritasında sorgulayın."
  2: "Mevcutsa indeks çiftini döndürün, değilse vec[i] değerini indeksiyle haritaya kaydedin."
  3: "Bu algoritma 'karma tablosuyla iki sayı toplamı (hash map two sum)' olarak bilinir."
```

---

### cpp-easy-merge-sorted-ranges

```yaml
id: cpp-easy-merge-sorted-ranges
version: 1
language: cpp
engine: none
difficulty: easy
title: "İki sıralı vektörü tek bir sıralı vektörde birleştirme"
prompt: |
  Küçükten büyüğe sıralı a (n elemanlı) ve b (m elemanlı) vektörlerini birleştirerek n + m elemanlı yeni bir sıralı vektör üreten `std::vector<int> merge_sorted(const std::vector<int>& a, const std::vector<int>& b)` fonksiyonunu yazın. n ve m vektör boyutlarıdır.
constraints:
  - "Zaman karmaşıklığı O(n + m) olmalı"
  - "Ek bellek O(n + m) olmalı"
  - "reserve(n + m) çağrılmalıdır"
expected:
  time: { merge_sorted: "n + m" }
  space: "n + m"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Sonuç vektörünün kapasitesi reserve ile baştan ayrılmış mı?"
  - "std::merge veya iki indeks kullanılmış mı?"
reference_solution_path: private/solutions/cpp-easy-merge-sorted-ranges.cpp
hint_ladder:
  1: "Sonuç vektörüne a.size() + b.size() kadar reserve yapın."
  2: "İki işaretçi ile küçük olan elemanı sırayla sonuca ekleyin ya da std::merge çağırın."
  3: "Bu algoritma 'sıralı aralıkları birleştirme (merge sorted ranges)' olarak bilinir."
```

---

### cpp-easy-custom-string-builder

```yaml
id: cpp-easy-custom-string-builder
version: 1
language: cpp
engine: none
difficulty: easy
title: "Gereksiz kopyalamaları önleyen metin biriktirici"
prompt: |
  Sık metin eklemelerinde yeniden tahsisleri azaltmak için reserve desteği sunan ve append ile metin parçalarını biriktiren `class SimpleStringBuilder` sınıfını yazın. m eklenen metin uzunluğudur.
constraints:
  - "Amortize zaman karmaşıklığı O(m) olmalı"
  - "Ek bellek O(m) olmalı"
  - "move semantiğiyle nihai std::string döndürülmelidir"
expected:
  time: { SimpleStringBuilder: "m" }
  space: "m"
concept_tags: [strings, move-semantics]
checklist_extra:
  - "append işlemlerinde string_view kullanılmış mı?"
  - "str() metodu taşınabilir std::string döndürüyor mu?"
reference_solution_path: private/solutions/cpp-easy-custom-string-builder.cpp
hint_ladder:
  1: "Dahili bir std::string üyesinde tamponu tutun."
  2: "append(std::string_view piece) ile gereksiz kopyalama olmadan tampona ekleme yapın."
  3: "Bu tasarım 'metin inşa edici deseni (string builder pattern)' olarak bilinir."
```

---

### cpp-easy-point-operators

```yaml
id: cpp-easy-point-operators
version: 1
language: cpp
engine: none
difficulty: easy
title: "İki boyutlu nokta sınıfı için operatör aşırı yüklemesi"
prompt: |
  x ve y koordinatlarını tutan `struct Point2D` yapısı için iki noktayı toplayan operator+ ve eşitliklerini denetleyen operator== aşırı yüklemelerini const doğruluğuna uygun olarak yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Operatörler const referans almalı ve const olmalıdır"
expected:
  time: { Point2D: "1" }
  space: "1"
concept_tags: [operator-overloading, const-correctness]
checklist_extra:
  - "operator+ yeni bir Point2D nesnesi döndürüyor mu?"
  - "operator== const niteleyicisi almış mı?"
reference_solution_path: private/solutions/cpp-easy-point-operators.cpp
hint_ladder:
  1: "Point2D operator+(const Point2D& other) const { return {x + other.x, y + other.y}; } şeklinde tanımlayın."
  2: "Eşitlik operatöründe (x == other.x && y == other.y) karşılaştırması yapın."
  3: "Bu C++ yeteneği 'operatör aşırı yükleme (operator overloading)' olarak bilinir."
```

---

### cpp-easy-rule-of-three-buffer

```yaml
id: cpp-easy-rule-of-three-buffer
version: 1
language: cpp
engine: none
difficulty: easy
title: "Dinamik bellek yöneten sınıfta 3 kuralını uygulama"
prompt: |
  Dinamik bir tamsayı dizisi ve kapasite tutan `class IntBuffer` sınıfında bellek sızıntısı ve çifte serbest bırakmayı önlemek için yıkıcı, kopya yapıcı ve kopya atama operatörünü (Rule of Three) yazın.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Kendine atama (self-assignment) kontrol edilmelidir"
expected:
  time: { IntBuffer: "n" }
  space: "n"
concept_tags: [rule-of-five, raii]
checklist_extra:
  - "Kopya yapıcı derin kopyalama yapıyor mu?"
  - "Kopya atama operatöründe if (this != &other) kontrolü var mı?"
reference_solution_path: private/solutions/cpp-easy-rule-of-three-buffer.cpp
hint_ladder:
  1: "Yıkıcıda delete[] data_ çağrısı yapın."
  2: "Kopya yapıcı ve kopya atama operatöründe belleğin bağımsız bir kopyasını tahsis ederek derin kopyalama sağlayın."
  3: "Bu C++ temel kuralı 'üç kuralı (Rule of Three)' olarak bilinir."
```

---

### cpp-easy-avoid-string-copies

```yaml
id: cpp-easy-avoid-string-copies
version: 1
language: cpp
engine: none
difficulty: easy
title: "Metin işleme fonksiyonunda kopyalamayı önlemek için görünüm kullanma"
prompt: |
  Metin içindeki büyük harfle başlayan sözcüklerin sayısını std::string_view kullanarak hiçbir bellek kopyalaması yapmadan hesaplayan `size_t count_uppercase_words(std::string_view text)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "std::string_view kullanılmalıdır"
expected:
  time: { count_uppercase_words: "n" }
  space: "1"
concept_tags: [copies, strings]
checklist_extra:
  - "std::string_view değerle geçilmiş mi?"
  - "Kopyasız sözcük ayrıştırması yapılmış mı?"
reference_solution_path: private/solutions/cpp-easy-avoid-string-copies.cpp
hint_ladder:
  1: "std::string yerine std::string_view alarak kopya tahsisini sıfırlayın."
  2: "Boşlukları atlayıp her sözcüğün ilk karakterinin std::isupper olup olmadığını test edin."
  3: "Bu optimizasyon 'metin kopyalamalarını önleme (avoiding string copies)' olarak bilinir."
```

---

### cpp-easy-shared-ownership-counter

```yaml
id: cpp-easy-shared-ownership-counter
version: 1
language: cpp
engine: none
difficulty: easy
title: "Paylaşılan kaynak için başvuru sayacını izleme"
prompt: |
  std::shared_ptr ile yönetilen bir kaynağın mevcut referans sayısını use_count() ile sorgulayarak kaynak birden fazla yerde paylaşılıyorsa true dönen `bool is_shared(const std::shared_ptr<SharedResource>& ptr)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "use_count() kontrol edilmelidir"
expected:
  time: { is_shared: "1" }
  space: "1"
concept_tags: [smart-pointers, ownership]
checklist_extra:
  - "ptr nullptr olduğunda false dönülmüş mü?"
  - "ptr->use_count() > 1 kontrolü yapılmış mı?"
reference_solution_path: private/solutions/cpp-easy-shared-ownership-counter.cpp
hint_ladder:
  1: "ptr == nullptr ise false dönün."
  2: "ptr.use_count() > 1 ifadesinin doğruluğunu kontrol edin."
  3: "Bu mekanizma 'paylaşımlı sahiplik başvuru takibi (shared ownership use count)' olarak bilinir."
```

---

### cpp-easy-find-intersection-sets

```yaml
id: cpp-easy-find-intersection-sets
version: 1
language: cpp
engine: none
difficulty: easy
title: "İki kümenin kesişim elemanlarını yeni kümede toplama"
prompt: |
  n elemanlı a ve m elemanlı b karma kümelerindeki ortak elemanları yeni bir std::unordered_set<int> içinde döndüren `std::unordered_set<int> set_intersection(const std::unordered_set<int>& a, const std::unordered_set<int>& b)` fonksiyonunu yazın. n ve m küme boyutlarıdır.
constraints:
  - "Zaman karmaşıklığı O(min(n, m)) olmalı"
  - "Ek bellek O(min(n, m)) olmalı"
  - "Daha küçük küme üzerinde döngü kurulmalıdır"
expected:
  time: { set_intersection: "n + m" }
  space: "n + m"
concept_tags: [hash-map, performance]
checklist_extra:
  - "Döngü daha küçük olan küme üzerinde mi kurulmuş?"
  - "const referanslar kullanılmış mı?"
reference_solution_path: private/solutions/cpp-easy-find-intersection-sets.cpp
hint_ladder:
  1: "Boyutu daha küçük olan kümeyi döngüye sokun."
  2: "Her elemanı büyük kümede count veya find ile arayarak sonuca ekleyin."
  3: "Bu işlem 'küme kesişimi bulma (hash set intersection)' olarak bilinir."
```

---

### cpp-easy-remove-if-erase

```yaml
id: cpp-easy-remove-if-erase
version: 1
language: cpp
engine: none
difficulty: easy
title: "Şartı sağlayan elemanları vektörden kaldırma"
prompt: |
  n elemanlı tamsayı vektöründeki tüm tek sayıları silen ve boyutu daraltan `void remove_odd_numbers(std::vector<int>& vec)` fonksiyonunu yazın. n vektörün eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "std::erase_if veya std::remove_if kullanılmalıdır"
expected:
  time: { remove_odd_numbers: "n" }
  space: "1"
concept_tags: [data-structures, iterator-invalidation]
checklist_extra:
  - "Tek döngüde O(n) karmaşıklık sağlanmış mı?"
  - "vec.erase(std::remove_if(...), vec.end()) doğru uygulanmış mı?"
reference_solution_path: private/solutions/cpp-easy-remove-if-erase.cpp
hint_ladder:
  1: "std::erase_if(vec, [](int x){ return x % 2 != 0; }) fonksiyonunu çağırın."
  2: "Vektör içindeki tek sayılar kaldırılıp çift sayılar öne kaydırılacaktır."
  3: "Bu deyim 'vektörden eleman silme deyimi (erase-remove idiom)' olarak bilinir."
```

---

### cpp-easy-circular-buffer-index

```yaml
id: cpp-easy-circular-buffer-index
version: 1
language: cpp
engine: none
difficulty: easy
title: "Sabit boyutlu dairesel tampon indeksi ilerletme"
prompt: |
  Kapasitesi baştan tanımlanan bir dairesel tamponda yazma indeksini güvenle bir adım ilerleten ve başa sarmayı sağlayan `class CircularIndex` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Modül aritmetiği kullanılmalıdır"
expected:
  time: { CircularIndex: "1" }
  space: "1"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "index = (index + 1) % capacity formülü kullanılmış mı?"
  - "Kapasite 0 kontrolü yapılmış mı?"
reference_solution_path: private/solutions/cpp-easy-circular-buffer-index.cpp
hint_ladder:
  1: "İndeksi artırırken (index_ + 1) % capacity_ formülünü kullanın."
  2: "Böylece tampon sınırına gelindiğinde otomatik olarak sıfırıncı indekse dönülmesini sağlayın."
  3: "Bu mekanizma 'dairesel indeksleme (circular buffer indexing)' olarak bilinir."
```

---

### cpp-easy-matrix-transpose-vector

```yaml
id: cpp-easy-matrix-transpose-vector
version: 1
language: cpp
engine: none
difficulty: easy
title: "Vektörler vektörü matrisin devriğini alma"
prompt: |
  n x m boyutundaki bir tamsayı matrisinin devriğini alarak m x n boyutunda yeni bir matris üreten `std::vector<std::vector<int>> transpose_matrix(const std::vector<std::vector<int>>& mat)` fonksiyonunu yazın. n satır ve m sütun sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(n * m) olmalı"
  - "Boyutlar baştan ayrılmalıdır"
expected:
  time: { transpose_matrix: "n*m" }
  space: "n*m"
concept_tags: [data-structures, const-correctness]
checklist_extra:
  - "Sonuç matrisi m x n boyutunda baştan tahsis edilmiş mi?"
  - "result[j][i] = mat[i][j] ataması doğru yapılmış mı?"
reference_solution_path: private/solutions/cpp-easy-matrix-transpose-vector.cpp
hint_ladder:
  1: "m satır ve n sütundan oluşan yeni bir matris oluşturun."
  2: "İç içe döngüyle result[j][i] = mat[i][j] kopyalamasını yapın."
  3: "Bu işlem 'matris transpozu alma (matrix transpose)' olarak bilinir."
```

---

### cpp-easy-check-anagram-hash

```yaml
id: cpp-easy-check-anagram-hash
version: 1
language: cpp
engine: none
difficulty: easy
title: "İki metnin karma tablosuyla anagram olduğunu denetleme"
prompt: |
  İki metin görünümünün karakter sıklıklarını std::unordered_map ile sayarak anagram olup olmadığını denetleyen `bool are_anagrams_hash(std::string_view s1, std::string_view s2)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Boyut eşitliği başta kontrol edilmelidir"
expected:
  time: { are_anagrams_hash: "n" }
  space: "n"
concept_tags: [hash-map, strings]
checklist_extra:
  - "Boyut farkı varsa hemen false dönülmüş mü?"
  - "İlk metin için frekans artırılıp ikincisi için azaltılmış mı?"
reference_solution_path: private/solutions/cpp-easy-check-anagram-hash.cpp
hint_ladder:
  1: "s1.size() != s2.size() ise hemen false dönün."
  2: "std::unordered_map<char, int> açıp s1 harflerini artırın, s2 harflerini azaltın; tüm değerlerin 0 kaldığını doğrulayın."
  3: "Bu algoritma 'karma tablosu ile anagram testi (hash map anagram check)' olarak bilinir."
```

---

### cpp-easy-custom-optional-type

```yaml
id: cpp-easy-custom-optional-type
version: 1
language: cpp
engine: none
difficulty: easy
title: "Değerin varlığını veya yokluğunu temsil eden basit tür"
prompt: |
  İçinde bir değer bulunup bulunmadığını bir boole bayrağıyla tutan ve değer varsa erişim sağlayan `class CustomOptional` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Boş durumda erişim istisna fırlatmalı veya tanımsız olmamalıdır"
expected:
  time: { CustomOptional: "1" }
  space: "1"
concept_tags: [edge-cases, const-correctness]
checklist_extra:
  - "has_value() üye fonksiyonu const mu?"
  - "value() çağrısı değer yoksa istisna fırlatıyor mu?"
reference_solution_path: private/solutions/cpp-easy-custom-optional-type.cpp
hint_ladder:
  1: "bool has_val_ ve T value_ üyelerini tutun."
  2: "has_value() true ise değeri döndürün, değilse güvenli hata yönetimini devreye sokun."
  3: "Bu tasarım 'isteğe bağlı değer sarmalayıcısı (optional type wrapper)' olarak bilinir."
```

---

### cpp-easy-weak-ptr-break-cycle

```yaml
id: cpp-easy-weak-ptr-break-cycle
version: 1
language: cpp
engine: none
difficulty: easy
title: "İki nesne arasındaki karşılıklı döngüsel sahipliği zayıf işaretçiyle kırma"
prompt: |
  Ebeveyn nesnenin çocuğu std::shared_ptr ile tuttuğu, çocuğun ise ebeveyni std::weak_ptr ile gösterdiği `struct NodeParentChild` yapısını tasarlayarak bellek sızıntısını önleyin.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "weak_ptr kullanılarak döngü kırılmalıdır"
expected:
  time: { NodeParentChild: "1" }
  space: "1"
concept_tags: [smart-pointers, cyclic-reference]
checklist_extra:
  - "Çocuk düğümde ebeveyn işaretçisi weak_ptr yapılmış mı?"
  - "shared_ptr döngüsü kırılmış mı?"
reference_solution_path: private/solutions/cpp-easy-weak-ptr-break-cycle.cpp
hint_ladder:
  1: "Ebeveyn düğüm çocuğa shared_ptr ile bağlansın."
  2: "Çocuk düğüm ebeveyne sahiplik almadan std::weak_ptr ile işaret etsin; böylece yıkıcılar birbirini engellemesin."
  3: "Bu teknik 'döngüsel başvuruyu zayıf işaretçiyle kırma (breaking reference cycles with weak_ptr)' olarak bilinir."
```

---

### cpp-easy-safe-vector-at

```yaml
id: cpp-easy-safe-vector-at
version: 1
language: cpp
engine: none
difficulty: easy
title: "Sınır dışı erişimlerde istisna fırlatan güvenli erişim fonksiyonu"
prompt: |
  n elemanlı bir tamsayı vektöründe index konumundaki elemanı döndüren, index >= n ise std::out_of_range istisnası fırlatan `int safe_get(const std::vector<int>& vec, size_t index)` fonksiyonunu yazın. n vektörün boyutudur.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "vec.at() veya sınır denetimi kullanılmalıdır"
expected:
  time: { safe_get: "1" }
  space: "1"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "vec.at(index) kullanılarak güvenli kontrol sağlanmış mı?"
  - "const referans kullanılmış mı?"
reference_solution_path: private/solutions/cpp-easy-safe-vector-at.cpp
hint_ladder:
  1: "Köşeli parantez [] operatörü sınır denetimi yapmaz."
  2: "vec.at(index) metodunu kullanarak sınır aşımında otomatik istisna fırlatılmasını sağlayın."
  3: "Bu kontrol 'sınır korumalı vektör erişimi (bounds checked vector access)' olarak bilinir."
```

---

### cpp-easy-sort-by-custom-lambda

```yaml
id: cpp-easy-sort-by-custom-lambda
version: 1
language: cpp
engine: none
difficulty: easy
title: "Dizgileri uzunluklarına göre lambda ifadesiyle sıralama"
prompt: |
  Dizgiler vektörünü karakter uzunluklarına göre küçükten büyüğe std::sort ve lambda fonksiyonu kullanarak sıralayan `void sort_by_length(std::vector<std::string>& words)` fonksiyonunu yazın. n vektörün eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n log n) olmalı"
  - "Ek bellek O(log n) olmalı"
  - "Lambda parametreleri const referans almalıdır"
expected:
  time: { sort_by_length: "n log n" }
  space: "log n"
concept_tags: [performance, copies]
checklist_extra:
  - "Lambda parametresi (const std::string& a, const std::string& b) kopyalamasız mı?"
  - "a.size() < b.size() karşılaştırması yapılmış mı?"
reference_solution_path: private/solutions/cpp-easy-sort-by-custom-lambda.cpp
hint_ladder:
  1: "std::sort algoritmasını çağırın."
  2: "Karşılaştırıcı olarak [](const std::string& a, const std::string& b){ return a.size() < b.size(); } lambdasını geçin."
  3: "Bu işlem 'özel lambda ile sıralama (sort with custom lambda)' olarak bilinir."
```

---

### cpp-easy-find-majority-element

```yaml
id: cpp-easy-find-majority-element
version: 1
language: cpp
engine: none
difficulty: easy
title: "Boyutun yarısından fazla tekrar eden çoğunluk elemanını bulma"
prompt: |
  n elemanlı bir tamsayı vektöründe n/2'den fazla kez geçen çoğunluk elemanını Boyer-Moore oylama algoritmasıyla O(n) zaman ve O(1) ek alanda bulan `std::optional<int> find_majority(const std::vector<int>& vec)` fonksiyonunu yazın. n vektörün boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "İkinci geçişte adayın doğrulaması yapılmalıdır"
expected:
  time: { find_majority: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Oylama algoritmasıyla aday tek geçişte bulunmuş mu?"
  - "İkinci geçişte adayın gerçekten > n/2 olduğu doğrulanmış mı?"
reference_solution_path: private/solutions/cpp-easy-find-majority-element.cpp
hint_ladder:
  1: "Bir aday ve sayaç değişkeni tutarak aynı elemanda sayacı artırın, farklı elemanda sayacı azaltın."
  2: "Sayaç sıfırlanırsa yeni elemanı aday yapın; son turda adayın frekansını sayıp n/2'den büyükse döndürün."
  3: "Bu algoritma 'Boyer-Moore çoğunluk oylama algoritması (Boyer-Moore majority vote)' olarak bilinir."
```

---

### cpp-easy-immutable-string-wrapper

```yaml
id: cpp-easy-immutable-string-wrapper
version: 1
language: cpp
engine: none
difficulty: easy
title: "Değiştirilemez metin sarmalayıcısı ve const güvenliği"
prompt: |
  Oluşturulduktan sonra içeriği hiçbir şekilde değiştirilemeyen, const üye fonksiyonlarla okuma sağlayan `class ImmutableString` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "const doğruluğu tam uygulanmalıdır"
expected:
  time: { ImmutableString: "1" }
  space: "1"
concept_tags: [const-correctness, strings]
checklist_extra:
  - "Üye değişken private ve const mu?"
  - "Tüm erişimciler const niteleyicisi almış mı?"
reference_solution_path: private/solutions/cpp-easy-immutable-string-wrapper.cpp
hint_ladder:
  1: "Dahili std::string nesnesini private olarak saklayın."
  2: "Yalnızca const referans veya string_view döndüren const metotlar sunarak içeriğin dışarıdan değiştirilmesini engelleyin."
  3: "Bu tasarım deseni 'değiştirilemez nesne sarmalayıcısı (immutable object wrapper)' olarak bilinir."
```

---

### cpp-easy-array-view-span

```yaml
id: cpp-easy-array-view-span
version: 1
language: cpp
engine: none
difficulty: easy
title: "Dizi ve boyuttan güvenli aralık görünümü oluşturma"
prompt: |
  C tarzı dizi göstericisi ve boyut alarak std::span<const int> üzerinden elemanların toplamını hesaplayan `long long sum_span_elements(std::span<const int> s)` fonksiyonunu yazın. n span içindeki eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "std::span değerle geçilmelidir"
expected:
  time: { sum_span_elements: "n" }
  space: "1"
concept_tags: [data-structures, const-correctness]
checklist_extra:
  - "std::span kopyalanmadan değerle hafif geçilmiş mi?"
  - "Elemanlar const olarak korunmuş mu?"
reference_solution_path: private/solutions/cpp-easy-array-view-span.cpp
hint_ladder:
  1: "std::span<const int> türünü parametre olarak alın."
  2: "Aralık tabanlı for döngüsüyle elemanları gezip 64-bit biriktiricide toplayın."
  3: "Bu modern C++ aracı 'aralık görünümü sarmalayıcısı (span array view)' olarak bilinir."
```

---

### cpp-easy-queue-with-two-stacks

```yaml
id: cpp-easy-queue-with-two-stacks
version: 1
language: cpp
engine: none
difficulty: easy
title: "İki yığın yapısı kullanarak ilk giren ilk çıkar kuyruk oluşturma"
prompt: |
  Yalnızca iki adet std::stack<int> kullanarak FIFO (ilk giren ilk çıkar) kuyruk mantığını gerçekleştiren `class QueueTwoStacks` sınıfını yazın. enqueue ve dequeue operasyonları desteklenmelidir.
constraints:
  - "Amortize zaman karmaşıklığı O(1*) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Ters aktarım gerektiğinde yapılmalıdır"
expected:
  time: { QueueTwoStacks: "1*" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Çıkış yığını boşaldığında giriş yığınından elemanlar devredilmiş mi?"
  - "Amortize O(1) maliyet korunmuş mu?"
reference_solution_path: private/solutions/cpp-easy-queue-with-two-stacks.cpp
hint_ladder:
  1: "Ekleme işlemlerini in_stack'e yapın."
  2: "Çıkarma işleminde out_stack boşsa in_stack'teki tüm elemanları out_stack'e aktarıp en üsttekini çekin."
  3: "Bu veri yapısı mekanizması 'iki yığın ile kuyruk simülasyonu (queue using two stacks)' olarak bilinir."
```

---

### cpp-easy-valid-parentheses-stack

```yaml
id: cpp-easy-valid-parentheses-stack
version: 1
language: cpp
engine: none
difficulty: easy
title: "Yığın veri yapısıyla parantez dengesini doğrulama"
prompt: |
  Yalnızca '(', ')', '{', '}', '[' ve ']' içeren bir metin görünümündeki parantezlerin dengeli olduğunu std::stack kullanarak doğrulayan `bool check_parentheses(std::string_view expr)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Metin bittiğinde yığın boş kalmalıdır"
expected:
  time: { check_parentheses: "n" }
  space: "n"
concept_tags: [data-structures, strings]
checklist_extra:
  - "Boş yığında kapatma parantezi gelmesi kontrol edilmiş mi?"
  - "Tüm karakterler bittiğinde stack.empty() sınanmış mı?"
reference_solution_path: private/solutions/cpp-easy-valid-parentheses-stack.cpp
hint_ladder:
  1: "Açma parantezi gördükçe yığına itin."
  2: "Kapatma parantezi gördükçe yığının tepesindekiyle eşleşip eşleşmediğini kontrol edip tepeyi çekin."
  3: "Bu algoritma 'yığın ile parantez doğrulama (valid parentheses check)' olarak bilinir."
```

---

### cpp-easy-min-stack-support

```yaml
id: cpp-easy-min-stack-support
version: 1
language: cpp
engine: none
difficulty: easy
title: "Sabit sürede asgari elemanı döndüren yığın"
prompt: |
  Standart push, pop, top operasyonlarının yanında mevcut en küçük elemanı O(1) sürede döndüren get_min() fonksiyonuna sahip `class MinStack` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı her işlem için O(1) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Ek bir min_stack tutulmalıdır"
expected:
  time: { MinStack: "1" }
  space: "n"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "Her push işleminde min_stack güncellenmiş mi?"
  - "pop işleminde min_stack senkron tutulmuş mu?"
reference_solution_path: private/solutions/cpp-easy-min-stack-support.cpp
hint_ladder:
  1: "Asıl elemanları saklayan bir yığın ve o ana kadarki minimumları saklayan ikinci bir min_stack tutun."
  2: "get_min() çağrıldığında min_stack'in tepesindeki değeri doğrudan döndürün."
  3: "Bu veri yapısı 'asgari eleman takipli yığın (min stack)' olarak bilinir."
```

---

### cpp-easy-flatten-nested-vectors

```yaml
id: cpp-easy-flatten-nested-vectors
version: 1
language: cpp
engine: none
difficulty: easy
title: "İki boyutlu vektör elemanlarını tek boyutlu vektöre düzleştirme"
prompt: |
  Satır uzunlukları değişken olabilen bir iki boyutlu tamsayı vektörünün tüm elemanlarını tek boyutlu bir vektörde sırayla birleştiren `std::vector<int> flatten_matrix(const std::vector<std::vector<int>>& mat)` fonksiyonunu yazın. n toplam eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Toplam boyut hesaplanıp reserve edilmelidir"
expected:
  time: { flatten_matrix: "n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Toplam eleman sayısı hesaplanıp reserve(total) yapılmış mı?"
  - "Satırlar sırayla eklenmiş mi?"
reference_solution_path: private/solutions/cpp-easy-flatten-nested-vectors.cpp
hint_ladder:
  1: "Önce matristeki tüm satırların boyutlarını toplayıp sonuç vektörünü rezerve edin."
  2: "İç içe iki döngüyle elemanları sırayla tek boyutlu vektöre aktarın."
  3: "Bu işlem 'vektör düzleştirme (matrix flattening)' olarak bilinir."
```

---

### cpp-easy-find-single-number

```yaml
id: cpp-easy-find-single-number
version: 1
language: cpp
engine: none
difficulty: easy
title: "Dizide tek kalan sayıyı bit işlemiyle bulma"
prompt: |
  n elemanlı bir tamsayı vektöründe bir tanesi hariç tüm sayılar tam olarak ikişer kez geçmektedir. Yalnızca bir kez geçen sayıyı O(1) ek bellekle bulan `int find_unique_element(const std::vector<int>& vec)` fonksiyonunu yazın. n eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Bit düzeyi XOR (^) kullanılmalıdır"
expected:
  time: { find_unique_element: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Tüm elemanlar ardışık XOR işlemine sokulmuş mu?"
  - "Ek bellek O(1) sabit tutulmuş mu?"
reference_solution_path: private/solutions/cpp-easy-find-single-number.cpp
hint_ladder:
  1: "result değişkenini 0 ile başlatın."
  2: "Vektördeki tüm elemanları result ^= x işlemiyle XOR'layın; çift gelen sayılar birbirini sıfırlayacaktır."
  3: "Bu teknik 'XOR ile benzersiz eleman tespiti (single number XOR)' olarak bilinir."
```

---

### cpp-easy-group-by-parity

```yaml
id: cpp-easy-group-by-parity
version: 1
language: cpp
engine: none
difficulty: easy
title: "Vektördeki elemanları çiftler önde tekler arkada gruplama"
prompt: |
  n elemanlı bir tamsayı vektöründeki çift sayıları başa, tek sayıları sona yerinde iki işaretçiyle toplayan `void partition_by_parity(std::vector<int>& vec)` fonksiyonunu yazın. n vektörün boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "İki indeks kullanılmalıdır"
expected:
  time: { partition_by_parity: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Sol indeks çift, sağ indeks tek arayarak karşılaşana kadar takas edilmiş mi?"
  - "Yerinde O(1) ek bellek kullanılmış mı?"
reference_solution_path: private/solutions/cpp-easy-group-by-parity.cpp
hint_ladder:
  1: "Soldan çift olmayan, sağdan tek olmayan ilk elemanları bulun."
  2: "İndeksler kesişene kadar elemanları yer değiştirin."
  3: "Bu algoritma 'pariteye göre yerinde bölümleme (partition by parity)' olarak bilinir."
```

---

### cpp-easy-custom-comparator-set

```yaml
id: cpp-easy-custom-comparator-set
version: 1
language: cpp
engine: none
difficulty: easy
title: "Özel sıralama kriteri kullanan sıralı küme yapısı"
prompt: |
  Dizgileri alfabetik sıra yerine uzunluklarına göre, uzunluklar eşitse alfabetik sıraya göre sıralayan karşılaştırıcı nesneyle çalışan `std::set<std::string, CustomCompare>` kümesini tasarlayın.
constraints:
  - "Zaman karmaşıklığı arama/ekleme için O(log n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Sıkı zayıf sıralama (strict weak ordering) kuralı sağlanmalıdır"
expected:
  time: { CustomCompare: "log n" }
  space: "1"
concept_tags: [data-structures, const-correctness]
checklist_extra:
  - "operator() const bildirilmiş mi?"
  - "Eşitlik durumunda sözlük sırasına bakılarak eleman kaybı önlenmiş mi?"
reference_solution_path: private/solutions/cpp-easy-custom-comparator-set.cpp
hint_ladder:
  1: "Karşılaştırıcı yapıda bool operator()(const std::string& a, const std::string& b) const fonksiyonunu aşırı yükleyin."
  2: "a.size() != b.size() ise boyutları, eşitse a < b sonucunu döndürün."
  3: "Bu teknik 'özel karşılaştırıcılı sıralı küme (custom comparator set)' olarak bilinir."
```

---

### cpp-easy-subvector-product-k

```yaml
id: cpp-easy-subvector-product-k
version: 1
language: cpp
engine: none
difficulty: easy
title: "Boyutu k olan bitişik alt dizilerin maksimum çarpımını bulma"
prompt: |
  n elemanlı pozitif tamsayılar vektöründe uzunluğu tam olarak k olan bitişik alt dizilerin maksimum çarpımını kayan pencereyle hesaplayan `long long max_sub_product_k(const std::vector<int>& vec, size_t k)` fonksiyonunu yazın. n dizi boyutu ve k pencere boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "k > n durumunda 0 dönmelidir"
expected:
  time: { max_sub_product_k: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "İlk k elemanın çarpımı hesaplanıp sonraki adımlarda kayan pencere bölme/çarpma yapılmış mı?"
  - "64-bit çarpım kullanılmış mı?"
reference_solution_path: private/solutions/cpp-easy-subvector-product-k.cpp
hint_ladder:
  1: "İlk k elemanın çarpımını hesaplayarak pencereyi başlatın."
  2: "Her kaydırmada yeni elemanı çarpıp pencereden çıkan elemana bölerek maksimumu güncelleyin."
  3: "Bu algoritma 'kayan pencere ile alt dizi çarpımı (sliding window product)' olarak bilinir."
```

---

### cpp-easy-detect-duplicate-hash

```yaml
id: cpp-easy-detect-duplicate-hash
version: 1
language: cpp
engine: none
difficulty: easy
title: "Dizide mükerrer eleman olup olmadığını karma kümesiyle denetleme"
prompt: |
  n elemanlı bir tamsayı vektöründe herhangi bir elemanın birden fazla kez geçip geçmediğini std::unordered_set kullanarak O(n) sürede denetleyen `bool has_duplicates(const std::vector<int>& vec)` fonksiyonunu yazın. n vektörün eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Mükerrer eleman görüldüğü anda erken dönülmelidir"
expected:
  time: { has_duplicates: "n" }
  space: "n"
concept_tags: [hash-map, data-structures]
checklist_extra:
  - "Her eleman kümeye eklenirken insert dönüşü kontrol edilmiş mi?"
  - "İlk mükerrer elemanda erken çıkış yapılmış mı?"
reference_solution_path: private/solutions/cpp-easy-detect-duplicate-hash.cpp
hint_ladder:
  1: "Boş bir std::unordered_set<int> açın."
  2: "Elemanları gezerken !seen.insert(x).second olduğu an mükerrer eleman bulmuş olarak true dönün."
  3: "Bu algoritma 'karma kümesi ile mükerrerlik denetimi (hash set duplicate check)' olarak bilinir."
```

---

### cpp-easy-top-k-frequent-basic

```yaml
id: cpp-easy-top-k-frequent-basic
version: 1
language: cpp
engine: none
difficulty: easy
title: "Dizide en sık geçen k adet elemanı bulma"
prompt: |
  n elemanlı bir tamsayı vektöründe en yüksek frekansa sahip k adet elemanı karma haritası ve sıralama kullanarak bulan `std::vector<int> top_k_frequent(const std::vector<int>& vec, size_t k)` fonksiyonunu yazın. n vektörün boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n log n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "k elemanlı vektör dönmelidir"
expected:
  time: { top_k_frequent: "n log n" }
  space: "n"
concept_tags: [hash-map, data-structures]
checklist_extra:
  - "Eleman frekansları std::unordered_map ile sayılmış mı?"
  - "Frekanslara göre sıralama yapılıp ilk k eleman seçilmiş mi?"
reference_solution_path: private/solutions/cpp-easy-top-k-frequent-basic.cpp
hint_ladder:
  1: "Önce her sayının geçiş sıklığını bir karma haritasında biriktirin."
  2: "Haritadaki (sayı, frekans) çiftlerini bir vektöre aktarıp frekansa göre azalan sırada sıralayın ve ilk k sayıyı döndürün."
  3: "Bu algoritma 'en sık geçen elemanları bulma (top k frequent elements)' olarak bilinir."
```

---

### cpp-easy-string-compression-rle

```yaml
id: cpp-easy-string-compression-rle
version: 1
language: cpp
engine: none
difficulty: easy
title: "Karakter ve sayı çiftleriyle basit metin sıkıştırma"
prompt: |
  Metin görünümündeki ardışık tekrarlayan karakterleri harf ve tekrar sayısı biçiminde (ör. 'aaabb' -> 'a3b2') std::string olarak sıkıştıran `std::string compress_string(std::string_view str)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "str boşsa boş dizgi dönmelidir"
expected:
  time: { compress_string: "n" }
  space: "n"
concept_tags: [strings, performance]
checklist_extra:
  - "Ardışık karakter sayımı tek geçişte yapılmış mı?"
  - "std::to_string ile sayılar metne eklenmiş mi?"
reference_solution_path: private/solutions/cpp-easy-string-compression-rle.cpp
hint_ladder:
  1: "Metni tararken mevcut karakter değişene kadar sayacı artırın."
  2: "Karakter değiştiğinde harfi ve sayacı sonuç metnine ekleyip sayacı 1 yapın."
  3: "Bu sıkıştırma yöntemi 'çalışma uzunluğu kodlaması (run length compression)' olarak bilinir."
```

---

### cpp-easy-safe-downcast-dyn

```yaml
id: cpp-easy-safe-downcast-dyn
version: 1
language: cpp
engine: none
difficulty: easy
title: "Polimorfik hiyerarşide güvenli dinamik tür dönüşümü"
prompt: |
  Temel sınıf Base göstericisini türetilmiş Derived sınıf göstericisine dynamic_cast kullanarak güvenle dönüştüren, geçersizse nullptr dönen `Derived* try_downcast(Base* b)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "dynamic_cast kullanılmalıdır"
expected:
  time: { try_downcast: "1" }
  space: "1"
concept_tags: [ownership, edge-cases]
checklist_extra:
  - "Base sınıfının en az bir sanal (virtual) fonksiyona sahip olduğu gözetilmiş mi?"
  - "Dönüş nullptr güvenliğiyle kontrol edilmiş mi?"
reference_solution_path: private/solutions/cpp-easy-safe-downcast-dyn.cpp
hint_ladder:
  1: "dynamic_cast<Derived*>(b) çağrısı yapın."
  2: "Çalışma zamanı tür bilgisi (RTTI) nesnenin gerçekten Derived türünde olduğunu doğrularsa geçerli gösterici, aksi halde nullptr dönecektir."
  3: "Bu dönüşüm 'güvenli aşağı doğru tür dönüşümü (safe downcasting)' olarak bilinir."
```

---

### cpp-easy-scoped-timer-raii

```yaml
id: cpp-easy-scoped-timer-raii
version: 1
language: cpp
engine: none
difficulty: easy
title: "Yapıcıda başlayıp yıkıcıda süreyi kaydeden süre ölçer"
prompt: |
  Oluşturulduğu anda std::chrono::steady_clock ile zamanı başlatan ve kapsamdan çıktığında yıkıcısında geçen milisaniyeyi sağlanan referansa yazan `class ScopedTimer` RAII sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "steady_clock kullanılmalıdır"
expected:
  time: { ScopedTimer: "1" }
  space: "1"
concept_tags: [raii, performance]
checklist_extra:
  - "steady_clock kullanılarak sistem saati değişikliklerinden etkilenme önlenmiş mi?"
  - "Yıkıcıda süre hesaplanıp referansa yazılmış mı?"
reference_solution_path: private/solutions/cpp-easy-scoped-timer-raii.cpp
hint_ladder:
  1: "Yapıcıda start_time_ = std::chrono::steady_clock::now() zamanını kaydedin."
  2: "Yıkıcıda elapsed süreyi duration_cast ile milisaniyeye çevirip çıktı referansına atayın."
  3: "Bu RAII deseni 'kapsam tabanlı süre ölçer (scoped timer)' olarak bilinir."
```

---

### cpp-easy-mutex-lock-guard

```yaml
id: cpp-easy-mutex-lock-guard
version: 1
language: cpp
engine: none
difficulty: easy
title: "Kritik bölgeyi RAII kilit koruyucusu ile senkronize etme"
prompt: |
  Birden fazla iş parçacığının eriştiği counter tamsayısını std::lock_guard kullanarak istisna güvenli biçimde 1 artıran `void thread_safe_increment(int& counter, std::mutex& mtx)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "std::lock_guard kullanılmalıdır"
expected:
  time: { thread_safe_increment: "1" }
  space: "1"
concept_tags: [concurrency, data-race]
checklist_extra:
  - "std::lock_guard<std::mutex> ile kilit edinilmiş mi?"
  - "Kapsam sonunda kilit otomatik serbest kalıyor mu?"
reference_solution_path: private/solutions/cpp-easy-mutex-lock-guard.cpp
hint_ladder:
  1: "Fonksiyon başında std::lock_guard<std::mutex> lock(mtx); satırını çalıştırın."
  2: "Kritik bölgedeki counter++ işlemi tamamlandığında kilit kapsam çıkışında otomatik açılacaktır."
  3: "Bu eşzamanlılık deseni 'RAII kilit koruyucusu (scoped lock guard)' olarak bilinir."
```

---

### cpp-easy-atomic-flag-spinlock

```yaml
id: cpp-easy-atomic-flag-spinlock
version: 1
language: cpp
engine: none
difficulty: easy
title: "Atomik bayrak kullanarak döner kilit tasarlama"
prompt: |
  std::atomic_flag kullanarak test_and_set ve clear işlemleriyle çalışan temel bir kullanıcı alanı döner kilidi gerçekleştiren `class SpinLock` sınıfını yazın. lock() ve unlock() metotları bulunmalıdır.
constraints:
  - "Zaman karmaşıklığı kilitlemede O(1) döngü olmalı"
  - "Ek bellek O(1) olmalı"
  - "std::memory_order kullanılmalıdır"
expected:
  time: { SpinLock: "1" }
  space: "1"
concept_tags: [concurrency, data-race]
checklist_extra:
  - "lock() metodunda test_and_set döngüyle beklenmiş mi?"
  - "unlock() metodunda clear çağrılmış mı?"
reference_solution_path: private/solutions/cpp-easy-atomic-flag-spinlock.cpp
hint_ladder:
  1: "lock() içinde while (flag_.test_and_set(std::memory_order_acquire)) döngüsü kurun."
  2: "unlock() içinde flag_.clear(std::memory_order_release) ile kilidi açın."
  3: "Bu düşük seviyeli senkronizasyon aracı 'döner kilit (spinlock)' olarak bilinir."
```

---

### cpp-easy-thread-safe-counter

```yaml
id: cpp-easy-thread-safe-counter
version: 1
language: cpp
engine: none
difficulty: easy
title: "Atomik tamsayı kullanarak sayaç oluşturma"
prompt: |
  Kilit kullanmadan std::atomic<long long> ile iş parçacığı güvenli artırma, azaltma ve değer okuma operasyonları sunan `class ThreadSafeCounter` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "fetch_add ve fetch_sub kullanılmalıdır"
expected:
  time: { ThreadSafeCounter: "1" }
  space: "1"
concept_tags: [concurrency, performance]
checklist_extra:
  - "std::atomic türü kullanılarak veri yarışı engellenmiş mi?"
  - "Bellek sıralaması doğru belirtilmiş mi?"
reference_solution_path: private/solutions/cpp-easy-thread-safe-counter.cpp
hint_ladder:
  1: "Dahili sayaç değişkenini std::atomic<long long> olarak tutun."
  2: "increment() için fetch_add(1), decrement() için fetch_sub(1) çağrıları yapın."
  3: "Bu eşzamanlılık yapısı 'atomik sayaç (atomic counter)' olarak bilinir."
```

---

### cpp-easy-rotate-vector-k

```yaml
id: cpp-easy-rotate-vector-k
version: 1
language: cpp
engine: none
difficulty: easy
title: "Vektörü k adım sağa döndürme"
prompt: |
  n elemanlı bir tamsayı vektörünün elemanlarını k adım sağa dairesel döndüren `void rotate_right(std::vector<int>& vec, size_t k)` fonksiyonunu yazın. n vektörün boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "k = k % n normalizasyonu yapılmalıdır"
expected:
  time: { rotate_right: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "k = k % n ile gereksiz turlar elenmiş mi?"
  - "std::rotate ile O(n) sürede yerinde döndürülmüş mü?"
reference_solution_path: private/solutions/cpp-easy-rotate-vector-k.cpp
hint_ladder:
  1: "k değerini vec.size() modülüne indirgeyin."
  2: "std::rotate(vec.rbegin(), vec.rbegin() + k, vec.rend()) ile sağa döndürmeyi gerçekleştirin."
  3: "Bu işlem 'vektörü k adım sağa döndürme (rotate right by k)' olarak bilinir."
```

---

### cpp-easy-longest-continuous-ones

```yaml
id: cpp-easy-longest-continuous-ones
version: 1
language: cpp
engine: none
difficulty: easy
title: "İkilik dizide en uzun ardışık 1 dizilimini bulma"
prompt: |
  Yalnızca 0 ve 1 içeren n elemanlı bir tamsayı vektöründeki en uzun ardışık 1'lerin sayısını hesaplayan `size_t longest_ones(const std::vector<int>& vec)` fonksiyonunu yazın. n vektörün eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "const referans kullanılmalıdır"
expected:
  time: { longest_ones: "n" }
  space: "1"
concept_tags: [data-structures, const-correctness]
checklist_extra:
  - "1 görüldükçe sayaç artırılıp 0'da sıfırlanmış mı?"
  - "Maksimum sayaç her adımda güncellenmiş mi?"
reference_solution_path: private/solutions/cpp-easy-longest-continuous-ones.cpp
hint_ladder:
  1: "Mevcut 1 sayısını ve görülen maksimum sayıyı iki değişkende takip edin."
  2: "1 gördükçe sayacı artırıp maksimumu güncelleyin; 0 gördükçe sayacı sıfırlayın."
  3: "Bu algoritma 'ardışık birlerin maksimum uzunluğu (longest consecutive ones)' olarak bilinir."
```

---

### cpp-easy-move-only-task

```yaml
id: cpp-easy-move-only-task
version: 1
language: cpp
engine: none
difficulty: easy
title: "Kopyalanamayan yalnızca taşınabilen görev nesnesi"
prompt: |
  Kopya yapıcı ve kopya atama operatörleri silinmiş (= delete), ancak taşıma yapıcı ve taşıma ataması varsayılan (= default) bildirilmiş `class MoveOnlyTask` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Kopya operasyonları açıkça silinmelidir"
expected:
  time: { MoveOnlyTask: "1" }
  space: "1"
concept_tags: [move-semantics, ownership]
checklist_extra:
  - "MoveOnlyTask(const MoveOnlyTask&) = delete bildirilmiş mi?"
  - "Taşıma işlemleri noexcept olarak kullanılabilir mi?"
reference_solution_path: private/solutions/cpp-easy-move-only-task.cpp
hint_ladder:
  1: "Kopya yapıcıyı ve kopya atama operatörünü = delete ile devre dışı bırakın."
  2: "Taşıma yapıcıyı MoveOnlyTask(MoveOnlyTask&&) = default ile açık tutun."
  3: "Bu C++ kalıbı 'yalnızca taşınabilir tür (move-only type)' olarak bilinir."
```

---

### cpp-easy-string-token-view

```yaml
id: cpp-easy-string-token-view
version: 1
language: cpp
engine: none
difficulty: easy
title: "String_view ile sıfır kopyalı dizgi parçalayıcı"
prompt: |
  Metin görünümünü delim karakterine göre parçalayarak her bir parçayı std::string_view olarak std::vector içinde döndüren `std::vector<std::string_view> tokenize_view(std::string_view text, char delim)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(k) olmalı (k parça sayısı)"
  - "Sıfır karakter kopyalaması yapılmalıdır"
expected:
  time: { tokenize_view: "n" }
  space: "k"
concept_tags: [strings, copies]
checklist_extra:
  - "std::string_view::substr ile sıfır bellek kopyalaması yapılmış mı?"
  - "Ardışık ayraçlar doğru ele alınmış mı?"
reference_solution_path: private/solutions/cpp-easy-string-token-view.cpp
hint_ladder:
  1: "std::string_view::find ile ayraç karakterlerini bulun."
  2: "Her bulunan aralık için text.substr(start, len) alt görünümünü vektöre ekleyin."
  3: "Bu teknik 'sıfır kopyalı metin parçalama (zero-copy string view tokenization)' olarak bilinir."
```

---

### cpp-easy-binary-tree-leaf-count

```yaml
id: cpp-easy-binary-tree-leaf-count
version: 1
language: cpp
engine: none
difficulty: easy
title: "Akıllı işaretçili ikili ağaçta yaprak düğüm sayısını hesaplama"
prompt: |
  std::unique_ptr ile yönetilen ikili ağaçta çocuğu olmayan tüm yaprak düğümlerin sayısını özyinelemeli olarak hesaplayan `size_t count_leaves(const std::unique_ptr<TreeNode>& root)` fonksiyonunu yazın. n ağaçtaki toplam düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek çağrı yığını için O(log n) olmalı"
  - "root nullptr ise 0 dönmelidir"
expected:
  time: { count_leaves: "n" }
  space: "log n"
concept_tags: [trees, smart-pointers]
checklist_extra:
  - "Hem sol hem sağ çocuğu nullptr olan düğümler 1 sayılmış mı?"
  - "unique_ptr const referansla alınmış mı?"
reference_solution_path: private/solutions/cpp-easy-binary-tree-leaf-count.cpp
hint_ladder:
  1: "Kök nullptr ise 0 dönün."
  2: "Sol ve sağ çocukların her ikisi de nullptr ise yaprak düğümdür, 1 dönün; aksi halde iki alt ağacın toplamını döndürün."
  3: "Bu algoritma 'ikili ağaçta yaprak sayımı (binary tree leaf counting)' olarak bilinir."
```

---

### cpp-easy-invert-binary-tree

```yaml
id: cpp-easy-invert-binary-tree
version: 1
language: cpp
engine: none
difficulty: easy
title: "İkili ağacın sol ve sağ alt dallarını yer değiştirme"
prompt: |
  std::unique_ptr ile yönetilen ikili bir ağacın tüm düğümlerinin sol ve sağ çocuklarını yerinde takas ederek ağacı aynalayan `void invert_tree(std::unique_ptr<TreeNode>& root)` fonksiyonunu yazın. n ağaçtaki düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek çağrı yığını için O(log n) olmalı"
  - "std::swap kullanılabilir"
expected:
  time: { invert_tree: "n" }
  space: "log n"
concept_tags: [trees, smart-pointers]
checklist_extra:
  - "Sol ve sağ unique_ptr işaretçileri std::swap ile takas edilmiş mi?"
  - "Özyineleme çocuk alt ağaçlara uygulanmış mı?"
reference_solution_path: private/solutions/cpp-easy-invert-binary-tree.cpp
hint_ladder:
  1: "Kök nullptr ise doğrudan dönün."
  2: "std::swap(root->left, root->right) ile iki çocuğu takas edip özyinelemeli olarak çocukları çağırın."
  3: "Bu algoritma 'ikili ağacı tersine çevirme (invert binary tree)' olarak bilinir."
```

---

### cpp-easy-is-same-tree

```yaml
id: cpp-easy-is-same-tree
version: 1
language: cpp
engine: none
difficulty: easy
title: "İki ikili ağacın yapısal ve değer eşitliğini sınama"
prompt: |
  İki ikili ağacın hem yapısal olarak özdeş hem de karşılık gelen tüm düğüm değerlerinin eşit olup olmadığını denetleyen `bool are_trees_identical(const TreeNode* t1, const TreeNode* t2)` fonksiyonunu yazın. n ağaçlardaki düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek çağrı yığını için O(log n) olmalı"
  - "Her iki gösterici nullptr olduğunda true dönmelidir"
expected:
  time: { are_trees_identical: "n" }
  space: "log n"
concept_tags: [trees, const-correctness]
checklist_extra:
  - "Biri nullptr diğeri dolu olduğunda false dönülmüş mü?"
  - "Düğüm değerleri ve sol/sağ alt ağaçlar özyinelemeli test edilmiş mi?"
reference_solution_path: private/solutions/cpp-easy-is-same-tree.cpp
hint_ladder:
  1: "Her iki gösterici de nullptr ise true dönün."
  2: "Biri nullptr ise veya değerleri uyuşmuyorsa false dönün; sol ve sağ alt ağaçları özyinelemeli kıyaslayın."
  3: "Bu algoritma 'özdeş ikili ağaç kontrolü (identical binary trees)' olarak bilinir."
```

---

### cpp-easy-vector-capacity-shrink

```yaml
id: cpp-easy-vector-capacity-shrink
version: 1
language: cpp
engine: none
difficulty: easy
title: "Vektör kapasitesini boyutuna daraltma"
prompt: |
  Eleman silme işlemlerinden sonra gereksiz bellek tutan bir tamsayı vektörünün kapasitesini tam olarak eleman sayısına indiren `void shrink_capacity(std::vector<int>& vec)` fonksiyonunu yazın. n vektörün eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "shrink_to_fit kullanılmalıdır"
expected:
  time: { shrink_capacity: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "vec.shrink_to_fit() çağrılmış mı?"
  - "Kapasite fazlalığı sisteme iade edilmiş mi?"
reference_solution_path: private/solutions/cpp-easy-vector-capacity-shrink.cpp
hint_ladder:
  1: "vec.shrink_to_fit() fonksiyonunu çağırın."
  2: "Bu çağrı çalışma zamanına kapasiteyi mevcut boyutla eşitleme talebi ileterek kullanılmayan belleği serbest bırakır."
  3: "Bu optimizasyon 'vektör kapasitesini daraltma (shrink to fit)' olarak bilinir."
```

---


---

## 3. Orta (Medium) — 50 Soru

---

### cpp-medium-safe-erase-iteration

```yaml
id: cpp-medium-safe-erase-iteration
version: 1
language: cpp
engine: none
difficulty: medium
title: "Döngü sırasında koşula uyan elemanları güvenle silme"
prompt: |
  n elemanlı bir tamsayı vektörünü gezerken belirli bir koşulu sağlayan çift elemanları iterator geçersizleşmesine (invalidation) düşmeden silen `void safe_erase_even(std::vector<int>& vec)` fonksiyonunu yazın. n vektörün boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Dönen iterator ile döngü ilerletilmelidir"
expected:
  time: { safe_erase_even: "n" }
  space: "1"
concept_tags: [iterator-invalidation, data-structures]
checklist_extra:
  - "it = vec.erase(it) dönüş değeri kullanılarak iterator güncellenmiş mi?"
  - "Silinmeyen durumlarda ++it doğru yapılmış mı?"
reference_solution_path: private/solutions/cpp-medium-safe-erase-iteration.cpp
hint_ladder:
  1: "vec.erase(it) silinen elemanın bir sonraki geçerli iteratorünü döndürür."
  2: "Silme yapıldığında dönen iteratorü atayın, silme yapılmadığında iteratorü bir artırın ya da std::erase_if kullanın."
  3: "Bu yöntem 'güvenli iterator döngü silmesi (safe iterator erase)' olarak bilinir."
```

---

### cpp-medium-binary-tree-unique-ptr

```yaml
id: cpp-medium-binary-tree-unique-ptr
version: 1
language: cpp
engine: none
difficulty: medium
title: "Benzersiz akıllı işaretçi ile ikili arama ağacına düğüm ekleme"
prompt: |
  Düğümleri std::unique_ptr ile sahiplenilen bir ikili arama ağacına yeni bir tamsayı ekleyen `void bst_insert(std::unique_ptr<BSTNode>& root, int val)` fonksiyonunu yazın. n ağaçtaki düğüm sayısıdır.
constraints:
  - "Dengeli ağaçta zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek çağrı yığını için O(log n) olmalı"
  - "Çıplak gösterici veya delete kullanılmamalıdır"
expected:
  time: { bst_insert: "log n" }
  space: "log n"
concept_tags: [trees, smart-pointers]
checklist_extra:
  - "std::make_unique kullanılmış mı?"
  - "unique_ptr referansı & üzerinden özyineleme yapılmış mı?"
reference_solution_path: private/solutions/cpp-medium-binary-tree-unique-ptr.cpp
hint_ladder:
  1: "root nullptr ise std::make_unique<BSTNode>(val) ile yeni düğüm oluşturun."
  2: "val < root->val ise root->left referansına, aksi halde root->right referansına özyinelemeli dallanın."
  3: "Bu algoritma 'akıllı işaretçili ikili arama ağacı ekleme işlemi (smart pointer BST insertion)' olarak bilinir."
```

---

### cpp-medium-weak-ptr-cache

```yaml
id: cpp-medium-weak-ptr-cache
version: 1
language: cpp
engine: none
difficulty: medium
title: "Zayıf işaretçi kullanarak döngüsel başvuruları önleyen önbellek tablosu"
prompt: |
  Daha önce yüklenmiş kaynakları std::weak_ptr olarak saklayan ve talep edildiğinde lock() ile kaynağın yaşayıp yaşamadığını denetleyen `class SharedResourceCache` önbellek sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı arama için O(1) ortalama olmalı"
  - "Ek bellek O(n) olmalı"
  - "Süresi dolmuş weak_ptr temizlenmelidir"
expected:
  time: { SharedResourceCache: "1" }
  space: "n"
concept_tags: [smart-pointers, cyclic-reference]
checklist_extra:
  - "weak_ptr.lock() ile shared_ptr elde edilmiş mi?"
  - "Kaynağın ömrü dolmuşsa yeni nesne tahsis edilmiş mi?"
reference_solution_path: private/solutions/cpp-medium-weak-ptr-cache.cpp
hint_ladder:
  1: "Karma tablosunda anahtar ile std::weak_ptr eşleşmesi tutun."
  2: "Arama yaparken wp.lock() çağırın; null dönerse nesne silinmiştir, yeni oluşturup paylaştırın."
  3: "Bu önbellekleme deseni 'zayıf işaretçili nesne önbelleği (weak pointer cache)' olarak bilinir."
```

---

### cpp-medium-rule-of-five-string

```yaml
id: cpp-medium-rule-of-five-string
version: 1
language: cpp
engine: none
difficulty: medium
title: "Dinamik metin yöneten sınıfta 5 kuralını uygulama"
prompt: |
  Kendi dinamik karakter dizisini yöneten `class CustomString` sınıfında Rule of Five kuralına tam uyumlu yıkıcı, kopya yapıcı, taşıma yapıcı, kopya atama ve taşıma atama operatörlerini noexcept niteleyicileriyle yazın.
constraints:
  - "Zaman karmaşıklığı kopyalamada O(n), taşımada O(1) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Taşıma işlemleri noexcept olmalıdır"
expected:
  time: { CustomString: "n" }
  space: "n"
concept_tags: [rule-of-five, move-semantics]
checklist_extra:
  - "Taşıma operatörlerinde kaynak nesne geçerli ve boş duruma getirilmiş mi?"
  - "Kendine atama if (this != &other) denetlenmiş mi?"
reference_solution_path: private/solutions/cpp-medium-rule-of-five-string.cpp
hint_ladder:
  1: "Kopya işlemlerinde derin kopyalama için yeni bellek ayırın."
  2: "Taşıma işlemlerinde diğer nesnenin bellek işaretçisini çalıp onu nullptr yaparak noexcept garantisi sağlayın."
  3: "Bu C++ kaynak yönetim kuralı 'beş kuralı (Rule of Five)' olarak bilinir."
```

---

### cpp-medium-copy-and-swap-idiom

```yaml
id: cpp-medium-copy-and-swap-idiom
version: 1
language: cpp
engine: none
difficulty: medium
title: "Güçlü istisna güvenliği için kopyala-ve-takas deyimini uygulama"
prompt: |
  Dinamik dizi tutan bir sınıfta kopya atama operatörünü değerle alma (pass-by-value) ve std::swap kullanarak istisna güvenli tasarlayan `CustomArray& operator=(CustomArray other)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "noexcept takas fonksiyonu kullanılmalıdır"
expected:
  time: { operator=: "n" }
  space: "n"
concept_tags: [rule-of-five, raii]
checklist_extra:
  - "Parametre değerle alınarak (pass-by-value) kopya otomatik oluşturulmuş mı?"
  - "std::swap ile üyeler güvenle takas edilmiş mi?"
reference_solution_path: private/solutions/cpp-medium-copy-and-swap-idiom.cpp
hint_ladder:
  1: "Atama operatörünün parametresini değerle (by-value) alarak kopyalama aşamasında hata olursa mevcut nesnenin bozulmasını önleyin."
  2: "Oluşan geçici kopya ile mevcut nesnenin üyelerini swap edin; eski kaynaklar geçici nesnenin yıkıcısında temizlensin."
  3: "Bu tasarım 'kopyala ve takas deyimi (copy-and-swap idiom)' olarak bilinir."
```

---

### cpp-medium-custom-iterator-range

```yaml
id: cpp-medium-custom-iterator-range
version: 1
language: cpp
engine: none
difficulty: medium
title: "Kendi özel veri yapısı için ileri yönlü iterator tasarlama"
prompt: |
  Bir tamsayı aralığı [first, last) üzerinde döngü kurmayı sağlayan ve operator*, operator++, operator!= fonksiyonlarına sahip `class RangeView` sınıfı ve iç iteratorünü yazın.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "STL iterator standartlarına uyulmalıdır"
expected:
  time: { RangeView: "n" }
  space: "1"
concept_tags: [data-structures, const-correctness]
checklist_extra:
  - "begin() ve end() metotları doğru iterator döndürüyor mu?"
  - "operator++ ön ek ve son ek doğru tanımlanmış mı?"
reference_solution_path: private/solutions/cpp-medium-custom-iterator-range.cpp
hint_ladder:
  1: "Dahili bir Iterator sınıfı tanımlayıp *it, ++it ve it1 != it2 operatörlerini aşırı yükleyin."
  2: "begin() ile başlangıç değerini, end() ile bitiş sınırını temsil eden iteratorleri döndürün."
  3: "Bu tasarım 'özel aralık iteratorü (custom range iterator)' olarak bilinir."
```

---

### cpp-medium-lru-cache-sync

```yaml
id: cpp-medium-lru-cache-sync
version: 1
language: cpp
engine: none
difficulty: medium
title: "Çift yönlü liste ve karma haritasını senkron tutan LRU önbellek"
prompt: |
  Kapasitesi sınırlandırılmış bir önbellekte get ve put operasyonlarını std::list ve std::unordered_map kullanarak O(1) sürede gerçekleştiren `class SimpleLRUCache` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı her işlem için O(1) olmalı"
  - "Ek bellek O(capacity) olmalı"
  - "Liste ve harita her işlemde senkron tutulmalıdır"
expected:
  time: { SimpleLRUCache: "1" }
  space: "1"
concept_tags: [lru-cache, hash-map]
checklist_extra:
  - "Erişilen düğüm std::list::splice ile başa taşınmış mı?"
  - "Kapasite dolduğunda kuyruktaki en eski eleman haritadan ve listeden silinmiş mi?"
reference_solution_path: private/solutions/cpp-medium-lru-cache-sync.cpp
hint_ladder:
  1: "Elemanları kullanım sırasına göre bir std::list içinde tutun."
  2: "std::unordered_map içinde anahtar ile liste iteratorünü eşleştirerek her erişimde düğümü listenin en başına splice ile taşıyın."
  3: "Bu önbellek veri yapısı 'en az son kullanılan önbellek senkronizasyonu (LRU cache synchronization)' olarak bilinir."
```

---

### cpp-medium-longest-substring-distinct

```yaml
id: cpp-medium-longest-substring-distinct
version: 1
language: cpp
engine: none
difficulty: medium
title: "Tekrarlayan karakter içermeyen en uzun alt dizgiyi kayan pencereyle bulma"
prompt: |
  Verilen bir metin görünümünde tekrarlayan karakter içermeyen en uzun kesintisiz alt dizginin uzunluğunu kayan pencereyle bulan `size_t length_of_longest_unique_substring(std::string_view s)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) (256 elemanlı son görülme tablosu) olmalı"
  - "string_view kullanılmalıdır"
expected:
  time: { length_of_longest_unique_substring: "n" }
  space: "1"
concept_tags: [strings, performance]
checklist_extra:
  - "Karakterin son indeksi tabloda saklanmış mı?"
  - "Sol işaretçi sadece ileriye doğru hareket ettirilmiş mi?"
reference_solution_path: private/solutions/cpp-medium-longest-substring-distinct.cpp
hint_ladder:
  1: "Her karakterin en son görüldüğü indeksi bir dizide tutun."
  2: "Karakter tekrarlandığında sol pencere sınırını karakterin son indeksinin bir sağına çekin ve pencere genişliğini güncelleyin."
  3: "Bu algoritma 'kayan pencere ile benzersiz alt metin analizi (sliding window unique substring)' olarak bilinir."
```

---

### cpp-medium-three-sum-target

```yaml
id: cpp-medium-three-sum-target
version: 1
language: cpp
engine: none
difficulty: medium
title: "Sıralı arama ve iki işaretçiyle toplamı sıfır olan üçlüleri bulma"
prompt: |
  n elemanlı bir tamsayı vektöründe toplamları sıfır olan tüm benzersiz [a, b, c] üçlülerini bulan `std::vector<std::vector<int>> three_sum(std::vector<int>& nums)` fonksiyonunu yazın. n vektörün boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n^2) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Yinelenen üçlüler atlanmalıdır"
expected:
  time: { three_sum: "n^2" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Dizi sıralandıktan sonra ardışık yinelenen elemanlar atlanmış mı?"
  - "İki işaretçi yöntemiyle O(n^2) sağlanmış mı?"
reference_solution_path: private/solutions/cpp-medium-three-sum-target.cpp
hint_ladder:
  1: "Vektörü std::sort ile küçükten büyüğe sıralayın."
  2: "İlk elemanı sabitleyip kalan aralıkta iki işaretçi ile toplamı sıfır yapan çiftleri ararken mükerrer değerleri atlayın."
  3: "Bu klasik problem 'üçlü toplam algoritması (three sum algorithm)' olarak bilinir."
```

---

### cpp-medium-container-max-water

```yaml
id: cpp-medium-container-max-water
version: 1
language: cpp
engine: none
difficulty: medium
title: "İki sütun arasında tutulan azami su alanını hesaplama"
prompt: |
  n elemanlı yükseklik vektöründe en fazla su tutabilecek iki sütun arasındaki alanı iki işaretçiyle hesaplayan `long long max_water(const std::vector<int>& heights)` fonksiyonunu yazın. n eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) tek geçiş olmalı"
  - "Ek bellek O(1) olmalı"
  - "const referans kullanılmalıdır"
expected:
  time: { max_water: "n" }
  space: "1"
concept_tags: [data-structures, const-correctness]
checklist_extra:
  - "Kısa olan sütunun işaretçisi içeri kaydırılmış mı?"
  - "Maksimum alan long long olarak hesaplanmış mı?"
reference_solution_path: private/solutions/cpp-medium-container-max-water.cpp
hint_ladder:
  1: "Sol ve sağ uçlara iki işaretçi koyup alanı hesaplayın."
  2: "Kısa olan sütunun işaretçisini içeri kaydırarak daha yüksek sütunlar arayın."
  3: "Bu açgözlü yöntem 'çift işaretçi ile maksimum su alanı (container with most water)' olarak bilinir."
```

---

### cpp-medium-trapping-rain-water

```yaml
id: cpp-medium-trapping-rain-water
version: 1
language: cpp
engine: none
difficulty: medium
title: "Yükseklik haritasında biriken yağmur suyunu iki işaretçiyle hesaplama"
prompt: |
  n elemanlı negatif olmayan yükseklik vektörünün tutabileceği toplam yağmur suyu hacmini O(n) zaman ve O(1) alanda hesaplayan `long long trap_water(const std::vector<int>& heights)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "İki işaretçi ve sol/sağ tepe takibi yapılmalı"
expected:
  time: { trap_water: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "left_max ve right_max doğru güncellenmiş mi?"
  - "Su miktarı her adımda negatif olmayacak biçimde toplanmış mı?"
reference_solution_path: private/solutions/cpp-medium-trapping-rain-water.cpp
hint_ladder:
  1: "İki uçtan ortaya doğru ilerleyen iki işaretçi ve tepe yüksekliklerini tutun."
  2: "Daha alçak tepeye sahip taraftan su miktarını ekleyip o işaretçiyi ilerletin."
  3: "Bu algoritma 'yağmur suyu tutma algoritması (trapping rain water two-pointer)' olarak bilinir."
```

---

### cpp-medium-kadane-subarray

```yaml
id: cpp-medium-kadane-subarray
version: 1
language: cpp
engine: none
difficulty: medium
title: "Bitişik alt dizi maksimum toplamını bulma (C++)"
prompt: |
  n elemanlı tamsayı vektöründe toplamı en büyük olan bitişik alt dizinin toplamını Kadane algoritmasıyla bulan `long long max_subarray(const std::vector<int>& nums)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) tek geçiş olmalı"
  - "Ek bellek O(1) olmalı"
  - "Tümü negatif diziler doğru yönetilmelidir"
expected:
  time: { max_subarray: "n" }
  space: "1"
concept_tags: [data-structures, const-correctness]
checklist_extra:
  - "Maksimum aday nums[0] ile başlatılmış mı?"
  - "Mevcut toplam negatif olduğunda sıfırlanmış mı?"
reference_solution_path: private/solutions/cpp-medium-kadane-subarray.cpp
hint_ladder:
  1: "Diziyi tararken o anki bitişik toplamı güncelleyin."
  2: "Toplam negatif olduğunda sıfırlayıp bir sonraki elemandan yeni dizi başlatın; maksimumu her adımda kaydedin."
  3: "Bu dinamik programlama tekniği 'Kadane maksimum alt dizi algoritması (Kadane's algorithm)' olarak bilinir."
```

---

### cpp-medium-binary-search-rotated

```yaml
id: cpp-medium-binary-search-rotated
version: 1
language: cpp
engine: none
difficulty: medium
title: "Döndürülmüş sıralı vektörde hedef değeri arama"
prompt: |
  Bilinmeyen bir noktadan döndürülmüş sıralı n elemanlı benzersiz tamsayı vektöründe target değerinin indeksini ikili aramayla bulan `int search_rotated(const std::vector<int>& nums, int target)` fonksiyonunu yazın. n vektörün eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Bulunamazsa -1 dönmelidir"
expected:
  time: { search_rotated: "log n" }
  space: "1"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "Sol veya sağ yarının sıralı olup olmadığı doğru belirlenmiş mi?"
  - "Hedefin sıralı aralıkta olup olmadığı test edilmiş mi?"
reference_solution_path: private/solutions/cpp-medium-binary-search-rotated.cpp
hint_ladder:
  1: "Her adımda ortadaki elemanı bulup sol ve sağ yarımlardan hangisinin sıralı olduğunu denetleyin."
  2: "Hedef değerin sıralı yarıda olup olmadığına bakarak arama aralığını yarıya daraltın."
  3: "Bu arama 'döndürülmüş dizide ikili arama (rotated array binary search)' olarak bilinir."
```

---

### cpp-medium-dutch-flag-partition

```yaml
id: cpp-medium-dutch-flag-partition
version: 1
language: cpp
engine: none
difficulty: medium
title: "Üç farklı değeri tek geçişte yerinde sıralama"
prompt: |
  Yalnızca 0, 1 ve 2 değerlerinden oluşan n elemanlı bir tamsayı vektörünü ek bellek ayırmadan yerinde sıralayan `void sort_colors(std::vector<int>& nums)` fonksiyonunu yazın. n vektör boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) tek geçiş olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "Üç işaretçi yöntemi kullanılmalıdır"
expected:
  time: { sort_colors: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "low, mid ve high işaretçileri doğru güncellenmiş mi?"
  - "std::swap ile yerinde değişim yapılmış mı?"
reference_solution_path: private/solutions/cpp-medium-dutch-flag-partition.cpp
hint_ladder:
  1: "low, mid ve high olmak üzere 3 indeks tutun."
  2: "nums[mid] == 0 ise low ile takas edin, 2 ise high ile takas edin, 1 ise mid'i ilerletin."
  3: "Bu algoritma 'üçlü bölme algoritması (Dutch national flag partition)' olarak bilinir."
```

---

### cpp-medium-group-anagrams-map

```yaml
id: cpp-medium-group-anagrams-map
version: 1
language: cpp
engine: none
difficulty: medium
title: "Karakter sayılarına göre anagram dizgileri kümeleme (C++)"
prompt: |
  n adet metin içeren dizgiler vektöründeki anagramları harf sıklığı anahtarıyla gruplayarak std::vector<std::vector<std::string>> içinde döndüren `std::vector<std::vector<std::string>> group_anagrams(const std::vector<std::string>& strs)` fonksiyonunu yazın. m ortalama sözcük uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(n) olmalı"
  - "std::unordered_map kullanılmalıdır"
expected:
  time: { group_anagrams: "n*m" }
  space: "n"
concept_tags: [hash-map, strings]
checklist_extra:
  - "Her dizginin sıralanmış hali veya 26 boyutlu harf frekansı anahtar yapılmış mı?"
  - "Gruplar sonuca aktarılmış mı?"
reference_solution_path: private/solutions/cpp-medium-group-anagrams-map.cpp
hint_ladder:
  1: "Her metnin sıralanmış kopyasını veya karakter frekansını anahtar olarak belirleyin."
  2: "std::unordered_map<std::string, std::vector<std::string>> içinde aynı anahtara sahip sözcükleri toplayın."
  3: "Bu kümeleme yöntemi 'karma haritası ile anagram gruplama (anagram grouping)' olarak bilinir."
```

---

### cpp-medium-product-except-self

```yaml
id: cpp-medium-product-except-self
version: 1
language: cpp
engine: none
difficulty: medium
title: "Kendisi hariç diğer elemanların çarpımı vektörünü üretme"
prompt: |
  n elemanlı tamsayı vektöründe her elemanın yerine diğer tüm elemanların çarpımını bölme operatörü (/) kullanmadan hesaplayan `std::vector<long long> product_except_self(const std::vector<int>& nums)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı (sonuç vektörü)"
  - "Bölme işlemi kesinlikle kullanılmamalıdır"
expected:
  time: { product_except_self: "n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Sol ve sağ önek çarpımları iki geçişte birleştirilmiş mi?"
  - "Bölme operatörü kullanılmamış mı?"
reference_solution_path: private/solutions/cpp-medium-product-except-self.cpp
hint_ladder:
  1: "İlk geçişte soldan gelen elemanların birikimli çarpımını sonuç dizisine yazın."
  2: "İkinci geçişte sağdan geriye gelerek sağdaki çarpımı bir değişkende tutup sonuçla çarpın."
  3: "Bu algoritma 'önek ve sonek çarpımları (prefix and suffix products)' olarak bilinir."
```

---

### cpp-medium-spiral-matrix-order

```yaml
id: cpp-medium-spiral-matrix-order
version: 1
language: cpp
engine: none
difficulty: medium
title: "Matris elemanlarını spiral sırada tek boyutlu vektöre aktarma"
prompt: |
  n x m boyutundaki bir tamsayı matrisinin elemanlarını dıştan içe doğru saat yönünde spiral sırada okuyarak tek boyutlu vektörde döndüren `std::vector<int> spiral_order(const std::vector<std::vector<int>>& matrix)` fonksiyonunu yazın. n satır ve m sütun sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(n * m) olmalı"
  - "Dört sınır değişkeni daraltılmalıdır"
expected:
  time: { spiral_order: "n*m" }
  space: "n*m"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "top, bottom, left, right sınırları doğru yönetilmiş mi?"
  - "Matris boş durumu kontrol edilmiş mi?"
reference_solution_path: private/solutions/cpp-medium-spiral-matrix-order.cpp
hint_ladder:
  1: "Dört kenar sınırını belirleyip sırasıyla sağa, aşağı, sola ve yukarı adımlarla matrisi tarayın."
  2: "Her kenar tamamlandığında ilgili sınırı bir birim içeriye daraltın."
  3: "Bu matris okuma düzeni 'spiral matris gezintisi (spiral matrix order)' olarak bilinir."
```

---

### cpp-medium-rotate-image-90

```yaml
id: cpp-medium-rotate-image-90
version: 1
language: cpp
engine: none
difficulty: medium
title: "Kare matrisi ek bellek ayırmadan saat yönünde 90 derece döndürme"
prompt: |
  n x n boyutundaki kare tamsayı matrisini yerinde saat yönünde 90 derece döndüren `void rotate_matrix(std::vector<std::vector<int>>& matrix)` fonksiyonunu yazın. n matris satır ve sütun boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n^2) olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "Önce devrik alma ardından satır ters çevirme uygulanmalıdır"
expected:
  time: { rotate_matrix: "n^2" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Köşegene göre devrik alma doğru yapılmış mı?"
  - "Her satır std::reverse ile ters çevrilmiş mi?"
reference_solution_path: private/solutions/cpp-medium-rotate-image-90.cpp
hint_ladder:
  1: "Önce matrisin asal köşegene göre devriğini (transpozunu) alın."
  2: "Ardından her bir satırı std::reverse ile yatay eksende ters çevirin."
  3: "Bu iki adımlı dönüşüm 'kare matrisi yerinde döndürme (in-place matrix rotation)' olarak bilinir."
```

---

### cpp-medium-set-matrix-zeroes

```yaml
id: cpp-medium-set-matrix-zeroes
version: 1
language: cpp
engine: none
difficulty: medium
title: "Sıfır içeren satır ve sütunları sabit ek bellekle sıfırlama (C++)"
prompt: |
  n x m boyutundaki tamsayı matrisinde sıfır bulunan hücrelerin tüm satır ve sütununu yerinde sıfırlayan `void set_zeroes(std::vector<std::vector<int>>& matrix)` fonksiyonunu yazın. Ek bellek O(1) olmalıdır. n satır ve m sütun adedidir.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "İlk satır ve sütun işaretçi olarak kullanılabilir"
expected:
  time: { set_zeroes: "n*m" }
  space: "1"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "İlk satır ve sütunun orijinal sıfır durumu ayrı bayraklarla saklanmış mı?"
  - "Sıfırlama içeriden dışarıya doğru mu yapılmış?"
reference_solution_path: private/solutions/cpp-medium-set-matrix-zeroes.cpp
hint_ladder:
  1: "İlk satır ve ilk sütunu sıfır işaretleme tablosu olarak kullanın."
  2: "İlk satır ve sütunun kendi sıfır olma durumunu iki boole değişkeninde tutarak matrisi güncelleyin."
  3: "Bu algoritma 'matris satır ve sütunlarını yerinde sıfırlama (set matrix zeroes)' olarak bilinir."
```

---

### cpp-medium-thread-pool-basic

```yaml
id: cpp-medium-thread-pool-basic
version: 1
language: cpp
engine: none
difficulty: medium
title: "Görev kuyruğu ve çalışan iş parçacıkları olan temel iş havuzu"
prompt: |
  Sabit sayıda iş parçacığı barındıran, görevleri std::queue<std::function<void()>> içinde toplayıp durum değişkeniyle iş parçacıklarına dağıtan `class SimpleThreadPool` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı görev eklemede O(1) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Yıkıcıda tüm iş parçacıkları güvenle sonlandırılmalıdır"
expected:
  time: { SimpleThreadPool: "1" }
  space: "n"
concept_tags: [concurrency, data-race]
checklist_extra:
  - "condition_variable ile iş parçacıkları uyandırılmış mı?"
  - "Yıkıcıda stop bayrağı çekilip join() çağrılmış mı?"
reference_solution_path: private/solutions/cpp-medium-thread-pool-basic.cpp
hint_ladder:
  1: "İş parçacıklarını bir vektörde, görevleri mutex korumalı bir kuyrukta saklayın."
  2: "condition_variable.notify_one() ile bekleyen iş parçacıklarını uyandırın ve kapanışta notify_all() çağırın."
  3: "Bu eşzamanlılık deseni 'iş parçacığı havuzu (thread pool pattern)' olarak bilinir."
```

---

### cpp-medium-blocking-queue-cv

```yaml
id: cpp-medium-blocking-queue-cv
version: 1
language: cpp
engine: none
difficulty: medium
title: "Durum değişkeni ile korunan iş parçacığı güvenli kuyruk"
prompt: |
  Maksimum kapasitesi olan, kuyruk doluyken eklemeyi ve boşken çekmeyi std::condition_variable ile bloklayan `class BlockingQueue` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı her işlem için O(1) olmalı"
  - "Ek bellek O(capacity) olmalı"
  - "Sahte uyanmalar (spurious wakeups) döngüyle önlenmelidir"
expected:
  time: { BlockingQueue: "1" }
  space: "1"
concept_tags: [concurrency, data-race]
checklist_extra:
  - "wait çağrıları while döngüsü veya yüklem (predicate) ile yapılmış mı?"
  - "push ve pop işlemlerinde bildirim yapılmış mı?"
reference_solution_path: private/solutions/cpp-medium-blocking-queue-cv.cpp
hint_ladder:
  1: "std::unique_lock<std::mutex> ile kuyruk kilidini edinin."
  2: "cv.wait(lock, [this]{ return !queue_.empty(); }) ile sahte uyanmaları engelleyerek elemanı çekin."
  3: "Bu senkronizasyon yapısı 'bloklayan kuyruk (blocking queue)' olarak bilinir."
```

---

### cpp-medium-read-write-lock-shared

```yaml
id: cpp-medium-read-write-lock-shared
version: 1
language: cpp
engine: none
difficulty: medium
title: "Paylaşılan okuma ve özel yazma kilitlerini yöneten sınıf"
prompt: |
  Aynı anda birden fazla okuyucuya izin veren, yazma anında ise tüm okuma ve yazmaları kilitleyen std::shared_mutex tabanlı `class ReadWriteLock` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "std::shared_lock ve std::unique_lock kullanılmalıdır"
expected:
  time: { ReadWriteLock: "1" }
  space: "1"
concept_tags: [concurrency, performance]
checklist_extra:
  - "Okuma işlemlerinde shared_lock kullanılmış mı?"
  - "Yazma işlemlerinde unique_lock kullanılmış mı?"
reference_solution_path: private/solutions/cpp-medium-read-write-lock-shared.cpp
hint_ladder:
  1: "std::shared_mutex nesnesini üye olarak tutun."
  2: "Okuma fonksiyonlarında std::shared_lock, yazma fonksiyonlarında std::unique_lock kullanarak kilit şemasını ayırın."
  3: "Bu eşzamanlılık aracı 'okuyucu-yazıcı kilidi (reader-writer lock)' olarak bilinir."
```

---

### cpp-medium-producer-consumer-sync

```yaml
id: cpp-medium-producer-consumer-sync
version: 1
language: cpp
engine: none
difficulty: medium
title: "Üretici ve tüketici iş parçacıklarını senkronize eden tampon"
prompt: |
  Üreticinin veri eklediği ve tüketicinin veri çektiği sınırlı dairesel tamponu iki condition_variable (not_full, not_empty) ile senkronize eden `class BoundedBuffer` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(capacity) olmalı"
  - "Kapasite aşımı önlenmelidir"
expected:
  time: { BoundedBuffer: "1" }
  space: "1"
concept_tags: [concurrency, data-race]
checklist_extra:
  - "İki ayrı durum değişkeni (not_full ve not_empty) kullanılmış mı?"
  - "Kritik bölge mutex ile korunmuş mu?"
reference_solution_path: private/solutions/cpp-medium-producer-consumer-sync.cpp
hint_ladder:
  1: "Tampon dolduğunda üreticiyi not_full üzerinde, boşken tüketiciyi not_empty üzerinde bekletin."
  2: "Her başarılı işlemde karşı tarafın durum değişkenine bildirim (notify_one) gönderin."
  3: "Bu klasik problem 'üretici-tüketici senkronizasyonu (producer-consumer synchronization)' olarak bilinir."
```

---

### cpp-medium-future-promise-channel

```yaml
id: cpp-medium-future-promise-channel
version: 1
language: cpp
engine: none
difficulty: medium
title: "Future ve promise ile iş parçacıkları arası tekil veri aktarımı"
prompt: |
  Arka planda çalışan bir iş parçacığının ürettiği tamsayı sonucunu std::promise üzerinden ana iş parçacığına iletip std::future::get() ile elde eden `void async_channel_send()` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "std::promise ve std::future kullanılmalıdır"
expected:
  time: { async_channel_send: "1" }
  space: "1"
concept_tags: [concurrency, move-semantics]
checklist_extra:
  - "std::promise taşıma semantiğiyle iş parçacığına aktarılmış mı?"
  - "get() çağrısı beklenen değeri almış mı?"
reference_solution_path: private/solutions/cpp-medium-future-promise-channel.cpp
hint_ladder:
  1: "Bir std::promise<int> nesnesi oluşturup get_future() ile geleceğini alın."
  2: "Promise nesnesini iş parçacığına taşıyıp set_value ile sonucu yazın ve future.get() ile okuyun."
  3: "Bu eşzamanlılık mekanizması 'söz ve gelecek kanalı (promise and future channel)' olarak bilinir."
```

---

### cpp-medium-topological-sort-dag

```yaml
id: cpp-medium-topological-sort-dag
version: 1
language: cpp
engine: none
difficulty: medium
title: "Yönlü döngüsüz çizgede giriş dereceleriyle topolojik sıralama"
prompt: |
  n düğümlü bir DAG'daki kenar listesini alarak giriş dereceleri (in-degree) ve kuyruk yardımıyla düğümlerin geçerli bir topolojik sıralamasını std::vector<int> olarak üreten `std::vector<int> topological_sort(size_t n, const std::vector<std::pair<int, int>>& edges)` fonksiyonunu yazın. Çizgede döngü varsa boş vektör dönmelidir. m kenar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n + m) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Döngü tespitinde boş vektör dönülmelidir"
expected:
  time: { topological_sort: "n + m" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Giriş derecesi 0 olan düğümler başlangıçta kuyruğa alınmış mı?"
  - "Sıralanan düğüm sayısı n değilse döngü saptanmış mı?"
reference_solution_path: private/solutions/cpp-medium-topological-sort-dag.cpp
hint_ladder:
  1: "Tüm düğümlerin giriş derecelerini hesaplayıp derecesi 0 olanları bir kuyruğa atın."
  2: "Kuyruktan düğüm çektikçe komşuların derecesini azaltıp sıfırlananları kuyruğa ekleyin."
  3: "Bu algoritma 'Kahn topolojik sıralama algoritması (Kahn's algorithm)' olarak bilinir."
```

---

### cpp-medium-dijkstra-min-heap

```yaml
id: cpp-medium-dijkstra-min-heap
version: 1
language: cpp
engine: none
difficulty: medium
title: "Öncelik kuyruğu ile ağırlıklı çizgede en kısa yol mesafelerini hesaplama"
prompt: |
  n düğümlü ve pozitif ağırlıklı kenarlara sahip bir çizgede src düğümünden tüm düğümlere en kısa mesafeleri std::priority_queue kullanarak hesaplayan `std::vector<int> dijkstra_shortest_paths(size_t n, const std::vector<std::tuple<int, int, int>>& edges, int src)` fonksiyonunu yazın. m kenar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(m log n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Min-heap kullanılmalıdır"
expected:
  time: { dijkstra_shortest_paths: "m log n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Mesafe vektörü sonsuzla başlatılmış mı?"
  - "Eski ve daha uzun yollar min-heap'ten çekildiğinde elenmiş mi?"
reference_solution_path: private/solutions/cpp-medium-dijkstra-min-heap.cpp
hint_ladder:
  1: "std::priority_queue<std::pair<int, int>, ..., std::greater<>> ile min-heap oluşturun."
  2: "En küçük mesafeli düğümü çekip komşularını gevşetin (relaxation) ve güncellenen mesafeleri kuyruğa ekleyin."
  3: "Bu algoritma 'Dijkstra en kısa yol algoritması (Dijkstra algorithm)' olarak bilinir."
```

---

### cpp-medium-course-schedule-cycle

```yaml
id: cpp-medium-course-schedule-cycle
version: 1
language: cpp
engine: none
difficulty: medium
title: "Önkoşul bağımlılıklarında döngü olup olmadığını DFS ile denetleme"
prompt: |
  num_courses adet ders ve önkoşul kenarları verildiğinde tüm derslerin tamamlanıp tamamlanamayacağını 3 renkli DFS durumlarıyla (ziyaret edilmedi, yığında, tamamlandı) denetleyen `bool can_finish_courses(int num_courses, const std::vector<std::pair<int, int>>& prerequisites)` fonksiyonunu yazın. n ders ve m önkoşul sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n + m) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Döngü tespitinde false dönmelidir"
expected:
  time: { can_finish_courses: "n + m" }
  space: "n"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "Döngü tespiti için 3 durumlu ziyaret tablosu (0: unvisited, 1: visiting, 2: visited) kullanılmış mı?"
  - "DFS geri izlemede durum güncellenmiş mi?"
reference_solution_path: private/solutions/cpp-medium-course-schedule-cycle.cpp
hint_ladder:
  1: "Her düğüm için 3 durum tutun (0: ziyaret edilmedi, 1: aktif çağrı yığınında, 2: tamamlandı)."
  2: "DFS sırasında durumu 1 olan bir komşuya rastlarsanız döngü vardır, doğrudan false dönün."
  3: "Bu çizge algoritması 'yönlü çizgede döngü tespiti (cycle detection in directed graph)' olarak bilinir."
```

---

### cpp-medium-trie-prefix-class

```yaml
id: cpp-medium-trie-prefix-class
version: 1
language: cpp
engine: none
difficulty: medium
title: "Sözcük öneklerini saklayan ve arayan önek ağacı sınıfı"
prompt: |
  Küçük harflerden oluşan sözcükleri ekleyen insert, tam sözcük arayan search ve verilen önekle başlayan sözcük varlığını sorgulayan starts_with metotlarına sahip `class Trie` sınıfını yazın. m sözcüğün uzunluğudur.
constraints:
  - "Zaman karmaşıklığı ekleme/arama için O(m) olmalı"
  - "Ek bellek O(m) olmalı"
  - "Akıllı işaretçiler veya çıplak işaretçi dizisi kullanılabilir"
expected:
  time: { Trie: "m" }
  space: "m"
concept_tags: [trees, smart-pointers]
checklist_extra:
  - "Her düğümde 26 çocuk ve is_end bayrağı tutulmuş mu?"
  - "Bellek sızıntısı önlenmiş mi?"
reference_solution_path: private/solutions/cpp-medium-trie-prefix-class.cpp
hint_ladder:
  1: "Kök düğümden başlayarak her harf için çocuk göstericisini takip edin."
  2: "Sözcük bittiğinde is_end işaretini koyun; aramalarda yol boyunca eksik düğüm yoksa sonucu dönün."
  3: "Bu veri yapısı 'önek ağacı yapısı (trie prefix tree)' olarak bilinir."
```

---

### cpp-medium-kth-largest-heap

```yaml
id: cpp-medium-kth-largest-heap
version: 1
language: cpp
engine: none
difficulty: medium
title: "Akıştan gelen elemanlar arasında en büyük k'ıncı elemanı takip etme"
prompt: |
  Akışa yeni eleman eklendikçe en büyük k'ıncı elemanı boyutu k ile sınırlandırılmış bir std::priority_queue (min-heap) ile O(log k) sürede döndüren `class KthLargest` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı eklemede O(log k) olmalı"
  - "Ek bellek O(k) olmalı"
  - "Min-heap boyutu daima k kalmalıdır"
expected:
  time: { KthLargest: "log k" }
  space: "k"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Kuyruk boyutu k'yı aştığında tepedeki en küçük eleman çekilmiş mi?"
  - "std::greater karşılaştırıcısı kullanılmış mı?"
reference_solution_path: private/solutions/cpp-medium-kth-largest-heap.cpp
hint_ladder:
  1: "std::priority_queue<int, std::vector<int>, std::greater<int>> ile min-heap oluşturun."
  2: "Heap boyutu k'yı aşınca pop() yapın; böylece heap tepesinde daima k'ıncı en büyük eleman kalsın."
  3: "Bu algoritma 'min-heap ile k'ıncı en büyük eleman takibi (kth largest element min-heap)' olarak bilinir."
```

---

### cpp-medium-merge-k-sorted-vectors

```yaml
id: cpp-medium-merge-k-sorted-vectors
version: 1
language: cpp
engine: none
difficulty: medium
title: "k adet sıralı vektörü min-heap ile birleştirme"
prompt: |
  Her biri küçükten büyüğe sıralı k adet tamsayı vektörünü std::priority_queue kullanarak tek bir sıralı vektörde O(n log k) sürede birleştiren `std::vector<int> merge_k_sorted(const std::vector<std::vector<int>>& lists)` fonksiyonunu yazın. n toplam eleman sayısı ve k liste sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n log k) olmalı"
  - "Ek bellek O(k) (heap boyutu) olmalı"
  - "reserve(n) çağrılmalıdır"
expected:
  time: { merge_k_sorted: "n log k" }
  space: "k"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Min-heap'te eleman değeri, liste indeksi ve eleman indeksi üçlüsü tutulmuş mı?"
  - "Toplam n eleman için reserve yapılmış mı?"
reference_solution_path: private/solutions/cpp-medium-merge-k-sorted-vectors.cpp
hint_ladder:
  1: "Her listenin ilk elemanını min-heap'e yerleştirin."
  2: "En küçük elemanı çekip sonuç vektörüne ekleyin ve o elemanın geldiği listeden bir sonraki elemanı heap'e itin."
  3: "Bu algoritma 'k adet sıralı diziyi yığınla birleştirme (merge k sorted vectors)' olarak bilinir."
```

---

### cpp-medium-longest-consecutive-seq

```yaml
id: cpp-medium-longest-consecutive-seq
version: 1
language: cpp
engine: none
difficulty: medium
title: "Sıralı olmayan dizide en uzun ardışık dizi uzunluğunu bulma"
prompt: |
  n elemanlı sıralı olmayan bir tamsayı vektöründe ardışık sayılardan oluşan (x, x+1, x+2, ...) en uzun dizilimin uzunluğunu std::unordered_set kullanarak O(n) sürede bulan `size_t longest_consecutive(const std::vector<int>& nums)` fonksiyonunu yazın. n vektörün boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Yalnızca ardışık dizinin başlangıç elemanından tarama yapılmalıdır"
expected:
  time: { longest_consecutive: "n" }
  space: "n"
concept_tags: [hash-map, data-structures]
checklist_extra:
  - "num - 1 kümede yoksa dizi başlangıcı olarak seçilmiş mi?"
  - "Her eleman en fazla iki kez ziyaret edilerek O(n) sağlanmış mı?"
reference_solution_path: private/solutions/cpp-medium-longest-consecutive-seq.cpp
hint_ladder:
  1: "Tüm elemanları bir std::unordered_set içine atın."
  2: "Bir sayı için num - 1 kümede yoksa bu sayıyı bir ardışık dizinin başı kabul edip num + 1, num + 2 ... varlığını sayın."
  3: "Bu algoritma 'en uzun ardışık sayı dizisi tespiti (longest consecutive sequence)' olarak bilinir."
```

---

### cpp-medium-subarray-sum-k

```yaml
id: cpp-medium-subarray-sum-k
version: 1
language: cpp
engine: none
difficulty: medium
title: "Toplamı k olan alt dizi sayısını önek toplamı haritasıyla bulma"
prompt: |
  n elemanlı bir tamsayı vektöründe elemanlarının toplamı k'ya eşit olan bitişik alt dizilerin adedini önek toplamı karma haritasıyla bulan `size_t subarray_sum(const std::vector<int>& nums, int k)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "std::unordered_map kullanılmalıdır"
expected:
  time: { subarray_sum: "n" }
  space: "n"
concept_tags: [hash-map, data-structures]
checklist_extra:
  - "curr_sum - k değeri haritada sorgulanmış mı?"
  - "Başlangıç için {0, 1} kaydı eklenmiş mi?"
reference_solution_path: private/solutions/cpp-medium-subarray-sum-k.cpp
hint_ladder:
  1: "Diziyi tararken birikimli toplamı güncelleyin."
  2: "curr_sum - k değerinin geçmişte kaç kez oluştuğunu haritadan okuyup cevaba ekleyin."
  3: "Bu algoritma 'önek toplamı ile alt dizi sayımı (subarray sum equals k)' olarak bilinir."
```

---

### cpp-medium-find-duplicate-floyd

```yaml
id: cpp-medium-find-duplicate-floyd
version: 1
language: cpp
engine: none
difficulty: medium
title: "Dizide mükerrer sayıyı iki işaretçiyle bulma"
prompt: |
  1'den n'e kadar sayılar içeren n+1 elemanlı bir tamsayı vektöründe tam olarak bir sayının tekrar ettiği bilinmektedir. Diziyi değiştirmeden ve ek bellek kullanmadan Floyd kaplumbağa-tavşan algoritmasıyla bu sayıyı bulan `int find_duplicate(const std::vector<int>& nums)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (dizi değiştirilemez)"
  - "İki fazlı döngü bulma algoritması uygulanmalıdır"
expected:
  time: { find_duplicate: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Dizi değerleri indeks olarak kabul edilmiş mi?"
  - "İlk kesişimden sonra biri başa alınıp döngü girişi bulunmuş mu?"
reference_solution_path: private/solutions/cpp-medium-find-duplicate-floyd.cpp
hint_ladder:
  1: "Diziyi bir bağlı liste gibi görerek slow = nums[slow] ve fast = nums[nums[fast]] adımlarıyla ilerleyin."
  2: "Kesiştikten sonra işaretçilerden birini başa alıp aynı hızla ilerleterek döngünün başladığı mükerrer sayıyı bulun."
  3: "Bu algoritma 'Floyd döngü bulma ile mükerrer eleman tespiti (Floyd cycle duplicate detection)' olarak bilinir."
```

---

### cpp-medium-binary-tree-lca

```yaml
id: cpp-medium-binary-tree-lca
version: 1
language: cpp
engine: none
difficulty: medium
title: "İkili arama ağacında iki değerin en yakın ortak atasını bulma"
prompt: |
  İkili arama ağacında p ve q değerlerini içeren düğümlerin en yakın ortak atasını (LCA) döngüsel olarak bulan `TreeNode* lowest_common_ancestor(TreeNode* root, int p, int q)` fonksiyonunu yazın. n ağaçtaki düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Döngüsel arama yapılmalıdır"
expected:
  time: { lowest_common_ancestor: "log n" }
  space: "1"
concept_tags: [trees, data-structures]
checklist_extra:
  - "p ve q ikisi birden küçükse sola, büyükse sağa gidilmiş mi?"
  - "Ayrışma noktası LCA olarak dönülmüş mü?"
reference_solution_path: private/solutions/cpp-medium-binary-tree-lca.cpp
hint_ladder:
  1: "Kökten başlayarak her iki değer de kökten küçükse sola, büyükse sağa geçin."
  2: "Değerler iki farklı kola ayrıldığı an ulaşılan düğüm en yakın ortak atadır."
  3: "Bu algoritma 'ikili arama ağacında en yakın ortak ata (lowest common ancestor in BST)' olarak bilinir."
```

---

### cpp-medium-binary-tree-level-order

```yaml
id: cpp-medium-binary-tree-level-order
version: 1
language: cpp
engine: none
difficulty: medium
title: "İkili ağacın elemanlarını seviye seviye gruplayarak gezme"
prompt: |
  Kökü verilen ikili ağacın elemanlarını derinlik seviyelerine göre gruplayarak std::vector<std::vector<int>> biçiminde döndüren `std::vector<std::vector<int>> level_order(TreeNode* root)` fonksiyonunu yazın. n ağaçtaki toplam düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "std::queue kullanılmalıdır"
expected:
  time: { level_order: "n" }
  space: "n"
concept_tags: [trees, data-structures]
checklist_extra:
  - "Her seviyenin başında kuyruk boyutu (level_size) kadar eleman çekilmiş mi?"
  - "Sol ve sağ çocuklar kuyruğa eklenmiş mi?"
reference_solution_path: private/solutions/cpp-medium-binary-tree-level-order.cpp
hint_ladder:
  1: "Kökü bir kuyruğa ekleyin."
  2: "Her turda kuyruğun o anki boyutu kadar düğüm çekip değerlerini o seviyenin vektörüne yazın ve çocuklarını kuyruğa ekleyin."
  3: "Bu algoritma 'seviye sıralı ağaç gezintisi (level order traversal)' olarak bilinir."
```

---

### cpp-medium-binary-tree-is-bst

```yaml
id: cpp-medium-binary-tree-is-bst
version: 1
language: cpp
engine: none
difficulty: medium
title: "Ağacın geçerli ikili arama ağacı olduğunu aralık sınırlarıyla doğrulama"
prompt: |
  İkili bir ağacın tüm düğümlerinin ikili arama ağacı kuralını eksiksiz sağladığını özyinelemeli aralık sınırlarıyla (min, max) doğrulayan `bool is_valid_bst(TreeNode* root)` fonksiyonunu yazın. n ağaçtaki düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek çağrı yığını için O(log n) olmalı"
  - "Tamsayı taşmasını önlemek için std::optional veya 64-bit sınırlar kullanılmalı"
expected:
  time: { is_valid_bst: "n" }
  space: "log n"
concept_tags: [trees, edge-cases]
checklist_extra:
  - "INT_MIN ve INT_MAX sınırları için güvenli aralık kullanılmış mı?"
  - "Tüm sol alt ağacın kesinlikle küçük olduğu doğrulanmış mı?"
reference_solution_path: private/solutions/cpp-medium-binary-tree-is-bst.cpp
hint_ladder:
  1: "Her düğüm için geçerli bir (min_limit, max_limit) aralığı tanımlayın."
  2: "Sola dallanırken üst sınırı, sağa dallanırken alt sınırı mevcut düğümün değeriyle daraltın."
  3: "Bu kontrol 'aralık kısıtlamalı ikili arama ağacı doğrulaması (valid BST range check)' olarak bilinir."
```

---

### cpp-medium-serialize-deserialize-tree

```yaml
id: cpp-medium-serialize-deserialize-tree
version: 1
language: cpp
engine: none
difficulty: medium
title: "İkili ağacı dizgiye serileştirme ve geri oluşturma"
prompt: |
  İkili bir ağacı ön-sıralı (pre-order) dolaşarak aralarına virgül koyarak ve null düğümleri '#' ile göstererek dizgiye çeviren ve bu dizgiden ağacı yeniden kuran `class TreeCodec` sınıfını yazın. n düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Dizgi akışı veya parçalama kullanılmalıdır"
expected:
  time: { TreeCodec: "n" }
  space: "n"
concept_tags: [trees, strings]
checklist_extra:
  - "Düğüm değerleri ve null işaretleri doğru ayrıştırılmış mı?"
  - "Ön-sıralı özyinelemeyle ağaç eksiksiz kurulmuş mu?"
reference_solution_path: private/solutions/cpp-medium-serialize-deserialize-tree.cpp
hint_ladder:
  1: "Ön-sıralı dolaşımda her düğümün değerini dizgiye yazıp null çocuklar için '#' ekleyin."
  2: "Geri oluştururken dizgiyi sırayla okuyup '#' gördükçe nullptr, sayı gördükçe yeni düğüm oluşturun."
  3: "Bu mekanizma 'ikili ağaç serileştirme ve geri kurma (tree serialization and deserialization)' olarak bilinir."
```

---

### cpp-medium-flatten-tree-linked-list

```yaml
id: cpp-medium-flatten-tree-linked-list
version: 1
language: cpp
engine: none
difficulty: medium
title: "İkili ağacı yerinde tek yönlü bağlı liste gibi sağa düzleştirme"
prompt: |
  İkili bir ağacın tüm düğümlerini ön-sıralı (pre-order) düzende sağ çocuk işaretçileri üzerinden tek yönlü bağlı liste yapısına dönüştüren ve sol işaretçileri nullptr yapan `void flatten_to_list(TreeNode* root)` fonksiyonunu yazın. n ağaçtaki düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (Morris benzeri veya işaretçi kaydırma)"
  - "Sol göstericiler sıfırlanmalıdır"
expected:
  time: { flatten_to_list: "n" }
  space: "1"
concept_tags: [trees, smart-pointers]
checklist_extra:
  - "Sol alt dal sağa taşınmadan önce sağ alt dal solun en sağına bağlanmış mı?"
  - "Sol işaretçiler nullptr yapılmış mı?"
reference_solution_path: private/solutions/cpp-medium-flatten-tree-linked-list.cpp
hint_ladder:
  1: "Sol çocuğu olan her düğüm için sol alt ağacın en sağ yaprağını bulun."
  2: "O yaprağın sağına mevcut sağ çocuğu bağlayıp tüm sol dalı sağa taşıyın ve solu nullptr yapın."
  3: "Bu dönüştürme işlemi 'ikili ağacı bağlı listeye düzleştirme (flatten binary tree to linked list)' olarak bilinir."
```

---

### cpp-medium-clone-graph-hash

```yaml
id: cpp-medium-clone-graph-hash
version: 1
language: cpp
engine: none
difficulty: medium
title: "Düğümleri ve komşulukları karma haritasıyla kopyalayarak çizge klonlama"
prompt: |
  Bağlantılı yönsüz bir çizgenin başlangıç düğümünü alarak tüm düğümleri ve komşuluk ilişkilerini derinlemesine kopyalayan `Node* clone_graph(Node* node)` fonksiyonunu yazın. n düğüm ve m kenar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n + m) olmalı"
  - "Ek bellek O(n) olmalı"
  - "std::unordered_map<Node*, Node*> ile döngüler önlenmelidir"
expected:
  time: { clone_graph: "n + m" }
  space: "n"
concept_tags: [data-structures, hash-map]
checklist_extra:
  - "Orijinal düğüm ile kopya düğüm haritada eşleştirilmiş mi?"
  - "Döngüsel kenarlarda sonsuz özyineleme engellenmiş mi?"
reference_solution_path: private/solutions/cpp-medium-clone-graph-hash.cpp
hint_ladder:
  1: "Ziyaret edilen her orijinal düğüm için yeni bir kopya düğüm tahsis edip haritaya kaydedin."
  2: "Komşuları özyinelemeli veya BFS ile dolaşarak haritadaki kopyaları komşuluk listesine ekleyin."
  3: "Bu çizge algoritması 'karma tablosu ile derin çizge klonlama (deep clone graph)' olarak bilinir."
```

---

### cpp-medium-number-of-islands-bfs

```yaml
id: cpp-medium-number-of-islands-bfs
version: 1
language: cpp
engine: none
difficulty: medium
title: "2D ızgaradaki adaların toplam sayısını BFS ile bulma"
prompt: |
  '1' (kara) ve '0' (su) karakterlerinden oluşan n x m boyutundaki bir ızgarada yatay ve dikey bağlı adalardan kaç tane olduğunu BFS ile hesaplayan `int count_islands(std::vector<std::vector<char>>& grid)` fonksiyonunu yazın. n satır ve m sütun adedidir.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(min(n, m)) (BFS kuyruğu) olmalı"
  - "Ziyaret edilen hücreler '0' yapılarak işaretlenebilir"
expected:
  time: { count_islands: "n*m" }
  space: "n + m"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "Izgara sınırları kontrol edilmiş mi?"
  - "Ziyaret edilen hücreler hemen işaretlenerek kuyruk şişmesi önlenmiş mi?"
reference_solution_path: private/solutions/cpp-medium-number-of-islands-bfs.cpp
hint_ladder:
  1: "Izgarayı gezerken '1' gördükçe ada sayısını artırın."
  2: "BFS kuyruğu başlatarak adanın tüm bağlı komşularını '0' yaparak batırın."
  3: "Bu ızgara algoritması 'ada sayısı hesaplama (number of islands BFS)' olarak bilinir."
```

---

### cpp-medium-word-break-dp

```yaml
id: cpp-medium-word-break-dp
version: 1
language: cpp
engine: none
difficulty: medium
title: "Metnin sözlükteki sözcüklerle oluşturulup oluşturulamayacağını bulma"
prompt: |
  Verilen bir metin görünümünün sözlükteki sözcüklerin ardışık birleşimiyle oluşturulup oluşturulamayacağını dinamik programlamayla denetleyen `bool word_break(std::string_view s, const std::unordered_set<std::string>& word_dict)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n^2) olmalı"
  - "Ek bellek O(n) olmalı"
  - "dp[i] i uzunluğundaki önekin kurulabilirliğini göstermelidir"
expected:
  time: { word_break: "n^2" }
  space: "n"
concept_tags: [strings, hash-map]
checklist_extra:
  - "dp[0] = true başlatılmış mı?"
  - "Alt dizgiler s.substr(j, i - j) sözlükte hızlıca sorgulanmış mı?"
reference_solution_path: private/solutions/cpp-medium-word-break-dp.cpp
hint_ladder:
  1: "dp[i] değerini ilk i karakterin sözlükteki kelimelerle bölünebilirliği olarak tanımlayın."
  2: "dp[j] true ise s[j...i] parçasının sözlükte olup olmadığını kontrol ederek dp[i]'yi güncelleyin."
  3: "Bu dinamik programlama algoritması 'sözcük kırma problemi (word break dynamic programming)' olarak bilinir."
```

---

### cpp-medium-coin-change-min

```yaml
id: cpp-medium-coin-change-min
version: 1
language: cpp
engine: none
difficulty: medium
title: "Hedef tutara ulaşmak için gereken asgari madeni para sayısını hesaplama"
prompt: |
  Farklı nominal değerlere sahip madeni paralarla k tutarına ulaşmak için gereken minimum para sayısını dinamik programlamayla hesaplayan `int coin_change(const std::vector<int>& coins, int k)` fonksiyonunu yazın. Ulaşılamazsa -1 dönmelidir. n para çeşit sayısı ve k hedef tutardır.
constraints:
  - "Zaman karmaşıklığı O(n * k) olmalı"
  - "Ek bellek O(k) olmalı"
  - "Taban durum dp[0] = 0 ayarlanmalıdır"
expected:
  time: { coin_change: "n*k" }
  space: "k"
concept_tags: [data-structures, performance]
checklist_extra:
  - "dp tablosu k + 1 veya sonsuz ile başlatılmış mı?"
  - "Ulaşılamayan tutarlar için -1 dönülmüş mü?"
reference_solution_path: private/solutions/cpp-medium-coin-change-min.cpp
hint_ladder:
  1: "dp[i] değerini i tutarına ulaşmak için gereken minimum madeni para sayısı olarak tanımlayın."
  2: "Her para değeri için dp[i] = min(dp[i], dp[i - coin] + 1) geçişini uygulayın."
  3: "Bu problem 'madeni para değiştirme problemi (coin change problem)' olarak bilinir."
```

---

### cpp-medium-longest-increasing-subseq

```yaml
id: cpp-medium-longest-increasing-subseq
version: 1
language: cpp
engine: none
difficulty: medium
title: "En uzun artan alt dizinin uzunluğunu dinamik programlamayla bulma"
prompt: |
  n elemanlı bir tamsayı vektöründe kesinlikle artan en uzun alt dizinin uzunluğunu O(n^2) dinamik programlama yaklaşımıyla hesaplayan `size_t length_of_lis(const std::vector<int>& nums)` fonksiyonunu yazın. n vektörün boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n^2) olmalı"
  - "Ek bellek O(n) olmalı"
  - "dp dizisi 1 ile başlatılmalıdır"
expected:
  time: { length_of_lis: "n^2" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Her i için önceki tüm j < i elemanları taranmış mı?"
  - "nums[i] > nums[j] ise dp[i] = max(dp[i], dp[j] + 1) yapılmış mı?"
reference_solution_path: private/solutions/cpp-medium-longest-increasing-subseq.cpp
hint_ladder:
  1: "dp[i] değerini i. elemanda sonlanan en uzun artan alt dizi uzunluğu yapın."
  2: "Önceki tüm küçük elemanların dp değerlerinin maksimumuna 1 ekleyerek genel maksimumu güncelleyin."
  3: "Bu klasik algoritma 'en uzun artan alt dizi dinamik programlama çözümü (longest increasing subsequence DP)' olarak bilinir."
```

---

### cpp-medium-evaluate-rpn-stack

```yaml
id: cpp-medium-evaluate-rpn-stack
version: 1
language: cpp
engine: none
difficulty: medium
title: "Ters Polonyalı Notasyonundaki matematiksel ifadeyi yığınla hesaplama"
prompt: |
  Ters Polonyalı Notasyonunda (RPN) verilmiş n adet simgeyi std::stack kullanarak değerlendiren ve sonucu hesaplayan `int eval_rpn(const std::vector<std::string>& tokens)` fonksiyonunu yazın. Desteklenen operatörler: +, -, *, /.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "İşlenenlerin sırası çıkarma ve bölmede gözetilmelidir"
expected:
  time: { eval_rpn: "n" }
  space: "n"
concept_tags: [data-structures, strings]
checklist_extra:
  - "İkinci çekilen sol işlenen, ilk çekilen sağ işlenen olarak bölünmüş mü?"
  - "std::stoi ile sayılar dönüştürülmüş mü?"
reference_solution_path: private/solutions/cpp-medium-evaluate-rpn-stack.cpp
hint_ladder:
  1: "Sayı gördükçe yığına itin."
  2: "Operatör gördükçe yığından iki sayı çekip b ve a olarak adlandırarak a op b sonucunu tekrar yığına itin."
  3: "Bu algoritma 'ters Polonyalı notasyonu yığın değerlendirmesi (reverse Polish notation stack evaluation)' olarak bilinir."
```

---

### cpp-medium-daily-temperatures-mono

```yaml
id: cpp-medium-daily-temperatures-mono
version: 1
language: cpp
engine: none
difficulty: medium
title: "Monotonik yığın kullanarak daha sıcak gün için bekleme günlerini hesaplama"
prompt: |
  n günlük sıcaklık vektörü verildiğinde her gün için daha sıcak bir günün gelmesi için kaç gün beklenmesi gerektiğini monotonik azalan yığınla bulan `std::vector<int> daily_temperatures(const std::vector<int>& temps)` fonksiyonunu yazın. n gün sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Yığında indeksler saklanmalıdır"
expected:
  time: { daily_temperatures: "n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Yığında sıcaklık yerine gün indeksi tutulmuş mu?"
  - "Mevcut sıcaklık yığındaki günden sıcaksa aradaki gün farkı sonuca yazılmış mı?"
reference_solution_path: private/solutions/cpp-medium-daily-temperatures-mono.cpp
hint_ladder:
  1: "Günün indekslerini saklayan monotonik azalan bir yığın tutun."
  2: "Daha sıcak bir gün gördükçe yığından önceki günleri çekip aradaki indeks farkını sonuç dizisine yazın."
  3: "Bu algoritma 'monotonik yığın ile sıcaklık takibi (monotonic stack daily temperatures)' olarak bilinir."
```

---

### cpp-medium-next-greater-element-stack

```yaml
id: cpp-medium-next-greater-element-stack
version: 1
language: cpp
engine: none
difficulty: medium
title: "Monotonik azalan yığın ile sağdaki ilk büyük elemanı bulma"
prompt: |
  n elemanlı bir dizide her elemanın sağında yer alan kendisinden kesinlikle büyük ilk elemanı monotonik yığınla bulan `std::vector<int> next_greater_elements(const std::vector<int>& nums)` fonksiyonunu yazın. Sağında daha büyük eleman yoksa -1 olmalıdır. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Her eleman yığına bir kez girip bir kez çıkmalıdır"
expected:
  time: { next_greater_elements: "n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Dizi sağdan sola veya soldan sağa taranarak monotonik yığın kurulmuş mu?"
  - "Büyük eleman bulunamayanlar -1 kalmış mı?"
reference_solution_path: private/solutions/cpp-medium-next-greater-element-stack.cpp
hint_ladder:
  1: "Diziyi sağdan sola doğru tarayarak mevcut elemandan küçük veya eşit olanları yığından atın."
  2: "Yığının tepesindeki eleman sağdaki ilk büyük elemandır; yığın boşsa -1 yazıp mevcut elemanı yığına itin."
  3: "Bu algoritma 'sağdaki ilk büyük eleman tespiti (next greater element)' olarak bilinir."
```

---

### cpp-medium-matrix-word-search

```yaml
id: cpp-medium-matrix-word-search
version: 1
language: cpp
engine: none
difficulty: medium
title: "2D karakter ızgarasında verilen sözcüğü geri izleme ile arama"
prompt: |
  n x m boyutundaki bir karakter matrisinde ardışık komşu hücreleri (yukarı, aşağı, sol, sağ) takip ederek verilen word sözcüğünün bulunup bulunmadığını geri izleme (backtracking) ile denetleyen `bool word_search(const std::vector<std::vector<char>>& board, std::string_view word)` fonksiyonunu yazın. k sözcüğün uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n * m * 4^k) olmalı"
  - "Ek bellek O(k) olmalı"
  - "Ziyaret edilen hücreler geçici değiştirilip geri yüklenmelidir"
expected:
  time: { word_search: "n*m" }
  space: "k"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "Hücreler ziyaret edildiğinde '#' yapılıp dönüşte eski karakter geri yüklenmiş mi?"
  - "Izgara sınırları denetlenmiş mi?"
reference_solution_path: private/solutions/cpp-medium-matrix-word-search.cpp
hint_ladder:
  1: "Matristeki her hücreden başlayarak sözcüğün ilk harfiyle eşleşenlerde DFS başlatın."
  2: "Geçici olarak hücreyi '#' yaparak aynı hücrenin iki kez kullanılmasını önleyin ve dönüşte eski karakteri geri yükleyin."
  3: "Bu algoritma 'ızgarada sözcük arama geri izlemesi (word search backtracking)' olarak bilinir."
```

---

### cpp-medium-subsets-backtrack

```yaml
id: cpp-medium-subsets-backtrack
version: 1
language: cpp
engine: none
difficulty: medium
title: "Elemanları benzersiz kümenin tüm alt kümelerini geri izleme ile üretme"
prompt: |
  n elemanlı benzersiz tamsayı vektörünün tüm 2^n adet alt kümesini geri izleme yöntemiyle üreten `std::vector<std::vector<int>> generate_subsets(const std::vector<int>& nums)` fonksiyonunu yazın. n eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n * 2^n) olmalı"
  - "Ek bellek O(n) (özyineleme yığını) olmalı"
  - "Her adımda elemanı dahil etme ve etmeme dalları oluşturulmalıdır"
expected:
  time: { generate_subsets: "2^n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Mevcut alt küme her özyineleme başında sonuca kopyalanmış mı?"
  - "Geri izlemede pop_back yapılmış mı?"
reference_solution_path: private/solutions/cpp-medium-subsets-backtrack.cpp
hint_ladder:
  1: "Her özyineleme adımında mevcut geçici alt kümeyi sonuç listesine ekleyin."
  2: "start indeksinden itibaren her elemanı geçici kümeye ekleyip bir sonraki indekse dalın ve dönüşte pop_back ile geri alın."
  3: "Bu algoritma 'alt küme üretme geri izleme algoritması (subsets backtracking)' olarak bilinir."
```

---

### cpp-medium-permutations-backtrack

```yaml
id: cpp-medium-permutations-backtrack
version: 1
language: cpp
engine: none
difficulty: medium
title: "Tamsayı dizisinin tüm permütasyonlarını geri izleme ile üretme"
prompt: |
  n elemanlı benzersiz tamsayılardan oluşan bir vektörün tüm n! permütasyonunu geri izleme veya yerinde takas (in-place swap) ile üreten `std::vector<std::vector<int>> generate_permutations(std::vector<int>& nums)` fonksiyonunu yazın. n vektörün boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n * n!) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Yerinde takas yöntemi uygulanabilir"
expected:
  time: { generate_permutations: "n!" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "start indeksi son elemana ulaştığında permütasyon kaydedilmiş mi?"
  - "Geri izleme dönüşünde takas geri alınmış mı?"
reference_solution_path: private/solutions/cpp-medium-permutations-backtrack.cpp
hint_ladder:
  1: "start indeksinden sona kadar her elemanı start ile takas ederek özyinelemeyi başlatın."
  2: "Dönüşte takası geri alarak dizinin orijinal sırasını koruyun."
  3: "Bu algoritma 'permütasyon üretme geri izleme algoritması (permutations backtracking)' olarak bilinir."
```

---

### cpp-medium-custom-shared-ptr

```yaml
id: cpp-medium-custom-shared-ptr
version: 1
language: cpp
engine: none
difficulty: medium
title: "Özel paylaşımlı akıllı işaretçi tasarlama"
prompt: |
  Dinamik nesne için başvuru sayacını (reference counter) heap üzerinde tutan, kopya yapıcıda sayacı artıran ve yıkıcıda sayaç sıfıra düştüğünde belleği serbest bırakan `class SimpleSharedPtr` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı her işlem için O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Kopya atamada eski kaynağın sayacı azaltılmalıdır"
expected:
  time: { SimpleSharedPtr: "1" }
  space: "1"
concept_tags: [smart-pointers, ownership]
checklist_extra:
  - "Sayaç heap üzerinde tahsis edilmiş mi?"
  - "Sayaç 0 olduğunda hem veri hem sayaç delete edilmiş mi?"
reference_solution_path: private/solutions/cpp-medium-custom-shared-ptr.cpp
hint_ladder:
  1: "T* ptr_ ve size_t* ref_count_ işaretçilerini tutun."
  2: "Kopyalamalarda (*ref_count_)++ yapın; yıkıcıda sayacı bir azaltıp sıfıra indiğinde nesneyi ve sayacı delete ile temizleyin."
  3: "Bu C++ veri yapısı 'paylaşımlı akıllı işaretçi gerçeklemesi (custom shared pointer implementation)' olarak bilinir."
```

---


---

## 4. Zor (Hard) — 50 Soru

---

### cpp-hard-concurrent-lru-cache

```yaml
id: cpp-hard-concurrent-lru-cache
version: 1
language: cpp
engine: none
difficulty: hard
title: "Çoklu okuyucu tekil yazıcı destekli kilitli LRU önbellek"
prompt: |
  std::shared_mutex ve ince taneli kilitlerle birden çok iş parçacığının eşzamanlı get çağrısı yapabildiği, put anında ise güvenle güncellenen `class ConcurrentLRUCache` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(capacity) olmalı"
  - "Veri yarışı kesinlikle engellenmelidir"
expected:
  time: { ConcurrentLRUCache: "1" }
  space: "1"
concept_tags: [lru-cache, concurrency]
checklist_extra:
  - "std::shared_lock ile okuma, std::unique_lock ile yazma ayrılmış mı?"
  - "Veri yarışı önlenmiş mi?"
reference_solution_path: private/solutions/cpp-hard-concurrent-lru-cache.cpp
hint_ladder:
  1: "std::shared_mutex ile okuma anında paylaşımlı kilit edinin."
  2: "Önbellek isabetinde elemanı başa taşırken veya yeni eleman eklerken benzersiz kilide (unique_lock) geçiş yapın."
  3: "Bu eşzamanlı veri yapısı 'eşzamanlı LRU önbellek sistemi (concurrent LRU cache)' olarak bilinir."
```

---

### cpp-hard-thread-safe-bounded-queue

```yaml
id: cpp-hard-thread-safe-bounded-queue
version: 1
language: cpp
engine: none
difficulty: hard
title: "Durum değişkenleri ve kilitlerle tam korumalı sınırlı kuyruk"
prompt: |
  Kapasitesi sınırlı olan, kuyruk doluyken üreticileri, boşken tüketicileri std::condition_variable ile bekleten ve kapanışta tüm bekleyenleri uyandıran `class SafeBoundedQueue` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(capacity) olmalı"
  - "Kapanışta deadlock oluşmamalıdır"
expected:
  time: { SafeBoundedQueue: "1" }
  space: "1"
concept_tags: [concurrency, data-race]
checklist_extra:
  - "Sahte uyanmalar döngüyle denetlenmiş mi?"
  - "close() metodunda notify_all() çağrılarak tüm iş parçacıkları uyandırılmış mı?"
reference_solution_path: private/solutions/cpp-hard-thread-safe-bounded-queue.cpp
hint_ladder:
  1: "Dahili kuyruğu std::mutex ve iki std::condition_variable ile koruyun."
  2: "Kapanma bayrağı çekildiğinde tüm bekleyen iş parçacıklarının güvenle döngüden çıkmasını sağlayın."
  3: "Bu senkronizasyon yapısı 'iş parçacığı güvenli sınırlı kuyruk (thread-safe bounded queue)' olarak bilinir."
```

---

### cpp-hard-lock-free-stack-treiber

```yaml
id: cpp-hard-lock-free-stack-treiber
version: 1
language: cpp
engine: none
difficulty: hard
title: "Atomik CAS işlemleriyle Treiber kilit-serbest yığın gerçekleştirme"
prompt: |
  std::atomic<Node*> başlık göstericisi üzerinde compare_exchange_weak döngüsü ile kilit kullanmadan eleman ekleyen (push) ve çeken (pop) `class LockFreeStack` sınıfını yazın.
constraints:
  - "Amortize zaman karmaşıklığı O(1*) olmalı"
  - "Ek bellek O(1) olmalı"
  - "C++11/20 bellek modelleri kullanılmalıdır"
expected:
  time: { LockFreeStack: "1*" }
  space: "1"
concept_tags: [concurrency, performance]
checklist_extra:
  - "compare_exchange_weak döngü içinde kullanılmış mı?"
  - "Bellek sırası std::memory_order_release ve acquire ile doğru kurgulanmış mı?"
reference_solution_path: private/solutions/cpp-hard-lock-free-stack-treiber.cpp
hint_ladder:
  1: "Yeni düğümün next işaretçisini mevcut başlığa bağlayın."
  2: "head_.compare_exchange_weak ile başlığı atomik olarak yeni düğüme güncelleyene kadar döngüyü sürdürün."
  3: "Bu kilit-serbest algoritma 'Treiber yığını (Treiber lock-free stack)' olarak bilinir."
```

---

### cpp-hard-lock-free-spsc-queue

```yaml
id: cpp-hard-lock-free-spsc-queue
version: 1
language: cpp
engine: none
difficulty: hard
title: "Atomik indeksler ve bellek sıralamalarıyla tek üretici tek tüketici kuyruk"
prompt: |
  Kilit kullanmadan tek bir üretici ve tek bir tüketici arasında çalışan, sabit boyutlu dairesel dizi üzerinde atomik indekslerle veri ileten `class LockFreeSPSCQueue` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(capacity) olmalı"
  - "acquire ve release bellek sıralamaları uygulanmalıdır"
expected:
  time: { LockFreeSPSCQueue: "1" }
  space: "1"
concept_tags: [concurrency, performance]
checklist_extra:
  - "Yazma ve okuma indeksleri farklı önbellek satırlarına (alignas(64)) yerleştirilerek false sharing önlenmiş mi?"
  - "Kilit kullanılmamış mı?"
reference_solution_path: private/solutions/cpp-hard-lock-free-spsc-queue.cpp
hint_ladder:
  1: "Üretici tail indeksini artırıp release bariyeri uygulasın."
  2: "Tüketici head indeksini okurken acquire bariyeri kullanarak verinin işlemciler arasında doğru senkronize olmasını sağlayın."
  3: "Bu yüksek başarımlı kuyruk 'kilit-serbest SPSC kuyruğu (lock-free single-producer single-consumer queue)' olarak bilinir."
```

---

### cpp-hard-hazard-pointers-reclaim

```yaml
id: cpp-hard-hazard-pointers-reclaim
version: 1
language: cpp
engine: none
difficulty: hard
title: "Kilit-serbest veri yapılarında tehlike işaretçileriyle güvenli bellek iadesi"
prompt: |
  Okuyucuların eriştiği düğümleri tehlike işaretçisi (hazard pointer) tablosuna kaydederek, başka bir iş parçacığının bu düğümü erken silmesini önleyen `class HazardPointerManager` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(threads) olmalı"
  - "Emekli listesindeki düğümler taranmalıdır"
expected:
  time: { HazardPointerManager: "1" }
  space: "1"
concept_tags: [concurrency, ownership]
checklist_extra:
  - "Tehlike listesindeki adresler taranmadan düğüm silinmesi engellenmiş mi?"
  - "use-after-free önlenmiş mi?"
reference_solution_path: private/solutions/cpp-hard-hazard-pointers-reclaim.cpp
hint_ladder:
  1: "Okuyucu düğümü okumadan önce adresini kendi tehlike yuvasına atomik olarak yazsın."
  2: "Silici iş parçacığı düğümü emekli listesine alsın; liste dolduğunda tehlike yuvalarında olmayan düğümleri silsin."
  3: "Bu bellek güvenliği algoritması 'tehlike işaretçisi bellek yönetimi (hazard pointers memory reclamation)' olarak bilinir."
```

---

### cpp-hard-atomic-shared-ptr-ops

```yaml
id: cpp-hard-atomic-shared-ptr-ops
version: 1
language: cpp
engine: none
difficulty: hard
title: "Paylaşılan işaretçileri atomik operasyonlarla veri yarışsız güncelleme"
prompt: |
  std::atomic<std::shared_ptr<State>> kullanarak paylaşılan durumu kilit kullanmadan atomik olarak güncelleyen `class AtomicSharedState` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "C++20 std::atomic<std::shared_ptr> kullanılmalıdır"
expected:
  time: { AtomicSharedState: "1" }
  space: "1"
concept_tags: [smart-pointers, concurrency]
checklist_extra:
  - "std::atomic<std::shared_ptr<T>> uzmanlaşması kullanılmış mı?"
  - "Veri yarışı olmadan durum güncellenmiş mi?"
reference_solution_path: private/solutions/cpp-hard-atomic-shared-ptr-ops.cpp
hint_ladder:
  1: "C++20 ile gelen std::atomic<std::shared_ptr<T>> türünü üye olarak saklayın."
  2: "load() ve store() veya compare_exchange ile paylaşılan nesneyi kilit olmaksızın iş parçacıkları arasında güvenle değiştirin."
  3: "Bu modern eşzamanlılık aracı 'atomik paylaşımlı işaretçi operasyonu (atomic shared pointer operations)' olarak bilinir."
```

---

### cpp-hard-work-stealing-pool

```yaml
id: cpp-hard-work-stealing-pool
version: 1
language: cpp
engine: none
difficulty: hard
title: "Çift uçlu kuyruklardan görev çalan yüksek başarımlı iş havuzu"
prompt: |
  Her iş parçacığının kendi yerel deque'si olan ve kendi işi bittiğinde diğer iş parçacıklarının kuyruğundan görev çalan `class WorkStealingPool` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(threads * capacity) olmalı"
  - "Kilit çatışması en aza indirilmelidir"
expected:
  time: { WorkStealingPool: "1" }
  space: "1"
concept_tags: [concurrency, performance]
checklist_extra:
  - "Yerel iş parçacığı kuyruk sonundan (LIFO), çalan iş parçacığı kuyruk başından (FIFO) mı işlem yapıyor?"
  - "Deadlock önlenmiş mi?"
reference_solution_path: private/solutions/cpp-hard-work-stealing-pool.cpp
hint_ladder:
  1: "Her iş parçacığı kendi yerel kuyruğunun arkasından görev çekip çalıştırsın."
  2: "Kendi kuyruğu boşalan iş parçacığı rastgele başka bir iş parçacığının kuyruk önünden görev çalarak iş yükünü dengelesin."
  3: "Bu gelişmiş iş parçacığı mimarisi 'iş çalma havuzu (work-stealing thread pool)' olarak bilinir."
```

---

### cpp-hard-custom-arena-allocator

```yaml
id: cpp-hard-custom-arena-allocator
version: 1
language: cpp
engine: none
difficulty: hard
title: "STL kapsayıcılarıyla uyumlu bellek havuzu tahsisçisi"
prompt: |
  Büyük bir bellek bloğunu baştan tahsis eden ve STL kapsayıcılarının iç tahsislerini bu bloktan tek yönlü ofset artışıyla O(1) sürede karşılayan `class MonotonicArenaResource` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "std::pmr::memory_resource arayüzü gerçekleştirilmelidir"
expected:
  time: { MonotonicArenaResource: "1" }
  space: "1"
concept_tags: [raii, performance]
checklist_extra:
  - "do_allocate ve do_deallocate metotları ezilmiş mi?"
  - "Hizalama (alignment) kurallarına uyulmuş mu?"
reference_solution_path: private/solutions/cpp-hard-custom-arena-allocator.cpp
hint_ladder:
  1: "std::pmr::memory_resource sınıfından türeyerek do_allocate içinde tampon ofsetini hizalayarak ilerletin."
  2: "do_deallocate içinde tekil serbest bırakma yapmayıp tüm belleği havuz yıkıcısında tek seferde temizleyin."
  3: "Bu bellek mimarisi 'monotonik arena bellek yöneticisi (monotonic arena allocator)' olarak bilinir."
```

---

### cpp-hard-small-string-optimization

```yaml
id: cpp-hard-small-string-optimization
version: 1
language: cpp
engine: none
difficulty: hard
title: "Küçük metinleri dinamik bellek ayırmadan yerel tamponda saklama"
prompt: |
  Karakter sayısı 15 veya daha az olduğunda yığında yerel tamponda saklayan, aşıldığında dinamik heap tahsisine geçen `class SSOString` sınıfını yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(1) veya O(n) olmalı"
  - "Ek bellek O(1) (küçük metinler için) olmalı"
  - "Birlik (union) veya bayrak yapısı kullanılmalıdır"
expected:
  time: { SSOString: "n" }
  space: "1"
concept_tags: [strings, performance]
checklist_extra:
  - "Küçük metinlerde heap tahsisi (malloc/new) engellenmiş mi?"
  - "Büyük metinlerde dinamik tampon doğru serbest bırakılmış mı?"
reference_solution_path: private/solutions/cpp-hard-small-string-optimization.cpp
hint_ladder:
  1: "Sınıf içinde 16 baytlık yerel bir dizi ve heap göstericisini içeren bir birlik (union) tutun."
  2: "Metin uzunluğuna göre küçük/büyük durum bayrağını ayarlayarak küçük dizgilerde dinamik bellek maliyetini sıfırlayın."
  3: "Bu C++ dizgi optimizasyonu 'küçük dizgi optimizasyonu (small string optimization SSO)' olarak bilinir."
```

---

### cpp-hard-cow-string-atomic

```yaml
id: cpp-hard-cow-string-atomic
version: 1
language: cpp
engine: none
difficulty: hard
title: "Atomik başvuru sayacı ile kopyalama anında yazma destekli dizgi"
prompt: |
  Metin kopyalandığında belleği çoğaltmayıp başvuru sayacını atomik artıran, yalnızca içeriği değiştiren bir yazma çağrısında kopya çıkaran `class COWString` sınıfını yazın.
constraints:
  - "Kopyalama zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Yazma operasyonunda unshare yapılmalıdır"
expected:
  time: { COWString: "1" }
  space: "1"
concept_tags: [ownership, concurrency]
checklist_extra:
  - "Başvuru sayacı atomik artırılıp azaltılmış mı?"
  - "Yazma anında başvuru sayısı > 1 ise bağımsız kopya oluşturulmuş mu?"
reference_solution_path: private/solutions/cpp-hard-cow-string-atomic.cpp
hint_ladder:
  1: "Metin tamponunun başlığında bir std::atomic<size_t> başvuru sayacı tutun."
  2: "Kopya yapıcıda sadece sayacı artırın; değiştirici bir metot çağrıldığında sayaç > 1 ise yeni bir kopya tahsis edip sayacı düşürün."
  3: "Bu optimizasyon tekniği 'yazma anında kopyalama metin yapısı (copy-on-write string COW)' olarak bilinir."
```

---

### cpp-hard-median-two-sorted-arrays

```yaml
id: cpp-hard-median-two-sorted-arrays
version: 1
language: cpp
engine: none
difficulty: hard
title: "İki sıralı dizinin birleşim medyanını ikili aramayla bulma"
prompt: |
  Küçükten büyüğe sıralı nums1 (n elemanlı) ve nums2 (m elemanlı) vektörlerini birleştirmeden ikili arama ile birleşim medyanını O(log(min(n, m))) sürede hesaplayan `double find_median_sorted_arrays(const std::vector<int>& nums1, const std::vector<int>& nums2)` fonksiyonunu yazın. n ve m dizi boyutlarıdır.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Kısa olan dizi üzerinde ikili arama yapılmalıdır"
expected:
  time: { find_median_sorted_arrays: "log n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Sol ve sağ yarıları bölen bölüm çizgisi doğru hesaplanmış mı?"
  - "Sınır koşullarında INT_MIN ve INT_MAX kullanılmış mı?"
reference_solution_path: private/solutions/cpp-hard-median-two-sorted-arrays.cpp
hint_ladder:
  1: "Daha kısa olan vektör üzerinde ikili arama yaparak bölüm noktasını belirleyin."
  2: "Her iki dizinin sol maksimumları sağ minimumlardan küçük veya eşit olduğu an medyanı hesaplayın."
  3: "Bu algoritma 'iki sıralı dizinin medyanını ikili aramayla bulma (median of two sorted arrays)' olarak bilinir."
```

---

### cpp-hard-sliding-window-median-heaps

```yaml
id: cpp-hard-sliding-window-median-heaps
version: 1
language: cpp
engine: none
difficulty: hard
title: "İki öncelik kuyruğu ile kayan pencere medyanını hesaplama (C++)"
prompt: |
  n elemanlı bir vektörde boyutu k olan kayan bir pencerenin her adımındaki medyanı iki heap (max-heap ve min-heap) ile O(n log k) sürede hesaplayan `std::vector<double> median_sliding_window(const std::vector<int>& nums, size_t k)` fonksiyonunu yazın. n dizi boyutu ve k pencere boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n log k) olmalı"
  - "Ek bellek O(k) olmalı"
  - "Tembel silme (lazy deletion) veya std::multiset kullanılabilir"
expected:
  time: { median_sliding_window: "n log k" }
  space: "k"
concept_tags: [data-structures, performance]
checklist_extra:
  - "İki yarı arasındaki denge korunmuş mu?"
  - "Pencereden çıkan elemanlar doğru temizlenmiş mi?"
reference_solution_path: private/solutions/cpp-hard-sliding-window-median-heaps.cpp
hint_ladder:
  1: "Küçük yarıyı bir max-heap'te, büyük yarıyı bir min-heap'te dengeli olarak saklayın."
  2: "Pencere kaydıkça çıkan elemanı düşürüp yeni elemanı uygun yarıya ekleyerek medyanı hesaplayın."
  3: "Bu algoritma 'çift yığın ile kayan pencere medyanı (sliding window median with dual heaps)' olarak bilinir."
```

---

### cpp-hard-trapping-rain-water-2d

```yaml
id: cpp-hard-trapping-rain-water-2d
version: 1
language: cpp
engine: none
difficulty: hard
title: "2D yükseklik matrisinde biriken su miktarını hesaplama"
prompt: |
  n x m boyutundaki bir 3D arazi yükseklik matrisinde göllenerek birikebilecek toplam yağmur suyu hacmini min-heap ve BFS ile hesaplayan `int trap_rain_water_2d(const std::vector<std::vector<int>>& height_map)` fonksiyonunu yazın. n satır ve m sütun adedidir.
constraints:
  - "Zaman karmaşıklığı O(n * m log n) olmalı"
  - "Ek bellek O(n * m) olmalı"
  - "Dış sınırlar min-heap ile başlatılmalıdır"
expected:
  time: { trap_rain_water_2d: "n*m log n" }
  space: "n*m"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "Tüm dış kenar hücreleri başlangıçta heap'e eklenmiş mi?"
  - "İçeriye doğru min-heap ile genişleme yapılarak su toplanmış mı?"
reference_solution_path: private/solutions/cpp-hard-trapping-rain-water-2d.cpp
hint_ladder:
  1: "Izgaranın dış sınırındaki tüm hücreleri min-heap'e ekleyip ziyaret edildi olarak işaretleyin."
  2: "En alçak sınır hücresini çekip komşularını inceleyin; komşu daha alçaksa aradaki fark kadar su biriktirip komşuyu güncellenmiş tepe olarak heap'e ekleyin."
  3: "Bu algoritma 'iki boyutlu arazide yağmur suyu tutma (trapping rain water 2D)' olarak bilinir."
```

---

### cpp-hard-largest-rectangle-histogram

```yaml
id: cpp-hard-largest-rectangle-histogram
version: 1
language: cpp
engine: none
difficulty: hard
title: "Monotonik yığın ile histogramdaki en büyük dikdörtgen alanını bulma"
prompt: |
  n elemanlı çubuk yükseklikleri dizisinde oluşturulabilecek en büyük dikdörtgenin alanını monotonik artan yığın kullanarak O(n) sürede bulan `long long largest_rectangle_area(const std::vector<int>& heights)` fonksiyonunu yazın. n histogram çubuğu sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Her çubuk yığına bir kez girip bir kez çıkmalıdır"
expected:
  time: { largest_rectangle_area: "n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Yığında çubuk indeksleri monotonik artan sırada saklanmış mı?"
  - "Yığından çıkarılan çubuk için sol ve sağ sınırlar doğru hesaplanmış mı?"
reference_solution_path: private/solutions/cpp-hard-largest-rectangle-histogram.cpp
hint_ladder:
  1: "Yükseklik indekslerini monotonik artan bir yığında tutun."
  2: "Daha alçak bir çubuk görüldüğünde yığından elemanları çekerek genişliği (i - yığının yeni tepesi - 1) ve alanı hesaplayın."
  3: "Bu algoritma 'histogramda en büyük dikdörtgen alanı (largest rectangle in histogram)' olarak bilinir."
```

---

### cpp-hard-maximal-rectangle-matrix

```yaml
id: cpp-hard-maximal-rectangle-matrix
version: 1
language: cpp
engine: none
difficulty: hard
title: "Matriste en büyük 1'lerden oluşan dikdörtgeni bulma"
prompt: |
  Yalnızca '0' ve '1' karakterleri içeren n x m boyutundaki bir matriste tümüyle '1'lerden oluşan en büyük dikdörtgenin alanını histogram problemine indirgeyerek O(n * m) sürede bulan `int maximal_rectangle(const std::vector<std::vector<char>>& matrix)` fonksiyonunu yazın. n satır ve m sütun adedidir.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(m) olmalı"
  - "Her satır bir histogram olarak güncellenmelidir"
expected:
  time: { maximal_rectangle: "n*m" }
  space: "m"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Her satır için yükseklik dizisi birikimli güncellenmiş mi ('0' gelirse sıfırlanmış mı)?"
  - "Her satırda histogram çözümü çağrılmış mı?"
reference_solution_path: private/solutions/cpp-hard-maximal-rectangle-matrix.cpp
hint_ladder:
  1: "Her satır için m boyutunda bir yükseklik dizisi tutarak '1' gördükçe yüksekliği artırın, '0' görünce sıfırlayın."
  2: "Her satırda oluşan histogram için en büyük dikdörtgen alanını hesaplayıp genel maksimumu güncelleyin."
  3: "Bu algoritma 'matriste azami dikdörtgen alanı (maximal rectangle in 2D binary matrix)' olarak bilinir."
```

---

### cpp-hard-edit-distance-levenshtein

```yaml
id: cpp-hard-edit-distance-levenshtein
version: 1
language: cpp
engine: none
difficulty: hard
title: "İki metin arasındaki düzenleme mesafesini dinamik programlamayla bulma"
prompt: |
  word1 metnini word2 metnine dönüştürmek için gereken minimum ekleme, silme ve değiştirme işlem sayısını dinamik programlama ile hesaplayan `int min_distance(std::string_view word1, std::string_view word2)` fonksiyonunu yazın. n birinci ve m ikinci metnin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(m) olmalı (alan optimizasyonu yapılmış)"
  - "string_view kullanılmalıdır"
expected:
  time: { min_distance: "n*m" }
  space: "m"
concept_tags: [strings, performance]
checklist_extra:
  - "Karakterler eşitse dp[i-1][j-1] maliyetsiz aktarılmış mı?"
  - "Eşit değilse min(ekle, sil, değiştir) + 1 alınmış mı?"
reference_solution_path: private/solutions/cpp-hard-edit-distance-levenshtein.cpp
hint_ladder:
  1: "dp tablosunda dp[i][j] değerini word1[0...i] ile word2[0...j] arasındaki asgari işlem sayısı yapın."
  2: "Karakterler eşleşirse çaprazdan doğrudan geçin, eşleşmezse 3 olası operasyonun minimumuna 1 ekleyin."
  3: "Bu dinamik programlama algoritması 'Levenshtein düzenleme mesafesi (Levenshtein edit distance)' olarak bilinir."
```

---

### cpp-hard-regular-expression-matching

```yaml
id: cpp-hard-regular-expression-matching
version: 1
language: cpp
engine: none
difficulty: hard
title: "Düzenli ifadeleri dinamik programlamayla eşleştirme"
prompt: |
  '.' ve '*' meta-karakterlerini destekleyen bir p desenini s metni ile tam olarak eşleştiren `bool is_regex_match(std::string_view s, std::string_view p)` fonksiyonunu yazın. n metin ve m desen uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(n * m) olmalı"
  - "string_view kullanılmalıdır"
expected:
  time: { is_regex_match: "n*m" }
  space: "n*m"
concept_tags: [strings, edge-cases]
checklist_extra:
  - "p[j-1] == '*' durumunda sıfır eşleşme dp[i][j-2] doğru test edilmiş mi?"
  - "Nokta karakteri genel eşleşme sağlamış mı?"
reference_solution_path: private/solutions/cpp-hard-regular-expression-matching.cpp
hint_ladder:
  1: "dp[i][j] tablosunu s[0...i] ile p[0...j] eşleşme durumu olarak kurun."
  2: "'*' karakterinde sıfır tekrarı (dp[i][j-2]) veya bir önceki karakter metinle uyuşuyorsa bir tekrarı (dp[i-1][j]) kontrol edin."
  3: "Bu algoritma 'düzenli ifade dinamik programlama eşleşmesi (regular expression matching DP)' olarak bilinir."
```

---

### cpp-hard-wildcard-matching-dp

```yaml
id: cpp-hard-wildcard-matching-dp
version: 1
language: cpp
engine: none
difficulty: hard
title: "Joker karakterleri destekleyen desen eşleme"
prompt: |
  '?' (herhangi tek bir karakter) ve '*' (herhangi bir karakter dizisi, boş dahil) joker karakterlerini destekleyen p desenini s metni ile eşleştiren `bool is_wildcard_match(std::string_view s, std::string_view p)` fonksiyonunu yazın. n metin ve m desen uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(m) olmalı"
  - "string_view kullanılmalıdır"
expected:
  time: { is_wildcard_match: "n*m" }
  space: "m"
concept_tags: [strings, performance]
checklist_extra:
  - "p[j-1] == '*' için dp[i][j] = dp[i-1][j] || dp[i][j-1] geçişi uygulanmış mı?"
  - "Başlangıç deseni '*' olan durumlar doğru başlatılmış mı?"
reference_solution_path: private/solutions/cpp-hard-wildcard-matching-dp.cpp
hint_ladder:
  1: "dp tablosunu tanımlayın; p'de '*' gördükçe ya boş metinle eşleşin ya da metinden bir karakter tüketerek deseni koruyun."
  2: "İki satırlı DP kullanarak ek bellek kullanımını O(m) seviyesine optimize edin."
  3: "Bu algoritma 'joker karakter desen eşleştirme algoritması (wildcard matching DP)' olarak bilinir."
```

---

### cpp-hard-longest-valid-parentheses

```yaml
id: cpp-hard-longest-valid-parentheses
version: 1
language: cpp
engine: none
difficulty: hard
title: "En uzun geçerli parantez alt dizgisini bulma"
prompt: |
  Yalnızca '(' ve ')' karakterlerinden oluşan bir metin görünümündeki en uzun dengeli parantez alt dizgisinin uzunluğunu yığın veya iki geçişli sayaçla O(n) sürede bulan `int longest_valid_parentheses(std::string_view s)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (iki geçişli sayaç ile)"
  - "string_view kullanılmalıdır"
expected:
  time: { longest_valid_parentheses: "n" }
  space: "1"
concept_tags: [strings, performance]
checklist_extra:
  - "Soldan sağa ve sağdan sola iki geçiş yapılarak açık ve kapalı parantez dengesi gözetilmiş mi?"
  - "Sayaç sıfırlamaları doğru yapılmış mı?"
reference_solution_path: private/solutions/cpp-hard-longest-valid-parentheses.cpp
hint_ladder:
  1: "Soldan sağa gezerken '(' ve ')' sayılarını tutun; eşitlendiğinde uzunluğu güncelleyin, ')' aşarsa sıfırlayın."
  2: "Aynı işlemi sağdan sola tersine uygulayarak '(((())' gibi durumlarda da maksimum uzunluğu bulun."
  3: "Bu algoritma 'iki geçişte en uzun geçerli parantez bulma (longest valid parentheses two-pass)' olarak bilinir."
```

---

### cpp-hard-minimum-window-substring

```yaml
id: cpp-hard-minimum-window-substring
version: 1
language: cpp
engine: none
difficulty: hard
title: "Hedef karakterlerin tümünü içeren en küçük pencere alt dizgisini bulma"
prompt: |
  s metni içinde t metnindeki tüm karakterleri frekanslarıyla birlikte içeren en kısa kesintisiz alt dizgiyi kayan pencere ile bulan `std::string min_window(std::string_view s, std::string_view t)` fonksiyonunu yazın. Bulunamazsa boş dizgi dönmelidir. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) (ASCII frekans tabloları) olmalı"
  - "string_view kullanılmalıdır"
expected:
  time: { min_window: "n" }
  space: "1"
concept_tags: [strings, performance]
checklist_extra:
  - "Gereken karakter sayısı match_count ile takip edilmiş mi?"
  - "Sol sınır daraltılarak en kısa pencere saklanmış mı?"
reference_solution_path: private/solutions/cpp-hard-minimum-window-substring.cpp
hint_ladder:
  1: "t metninin karakter frekanslarını bir haritada tutun."
  2: "s metninde sağ işaretçiyi ilerletip tüm karakterler tamamlandığında, sol işaretçiyi mümkün olduğunca sağa çekerek en küçük pencereyi kaydedin."
  3: "Bu algoritma 'asgari pencere alt metni algoritması (minimum window substring)' olarak bilinir."
```

---

### cpp-hard-merge-k-sorted-lists-nodes

```yaml
id: cpp-hard-merge-k-sorted-lists-nodes
version: 1
language: cpp
engine: none
difficulty: hard
title: "Bağlı liste düğümlerini min-heap ile kopyalamadan birleştirme"
prompt: |
  Her biri sıralı k adet tek yönlü bağlı listenin düğüm göstericilerini std::priority_queue kullanarak yeni düğüm tahsis etmeden tek bir sıralı bağlı listede birleştiren `ListNode* merge_k_lists(std::vector<ListNode*>& lists)` fonksiyonunu yazın. n toplam düğüm sayısı ve k liste sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n log k) olmalı"
  - "Ek bellek O(k) olmalı"
  - "Yalancı (dummy) baş düğüm kullanılmalıdır"
expected:
  time: { merge_k_lists: "n log k" }
  space: "k"
concept_tags: [smart-pointers, data-structures]
checklist_extra:
  - "Min-heap karşılaştırıcısı düğüm değerlerini doğru sıralıyor mu?"
  - "Çekilen düğümün next düğümü hemen heap'e eklenmiş mi?"
reference_solution_path: private/solutions/cpp-hard-merge-k-sorted-lists-nodes.cpp
hint_ladder:
  1: "Tüm listelerin baş göstericilerini boyutu k olan bir min-heap'e yerleştirin."
  2: "En küçük düğümü çekip sonuç zincirine bağlayın ve çekilen düğümün next işaretçisini heap'e ekleyin."
  3: "Bu algoritma 'k adet sıralı bağlı listeyi yığınla birleştirme (merge k sorted linked lists with heap)' olarak bilinir."
```

---

### cpp-hard-reverse-nodes-in-k-group

```yaml
id: cpp-hard-reverse-nodes-in-k-group
version: 1
language: cpp
engine: none
difficulty: hard
title: "Bağlı listenin düğümlerini k elemanlık gruplar halinde tersine çevirme"
prompt: |
  Tek yönlü bir bağlı listenin düğümlerini her k düğümlük bloklar halinde yerinde tersine çeviren, son kalan k'dan az elemanlı bloğu ise olduğu gibi bırakan `ListNode* reverse_k_group(ListNode* head, int k)` fonksiyonunu yazın. n listedeki toplam düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "Düğüm değerleri değil göstericiler ters çevrilmelidir"
expected:
  time: { reverse_k_group: "n" }
  space: "1"
concept_tags: [data-structures, smart-pointers]
checklist_extra:
  - "Grupta en az k düğüm olup olmadığı önceden taranmış mı?"
  - "Grup ters çevrildikten sonra önceki ve sonraki parçalara doğru bağlanmış mı?"
reference_solution_path: private/solutions/cpp-hard-reverse-nodes-in-k-group.cpp
hint_ladder:
  1: "Önce önünüzde en az k adet düğüm olup olmadığını kontrol edin; yoksa dokunmadan dönün."
  2: "k adet düğümün göstericilerini yerinde ters çevirip bir sonraki bloğa özyinelemeli olarak bağlayın."
  3: "Bu algoritma 'bağlı liste düğümlerini k gruplarında tersine çevirme (reverse nodes in k-group)' olarak bilinir."
```

---

### cpp-hard-lfu-cache-implementation

```yaml
id: cpp-hard-lfu-cache-implementation
version: 1
language: cpp
engine: none
difficulty: hard
title: "En az sıklıkla kullanılan elemanları çıkaran LFU önbellek sınıfı"
prompt: |
  Kapasitesi dolduğunda kullanım frekansı en düşük olanı, eşitlik durumunda ise en eski kullanılanı (LRU) çıkaran ve get/put işlemlerini O(1) sürede yapan `class LFUCache` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı her işlem için O(1) olmalı"
  - "Ek bellek O(capacity) olmalı"
  - "Frekans listeleri ve min_frequency takibi yapılmalıdır"
expected:
  time: { LFUCache: "1" }
  space: "1"
concept_tags: [lru-cache, hash-map]
checklist_extra:
  - "min_frequency değişkeni doğru güncellenmiş mi?"
  - "Her frekans için çift yönlü liste ve anahtar eşleşmesi tutulmuş mu?"
reference_solution_path: private/solutions/cpp-hard-lfu-cache-implementation.cpp
hint_ladder:
  1: "Her elemanın değerini ve frekansını bir haritada, her frekansa ait elemanları çift yönlü listelerde saklayın."
  2: "Erişilen elemanın frekansını artırıp bir üst frekans listesine taşıyın ve min_frequency değerini güncelleyin."
  3: "Bu veri yapısı mekanizması 'en az sıklıkla kullanılan önbellek (LFU cache implementation)' olarak bilinir."
```

---

### cpp-hard-all-o1-data-structure

```yaml
id: cpp-hard-all-o1-data-structure
version: 1
language: cpp
engine: none
difficulty: hard
title: "Tüm sorguları O(1) sürede yapan veri yapısı"
prompt: |
  Metin anahtarları için inc(key), dec(key), get_max_key() ve get_min_key() operasyonlarının tamamını O(1) sürede gerçekleştiren `class AllOne` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı tüm operasyonlar için O(1) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Çift yönlü kova listesi ve karma haritası kullanılmalıdır"
expected:
  time: { AllOne: "1" }
  space: "1"
concept_tags: [data-structures, hash-map]
checklist_extra:
  - "Frekans kovaları çift yönlü liste ile sıralı tutulmuş mu?"
  - "Boşalan kovalar listeden silinmiş mi?"
reference_solution_path: private/solutions/cpp-hard-all-o1-data-structure.cpp
hint_ladder:
  1: "Aynı frekansa sahip anahtarları bir kümede tutan sıralı kova (Bucket) düğümlerinden oluşan bir çift yönlü liste kurun."
  2: "Artırma ve azaltmalarda anahtarı komşu kovaya taşıyarak listenin başından min_key, sonundan max_key değerlerini O(1) sürede okuyun."
  3: "Bu gelişmiş veri yapısı 'tüm işlemleri sabit sürede yapan yapı (All O-one data structure)' olarak bilinir."
```

---

### cpp-hard-binary-tree-max-path-sum

```yaml
id: cpp-hard-binary-tree-max-path-sum
version: 1
language: cpp
engine: none
difficulty: hard
title: "İkili ağaçta herhangi iki düğüm arasındaki maksimum yol toplamını hesaplama"
prompt: |
  İkili bir ağacın herhangi bir düğümünden başlayıp herhangi bir düğümünde biten ve her düğümün en fazla bir kez kullanıldığı yollar arasındaki maksimum toplamı bulan `int max_path_sum(TreeNode* root)` fonksiyonunu yazın. n ağaçtaki düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek çağrı yığını için O(log n) olmalı"
  - "Negatif katkılar max(0, gain) ile budanmalıdır"
expected:
  time: { max_path_sum: "n" }
  space: "log n"
concept_tags: [trees, edge-cases]
checklist_extra:
  - "Alt ağaçtan gelen negatif yollar sıfırlanarak elenmiş mi?"
  - "Global maksimum her düğümde sol + sağ + kök toplamıyla güncellenmiş mi?"
reference_solution_path: private/solutions/cpp-hard-binary-tree-max-path-sum.cpp
hint_ladder:
  1: "Her düğüm için ebeveyne iletilebilecek tek taraflı maksimum kazancı max(0, subtree_sum) ile hesaplayın."
  2: "O düğümden geçen çatallı yolu (root + left + right) hesaplayarak global maksimum ile kıyaslayın."
  3: "Bu algoritma 'ikili ağaçta azami yol toplamı (binary tree maximum path sum)' olarak bilinir."
```

---

### cpp-hard-word-ladder-two-bfs

```yaml
id: cpp-hard-word-ladder-two-bfs
version: 1
language: cpp
engine: none
difficulty: hard
title: "Başlangıç sözcüğünden hedef sözcüğe en kısa dönüşüm yollarını çıkarma"
prompt: |
  Tek harf değişimleriyle begin_word'den end_word'e ulaşan tüm en kısa dönüşüm zincirlerini BFS ile seviye grafiği kurup geri izleme ile bulan `std::vector<std::vector<std::string>> find_ladders(std::string_view begin_word, std::string_view end_word, const std::vector<std::string>& word_list)` fonksiyonunu yazın. n sözlük boyutu ve m sözcük uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(n) olmalı"
  - "BFS ile en kısa mesafe seviyesi belirlenmelidir"
expected:
  time: { find_ladders: "n*m" }
  space: "n"
concept_tags: [strings, data-structures]
checklist_extra:
  - "BFS sırasında kelimeler aynı seviyede paylaşılabilecek şekilde ziyaret edilmiş mi?"
  - "DFS geri izleme ile tüm yollar toplanmış mı?"
reference_solution_path: private/solutions/cpp-hard-word-ladder-two-bfs.cpp
hint_ladder:
  1: "BFS ile sözcükler arası ebeveyn-çocuk ilişkilerini ve en kısa adımı çıkarın."
  2: "Hedefe ulaşıldığında DFS ile ebeveyn haritasını geriye doğru takip ederek tüm en kısa yolları toplayın."
  3: "Bu algoritma 'sözcük merdiveni en kısa yolları (word ladder II BFS-DFS)' olarak bilinir."
```

---

### cpp-hard-n-queens-puzzle

```yaml
id: cpp-hard-n-queens-puzzle
version: 1
language: cpp
engine: none
difficulty: hard
title: "Satranç tahtasına n veziri birbirini tehdit etmeyecek şekilde yerleştirme"
prompt: |
  n x n boyutundaki satranç tahtasına n adet veziri hiçbir vezirin aynı satır, sütun veya çaprazda yer almayacağı tüm geçerli dizilimleri std::vector<std::vector<std::string>> olarak üreten `std::vector<std::vector<std::string>> solve_n_queens(int n)` fonksiyonunu yazın. n tahta boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n!) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Bit maskeleri veya boolean dizileriyle kısıt denetimi yapılmalıdır"
expected:
  time: { solve_n_queens: "n!" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Sütun, sol çapraz ve sağ çapraz bayrakları O(1) sürede denetlenmiş mi?"
  - "Tüm çözümler tahta formatında oluşturulmuş mu?"
reference_solution_path: private/solutions/cpp-hard-n-queens-puzzle.cpp
hint_ladder:
  1: "Satır satır ilerleyerek her satıra bir vezir yerleştirin."
  2: "Sütun (cols), sol çapraz (row - col) ve sağ çapraz (row + col) kümelerini kullanarak çakışmaları O(1) sürede engelleyin."
  3: "Bu klasik problem 'N-Vezir geri izleme algoritması (N-Queens backtracking puzzle)' olarak bilinir."
```

---

### cpp-hard-sudoku-solver-backtrack

```yaml
id: cpp-hard-sudoku-solver-backtrack
version: 1
language: cpp
engine: none
difficulty: hard
title: "Sudoku tablosunu kısıt yayılımı ve geri izleme ile çözme"
prompt: |
  9x9 boyutundaki kısmen doldurulmuş Sudoku tahtasını satır, sütun ve 3x3 kutu kurallarını bit maskesiyle denetleyerek yerinde çözen `void solve_sudoku(std::vector<std::vector<char>>& board)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) (sabit 9x9 tahta için) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Çözüm bulunduğunda hemen geri dönülmelidir"
expected:
  time: { solve_sudoku: "1" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Satır, sütun ve 3x3 kutu bit maskeleri tutulmuş mu?"
  - "Geri izlemede geçersiz deneme geri alınmış mı?"
reference_solution_path: private/solutions/cpp-hard-sudoku-solver-backtrack.cpp
hint_ladder:
  1: "Her satır, sütun ve 3x3 blok için kullanılan rakamları 9-bit maskelerde saklayın."
  2: "Boş hücrelere 1-9 arası uygun adayları deneyerek geri izleme yapın ve çözüm bulununca sonlandırın."
  3: "Bu algoritma 'Sudoku çözücü geri izleme algoritması (Sudoku solver backtracking)' olarak bilinir."
```

---

### cpp-hard-alien-dictionary-topological

```yaml
id: cpp-hard-alien-dictionary-topological
version: 1
language: cpp
engine: none
difficulty: hard
title: "Uzaylı alfabesindeki harflerin sözlük sırasını topolojik sıralamayla bulma"
prompt: |
  Sözlük sırasına göre sıralanmış sözcük listesinden harfler arası öncelik ilişkilerini çıkararak uzaylı alfabesinin geçerli harf sıralamasını dizgi olarak bulan `std::string alien_order(const std::vector<std::string>& words)` fonksiyonunu yazın. Geçersizlik veya döngüde boş metin dönmelidir. n sözcük ve m toplam karakter sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n + m) olmalı"
  - "Ek bellek O(1) (26 harf) olmalı"
  - "Kahn topolojik sıralama uygulanmalıdır"
expected:
  time: { alien_order: "n + m" }
  space: "1"
concept_tags: [data-structures, strings]
checklist_extra:
  - "Ardışık kelimelerin ilk farklılaşan harfi yönlü kenar olarak eklenmiş mi?"
  - "Önek hatası (ör. 'abc' ardından 'ab') geçersiz sayılmış mı?"
reference_solution_path: private/solutions/cpp-hard-alien-dictionary-topological.cpp
hint_ladder:
  1: "Komşu iki kelimenin ilk farklılaşan harflerini bularak yönlü bir bağımlılık grafiği kurun."
  2: "Grafik üzerinde topolojik sıralama uygulayarak tüm harflerin sıralamasını elde edin; döngü varsa boş dönün."
  3: "Bu çizge problemi 'uzaylı sözlüğü topolojik sıralaması (alien dictionary topological sort)' olarak bilinir."
```

---

### cpp-hard-tarjan-scc-directed

```yaml
id: cpp-hard-tarjan-scc-directed
version: 1
language: cpp
engine: none
difficulty: hard
title: "Yönlü çizgedeki tüm güçlü bağlı bileşenleri Tarjan ile bulma"
prompt: |
  n düğümlü yönlü bir çizgedeki tüm güçlü bağlı bileşenleri (SCC) Tarjan algoritmasıyla tek bir DFS geçişinde bularak std::vector<std::vector<int>> olarak döndüren `std::vector<std::vector<int>> find_scc(size_t n, const std::vector<std::pair<int, int>>& edges)` fonksiyonunu yazın. m kenar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n + m) olmalı"
  - "Ek bellek O(n) olmalı"
  - "dfn ve lowlink dizileri tutulmalıdır"
expected:
  time: { find_scc: "n + m" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Keşif zamanı ve en düşük ulaşılabilir zaman doğru güncellenmiş mi?"
  - "Düğüm kök olduğunda yığından bileşen boşaltılmış mı?"
reference_solution_path: private/solutions/cpp-hard-tarjan-scc-directed.cpp
hint_ladder:
  1: "DFS sırasında her düğüme keşif zamanı (tin) ve lowlink değeri atayın."
  2: "lowlink değeri keşif zamanına eşit olan düğümlerde yığındaki elemanları çekerek güçlü bileşeni tamamlayın."
  3: "Bu çizge algoritması 'Tarjan güçlü bağlı bileşenler algoritması (Tarjan's strongly connected components)' olarak bilinir."
```

---

### cpp-hard-critical-connections-bridges

```yaml
id: cpp-hard-critical-connections-bridges
version: 1
language: cpp
engine: none
difficulty: hard
title: "Çizgedeki kritik köprü kenarları Tarjan köprü algoritmasıyla tespit etme"
prompt: |
  n sunucu ve bağlantı kenarları içeren ağda, kaldırıldığında sunucuların birbirinden kopmasına neden olan kritik bağlantıları (köprüleri) bulan `std::vector<std::vector<int>> critical_connections(int n, const std::vector<std::vector<int>>& connections)` fonksiyonunu yazın. m kenar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n + m) olmalı"
  - "Ek bellek O(n) olmalı"
  - "low[v] > tin[u] koşulu denetlenmelidir"
expected:
  time: { critical_connections: "n + m" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Ebeveyn kenara geri dönülmesi DFS'te engellenmiş mi?"
  - "low[v] > tin[u] olan kenarlar köprü listesine eklenmiş mi?"
reference_solution_path: private/solutions/cpp-hard-critical-connections-bridges.cpp
hint_ladder:
  1: "Yönsüz grafikte DFS ile her düğüme keşif zamanı ve low değeri atayın."
  2: "Çocuk v için low[v] > tin[u] ise (u, v) kenarı silindiğinde v'nin u'ya başka bir alternatif yolu yoktur; bu kenar bir köprüdür."
  3: "Bu algoritma 'çizgede köprü kenar tespiti (bridge finding algorithm in graph)' olarak bilinir."
```

---

### cpp-hard-network-flow-dinic

```yaml
id: cpp-hard-network-flow-dinic
version: 1
language: cpp
engine: none
difficulty: hard
title: "Dinic algoritması ve seviye çizgesiyle azami ağ akışını hesaplama"
prompt: |
  n düğümlü bir akış ağında src kaynağından sink hedefine azami akışı BFS ile seviye grafiği kurup DFS ile engelleyici akışları (blocking flow) bularak hesaplayan `long long max_flow_dinic(size_t n, size_t src, size_t sink, const std::vector<std::tuple<size_t, size_t, long long>>& edges)` fonksiyonunu yazın. m kenar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n^2 * m) olmalı"
  - "Ek bellek O(n + m) olmalı"
  - "Seviye grafiği ve çalışma işaretçisi (current arc) tutulmalıdır"
expected:
  time: { max_flow_dinic: "n^2 * m" }
  space: "n + m"
concept_tags: [data-structures, performance]
checklist_extra:
  - "BFS ile seviye grafiği (level array) doğru kurulmuş mu?"
  - "DFS'te gereksiz kenarları tekrar denememek için ptr dizisi kullanılmış mı?"
reference_solution_path: private/solutions/cpp-hard-network-flow-dinic.cpp
hint_ladder:
  1: "BFS ile artık kapasitesi olan kenarlar üzerinden her düğüme bir mesafe seviyesi atayın."
  2: "Sadece bir sonraki seviyeye giden kenarlar üzerinden DFS ile engelleyici akış gönderip artık kapasiteleri güncelleyin."
  3: "Bu ağ akış algoritması 'Dinic azami akış algoritması (Dinic's maximum flow algorithm)' olarak bilinir."
```

---

### cpp-hard-min-cost-max-flow

```yaml
id: cpp-hard-min-cost-max-flow
version: 1
language: cpp
engine: none
difficulty: hard
title: "Artık çizgede en az maliyetli azami akışı bulma"
prompt: |
  n düğümlü bir ağda akış gönderirken birim kenar maliyetlerini de hesaba katarak toplam maliyeti en küçük olan maksimum akışı hesaplayan `std::pair<long long, long long> min_cost_max_flow(size_t n, size_t src, size_t sink, const std::vector<std::tuple<size_t, size_t, long long, long long>>& edges)` fonksiyonunu yazın. m kenar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n * m) her artırımda olmalı"
  - "Ek bellek O(n + m) olmalı"
  - "SPFA veya potansiyel destekli Dijkstra kullanılmalıdır"
expected:
  time: { min_cost_max_flow: "n*m" }
  space: "n + m"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Ters kenarlar negatif maliyetle oluşturulmuş mu?"
  - "Akış ve maliyet çifti doğru hesaplanmış mı?"
reference_solution_path: private/solutions/cpp-hard-min-cost-max-flow.cpp
hint_ladder:
  1: "Her adımda artık kapasitesi pozitif olan kenarlar üzerinde en küçük maliyetli genişletici yolu bulun."
  2: "Bu yol boyunca akış göndererek toplam akışı ve toplam birikimli maliyeti artırın."
  3: "Bu çizge optimizasyonu 'asgari maliyetli azami akış algoritması (minimum-cost maximum-flow)' olarak bilinir."
```

---

### cpp-hard-segment-tree-range-update

```yaml
id: cpp-hard-segment-tree-range-update
version: 1
language: cpp
engine: none
difficulty: hard
title: "Tembel yayılım ile aralık toplamı ve aralık güncelleme ağacı (C++)"
prompt: |
  n elemanlı bir vektör üzerinde aralık toplama (range add) ve aralık toplamı sorgulama işlemlerini O(log n) sürede gerçekleştiren `class LazySegmentTree` sınıfını yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Tembel etiketler push-down ile yayılmalıdır"
expected:
  time: { LazySegmentTree: "log n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Aralık tam örtüştüğünde tembel değer atanıp dönülmüş mü?"
  - "Kısmi örtüşmede push_down yapılarak çocuklara iletilmiş mi?"
reference_solution_path: private/solutions/cpp-hard-segment-tree-range-update.cpp
hint_ladder:
  1: "4n boyutunda bir ağaç ve tembel etiket dizisi açın."
  2: "Aralık güncellemelerinde tembel değeri düğüme kaydedin; sorgularda veya alt dallara inerken bekleyen değeri çocuklara iletin."
  3: "Bu veri yapısı mekanizması 'tembel yayılımlı kesim ağacı (lazy segment tree)' olarak bilinir."
```

---

### cpp-hard-fenwick-tree-2d

```yaml
id: cpp-hard-fenwick-tree-2d
version: 1
language: cpp
engine: none
difficulty: hard
title: "İki boyutlu ızgarada alt matris toplamlarını logaritmik sürede sorgulama"
prompt: |
  n x m boyutundaki bir ızgarada tekil hücre güncellemelerini ve (0,0)'dan (r,c)'ye alt matris toplamlarını O(log n * log m) sürede yapan `class FenwickTree2D` sınıfını yazın. n satır ve m sütun adedidir.
constraints:
  - "Zaman karmaşıklığı O(log n * log m) olmalı"
  - "Ek bellek O(n * m) olmalı"
  - "İki boyutlu en düşük anlamlı bit (LSB) kaydırmaları yapılmalıdır"
expected:
  time: { FenwickTree2D: "log n * log m" }
  space: "n*m"
concept_tags: [data-structures, performance]
checklist_extra:
  - "1 tabanlı indeksleme kuralına uyulmuş mu?"
  - "İç içe döngülerde i += i & -i ve j += j & -j uygulanmış mı?"
reference_solution_path: private/solutions/cpp-hard-fenwick-tree-2d.cpp
hint_ladder:
  1: "İki boyutlu bir ağaç matrisi tutun."
  2: "Hücre güncellerken hem satır hem sütun indekslerinde en düşük anlamlı biti (index & -index) ekleyerek ilerleyin."
  3: "Bu veri yapısı 'iki boyutlu ikili indeksli ağaç (2D Fenwick tree)' olarak bilinir."
```

---

### cpp-hard-heavy-light-tree-queries

```yaml
id: cpp-hard-heavy-light-tree-queries
version: 1
language: cpp
engine: none
difficulty: hard
title: "Ağaçta iki düğüm arasındaki en büyük değeri ağır-hafif ayrıştırmasıyla sorgulama"
prompt: |
  n düğümlü bir ağaçta düğüm değerlerini güncelleyen ve iki düğüm arasındaki yoldaki maksimum değeri O(log^2 n) sürede sorgulayan `class HLDTree` sınıfını yazın. n düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı yol sorgusu için O(log n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Ağır zincirler kesim ağacıyla eşleştirilmelidir"
expected:
  time: { HLDTree: "log n" }
  space: "n"
concept_tags: [trees, data-structures]
checklist_extra:
  - "En büyük alt ağaç ağır çocuk seçilmiş mi?"
  - "Zincir başları arasındaki atlamalarla kesim ağacından aralık maksimumu sorgulanmış mı?"
reference_solution_path: private/solutions/cpp-hard-heavy-light-tree-queries.cpp
hint_ladder:
  1: "Ağacı ağır ve hafif zincirlere ayırarak her düğüme tek boyutlu düz bir dizi indeksi atayın."
  2: "İki düğüm arasındaki yolda ilerlerken aynı zincirdeki parçaları kesim ağacından logaritmik sürede sorgulayın."
  3: "Bu ağaç sorgu tekniği 'ağır-hafif ağaç ayrıştırması (heavy-light decomposition)' olarak bilinir."
```

---

### cpp-hard-treap-implicit-split-merge

```yaml
id: cpp-hard-treap-implicit-split-merge
version: 1
language: cpp
engine: none
difficulty: hard
title: "Örtük anahtarlı Treap ile aralık ters çevirme ve bölme operasyonları"
prompt: |
  Dizi indislerini örtük anahtar olarak kullanan, split ve merge operasyonlarıyla belirli bir alt diziyi O(log n) sürede tersine çeviren `class ImplicitTreap` sınıfını yazın. n eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Tembel etiketler (lazy reverse) aşağı yayılmalıdır"
expected:
  time: { ImplicitTreap: "log n" }
  space: "n"
concept_tags: [trees, data-structures]
checklist_extra:
  - "Rastgele önceliklerle yığın (heap) kuralı korunmuş mu?"
  - "Alt ağaç boyutları doğru güncellenmiş mi?"
reference_solution_path: private/solutions/cpp-hard-treap-implicit-split-merge.cpp
hint_ladder:
  1: "Her düğüme rastgele bir öncelik (priority) ve alt ağaç boyutu (size) atayın."
  2: "Aralık işlemlerini ağacı split ile bölüp, işlemi tembel bayrakla uygulayıp tekrar merge ile birleştirerek tamamlayın."
  3: "Bu veri yapısı mekanizması 'örtük anahtarlı ağaç-yığın yapısı (implicit treap split and merge)' olarak bilinir."
```

---

### cpp-hard-suffix-automaton-string

```yaml
id: cpp-hard-suffix-automaton-string
version: 1
language: cpp
engine: none
difficulty: hard
title: "Metin için doğrusal sürede son ek otomatı oluşturma"
prompt: |
  n karakterli bir metnin tüm alt dizgilerini tanıyan son ek otomatını (Suffix Automaton) O(n) zaman ve alanda çevrimiçi (online) inşa eden `class SuffixAutomaton` sınıfını yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) doğrusal olmalı"
  - "Ek bellek O(n) olmalı"
  - "Bağlantı kopyalama (clone node) adımları uygulanmalıdır"
expected:
  time: { SuffixAutomaton: "n" }
  space: "n"
concept_tags: [strings, data-structures]
checklist_extra:
  - "Düğümlerin len ve link alanları doğru bağlanmış mı?"
  - "len[q] == len[p] + 1 koşuluna göre klon düğüm oluşturulmuş mu?"
reference_solution_path: private/solutions/cpp-hard-suffix-automaton-string.cpp
hint_ladder:
  1: "Metne her yeni karakter eklendiğinde otomat durumunu güncelleyin."
  2: "Gerektiğinde geçişleri ayırmak için klon düğüm oluşturup bağlantı işaretçilerini yönlendirin."
  3: "Bu gelişmiş metin otomatı 'son ek otomatı inşası (suffix automaton construction)' olarak bilinir."
```

---

### cpp-hard-aho-corasick-multi-pattern

```yaml
id: cpp-hard-aho-corasick-multi-pattern
version: 1
language: cpp
engine: none
difficulty: hard
title: "Çoklu desen aramak için Aho-Corasick durum makinesi"
prompt: |
  Verilen sözlükteki desenleri Trie ağacında toplayıp BFS ile başarısızlık bağlantılarını (failure links) kurarak metin üzerinde tek geçişte tüm eşleşmeleri bulan `class AhoCorasick` sınıfını yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) metin tarama için olmalı"
  - "Ek bellek O(k) olmalı (k toplam desen karakter sayısı)"
  - "BFS ile failure ve dictionary suffix bağlantıları kurulmalıdır"
expected:
  time: { AhoCorasick: "n" }
  space: "k"
concept_tags: [strings, data-structures]
checklist_extra:
  - "Failure linkleri seviye seviye BFS ile doğru oluşturulmuş mu?"
  - "Eşleşen desenler çıktı bağlantılarından toplanmış mı?"
reference_solution_path: private/solutions/cpp-hard-aho-corasick-multi-pattern.cpp
hint_ladder:
  1: "Desenlerden bir önek ağacı (Trie) kurun."
  2: "BFS ile her düğüme uyuşmazlık anında geri çekileceği en uzun geçerli önek düğümünü (failure link) bağlayın."
  3: "Bu durum makinesi 'Aho-Corasick çoklu desen eşleme algoritması (Aho-Corasick automaton)' olarak bilinir."
```

---

### cpp-hard-manacher-palindrome-linear

```yaml
id: cpp-hard-manacher-palindrome-linear
version: 1
language: cpp
engine: none
difficulty: hard
title: "Doğrusal sürede en uzun palindromik alt dizgiyi bulma"
prompt: |
  Verilen bir metin görünümündeki en uzun palindromik alt metni Manacher algoritmasıyla simetri aynalama tekniğini kullanarak O(n) sürede bulan `std::string longest_palindrome_linear(std::string_view s)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) doğrusal olmalı"
  - "Ek bellek O(n) olmalı"
  - "Karakterler arasına ayraç konulmalıdır"
expected:
  time: { longest_palindrome_linear: "n" }
  space: "n"
concept_tags: [strings, performance]
checklist_extra:
  - "Metin '#' karakterleriyle genişletilmiş mi?"
  - "Sağ sınır r ve merkez c doğru güncellenmiş mi?"
reference_solution_path: private/solutions/cpp-hard-manacher-palindrome-linear.cpp
hint_ladder:
  1: "Karakterler arasına özel ayraçlar koyarak çift uzunluklu palindromları tek merkezli forma sokun."
  2: "Daha önce hesaplanan simetrik noktanın yarıçapını taban alarak gereksiz karşılaştırmalardan kaçının."
  3: "Bu algoritma 'Manacher en uzun palindrom algoritması (Manacher's palindrome algorithm)' olarak bilinir."
```

---

### cpp-hard-disjoint-set-rollback

```yaml
id: cpp-hard-disjoint-set-rollback
version: 1
language: cpp
engine: none
difficulty: hard
title: "Kontrol noktası oluşturup geri alma destekleyen ayrık küme"
prompt: |
  Yol sıkıştırması yerine rütbe birleştirme (union by rank) kullanan ve yapılan birleştirme işlemlerini bir yığında saklayarak snapshot/rollback operasyonlarını O(log n) sürede destekleyen `class RollbackDSU` sınıfını yazın. n eleman adedidir.
constraints:
  - "Zaman karmaşıklığı birleştirme/geri alma için O(log n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Yol sıkıştırması yapılmamalıdır (geri alma için)"
expected:
  time: { RollbackDSU: "log n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Değişen ebeveyn ve rütbe değerleri geçmiş yığınına kaydedilmiş mi?"
  - "rollback çağrısında değerler eski haline getirilmiş mi?"
reference_solution_path: private/solutions/cpp-hard-disjoint-set-rollback.cpp
hint_ladder:
  1: "Geri alma geçmişini korumak için yol sıkıştırması yapmadan rütbeye göre birleştirin."
  2: "Her birleştirmede değişen düğümün eski ebeveyn ve rütbe değerini bir geçmiş yığınına atıp rollback anında geri yükleyin."
  3: "Bu veri yapısı mekanizması 'geri alınabilir ayrık küme yapısı (rollback disjoint set union)' olarak bilinir."
```

---

### cpp-hard-red-black-tree-map

```yaml
id: cpp-hard-red-black-tree-map
version: 1
language: cpp
engine: none
difficulty: hard
title: "Kırmızı-siyah ağaç tabanlı sıralı anahtar-değer haritası tasarlama"
prompt: |
  Düğümlerin kırmızı ve siyah renk özelliklerini, sol/sağ döndürmelerini ve renk onarım adımlarını uygulayarak O(log n) garantili ekleme ve arama sunan `class RedBlackMap` sınıfını yazın. n eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Kökün daima siyah olması garanti edilmelidir"
expected:
  time: { RedBlackMap: "log n" }
  space: "n"
concept_tags: [trees, data-structures]
checklist_extra:
  - "Amca düğümün rengine göre renklendirme ve döndürme durumları doğru ayrılmış mı?"
  - "Bellek sızıntısı önlenmiş mi?"
reference_solution_path: private/solutions/cpp-hard-red-black-tree-map.cpp
hint_ladder:
  1: "Yeni elemanı kırmızı bir yaprak olarak ekleyin."
  2: "Ebeveyn kırmızı olduğunda amca düğümün rengine göre yeniden renklendirme veya sol/sağ döndürme yaparak dengeyi koruyun."
  3: "Bu dengeli ağaç yapısı 'kırmızı-siyah ağaç eşlemesi (red-black tree map)' olarak bilinir."
```

---

### cpp-hard-b-tree-disk-optimized

```yaml
id: cpp-hard-b-tree-disk-optimized
version: 1
language: cpp
engine: none
difficulty: hard
title: "Sabit blok boyutuyla optimize B-Ağacı arama ve düğüm bölme"
prompt: |
  Her düğümünde t ile 2t - 1 arasında anahtar tutan, düğüm dolduğunda ortanca elemanı ebeveyne fırlatarak bölünen B-Ağacı ekleme ve arama mantığına sahip `class BTree` sınıfını yazın. n anahtar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(log n) olmalı"
  - "Kök bölündüğünde yeni bir kök atanmalıdır"
expected:
  time: { BTree: "log n" }
  space: "log n"
concept_tags: [trees, data-structures]
checklist_extra:
  - "Dolu düğümler aşağı inerken önceden bölünmüş mü?"
  - "Ortanca eleman ebeveyne doğru aktarılmış mı?"
reference_solution_path: private/solutions/cpp-hard-b-tree-disk-optimized.cpp
hint_ladder:
  1: "Ağaçta aşağı inerken karşılaşılan tüm dolu düğümleri bölerek tek geçişte ekleme garantisi sağlayın."
  2: "Kök dolduğunda yüksekliği bir artırıp eski kökü bölün."
  3: "Bu veritabanı indeks veri yapısı 'B-Ağacı düğüm bölme ve arama (B-tree indexing)' olarak bilinir."
```

---

### cpp-hard-skip-list-map

```yaml
id: cpp-hard-skip-list-map
version: 1
language: cpp
engine: none
difficulty: hard
title: "Çok seviyeli atlama listesi ile sıralı harita gerçekleştirimi"
prompt: |
  Rastgele belirlenen geometrik seviyelerle bağlantılı işaretçiler üzerinden O(log n) ortalama sürede arama, ekleme ve silme desteği sunan `class SkipListMap` sınıfını yazın. n eleman sayısıdır.
constraints:
  - "Ortalama zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "İleri yönlü işaretçi dizisi (forward array) doğru güncellenmelidir"
expected:
  time: { SkipListMap: "log n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Rastgele seviye üretimi (yazı-tura mantığı) yapılmış mı?"
  - "Güncellenecek önceki işaretçiler update dizisinde toplanmış mı?"
reference_solution_path: private/solutions/cpp-hard-skip-list-map.cpp
hint_ladder:
  1: "En üst seviyeden başlayarak hedef anahtardan küçük olan en sağdaki düğüme kadar ilerleyin."
  2: "Yeni düğüm eklerken rastgele bir yükseklik belirleyip tüm alt seviyelerdeki işaretçileri bağlayın."
  3: "Bu olasılıksal veri yapısı 'atlama listesi sıralı haritası (skip list map)' olarak bilinir."
```

---

### cpp-hard-expression-parser-ast

```yaml
id: cpp-hard-expression-parser-ast
version: 1
language: cpp
engine: none
difficulty: hard
title: "Aritmetik ifadeleri soyut sözdizim ağacına dönüştüren ayrıştırıcı"
prompt: |
  +, -, *, /, parantez ve sayı içeren bir matematiksel metni özyinelemeli iniş (recursive descent) ile ayrıştırıp AST kök düğümünü ve değerlendirme (eval) fonksiyonunu sunan `class ExpressionParser` sınıfını yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "std::unique_ptr ile AST düğümleri yönetilmelidir"
expected:
  time: { ExpressionParser: "n" }
  space: "n"
concept_tags: [trees, smart-pointers]
checklist_extra:
  - "Operatör öncelikleri (çarpma/bölme önce, toplama/çıkarma sonra) doğru kurgulanmış mı?"
  - "Bellek sızıntısı akıllı işaretçilerle engellenmiş mi?"
reference_solution_path: private/solutions/cpp-hard-expression-parser-ast.cpp
hint_ladder:
  1: "Gramer kurallarını expr -> term -> factor seviyelerine ayırın."
  2: "Her seviyede özyinelemeli fonksiyon çağırarak operatör önceliklerine uygun bir AST ağacı kurun."
  3: "Bu derleyici tekniği 'özyinelemeli iniş ifade ayrıştırıcısı (recursive descent expression parser)' olarak bilinir."
```

---

### cpp-hard-burst-balloons-dp

```yaml
id: cpp-hard-burst-balloons-dp
version: 1
language: cpp
engine: none
difficulty: hard
title: "Balon patlatma oyununda maksimum altın kazancını hesaplama"
prompt: |
  n elemanlı pozitif sayılar dizisinde balonları patlatırken nums[left] * nums[i] * nums[right] puanı toplayan ve maksimum puanı aralık dinamik programlamasıyla bulan `int max_coins(const std::vector<int>& nums)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n^3) olmalı"
  - "Ek bellek O(n^2) olmalı"
  - "Sınırlar 1 ile genişletilmelidir"
expected:
  time: { max_coins: "n^3" }
  space: "n^2"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Dizi başına ve sonuna sanal 1 elemanları eklenmiş mi?"
  - "En son patlatılan balon k pivotu seçilerek DP geçişi kurulmuş mu?"
reference_solution_path: private/solutions/cpp-hard-burst-balloons-dp.cpp
hint_ladder:
  1: "Dizinin iki ucuna 1 ekleyip aralık DP kurun."
  2: "(left, right) aralığında en son patlayacak balonu k seçerek dp[left][right] = max(dp[left][k] + dp[k][right] + nums[left]*nums[k]*nums[right]) geçişini hesaplayın."
  3: "Bu algoritma 'aralık dinamik programlaması ile balon patlatma (burst balloons interval DP)' olarak bilinir."
```

---

### cpp-hard-tsp-bitmask-dp

```yaml
id: cpp-hard-tsp-bitmask-dp
version: 1
language: cpp
engine: none
difficulty: hard
title: "Gezgin Satıcı Problemini bit maskeli dinamik programlamayla çözme"
prompt: |
  n şehir arasındaki mesafe matrisi verildiğinde tüm şehirleri bir kez ziyaret edip başlangıca dönen en kısa tur uzunluğunu O(n^2 * 2^n) sürede çözen `int solve_tsp(const std::vector<std::vector<int>>& dist)` fonksiyonunu yazın. n <= 16 kabul edilir. n şehir sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n^2) alt problem geçişleriyle olmalı"
  - "Ek bellek O(n) olmalı"
  - "Bit maskesi (1 << n) durumları tutulmalıdır"
expected:
  time: { solve_tsp: "n^2" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Ziyaret edilen şehirler kümesi bit maskesiyle ifade edilmiş mi?"
  - "Başlangıç şehrine dönüş mesafesi eklenmiş mi?"
reference_solution_path: private/solutions/cpp-hard-tsp-bitmask-dp.cpp
hint_ladder:
  1: "dp[mask][u] değerini u şehrinde bulunup mask ile belirtilen şehirlerin ziyaret edildiği minimum maliyet yapın."
  2: "Henüz ziyaret edilmemiş v şehirlerine geçişlerin minimumunu hesaplayarak sonuca ulaşın."
  3: "Bu algoritma 'Held-Karp gezgin satıcı bit maskeli çözümü (Held-Karp TSP algorithm)' olarak bilinir."
```

---

### cpp-hard-concurrent-hash-map

```yaml
id: cpp-hard-concurrent-hash-map
version: 1
language: cpp
engine: none
difficulty: hard
title: "İnce taneli kilit şeritleme ile iş parçacığı güvenli karma tablosu"
prompt: |
  Tüm tabloyu tek bir kilitle kitlemek yerine k adet bağımsız şerit (stripe) kilidi tutarak eşzamanlı erişim çatışmasını en aza indiren `class ConcurrentHashMap` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(n) olmalı"
  - "std::mutex veya shared_mutex şeritleri kullanılmalıdır"
expected:
  time: { ConcurrentHashMap: "1" }
  space: "n"
concept_tags: [hash-map, concurrency]
checklist_extra:
  - "Anahtarın karma değerine göre ilgili şerit kilidi seçilmiş mi?"
  - "Aynı anda farklı kovalara erişen iş parçacıkları birbirini engellemiyor mu?"
reference_solution_path: private/solutions/cpp-hard-concurrent-hash-map.cpp
hint_ladder:
  1: "Sabit sayıda (ör. 16 veya 32) bağımsız mutex içeren bir şerit dizisi tutun."
  2: "Anahtarın hash kodunu bu şerit sayısına bölerek yalnızca ilgili şeridin kilidini edinin."
  3: "Bu eşzamanlılık deseni 'kilit şeritlemeli karma haritası (lock striping hash map)' olarak bilinir."
```

---

### cpp-hard-ring-buffer-wait-free

```yaml
id: cpp-hard-ring-buffer-wait-free
version: 1
language: cpp
engine: none
difficulty: hard
title: "Çoklu üretici çoklu tüketici için dizi tabanlı dairesel tampon"
prompt: |
  Birden çok iş parçacığının kilit kullanmadan atomik dizi hücreleri ve sıra numaraları (sequence numbers) üzerinden veri ekleyip çektiği `class MPMCQueue` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(capacity) olmalı"
  - "Hücre başı sıra numarası atomik kontrol edilmelidir"
expected:
  time: { MPMCQueue: "1" }
  space: "1"
concept_tags: [concurrency, performance]
checklist_extra:
  - "Dmitry Vyukov tarzı hücre sıra numarası (sequence) kullanılmış mı?"
  - "Kuyruk başı ve sonu atomik ilerletilmiş mi?"
reference_solution_path: private/solutions/cpp-hard-ring-buffer-wait-free.cpp
hint_ladder:
  1: "Her hücrede bir veri ve atomik sequence numarası saklayın."
  2: "Üretici ve tüketici CAS ile kuyruk indekslerini kapıp hücrenin sıra numarası beklenen değerde olduğunda işlemi tamamlasın."
  3: "Bu eşzamanlı kuyruk algoritması 'Vyukov çoklu üretici çoklu tüketici kuyruğu (MPMC wait-free ring buffer)' olarak bilinir."
```

---

### cpp-hard-custom-coroutine-generator

```yaml
id: cpp-hard-custom-coroutine-generator
version: 1
language: cpp
engine: none
difficulty: hard
title: "C++20 coroutine handle ve promise ile tembel değer üreteci"
prompt: |
  co_yield ile talep edildikçe sıradaki tamsayıyı üreten, bellekte tüm diziyi tutmayan ve tembel değerlendirme (lazy evaluation) sağlayan `class Generator` coroutine sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı adım başı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "std::coroutine_handle ve promise_type kurgulanmalıdır"
expected:
  time: { Generator: "1" }
  space: "1"
concept_tags: [move-semantics, ownership]
checklist_extra:
  - "promise_type içinde initial_suspend, final_suspend, yield_value doğru tanımlanmış mı?"
  - "coroutine_handle yıkıcıda destroy edilmiş mi?"
reference_solution_path: private/solutions/cpp-hard-custom-coroutine-generator.cpp
hint_ladder:
  1: "Sınıf içinde promise_type yapısını tanımlayıp initial_suspend'i std::suspend_always yapın."
  2: "yield_value(val) içinde değeri saklayıp yürütmeyi duraklatın; iteratorün operator++ çağrısında handle.resume() yapın."
  3: "Bu modern C++ mekanizması 'C++20 eşyordam değer üreteci (coroutine generator)' olarak bilinir."
```
