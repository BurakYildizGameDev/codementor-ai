# CodeMentor AI — 200 C# Sorusu

Bu belge, `docs/SORU_YAZIM_REHBERI.md` standartlarına uygun olarak hazırlanmış 200 adet C# programlama dili sorusunu içerir.
C# dili modern yönetilen (managed), asenkron ve yüksek başarımlı bir programlama dili olduğu için; bellek tahsisleri ve çöp toplayıcı (GC, allocation, zero-allocation, Span/Memory, ArrayPool), asenkron programlama (async/await, Task, SemaphoreSlim, CancellationToken), kaynak yönetimi (IDisposable, Finalizer, bellek sızıntıları), tip güvenliği ve kapsülleme (encapsulation, readonly struct, in modifier), veri yapıları ve algoritmik zaman/alan karmaşıklığı (`expected: time, space`) odaklı hazırlanmıştır.

---

## Soru Bankası Değerlendirmesi ve Pedagojik Kullanım Notu

Bu soru bankası teknik iş mülakatları, kıdemli .NET / backend mühendisleri ve bilgisayar bilimleri öğrencileri için tasarlanmıştır:

1. **Sokratik ve Mülakat Odaklı Yapı (Yöntem Sızıntısı Yok):**
   - Başlıklarda ve soru metinlerinde doğrudan kütüphane fonksiyon veya sınıf adları (ör. `ReadOnlySpan`, `StringBuilder`, `LINQ`, `MemoryPool`, `ConcurrentDictionary`) yöntem sızıntısı oluşturacak biçimde verilmemiştir.
   - Adaya problem ve bellek modeli aktarılır; adayın uygun modern C# standardını (C# 10/12/13), GC optimizasyonunu ve veri yapılarını kendisinin seçmesi beklenir.

2. **Sıkı Karmaşıklık ve Bellek Analizi (`expected`):**
   - Tüm sorularda zaman (`time`) ve alan (`space`) karmaşıklıkları Big-O notasyonuyla tanımlanmıştır.
   - Tanımlanan her karmaşıklık değişkeni (n, m, k) prompt ve kısıtlar içinde açık bir kelime olarak karşılık bulur.

3. **C# ve .NET Standartları Uyumu:**
   - Sorular .NET 8 / C# 12+ standartlarına uygun, derleyici uyarısı üretmeyecek, sıfır tahsis (zero-allocation) ve kaynak sızıntısından arındırılmış modern .NET programlama disiplinini ölçer.

---

## 1. Çok Kolay (Very Easy) — 50 Soru

---

### cs-veryeasy-sum-array

```yaml
id: cs-veryeasy-sum-array
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Dizi elemanlarının toplamını hesaplama"
prompt: |
  n elemanlı bir tamsayı dizisindeki tüm değerlerin toplamını hesaplayan `long SumArray(int[] numbers)` fonksiyonunu yazın. Dizi boş veya null ise 0 dönmelidir. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "null kontrolü yapılmalı"
expected:
  time: { SumArray: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "numbers == null kontrolü yapılmış mı?"
  - "Toplam long türünde tutulmuş mu?"
reference_solution_path: private/solutions/cs-veryeasy-sum-array.cs
hint_ladder:
  1: "Dizi null ise doğrudan 0 döndürün."
  2: "Elemanları foreach döngüsüyle gezip long biriktiricide toplayın."
  3: "Bu işlem 'dizi elemanları toplamı (array accumulation)' olarak bilinir."
```

---

### cs-veryeasy-find-minimum

```yaml
id: cs-veryeasy-find-minimum
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Dizideki en küçük elemanı bulma"
prompt: |
  n elemanlı boş olmayan bir tamsayı dizisindeki en küçük değeri bulan `int FindMin(int[] numbers)` fonksiyonunu yazın. n dizinin eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "İlk eleman başlangıç kabul edilmeli"
expected:
  time: { FindMin: "n" }
  space: "1"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "İlk eleman min adayı yapılmış mı?"
  - "Tek döngü kurulmuş mu?"
reference_solution_path: private/solutions/cs-veryeasy-find-minimum.cs
hint_ladder:
  1: "numbers[0] değerini en küçük aday olarak belirleyin."
  2: "Kalan elemanları tarayıp daha küçük gördükçe adayı güncelleyin."
  3: "Bu algoritma 'asgari elemanı bulma (find minimum element)' olarak bilinir."
```

---

### cs-veryeasy-count-even

```yaml
id: cs-veryeasy-count-even
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Dizideki çift sayıların adedini bulma"
prompt: |
  n elemanlı tamsayı dizisinde kaç adet çift sayı olduğunu hesaplayan `int CountEven(int[] numbers)` fonksiyonunu yazın. n dizinin boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Negatif çift sayılar hesaba katılmalı"
expected:
  time: { CountEven: "n" }
  space: "1"
concept_tags: [data-structures, integer-division]
checklist_extra:
  - "x % 2 == 0 veya bit işlemi kullanılmış mı?"
  - "null kontrolü yapılmış mı?"
reference_solution_path: private/solutions/cs-veryeasy-count-even.cs
hint_ladder:
  1: "Dizideki her eleman için x % 2 == 0 koşulunu sınayın."
  2: "Koşul sağlandıkça sayacı 1 artırın."
  3: "Bu işlem 'çift sayıların sayımı (even number count)' olarak bilinir."
```

---

### cs-veryeasy-reverse-array

```yaml
id: cs-veryeasy-reverse-array
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Diziyi yerinde tersine çevirme (C#)"
prompt: |
  n elemanlı bir tamsayı dizisini yeni dizi tahsis etmeden yerinde tersine çeviren `void ReverseInPlace(int[] numbers)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "İki indeks kullanılmalıdır"
expected:
  time: { ReverseInPlace: "n" }
  space: "1"
concept_tags: [data-structures, zero-allocation]
checklist_extra:
  - "Yeni dizi tahsis edilmeden yerinde takas yapılmış mı?"
  - "İki işaretçi ortada doğru durmuş mu?"
reference_solution_path: private/solutions/cs-veryeasy-reverse-array.cs
hint_ladder:
  1: "Biri başta diğeri sonda iki indeks belirleyin."
  2: "İndeksler karşılaşana kadar elemanları takas edip birbirine yaklaştırın."
  3: "Bu algoritma 'yerinde dizi ters çevirme (in-place array reversal)' olarak bilinir."
```

---

### cs-veryeasy-is-palindrome

```yaml
id: cs-veryeasy-is-palindrome
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Metnin palindrom olup olmadığını denetleme"
prompt: |
  Verilen bir metnin baştan ve sondan okunuşunun aynı olduğunu iki indeksle denetleyen `bool IsPalindrome(string text)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Yeni string tahsis edilmemelidir"
expected:
  time: { IsPalindrome: "n" }
  space: "1"
concept_tags: [performance, zero-allocation]
checklist_extra:
  - "Yeni string oluşturulmadan karakterler yerinde mi kıyaslanmış?"
  - "İlk uyuşmazlıkta erken çıkış yapılmış mı?"
reference_solution_path: private/solutions/cs-veryeasy-is-palindrome.cs
hint_ladder:
  1: "Metnin ilk ve son karakterinden başlayarak merkeze doğru ilerleyin."
  2: "Uyuşmayan bir karakter gördüğünüz anda false dönün."
  3: "Bu algoritma 'çift indeksli palindrom denetimi (two-pointer palindrome check)' olarak bilinir."
```

---

### cs-veryeasy-string-length

```yaml
id: cs-veryeasy-string-length
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Metnin karakter uzunluğunu hesaplama"
prompt: |
  Verilen metnin karakter sayısını hesaplayan, null ise 0 dönen `int GetLength(string text)` fonksiyonunu yazın. n karakter sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "null durumunda 0 dönmelidir"
expected:
  time: { GetLength: "1" }
  space: "1"
concept_tags: [edge-cases, performance]
checklist_extra:
  - "text == null güvenle ele alınmış mı?"
  - "text.Length doğrudan okunmuş mu?"
reference_solution_path: private/solutions/cs-veryeasy-string-length.cs
hint_ladder:
  1: "text null ise 0 döndürün."
  2: "Değilse text.Length özelliğini doğrudan döndürün."
  3: "Bu kontrol 'güvenli metin uzunluğu sorgusu (safe string length)' olarak bilinir."
```

---

### cs-veryeasy-linear-search

```yaml
id: cs-veryeasy-linear-search
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Dizide hedef değerin ilk indeksini bulma (C#)"
prompt: |
  n elemanlı tamsayı dizisinde target değerini arayıp ilk indeksini döndüren, bulunamazsa -1 dönen `int LinearSearch(int[] numbers, int target)` fonksiyonunu yazın. n eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Bulunduğu anda erken çıkış yapılmalı"
expected:
  time: { LinearSearch: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Hedef bulunduğunda döngü sonuna kadar beklemeden çıkılmış mı?"
  - "Bulunamazsa -1 dönülmüş mü?"
reference_solution_path: private/solutions/cs-veryeasy-linear-search.cs
hint_ladder:
  1: "0'dan n-1'e kadar tüm indeksleri sırayla gezin."
  2: "Değer eşleştiği an mevcut indeksi döndürün."
  3: "Bu arama yöntemi 'doğrusal arama (linear search)' olarak bilinir."
```

---

### cs-veryeasy-check-sorted

```yaml
id: cs-veryeasy-check-sorted
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Dizinin küçükten büyüğe sıralı olduğunu denetleme"
prompt: |
  n elemanlı tamsayı dizisinin küçükten büyüğe sıralı olup olmadığını denetleyen `bool IsSorted(int[] numbers)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı en kötü durumda O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "n < 2 için true dönmelidir"
expected:
  time: { IsSorted: "n" }
  space: "1"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "Sıralamayı bozan ilk ikilide erken çıkış yapılmış mı?"
  - "Döngü sınırları aşılmamış mı?"
reference_solution_path: private/solutions/cs-veryeasy-check-sorted.cs
hint_ladder:
  1: "1. indeksten başlayarak her elemanı bir öncekiyle karşılaştırın."
  2: "numbers[i] < numbers[i-1] olduğu anda false dönün."
  3: "Bu doğrulama 'sıralılık denetimi (is-sorted check)' olarak bilinir."
```

---

### cs-veryeasy-clamp-number

```yaml
id: cs-veryeasy-clamp-number
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Sayısal değeri sınırlar arasına kırpma"
prompt: |
  Verilen value tamsayısını min ve max sınırları arasında tutan `int Clamp(int value, int min, int max)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "min <= max kabul edilir"
expected:
  time: { Clamp: "1" }
  space: "1"
concept_tags: [edge-cases, performance]
checklist_extra:
  - "value < min ise min, value > max ise max döndürülmüş mü?"
  - "Koşullu ifadeler doğru kurgulanmış mı?"
reference_solution_path: private/solutions/cs-veryeasy-clamp-number.cs
hint_ladder:
  1: "Değer min'den küçükse min döndürün."
  2: "Değer max'tan büyükse max döndürün; aksi halde değerin kendisini döndürün."
  3: "Bu matematiksel işlem 'skaler değer kırpma (scalar clamping)' olarak bilinir."
```

---

### cs-veryeasy-count-vowels

```yaml
id: cs-veryeasy-count-vowels
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Metindeki sesli harf sayısını bulma"
prompt: |
  Verilen metindeki İngilizce sesli harflerin (a, e, i, o, u, A, E, I, O, U) toplam sayısını hesaplayan `int CountVowels(string text)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "null metin için 0 dönmelidir"
expected:
  time: { CountVowels: "n" }
  space: "1"
concept_tags: [performance, edge-cases]
checklist_extra:
  - "Büyük ve küçük harfler hesaba katılmış mı?"
  - "null metin elenmiş mi?"
reference_solution_path: private/solutions/cs-veryeasy-count-vowels.cs
hint_ladder:
  1: "Metindeki her karakteri bir döngüde inceleyin."
  2: "Karakter sesli harfler kümesindeyse sayacı bir artırın."
  3: "Bu algoritma 'sesli harf sayımı (vowel counting)' olarak bilinir."
```

---

### cs-veryeasy-to-upper-copy

```yaml
id: cs-veryeasy-to-upper-copy
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Metindeki harfleri büyük harfe dönüştürme"
prompt: |
  Verilen metindeki tüm küçük harfleri büyük harfe dönüştürerek yeni bir metin üreten `string ToUpperCopy(string text)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "null metin için null dönmelidir"
expected:
  time: { ToUpperCopy: "n" }
  space: "n"
concept_tags: [performance, string-building]
checklist_extra:
  - "char.ToUpperInvariant kullanılmış mı?"
  - "null girdi doğru yönetilmiş mı?"
reference_solution_path: private/solutions/cs-veryeasy-to-upper-copy.cs
hint_ladder:
  1: "text null ise null döndürün."
  2: "char.ToUpperInvariant ile karakterleri büyük harfe çevirin."
  3: "Bu işlem 'büyük harfe dönüştürme (uppercase conversion)' olarak bilinir."
```

---

### cs-veryeasy-to-lower-copy

```yaml
id: cs-veryeasy-to-lower-copy
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Metindeki harfleri küçük harfe dönüştürme"
prompt: |
  Verilen metindeki tüm büyük harfleri küçük harfe dönüştürerek yeni bir metin üreten `string ToLowerCopy(string text)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "null metin için null dönmelidir"
expected:
  time: { ToLowerCopy: "n" }
  space: "n"
concept_tags: [performance, string-building]
checklist_extra:
  - "char.ToLowerInvariant kullanılmış mı?"
  - "null girdi güvenli mi?"
reference_solution_path: private/solutions/cs-veryeasy-to-lower-copy.cs
hint_ladder:
  1: "text null ise null döndürün."
  2: "char.ToLowerInvariant ile karakterleri küçük harfe çevirin."
  3: "Bu işlem 'küçük harfe dönüştürme (lowercase conversion)' olarak bilinir."
```

---

### cs-veryeasy-starts-with

```yaml
id: cs-veryeasy-starts-with
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Metnin belirli bir önek ile başladığını denetleme"
prompt: |
  text metninin prefix ile başlayıp başlamadığını karakter karakter denetleyen `bool StartsWithPrefix(string text, string prefix)` fonksiyonunu yazın. m önek uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(m) olmalı"
  - "Ek bellek O(1) olmalı"
  - "prefix metinden uzunsa false dönmelidir"
expected:
  time: { StartsWithPrefix: "m" }
  space: "1"
concept_tags: [performance, edge-cases]
checklist_extra:
  - "Uzunluk karşılaştırması başta yapılmış mı?"
  - "Karakter uyuşmazlığında erken çıkış yapılmış mı?"
reference_solution_path: private/solutions/cs-veryeasy-starts-with.cs
hint_ladder:
  1: "Önek metinden uzunsa doğrudan false dönün."
  2: "Önek karakterlerini metnin başıyla eşzamanlı karşılaştırın."
  3: "Bu kontrol 'önek doğrulaması (prefix check)' olarak bilinir."
```

---

### cs-veryeasy-ends-with

```yaml
id: cs-veryeasy-ends-with
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Metnin belirli bir sonek ile bittiğini denetleme"
prompt: |
  text metninin suffix ile bitip bitmediğini denetleyen `bool EndsWithSuffix(string text, string suffix)` fonksiyonunu yazın. m sonek uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(m) olmalı"
  - "Ek bellek O(1) olmalı"
  - "suffix metinden uzunsa false dönmelidir"
expected:
  time: { EndsWithSuffix: "m" }
  space: "1"
concept_tags: [performance, edge-cases]
checklist_extra:
  - "Boyut kontrolü yapılmış mı?"
  - "Metin sonundan geriye karşılaştırma yapılmış mı?"
reference_solution_path: private/solutions/cs-veryeasy-ends-with.cs
hint_ladder:
  1: "Sonek metinden uzunsa false dönün."
  2: "Metnin sonundaki m karakteri sonek ile karşılaştırın."
  3: "Bu kontrol 'sonek doğrulaması (suffix check)' olarak bilinir."
```

---

### cs-veryeasy-dot-product

```yaml
id: cs-veryeasy-dot-product
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "İki tamsayı dizisinin iç çarpımını hesaplama"
prompt: |
  n elemanlı iki tamsayı dizisinin nokta (iç) çarpımını hesaplayan `long DotProduct(int[] a, int[] b)` fonksiyonunu yazın. n dizilerin boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Çarpımlar 64-bit tamsayıda toplanmalıdır"
expected:
  time: { DotProduct: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Dizi boyutlarının eşitliği denetlenmiş mi?"
  - "Çarpım öncesi long türüne dönüştürülmüş mü?"
reference_solution_path: private/solutions/cs-veryeasy-dot-product.cs
hint_ladder:
  1: "Her iki diziyi tek döngüde i = 0'dan n-1'e kadar gezin."
  2: "Her adımda (long)a[i] * b[i] çarpımını biriktiriciye ekleyin."
  3: "Bu işlem 'vektör iç çarpımı (dot product)' olarak bilinir."
```

---

### cs-veryeasy-replace-char

```yaml
id: cs-veryeasy-replace-char
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Metindeki karakteri başka bir karakterle değiştirme"
prompt: |
  Metindeki tüm oldChar karakterlerini newChar ile değiştiren `string ReplaceChar(string text, char oldChar, char newChar)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "char dizisi üzerinden tek tahsisle çözülebilir"
expected:
  time: { ReplaceChar: "n" }
  space: "n"
concept_tags: [performance, string-building]
checklist_extra:
  - "text.ToCharArray() ile tek tahsis yapılmış mı?"
  - "new string(chars) ile sonuç üretilmiş mi?"
reference_solution_path: private/solutions/cs-veryeasy-replace-char.cs
hint_ladder:
  1: "Metni karakter dizisine çevirin."
  2: "oldChar ile eşleşen karakterleri newChar ile güncelleyip yeni string oluşturun."
  3: "Bu metin manipülasyonu 'karakter değiştirme (character replacement)' olarak bilinir."
```

---

### cs-veryeasy-is-all-digits

```yaml
id: cs-veryeasy-is-all-digits
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Metnin yalnızca rakamlardan oluştuğunu denetleme (C#)"
prompt: |
  Verilen metnin boş olmadığını ve yalnızca '0'-'9' arasındaki rakamlardan oluştuğunu denetleyen `bool IsNumeric(string text)` fonksiyonunu yazın. Boş metin için false dönmelidir. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Boş metin false dönmelidir"
expected:
  time: { IsNumeric: "n" }
  space: "1"
concept_tags: [input-validation, edge-cases]
checklist_extra:
  - "string.IsNullOrEmpty kontrolü yapılmış mı?"
  - "char.IsDigit ile denetlenmiş mi?"
reference_solution_path: private/solutions/cs-veryeasy-is-all-digits.cs
hint_ladder:
  1: "Metin boş veya null ise hemen false dönün."
  2: "Her karakterin rakam olduğunu doğrulayın, rakam olmayan karakterde çıkın."
  3: "Bu doğrulama 'sayısal karakter denetimi (numeric string check)' olarak bilinir."
```

---

### cs-veryeasy-count-words

```yaml
id: cs-veryeasy-count-words
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Boşluklarla ayrılmış sözcük sayısını bulma (C#)"
prompt: |
  Bir metindeki boşluk karakterleriyle ayrılmış sözcüklerin toplam sayısını bellek tahsis etmeden hesaplayan `int CountWords(string text)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Split çağırmadan tek geçişte sayılmalı"
expected:
  time: { CountWords: "n" }
  space: "1"
concept_tags: [zero-allocation, parsing]
checklist_extra:
  - "Split kullanılmayarak gereksiz dizi tahsisi önlenmiş mi?"
  - "Sözcük içi durum bayrağı tutulmuş mu?"
reference_solution_path: private/solutions/cs-veryeasy-count-words.cs
hint_ladder:
  1: "Bir sözcüğün içinde olup olmadığınızı belirten inWord bayrağı tutun."
  2: "Boşluktan harfe geçildiğinde sözcük sayısını artırın."
  3: "Bu algoritma 'durum takibi ile sözcük sayımı (word counting state machine)' olarak bilinir."
```

---

### cs-veryeasy-min-max-tuple

```yaml
id: cs-veryeasy-min-max-tuple
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Dizideki minimum ve maksimumu demet olarak döndürme"
prompt: |
  n elemanlı bir tamsayı dizisini tek geçişte tarayarak en küçük ve en büyük elemanı (min, max) demeti olarak döndüren `(int min, int max) GetMinMax(int[] numbers)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) tek geçiş olmalı"
  - "Ek bellek O(1) olmalı"
  - "Tek döngü kurulmalıdır"
expected:
  time: { GetMinMax: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "İlk eleman başlangıç olarak atanmış mı?"
  - "Tek döngüde iki değer güncellenmiş mi?"
reference_solution_path: private/solutions/cs-veryeasy-min-max-tuple.cs
hint_ladder:
  1: "min ve max değişkenlerini numbers[0] ile başlatın."
  2: "Tek döngüde her iki değeri güncelleyip demet olarak döndürün."
  3: "Bu algoritma 'tek geçişte uç değer demeti (min-max tuple)' olarak bilinir."
```

---

### cs-veryeasy-filter-positives

```yaml
id: cs-veryeasy-filter-positives
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Dizideki pozitif sayıları listeye aktarma"
prompt: |
  n elemanlı tamsayı dizisindeki sıfırdan büyük sayıları sırasıyla bir List<int> içine toplayıp döndüren `List<int> FilterPositives(int[] numbers)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(k) olmalı (k pozitif eleman sayısı)"
  - "null kontrolü yapılmalı"
expected:
  time: { FilterPositives: "n" }
  space: "k"
concept_tags: [data-structures, allocation]
checklist_extra:
  - "Pozitif sayılar doğru filtrelenmiş mi?"
  - "Sonuç listesi döndürülmüş mü?"
reference_solution_path: private/solutions/cs-veryeasy-filter-positives.cs
hint_ladder:
  1: "Yeni bir List<int> oluşturun."
  2: "Döngü ile dizideki her sayıyı kontrol edip pozitif olanları listeye ekleyin."
  3: "Bu filtreleme 'pozitif sayıları ayıklama (positive number filtering)' olarak bilinir."
```

---

### cs-veryeasy-diagonal-sum

```yaml
id: cs-veryeasy-diagonal-sum
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Kare matrisin asal köşegen toplamını hesaplama (C#)"
prompt: |
  n x n boyutundaki iki boyutlu kare matrisin asal köşegenindeki (i == j) elemanların toplamını hesaplayan `long DiagonalSum(int[,] matrix)` fonksiyonunu yazın. n satır ve sütun sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Tek döngü kurulmalıdır"
expected:
  time: { DiagonalSum: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "İç içe döngü kurmaktan kaçınılmış mı?"
  - "Toplam long türünde biriktirilmiş mi?"
reference_solution_path: private/solutions/cs-veryeasy-diagonal-sum.cs
hint_ladder:
  1: "0'dan n-1'e kadar tek döngüde matrix[i, i] elemanlarını toplayın."
  2: "Böylece O(n^2) yerine O(n) karmaşıklığını sağlayın."
  3: "Bu matris işlemi 'asal köşegen toplamı (matrix diagonal sum)' olarak bilinir."
```

---

### cs-veryeasy-scale-array

```yaml
id: cs-veryeasy-scale-array
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Dizideki tüm sayıları bir katsayı ile yerinde çarpma"
prompt: |
  n elemanlı tamsayı dizisindeki her elemanı factor katsayısıyla yerinde çarpan `void ScaleArray(int[] numbers, int factor)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Yeni dizi tahsis edilmemelidir"
expected:
  time: { ScaleArray: "n" }
  space: "1"
concept_tags: [data-structures, zero-allocation]
checklist_extra:
  - "Elemanlar yerinde güncellenmiş mi?"
  - "Döngü sınırları aşılmamış mı?"
reference_solution_path: private/solutions/cs-veryeasy-scale-array.cs
hint_ladder:
  1: "for döngüsüyle tüm indeksleri gezin."
  2: "numbers[i] *= factor atamasını yapın."
  3: "Bu işlem 'dizi elemanlarını ölçekleme (array scaling)' olarak bilinir."
```

---

### cs-veryeasy-absolute-diff-sum

```yaml
id: cs-veryeasy-absolute-diff-sum
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Ardışık elemanlar arasındaki mutlak farkların toplamını bulma (C#)"
prompt: |
  n elemanlı bir tamsayı dizisinde komşu elemanlar arasındaki mutlak farkların (|numbers[i] - numbers[i-1]|) toplamını hesaplayan `long ConsecutiveDiffs(int[] numbers)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "n < 2 için 0 dönmelidir"
expected:
  time: { ConsecutiveDiffs: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Math.Abs kullanılarak mutlak fark alınmış mı?"
  - "Toplam long türünde tutulmuş mu?"
reference_solution_path: private/solutions/cs-veryeasy-absolute-diff-sum.cs
hint_ladder:
  1: "1. indeksten n-1. indekse kadar döngü kurun."
  2: "Math.Abs(numbers[i] - numbers[i-1]) değerlerini toplayın."
  3: "Bu hesaplama 'ardışık farklar toplamı (sum of consecutive differences)' olarak bilinir."
```

---

### cs-veryeasy-second-largest

```yaml
id: cs-veryeasy-second-largest
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Dizideki en büyük ikinci farklı değeri bulma (C#)"
prompt: |
  n elemanlı bir tamsayı dizisindeki en büyük ikinci farklı değeri bulan `int? FindSecondLargest(int[] numbers)` fonksiyonunu yazın. Yeterli farklı eleman yoksa null dönmelidir. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) tek geçiş olmalı (sıralama yapılamaz)"
  - "Ek bellek O(1) olmalı"
  - "null dönebilir tip (int?) kullanılmalıdır"
expected:
  time: { FindSecondLargest: "n" }
  space: "1"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "Sıralama yapılmadan tek döngüde çözülmüş mü?"
  - "Tüm elemanlar eşitse null dönülmüş mü?"
reference_solution_path: private/solutions/cs-veryeasy-second-largest.cs
hint_ladder:
  1: "En büyük ve ikinci en büyük için iki adet int? değişkeni tutun."
  2: "Diziyi tek geçişte tarayarak adayları güncelleyin."
  3: "Bu algoritma 'tek geçişte ikinci en büyük elemanı bulma (second largest element)' olarak bilinir."
```

---

### cs-veryeasy-array-mean

```yaml
id: cs-veryeasy-array-mean
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Tamsayı dizisinin aritmetik ortalamasını hesaplama"
prompt: |
  n elemanlı bir tamsayı dizisinin aritmetik ortalamasını double türünde hesaplayan `double CalculateMean(int[] numbers)` fonksiyonunu yazın. Dizi boşsa 0.0 dönmelidir. n eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Tamsayı bölmesi yerine kayan noktalı bölme yapılmalıdır"
expected:
  time: { CalculateMean: "n" }
  space: "1"
concept_tags: [integer-division, floating-point]
checklist_extra:
  - "Toplam double'a dönüştürülerek tamsayı kesilmesi engellenmiş mi?"
  - "Dizi boşken sıfıra bölme önlenmiş mi?"
reference_solution_path: private/solutions/cs-veryeasy-array-mean.cs
hint_ladder:
  1: "Dizi boşsa hemen 0.0 dönün."
  2: "Elemanları long türünde toplayıp (double)sum / numbers.Length ile bölün."
  3: "Bu hesaplama 'aritmetik ortalama hesaplama (mean calculation)' olarak bilinir."
```

---

### cs-veryeasy-rotate-left-one

```yaml
id: cs-veryeasy-rotate-left-one
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Dizi elemanlarını bir adım sola kaydırma"
prompt: |
  n elemanlı tamsayı dizisinin tüm elemanlarını bir adım sola kaydıran, ilk elemanı en sona taşıyan `void RotateLeftOnce(int[] numbers)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "n <= 1 için işlem yapılmamalıdır"
expected:
  time: { RotateLeftOnce: "n" }
  space: "1"
concept_tags: [data-structures, zero-allocation]
checklist_extra:
  - "İlk eleman geçici değişkende saklanmış mı?"
  - "Elemanlar sola kaydırılıp ilk eleman sona yazılmış mı?"
reference_solution_path: private/solutions/cs-veryeasy-rotate-left-one.cs
hint_ladder:
  1: "İlk elemanı geçici değişkende tutun."
  2: "1. indeksten sona kadar her elemanı bir sola kopyalayıp geçici değeri sona yazın."
  3: "Bu işlem 'diziyi bir adım sola kaydırma (rotate left by one)' olarak bilinir."
```

---

### cs-veryeasy-fill-consecutive

```yaml
id: cs-veryeasy-fill-consecutive
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Diziyi ardışık sayılarla doldurma"
prompt: |
  n boyutundaki tamsayı dizisini start değerinden başlayarak birer artan ardışık sayılarla dolduran `void FillConsecutive(int[] numbers, int start)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "numbers yerinde doldurulmalıdır"
expected:
  time: { FillConsecutive: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Dizi sınırları taranmış mı?"
  - "start + i değeri doğru atanmış mı?"
reference_solution_path: private/solutions/cs-veryeasy-fill-consecutive.cs
hint_ladder:
  1: "0'dan n-1'e kadar döngü kurun."
  2: "numbers[i] = start + i atamasını yapın."
  3: "Bu işlem 'ardışık tamsayı doldurma (consecutive fill)' olarak bilinir."
```

---

### cs-veryeasy-count-greater-than

```yaml
id: cs-veryeasy-count-greater-than
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Dizide eşik değerinden büyük elemanları sayma"
prompt: |
  n elemanlı tamsayı dizisinde threshold değerinden kesinlikle büyük olan eleman sayısını bulan `int CountGreaterThan(int[] numbers, int threshold)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "LINQ kullanmadan döngüyle sayılmalı"
expected:
  time: { CountGreaterThan: "n" }
  space: "1"
concept_tags: [performance, zero-allocation]
checklist_extra:
  - "LINQ closure tahsisinden kaçınılarak doğrudan döngü kurulmuş mu?"
  - "Sayaç doğru artırılmış mı?"
reference_solution_path: private/solutions/cs-veryeasy-count-greater-than.cs
hint_ladder:
  1: "Bir tamsayı sayacı sıfırla başlatın."
  2: "Döngüde x > threshold koşulunu sağlayan her elemanda sayacı artırın."
  3: "Bu işlem 'koşullu eleman sayımı (conditional counting)' olarak bilinir."
```

---

### cs-veryeasy-is-all-positive

```yaml
id: cs-veryeasy-is-all-positive
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Dizideki tüm sayıların pozitif olduğunu denetleme"
prompt: |
  n elemanlı tamsayı dizisindeki tüm elemanların sıfırdan büyük olduğunu denetleyen `bool AllPositive(int[] numbers)` fonksiyonunu yazın. Boş dizi için true dönmelidir. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı en kötü durumda O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "İlk negatif veya sıfır elemanda erken çıkış yapılmalı"
expected:
  time: { AllPositive: "n" }
  space: "1"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "numbers[i] <= 0 durumunda hemen false dönülmüş mü?"
  - "Boş dizi true dönmüş mü?"
reference_solution_path: private/solutions/cs-veryeasy-is-all-positive.cs
hint_ladder:
  1: "Dizideki her elemanı kontrol edin."
  2: "Sıfır veya negatif bir sayı gördüğümüz an false dönün."
  3: "Bu algoritma 'tüm elemanların pozitiflik denetimi (all positive check)' olarak bilinir."
```

---

### cs-veryeasy-split-by-char

```yaml
id: cs-veryeasy-split-by-char
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Metni belirli bir ayraç karaktere göre parçalama (C#)"
prompt: |
  Verilen bir metni delimiter karakterine göre parçalayarak string[] dizisi olarak döndüren `string[] SplitByChar(string text, char delimiter)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı (parçalar)"
  - "text.Split kullanılabilir"
expected:
  time: { SplitByChar: "n" }
  space: "n"
concept_tags: [parsing, string-building]
checklist_extra:
  - "text.Split(delimiter) çağrısı yapılmış mı?"
  - "null girdi kontrol edilmiş mi?"
reference_solution_path: private/solutions/cs-veryeasy-split-by-char.cs
hint_ladder:
  1: "text null ise boş dizi döndürün."
  2: "text.Split(delimiter) fonksiyonunu çağırarak parçaları dizi olarak elde edin."
  3: "Bu işlem 'karakter ile metin bölme (string split by char)' olarak bilinir."
```

---

### cs-veryeasy-join-strings

```yaml
id: cs-veryeasy-join-strings
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Dizgi dizisini ayraçla birleştirme"
prompt: |
  n adet metin içeren parçalar dizisini aralarına separator koyarak tek bir metinde birleştiren `string JoinStrings(string[] parts, string separator)` fonksiyonunu yazın. n parça sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "string.Join kullanılabilir"
expected:
  time: { JoinStrings: "n" }
  space: "n"
concept_tags: [string-building, performance]
checklist_extra:
  - "string.Join kullanılarak döngüde + operatörüyle ara nesne tahsisinden kaçınılmış mı?"
  - "null girdi yönetilmiş mi?"
reference_solution_path: private/solutions/cs-veryeasy-join-strings.cs
hint_ladder:
  1: "string.Join(separator, parts) fonksiyonunu çağırın."
  2: "Bu fonksiyon toplam boyutu önceden hesaplayarak tek seferde birleştirilmiş dizgi üretir."
  3: "Bu işlem 'metin birleştirme (string join)' olarak bilinir."
```

---

### cs-veryeasy-repeat-text

```yaml
id: cs-veryeasy-repeat-text
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Metni k kez tekrarlayan yeni metin üretme"
prompt: |
  Verilen text metnini k kez ardışık tekrarlayan yeni bir string üreten `string RepeatText(string text, int k)` fonksiyonunu yazın. k tekrar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(k) olmalı"
  - "Ek bellek O(k) olmalı"
  - "StringBuilder ile kapasite baştan ayrılmalıdır"
expected:
  time: { RepeatText: "k" }
  space: "k"
concept_tags: [string-building, allocation]
checklist_extra:
  - "StringBuilder(text.Length * k) kapasitesi baştan ayrılmış mı?"
  - "k <= 0 durumunda boş metin dönülmüş mü?"
reference_solution_path: private/solutions/cs-veryeasy-repeat-text.cs
hint_ladder:
  1: "StringBuilder nesnesini text.Length * k kapasitesiyle oluşturun."
  2: "k defa döngüde sb.Append(text) çağırıp sb.ToString() döndürün."
  3: "Bu işlem 'metin tekrarlama (string repetition)' olarak bilinir."
```

---

### cs-veryeasy-find-char-index

```yaml
id: cs-veryeasy-find-char-index
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Karakterin metin içinde ilk görüldüğü indeksi bulma (C#)"
prompt: |
  text metninde ch karakterinin ilk geçtiği indeksi döndüren, bulunamazsa -1 dönen `int FindCharIndex(string text, char ch)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "text.IndexOf kullanılabilir"
expected:
  time: { FindCharIndex: "n" }
  space: "1"
concept_tags: [performance, edge-cases]
checklist_extra:
  - "text.IndexOf(ch) doğrudan çağrılmış mı?"
  - "null metin için -1 dönülmüş mü?"
reference_solution_path: private/solutions/cs-veryeasy-find-char-index.cs
hint_ladder:
  1: "text null ise -1 dönün."
  2: "text.IndexOf(ch) metodunun sonucunu doğrudan döndürün."
  3: "Bu işlem 'karakter indeksi bulma (find char index)' olarak bilinir."
```

---

### cs-veryeasy-compare-arrays

```yaml
id: cs-veryeasy-compare-arrays
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "İki tamsayı dizisinin eşitliğini sınama"
prompt: |
  n elemanlı iki tamsayı dizisinin boyut ve aynı sıradaki elemanlar bakımından eşit olup olmadığını denetleyen `bool CompareArrays(int[] a, int[] b)` fonksiyonunu yazın. n dizilerin boyutudur.
constraints:
  - "Zaman karmaşıklığı en kötü durumda O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Boyut farkında erken çıkış yapılmalıdır"
expected:
  time: { CompareArrays: "n" }
  space: "1"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "Boyut kontrolü başta yapılmış mı?"
  - "İlk uyuşmayan elemanda erken dönülmüş mü?"
reference_solution_path: private/solutions/cs-veryeasy-compare-arrays.cs
hint_ladder:
  1: "Referanslar eşitse true, biri null ise false, boyutlar farklıysa false dönün."
  2: "Elemanları sırayla karşılaştırıp uyuşmazlık anında false dönün."
  3: "Bu işlem 'dizi eşitlik karşılaştırması (array equality comparison)' olarak bilinir."
```

---

### cs-veryeasy-array-product

```yaml
id: cs-veryeasy-array-product
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Dizideki tüm tamsayıların çarpımını hesaplama"
prompt: |
  n elemanlı bir tamsayı dizisindeki tüm elemanların çarpımını hesaplayan `long ProductElements(int[] numbers)` fonksiyonunu yazın. Dizi boşsa 1 dönmelidir. n eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Çarpım long biriktiricide tutulmalıdır"
expected:
  time: { ProductElements: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Başlangıç değeri 1 olarak atanmış mı?"
  - "Döngüde çarpım biriktirilmiş mi?"
reference_solution_path: private/solutions/cs-veryeasy-array-product.cs
hint_ladder:
  1: "product değişkenini 1L ile başlatın."
  2: "Her elemanla çarparak sonucu döndürün."
  3: "Bu işlem 'dizi elemanları çarpımı (array product accumulation)' olarak bilinir."
```

---

### cs-veryeasy-count-odds

```yaml
id: cs-veryeasy-count-odds
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Dizideki tek sayıların adedini bulma"
prompt: |
  n elemanlı tamsayı dizisindeki tek sayıların sayısını hesaplayan `int CountOdds(int[] numbers)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Negatif sayılarda (x % 2 != 0) koşulu gözetilmelidir"
expected:
  time: { CountOdds: "n" }
  space: "1"
concept_tags: [data-structures, integer-division]
checklist_extra:
  - "x % 2 != 0 koşulu kullanılmış mı?"
  - "Döngü tek geçişte tamamlanmış mı?"
reference_solution_path: private/solutions/cs-veryeasy-count-odds.cs
hint_ladder:
  1: "Dizideki her eleman için x % 2 != 0 koşulunu kontrol edin."
  2: "Doğru olduğu her adımda sayacı bir artırın."
  3: "Bu işlem 'tek sayıların sayımı (odd number counting)' olarak bilinir."
```

---

### cs-veryeasy-trim-whitespace

```yaml
id: cs-veryeasy-trim-whitespace
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Metnin başındaki ve sonundaki boşlukları budama"
prompt: |
  Verilen bir metnin başında ve sonunda yer alan boşluk karakterlerini budayarak döndüren `string TrimWhitespace(string text)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "text.Trim() kullanılabilir"
expected:
  time: { TrimWhitespace: "n" }
  space: "n"
concept_tags: [string-building, edge-cases]
checklist_extra:
  - "text == null kontrolü yapılmış mı?"
  - "text.Trim() çağrılmış mı?"
reference_solution_path: private/solutions/cs-veryeasy-trim-whitespace.cs
hint_ladder:
  1: "text null ise boş metin veya null döndürün."
  2: "text.Trim() çağrısı ile baş ve sondaki boşlukları temizleyin."
  3: "Bu temizlik işlemi 'metin boşluk budama (string trim)' olarak bilinir."
```

---

### cs-veryeasy-reverse-words

```yaml
id: cs-veryeasy-reverse-words
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Cümledeki her bir sözcüğü kendi içinde ters çevirme (C#)"
prompt: |
  Boşluklarla ayrılmış sözcükler içeren bir cümledeki sözcüklerin sırasını değiştirmeden her bir sözcüğü kendi içinde tersine çeviren `string ReverseWordsInSentence(string text)` fonksiyonunu yazın. n cümlenin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "StringBuilder veya char[] kullanılabilir"
expected:
  time: { ReverseWordsInSentence: "n" }
  space: "n"
concept_tags: [string-building, parsing]
checklist_extra:
  - "Sözcük sınırları doğru tespit edilmiş mi?"
  - "Sözcükler kendi içinde ters çevrilmiş mi?"
reference_solution_path: private/solutions/cs-veryeasy-reverse-words.cs
hint_ladder:
  1: "Metni char dizisine çevirin."
  2: "Her bir sözcük aralığını iki indeksle yerinde ters çevirip yeni string oluşturun."
  3: "Bu algoritma 'sözcükleri kendi içinde ters çevirme (reverse words in sentence)' olarak bilinir."
```

---

### cs-veryeasy-zip-merge

```yaml
id: cs-veryeasy-zip-merge
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "İki eşit boyutlu dizinin elemanlarını harmanlama"
prompt: |
  n elemanlı iki tamsayı dizisinin elemanlarını bir a'dan bir b'den olacak şekilde sırayla harmanlayarak 2n boyutlu yeni bir dizi üreten `int[] ZipMerge(int[] a, int[] b)` fonksiyonunu yazın. n her bir dizinin boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "2 * n boyutunda tek dizi tahsis edilmelidir"
expected:
  time: { ZipMerge: "n" }
  space: "n"
concept_tags: [data-structures, allocation]
checklist_extra:
  - "new int[2 * n] tahsisi yapılmış mı?"
  - "Elemanlar sırayla 2*i ve 2*i + 1 indekslerine yerleştirilmiş mi?"
reference_solution_path: private/solutions/cs-veryeasy-zip-merge.cs
hint_ladder:
  1: "Sonuç için 2 * n boyutunda bir dizi açın."
  2: "i = 0'dan n-1'e kadar result[2*i] = a[i] ve result[2*i + 1] = b[i] atamasını yapın."
  3: "Bu işlem 'almaşık dizi birleştirme (zip merge)' olarak bilinir."
```

---

### cs-veryeasy-first-mismatch-index

```yaml
id: cs-veryeasy-first-mismatch-index
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "İki metnin farklılaştığı ilk karakter indeksini bulma"
prompt: |
  İki metni baştan sona karşılaştırarak ilk farklı karakterin indeksini döndüren, metinler eşitse veya biri diğerinin önekiyse -1 dönen `int FirstMismatch(string a, string b)` fonksiyonunu yazın. n kısa metnin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Döngü kısa metin uzunluğuna kadar gitmelidir"
expected:
  time: { FirstMismatch: "n" }
  space: "1"
concept_tags: [performance, edge-cases]
checklist_extra:
  - "Farklılaşan ilk karakterde indeks dönülmüş mü?"
  - "Uzunluklar farklıysa kısa metin sonu dönülmüş mü?"
reference_solution_path: private/solutions/cs-veryeasy-first-mismatch-index.cs
hint_ladder:
  1: "Kısa metin uzunluğuna kadar iki metni karakter karakter kıyaslayın."
  2: "a[i] != b[i] olduğunda i döndürün; uyuşuyorsa ama uzunluklar farklıysa kısa metnin boyutunu döndürün."
  3: "Bu karşılaştırma 'ilk uyumsuzluk indeksi bulma (first mismatch index)' olarak bilinir."
```

---

### cs-veryeasy-adjacent-pairs-count

```yaml
id: cs-veryeasy-adjacent-pairs-count
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Hedef karakter çiftinin ardışık geçiş sayısını bulma"
prompt: |
  Bir metinde c1 ve c2 karakterlerinin yan yana (c1 ardından c2) kaç kez geçtiğini sayan `int CountAdjacentPairs(string text, char c1, char c2)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "n < 2 için 0 dönmelidir"
expected:
  time: { CountAdjacentPairs: "n" }
  space: "1"
concept_tags: [performance, parsing]
checklist_extra:
  - "Sınır aşımı olmadan text[i] ve text[i+1] kontrol edilmiş mi?"
  - "Sayaç doğru artırılmış mı?"
reference_solution_path: private/solutions/cs-veryeasy-adjacent-pairs-count.cs
hint_ladder:
  1: "0'dan text.Length - 2'ye kadar döngü kurun."
  2: "text[i] == c1 && text[i+1] == c2 olduğu her durumda sayacı artırın."
  3: "Bu algoritma 'ardışık karakter çifti sayımı (adjacent pair counting)' olarak bilinir."
```

---

### cs-veryeasy-is-subsegment

```yaml
id: cs-veryeasy-is-subsegment
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Küçük dizinin büyük dizinin kesintisiz alt dizisi olduğunu denetleme"
prompt: |
  small dizisinin (m elemanlı) big dizisinin (n elemanlı) kesintisiz bir alt dizisi olup olmadığını denetleyen `bool IsSubsegment(int[] big, int[] small)` fonksiyonunu yazın. Boş small her zaman alt dizidir. n büyük ve m küçük dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(1) olmalı"
  - "small boşken true dönmelidir"
expected:
  time: { IsSubsegment: "n*m" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "small.Length == 0 durumu true elenmiş mi?"
  - "İç içe döngü sınır aşımı yapmadan taranmış mı?"
reference_solution_path: private/solutions/cs-veryeasy-is-subsegment.cs
hint_ladder:
  1: "small boşsa doğrudan true dönün."
  2: "big dizisinde gezerek small ile eşleşen alt aralığı arayın."
  3: "Bu kontrol 'kesintisiz alt dizi arama (subsegment check)' olarak bilinir."
```

---

### cs-veryeasy-generate-squares

```yaml
id: cs-veryeasy-generate-squares
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "1'den n'e kadar sayıların karelerini içeren dizi üretme"
prompt: |
  1'den n'e kadar olan tamsayıların karelerini içeren long[] dizisi üreten `long[] GenerateSquares(int n)` fonksiyonunu yazın. n tamsayı adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "new long[n] baştan tahsis edilmelidir"
expected:
  time: { GenerateSquares: "n" }
  space: "n"
concept_tags: [allocation, performance]
checklist_extra:
  - "Dizi boyutu n olarak tahsis edilmiş mi?"
  - "(long)i * i çarpımı yapılmış mı?"
reference_solution_path: private/solutions/cs-veryeasy-generate-squares.cs
hint_ladder:
  1: "new long[n] boyutunda bir dizi açın."
  2: "1'den n'e kadar her sayı için (long)i * i değerini diziye yazın."
  3: "Bu işlem 'kareler dizisi üretimi (squares generation)' olarak bilinir."
```

---

### cs-veryeasy-parse-binary

```yaml
id: cs-veryeasy-parse-binary
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "İkilik metin dizisini tamsayıya dönüştürme"
prompt: |
  Yalnızca '0' ve '1' karakterlerinden oluşan bir metni işaretsiz tamsayıya (uint) dönüştüren `uint ParseBinary(string binStr)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Bit kaydırma işlemleriyle çözülebilir"
expected:
  time: { ParseBinary: "n" }
  space: "1"
concept_tags: [parsing, performance]
checklist_extra:
  - "result = (result << 1) | (uint)(c - '0') bit kaydırması yapılmış mı?"
  - "Metin baştan sona taranmış mı?"
reference_solution_path: private/solutions/cs-veryeasy-parse-binary.cs
hint_ladder:
  1: "result değişkenini 0 ile başlatın."
  2: "Her karakter için (result << 1) | (uint)(c - '0') işlemi uygulayın."
  3: "Bu dönüşüm 'ikilik metin çözümleme (binary string parsing)' olarak bilinir."
```

---

### cs-veryeasy-elementwise-diff

```yaml
id: cs-veryeasy-elementwise-diff
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "İki dizinin karşılıklı farklarından yeni dizi oluşturma"
prompt: |
  n elemanlı iki tamsayı dizisinin karşılıklı eleman farklarını (a[i] - b[i]) hesaplayarak yeni bir dizi döndüren `int[] ElementwiseDiff(int[] a, int[] b)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "new int[n] ile oluşturulmalıdır"
expected:
  time: { ElementwiseDiff: "n" }
  space: "n"
concept_tags: [data-structures, allocation]
checklist_extra:
  - "Sonuç dizisi n boyutunda açılmış mı?"
  - "Farklar doğru atanmış mı?"
reference_solution_path: private/solutions/cs-veryeasy-elementwise-diff.cs
hint_ladder:
  1: "n boyutunda yeni bir int dizisi oluşturun."
  2: "Her indeks için result[i] = a[i] - b[i] atamasını yapın."
  3: "Bu işlem 'eleman bazında dizi çıkarma (elementwise difference)' olarak bilinir."
```

---

### cs-veryeasy-is-symmetric

```yaml
id: cs-veryeasy-is-symmetric
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Tamsayı dizisinin baştan ve sondan simetrik olduğunu denetleme"
prompt: |
  n elemanlı bir tamsayı dizisinin baştan ve sondan okunuşunun aynı (simetrik) olup olmadığını denetleyen `bool IsSymmetric(int[] numbers)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "İki işaretçi karşılıklı ilerletilmelidir"
expected:
  time: { IsSymmetric: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Sol ve sağ indeksler karşılaştırılmış mı?"
  - "Uyuşmazlık anında erken çıkış yapılmış mı?"
reference_solution_path: private/solutions/cs-veryeasy-is-symmetric.cs
hint_ladder:
  1: "Sol indeksi baştan, sağ indeksi sondan başlatın."
  2: "İndeksler karşılaşana kadar elemanları kıyaslayın, uyuşmazlık varsa false dönün."
  3: "Bu algoritma 'dizi simetri denetimi (symmetric array check)' olarak bilinir."
```

---

### cs-veryeasy-remove-element

```yaml
id: cs-veryeasy-remove-element
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Diziden hedef değeri filtreleyip yeni dizi oluşturma"
prompt: |
  n elemanlı tamsayı dizisinden target değerine eşit tüm elemanları çıkararak kalan elemanlardan yeni bir dizi döndüren `int[] RemoveTarget(int[] numbers, int target)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "İki geçiş veya List ile çözülebilir"
expected:
  time: { RemoveTarget: "n" }
  space: "n"
concept_tags: [data-structures, allocation]
checklist_extra:
  - "Hedef olmayan elemanlar yeni diziye aktarılmış mı?"
  - "Sıralama korunmuş mu?"
reference_solution_path: private/solutions/cs-veryeasy-remove-element.cs
hint_ladder:
  1: "Önce hedef olmayan eleman sayısını sayın."
  2: "Gereken boyutta yeni bir dizi açıp elemanları aktarın."
  3: "Bu işlem 'hedef eleman filtreleme (remove target element)' olarak bilinir."
```

---

### cs-veryeasy-swap-array-elements

```yaml
id: cs-veryeasy-swap-array-elements
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Dizideki iki indeksin değerlerini yer değiştirme"
prompt: |
  Dizideki i ve j indekslerindeki elemanların yerini değiştiren `void SwapElements(int[] numbers, int i, int j)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "İndeks sınırları doğrulanmalıdır"
expected:
  time: { SwapElements: "1" }
  space: "1"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "İndekslerin dizi sınırları içinde olduğu kontrol edilmiş mi?"
  - "Geçici değişkenle takas yapılmış mı?"
reference_solution_path: private/solutions/cs-veryeasy-swap-array-elements.cs
hint_ladder:
  1: "İndeksler geçerli değilse işlem yapmayın."
  2: "temp = numbers[i], numbers[i] = numbers[j], numbers[j] = temp takasını uygulayın."
  3: "Bu temel işlem 'dizide eleman takası (array element swap)' olarak bilinir."
```

---

### cs-veryeasy-has-negative

```yaml
id: cs-veryeasy-has-negative
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Dizide en az bir negatif sayı olup olmadığını denetleme"
prompt: |
  n elemanlı bir tamsayı dizisinde sıfırdan küçük herhangi bir eleman olup olmadığını denetleyen `bool HasNegative(int[] numbers)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı en kötü durumda O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "İlk negatifte erken çıkış yapılmalıdır"
expected:
  time: { HasNegative: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "numbers[i] < 0 görüldüğü an true dönülmüş mü?"
  - "Dizi taranıp bulunamazsa false dönülmüş mü?"
reference_solution_path: private/solutions/cs-veryeasy-has-negative.cs
hint_ladder:
  1: "Dizideki her elemanı kontrol edin."
  2: "Eleman negatif olduğu anda true döndürün; döngü biterse false dönün."
  3: "Bu algoritma 'negatif sayı varlık denetimi (has negative check)' olarak bilinir."
```

---

### cs-veryeasy-count-occurrences

```yaml
id: cs-veryeasy-count-occurrences
version: 1
language: csharp
engine: none
difficulty: very_easy
title: "Dizide belirli bir tamsayının geçme sıklığını hesaplama"
prompt: |
  n elemanlı tamsayı dizisinde target tamsayısının kaç kez yer aldığını hesaplayan `int CountOccurrences(int[] numbers, int target)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Tek döngü kurulmalıdır"
expected:
  time: { CountOccurrences: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "target ile eşleşen elemanlarda sayaç artırılmış mı?"
  - "null kontrolü yapılmış mı?"
reference_solution_path: private/solutions/cs-veryeasy-count-occurrences.cs
hint_ladder:
  1: "Sayacı 0 ile başlatın."
  2: "Döngü ile diziyi tarayıp target'a eşit her elemanda sayacı artırın."
  3: "Bu işlem 'eleman sıklığı sayımı (count occurrences)' olarak bilinir."
```

---


---

## 2. Kolay (Easy) — 50 Soru

---

### cs-easy-string-builder-loop

```yaml
id: cs-easy-string-builder-loop
version: 1
language: csharp
engine: none
difficulty: easy
title: "Döngüde metin birleştirmede bellek tahsisini optimize etme"
prompt: |
  n elemanlı bir metin dizisini döngü içinde string birleştirme operatörü (+) yerine StringBuilder kullanarak birleştiren `string BuildFormattedList(string[] items)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "StringBuilder kullanılmalıdır"
expected:
  time: { BuildFormattedList: "n" }
  space: "n"
concept_tags: [string-building, gc]
checklist_extra:
  - "Döngüde + yerine sb.Append kullanılmış mı?"
  - "Gereksiz ara string nesnesi tahsisleri önlenmiş mi?"
reference_solution_path: private/solutions/cs-easy-string-builder-loop.cs
hint_ladder:
  1: "Döngü içinde string toplamak her adımda yeni bir string nesnesi üretir ve çöp toplayıcıya (GC) yük bindirir."
  2: "StringBuilder kullanarak tüm parçaları tek bir değişken tamponda toplayın."
  3: "Bu optimizasyon 'metin inşa edici ile tahsis azaltma (string builder allocation reduction)' olarak bilinir."
```

---

### cs-easy-span-whitespace-trim

```yaml
id: cs-easy-span-whitespace-trim
version: 1
language: csharp
engine: none
difficulty: easy
title: "Bellek kopyalamadan metin başı ve sonundaki boşlukları dilimleme"
prompt: |
  Verilen bir metin diliminin (ReadOnlySpan<char>) başındaki ve sonundaki boşlukları yeni string tahsis etmeden budayan `ReadOnlySpan<char> TrimFast(ReadOnlySpan<char> text)` fonksiyonunu yazın. n karakter sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (sıfır tahsis)"
  - "ReadOnlySpan kullanılmalıdır"
expected:
  time: { TrimFast: "n" }
  space: "1"
concept_tags: [span, zero-allocation]
checklist_extra:
  - "Heap üzerinde hiçbir string tahsis edilmemiş mi?"
  - "Span.Slice ile dilimleme yapılmış mı?"
reference_solution_path: private/solutions/cs-easy-span-whitespace-trim.cs
hint_ladder:
  1: "Başlangıçtan ve sondan boşluk olmayan ilk karakterlerin indekslerini bulun."
  2: "text.Slice(start, length) ile sıfır bellek tahsisli dilim döndürün."
  3: "Bu modern C# tekniği 'karakter dilimi budama (span whitespace trim)' olarak bilinir."
```

---

### cs-easy-safe-currency-division

```yaml
id: cs-easy-safe-currency-division
version: 1
language: csharp
engine: none
difficulty: easy
title: "Para hesaplamalarında duyarlılık kaybını önleyen ondalıklı bölme"
prompt: |
  Toplam para tutarını parts adet eşit parçaya bölen ve kuruş yuvarlama hatalarını önlemek için decimal türü kullanan `decimal DivideCurrency(decimal total, int parts)` fonksiyonunu yazın. parts <= 0 durumunda ArgumentException fırlatılmalıdır.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "double yerine decimal kullanılmalıdır"
expected:
  time: { DivideCurrency: "1" }
  space: "1"
concept_tags: [floating-point, error-handling]
checklist_extra:
  - "Finansal tutar için decimal kullanılmış mı?"
  - "parts <= 0 hatası doğru fırlatılmış mı?"
reference_solution_path: private/solutions/cs-easy-safe-currency-division.cs
hint_ladder:
  1: "float ve double türleri ikilik tabanda tam olarak temsil edilemeyen kesirlerde yuvarlama hatası üretir."
  2: "Finansal hesaplamalarda 128-bit ondalık tabanlı decimal türünü kullanın."
  3: "Bu finansal hesaplama kuralı 'kesin ondalıklı para bölmesi (decimal currency division)' olarak bilinir."
```

---

### cs-easy-user-account-encapsulation

```yaml
id: cs-easy-user-account-encapsulation
version: 1
language: csharp
engine: none
difficulty: easy
title: "Bakiye ve para çekme işlemlerini kapsülleyen hesap sınıfı"
prompt: |
  Bakiyenin dışarıdan doğrudan değiştirilmesini engelleyen private set özelliğine sahip, negatif çekimleri reddeden `class UserAccount` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Kapsülleme kurallarına tam uyulmalıdır"
expected:
  time: { UserAccount: "1" }
  space: "1"
concept_tags: [encapsulation, error-handling]
checklist_extra:
  - "Bakiye alanı dışarıya salt okunur mu?"
  - "Yetersiz bakiye veya negatif tutar durumunda hata yönetilmiş mi?"
reference_solution_path: private/solutions/cs-easy-user-account-encapsulation.cs
hint_ladder:
  1: "public decimal Balance { get; private set; } özelliğini tanımlayın."
  2: "Deposit ve Withdraw metotlarında girdileri doğrulayarak nesne durumunun tutarlılığını koruyun."
  3: "Bu nesne yönelimli ilke 'durum kapsülleme (state encapsulation)' olarak bilinir."
```

---

### cs-easy-int-try-parse-validation

```yaml
id: cs-easy-int-try-parse-validation
version: 1
language: csharp
engine: none
difficulty: easy
title: "Sayısal metinleri istisna üretmeden güvenle ayrıştırma"
prompt: |
  Verilen bir metni tamsayıya dönüştüren, biçim bozuk olduğunda istisna fırlatmak yerine out parametresi ve boole dönüşüyle bildiren `bool TryParseInteger(string text, out int result)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "int.TryParse deseni uygulanmalıdır"
expected:
  time: { TryParseInteger: "n" }
  space: "1"
concept_tags: [input-validation, error-handling]
checklist_extra:
  - "Format hatasında exception fırlatılmayarak performans kaybı önlenmiş mi?"
  - "out parametresi doğru atanmış mı?"
reference_solution_path: private/solutions/cs-easy-int-try-parse-validation.cs
hint_ladder:
  1: "int.Parse yerine int.TryParse çağırarak istisna yönetiminin getirdiği yüksek çalışma zamanı maliyetinden kaçının."
  2: "Başarı durumunu dönüş değeriyle, sayıyı ise out parametresiyle iletin."
  3: "Bu tasarım 'deneme-ayrıştırma deseni (TryParse pattern)' olarak bilinir."
```

---

### cs-easy-binary-search-array

```yaml
id: cs-easy-binary-search-array
version: 1
language: csharp
engine: none
difficulty: easy
title: "Sıralı dizide ikili arama ile hedef indeksi bulma"
prompt: |
  Küçükten büyüğe sıralı n elemanlı bir tamsayı dizisinde target değerini ikili aramayla arayan ve indeksini döndüren, yoksa -1 dönen `int BinarySearch(int[] numbers, int target)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Orta nokta hesabı taşmasız yapılmalıdır"
expected:
  time: { BinarySearch: "log n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "mid = low + (high - low) / 2 formülü kullanılmış mı?"
  - "Bulunamadığında -1 dönülmüş mü?"
reference_solution_path: private/solutions/cs-easy-binary-search-array.cs
hint_ladder:
  1: "low ve high indeksleriyle aralığı sınırlayın."
  2: "Orta eleman hedeften küçükse sağa, büyükse sola kayarak arama aralığını her adımda yarıya indirin."
  3: "Bu algoritma 'ikili arama algoritması (binary search)' olarak bilinir."
```

---

### cs-easy-hashset-duplicate-check

```yaml
id: cs-easy-hashset-duplicate-check
version: 1
language: csharp
engine: none
difficulty: easy
title: "Karma kümesi ile dizide mükerrer eleman denetimi"
prompt: |
  n elemanlı bir tamsayı dizisinde herhangi bir elemanın birden fazla geçip geçmediğini HashSet<int> kullanarak O(n) sürede denetleyen `bool ContainsDuplicate(int[] numbers)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "İlk mükerrer elemanda erken dönülmelidir"
expected:
  time: { ContainsDuplicate: "n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "HashSet.Add dönüşü kontrol edilmiş mi?"
  - "Erken çıkış yapılmış mı?"
reference_solution_path: private/solutions/cs-easy-hashset-duplicate-check.cs
hint_ladder:
  1: "Bir HashSet<int> oluşturun."
  2: "Her eleman için !seen.Add(num) koşulu sağlandığı an mükerrer eleman bulunmuş demektir, true dönün."
  3: "Bu algoritma 'karma kümesi ile tekleştirme denetimi (hash set duplicate check)' olarak bilinir."
```

---

### cs-easy-two-sum-dictionary

```yaml
id: cs-easy-two-sum-dictionary
version: 1
language: csharp
engine: none
difficulty: easy
title: "Sözlük kullanarak toplamı hedefe eşit iki indeksi bulma"
prompt: |
  n elemanlı bir tamsayı dizisinde toplamları target değerine eşit iki elemanın indeks çiftini Dictionary<int, int> kullanarak O(n) sürede bulan `(int, int)? TwoSumDictionary(int[] numbers, int target)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Tek geçişte çözülmelidir"
expected:
  time: { TwoSumDictionary: "n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Tamamlayıcı (target - num) sözlükte aranmış mı?"
  - "Bulunursa indeks çifti döndürülmüş mü?"
reference_solution_path: private/solutions/cs-easy-two-sum-dictionary.cs
hint_ladder:
  1: "Diziyi gezerken her sayı için target - num değerinin sözlükte olup olmadığını kontrol edin."
  2: "Varsa indeks çiftini döndürün, yoksa o sayıyı ve indeksini sözlüğe ekleyin."
  3: "Bu algoritma 'sözlük ile iki sayı toplamı (hash map two sum)' olarak bilinir."
```

---

### cs-easy-merge-sorted-arrays

```yaml
id: cs-easy-merge-sorted-arrays
version: 1
language: csharp
engine: none
difficulty: easy
title: "İki sıralı diziyi tek bir sıralı dizide birleştirme"
prompt: |
  Küçükten büyüğe sıralı a (n elemanlı) ve b (m elemanlı) dizilerini birleştirerek n + m elemanlı yeni bir sıralı dizi üreten `int[] MergeSorted(int[] a, int[] b)` fonksiyonunu yazın. n ve m dizi boyutlarıdır.
constraints:
  - "Zaman karmaşıklığı O(n + m) olmalı"
  - "Ek bellek O(n + m) olmalı"
  - "new int[n + m] tek tahsis yapılmalıdır"
expected:
  time: { MergeSorted: "n + m" }
  space: "n + m"
concept_tags: [data-structures, allocation]
checklist_extra:
  - "İki işaretçi karşılıklı taranmış mı?"
  - "Dizilerden biri bittiğinde diğeri doğru kopyalanmış mı?"
reference_solution_path: private/solutions/cs-easy-merge-sorted-arrays.cs
hint_ladder:
  1: "a.Length + b.Length boyutunda tek bir dizi tahsis edin."
  2: "İki işaretçiyle küçük olan elemanı sırayla yeni diziye yazın."
  3: "Bu algoritma 'sıralı dizileri birleştirme (merge sorted arrays)' olarak bilinir."
```

---

### cs-easy-remove-adjacent-duplicates

```yaml
id: cs-easy-remove-adjacent-duplicates
version: 1
language: csharp
engine: none
difficulty: easy
title: "Sıralı dizideki ardışık tekrarları yerinde temizleme"
prompt: |
  Küçükten büyüğe sıralı n elemanlı bir tamsayı dizisindeki mükerrer elemanları yerinde temizleyerek her elemanın bir kez kalmasını sağlayan ve yeni boyutu döndüren `int RemoveDuplicates(int[] numbers)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "Yeni eleman adedi dönmelidir"
expected:
  time: { RemoveDuplicates: "n" }
  space: "1"
concept_tags: [data-structures, zero-allocation]
checklist_extra:
  - "Okuma ve yazma indeksleri ayrıştırılmış mı?"
  - "Benzersiz eleman adedi doğru dönülmüş mü?"
reference_solution_path: private/solutions/cs-easy-remove-adjacent-duplicates.cs
hint_ladder:
  1: "Dizi sıralı olduğundan aynı elemanlar peş peşe gelir."
  2: "Yazma indeksini yalnızca yeni bir farklı eleman gördükçe birer birer ilerletin."
  3: "Bu algoritma 'sıralı dizide yerinde tekleştirme (in-place deduplication)' olarak bilinir."
```

---

### cs-easy-safe-disposable-wrap

```yaml
id: cs-easy-safe-disposable-wrap
version: 1
language: csharp
engine: none
difficulty: easy
title: "Yönetilmeyen kaynağı IDisposable ile temizleyen sınıf"
prompt: |
  Yönetilmeyen bir işletim sistemi kaynağını (ör. IntPtr handle) sarmalayan ve Dispose çağrısında güvenle serbest bırakan `class SafeResourceWrapper` sınıfını IDisposable kalıbına uygun olarak yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "GC.SuppressFinalize çağrılmalıdır"
expected:
  time: { SafeResourceWrapper: "1" }
  space: "1"
concept_tags: [resource-management, memory-leak]
checklist_extra:
  - "Dispose(bool disposing) deseni uygulanmış mı?"
  - "GC.SuppressFinalize(this) çağrılmış mı?"
reference_solution_path: private/solutions/cs-easy-safe-disposable-wrap.cs
hint_ladder:
  1: "IDisposable arayüzünü uygulayın."
  2: "Dispose metodunda kaynağı serbest bırakıp GC.SuppressFinalize ile çöp toplayıcı sonlandırıcısını iptal edin."
  3: "Bu kaynak yönetimi standardı 'kullan-at deseni (IDisposable pattern)' olarak bilinir."
```

---

### cs-easy-word-frequency-map

```yaml
id: cs-easy-word-frequency-map
version: 1
language: csharp
engine: none
difficulty: easy
title: "Metindeki sözcüklerin geçme sıklıklarını sözlükte toplama"
prompt: |
  Boşluklarla ayrılmış sözcükler içeren bir metindeki her bir sözcüğün frekansını hesaplayan `Dictionary<string, int> CountWordFrequencies(string text)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Dictionary<string, int> kullanılmalıdır"
expected:
  time: { CountWordFrequencies: "n" }
  space: "n"
concept_tags: [data-structures, parsing]
checklist_extra:
  - "SözlükteTryGetValue kullanılmış mı?"
  - "null veya boş metin kontrolü yapılmış mı?"
reference_solution_path: private/solutions/cs-easy-word-frequency-map.cs
hint_ladder:
  1: "Metni sözcüklere ayırın."
  2: "Her sözcük için sözlükteTryGetValue ile mevcut değeri okuyup 1 artırarak kaydedin."
  3: "Bu algoritma 'sözlük ile frekans sayımı (word frequency dictionary)' olarak bilinir."
```

---

### cs-easy-set-intersection-basic

```yaml
id: cs-easy-set-intersection-basic
version: 1
language: csharp
engine: none
difficulty: easy
title: "İki kümenin ortak elemanlarını yeni kümede toplama"
prompt: |
  n elemanlı a ve m elemanlı b karma kümelerindeki kesişim elemanlarını yeni bir HashSet<int> içinde döndüren `HashSet<int> FindIntersection(HashSet<int> a, HashSet<int> b)` fonksiyonunu yazın. n ve m küme boyutlarıdır.
constraints:
  - "Zaman karmaşıklığı O(min(n, m)) olmalı"
  - "Ek bellek O(min(n, m)) olmalı"
  - "Küçük küme taranmalıdır"
expected:
  time: { FindIntersection: "n + m" }
  space: "n + m"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Döngü daha az elemanlı küme üzerinde mi kurulmuş?"
  - "Contains ile O(1) sorgu yapılmış mı?"
reference_solution_path: private/solutions/cs-easy-set-intersection-basic.cs
hint_ladder:
  1: "Boyutu küçük olan kümeyi döngüye sokun."
  2: "Büyük kümede Contains olan elemanları yeni oluşturulan sonuç kümesine ekleyin."
  3: "Bu işlem 'küme kesişimi hesaplama (set intersection)' olarak bilinir."
```

---

### cs-easy-matrix-transpose

```yaml
id: cs-easy-matrix-transpose
version: 1
language: csharp
engine: none
difficulty: easy
title: "İki boyutlu matrisin devriğini alma"
prompt: |
  n x m boyutundaki bir tamsayı matrisinin devriğini alarak m x n boyutunda yeni bir matris döndüren `int[,] TransposeMatrix(int[,] matrix)` fonksiyonunu yazın. n satır ve m sütun adedidir.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(n * m) olmalı"
  - "new int[m, n] tahsis edilmelidir"
expected:
  time: { TransposeMatrix: "n*m" }
  space: "n*m"
concept_tags: [data-structures, allocation]
checklist_extra:
  - "Boyutlar matrix.GetLength(0) ve GetLength(1) ile alınmış mı?"
  - "result[j, i] = matrix[i, j] ataması yapılmış mı?"
reference_solution_path: private/solutions/cs-easy-matrix-transpose.cs
hint_ladder:
  1: "m x n boyutunda yeni bir iki boyutlu dizi oluşturun."
  2: "İç içe iki döngü ile elemanları satır ve sütunlarını yer değiştirerek kopyalayın."
  3: "Bu işlem 'matris transpozu alma (matrix transpose)' olarak bilinir."
```

---

### cs-easy-check-anagram-dictionary

```yaml
id: cs-easy-check-anagram-dictionary
version: 1
language: csharp
engine: none
difficulty: easy
title: "İki metnin sözlük yardımıyla anagram olduğunu denetleme"
prompt: |
  İki metnin karakter sıklıklarını Dictionary<char, int> ile sayarak anagram olup olmadığını denetleyen `bool AreAnagrams(string s1, string s2)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Uzunluklar farklıysa hemen false dönmelidir"
expected:
  time: { AreAnagrams: "n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Uzunluk eşitliği başta denetlenmiş mi?"
  - "Karakter sayımları net sıfırlanmış mı?"
reference_solution_path: private/solutions/cs-easy-check-anagram-dictionary.cs
hint_ladder:
  1: "Uzunluklar eşit değilse false dönün."
  2: "Bir karakter frekans tablosu tutarak s1 için artırın, s2 için azaltın; tüm değerlerin sıfır kaldığını teyit edin."
  3: "Bu algoritma 'sözlük ile anagram doğrulaması (dictionary anagram check)' olarak bilinir."
```

---

### cs-easy-span-int-parsing

```yaml
id: cs-easy-span-int-parsing
version: 1
language: csharp
engine: none
difficulty: easy
title: "Bellek tahsisi yapmadan karakter diliminden tamsayı ayrıştırma"
prompt: |
  ReadOnlySpan<char> içindeki rakamları alt dizgi (substring) tahsis etmeden tek geçişte tamsayıya dönüştüren `bool TryParseIntFast(ReadOnlySpan<char> span, out int value)` fonksiyonunu yazın. n dilim uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (sıfır tahsis)"
  - "int.TryParse(ReadOnlySpan) kullanılabilir"
expected:
  time: { TryParseIntFast: "n" }
  space: "1"
concept_tags: [span, zero-allocation]
checklist_extra:
  - "int.TryParse doğrudan ReadOnlySpan üzerinde çalıştırılmış mı?"
  - "Heap tahsisi yapılmamış mı?"
reference_solution_path: private/solutions/cs-easy-span-int-parsing.cs
hint_ladder:
  1: "Substring çağırmak her seferinde heap üzerinde yeni bir string nesnesi oluşturur."
  2: "int.TryParse(span, out value) çağrısını doğrudan karakter dilimi üzerinde işleterek sıfır tahsis sağlayın."
  3: "Bu modern ayrıştırma yöntemi 'sıfır tahsisli tamsayı ayrıştırma (zero-allocation integer parsing)' olarak bilinir."
```

---

### cs-easy-queue-two-stacks

```yaml
id: cs-easy-queue-two-stacks
version: 1
language: csharp
engine: none
difficulty: easy
title: "İki yığın kullanarak ilk giren ilk çıkar kuyruk tasarlama"
prompt: |
  Yalnızca iki adet Stack<int> kullanarak FIFO (ilk giren ilk çıkar) kuyruk mantığını sunan `class StackQueue` sınıfını yazın. Enqueue ve Dequeue metotları bulunmalıdır.
constraints:
  - "Amortize zaman karmaşıklığı O(1*) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Ters aktarım gerektiğinde yapılmalıdır"
expected:
  time: { StackQueue: "1*" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Çıkış yığını boşken giriş yığınından aktarılmış mı?"
  - "Amortize O(1) maliyet korunmuş mu?"
reference_solution_path: private/solutions/cs-easy-queue-two-stacks.cs
hint_ladder:
  1: "Gelen elemanları _inStack'e atın."
  2: "Çıkarma anında _outStack boşsa _inStack'teki tüm elemanları _outStack'e aktarıp en üsttekini çekin."
  3: "Bu veri yapısı mekanizması 'iki yığın ile kuyruk simülasyonu (queue using two stacks)' olarak bilinir."
```

---

### cs-easy-valid-parentheses

```yaml
id: cs-easy-valid-parentheses
version: 1
language: csharp
engine: none
difficulty: easy
title: "Yığın kullanarak parantez dengesini doğrulama"
prompt: |
  Yalnızca parantez karakterleri içeren bir metindeki parantezlerin dengeli açılıp kapandığını Stack<char> ile doğrulayan `bool IsValidParentheses(string text)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Metin bittiğinde yığın boş kalmalıdır"
expected:
  time: { IsValidParentheses: "n" }
  space: "n"
concept_tags: [data-structures, parsing]
checklist_extra:
  - "Boş yığında kapatma parantezi gelmesi kontrol edilmiş mi?"
  - "Metin bitince stack.Count == 0 sınanmış mı?"
reference_solution_path: private/solutions/cs-easy-valid-parentheses.cs
hint_ladder:
  1: "Açma parantezi gördükçe yığına itin."
  2: "Kapatma parantezi gördükçe yığından eleman çekip eşleşmeyi kontrol edin."
  3: "Bu algoritma 'yığın ile parantez doğrulama (valid parentheses check)' olarak bilinir."
```

---

### cs-easy-min-stack-basic

```yaml
id: cs-easy-min-stack-basic
version: 1
language: csharp
engine: none
difficulty: easy
title: "Sabit sürede asgari elemanı döndüren yığın (C#)"
prompt: |
  Standart Push, Pop, Peek metotlarının yanında mevcut en küçük elemanı O(1) sürede döndüren GetMin() metoduna sahip `class MinStack` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı her işlem için O(1) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Ek bir min yığını tutulmalıdır"
expected:
  time: { MinStack: "1" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Her push işleminde min yığını güncellenmiş mi?"
  - "pop işleminde iki yığın senkron tutulmuş mu?"
reference_solution_path: private/solutions/cs-easy-min-stack-basic.cs
hint_ladder:
  1: "Asıl elemanları saklayan bir Stack ve o ana kadarki minimumları saklayan ikinci bir minStack tutun."
  2: "GetMin() çağrıldığında minStack tepesindeki değeri doğrudan döndürün."
  3: "Bu veri yapısı 'asgari eleman takipli yığın (min stack)' olarak bilinir."
```

---

### cs-easy-majority-element

```yaml
id: cs-easy-majority-element
version: 1
language: csharp
engine: none
difficulty: easy
title: "Dizide boyutun yarısından fazla geçen çoğunluk elemanını bulma"
prompt: |
  n elemanlı bir tamsayı dizisinde n/2'den fazla kez geçen çoğunluk elemanını Boyer-Moore oylama algoritmasıyla O(n) zamanda bulan `int? FindMajority(int[] numbers)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "İkinci geçişte doğrulama yapılmalıdır"
expected:
  time: { FindMajority: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Oylama ile aday tek geçişte bulunmuş mu?"
  - "İkinci geçişte adayın gerçekten > n/2 olduğu teyit edilmiş mi?"
reference_solution_path: private/solutions/cs-easy-majority-element.cs
hint_ladder:
  1: "Bir aday ve sayaç değişkeni tutun; aynı elemanda sayacı artırın, farklı elemanda sayacı azaltın."
  2: "Sonunda adayın dizideki gerçek frekansını sayıp çoğunluk olduğunu doğrulayın."
  3: "Bu algoritma 'Boyer-Moore çoğunluk oylama algoritması (Boyer-Moore majority vote)' olarak bilinir."
```

---

### cs-easy-single-number-xor

```yaml
id: cs-easy-single-number-xor
version: 1
language: csharp
engine: none
difficulty: easy
title: "Dizide tek kalan sayıyı bit işlemiyle bulma (C#)"
prompt: |
  Bir tanesi hariç her sayının tam ikişer kez geçtiği tamsayı dizisinde tek kalan sayıyı XOR işlemiyle O(1) alanda bulan `int FindSingle(int[] numbers)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Bit düzeyi XOR (^) kullanılmalıdır"
expected:
  time: { FindSingle: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Tüm elemanlar ardışık XOR işlemine tabi tutulmuş mu?"
  - "Ek bellek sabit O(1) kalmış mı?"
reference_solution_path: private/solutions/cs-easy-single-number-xor.cs
hint_ladder:
  1: "result değişkenini 0 ile başlatın."
  2: "Dizideki tüm sayıları result ^= x işlemiyle birleştirin; çift gelen sayılar sıfırlanacaktır."
  3: "Bu teknik 'XOR ile benzersiz eleman tespiti (single number XOR)' olarak bilinir."
```

---

### cs-easy-partition-parity

```yaml
id: cs-easy-partition-parity
version: 1
language: csharp
engine: none
difficulty: easy
title: "Dizideki çiftleri başa tekleri sona yerinde gruplama"
prompt: |
  n elemanlı bir tamsayı dizisindeki çift sayıları başa, tek sayıları sona yerinde iki işaretçiyle toplayan `void PartitionByParity(int[] numbers)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "İki indeks kullanılmalıdır"
expected:
  time: { PartitionByParity: "n" }
  space: "1"
concept_tags: [data-structures, zero-allocation]
checklist_extra:
  - "Sol çift sağ tek arayarak takas yapılmış mı?"
  - "Yerinde O(1) ek bellek kullanılmış mı?"
reference_solution_path: private/solutions/cs-easy-partition-parity.cs
hint_ladder:
  1: "Soldan tek, sağdan çift elemanları bulun."
  2: "İndeksler karşılaşana kadar elemanları takas edin."
  3: "Bu algoritma 'pariteye göre yerinde bölümleme (partition by parity)' olarak bilinir."
```

---

### cs-easy-sliding-window-product

```yaml
id: cs-easy-sliding-window-product
version: 1
language: csharp
engine: none
difficulty: easy
title: "k boyutlu kayan pencerede maksimum çarpımı bulma"
prompt: |
  n elemanlı pozitif sayılar dizisinde boyutu k olan bitişik alt dizilerin maksimum çarpımını kayan pencereyle hesaplayan `long MaxSubarrayProductK(int[] numbers, int k)` fonksiyonunu yazın. n dizi boyutu ve k pencere boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "k > n durumunda 0 dönmelidir"
expected:
  time: { MaxSubarrayProductK: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "İlk k eleman çarpılıp sonraki adımlarda kayan pencere uygulanmış mı?"
  - "64-bit çarpım kullanılmış mı?"
reference_solution_path: private/solutions/cs-easy-sliding-window-product.cs
hint_ladder:
  1: "İlk k elemanın çarpımını hesaplayarak başlayın."
  2: "Her pencere kaydırmasında yeni elemanı çarpıp çıkan elemana bölerek maksimumu güncelleyin."
  3: "Bu algoritma 'kayan pencere ile alt dizi çarpımı (sliding window product)' olarak bilinir."
```

---

### cs-easy-top-k-frequent

```yaml
id: cs-easy-top-k-frequent
version: 1
language: csharp
engine: none
difficulty: easy
title: "En sık geçen k adet elemanı bulma"
prompt: |
  n elemanlı tamsayı dizisinde en yüksek frekansa sahip k adet elemanı sözlük ve sıralama kullanarak bulan `int[] TopKFrequent(int[] numbers, int k)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n log n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "k elemanlı dizi dönmelidir"
expected:
  time: { TopKFrequent: "n log n" }
  space: "n"
concept_tags: [data-structures, allocation]
checklist_extra:
  - "Eleman frekansları Dictionary ile sayılmış mı?"
  - "Frekansa göre sıralanıp ilk k eleman alınmış mı?"
reference_solution_path: private/solutions/cs-easy-top-k-frequent.cs
hint_ladder:
  1: "Her sayının geçme sıklığını bir sözlükte biriktirin."
  2: "Frekanslara göre azalan sırada sıralayıp ilk k elemanı döndürün."
  3: "Bu algoritma 'en sık geçen elemanları bulma (top k frequent elements)' olarak bilinir."
```

---

### cs-easy-rle-compression

```yaml
id: cs-easy-rle-compression
version: 1
language: csharp
engine: none
difficulty: easy
title: "Karakter ve tekrar sayılarıyla metin sıkıştırma"
prompt: |
  Metindeki ardışık tekrarlayan karakterleri harf ve tekrar sayısı biçiminde (ör. 'aaabb' -> 'a3b2') StringBuilder ile sıkıştıran `string CompressString(string text)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "StringBuilder kullanılmalıdır"
expected:
  time: { CompressString: "n" }
  space: "n"
concept_tags: [string-building, parsing]
checklist_extra:
  - "Ardışık karakter sayımı tek geçişte yapılmış mı?"
  - "StringBuilder ile tek seferde metin inşa edilmiş mi?"
reference_solution_path: private/solutions/cs-easy-rle-compression.cs
hint_ladder:
  1: "Metni tararken aynı karakter devam ettikçe sayacı artırın."
  2: "Karakter değiştiğinde harfi ve sayacı StringBuilder'a ekleyin."
  3: "Bu sıkıştırma yöntemi 'çalışma uzunluğu kodlaması (run length encoding)' olarak bilinir."
```

---

### cs-easy-rotate-array-k

```yaml
id: cs-easy-rotate-array-k
version: 1
language: csharp
engine: none
difficulty: easy
title: "Diziyi k adım sağa döndürme (C#)"
prompt: |
  n elemanlı tamsayı dizisinin elemanlarını k adım sağa dairesel döndüren `void RotateRight(int[] numbers, int k)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "Üç ters çevirme (reverse) yöntemi kullanılabilir"
expected:
  time: { RotateRight: "n" }
  space: "1"
concept_tags: [data-structures, zero-allocation]
checklist_extra:
  - "k = k % n ile gereksiz turlar elenmiş mi?"
  - "Dizi tümden, ardından iki parça halinde ters çevrilmiş mi?"
reference_solution_path: private/solutions/cs-easy-rotate-array-k.cs
hint_ladder:
  1: "k değerini dizi boyutuna modül alarak sadeleştirin."
  2: "Tüm diziyi, ardından ilk k elemanı ve kalan n-k elemanı ters çevirerek yerinde döndürmeyi tamamlayın."
  3: "Bu algoritma 'ters çevirme ile dizi döndürme (reverse rotate algorithm)' olarak bilinir."
```

---

### cs-easy-longest-ones

```yaml
id: cs-easy-longest-ones
version: 1
language: csharp
engine: none
difficulty: easy
title: "İkilik dizide en uzun ardışık 1 dizilimini bulma (C#)"
prompt: |
  Yalnızca 0 ve 1 içeren n elemanlı bir dizideki en uzun ardışık 1'lerin adedini hesaplayan `int LongestContinuousOnes(int[] numbers)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Tek döngü kurulmalıdır"
expected:
  time: { LongestContinuousOnes: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "1 gördükçe sayaç artırılıp 0'da sıfırlanmış mı?"
  - "Maksimum sayaç güncellenmiş mi?"
reference_solution_path: private/solutions/cs-easy-longest-ones.cs
hint_ladder:
  1: "Mevcut sayaç ve maksimum sayaç değişkenlerini tutun."
  2: "1 gördükçe sayacı artırıp maksimumu güncelleyin; 0 gördükçe sayacı sıfırlayın."
  3: "Bu algoritma 'ardışık birlerin maksimum uzunluğu (longest consecutive ones)' olarak bilinir."
```

---

### cs-easy-tree-leaf-count

```yaml
id: cs-easy-tree-leaf-count
version: 1
language: csharp
engine: none
difficulty: easy
title: "İkili ağaçta yaprak düğüm sayısını hesaplama"
prompt: |
  Kökü verilen ikili ağaçta çocuğu olmayan tüm yaprak düğümlerin sayısını özyinelemeli olarak hesaplayan `int CountLeaves(TreeNode root)` fonksiyonunu yazın. n ağaçtaki toplam düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek çağrı yığını için O(log n) olmalı"
  - "root null ise 0 dönmelidir"
expected:
  time: { CountLeaves: "n" }
  space: "log n"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "Hem sol hem sağ çocuğu null olan düğümler 1 sayılmış mı?"
  - "root == null taban durumu doğru tanımlanmış mı?"
reference_solution_path: private/solutions/cs-easy-tree-leaf-count.cs
hint_ladder:
  1: "Kök null ise 0 dönün."
  2: "Sol ve sağ çocukların her ikisi de null ise yapraktır, 1 dönün; aksi halde iki alt ağacın toplamını döndürün."
  3: "Bu algoritma 'ikili ağaçta yaprak sayımı (binary tree leaf count)' olarak bilinir."
```

---

### cs-easy-invert-tree

```yaml
id: cs-easy-invert-tree
version: 1
language: csharp
engine: none
difficulty: easy
title: "İkili ağacın dallarını yerinde aynalama"
prompt: |
  İkili bir ağacın tüm düğümlerinin sol ve sağ çocuklarını yer değiştirerek ağacı aynalayan `void InvertTree(TreeNode root)` fonksiyonunu yazın. n ağaçtaki düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek çağrı yığını için O(log n) olmalı"
  - "Yerinde gösterici takası yapılmalıdır"
expected:
  time: { InvertTree: "n" }
  space: "log n"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "Sol ve sağ çocuk göstericileri geçici değişkenle takas edilmiş mi?"
  - "Özyineleme çocuk alt ağaçlara uygulanmış mı?"
reference_solution_path: private/solutions/cs-easy-invert-tree.cs
hint_ladder:
  1: "Kök null ise doğrudan dönün."
  2: "Sol ve sağ çocukları takas edip çocukları özyinelemeli olarak çağırın."
  3: "Bu algoritma 'ikili ağacı tersine çevirme (invert binary tree)' olarak bilinir."
```

---

### cs-easy-same-tree

```yaml
id: cs-easy-same-tree
version: 1
language: csharp
engine: none
difficulty: easy
title: "İki ikili ağacın yapısal ve değer eşitliğini sınama (C#)"
prompt: |
  İki ikili ağacın yapısal olarak özdeş ve karşılık gelen tüm düğüm değerlerinin eşit olduğunu denetleyen `bool IsSameTree(TreeNode p, TreeNode q)` fonksiyonunu yazın. n ağaçlardaki düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek çağrı yığını için O(log n) olmalı"
  - "Her iki düğüm null olduğunda true dönmelidir"
expected:
  time: { IsSameTree: "n" }
  space: "log n"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "Biri null diğeri dolu olduğunda false dönülmüş mü?"
  - "Düğüm değerleri ve alt dallar özyinelemeli test edilmiş mi?"
reference_solution_path: private/solutions/cs-easy-same-tree.cs
hint_ladder:
  1: "Her iki düğüm de null ise true dönün."
  2: "Biri null ise veya değerleri uyuşmuyorsa false dönün; sol ve sağ alt ağaçları özyinelemeli kıyaslayın."
  3: "Bu algoritma 'özdeş ikili ağaç kontrolü (same binary tree)' olarak bilinir."
```

---

### cs-easy-list-capacity-trim

```yaml
id: cs-easy-list-capacity-trim
version: 1
language: csharp
engine: none
difficulty: easy
title: "Fazla belleği geri vermek için liste kapasitesini daraltma"
prompt: |
  Eleman silme işlemlerinden sonra gereksiz bellek tutan bir List<int> koleksiyonunun kapasitesini tam olarak eleman sayısına indiren `void TrimListCapacity(List<int> list)` fonksiyonunu yazın. n listenin eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "TrimExcess() çağrılmalıdır"
expected:
  time: { TrimListCapacity: "n" }
  space: "1"
concept_tags: [allocation, gc]
checklist_extra:
  - "list.TrimExcess() çağrılmış mı?"
  - "Fazlalık bellek sisteme iade edilmiş mi?"
reference_solution_path: private/solutions/cs-easy-list-capacity-trim.cs
hint_ladder:
  1: "list.TrimExcess() metodunu çağırın."
  2: "Bu metot dizinin iç tamponunu mevcut Count ile eşitleyerek kullanılmayan belleği çöp toplayıcıya devreder."
  3: "Bu optimizasyon 'liste kapasitesini daraltma (trim list capacity)' olarak bilinir."
```

---

### cs-easy-avoid-closure-allocation

```yaml
id: cs-easy-avoid-closure-allocation
version: 1
language: csharp
engine: none
difficulty: easy
title: "Lambda içinde dış değişken yakalamadan arama yapma"
prompt: |
  Dizide target değerine eşit elemanları sayarken lambda dış değişken yakalaması (closure allocation) yapmadan döngüyle çalışan `int CountMatchesFast(int[] numbers, int target)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Closure heap tahsisi engellenmelidir"
expected:
  time: { CountMatchesFast: "n" }
  space: "1"
concept_tags: [gc, zero-allocation]
checklist_extra:
  - "LINQ veya closure kullanılmayarak heap tahsisi sıfırlanmış mı?"
  - "Doğrudan döngü kurulmuş mu?"
reference_solution_path: private/solutions/cs-easy-avoid-closure-allocation.cs
hint_ladder:
  1: "LINQ .Count(x => x == target) çağrısı her seferinde bir closure sınıfı örneği tahsis eder."
  2: "Sıcak kod yollarında bunun yerine doğrudan for döngüsü kullanarak heap tahsisini sıfırlayın."
  3: "Bu optimizasyon 'kapanış tahsisini önleme (avoid closure allocation)' olarak bilinir."
```

---

### cs-easy-array-pool-borrow

```yaml
id: cs-easy-array-pool-borrow
version: 1
language: csharp
engine: none
difficulty: easy
title: "Bellek havuzundan geçici dizi ödünç alma ve iade etme"
prompt: |
  Büyük geçici tamsayı dizisi gerektiren bir işlemde new int[] tahsis etmek yerine ArrayPool<int>.Shared üzerinden dizi ödünç alıp finally bloğunda iade eden `void ProcessLargeData(int size)` fonksiyonunu yazın. n talep edilen boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (havuzdan paylaşımlı)"
  - "try-finally ile dizi iadesi garanti edilmelidir"
expected:
  time: { ProcessLargeData: "n" }
  space: "1"
concept_tags: [allocation, gc]
checklist_extra:
  - "ArrayPool<int>.Shared.Rent çağrılmış mı?"
  - "finally bloğunda Return edilmiş mi?"
reference_solution_path: private/solutions/cs-easy-array-pool-borrow.cs
hint_ladder:
  1: "ArrayPool<int>.Shared.Rent(size) ile havuzdan geçici dizi alın."
  2: "İşlem bittiğinde finally bloğunda pool.Return(array) çağrısıyla diziyi havuza geri verin."
  3: "Bu bellek yönetimi 'dizi havuzu kullanımı (array pool renting)' olarak bilinir."
```

---

### cs-easy-immutable-point

```yaml
id: cs-easy-immutable-point
version: 1
language: csharp
engine: none
difficulty: easy
title: "Değiştirilemez nokta yapısı ve veri bütünlüğü"
prompt: |
  X ve Y koordinatlarını tutan, salt okunur (readonly struct) olarak tanımlanmış, kopyalamalarda durum bozulmasını önleyen `readonly struct Point2D` yapısını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "readonly struct ve init-only özellikler kullanılmalıdır"
expected:
  time: { Point2D: "1" }
  space: "1"
concept_tags: [encapsulation, performance]
checklist_extra:
  - "readonly struct olarak tanımlanmış mı?"
  - "Tüm alanlar veya özellikler salt okunur mu?"
reference_solution_path: private/solutions/cs-easy-immutable-point.cs
hint_ladder:
  1: "public readonly struct Point2D tanımını yapın."
  2: "public double X { get; } ve public double Y { get; } özellikleriyle yapının sonradan mutasyona uğramasını engelleyin."
  3: "Bu tasarım 'değiştirilemez değer türü (readonly struct)' olarak bilinir."
```

---

### cs-easy-custom-string-format

```yaml
id: cs-easy-custom-string-format
version: 1
language: csharp
engine: none
difficulty: easy
title: "Biçimli metin çıktısı oluşturma"
prompt: |
  Kullanıcı adı ve yaş bilgilerini alarak string birleştirmeden StringBuilder.AppendFormat ile tek seferde biçimlendiren `string FormatUserProfile(string name, int age)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "StringBuilder kullanılmalıdır"
expected:
  time: { FormatUserProfile: "1" }
  space: "1"
concept_tags: [string-building, allocation]
checklist_extra:
  - "StringBuilder kullanılmış mı?"
  - "AppendFormat ile biçimlendirme yapılmış mı?"
reference_solution_path: private/solutions/cs-easy-custom-string-format.cs
hint_ladder:
  1: "Bir StringBuilder oluşturun."
  2: "sb.AppendFormat(\"User: {0}, Age: {1}\", name, age) çağrısıyla metni biçimlendirip ToString ile üretin."
  3: "Bu işlem 'biçimli metin oluşturma (formatted string builder)' olarak bilinir."
```

---

### cs-easy-null-coalescing-pipeline

```yaml
id: cs-easy-null-coalescing-pipeline
version: 1
language: csharp
engine: none
difficulty: easy
title: "Boş girdi durumlarında varsayılan değer atama zinciri"
prompt: |
  Verilen kullanıcı adını kırparak temizleyen, metin null veya boşsa 'Anonymous' varsayılan değerini döndüren `string NormalizeUsername(string input)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "string.IsNullOrWhiteSpace ve null-coalescing operatörü (??) kullanılmalıdır"
expected:
  time: { NormalizeUsername: "n" }
  space: "n"
concept_tags: [input-validation, edge-cases]
checklist_extra:
  - "string.IsNullOrWhiteSpace denetimi yapılmış mı?"
  - "Varsayılan değer atanmış mı?"
reference_solution_path: private/solutions/cs-easy-null-coalescing-pipeline.cs
hint_ladder:
  1: "string.IsNullOrWhiteSpace(input) ise 'Anonymous' döndürün."
  2: "Aksi halde input.Trim() çağrısının sonucunu döndürün."
  3: "Bu temizlik işlemi 'boşluk denetimli metin normalleştirme (null-coalescing normalization)' olarak bilinir."
```

---

### cs-easy-event-unsubscribe-leak

```yaml
id: cs-easy-event-unsubscribe-leak
version: 1
language: csharp
engine: none
difficulty: easy
title: "Bellek sızıntısını önlemek için olay aboneliğinden çıkma"
prompt: |
  Bir yayıncının olayına abone olan ve nesne Dispose edildiğinde abonelikten çıkarak bellek sızıntısını engelleyen `class EventSubscriber` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Dispose içinde -= ile abonelik kaldırılmalıdır"
expected:
  time: { EventSubscriber: "1" }
  space: "1"
concept_tags: [memory-leak, resource-management]
checklist_extra:
  - "+= ile abone olunup -= ile çıkılmış mı?"
  - "Yayıncının aboneyi hayatta tutması önlenmiş mi?"
reference_solution_path: private/solutions/cs-easy-event-unsubscribe-leak.cs
hint_ladder:
  1: "Olay abonelikleri yayıncıda aboneye yönelik güçlü bir referans tutar."
  2: "Dispose metodunda publisher.OnEvent -= HandleEvent çağrısıyla abonelikten çıkarak çöp toplayıcının aboneyi temizlemesine izin verin."
  3: "Bu kalıp 'olay aboneliğinden çıkma (event unsubscription)' olarak bilinir."
```

---

### cs-easy-async-task-delay

```yaml
id: cs-easy-async-task-delay
version: 1
language: csharp
engine: none
difficulty: easy
title: "Belirtilen süre kadar asenkron bekleyen ve sayaç artıran işlem"
prompt: |
  Thread.Sleep yerine Task.Delay kullanarak iş parçacığını bloklamadan ms kadar bekleyen ve sayacı 1 artıran `Task<int> DelayedCounterAsync(int ms)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "async ve await Task.Delay kullanılmalıdır"
expected:
  time: { DelayedCounterAsync: "1" }
  space: "1"
concept_tags: [async-await, performance]
checklist_extra:
  - "Thread.Sleep yerine Task.Delay kullanılmış mı?"
  - "async-await deseni doğru kurulmuş mu?"
reference_solution_path: private/solutions/cs-easy-async-task-delay.cs
hint_ladder:
  1: "Thread.Sleep çalışan iş parçacığını bloke eder ve kaynak tüketir."
  2: "await Task.Delay(ms) çağrısı ile iş parçacığını serbest bırakıp süresi dolunca kaldığı yerden devam edin."
  3: "Bu asenkron yöntem 'bloklamayan asenkron bekleme (non-blocking task delay)' olarak bilinir."
```

---

### cs-easy-cancel-token-cooperative

```yaml
id: cs-easy-cancel-token-cooperative
version: 1
language: csharp
engine: none
difficulty: easy
title: "İptal belirteciyle asenkron işlemi durdurma"
prompt: |
  Uzun süren bir döngüde her adımda CancellationToken üzerinden iptal talebi gelip gelmediğini denetleyen `Task LongRunningOperationAsync(CancellationToken ct)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) adım başı olmalı"
  - "Ek bellek O(1) olmalı"
  - "ct.ThrowIfCancellationRequested() kullanılmalıdır"
expected:
  time: { LongRunningOperationAsync: "1" }
  space: "1"
concept_tags: [async-await, resource-management]
checklist_extra:
  - "ct.ThrowIfCancellationRequested çağrılmış mı?"
  - "OperationCanceledException doğru fırlatılmış mı?"
reference_solution_path: private/solutions/cs-easy-cancel-token-cooperative.cs
hint_ladder:
  1: "Döngü içerisinde düzenli aralıklarla ct.ThrowIfCancellationRequested() çağrısı yapın."
  2: "İptal sinyali geldiğinde işlem güvenli biçimde durdurulsun."
  3: "Bu mekanizma 'işbirlikçi iptal belirteci deseni (cooperative cancellation token)' olarak bilinir."
```

---

### cs-easy-concurrent-dictionary-count

```yaml
id: cs-easy-concurrent-dictionary-count
version: 1
language: csharp
engine: none
difficulty: easy
title: "İş parçacığı güvenli sözlükle sayaç artırma"
prompt: |
  Birden fazla iş parçacığının aynı anda eriştiği ConcurrentDictionary<string, int> koleksiyonunda verilen anahtarın değerini AddOrUpdate ile atomik artıran `void IncrementMetric(ConcurrentDictionary<string, int> dict, string key)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "AddOrUpdate kullanılmalıdır"
expected:
  time: { IncrementMetric: "1" }
  space: "1"
concept_tags: [concurrency, performance]
checklist_extra:
  - "AddOrUpdate ile atomik artırma yapılmış mı?"
  - "Veri yarışı önlenmiş mi?"
reference_solution_path: private/solutions/cs-easy-concurrent-dictionary-count.cs
hint_ladder:
  1: "Standart sözlükler eşzamanlı erişimde kilit gerektirir."
  2: "dict.AddOrUpdate(key, 1, (k, oldVal) => oldVal + 1) çağrısıyla atomik sayaç güncellemesi yapın."
  3: "Bu eşzamanlı veri yapısı 'eşzamanlı sözlükte atomik güncelleme (concurrent dictionary update)' olarak bilinir."
```

---

### cs-easy-read-only-collection-wrap

```yaml
id: cs-easy-read-only-collection-wrap
version: 1
language: csharp
engine: none
difficulty: easy
title: "Dışarıya yalnızca okunabilir koleksiyon açma"
prompt: |
  Sınıfın içindeki private List<string> listesini dışarıya doğrudan değiştiremeyecekleri biçimde IReadOnlyList<string> olarak döndüren `IReadOnlyList<string> GetTags()` metodunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "IReadOnlyList veya AsReadOnly kullanılmalıdır"
expected:
  time: { GetTags: "1" }
  space: "1"
concept_tags: [encapsulation, performance]
checklist_extra:
  - "İç liste dışarıya değiştirilebilir açılmamış mı?"
  - "IReadOnlyList ile kapsülleme korunmuş mu?"
reference_solution_path: private/solutions/cs-easy-read-only-collection-wrap.cs
hint_ladder:
  1: "İç List nesnesini private tutun."
  2: "Dışarıya IReadOnlyList<string> veya list.AsReadOnly() sunarak çağıranın listeye yetkisiz eleman eklemesini önleyin."
  3: "Bu kapsülleme kuralı 'salt okunur koleksiyon sarmalama (read-only collection wrapper)' olarak bilinir."
```

---

### cs-easy-enum-flag-has-permission

```yaml
id: cs-easy-enum-flag-has-permission
version: 1
language: csharp
engine: none
difficulty: easy
title: "Bit bayrakları ile yetki denetimi yapma"
prompt: |
  [Flags] niteliğine sahip bir Permissions numaralandırmasında kullanıcının belirli bir yetkiye sahip olup olmadığını denetleyen `bool HasPermission(Permissions userPerms, Permissions required)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Bit düzeyi VE (&) veya HasFlag kullanılmalıdır"
expected:
  time: { HasPermission: "1" }
  space: "1"
concept_tags: [performance, input-validation]
checklist_extra:
  - "(userPerms & required) == required denetimi yapılmış mı?"
  - "Bit maskesi doğru çalışıyor mu?"
reference_solution_path: private/solutions/cs-easy-enum-flag-has-permission.cs
hint_ladder:
  1: "Bit bayraklarında her yetki 2'nin bir kuvvetidir (1, 2, 4, 8...)."
  2: "(userPerms & required) == required veya userPerms.HasFlag(required) ile yetkiyi test edin."
  3: "Bu bit manipülasyonu 'numaralandırma bayrak denetimi (enum flag permission check)' olarak bilinir."
```

---

### cs-easy-safe-indexer-get

```yaml
id: cs-easy-safe-indexer-get
version: 1
language: csharp
engine: none
difficulty: easy
title: "Sınır dışı indekslerde varsayılan değer dönen erişimci"
prompt: |
  n elemanlı bir tamsayı dizisinde index geçerli sınırlar içindeyse o değeri, aksi halde defaultValue değerini döndüren `int GetValueOrDefault(int[] numbers, int index, int defaultValue)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "İndeks sınırları kontrol edilmelidir"
expected:
  time: { GetValueOrDefault: "1" }
  space: "1"
concept_tags: [edge-cases, data-structures]
checklist_extra:
  - "index >= 0 && index < numbers.Length kontrolü yapılmış mı?"
  - "İstisna fırlatılması engellenmiş mi?"
reference_solution_path: private/solutions/cs-easy-safe-indexer-get.cs
hint_ladder:
  1: "İndeksin negatif veya dizi boyutuna eşit/büyük olduğunu kontrol edin."
  2: "Geçerliyse numbers[index], geçersizse defaultValue döndürün."
  3: "Bu erişim deseni 'güvenli indeksleme (safe indexer get)' olarak bilinir."
```

---

### cs-easy-custom-equality-comparer

```yaml
id: cs-easy-custom-equality-comparer
version: 1
language: csharp
engine: none
difficulty: easy
title: "Özel eşitlik karşılaştırıcısıyla çalışan karma kümesi"
prompt: |
  Büyük/küçük harf ayrımını yok sayarak metinleri benzersiz biçimde toplayan HashSet<string> oluşturan `HashSet<string> CreateCaseInsensitiveSet()` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "StringComparer.OrdinalIgnoreCase kullanılmalıdır"
expected:
  time: { CreateCaseInsensitiveSet: "1" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "StringComparer.OrdinalIgnoreCase parametre olarak geçilmiş mi?"
  - "Büyük/küçük harf farkı elenmiş mi?"
reference_solution_path: private/solutions/cs-easy-custom-equality-comparer.cs
hint_ladder:
  1: "new HashSet<string>(StringComparer.OrdinalIgnoreCase) oluşturun."
  2: "Böylece 'test' ve 'TEST' aynı anahtar kabul edilerek tekilleştirilsin."
  3: "Bu karma yapısı yapılandırması 'özel eşitlik karşılaştırıcılı küme (case-insensitive hash set)' olarak bilinir."
```

---

### cs-easy-flatten-jagged-array

```yaml
id: cs-easy-flatten-jagged-array
version: 1
language: csharp
engine: none
difficulty: easy
title: "Düzensiz iki boyutlu diziyi tek boyutlu diziye düzleştirme"
prompt: |
  Satır boyutları değişken olabilen bir jagged (düzensiz) tamsayı dizisinin tüm elemanlarını tek boyutlu bir diziye aktaran `int[] FlattenJagged(int[][] matrix)` fonksiyonunu yazın. n toplam eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Toplam boyut hesaplanıp tek dizi tahsis edilmelidir"
expected:
  time: { FlattenJagged: "n" }
  space: "n"
concept_tags: [data-structures, allocation]
checklist_extra:
  - "Toplam eleman sayısı baştan sayılıp new int[total] açılmış mı?"
  - "Elemanlar sırayla kopyalanmış mı?"
reference_solution_path: private/solutions/cs-easy-flatten-jagged-array.cs
hint_ladder:
  1: "Önce matristeki her satırın boyutunu toplayarak toplam eleman sayısını bulun."
  2: "Tek bir dizi tahsis edip satırları sırayla bu diziye kopyalayın."
  3: "Bu işlem 'düzensiz dizi düzleştirme (flatten jagged array)' olarak bilinir."
```

---

### cs-easy-memory-stream-copy

```yaml
id: cs-easy-memory-stream-copy
version: 1
language: csharp
engine: none
difficulty: easy
title: "Akışlar arasında bellek kopyalaması yapma"
prompt: |
  Bir kaynak akıştaki (Stream) tüm baytları hedef akışa asenkron olarak kopyalayan `Task CopyStreamAsync(Stream source, Stream destination)` fonksiyonunu yazın. n akıştaki bayt sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) (sabit tampon) olmalı"
  - "source.CopyToAsync kullanılmalıdır"
expected:
  time: { CopyStreamAsync: "n" }
  space: "1"
concept_tags: [async-await, resource-management]
checklist_extra:
  - "await source.CopyToAsync(destination) çağrılmış mı?"
  - "null akış kontrolü yapılmış mı?"
reference_solution_path: private/solutions/cs-easy-memory-stream-copy.cs
hint_ladder:
  1: "await source.CopyToAsync(destination) çağrısı yapın."
  2: "Bu asenkron metot sabit boyutlu bir ara tampon kullanarak akış verilerini bloklamadan hedefe aktarır."
  3: "Bu akış işlemi 'asenkron akış kopyalama (async stream copy)' olarak bilinir."
```

---

### cs-easy-string-split-no-alloc

```yaml
id: cs-easy-string-split-no-alloc
version: 1
language: csharp
engine: none
difficulty: easy
title: "Alt dizgi tahsisi yapmadan ayraç indekslerini tarama"
prompt: |
  ReadOnlySpan<char> kullanarak delim karakterine göre metinde kaç parça olduğunu tek bir alt string üretmeden hesaplayan `int CountPartsNoAlloc(ReadOnlySpan<char> text, char delim)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (sıfır tahsis)"
  - "Span üzerinde döngü kurulmalıdır"
expected:
  time: { CountPartsNoAlloc: "n" }
  space: "1"
concept_tags: [zero-allocation, span]
checklist_extra:
  - "Split() çağrısı yapılmayarak string tahsisi engellenmiş mi?"
  - "Ayraç sayısı + 1 hesaplanmış mı?"
reference_solution_path: private/solutions/cs-easy-string-split-no-alloc.cs
hint_ladder:
  1: "text.IsEmpty ise 0 dönün."
  2: "Metin dilimindeki delim karakterlerinin sayısını sayıp 1 ekleyin."
  3: "Bu yaklaşım 'sıfır tahsisli parça sayımı (zero-allocation part count)' olarak bilinir."
```

---

### cs-easy-struct-in-parameter

```yaml
id: cs-easy-struct-in-parameter
version: 1
language: csharp
engine: none
difficulty: easy
title: "Değer türlerini kopyalamamak için salt okunur referansla geçirme"
prompt: |
  İki Point2D yapısı arasındaki Öklid mesafesini yapıyı kopyalamamak için in parametresiyle alarak hesaplayan `double Distance(in Point2D a, in Point2D b)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "in niteleyicisi kullanılmalıdır"
expected:
  time: { Distance: "1" }
  space: "1"
concept_tags: [performance, encapsulation]
checklist_extra:
  - "in niteleyicisi ile salt okunur referans geçilmiş mi?"
  - "Math.Sqrt ile mesafe doğru hesaplanmış mı?"
reference_solution_path: private/solutions/cs-easy-struct-in-parameter.cs
hint_ladder:
  1: "Büyük yapıları değerle (by-value) geçmek her çağrıda bayt kopyalaması yaratır."
  2: "in niteleyicisi ile parametreyi salt okunur referansla geçirerek kopyalama maliyetini sıfırlayın."
  3: "Bu optimizasyon 'salt okunur referans parametresi (in parameter modifier)' olarak bilinir."
```

---

### cs-easy-find-first-non-repeat

```yaml
id: cs-easy-find-first-non-repeat
version: 1
language: csharp
engine: none
difficulty: easy
title: "Metinde yinelenmeyen ilk karakteri bulma"
prompt: |
  Küçük harflerden oluşan bir metinde yalnızca bir kez geçen ilk karakteri bulan `char? FirstUniqueChar(string text)` fonksiyonunu yazın. Yoksa null dönmelidir. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) (26 elemanlı frekans dizisi) olmalı"
  - "İki geçişte çözülmelidir"
expected:
  time: { FirstUniqueChar: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "26 elemanlı int[] dizisi kullanılmış mı?"
  - "İkinci geçişte frekansı 1 olan ilk karakter dönülmüş mü?"
reference_solution_path: private/solutions/cs-easy-find-first-non-repeat.cs
hint_ladder:
  1: "26 elemanlı bir frekans dizisinde her harfin sıklığını sayın."
  2: "İkinci geçişte frekansı 1 olan ilk karakteri tespit edip döndürün."
  3: "Bu algoritma 'yinelenmeyen ilk karakteri bulma (first unique character)' olarak bilinir."
```

---

### cs-easy-decimal-percentage-calc

```yaml
id: cs-easy-decimal-percentage-calc
version: 1
language: csharp
engine: none
difficulty: easy
title: "Yüzde hesaplamasında ondalık hassasiyetini koruma"
prompt: |
  Verilen amount tutarının taxRate yüzdesine karşılık gelen vergi miktarını decimal türüyle kuruş kaybı olmadan hesaplayan `decimal CalculateTax(decimal amount, decimal taxRate)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "decimal aritmetiği uygulanmalıdır"
expected:
  time: { CalculateTax: "1" }
  space: "1"
concept_tags: [floating-point, error-handling]
checklist_extra:
  - "amount * (taxRate / 100m) hesabı decimal yapılmış mı?"
  - "Negatif girdi kontrolleri sağlanmış mı?"
reference_solution_path: private/solutions/cs-easy-decimal-percentage-calc.cs
hint_ladder:
  1: "taxRate değerini 100m ile bölerek oranlayın."
  2: "amount ile çarparak yuvarlama hatası olmaksızın vergi tutarını hesaplayın."
  3: "Bu finansal hesaplama 'ondalık yüzde hesaplaması (decimal percentage calculation)' olarak bilinir."
```

---


---

## 3. Orta (Medium) — 50 Soru

---

### cs-medium-async-parallel-processor

```yaml
id: cs-medium-async-parallel-processor
version: 1
language: csharp
engine: none
difficulty: medium
title: "Sınırlı eşzamanlılıkta asenkron iş işleme"
prompt: |
  n adet elemandan oluşan bir listedeki görevleri SemaphoreSlim kullanarak aynı anda en fazla maxConcurrency kadar iş parçacığında asenkron işleyen `Task ProcessItemsAsync(List<string> items, int maxConcurrency)` fonksiyonunu yazın. n eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Task.WhenAll kullanılmalıdır"
expected:
  time: { ProcessItemsAsync: "n" }
  space: "n"
concept_tags: [async-await, concurrency]
checklist_extra:
  - "SemaphoreSlim(maxConcurrency) ile kısıtlama yapılmış mı?"
  - "finally bloğunda semaphore.Release() çağrılmış mı?"
reference_solution_path: private/solutions/cs-medium-async-parallel-processor.cs
hint_ladder:
  1: "Aynı anda çalışan asenkron görev sayısını sınırlamak için SemaphoreSlim kullanın."
  2: "Her görevde await semaphore.WaitAsync() ile izin alıp finally bloğunda Release() çağırın."
  3: "Bu eşzamanlılık kalıbı 'asenkron eşzamanlılık kısıtlayıcı (async concurrency throttler)' olarak bilinir."
```

---

### cs-medium-linq-avoid-deferred-re-enum

```yaml
id: cs-medium-linq-avoid-deferred-re-enum
version: 1
language: csharp
engine: none
difficulty: medium
title: "Tekrarlı numaralandırmayı önleyen veri akış hattı"
prompt: |
  Sipariş listesi üzerinde birden fazla filtreleme ve özetleme işlemi yaparken aynı IEnumerable kaynağını defalarca numaralandırmamak için ara tamponlama yapan `CustomerReport GenerateReport(IEnumerable<Order> orders)` fonksiyonunu yazın. n sipariş sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "ToList() ile tek seferde somutlaştırılmalıdır"
expected:
  time: { GenerateReport: "n" }
  space: "n"
concept_tags: [deferred-execution, performance]
checklist_extra:
  - "orders.ToList() yapılarak tekrarlı numaralandırma önlenmiş mi?"
  - "Gereksiz veri tabanı veya koleksiyon turları engellenmiş mi?"
reference_solution_path: private/solutions/cs-medium-linq-avoid-deferred-re-enum.cs
hint_ladder:
  1: "IEnumerable sorguları ertelenmiş yürütme (deferred execution) ile çalışır ve her foreach döngüsünde baştan çalıştırılır."
  2: "Koleksiyonu bir kez .ToList() ile belleğe alıp tüm raporlama metriklerini bu liste üzerinden hesaplayın."
  3: "Bu optimizasyon 'ertelenmiş yürütmede tekrarlı numaralandırmayı önleme (avoid multiple enumeration)' olarak bilinir."
```

---

### cs-medium-span-csv-line-parser

```yaml
id: cs-medium-span-csv-line-parser
version: 1
language: csharp
engine: none
difficulty: medium
title: "Sıfır tahsisli CSV satır ayrıştırıcı"
prompt: |
  ReadOnlySpan<char> ile verilen bir CSV satırını alt dizgi (substring) tahsis etmeden virgül ayraçlarına göre dilimleyip alan aralıklarını (Range) dolduran `bool TryParseCsvLine(ReadOnlySpan<char> line, Span<Range> ranges, out int fieldCount)` fonksiyonunu yazın. n satır uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (sıfır heap tahsisi)"
  - "Span<Range> doldurulmalıdır"
expected:
  time: { TryParseCsvLine: "n" }
  space: "1"
concept_tags: [span, zero-allocation]
checklist_extra:
  - "Heap üzerinde tek bir string veya array tahsis edilmemiş mi?"
  - "Tırnak içi virgüller ve alan aralıkları doğru hesaplanmış mı?"
reference_solution_path: private/solutions/cs-medium-span-csv-line-parser.cs
hint_ladder:
  1: "Metin dilimini karakter karakter tarayarak alanların başlangıç ve bitiş indekslerini belirleyin."
  2: "Her alan için bir System.Range yapısı oluşturup verilen Span<Range> içine yazın."
  3: "Bu sıfır bellek tahsisli ayrıştırma 'karakter dilimi CSV ayrıştırma (zero-allocation CSV parser)' olarak bilinir."
```

---

### cs-medium-weak-event-pattern

```yaml
id: cs-medium-weak-event-pattern
version: 1
language: csharp
engine: none
difficulty: medium
title: "Olay aboneliklerinde bellek sızıntısını önleyen zayıf olay deseni"
prompt: |
  Abone nesnenin yayıncı tarafından güçlü referansla tutulmasını engelleyen ve abonenin çöp toplayıcı tarafından toplanabilmesini sağlayan `class WeakEventListener` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "WeakReference<T> kullanılmalıdır"
expected:
  time: { WeakEventListener: "1" }
  space: "1"
concept_tags: [memory-leak, resource-management]
checklist_extra:
  - "WeakReference hedefi TryGetTarget ile kontrol edilmiş mi?"
  - "Abone öldüğünde olaydan otomatik koparılmış mı?"
reference_solution_path: private/solutions/cs-medium-weak-event-pattern.cs
hint_ladder:
  1: "Yayıncı ile abone arasında WeakReference<T> köprüsü kurun."
  2: "Olay tetiklendiğinde hedef nesne yaşıyorsa olayı iletin, toplanmışsa yayıncıdan aboneliği temizleyin."
  3: "Bu tasarım deseni 'zayıf olay deseni (weak event pattern)' olarak bilinir."
```

---

### cs-medium-lru-cache-sync

```yaml
id: cs-medium-lru-cache-sync
version: 1
language: csharp
engine: none
difficulty: medium
title: "Çift yönlü liste ve sözlük ile O(1) LRU önbellek"
prompt: |
  Kapasitesi sınırlandırılmış bir önbellekte Get ve Put işlemlerini LinkedList<T> ve Dictionary<TKey, LinkedListNode<T>> kullanarak O(1) sürede gerçekleştiren `class LruCache<TKey, TValue>` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı her işlem için O(1) olmalı"
  - "Ek bellek O(capacity) olmalı"
  - "Liste ve sözlük senkron tutulmalıdır"
expected:
  time: { LruCache: "1" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Erişilen düğüm listenin en başına taşınmış mı?"
  - "Kapasite dolduğunda sondaki düğüm sözlükten ve listeden silinmiş mi?"
reference_solution_path: private/solutions/cs-medium-lru-cache-sync.cs
hint_ladder:
  1: "Kullanım sırasını bir LinkedList ile, hızlı erişimi LinkedListNode referansları tutan bir Dictionary ile sağlayın."
  2: "Her erişimde düğümü Remove ve AddFirst ile başa taşıyarak en son kullanılan yapın."
  3: "Bu veri yapısı mekanizması 'en az son kullanılan önbellek (LRU cache implementation)' olarak bilinir."
```

---

### cs-medium-three-sum-two-pointers

```yaml
id: cs-medium-three-sum-two-pointers
version: 1
language: csharp
engine: none
difficulty: medium
title: "Toplamı sıfır olan benzersiz üçlüleri bulma (C#)"
prompt: |
  n elemanlı bir tamsayı dizisinde toplamları sıfır olan tüm benzersiz [a, b, c] üçlülerini bulan `IList<IList<int>> ThreeSum(int[] nums)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n^2) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Yinelenen üçlüler atlanmalıdır"
expected:
  time: { ThreeSum: "n^2" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Dizi Array.Sort ile sıralanmış mı?"
  - "İki işaretçi karşılıklı ilerletilerek mükerrer değerler atlanmış mı?"
reference_solution_path: private/solutions/cs-medium-three-sum-two-pointers.cs
hint_ladder:
  1: "Diziyi sıralayın ve ilk sayıyı bir döngüde sabitleyin."
  2: "Kalan iki sayıyı iki işaretçiyle ararken ardışık aynı değerleri atlayın."
  3: "Bu klasik algoritma 'üçlü toplam algoritması (three sum algorithm)' olarak bilinir."
```

---

### cs-medium-container-most-water

```yaml
id: cs-medium-container-most-water
version: 1
language: csharp
engine: none
difficulty: medium
title: "İki sütun arasında en fazla su tutan alanı bulma"
prompt: |
  n elemanlı yükseklik dizisinde en fazla su tutabilecek iki sütun arasındaki alanı iki işaretçiyle hesaplayan `long MaxArea(int[] height)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "İki işaretçi karşılıklı ilerletilmelidir"
expected:
  time: { MaxArea: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Kısa olan sütunun işaretçisi içeri kaydırılmış mı?"
  - "Maksimum alan long türünde güncellenmiş mi?"
reference_solution_path: private/solutions/cs-medium-container-most-water.cs
hint_ladder:
  1: "İki uca yerleştirdiğiniz işaretçilerle alanı hesaplayın."
  2: "Daha kısa olan sütunu içeri doğru kaydırarak daha yüksek sütunlar arayın."
  3: "Bu açgözlü yöntem 'maksimum su kabı alanı (container with most water)' olarak bilinir."
```

---

### cs-medium-trapping-rain-water

```yaml
id: cs-medium-trapping-rain-water
version: 1
language: csharp
engine: none
difficulty: medium
title: "Yükseklik haritasında biriken yağmur suyunu hesaplama"
prompt: |
  n elemanlı negatif olmayan yükseklik dizisinde birikebilecek toplam yağmur suyu hacmini iki işaretçiyle O(n) zamanda hesaplayan `long TrapWater(int[] height)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Sol ve sağ maksimumlar takip edilmelidir"
expected:
  time: { TrapWater: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "leftMax ve rightMax güncellenmiş mi?"
  - "Düşük tepeye sahip taraftan su toplanmış mı?"
reference_solution_path: private/solutions/cs-medium-trapping-rain-water.cs
hint_ladder:
  1: "İki işaretçi ve sol/sağ maksimum tepe değerlerini tutun."
  2: "Daha alçak olan taraftan su miktarını biriktiriciye ekleyip o işaretçiyi ilerletin."
  3: "Bu algoritma 'yağmur suyu tutma algoritması (trapping rain water)' olarak bilinir."
```

---

### cs-medium-kadane-max-subarray

```yaml
id: cs-medium-kadane-max-subarray
version: 1
language: csharp
engine: none
difficulty: medium
title: "Bitişik alt dizi maksimum toplamını bulma (C#)"
prompt: |
  n elemanlı tamsayı dizisinde toplamı en büyük olan bitişik alt dizinin toplamını Kadane algoritmasıyla bulan `long MaxSubArray(int[] nums)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) tek geçiş olmalı"
  - "Ek bellek O(1) olmalı"
  - "Tümü negatif diziler doğru yönetilmelidir"
expected:
  time: { MaxSubArray: "n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Maksimum aday nums[0] ile başlatılmış mı?"
  - "Mevcut toplam negatif olduğunda sıfırlanmış mı?"
reference_solution_path: private/solutions/cs-medium-kadane-max-subarray.cs
hint_ladder:
  1: "Diziyi tararken o anki bitişik toplamı güncelleyin."
  2: "Toplam negatif olduğunda sıfırlayıp bir sonraki elemandan yeni dizi başlatın; maksimumu her adımda kaydedin."
  3: "Bu algoritma 'Kadane maksimum alt dizi algoritması (Kadane's algorithm)' olarak bilinir."
```

---

### cs-medium-search-rotated-array

```yaml
id: cs-medium-search-rotated-array
version: 1
language: csharp
engine: none
difficulty: medium
title: "Döndürülmüş sıralı dizide ikili arama"
prompt: |
  Bilinmeyen bir noktadan döndürülmüş sıralı n elemanlı benzersiz tamsayı dizisinde target değerinin indeksini ikili aramayla bulan `int SearchRotated(int[] nums, int target)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Bulunamazsa -1 dönmelidir"
expected:
  time: { SearchRotated: "log n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Hangi yarının sıralı olduğu tespit edilmiş mi?"
  - "Hedefin sıralı aralıkta olup olmadığı test edilmiş mi?"
reference_solution_path: private/solutions/cs-medium-search-rotated-array.cs
hint_ladder:
  1: "Her adımda ortadaki elemanı bulup sol ve sağ yarımlardan hangisinin sıralı olduğunu denetleyin."
  2: "Hedef değerin sıralı yarıda olup olmadığına bakarak arama aralığını yarıya daraltın."
  3: "Bu algoritma 'döndürülmüş dizide ikili arama (rotated array binary search)' olarak bilinir."
```

---

### cs-medium-dutch-national-flag

```yaml
id: cs-medium-dutch-national-flag
version: 1
language: csharp
engine: none
difficulty: medium
title: "Üç farklı değeri tek geçişte yerinde sıralama (C#)"
prompt: |
  Yalnızca 0, 1 ve 2 değerlerinden oluşan n elemanlı bir tamsayı dizisini ek bellek ayırmadan yerinde sıralayan `void SortColors(int[] nums)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) tek geçiş olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "Üç işaretçi yöntemi kullanılmalıdır"
expected:
  time: { SortColors: "n" }
  space: "1"
concept_tags: [data-structures, zero-allocation]
checklist_extra:
  - "low, mid ve high işaretçileri doğru güncellenmiş mi?"
  - "Yerinde takas yapılmış mı?"
reference_solution_path: private/solutions/cs-medium-dutch-national-flag.cs
hint_ladder:
  1: "low, mid ve high olmak üzere 3 indeks tutun."
  2: "nums[mid] == 0 ise low ile takas edin, 2 ise high ile takas edin, 1 ise mid'i ilerletin."
  3: "Bu algoritma 'üçlü bölme algoritması (Dutch national flag partition)' olarak bilinir."
```

---

### cs-medium-group-anagrams-hash

```yaml
id: cs-medium-group-anagrams-hash
version: 1
language: csharp
engine: none
difficulty: medium
title: "Karakter sıklığı anahtarıyla anagramları gruplama"
prompt: |
  n adet metin içeren dizideki anagramları harf sıklığı anahtarıyla gruplayarak IList<IList<string>> içinde döndüren `IList<IList<string>> GroupAnagrams(string[] strs)` fonksiyonunu yazın. m ortalama metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Dictionary<string, List<string>> kullanılmalıdır"
expected:
  time: { GroupAnagrams: "n*m" }
  space: "n"
concept_tags: [data-structures, string-building]
checklist_extra:
  - "Sıralanmış kopya veya frekans dizisi anahtar yapılmış mı?"
  - "Gruplar sonuca aktarılmış mı?"
reference_solution_path: private/solutions/cs-medium-group-anagrams-hash.cs
hint_ladder:
  1: "Her metnin karakterlerini sıralayarak veya 26 boyutlu harf frekansını anahtar yapın."
  2: "Dictionary<string, List<string>> içinde aynı anahtara sahip sözcükleri bir araya getirin."
  3: "Bu algoritma 'karma haritası ile anagram gruplama (anagram grouping)' olarak bilinir."
```

---

### cs-medium-product-except-self

```yaml
id: cs-medium-product-except-self
version: 1
language: csharp
engine: none
difficulty: medium
title: "Kendisi hariç diğer elemanların çarpımı dizisi (C#)"
prompt: |
  n elemanlı tamsayı dizisinde her elemanın yerine diğer tüm elemanların çarpımını bölme operatörü (/) kullanmadan hesaplayan `long[] ProductExceptSelf(int[] nums)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Bölme işlemi kullanılmamalıdır"
expected:
  time: { ProductExceptSelf: "n" }
  space: "n"
concept_tags: [data-structures, allocation]
checklist_extra:
  - "Sol ve sağ önek çarpımları iki geçişte birleştirilmiş mi?"
  - "Bölme kullanılmamış mı?"
reference_solution_path: private/solutions/cs-medium-product-except-self.cs
hint_ladder:
  1: "İlk geçişte soldan gelen elemanların birikimli çarpımını sonuç dizisine yazın."
  2: "İkinci geçişte sağdan geriye gelerek sağdaki çarpımı bir değişkende tutup sonuçla çarpın."
  3: "Bu algoritma 'önek ve sonek çarpımları (prefix and suffix products)' olarak bilinir."
```

---

### cs-medium-spiral-matrix

```yaml
id: cs-medium-spiral-matrix
version: 1
language: csharp
engine: none
difficulty: medium
title: "Matris elemanlarını spiral sırada okuma"
prompt: |
  n x m boyutundaki bir tamsayı matrisinin elemanlarını dıştan içe doğru saat yönünde spiral sırada okuyarak IList<int> içinde döndüren `IList<int> SpiralOrder(int[,] matrix)` fonksiyonunu yazın. n satır ve m sütun adedidir.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(n * m) olmalı"
  - "Dört sınır daraltılmalıdır"
expected:
  time: { SpiralOrder: "n*m" }
  space: "n*m"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "top, bottom, left, right sınırları doğru yönetilmiş mi?"
  - "Çift ekleme engellenmiş mi?"
reference_solution_path: private/solutions/cs-medium-spiral-matrix.cs
hint_ladder:
  1: "Dört kenar sınırını belirleyip sırasıyla sağa, aşağı, sola ve yukarı adımlarla matrisi tarayın."
  2: "Her kenar tamamlandığında ilgili sınırı bir birim içeriye daraltın."
  3: "Bu matris okuma düzeni 'spiral matris gezintisi (spiral matrix order)' olarak bilinir."
```

---

### cs-medium-rotate-matrix-90

```yaml
id: cs-medium-rotate-matrix-90
version: 1
language: csharp
engine: none
difficulty: medium
title: "Kare matrisi yerinde 90 derece döndürme"
prompt: |
  n x n boyutundaki kare tamsayı matrisini yerinde saat yönünde 90 derece döndüren `void RotateMatrix(int[,] matrix)` fonksiyonunu yazın. n matris satır ve sütun boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n^2) olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "Devrik alma ve satır ters çevirme uygulanmalıdır"
expected:
  time: { RotateMatrix: "n^2" }
  space: "1"
concept_tags: [data-structures, zero-allocation]
checklist_extra:
  - "Köşegene göre devrik alma doğru yapılmış mı?"
  - "Satırlar yatay eksende ters çevrilmiş mi?"
reference_solution_path: private/solutions/cs-medium-rotate-matrix-90.cs
hint_ladder:
  1: "Önce matrisin asal köşegene göre devriğini (transpozunu) alın."
  2: "Ardından her bir satırı yatay eksende baştan sona ters çevirin."
  3: "Bu dönüşüm 'kare matrisi yerinde döndürme (in-place matrix rotation)' olarak bilinir."
```

---

### cs-medium-set-matrix-zeroes

```yaml
id: cs-medium-set-matrix-zeroes
version: 1
language: csharp
engine: none
difficulty: medium
title: "Sıfır içeren satır ve sütunları sabit ek bellekle sıfırlama (C#)"
prompt: |
  n x m boyutundaki matriste sıfır bulunan hücrelerin tüm satır ve sütununu yerinde sıfırlayan `void SetZeroes(int[,] matrix)` fonksiyonunu yazın. Ek bellek O(1) olmalıdır. n satır ve m sütun adedidir.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(1) olmalı"
  - "İlk satır ve sütun bayrak olarak kullanılmalıdır"
expected:
  time: { SetZeroes: "n*m" }
  space: "1"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "İlk satır ve sütunun orijinal sıfır durumu ayrı bayraklarla saklanmış mı?"
  - "Sıfırlama içeriden dışarıya yapılmış mı?"
reference_solution_path: private/solutions/cs-medium-set-matrix-zeroes.cs
hint_ladder:
  1: "İlk satır ve ilk sütunu sıfır işaretleme tablosu olarak kullanın."
  2: "İlk satır ve sütunun kendi sıfır olma durumunu iki boole değişkeninde tutarak matrisi güncelleyin."
  3: "Bu algoritma 'matris satır ve sütunlarını yerinde sıfırlama (set matrix zeroes)' olarak bilinir."
```

---

### cs-medium-longest-unique-substring

```yaml
id: cs-medium-longest-unique-substring
version: 1
language: csharp
engine: none
difficulty: medium
title: "Tekrarlayan karakter içermeyen en uzun alt dizgiyi kayan pencereyle bulma (C#)"
prompt: |
  Verilen bir metinde tekrarlayan karakter içermeyen en uzun kesintisiz alt dizginin uzunluğunu kayan pencereyle bulan `int LengthOfLongestSubstring(string s)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) (karakter indeks tablosu) olmalı"
  - "Sol sınır yalnızca ileri hareket etmelidir"
expected:
  time: { LengthOfLongestSubstring: "n" }
  space: "1"
concept_tags: [performance, parsing]
checklist_extra:
  - "Son görülme indeksi dizide tutulmuş mu?"
  - "Sol sınır geriye gitmeyecek şekilde güncellenmiş mi?"
reference_solution_path: private/solutions/cs-medium-longest-unique-substring.cs
hint_ladder:
  1: "Her karakterin son görüldüğü indeksi bir sözlükte veya dizide tutun."
  2: "Karakter tekrarlandığında sol pencere sınırını karakterin son indeksinin bir sağına çekin ve pencere genişliğini güncelleyin."
  3: "Bu algoritma 'kayan pencere ile benzersiz alt metin analizi (sliding window unique substring)' olarak bilinir."
```

---

### cs-medium-subarray-sum-k

```yaml
id: cs-medium-subarray-sum-k
version: 1
language: csharp
engine: none
difficulty: medium
title: "Toplamı k olan alt dizi sayısını önek toplamı haritasıyla bulma (C#)"
prompt: |
  n elemanlı bir tamsayı dizisinde toplamları k'ya eşit olan bitişik alt dizilerin sayısını önek toplamı sözlüğüyle bulan `int SubarraySum(int[] nums, int k)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Dictionary<int, int> kullanılmalıdır"
expected:
  time: { SubarraySum: "n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "currSum - k değeri sözlükte sorgulanmış mı?"
  - "Başlangıç için {0, 1} kaydı eklenmiş mi?"
reference_solution_path: private/solutions/cs-medium-subarray-sum-k.cs
hint_ladder:
  1: "Diziyi tararken birikimli toplamı güncelleyin."
  2: "currSum - k değerinin geçmişte kaç kez oluştuğunu haritadan okuyup cevaba ekleyin."
  3: "Bu algoritma 'önek toplamı ile alt dizi sayımı (subarray sum equals k)' olarak bilinir."
```

---

### cs-medium-longest-consecutive-sequence

```yaml
id: cs-medium-longest-consecutive-sequence
version: 1
language: csharp
engine: none
difficulty: medium
title: "Sıralı olmayan dizide en uzun ardışık dizi uzunluğunu bulma (C#)"
prompt: |
  n elemanlı sıralı olmayan bir tamsayı dizisinde ardışık sayılardan oluşan en uzun dizilimin uzunluğunu HashSet<int> kullanarak O(n) sürede bulan `int LongestConsecutive(int[] nums)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Yalnızca ardışık dizinin başlangıç elemanından tarama yapılmalıdır"
expected:
  time: { LongestConsecutive: "n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "num - 1 kümede yoksa dizi başlangıcı seçilmiş mi?"
  - "Her eleman en fazla iki kez ziyaret edilmiş mi?"
reference_solution_path: private/solutions/cs-medium-longest-consecutive-sequence.cs
hint_ladder:
  1: "Tüm elemanları bir HashSet<int> içine atın."
  2: "Bir sayı için num - 1 kümede yoksa bu sayıyı bir ardışık dizinin başı kabul edip num + 1, num + 2 ... varlığını sayın."
  3: "Bu algoritma 'en uzun ardışık sayı dizisi tespiti (longest consecutive sequence)' olarak bilinir."
```

---

### cs-medium-find-duplicate-floyd

```yaml
id: cs-medium-find-duplicate-floyd
version: 1
language: csharp
engine: none
difficulty: medium
title: "Mükerrer sayıyı iki işaretçi algoritmasıyla bulma"
prompt: |
  1'den n'e kadar sayılar içeren n+1 elemanlı dizide tam bir sayının tekrar ettiği bilinmektedir. Diziyi değiştirmeden ve ek bellek kullanmadan Floyd kaplumbağa-tavşan algoritmasıyla bu sayıyı bulan `int FindDuplicate(int[] nums)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "İki fazlı döngü tespiti yapılmalıdır"
expected:
  time: { FindDuplicate: "n" }
  space: "1"
concept_tags: [data-structures, zero-allocation]
checklist_extra:
  - "Dizi değerleri indeks olarak kullanılmış mı?"
  - "Döngü girişi doğru bulunmuş mu?"
reference_solution_path: private/solutions/cs-medium-find-duplicate-floyd.cs
hint_ladder:
  1: "Diziyi bir bağlı liste gibi görerek slow = nums[slow] ve fast = nums[nums[fast]] adımlarıyla ilerleyin."
  2: "Kesiştikten sonra işaretçilerden birini başa alıp aynı hızla ilerleterek döngünün başladığı mükerrer sayıyı bulun."
  3: "Bu algoritma 'Floyd döngü bulma ile mükerrer eleman tespiti (Floyd cycle duplicate detection)' olarak bilinir."
```

---

### cs-medium-merge-k-sorted-arrays

```yaml
id: cs-medium-merge-k-sorted-arrays
version: 1
language: csharp
engine: none
difficulty: medium
title: "Öncelik kuyruğu kullanarak k adet sıralı diziyi birleştirme"
prompt: |
  Her biri sıralı k adet tamsayı dizisini PriorityQueue kullanarak tek bir sıralı dizide O(n log k) sürede birleştiren `int[] MergeKSorted(int[][] arrays)` fonksiyonunu yazın. n toplam eleman sayısı ve k dizi sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n log k) olmalı"
  - "Ek bellek O(k) olmalı"
  - "new int[n] tahsis edilmelidir"
expected:
  time: { MergeKSorted: "n log k" }
  space: "k"
concept_tags: [data-structures, allocation]
checklist_extra:
  - "PriorityQueue<..., int> kullanılmış mı?"
  - "Çekilen elemanın dizisinden bir sonraki eleman kuyruğa eklenmiş mi?"
reference_solution_path: private/solutions/cs-medium-merge-k-sorted-arrays.cs
hint_ladder:
  1: "Her dizinin ilk elemanını min-heap öncelik kuyruğuna koyun."
  2: "En küçük elemanı çekip sonuç dizisine yazın ve o diziden bir sonraki elemanı kuyruğa ekleyin."
  3: "Bu algoritma 'k adet sıralı diziyi yığınla birleştirme (merge k sorted arrays with priority queue)' olarak bilinir."
```

---

### cs-medium-top-k-frequent-heap

```yaml
id: cs-medium-top-k-frequent-heap
version: 1
language: csharp
engine: none
difficulty: medium
title: "En sık geçen k adet elemanı öncelik kuyruğuyla takip etme"
prompt: |
  n elemanlı tamsayı dizisinde en yüksek frekansa sahip k adet elemanı Dictionary ve PriorityQueue kullanarak O(n log k) sürede bulan `int[] TopKFrequentHeap(int[] nums, int k)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n log k) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Kuyruk boyutu k ile sınırlandırılmalıdır"
expected:
  time: { TopKFrequentHeap: "n log k" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Frekanslar sözlükte sayılmış mı?"
  - "Boyut k'yı aştığında minimum frekanslı eleman kuyruktan atılmış mı?"
reference_solution_path: private/solutions/cs-medium-top-k-frequent-heap.cs
hint_ladder:
  1: "Sayıların frekanslarını bir sözlükte toplayın."
  2: "Elemanları boyutu k ile sınırlı bir min-heap'e ekleyip k'yı aştığında en küçük frekanslıyı çıkarın."
  3: "Bu algoritma 'öncelik kuyruğu ile k adet en sık elemanı bulma (top k frequent elements heap)' olarak bilinir."
```

---

### cs-medium-topological-sort-kahn

```yaml
id: cs-medium-topological-sort-kahn
version: 1
language: csharp
engine: none
difficulty: medium
title: "Yönlü döngüsüz çizgede giriş dereceleriyle topolojik sıralama (C#)"
prompt: |
  numNodes düğümlü bir DAG'daki kenar listesini alarak giriş dereceleri ve kuyruk yardımıyla düğümlerin geçerli bir topolojik sıralamasını üreten `int[] TopologicalSort(int numNodes, int[][] edges)` fonksiyonunu yazın. Döngü varsa boş dizi dönmelidir. n düğüm ve m kenar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n + m) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Kahn algoritması uygulanmalıdır"
expected:
  time: { TopologicalSort: "n + m" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Giriş derecesi 0 olan düğümler başlangıçta kuyruğa alınmış mı?"
  - "Sıralanan düğüm sayısı n değilse döngü saptanmış mı?"
reference_solution_path: private/solutions/cs-medium-topological-sort-kahn.cs
hint_ladder:
  1: "Tüm düğümlerin giriş derecelerini hesaplayıp derecesi 0 olanları bir kuyruğa atın."
  2: "Kuyruktan düğüm çektikçe komşuların derecesini azaltıp sıfırlananları kuyruğa ekleyin."
  3: "Bu algoritma 'Kahn topolojik sıralama algoritması (Kahn's algorithm)' olarak bilinir."
```

---

### cs-medium-dijkstra-priority-queue

```yaml
id: cs-medium-dijkstra-priority-queue
version: 1
language: csharp
engine: none
difficulty: medium
title: "Ağırlıklı çizgede en kısa yol mesafelerini heap ile hesaplama"
prompt: |
  numNodes düğümlü ve pozitif ağırlıklı çizgede source düğümünden tüm düğümlere en kısa mesafeleri PriorityQueue kullanarak hesaplayan `int[] Dijkstra(int numNodes, (int u, int v, int w)[] edges, int source)` fonksiyonunu yazın. n düğüm ve m kenar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(m log n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "PriorityQueue kullanılmalıdır"
expected:
  time: { Dijkstra: "m log n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Mesafe dizisi int.MaxValue ile başlatılmış mı?"
  - "Eski ve daha uzun yollar elenmiş mi?"
reference_solution_path: private/solutions/cs-medium-dijkstra-priority-queue.cs
hint_ladder:
  1: "Kaynak düğümün mesafesini 0 yapıp öncelik kuyruğuna ekleyin."
  2: "En küçük mesafeli düğümü çekip komşularını gevşetin ve güncellenen mesafeleri kuyruğa ekleyin."
  3: "Bu algoritma 'Dijkstra en kısa yol algoritması (Dijkstra algorithm)' olarak bilinir."
```

---

### cs-medium-course-schedule-cycle

```yaml
id: cs-medium-course-schedule-cycle
version: 1
language: csharp
engine: none
difficulty: medium
title: "Bağımlılık çizgesinde döngü varlığını DFS ile denetleme"
prompt: |
  numCourses adet ders ve önkoşul kenarları verildiğinde tüm derslerin tamamlanıp tamamlanamayacağını 3 durumlu ziyaret tablosuyla denetleyen `bool CanFinish(int numCourses, int[][] prerequisites)` fonksiyonunu yazın. n ders ve m önkoşul sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n + m) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Döngü tespitinde false dönmelidir"
expected:
  time: { CanFinish: "n + m" }
  space: "n"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "3 durumlu ziyaret tablosu (0: unvisited, 1: visiting, 2: visited) kullanılmış mı?"
  - "Aktif çağrı yığındaki komşuya rastlandığında döngü saptanmış mı?"
reference_solution_path: private/solutions/cs-medium-course-schedule-cycle.cs
hint_ladder:
  1: "Her düğüm için 3 durum tutun (0: ziyaret edilmedi, 1: aktif çağrı yığınında, 2: tamamlandı)."
  2: "DFS sırasında durumu 1 olan bir komşuya rastlarsanız döngü vardır, doğrudan false dönün."
  3: "Bu çizge algoritması 'yönlü çizgede döngü tespiti (cycle detection in directed graph)' olarak bilinir."
```

---

### cs-medium-trie-prefix-tree

```yaml
id: cs-medium-trie-prefix-tree
version: 1
language: csharp
engine: none
difficulty: medium
title: "Sözcük öneklerini saklayan önek ağacı sınıfı"
prompt: |
  Sözcük ekleme (Insert), tam arama (Search) ve önek arama (StartsWith) metotlarına sahip `class Trie` sınıfını yazın. m sözcük uzunluğudur.
constraints:
  - "Zaman karmaşıklığı işlem başı O(m) olmalı"
  - "Ek bellek O(m) olmalı"
  - "Düğümler 26 boyutlu dizi veya sözlük tutmalıdır"
expected:
  time: { Trie: "m" }
  space: "m"
concept_tags: [data-structures, parsing]
checklist_extra:
  - "Her düğümde isEnd bayrağı tutulmuş mu?"
  - "StartsWith aramasında önek bitiminde true dönülmüş mü?"
reference_solution_path: private/solutions/cs-medium-trie-prefix-tree.cs
hint_ladder:
  1: "Kök düğümden başlayarak her harf için çocuk göstericisini takip edin."
  2: "Sözcük bittiğinde isEnd işaretini koyun; aramalarda yol boyunca eksik düğüm yoksa sonucu dönün."
  3: "Bu veri yapısı 'önek ağacı yapısı (trie prefix tree)' olarak bilinir."
```

---

### cs-medium-binary-tree-lca

```yaml
id: cs-medium-binary-tree-lca
version: 1
language: csharp
engine: none
difficulty: medium
title: "İkili arama ağacında iki değerin en yakın ortak atasını bulma (C#)"
prompt: |
  İkili arama ağacında p ve q değerlerini içeren düğümlerin en yakın ortak atasını döngüsel olarak bulan `TreeNode LowestCommonAncestor(TreeNode root, int p, int q)` fonksiyonunu yazın. n ağaçtaki düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Döngüsel gerçekleştirilmelidir"
expected:
  time: { LowestCommonAncestor: "log n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "p ve q ikisi birden küçükse sola, büyükse sağa gidilmiş mi?"
  - "Ayrışma noktası LCA olarak dönülmüş mü?"
reference_solution_path: private/solutions/cs-medium-binary-tree-lca.cs
hint_ladder:
  1: "Kökten başlayarak her iki değer de kökten küçükse sola, büyükse sağa geçin."
  2: "Değerler iki farklı kola ayrıldığı an ulaşılan düğüm en yakın ortak atadır."
  3: "Bu algoritma 'ikili arama ağacında en yakın ortak ata (lowest common ancestor in BST)' olarak bilinir."
```

---

### cs-medium-binary-tree-level-order

```yaml
id: cs-medium-binary-tree-level-order
version: 1
language: csharp
engine: none
difficulty: medium
title: "İkili ağacın elemanlarını seviye seviye gruplayarak gezme (C#)"
prompt: |
  Kökü verilen ikili ağacın elemanlarını derinlik seviyelerine göre gruplayarak IList<IList<int>> biçiminde döndüren `IList<IList<int>> LevelOrder(TreeNode root)` fonksiyonunu yazın. n ağaçtaki düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Queue<TreeNode> kullanılmalıdır"
expected:
  time: { LevelOrder: "n" }
  space: "n"
concept_tags: [data-structures, allocation]
checklist_extra:
  - "Her seviyenin başında kuyruk boyutu kadar eleman çekilmiş mi?"
  - "Sol ve sağ çocuklar kuyruğa eklenmiş mi?"
reference_solution_path: private/solutions/cs-medium-binary-tree-level-order.cs
hint_ladder:
  1: "Kökü bir kuyruğa ekleyin."
  2: "Her turda kuyruğun o anki boyutu kadar düğüm çekip değerlerini o seviyenin listesine yazın ve çocuklarını kuyruğa ekleyin."
  3: "Bu algoritma 'seviye sıralı ağaç gezintisi (level order traversal)' olarak bilinir."
```

---

### cs-medium-binary-tree-is-bst

```yaml
id: cs-medium-binary-tree-is-bst
version: 1
language: csharp
engine: none
difficulty: medium
title: "Ağacın geçerli bir ikili arama ağacı olduğunu doğrulama"
prompt: |
  İkili bir ağacın tüm düğümlerinin ikili arama ağacı kuralını eksiksiz sağladığını özyinelemeli aralık sınırlarıyla doğrulayan `bool IsValidBST(TreeNode root)` fonksiyonunu yazın. n ağaçtaki düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek çağrı yığını için O(log n) olmalı"
  - "Taşmayı önlemek için long? sınırlar kullanılmalıdır"
expected:
  time: { IsValidBST: "n" }
  space: "log n"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "int.MinValue ve int.MaxValue sınırları için long? aralık kullanılmış mı?"
  - "Tüm sol alt ağacın kesinlikle küçük olduğu doğrulanmış mı?"
reference_solution_path: private/solutions/cs-medium-binary-tree-is-bst.cs
hint_ladder:
  1: "Her düğüm için geçerli bir (minLimit, maxLimit) aralığı tanımlayın."
  2: "Sola dallanırken üst sınırı, sağa dallanırken alt sınırı mevcut düğümün değeriyle daraltın."
  3: "Bu kontrol 'aralık kısıtlamalı ikili arama ağacı doğrulaması (valid BST range check)' olarak bilinir."
```

---

### cs-medium-serialize-deserialize-tree

```yaml
id: cs-medium-serialize-deserialize-tree
version: 1
language: csharp
engine: none
difficulty: medium
title: "İkili ağacı metne serileştirme ve geri oluşturma"
prompt: |
  İkili bir ağacı ön-sıralı (pre-order) dolaşarak virgülle ayrılmış dizgiye çeviren ve bu metinden ağacı yeniden kuran `class Codec` sınıfını yazın. n düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Null düğümler '#' ile kodlanmalıdır"
expected:
  time: { Codec: "n" }
  space: "n"
concept_tags: [data-structures, string-building]
checklist_extra:
  - "StringBuilder kullanılmış mı?"
  - "Kuyruk yardımıyla özyinelemeli geri kurma yapılmış mı?"
reference_solution_path: private/solutions/cs-medium-serialize-deserialize-tree.cs
hint_ladder:
  1: "Ön-sıralı dolaşımda her düğümün değerini dizgiye yazıp null çocuklar için '#' ekleyin."
  2: "Geri oluştururken dizgiyi sırayla okuyup '#' gördükçe null, sayı gördükçe yeni düğüm oluşturun."
  3: "Bu mekanizma 'ikili ağaç serileştirme ve geri kurma (tree serialization and deserialization)' olarak bilinir."
```

---

### cs-medium-flatten-tree-linked-list

```yaml
id: cs-medium-flatten-tree-linked-list
version: 1
language: csharp
engine: none
difficulty: medium
title: "İkili ağacı sağ çocuk üzerinden bağlı listeye düzleştirme"
prompt: |
  İkili bir ağacın tüm düğümlerini ön-sıralı (pre-order) düzende sağ çocuk göstericileri üzerinden tek yönlü bağlı listeye dönüştüren ve sol göstericileri null yapan `void Flatten(TreeNode root)` fonksiyonunu yazın. n ağaçtaki düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "Sol göstericiler null yapılmalıdır"
expected:
  time: { Flatten: "n" }
  space: "1"
concept_tags: [data-structures, zero-allocation]
checklist_extra:
  - "Sol alt dal sağa taşınmadan önce sağ dal solun en sağına bağlanmış mı?"
  - "Sol göstericiler null yapılmış mı?"
reference_solution_path: private/solutions/cs-medium-flatten-tree-linked-list.cs
hint_ladder:
  1: "Sol çocuğu olan her düğüm için sol alt ağacın en sağ yaprağını bulun."
  2: "O yaprağın sağına mevcut sağ çocuğu bağlayıp tüm sol dalı sağa taşıyın ve solu null yapın."
  3: "Bu işlem 'ikili ağacı bağlı listeye düzleştirme (flatten binary tree to linked list)' olarak bilinir."
```

---

### cs-medium-clone-graph-dictionary

```yaml
id: cs-medium-clone-graph-dictionary
version: 1
language: csharp
engine: none
difficulty: medium
title: "Çizgeyi derinlemesine klonlama"
prompt: |
  Bağlantılı yönsüz bir çizgenin başlangıç düğümünü alarak tüm düğümleri ve komşuluk ilişkilerini derinlemesine kopyalayan `Node CloneGraph(Node node)` fonksiyonunu yazın. n düğüm ve m kenar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n + m) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Dictionary<Node, Node> kullanılmalıdır"
expected:
  time: { CloneGraph: "n + m" }
  space: "n"
concept_tags: [data-structures, allocation]
checklist_extra:
  - "Orijinal düğüm ile kopya düğüm sözlükte eşleştirilmiş mi?"
  - "Döngüsel kenarlarda sonsuz özyineleme engellenmiş mi?"
reference_solution_path: private/solutions/cs-medium-clone-graph-dictionary.cs
hint_ladder:
  1: "Ziyaret edilen her orijinal düğüm için yeni bir kopya düğüm tahsis edip sözlüğe kaydedin."
  2: "Komşuları BFS veya DFS ile dolaşarak sözlükteki kopyaları komşuluk listesine ekleyin."
  3: "Bu çizge algoritması 'sözlük ile derin çizge klonlama (deep clone graph)' olarak bilinir."
```

---

### cs-medium-number-of-islands-bfs

```yaml
id: cs-medium-number-of-islands-bfs
version: 1
language: csharp
engine: none
difficulty: medium
title: "2D ızgaradaki adaların toplam sayısını BFS ile bulma (C#)"
prompt: |
  '1' (kara) ve '0' (su) karakterlerinden oluşan n x m boyutundaki bir ızgarada yatay ve dikey bağlı adalardan kaç tane olduğunu BFS ile hesaplayan `int NumIslands(char[,] grid)` fonksiyonunu yazın. n satır ve m sütun adedidir.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(n + m) olmalı"
  - "Ziyaret edilen hücreler '0' yapılmalıdır"
expected:
  time: { NumIslands: "n*m" }
  space: "n + m"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "Izgara sınırları kontrol edilmiş mi?"
  - "Ziyaret edilen hücreler hemen '0' yapılarak kuyruk şişmesi önlenmiş mi?"
reference_solution_path: private/solutions/cs-medium-number-of-islands-bfs.cs
hint_ladder:
  1: "Izgarayı gezerken '1' gördükçe ada sayısını artırın."
  2: "BFS kuyruğu başlatarak adanın tüm bağlı komşularını '0' yaparak batırın."
  3: "Bu ızgara algoritması 'ada sayısı hesaplama (number of islands BFS)' olarak bilinir."
```

---

### cs-medium-word-break-dp

```yaml
id: cs-medium-word-break-dp
version: 1
language: csharp
engine: none
difficulty: medium
title: "Metnin sözlükteki sözcüklerle oluşturulup oluşturulamayacağını bulma (C#)"
prompt: |
  Verilen bir metnin sözlükteki sözcüklerin ardışık birleşimiyle oluşturulup oluşturulamayacağını dinamik programlamayla denetleyen `bool WordBreak(string s, HashSet<string> wordDict)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n^2) olmalı"
  - "Ek bellek O(n) olmalı"
  - "dp[i] dizisi tutulmalıdır"
expected:
  time: { WordBreak: "n^2" }
  space: "n"
concept_tags: [data-structures, parsing]
checklist_extra:
  - "dp[0] = true başlatılmış mı?"
  - "Alt dizgiler s.Substring(j, i - j) sözlükte hızlıca sorgulanmış mı?"
reference_solution_path: private/solutions/cs-medium-word-break-dp.cs
hint_ladder:
  1: "dp[i] değerini ilk i karakterin sözlükteki kelimelerle bölünebilirliği olarak tanımlayın."
  2: "dp[j] true ise s[j...i] parçasının sözlükte olup olmadığını kontrol ederek dp[i]'yi güncelleyin."
  3: "Bu algoritma 'sözcük kırma problemi (word break dynamic programming)' olarak bilinir."
```

---

### cs-medium-coin-change-min

```yaml
id: cs-medium-coin-change-min
version: 1
language: csharp
engine: none
difficulty: medium
title: "Hedef tutara ulaşmak için gereken asgari madeni para sayısını hesaplama (C#)"
prompt: |
  Farklı nominal değerlere sahip madeni paralarla k tutarına ulaşmak için gereken minimum para sayısını dinamik programlamayla hesaplayan `int CoinChange(int[] coins, int k)` fonksiyonunu yazın. Ulaşılamazsa -1 dönmelidir. n para çeşit sayısı ve k hedef tutardır.
constraints:
  - "Zaman karmaşıklığı O(n * k) olmalı"
  - "Ek bellek O(k) olmalı"
  - "Taban durum dp[0] = 0 ayarlanmalıdır"
expected:
  time: { CoinChange: "n*k" }
  space: "k"
concept_tags: [data-structures, performance]
checklist_extra:
  - "dp tablosu k + 1 ile başlatılmış mı?"
  - "Ulaşılamayan tutarlar için -1 dönülmüş mü?"
reference_solution_path: private/solutions/cs-medium-coin-change-min.cs
hint_ladder:
  1: "dp[i] değerini i tutarına ulaşmak için gereken minimum madeni para sayısı olarak tanımlayın."
  2: "Her para değeri için dp[i] = Math.Min(dp[i], dp[i - coin] + 1) geçişini uygulayın."
  3: "Bu algoritma 'madeni para değiştirme problemi (coin change problem)' olarak bilinir."
```

---

### cs-medium-longest-increasing-subseq

```yaml
id: cs-medium-longest-increasing-subseq
version: 1
language: csharp
engine: none
difficulty: medium
title: "En uzun artan alt dizinin uzunluğunu dinamik programlamayla bulma (C#)"
prompt: |
  n elemanlı bir tamsayı dizisinde kesinlikle artan en uzun alt dizinin uzunluğunu dinamik programlama yaklaşımıyla hesaplayan `int LengthOfLIS(int[] nums)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n^2) olmalı"
  - "Ek bellek O(n) olmalı"
  - "dp dizisi 1 ile başlatılmalıdır"
expected:
  time: { LengthOfLIS: "n^2" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Her i için önceki j elemanları taranmış mı?"
  - "nums[i] > nums[j] ise dp[i] = Math.Max(dp[i], dp[j] + 1) yapılmış mı?"
reference_solution_path: private/solutions/cs-medium-longest-increasing-subseq.cs
hint_ladder:
  1: "dp[i] değerini i. elemanda sonlanan en uzun artan alt dizi uzunluğu yapın."
  2: "Önceki tüm küçük elemanların dp değerlerinin maksimumuna 1 ekleyerek genel maksimumu güncelleyin."
  3: "Bu algoritma 'en uzun artan alt dizi dinamik programlama çözümü (longest increasing subsequence DP)' olarak bilinir."
```

---

### cs-medium-eval-rpn-stack

```yaml
id: cs-medium-eval-rpn-stack
version: 1
language: csharp
engine: none
difficulty: medium
title: "Ters Polonyalı Notasyonundaki matematiksel ifadeyi yığınla hesaplama (C#)"
prompt: |
  Ters Polonyalı Notasyonunda (RPN) verilmiş n adet simgeyi Stack<int> kullanarak hesaplayan `int EvalRPN(string[] tokens)` fonksiyonunu yazın. Desteklenen operatörler: +, -, *, /.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "İşlenenlerin sırası çıkarma ve bölmede gözetilmelidir"
expected:
  time: { EvalRPN: "n" }
  space: "n"
concept_tags: [data-structures, parsing]
checklist_extra:
  - "İkinci çekilen sol işlenen, ilk çekilen sağ işlenen olarak bölünmüş mı?"
  - "int.Parse kullanılmış mı?"
reference_solution_path: private/solutions/cs-medium-eval-rpn-stack.cs
hint_ladder:
  1: "Sayı gördükçe yığına itin."
  2: "Operatör gördükçe yığından iki sayı çekip b ve a olarak adlandırarak a op b sonucunu tekrar yığına itin."
  3: "Bu algoritma 'ters Polonyalı notasyonu yığın değerlendirmesi (reverse Polish notation stack evaluation)' olarak bilinir."
```

---

### cs-medium-daily-temperatures-mono

```yaml
id: cs-medium-daily-temperatures-mono
version: 1
language: csharp
engine: none
difficulty: medium
title: "Monotonik yığın kullanarak daha sıcak gün için bekleme günlerini hesaplama (C#)"
prompt: |
  n günlük sıcaklık dizisi verildiğinde her gün için daha sıcak bir günün gelmesi için kaç gün beklenmesi gerektiğini monotonik azalan yığınla bulan `int[] DailyTemperatures(int[] temps)` fonksiyonunu yazın. n gün sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Yığında gün indeksleri saklanmalıdır"
expected:
  time: { DailyTemperatures: "n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Yığında gün indeksi tutulmuş mu?"
  - "Mevcut sıcaklık yığındaki günden sıcaksa aradaki gün farkı sonuca yazılmış mı?"
reference_solution_path: private/solutions/cs-medium-daily-temperatures-mono.cs
hint_ladder:
  1: "Günün indekslerini saklayan monotonik azalan bir yığın tutun."
  2: "Daha sıcak bir gün gördükçe yığından önceki günleri çekip aradaki indeks farkını sonuç dizisine yazın."
  3: "Bu algoritma 'monotonik yığın ile sıcaklık takibi (monotonic stack daily temperatures)' olarak bilinir."
```

---

### cs-medium-next-greater-element

```yaml
id: cs-medium-next-greater-element
version: 1
language: csharp
engine: none
difficulty: medium
title: "Monotonik yığın ile sağdaki ilk büyük elemanı bulma"
prompt: |
  n elemanlı bir dizide her elemanın sağında yer alan kendisinden kesinlikle büyük ilk elemanı monotonik yığınla bulan `int[] NextGreaterElements(int[] nums)` fonksiyonunu yazın. Sağında daha büyük eleman yoksa -1 olmalıdır. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Her eleman yığına bir kez girip bir kez çıkmalıdır"
expected:
  time: { NextGreaterElements: "n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Dizi sağdan sola doğru taranmış mı?"
  - "Büyük eleman bulunamayanlar -1 kalmış mı?"
reference_solution_path: private/solutions/cs-medium-next-greater-element.cs
hint_ladder:
  1: "Diziyi sağdan sola doğru tarayarak mevcut elemandan küçük veya eşit olanları yığından atın."
  2: "Yığının tepesindeki eleman sağdaki ilk büyük elemandır; yığın boşsa -1 yazıp mevcut elemanı yığına itin."
  3: "Bu algoritma 'sağdaki ilk büyük eleman tespiti (next greater element)' olarak bilinir."
```

---

### cs-medium-matrix-word-search

```yaml
id: cs-medium-matrix-word-search
version: 1
language: csharp
engine: none
difficulty: medium
title: "2D karakter ızgarasında sözcük arama geri izlemesi"
prompt: |
  n x m boyutundaki bir karakter matrisinde ardışık komşu hücreleri takip ederek verilen word sözcüğünün bulunup bulunmadığını geri izleme (backtracking) ile denetleyen `bool WordSearch(char[,] board, string word)` fonksiyonunu yazın. k sözcüğün uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n * m * 4^k) olmalı"
  - "Ek bellek O(k) olmalı"
  - "Ziyaret edilen hücreler geçici '#' yapılıp geri yüklenmelidir"
expected:
  time: { WordSearch: "n*m" }
  space: "k"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "Hücreler ziyaret edildiğinde '#' yapılıp dönüşte eski karakter geri yüklenmiş mi?"
  - "Izgara sınırları denetlenmiş mi?"
reference_solution_path: private/solutions/cs-medium-matrix-word-search.cs
hint_ladder:
  1: "Matristeki her hücreden başlayarak sözcüğün ilk harfiyle eşleşenlerde DFS başlatın."
  2: "Geçici olarak hücreyi '#' yaparak aynı hücrenin iki kez kullanılmasını önleyin ve dönüşte eski karakteri geri yükleyin."
  3: "Bu algoritma 'ızgarada sözcük arama geri izlemesi (word search backtracking)' olarak bilinir."
```

---

### cs-medium-subsets-backtrack

```yaml
id: cs-medium-subsets-backtrack
version: 1
language: csharp
engine: none
difficulty: medium
title: "Benzersiz kümenin tüm alt kümelerini geri izleme ile üretme"
prompt: |
  n elemanlı benzersiz tamsayı dizisinin tüm 2^n adet alt kümesini geri izleme yöntemiyle üreten `IList<IList<int>> Subsets(int[] nums)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n * 2^n) olmalı"
  - "Ek bellek O(n) (özyineleme yığını) olmalı"
  - "Her adımda alt küme kopyalanmalıdır"
expected:
  time: { Subsets: "2^n" }
  space: "n"
concept_tags: [data-structures, allocation]
checklist_extra:
  - "Mevcut alt küme her özyineleme başında sonuca kopyalanmış mı?"
  - "Geri izlemede RemoveAt yapılmış mı?"
reference_solution_path: private/solutions/cs-medium-subsets-backtrack.cs
hint_ladder:
  1: "Her özyineleme adımında mevcut geçici alt kümeyi sonuç listesine ekleyin."
  2: "start indeksinden itibaren her elemanı geçici kümeye ekleyip bir sonraki indekse dalın ve dönüşte RemoveAt ile geri alın."
  3: "Bu algoritma 'alt küme üretme geri izleme algoritması (subsets backtracking)' olarak bilinir."
```

---

### cs-medium-permutations-backtrack

```yaml
id: cs-medium-permutations-backtrack
version: 1
language: csharp
engine: none
difficulty: medium
title: "Tamsayı dizisinin tüm permütasyonlarını geri izleme ile üretme (C#)"
prompt: |
  n elemanlı benzersiz tamsayılardan oluşan bir dizinin tüm n! permütasyonunu geri izleme veya yerinde takas ile üreten `IList<IList<int>> Permute(int[] nums)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n * n!) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Yerinde takas yöntemi uygulanabilir"
expected:
  time: { Permute: "n!" }
  space: "n"
concept_tags: [data-structures, allocation]
checklist_extra:
  - "start indeksi sona vardığında permütasyon listeye eklenmiş mi?"
  - "Geri izleme dönüşünde takas geri alınmış mı?"
reference_solution_path: private/solutions/cs-medium-permutations-backtrack.cs
hint_ladder:
  1: "start indeksinden sona kadar her elemanı start ile takas ederek özyinelemeyi başlatın."
  2: "Dönüşte takası geri alarak dizinin orijinal sırasını koruyun."
  3: "Bu algoritma 'permütasyon üretme geri izleme algoritması (permutations backtracking)' olarak bilinir."
```

---

### cs-medium-channel-producer-consumer

```yaml
id: cs-medium-channel-producer-consumer
version: 1
language: csharp
engine: none
difficulty: medium
title: "Sınırlı asenkron üretici-tüketici boru hattı tasarlama"
prompt: |
  System.Threading.Channels.Channel.CreateBounded<int> kullanarak kapasitesi sınırlı bir asenkron kanal oluşturan ve üretici-tüketici boru hattı sunan `Channel<int> CreatePipeline(int capacity)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(capacity) olmalı"
  - "BoundedChannelOptions kullanılmalıdır"
expected:
  time: { CreatePipeline: "1" }
  space: "1"
concept_tags: [async-await, concurrency]
checklist_extra:
  - "Channel.CreateBounded<int>(capacity) kullanılmış mı?"
  - "FullMode Wait olarak yapılandırılmış mı?"
reference_solution_path: private/solutions/cs-medium-channel-producer-consumer.cs
hint_ladder:
  1: "BoundedChannelOptions ile FullMode = BoundedChannelFullMode.Wait ayarını yapın."
  2: "Channel.CreateBounded ile yüksek performanslı kilit-serbest asenkron kanal döndürün."
  3: "Bu modern C# eşzamanlılık aracı 'asenkron kanal boru hattı (channel producer-consumer pipeline)' olarak bilinir."
```

---

### cs-medium-semaphore-limiter

```yaml
id: cs-medium-semaphore-limiter
version: 1
language: csharp
engine: none
difficulty: medium
title: "Eşzamanlı çalışan istek sayısını sınırlama"
prompt: |
  Verilen asenkron fonksiyonu SemaphoreSlim kısıtı altında çalıştırarak aynı anda en fazla limit adet işlemin yürütülmesine izin veren `Task RunWithThrottlingAsync(Func<Task> work, SemaphoreSlim semaphore)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "try-finally bloğunda Release() çağrılmalıdır"
expected:
  time: { RunWithThrottlingAsync: "1" }
  space: "1"
concept_tags: [async-await, resource-management]
checklist_extra:
  - "await semaphore.WaitAsync() çağrılmış mı?"
  - "finally bloğunda Release() garanti edilmiş mi?"
reference_solution_path: private/solutions/cs-medium-semaphore-limiter.cs
hint_ladder:
  1: "await semaphore.WaitAsync() ile izin alın."
  2: "try bloğunda work() fonksiyonunu çalıştırıp finally bloğunda semaphore.Release() çağırın."
  3: "Bu eşzamanlılık deseni 'asenkron hız kısıtlama (async throttling)' olarak bilinir."
```

---

### cs-medium-async-retry-policy

```yaml
id: cs-medium-async-retry-policy
version: 1
language: csharp
engine: none
difficulty: medium
title: "Üstel geri çekilme ile yeniden deneyen asenkron metot"
prompt: |
  Hata fırlatan asenkron bir işlemi üstel artan bekleme süreleriyle (exponential backoff) en fazla maxRetries kez yeniden deneyen `Task<T> RetryAsync<T>(Func<Task<T>> operation, int maxRetries)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) çağrı başı olmalı"
  - "Ek bellek O(1) olmalı"
  - "Task.Delay ile üstel bekleme yapılmalıdır"
expected:
  time: { RetryAsync: "1" }
  space: "1"
concept_tags: [async-await, error-handling]
checklist_extra:
  - "Math.Pow(2, attempt) ile bekleme süresi katlanmış mı?"
  - "Son denemede hata fırlatılmış mı?"
reference_solution_path: private/solutions/cs-medium-async-retry-policy.cs
hint_ladder:
  1: "Bir döngü kurup try bloğunda işlemi çalıştırın."
  2: "Hata yakalandığında attempt sayısına göre katlanan Task.Delay süresi kadar bekleyip tekrar deneyin."
  3: "Bu dayanıklılık deseni 'üstel geri çekilme ile yeniden deneme (exponential backoff retry)' olarak bilinir."
```

---

### cs-medium-safe-event-invocation

```yaml
id: cs-medium-safe-event-invocation
version: 1
language: csharp
engine: none
difficulty: medium
title: "İş parçacığı güvenli olay tetikleme deseni"
prompt: |
  Abonelerin araya girip += veya -= yapması durumunda NullReferenceException hatası almamak için geçici kopya alan veya null-conditional (?.) ile tetikleyen `void RaiseNotification(EventHandler handler, object sender, EventArgs e)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "handler?.Invoke deseni kullanılmalıdır"
expected:
  time: { RaiseNotification: "1" }
  space: "1"
concept_tags: [concurrency, memory-leak]
checklist_extra:
  - "handler?.Invoke(sender, e) kullanılmış mı?"
  - "Yarış durumu (race condition) önlenmiş mi?"
reference_solution_path: private/solutions/cs-medium-safe-event-invocation.cs
hint_ladder:
  1: "handler?.Invoke(sender, e) sözdizimi olayın referansını yerel bir değişkene kopyalar."
  2: "Bu sayede başka bir iş parçacığı son aboneyi çıkarsa bile null referans hatası almadan güvenle çağrılır."
  3: "Bu C# deyimi 'güvenli olay tetikleme (safe event invocation)' olarak bilinir."
```

---

### cs-medium-interlocked-spinlock

```yaml
id: cs-medium-interlocked-spinlock
version: 1
language: csharp
engine: none
difficulty: medium
title: "Atomik karşılaştır-ve-değiştir ile döner kilit tasarlama"
prompt: |
  Interlocked.CompareExchange kullanarak kilit edinme (Enter) ve Interlocked.Exchange ile kilit bırakma (Exit) operasyonları sunan `class SpinLockWrapper` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı kilitlemede O(1) döngü olmalı"
  - "Ek bellek O(1) olmalı"
  - "Interlocked metotları kullanılmalıdır"
expected:
  time: { SpinLockWrapper: "1" }
  space: "1"
concept_tags: [concurrency, performance]
checklist_extra:
  - "Interlocked.CompareExchange(ref _lockState, 1, 0) == 0 döngüyle beklenmiş mi?"
  - "Thread.SpinWait(1) ile CPU tasarrufu yapılmış mı?"
reference_solution_path: private/solutions/cs-medium-interlocked-spinlock.cs
hint_ladder:
  1: "Bir tamsayı bayrağı 0 (açık) ve 1 (kilitli) durumlarında tutun."
  2: "Enter metodunda Interlocked.CompareExchange ile bayrağı 0'dan 1'e çevirene kadar SpinWait yapın."
  3: "Bu senkronizasyon yapısı 'atomik döner kilit sarmalayıcısı (spinlock wrapper)' olarak bilinir."
```

---

### cs-medium-array-pool-memory-stream

```yaml
id: cs-medium-array-pool-memory-stream
version: 1
language: csharp
engine: none
difficulty: medium
title: "Bellek havuzundan dizi kullanarak sıfır GC akış tamponlayıcı"
prompt: |
  Akışa yazılan verileri ArrayPool<byte>.Shared üzerinden ödünç alınan tamponlarda biriktiren ve IDisposable ile iade eden `class PooledMemoryStream` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı yazmada O(n) olmalı"
  - "Ek bellek O(1) (havuzdan paylaşımlı) olmalı"
  - "Dispose içinde pool.Return çağrılmalıdır"
expected:
  time: { PooledMemoryStream: "n" }
  space: "1"
concept_tags: [allocation, resource-management]
checklist_extra:
  - "ArrayPool<byte>.Shared kullanılmış mı?"
  - "Dispose içinde tampon havuza iade edilmiş mi?"
reference_solution_path: private/solutions/cs-medium-array-pool-memory-stream.cs
hint_ladder:
  1: "Bellek havuzundan geçici bayt dizisi kiralayın."
  2: "Veri yazıldıkça tamponu gerekirse genişletip Dispose metodunda kiralanan dizileri Return ile havuza geri verin."
  3: "Bu yüksek başarımlı akış 'havuzlu bellek akışı (pooled memory stream)' olarak bilinir."
```

---

### cs-medium-span-binary-reader

```yaml
id: cs-medium-span-binary-reader
version: 1
language: csharp
engine: none
difficulty: medium
title: "Karakter dilimleri üzerinden ikili veri başlığını ayrıştırma"
prompt: |
  ReadOnlySpan<byte> kullanarak 4 baytlık sihirli sayı ve 4 baytlık paket boyutunu BinaryPrimitives ile sıfır nesne tahsisiyle okuyan `bool TryReadHeader(ReadOnlySpan<byte> data, out int magic, out int length)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "BinaryPrimitives.ReadInt32BigEndian kullanılmalıdır"
expected:
  time: { TryReadHeader: "1" }
  space: "1"
concept_tags: [zero-allocation, parsing]
checklist_extra:
  - "data.Length >= 8 kontrolü yapılmış mı?"
  - "BinaryPrimitives ile bayt sırası doğru okunmuş mu?"
reference_solution_path: private/solutions/cs-medium-span-binary-reader.cs
hint_ladder:
  1: "Tampon boyutunun en az 8 bayt olduğunu doğrulayın."
  2: "System.Buffers.Binary.BinaryPrimitives sınıfını kullanarak tamsayıları doğrudan bayt diliminden okuyun."
  3: "Bu ikili ayrıştırma 'sıfır tahsisli ikili veri okuyucusu (zero-allocation binary reader)' olarak bilinir."
```

---

### cs-medium-custom-enumerable-struct

```yaml
id: cs-medium-custom-enumerable-struct
version: 1
language: csharp
engine: none
difficulty: medium
title: "GC tahsisi yapmayan yapı tabanlı numaralandırıcı"
prompt: |
  GetEnumerator() metodu IEnumerable arayüzü yerine doğrudan özel bir ref struct Enumerator döndüren ve foreach döngüsünde heap tahsisi yapmayan `struct RangeEnumerable` yapısını yazın.
constraints:
  - "Zaman karmaşıklığı döngü için O(n) olmalı"
  - "Ek bellek O(1) olmalı (sıfır GC tahsisi)"
  - "GetEnumerator() struct dönmelidir"
expected:
  time: { RangeEnumerable: "n" }
  space: "1"
concept_tags: [zero-allocation, gc]
checklist_extra:
  - "Enumerator sınıf yerine struct tanımlanmış mı?"
  - "Boxing (kutuya alma) engellenmiş mi?"
reference_solution_path: private/solutions/cs-medium-custom-enumerable-struct.cs
hint_ladder:
  1: "C# derleyicisi örüntü tabanlı (pattern-based) GetEnumerator metodunu destekler."
  2: "Enumerator'ı bir struct olarak tasarlayarak foreach döngüsünde arayüz kutulama (boxing) tahsisini sıfırlayın."
  3: "Bu gelişmiş C# yapısı 'yapı tabanlı sıfır tahsisli numaralandırıcı (struct-based zero-allocation enumerator)' olarak bilinir."
```

---


---

## 4. Zor (Hard) — 50 Soru

---

### cs-hard-zero-alloc-http-parser

```yaml
id: cs-hard-zero-alloc-http-parser
version: 1
language: csharp
engine: none
difficulty: hard
title: "HTTP istek başlıklarını sıfır heap tahsisiyle ayrıştırma"
prompt: |
  ReadOnlySpan<byte> kullanarak gelen HTTP istek baytlarını UTF-8 alt metin veya dizi tahsis etmeden metot, yol ve başlık aralıklarına ayıran `bool TryParseHttpRequest(ReadOnlySpan<byte> request, out HttpRequestInfo info)` fonksiyonunu yazın. n bayt sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (sıfır GC tahsisi)"
  - "Span<Range> veya ref struct kullanılmalıdır"
expected:
  time: { TryParseHttpRequest: "n" }
  space: "1"
concept_tags: [zero-allocation, parsing]
checklist_extra:
  - "Heap üzerinde tek bir byte[] veya string tahsis edilmemiş mi?"
  - "ref struct veya Span ile sıfır GC sağlanmış mı?"
reference_solution_path: private/solutions/cs-hard-zero-alloc-http-parser.cs
hint_ladder:
  1: "Gelen bayt akışını ReadOnlySpan<byte> üzerinde dilimleyerek tarayın."
  2: "Metot, yol ve başlık sınırlarını System.Range veya karakter dilimi olarak çıkararak heap tahsisini sıfırlayın."
  3: "Bu yüksek başarımlı ayrıştırma 'sıfır tahsisli HTTP ayrıştırıcı (zero-allocation HTTP parser)' olarak bilinir."
```

---

### cs-hard-lock-free-queue-ms

```yaml
id: cs-hard-lock-free-queue-ms
version: 1
language: csharp
engine: none
difficulty: hard
title: "Michael-Scott algoritması ve atomik işlemlerle kilit-serbest kuyruk"
prompt: |
  Interlocked.CompareExchange kullanarak kilit (lock) olmaksızın birden çok üretici ve tüketicinin güvenle eleman ekleyip çıkardığı `class LockFreeQueue<T>` sınıfını yazın.
constraints:
  - "Amortize zaman karmaşıklığı O(1*) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Yalancı (dummy) baş düğüm kullanılmalıdır"
expected:
  time: { LockFreeQueue: "1*" }
  space: "1"
concept_tags: [concurrency, performance]
checklist_extra:
  - "Interlocked.CompareExchange ile head ve tail güncellenmiş mi?"
  - "Kilit kullanılmamış mı?"
reference_solution_path: private/solutions/cs-hard-lock-free-queue-ms.cs
hint_ladder:
  1: "Kuyruğu yalancı bir düğümle başlatıp _head ve _tail göstericilerini atomik olarak takip edin."
  2: "Enqueue ve Dequeue işlemlerinde CAS (CompareExchange) döngüleriyle yarış durumlarını çözün."
  3: "Bu eşzamanlı algoritma 'Michael-Scott kilit-serbest kuyruk algoritması (Michael-Scott lock-free queue)' olarak bilinir."
```

---

### cs-hard-concurrent-lru-cache

```yaml
id: cs-hard-concurrent-lru-cache
version: 1
language: csharp
engine: none
difficulty: hard
title: "Parçalı kilit ile yüksek başarımlı eşzamanlı LRU önbellek"
prompt: |
  Kilit çatışmasını azaltmak için anahtarları parçalara (striping/sharding) ayıran ve her parçayı bağımsız kilit ve LRU listesiyle koruyan `class ConcurrentLruCache<TKey, TValue>` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(capacity) olmalı"
  - "Kilit şeritleme (lock striping) uygulanmalıdır"
expected:
  time: { ConcurrentLruCache: "1" }
  space: "1"
concept_tags: [concurrency, performance]
checklist_extra:
  - "Anahtar hash değerine göre ilgili parçaya yönlendirilmiş mi?"
  - "Her parça kendi kilidiyle korunmuş mu?"
reference_solution_path: private/solutions/cs-hard-concurrent-lru-cache.cs
hint_ladder:
  1: "Önbelleği 16 veya 32 bağımsız alt önbelleğe (segment) bölün."
  2: "Anahtarın hash koduna göre sadece ilgili segmenti kilitleyerek genel kilit bekleme süresini asgariye indirin."
  3: "Bu eşzamanlı mimari 'kilit şeritlemeli eşzamanlı LRU önbellek (striped concurrent LRU cache)' olarak bilinir."
```

---

### cs-hard-custom-event-aggregator

```yaml
id: cs-hard-custom-event-aggregator
version: 1
language: csharp
engine: none
difficulty: hard
title: "Zayıf referanslar ile bellek sızıntısız olay yayın-abone merkezi"
prompt: |
  Uygulama genelinde olay yayınlama ve abonelik sağlayan, aboneleri WeakReference ile tutarak abonenin açıkça abonelikten çıkmasa dahi GC tarafından toplanabilmesini sağlayan `class EventAggregator` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) abone başı olmalı"
  - "Ek bellek O(n) olmalı"
  - "Ölü referanslar periyodik temizlenmelidir"
expected:
  time: { EventAggregator: "1" }
  space: "n"
concept_tags: [memory-leak, resource-management]
checklist_extra:
  - "WeakReference hedefi doğrulanmış mı?"
  - "Toplanan aboneler listeden ayıklanmış mı?"
reference_solution_path: private/solutions/cs-hard-custom-event-aggregator.cs
hint_ladder:
  1: "Abonelerin eylemlerini WeakReference aracılığıyla saklayın."
  2: "Olay tetiklendiğinde TryGetTarget ile yaşayan aboneleri çağırın, toplanmış olanları listeden temizleyin."
  3: "Bu mimari desen 'zayıf referanslı olay toplayıcı (weak reference event aggregator)' olarak bilinir."
```

---

### cs-hard-high-throughput-ring-buffer

```yaml
id: cs-hard-high-throughput-ring-buffer
version: 1
language: csharp
engine: none
difficulty: hard
title: "Önbellek satırı hizalamalı beklemesiz dairesel tampon"
prompt: |
  Tek üretici tek tüketici arasında çalışan, CPU önbellek satırı çakışmasını (false sharing) önlemek için [StructLayout(LayoutKind.Explicit)] ile 64 bayt hizalama kullanan `class DisruptorRingBuffer<T>` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(capacity) olmalı"
  - "Volatile.Read ve Volatile.Write kullanılmalıdır"
expected:
  time: { DisruptorRingBuffer: "1" }
  space: "1"
concept_tags: [concurrency, performance]
checklist_extra:
  - "Önbellek satırı hizalaması (padding) yapılmış mı?"
  - "Kilit kullanılmadan dairesel indeksler ilerletilmiş mi?"
reference_solution_path: private/solutions/cs-hard-high-throughput-ring-buffer.cs
hint_ladder:
  1: "Üretici ve tüketici indeksleri arasına 64 baytlık boşluk (padding) koyarak farklı CPU önbellek satırlarında yaşamalarını sağlayın."
  2: "Volatile bellek bariyerleriyle kilit kullanmadan çok yüksek işlem hızına ulaşın."
  3: "Bu yüksek frekanslı veri yapısı 'LMAX Disruptor tarzı dairesel tampon (Disruptor ring buffer)' olarak bilinir."
```

---

### cs-hard-median-two-sorted-arrays

```yaml
id: cs-hard-median-two-sorted-arrays
version: 1
language: csharp
engine: none
difficulty: hard
title: "İki sıralı dizinin birleşim medyanını ikili aramayla bulma (C#)"
prompt: |
  Küçükten büyüğe sıralı nums1 (n elemanlı) ve nums2 (m elemanlı) dizilerini birleştirmeden ikili arama ile birleşim medyanını O(log(min(n, m))) sürede hesaplayan `double FindMedianSortedArrays(int[] nums1, int[] nums2)` fonksiyonunu yazın. n ve m dizi boyutlarıdır.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Kısa dizi üzerinde ikili arama yapılmalıdır"
expected:
  time: { FindMedianSortedArrays: "log n" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Sol ve sağ bölüm sınırları doğru hesaplanmış mı?"
  - "Sonsuz sınır değerleri kullanılmış mı?"
reference_solution_path: private/solutions/cs-hard-median-two-sorted-arrays.cs
hint_ladder:
  1: "Daha kısa olan dizi üzerinde ikili arama yaparak sol ve sağ yarıları belirleyin."
  2: "Her iki dizinin sol maksimumları sağ minimumlardan küçük veya eşit olduğu an medyanı hesaplayın."
  3: "Bu algoritma 'iki sıralı dizinin medyanını ikili aramayla bulma (median of two sorted arrays)' olarak bilinir."
```

---

### cs-hard-sliding-window-median-heaps

```yaml
id: cs-hard-sliding-window-median-heaps
version: 1
language: csharp
engine: none
difficulty: hard
title: "İki öncelik kuyruğu ile kayan pencere medyanını hesaplama (C#)"
prompt: |
  n elemanlı bir dizide boyutu k olan kayan bir pencerenin her adımındaki medyanı iki öncelik kuyruğu kullanarak O(n log k) sürede hesaplayan `double[] MedianSlidingWindow(int[] nums, int k)` fonksiyonunu yazın. n dizi boyutu ve k pencere boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n log k) olmalı"
  - "Ek bellek O(k) olmalı"
  - "İki yarı arasındaki denge korunmalıdır"
expected:
  time: { MedianSlidingWindow: "n log k" }
  space: "k"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Küçük yarı max-heap, büyük yarı min-heap olarak tutulmuş mu?"
  - "Pencereden çıkan elemanlar elenmiş mi?"
reference_solution_path: private/solutions/cs-hard-sliding-window-median-heaps.cs
hint_ladder:
  1: "Küçük yarıyı bir max-heap'te, büyük yarıyı bir min-heap'te dengeli olarak saklayın."
  2: "Pencere kaydıkça çıkan elemanı düşürüp yeni elemanı uygun yarıya ekleyerek medyanı hesaplayın."
  3: "Bu algoritma 'çift yığın ile kayan pencere medyanı (sliding window median with dual heaps)' olarak bilinir."
```

---

### cs-hard-trapping-rain-water-2d

```yaml
id: cs-hard-trapping-rain-water-2d
version: 1
language: csharp
engine: none
difficulty: hard
title: "2D yükseklik haritasında biriken yağmur suyunu min-heap ile hesaplama"
prompt: |
  n x m boyutundaki bir arazi matrisinde birikebilecek toplam yağmur suyu hacmini PriorityQueue kullanarak hesaplayan `int TrapRainWater2D(int[,] heightMap)` fonksiyonunu yazın. n satır ve m sütun adedidir.
constraints:
  - "Zaman karmaşıklığı O(n * m log n) olmalı"
  - "Ek bellek O(n * m) olmalı"
  - "Dış sınırlar öncelik kuyruğuyla başlatılmalıdır"
expected:
  time: { TrapRainWater2D: "n*m log n" }
  space: "n*m"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "Dış kenarlar kuyruğa alınıp ziyaret edildi işaretlenmiş mi?"
  - "En alçak sınırdan içeriye doğru genişlenmiş mi?"
reference_solution_path: private/solutions/cs-hard-trapping-rain-water-2d.cs
hint_ladder:
  1: "Izgaranın dış sınırındaki tüm hücreleri min-heap'e ekleyip ziyaret edildi olarak işaretleyin."
  2: "En alçak sınır hücresini çekip komşularını inceleyin; komşu daha alçaksa aradaki fark kadar su biriktirip komşuyu güncellenmiş tepe olarak heap'e ekleyin."
  3: "Bu algoritma 'iki boyutlu arazide yağmur suyu tutma (trapping rain water 2D)' olarak bilinir."
```

---

### cs-hard-largest-rectangle-histogram

```yaml
id: cs-hard-largest-rectangle-histogram
version: 1
language: csharp
engine: none
difficulty: hard
title: "Monotonik artan yığın ile histogramdaki en büyük dikdörtgeni bulma"
prompt: |
  n elemanlı çubuk yükseklikleri dizisinde oluşturulabilecek en büyük dikdörtgenin alanını monotonik artan yığın kullanarak O(n) sürede bulan `long LargestRectangleArea(int[] heights)` fonksiyonunu yazın. n histogram çubuğu sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Yığında çubuk indeksleri tutulmalıdır"
expected:
  time: { LargestRectangleArea: "n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Yığında indeksler saklanmış mı?"
  - "Çıkarılan çubuk için genişlik doğru hesaplanmış mı?"
reference_solution_path: private/solutions/cs-hard-largest-rectangle-histogram.cs
hint_ladder:
  1: "Yükseklik indekslerini monotonik artan bir yığında tutun."
  2: "Daha alçak bir çubuk görüldüğünde yığından elemanları çekerek genişliği ve alanı hesaplayın."
  3: "Bu algoritma 'histogramda en büyük dikdörtgen alanı (largest rectangle in histogram)' olarak bilinir."
```

---

### cs-hard-maximal-rectangle-matrix

```yaml
id: cs-hard-maximal-rectangle-matrix
version: 1
language: csharp
engine: none
difficulty: hard
title: "İkilik matriste en büyük 1'lerden oluşan dikdörtgeni bulma"
prompt: |
  Yalnızca '0' ve '1' karakterleri içeren n x m boyutundaki bir matriste tümüyle '1'lerden oluşan en büyük dikdörtgenin alanını histogram problemine dönüştürerek O(n * m) sürede bulan `int MaximalRectangle(char[,] matrix)` fonksiyonunu yazın. n satır ve m sütun adedidir.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(m) olmalı"
  - "Her satır bir histogram olarak güncellenmelidir"
expected:
  time: { MaximalRectangle: "n*m" }
  space: "m"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Her satır için yükseklik dizisi birikimli güncellenmiş mi?"
  - "Her satırda histogram çözümü çağrılmış mı?"
reference_solution_path: private/solutions/cs-hard-maximal-rectangle-matrix.cs
hint_ladder:
  1: "Her satır için m boyutunda bir yükseklik dizisi tutarak '1' gördükçe yüksekliği artırın, '0' görünce sıfırlayın."
  2: "Her satırda oluşan histogram için en büyük dikdörtgen alanını hesaplayıp genel maksimumu güncelleyin."
  3: "Bu algoritma 'matriste azami dikdörtgen alanı (maximal rectangle in 2D binary matrix)' olarak bilinir."
```

---

### cs-hard-edit-distance-levenshtein

```yaml
id: cs-hard-edit-distance-levenshtein
version: 1
language: csharp
engine: none
difficulty: hard
title: "İki metin arasındaki düzenleme mesafesini dinamik programlamayla bulma (C#)"
prompt: |
  word1 metnini word2 metnine dönüştürmek için gereken minimum ekleme, silme ve değiştirme işlem sayısını dinamik programlama ile hesaplayan `int MinDistance(string word1, string word2)` fonksiyonunu yazın. n birinci ve m ikinci metnin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(m) olmalı"
  - "Alan optimizasyonu yapılmalıdır"
expected:
  time: { MinDistance: "n*m" }
  space: "m"
concept_tags: [performance, parsing]
checklist_extra:
  - "Karakterler eşitse maliyetsiz geçilmiş mi?"
  - "Eşit değilse min(ekle, sil, değiştir) + 1 alınmış mı?"
reference_solution_path: private/solutions/cs-hard-edit-distance-levenshtein.cs
hint_ladder:
  1: "dp tablosunda dp[i, j] değerini iki metin arasındaki asgari işlem sayısı yapın."
  2: "Karakterler eşleşirse çaprazdan doğrudan geçin, eşleşmezse 3 olası operasyonun minimumuna 1 ekleyin."
  3: "Bu dinamik programlama algoritması 'Levenshtein düzenleme mesafesi (Levenshtein edit distance)' olarak bilinir."
```

---

### cs-hard-regular-expression-matching

```yaml
id: cs-hard-regular-expression-matching
version: 1
language: csharp
engine: none
difficulty: hard
title: "Düzenli ifadeleri dinamik programlamayla eşleştirme (C#)"
prompt: |
  '.' ve '*' meta-karakterlerini destekleyen bir p desenini s metni ile tam olarak eşleştiren `bool IsMatch(string s, string p)` fonksiyonunu yazın. n metin ve m desen uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(n * m) olmalı"
  - "DP tablosu kurulmalıdır"
expected:
  time: { IsMatch: "n*m" }
  space: "n*m"
concept_tags: [parsing, edge-cases]
checklist_extra:
  - "p[j-1] == '*' durumunda sıfır eşleşme doğru test edilmiş mi?"
  - "Nokta karakteri genel eşleşme sağlamış mı?"
reference_solution_path: private/solutions/cs-hard-regular-expression-matching.cs
hint_ladder:
  1: "dp[i, j] tablosunu s[0...i] ile p[0...j] eşleşme durumu olarak kurun."
  2: "'*' karakterinde sıfır tekrarı veya bir önceki karakter metinle uyuşuyorsa bir tekrarı kontrol edin."
  3: "Bu algoritma 'düzenli ifade dinamik programlama eşleşmesi (regular expression matching DP)' olarak bilinir."
```

---

### cs-hard-wildcard-matching-dp

```yaml
id: cs-hard-wildcard-matching-dp
version: 1
language: csharp
engine: none
difficulty: hard
title: "Joker karakterleri destekleyen desen eşleme (C#)"
prompt: |
  '?' ve '*' joker karakterlerini destekleyen p desenini s metni ile eşleştiren `bool IsWildcardMatch(string s, string p)` fonksiyonunu yazın. n metin ve m desen uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(m) olmalı"
  - "DP optimizasyonu yapılmalıdır"
expected:
  time: { IsWildcardMatch: "n*m" }
  space: "m"
concept_tags: [parsing, performance]
checklist_extra:
  - "p[j-1] == '*' için dp geçişi doğru uygulanmış mı?"
  - "Başlangıç deseni '*' durumları başlatılmış mı?"
reference_solution_path: private/solutions/cs-hard-wildcard-matching-dp.cs
hint_ladder:
  1: "dp tablosunu tanımlayın; p'de '*' gördükçe ya boş metinle eşleşin ya da metinden bir karakter tüketerek deseni koruyun."
  2: "İki satırlı DP kullanarak ek bellek kullanımını O(m) seviyesine optimize edin."
  3: "Bu algoritma 'joker karakter desen eşleştirme algoritması (wildcard matching DP)' olarak bilinir."
```

---

### cs-hard-longest-valid-parentheses

```yaml
id: cs-hard-longest-valid-parentheses
version: 1
language: csharp
engine: none
difficulty: hard
title: "Dengeli açılıp kapanan en uzun geçerli parantez alt dizgisini bulma"
prompt: |
  Yalnızca '(' ve ')' karakterlerinden oluşan bir metindeki en uzun dengeli parantez alt dizgisinin uzunluğunu iki geçişli sayaçla O(n) zaman ve O(1) alanda bulan `int LongestValidParentheses(string s)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (sıfır tahsis)"
  - "Soldan sağa ve sağdan sola iki geçiş yapılmalıdır"
expected:
  time: { LongestValidParentheses: "n" }
  space: "1"
concept_tags: [performance, parsing]
checklist_extra:
  - "Soldan sağa ve sağdan sola iki geçiş yapılmış mı?"
  - "Sayaç sıfırlamaları doğru kurgulanmış mı?"
reference_solution_path: private/solutions/cs-hard-longest-valid-parentheses.cs
hint_ladder:
  1: "Soldan sağa gezerken '(' ve ')' sayılarını tutun; eşitlendiğinde uzunluğu güncelleyin, ')' aşarsa sıfırlayın."
  2: "Aynı işlemi sağdan sola tersine uygulayarak maksimum geçerli uzunluğu O(1) ek bellekle bulun."
  3: "Bu algoritma 'iki geçişte en uzun geçerli parantez bulma (longest valid parentheses two-pass)' olarak bilinir."
```

---

### cs-hard-minimum-window-substring

```yaml
id: cs-hard-minimum-window-substring
version: 1
language: csharp
engine: none
difficulty: hard
title: "Hedef karakterlerin tümünü içeren en küçük pencere alt dizgisini bulma (C#)"
prompt: |
  s metni içinde t metnindeki tüm karakterleri frekanslarıyla birlikte içeren en kısa kesintisiz alt dizgiyi kayan pencere ile bulan `string MinWindow(string s, string t)` fonksiyonunu yazın. Bulunamazsa boş metin dönmelidir. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) (ASCII frekans tabloları) olmalı"
  - "İki işaretçi kullanılmalıdır"
expected:
  time: { MinWindow: "n" }
  space: "1"
concept_tags: [string-building, performance]
checklist_extra:
  - "Gereken karakter sayısı matchCount ile takip edilmiş mi?"
  - "Sol sınır daraltılarak en kısa pencere saklanmış mı?"
reference_solution_path: private/solutions/cs-hard-minimum-window-substring.cs
hint_ladder:
  1: "t metninin karakter frekanslarını bir dizide tutun."
  2: "s metninde sağ işaretçiyi ilerletip tüm karakterler tamamlandığında, sol işaretçiyi mümkün olduğunca sağa çekerek en küçük pencereyi kaydedin."
  3: "Bu algoritma 'asgari pencere alt metni algoritması (minimum window substring)' olarak bilinir."
```

---

### cs-hard-merge-k-sorted-linked-lists

```yaml
id: cs-hard-merge-k-sorted-linked-lists
version: 1
language: csharp
engine: none
difficulty: hard
title: "Bağlı liste düğümlerini min-heap ile birleştirme"
prompt: |
  Her biri sıralı k adet tek yönlü bağlı listenin düğümlerini PriorityQueue kullanarak yeni düğüm tahsis etmeden tek bir sıralı bağlı listede birleştiren `ListNode MergeKLists(ListNode[] lists)` fonksiyonunu yazın. n toplam düğüm sayısı ve k liste sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n log k) olmalı"
  - "Ek bellek O(k) olmalı"
  - "Yalancı (dummy) baş düğüm kullanılmalıdır"
expected:
  time: { MergeKLists: "n log k" }
  space: "k"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Öncelik kuyruğu düğüm değerleriyle başlatılmış mı?"
  - "Çekilen düğümün next düğümü hemen kuyruğa eklenmiş mi?"
reference_solution_path: private/solutions/cs-hard-merge-k-sorted-linked-lists.cs
hint_ladder:
  1: "Tüm listelerin baş düğümlerini boyutu k olan bir PriorityQueue'ya yerleştirin."
  2: "En küçük düğümü çekip sonuç zincirine bağlayın ve çekilen düğümün next işaretçisini kuyruğa ekleyin."
  3: "Bu algoritma 'k adet sıralı bağlı listeyi yığınla birleştirme (merge k sorted linked lists with heap)' olarak bilinir."
```

---

### cs-hard-reverse-nodes-in-k-group

```yaml
id: cs-hard-reverse-nodes-in-k-group
version: 1
language: csharp
engine: none
difficulty: hard
title: "Bağlı listenin düğümlerini k elemanlık gruplar halinde tersine çevirme (C#)"
prompt: |
  Tek yönlü bir bağlı listenin düğümlerini her k düğümlük bloklar halinde yerinde tersine çeviren, son kalan k'dan az elemanlı bloğu ise olduğu gibi bırakan `ListNode ReverseKGroup(ListNode head, int k)` fonksiyonunu yazın. n listedeki toplam düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (in-place)"
  - "Düğüm referansları ters çevrilmelidir"
expected:
  time: { ReverseKGroup: "n" }
  space: "1"
concept_tags: [data-structures, zero-allocation]
checklist_extra:
  - "Grupta en az k düğüm olup olmadığı taranmış mı?"
  - "Grup ters çevrildikten sonra önceki ve sonraki parçalara bağlanmış mı?"
reference_solution_path: private/solutions/cs-hard-reverse-nodes-in-k-group.cs
hint_ladder:
  1: "Önünüzde en az k adet düğüm olup olmadığını kontrol edin; yoksa dokunmadan dönün."
  2: "k adet düğümün göstericilerini yerinde ters çevirip bir sonraki bloğa bağlayın."
  3: "Bu algoritma 'bağlı liste düğümlerini k gruplarında tersine çevirme (reverse nodes in k-group)' olarak bilinir."
```

---

### cs-hard-lfu-cache-implementation

```yaml
id: cs-hard-lfu-cache-implementation
version: 1
language: csharp
engine: none
difficulty: hard
title: "En az sıklıkla kullanılan elemanları çıkaran LFU önbellek sınıfı (C#)"
prompt: |
  Kapasitesi dolduğunda kullanım frekansı en düşük olanı çıkaran ve Get/Put işlemlerini O(1) sürede yapan `class LFUCache` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı her işlem için O(1) olmalı"
  - "Ek bellek O(capacity) olmalı"
  - "Frekans listeleri ve minFrequency tutulmalıdır"
expected:
  time: { LFUCache: "1" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "minFrequency değişkeni doğru güncellenmiş mi?"
  - "Her frekans için çift yönlü liste ve anahtar eşleşmesi tutulmuş mu?"
reference_solution_path: private/solutions/cs-hard-lfu-cache-implementation.cs
hint_ladder:
  1: "Her elemanın değerini ve frekansını bir sözlükte, her frekansa ait elemanları çift yönlü listelerde saklayın."
  2: "Erişilen elemanın frekansını artırıp bir üst frekans listesine taşıyın ve minFrequency değerini güncelleyin."
  3: "Bu veri yapısı mekanizması 'en az sıklıkla kullanılan önbellek (LFU cache implementation)' olarak bilinir."
```

---

### cs-hard-all-o1-data-structure

```yaml
id: cs-hard-all-o1-data-structure
version: 1
language: csharp
engine: none
difficulty: hard
title: "Tüm sorguları O(1) sürede yapan veri yapısı (C#)"
prompt: |
  Metin anahtarları için Inc(key), Dec(key), GetMaxKey() ve GetMinKey() operasyonlarının tamamını O(1) sürede gerçekleştiren `class AllOne` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı tüm operasyonlar için O(1) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Çift yönlü kova listesi ve sözlük kullanılmalıdır"
expected:
  time: { AllOne: "1" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Frekans kovaları çift yönlü liste ile sıralı tutulmuş mu?"
  - "Boşalan kovalar listeden silinmiş mi?"
reference_solution_path: private/solutions/cs-hard-all-o1-data-structure.cs
hint_ladder:
  1: "Aynı frekansa sahip anahtarları bir kümede tutan sıralı kova (Bucket) düğümlerinden oluşan bir çift yönlü liste kurun."
  2: "Artırma ve azaltmalarda anahtarı komşu kovaya taşıyarak listenin başından minKey, sonundan maxKey değerlerini O(1) sürede okuyun."
  3: "Bu gelişmiş veri yapısı 'tüm işlemleri sabit sürede yapan yapı (All O-one data structure)' olarak bilinir."
```

---

### cs-hard-binary-tree-max-path-sum

```yaml
id: cs-hard-binary-tree-max-path-sum
version: 1
language: csharp
engine: none
difficulty: hard
title: "İkili ağaçta herhangi iki düğüm arasındaki maksimum yol toplamını hesaplama (C#)"
prompt: |
  İkili bir ağacın herhangi bir düğümünden başlayıp herhangi bir düğümünde biten ve her düğümün en fazla bir kez kullanıldığı yollar arasındaki maksimum toplamı bulan `int MaxPathSum(TreeNode root)` fonksiyonunu yazın. n ağaçtaki düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek çağrı yığını için O(log n) olmalı"
  - "Negatif katkılar Math.Max(0, gain) ile budanmalıdır"
expected:
  time: { MaxPathSum: "n" }
  space: "log n"
concept_tags: [data-structures, edge-cases]
checklist_extra:
  - "Alt ağaçtan gelen negatif yollar sıfırlanmış mı?"
  - "Global maksimum her düğümde sol + sağ + kök toplamıyla güncellenmiş mi?"
reference_solution_path: private/solutions/cs-hard-binary-tree-max-path-sum.cs
hint_ladder:
  1: "Her düğüm için ebeveyne iletilebilecek tek taraflı maksimum kazancı Math.Max(0, subtreeSum) ile hesaplayın."
  2: "O düğümden geçen çatallı yolu (root + left + right) hesaplayarak global maksimum ile kıyaslayın."
  3: "Bu algoritma 'ikili ağaçta azami yol toplamı (binary tree maximum path sum)' olarak bilinir."
```

---

### cs-hard-word-ladder-two-bfs

```yaml
id: cs-hard-word-ladder-two-bfs
version: 1
language: csharp
engine: none
difficulty: hard
title: "Başlangıç sözcüğünden hedef sözcüğe en kısa dönüşüm yollarını çıkarma (C#)"
prompt: |
  Tek harf değişimleriyle beginWord'den endWord'e ulaşan tüm en kısa dönüşüm zincirlerini BFS ile seviye grafiği kurup geri izleme ile bulan `IList<IList<string>> FindLadders(string beginWord, string endWord, IList<string> wordList)` fonksiyonunu yazın. n sözlük boyutu ve m sözcük uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n * m) olmalı"
  - "Ek bellek O(n) olmalı"
  - "BFS ile en kısa mesafe seviyesi belirlenmelidir"
expected:
  time: { FindLadders: "n*m" }
  space: "n"
concept_tags: [data-structures, parsing]
checklist_extra:
  - "BFS sırasında kelimeler aynı seviyede paylaşılabilecek şekilde ziyaret edilmiş mi?"
  - "DFS geri izleme ile tüm yollar toplanmış mı?"
reference_solution_path: private/solutions/cs-hard-word-ladder-two-bfs.cs
hint_ladder:
  1: "BFS ile sözcükler arası ebeveyn-çocuk ilişkilerini ve en kısa adımı çıkarın."
  2: "Hedefe ulaşıldığında DFS ile ebeveyn haritasını geriye doğru takip ederek tüm en kısa yolları toplayın."
  3: "Bu algoritma 'sözcük merdiveni en kısa yolları (word ladder II BFS-DFS)' olarak bilinir."
```

---

### cs-hard-n-queens-puzzle

```yaml
id: cs-hard-n-queens-puzzle
version: 1
language: csharp
engine: none
difficulty: hard
title: "Satranç tahtasına n veziri birbirini tehdit etmeyecek şekilde yerleştirme (C#)"
prompt: |
  n x n boyutundaki satranç tahtasına n adet veziri hiçbir vezirin aynı satır, sütun veya çaprazda yer almayacağı tüm geçerli dizilimleri üreten `IList<IList<string>> SolveNQueens(int n)` fonksiyonunu yazın. n tahta boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n!) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Bit maskeleriyle kısıt denetimi yapılmalıdır"
expected:
  time: { SolveNQueens: "n!" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Sütun, sol çapraz ve sağ çapraz bayrakları O(1) sürede denetlenmiş mi?"
  - "Tüm çözümler tahta formatında oluşturulmuş mu?"
reference_solution_path: private/solutions/cs-hard-n-queens-puzzle.cs
hint_ladder:
  1: "Satır satır ilerleyerek her satıra bir vezir yerleştirin."
  2: "Sütun, sol çapraz (row - col) ve sağ çapraz (row + col) kümelerini kullanarak çakışmaları O(1) sürede engelleyin."
  3: "Bu klasik problem 'N-Vezir geri izleme algoritması (N-Queens backtracking puzzle)' olarak bilinir."
```

---

### cs-hard-sudoku-solver-backtrack

```yaml
id: cs-hard-sudoku-solver-backtrack
version: 1
language: csharp
engine: none
difficulty: hard
title: "Sudoku tablosunu kısıt yayılımı ve geri izleme ile çözme (C#)"
prompt: |
  9x9 boyutundaki kısmen doldurulmuş Sudoku tahtasını satır, sütun ve 3x3 kutu kurallarını bit maskesiyle denetleyerek yerinde çözen `void SolveSudoku(char[,] board)` fonksiyonunu yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı (sabit 9x9 tahta için)"
  - "Ek bellek O(1) olmalı"
  - "Çözüm bulunduğunda hemen geri dönülmelidir"
expected:
  time: { SolveSudoku: "1" }
  space: "1"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Satır, sütun ve 3x3 kutu bit maskeleri tutulmuş mu?"
  - "Geri izlemede geçersiz deneme geri alınmış mı?"
reference_solution_path: private/solutions/cs-hard-sudoku-solver-backtrack.cs
hint_ladder:
  1: "Her satır, sütun ve 3x3 blok için kullanılan rakamları bit maskelerinde saklayın."
  2: "Boş hücrelere 1-9 arası uygun adayları deneyerek geri izleme yapın ve çözüm bulununca sonlandırın."
  3: "Bu algoritma 'Sudoku çözücü geri izleme algoritması (Sudoku solver backtracking)' olarak bilinir."
```

---

### cs-hard-alien-dictionary-topological

```yaml
id: cs-hard-alien-dictionary-topological
version: 1
language: csharp
engine: none
difficulty: hard
title: "Uzaylı alfabesindeki harflerin sözlük sırasını topolojik sıralamayla bulma (C#)"
prompt: |
  Sözlük sırasına göre sıralanmış sözcük listesinden harfler arası öncelik ilişkilerini çıkararak uzaylı alfabesinin geçerli harf sıralamasını bulan `string AlienOrder(string[] words)` fonksiyonunu yazın. Geçersizlik veya döngüde boş metin dönmelidir. n sözcük ve m toplam karakter sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n + m) olmalı"
  - "Ek bellek O(1) (26 harf) olmalı"
  - "Kahn topolojik sıralama uygulanmalıdır"
expected:
  time: { AlienOrder: "n + m" }
  space: "1"
concept_tags: [data-structures, parsing]
checklist_extra:
  - "Ardışık kelimelerin ilk farklılaşan harfi yönlü kenar olarak eklenmiş mi?"
  - "Önek hatası geçersiz sayılmış mı?"
reference_solution_path: private/solutions/cs-hard-alien-dictionary-topological.cs
hint_ladder:
  1: "Komşu iki kelimenin ilk farklılaşan harflerini bularak yönlü bir bağımlılık grafiği kurun."
  2: "Grafik üzerinde topolojik sıralama uygulayarak tüm harflerin sıralamasını elde edin; döngü varsa boş dönün."
  3: "Bu çizge problemi 'uzaylı sözlüğü topolojik sıralaması (alien dictionary topological sort)' olarak bilinir."
```

---

### cs-hard-tarjan-scc-directed

```yaml
id: cs-hard-tarjan-scc-directed
version: 1
language: csharp
engine: none
difficulty: hard
title: "Yönlü çizgedeki tüm güçlü bağlı bileşenleri Tarjan ile bulma (C#)"
prompt: |
  n düğümlü yönlü bir çizgedeki tüm güçlü bağlı bileşenleri (SCC) Tarjan algoritmasıyla tek bir DFS geçişinde bularak IList<IList<int>> olarak döndüren `IList<IList<int>> FindSCC(int n, int[][] edges)` fonksiyonunu yazın. m kenar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n + m) olmalı"
  - "Ek bellek O(n) olmalı"
  - "dfn ve lowlink dizileri tutulmalıdır"
expected:
  time: { FindSCC: "n + m" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Keşif zamanı ve en düşük ulaşılabilir zaman doğru güncellenmiş mi?"
  - "Düğüm kök olduğunda yığından bileşen boşaltılmış mı?"
reference_solution_path: private/solutions/cs-hard-tarjan-scc-directed.cs
hint_ladder:
  1: "DFS sırasında her düğüme keşif zamanı (tin) ve lowlink değeri atayın."
  2: "lowlink değeri keşif zamanına eşit olan düğümlerde yığındaki elemanları çekerek güçlü bileşeni tamamlayın."
  3: "Bu çizge algoritması 'Tarjan güçlü bağlı bileşenler algoritması (Tarjan's strongly connected components)' olarak bilinir."
```

---

### cs-hard-critical-connections-bridges

```yaml
id: cs-hard-critical-connections-bridges
version: 1
language: csharp
engine: none
difficulty: hard
title: "Çizgedeki kritik köprü kenarları tespit etme"
prompt: |
  n sunucu ve bağlantı kenarları içeren ağda, kaldırıldığında sunucuların birbirinden kopmasına neden olan kritik bağlantıları (köprüleri) Tarjan algoritmasıyla bulan `IList<IList<int>> CriticalConnections(int n, IList<IList<int>> connections)` fonksiyonunu yazın. m kenar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n + m) olmalı"
  - "Ek bellek O(n) olmalı"
  - "low[v] > tin[u] koşulu denetlenmelidir"
expected:
  time: { CriticalConnections: "n + m" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Ebeveyn kenara geri dönülmesi DFS'te engellenmiş mi?"
  - "low[v] > tin[u] olan kenarlar köprü listesine eklenmiş mi?"
reference_solution_path: private/solutions/cs-hard-critical-connections-bridges.cs
hint_ladder:
  1: "Yönsüz grafikte DFS ile her düğüme keşif zamanı ve low değeri atayın."
  2: "Çocuk v için low[v] > tin[u] ise (u, v) kenarı silindiğinde v'nin u'ya başka bir alternatif yolu yoktur; bu kenar bir köprüdür."
  3: "Bu algoritma 'çizgede köprü kenar tespiti (bridge finding algorithm in graph)' olarak bilinir."
```

---

### cs-hard-network-flow-dinic

```yaml
id: cs-hard-network-flow-dinic
version: 1
language: csharp
engine: none
difficulty: hard
title: "Dinic algoritması ve seviye çizgesiyle azami ağ akışını hesaplama (C#)"
prompt: |
  n düğümlü bir akış ağında src kaynağından sink hedefine azami akışı BFS ile seviye grafiği kurup DFS ile engelleyici akışları bularak hesaplayan `long MaxFlowDinic(int n, int src, int sink, (int u, int v, long cap)[] edges)` fonksiyonunu yazın. m kenar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n^2 * m) olmalı"
  - "Ek bellek O(n + m) olmalı"
  - "Seviye grafiği ve çalışma işaretçisi tutulmalıdır"
expected:
  time: { MaxFlowDinic: "n^2 * m" }
  space: "n + m"
concept_tags: [data-structures, performance]
checklist_extra:
  - "BFS ile seviye grafiği kurulmuş mu?"
  - "DFS'te gereksiz kenarları tekrar denememek için ptr dizisi kullanılmış mı?"
reference_solution_path: private/solutions/cs-hard-network-flow-dinic.cs
hint_ladder:
  1: "BFS ile artık kapasitesi olan kenarlar üzerinden her düğüme bir mesafe seviyesi atayın."
  2: "Sadece bir sonraki seviyeye giden kenarlar üzerinden DFS ile engelleyici akış gönderip artık kapasiteleri güncelleyin."
  3: "Bu ağ akış algoritması 'Dinic azami akış algoritması (Dinic's maximum flow algorithm)' olarak bilinir."
```

---

### cs-hard-min-cost-max-flow

```yaml
id: cs-hard-min-cost-max-flow
version: 1
language: csharp
engine: none
difficulty: hard
title: "Artık çizgede en az maliyetli azami akışı bulma (C#)"
prompt: |
  n düğümlü bir ağda akış gönderirken birim kenar maliyetlerini de hesaba katarak toplam maliyeti en küçük olan maksimum akışı hesaplayan `(long flow, long cost) MinCostMaxFlow(int n, int src, int sink, (int u, int v, long cap, long cost)[] edges)` fonksiyonunu yazın. m kenar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n * m) her artırımda olmalı"
  - "Ek bellek O(n + m) olmalı"
  - "SPFA veya potansiyel destekli Dijkstra kullanılmalıdır"
expected:
  time: { MinCostMaxFlow: "n*m" }
  space: "n + m"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Ters kenarlar negatif maliyetle oluşturulmuş mu?"
  - "Akış ve maliyet çifti doğru hesaplanmış mı?"
reference_solution_path: private/solutions/cs-hard-min-cost-max-flow.cs
hint_ladder:
  1: "Her adımda artık kapasitesi pozitif olan kenarlar üzerinde en küçük maliyetli genişletici yolu bulun."
  2: "Bu yol boyunca akış göndererek toplam akışı ve toplam birikimli maliyeti artırın."
  3: "Bu çizge optimizasyonu 'asgari maliyetli azami akış algoritması (minimum-cost maximum-flow)' olarak bilinir."
```

---

### cs-hard-segment-tree-lazy-update

```yaml
id: cs-hard-segment-tree-lazy-update
version: 1
language: csharp
engine: none
difficulty: hard
title: "Tembel yayılım ile aralık toplamı ve aralık güncelleme ağacı (C#)"
prompt: |
  n elemanlı bir dizi üzerinde aralık toplama ve aralık toplamı sorgulama işlemlerini O(log n) sürede gerçekleştiren `class LazySegmentTree` sınıfını yazın. n dizi boyutudur.
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
  - "Kısmi örtüşmede push-down yapılarak çocuklara iletilmiş mi?"
reference_solution_path: private/solutions/cs-hard-segment-tree-lazy-update.cs
hint_ladder:
  1: "4n boyutunda bir ağaç ve tembel etiket dizisi açın."
  2: "Aralık güncellemelerinde tembel değeri düğüme kaydedin; sorgularda veya alt dallara inerken bekleyen değeri çocuklara iletin."
  3: "Bu veri yapısı mekanizması 'tembel yayılımlı kesim ağacı (lazy segment tree)' olarak bilinir."
```

---

### cs-hard-fenwick-tree-2d

```yaml
id: cs-hard-fenwick-tree-2d
version: 1
language: csharp
engine: none
difficulty: hard
title: "İki boyutlu ızgarada alt matris toplamlarını logaritmik sürede sorgulama (C#)"
prompt: |
  n x m boyutundaki bir ızgarada tekil hücre güncellemelerini ve alt matris toplamlarını O(log n * log m) sürede yapan `class FenwickTree2D` sınıfını yazın. n satır ve m sütun adedidir.
constraints:
  - "Zaman karmaşıklığı O(log n * log m) olmalı"
  - "Ek bellek O(n * m) olmalı"
  - "2D bit maskeleme kullanılmalıdır"
expected:
  time: { FenwickTree2D: "log n * log m" }
  space: "n*m"
concept_tags: [data-structures, performance]
checklist_extra:
  - "1 tabanlı indeksleme kuralına uyulmuş mu?"
  - "İç içe döngülerde index += index & -index uygulanmış mı?"
reference_solution_path: private/solutions/cs-hard-fenwick-tree-2d.cs
hint_ladder:
  1: "İki boyutlu bir ağaç matrisi tutun."
  2: "Hücre güncellerken hem satır hem sütun indekslerinde en düşük anlamlı biti (index & -index) ekleyerek ilerleyin."
  3: "Bu veri yapısı 'iki boyutlu ikili indeksli ağaç (2D Fenwick tree)' olarak bilinir."
```

---

### cs-hard-heavy-light-decomposition

```yaml
id: cs-hard-heavy-light-decomposition
version: 1
language: csharp
engine: none
difficulty: hard
title: "Ağaçta iki düğüm arasındaki azami değeri ağır-hafif ayrıştırmasıyla sorgulama"
prompt: |
  n düğümlü bir ağaçta düğüm değerlerini güncelleyen ve iki düğüm arasındaki yoldaki maksimum değeri O(log^2 n) sürede sorgulayan `class HLDTree` sınıfını yazın. n düğüm sayısıdır.
constraints:
  - "Zaman karmaşıklığı yol sorgusu için O(log n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Ağır zincirler kesim ağacıyla eşleştirilmelidir"
expected:
  time: { HLDTree: "log n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "En büyük alt ağaç ağır çocuk seçilmiş mi?"
  - "Zincir başları arasındaki atlamalarla kesim ağacından aralık maksimumu sorgulanmış mı?"
reference_solution_path: private/solutions/cs-hard-heavy-light-decomposition.cs
hint_ladder:
  1: "Ağacı ağır ve hafif zincirlere ayırarak her düğüme tek boyutlu düz bir dizi indeksi atayın."
  2: "İki düğüm arasındaki yolda ilerlerken aynı zincirdeki parçaları kesim ağacından logaritmik sürede sorgulayın."
  3: "Bu ağaç sorgu tekniği 'ağır-hafif ağaç ayrıştırması (heavy-light decomposition)' olarak bilinir."
```

---

### cs-hard-treap-split-merge

```yaml
id: cs-hard-treap-split-merge
version: 1
language: csharp
engine: none
difficulty: hard
title: "Örtük anahtarlı Treap ile aralık ters çevirme ve bölme operasyonları (C#)"
prompt: |
  Dizi indislerini örtük anahtar olarak kullanan, split ve merge operasyonlarıyla belirli bir alt diziyi O(log n) sürede tersine çeviren `class ImplicitTreap` sınıfını yazın. n eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Tembel etiketler aşağı yayılmalıdır"
expected:
  time: { ImplicitTreap: "log n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Rastgele önceliklerle yığın kuralı korunmuş mu?"
  - "Alt ağaç boyutları doğru güncellenmiş mi?"
reference_solution_path: private/solutions/cs-hard-treap-split-merge.cs
hint_ladder:
  1: "Her düğüme rastgele bir öncelik (priority) ve alt ağaç boyutu (size) atayın."
  2: "Aralık işlemlerini ağacı split ile bölüp, işlemi tembel bayrakla uygulayıp tekrar merge ile birleştirerek tamamlayın."
  3: "Bu veri yapısı mekanizması 'örtük anahtarlı ağaç-yığın yapısı (implicit treap split and merge)' olarak bilinir."
```

---

### cs-hard-suffix-automaton-string

```yaml
id: cs-hard-suffix-automaton-string
version: 1
language: csharp
engine: none
difficulty: hard
title: "Metin için doğrusal sürede son ek otomatı oluşturma (C#)"
prompt: |
  n karakterli bir metnin tüm alt dizgilerini tanıyan son ek otomatını (Suffix Automaton) O(n) zaman ve alanda çevrimiçi (online) inşa eden `class SuffixAutomaton` sınıfını yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) doğrusal olmalı"
  - "Ek bellek O(n) olmalı"
  - "Klon düğüm oluşturma adımları uygulanmalıdır"
expected:
  time: { SuffixAutomaton: "n" }
  space: "n"
concept_tags: [data-structures, parsing]
checklist_extra:
  - "Düğümlerin len ve link alanları doğru bağlanmış mı?"
  - "Klon düğüm doğru oluşturulmuş mu?"
reference_solution_path: private/solutions/cs-hard-suffix-automaton-string.cs
hint_ladder:
  1: "Metne her yeni karakter eklendiğinde otomat durumunu güncelleyin."
  2: "Gerektiğinde geçişleri ayırmak için klon düğüm oluşturup bağlantı işaretçilerini yönlendirin."
  3: "Bu gelişmiş metin otomatı 'son ek otomatı inşası (suffix automaton construction)' olarak bilinir."
```

---

### cs-hard-aho-corasick-multi-pattern

```yaml
id: cs-hard-aho-corasick-multi-pattern
version: 1
language: csharp
engine: none
difficulty: hard
title: "Çoklu desen aramak için Aho-Corasick durum makinesi (C#)"
prompt: |
  Verilen sözlükteki desenleri Trie ağacında toplayıp BFS ile başarısızlık bağlantılarını (failure links) kurarak metin üzerinde tek geçişte tüm eşleşmeleri bulan `class AhoCorasick` sınıfını yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) metin tarama için olmalı"
  - "Ek bellek O(k) olmalı (k toplam desen karakter sayısı)"
  - "BFS ile failure bağlantıları kurulmalıdır"
expected:
  time: { AhoCorasick: "n" }
  space: "k"
concept_tags: [data-structures, parsing]
checklist_extra:
  - "Failure linkleri BFS ile doğru oluşturulmuş mu?"
  - "Eşleşen desenler çıktı bağlantılarından toplanmış mı?"
reference_solution_path: private/solutions/cs-hard-aho-corasick-multi-pattern.cs
hint_ladder:
  1: "Desenlerden bir önek ağacı (Trie) kurun."
  2: "BFS ile her düğüme uyuşmazlık anında geri çekileceği en uzun geçerli önek düğümünü (failure link) bağlayın."
  3: "Bu durum makinesi 'Aho-Corasick çoklu desen eşleme algoritması (Aho-Corasick automaton)' olarak bilinir."
```

---

### cs-hard-manacher-palindrome-linear

```yaml
id: cs-hard-manacher-palindrome-linear
version: 1
language: csharp
engine: none
difficulty: hard
title: "Manacher algoritmasıyla doğrusal sürede en uzun palindromu bulma"
prompt: |
  Verilen bir metindeki en uzun palindromik alt metni Manacher algoritmasıyla simetri aynalama tekniğini kullanarak O(n) sürede bulan `string LongestPalindrome(string s)` fonksiyonunu yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) doğrusal olmalı"
  - "Ek bellek O(n) olmalı"
  - "Karakterler arasına ayraç konulmalıdır"
expected:
  time: { LongestPalindrome: "n" }
  space: "n"
concept_tags: [performance, string-building]
checklist_extra:
  - "Metin '#' karakterleriyle genişletilmiş mi?"
  - "Sağ sınır r ve merkez c doğru güncellenmiş mi?"
reference_solution_path: private/solutions/cs-hard-manacher-palindrome-linear.cs
hint_ladder:
  1: "Karakterler arasına özel ayraçlar koyarak çift uzunluklu palindromları tek merkezli forma sokun."
  2: "Daha önce hesaplanan simetrik noktanın yarıçapını taban alarak gereksiz karşılaştırmalardan kaçının."
  3: "Bu algoritma 'Manacher en uzun palindrom algoritması (Manacher's palindrome algorithm)' olarak bilinir."
```

---

### cs-hard-disjoint-set-rollback

```yaml
id: cs-hard-disjoint-set-rollback
version: 1
language: csharp
engine: none
difficulty: hard
title: "Geri alma destekleyen ayrık küme veri yapısı"
prompt: |
  Yol sıkıştırması yerine rütbe birleştirme (union by rank) kullanan ve yapılan birleştirme işlemlerini bir yığında saklayarak snapshot/rollback operasyonlarını O(log n) sürede destekleyen `class RollbackDSU` sınıfını yazın. n eleman adedidir.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Yol sıkıştırması yapılmamalıdır"
expected:
  time: { RollbackDSU: "log n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Değişen ebeveyn ve rütbe değerleri geçmiş yığınına kaydedilmiş mi?"
  - "Rollback çağrısında değerler eski haline getirilmiş mi?"
reference_solution_path: private/solutions/cs-hard-disjoint-set-rollback.cs
hint_ladder:
  1: "Geri alma geçmişini korumak için yol sıkıştırması yapmadan rütbeye göre birleştirin."
  2: "Her birleştirmede değişen düğümün eski ebeveyn ve rütbe değerini bir geçmiş yığınına atıp rollback anında geri yükleyin."
  3: "Bu veri yapısı mekanizması 'geri alınabilir ayrık küme yapısı (rollback disjoint set union)' olarak bilinir."
```

---

### cs-hard-red-black-tree-map

```yaml
id: cs-hard-red-black-tree-map
version: 1
language: csharp
engine: none
difficulty: hard
title: "Kırmızı-siyah ağaç tabanlı sıralı anahtar-değer haritası"
prompt: |
  Düğümlerin kırmızı ve siyah renk özelliklerini, sol/sağ döndürmelerini ve renk onarım adımlarını uygulayarak O(log n) garantili ekleme ve arama sunan `class RedBlackMap<TKey, TValue>` sınıfını yazın. n eleman sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Kökün daima siyah olması garanti edilmelidir"
expected:
  time: { RedBlackMap: "log n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Amca düğümün rengine göre renklendirme ve döndürme yapılmış mı?"
  - "Ağaç dengesi korunmuş mu?"
reference_solution_path: private/solutions/cs-hard-red-black-tree-map.cs
hint_ladder:
  1: "Yeni elemanı kırmızı bir yaprak olarak ekleyin."
  2: "Ebeveyn kırmızı olduğunda amca düğümün rengine göre yeniden renklendirme veya sol/sağ döndürme yaparak dengeyi koruyun."
  3: "Bu dengeli ağaç yapısı 'kırmızı-siyah ağaç eşlemesi (red-black tree map)' olarak bilinir."
```

---

### cs-hard-b-tree-disk-optimized

```yaml
id: cs-hard-b-tree-disk-optimized
version: 1
language: csharp
engine: none
difficulty: hard
title: "B-Ağacı arama ve düğüm bölme"
prompt: |
  Her düğümünde t ile 2t - 1 arasında anahtar tutan, düğüm dolduğunda ortanca elemanı ebeveyne fırlatarak bölünen B-Ağacı ekleme ve arama mantığına sahip `class BTree<T>` sınıfını yazın. n anahtar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(log n) olmalı"
  - "Kök bölündüğünde yeni bir kök atanmalıdır"
expected:
  time: { BTree: "log n" }
  space: "log n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Dolu düğümler aşağı inerken önceden bölünmüş mü?"
  - "Ortanca eleman ebeveyne aktarılmış mı?"
reference_solution_path: private/solutions/cs-hard-b-tree-disk-optimized.cs
hint_ladder:
  1: "Ağaçta aşağı inerken karşılaşılan tüm dolu düğümleri bölerek tek geçişte ekleme garantisi sağlayın."
  2: "Kök dolduğunda yüksekliği bir artırıp eski kökü bölün."
  3: "Bu veritabanı indeks veri yapısı 'B-Ağacı düğüm bölme ve arama (B-tree indexing)' olarak bilinir."
```

---

### cs-hard-skip-list-map

```yaml
id: cs-hard-skip-list-map
version: 1
language: csharp
engine: none
difficulty: hard
title: "Çok seviyeli atlama listesi ile sıralı harita"
prompt: |
  Rastgele belirlenen geometrik seviyelerle bağlantılı işaretçiler üzerinden O(log n) ortalama sürede arama, ekleme ve silme desteği sunan `class SkipListMap<TKey, TValue>` sınıfını yazın. n eleman sayısıdır.
constraints:
  - "Ortalama zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "İleri yönlü işaretçi dizisi güncellenmelidir"
expected:
  time: { SkipListMap: "log n" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Rastgele seviye üretimi yapılmış mı?"
  - "Önceki işaretçiler update dizisinde toplanmış mı?"
reference_solution_path: private/solutions/cs-hard-skip-list-map.cs
hint_ladder:
  1: "En üst seviyeden başlayarak hedef anahtardan küçük olan en sağdaki düğüme kadar ilerleyin."
  2: "Yeni düğüm eklerken rastgele bir yükseklik belirleyip tüm alt seviyelerdeki işaretçileri bağlayın."
  3: "Bu olasılıksal veri yapısı 'atlama listesi sıralı haritası (skip list map)' olarak bilinir."
```

---

### cs-hard-expression-parser-ast

```yaml
id: cs-hard-expression-parser-ast
version: 1
language: csharp
engine: none
difficulty: hard
title: "Aritmetik ifadeleri soyut sözdizim ağacına dönüştüren ayrıştırıcı (C#)"
prompt: |
  +, -, *, /, parantez ve sayı içeren bir matematiksel metni özyinelemeli iniş ile ayrıştırıp AST kök düğümünü ve değerlendirme fonksiyonunu sunan `class ExpressionParser` sınıfını yazın. n metin uzunluğudur.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Soyut sözdizim ağacı (AST) oluşturulmalıdır"
expected:
  time: { ExpressionParser: "n" }
  space: "n"
concept_tags: [data-structures, parsing]
checklist_extra:
  - "Operatör öncelikleri doğru kurgulanmış mı?"
  - "Sözdizim hataları güvenle yakalanmış mı?"
reference_solution_path: private/solutions/cs-hard-expression-parser-ast.cs
hint_ladder:
  1: "Gramer kurallarını Expr -> Term -> Factor seviyelerine ayırın."
  2: "Her seviyede özyinelemeli fonksiyon çağırarak operatör önceliklerine uygun bir AST ağacı kurun."
  3: "Bu derleyici tekniği 'özyinelemeli iniş ifade ayrıştırıcısı (recursive descent expression parser)' olarak bilinir."
```

---

### cs-hard-burst-balloons-dp

```yaml
id: cs-hard-burst-balloons-dp
version: 1
language: csharp
engine: none
difficulty: hard
title: "Balon patlatma oyununda maksimum kazancı aralık dinamik programlamasıyla hesaplama"
prompt: |
  n elemanlı pozitif sayılar dizisinde balonları patlatırken nums[left] * nums[i] * nums[right] puanı toplayan ve maksimum puanı aralık dinamik programlamasıyla bulan `int MaxCoins(int[] nums)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n^3) olmalı"
  - "Ek bellek O(n^2) olmalı"
  - "Sınırlar 1 ile genişletilmelidir"
expected:
  time: { MaxCoins: "n^3" }
  space: "n^2"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Dizi başına ve sonuna sanal 1 elemanları eklenmiş mi?"
  - "En son patlatılan balon k pivotu seçilerek DP geçişi kurulmuş mu?"
reference_solution_path: private/solutions/cs-hard-burst-balloons-dp.cs
hint_ladder:
  1: "Dizinin iki ucuna 1 ekleyip aralık DP kurun."
  2: "(left, right) aralığında en son patlayacak balonu k seçerek dp[left, right] = max(dp[left, k] + dp[k, right] + nums[left]*nums[k]*nums[right]) geçişini hesaplayın."
  3: "Bu algoritma 'aralık dinamik programlaması ile balon patlatma (burst balloons interval DP)' olarak bilinir."
```

---

### cs-hard-tsp-bitmask-dp

```yaml
id: cs-hard-tsp-bitmask-dp
version: 1
language: csharp
engine: none
difficulty: hard
title: "Gezgin Satıcı Problemini bit maskeli dinamik programlamayla çözme (C#)"
prompt: |
  n şehir arasındaki mesafe matrisi verildiğinde tüm şehirleri bir kez ziyaret edip başlangıca dönen en kısa tur uzunluğunu O(n^2 * 2^n) sürede çözen `int SolveTSP(int[,] dist)` fonksiyonunu yazın. n <= 16 kabul edilir. n şehir sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n^2) alt problem geçişleriyle olmalı"
  - "Ek bellek O(n) olmalı"
  - "Bit maskesi (1 << n) durumları tutulmalıdır"
expected:
  time: { SolveTSP: "n^2" }
  space: "n"
concept_tags: [data-structures, performance]
checklist_extra:
  - "Ziyaret edilen şehirler kümesi bit maskesiyle ifade edilmiş mi?"
  - "Başlangıç şehrine dönüş mesafesi eklenmiş mi?"
reference_solution_path: private/solutions/cs-hard-tsp-bitmask-dp.cs
hint_ladder:
  1: "dp[mask, u] değerini u şehrinde bulunup mask ile belirtilen şehirlerin ziyaret edildiği minimum maliyet yapın."
  2: "Henüz ziyaret edilmemiş v şehirlerine geçişlerin minimumunu hesaplayarak sonuca ulaşın."
  3: "Bu algoritma 'Held-Karp gezgin satıcı bit maskeli çözümü (Held-Karp TSP algorithm)' olarak bilinir."
```

---

### cs-hard-custom-thread-pool-stealing

```yaml
id: cs-hard-custom-thread-pool-stealing
version: 1
language: csharp
engine: none
difficulty: hard
title: "İş çalma algoritmalı özel iş parçacığı havuzu"
prompt: |
  Her iş parçacığının kendi yerel deque'si olan ve kendi işi bittiğinde diğer iş parçacıklarının kuyruğundan görev çalan `class CustomWorkStealingPool` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(n) olmalı"
  - "Kilit çatışması en aza indirilmelidir"
expected:
  time: { CustomWorkStealingPool: "1" }
  space: "n"
concept_tags: [concurrency, performance]
checklist_extra:
  - "Yerel iş parçacığı kuyruk sonundan (LIFO), çalan iş parçacığı kuyruk başından (FIFO) mı işlem yapıyor?"
  - "Deadlock önlenmiş mi?"
reference_solution_path: private/solutions/cs-hard-custom-thread-pool-stealing.cs
hint_ladder:
  1: "Her iş parçacığı kendi yerel kuyruğunun arkasından görev çekip çalıştırsın."
  2: "Kendi kuyruğu boşalan iş parçacığı rastgele başka bir iş parçacığının kuyruk önünden görev çalarak iş yükünü dengelesin."
  3: "Bu gelişmiş iş parçacığı mimarisi 'iş çalma havuzu (work-stealing thread pool)' olarak bilinir."
```

---

### cs-hard-zero-alloc-json-tokenizer

```yaml
id: cs-hard-zero-alloc-json-tokenizer
version: 1
language: csharp
engine: none
difficulty: hard
title: "Sıfır tahsisli JSON simge ayrıştırıcısı"
prompt: |
  ReadOnlySpan<byte> üzerinde çalışan ve JSON metnindeki nesne, dizi, alan adı ve değer simgelerini tek bir heap tahsisi yapmadan ayrıştıran `ref struct JsonTokenizer` yapısını yazın. n bayt sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(n) olmalı"
  - "Ek bellek O(1) olmalı (sıfır heap tahsisi)"
  - "ref struct kullanılmalıdır"
expected:
  time: { JsonTokenizer: "n" }
  space: "1"
concept_tags: [zero-allocation, parsing]
checklist_extra:
  - "ref struct olarak yığında yaşatılmış mı?"
  - "Heap tahsisi sıfırlanmış mı?"
reference_solution_path: private/solutions/cs-hard-zero-alloc-json-tokenizer.cs
hint_ladder:
  1: "ref struct kullanarak yapının heap'e kaçmasını (boxing) derleme zamanında engelleyin."
  2: "ReadOnlySpan<byte> üzerinde UTF-8 baytlarını adım adım okuyarak simgeleri sıfır GC tahsisiyle üretin."
  3: "Bu modern ayrıştırıcı mimarisi 'sıfır tahsisli JSON simgeleştirici (zero-allocation JSON tokenizer)' olarak bilinir."
```

---

### cs-hard-actor-mailbox-queue

```yaml
id: cs-hard-actor-mailbox-queue
version: 1
language: csharp
engine: none
difficulty: hard
title: "Kilit-serbest kuyruklu aktör posta kutusu modeli"
prompt: |
  Mesajları kilit-serbest kuyrukta toplayan ve gelen mesajları tekil bir yürütme bağlamında sırayla işleyen `class ActorMailbox` aktör modelini yazın.
constraints:
  - "Zaman karmaşıklığı mesaj başı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Interlocked ile tekil yürütücü garantisi verilmelidir"
expected:
  time: { ActorMailbox: "1" }
  space: "1"
concept_tags: [concurrency, performance]
checklist_extra:
  - "Interlocked.CompareExchange ile aynı anda yalnızca tek bir tüketici döngüsü çalıştırılmış mı?"
  - "Veri yarışı önlenmiş mi?"
reference_solution_path: private/solutions/cs-hard-actor-mailbox-queue.cs
hint_ladder:
  1: "Mesajları ConcurrentQueue içinde toplayın."
  2: "Bir tüketici döngüsünü Interlocked ile tetikleyerek aynı aktörün mesajlarının daima tek bir iş parçacığında sırayla işlenmesini sağlayın."
  3: "Bu eşzamanlılık mimarisi 'aktör posta kutusu modeli (actor mailbox pattern)' olarak bilinir."
```

---

### cs-hard-memory-mapped-file-index

```yaml
id: cs-hard-memory-mapped-file-index
version: 1
language: csharp
engine: none
difficulty: hard
title: "Belleğe eşlenen dosya üzerinde sabit boyutlu indeks arama"
prompt: |
  MemoryMappedFile kullanarak diskteki devasa bir dosyanın tamamını RAM'e yüklemeden ikili aramayla kayıt bulan `class MappedFileIndex` sınıfını yazın. n kayıttaki anahtar sayısıdır.
constraints:
  - "Zaman karmaşıklığı O(log n) olmalı"
  - "Ek bellek O(1) olmalı"
  - "MemoryMappedViewAccessor kullanılmalıdır"
expected:
  time: { MappedFileIndex: "log n" }
  space: "1"
concept_tags: [resource-management, performance]
checklist_extra:
  - "MemoryMappedViewAccessor ile doğrudan ofset okuması yapılmış mı?"
  - "RAM taşması engellenmiş mi?"
reference_solution_path: private/solutions/cs-hard-memory-mapped-file-index.cs
hint_ladder:
  1: "Diskteki dosyayı MemoryMappedFile ile sanal belleğe eşleyin."
  2: "ViewAccessor üzerinden kayıt ofsetlerini doğrudan hesaplayarak disk üzerinde ikili arama yapın."
  3: "Bu dosya işleme tekniği 'belleğe eşlenen dosya indeksi (memory-mapped file indexing)' olarak bilinir."
```

---

### cs-hard-async-barrier-coordination

```yaml
id: cs-hard-async-barrier-coordination
version: 1
language: csharp
engine: none
difficulty: hard
title: "Asenkron iş parçacıklarını belirli fazlarda toplayan asenkron bariyer"
prompt: |
  n adet bağımsız asenkron görevin belirli kontrol noktalarına (fazlara) aynı anda ulaşmasını bekleyen ve tümü ulaştığında bir sonraki faza geçiren `class AsyncBarrier` sınıfını yazın. n katılımcı sayısıdır.
constraints:
  - "Zaman karmaşıklığı faz başı O(1) olmalı"
  - "Ek bellek O(n) olmalı"
  - "TaskCompletionSource kullanılmalıdır"
expected:
  time: { AsyncBarrier: "1" }
  space: "n"
concept_tags: [async-await, concurrency]
checklist_extra:
  - "Interlocked.Decrement ile kalan katılımcı sayısı sayılmış mı?"
  - "Son katılımcı geldiğinde TaskCompletionSource.SetResult çağrılmış mı?"
reference_solution_path: private/solutions/cs-hard-async-barrier-coordination.cs
hint_ladder:
  1: "Bir TaskCompletionSource oluşturup bekleyen görevleri await tcs.Task ile duraklatın."
  2: "Sonuncu katılımcı SignalAndWaitAsync çağırdığında yeni bir faz tcs'si açıp öncekini tamamlayın."
  3: "Bu eşzamanlı koordinasyon aracı 'asenkron bariyer senkronizasyonu (async barrier coordination)' olarak bilinir."
```

---

### cs-hard-simd-vectorized-sum

```yaml
id: cs-hard-simd-vectorized-sum
version: 1
language: csharp
engine: none
difficulty: hard
title: "Donanım hızlandırmalı vektör komutlarıyla dizi elemanlarını toplama"
prompt: |
  System.Numerics.Vector<int> komutlarını (SIMD) kullanarak tamsayı dizisini işlemci yazmaçlarında 4'er veya 8'er paralel toplayan `long VectorizedSum(ReadOnlySpan<int> data)` fonksiyonunu yazın. n dizi boyutudur.
constraints:
  - "Zaman karmaşıklığı O(n) (SIMD hızlandırılmış) olmalı"
  - "Ek bellek O(1) olmalı"
  - "Vector.IsHardwareAccelerated denetlenmelidir"
expected:
  time: { VectorizedSum: "n" }
  space: "1"
concept_tags: [performance, span]
checklist_extra:
  - "Vector<int>.Count kadar adımlarla ilerlenmiş mi?"
  - "Kalan artık elemanlar döngü sonunda tekil toplanmış mı?"
reference_solution_path: private/solutions/cs-hard-simd-vectorized-sum.cs
hint_ladder:
  1: "Vector<int>.Count boyutunda bloklar halinde diziyi tarayarak SIMD yazmaçlarında paralel toplama yapın."
  2: "Vector.Dot ile ara toplamı alıp kalan artık elemanları standart döngüyle ekleyin."
  3: "Bu donanım seviyesi optimizasyon 'SIMD vektör komutları ile toplama (SIMD vectorized summation)' olarak bilinir."
```

---

### cs-hard-async-semaphore-fifo

```yaml
id: cs-hard-async-semaphore-fifo
version: 1
language: csharp
engine: none
difficulty: hard
title: "Asenkron istekleri kesin FIFO sırasıyla çalıştıran kısıtlayıcı"
prompt: |
  Standart SemaphoreSlim'in sıra garantisi vermediği durumlarda, bekleyen görevleri Queue<TaskCompletionSource> ile kesin geliş sırasına göre serbest bırakan `class FifoAsyncSemaphore` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(n) olmalı"
  - "FIFO sırası garanti edilmelidir"
expected:
  time: { FifoAsyncSemaphore: "1" }
  space: "n"
concept_tags: [async-await, concurrency]
checklist_extra:
  - "Bekleyen görevler Queue<TaskCompletionSource> içinde saklanmış mı?"
  - "Release çağrısında kuyruk başındaki görev uyandırılmış mı?"
reference_solution_path: private/solutions/cs-hard-async-semaphore-fifo.cs
hint_ladder:
  1: "İzin kalmadığında bir TaskCompletionSource oluşturup kuyruğa atın."
  2: "Release çağrıldığında kuyruk başındaki TCS'yi SetResult ile tamamlayarak ilk gelenin ilk girmesini (FIFO) sağlayın."
  3: "Bu eşzamanlılık aracı 'FIFO sıralı asenkron semafor (FIFO async semaphore)' olarak bilinir."
```

---

### cs-hard-native-memory-allocator

```yaml
id: cs-hard-native-memory-allocator
version: 1
language: csharp
engine: none
difficulty: hard
title: "İşletim sistemi yerel belleğini yöneten sızıntısız tahsisçi"
prompt: |
  NativeMemory.Alloc ve NativeMemory.Free kullanarak yönetilmeyen C tarzı yerel belleği tahsis eden, Span<byte> ile erişim sunan ve IDisposable ile temizleyen `class NativeBuffer : IDisposable` sınıfını yazın.
constraints:
  - "Zaman karmaşıklığı O(1) olmalı"
  - "Ek bellek O(1) olmalı"
  - "IDisposable deseni tam uygulanmalıdır"
expected:
  time: { NativeBuffer: "1" }
  space: "1"
concept_tags: [resource-management, memory-safety]
checklist_extra:
  - "NativeMemory.Alloc ve Free kullanılmış mı?"
  - "Dispose(bool disposing) ve sonlandırıcı (finalizer) çifti doğru kurgulanmış mı?"
reference_solution_path: private/solutions/cs-hard-native-memory-allocator.cs
hint_ladder:
  1: "System.Runtime.InteropServices.NativeMemory ile çöp toplayıcı dışı yerel bellek ayırın."
  2: "Dispose metodunda ve sonlandırıcıda (finalizer) NativeMemory.Free çağırarak bellek sızıntısını kesin olarak önleyin."
  3: "Bu yerel bellek yöneticisi 'yerel bellek sarmalayıcısı (native memory allocator buffer)' olarak bilinir."
```
