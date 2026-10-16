# Kural Kataloğu

> Bu dosya otomatik üretilir: `make rules-doc`
> (`uv run codementor rules doc --out docs/rules-catalog.md`). Elle düzenlemeyin.

Statik kurallar (mimari §5.3.3, §8.2). "LLM" tespitli maddeler burada değil,
`data/checklists/` altındaki kontrol listelerindedir. Bir kural `codementor.toml`
içinde `[rules] disabled = ["KURAL-ID"]` ile kapatılabilir.

Toplam: 41 kural.

| ID | Başlık | Dil | Motor | Kategori | Önem | Tür |
|---|---|---|---|---|---|---|
| C-BUF-001 | Sınır denetimsiz tampon fonksiyonu | c | — | memory_safety | high | hata |
| C-BUF-002 | Sınırı olmayan scanf %s | c | — | memory_safety | high | hata |
| C-IO-001 | scanf dönüş değeri denetlenmiyor | c | — | input_handling | medium | hata |
| C-MEM-001 | Serbest bırakılmayan bellek | c | — | resource_leak | high | hata |
| C-MEM-002 | realloc sonucu aynı işaretçiye atanıyor | c | — | memory_safety | high | hata |
| C-MEM-003 | Tahsis sonucu NULL denetimi yok | c | — | memory_safety | medium | hata |
| C-PERF-001 | Döngü koşulunda strlen | c | — | performance | low | hata |
| C-UB-001 | fflush(stdin) | c | — | undefined_behavior | medium | hata |
| CPP-OWN-001 | Çıplak new/delete | cpp | — | memory_safety | medium | hata |
| CPP-PERF-001 | Büyük nesne değerle geçiriliyor | cpp | — | performance | low | hata |
| CPP-PERF-002 | Döngüde tam metin kopyası | cpp | — | performance | medium | hata |
| CPP-PERF-003 | Döngüde std::endl | cpp | — | performance | low | öneri |
| CPP-PERF-004 | Reserve olmadan push_back | cpp | — | performance | low | öneri |
| CPP-SP-001 | Döngüsel shared_ptr şüphesi | cpp | — | resource_leak | high | hata |
| CS-ALLOC-001 | Döngüde string birleştirme | csharp | — | garbage_collection | medium | hata |
| CS-ALLOC-002 | Sıcak yolda LINQ | csharp | — | garbage_collection | medium | hata |
| CS-PERF-001 | Döngüde doğrusal arama | csharp | — | performance | medium | hata |
| CSS-ACC-001 | Odak göstergesi kaldırılmış | css | — | accessibility | medium | hata |
| CSS-LAYOUT-001 | Sabit yükseklikte metin kutusu | css | — | edge_case | low | öneri |
| CSS-LAYOUT-002 | Negatif margin ile ortalama | css | — | maintainability | low | öneri |
| CSS-MAINT-001 | Çok sayıda !important | css | — | maintainability | low | hata |
| CSS-MAINT-002 | Boş kural bloğu | css | — | maintainability | low | hata |
| CSS-STD-001 | Aynı blokta yinelenen özellik | css | — | maintainability | low | hata |
| HTML-ACC-001 | Alternatif metni olmayan görsel | html | — | accessibility | medium | hata |
| HTML-ACC-002 | Belge dili belirtilmemiş | html | — | accessibility | low | hata |
| HTML-ACC-003 | Etiketsiz form alanı | html | — | accessibility | medium | hata |
| HTML-STD-001 | Yinelenen id | html | — | design | medium | hata |
| HTML-STD-002 | DOCTYPE bildirimi yok | html | — | design | low | hata |
| HTML-STD-003 | Dengesiz etiket | html | — | design | medium | hata |
| PY-DESIGN-001 | Değiştirilebilir varsayılan argüman | python | — | design | medium | hata |
| PY-DESIGN-002 | None ile eşitlik karşılaştırması | python | — | design | low | hata |
| PY-EDGE-001 | Çıplak except | python | — | edge_case | medium | hata |
| PY-PERF-001 | Döngüde doğrusal liste işlemi | python | — | performance | medium | hata |
| PY-RES-001 | with dışında open() | python | — | resource_leak | medium | hata |
| UE-GC-001 | UPROPERTY'siz UObject alanı | cpp | unreal | garbage_collection | high | hata |
| UE-MEM-001 | Reserve olmadan TArray::Add | cpp | unreal | performance | low | öneri |
| UE-PERF-001 | Tick içinde ağır iş | cpp | unreal | performance | medium | hata |
| UNITY-EVT-001 | Kaldırılmayan olay aboneliği | csharp | unity | resource_leak | medium | hata |
| UNITY-GC-001 | Sıcak yolda heap tahsisi | csharp | unity | garbage_collection | high | hata |
| UNITY-PERF-001 | Sıcak yolda bileşen/sahne araması | csharp | unity | performance | high | hata |
| UNITY-PERF-002 | Sıcak yolda string etiket karşılaştırma | csharp | unity | performance | low | hata |

## Açıklamalar

### C-BUF-001 — Sınır denetimsiz tampon fonksiyonu

`gets`, `strcpy`, `strcat` ve `sprintf` hedef tamponun boyutunu bilmez; girdi tampondan uzunsa bellek taşar. Hedefin kaç bayt aldığını nereden biliyorsun?

### C-BUF-002 — Sınırı olmayan scanf %s

`%s` hedefe kaç karakter yazacağını bilmez; kullanıcı tampondan uzun bir girdi yazarsa ne olur ve genişliği kim belirlemeli?

*Kapsam ve sınırlar:* Yalnızca `scanf`/`fscanf` ve yalnızca biçim metin sabiti olduğunda çalışır. Genişlikli (`%99s`) ve atama yapmayan (`%*s`) dönüşümler, `sscanf` ile sınırı olmayan `%[` taraması kapsam dışıdır (muhafazakâr).

### C-IO-001 — scanf dönüş değeri denetlenmiyor

`scanf` kaç alanı başarıyla okuduğunu döndürür ama bu değer kullanılmıyor. Kullanıcı sayı yerine harf girerse ya da girdi biterse değişkende ne olur?

### C-MEM-001 — Serbest bırakılmayan bellek

Bu fonksiyonda `malloc`/`calloc` ile ayrılan bellek ne `free` ediliyor ne de fonksiyondan dışarı veriliyor. Fonksiyon bittiğinde bu bellek kimde kalıyor?

### C-MEM-002 — realloc sonucu aynı işaretçiye atanıyor

`realloc` başarısız olursa NULL döndürür ama eski blok serbest bırakılmaz. Sonuç doğrudan aynı işaretçiye yazıldığında eski bloğun adresi nerede kalır?

### C-MEM-003 — Tahsis sonucu NULL denetimi yok

`malloc`/`calloc`/`realloc` bellek ayıramazsa NULL döndürür. Bu işaretçi denetlenmeden kullanılıyor; tahsis başarısız olursa bu satırdan sonra ne olur?

### C-PERF-001 — Döngü koşulunda strlen

Döngü koşulu her turda yeniden değerlendirilir ve `strlen` her seferinde metni sonuna kadar tarar. n karakterlik bir metinde toplam kaç karakter okunur?

### C-UB-001 — fflush(stdin)

C standardı `fflush`'ı yalnızca çıkış akışları için tanımlar; `stdin` üzerinde davranış tanımsızdır ve derleyiciden derleyiciye değişir. Satırın geri kalanını atmak için girişten ne okuyabilirsin?

### CPP-OWN-001 — Çıplak new/delete

Nesnenin ömrü elle yönetiliyor. Arada bir istisna ya da erken `return` olursa `delete` çalışır mı? Sahipliği kim taşıyor?

*Kapsam ve sınırlar:* Aynı kapsamda aynı ada atanan tahsis ile `delete` eşleşirse öneri, eşleşmezse hata. Eşleşse bile arada aynı kapsamda erken çıkış (`return`/`throw`/`goto`/`break`/`continue`) varsa `delete` atlanabilir sayıldığı için hata verilir; lambda gövdesindeki atlamalar dışarıdan çıkış sayılmaz.

### CPP-PERF-001 — Büyük nesne değerle geçiriliyor

Bu parametre değerle geçiriliyor; her çağrıda kapsayıcının tamamı kopyalanır. Fonksiyon bu kopyayı değiştirmeye ya da saklamaya ihtiyaç duyuyor mu?

### CPP-PERF-002 — Döngüde tam metin kopyası

`s = s + x` her turda s'in tamamını yeni bir tampona kopyalar. n tur dönen bir döngüde toplam kaç karakter kopyalanır ve `s += x` bunu nasıl değiştirir?

*Kapsam ve sınırlar:* Yalnızca döngü gövdesindeki `s = s + …` biçimi (aynı yalın ad sağda yaprak olarak) aranır; `s += …`, `s.append(…)`, döngü dışı atamalar ve `this->alan = this->alan + …` kapsam dışıdır.

### CPP-PERF-003 — Döngüde std::endl

`std::endl` satır sonu eklemekle kalmaz, tamponu da her turda boşaltır. Döngü 10 000 kez dönüyorsa alt katmana kaç yazma çağrısı iner?

*Kapsam ve sınırlar:* Yalnızca `std::endl` yazımı ve döngü gövdesi aranır; `using namespace std;` ile yazılan yalın `endl`, `std::flush` ve döngü dışı kullanımlar kapsam dışıdır (muhafazakâr).

### CPP-PERF-004 — Reserve olmadan push_back

Döngünün kaç kez döneceği belli ve her turda kapsayıcıya bir eleman ekleniyor. Kapasite dolduğunda `push_back` ne yapmak zorunda kalır ve bu döngüde kaç kez olur?

*Kapsam ve sınırlar:* Yalnızca sınırı bilinen `for`/aralık döngüleri, yalın adlı kapsayıcılar (`std::vector`/`std::deque`/`std::list`/`TArray`/`TSet`) ve koşulsuz `push_back`/`emplace_back` sayılır; erken `return`/`break`/koşul varsa susar. Aynı alıcı için fonksiyonda bir `reserve`/`resize` çağrısı varsa bulgu verilmez: sıralama denetlenmez. Unreal'daki `TArray::Add` için UE-MEM-001 geçerlidir.

### CPP-SP-001 — Döngüsel shared_ptr şüphesi

Bu alan, kendisini de `shared_ptr` ile tutan bir nesneyi gösteriyor. İki nesne birbirini tutarsa sayaçları hiç sıfıra iner mi? Bağlardan biri sahiplik gerektirmiyorsa hangi tür daha uygun olur?

### CS-ALLOC-001 — Döngüde string birleştirme

`string` değiştirilemez: her `+=` yeni bir metin ayırıp eskisini kopyalar. Döngü n kez dönerse toplam kaç karakter kopyalanır?

### CS-ALLOC-002 — Sıcak yolda LINQ

LINQ her çağrıda yineleyici ve çoğu zaman temsilci nesneleri ayırır; bu satır her karede ya da döngünün her turunda çalışıyor. Bu satır kaç kez çalışıyor ve ürettiği sonuç her seferinde gerçekten değişiyor mu?

### CS-PERF-001 — Döngüde doğrusal arama

`List.Contains`/`IndexOf`/`Remove` elemanı bulmak için listeyi baştan sona tarar ve bu bir döngünün içinde. Toplam maliyet ne olur? Hangi veri yapısı bu aramayı daha hızlı yapar?

### CSS-ACC-001 — Odak göstergesi kaldırılmış

`outline: none` klavyeyle gezen kullanıcının kaldığı yeri gösteren tek işareti siliyor. Bu kutu odaklandığında ekranda ne değişiyor?

*Kapsam ve sınırlar:* Yalnızca `:focus` (ama `:focus-visible` değil) içeren bloklar taranır: `outline: none` yanında aynı blokta `border`/`box-shadow`/`background`/`text-decoration` varsa ya da aynı seçici için ayrı bir `:focus-visible` kuralı yazılmışsa susar.

### CSS-LAYOUT-001 — Sabit yükseklikte metin kutusu

Kutunun yüksekliği pikselle sabitlenmiş. Metin uzayınca, yazı tipi büyüyünce ya da ekran daralınca fazlası nereye gider ve bunu kim fark eder?

*Kapsam ve sınırlar:* Yalnızca `height: <sayı>px` aranır; `min-height`/`max-height`, yüzde ve `rem` ile tümü görsel öğelerden (`img`, `svg`, `canvas`, `video`, `iframe`, `input` …) oluşan seçiciler kapsam dışıdır. Kutunun gerçekten metin içerdiği doğrulanamaz.

### CSS-LAYOUT-002 — Negatif margin ile ortalama

Kutu `left: 50%` ile sağa itilip yarı genişliği kadar geri çekiliyor. Genişlik değişince o sabit sayı ne olur? Aynı sonucu genişlikten bağımsız nasıl alırsın?

*Kapsam ve sınırlar:* `position: absolute|fixed`, `left: 50%` ve negatif `margin-left` üçlüsü aynı blokta aranır; `transform: translateX(-50%)` gibi genişlikten bağımsız yöntemler kapsam dışıdır.

### CSS-MAINT-001 — Çok sayıda !important

Bu kural neden !important olmadan uygulanmıyordu? Bir sonraki değişiklikte bunu ezmek için ne yapman gerekecek?

### CSS-MAINT-002 — Boş kural bloğu

Bu seçici için bir stil yazılmamış. Kalması gerekiyor mu, yoksa yarım kalmış bir düzenlemenin izi mi?

### CSS-STD-001 — Aynı blokta yinelenen özellik

Bu blokta aynı özelliğe iki değer verilmiş. Tarayıcı hangisini kullanıyor ve öteki satır ne işe yarıyor?

### HTML-ACC-001 — Alternatif metni olmayan görsel

Bu görseli göremeyen bir kullanıcı (ekran okuyucu, yüklenemeyen resim) burada ne duyar ya da görür?

### HTML-ACC-002 — Belge dili belirtilmemiş

Ekran okuyucu bu sayfayı hangi dilin telaffuzuyla okuyacağını nereden biliyor?

### HTML-ACC-003 — Etiketsiz form alanı

Bu alana klavyeyle gelen bir ekran okuyucu kullanıcısı, alanın ne istediğini nereden öğreniyor?

### HTML-STD-001 — Yinelenen id

Bu id'ye bağlanan bir etiket, bağlantı ya da betik iki öğeden hangisini bulur?

### HTML-STD-002 — DOCTYPE bildirimi yok

Tarayıcı bu belgeyi hangi kurallara göre çizeceğine nasıl karar veriyor? Bildirim olmadan düzen farklı tarayıcılarda aynı görünür mü?

### HTML-STD-003 — Dengesiz etiket

Bu etiket nerede kapanıyor? Kapanışı tarayıcı kendisi tahmin ederse sayfanın yapısı senin düşündüğünle aynı kalır mı?

*Kapsam ve sınırlar:* Kapanmayan öğe, eşi olmayan kapanış, iç içe karışan etiketler ve dosya sonunda bitmemiş açılış (`<div`). İsteğe bağlı kapanışlar (`p`, `li`, tablo bölümleri…), örtük kapanış (`<p>` blok öğeyle; `span` gibi satır içi öğelerin altından da, bulgu tetikleyen satırda), tablo hücresi kapsamı ve DOCTYPE'sız (quirks) belgede `table`'ın `p`'yi kapatmaması dikkate alınır. Aynı satırdaki farklı türde ihlaller tek bulguda birlikte anlatılır. Bilinen sınırlar: HTML5 ağaç kurma algoritmasının tamamı değil; biçimlendirme öğelerinin yeniden kurulması, tabloya yanlış konan içeriğin dışarı taşınması ve eski DOCTYPE'ların modu modellenmez — emin olunmayan durumda kural sessiz kalır.

### PY-DESIGN-001 — Değiştirilebilir varsayılan argüman

Varsayılan değer fonksiyon tanımlanırken bir kez oluşturulur. Fonksiyonu iki kez çağırdığında ikinci çağrı birincinin bıraktığı nesneyi mi görüyor?

### PY-DESIGN-002 — None ile eşitlik karşılaştırması

None bir değer mi, bir kimlik mi? Kendi `__eq__` yöntemi olan bir nesne bu karşılaştırmada ne döndürebilir?

### PY-EDGE-001 — Çıplak except

Bu blok hangi hataları yakalıyor? Beklemediğin bir hata (yazım hatası, Ctrl+C) da buraya düşerse fark eder misin?

### PY-PERF-001 — Döngüde doğrusal liste işlemi

Bu işlem listenin ne kadarını kaydırıyor ya da tarıyor? Döngüyle birlikte toplam iş girdi büyüdükçe nasıl artıyor?

### PY-RES-001 — with dışında open()

Bu dosya ne zaman kapanıyor? Okuma sırasında bir hata olursa kapanma satırına ulaşılır mı?

### UE-GC-001 — UPROPERTY'siz UObject alanı

Çöp toplayıcı yalnızca `UPROPERTY` ile işaretli alanları görür. Bu alanın gösterdiği nesne başka hiçbir yerden tutulmuyorsa GC onu toplar; alan ne gösterir?

### UE-MEM-001 — Reserve olmadan TArray::Add

Döngünün kaç kez döneceği belli ve her turda diziye bir eleman ekleniyor. Dizinin kapasitesi dolduğunda `Add` ne yapmak zorunda kalır ve bu döngüde kaç kez olabilir?

### UE-PERF-001 — Tick içinde ağır iş

`Tick` her karede çalışır. Bu iş gerçekten her karede mi gerekli, yoksa bir olaya, zamanlayıcıya ya da önbelleğe taşınabilir mi?

### UNITY-EVT-001 — Kaldırılmayan olay aboneliği

Bu abonelik `OnDisable`/`OnDestroy` içinde kaldırılmıyor. Nesne yok edildikten sonra olay tetiklenirse ne olur?

### UNITY-GC-001 — Sıcak yolda heap tahsisi

Bu satır her karede yeni bir nesne ayırıyor; çöp toplayıcı bunları bir noktada toplarken oyun takılabilir. Bu nesne bir kez oluşturulup yeniden kullanılabilir mi?

### UNITY-PERF-001 — Sıcak yolda bileşen/sahne araması

Bu arama her karede yeniden yapılıyor ama sonucu kareden kareye değişiyor mu? Sonucu bir kez bulup saklamak mümkün mü?

### UNITY-PERF-002 — Sıcak yolda string etiket karşılaştırma

`tag` özelliği her okunduğunda yeni bir string ayırır ve bu karşılaştırma sık çalışıyor. Unity etiket karşılaştırması için ayırma yapmayan hangi metodu sunar?
