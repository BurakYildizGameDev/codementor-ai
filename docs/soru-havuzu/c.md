# CodeMentor AI — 200 C Sorusu

Bu belge, `docs/SORU_YAZIM_REHBERI.md` standartlarına uygun olarak hazırlanmış 200 adet C programlama dili sorusunu içerir.
C dili sistem seviyesi bir programlama dili olduğu için; bellek yönetimi (malloc/free, realloc, sahiplik), işaretçi aritmetiği (pointer arithmetic), tamsayı taşmaları (integer overflow), bellek güvenliği (buffer overflow, use-after-free, dangling pointer), tanımsız davranışlar (undefined behavior) ve algoritmik zaman/alan karmaşıklığı (`expected: time, space`) odaklı hazırlanmıştır.

---

## Soru Bankası Değerlendirmesi ve Pedagojik Kullanım Notu

Bu soru bankası teknik iş mülakatları, gömülü sistem / sistem programlama mühendisleri ve bilgisayar bilimleri öğrencileri için tasarlanmıştır:

1. **Sokratik ve Mülakat Odaklı Yapı (Yöntem Sızıntısı Yok):**
   - Başlıklarda ve soru metinlerinde doğrudan kütüphane fonksiyon adları (ör. `malloc`, `realloc`, `strtok`, `memcpy`) verilmemiştir.
   - Soru, adaya gerçek dünya sistem kısıtlarını ve bellek gereksinimlerini aktarır; adayın uygun C standardını ve bellek modelini kendisinin seçmesi beklenir.

2. **Sıkı Karmaşıklık ve Bellek Analizi (`expected`):**
   - Tüm sorularda zaman (`time`) ve alan (`space`) karmaşıklıkları Big-O notasyonuyla tanımlanmıştır.
   - Tanımlanan her karmaşıklık değişkeni (n, m, k) prompt ve kısıtlar içinde açık bir kelime olarak karşılık bulur.

3. **C Standartları Uyumu:**
   - Sorular ISO/IEC C17 standardına uygun, derleyici uyarısı üretmeyecek ve tanımsız davranışlardan (UB) arındırılmış güvenli C programlama disiplinini ölçer.

---

## 1. Çok Kolay (Very Easy) — 50 Soru

### c-veryeasy-sum-array

```yaml
id: c-veryeasy-sum-array
version: 1
language: c
engine: none
difficulty: very_easy
title: "Tamsayı dizisi elemanlarının toplamı"
prompt: |
  Verilen n elemanlı bir tamsayı dizisindeki tüm değerlerin toplamını hesaplayan
  `int sum_array(const int *arr, size_t n)` fonksiyonunu yazın. Dizi boş olduğunda
  (n = 0) veya dizi işaretçisi NULL olduğunda toplam 0 kabul edilmelidir. Dizi
  uzunluğu n tamsayı adedini ifade eder.
constraints:
  - "Dizi boyutu n için zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek kullanımı O(1) sabit alanla sınırlı kalmalı"
  - "Geçersiz işaretçi veya n = 0 durumu güvenle ele alınmalı"
expected:
  time: { sum_array: "n" }
  space: "1"
concept_tags: [arrays, memory-safety]
checklist_extra:
  - "İşaretçi NULL kontrolü döngüden önce yapılmış mı?"
  - "Dizi elemanları const belirteciyle salt okunur korunmuş mu?"
reference_solution_path: private/solutions/c-veryeasy-sum-array.c
hint_ladder:
  1: "Diziye erişmeden önce işaretçinin geçerli bir bellek adresine işaret edip etmediğini nasıl denetlersiniz?"
  2: "Dizi elemanlarını baştan sona tek geçişte toplamak için hangi döngü yapısı uygundur?"
  3: "Bu temel işlem 'dizi elemanları toplamı (linear array accumulation)' olarak bilinir."
```

---
### c-veryeasy-find-minimum

```yaml
id: c-veryeasy-find-minimum
version: 1
language: c
engine: none
difficulty: very_easy
title: "Dizideki en küçük değeri bulma"
prompt: |
  Pozitif ve negatif tamsayılar içeren n elemanlı bir dizideki en küçük elemanı bulan
  `int find_minimum(const int *arr, size_t n, int *out_min)` fonksiyonunu yazın. Dizi geçerli
  ve n > 0 ise bulunan minimum değer `out_min` adresine yazılmalı ve fonksiyon 1 dönmelidir.
  Dizi boşsa veya işaretçiler geçersizse fonksiyon 0 dönmelidir. n eleman sayısını belirtir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ekstra bellek kullanımı O(1) olmalı"
  - "Başarı durumunda 1, geçersiz durumda 0 döndürülmeli"
expected:
  time: { find_minimum: "n" }
  space: "1"
concept_tags: [arrays, input-validation]
checklist_extra:
  - "out_min işaretçisinin NULL olup olmadığı kontrol edilmiş mi?"
  - "İlk minimum aday olarak rastgele bir sayı yerine dizinin ilk elemanı mı seçilmiş?"
reference_solution_path: private/solutions/c-veryeasy-find-minimum.c
hint_ladder:
  1: "Dizinin ilk elemanını başlangıç minimumu kabul edip kalan elemanlarla karşılaştırmak neden güvenlidir?"
  2: "Çıkış parametresine değer yazmadan önce işaretçinin adres doğruluğu nasıl garanti edilir?"
  3: "Bu arama algoritması 'doğrusal minimum bulma (linear scan minimum)' olarak bilinir."
```

---
### c-veryeasy-count-evens

```yaml
id: c-veryeasy-count-evens
version: 1
language: c
engine: none
difficulty: very_easy
title: "Dizideki çift sayıların adedi"
prompt: |
  n tamsayıdan oluşan bir dizide bulunan çift sayıların (hem pozitif hem negatif çiftler dahil)
  toplam adedini sayan `size_t count_evens(const int *arr, size_t n)` fonksiyonunu yazın.
  Negatif sayıların çift olma durumu da doğru tespit edilmelidir (örneğin -4 çifttir).
  n parametresi dizideki eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek karmaşıklığı O(1) olmalı"
  - "Dizi NULL ise 0 döndürülmeli"
expected:
  time: { count_evens: "n" }
  space: "1"
concept_tags: [arrays, edge-cases]
checklist_extra:
  - "Negatif sayılarda mod operatörünün (% 2) sıfıra eşitliği doğru sorgulanmış mı?"
  - "Dizi işaretçisi NULL olduğunda tanımsız davranış engellenmiş mi?"
reference_solution_path: private/solutions/c-veryeasy-count-evens.c
hint_ladder:
  1: "C'de negatif sayıların ikiye bölümünden kalan sıfır olduğunda çiftlik kuralı değişir mi?"
  2: "Bit düzeyinde kontrol için son bitin (arr[i] & 1) sıfır olması ne anlama gelir?"
  3: "Bu kontrol 'çift sayı parite denetimi (parity check)' olarak bilinir."
```

---
### c-veryeasy-string-length

```yaml
id: c-veryeasy-string-length
version: 1
language: c
engine: none
difficulty: very_easy
title: "Sonlandırıcı karaktere kadar metin uzunluğu"
prompt: |
  Standart kütüphane fonksiyonu `strlen` kullanmadan, boş karakterle (`\0`) sonlandırılmış
  bir C dizgisinin karakter uzunluğunu hesaplayan `size_t safe_strlen(const char *str)`
  fonksiyonunu yazın. İşaretçi NULL ise 0 dönmelidir. n dizginin karakter uzunluğunu ifade eder.
constraints:
  - "Karakter sayısı n için O(n) sürede tamamlanmalı"
  - "Yardımcı bellek O(1) olmalı"
  - "Dizgi sonlandırıcı `\\0` karakteri uzunluğa dahil edilmemeli"
expected:
  time: { safe_strlen: "n" }
  space: "1"
concept_tags: [strings, pointers]
checklist_extra:
  - "Döngü koşulunda `*str != '\\0'` veya `*str` doğru kullanılmış mı?"
  - "NULL işaretçi verildiğinde program çökmeden 0 dönüyor mu?"
reference_solution_path: private/solutions/c-veryeasy-string-length.c
hint_ladder:
  1: "C dilinde bir dizginin nerede bittiğini anlamanın yegane kuralı nedir?"
  2: "İşaretçiyi her adımda bir ileri kaydırarak null karaktere kadar saymak nasıl uygulanır?"
  3: "Bu işlem 'C dizgi uzunluğu hesabı (null-terminated string traversal)' olarak bilinir."
```

---
### c-veryeasy-count-vowels

```yaml
id: c-veryeasy-count-vowels
version: 1
language: c
engine: none
difficulty: very_easy
title: "Metin içindeki sesli harf sayısı"
prompt: |
  Boş karakterle sonlandırılmış bir İngilizce metindeki sesli harflerin (a, e, i, o, u hem
  küçük hem büyük harf) toplam adedini sayan `size_t count_vowels(const char *str)`
  fonksiyonunu yazın. Metin NULL ise 0 dönmelidir. n metnin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Büyük ve küçük harfler eşit şekilde sayılmalı"
expected:
  time: { count_vowels: "n" }
  space: "1"
concept_tags: [strings, edge-cases]
checklist_extra:
  - "Büyük harf (A, E, I, O, U) durumları unutulmuş mu?"
  - "Dizgi sonu null karakter kontrolü doğru yapılmış mı?"
reference_solution_path: private/solutions/c-veryeasy-count-vowels.c
hint_ladder:
  1: "Her karakteri incelerken büyük/küçük harf ayrımını teke indirmek için ne yapılabilir?"
  2: "Bir switch-case veya karakter kümesi kontrolü döngü içinde nasıl çalıştırılır?"
  3: "Bu karakter filtreleme işlemi 'sesli harf frekans sayımı (vowel counting)' olarak bilinir."
```

---
### c-veryeasy-swap-integers

```yaml
id: c-veryeasy-swap-integers
version: 1
language: c
engine: none
difficulty: very_easy
title: "İki tamsayının değerini işaretçilerle takas etme"
prompt: |
  İki tamsayı değişkeninin adreslerini alarak bellek üzerindeki değerlerini birbiriyle
  değiştiren (swap) `void swap_integers(int *a, int *b)` fonksiyonunu yazın. İşaretçilerden
  herhangi biri NULL ise fonksiyon hiçbir işlem yapmadan güvenle dönmelidir. İki işaretçi
  aynı bellek adresini gösteriyorsa değer bozulmamalıdır.
constraints:
  - "Zaman karmaşıklığı O(1) sabit sürede olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "NULL işaretçi ve kendisiyle takas (aliasing) durumları güvenli olmalı"
expected:
  time: { swap_integers: "1" }
  space: "1"
concept_tags: [pointers, memory-safety]
checklist_extra:
  - "NULL işaretçi kontrolü yapılmış mı?"
  - "Geçici bir değişken kullanılarak değer kaybı önlenmiş mi?"
reference_solution_path: private/solutions/c-veryeasy-swap-integers.c
hint_ladder:
  1: "İki bellek bölgesini takas ederken ilk değeri kaybetmemek için neye ihtiyaç duyulur?"
  2: "İşaretçinin işaret ettiği değere erişmek için yıldız (*) operatörü nasıl kullanılır?"
  3: "Bu klasik işlem 'işaretçi ile bellek takası (pointer dereference swap)' olarak bilinir."
```

---
### c-veryeasy-is-sorted-ascending

```yaml
id: c-veryeasy-is-sorted-ascending
version: 1
language: c
engine: none
difficulty: very_easy
title: "Dizinin artan sırada olduğunu denetleme"
prompt: |
  n elemanlı bir tamsayı dizisinin küçükten büyüğe (artan veya eşit) sıralı olup olmadığını
  denetleyen `int is_sorted_ascending(const int *arr, size_t n)` fonksiyonunu yazın.
  Dizi sıralıysa 1, değilse 0 dönmelidir. Boş dizi (n = 0) ve tek elemanlı dizi (n = 1)
  doğal olarak sıralı kabul edilmelidir. n eleman sayısını temsil eder.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek karmaşıklığı O(1) olmalı"
  - "Sıralamayı bozan ilk eleman çiftinde döngü erken sonlanmalı"
expected:
  time: { is_sorted_ascending: "n" }
  space: "1"
concept_tags: [arrays, loop-invariant]
checklist_extra:
  - "Döngü sınırında `i < n - 1` kontrolü yapılarak dizi dışına taşma (OOB) önlenmiş mi?"
  - "n < 2 durumları doğru ele alınmış mı?"
reference_solution_path: private/solutions/c-veryeasy-is-sorted-ascending.c
hint_ladder:
  1: "Ardışık iki elemandan ilki ikincisinden büyükse dizinin sıralı olma ihtimali kalır mı?"
  2: "Döngüyü son elemana kadar sürdürürken arr[i+1] erişiminin taşmaması için üst sınır ne olmalıdır?"
  3: "Bu doğrulama 'artan dizi sıralılık denetimi (monotonic array check)' olarak bilinir."
```

---
### c-veryeasy-linear-search-index

```yaml
id: c-veryeasy-linear-search-index
version: 1
language: c
engine: none
difficulty: very_easy
title: "Dizide hedef değerin ilk indeksini bulma"
prompt: |
  n elemanlı bir dizide aranan `target` değerinin ilk görüldüğü indeksi döndüren
  `long long linear_search_index(const int *arr, size_t n, int target)` fonksiyonunu yazın.
  Değer dizide bulunursa sıfır tabanlı indeksi (0, 1, 2...), bulunamazsa veya dizi NULL ise
  -1 döndürülmelidir. n dizi uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "Bulunamazsa -1 dönmeli"
expected:
  time: { linear_search_index: "n" }
  space: "1"
concept_tags: [arrays, pointers]
checklist_extra:
  - "Hedef değer bulunduğunda hemen o anki indeks döndürülüp döngü kırılıyor mu?"
  - "Dönüş tipi negatif -1 değerini güvenle taşıyacak işaretli bir tip mi?"
reference_solution_path: private/solutions/c-veryeasy-linear-search-index.c
hint_ladder:
  1: "Sırasız bir dizide aranan bir değeri bulmak için baştan sona nasıl taranır?"
  2: "İlk eşleşme anında döngüden çıkmak arama süresini ortalamada nasıl etkiler?"
  3: "Bu temel arama yöntemi 'doğrusal arama (linear search)' olarak bilinir."
```

---
### c-veryeasy-array-contains

```yaml
id: c-veryeasy-array-contains
version: 1
language: c
engine: none
difficulty: very_easy
title: "Dizide hedef eleman varlık kontrolü"
prompt: |
  n elemanlı bir dizide belirli bir tamsayının mevcut olup olmadığını denetleyen
  `int array_contains(const int *arr, size_t n, int target)` fonksiyonunu yazın. Eleman
  dizide varsa 1, yoksa veya işaretçi geçersizse 0 dönmelidir. n dizideki eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "Boolean karşılığı olarak 1 veya 0 dönmeli"
expected:
  time: { array_contains: "n" }
  space: "1"
concept_tags: [arrays, memory-safety]
checklist_extra:
  - "arr NULL kontrolü yapılmış mı?"
  - "Değer bulunur bulunmaz 1 ile erken çıkış sağlanıyor mu?"
reference_solution_path: private/solutions/c-veryeasy-array-contains.c
hint_ladder:
  1: "Elemanın varlığını doğrulamak için dizinin sonuna kadar beklemek gerekir mi?"
  2: "İlk eşleşmede 1 dönmek en iyi durumda fonksiyonu ne kadar hızlandırır?"
  3: "Bu mantıksal sorgu 'dizi üyelik denetimi (array membership test)' olarak bilinir."
```

---
### c-veryeasy-clamp-value

```yaml
id: c-veryeasy-clamp-value
version: 1
language: c
engine: none
difficulty: very_easy
title: "Değeri alt ve üst sınırlar arasına sıkıştırma"
prompt: |
  Verilen bir `val` tamsayısını, `min_val` ve `max_val` sınırları arasına sıkıştıran
  `int clamp_value(int val, int min_val, int max_val)` fonksiyonunu yazın. Değer `min_val`dan
  küçükse `min_val`, `max_val`dan büyükse `max_val`, aralıkta ise `val` kendisi dönmelidir.
  Girdi olarak `min_val > max_val` verilirse sınırlar kendi arasında takas edilmelidir.
constraints:
  - "Zaman karmaşıklığı O(1) sabit sürede olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "Ters sınır girdileri (`min_val > max_val`) düzeltilmeli"
expected:
  time: { clamp_value: "1" }
  space: "1"
concept_tags: [edge-cases, input-validation]
checklist_extra:
  - "min_val ile max_val ters verildiğinde takas yapılıyor mu?"
  - "Koşullu ifadeler doğru sırada kurgulanmış mı?"
reference_solution_path: private/solutions/c-veryeasy-clamp-value.c
hint_ladder:
  1: "Gelen değerin önce minimumdan küçük olup olmadığını kontrol etmek ne sağlar?"
  2: "min_val büyüktür max_val uç durumunda değişkenleri nasıl hizalarsınız?"
  3: "Bu matematiksel sınırlandırma 'aralık sıkıştırma işlemi (clamping)' olarak bilinir."
```

---
### c-veryeasy-count-occurrences

```yaml
id: c-veryeasy-count-occurrences
version: 1
language: c
engine: none
difficulty: very_easy
title: "Dizideki hedef değerin tekrarlanma sıklığı"
prompt: |
  n elemanlı bir tamsayı dizisinde `target` değerinin kaç defa geçtiğini sayan
  `size_t count_occurrences(const int *arr, size_t n, int target)` fonksiyonunu yazın.
  Dizi boşsa veya NULL ise 0 dönmelidir. n dizi boyutunu ifade eder.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek karmaşıklığı O(1) olmalı"
  - "Dizi elemanları değiştirilmemeli (const)"
expected:
  time: { count_occurrences: "n" }
  space: "1"
concept_tags: [arrays, memory-safety]
checklist_extra:
  - "Sayaç değişkeni 0 ile başlatılmış mı?"
  - "Tüm dizi eksiksiz taranıyor mu?"
reference_solution_path: private/solutions/c-veryeasy-count-occurrences.c
hint_ladder:
  1: "Her eşleşmede sayacı bir artırmak için döngü içinde hangi koşul yazılır?"
  2: "Dizinin değiştirilmesini önlemek için işaretçi türü nasıl tanımlanmalıdır?"
  3: "Bu frekans analizi 'frekans sayımı (occurrence frequency)' olarak bilinir."
```

---
### c-veryeasy-reverse-array-inplace

```yaml
id: c-veryeasy-reverse-array-inplace
version: 1
language: c
engine: none
difficulty: very_easy
title: "Diziyi yerinde tersine çevirme"
prompt: |
  n elemanlı bir tamsayı dizisini ek bir dizi tahsis etmeden, yerinde (in-place) tersine
  çeviren `void reverse_array_inplace(int *arr, size_t n)` fonksiyonunu yazın. İki işaretçi
  veya çift indeks yaklaşımıyla baştaki ve sondaki elemanları merkeze doğru takas edin.
  n parametresi dizinin eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek karmaşıklığı O(1) olmalı (yeni dizi oluşturulamaz)"
  - "n = 0 veya n = 1 durumunda güvenle dönmeli"
expected:
  time: { reverse_array_inplace: "n" }
  space: "1"
concept_tags: [arrays, pointers]
checklist_extra:
  - "Döngü durma koşulu olarak sol indeksin sağ indeksten küçük olması (`left < right`) sağlanmış mı?"
  - "Ek bellek tahsis edilmeden doğrudan yerinde takas yapılmış mı?"
reference_solution_path: private/solutions/c-veryeasy-reverse-array-inplace.c
hint_ladder:
  1: "Dizinin başı ile sonunu takas ettikten sonra göstergeleri merkeze doğru nasıl yaklaştırırsınız?"
  2: "Döngü ne zaman durmalıdır? Ortada karşılaştıklarında mı?"
  3: "Bu algoritma 'çift işaretçi ile yerinde dizi ters çevirme (two-pointer in-place reversal)' olarak bilinir."
```

---
### c-veryeasy-copy-array

```yaml
id: c-veryeasy-copy-array
version: 1
language: c
engine: none
difficulty: very_easy
title: "Tamsayı dizisini hedef belleğe kopyalama"
prompt: |
  Kaynak dizideki (`src`) n adet tamsayıyı, ayrılmış hedef bellek bölgesine (`dest`)
  kopyalayan `int copy_array(int *dest, const int *src, size_t n)` fonksiyonunu yazın.
  İşaretçilerden biri NULL ise kopyalama yapılmamalı ve 0 dönmelidir. Başarılı kopyalamada
  1 dönmelidir. n kopyalanacak eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek karmaşıklığı O(1) olmalı"
  - "NULL işaretçi koruması bulunmalı"
expected:
  time: { copy_array: "n" }
  space: "1"
concept_tags: [arrays, memory-safety]
checklist_extra:
  - "dest ve src işaretçilerinin NULL kontrolü yapılmış mı?"
  - "Kopyalama döngüsü sınırları n elemanla tam örtüşüyor mu?"
reference_solution_path: private/solutions/c-veryeasy-copy-array.c
hint_ladder:
  1: "Her iki dizinin de geçerli birer adrese sahip olduğunu fonksiyona girer girmez nasıl doğrularsınız?"
  2: "Kaynak diziyi değiştirmemek için parametre tanımına hangi anahtar kelime eklenir?"
  3: "Bu işlem 'dizi elemanları kopyalama (array copy)' olarak bilinir."
```

---
### c-veryeasy-fill-array

```yaml
id: c-veryeasy-fill-array
version: 1
language: c
engine: none
difficulty: very_easy
title: "Dizi alanını sabit bir değerle doldurma"
prompt: |
  n elemanlı bir tamsayı dizisinin tüm elemanlarını verilen `value` sabit değeriyle dolduran
  `void fill_array(int *arr, size_t n, int value)` fonksiyonunu yazın. İşaretçi NULL veya
  n = 0 ise fonksiyon güvenle hiçbir işlem yapmadan dönmelidir. n eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek karmaşıklığı O(1) olmalı"
  - "NULL işaretçi verildiğinde tanımsız davranış oluşmamalı"
expected:
  time: { fill_array: "n" }
  space: "1"
concept_tags: [arrays, memory-safety]
checklist_extra:
  - "arr NULL kontrolü yapılmış mı?"
  - "Döngü 0'dan n - 1'e kadar tüm indeksleri kapsıyor mu?"
reference_solution_path: private/solutions/c-veryeasy-fill-array.c
hint_ladder:
  1: "Dizinin her hücresine sırayla aynı değeri atamak için hangi döngü kurulur?"
  2: "İşaretçi güvenliği için döngüden önce ne kontrol edilir?"
  3: "Bu başlatma işlemi 'dizi doldurma (array fill)' olarak bilinir."
```

---
### c-veryeasy-is-power-of-two

```yaml
id: c-veryeasy-is-power-of-two
version: 1
language: c
engine: none
difficulty: very_easy
title: "Sayının ikinin kuvveti olduğunu bit düzeyinde denetleme"
prompt: |
  Pozitif bir tamsayının ikinin tam kuvveti (1, 2, 4, 8, 16, 32...) olup olmadığını
  denetleyen `int is_power_of_two(unsigned int x)` fonksiyonunu yazın. Döngü kullanmadan,
  sabit zamanda bit düzeyinde mantıksal işlemle kontrol edin. Sayı ikinin kuvveti ise 1,
  değilse veya 0 ise 0 dönmelidir.
constraints:
  - "Zaman karmaşıklığı O(1) sabit sürede olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "x = 0 durumu için 0 dönmeli"
expected:
  time: { is_power_of_two: "1" }
  space: "1"
concept_tags: [edge-cases, performance]
checklist_extra:
  - "x = 0 özel durumu ele alınmış mı?"
  - "Bitwise `(x & (x - 1)) == 0` mantığı doğru parantezlenmiş mi?"
reference_solution_path: private/solutions/c-veryeasy-is-power-of-two.c
hint_ladder:
  1: "İkinin kuvveti olan bir sayının ikilik (binary) gösteriminde kaç tane '1' biti bulunur?"
  2: "x ile x - 1 sayısını bit düzeyinde AND (&) işlemine soktuğumuzda sonuç ne olur?"
  3: "Bu klasik bit optimizasyonu 'ikinin kuvveti bit hilesi (power of two bitwise check)' olarak bilinir."
```

---
### c-veryeasy-count-set-bits

```yaml
id: c-veryeasy-count-set-bits
version: 1
language: c
engine: none
difficulty: very_easy
title: "İkili tabanda bir olan bitlerin sayısını bulma"
prompt: |
  Verilen 32-bitlik işaretsiz bir tamsayının ikilik tabandaki gösteriminde 1 olan bitlerinin
  (set bits) toplam sayısını hesaplayan `unsigned int count_set_bits(unsigned int n)`
  fonksiyonunu yazın. Sayının bit uzunluğu sabit (32 bit) olduğu için işlem sabit sürede
  tamamlanmalıdır.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı (32 bitten bağımsız)"
  - "Ek bellek kullanımı O(1) olmalı"
  - "0 girdiğinde 0 dönmeli"
expected:
  time: { count_set_bits: "1" }
  space: "1"
concept_tags: [edge-cases, performance]
checklist_extra:
  - "Brian Kernighan algoritması veya bit kaydırma mantığı doğru kurulmuş mu?"
  - "İşaretsiz tamsayı taşması ve mantıksal kaydırma korunmuş mu?"
reference_solution_path: private/solutions/c-veryeasy-count-set-bits.c
hint_ladder:
  1: "Her adımda sayının en sağdaki bir bitini yok etmek için n & (n - 1) işlemi nasıl kullanılır?"
  2: "Döngü yalnızca 1 olan bit sayısı kadar dönerse ne kadar hızlanır?"
  3: "Bu bit sayma yöntemi 'Kernighan bit sayma algoritması (population count)' olarak bilinir."
```

---
### c-veryeasy-find-maximum-index

```yaml
id: c-veryeasy-find-maximum-index
version: 1
language: c
engine: none
difficulty: very_easy
title: "Dizideki en büyük değerin indeksini bulma"
prompt: |
  n elemanlı bir dizideki en büyük elemanın dizideki ilk indeksini döndüren
  `long long find_maximum_index(const int *arr, size_t n)` fonksiyonunu yazın. Dizi boşsa
  veya NULL ise -1 dönmelidir. n eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek karmaşıklığı O(1) olmalı"
  - "Geçersiz durumda -1 dönmeli"
expected:
  time: { find_maximum_index: "n" }
  space: "1"
concept_tags: [arrays, input-validation]
checklist_extra:
  - "Maksimum indeks 0 ile başlatılıp döngü 1'den başlatılmış mı?"
  - "Birden fazla aynı maksimum varsa ilk indeks korunuyor mu?"
reference_solution_path: private/solutions/c-veryeasy-find-maximum-index.c
hint_ladder:
  1: "En büyük değeri değil onun indeksini saklayarak ilerlemek neden daha avantajlıdır?"
  2: "Daha büyük bir değerle karşılaşıldığında hem maksimumu hem indeksi güncellemek nasıl yapılır?"
  3: "Bu işlem 'maksimum eleman indeks taraması (argmax linear search)' olarak bilinir."
```

---
### c-veryeasy-is-all-positive

```yaml
id: c-veryeasy-is-all-positive
version: 1
language: c
engine: none
difficulty: very_easy
title: "Dizideki tüm elemanların pozitif olduğunu denetleme"
prompt: |
  n elemanlı bir tamsayı dizisindeki tüm elemanların kesinlikle pozitif (> 0) olup olmadığını
  denetleyen `int is_all_positive(const int *arr, size_t n)` fonksiyonunu yazın. Dizi boşsa
  (n = 0) koşulu bozan eleman olmadığı için 1 dönmelidir. Dizide sıfır veya negatif bir sayı
  görüldüğü an 0 dönmelidir. n eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek karmaşıklığı O(1) olmalı"
  - "İlk sıfır veya negatif elemanda erken çıkış yapılmalı"
expected:
  time: { is_all_positive: "n" }
  space: "1"
concept_tags: [arrays, edge-cases]
checklist_extra:
  - "0 sayısı pozitif kabul edilmeyip döngüden çıkılmış mı?"
  - "Boş dizi durumu için doğru kabul (vacuous truth) 1 döndürülmüş mü?"
reference_solution_path: private/solutions/c-veryeasy-is-all-positive.c
hint_ladder:
  1: "Sıfır sayısı pozitif midir yoksa nötr müdür?"
  2: "Kuralı bozan ilk elemanla karşılaşıldığında döngüyü sürdürmenin bir anlamı var mıdır?"
  3: "Bu mantıksal doğrulama 'tüm elemanların pozitiflik denetimi (all positive predicate)' olarak bilinir."
```

---
### c-veryeasy-has-duplicates-consecutive

```yaml
id: c-veryeasy-has-duplicates-consecutive
version: 1
language: c
engine: none
difficulty: very_easy
title: "Ardışık yinelenen eleman kontrolü"
prompt: |
  n elemanlı bir dizide yan yana duran iki elemanın birbirine eşit olup olmadığını denetleyen
  `int has_consecutive_duplicates(const int *arr, size_t n)` fonksiyonunu yazın. Dizide
  en az bir ardışık eşitlik varsa (örneğin [1, 2, 2, 4]) 1, yoksa veya dizi 2 elemandan
  kısa ise 0 dönmelidir. n dizi uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek karmaşıklığı O(1) olmalı"
  - "Dizi sınırları dışına erişilmemeli"
expected:
  time: { has_consecutive_duplicates: "n" }
  space: "1"
concept_tags: [arrays, loop-invariant]
checklist_extra:
  - "Döngü üst sınırı `n - 1` olarak ayarlanmış mı?"
  - "İlk ardışık eşleşmede erken 1 dönülüyor mu?"
reference_solution_path: private/solutions/c-veryeasy-has-duplicates-consecutive.c
hint_ladder:
  1: "i'inci eleman ile i+1'inci elemanı karşılaştırırken son elemandan sonra taşmamak için döngü nerede durmalıdır?"
  2: "Eşitlik tespit edildiğinde hemen çıkmak zaman karmaşıklığını nasıl iyileştirir?"
  3: "Bu kontrol 'ardışık tekrar denetimi (consecutive duplicate check)' olarak bilinir."
```

---
### c-veryeasy-string-to-uppercase

```yaml
id: c-veryeasy-string-to-uppercase
version: 1
language: c
engine: none
difficulty: very_easy
title: "Metni yerinde büyük harfe dönüştürme"
prompt: |
  Boş karakterle sonlandırılmış bir karakter dizisindeki tüm küçük ASCII harflerini ('a'-'z'),
  aynı bellek alanında (in-place) büyük harfe ('A'-'Z') dönüştüren `void str_to_uppercase(char *str)`
  fonksiyonunu yazın. Rakamlar, boşluklar ve noktalama işaretleri değişmeden kalmalıdır.
  n metnin uzunluğudur.
constraints:
  - "Karakter sayısı n için O(n) sürede tamamlanmalı"
  - "Ek bellek O(1) olmalı"
  - "NULL işaretçi verildiğinde işlem yapılmamalı"
expected:
  time: { str_to_uppercase: "n" }
  space: "1"
concept_tags: [strings, pointers]
checklist_extra:
  - "Küçük harf aralığı kontrolü (`*s >= 'a' && *s <= 'z'`) doğru yapılmış mı?"
  - "ASCII farkı (`'a' - 'A'` veya 32) doğru çıkarılmış mı?"
reference_solution_path: private/solutions/c-veryeasy-string-to-uppercase.c
hint_ladder:
  1: "ASCII tablosunda küçük bir harfi büyütmek için değerinden ne çıkarılır?"
  2: "Sadece harf olan karakterleri dönüştürüp sembolleri nasıl pas geçersiniz?"
  3: "Bu metin manipülasyonu 'yerinde büyük harfe dönüştürme (in-place uppercase)' olarak bilinir."
```

---
### c-veryeasy-string-copy-safe

```yaml
id: c-veryeasy-string-copy-safe
version: 1
language: c
engine: none
difficulty: very_easy
title: "Boyut sınırlı güvenli metin kopyalama"
prompt: |
  Kaynak metinden (`src`) hedef tampona (`dest`) en fazla `dest_size - 1` karakter kopyalayan
  ve hedef metnin sonunu her koşulda mutlaka null karakterle (`\0`) kapatan
  `size_t safe_str_copy(char *dest, const char *src, size_t dest_size)` fonksiyonunu yazın.
  Tampon taşmalarına (buffer overflow) karşı korumalı olmalı; kopyalanan karakter sayısını
  (null hariç) döndürmelidir. n kaynak metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Hedef tampon asla taşırılmamalı ve daima null ile sonlandırılmalı"
expected:
  time: { safe_str_copy: "n" }
  space: "1"
concept_tags: [strings, memory-safety]
checklist_extra:
  - "dest_size = 0 durumunda hiçbir yazma yapılmadan dönülüyor mu?"
  - "Son karaktere `dest[i] = '\\0'` garantisi verilmiş mi?"
reference_solution_path: private/solutions/c-veryeasy-string-copy-safe.c
hint_ladder:
  1: "Hedef tamponun sonuna null koyabilmek için azami kaç karakter kopyalanabilir?"
  2: "Klasik strcpy fonksiyonunun en büyük güvenlik açığı nedir?"
  3: "Bu güvenli kopyalama 'sınırlı bellek güvenli dizgi kopyalama (bounded string copy)' olarak bilinir."
```

---
### c-veryeasy-string-compare-ascii

```yaml
id: c-veryeasy-string-compare-ascii
version: 1
language: c
engine: none
difficulty: very_easy
title: "İki metni alfabetik olarak karşılaştırma"
prompt: |
  Standart `strcmp` fonksiyonu kullanmadan, boş karakterle sonlandırılmış iki metni
  sözlük sırasına (ASCII) göre karşılaştıran `int safe_strcmp(const char *s1, const char *s2)`
  fonksiyonunu yazın. Metinler eşitse 0, `s1` önce geliyorsa negatif bir değer, `s2` önce
  geliyorsa pozitif bir değer dönmelidir. n en kısa dizginin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Karakter farkı unsigned char üzerinden hesaplanmalı"
expected:
  time: { safe_strcmp: "n" }
  space: "1"
concept_tags: [strings, pointers]
checklist_extra:
  - "Karakterler karşılaştırılırken unsigned char dönüşümü yapılmış mı (negatif char riski)?"
  - "Döngü iki dizgiden biri bittiğinde veya fark görüldüğünde kırılıyor mu?"
reference_solution_path: private/solutions/c-veryeasy-string-compare-ascii.c
hint_ladder:
  1: "C standardında strcmp sonucunun negatif karakter değerlerinden etkilenmemesi için hangi tipe dönüştürülmesi gerekir?"
  2: "İki dizgi eşit ilerlerken null karaktere ulaşıldığında döngü ne yapmalıdır?"
  3: "Bu işlem 'ASCII sözlük sırası karşılaştırması (lexicographical string comparison)' olarak bilinir."
```

---
### c-veryeasy-dot-product-vectors

```yaml
id: c-veryeasy-dot-product-vectors
version: 1
language: c
engine: none
difficulty: very_easy
title: "İki vektörün skaler nokta çarpımı"
prompt: |
  n elemanlı iki tamsayı dizisinin (`a` ve `b`) skaler nokta çarpımını (dot product) hesaplayan
  `long long dot_product(const int *a, const int *b, size_t n)` fonksiyonunu yazın.
  Her iki dizinin aynı indeksteki elemanları birbiriyle çarpılmalı ve sonuçlar toplanmalıdır.
  Sonucun taşmaması için 64-bitlik `long long` akümülatör kullanılmalıdır. n eleman sayısıdır.
constraints:
  - "Vektör uzunluğu n için O(n) sürede tamamlanmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "Ara çarpımlarda 32-bit tamsayı taşması engellenmeli"
expected:
  time: { dot_product: "n" }
  space: "1"
concept_tags: [arrays, integer-overflow]
checklist_extra:
  - "Çarpım yapılmadan önce elemanlar `(long long)` tipine dönüştürülmüş mü?"
  - "İşaretçilerden biri NULL ise 0 dönülüyor mu?"
reference_solution_path: private/solutions/c-veryeasy-dot-product-vectors.c
hint_ladder:
  1: "İki 32-bit tamsayı çarpıldığında sonucun taşmaması için çarpım öncesi ne yapılmalıdır?"
  2: "Vektörlerin karşılıklı elemanlarını çarpıp toplamak için tek döngü yeterli midir?"
  3: "Bu matematiksel işlem 'vektör skaler nokta çarpımı (dot product)' olarak bilinir."
```

---
### c-veryeasy-celsius-to-fahrenheit

```yaml
id: c-veryeasy-celsius-to-fahrenheit
version: 1
language: c
engine: none
difficulty: very_easy
title: "Sıcaklık dönüşümünde tamsayı bölme hatasını önleme"
prompt: |
  Santigrat (°C) cinsinden verilen bir sıcaklığı Fahrenhayt (°F) cinsine dönüştüren
  `double celsius_to_fahrenheit(double celsius)` fonksiyonunu yazın. C dilinde `9 / 5`
  yazıldığında gerçekleşen tamsayı bölmesi (integer truncation) hatasına düşmeden,
  kesirli formülü (`(celsius * 9.0 / 5.0) + 32.0`) hatasız uygulayın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Tamsayı bölme kesilmesi (integer division bug) yaşanmamalı"
expected:
  time: { celsius_to_fahrenheit: "1" }
  space: "1"
concept_tags: [edge-cases, input-validation]
checklist_extra:
  - "9 / 5 yerine 9.0 / 5.0 kesirli sabitler kullanılmış mı?"
  - "Formül parantezleri doğru yapılandırılmış mı?"
reference_solution_path: private/solutions/c-veryeasy-celsius-to-fahrenheit.c
hint_ladder:
  1: "C dilinde iki tamsayıyı böldüğünüzde (örneğin 9 / 5) sonuç neden 1.8 değil de 1 çıkar?"
  2: "Bölme işleminin kayan noktalı çalışması için sabit sayılara ne eklenmelidir?"
  3: "Bu tipik hata 'tamsayı bölme kesilmesi (integer division truncation)' olarak bilinir."
```

---
### c-veryeasy-abs-difference

```yaml
id: c-veryeasy-abs-difference
version: 1
language: c
engine: none
difficulty: very_easy
title: "İki tamsayı arasındaki mutlak fark"
prompt: |
  İki tamsayı (`a` ve `b`) arasındaki mutlak mesafeyi (farkı) hesaplayan
  `unsigned int abs_difference(int a, int b)` fonksiyonunu yazın. `a - b` işlemi sırasında
  meydana gelebilecek tamsayı taşması (signed integer overflow) tanımsız davranışını
  engellemek için, önce büyük olan sayıyı tespit edip büyükten küçüğü çıkarın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "İşaretli tamsayı taşması (undefined behavior) engellenmeli"
  - "Dönüş tipi negatif olmayan `unsigned int` olmalı"
expected:
  time: { abs_difference: "1" }
  space: "1"
concept_tags: [integer-overflow, undefined-behavior]
checklist_extra:
  - "INT_MIN durumunda a - b çıkarma taşması önlenmiş mi?"
  - "Büyükten küçük çıkarılarak pozitif fark garanti edilmiş mi?"
reference_solution_path: private/solutions/c-veryeasy-abs-difference.c
hint_ladder:
  1: "a pozitif maksimum, b negatif minimum olduğunda a - b işlemi neye yol açar?"
  2: "Taşmayı önlemek için sayılardan hangisinin büyük olduğunu önce belirlemek nasıl fayda sağlar?"
  3: "Bu güvenli hesaplama 'taşmasız mutlak fark (overflow-safe absolute difference)' olarak bilinir."
```

---
### c-veryeasy-is-leap-year

```yaml
id: c-veryeasy-is-leap-year
version: 1
language: c
engine: none
difficulty: very_easy
title: "Artık yıl hesaplama kuralları"
prompt: |
  Verilen bir yılın (yıl > 0) Gregoryen takvimine göre artık yıl (leap year) olup olmadığını
  denetleyen `int is_leap_year(int year)` fonksiyonunu yazın. Yıl 4'e tam bölünmeli; ancak
  100'e tam bölünen yıllar 400'e de tam bölünmüyorsa artık yıl kabul edilmemelidir.
  Artık yıl ise 1, değilse veya geçersizse 0 dönmelidir.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "100 ve 400 bölünebilme istisnaları eksiksiz uygulanmalı"
  - "Negatif veya sıfır yıl girdilerinde 0 dönmeli"
expected:
  time: { is_leap_year: "1" }
  space: "1"
concept_tags: [edge-cases, input-validation]
checklist_extra:
  - "1900 gibi 100'e bölünüp 400'e bölünmeyen yıllar için 0 dönüyor mu?"
  - "2000 gibi 400'e bölünen yıllar için 1 dönüyor mu?"
reference_solution_path: private/solutions/c-veryeasy-is-leap-year.c
hint_ladder:
  1: "Bir yılın 4'e bölünmesi artık yıl olması için her zaman yeterli midir?"
  2: "Yüzün katı olan yıllarda 400 kuralı nasıl işletilir?"
  3: "Bu takvim kuralı 'Gregoryen artık yıl denetimi (leap year rule)' olarak bilinir."
```

---
### c-veryeasy-average-integers-safe

```yaml
id: c-veryeasy-average-integers-safe
version: 1
language: c
engine: none
difficulty: very_easy
title: "Tamsayı taşması olmadan dizi ortalaması alma"
prompt: |
  n elemanlı bir tamsayı dizisinin aritmetik ortalamasını hesaplayan
  `double average_integers_safe(const int *arr, size_t n)` fonksiyonunu yazın. Dizi elemanları
  büyük sayılardan oluştuğunda toplam değişkeninin 32-bit tamsayı sınırını aşıp taşmaması için
  toplama işlemini 64-bitlik `long long` veya doğrudan `double` üzerinde yürütün. n = 0 ise
  0.0 dönmelidir. n eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ara toplamlarda tamsayı taşması yaşanmamalı"
  - "n = 0 sıfıra bölme hatası güvenle engellenmeli"
expected:
  time: { average_integers_safe: "n" }
  space: "1"
concept_tags: [integer-overflow, arrays]
checklist_extra:
  - "n = 0 durumunda sıfıra bölme (division by zero) engellenmiş mi?"
  - "Toplama işlemi taşmaya karşı 64-bitlik tipte mi yürütülmüş?"
reference_solution_path: private/solutions/c-veryeasy-average-integers-safe.c
hint_ladder:
  1: "Çok sayıda büyük int toplandığında 32-bit işaretli tamsayı ne zaman taşar?"
  2: "Sıfıra bölme hatasını önlemek için n değişkeni ilk satırda nasıl denetlenir?"
  3: "Bu hesaplama 'taşmasız ortalama hesabı (overflow-safe average)' olarak bilinir."
```

---
### c-veryeasy-find-first-negative

```yaml
id: c-veryeasy-find-first-negative
version: 1
language: c
engine: none
difficulty: very_easy
title: "Dizideki ilk negatif sayının indeksi"
prompt: |
  n tamsayıdan oluşan bir diziyi baştan sona tarayarak ilk negatif (< 0) elemanın indeksini
  döndüren `long long find_first_negative(const int *arr, size_t n)` fonksiyonunu yazın.
  Dizide hiçbir negatif sayı yoksa veya dizi geçersizse -1 dönmelidir. n eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek karmaşıklığı O(1) olmalı"
  - "İlk negatif sayıda arama derhal sonlandırılmalı"
expected:
  time: { find_first_negative: "n" }
  space: "1"
concept_tags: [arrays, loop-invariant]
checklist_extra:
  - "Negatif eleman bulunduğunda break veya return ile erken çıkış yapılıyor mu?"
  - "Bulunamazsa -1 dönüyor mu?"
reference_solution_path: private/solutions/c-veryeasy-find-first-negative.c
hint_ladder:
  1: "Diziyi gezerken arr[i] < 0 şartı sağlandığı anda ne yapılmalıdır?"
  2: "Sonuna kadar gidip bulamama durumunda ne döndürülür?"
  3: "Bu arama işlemi 'ilk negatif eleman taraması (first negative search)' olarak bilinir."
```

---
### c-veryeasy-prefix-sum-inplace

```yaml
id: c-veryeasy-prefix-sum-inplace
version: 1
language: c
engine: none
difficulty: very_easy
title: "Diziyi yerinde kümülatif ön ek toplamına dönüştürme"
prompt: |
  n elemanlı bir tamsayı dizisini, her elemanın kendisinden önceki tüm elemanların toplamını
  barındırdığı kümülatif ön ek toplamı (prefix sum) dizisine yerinde (in-place) dönüştüren
  `void prefix_sum_inplace(int *arr, size_t n)` fonksiyonunu yazın. Ekstra dizi tahsis
  etmeden tek geçişte tamamlayın. n dizi uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "1. indeksten başlayarak bir önceki toplam eklenmeli"
expected:
  time: { prefix_sum_inplace: "n" }
  space: "1"
concept_tags: [arrays, loop-invariant]
checklist_extra:
  - "Döngü 1. indeksten başlatılarak `arr[i] += arr[i-1]` yapılmış mı?"
  - "n < 2 durumları güvenle ele alınmış mı?"
reference_solution_path: private/solutions/c-veryeasy-prefix-sum-inplace.c
hint_ladder:
  1: "Her elemanı bir önceki kümülatif toplamla toplamak için döngü hangi indeksten başlamalıdır?"
  2: "Ek dizi oluşturmadan dizinin kendi hücrelerini güncellemek bellek karmaşıklığını nasıl O(1) yapar?"
  3: "Bu algoritma 'yerinde ön ek toplamı (in-place prefix sum)' olarak bilinir."
```

---
### c-veryeasy-is-char-alphanumeric

```yaml
id: c-veryeasy-is-char-alphanumeric
version: 1
language: c
engine: none
difficulty: very_easy
title: "Karakterin alfasayısal olduğunu denetleme"
prompt: |
  Standart `isalnum` fonksiyonunu kullanmadan, bir karakterin ASCII harf ('a'-'z', 'A'-'Z')
  veya rakam ('0'-'9') olup olmadığını denetleyen `int is_alphanumeric(int c)` fonksiyonunu
  yazın. Karakter alfasayısal ise 1, değilse 0 dönmelidir.
constraints:
  - "Zaman karmaşıklığı O(1) sabit sürede olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "ASCII aralıkları güvenle kontrol edilmeli"
expected:
  time: { is_alphanumeric: "1" }
  space: "1"
concept_tags: [strings, edge-cases]
checklist_extra:
  - "Küçük harf, büyük harf ve rakam aralıkları eksiksiz birleştirilmiş mi?"
  - "Mantıksal VEYA (||) operatörü doğru kurgulanmış mı?"
reference_solution_path: private/solutions/c-veryeasy-is-char-alphanumeric.c
hint_ladder:
  1: "ASCII tablosunda rakamlar, büyük harfler ve küçük harfler hangi aralıklardadır?"
  2: "Üç aralıktan birine uyma durumunu tek bir if koşulunda nasıl yazarsınız?"
  3: "Bu karakter sınıflandırması 'alfasayısal karakter denetimi (alphanumeric check)' olarak bilinir."
```

---
### c-veryeasy-count-words-whitespace

```yaml
id: c-veryeasy-count-words-whitespace
version: 1
language: c
engine: none
difficulty: very_easy
title: "Boşluklarla ayrılmış kelimelerin sayısını bulma"
prompt: |
  Boş karakterle sonlandırılmış bir metinde, boşluk karakterleriyle (`' '`, `'\t'`, `'\n'`)
  ayrılmış toplam kelime sayısını hesaplayan `size_t count_words(const char *str)` fonksiyonunu
  yazın. Ardışık birden fazla boşluk tek bir ayraç kabul edilmeli; metnin başındaki ve sonundaki
  boşluklar kelime sayılmamalıdır. n metnin karakter sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) tek geçişte olmalı"
  - "Ek bellek O(1) olmalı (durum makinesi bayrağı)"
  - "Ardışık boşluklar birden çok kelime üretmemeli"
expected:
  time: { count_words: "n" }
  space: "1"
concept_tags: [strings, state-machine]
checklist_extra:
  - "Bir kelimenin içinde olup olmadığını tutan bir durum bayrağı (in_word) kullanılmış mı?"
  - "Metin başındaki ve sonundaki boşluklar kelime sayısını yanıltıyor mu?"
reference_solution_path: private/solutions/c-veryeasy-count-words-whitespace.c
hint_ladder:
  1: "Boşluktan boşluk olmayan bir karaktere geçiş anı bize neyi haber verir?"
  2: "İki durumlu (kelime içi / kelime dışı) basit bir bayrakla sayacı ne zaman artırırız?"
  3: "Bu metin ayrıştırma tekniği 'durum bayraklı kelime sayımı (word count state machine)' olarak bilinir."
```

---
### c-veryeasy-replace-char-inplace

```yaml
id: c-veryeasy-replace-char-inplace
version: 1
language: c
engine: none
difficulty: very_easy
title: "Metindeki hedef karakteri başka bir karakterle değiştirme"
prompt: |
  Boş karakterle sonlandırılmış bir metin içinde geçen tüm `old_char` karakterlerini
  `new_char` karakteriyle yerinde değiştiren `size_t replace_char_inplace(char *str, char old_char, char new_char)`
  fonksiyonunu yazın. Fonksiyon kaç adet karakterin değiştirildiğini döndürmelidir.
  Metin sonlandırıcı null karakter değiştirilemez. n metnin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Değiştirilen karakter adedi döndürülmeli"
expected:
  time: { replace_char_inplace: "n" }
  space: "1"
concept_tags: [strings, pointers]
checklist_extra:
  - "old_char == '\\0' durumu için işlem engellenmiş mi?"
  - "Değiştirme sayacı doğru artırılıyor mu?"
reference_solution_path: private/solutions/c-veryeasy-replace-char-inplace.c
hint_ladder:
  1: "Dizgiyi gezerken *str == old_char koşulu sağlandığında ne yapılır?"
  2: "Null karakterin kazara değiştirilmesini önlemek için hangi kontrol şarttır?"
  3: "Bu metin güncellemesi 'yerinde karakter ikamesi (in-place character replacement)' olarak bilinir."
```

---
### c-veryeasy-scalar-multiply-array

```yaml
id: c-veryeasy-scalar-multiply-array
version: 1
language: c
engine: none
difficulty: very_easy
title: "Diziyi skaler bir katsayı ile çarpma"
prompt: |
  n elemanlı bir tamsayı dizisinin her bir elemanını verilen `factor` katsayısıyla yerinde
  çarpan `void scalar_multiply_array(int *arr, size_t n, int factor)` fonksiyonunu yazın.
  İşaretçi NULL veya n = 0 ise hiçbir işlem yapılmamalıdır. n dizi eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek karmaşıklığı O(1) olmalı"
  - "Yerinde (in-place) güncelleme yapılmalı"
expected:
  time: { scalar_multiply_array: "n" }
  space: "1"
concept_tags: [arrays, pointers]
checklist_extra:
  - "arr NULL kontrolü yapılmış mı?"
  - "Her eleman `arr[i] *= factor` ile güncellenmiş mi?"
reference_solution_path: private/solutions/c-veryeasy-scalar-multiply-array.c
hint_ladder:
  1: "Dizinin her hücresini verilen çarpanla güncellemek için tek döngü yeterli midir?"
  2: "İşaretçi adresi geçerli değilse programın çökmesini nasıl engellersiniz?"
  3: "Bu vektör işlemi 'skaler dizi çarpımı (scalar multiplication)' olarak bilinir."
```

---
### c-veryeasy-count-matching-elements

```yaml
id: c-veryeasy-count-matching-elements
version: 1
language: c
engine: none
difficulty: very_easy
title: "İki dizide aynı indeksteki eşleşen eleman sayısı"
prompt: |
  Aynı n uzunluğuna sahip iki tamsayı dizisinde (`a` ve `b`), aynı indekste eşit değere
  sahip olan (`a[i] == b[i]`) eleman çiftlerinin toplam adedini bulan
  `size_t count_matching_elements(const int *a, const int *b, size_t n)` fonksiyonunu yazın.
  İşaretçilerden biri NULL ise 0 dönmelidir. n dizi boyutunu ifade eder.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek karmaşıklığı O(1) olmalı"
  - "Diziler salt okunur (const) tutulmalı"
expected:
  time: { count_matching_elements: "n" }
  space: "1"
concept_tags: [arrays, memory-safety]
checklist_extra:
  - "İki dizinin de NULL kontrolü yapılmış mı?"
  - "Eşleşme sayacı size_t tipinde tutulmuş mu?"
reference_solution_path: private/solutions/c-veryeasy-count-matching-elements.c
hint_ladder:
  1: "Aynı indeksteki iki değeri karşılaştırmak için tek bir for döngüsü yeterli midir?"
  2: "İşaretçilerin ikisinin de geçerli olduğunu döngü öncesinde nasıl doğrularsınız?"
  3: "Bu dizi karşılaştırması 'indeks eşleşme sayımı (element-wise match count)' olarak bilinir."
```

---
### c-veryeasy-is-identity-matrix

```yaml
id: c-veryeasy-is-identity-matrix
version: 1
language: c
engine: none
difficulty: very_easy
title: "Birim matris denetimi"
prompt: |
  Tek boyutlu dizide satır-öncelikli (row-major) olarak saklanan n x n boyutundaki bir kare
  matrisin birim matris (ana köşegeni 1, diğer tüm elemanları 0) olup olmadığını denetleyen
  `int is_identity_matrix(const int *matrix, size_t n)` fonksiyonunu yazın. Birim matris ise
  1, değilse 0 dönmelidir. n satır ve sütun sayısıdır.
constraints:
  - "Eleman sayısı n için zaman karmaşıklığı O(n^2) olmalı"
  - "Ek bellek karmaşıklığı O(1) olmalı"
  - "Kuralı bozan ilk elemanda erken çıkış yapılmalı"
expected:
  time: { is_identity_matrix: "n^2" }
  space: "1"
concept_tags: [arrays, loop-invariant]
checklist_extra:
  - "2D indeksleme formülü `matrix[row * n + col]` doğru yazılmış mı?"
  - "Köşegen (row == col) için 1, köşegen dışı için 0 kontrolü yapılmış mı?"
reference_solution_path: private/solutions/c-veryeasy-is-identity-matrix.c
hint_ladder:
  1: "Satır ve sütun numarası eşit olduğunda (row == col) değerin ne olması gerekir?"
  2: "row != col iken değer sıfırdan farklıysa matris birim matris olabilir mi?"
  3: "Bu matris doğrulama işlemi 'birim matris denetimi (identity matrix check)' olarak bilinir."
```

---
### c-veryeasy-matrix-trace-sum

```yaml
id: c-veryeasy-matrix-trace-sum
version: 1
language: c
engine: none
difficulty: very_easy
title: "Kare matrisin köşegen iz toplamı"
prompt: |
  Satır-öncelikli olarak saklanan n x n boyutundaki bir kare matrisin ana köşegeninde
  yer alan elemanların toplamını (matris izini / trace) hesaplayan
  `long long matrix_trace_sum(const int *matrix, size_t n)` fonksiyonunu yazın.
  Tüm matrisi n x n taramak yerine yalnızca ana köşegen elemanlarını doğrudan indeksleyerek
  O(n) sürede tamamlayın. n kare matrisin kenar boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) sürede tamamlanmalı (tüm matris taranmamalı)"
  - "Ek bellek kullanımı O(1) olmalı"
  - "Ara toplamlarda 64-bit long long akümülatör kullanılmalı"
expected:
  time: { matrix_trace_sum: "n" }
  space: "1"
concept_tags: [arrays, performance]
checklist_extra:
  - "İç içe çift döngü yerine tek döngüyle `matrix[i * n + i]` erişimi yapılmış mı?"
  - "Dönüş tipi taşmayı önleyecek long long seçilmiş mi?"
reference_solution_path: private/solutions/c-veryeasy-matrix-trace-sum.c
hint_ladder:
  1: "Ana köşegendeki elemanların satır ve sütun indeksleri (i, i) olduğuna göre tek döngü yeterli midir?"
  2: "Tek boyutlu düz dizide (i, i) hücresinin formülü i * n + i midir?"
  3: "Bu lineer cebir işlemi 'matris izi hesabı (matrix trace)' olarak bilinir."
```

---
### c-veryeasy-remove-trailing-whitespace

```yaml
id: c-veryeasy-remove-trailing-whitespace
version: 1
language: c
engine: none
difficulty: very_easy
title: "Metin sonundaki boşlukları yerinde budama"
prompt: |
  Boş karakterle sonlandırılmış bir dizginin sonunda yer alan tüm boşluk karakterlerini
  (' ', '\t', '\r', '\n') dizgiyi kopyalamadan, yerinde budayan (trim trailing whitespace)
  `void trim_trailing_whitespace(char *str)` fonksiyonunu yazın. Sondan geriye doğru
  tarayarak son geçerli karakterin hemen ardına `\0` yerleştirin. n metnin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "Tamamen boşluktan oluşan metinler için boş dizgi oluşturmalı"
expected:
  time: { trim_trailing_whitespace: "n" }
  space: "1"
concept_tags: [strings, pointers]
checklist_extra:
  - "Geriye doğru tarama sırasında negatif indekse düşme riski önlenmiş mi?"
  - "Metin sonuna null karakteri doğru konulmuş mu?"
reference_solution_path: private/solutions/c-veryeasy-remove-trailing-whitespace.c
hint_ladder:
  1: "Metnin en sonundaki karakterden geriye doğru yürüyerek boşluk olmayan ilk karakteri nasıl bulursunuz?"
  2: "O karakterin hemen bir sağına '\\0' koyduğumuzda metnin sonundaki boşluklara ne olur?"
  3: "Bu metin temizliği 'sondaki boşlukları budama (trim trailing whitespace)' olarak bilinir."
```

---
### c-veryeasy-find-second-largest

```yaml
id: c-veryeasy-find-second-largest
version: 1
language: c
engine: none
difficulty: very_easy
title: "Dizideki en büyük ikinci farklı değeri bulma"
prompt: |
  n elemanlı bir tamsayı dizisindeki en büyük ikinci farklı değeri bulan
  `int find_second_largest(const int *arr, size_t n, int *out_second)` fonksiyonunu yazın.
  Diziyi sıralamadan tek geçişte en büyük ve ikinci en büyük adaylarını takip edin.
  Dizide en az iki farklı değer varsa ikinci değer `out_second` adresine yazılıp 1 dönmeli,
  tüm elemanlar eşitse veya n < 2 ise 0 dönmelidir. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) tek geçiş olmalı (sıralama yapılamaz)"
  - "Ek bellek kullanımı O(1) olmalı"
  - "Farklı ikinci değer bulunamazsa 0 dönmeli"
expected:
  time: { find_second_largest: "n" }
  space: "1"
concept_tags: [arrays, edge-cases]
checklist_extra:
  - "Dizideki tüm elemanların aynı olması durumu (ör. [5, 5, 5]) 0 döndürüyor mu?"
  - "Tek geçişte hem first hem second max değişkenleri güncelleniyor mu?"
reference_solution_path: private/solutions/c-veryeasy-find-second-largest.c
hint_ladder:
  1: "Yeni bir eleman mevcut en büyükten büyükse, eski en büyük sayı neye dönüşür?"
  2: "Eleman en büyükten küçük ama ikinci büyükten büyükse hangi değişken güncellenir?"
  3: "Bu algoritma 'tek geçişte ikinci en büyük elemanı bulma (second largest element)' olarak bilinir."
```

---
### c-veryeasy-is-strictly-monotonic

```yaml
id: c-veryeasy-is-strictly-monotonic
version: 1
language: c
engine: none
difficulty: very_easy
title: "Kesin monoton artan dizi denetimi"
prompt: |
  n elemanlı bir dizinin kesin olarak artan (strictly increasing, eşitlik dahi kabul edilmez)
  olup olmadığını denetleyen `int is_strictly_increasing(const int *arr, size_t n)` fonksiyonunu
  yazın. Her eleman bir öncekinden kesinlikle büyük olmalıdır (`arr[i] > arr[i-1]`).
  Kural sağlanırsa 1, herhangi bir eşitlik veya azalma varsa 0 dönmelidir. n eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Eşit iki eleman görüldüğünde derhal 0 dönülmeli"
expected:
  time: { is_strictly_increasing: "n" }
  space: "1"
concept_tags: [arrays, loop-invariant]
checklist_extra:
  - "Eşitlik durumunda (`arr[i] <= arr[i-1]`) 0 dönülüyor mu?"
  - "Döngü 1'den n-1'e kadar güvenle çalışıyor mu?"
reference_solution_path: private/solutions/c-veryeasy-is-strictly-monotonic.c
hint_ladder:
  1: "Kesin artan dizide iki elemanın birbirine eşit olması kuralı bozar mı?"
  2: "arr[i] <= arr[i-1] şartı görüldüğü anda fonksiyon ne döndürmelidir?"
  3: "Bu matematiksel kontrol 'kesin monoton artış denetimi (strictly monotonic increasing)' olarak bilinir."
```

---
### c-veryeasy-accumulate-range

```yaml
id: c-veryeasy-accumulate-range
version: 1
language: c
engine: none
difficulty: very_easy
title: "1'den n'e kadar tamsayıların toplamı"
prompt: |
  1'den n pozitif tamsayısına kadar olan tüm sayıların toplamını döngü kurmadan, Gauss formülüyle
  hesaplayan `long long sum_up_to_n(unsigned int n)` fonksiyonunu yazın. `n * (n + 1)`
  çarpımının 32-bit tamsayı taşmasına uğramaması için çarpım öncesinde `long long` dönüşümü
  uygulayın. n hedef tamsayıdır.
constraints:
  - "Zaman karmaşıklığı O(1) sabit zamanda olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "Ara çarpım taşması 64-bit dönüşümle engellenmeli"
expected:
  time: { sum_up_to_n: "1" }
  space: "1"
concept_tags: [integer-overflow, performance]
checklist_extra:
  - "Gauss formülü `(long long)n * (n + 1) / 2` şeklinde taşmasız yazılmış mı?"
  - "Döngü yerine kapalı formül kullanılmış mı?"
reference_solution_path: private/solutions/c-veryeasy-accumulate-range.c
hint_ladder:
  1: "1'den n'e kadar sayıların toplamını veren meşhur Gauss formülü nedir?"
  2: "n değeri 100.000 olduğunda n * (n + 1) çarpımı standart 32-bit int içine sığar mı?"
  3: "Bu kapalı formül 'Gauss toplam formülü (arithmetic series sum)' olarak bilinir."
```

---
### c-veryeasy-count-null-pointers

```yaml
id: c-veryeasy-count-null-pointers
version: 1
language: c
engine: none
difficulty: very_easy
title: "İşaretçi dizisindeki boş işaretçi sayısı"
prompt: |
  n elemanlı bir işaretçi dizisinde (`void *const *ptrs`) kaç adet `NULL` işaretçi
  bulunduğunu sayan `size_t count_null_pointers(void *const *ptrs, size_t n)` fonksiyonunu
  yazın. ptrs dizisinin kendisi NULL ise 0 dönmelidir. n dizideki işaretçi sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "İşaretçi dizisinin işaret ettiği adresler güvenle kontrol edilmeli"
expected:
  time: { count_null_pointers: "n" }
  space: "1"
concept_tags: [pointers, memory-safety]
checklist_extra:
  - "Dizi işaretçisinin kendisi NULL olduğunda koruma sağlanmış mı?"
  - "Her eleman `ptrs[i] == NULL` ile denetlenmiş mi?"
reference_solution_path: private/solutions/c-veryeasy-count-null-pointers.c
hint_ladder:
  1: "Bir işaretçinin hiçbir geçerli nesneye işaret etmediğini gösteren standart makro nedir?"
  2: "İşaretçi dizisini tararken ptrs[i] == NULL karşılaştırması nasıl yapılır?"
  3: "Bu güvenlik taraması 'boş işaretçi sayımı (null pointer counting)' olarak bilinir."
```

---
### c-veryeasy-pointer-offset-advance

```yaml
id: c-veryeasy-pointer-offset-advance
version: 1
language: c
engine: none
difficulty: very_easy
title: "İşaretçi öteleme ve sınır doğrulama"
prompt: |
  n elemanlı bir dizinin başlangıç adresini alarak, bu adresi k adım ileriye öteleyen
  `const int *advance_pointer_safe(const int *base, size_t n, size_t k)` fonksiyonunu yazın.
  Eğer istenen öteleme adımı k dizinin sınırları dışına çıkıyorsa (`k >= n`) veya base NULL ise
  fonksiyon güvenli bir şekilde `NULL` döndürmelidir. n dizi boyutu, k öteleme miktarıdır.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Dizi sınırını aşan ötelemeler (`k >= n`) engellenmeli"
  - "Geçersiz durumlarda NULL dönmeli"
expected:
  time: { advance_pointer_safe: "1" }
  space: "1"
concept_tags: [pointer-arithmetic, memory-safety]
checklist_extra:
  - "k >= n sınır kontrolü yapılmış mı?"
  - "İşaretçi aritmetiği `base + k` ile doğru hesaplanmış mı?"
reference_solution_path: private/solutions/c-veryeasy-pointer-offset-advance.c
hint_ladder:
  1: "Bir işaretçiyi k eleman ileri kaydırmak için hangi aritmetik operatör kullanılır?"
  2: "Öteleme sonucunun dizinin sınırları içinde kaldığını nasıl garanti edersiniz?"
  3: "Bu işlem 'sınır korumalı işaretçi ötelemesi (safe pointer arithmetic)' olarak bilinir."
```

---
### c-veryeasy-initialize-struct-point

```yaml
id: c-veryeasy-initialize-struct-point
version: 1
language: c
engine: none
difficulty: very_easy
title: "Yapı örneğini başlatma ve sıfırlama"
prompt: |
  2D bir noktayı temsil eden `typedef struct { int x; int y; } Point;` yapısını başlatan
  `int init_point(Point *p, int x, int y)` fonksiyonunu yazın. İşaretçi NULL ise 0 dönmeli,
  geçerli ise koordinatları yapıya atayıp 1 dönmelidir.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "İşaretçi NULL ise 0 dönmeli"
  - "Ok operatörü (`->`) ile üyelere güvenle atanmalı"
expected:
  time: { init_point: "1" }
  space: "1"
concept_tags: [pointers, memory-safety]
checklist_extra:
  - "p == NULL kontrolü yapılmış mı?"
  - "p->x ve p->y atamaları doğru yapılmış mı?"
reference_solution_path: private/solutions/c-veryeasy-initialize-struct-point.c
hint_ladder:
  1: "Bir yapı işaretçisinin içindeki alanlara erişmek için hangi operatör kullanılır?"
  2: "İşaretçinin geçerliliği denetlenmeden atama yapılırsa ne olur?"
  3: "Bu başlatma işlemi 'yapı işaretçisi başlatma (struct pointer initialization)' olarak bilinir."
```

---
### c-veryeasy-manhattan-distance

```yaml
id: c-veryeasy-manhattan-distance
version: 1
language: c
engine: none
difficulty: very_easy
title: "İki nokta arasındaki Manhattan mesafesi"
prompt: |
  `Point` yapısına (`int x, y`) sahip iki nokta arasındaki Manhattan mesafesini
  (`|x1 - x2| + |y1 - y2|`) hesaplayan `unsigned int manhattan_distance(Point a, Point b)`
  fonksiyonunu yazın. Koordinat farklarını mutlak değere çevirirken tamsayı taşmasını önleyin.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "İki eksendeki mutlak farklar toplanmalı"
  - "Taşma güvenliği sağlanmalı"
expected:
  time: { manhattan_distance: "1" }
  space: "1"
concept_tags: [integer-overflow, edge-cases]
checklist_extra:
  - "X ve Y ekseni farkları ayrı ayrı mutlak değere alınmış mı?"
  - "Dönüş tipi unsigned int ile negatiflikten arındırılmış mı?"
reference_solution_path: private/solutions/c-veryeasy-manhattan-distance.c
hint_ladder:
  1: "Manhattan mesafesi iki noktanın yatay ve dikey farklarının mutlak toplamı mıdır?"
  2: "Farkları alırken büyük koordinattan küçüğü çıkarmak taşmayı nasıl önler?"
  3: "Bu metrik 'Manhattan ızgara mesafesi (Manhattan distance)' olarak bilinir."
```

---
### c-veryeasy-check-null-terminated

```yaml
id: c-veryeasy-check-null-terminated
version: 1
language: c
engine: none
difficulty: very_easy
title: "Tampon içinde null sonlandırıcı varlığını doğrulama"
prompt: |
  Belirli bir `max_len` baytlık bellek tamponu içinde, tampon sınırları aşılmadan bir
  null sonlandırıcı (`\0`) karakter bulunup bulunmadığını denetleyen
  `int is_null_terminated(const char *buf, size_t max_len)` fonksiyonunu yazın. Tampon içinde
  null karakter varsa 1, `max_len` taranıp bulunamazsa veya `buf == NULL` ise 0 dönmelidir.
  n tamponun incelenen bayt sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "`max_len` sınırı asla aşılmamalı (out-of-bounds engeli)"
  - "Null bulunursa derhal 1 dönmeli"
expected:
  time: { is_null_terminated: "n" }
  space: "1"
concept_tags: [strings, memory-safety]
checklist_extra:
  - "Döngü sayacı `i < max_len` sınırını kesinlikle aşmıyor mu?"
  - "Null bulunduğunda 1 ile erken çıkış yapılıyor mu?"
reference_solution_path: private/solutions/c-veryeasy-check-null-terminated.c
hint_ladder:
  1: "Bilinmeyen bir bellek bölgesinde strlen çağırırsak ve null yoksa ne felaketi yaşanır?"
  2: "Belirli bir maksimum sınır içinde null aramak bellek güvenliğini nasıl kurtarır?"
  3: "Bu güvenlik kuralı 'sınır korumalı null sonlandırıcı denetimi (bounded null check)' olarak bilinir."
```

---
### c-veryeasy-left-shift-array-one

```yaml
id: c-veryeasy-left-shift-array-one
version: 1
language: c
engine: none
difficulty: very_easy
title: "Dizi elemanlarını bir basamak sola kaydırma"
prompt: |
  n elemanlı bir tamsayı dizisinin tüm elemanlarını 1 pozisyon sola kaydıran, ilk elemanı
  kaybedip dizinin son elemanına 0 yazan `void shift_array_left_by_one(int *arr, size_t n)`
  fonksiyonunu yazın. Dizi yerinde (in-place) güncellenmelidir. n dizi uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek karmaşıklığı O(1) olmalı"
  - "Son eleman 0 ile doldurulmalı"
expected:
  time: { shift_array_left_by_one: "n" }
  space: "1"
concept_tags: [arrays, pointers]
checklist_extra:
  - "Kaydırma döngüsü soldan sağa doğru `arr[i] = arr[i+1]` şeklinde yapılmış mı?"
  - "n = 0 ve n = 1 sınır durumları güvenle ele alınmış mı?"
reference_solution_path: private/solutions/c-veryeasy-left-shift-array-one.c
hint_ladder:
  1: "Elemanları sola kaydırırken döngü 0'dan n-2'ye kadar mı gitmelidir?"
  2: "Döngü bittikten sonra en son hücreye (arr[n-1]) ne atanmalıdır?"
  3: "Bu temel dizi operasyonu 'tek basamak sola kaydırma (array left shift by one)' olarak bilinir."
```

---
### c-veryeasy-right-shift-array-one

```yaml
id: c-veryeasy-right-shift-array-one
version: 1
language: c
engine: none
difficulty: very_easy
title: "Dizi elemanlarını bir basamak sağa kaydırma"
prompt: |
  n elemanlı bir tamsayı dizisinin tüm elemanlarını 1 pozisyon sağa kaydıran, son elemanı
  dışarı atıp dizinin başına (0. indekse) 0 yazan `void shift_array_right_by_one(int *arr, size_t n)`
  fonksiyonunu yazın. Elemanların birbirini ezmemesi için kaydırmayı sondan başa doğru
  gerçekleştirin. n dizi eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "Kaydırma yönü nedeniyle sondan başa doğru taranmalı"
expected:
  time: { shift_array_right_by_one: "n" }
  space: "1"
concept_tags: [arrays, edge-cases]
checklist_extra:
  - "Baştan başlandığında tüm elemanların aynı değerle ezilmesi hatası önlenmiş mi?"
  - "İlk elemana 0 atanmış mı?"
reference_solution_path: private/solutions/c-veryeasy-right-shift-array-one.c
hint_ladder:
  1: "Elemanları sağa kaydırırken soldan başlarsanız ne olur? Veri ezilir mi?"
  2: "Veri kaybını önlemek için döngünün n-1'den geriye doğru gitmesi neden şarttır?"
  3: "Bu işlem 'tersten dizi sağa kaydırma (array right shift by one)' olarak bilinir."
```

---
### c-veryeasy-is-even-bitwise

```yaml
id: c-veryeasy-is-even-bitwise
version: 1
language: c
engine: none
difficulty: very_easy
title: "Bit düzeyinde AND ile çift sayı kontrolü"
prompt: |
  Mod alma operatörü (`%`) kullanmadan, yalnızca bit düzeyinde VE (`&`) operatörünü kullanarak
  bir tamsayının çift olup olmadığını denetleyen `int is_even_bitwise(int n)` fonksiyonunu yazın.
  Sayı çift ise 1, tek ise 0 dönmelidir. Negatif sayılarda da kusursuz çalışmalıdır.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Mod operatörü (`%`) kullanılmamalı, bitwise işlem tercih edilmeli"
  - "Negatif tamsayılarda ikiye tümleyen aritmetiği korunmalı"
expected:
  time: { is_even_bitwise: "1" }
  space: "1"
concept_tags: [edge-cases, performance]
checklist_extra:
  - "En düşük anlamlı bit (LSB) `(n & 1) == 0` ile denetlenmiş mi?"
  - "Parantezleme operatör önceliğine uygun mu?"
reference_solution_path: private/solutions/c-veryeasy-is-even-bitwise.c
hint_ladder:
  1: "İkili tabanda çift sayıların en son biti (en sağdaki bit) her zaman kaçtır?"
  2: "Bir sayının son bitini izole etmek için hangi sayıyla AND (&) işlemi yapılır?"
  3: "Bu donanım seviyesi kontrol 'bit düzeyinde çiftlik denetimi (bitwise even check)' olarak bilinir."
```

---
### c-veryeasy-toggle-bit

```yaml
id: c-veryeasy-toggle-bit
version: 1
language: c
engine: none
difficulty: very_easy
title: "Belirli bir indeksteki biti tersine çevirme"
prompt: |
  Verilen 32-bitlik işaretsiz bir tamsayının `k`ıncı bitini (0-31 aralığında) tersine çeviren
  (0 ise 1, 1 ise 0 yapan) `unsigned int toggle_bit(unsigned int num, unsigned int k)`
  fonksiyonunu yazın. k >= 32 ise sayı değiştirilmeden dönmelidir. Bit düzeyinde XOR (`^`)
  operatörünü kullanın.
constraints:
  - "Zaman karmaşıklığı O(1) sabit sürede olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "`k >= 32` tanımsız bit kaydırma hatası (UB) engellenmeli"
expected:
  time: { toggle_bit: "1" }
  space: "1"
concept_tags: [undefined-behavior, performance]
checklist_extra:
  - "k >= 32 taşma kontrolü yapılmış mı?"
  - "XOR maskesi `(1U << k)` doğru oluşturulmuş mu?"
reference_solution_path: private/solutions/c-veryeasy-toggle-bit.c
hint_ladder:
  1: "Bir biti tersine çevirmek için hangi mantıksal bit operatörü kullanılır?"
  2: "Sadece k'ıncı biti 1 olan bir maske üretmek için 1 sayısı sola kaç kez kaydırılır?"
  3: "Bu işlem 'bit evirme işlemi (bit toggle XOR mask)' olarak bilinir."
```

---
### c-veryeasy-min-max-pair

```yaml
id: c-veryeasy-min-max-pair
version: 1
language: c
engine: none
difficulty: very_easy
title: "Tek geçişte hem minimum hem maksimumu bulma"
prompt: |
  n elemanlı bir tamsayı dizisini yalnızca bir kez tarayarak hem en küçük hem en büyük
  değeri bir yapıda döndüren `typedef struct { int min; int max; } MinMax;`
  `MinMax find_min_max_pair(const int *arr, size_t n)` fonksiyonunu yazın. Dizi boşsa
  veya NULL ise yapının her iki üyesi 0 olmalıdır. n eleman adedidir.
constraints:
  - "Dizi boyutu n için tek geçişte O(n) sürede tamamlanmalı"
  - "Ek bellek O(1) olmalı"
  - "Sonuç yapı olarak döndürülmeli"
expected:
  time: { find_min_max_pair: "n" }
  space: "1"
concept_tags: [arrays, loop-invariant]
checklist_extra:
  - "Dizi iki ayrı döngüde taranmak yerine tek döngüde mi bitirilmiş?"
  - "İlk eleman başlangıçta hem min hem max olarak atanmış mı?"
reference_solution_path: private/solutions/c-veryeasy-min-max-pair.c
hint_ladder:
  1: "Diziyi iki defa gezmek yerine tek döngüde hem min hem max güncellenebilir mi?"
  2: "Sonucu iki ayrı işaretçi yerine tek bir C struct içinde döndürmenin avantajı nedir?"
  3: "Bu algoritma 'tek geçişte uç değer bulma (single-pass min-max pair)' olarak bilinir."
```

---
### c-easy-string-length

```yaml
id: c-easy-string-length
version: 1
language: c
engine: none
difficulty: easy
title: "Null ile sonlandırılmış dizginin uzunluğunu hesaplama"
prompt: |
  Null karakter ('\0') ile sonlandırılmış bir karakter dizisinin uzunluğunu standart kütüphane kullanmadan hesaplayan `size_t custom_strlen(const char *str)` fonksiyonunu yazın. n dizginin karakter sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "str NULL ise 0 dönmeli"
expected:
  time: { custom_strlen: "n" }
  space: "1"
concept_tags: [strings, pointers]
checklist_extra:
  - "İşaretçi NULL olduğunda güvenli dönüş yapılmış mı?"
  - "Null terminatör karakteri sayıma dahil edilmemiş mi?"
reference_solution_path: private/solutions/c-easy-string-length.c
hint_ladder:
  1: "Null karakteri görene kadar işaretçiyi birer birer nasıl ilerletirsiniz?"
  2: "Başlangıç adresi ile son ulaşılan adres arasındaki farkı almak doğrudan uzunluğu verir mi?"
  3: "Bu işlem 'karakter dizisi uzunluğu hesaplama (string length)' olarak bilinir."
```

---
### c-easy-count-vowels

```yaml
id: c-easy-count-vowels
version: 1
language: c
engine: none
difficulty: easy
title: "Dizgideki sesli harf sayısını bulma"
prompt: |
  Verilen bir metin içindeki Türkçe olmayan standart sesli harflerin (a, e, i, o, u, A, E, I, O, U) toplam adedini bulan `size_t count_vowels(const char *str)` fonksiyonunu yazın. n metnin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "NULL işaretçi kontrolü yapılmalı"
expected:
  time: { count_vowels: "n" }
  space: "1"
concept_tags: [strings, loop-invariant]
checklist_extra:
  - "Hem büyük hem küçük harfler doğru kontrol edilmiş mi?"
  - "NULL girdi güvenle ele alınmış mı?"
reference_solution_path: private/solutions/c-easy-count-vowels.c
hint_ladder:
  1: "Her bir karakterin sesli harf kümesinde olup olmadığını sabit sürede nasıl denetlersiniz?"
  2: "Döngü içerisinde büyük/küçük harf ayrımını basitleştirmek için tolower mantığı kullanılabilir mi?"
  3: "Bu arama ve filtreleme yaklaşımı 'sesli harf sayımı (vowel counting)' olarak bilinir."
```

---
### c-easy-char-frequency

```yaml
id: c-easy-char-frequency
version: 1
language: c
engine: none
difficulty: easy
title: "Dizgide hedef karakterin geçme sıklığını hesaplama"
prompt: |
  Verilen bir dizgi içinde belirli bir karakterin kaç kez geçtiğini sayan `size_t count_char_occurrence(const char *str, char target)` fonksiyonunu yazın. n metnin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "str NULL ise 0 dönmeli"
expected:
  time: { count_char_occurrence: "n" }
  space: "1"
concept_tags: [strings, pointers]
checklist_extra:
  - "Hedef karakter null terminatör ise davranış doğru mu?"
  - "NULL işaretçi kontrolü yapılmış mı?"
reference_solution_path: private/solutions/c-easy-char-frequency.c
hint_ladder:
  1: "Dizgiyi baştan sona gezen bir işaretçi ile her adımda target karakteriyle karşılaştırma yapın."
  2: "Hedef '\0' ise dizgi sonuna ulaşıldığında döngü nasıl sonlanmalıdır?"
  3: "Bu algoritma 'karakter frekans sayımı (character frequency)' olarak bilinir."
```

---
### c-easy-array-reverse

```yaml
id: c-easy-array-reverse
version: 1
language: c
engine: none
difficulty: easy
title: "Tamsayı dizisini yerinde tersine çevirme"
prompt: |
  n elemanlı bir tamsayı dizisini ek bellek ayırmadan yerinde tersine çeviren `void reverse_int_array(int *arr, size_t n)` fonksiyonunu yazın. n dizinin eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı (in-place)"
  - "n <= 1 durumlarında dizi değişmemeli"
expected:
  time: { reverse_int_array: "n" }
  space: "1"
concept_tags: [arrays, pointer-arithmetic]
checklist_extra:
  - "İki işaretçi karşılıklı ilerlerken orta noktada doğru duruyor mu?"
  - "n sıfır veya bir iken bellek ihlali engellenmiş mi?"
reference_solution_path: private/solutions/c-easy-array-reverse.c
hint_ladder:
  1: "Biri dizinin başında, diğeri sonunda iki işaretçi veya indeks tanımlayabilirsiniz."
  2: "İşaretçiler birbirini geçene kadar elemanları takas edip merkeze doğru birer adım yaklaşın."
  3: "Bu teknik 'çift işaretçi ile yerinde ters çevirme (two-pointer in-place reversal)' olarak bilinir."
```

---
### c-easy-check-sorted

```yaml
id: c-easy-check-sorted
version: 1
language: c
engine: none
difficulty: easy
title: "Dizinin artan sırada olup olmadığını denetleme"
prompt: |
  n elemanlı bir tamsayı dizisinin küçükten büyüğe sıralı (her eleman bir öncekinden büyük veya eşit) olup olmadığını denetleyen `bool is_array_sorted(const int *arr, size_t n)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı en kötü durumda O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "n < 2 için true dönmeli"
expected:
  time: { is_array_sorted: "n" }
  space: "1"
concept_tags: [arrays, loop-invariant]
checklist_extra:
  - "Döngü n-1 sınırına kadar güvenle ilerliyor mu?"
  - "Sıralamayı bozan ilk ikilide erken çıkış (early exit) yapılıyor mu?"
reference_solution_path: private/solutions/c-easy-check-sorted.c
hint_ladder:
  1: "Dizideki her elemanı kendisinden sonraki elemanla karşılaştırın."
  2: "Herhangi bir eleman bir sonrakinden büyükse hemen false dönebilir misiniz?"
  3: "Bu denetim 'sıralılık doğrulaması (is-sorted check)' olarak bilinir."
```

---
### c-easy-linear-search

```yaml
id: c-easy-linear-search
version: 1
language: c
engine: none
difficulty: easy
title: "Dizide doğrusal arama ve ilk indeksi bulma"
prompt: |
  n elemanlı tamsayı dizisinde hedef değeri arayan ve ilk bulunduğu indeksi döndüren, bulunamazsa -1 dönen `int linear_search(const int *arr, size_t n, int target)` fonksiyonunu yazın. n eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "arr NULL ise veya n 0 ise -1 dönmeli"
expected:
  time: { linear_search: "n" }
  space: "1"
concept_tags: [arrays, pointers]
checklist_extra:
  - "Hedef bulunduğunda döngü sonuna kadar beklemeden çıkılıyor mu?"
  - "Negatif indeks dönme durumu güvenli mi?"
reference_solution_path: private/solutions/c-easy-linear-search.c
hint_ladder:
  1: "0'dan n-1'e kadar tüm indeksleri sırayla ziyaret edin."
  2: "Değer eşleştiğinde o anki indeksi hemen döndürün."
  3: "Bu temel arama yöntemi 'doğrusal arama (linear search)' olarak bilinir."
```

---
### c-easy-count-occurrences

```yaml
id: c-easy-count-occurrences
version: 1
language: c
engine: none
difficulty: easy
title: "Dizide belirli bir tamsayının sıklığını sayma"
prompt: |
  n elemanlı bir dizide verilen hedef tamsayının kaç kez yer aldığını hesaplayan `size_t count_int_occurrences(const int *arr, size_t n, int target)` fonksiyonunu yazın. n dizi eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "arr NULL ise 0 dönmeli"
expected:
  time: { count_int_occurrences: "n" }
  space: "1"
concept_tags: [arrays, loop-invariant]
checklist_extra:
  - "Dizi sınırları tam olarak taranıyor mu?"
  - "Sayaç taşma riski olmadan artırılıyor mu?"
reference_solution_path: private/solutions/c-easy-count-occurrences.c
hint_ladder:
  1: "Diziyi tek bir döngüde tarayıp hedefle eşleşen elemanlarda sayacı bir artırın."
  2: "Tüm elemanlar gezildikten sonra sayacın nihai değerini döndürün."
  3: "Bu işlem 'eleman frekansı sayımı (occurrence counting)' olarak bilinir."
```

---
### c-easy-sum-even-numbers

```yaml
id: c-easy-sum-even-numbers
version: 1
language: c
engine: none
difficulty: easy
title: "Dizideki çift sayıların toplamını hesaplama"
prompt: |
  n elemanlı bir tamsayı dizisindeki çift sayıların toplamını hesaplayan `long long sum_even_numbers(const int *arr, size_t n)` fonksiyonunu yazın. Olası taşmaları önlemek için dönüş tipi 64-bit tamsayı olmalıdır. n dizi eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Toplama işlemi 64-bit tamsayıda biriktirilmeli"
expected:
  time: { sum_even_numbers: "n" }
  space: "1"
concept_tags: [arrays, integer-overflow]
checklist_extra:
  - "Negatif çift sayılar doğru modül ile tespit edilmiş mi?"
  - "Büyük toplamlar için 64-bit biriktirici kullanılmış mı?"
reference_solution_path: private/solutions/c-easy-sum-even-numbers.c
hint_ladder:
  1: "Bir sayının çift olup olmadığını bit düzeyi VE (val & 1) veya modül (val % 2 == 0) ile nasıl anlarsınız?"
  2: "Negatif sayılarda modül operatörünün sonucuna dikkat edin."
  3: "Bu işlem 'çift sayıların filtrelenerek toplanması (even numbers summation)' olarak bilinir."
```

---
### c-easy-copy-string

```yaml
id: c-easy-copy-string
version: 1
language: c
engine: none
difficulty: easy
title: "Güvenli dizgi kopyalama fonksiyonu gerçekleştirme"
prompt: |
  Kaynak dizgiyi hedef tampona kopyalayan ve hedef tampon sınırını aşmadan daima null karakteri ekleyen `char *safe_strcpy(char *dest, size_t dest_size, const char *src)` fonksiyonunu yazın. n kaynak metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "dest_size sıfır ise hiçbir yazma yapılmamalı"
expected:
  time: { safe_strcpy: "n" }
  space: "1"
concept_tags: [strings, memory-safety]
checklist_extra:
  - "dest_size sınırına ulaşıldığında null terminatör yazılması garanti edilmiş mi?"
  - "src veya dest NULL ise güvenli dönüş sağlanmış mı?"
reference_solution_path: private/solutions/c-easy-copy-string.c
hint_ladder:
  1: "Hedef tamponda en fazla dest_size - 1 karakter kopyalayabilir, son karaktere '\0' yazmalısınız."
  2: "Kaynak dizgi hedeften kısaysa ne zaman durmalısınız?"
  3: "Bu güvenli kopyalama yaklaşımı 'sınır korumalı dizgi kopyalama (bounded string copy)' olarak bilinir."
```

---
### c-easy-concat-strings

```yaml
id: c-easy-concat-strings
version: 1
language: c
engine: none
difficulty: easy
title: "Sınır korumalı iki dizgiyi birleştirme"
prompt: |
  Hedef dizginin sonuna kaynak dizgiyi ekleyen ve hedef tamponun dest_size sınırını aşmayan `char *safe_strcat(char *dest, size_t dest_size, const char *src)` fonksiyonunu yazın. n hedef ve m kaynak dizgi uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n + m) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Hedef daima null ile sonlandırılmalı"
expected:
  time: { safe_strcat: "n + m" }
  space: "1"
concept_tags: [strings, memory-safety]
checklist_extra:
  - "Hedef dizginin mevcut uzunluğu dest_size'dan büyükse tanımsız davranış önlenmiş mi?"
  - "Kalan boşluktan fazla karakter yazılmaması sağlanmış mı?"
reference_solution_path: private/solutions/c-easy-concat-strings.c
hint_ladder:
  1: "Önce hedef dizginin sonundaki null karakterin indeksini bulun."
  2: "Kalan alana kaynak dizginin karakterlerini sırayla ekleyip sonuna null koyun."
  3: "Bu işlem 'sınır korumalı dizgi bitiştirme (bounded string concatenation)' olarak bilinir."
```

---
### c-easy-find-first-non-repeating

```yaml
id: c-easy-find-first-non-repeating
version: 1
language: c
engine: none
difficulty: easy
title: "Küçük harf dizgisinde tekrarlanmayan ilk karakteri bulma"
prompt: |
  Yalnızca İngilizce küçük harfler içeren bir dizgide yalnızca bir kez geçen ilk karakteri bulan, yoksa '\0' dönen `char first_unique_char(const char *str)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (26 boyutlu sabit dizi)"
  - "İki geçişte çözülmeli"
expected:
  time: { first_unique_char: "n" }
  space: "1"
concept_tags: [strings, arrays]
checklist_extra:
  - "Karakter frekansları için 26 elemanlı sabit dizi doğru sıfırlanmış mı?"
  - "İkinci geçişte ilk frekansı 1 olan karakter tespit edilip erken çıkış yapılmış mı?"
reference_solution_path: private/solutions/c-easy-find-first-non-repeating.c
hint_ladder:
  1: "İlk geçişte her harfin frekansını 26 elemanlı bir int dizisinde sayın."
  2: "İkinci geçişte metni baştan okuyarak frekansı 1 olan ilk harfi döndürün."
  3: "Bu algoritma 'tekrarlanmayan ilk karakteri bulma (first unique character)' olarak bilinir."
```

---
### c-easy-remove-element

```yaml
id: c-easy-remove-element
version: 1
language: c
engine: none
difficulty: easy
title: "Diziden hedef değeri yerinde silip yeni boyutu bulma"
prompt: |
  n elemanlı tamsayı dizisinden target değerine eşit tüm elemanları yerinde silen ve kalan eleman sayısını döndüren `size_t remove_target_value(int *arr, size_t n, int target)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı (in-place)"
  - "Kalan elemanların sırası korunmalıdır"
expected:
  time: { remove_target_value: "n" }
  space: "1"
concept_tags: [arrays, pointers]
checklist_extra:
  - "Yazma ve okuma indeksleri ayrıştırılarak tek geçişte yapılmış mı?"
  - "Yeni boyut doğru hesaplanıp döndürülmüş mü?"
reference_solution_path: private/solutions/c-easy-remove-element.c
hint_ladder:
  1: "Biri okuyan diğeri yazan iki indeks kullanarak diziyi tarayın."
  2: "Okunan eleman target değerine eşit değilse yazma indeksine kopyalayıp yazma indeksini artırın."
  3: "Bu teknik 'iki indeksli yerinde eleman filtreleme (two-pointer filter)' olarak bilinir."
```

---
### c-easy-remove-duplicates-sorted

```yaml
id: c-easy-remove-duplicates-sorted
version: 1
language: c
engine: none
difficulty: easy
title: "Sıralı dizideki mükerrer elemanları yerinde temizleme"
prompt: |
  Küçükten büyüğe sıralı n elemanlı bir dizideki yinelenen elemanları yerinde temizleyerek her elemanın bir kez kalmasını sağlayan `size_t remove_duplicates_sorted(int *arr, size_t n)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Benzersiz eleman adedi dönmeli"
expected:
  time: { remove_duplicates_sorted: "n" }
  space: "1"
concept_tags: [arrays, loop-invariant]
checklist_extra:
  - "Dizi boş veya 1 elemanlı olduğunda sınır kontrolü doğru çalışıyor mu?"
  - "Sıralı olma özelliğinden faydalanarak komşu elemanlar karşılaştırılmış mı?"
reference_solution_path: private/solutions/c-easy-remove-duplicates-sorted.c
hint_ladder:
  1: "Dizi zaten sıralı olduğundan aynı değerler yan yanadır."
  2: "Yavaş ilerleyen yazma işaretçisini sadece yeni ve farklı bir değer gördükçe ilerletin."
  3: "Bu algoritma 'sıralı dizide tekleştirme (deduplication of sorted array)' olarak bilinir."
```

---
### c-easy-rotate-array-by-one

```yaml
id: c-easy-rotate-array-by-one
version: 1
language: c
engine: none
difficulty: easy
title: "Diziyi bir adım sola kaydırma"
prompt: |
  n elemanlı tamsayı dizisinin tüm elemanlarını bir adım sola kaydıran, ilk elemanı ise dizinin sonuna taşıyan `void rotate_left_once(int *arr, size_t n)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "n <= 1 için dizi değişmemeli"
expected:
  time: { rotate_left_once: "n" }
  space: "1"
concept_tags: [arrays, pointer-arithmetic]
checklist_extra:
  - "İlk eleman geçici değişkende saklanıp en sona doğru yazılmış mı?"
  - "Elemanlar öne doğru taşınırken veri kaybı engellenmiş mi?"
reference_solution_path: private/solutions/c-easy-rotate-array-by-one.c
hint_ladder:
  1: "İlk elemanı geçici bir değişkende saklayın."
  2: "1. indeksten n-1. indekse kadar olan tüm elemanları birer indeks sola kopyalayın ve geçici değeri sona yazın."
  3: "Bu işlem 'diziyi tek adım sola döndürme (left rotation by one)' olarak bilinir."
```

---
### c-easy-array-element-swap

```yaml
id: c-easy-array-element-swap
version: 1
language: c
engine: none
difficulty: easy
title: "İki işaretçinin gösterdiği değerleri yer değiştirme"
prompt: |
  İki tamsayı işaretçisinin gösterdiği bellek hücrelerindeki değerleri takas eden `void swap_integers(int *a, int *b)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "İşaretçilerin NULL olup olmadığı denetlenmeli"
expected:
  time: { swap_integers: "1" }
  space: "1"
concept_tags: [pointers, memory-safety]
checklist_extra:
  - "İşaretçiler NULL ise bellek erişim hatası önlenmiş mi?"
  - "İşaretçiler aynı adresi gösteriyorsa (a == b) takas güvenli mi?"
reference_solution_path: private/solutions/c-easy-array-element-swap.c
hint_ladder:
  1: "Bir geçici tamsayı değişkeninde *a değerini saklayın."
  2: "*a adresine *b değerini, ardından *b adresine saklanan geçici değeri yazın."
  3: "Bu temel işlem 'işaretçi ile değer takası (pointer swap)' olarak bilinir."
```

---
### c-easy-clamp-values

```yaml
id: c-easy-clamp-values
version: 1
language: c
engine: none
difficulty: easy
title: "Dizideki değerleri alt ve üst sınırlar arasında kırpma"
prompt: |
  n elemanlı tamsayı dizisindeki değerleri min_val ve max_val sınırları arasında tutacak şekilde yerinde kırpan `void clamp_array_values(int *arr, size_t n, int min_val, int max_val)` fonksiyonunu yazın. n eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "min_val > max_val ise fonksiyon işlem yapmamalıdır"
expected:
  time: { clamp_array_values: "n" }
  space: "1"
concept_tags: [arrays, loop-invariant]
checklist_extra:
  - "min_val > max_val geçersiz sınır durumu başta denetlenmiş mi?"
  - "Her eleman yerinde güvenle güncellenmiş mi?"
reference_solution_path: private/solutions/c-easy-clamp-values.c
hint_ladder:
  1: "Döngü ile dizideki her elemanı gezin."
  2: "Eleman min_val'den küçükse min_val, max_val'den büyükse max_val olarak güncelleyin."
  3: "Bu sınırlandırma işlemi 'değer kırpma (clamping)' olarak bilinir."
```

---
### c-easy-replace-char

```yaml
id: c-easy-replace-char
version: 1
language: c
engine: none
difficulty: easy
title: "Dizgideki belirli bir karakteri başka karakterle değiştirme"
prompt: |
  Null ile sonlandırılmış bir metinde geçen tüm old_char karakterlerini new_char ile yerinde değiştiren `void replace_char(char *str, char old_char, char new_char)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "old_char null terminatör olamaz"
expected:
  time: { replace_char: "n" }
  space: "1"
concept_tags: [strings, pointers]
checklist_extra:
  - "old_char '\0' ise dizgi bütünlüğünün bozulması engellenmiş mi?"
  - "str NULL ise erken çıkış yapılmış mı?"
reference_solution_path: private/solutions/c-easy-replace-char.c
hint_ladder:
  1: "İşaretçi ile metni sonundaki null karaktere kadar tarayın."
  2: "Gördüğünüz her old_char yerine new_char yazarak ilerleyin."
  3: "Bu metin manipülasyonu 'yerinde karakter değiştirme (in-place character replacement)' olarak bilinir."
```

---
### c-easy-is-all-digits

```yaml
id: c-easy-is-all-digits
version: 1
language: c
engine: none
difficulty: easy
title: "Dizginin yalnızca rakamlardan oluştuğunu denetleme"
prompt: |
  Verilen bir metnin yalnızca '0'-'9' arasındaki rakam karakterlerinden oluşup oluşmadığını denetleyen `bool is_numeric_string(const char *str)` fonksiyonunu yazın. Boş metin için false dönmelidir. n dizginin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Boş dizgi ve NULL işaretçi için false dönmeli"
expected:
  time: { is_numeric_string: "n" }
  space: "1"
concept_tags: [strings, input-validation]
checklist_extra:
  - "Boş dizgi durumu doğru elenmiş mi?"
  - "Rakam olmayan ilk karakterde döngüden çıkılmış mı?"
reference_solution_path: private/solutions/c-easy-is-all-digits.c
hint_ladder:
  1: "str NULL veya boş ise doğrudan false dönün."
  2: "Tüm karakterlerin '0' ile '9' ASCII aralığında olduğunu sırayla kontrol edin."
  3: "Bu denetim 'sayısal karakter doğrulaması (numeric string validation)' olarak bilinir."
```

---
### c-easy-string-to-lower

```yaml
id: c-easy-string-to-lower
version: 1
language: c
engine: none
difficulty: easy
title: "Dizgideki büyük harfleri yerinde küçük harfe dönüştürme"
prompt: |
  Null ile sonlandırılmış bir dizgideki tüm büyük İngilizce harfleri ('A'-'Z') yerinde küçük harfe dönüştüren `void to_lowercase_inplace(char *str)` fonksiyonunu yazın. n dizgi uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "İngilizce dışındaki karakterler değişmemeli"
expected:
  time: { to_lowercase_inplace: "n" }
  space: "1"
concept_tags: [strings, pointer-arithmetic]
checklist_extra:
  - "ASCII aralık kontrolü 'A' <= c && c <= 'Z' ile yapılmış mı?"
  - "Fark ('a' - 'A') eklenerek doğru dönüşüm sağlanmış mı?"
reference_solution_path: private/solutions/c-easy-string-to-lower.c
hint_ladder:
  1: "Karakter 'A' ile 'Z' arasında ise 'a' - 'A' farkını ekleyerek küçük harf karşılığını elde edin."
  2: "İşaretçi aritmetiği kullanarak metin üzerinde yerinde güncelleme yapın."
  3: "Bu işlem 'büyük harfleri küçültme (lowercase conversion)' olarak bilinir."
```

---
### c-easy-string-to-upper

```yaml
id: c-easy-string-to-upper
version: 1
language: c
engine: none
difficulty: easy
title: "Dizgideki küçük harfleri yerinde büyük harfe dönüştürme"
prompt: |
  Null ile sonlandırılmış bir dizgideki tüm küçük İngilizce harfleri ('a'-'z') yerinde büyük harfe dönüştüren `void to_uppercase_inplace(char *str)` fonksiyonunu yazın. n dizgi uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "Harf olmayan karakterler değişmemeli"
expected:
  time: { to_uppercase_inplace: "n" }
  space: "1"
concept_tags: [strings, pointers]
checklist_extra:
  - "ASCII sınırları 'a' <= c && c <= 'z' doğru kontrol edilmiş mi?"
  - "NULL işaretçi kontrolü yapılmış mı?"
reference_solution_path: private/solutions/c-easy-string-to-upper.c
hint_ladder:
  1: "Karakter 'a' ile 'z' arasında ise 'a' - 'A' farkını çıkararak büyük harf karşılığını elde edin."
  2: "Null terminatöre kadar ilerleyerek her küçük harfi yerinde güncelleyin."
  3: "Bu işlem 'küçük harfleri büyütme (uppercase conversion)' olarak bilinir."
```

---
### c-easy-prefix-match

```yaml
id: c-easy-prefix-match
version: 1
language: c
engine: none
difficulty: easy
title: "Dizginin verilen önek ile başlayıp başlamadığını denetleme"
prompt: |
  str dizgisinin prefix dizgisiyle başlayıp başlamadığını denetleyen `bool starts_with(const char *str, const char *prefix)` fonksiyonunu yazın. m önek uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(m) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Boş önek her dizginin başında kabul edilir ve true döner"
expected:
  time: { starts_with: "m" }
  space: "1"
concept_tags: [strings, edge-cases]
checklist_extra:
  - "Önek dizgiden daha uzun olduğunda bellek dışına çıkış engellenmiş mi?"
  - "NULL parametreler güvenle yönetilmiş mi?"
reference_solution_path: private/solutions/c-easy-prefix-match.c
hint_ladder:
  1: "Prefix bitene kadar her iki dizgideki karakterleri eşzamanlı karşılaştırın."
  2: "Eşleşmeyen bir karakterle karşılaşırsanız veya str daha önce biterse false dönün."
  3: "Bu algoritma 'önek eşleştirme (prefix matching)' olarak bilinir."
```

---
### c-easy-suffix-match

```yaml
id: c-easy-suffix-match
version: 1
language: c
engine: none
difficulty: easy
title: "Dizginin verilen sonek ile bittiğini denetleme"
prompt: |
  str dizgisinin suffix dizgisi ile bitip bitmediğini denetleyen `bool ends_with(const char *str, const char *suffix)` fonksiyonunu yazın. n metin uzunluğu ve m sonek uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(m) olmalı"
  - "Ek bellek O(1) olmalı"
  - "m > n durumunda false dönmeli"
expected:
  time: { ends_with: "m" }
  space: "1"
concept_tags: [strings, pointers]
checklist_extra:
  - "n ve m uzunlukları doğru kıyaslanmış mı?"
  - "str sonundan m kadar geriye gidilip karakter karşılaştırması yapılmış mı?"
reference_solution_path: private/solutions/c-easy-suffix-match.c
hint_ladder:
  1: "Her iki dizginin uzunluğunu bulun. Sonek daha uzunsa doğrudan false dönün."
  2: "str'nin son m karakteri ile suffix'i baştan sona karşılaştırın."
  3: "Bu kontrol 'sonek eşleştirme (suffix matching)' olarak bilinir."
```

---
### c-easy-split-lines-count

```yaml
id: c-easy-split-lines-count
version: 1
language: c
engine: none
difficulty: easy
title: "Metin içindeki satır sayısını sayma"
prompt: |
  Verilen bir metinde yer alan satır sayısını yeni satır ('\n') karakterlerine göre hesaplayan `size_t count_lines(const char *text)` fonksiyonunu yazın. Boş metin 0 satır kabul edilir. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Boş dizgi için 0 satır dönmeli"
expected:
  time: { count_lines: "n" }
  space: "1"
concept_tags: [strings, edge-cases]
checklist_extra:
  - "Son satırın '\n' ile bitmediği durumlar doğru sayılmış mı?"
  - "Boş metin kontrolü yapılmış mı?"
reference_solution_path: private/solutions/c-easy-split-lines-count.c
hint_ladder:
  1: "Metin boş değilse satır sayısı en az 1 ile başlar."
  2: "Her '\n' karakteri gördükçe satır sayısını artırın; son karakter '\n' ise fazladan satır saymamaya dikkat edin."
  3: "Bu algoritma 'satır sayısı hesaplama (line counting)' olarak bilinir."
```

---
### c-easy-matrix-trace

```yaml
id: c-easy-matrix-trace
version: 1
language: c
engine: none
difficulty: easy
title: "Kare matrisin asal köşegen toplamını bulma"
prompt: |
  n x n boyutundaki bir tamsayı kare matrisin asal köşegenindeki (i == j) elemanların toplamını hesaplayan `long long matrix_trace(size_t n, const int *matrix)` fonksiyonunu yazın. n matrisin satır ve sütun boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "İki boyutlu indeksleme matrix[i * n + i] ile yapılmalı"
expected:
  time: { matrix_trace: "n" }
  space: "1"
concept_tags: [arrays, pointer-arithmetic]
checklist_extra:
  - "Döngü n adımda tamamlanıyor mu (iç içe döngü kurulmamış mı)?"
  - "Tek boyutlu tampon erişiminde sınır aşımı engellenmiş mi?"
reference_solution_path: private/solutions/c-easy-matrix-trace.c
hint_ladder:
  1: "Köşegen elemanlarına tek bir döngüde i * n + i adresiyle doğrudan erişebilirsiniz."
  2: "İç içe iki döngü kurmak yerine tek döngü kurarak O(n) karmaşıklığı sağlayın."
  3: "Bu matematiksel işlem 'matris izi hesaplama (matrix trace)' olarak bilinir."
```

---
### c-easy-dot-product

```yaml
id: c-easy-dot-product
version: 1
language: c
engine: none
difficulty: easy
title: "İki tamsayı vektörünün iç çarpımını hesaplama"
prompt: |
  n elemanlı iki tamsayı dizisinin nokta (iç) çarpımını hesaplayan `long long dot_product(const int *a, const int *b, size_t n)` fonksiyonunu yazın. Olası tamsayı taşmalarını önlemek için çarpım toplamı 64-bit tamsayıda biriktirilmelidir. n vektör uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Taşma önlenmeli"
expected:
  time: { dot_product: "n" }
  space: "1"
concept_tags: [arrays, integer-overflow]
checklist_extra:
  - "Her iki dizi için tek döngüde çarpım toplanmış mı?"
  - "Çarpım sonucu önce 64-bit türe dönüştürülüp mü toplanmış?"
reference_solution_path: private/solutions/c-easy-dot-product.c
hint_ladder:
  1: "Her adımda a[i] ve b[i] elemanlarını çarpıp biriktiriciye ekleyin."
  2: "Çarpım sırasında 32-bit tamsayı taşmasını önlemek için elemanları çarpmadan önce long long türüne yayın."
  3: "Bu vektör işlemi 'iç çarpım (dot product)' olarak bilinir."
```

---
### c-easy-find-median-sorted

```yaml
id: c-easy-find-median-sorted
version: 1
language: c
engine: none
difficulty: easy
title: "Sıralı dizinin medyanını bulma"
prompt: |
  Küçükten büyüğe sıralı n elemanlı bir tamsayı dizisinin medyan değerini hesaplayan `double median_sorted(const int *arr, size_t n)` fonksiyonunu yazın. Eleman sayısı tek ise ortadaki eleman, çift ise ortadaki iki elemanın aritmetik ortalaması dönmelidir. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "n == 0 durumunda 0.0 dönmelidir"
expected:
  time: { median_sorted: "1" }
  space: "1"
concept_tags: [arrays, edge-cases]
checklist_extra:
  - "Çift elemanlı dizilerde tamsayı bölmesi yerine kayan noktalı bölme yapılmış mı?"
  - "n == 0 sınır durumu kontrol edilmiş mi?"
reference_solution_path: private/solutions/c-easy-find-median-sorted.c
hint_ladder:
  1: "Dizi sıralı olduğu için ortadaki elemanlara doğrudan indeksle erişebilirsiniz."
  2: "n çift ise (arr[n/2 - 1] + arr[n/2]) / 2.0 hesabını yapın."
  3: "Bu istatistiksel hesap 'sıralı dizide medyan bulma (median of sorted array)' olarak bilinir."
```

---
### c-easy-filter-positives

```yaml
id: c-easy-filter-positives
version: 1
language: c
engine: none
difficulty: easy
title: "Dizideki pozitif sayıları dinamik diziye aktarma"
prompt: |
  n elemanlı bir tamsayı dizisindeki sıfırdan büyük pozitif sayıları dinamik olarak tahsis edilen yeni bir diziye kopyalayan `int *filter_positives(const int *arr, size_t n, size_t *out_size)` fonksiyonunu yazın. Pozitif eleman yoksa out_size 0 olmalı ve NULL dönmelidir. n eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(k) olmalı (k pozitif eleman sayısı)"
  - "Tahsis edilen bellek çağıran tarafından serbest bırakılacaktır"
expected:
  time: { filter_positives: "n" }
  space: "k"
concept_tags: [dynamic-memory, arrays]
checklist_extra:
  - "İlk geçişte pozitif sayısı sayılıp tam gereken boyutta malloc yapılmış mı?"
  - "malloc başarısızlığı durumunda NULL dönüşü kontrol edilmiş mi?"
reference_solution_path: private/solutions/c-easy-filter-positives.c
hint_ladder:
  1: "İlk turda dizide kaç pozitif sayı olduğunu sayın."
  2: "Gereken bellek bloğunu malloc ile ayırıp ikinci turda pozitif sayıları bu bloğa doldurun."
  3: "Bu işlem 'dinamik filtreleme (dynamic filtering)' olarak bilinir."
```

---
### c-easy-allocate-zero-matrix

```yaml
id: c-easy-allocate-zero-matrix
version: 1
language: c
engine: none
difficulty: easy
title: "Sıfırlanmış iki boyutlu matris tahsisi"
prompt: |
  n satır ve m sütundan oluşan iki boyutlu tamsayı matrisini satır işaretçileri dizisi olarak dinamik tahsis eden ve tüm hücreleri 0 yapan `int **allocate_zero_matrix(size_t n, size_t m)` fonksiyonunu yazın. Satır veya sütun sayısı 0 ise NULL dönmelidir. n satır ve m sütun sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(n * m) olmalı"
  - "Ara tahsis başarısız olursa önceden tahsis edilen satırlar serbest bırakılmalı"
expected:
  time: { allocate_zero_matrix: "n * m" }
  space: "n * m"
concept_tags: [dynamic-memory, memory-safety]
checklist_extra:
  - "Herhangi bir satırın tahsisi başarısız olduğunda bellek sızıntısı olmadan geri alma yapılmış mı?"
  - "Tüm elemanlar sıfır ile başlatılmış mı?"
reference_solution_path: private/solutions/c-easy-allocate-zero-matrix.c
hint_ladder:
  1: "Önce satır işaretçileri için n * sizeof(int*) boyutunda bir alan ayırın."
  2: "Her satır için m * sizeof(int) alan ayırın; herhangi biri başarısız olursa önceki satırları tek tek serbest bırakıp çıkın."
  3: "Bu tahsis yöntemi 'dinamik matris oluşturma (matrix allocation)' olarak bilinir."
```

---
### c-easy-free-matrix

```yaml
id: c-easy-free-matrix
version: 1
language: c
engine: none
difficulty: easy
title: "Dinamik iki boyutlu matrisi serbest bırakma"
prompt: |
  Daha önce allocate_zero_matrix benzeri bir yaklaşımla ayrılmış n satırlı iki boyutlu tamsayı matrisini ve satır işaretçilerini sızıntısız serbest bırakan `void free_matrix(int **matrix, size_t n)` fonksiyonunu yazın. n satır adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "matrix NULL ise işlem yapmamalıdır"
expected:
  time: { free_matrix: "n" }
  space: "1"
concept_tags: [dynamic-memory, pointers]
checklist_extra:
  - "Önce satırlar sonra ana işaretçi serbest bırakılmış mı?"
  - "use-after-free engellenmiş mi?"
reference_solution_path: private/solutions/c-easy-free-matrix.c
hint_ladder:
  1: "Önce 0'dan n-1'e kadar her matrix[i] işaretçisini serbest bırakın."
  2: "Tüm satırlar serbest kaldıktan sonra ana matrix işaretçisini free ile temizleyin."
  3: "Bu temizlik işlemi 'iki boyutlu bellek boşaltma (matrix deallocation)' olarak bilinir."
```

---
### c-easy-duplicate-string

```yaml
id: c-easy-duplicate-string
version: 1
language: c
engine: none
difficulty: easy
title: "Metni dinamik bellekte kopyalama"
prompt: |
  Verilen null ile sonlandırılmış karakter dizisinin aynısını dinamik bellekte yeni bir tampon açarak kopyalayan `char *custom_strdup(const char *src)` fonksiyonunu yazın. n metnin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "src NULL ise NULL dönmeli"
expected:
  time: { custom_strdup: "n" }
  space: "n"
concept_tags: [dynamic-memory, strings]
checklist_extra:
  - "Null terminatör için n + 1 bayt bellek tahsis edilmiş mi?"
  - "malloc başarısız olursa NULL dönülmüş mü?"
reference_solution_path: private/solutions/c-easy-duplicate-string.c
hint_ladder:
  1: "src uzunluğunu bulun ve sonundaki '\0' karakteri için fazladan 1 bayt ekleyerek malloc çağırın."
  2: "Karakterleri yeni belleğe kopyalayıp yeni işaretçiyi döndürün."
  3: "Bu işlem 'dizgi kopyalama (string duplication)' olarak bilinir."
```

---
### c-easy-parse-unsigned-int

```yaml
id: c-easy-parse-unsigned-int
version: 1
language: c
engine: none
difficulty: easy
title: "Metinden işaretsiz tamsayı çözümleme"
prompt: |
  Yalnızca rakamlardan oluşan bir dizgiyi işaretsiz tamsayıya (unsigned int) dönüştüren `bool parse_uint(const char *str, unsigned int *out_val)` fonksiyonunu yazın. Sayı taşarsa veya geçersiz karakter varsa false dönmelidir. n dizginin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Tamsayı taşması kontrol edilmeli"
expected:
  time: { parse_uint: "n" }
  space: "1"
concept_tags: [input-validation, integer-overflow]
checklist_extra:
  - "Çarpma ve toplama öncesinde UINT_MAX taşma kontrolü yapılmış mı?"
  - "Boş metin ve geçersiz karakterler doğru elenmiş mi?"
reference_solution_path: private/solutions/c-easy-parse-unsigned-int.c
hint_ladder:
  1: "Her rakam için mevcut toplamı 10 ile çarpıp yeni rakamı ekleyin."
  2: "10 ile çarpmadan önce (UINT_MAX - rakam) / 10 sınırını kontrol ederek taşmayı engelleyin."
  3: "Bu dönüşüm 'işaretsiz tamsayı ayrıştırma (unsigned integer parsing)' olarak bilinir."
```

---
### c-easy-count-words

```yaml
id: c-easy-count-words
version: 1
language: c
engine: none
difficulty: easy
title: "Boşluklarla ayrılmış sözcük sayısını bulma"
prompt: |
  Bir metinde boşluk (' ', '\t', '\n') karakterleriyle birbirinden ayrılmış sözcüklerin toplam adedini bulan `size_t count_words(const char *str)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Ardışık boşluklar tek ayraç sayılmalı"
expected:
  time: { count_words: "n" }
  space: "1"
concept_tags: [strings, state-machine]
checklist_extra:
  - "Sözcük içinde olup olmadığını belirten bir bayrak (in_word) kullanılmış mı?"
  - "Metin başındaki ve sonundaki boşluklar doğru elenmiş mi?"
reference_solution_path: private/solutions/c-easy-count-words.c
hint_ladder:
  1: "Metni tararken şu an bir sözcüğün içinde olup olmadığınızı tutan bir bayrak kullanın."
  2: "Boşluktan boşluk olmayan bir karaktere geçiş yaptığınız an sözcük sayacını bir artırın."
  3: "Bu iki durumlu çözüm 'basit durum makinesi ile sözcük sayımı (word counting state machine)' olarak bilinir."
```

---
### c-easy-check-anagram-basic

```yaml
id: c-easy-check-anagram-basic
version: 1
language: c
engine: none
difficulty: easy
title: "İki dizginin anagram olduğunu frekans dizisiyle denetleme"
prompt: |
  Yalnızca İngilizce küçük harflerden oluşan iki dizginin birbirinin anagramı (harflerin sırası değişse de aynı harf sayılarına sahip) olup olmadığını denetleyen `bool are_anagrams(const char *s1, const char *s2)` fonksiyonunu yazın. n birinci dizginin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (26 elemanlı frekans tablosu)"
  - "Uzunluklar farklıysa hemen false dönmeli"
expected:
  time: { are_anagrams: "n" }
  space: "1"
concept_tags: [strings, arrays]
checklist_extra:
  - "Frekans dizisi s1 için artırılıp s2 için azaltılmış mı?"
  - "Döngü sonunda tüm frekansların sıfır olduğu doğrulanmış mı?"
reference_solution_path: private/solutions/c-easy-check-anagram-basic.c
hint_ladder:
  1: "26 boyutlu bir tamsayı dizisi açıp ilk dizgideki harfler için artırın, ikinci dizgideki harfler için azaltın."
  2: "Dizi sonunda tüm değerler sıfır kalmışsa iki metin anagramdır."
  3: "Bu yöntem 'karakter frekans karşılaştırması (anagram check)' olarak bilinir."
```

---
### c-easy-array-diff-sum

```yaml
id: c-easy-array-diff-sum
version: 1
language: c
engine: none
difficulty: easy
title: "Ardışık elemanlar arasındaki mutlak farkların toplamı"
prompt: |
  n elemanlı bir tamsayı dizisinde komşu elemanlar arasındaki mutlak farkların (|arr[i] - arr[i-1]|) toplamını hesaplayan `long long sum_consecutive_diffs(const int *arr, size_t n)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "n < 2 durumunda 0 dönmeli"
expected:
  time: { sum_consecutive_diffs: "n" }
  space: "1"
concept_tags: [arrays, integer-overflow]
checklist_extra:
  - "İki eleman farkı alınırken mutlak değer doğru hesaplanmış mı?"
  - "Toplama sonucu 64-bit değişkende biriktirilmiş mi?"
reference_solution_path: private/solutions/c-easy-array-diff-sum.c
hint_ladder:
  1: "1. indeksten n-1. indekse kadar döngü kurun."
  2: "arr[i] ve arr[i-1] arasındaki mutlak farkı hesaplayıp toplama ekleyin."
  3: "Bu hesaplama 'ardışık eleman farkları toplamı (sum of consecutive differences)' olarak bilinir."
```

---
### c-easy-reverse-words-inplace

```yaml
id: c-easy-reverse-words-inplace
version: 1
language: c
engine: none
difficulty: easy
title: "Metindeki sözcükleri kendi içinde ters çevirme"
prompt: |
  Boşluklarla ayrılmış sözcükler içeren bir metinde, sözcüklerin cümledeki yerini değiştirmeden her bir sözcüğü kendi içinde yerinde tersine çeviren `void reverse_each_word(char *str)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "str NULL ise erken çıkış yapılmalı"
expected:
  time: { reverse_each_word: "n" }
  space: "1"
concept_tags: [strings, pointer-arithmetic]
checklist_extra:
  - "Her sözcüğün başlangıç ve bitiş indeksleri doğru bulunmuş mu?"
  - "Sözcük ters çevirme işlemi yerinde iki işaretçi ile yapılmış mı?"
reference_solution_path: private/solutions/c-easy-reverse-words-inplace.c
hint_ladder:
  1: "Metni tarayarak her sözcüğün başlangıç ve bitiş noktalarını belirleyin."
  2: "Belirlediğiniz her alt aralıkta iki işaretçi kullanarak sözcüğü yerinde ters çevirin."
  3: "Bu algoritma 'sözcükleri yerinde ters çevirme (reverse words in-place)' olarak bilinir."
```

---
### c-easy-find-missing-number

```yaml
id: c-easy-find-missing-number
version: 1
language: c
engine: none
difficulty: easy
title: "1 ile n+1 arasındaki eksik sayıyı bulma"
prompt: |
  1'den n+1'e kadar olan sayılardan tam olarak bir tanesinin eksik olduğu n elemanlı bir dizide eksik olan sayıyı matematiksel toplam veya XOR ile bulan `int find_missing_number(const int *arr, size_t n)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Tamsayı taşması XOR ile önlenebilir"
expected:
  time: { find_missing_number: "n" }
  space: "1"
concept_tags: [arrays, loop-invariant]
checklist_extra:
  - "XOR veya formül doğru kurulmuş mu?"
  - "Döngü 1'den n+1'e kadar tüm değerleri kapsıyor mu?"
reference_solution_path: private/solutions/c-easy-find-missing-number.c
hint_ladder:
  1: "1'den n+1'e kadar tüm sayıları ve dizideki tüm sayıları ardışık olarak XOR işlemine tabi tutun."
  2: "Çift gelen tüm sayılar birbirini sıfırlayacak, geriye yalnızca eksik sayı kalacaktır."
  3: "Bu yöntem 'XOR ile eksik sayı tespiti (missing number XOR)' olarak bilinir."
```

---
### c-easy-byte-swap-uint16

```yaml
id: c-easy-byte-swap-uint16
version: 1
language: c
engine: none
difficulty: easy
title: "16-bit tamsayının bayt sırasını ters çevirme"
prompt: |
  16-bit işaretsiz bir tamsayının (uint16_t) alt ve üst baytlarını bit kaydırma ve maskeleme işlemleriyle yer değiştiren `uint16_t swap_bytes_u16(uint16_t val)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Bit kaydırma ve VE işlemleriyle çözülmeli"
expected:
  time: { swap_bytes_u16: "1" }
  space: "1"
concept_tags: [input-validation, undefined-behavior]
checklist_extra:
  - "Alt bayt sola 8 bit kaydırılmış mı?"
  - "Üst bayt sağa 8 bit kaydırılıp VEYA ile birleştirilmiş mi?"
reference_solution_path: private/solutions/c-easy-byte-swap-uint16.c
hint_ladder:
  1: "(val << 8) ifadesi alt baytı üste taşır, (val >> 8) ise üst baytı alta indirir."
  2: "Bu iki parçayı bit düzeyinde VEYA (|) operatörü ile birleştirin."
  3: "Bu bayt düzenleme işlemi 'bayt takası (endianness byte swap)' olarak bilinir."
```

---
### c-easy-count-set-bits

```yaml
id: c-easy-count-set-bits
version: 1
language: c
engine: none
difficulty: easy
title: "32-bit tamsayıda 1 olan bit sayısını bulma"
prompt: |
  32-bit işaretsiz bir tamsayıda (uint32_t) ikilik tabanda 1 olan bitlerin (nüfus sayımı / popcount) adedini hesaplayan `int count_set_bits(uint32_t val)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı en fazla O(1) veya bit sayısı kadar olmalı"
  - "Ek bellek O(1) olmalı"
  - "Brian Kernighan algoritması val & (val - 1) kullanılabilir"
expected:
  time: { count_set_bits: "1" }
  space: "1"
concept_tags: [loop-invariant, performance]
checklist_extra:
  - "val sıfırlanana kadar döngü güvenle çalışıyor mu?"
  - "Kernighan hilesi val &= (val - 1) doğru uygulanmış mı?"
reference_solution_path: private/solutions/c-easy-count-set-bits.c
hint_ladder:
  1: "val & (val - 1) işlemi en sağdaki 1 bitini sıfırlar."
  2: "Sayı 0 olana kadar bu işlemi uygulayıp adımları sayın."
  3: "Bu yöntem 'Brian Kernighan bit sayma algoritması (popcount)' olarak bilinir."
```

---
### c-easy-check-power-of-two

```yaml
id: c-easy-check-power-of-two
version: 1
language: c
engine: none
difficulty: easy
title: "Sayının ikinin kuvveti olduğunu bit işlemiyle denetleme"
prompt: |
  İşaretsiz 32-bit tamsayının ikinin tam bir pozitif kuvveti (1, 2, 4, 8, ...) olup olmadığını bit işlemiyle denetleyen `bool is_power_of_two(uint32_t val)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "0 sayısı ikinin kuvveti değildir ve false dönmelidir"
expected:
  time: { is_power_of_two: "1" }
  space: "1"
concept_tags: [edge-cases, input-validation]
checklist_extra:
  - "val == 0 sınır durumu kontrol edilmiş mi?"
  - "val & (val - 1) sıfıra eşitlik sınaması yapılmış mı?"
reference_solution_path: private/solutions/c-easy-check-power-of-two.c
hint_ladder:
  1: "İkinin kuvveti olan sayıların ikilik temsilinde yalnızca tek bir bit 1'dir."
  2: "val > 0 iken (val & (val - 1)) == 0 ifadesi bu özelliği doğrudan doğrular."
  3: "Bu kontrol 'ikinin kuvveti bit sınaması (power of two bit test)' olarak bilinir."
```

---
### c-easy-singly-list-length

```yaml
id: c-easy-singly-list-length
version: 1
language: c
engine: none
difficulty: easy
title: "Tek yönlü bağlı listenin düğüm sayısını hesaplama"
prompt: |
  Tek yönlü bağlı listenin başlangıç düğümünü alarak listedeki toplam düğüm sayısını hesaplayan `size_t get_list_length(const Node *head)` fonksiyonunu yazın. n listedeki düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "head NULL ise 0 dönmeli"
expected:
  time: { get_list_length: "n" }
  space: "1"
concept_tags: [linked-list, pointers]
checklist_extra:
  - "İşaretçi NULL olana kadar döngü ilerletilmiş mi?"
  - "Döngüde düğüm atlama hatası yapılmamış mı?"
reference_solution_path: private/solutions/c-easy-singly-list-length.c
hint_ladder:
  1: "head işaretçisinden başlayarak curr = curr->next adımıyla listenin sonuna kadar yürüyün."
  2: "Her adımda sayaç değişkenini 1 artırın."
  3: "Bu temel işlem 'bağlı liste uzunluğu hesaplama (singly linked list traversal)' olarak bilinir."
```

---
### c-easy-singly-list-search

```yaml
id: c-easy-singly-list-search
version: 1
language: c
engine: none
difficulty: easy
title: "Tek yönlü bağlı listede değer arama"
prompt: |
  Tek yönlü bağlı listede verilen target tamsayısının bulunup bulunmadığını denetleyen `bool list_contains(const Node *head, int target)` fonksiyonunu yazın. n düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Hedef bulunduğunda döngü erken sonlanmalı"
expected:
  time: { list_contains: "n" }
  space: "1"
concept_tags: [linked-list, pointers]
checklist_extra:
  - "Hedef düğüm bulunduğunda hemen true dönülmüş mü?"
  - "Liste sonu (NULL) kontrolü yapılmış mı?"
reference_solution_path: private/solutions/c-easy-singly-list-search.c
hint_ladder:
  1: "curr işaretçisiyle düğümleri teker teker gezin."
  2: "curr->val == target olduğu anda true dönün; liste biterse false dönün."
  3: "Bu arama 'bağlı listede doğrusal arama (linked list search)' olarak bilinir."
```

---
### c-easy-singly-list-insert-head

```yaml
id: c-easy-singly-list-insert-head
version: 1
language: c
engine: none
difficulty: easy
title: "Bağlı listenin başına yeni düğüm ekleme"
prompt: |
  Mevcut bağlı listenin en başına value değerini taşıyan yeni bir düğüm ekleyen ve yeni liste başını döndüren `Node *insert_at_head(Node *head, int value)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "malloc başarısızlığında eski head dönmeli veya NULL güvenle yönetilmeli"
expected:
  time: { insert_at_head: "1" }
  space: "1"
concept_tags: [linked-list, dynamic-memory]
checklist_extra:
  - "Yeni düğümün next işaretçisi eski head'e bağlanmış mı?"
  - "malloc başarısızlığı kontrol edilmiş mi?"
reference_solution_path: private/solutions/c-easy-singly-list-insert-head.c
hint_ladder:
  1: "Yeni bir Node için malloc çağırıp bellek ayırın ve değerini atayın."
  2: "Yeni düğümün next alanına mevcut head işaretçisini bağlayıp yeni düğümü döndürün."
  3: "Bu ekleme 'bağlı liste başına ekleme (insert at head)' olarak bilinir."
```

---
### c-easy-singly-list-free

```yaml
id: c-easy-singly-list-free
version: 1
language: c
engine: none
difficulty: easy
title: "Bağlı listenin tüm düğümlerini serbest bırakma"
prompt: |
  Dinamik olarak tahsis edilmiş bir bağlı listenin tüm düğümlerini sızıntısız serbest bırakan `void free_entire_list(Node *head)` fonksiyonunu yazın. n listedeki düğüm adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "use-after-free kesinlikle önlenmeli"
expected:
  time: { free_entire_list: "n" }
  space: "1"
concept_tags: [linked-list, use-after-free]
checklist_extra:
  - "curr düğümü serbest bırakılmadan önce curr->next geçici değişkende saklanmış mı?"
  - "Serbest bırakılan bellek üzerinden okuma yapılmamış mı?"
reference_solution_path: private/solutions/c-easy-singly-list-free.c
hint_ladder:
  1: "Mevcut düğümü free yapmadan önce next işaretçisini geçici bir değişkende saklayın."
  2: "Düğümü serbest bıraktıktan sonra sakladığınız next adresine geçerek ilerleyin."
  3: "Bu temizlik işlemi 'bağlı liste düğümlerini serbest bırakma (free linked list)' olarak bilinir."
```

---
### c-easy-find-intersection-sorted

```yaml
id: c-easy-find-intersection-sorted
version: 1
language: c
engine: none
difficulty: easy
title: "İki sıralı dizinin kesişim elemanlarını yeni diziye aktarma"
prompt: |
  Küçükten büyüğe sıralı a (n elemanlı) ve b (m elemanlı) dizilerindeki ortak elemanları dinamik olarak tahsis edilen yeni bir sıralı diziye aktaran `int *sorted_intersection(const int *a, size_t n, const int *b, size_t m, size_t *out_len)` fonksiyonunu yazın. n ve m dizi boyutlarıdır.
constraints:
  - "Zaman karmaşıklığı O(n + m) olmalı"
  - "Ek bellek O(min(n, m)) olmalı"
  - "Ortak eleman yoksa out_len 0 olmalı ve NULL dönmeli"
expected:
  time: { sorted_intersection: "n + m" }
  space: "n + m"
concept_tags: [arrays, pointers]
checklist_extra:
  - "İki işaretçi karşılıklı ilerletilerek O(n + m) sağlanmış mı?"
  - "malloc ile ayrılan bellek boyutu doğru yönetilmiş mi?"
reference_solution_path: private/solutions/c-easy-find-intersection-sorted.c
hint_ladder:
  1: "İki diziyi iki ayrı indeksle baştan sona eşzamanlı tarayın."
  2: "Elemanlar eşitse kesişime ekleyip her iki indeksi artırın; küçük olan elemanın indeksini bir ilerletin."
  3: "Bu yöntem 'sıralı dizilerin iki işaretçiyle kesişimi (sorted arrays intersection)' olarak bilinir."
```

---
### c-easy-dynamic-array-append

```yaml
id: c-easy-dynamic-array-append
version: 1
language: c
engine: none
difficulty: easy
title: "Kapasite dolduğunda genişleyen dinamik diziye ekleme"
prompt: |
  Dinamik bir tamsayı dizisine eleman ekleyen, kapasite dolduğunda realloc ile kapasiteyi iki katına çıkaran `bool dyn_array_append(DynArray *da, int val)` fonksiyonunu yazın. İşlem başarısız olursa false dönmeli ve mevcut veriyi korumalıdır.
constraints:
  - "Amortize zaman karmaşıklığı O(1*) olmalı"
  - "Ek bellek O(1) olmalı"
  - "realloc sızıntısı önlenmeli"
expected:
  time: { dyn_array_append: "1*" }
  space: "1"
concept_tags: [dynamic-memory, realloc]
checklist_extra:
  - "realloc doğrudan da->data üzerine yazılmayıp geçici işaretçide tutulmuş mu?"
  - "Kapasite 2 katına çıkarılarak amortize O(1) sağlanmış mı?"
reference_solution_path: private/solutions/c-easy-dynamic-array-append.c
hint_ladder:
  1: "Boyut kapasiteye ulaştığında yeni kapasiteyi mevcut kapasitenin iki katı olarak belirleyin."
  2: "realloc sonucunu geçici bir işaretçiye alıp ancak NULL değilse asıl dizi işaretçisine atayın."
  3: "Bu büyüme mekanizması 'amortize dinamik dizi büyümesi (dynamic array geometric resizing)' olarak bilinir."
```

---
### c-easy-matrix-transpose

```yaml
id: c-easy-matrix-transpose
version: 1
language: c
engine: none
difficulty: easy
title: "Kare matrisin devriğini yerinde alma"
prompt: |
  n x n boyutundaki bir kare matrisin devriğini (transpozunu) ek bir matris tahsis etmeden yerinde alan `void transpose_square_matrix(size_t n, int *matrix)` fonksiyonunu yazın. n matris satır ve sütun boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n^2) olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "matrix[i * n + j] ve matrix[j * n + i] takas edilmeli"
expected:
  time: { transpose_square_matrix: "n^2" }
  space: "1"
concept_tags: [arrays, pointer-arithmetic]
checklist_extra:
  - "İç döngü j = i + 1'den başlayarak elemanların iki kez takas edilip eski haline dönmesi önlenmiş mi?"
  - "Tek boyutlu matris indekslemesi doğru yapılmış mı?"
reference_solution_path: private/solutions/c-easy-matrix-transpose.c
hint_ladder:
  1: "Asal köşegenin üzerindeki elemanlar için (j > i) matrix[i * n + j] ile matrix[j * n + i] değerlerini takas edin."
  2: "Döngü sınırını j = i + 1 yaparak elemanların iki defa takas edilmesini önleyin."
  3: "Bu matris işlemi 'kare matris devriği alma (in-place matrix transpose)' olarak bilinir."
```

---
### c-easy-check-palindrome-chars

```yaml
id: c-easy-check-palindrome-chars
version: 1
language: c
engine: none
difficulty: easy
title: "Karakter dizisinde palindrom denetimi"
prompt: |
  Verilen bir dizginin baştan ve sondan okunuşlarının aynı olup olmadığını yerinde iki işaretçi ile denetleyen `bool is_alphanumeric_palindrome(const char *str)` fonksiyonunu yazın. Büyük/küçük harf ayrımı yapılmamalıdır. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "str NULL ise true dönmeli"
expected:
  time: { is_alphanumeric_palindrome: "n" }
  space: "1"
concept_tags: [strings, pointers]
checklist_extra:
  - "Biri başta diğeri sonda iki işaretçi merkeze doğru ilerletilmiş mi?"
  - "Büyük/küçük harf eşleşmesi tolower mantığıyla yapılmış mı?"
reference_solution_path: private/solutions/c-easy-check-palindrome-chars.c
hint_ladder:
  1: "Sol işaretçiyi baştan, sağ işaretçiyi sondan başlatın."
  2: "Karakterlerin küçük harf karşılıkları eşleştiği sürece işaretçileri birbirine yaklaştırın."
  3: "Bu algoritma 'çift işaretçi ile palindrom kontrolü (two-pointer palindrome check)' olarak bilinir."
```

---
### c-easy-caesar-cipher

```yaml
id: c-easy-caesar-cipher
version: 1
language: c
engine: none
difficulty: easy
title: "Metindeki harfleri sabit kaydırmayla şifreleme"
prompt: |
  Null ile sonlandırılmış bir dizgideki İngilizce harfleri shift miktarı kadar ileri kaydırarak şifreleyen `void caesar_encrypt(char *str, int shift)` fonksiyonunu yazın. Harf dışı karakterler değişmemeli, alfabe sonunda sarma (wrap-around) yapılmalıdır. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Negatif shift değerleri doğru modül ile yönetilmeli"
expected:
  time: { caesar_encrypt: "n" }
  space: "1"
concept_tags: [strings, integer-overflow]
checklist_extra:
  - "Büyük ve küçük harf sınırları korunmuş mu?"
  - "(shift % 26 + 26) % 26 ile negatif kaydırma normalize edilmiş mi?"
reference_solution_path: private/solutions/c-easy-caesar-cipher.c
hint_ladder:
  1: "shift değerini 26 tabanında mod alarak 0-25 aralığına indirgeyin."
  2: "Her harfin alfabedeki sırasına shift ekleyip 26 modülünü alarak yeni harfe dönüştürün."
  3: "Bu klasik yöntem 'Sezar şifrelemesi (Caesar cipher)' olarak bilinir."
```

---
### c-easy-merge-sorted-arrays

```yaml
id: c-easy-merge-sorted-arrays
version: 1
language: c
engine: none
difficulty: easy
title: "İki sıralı diziyi tek bir sıralı dizi halinde birleştirme"
prompt: |
  Küçükten büyüğe sıralı a (n elemanlı) ve b (m elemanlı) dizilerini birleştirerek n + m elemanlı yeni bir dinamik sıralı dizi oluşturan `int *merge_sorted_arrays(const int *a, size_t n, const int *b, size_t m)` fonksiyonunu yazın. n ve m dizi boyutlarıdır.
constraints:
  - "Zaman karmaşıklığı O(n + m) olmalı"
  - "Ek bellek O(n + m) olmalı"
  - "Tahsis edilen bellek çağıran tarafından free edilecektir"
expected:
  time: { merge_sorted_arrays: "n + m" }
  space: "n + m"
concept_tags: [arrays, dynamic-memory]
checklist_extra:
  - "malloc başarısızlığı kontrol edilmiş mi?"
  - "Dizilerden biri bittiğinde diğerinin kalan kısmı doğru aktarılmış mı?"
reference_solution_path: private/solutions/c-easy-merge-sorted-arrays.c
hint_ladder:
  1: "İki diziyi iki işaretçi ile eşzamanlı tarayıp küçük olan elemanı yeni diziye yazın."
  2: "Dizilerden biri bittiğinde diğer dizinin kalan elemanlarını doğrudan hedefe kopyalayın."
  3: "Bu algoritma 'sıralı dizileri birleştirme adımı (merge step of mergesort)' olarak bilinir."
```

---
### c-easy-stack-array-init

```yaml
id: c-easy-stack-array-init
version: 1
language: c
engine: none
difficulty: easy
title: "Sabit boyutlu dizi tabanlı yığına eleman ekleme"
prompt: |
  Sabit kapasiteli bir tamsayı yığın yapısına yeni eleman ekleyen `bool stack_push(ArrayStack *stack, int val)` fonksiyonunu yazın. Yığın doluysa false dönmeli, aksi halde elemanı ekleyip true dönmelidir.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Taşma (overflow) durumu kontrol edilmeli"
expected:
  time: { stack_push: "1" }
  space: "1"
concept_tags: [arrays, input-validation]
checklist_extra:
  - "stack->top == stack->capacity sınır kontrolü yapılmış mı?"
  - "top indeksi güvenle artırılmış mı?"
reference_solution_path: private/solutions/c-easy-stack-array-init.c
hint_ladder:
  1: "Yığının mevcut eleman sayısının kapasiteye eşit olup olmadığını denetleyin."
  2: "Kapasite aşılmadıysa top indeksine yeni değeri yazıp top değerini 1 artırın."
  3: "Bu temel veri yapısı işlemi 'yığına eleman itme (stack push)' olarak bilinir."
```

---
### c-medium-reverse-linked-list

```yaml
id: c-medium-reverse-linked-list
version: 1
language: c
engine: none
difficulty: medium
title: "Tek yönlü bağlı listeyi yerinde tersine çevirme"
prompt: |
  Tek yönlü bir bağlı listenin tüm düğüm işaretçilerini yerinde tersine çevirerek yeni liste başını döndüren `Node *reverse_linked_list(Node *head)` fonksiyonunu yazın. n listedeki düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "Liste boş veya tek düğümlüyse güvenle dönmeli"
expected:
  time: { reverse_linked_list: "n" }
  space: "1"
concept_tags: [linked-list, pointers]
checklist_extra:
  - "prev, curr ve next işaretçileri doğru sırada güncellenmiş mi?"
  - "Döngü sonunda yeni head olarak prev döndürülmüş mü?"
reference_solution_path: private/solutions/c-medium-reverse-linked-list.c
hint_ladder:
  1: "Her adımda mevcut düğümün next işaretçisini bir önceki düğüme bağlamak için üç işaretçi takip edebilirsiniz."
  2: "curr işaretçisi ilerletilmeden önce bir sonraki düğümün adresi geçici bir değişkende saklanmalıdır."
  3: "Bu algoritma 'bağlı listeyi yerinde tersine çevirme (in-place linked list reversal)' olarak bilinir."
```

---
### c-medium-detect-cycle-floyd

```yaml
id: c-medium-detect-cycle-floyd
version: 1
language: c
engine: none
difficulty: medium
title: "Bağlı listede döngü varlığını tespit etme"
prompt: |
  Tek yönlü bir bağlı listede herhangi bir döngü (cycle) olup olmadığını ek düğüm tablosu tutmadan iki işaretçiyle denetleyen `bool detect_cycle(const Node *head)` fonksiyonunu yazın. n düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "head NULL ise false dönmeli"
expected:
  time: { detect_cycle: "n" }
  space: "1"
concept_tags: [linked-list, loop-invariant]
checklist_extra:
  - "Hızlı işaretçinin iki adım atarken NULL aşımı kontrol edilmiş mi?"
  - "Döngü tespit edildiğinde erken çıkış yapılmış mı?"
reference_solution_path: private/solutions/c-medium-detect-cycle-floyd.c
hint_ladder:
  1: "Biri adım adım (yavaş), diğeri ikişer adım (hızlı) ilerleyen iki işaretçi tanımlayın."
  2: "Eğer listede döngü varsa hızlı işaretçi tur atarak arkadan yavaş işaretçiye yetişecektir."
  3: "Bu teknik 'Floyd döngü bulma algoritması (Floyd cycle detection)' olarak bilinir."
```

---
### c-medium-find-middle-node

```yaml
id: c-medium-find-middle-node
version: 1
language: c
engine: none
difficulty: medium
title: "Bağlı listenin orta düğümünü iki işaretçiyle bulma"
prompt: |
  Tek yönlü bir bağlı listenin ortasındaki düğümü liste uzunluğunu önceden saymadan tek geçişte bulan `const Node *find_middle_node(const Node *head)` fonksiyonunu yazın. Çift sayıda düğüm varsa ikinci orta düğümü dönmelidir. n düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) tek geçiş olmalı"
  - "Ek bellek O(1) olmalı"
  - "head NULL ise NULL dönmeli"
expected:
  time: { find_middle_node: "n" }
  space: "1"
concept_tags: [linked-list, pointers]
checklist_extra:
  - "Hızlı işaretçi sonlandığında yavaş işaretçinin tam ortada olduğu doğrulanmış mı?"
  - "NULL işaretçi hatası engellenmiş mi?"
reference_solution_path: private/solutions/c-medium-find-middle-node.c
hint_ladder:
  1: "Yavaş işaretçi birer adım, hızlı işaretçi ikişer adım ilerlesin."
  2: "Hızlı işaretçi listenin sonuna veya son düğümüne vardığında yavaş işaretçi listenin tam ortasında olacaktır."
  3: "Bu yöntem 'orta düğümü tek geçişte bulma (tortoise and hare middle node)' olarak bilinir."
```

---
### c-medium-merge-two-sorted-lists

```yaml
id: c-medium-merge-two-sorted-lists
version: 1
language: c
engine: none
difficulty: medium
title: "İki sıralı bağlı listeyi düğüm kopyalamadan birleştirme"
prompt: |
  Küçükten büyüğe sıralı iki bağlı listeyi (l1 ve l2) yeni düğüm tahsis etmeden yalnızca var olan düğüm işaretçilerini yeniden bağlayarak tek bir sıralı liste halinde birleştiren `Node *merge_sorted_lists(Node *l1, Node *l2)` fonksiyonunu yazın. n birinci ve m ikinci listenin düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n + m) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "Yeni bellek tahsisi (malloc) yapılmamalıdır"
expected:
  time: { merge_sorted_lists: "n + m" }
  space: "1"
concept_tags: [linked-list, pointers]
checklist_extra:
  - "Yalancı (dummy) baş düğüm kullanılarak kenar durum kodları sadeleştirilmiş mi?"
  - "Döngü sonrası kalan liste parçası tek hamlede bağlanmış mı?"
reference_solution_path: private/solutions/c-medium-merge-two-sorted-lists.c
hint_ladder:
  1: "Bir yalancı (dummy) baş düğüm oluşturup kuyruk işaretçisini küçük değere sahip düğüme bağlayın."
  2: "Listelerden biri tükendiğinde diğer listenin kalan kısmını doğrudan kuyruğa ekleyin."
  3: "Bu algoritma 'bağlı listeleri yerinde birleştirme (in-place list merge)' olarak bilinir."
```

---
### c-medium-remove-nth-from-end

```yaml
id: c-medium-remove-nth-from-end
version: 1
language: c
engine: none
difficulty: medium
title: "Bağlı listenin sonundan k'ıncı düğümü çıkarma"
prompt: |
  Tek yönlü bağlı listenin sondan k'ıncı düğümünü tek bir taramada silen ve serbest bırakan `Node *remove_nth_from_end(Node *head, size_t k)` fonksiyonunu yazın. k düğüm sayısından büyükse liste değişmemelidir. n düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) tek geçiş olmalı"
  - "Ek bellek O(1) olmalı"
  - "Silinen düğüm serbest bırakılmalıdır (free)"
expected:
  time: { remove_nth_from_end: "n" }
  space: "1"
concept_tags: [linked-list, memory-safety]
checklist_extra:
  - "İlk düğümün silinmesi durumunda head güncellenmiş mi?"
  - "Silinen düğüm free edilerek sızıntı önlenmiş mi?"
reference_solution_path: private/solutions/c-medium-remove-nth-from-end.c
hint_ladder:
  1: "İki işaretçi arasında k kadar aralık oluşturun."
  2: "İleri işaretçi liste sonuna vardığında gerideki işaretçi tam olarak silinecek düğümün bir öncesinde duracaktır."
  3: "Bu teknik 'aralıklı iki işaretçi ile sondan eleman silme (two-pointer offset deletion)' olarak bilinir."
```

---
### c-medium-binary-search-rotated

```yaml
id: c-medium-binary-search-rotated
version: 1
language: c
engine: none
difficulty: medium
title: "Döndürülmüş sıralı dizide hedef değeri arama"
prompt: |
  Bilinmeyen bir pivot noktasından döndürülmüş, elemanları benzersiz ve sıralı n elemanlı bir dizide hedef sayıyı ikili arama mantığıyla bulan `int search_rotated_array(const int *arr, size_t n, int target)` fonksiyonunu yazın. Bulunamazsa -1 dönmelidir. n eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Dizi boş ise -1 dönmelidir"
expected:
  time: { search_rotated_array: "log n" }
  space: "1"
concept_tags: [binary-search, arrays]
checklist_extra:
  - "Hangi yarı parçanın düzgün sıralı olduğu doğru tespit edilmiş mi?"
  - "Orta nokta hesabında tamsayı taşması engellenmiş mi?"
reference_solution_path: private/solutions/c-medium-binary-search-rotated.c
hint_ladder:
  1: "Her adımda ortadaki elemanı bulup sol ve sağ yarımlardan hangisinin kesintisiz sıralı olduğunu belirleyin."
  2: "Hedef değerin sıralı yarı aralıkta olup olmadığını test ederek arama aralığını yarıya indirin."
  3: "Bu algoritma 'döndürülmüş dizide ikili arama (rotated array binary search)' olarak bilinir."
```

---
### c-medium-kadane-max-subarray

```yaml
id: c-medium-kadane-max-subarray
version: 1
language: c
engine: none
difficulty: medium
title: "Bitişik alt dizi maksimum toplamını bulma"
prompt: |
  n elemanlı tamsayı dizisinde toplamı en büyük olan bitişik alt dizinin toplamını hesaplayan `long long max_subarray_sum(const int *arr, size_t n)` fonksiyonunu yazın. Dizi tümüyle negatif sayılardan oluşuyorsa en büyük negatif sayı dönmelidir. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) tek geçiş olmalı"
  - "Ek bellek O(1) olmalı"
  - "n == 0 durumunda 0 dönmelidir"
expected:
  time: { max_subarray_sum: "n" }
  space: "1"
concept_tags: [arrays, loop-invariant]
checklist_extra:
  - "Tümüyle negatif dizilerde sıfır dönme hatası önlenmiş mi?"
  - "Mevcut toplam negatife düştüğünde sıfırlanmış veya yeni elemandan başlatılmış mı?"
reference_solution_path: private/solutions/c-medium-kadane-max-subarray.c
hint_ladder:
  1: "Diziyi gezerken o ana kadarki bitişik toplamı tutun."
  2: "Mevcut toplam negatif olduğunda bir sonraki elemandan yeni bir alt dizi başlatmak daha kazançlıdır."
  3: "Bu dinamik programlama yaklaşımı 'Kadane algoritması (Kadane's algorithm)' olarak bilinir."
```

---
### c-medium-dutch-national-flag

```yaml
id: c-medium-dutch-national-flag
version: 1
language: c
engine: none
difficulty: medium
title: "Üç farklı değeri tek geçişte yerinde gruplama"
prompt: |
  Yalnızca 0, 1 ve 2 değerlerinden oluşan n elemanlı bir tamsayı dizisini tek geçişte küçükten büyüğe yerinde sıralayan `void sort_three_colors(int *arr, size_t n)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) tek geçiş olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "Sayma dizisi (counting sort) kullanılmadan üç işaretçiyle çözülmeli"
expected:
  time: { sort_three_colors: "n" }
  space: "1"
concept_tags: [arrays, pointer-arithmetic]
checklist_extra:
  - "low, mid ve high işaretçileri doğru aralıkları temsil ediyor mu?"
  - "2 ile takas yapıldığında mid işaretçisi sabit bırakılmış mı?"
reference_solution_path: private/solutions/c-medium-dutch-national-flag.c
hint_ladder:
  1: "Diziyi üçe ayırmak için low, mid ve high olmak üzere üç indeks tutun."
  2: "arr[mid] == 0 ise low ile takas edip her ikisini artırın, 2 ise high ile takas edip sadece high'ı azaltın."
  3: "Bu algoritma 'Hollanda Milli Bayrağı problemi (Dutch national flag algorithm)' olarak bilinir."
```

---
### c-medium-product-except-self

```yaml
id: c-medium-product-except-self
version: 1
language: c
engine: none
difficulty: medium
title: "Kendisi hariç diğer elemanların çarpımı dizisi"
prompt: |
  n elemanlı bir tamsayı dizisinde her elemanın yerine kendisi hariç diğer tüm elemanların çarpımını koyarak yeni dinamik bir dizi döndüren `long long *product_except_self(const int *arr, size_t n)` fonksiyonunu yazın. Bölme işlemi (/) kesinlikle kullanılmamalıdır. n eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) (sonuç dizisi) olmalı"
  - "Bölme operatörü kullanılmamalıdır"
expected:
  time: { product_except_self: "n" }
  space: "n"
concept_tags: [arrays, dynamic-memory]
checklist_extra:
  - "Sol ve sağ önek çarpımları tek bir geçişle birleştirilmiş mi?"
  - "Bölme işlemi kullanılmadan sıfır içeren elemanlar doğru yönetilmiş mi?"
reference_solution_path: private/solutions/c-medium-product-except-self.c
hint_ladder:
  1: "İlk geçişte her elemanın solundaki sayıların birikimli çarpımını sonuç dizisine yazın."
  2: "İkinci geçişte sağdan geriye gelerek sağdaki elemanların çarpımını bir değişkende tutup sonuçla çarpın."
  3: "Bu yöntem 'önek ve sonek çarpımları (prefix-suffix products)' olarak bilinir."
```

---
### c-medium-longest-common-prefix

```yaml
id: c-medium-longest-common-prefix
version: 1
language: c
engine: none
difficulty: medium
title: "Dizgiler kümesindeki en uzun ortak öneki bulma"
prompt: |
  count adet dizgi içeren bir dizideki tüm dizgilerin ortak olarak paylaştığı en uzun öneki dinamik bellekte yeni bir metin olarak döndüren `char *longest_common_prefix(const char **strs, size_t count)` fonksiyonunu yazın. Ortak önek yoksa boş metin dönmelidir. n toplam karakter sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) (sonuç hariç) olmalı"
  - "count == 0 için boş metin dönmeli"
expected:
  time: { longest_common_prefix: "n" }
  space: "1"
concept_tags: [strings, pointers]
checklist_extra:
  - "İlk dizginin karakterleri diğer dizgilerle sütun sütun karşılaştırılmış mı?"
  - "Herhangi bir dizgi bittiğinde veya uyuşmazlık çıktığında döngüden çıkılmış mı?"
reference_solution_path: private/solutions/c-medium-longest-common-prefix.c
hint_ladder:
  1: "İlk dizginin karakterlerini sırayla alın ve diğer tüm dizgilerin aynı indeksindeki karakterle kıyaslayın."
  2: "Herhangi bir dizgide farklı bir karakter gördüyseniz o ana kadarki kısmı kopyalayıp döndürün."
  3: "Bu yaklaşım 'düşey önek taraması (vertical scanning for common prefix)' olarak bilinir."
```

---
### c-medium-group-anagrams-hash

```yaml
id: c-medium-group-anagrams-hash
version: 1
language: c
engine: none
difficulty: medium
title: "Karakter sayılarına göre anagram dizgileri kümeleme"
prompt: |
  Yalnızca küçük harflerden oluşan n adet dizgiyi birbirinin anagramı olanlar aynı grupta yer alacak şekilde gruplayan `AnagramGroup *group_anagrams(const char **strs, size_t n, size_t *out_group_count)` fonksiyonunu yazın. m ortalama dizgi uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(n) olmalı"
  - "out_group_count işaretçisine toplam grup sayısı yazılmalı"
expected:
  time: { group_anagrams: "n*m" }
  space: "n"
concept_tags: [hashing, strings]
checklist_extra:
  - "Her dizginin 26 elemanlı karakter frekansı anahtar olarak kullanılmış mı?"
  - "Dinamik gruplar doğru tahsis edilip boyutlandırılmış mı?"
reference_solution_path: private/solutions/c-medium-group-anagrams-hash.c
hint_ladder:
  1: "Her dizginin harf sayılarını 26 elemanlı bir frekans dizisinde özetleyin."
  2: "Aynı frekans profiline sahip olan dizgileri aynı kova veya grupta toplayın."
  3: "Bu kümeleme yöntemi 'frekans tabanlı anagram gruplama (anagram grouping)' olarak bilinir."
```

---
### c-medium-two-sum-sorted

```yaml
id: c-medium-two-sum-sorted
version: 1
language: c
engine: none
difficulty: medium
title: "Sıralı dizide hedef toplama eşit iki indeksi bulma"
prompt: |
  Küçükten büyüğe sıralı n elemanlı bir tamsayı dizisinde toplamları target değerine eşit olan iki elemanın 0 tabanlı indekslerini bulan `bool two_sum_sorted(const int *arr, size_t n, int target, size_t *i1, size_t *i2)` fonksiyonunu yazın. Bulunursa true, yoksa false dönmelidir. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "Sıralılık avantajı kullanılmalı (çift işaretçi)"
expected:
  time: { two_sum_sorted: "n" }
  space: "1"
concept_tags: [arrays, pointers]
checklist_extra:
  - "Sol ve sağ işaretçilerin toplamı hedeften büyükse sağ işaretçi azaltılmış mı?"
  - "Hedef bulunduğunda indeksler doğru atanmış mı?"
reference_solution_path: private/solutions/c-medium-two-sum-sorted.c
hint_ladder:
  1: "Biri dizinin başında, diğeri sonunda iki işaretçi başlatın."
  2: "Toplam hedeften küçükse soldakini bir sağa kaydırın; hedeften büyükse sağdakini bir sola kaydırın."
  3: "Bu klasik yöntem 'çift işaretçi ile iki sayı toplamı (two-pointer two sum)' olarak bilinir."
```

---
### c-medium-three-sum-zero

```yaml
id: c-medium-three-sum-zero
version: 1
language: c
engine: none
difficulty: medium
title: "Toplamı sıfır olan benzersiz üçlüleri bulma"
prompt: |
  n elemanlı bir tamsayı dizisinde toplamları sıfır olan tüm benzersiz [a, b, c] üçlülerini dinamik iki boyutlu dizi olarak döndüren `int **three_sum_zero(int *arr, size_t n, size_t *out_count)` fonksiyonunu yazın. Yinelenen üçlüler sonuçta yer almamalıdır. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n^2) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Sonuç dizisi çağıran tarafından serbest bırakılacaktır"
expected:
  time: { three_sum_zero: "n^2" }
  space: "n"
concept_tags: [arrays, dynamic-memory]
checklist_extra:
  - "Dizi önce sıralanıp mükerrer üçlüler atlanmış mı?"
  - "out_count doğru güncellenmiş mi?"
reference_solution_path: private/solutions/c-medium-three-sum-zero.c
hint_ladder:
  1: "Diziyi küçükten büyüğe sıralayın ve ilk elemanı bir döngüde sabitleyin."
  2: "Kalan iki elemanı iki işaretçi tekniğiyle ararken ardışık aynı değerleri atlayın."
  3: "Bu algoritma 'sıralı üçlü toplamı (three sum problem)' olarak bilinir."
```

---
### c-medium-container-with-most-water

```yaml
id: c-medium-container-with-most-water
version: 1
language: c
engine: none
difficulty: medium
title: "İki çizgi arasında en fazla su tutan alanı hesaplama"
prompt: |
  n elemanlı bir yükseklik dizisinde herhangi iki çizgi ve x ekseni arasında hapsedilebilecek maksimum su alanını hesaplayan `long long max_water_area(const int *heights, size_t n)` fonksiyonunu yazın. Alan = min(h[i], h[j]) * (j - i) formülüyle bulunur. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "İki işaretçi karşılıklı ilerlemelidir"
expected:
  time: { max_water_area: "n" }
  space: "1"
concept_tags: [arrays, loop-invariant]
checklist_extra:
  - "Daha kısa olan sütunun işaretçisi içeriye doğru kaydırılmış mı?"
  - "Maksimum alan her adımda güncellenmiş mi?"
reference_solution_path: private/solutions/c-medium-container-with-most-water.c
hint_ladder:
  1: "En sol ve en sağdaki sütunlardan başlayarak alanı hesaplayın."
  2: "Alanı sınırlayan kısa sütun olduğundan daha kısa olan işaretçiyi içeri doğru bir adım ilerletin."
  3: "Bu açgözlü yöntem 'çift işaretçi ile azami su kabı (container with most water)' olarak bilinir."
```

---
### c-medium-trapping-rain-water-twopointer

```yaml
id: c-medium-trapping-rain-water-twopointer
version: 1
language: c
engine: none
difficulty: medium
title: "Yükseklik haritasında biriken yağmur suyu miktarını hesaplama"
prompt: |
  n elemanlı negatif olmayan yükseklik dizisinin temsil ettiği arazi profilinde birikebilecek toplam yağmur suyu hacmini hesaplayan `long long trap_rain_water(const int *heights, size_t n)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) tek geçiş olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "İki işaretçi ve sol/sağ tepe değerleri tutulmalı"
expected:
  time: { trap_rain_water: "n" }
  space: "1"
concept_tags: [arrays, pointer-arithmetic]
checklist_extra:
  - "Sol ve sağ tepe değerleri (left_max, right_max) doğru güncellenmiş mi?"
  - "Biriken su her adımda negatif olmayacak şekilde toplanmış mı?"
reference_solution_path: private/solutions/c-medium-trapping-rain-water-twopointer.c
hint_ladder:
  1: "İki uca yerleştirilen işaretçilerle birlikte o ana kadarki sol ve sağ maksimum yükseklikleri takip edin."
  2: "Daha düşük maksimuma sahip taraftaki işaretçiyi içeri kaydırıp aradaki fark kadar su biriktirin."
  3: "Bu algoritma 'çift işaretçi ile yağmur suyu tutma (trapping rain water two-pointer)' olarak bilinir."
```

---
### c-medium-valid-parentheses-stack

```yaml
id: c-medium-valid-parentheses-stack
version: 1
language: c
engine: none
difficulty: medium
title: "Dinamik yığın ile parantez dengesini doğrulama"
prompt: |
  Yalnızca '(', ')', '{', '}', '[' ve ']' karakterlerini içeren bir dizgide açılan her parantezin doğru türde ve doğru sırada kapatılıp kapatılmadığını yığın veri yapısıyla denetleyen `bool is_valid_parentheses(const char *expr)` fonksiyonunu yazın. n dizgi uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Bellek sızıntısı önlenmelidir"
expected:
  time: { is_valid_parentheses: "n" }
  space: "n"
concept_tags: [strings, dynamic-memory]
checklist_extra:
  - "Yığın için ayrılan bellek tüm çıkış noktalarında free edilmiş mi?"
  - "Boş yığından kapatma parantezi gelmesi durumu yakalanmış mı?"
reference_solution_path: private/solutions/c-medium-valid-parentheses-stack.c
hint_ladder:
  1: "Açma parantezi gördükçe karaktere karşılık gelen kapatma parantezini bir yığına atın."
  2: "Kapatma parantezi gördükçe yığının tepesindekiyle eşleşip eşleşmediğini kontrol edin; metin bittiğinde yığın boş kalmalıdır."
  3: "Bu algoritma 'yığın tabanlı parantez eşleştirme (valid parentheses stack)' olarak bilinir."
```

---
### c-medium-eval-reverse-polish

```yaml
id: c-medium-eval-reverse-polish
version: 1
language: c
engine: none
difficulty: medium
title: "Ters Polonyalı Notasyonu matematiksel ifadesini hesaplama"
prompt: |
  Ters Polonyalı Notasyonunda (RPN) verilmiş count adet simgeden oluşan matematiksel ifadeyi tamsayı yığını kullanarak hesaplayan `int eval_rpn(const char **tokens, size_t count)` fonksiyonunu yazın. Desteklenen operatörler +, -, *, / işlemleridir. n simge sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Sıfıra bölme ve yığın taşması kontrol edilmeli"
expected:
  time: { eval_rpn: "n" }
  space: "n"
concept_tags: [arrays, dynamic-memory]
checklist_extra:
  - "İkili operatörlerde işlenenlerin çıkarma ve bölmede sırası (ilk çekilen sağdaki işlenen) doğru gözetilmiş mi?"
  - "Yığın belleği çıkışta temizlenmiş mi?"
reference_solution_path: private/solutions/c-medium-eval-reverse-polish.c
hint_ladder:
  1: "Sayı gördükçe yığına itin."
  2: "Operatör gördükçe yığından iki sayı çekip işlemi uygulayın ve sonucu tekrar yığına itin."
  3: "Bu hesaplama mantığı 'Ters Polonyalı Notasyonu değerlendiricisi (reverse Polish notation evaluation)' olarak bilinir."
```

---
### c-medium-circular-queue

```yaml
id: c-medium-circular-queue
version: 1
language: c
engine: none
difficulty: medium
title: "Sabit tampon üzerinde dairesel kuyruk yapısı gerçekleştirme"
prompt: |
  Kapasitesi baştan belirlenmiş bir dairesel tampon üzerinde kuyruğa eleman ekleyen `bool circ_queue_enqueue(CircQueue *q, int val)` fonksiyonunu yazın. Kuyruk doluysa false dönmeli, boşluk varsa modül aritmetiğiyle yeni elemanı ekleyip true dönmelidir.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "rear indeksi (rear + 1) % capacity ile güncellenmeli"
expected:
  time: { circ_queue_enqueue: "1" }
  space: "1"
concept_tags: [arrays, edge-cases]
checklist_extra:
  - "Kuyruğun doluluk kontrolü count == capacity ile yapılmış mı?"
  - "rear işaretçisi tampon sonuna geldiğinde sıfıra sarıyor mu?"
reference_solution_path: private/solutions/c-medium-circular-queue.c
hint_ladder:
  1: "rear indeksine elemanı yerleştirin."
  2: "rear indeksini (rear + 1) % capacity formülüyle güncelleyip eleman sayacını 1 artırın."
  3: "Bu veri yapısı mekanizması 'dairesel kuyruk ekleme işlemi (circular queue enqueue)' olarak bilinir."
```

---
### c-medium-generic-vector

```yaml
id: c-medium-generic-vector
version: 1
language: c
engine: none
difficulty: medium
title: "Genel amaçlı işaretçi dinamik dizisi gerçekleştirme"
prompt: |
  Her türden veri işaretçisini (void*) saklayabilen dinamik bir vektöre eleman ekleyen ve kapasite yetmediğinde kapasiteyi iki katına çıkaran `bool gvec_push(GenericVector *vec, void *item)` fonksiyonunu yazın.
constraints:
  - "Amortize zaman karmaşıklığı O(1*) olmalı"
  - "Ek bellek O(1) olmalı"
  - "realloc sızıntısı önlenmeli"
expected:
  time: { gvec_push: "1*" }
  space: "1"
concept_tags: [dynamic-memory, amortized-analysis]
checklist_extra:
  - "realloc çağrısı geçici bir void** işaretçisine yapılmış mı?"
  - "Kapasite 2 katına çıkarılarak amortize O(1) sağlanmış mı?"
reference_solution_path: private/solutions/c-medium-generic-vector.c
hint_ladder:
  1: "Mevcut boyut kapasiteye ulaştığında yeni kapasiteyi ikiye katlayın."
  2: "realloc ile işaretçi dizisini genişletip yeni öğeyi dizinin sonuna ekleyin."
  3: "Bu yapı 'genel amaçlı dinamik işaretçi vektörü (generic dynamic vector)' olarak bilinir."
```

---
### c-medium-string-token-generator

```yaml
id: c-medium-string-token-generator
version: 1
language: c
engine: none
difficulty: medium
title: "Yeniden giriş yapılabilir dizgi bölücü tasarlama"
prompt: |
  Verilen bir metni ayraç karakterlerine göre parçalara bölen ve iç durumunu çağıranın sağladığı işaretçide saklayan `char *custom_strtok_r(char *str, const char *delim, char **saveptr)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "saveptr geçerli adresi saklamalı"
expected:
  time: { custom_strtok_r: "n" }
  space: "1"
concept_tags: [strings, pointers]
checklist_extra:
  - "str NULL olduğunda taramaya *saveptr adresinden devam edilmiş mi?"
  - "Bulunan ayracın yerine null karakteri yazılıp bir sonraki konum saklanmış mı?"
reference_solution_path: private/solutions/c-medium-string-token-generator.c
hint_ladder:
  1: "str NULL ise taramaya *saveptr adresinden devam edin."
  2: "İlk ayraç olmayan karakteri token başı yapın; bir sonraki ayracı bulduğunuzda '\0' ile kesip sonrasını *saveptr'ye kaydedin."
  3: "Bu güvenli metin bölücü 'yeniden giriş yapılabilir dizgi parçalayıcı (reentrant string tokenizer)' olarak bilinir."
```

---
### c-medium-safe-custom-printf-subset

```yaml
id: c-medium-safe-custom-printf-subset
version: 1
language: c
engine: none
difficulty: medium
title: "Temel biçimlendiricileri destekleyen metin tamponlayıcı"
prompt: |
  Format dizgisindeki %d, %s ve %c belirteçlerini değişken argüman listesi (va_list) kullanarak güvenle tampona yazan `int safe_format_string(char *buffer, size_t size, const char *format, ...)` fonksiyonunu yazın. n format metninin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Tampon boyutu asla aşılmamalı ve sonu null olmalı"
expected:
  time: { safe_format_string: "n" }
  space: "1"
concept_tags: [strings, memory-safety]
checklist_extra:
  - "va_start ve va_end doğru çağrılmış mı?"
  - "Tampon sınırına ulaşıldığında yazma durdurulup taşma önlenmiş mi?"
reference_solution_path: private/solutions/c-medium-safe-custom-printf-subset.c
hint_ladder:
  1: "Format metnini karakter karakter tarayıp '%' gördüğünüzde bir sonraki tipe göre va_arg çağırın."
  2: "Hedef tamponda kalan yer miktarını takip ederek tampon sonunu daima '\0' ile güvenceye alın."
  3: "Bu biçimlendirme yöntemi 'güvenli biçimli metin tamponlayıcı (bounded custom string formatter)' olarak bilinir."
```

---
### c-medium-matrix-spiral-order

```yaml
id: c-medium-matrix-spiral-order
version: 1
language: c
engine: none
difficulty: medium
title: "Matris elemanlarını spiral sırada tek boyutlu diziye aktarma"
prompt: |
  n satır ve m sütun boyutundaki iki boyutlu bir tamsayı matrisinin elemanlarını dıştan içe doğru saat yönünde spiral sırada okuyarak dinamik bir diziye aktaran `int *spiral_order_matrix(const int *matrix, size_t n, size_t m)` fonksiyonunu yazın. n ve m matris boyutlarıdır.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(n * m) olmalı"
  - "Dört sınır (top, bottom, left, right) doğru daraltılmalı"
expected:
  time: { spiral_order_matrix: "n * m" }
  space: "n * m"
concept_tags: [arrays, dynamic-memory]
checklist_extra:
  - "Sınırlar birbiriyle çakıştığında fazladan satır/sütun okunması engellenmiş mi?"
  - "Dinamik dizi tam n * m boyutunda açılmış mı?"
reference_solution_path: private/solutions/c-medium-matrix-spiral-order.c
hint_ladder:
  1: "Dört kenar için top, bottom, left ve right sınır indeksleri tutun."
  2: "Sırasıyla sağa, aşağıya, sola ve yukarıya hareket ederek sınırları birer adım içeri daraltın."
  3: "Bu gezinti 'matriste spiral sıra okuması (spiral matrix traversal)' olarak bilinir."
```

---
### c-medium-matrix-rotate-90

```yaml
id: c-medium-matrix-rotate-90
version: 1
language: c
engine: none
difficulty: medium
title: "Kare matrisi ek bellek ayırmadan saat yönünde döndürme"
prompt: |
  n x n boyutundaki kare tamsayı matrisini fazladan bir matris oluşturmadan yerinde saat yönünde 90 derece döndüren `void rotate_matrix_90(size_t n, int *matrix)` fonksiyonunu yazın. n matris satır ve sütun boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n^2) olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "Önce devrik alma ardından satırları ters çevirme yöntemi uygulanabilir"
expected:
  time: { rotate_matrix_90: "n^2" }
  space: "1"
concept_tags: [arrays, pointer-arithmetic]
checklist_extra:
  - "Devrik alma işleminde elemanlar iki kez takas edilmemiş mi?"
  - "Her satır kendi içinde iki işaretçiyle ters çevrilmiş mi?"
reference_solution_path: private/solutions/c-medium-matrix-rotate-90.c
hint_ladder:
  1: "Önce matrisin asal köşegene göre devriğini (transpozunu) alın."
  2: "Ardından her bir satırı yatay eksende baştan sona ters çevirin."
  3: "Bu iki adımlı dönüşüm 'matrisi yerinde 90 derece döndürme (in-place matrix rotation)' olarak bilinir."
```

---
### c-medium-set-matrix-zeroes

```yaml
id: c-medium-set-matrix-zeroes
version: 1
language: c
engine: none
difficulty: medium
title: "Sıfır içeren satır ve sütunları sabit ek bellekle sıfırlama"
prompt: |
  n satır ve m sütun boyutundaki bir tamsayı matrisinde herhangi bir eleman 0 ise, o elemanın bulunduğu satır ve sütundaki tüm elemanları yerinde sıfırlayan `void set_matrix_zeroes(int *matrix, size_t n, size_t m)` fonksiyonunu yazın. Ek bellek kullanımı O(1) olmalıdır. n satır ve m sütun adedidir.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "İlk satır ve sütun işaretçi olarak kullanılabilir"
expected:
  time: { set_matrix_zeroes: "n * m" }
  space: "1"
concept_tags: [arrays, edge-cases]
checklist_extra:
  - "İlk satır ve ilk sütunun başlangıçta sıfır içerip içermediği ayrı bayraklarla saklanmış mı?"
  - "Sıfırlama işlemi içeriden dışarıya doğru mu yapılmış?"
reference_solution_path: private/solutions/c-medium-set-matrix-zeroes.c
hint_ladder:
  1: "İlk satır ve ilk sütunu sıfır işaretleme tablosu olarak kullanın."
  2: "İlk satır ve sütunun kendi sıfır durumunu iki ayrı boole değişkeninde tutarak matrisi güncelleyin."
  3: "Bu alan optimizasyonu 'matrisi yerinde sıfırlama (in-place set matrix zeroes)' olarak bilinir."
```

---
### c-medium-quicksort-partition

```yaml
id: c-medium-quicksort-partition
version: 1
language: c
engine: none
difficulty: medium
title: "Hızlı sıralama için dizi bölme adımı gerçekleştirme"
prompt: |
  n elemanlı tamsayı dizisinin [low, high] aralığını son elemanı pivot seçerek Lomuto bölme yöntemiyle yerinde ikiye ayıran ve pivotun nihai indeksini döndüren `size_t lomuto_partition(int *arr, size_t low, size_t high)` fonksiyonunu yazın. n bölünen eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) tek geçiş olmalı"
  - "Ek bellek O(1) olmalı"
  - "Pivot nihai indeksine yerleştirilmeli"
expected:
  time: { lomuto_partition: "n" }
  space: "1"
concept_tags: [arrays, loop-invariant]
checklist_extra:
  - "Pivottan küçük elemanlar sol tarafa doğru takas edilmiş mi?"
  - "Pivot en son doğru konuma getirilmiş mi?"
reference_solution_path: private/solutions/c-medium-quicksort-partition.c
hint_ladder:
  1: "Dizinin son elemanını pivot seçip küçük elemanlar için bir sınır indeksi (i) tutun."
  2: "Pivottan küçük bir eleman gördükçe sınır indeksini artırıp elemanı o sınıra takas edin; en son pivotu sınırın bir sağına taşıyın."
  3: "Bu algoritma 'Lomuto bölme algoritması (Lomuto partition scheme)' olarak bilinir."
```

---
### c-medium-custom-qsort-generic

```yaml
id: c-medium-custom-qsort-generic
version: 1
language: c
engine: none
difficulty: medium
title: "Karşılaştırma fonksiyon işaretçisi alan genel hızlı sıralama"
prompt: |
  Her türlü veri türünü sıralayabilen, eleman boyutu ve karşılaştırma fonksiyon işaretçisi alan genel amaçlı hızlı sıralama `void custom_generic_sort(void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *))` fonksiyonunu yazın. n sıralanacak eleman sayısıdır.
constraints:
  - "Ortalama zaman karmaşıklığı O(n log n) olmalı"
  - "Ek bellek çağrı yığını için O(log n) olmalı"
  - "Bellek kopyalamaları bayt düzeyinde (char*) yapılmalı"
expected:
  time: { custom_generic_sort: "n log n" }
  space: "log n"
concept_tags: [pointers, pointer-arithmetic]
checklist_extra:
  - "Eleman takasları bayt bayt güvenle gerçekleştirilmiş mi?"
  - "Özyineleme derinliği log n düzeyinde tutulmuş mu?"
reference_solution_path: private/solutions/c-medium-custom-qsort-generic.c
hint_ladder:
  1: "Eleman adreslerini base + i * size şeklinde hesaplayın."
  2: "Karşılaştırma için çağıranın verdiği fonksiyon işaretçisini kullanıp yer değiştirmeleri bayt düzeyinde takas edin."
  3: "Bu yapı 'genel amaçlı hızlı sıralama gerçekleştirimi (generic quicksort implementation)' olarak bilinir."
```

---
### c-medium-binary-tree-insert

```yaml
id: c-medium-binary-tree-insert
version: 1
language: c
engine: none
difficulty: medium
title: "İkili arama ağacına düğüm ekleme"
prompt: |
  Kökü verilen ikili arama ağacına yeni bir tamsayı ekleyen ve ağacın kökünü döndüren `TreeNode *bst_insert(TreeNode *root, int val)` fonksiyonunu yazın. Değer ağaçta zaten varsa ekleme yapılmamalıdır. n ağaçtaki düğüm sayısıdır.
constraints:
  - "Dengeli ağaçta zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek çağrı yığını için O(log n) olmalı"
  - "Yeni düğüm dinamik tahsis edilmelidir"
expected:
  time: { bst_insert: "log n" }
  space: "log n"
concept_tags: [dynamic-memory, binary-search]
checklist_extra:
  - "Yeni düğüm oluşturulurken malloc hatası denetlenmiş mi?"
  - "Küçük değerler sola, büyük değerler sağa doğru yönlendirilmiş mi?"
reference_solution_path: private/solutions/c-medium-binary-tree-insert.c
hint_ladder:
  1: "Kök boşsa yeni düğümü oluşturup kök olarak döndürün."
  2: "Değer kökten küçükse sol alt ağaca, büyükse sağ alt ağaca özyinelemeli olarak ekleyin."
  3: "Bu işlem 'ikili arama ağacına eleman ekleme (binary search tree insertion)' olarak bilinir."
```

---
### c-medium-binary-tree-inorder

```yaml
id: c-medium-binary-tree-inorder
version: 1
language: c
engine: none
difficulty: medium
title: "İkili ağacı simetrik sırada diziye aktarma"
prompt: |
  İkili arama ağacının elemanlarını küçükten büyüğe (in-order) sırada out_arr dizisine yazan `void bst_inorder(const TreeNode *root, int *out_arr, size_t *out_idx)` fonksiyonunu yazın. n ağaçtaki toplam düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek çağrı yığını için O(log n) olmalı"
  - "out_idx her yazılan elemanda 1 artırılmalıdır"
expected:
  time: { bst_inorder: "n" }
  space: "log n"
concept_tags: [pointers, arrays]
checklist_extra:
  - "Önce sol alt ağaç, sonra kök, en son sağ alt ağaç ziyaret edilmiş mi?"
  - "out_idx işaretçisi doğru güncellenmiş mi?"
reference_solution_path: private/solutions/c-medium-binary-tree-inorder.c
hint_ladder:
  1: "Önce sol alt ağacı ziyaret edin."
  2: "Mevcut düğümün değerini diziye yazıp indeksi artırın, ardından sağ alt ağacı ziyaret edin."
  3: "Bu ağaç dolaşımı 'simetrik ağaç gezintisi (in-order tree traversal)' olarak bilinir."
```

---
### c-medium-binary-tree-height

```yaml
id: c-medium-binary-tree-height
version: 1
language: c
engine: none
difficulty: medium
title: "İkili ağacın maksimum derinliğini hesaplama"
prompt: |
  Kökü verilen ikili bir ağacın kökten en uzak yaprağa kadar olan düğüm sayısını (maksimum derinliğini) hesaplayan `size_t tree_max_depth(const TreeNode *root)` fonksiyonunu yazın. Boş ağaç için derinlik 0 olmalıdır. n ağaçtaki toplam düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek çağrı yığını için O(log n) olmalı"
  - "root NULL ise 0 dönmeli"
expected:
  time: { tree_max_depth: "n" }
  space: "log n"
concept_tags: [pointers, edge-cases]
checklist_extra:
  - "Sol ve sağ alt ağaç derinliklerinden büyük olanı seçilmiş mi?"
  - "Özyineleme taban koşulu (root == NULL) doğru tanımlanmış mı?"
reference_solution_path: private/solutions/c-medium-binary-tree-height.c
hint_ladder:
  1: "Kök boş ise derinlik sıfırdır."
  2: "Sol ve sağ alt ağaçların derinliklerini özyinelemeli olarak bulup büyük olanına 1 ekleyin."
  3: "Bu algoritma 'ağaç derinliği hesaplama (maximum depth of binary tree)' olarak bilinir."
```

---
### c-medium-binary-tree-is-bst

```yaml
id: c-medium-binary-tree-is-bst
version: 1
language: c
engine: none
difficulty: medium
title: "Ağacın geçerli ikili arama ağacı olduğunu doğrulama"
prompt: |
  İkili bir ağacın tüm düğümlerinin ikili arama ağacı kurallarına (sol alt ağaçtaki tüm değerler kesinlikle küçük, sağ alt ağaçtaki tüm değerler kesinlikle büyük) uyup uymadığını denetleyen `bool is_valid_bst(const TreeNode *root, long long min_val, long long max_val)` fonksiyonunu yazın. n ağaçtaki düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek çağrı yığını için O(log n) olmalı"
  - "Sınırlar tamsayı taşmasını önlemek için 64-bit tutulmalı"
expected:
  time: { is_valid_bst: "n" }
  space: "log n"
concept_tags: [binary-search, integer-overflow]
checklist_extra:
  - "Sadece ebeveyn-çocuk değil tüm alt ağacın aralık sınırları içinde kaldığı denetlenmiş mi?"
  - "INT_MIN ve INT_MAX sınırları için 64-bit aralık kullanılmış mı?"
reference_solution_path: private/solutions/c-medium-binary-tree-is-bst.c
hint_ladder:
  1: "Her düğümün değeri için geçerli bir (min, max) aralığı tanımlayın."
  2: "Sola giderken maksimum sınırı, sağa giderken minimum sınırı mevcut düğümün değeriyle daraltın."
  3: "Bu doğrulama yaklaşımı 'aralık kısıtlamalı ikili arama ağacı doğrulaması (valid BST range check)' olarak bilinir."
```

---
### c-medium-lowest-common-ancestor-bst

```yaml
id: c-medium-lowest-common-ancestor-bst
version: 1
language: c
engine: none
difficulty: medium
title: "İkili arama ağacında en yakın ortak atayı bulma"
prompt: |
  İkili arama ağacında p ve q değerlerine sahip iki düğümün en yakın ortak atasını (LCA) döngüsel olarak bulan `const TreeNode *lca_bst(const TreeNode *root, int p, int q)` fonksiyonunu yazın. n ağaçtaki düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı dengeli ağaçta O(log n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "Döngüsel (iterative) gerçekleştirilmeli"
expected:
  time: { lca_bst: "log n" }
  space: "1"
concept_tags: [binary-search, pointers]
checklist_extra:
  - "p ve q her ikisi birden küçükse sola, büyükse sağa gidilmiş mi?"
  - "Değerler çatallandığı an o düğüm LCA olarak dönülmüş mü?"
reference_solution_path: private/solutions/c-medium-lowest-common-ancestor-bst.c
hint_ladder:
  1: "Kökten başlayarak p ve q değerlerinin her ikisi de mevcut değerden küçükse sola, büyükse sağa yürüyün."
  2: "Ayrışma noktasına ulaştığınızda mevcut düğüm en yakın ortak atadır."
  3: "Bu arama yöntemi 'ikili arama ağacında en yakın ortak ata (lowest common ancestor in BST)' olarak bilinir."
```

---
### c-medium-min-heap-operations

```yaml
id: c-medium-min-heap-operations
version: 1
language: c
engine: none
difficulty: medium
title: "Dizi tabanlı min-heap yapısında kök elemanı çekme"
prompt: |
  Dizi ile temsil edilen bir min-heap yapısından en küçük elemanı (kökü) çeken, son elemanı köke taşıyıp aşağı doğru süzme (sift-down) ile heap özelliğini onaran `bool min_heap_pop(MinHeap *heap, int *out_min)` fonksiyonunu yazın. n yığındaki eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Heap boşsa false dönmeli"
expected:
  time: { min_heap_pop: "log n" }
  space: "1"
concept_tags: [arrays, loop-invariant]
checklist_extra:
  - "Çocuk indeksleri (2*i + 1 ve 2*i + 2) sınır kontrolüyle seçilmiş mi?"
  - "En küçük çocukla takas yapılarak süzme işlemi doğru tamamlanmış mı?"
reference_solution_path: private/solutions/c-medium-min-heap-operations.c
hint_ladder:
  1: "Kök elemanı sonuca kaydedip son elemanı köke taşıyın ve heap boyutunu 1 azaltın."
  2: "Kökteki elemanı iki çocuğu arasında daha küçük olanla takas ederek heap kuralı sağlanana kadar aşağı süzün."
  3: "Bu onarım adımı 'asgari yığından kök çekme ve aşağı süzme (min-heap extract-min sift-down)' olarak bilinir."
```

---
### c-medium-dynamic-string-builder

```yaml
id: c-medium-dynamic-string-builder
version: 1
language: c
engine: none
difficulty: medium
title: "Büyüyen tampon ile verimli metin birleştirici tasarlama"
prompt: |
  Sürekli metin eklemeleri yapıldığında tampon kapasitesini geometrik olarak genişleten ve belleği sızıntısız yöneten `bool sb_append(StringBuilder *sb, const char *str)` fonksiyonunu yazın. m eklenen dizginin uzunluğudur.
constraints:
  - "Amortize zaman karmaşıklığı O(m) olmalı"
  - "Ek bellek O(m) olmalı"
  - "realloc sızıntısı önlenmeli"
expected:
  time: { sb_append: "m" }
  space: "m"
concept_tags: [realloc, dynamic-memory]
checklist_extra:
  - "Gereken yeni kapasite hesaplanırken null terminatör dahil edilmiş mi?"
  - "realloc geçici bir işaretçiye alınıp başarı durumunda sb->buffer güncellenmiş mi?"
reference_solution_path: private/solutions/c-medium-dynamic-string-builder.c
hint_ladder:
  1: "Mevcut uzunluk ile yeni metin uzunluğunun toplamı kapasiteyi aşıyorsa kapasiteyi en az iki katına çıkarın."
  2: "realloc ile tamponu genişletip yeni metni memcpy ile ekleyin ve sonuna '\0' koyun."
  3: "Bu veri yapısı mekanizması 'dinamik metin inşa edici (string builder)' olarak bilinir."
```

---
### c-medium-simple-hash-set

```yaml
id: c-medium-simple-hash-set
version: 1
language: c
engine: none
difficulty: medium
title: "Ayrık zincirleme ile tamsayı karma kümesi tasarlama"
prompt: |
  Ayrık zincirleme (separate chaining) yöntemiyle çalışan bir tamsayı hash kümesine yeni eleman ekleyen `bool hash_set_insert(HashSet *hs, int key)` fonksiyonunu yazın. Eleman zaten varsa false, başarıyla eklenirse true dönmelidir.
constraints:
  - "Ortalama zaman karmaşıklığı O(1*) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Negatif anahtarlar için hash indeksi pozitif yapılmalıdır"
expected:
  time: { hash_set_insert: "1*" }
  space: "1"
concept_tags: [hashing, dynamic-memory]
checklist_extra:
  - "Negatif sayılar için ((key % num_buckets) + num_buckets) % num_buckets formülü kullanılmış mı?"
  - "Zincirdeki mükerrer eleman kontrolü yapılmış mı?"
reference_solution_path: private/solutions/c-medium-simple-hash-set.c
hint_ladder:
  1: "Anahtarın hash kodunu hesaplayıp ilgili kovanın (bucket) bağlı listesini bulun."
  2: "Listede anahtar yoksa yeni bir düğüm tahsis edip listenin başına ekleyin."
  3: "Bu karma yapısı tekniği 'ayrık zincirlemeli karma kümesi (separate chaining hash set)' olarak bilinir."
```

---
### c-medium-run-length-encode

```yaml
id: c-medium-run-length-encode
version: 1
language: c
engine: none
difficulty: medium
title: "Ardışık yinelenen karakterleri sayarak dizgi sıkıştırma"
prompt: |
  Ardışık tekrar eden karakterleri karakter ve tekrar sayısı biçiminde (örneğin 'aaabb' -> 'a3b2') dinamik bellekte sıkıştıran `char *run_length_encode(const char *str)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "str NULL veya boş ise boş metin dönmeli"
expected:
  time: { run_length_encode: "n" }
  space: "n"
concept_tags: [strings, dynamic-memory]
checklist_extra:
  - "Ardışık karakter sayımı tek geçişte yapılmış mı?"
  - "Sayılar metne dönüştürülürken tampon taşması engellenmiş mi?"
reference_solution_path: private/solutions/c-medium-run-length-encode.c
hint_ladder:
  1: "Metni tararken aynı karakter devam ettiği sürece sayacı artırın."
  2: "Karakter değiştiğinde harfi ve sayacı hedef tampona yazıp yeni karaktere geçin."
  3: "Bu veri sıkıştırma algoritması 'çalışma uzunluğu kodlaması (run-length encoding)' olarak bilinir."
```

---
### c-medium-run-length-decode

```yaml
id: c-medium-run-length-decode
version: 1
language: c
engine: none
difficulty: medium
title: "Sıkıştırılmış çalışma uzunluğu dizgisini açma"
prompt: |
  Karakter ve tekrar sayılarından oluşan (örneğin 'a3b2') bir dizgiyi orijinal haline ('aaabb') dinamik bellekte açan `char *run_length_decode(const char *encoded)` fonksiyonunu yazın. Geçersiz biçimde NULL dönmelidir. n kodlanmış metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Format hatası durumunda NULL dönülüp sızıntı önlenmeli"
expected:
  time: { run_length_decode: "n" }
  space: "n"
concept_tags: [strings, input-validation]
checklist_extra:
  - "Tekrar sayısı birden fazla basamaklı olduğunda doğru çözümlenmiş mi?"
  - "Tahsis edilen bellek boyutu önceden doğru hesaplanmış mı?"
reference_solution_path: private/solutions/c-medium-run-length-decode.c
hint_ladder:
  1: "Önce açılmış metnin toplam boyutunu hesaplamak için bir ön tarama yapıp malloc çağırın."
  2: "İkinci geçişte harfleri belirtilen adet kadar hedef tampona yazın."
  3: "Bu işlem 'çalışma uzunluğu kodunu açma (run-length decoding)' olarak bilinir."
```

---
### c-medium-bit-array-bloom

```yaml
id: c-medium-bit-array-bloom
version: 1
language: c
engine: none
difficulty: medium
title: "Kompakt bit dizisi üzerinde bit ayar ve denetim fonksiyonları"
prompt: |
  uint8_t dizisi olarak tutulan bir bit kümesinde bit_index konumundaki biti 1 yapan `void bitset_set(uint8_t *bitset, size_t bit_index)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Bayt indeksi bit_index / 8, bit ofseti bit_index % 8 ile hesaplanmalı"
expected:
  time: { bitset_set: "1" }
  space: "1"
concept_tags: [pointer-arithmetic, arrays]
checklist_extra:
  - "bit_index / 8 ve bit_index % 8 hesapları doğru yapılmış mı?"
  - "bitset[byte_idx] |= (1 << bit_offset) maskesi doğru uygulanmış mı?"
reference_solution_path: private/solutions/c-medium-bit-array-bloom.c
hint_ladder:
  1: "Hangi bayta erişeceğinizi bit_index / 8 (veya bit_index >> 3) ile bulun."
  2: "Bayt içindeki ilgili biti 1 << (bit_index & 7) maskesini VEYA operatörü ile uygulayarak 1 yapın."
  3: "Bu bit manipülasyonu 'bit dizisinde bit ayarlama (bitset bit manipulation)' olarak bilinir."
```

---
### c-medium-utf8-char-count

```yaml
id: c-medium-utf8-char-count
version: 1
language: c
engine: none
difficulty: medium
title: "Geçerli UTF-8 bayt dizisindeki Unicode karakter adedini sayma"
prompt: |
  Null ile sonlandırılmış geçerli bir UTF-8 metindeki gerçek Unicode karakter (kod noktası) adedini bayt başlıklarına bakarak hesaplayan `size_t utf8_strlen(const char *utf8_str)` fonksiyonunu yazın. n bayt sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Devam baytları (10xxxxxx) sayıma dahil edilmemeli"
expected:
  time: { utf8_strlen: "n" }
  space: "1"
concept_tags: [strings, input-validation]
checklist_extra:
  - "Devam baytı maskesi (byte & 0xC0) != 0x80 ile doğru filtrelenmiş mi?"
  - "NULL işaretçi kontrolü yapılmış mı?"
reference_solution_path: private/solutions/c-medium-utf8-char-count.c
hint_ladder:
  1: "UTF-8 kodlamasında çok baytlı karakterlerin devam baytları ikilik 10xxxxxx biçimindedir."
  2: "Yalnızca 10xxxxxx ile başlamayan baytları sayarak toplam karakter sayısını elde edebilirsiniz."
  3: "Bu algoritma 'UTF-8 karakter sayısı hesaplama (UTF-8 character counting)' olarak bilinir."
```

---
### c-medium-utf8-validate

```yaml
id: c-medium-utf8-validate
version: 1
language: c
engine: none
difficulty: medium
title: "Bayt dizisinin geçerli UTF-8 kodlaması olduğunu doğrulama"
prompt: |
  Verilen bir bayt dizisinin geçerli bir UTF-8 dizilimi olup olmadığını (önek baytları, beklenen devam baytı sayısı ve aşırı uzun kodlama kurallarına göre) denetleyen `bool is_valid_utf8(const uint8_t *data, size_t len)` fonksiyonunu yazın. n bayt sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Beklenmeyen dizi sonu ve hatalı devam baytları false dönmeli"
expected:
  time: { is_valid_utf8: "n" }
  space: "1"
concept_tags: [state-machine, input-validation]
checklist_extra:
  - "1, 2, 3 ve 4 baytlık karakter kalıpları doğru ayrıştırılmış mı?"
  - "Tamamlanmamış bayt dizilimleri için false dönülmüş mü?"
reference_solution_path: private/solutions/c-medium-utf8-validate.c
hint_ladder:
  1: "Her karakterin ilk baytından kaç devam baytı gelmesi gerektiğini belirleyin."
  2: "Takip eden baytların her birinin 10xxxxxx biçiminde olduğunu teyit edin."
  3: "Bu durum denetimi 'UTF-8 geçerlilik doğrulaması (UTF-8 validation state machine)' olarak bilinir."
```

---
### c-medium-aligned-memory-alloc

```yaml
id: c-medium-aligned-memory-alloc
version: 1
language: c
engine: none
difficulty: medium
title: "Belirtilen bayt sınırında hizalı bellek tahsis etme"
prompt: |
  Belirtilen bayt hizalamasında (alignment, ikinin kuvveti olmalıdır) size kadar bellek tahsis eden ve çağıranın standart free fonksiyonuyla serbest bırakabileceği bir üst başlık saklayan `void *aligned_malloc(size_t size, size_t alignment)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Orijinal işaretçi hizalı işaretçinin hemen öncesinde saklanmalıdır"
expected:
  time: { aligned_malloc: "1" }
  space: "1"
concept_tags: [dynamic-memory, pointer-arithmetic]
checklist_extra:
  - "alignment değerinin ikinin kuvveti olduğu doğrulanmış mı?"
  - "Orijinal malloc işaretçisi güvenli bir ofsette saklanmış mı?"
reference_solution_path: private/solutions/c-medium-aligned-memory-alloc.c
hint_ladder:
  1: "Hizalama payı ve orijinal göstericiyi saklamak için fazladan bellek ayırın."
  2: "Adresi maskeleyerek alignment sınırına yukarı yuvarlayın ve hemen öncesine orijinal adresi yazın."
  3: "Bu teknik 'özel bellek hizalama (aligned memory allocation)' olarak bilinir."
```

---
### c-medium-ring-buffer-byte

```yaml
id: c-medium-ring-buffer-byte
version: 1
language: c
engine: none
difficulty: medium
title: "Dairesel bayt tamponuna veri yazma"
prompt: |
  Sabit boyutlu dairesel bir bayt tamponuna gelen veri dizisini boş alan yettiği kadar yazan ve yazılan bayt miktarını döndüren `size_t ring_buffer_write(RingBuffer *rb, const uint8_t *data, size_t k)` fonksiyonunu yazın. k yazılmak istenen bayt adedidir.
constraints:
  - "Zaman karmaşıklığı O(k) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Tampon sınırını aşan veriler yazılmamalıdır"
expected:
  time: { ring_buffer_write: "k" }
  space: "1"
concept_tags: [arrays, memory-safety]
checklist_extra:
  - "Kalan boş alan doğru hesaplanmış mı?"
  - "Yazma sırasında tampon sonuna gelindiğinde başa sarma doğru yapılmış mı?"
reference_solution_path: private/solutions/c-medium-ring-buffer-byte.c
hint_ladder:
  1: "Kullanılabilir boş alanı hesaplayıp k ile minimumunu alın."
  2: "Dairesel yazma indeksini takip ederek veriyi tampona aktarın ve indisi modül ile güncelleyin."
  3: "Bu mekanizma 'dairesel tampon bayt yazımı (ring buffer byte write)' olarak bilinir."
```

---
### c-medium-longest-substring-k-distinct

```yaml
id: c-medium-longest-substring-k-distinct
version: 1
language: c
engine: none
difficulty: medium
title: "En fazla k farklı karakter içeren en uzun alt dizgiyi bulma"
prompt: |
  Verilen bir metinde en fazla k adet farklı karakter içeren en uzun kesintisiz alt dizginin uzunluğunu kayan pencere (sliding window) ile hesaplayan `size_t longest_k_distinct(const char *s, size_t k)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) (256 elemanlı ASCII frekans tablosu) olmalı"
  - "k == 0 ise 0 dönmeli"
expected:
  time: { longest_k_distinct: "n" }
  space: "1"
concept_tags: [strings, loop-invariant]
checklist_extra:
  - "Farklı karakter sayısı k'yı aştığında sol işaretçi doğru ilerletilmiş mi?"
  - "Maksimum uzunluk her genişletmede güncellenmiş mi?"
reference_solution_path: private/solutions/c-medium-longest-substring-k-distinct.c
hint_ladder:
  1: "Sağ işaretçiyi ilerleterek pencereye yeni karakterler ekleyin ve frekanslarını artırın."
  2: "Farklı karakter sayısı k'yı aştığında sol işaretçiyi ilerleterek frekansları azaltın ve pencereyi daraltın."
  3: "Bu algoritma 'kayan pencere ile alt dizgi analizi (sliding window k distinct)' olarak bilinir."
```

---
### c-medium-subarray-sum-equals-k

```yaml
id: c-medium-subarray-sum-equals-k
version: 1
language: c
engine: none
difficulty: medium
title: "Toplamı hedef değere eşit alt dizi adedini önek toplamıyla bulma"
prompt: |
  n elemanlı bir tamsayı dizisinde toplamları tam olarak k tamsayısına eşit olan bitişik alt dizilerin toplam sayısını önek toplamı tablosuyla bulan `size_t count_subarrays_sum_k(const int *arr, size_t n, int k)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Önek toplamı frekansları hash tablosunda tutulmalıdır"
expected:
  time: { count_subarrays_sum_k: "n" }
  space: "n"
concept_tags: [hashing, arrays]
checklist_extra:
  - "prefix_sum - k değeri hash tablosunda aranmış mı?"
  - "Başlangıç durumu için 0 toplamı frekansı 1 olarak eklenmiş mi?"
reference_solution_path: private/solutions/c-medium-subarray-sum-equals-k.c
hint_ladder:
  1: "Diziyi gezerken birikimli önek toplamını (curr_sum) güncelleyin."
  2: "curr_sum - k değerinin geçmişte kaç kez görüldüğünü hash tablosundan okuyup cevaba ekleyin."
  3: "Bu algoritma 'önek toplamı ve karma tablosuyla alt dizi sayımı (prefix sum hash map)' olarak bilinir."
```

---
### c-medium-realloc-growth-factor

```yaml
id: c-medium-realloc-growth-factor
version: 1
language: c
engine: none
difficulty: medium
title: "Üstel bellek büyütme stratejisiyle tampon genişletme"
prompt: |
  Dinamik bir tamponun kapasitesini üstel büyüme katsayısı (örneğin 1.5x veya 2x) ile genişleten, olası taşmaları denetleyen `bool grow_buffer_geometric(Buffer *buf, size_t min_capacity)` fonksiyonunu yazın. İşlem başarısız olursa eski bellek korunmalıdır.
constraints:
  - "Amortize zaman karmaşıklığı O(1*) olmalı"
  - "Ek bellek O(1) olmalı"
  - "SIZE_MAX taşması kontrol edilmelidir"
expected:
  time: { grow_buffer_geometric: "1*" }
  space: "1"
concept_tags: [realloc, amortized-analysis]
checklist_extra:
  - "Yeni kapasite hesaplanırken boyut taşması önlenmiş mi?"
  - "realloc geçici değişkene atanarak sızıntı engellenmiş mi?"
reference_solution_path: private/solutions/c-medium-realloc-growth-factor.c
hint_ladder:
  1: "Yeni kapasiteyi mevcut kapasitenin iki katı ve min_capacity'den büyük olacak şekilde seçin."
  2: "realloc çağrısını geçici işaretçide tutup başarılı olursa yapıya aktarın."
  3: "Bu strateji 'geometrik bellek genişletme (geometric buffer reallocation)' olarak bilinir."
```

---
### c-medium-doubly-linked-list-lru

```yaml
id: c-medium-doubly-linked-list-lru
version: 1
language: c
engine: none
difficulty: medium
title: "Çift yönlü bağlı listede düğümü başa taşıma"
prompt: |
  Çift yönlü bağlı bir listede verilen düğümü mevcut konumundan koparıp listenin en başına taşıyan `void dlist_move_to_front(DList *list, DNode *node)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Düğüm zaten baştaysa işlem yapılmamalıdır"
expected:
  time: { dlist_move_to_front: "1" }
  space: "1"
concept_tags: [linked-list, pointers]
checklist_extra:
  - "Düğümün önceki ve sonraki komşuları birbirine doğru bağlanmış mı?"
  - "Listenin tail ve head işaretçileri gerektiğinde güncellenmiş mi?"
reference_solution_path: private/solutions/c-medium-doubly-linked-list-lru.c
hint_ladder:
  1: "Düğümün prev ve next bağlantılarını kopararak komşularını birbirine bağlayın."
  2: "Düğümü listenin mevcut baş düğümünün önüne ekleyip listenin head işaretçisini güncelleyin."
  3: "Bu operasyon 'çift yönlü listede başa alma (splice to front)' olarak bilinir."
```

---
### c-medium-trie-prefix-tree

```yaml
id: c-medium-trie-prefix-tree
version: 1
language: c
engine: none
difficulty: medium
title: "Sözcük öneklerini saklayan önek ağacına ekleme yapma"
prompt: |
  Küçük İngilizce harfler içeren bir sözcüğü Trie (önek ağacı) yapısına ekleyen `bool trie_insert(TrieNode *root, const char *word)` fonksiyonunu yazın. m sözcüğün karakter sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(m) olmalı"
  - "Ek bellek O(m) olmalı"
  - "Sözcük sonundaki düğümün is_end bayrağı true yapılmalıdır"
expected:
  time: { trie_insert: "m" }
  space: "m"
concept_tags: [dynamic-memory, strings]
checklist_extra:
  - "Her harf için 26 çocuk işaretçisinden ilgili olanı bulunup yoksa tahsis edilmiş mi?"
  - "Bellek tahsis başarısızlıkları yönetilmiş mi?"
reference_solution_path: private/solutions/c-medium-trie-prefix-tree.c
hint_ladder:
  1: "Sözcüğün her harfi için kökten başlayarak ağaçta ilgili çocuk işaretçisini takip edin."
  2: "Düğüm mevcut değilse yeni bir TrieNode oluşturup bağlayın ve sözcük bittiğinde is_end işaretini koyun."
  3: "Bu veri yapısı adımı 'önek ağacına sözcük ekleme (trie insertion)' olarak bilinir."
```

---
### c-medium-topological-sort-indegree

```yaml
id: c-medium-topological-sort-indegree
version: 1
language: c
engine: none
difficulty: medium
title: "Yönlü döngüsüz çizgede giriş derecesiyle topolojik sıralama"
prompt: |
  num_nodes düğümlü bir yönlü döngüsüz çizgenin (DAG) topolojik sıralamasını kuyruk ve giriş dereceleri (in-degree) kullanarak dinamik bir dizide döndüren `int *topological_sort_kahn(size_t num_nodes, const AdjList *adj)` fonksiyonunu yazın. Çizgede döngü varsa NULL dönmelidir. n düğüm ve m kenar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n + m) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Döngü tespitinde NULL dönülmeli"
expected:
  time: { topological_sort_kahn: "n + m" }
  space: "n"
concept_tags: [arrays, dynamic-memory]
checklist_extra:
  - "Giriş derecesi 0 olan düğümler başlangıçta kuyruğa alınmış mı?"
  - "Sıralamaya giren düğüm sayısı num_nodes'a eşit değilse döngü saptanmış mı?"
reference_solution_path: private/solutions/c-medium-topological-sort-indegree.c
hint_ladder:
  1: "Tüm düğümlerin giriş derecelerini hesaplayıp derecesi 0 olanları bir kuyruğa ekleyin."
  2: "Kuyruktan düğüm çektikçe komşularının giriş derecelerini bir azaltıp derecesi 0 olanları kuyruğa ekleyin."
  3: "Bu çizge algoritması 'Kahn topolojik sıralama algoritması (Kahn's topological sort)' olarak bilinir."
```

---
### c-medium-dijkstra-shortest-path

```yaml
id: c-medium-dijkstra-shortest-path
version: 1
language: c
engine: none
difficulty: medium
title: "Ağırlıklı çizgede en kısa yol mesafesini hesaplama"
prompt: |
  Negatif kenar içermeyen ağırlıklı bir çizgede source düğümünden diğer tüm düğümlere olan en kısa mesafeleri hesaplayan `int *dijkstra_shortest_path(size_t num_nodes, const EdgeList *edges, size_t source)` fonksiyonunu yazın. Ulaşılamayan düğümler için mesafe INT_MAX olmalıdır. n düğüm ve m kenar adedidir.
constraints:
  - "Zaman karmaşıklığı O(m log n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Min-heap öncelik kuyruğu kullanılmalıdır"
expected:
  time: { dijkstra_shortest_path: "m log n" }
  space: "n"
concept_tags: [arrays, performance]
checklist_extra:
  - "Mesafe dizisi INT_MAX ile ve kaynak düğüm 0 ile başlatılmış mı?"
  - "Daha önce işlenmiş daha uzun yollar elenmiş mi?"
reference_solution_path: private/solutions/c-medium-dijkstra-shortest-path.c
hint_ladder:
  1: "Kaynak düğümün mesafesini 0 yapıp öncelik kuyruğuna ekleyin."
  2: "En küçük mesafeli düğümü çekerek komşularını gevşetin (relax) ve güncellenenleri kuyruğa ekleyin."
  3: "Bu algoritma 'Dijkstra en kısa yol algoritması (Dijkstra's shortest path)' olarak bilinir."
```

---
### c-medium-parse-json-number

```yaml
id: c-medium-parse-json-number
version: 1
language: c
engine: none
difficulty: medium
title: "JSON sayı dizgisini durumsal olarak ayrıştırma"
prompt: |
  Verilen bir metindeki JSON uyumlu tamsayı veya ondalıklı sayıyı (isteğe bağlı e/E üs gösterimi dahil) durum makinesiyle ayrıştırarak double türüne çeviren `bool parse_json_number(const char *str, double *out_val)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Geçersiz biçimlerde false dönmelidir"
expected:
  time: { parse_json_number: "n" }
  space: "1"
concept_tags: [state-machine, input-validation]
checklist_extra:
  - "İşaret, tam kısım, ondalık nokta ve üs durumları doğru modellenmiş mi?"
  - "Öncül sıfır kuralları (01 gibi geçersiz durumlar) kontrol edilmiş mi?"
reference_solution_path: private/solutions/c-medium-parse-json-number.c
hint_ladder:
  1: "Karakterleri durum makinesinde (işaret, tam sayı, ondalık, üs) ilerleterek okuyun."
  2: "Herhangi bir geçersiz geçişte veya bitişte kabul durumunda değilseniz false dönün."
  3: "Bu yöntem 'sonlu durum makinesi ile sayı ayrıştırma (finite state machine number parser)' olarak bilinir."
```

---
### c-medium-memory-pool-fixed-size

```yaml
id: c-medium-memory-pool-fixed-size
version: 1
language: c
engine: none
difficulty: medium
title: "Sabit boyutlu bloklar tahsis eden serbest liste bellek havuzu"
prompt: |
  Önceden tahsis edilmiş büyük bir bellek bloğunda sabit boyutlu hücreleri O(1) sürede tahsis eden `void *pool_alloc(MemoryPool *pool)` fonksiyonunu yazın. Havuzda serbest blok kalmadıysa NULL dönmelidir.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Serbest bloklar gömülü bağlı liste (free list) ile yönetilmelidir"
expected:
  time: { pool_alloc: "1" }
  space: "1"
concept_tags: [dynamic-memory, pointer-arithmetic]
checklist_extra:
  - "Serbest liste başındaki blok çekilip head bir sonrakine kaydırılmış mı?"
  - "Blok içi işaretçi gömme (embedded pointer) doğru kullanılmış mı?"
reference_solution_path: private/solutions/c-medium-memory-pool-fixed-size.c
hint_ladder:
  1: "Havuzun free_list işaretçisinin gösterdiği bloğu alın."
  2: "free_list işaretçisini o bloğun içinde saklanan next adresine güncelleyip bloğu döndürün."
  3: "Bu tahsis yöntemi 'sabit boyutlu bellek havuzu tahsisi (fixed-size memory pool allocation)' olarak bilinir."
```

---
### c-hard-lru-cache-implementation

```yaml
id: c-hard-lru-cache-implementation
version: 1
language: c
engine: none
difficulty: hard
title: "Sabit sürede çalışan en az son kullanılan önbellek sistemi"
prompt: |
  En son kullanılan elemanları çift yönlü bağlı listede ve karma tablosunda tutarak O(1) sürede get ve put operasyonlarını gerçekleştiren `int lru_get(LRUCache *cache, int key)` fonksiyonunu yazın. Anahtar bulunamazsa -1 dönmelidir.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Erişilen eleman listenin en başına taşınmalıdır"
expected:
  time: { lru_get: "1" }
  space: "1"
concept_tags: [hashing, linked-list]
checklist_extra:
  - "Hash tablosu araması O(1) ortalama sürede tamamlanıyor mu?"
  - "Okunan düğüm listenin başına taşınırken bağlantılar koparılmadan korunmuş mu?"
reference_solution_path: private/solutions/c-hard-lru-cache-implementation.c
hint_ladder:
  1: "Anahtarı karma tablosunda arayarak karşılık gelen çift yönlü liste düğümünü bulun."
  2: "Düğüm mevcutsa değerini okuyup düğümü listenin en başına taşıyın."
  3: "Bu veri yapısı mekanizması 'en az son kullanılan önbellek erişimi (LRU cache access)' olarak bilinir."
```

---
### c-hard-custom-malloc-free

```yaml
id: c-hard-custom-malloc-free
version: 1
language: c
engine: none
difficulty: hard
title: "Statik bellek bloğu üzerinde serbest liste bellek yöneticisi"
prompt: |
  Önceden ayrılmış büyük bir bellek havuzunda serbest blokları gezerek ilk uyan (first-fit) stratejisiyle blok tahsis eden `void *custom_malloc(size_t size)` fonksiyonunu yazın. Yeterli serbest blok yoksa NULL dönmelidir. n serbest blok sayısıdır.
constraints:
  - "Zaman karmaşıklığı en kötü durumda O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Blok başlıkları (Header) doğru hizalanmalıdır"
expected:
  time: { custom_malloc: "n" }
  space: "1"
concept_tags: [dynamic-memory, pointer-arithmetic]
checklist_extra:
  - "Talep edilen boyut blok başlığı ve hizalama baytlarıyla toplanmış mı?"
  - "Gerektiğinde büyük bir serbest blok ikiye bölünmüş mü?"
reference_solution_path: private/solutions/c-hard-custom-malloc-free.c
hint_ladder:
  1: "Serbest blok listesini baştan sona tarayarak istenen boyutu karşılayan ilk bloğu bulun."
  2: "Blok gerekenden büyükse bloğu bölüp kalan kısmı serbest listede bırakın."
  3: "Bu bellek yönetimi algoritması 'ilk uyan serbest liste bellek tahsisi (first-fit free-list allocator)' olarak bilinir."
```

---
### c-hard-lock-free-ring-buffer

```yaml
id: c-hard-lock-free-ring-buffer
version: 1
language: c
engine: none
difficulty: hard
title: "Atomik indekslerle tek üretici tek tüketici kilit-serbest kuyruk"
prompt: |
  Tek bir üretici ve tek bir tüketicinin eşzamanlı çalıştığı kilit-serbest (lock-free) dairesel kuyruğa atomik işlemlerle veri ekleyen `bool spsc_enqueue(SPSCQueue *q, uint64_t item)` fonksiyonunu yazın. Kuyruk doluysa false dönmelidir.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "C11 stdatomic veya bellek bariyerleri kullanılmalıdır"
expected:
  time: { spsc_enqueue: "1" }
  space: "1"
concept_tags: [performance, memory-safety]
checklist_extra:
  - "Üretici ve tüketici indeksleri atomik bellek sırasıyla (memory_order_release / acquire) güncellenmiş mi?"
  - "Kuyruk taşması önlenmiş mi?"
reference_solution_path: private/solutions/c-hard-lock-free-ring-buffer.c
hint_ladder:
  1: "Üretici kuyruğun başını ve tüketicinin son okuduğu konumu atomik olarak kontrol etsin."
  2: "Veriyi yazdıktan sonra üretici indeksini bellek serbest bırakma sırasıyla (release) ilerletin."
  3: "Bu eşzamanlı veri yapısı 'kilit-serbest tek üretici tek tüketici kuyruğu (lock-free SPSC queue)' olarak bilinir."
```

---
### c-hard-regex-nfa-evaluator

```yaml
id: c-hard-regex-nfa-evaluator
version: 1
language: c
engine: none
difficulty: hard
title: "Düzenli ifade durum çizgesi oluşturma ve desen eşleme"
prompt: |
  '.' (herhangi tek bir karakter) ve '*' (önceki karakterin sıfır veya daha fazla tekrarı) meta-karakterlerini destekleyen bir düzenli ifadeyi (pattern) metin üzerinde eşleştiren `bool match_regex_nfa(const char *pattern, const char *text)` fonksiyonunu yazın. n metin ve m desen uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(m) olmalı"
  - "Özyineleme veya durum çizgesiyle çözülmeli"
expected:
  time: { match_regex_nfa: "n*m" }
  space: "m"
concept_tags: [state-machine, strings]
checklist_extra:
  - "Yıldız (*) operatörünün sıfır eşleşme durumu doğru atlanmış mı?"
  - "Nokta (.) karakteri herhangi bir karakterle güvenle eşleştirilmiş mi?"
reference_solution_path: private/solutions/c-hard-regex-nfa-evaluator.c
hint_ladder:
  1: "Desen bir sonraki adımda '*' içeriyorsa sıfır karakter tüketmeyi veya ilk karakter eşleştiğinde metni ilerleterek deseni korumayı deneyin."
  2: "Durum geçişlerini dinamik programlama veya NFA simülasyonu ile takip edin."
  3: "Bu algoritma 'Thompson sonlu durum otomatı ile desen eşleme (Thompson NFA regex matching)' olarak bilinir."
```

---
### c-hard-tarjan-strongly-connected

```yaml
id: c-hard-tarjan-strongly-connected
version: 1
language: c
engine: none
difficulty: hard
title: "Yönlü çizgede güçlü bağlı bileşenleri derinlik öncelikli aramayla bulma"
prompt: |
  num_nodes düğümlü bir yönlü çizgedeki tüm güçlü bağlı bileşenleri (SCC) Tarjan algoritmasıyla tek bir derinlik öncelikli arama (DFS) geçişinde bulan `SCCResult find_scc_tarjan(size_t num_nodes, const AdjList *adj)` fonksiyonunu yazın. n düğüm ve m kenar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n + m) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Ziyaret indeksleri ve düşük bağlantı (lowlink) değerleri yığında takip edilmeli"
expected:
  time: { find_scc_tarjan: "n + m" }
  space: "n"
concept_tags: [arrays, dynamic-memory]
checklist_extra:
  - "dfn ve lowlink dizileri doğru güncellenmiş mi?"
  - "Düğüm kök olduğunda yığındaki düğümler bileşene boşaltılmış mı?"
reference_solution_path: private/solutions/c-hard-tarjan-strongly-connected.c
hint_ladder:
  1: "DFS sırasında her düğüme bir keşif zamanı ve ulaşabileceği en küçük zamanı (lowlink) atayın."
  2: "Düğümün lowlink değeri kendi keşif zamanına eşit olduğunda yığındaki tüm düğümleri yeni bir bileşen olarak çıkarın."
  3: "Bu çizge algoritması 'Tarjan güçlü bağlı bileşenler algoritması (Tarjan's strongly connected components)' olarak bilinir."
```

---
### c-hard-red-black-tree-insert

```yaml
id: c-hard-red-black-tree-insert
version: 1
language: c
engine: none
difficulty: hard
title: "Kırmızı-siyah ağaca düğüm ekleme ve renk onarım adımları"
prompt: |
  Kırmızı-siyah ağaç yapısına yeni bir tamsayı ekleyen ve kırmızı-kırmızı çatışmasını sol/sağ döndürmeler ve renk değişiklikleriyle gideren `RBNode *rb_insert(RBNode *root, int val)` fonksiyonunu yazın. n ağaçtaki düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Kökün daima siyah olması garanti edilmelidir"
expected:
  time: { rb_insert: "log n" }
  space: "1"
concept_tags: [pointers, binary-search]
checklist_extra:
  - "Amcanın (uncle) rengine göre yeniden renklendirme veya döndürme vakaları doğru ayırt edilmiş mi?"
  - "Ağaç kökü işlem sonunda siyah yapılmış mı?"
reference_solution_path: private/solutions/c-hard-red-black-tree-insert.c
hint_ladder:
  1: "Yeni düğümü kırmızı olarak BST kuralıyla yaprağa ekleyin."
  2: "Ebeveyn kırmızı ise amcanın rengine bakın; amca kırmızıysa renklendirme yapın, amca siyahsa döndürme uygulayın."
  3: "Bu dengeli ağaç operasyonu 'kırmızı-siyah ağaç onarımı (red-black tree insertion rebalance)' olarak bilinir."
```

---
### c-hard-avl-tree-rebalance

```yaml
id: c-hard-avl-tree-rebalance
version: 1
language: c
engine: none
difficulty: hard
title: "Dengeli ikili ağaçta ekleme sonrası döndürme operasyonları"
prompt: |
  AVL ağacına yeni bir anahtar ekleyen, her düğümün sol ve sağ yükseklik farkını (denge faktörü) hesaplayarak 4 olası döndürme durumunu (LL, RR, LR, RL) onaran `AVLNode *avl_insert(AVLNode *node, int key)` fonksiyonunu yazın. n ağaçtaki düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek çağrı yığını için O(log n) olmalı"
  - "Yükseklik alanları güncellenmelidir"
expected:
  time: { avl_insert: "log n" }
  space: "log n"
concept_tags: [pointers, binary-search]
checklist_extra:
  - "Denge faktörü [-1, 0, 1] aralığı dışına çıktığında doğru ikili döndürme yapılmış mı?"
  - "Düğüm yükseklikleri döndürme sonrası güncellenmiş mi?"
reference_solution_path: private/solutions/c-hard-avl-tree-rebalance.c
hint_ladder:
  1: "Elemanı standart BST gibi ekledikten sonra geri dönüşte her düğümün yüksekliğini güncelleyin."
  2: "Denge faktörü 1'den büyük veya -1'den küçükse tek veya çift döndürme uygulayarak dengeyi sağlayın."
  3: "Bu ağaç algoritması 'AVL ağacı dengeleme operasyonu (AVL tree rebalance)' olarak bilinir."
```

---
### c-hard-b-tree-search-insert

```yaml
id: c-hard-b-tree-search-insert
version: 1
language: c
engine: none
difficulty: hard
title: "Disk blokları için optimize B-Ağacı düğüm bölme ve ekleme"
prompt: |
  Minimum derecesi t olan bir B-Ağacı düğümüne yeni anahtar ekleyen ve dolu düğümleri yukarı doğru bölen `BTreeNode *btree_insert(BTreeNode *root, int key)` fonksiyonunu yazın. n ağaçtaki toplam anahtar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(log n) olmalı"
  - "Kök bölündüğünde yeni bir kök oluşturulmalıdır"
expected:
  time: { btree_insert: "log n" }
  space: "log n"
concept_tags: [pointers, dynamic-memory]
checklist_extra:
  - "Düğüm 2t - 1 anahtara ulaştığında tam ortadan bölünmüş mü?"
  - "Ortanca anahtar ebeveyn düğüme doğru taşınmış mı?"
reference_solution_path: private/solutions/c-hard-b-tree-search-insert.c
hint_ladder:
  1: "Ağaçta aşağı inerken karşılaşılan tüm dolu düğümleri önceden bölerek tek geçişte ekleme yapın."
  2: "Kök doluysa yeni bir kök tahsis edip eski kökü bölün."
  3: "Bu algoritma 'B-Ağacı düğüm bölme ve ekleme (B-tree insertion and node splitting)' olarak bilinir."
```

---
### c-hard-skip-list-concurrent

```yaml
id: c-hard-skip-list-concurrent
version: 1
language: c
engine: none
difficulty: hard
title: "Olasılıksal çok seviyeli atlama listesi üzerinde arama yapma"
prompt: |
  Rastgele belirlenen seviye yüksekliklerine sahip atlama listesinde (Skip List) hedef değeri en üst seviyeden başlayarak arayan `bool skiplist_search(const SkipList *list, int target)` fonksiyonunu yazın. n listedeki eleman sayısıdır.
constraints:
  - "Ortalama zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek kullanımı O(1) olmalı"
  - "İşaretçi dizisi (forward pointers) doğru taranmalı"
expected:
  time: { skiplist_search: "log n" }
  space: "1"
concept_tags: [linked-list, performance]
checklist_extra:
  - "Arama en üst seviyeden başlayıp aşağıya doğru mu inmiş?"
  - "Değer hedefi aştığında alt seviyeye geçiş doğru yapılmış mı?"
reference_solution_path: private/solutions/c-hard-skip-list-concurrent.c
hint_ladder:
  1: "Listenin en üst seviyesindeki baş düğümden başlayarak sağa doğru ilerleyin."
  2: "Bir sonraki düğümün değeri hedeften büyük veya eşit olduğunda bir alt seviyeye inin."
  3: "Bu arama mekanizması 'atlama listesinde arama (skip list search)' olarak bilinir."
```

---
### c-hard-fiber-coroutine-yield

```yaml
id: c-hard-fiber-coroutine-yield
version: 1
language: c
engine: none
difficulty: hard
title: "Yürütme bağlamını saklayarak kullanıcı alanı iş parçacığı geçişi"
prompt: |
  İki eşzamanlı fiber arasında yazmaçları (stack pointer, program counter vb.) saklayıp yükleyerek bağlam değişimi (context switch) yapan `void coroutine_yield(Coroutine *curr, Coroutine *next)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Tüm kalıcı yazmaçlar doğru saklanmalıdır"
expected:
  time: { coroutine_yield: "1" }
  space: "1"
concept_tags: [pointers, undefined-behavior]
checklist_extra:
  - "Yığın işaretçisi (SP) ve program sayacı (PC) doğru kaydedilip geri yüklenmiş mi?"
  - "Yığın sınır ihlalleri önlenmiş mi?"
reference_solution_path: private/solutions/c-hard-fiber-coroutine-yield.c
hint_ladder:
  1: "Mevcut fiberin çalışma bağlamını (yazmaçları) kendi yapısına kaydedin."
  2: "Hedef fiberin daha önce kaydedilmiş bağlamını işlemciye yükleyerek kaldığı yerden yürütmeyi başlatın."
  3: "Bu düşük seviyeli operasyon 'kullanıcı alanı eşyordam bağlam değişimi (fiber context switch yield)' olarak bilinir."
```

---
### c-hard-copy-on-write-string

```yaml
id: c-hard-copy-on-write-string
version: 1
language: c
engine: none
difficulty: hard
title: "Başvuru sayacı ve yazma anında kopyalama destekli metin yapısı"
prompt: |
  Paylaşılan bir metin tamponunu klonlayan ve başvuru sayacını (reference count) bir artıran, yazma yapılana kadar bellek kopyalamayan `COWString cow_clone(COWString *src)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Başvuru sayacı atomik veya güvenli artırılmalıdır"
expected:
  time: { cow_clone: "1" }
  space: "1"
concept_tags: [ownership, dynamic-memory]
checklist_extra:
  - "Aynı tampon işaretçisi paylaşılırken sayaç doğru artırılmış mı?"
  - "Yazma işleminde kopya çıkarma (unshare) mekanizması hazır tutulmuş mu?"
reference_solution_path: private/solutions/c-hard-copy-on-write-string.c
hint_ladder:
  1: "Yeni bir COWString yapısı oluşturup aynı veri bloğunu gösterin."
  2: "Bellekteki ortak başlıkta yer alan ref_count değerini 1 artırın."
  3: "Bu optimizasyon 'yazma anında kopyalama semantiği (copy-on-write string cloning)' olarak bilinir."
```

---
### c-hard-slab-allocator

```yaml
id: c-hard-slab-allocator
version: 1
language: c
engine: none
difficulty: hard
title: "Sabit boyutlu nesneler için önbellekli slab bellek tahsisçisi"
prompt: |
  Önceden ayrılmış slab sayfalarından sabit boyutlu nesneleri bit maskesi veya gömülü serbest liste ile O(1) sürede tahsis eden `void *slab_alloc(SlabCache *cache)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Dolu slab sayfaları doğru listede tutulmalıdır"
expected:
  time: { slab_alloc: "1" }
  space: "1"
concept_tags: [dynamic-memory, pointer-arithmetic]
checklist_extra:
  - "Kısmi dolu slab sayfasından ilk boş nesne çekilmiş mi?"
  - "Slab dolduğunda tam dolu slab listesine taşınmış mı?"
reference_solution_path: private/solutions/c-hard-slab-allocator.c
hint_ladder:
  1: "Önbelleğin kısmi dolu (partial) slab listesinden ilk sayfayı alın."
  2: "Sayfa içindeki serbest nesneyi ayırıp kullanım sayacını artırın; sayfa dolarsa tam dolu listesine aktarın."
  3: "Bu çekirdek mimarisi tekniği 'slab bellek tahsisçisi operasyonu (slab allocator allocation)' olarak bilinir."
```

---
### c-hard-buddy-memory-system

```yaml
id: c-hard-buddy-memory-system
version: 1
language: c
engine: none
difficulty: hard
title: "İkinin kuvveti blokları bölen ve birleştiren ikiz bellek yöneticisi"
prompt: |
  İstenen bayt boyutunu ikinin en yakın kuvvetine yuvarlayarak buddy (ikiz) ağacından uygun bloğu tahsis eden `void *buddy_alloc(BuddyPool *pool, size_t size)` fonksiyonunu yazın. n toplam blok seviyesi sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Büyük bloklar gerektiğinde ikiz kardeşlere bölünmelidir"
expected:
  time: { buddy_alloc: "log n" }
  space: "1"
concept_tags: [dynamic-memory, pointer-arithmetic]
checklist_extra:
  - "İstenen boyut 2'nin kuvvetine doğru yuvarlanmış mı?"
  - "Uygun blok bulunamadığında bir üst seviyedeki blok ikiye bölünmüş mü?"
reference_solution_path: private/solutions/c-hard-buddy-memory-system.c
hint_ladder:
  1: "İstenen boyutu karşılayan en küçük 2'nin kuvveti bloğu belirleyin."
  2: "O seviyede serbest blok yoksa daha büyük bir serbest bloğu bulup iki kardeş bloğa (buddy) ayırarak aşağı inin."
  3: "Bu bellek algoritması 'ikiz bellek tahsis sistemi (buddy memory allocation)' olarak bilinir."
```

---
### c-hard-garbage-collector-mark-sweep

```yaml
id: c-hard-garbage-collector-mark-sweep
version: 1
language: c
engine: none
difficulty: hard
title: "Sanal makine nesneleri için işaretle ve süpür bellek toplayıcı"
prompt: |
  Sanal makinenin kök işaretçilerinden (root set) ulaşılan tüm nesneleri işaretleyen ve ulaşılamayanları serbest bırakan `void gc_mark_and_sweep(VM *vm)` fonksiyonunu yazın. n yaşayan ve ölü tüm nesnelerin sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) (işaretleme yığını) olmalı"
  - "Döngüsel başvurular doğru işaretlenmelidir"
expected:
  time: { gc_mark_and_sweep: "n" }
  space: "n"
concept_tags: [memory-safety, dynamic-memory]
checklist_extra:
  - "Kök nesnelerden başlayarak tüm erişilebilir nesneler is_marked = 1 yapılmış mı?"
  - "Süpürme aşamasında işaretsiz nesneler free edilip işaretlilerin işareti sıfırlanmış mı?"
reference_solution_path: private/solutions/c-hard-garbage-collector-mark-sweep.c
hint_ladder:
  1: "Kök kümesindeki tüm nesneleri bir yığına atıp derinlemesine dolaşarak erişilebilir olanları işaretleyin."
  2: "Tüm tahsis listesini baştan sona tarayıp işaretsiz olanları serbest bırakın, işaretli olanların işaretini bir sonraki tur için kaldırın."
  3: "Bu çöp toplama algoritması 'işaretle ve süpür bellek toplayıcısı (mark-and-sweep garbage collection)' olarak bilinir."
```

---
### c-hard-disjoint-set-union-rank

```yaml
id: c-hard-disjoint-set-union-rank
version: 1
language: c
engine: none
difficulty: hard
title: "Yol sıkıştırma ve rütbe birleştirme ile ayrık küme veri yapısı"
prompt: |
  Ayrık küme veri yapısında (DSU) x elemanının ait olduğu kümenin kök temsilcisini yol sıkıştırmasıyla (path compression) bulan `size_t dsu_find(DSU *dsu, size_t x)` fonksiyonunu yazın.
constraints:
  - "Amortize zaman karmaşıklığı O(1*) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Yol üzerindeki tüm düğümlerin ebeveyni doğrudan köke bağlanmalıdır"
expected:
  time: { dsu_find: "1*" }
  space: "1"
concept_tags: [amortized-analysis, arrays]
checklist_extra:
  - "Özyineleme veya döngü ile ebeveyn doğrudan köke atanmış mı?"
  - "Tarjan'ın ters Ackermann fonksiyonu amortize analizle doğrulanmış mı?"
reference_solution_path: private/solutions/c-hard-disjoint-set-union-rank.c
hint_ladder:
  1: "Düğümün ebeveyni kendisi değilse özyinelemeli olarak kökü bulun."
  2: "Dönüşte düğümün ebeveynini doğrudan bulunan köke atayarak ağacı düzleştirin."
  3: "Bu optimizasyon 'ayrık kümelerde yol sıkıştırma (path compression in disjoint set union)' olarak bilinir."
```

---
### c-hard-kmp-string-matching

```yaml
id: c-hard-kmp-string-matching
version: 1
language: c
engine: none
difficulty: hard
title: "En uzun önek-sonek tablosu ile doğrusal dizgi arama"
prompt: |
  pattern deseninin text metninde geçtiği ilk indeksi Knuth-Morris-Pratt (KMP) pi tablosunu kullanarak O(n + m) sürede bulan `int kmp_search(const char *text, const char *pattern)` fonksiyonunu yazın. Bulunamazsa -1 dönmelidir. n metin ve m desen uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n + m) olmalı"
  - "Ek bellek O(m) olmalı"
  - "Geriye doğru karakter taraması yapılmamalıdır"
expected:
  time: { kmp_search: "n + m" }
  space: "m"
concept_tags: [strings, arrays]
checklist_extra:
  - "Desen için pi tablosu doğru hesaplanmış mı?"
  - "Uyuşmazlık olduğunda desen indeksi pi tablosuna göre geri çekilmiş mi?"
reference_solution_path: private/solutions/c-hard-kmp-string-matching.c
hint_ladder:
  1: "Öncelikle desenin her indeksi için en uzun uygun önek-sonek uzunluklarını (pi tablosu) hesaplayın."
  2: "Metni tararken bir uyumsuzlukla karşılaştığınızda pi tablosunu kullanarak deseni kaydırın ve metin işaretçisini asla geri almayın."
  3: "Bu algoritma 'Knuth-Morris-Pratt dizgi arama algoritması (Knuth-Morris-Pratt string matching)' olarak bilinir."
```

---
### c-hard-boyer-moore-search

```yaml
id: c-hard-boyer-moore-search
version: 1
language: c
engine: none
difficulty: hard
title: "Kötü karakter atlama kuralı ile hızlı desen arama"
prompt: |
  Kötü karakter kuralı (bad character heuristic) tablosunu kullanarak pattern dizgisini text içinde sağdan sola karşılaştırmalarla arayan `int boyer_moore_search(const char *text, const char *pattern)` fonksiyonunu yazın. Bulunamazsa -1 dönmelidir. n metin uzunluğudur.
constraints:
  - "Ortalama zaman karmaşıklığı O(n) veya daha hızlı olmalı"
  - "Ek bellek O(1) (256 elemanlı ASCII tablosu) olmalı"
  - "Sağdan sola karşılaştırma yapılmalıdır"
expected:
  time: { boyer_moore_search: "n" }
  space: "1"
concept_tags: [strings, performance]
checklist_extra:
  - "Kötü karakter atlama tablosu desenin son görünüm indeksleriyle doldurulmuş mu?"
  - "Eşleşmeme durumunda maksimum atlama miktarı uygulanmış mı?"
reference_solution_path: private/solutions/c-hard-boyer-moore-search.c
hint_ladder:
  1: "Desendeki her karakterin en son görüldüğü indeksi bir atlama tablosuna kaydedin."
  2: "Deseni metinle sağdan sola karşılaştırın; uyuşmayan karakterin tablodaki ofsetine göre metin üzerinde büyük adımlarla atlayın."
  3: "Bu algoritma 'Boyer-Moore dizgi arama algoritması (Boyer-Moore bad character search)' olarak bilinir."
```

---
### c-hard-aho-corasick-automaton

```yaml
id: c-hard-aho-corasick-automaton
version: 1
language: c
engine: none
difficulty: hard
title: "Çoklu sözcük deseni aramak için sonlu durum makinesi kurma"
prompt: |
  Trie ağacı üzerine başarısızlık bağlantıları (failure links) ve sözcük çıktı bağlantıları kurarak genişlik öncelikli aramayla Aho-Corasick otomatı oluşturan `void ac_build_failure_links(ACNode *root)` fonksiyonunu yazın. n ağaçtaki toplam düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) (BFS kuyruğu) olmalı"
  - "Kökün çocuklarının başarısızlık bağlantısı köke bağlanmalıdır"
expected:
  time: { ac_build_failure_links: "n" }
  space: "n"
concept_tags: [state-machine, strings]
checklist_extra:
  - "BFS kuyruğu ile seviye seviye failure linkleri bağlanmış mı?"
  - "Çıktı (output) listeleri alt düğümlere aktarılmış mı?"
reference_solution_path: private/solutions/c-hard-aho-corasick-automaton.c
hint_ladder:
  1: "Kök düğümün doğrudan altındaki düğümlerin başarısızlık bağlantılarını köke ayarlayıp kuyruğa atın."
  2: "Kuyruktan çektiğiniz her düğümün çocukları için ebeveynin başarısızlık bağlantısını takip ederek eşleşen en uzun önek durumunu bulun."
  3: "Bu durum makinesi 'Aho-Corasick çoklu desen otomatı (Aho-Corasick automaton failure links)' olarak bilinir."
```

---
### c-hard-huffman-encoder

```yaml
id: c-hard-huffman-encoder
version: 1
language: c
engine: none
difficulty: hard
title: "Bayt sıklıklarından öncelik kuyruğu ile Huffman ağacı oluşturma"
prompt: |
  256 olası baytın sıklık dizisini alarak min-heap yardımıyla optimal Huffman ağacını inşa eden ve kök düğümünü döndüren `HuffmanNode *build_huffman_tree(const size_t *frequencies)` fonksiyonunu yazın. n benzersiz karakter sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n log n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Tüm yaprak düğümler ve iç düğümler dinamik tahsis edilmelidir"
expected:
  time: { build_huffman_tree: "n log n" }
  space: "n"
concept_tags: [dynamic-memory, performance]
checklist_extra:
  - "Sıfır frekansa sahip baytlar elenmiş mi?"
  - "En küçük iki düğüm çekilip toplam frekansla yeni ebeveyn oluşturulmuş mu?"
reference_solution_path: private/solutions/c-hard-huffman-encoder.c
hint_ladder:
  1: "Frekansı sıfırdan büyük tüm karakterler için tek düğümlü yapraklar oluşturup min-heap'e ekleyin."
  2: "Heap içinde tek düğüm kalana kadar en küçük iki düğümü çekip ortak ebeveyne bağlayarak tekrar heap'e itin."
  3: "Bu algoritma 'Huffman kodlama ağacı inşası (Huffman tree construction)' olarak bilinir."
```

---
### c-hard-huffman-decoder

```yaml
id: c-hard-huffman-decoder
version: 1
language: c
engine: none
difficulty: hard
title: "Huffman bit akışını ağaç üzerinde gezinerek orijinal veriye çözme"
prompt: |
  Huffman ağacının kökünü ve sıkıştırılmış bit akışını alarak bitleri kökten yaprağa takip edip orijinal veriyi dinamik bir tamponda yeniden oluşturan `uint8_t *huffman_decode(const HuffmanNode *root, const uint8_t *bits, size_t bit_len, size_t *out_len)` fonksiyonunu yazın. n bit dizisinin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Yaprağa ulaşıldığında köke dönülmelidir"
expected:
  time: { huffman_decode: "n" }
  space: "n"
concept_tags: [dynamic-memory, pointers]
checklist_extra:
  - "Bit maskeleme (1 << (7 - (i % 8))) ile her bit doğru okunmuş mu?"
  - "Yaprağa varıldığında bayt çıkış tamponuna yazılıp köke sıfırlanmış mı?"
reference_solution_path: private/solutions/c-hard-huffman-decoder.c
hint_ladder:
  1: "Bit dizisindeki her biti sırayla okuyun; 0 ise sol, 1 ise sağ dala sapın."
  2: "Yaprak düğüme vardığınızda taşıdığı baytı çözülen tampona ekleyip ağacın köküne geri dönün."
  3: "Bu açma işlemi 'Huffman bit akışı çözümü (Huffman stream decoding)' olarak bilinir."
```

---
### c-hard-sliding-window-median

```yaml
id: c-hard-sliding-window-median
version: 1
language: c
engine: none
difficulty: hard
title: "İki öncelik kuyruğu ile kayan pencere medyanını hesaplama"
prompt: |
  n elemanlı bir dizide boyutu k olan kayan bir pencerenin her adımındaki medyan değerlerini iki heap (max-heap ve min-heap) yardımıyla hesaplayan `double *sliding_window_median(const int *arr, size_t n, size_t k, size_t *out_len)` fonksiyonunu yazın. n dizi boyutu ve k pencere boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n log k) olmalı"
  - "Ek bellek O(k) olmalı"
  - "Tembel silme (lazy removal) veya doğrudan çıkarma uygulanmalı"
expected:
  time: { sliding_window_median: "n log k" }
  space: "k"
concept_tags: [arrays, dynamic-memory]
checklist_extra:
  - "İki heap arasındaki denge (max_heap boyutu == min_heap boyutu veya +1) korunmuş mu?"
  - "Pencereden çıkan eleman doğru ayıklanmış mı?"
reference_solution_path: private/solutions/c-hard-sliding-window-median.c
hint_ladder:
  1: "Küçük yarıyı bir max-heap'te, büyük yarıyı bir min-heap'te dengeli olarak tutun."
  2: "Her pencere kaydırmasında çıkan elemanı düşürüp yeni elemanı uygun heap'e ekleyerek medyanı kaydedin."
  3: "Bu algoritma 'iki yığın ile kayan pencere medyanı (sliding window median with dual heaps)' olarak bilinir."
```

---
### c-hard-median-of-two-sorted-arrays

```yaml
id: c-hard-median-of-two-sorted-arrays
version: 1
language: c
engine: none
difficulty: hard
title: "İki sıralı dizinin birleşim medyanını logaritmik sürede bulma"
prompt: |
  Küçükten büyüğe sıralı nums1 (n elemanlı) ve nums2 (m elemanlı) dizilerini birleştirmeden ikili arama ile birleşim medyanını O(log(min(n, m))) sürede hesaplayan `double find_median_two_sorted(const int *nums1, size_t n, const int *nums2, size_t m)` fonksiyonunu yazın. n ve m dizi boyutlarıdır.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Daha kısa olan dizi üzerinde ikili arama yapılmalıdır"
expected:
  time: { find_median_two_sorted: "log n" }
  space: "1"
concept_tags: [binary-search, arrays]
checklist_extra:
  - "Bölüm çizgileri (partitionX, partitionY) toplam eleman sayısının yarısını verecek şekilde ayarlanmış mı?"
  - "Sonsuz sınır değerleri (INT_MIN, INT_MAX) doğru kullanılmış mı?"
reference_solution_path: private/solutions/c-hard-median-of-two-sorted-arrays.c
hint_ladder:
  1: "Daha kısa dizi üzerinde ikili arama yaparak sol ve sağ yarıları bölen noktayı belirleyin."
  2: "Her iki dizinin solundaki maksimumların sağındaki minimumlardan küçük veya eşit olduğu an medyanı hesaplayın."
  3: "Bu algoritma 'iki sıralı dizinin medyanını ikili aramayla bulma (median of two sorted arrays)' olarak bilinir."
```

---
### c-hard-merge-k-sorted-lists

```yaml
id: c-hard-merge-k-sorted-lists
version: 1
language: c
engine: none
difficulty: hard
title: "Öncelik kuyruğu kullanarak k adet sıralı bağlı listeyi birleştirme"
prompt: |
  Her biri küçükten büyüğe sıralı k adet bağlı listeyi min-heap kullanarak tek bir sıralı bağlı liste halinde birleştiren `Node *merge_k_sorted_lists(Node **lists, size_t k)` fonksiyonunu yazın. n toplam düğüm sayısı ve k liste sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n log k) olmalı"
  - "Ek bellek O(k) (min-heap boyutu) olmalı"
  - "Yeni düğüm tahsis edilmeden işaretçiler bağlanmalıdır"
expected:
  time: { merge_k_sorted_lists: "n log k" }
  space: "k"
concept_tags: [linked-list, dynamic-memory]
checklist_extra:
  - "k elemanlı min-heap liste başlarıyla başlatılmış mı?"
  - "En küçük düğüm çekilip listeye eklendikten sonra o listenin sonraki düğümü heap'e konmuş mu?"
reference_solution_path: private/solutions/c-hard-merge-k-sorted-lists.c
hint_ladder:
  1: "Her listenin ilk düğümünü k elemanlı bir min-heap'e yerleştirin."
  2: "En küçük düğümü çekip sonuç listesinin sonuna ekleyin ve çekilen düğümün next düğümünü tekrar heap'e itin."
  3: "Bu algoritma 'k adet sıralı listeyi yığınla birleştirme (merge k sorted lists with min-heap)' olarak bilinir."
```

---
### c-hard-maximum-flow-edmonds-karp

```yaml
id: c-hard-maximum-flow-edmonds-karp
version: 1
language: c
engine: none
difficulty: hard
title: "Çizgede artık kapasiteler üzerinde en genişletici yolu bularak akış hesaplama"
prompt: |
  n düğümlü bir akış ağında src kaynağından sink hedefine gönderilebilecek azami akışı (maximum flow) BFS ile en kısa genişletici yolları bularak hesaplayan `int edmonds_karp_max_flow(size_t n, int **capacity, size_t src, size_t sink)` fonksiyonunu yazın. n düğüm ve m kenar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(n^2) olmalı"
  - "Artık kapasite matrisi her genişletmede güncellenmelidir"
expected:
  time: { edmonds_karp_max_flow: "n*m" }
  space: "n^2"
concept_tags: [arrays, dynamic-memory]
checklist_extra:
  - "BFS ile ebeveyn dizisi doğru kurulup yol bulunmuş mu?"
  - "Genişletici yol boyunca artık kapasiteler azaltılıp ters kapasiteler artırılmış mı?"
reference_solution_path: private/solutions/c-hard-maximum-flow-edmonds-karp.c
hint_ladder:
  1: "BFS ile artık kapasitesi pozitif olan kenarlar üzerinden kaynaktan hedefe en kısa yolu arayın."
  2: "Yol üzerindeki darboğaz akış miktarını bulup kenarlardan düşürün ve ters kenarlara ekleyerek toplam akışı artırın."
  3: "Bu ağ akışı algoritması 'Edmonds-Karp azami akış algoritması (Edmonds-Karp maximum flow)' olarak bilinir."
```

---
### c-hard-min-cut-stoer-wagner

```yaml
id: c-hard-min-cut-stoer-wagner
version: 1
language: c
engine: none
difficulty: hard
title: "Yönsüz ağırlıklı çizgede asgari kesiti hesaplama"
prompt: |
  n düğümlü yönsüz ve pozitif ağırlıklı bir çizgenin düğümlerini iki ayrık kümeye bölen kenarların ağırlık toplamı en küçük olanını (global min-cut) Stoer-Wagner algoritmasıyla hesaplayan `int min_cut_stoer_wagner(size_t n, int **weights)` fonksiyonunu yazın. n düğüm adedidir.
constraints:
  - "Zaman karmaşıklığı O(n^2) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Her fazda en son eklenen iki düğüm birleştirilmelidir"
expected:
  time: { min_cut_stoer_wagner: "n^2" }
  space: "n"
concept_tags: [arrays, dynamic-memory]
checklist_extra:
  - "Her fazda en sıkı bağlı düğüm açgözlü olarak seçilmiş mi?"
  - "Faz kesiti global minimum ile kıyaslanıp son iki düğüm daraltılmış mı?"
reference_solution_path: private/solutions/c-hard-min-cut-stoer-wagner.c
hint_ladder:
  1: "Her fazda düğümleri mevcut kümeye olan toplam bağlantı ağırlıklarına göre sırayla ekleyin."
  2: "En son eklenen iki düğüm arasındaki kesit değerini kaydedip bu iki düğümü tek bir düğüm halinde birleştirin."
  3: "Bu algoritma 'Stoer-Wagner asgari kesit algoritması (Stoer-Wagner minimum cut)' olarak bilinir."
```

---
### c-hard-segment-tree-lazy-prop

```yaml
id: c-hard-segment-tree-lazy-prop
version: 1
language: c
engine: none
difficulty: hard
title: "Tembel yayılım ile aralık toplamı ve aralık güncelleme ağacı"
prompt: |
  n elemanlı bir dizide aralık güncellemesini (range update) tembel yayılım (lazy propagation) kullanarak O(log n) sürede uygulayan `void segtree_update_range(SegTree *st, size_t node, size_t l, size_t r, size_t ql, size_t qr, long long val)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Tembel etiketler çocuk düğümlere doğru zamanda yayılmalıdır"
expected:
  time: { segtree_update_range: "log n" }
  space: "1"
concept_tags: [arrays, loop-invariant]
checklist_extra:
  - "Mevcut düğümün tembel değeri alt düğümlere push_down edilmiş mi?"
  - "Aralık tam örtüşüyorsa tembel etiket güncellenip erken dönülmüş mü?"
reference_solution_path: private/solutions/c-hard-segment-tree-lazy-prop.c
hint_ladder:
  1: "Sorgu aralığı mevcut aralığı tamamen kapsıyorsa düğümün değerini güncelleyip tembel etiketini artırın ve hemen dönün."
  2: "Kısmi örtüşmede bekleyen tembel değeri çocuk düğümlere iletip (push-down) iki yarıya özyineleme yapın."
  3: "Bu veri yapısı mekanizması 'kesim ağacında tembel yayılım (segment tree lazy propagation)' olarak bilinir."
```

---
### c-hard-fenwick-binary-indexed-tree

```yaml
id: c-hard-fenwick-binary-indexed-tree
version: 1
language: c
engine: none
difficulty: hard
title: "En düşük anlamlı bit işlemiyle dinamik önek toplamı ağacı"
prompt: |
  İkili İndeksli Ağaç (Fenwick Tree) yapısında belirli bir indeksteki değere ekleme yaparak etkilenen tüm ağaç hücrelerini güncelleyen `void fenwick_add(FenwickTree *ft, size_t index, long long delta)` fonksiyonunu yazın. n ağacın boyutudur.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "index += index & (-index) adımıyla ilerlenmelidir"
expected:
  time: { fenwick_add: "log n" }
  space: "1"
concept_tags: [arrays, performance]
checklist_extra:
  - "1 tabanlı indeksleme kuralına uyulmuş mu?"
  - "index & (-index) ile en düşük anlamlı bit (LSB) doğru izole edilmiş mi?"
reference_solution_path: private/solutions/c-hard-fenwick-binary-indexed-tree.c
hint_ladder:
  1: "İndekse delta değerini ekleyin."
  2: "index += index & (-index) formülüyle en düşük anlamlı biti ekleyerek bir sonraki kapsayıcı aralığa geçin."
  3: "Bu algoritma 'Fenwick ağacı güncelleme adımı (Fenwick tree point update)' olarak bilinir."
```

---
### c-hard-heavy-light-decomposition

```yaml
id: c-hard-heavy-light-decomposition
version: 1
language: c
engine: none
difficulty: hard
title: "Ağaç yollarını ağır ve hafif zincirlere ayıran sorgu altyapısı"
prompt: |
  n düğümlü bir ağaçta alt ağaç boyutlarına göre en büyük alt ağaca giden kenarları ağır kenar seçerek zincirler oluşturan `void hld_decompose(HLDTree *tree, size_t root)` fonksiyonunu yazın. n ağaçtaki düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "DFS ile alt ağaç boyutları ve ağır çocuklar belirlenmeli"
expected:
  time: { hld_decompose: "n" }
  space: "n"
concept_tags: [arrays, dynamic-memory]
checklist_extra:
  - "İlk DFS geçişinde alt ağaç boyutları ve heavy çocuk doğru bulunmuş mu?"
  - "İkinci DFS geçişinde zincir başları (head) ve pozisyonlar doğru atanmış mı?"
reference_solution_path: private/solutions/c-hard-heavy-light-decomposition.c
hint_ladder:
  1: "İlk DFS turunda her düğümün en büyük alt ağaca sahip çocuğunu ağır (heavy) çocuk olarak işaretleyin."
  2: "İkinci turda ağır zincirleri takip ederek her düğüme düz bir dizide kesintisiz segment pozisyonları atayın."
  3: "Bu ağaç ayrıştırma tekniği 'ağır-hafif ağaç ayrıştırması (heavy-light decomposition)' olarak bilinir."
```

---
### c-hard-suffix-array-construction

```yaml
id: c-hard-suffix-array-construction
version: 1
language: c
engine: none
difficulty: hard
title: "Dizgi için son ek dizisini ikili kaldırma tekniğiyle oluşturma"
prompt: |
  n uzunluğundaki bir metnin tüm son eklerinin (suffix) sözlük sırasına göre sıralanmış indekslerini O(n log n) sürede hesaplayan `size_t *build_suffix_array(const char *str, size_t n)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n log n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "İkili kaldırma (prefix doubling) tekniği kullanılmalıdır"
expected:
  time: { build_suffix_array: "n log n" }
  space: "n"
concept_tags: [strings, arrays]
checklist_extra:
  - "2^k uzunluğundaki önekler sıralanırken derecelendirme (rank) dizisi doğru güncellenmiş mi?"
  - "Eşitlik durumlarında ikinci yarının rank değeri karşılaştırılmış mı?"
reference_solution_path: private/solutions/c-hard-suffix-array-construction.c
hint_ladder:
  1: "İlk adımda tek karakterlik öneklere göre sıralama yapıp rank değerlerini belirleyin."
  2: "Her turda uzunluğu iki katına çıkararak (2, 4, 8, ...) ikili parçaların rank çiftlerini sıralayın."
  3: "Bu algoritma 'önek ikiye katlama ile son ek dizisi inşası (suffix array prefix doubling)' olarak bilinir."
```

---
### c-hard-longest-palindromic-substring-manacher

```yaml
id: c-hard-longest-palindromic-substring-manacher
version: 1
language: c
engine: none
difficulty: hard
title: "Genişleme sınırlarını aynalayarak doğrusal sürede en uzun palindromu bulma"
prompt: |
  Verilen bir metindeki en uzun palindromik alt dizgiyi Manacher algoritmasıyla merkez aynalama özelliğini kullanarak O(n) sürede bulan `char *longest_palindrome_manacher(const char *str)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) doğrusal olmalı"
  - "Ek bellek O(n) olmalı"
  - "Karakterler arasına '#' yerleştirilerek çift uzunluklar tek forma indirgenmeli"
expected:
  time: { longest_palindrome_manacher: "n" }
  space: "n"
concept_tags: [strings, arrays]
checklist_extra:
  - "Sağ sınır r ve merkez c doğru güncellenmiş mi?"
  - "i aynası olan 2*c - i noktasının yarıçapı başlangıç değeri olarak kullanılmış mı?"
reference_solution_path: private/solutions/c-hard-longest-palindromic-substring-manacher.c
hint_ladder:
  1: "Metnin her harfinin arasına özel bir ayraç karakteri yerleştirerek tüm palindromları tek merkezli hale getirin."
  2: "Sağ sınırın içinde kalan noktalar için daha önce hesaplanan simetrik noktanın yarıçapını taban alıp sadece sınırı aşan kısımları genişleterek test edin."
  3: "Bu algoritma 'Manacher en uzun palindrom algoritması (Manacher's algorithm)' olarak bilinir."
```

---
### c-hard-arena-allocator-rollback

```yaml
id: c-hard-arena-allocator-rollback
version: 1
language: c
engine: none
difficulty: hard
title: "Bölgesel bellek tahsisçisinde kontrol noktası oluşturma ve geri alma"
prompt: |
  Sıralı bellek tahsis eden bir arena tahsisçisinde daha önce kaydedilmiş bir kontrol noktasına (checkpoint) ofseti geri alarak ara tahsislerin tamamını tek hamlede geçersiz kılan `void arena_restore(Arena *arena, size_t checkpoint)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "checkpoint arena->used değerinden büyükse işlem reddedilmelidir"
expected:
  time: { arena_restore: "1" }
  space: "1"
concept_tags: [dynamic-memory, pointer-arithmetic]
checklist_extra:
  - "Geçersiz bir checkpoint (used sınırından büyük) kontrol edilmiş mi?"
  - "Ofset geriye çekilerek sonraki tahsisler için alan açılmış mı?"
reference_solution_path: private/solutions/c-hard-arena-allocator-rollback.c
hint_ladder:
  1: "Kaydedilen checkpoint ofsetinin geçerli olduğunu teyit edin."
  2: "Arenanın kullanılan bellek sayacını (used) bu checkpoint değerine eşitleyerek aradaki tüm tahsisleri tek işlemde geri alın."
  3: "Bu bellek yönetimi operasyonu 'arena bellek kontrol noktası geri yükleme (arena allocator rollback)' olarak bilinir."
```

---
### c-hard-atomic-aba-solution

```yaml
id: c-hard-atomic-aba-solution
version: 1
language: c
engine: none
difficulty: hard
title: "İşaretli gösterici tekniğiyle kilit-serbest yığında ABA koruması"
prompt: |
  Kilit-serbest bir yığına atomik karşılaştır-ve-değiştir (CAS) ile eleman eklerken ABA problemini önlemek için işaretçi ile birlikte bir sürüm sayacı (tagged pointer) kullanan `bool lf_stack_push(LFStack *stack, void *data)` fonksiyonunu yazın.
constraints:
  - "Amortize zaman karmaşıklığı O(1*) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Çift genişlikte CAS (DWCAS) veya bit paketleme kullanılmalıdır"
expected:
  time: { lf_stack_push: "1*" }
  space: "1"
concept_tags: [pointers, memory-safety]
checklist_extra:
  - "Sürüm sayacı her başarılı veya başarısız denemede doğru yönetilmiş mi?"
  - "CAS döngüsü çakışma durumunda güncel başlığı tekrar okumuş mu?"
reference_solution_path: private/solutions/c-hard-atomic-aba-solution.c
hint_ladder:
  1: "Yığın tepesindeki işaretçiyi ve sürüm numarasını tek bir atomik yapıda okuyun."
  2: "Yeni düğümün next işaretçisini mevcut tepeye bağlayıp sürüm numarasını 1 artırarak CAS ile tepeyi güncelleyin."
  3: "Bu eşzamanlılık çözümü 'etiketli işaretçi ile ABA önleme (tagged pointer ABA prevention)' olarak bilinir."
```

---
### c-hard-hazard-pointers-gc

```yaml
id: c-hard-hazard-pointers-gc
version: 1
language: c
engine: none
difficulty: hard
title: "Kilit-serbest yapılarda güvenli bellek serbest bırakma tablosu"
prompt: |
  Eşzamanlı okuyucuların eriştiği işaretçileri tehlike işaretçisi (hazard pointer) tablosuna kaydederek diğer iş parçacıklarının bu belleği erken serbest bırakmasını engelleyen `void hazard_release(HazardRecord *rec)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Bellek bariyeri ile yazma diğer çekirdeklere görünür kılınmalıdır"
expected:
  time: { hazard_release: "1" }
  space: "1"
concept_tags: [memory-safety, dangling-pointer]
checklist_extra:
  - "Atomik mağaza (atomic store) serbest bırakma sırasıyla mı yapılmış?"
  - "use-after-free ve sarkan işaretçi kesin olarak engellenmiş mi?"
reference_solution_path: private/solutions/c-hard-hazard-pointers-gc.c
hint_ladder:
  1: "İş parçacığı bir düğümle işini bitirdiğinde ilgili hazard pointer kaydını atomik olarak NULL yapın."
  2: "Bellek bariyeri koyarak diğer iş parçacıklarının emekli listesini temizlerken bu adresi artık korumasız görmesini sağlayın."
  3: "Bu bellek güvenliği mekanizması 'tehlike işaretçisi serbest bırakma (hazard pointer retirement)' olarak bilinir."
```

---
### c-hard-thread-pool-work-stealing

```yaml
id: c-hard-thread-pool-work-stealing
version: 1
language: c
engine: none
difficulty: hard
title: "Çift uçlu kuyruktan yerel veya uzaktan görev çeken iş havuzu"
prompt: |
  Kendi yerel çift uçlu kuyruğu (deque) boşalan bir iş parçacığının başka bir rastgele iş parçacığının kuyruk başından görev çalmasını (work stealing) sağlayan `Task *deque_steal(WorkDeque *deque)` fonksiyonunu yazın. Kuyruk boşsa NULL dönmelidir.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Atomik CAS ile kuyruk başı (top) yarışı çözülmelidir"
expected:
  time: { deque_steal: "1" }
  space: "1"
concept_tags: [pointers, performance]
checklist_extra:
  - "Hırsız iş parçacığı kuyruğun başından (top), yerel iş parçacığı sonundan (bottom) mı işlem yapıyor?"
  - "Tek eleman kaldığında yarış durumu CAS ile engellenmiş mi?"
reference_solution_path: private/solutions/c-hard-thread-pool-work-stealing.c
hint_ladder:
  1: "Kuyruğun başındaki (top) indeksi atomik olarak okuyup görevi alın."
  2: "top indeksini atomik CAS ile bir artırmayı deneyin; başarılı olursa görevi döndürün, başarısız olursa çakışma nedeniyle vazgeçin."
  3: "Bu eşzamanlı görev dağıtım tekniği 'iş çalma çift uçlu kuyruğu (Chase-Lev work-stealing deque)' olarak bilinir."
```

---
### c-hard-custom-elf-header-parser

```yaml
id: c-hard-custom-elf-header-parser
version: 1
language: c
engine: none
difficulty: hard
title: "64-bit ikili dosya başlığı ve bölüm tablolarını doğrulama"
prompt: |
  Bellekteki bayt dizisinin geçerli bir 64-bit ELF ikili dosyası olup olmadığını sihirli baytlar (magic bytes), mimari, giriş noktası ve kesit tablosu sınırları üzerinden denetleyen `bool parse_elf64_header(const uint8_t *bytes, size_t size, Elf64Info *out_info)` fonksiyonunu yazın. n bayt sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Tampon aşımı kontrolleri kesinlikle yapılmalıdır"
expected:
  time: { parse_elf64_header: "n" }
  space: "1"
concept_tags: [input-validation, memory-safety]
checklist_extra:
  - "0x7F, 'E', 'L', 'F' sihirli baytları doğrulanmış mı?"
  - "Kesit ve program başlık ofsetlerinin dosya boyutunu aşmadığı denetlenmiş mi?"
reference_solution_path: private/solutions/c-hard-custom-elf-header-parser.c
hint_ladder:
  1: "İlk 4 baytın ELF tanımlayıcısı olduğunu, 5. baytın 64-bit sınıfını (ELFCLASS64) belirttiğini denetleyin."
  2: "Başlık tablosu ofsetlerini ve giriş sayısını okuyup çarpımların tampon sınırları içinde kaldığını doğrulayın."
  3: "Bu güvenlik ayrıştırması 'ELF ikili dosya başlığı doğrulaması (ELF64 header parsing and validation)' olarak bilinir."
```

---
### c-hard-compact-bitset-roaring

```yaml
id: c-hard-compact-bitset-roaring
version: 1
language: c
engine: none
difficulty: hard
title: "Seyrek bit kümeleri için aralık ve dizi tabanlı hibrit depolama"
prompt: |
  Üst 16 biti konteyner anahtarı, alt 16 biti ise eleman değeri olarak saklayan hibrit bit kümesinde verilen 32-bit sayının varlığını ikili aramayla sorgulayan `bool roaring_contains(const RoaringBitmap *bm, uint32_t val)` fonksiyonunu yazın. n toplam konteyner sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Dizi konteyneri ve bit seti konteyneri ayırt edilmelidir"
expected:
  time: { roaring_contains: "log n" }
  space: "1"
concept_tags: [arrays, binary-search]
checklist_extra:
  - "Üst 16 bit için konteyner dizisinde ikili arama yapılmış mı?"
  - "Konteyner türüne göre bit maskesi veya dizi içi arama doğru yönlendirilmiş mi?"
reference_solution_path: private/solutions/c-hard-compact-bitset-roaring.c
hint_ladder:
  1: "Sayının üst 16 bitini alarak sıralı konteyner listesinde ikili arama yapın."
  2: "Konteyner bulunursa alt 16 biti konteynerin türüne göre (dizi ise ikili aramayla, bitmap ise bit testiyle) denetleyin."
  3: "Bu veri yapısı mekanizması 'Roaring bitmap varlık sorgusu (Roaring bitmap membership query)' olarak bilinir."
```

---
### c-hard-diff-myers-algorithm

```yaml
id: c-hard-diff-myers-algorithm
version: 1
language: c
engine: none
difficulty: hard
title: "Düzenleme çizgesinde en kısa yolu bularak metin farkı çıkarma"
prompt: |
  İki dizgi dizisi arasındaki asgari düzenleme yolunu (diff) Myers'ın açgözlü algoritmasıyla köşegenler (k = x - y) üzerinde ilerleyerek bulan `DiffResult *myers_diff(const char **a, size_t n, const char **b, size_t m)` fonksiyonunu yazın. n birinci ve m ikinci dizinin eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(n + m) olmalı"
  - "Düzenleme mesafesi D adım adım artırılmalıdır"
expected:
  time: { myers_diff: "n*m" }
  space: "n + m"
concept_tags: [dynamic-memory, arrays]
checklist_extra:
  - "V dizisi köşegen indeksleri için doğru dengelenmiş mi?"
  - "Eşleşen karakterlerde yılan (snake) hareketiyle köşegen boyunca ücretsiz ilerlenmiş mi?"
reference_solution_path: private/solutions/c-hard-diff-myers-algorithm.c
hint_ladder:
  1: "Her D düzenleme adımı için k = -D'den D'ye kadar köşegenler üzerinde en uzak x noktalarını hesaplayın."
  2: "Metinler eşit olduğu sürece x ve y koordinatlarını çapraz olarak (yılan hareketi) ilerletip hedefe ulaştığınızda yolu geri izleyin."
  3: "Bu algoritma 'Myers metin farkı algoritması (Myers diff algorithm)' olarak bilinir."
```

---
### c-hard-matrix-strassen-multiply

```yaml
id: c-hard-matrix-strassen-multiply
version: 1
language: c
engine: none
difficulty: hard
title: "Matris bloklarını özyinelemeli 7 çarpımla birleştirme"
prompt: |
  n x n boyutundaki (n ikinin kuvveti) iki matrisi klasik 8 çarpım yerine Strassen'in 7 alt çarpım formülüyle çarpan `void strassen_multiply(size_t n, const int *A, const int *B, int *C)` fonksiyonunu yazın. n matris satır ve sütun boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n^2) alt matris toplamlarıyla olmalı"
  - "Ek bellek O(n^2) olmalı"
  - "Taban durumda (n <= 64) standart matris çarpımına geçilmelidir"
expected:
  time: { strassen_multiply: "n^2" }
  space: "n^2"
concept_tags: [arrays, dynamic-memory]
checklist_extra:
  - "7 ara matris (M1...M7) doğru formüllerle hesaplanmış mı?"
  - "Geçici alt matrisler işlem bitiminde sızıntısız serbest bırakılmış mı?"
reference_solution_path: private/solutions/c-hard-matrix-strassen-multiply.c
hint_ladder:
  1: "Matrisleri 4 eşit alt bloğa ayırın."
  2: "Strassen'in 7 ara matrisini (M1-M7) özyinelemeli çarparak hesaplayıp C bloklarını bu ara matrislerin toplamlarıyla oluşturun."
  3: "Bu algoritma 'Strassen hızlı matris çarpımı (Strassen matrix multiplication)' olarak bilinir."
```

---
### c-hard-quadtree-spatial-index

```yaml
id: c-hard-quadtree-spatial-index
version: 1
language: c
engine: none
difficulty: hard
title: "İki boyutlu uzayda aralık sorguları için dördül ağaç bölmesi"
prompt: |
  İki boyutlu noktaları saklayan bir dördül ağaca (Quadtree) nokta ekleyen ve kapasite aşıldığında düğümü 4 eşit alt bölgeye (NW, NE, SW, SE) ayıran `void quadtree_insert(QuadNode *node, Point pt)` fonksiyonunu yazın. n ağaçtaki nokta sayısıdır.
constraints:
  - "Dengeli ağaçta zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(log n) olmalı"
  - "Noktanın hangi kadrana düştüğü doğru belirlenmelidir"
expected:
  time: { quadtree_insert: "log n" }
  space: "log n"
concept_tags: [dynamic-memory, pointers]
checklist_extra:
  - "Düğüm kapasitesi dolduğunda 4 alt çocuk doğru tahsis edilmiş mi?"
  - "Sınır üzerindeki noktalar tutarlı bir kadrana yerleştirilmiş mi?"
reference_solution_path: private/solutions/c-hard-quadtree-spatial-index.c
hint_ladder:
  1: "Düğüm henüz bölünmemişse ve kapasite varsa noktayı doğrudan ekleyin."
  2: "Kapasite dolduğunda düğümü 4 kadrana bölüp mevcut noktaları ve yeni noktayı ilgili çocuk kadranlara dağıtın."
  3: "Bu uzamsal indeksleme yöntemi 'dördül ağaç bölme ve ekleme (quadtree spatial insertion)' olarak bilinir."
```

---
### c-hard-kd-tree-nearest-neighbor

```yaml
id: c-hard-kd-tree-nearest-neighbor
version: 1
language: c
engine: none
difficulty: hard
title: "Çok boyutlu uzayda eksen değiştirerek en yakın komşuyu bulma"
prompt: |
  k-boyutlu uzayda kurulmuş bir k-d ağacında verilen hedef noktaya Öklid mesafesi en küçük olan en yakın komşuyu budama (branch-and-bound) yöntemiyle bulan `const KDPoint *kd_nearest_neighbor(const KDNode *root, KDPoint target)` fonksiyonunu yazın. n ağaçtaki nokta sayısıdır.
constraints:
  - "Ortalama zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(log n) olmalı"
  - "Diğer yarı küre ancak aradaki dik mesafe mevcut en iyi mesafeden küçükse ziyaret edilmelidir"
expected:
  time: { kd_nearest_neighbor: "log n" }
  space: "log n"
concept_tags: [arrays, pointers]
checklist_extra:
  - "Derinliğe göre ayrım ekseni (axis = depth % k) doğru hesaplanmış mı?"
  - "Karşı alt ağaç gereksiz yere taranmayıp budanmış mı?"
reference_solution_path: private/solutions/c-hard-kd-tree-nearest-neighbor.c
hint_ladder:
  1: "Mevcut derinliğin eksenine göre hedefe daha yakın olan alt ağaca öncelikli olarak inin."
  2: "Geri dönüşte hedef ile ayırıcı düzlem arasındaki dik mesafe şu ana kadarki en iyi mesafeden küçükse diğer alt ağacı da araştırın."
  3: "Bu arama algoritması 'k-d ağacında en yakın komşu araması (k-d tree nearest neighbor search)' olarak bilinir."
```

---
### c-hard-consistent-hashing-ring

```yaml
id: c-hard-consistent-hashing-ring
version: 1
language: c
engine: none
difficulty: hard
title: "Sanal düğümlerle dairesel karma halkasında anahtar yönlendirme"
prompt: |
  Dairesel bir karma halkasında sıralı saklanan sanal düğümler arasında verilen anahtarın hash değerini aşan ilk düğümü ikili aramayla (binary search) bulan `size_t consistent_hash_lookup(const HashRing *ring, const char *key)` fonksiyonunu yazın. n halkadaki sanal düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Halka sonuna gelindiğinde ilk düğüme sarma (wrap-around) yapılmalıdır"
expected:
  time: { consistent_hash_lookup: "log n" }
  space: "1"
concept_tags: [hashing, binary-search]
checklist_extra:
  - "Anahtarın 32-bit karma değeri doğru hesaplanmış mı?"
  - "Hash değerinden büyük ilk sanal düğüm ikili aramayla bulunup yoksa sıfırıncı indeks dönülmüş mü?"
reference_solution_path: private/solutions/c-hard-consistent-hashing-ring.c
hint_ladder:
  1: "Anahtarın hash değerini hesaplayıp sıralı sanal düğüm dizisinde ikili aramayla bu değerden büyük ilk düğümü bulun."
  2: "Böyle bir düğüm yoksa halkanın başındaki (0. indeks) ilk düğümü seçin."
  3: "Bu dağıtık mimari yöntemi 'tutarlı karma halkasında arama (consistent hashing ring lookup)' olarak bilinir."
```

---
### c-hard-min-spanning-tree-kruskal

```yaml
id: c-hard-min-spanning-tree-kruskal
version: 1
language: c
engine: none
difficulty: hard
title: "Ayrık küme birliği ile kenar sıralayarak asgari yayılan ağaç bulma"
prompt: |
  Ağırlıklı yönsüz bir çizgenin asgari yayılan ağacını (MST) kenarları ağırlıklarına göre sıralayıp DSU (Ayrık Küme Birliği) ile döngü kontrolü yaparak oluşturan `EdgeList *kruskal_mst(size_t n, Edge *edges, size_t num_edges)` fonksiyonunu yazın. m kenar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(m log m) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Tam olarak n - 1 kenar seçildiğinde sonlanmalıdır"
expected:
  time: { kruskal_mst: "m log m" }
  space: "n"
concept_tags: [arrays, dynamic-memory]
checklist_extra:
  - "Kenarlar qsort ile küçükten büyüğe sıralanmış mı?"
  - "DSU find ile iki ucun aynı kümede olup olmadığı denetlenip döngü engellenmiş mi?"
reference_solution_path: private/solutions/c-hard-min-spanning-tree-kruskal.c
hint_ladder:
  1: "Tüm kenarları ağırlıklarına göre küçükten büyüğe sıralayın."
  2: "Her kenar için uç noktaların aynı kümede olup olmadığını DSU ile denetleyin; farklı kümelerdelerse kenarı ağaca ekleyip kümeleri birleştirin."
  3: "Bu algoritma 'Kruskal asgari yayılan ağaç algoritması (Kruskal's minimum spanning tree)' olarak bilinir."
```

---
### c-hard-bellman-ford-negative-cycles

```yaml
id: c-hard-bellman-ford-negative-cycles
version: 1
language: c
engine: none
difficulty: hard
title: "Ağırlıklı çizgede kenar gevşetme ve negatif döngü tespiti"
prompt: |
  num_nodes düğümlü çizgede kaynaktan tüm düğümlere en kısa mesafeleri hesaplayan ve negatif ağırlıklı döngü varsa false dönen `bool bellman_ford(size_t num_nodes, const Edge *edges, size_t num_edges, size_t src, int *dist)` fonksiyonunu yazın. n düğüm ve m kenar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(n) olmalı"
  - "n - 1 tur gevşetme sonrası n. turda güncelleme olursa negatif döngü vardır"
expected:
  time: { bellman_ford: "n*m" }
  space: "n"
concept_tags: [arrays, edge-cases]
checklist_extra:
  - "Başlangıç mesafeleri sonsuz (INT_MAX) yapılıp kaynak 0 olarak atanmış mı?"
  - "n. gevşetme adımında kısalan bir yol bulunursa negatif döngü saptanmış mı?"
reference_solution_path: private/solutions/c-hard-bellman-ford-negative-cycles.c
hint_ladder:
  1: "Tüm kenarları num_nodes - 1 kez gevşeterek (relax) en kısa yolları güncelleyin."
  2: "Son bir kez daha tüm kenarları tarayın; hala kısalan bir mesafe varsa çizgede negatif ağırlıklı bir döngü mevcuttur."
  3: "Bu algoritma 'Bellman-Ford negatif döngü tespit algoritması (Bellman-Ford algorithm)' olarak bilinir."
```

---
### c-hard-longest-increasing-subsequence-nlogn

```yaml
id: c-hard-longest-increasing-subsequence-nlogn
version: 1
language: c
engine: none
difficulty: hard
title: "Sabır sıralaması ve ikili aramayla en uzun artan alt dizi uzunluğu"
prompt: |
  n elemanlı bir tamsayı dizisindeki kesinlikle artan en uzun alt dizinin uzunluğunu (LIS) kuyruk tablosu ve ikili arama desteğiyle O(n log n) sürede hesaplayan `size_t length_of_lis(const int *arr, size_t n)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n log n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Sabır sıralaması (patience sorting) kuyruk tablosu tutulmalıdır"
expected:
  time: { length_of_lis: "n log n" }
  space: "n"
concept_tags: [binary-search, arrays]
checklist_extra:
  - "Kuyruk dizisinde elemanın gireceği yer ikili arama ile bulunmuş mu?"
  - "Eleman mevcut tüm sonlardan büyükse kuyruk dizisi genişletilmiş mi?"
reference_solution_path: private/solutions/c-hard-longest-increasing-subsequence-nlogn.c
hint_ladder:
  1: "Her uzunluktaki artan alt dizinin bitebileceği minimum son elemanı bir tails dizisinde tutun."
  2: "Dizideki her sayı için tails içinde ikili arama yaparak sayıyı uygun konuma yerleştirin veya en sona ekleyin."
  3: "Bu algoritma 'ikili arama ile en uzun artan alt dizi (longest increasing subsequence with binary search)' olarak bilinir."
```

---
### c-hard-custom-printf-floating-point

```yaml
id: c-hard-custom-printf-floating-point
version: 1
language: c
engine: none
difficulty: hard
title: "Kayan noktalı sayı bitlerini IEEE 754 standardında ondalık dizgiye çevirme"
prompt: |
  64-bit IEEE 754 çift duyarlıklı sayının işaret, üs ve kesir bitlerini ayrıştırarak standart kütüphane fonksiyonu kullanmadan biçimlendirilmiş ondalık dizgiye dönüştüren `size_t format_double_to_string(double val, char *buffer, size_t buf_size)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "NaN, sonsuzluk ve sıfır durumları ele alınmalıdır"
expected:
  time: { format_double_to_string: "1" }
  space: "1"
concept_tags: [strings, memory-safety]
checklist_extra:
  - "NaN ve +/- sonsuzluk özel durumları başta yakalanmış mı?"
  - "Tam kısım ve ondalık kısım tampon taşması olmadan yazılmış mı?"
reference_solution_path: private/solutions/c-hard-custom-printf-floating-point.c
hint_ladder:
  1: "Öncelikle sayının NaN veya sonsuz olup olmadığını bit maskesiyle kontrol edin."
  2: "Tam kısmı 10'a bölerek, kesirli kısmı 10 ile çarparak basamak basamak tampona aktarın."
  3: "Bu dönüşüm mantığı 'kayan noktalı sayıları ondalık metne çevirme (floating-point to string conversion)' olarak bilinir."
```

---
### c-hard-memory-leak-detector-wrapper

```yaml
id: c-hard-memory-leak-detector-wrapper
version: 1
language: c
engine: none
difficulty: hard
title: "Tahsis tablosu ile bellek sızıntılarını ve sarkan göstericileri izleme"
prompt: |
  Tüm bellek tahsislerini (adres, boyut, kaynak dosya adı ve satır numarası) bir karma tablosuna kaydeden ve serbest bırakılmamış blokları listeleyen `void record_allocation(void *ptr, size_t size, const char *file, int line)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "ptr anahtarı karma tablosuna eklenmelidir"
expected:
  time: { record_allocation: "1" }
  space: "1"
concept_tags: [hashing, memory-safety]
checklist_extra:
  - "Adres anahtarı için işaretçi karma fonksiyonu doğru çalışıyor mu?"
  - "Sızıntı raporu oluşturulurken tablo doğru taranmış mı?"
reference_solution_path: private/solutions/c-hard-memory-leak-detector-wrapper.c
hint_ladder:
  1: "Ayrılan her bellek adresini boyut ve satır bilgisiyle birlikte bir dahili karma tablosuna ekleyin."
  2: "Program sonunda tabloda kalan tüm kayıtları sızıntı olarak raporlayın."
  3: "Bu teşhis aracı mekanizması 'özel bellek sızıntısı takipçisi (custom memory leak detector)' olarak bilinir."
```

---
### c-hard-expression-parser-shunting-yard

```yaml
id: c-hard-expression-parser-shunting-yard
version: 1
language: c
engine: none
difficulty: hard
title: "Operatör önceliklerine göre infix ifadeyi postfix ifadeye dönüştürme"
prompt: |
  Parantezler ve öncelik kuralları (+, -, *, /, ^) içeren bir matematiksel infix dizgiyi Dijkstra'nın Shunting-yard algoritması ile postfix (RPN) metnine dönüştüren `char *shunting_yard_parse(const char *infix_expr)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Operatör öncelik tablosu doğru uygulanmalıdır"
expected:
  time: { shunting_yard_parse: "n" }
  space: "n"
concept_tags: [strings, dynamic-memory]
checklist_extra:
  - "Operatör yığınına eleman eklerken öncelik ve birleşme özelliği (sağdan sola / soldan sağa) gözetilmiş mi?"
  - "Parantez uyumsuzluğu yakalanmış mı?"
reference_solution_path: private/solutions/c-hard-expression-parser-shunting-yard.c
hint_ladder:
  1: "Sayıları doğrudan çıkış kuyruğuna yazın."
  2: "Operatör gördükçe yığındaki daha yüksek veya eşit öncelikli operatörleri çıkışa aktarıp yeni operatörü yığına itin."
  3: "Bu algoritma 'Dijkstra Shunting-yard ifadesi ayrıştırma algoritması (Shunting-yard algorithm)' olarak bilinir."
```

---
### c-hard-dynamic-programming-tsp-bitmask

```yaml
id: c-hard-dynamic-programming-tsp-bitmask
version: 1
language: c
engine: none
difficulty: hard
title: "Ziyaret edilen şehirleri bit maskesiyle tutarak en kısa turu hesaplama"
prompt: |
  n şehirli Gezgin Satıcı Problemini (TSP) bit maskeleme ve dinamik programlama (Held-Karp algoritması) ile O(n^2 * 2^n) sürede çözen `int tsp_held_karp(size_t n, const int *dist_matrix)` fonksiyonunu yazın. n <= 16 kabul edilir. n şehir sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n^2) alt problemler tablosuyla olmalı"
  - "Ek bellek O(n) olmalı"
  - "DP tablosu dp[mask][u] şeklinde modellenmelidir"
expected:
  time: { tsp_held_karp: "n^2" }
  space: "n"
concept_tags: [arrays, performance]
checklist_extra:
  - "Maske geçişleri (1 << v) ile ziyaret edilmemiş şehirler doğru taranmış mı?"
  - "Başlangıç şehrine dönüş mesafesi tura eklenmiş mi?"
reference_solution_path: private/solutions/c-hard-dynamic-programming-tsp-bitmask.c
hint_ladder:
  1: "Ziyaret edilen şehirler kümesini tamsayı bit maskesi olarak temsil edin."
  2: "Mevcut şehir ve maske durumundan henüz ziyaret edilmemiş şehirlere geçişlerin minimumunu hesaplayarak DP tablosunu doldurun."
  3: "Bu algoritma 'Held-Karp bit maskeli gezgin satıcı çözümü (Held-Karp TSP algorithm)' olarak bilinir."
```

---
### c-hard-two-phase-locking-sim

```yaml
id: c-hard-two-phase-locking-sim
version: 1
language: c
engine: none
difficulty: hard
title: "Paylaşımlı ve özel kilitlerle iki fazlı kilitleme çatışma denetimi"
prompt: |
  İşlemlerin büyüme (kilit alma) ve küçülme (kilit bırakma) fazlarını sıkı şekilde denetleyen, paylaşımlı (okuma) ve özel (yazma) kilit çatışmalarını yöneten `bool acquire_lock_2pl(Transaction *tx, ResourceID res, LockMode mode)` fonksiyonunu yazın. Küçülme fazında kilit talep edilirse reddedilmelidir.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "2PL kural ihlalleri engellenmelidir"
expected:
  time: { acquire_lock_2pl: "1" }
  space: "1"
concept_tags: [ownership, memory-safety]
checklist_extra:
  - "İşlem küçülme fazındayken (is_shrinking == true) kilit talebi reddedilmiş mi?"
  - "Okuma/yazma kilit uyumluluk matrisi doğru uygulanmış mı?"
reference_solution_path: private/solutions/c-hard-two-phase-locking-sim.c
hint_ladder:
  1: "İşlemin henüz büyüme fazında olduğunu teyit edin; küçülme fazında yeni kilit alınamaz."
  2: "Kaynağın mevcut kilit sahipleriyle talep edilen kilit türünün çakışıp çakışmadığını denetleyin."
  3: "Bu eşzamanlılık protokolü 'iki fazlı kilitleme mekanizması (two-phase locking protocol)' olarak bilinir."
```

---
### c-hard-b-plus-tree-leaf-traversal

```yaml
id: c-hard-b-plus-tree-leaf-traversal
version: 1
language: c
engine: none
difficulty: hard
title: "Aralık sorguları için yaprakları birbirine bağlı B+ Ağacı düğüm bölünmesi"
prompt: |
  B+ Ağacında dolu bir yaprak düğümü ikiye bölen, yeni yaprağı eskisinin sağına çift yönlü bağlayan ve yukarı ebeveyne iletilecek ayrım anahtarını üreten `BPlusNode *bplus_split_leaf(BPlusNode *leaf, int key, void *value)` fonksiyonunu yazın. n yapraktaki eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Yapraklar arası next/prev işaretçileri korunmalıdır"
expected:
  time: { bplus_split_leaf: "log n" }
  space: "1"
concept_tags: [pointers, dynamic-memory]
checklist_extra:
  - "Yeni yaprak tahsis edilip anahtarların üst yarısı oraya aktarılmış mı?"
  - "leaf->next ve new_leaf->prev işaretçileri doğru bağlanmış mı?"
reference_solution_path: private/solutions/c-hard-b-plus-tree-leaf-traversal.c
hint_ladder:
  1: "Yeni bir yaprak düğüm tahsis edip mevcut yapraktaki anahtarların sağ yarısını yeni düğüme taşıyın."
  2: "Yapraklar arası ardışık taramayı korumak için yeni düğümü bağlı liste zincirine ekleyin."
  3: "Bu veritabanı indeks operasyonu 'B+ Ağacı yaprak düğüm bölünmesi (B+ tree leaf splitting)' olarak bilinir."
```

---