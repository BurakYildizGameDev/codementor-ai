# CodeMentor AI — Soru Yazım Rehberi

Bu belge, CodeMentor AI soru bankasına yeni soru yazacak bir yazar ya da yapay zekâ ajanı
içindir. Kurallara uyan soru, ek düzenleme gerektirmeden bankaya eklenir ve testlerden geçer.

## 1. Bağlam: CodeMentor ne yapar?

CodeMentor öğrencinin kodunu **düzeltmez**. Kodu denetler ve öğrenciye Sokratik sorular sorar.
Bir **soru** (görev), öğrencinin çözmeye çalıştığı programlama ödevidir. Öğrenci kodunu
gönderdiğinde sistem kodu bu sorunun hedeflerine göre değerlendirir:

- **Beklenen Big-O:** Kodun karmaşıklığı hedefle karşılaştırılır.
- **Kavram etiketleri:** İlgili kontrol listesi maddeleri bu etiketlerle seçilip modele verilir.
- **Soruya özgü kontrol maddeleri:** Modele "şuna da bak" diye verilir.
- **İpucu merdiveni:** Öğrenci "bir ipucu daha" dedikçe 1 → 2 → 3 sırayla açılır.
- **Referans çözüm:** Yalnızca sızıntı koruması için kullanılır; model çözümü öğrenciye
  söylerse bu yakalanır. Çözüm öğrenciye ya da modele **hiçbir zaman** gösterilmez.

Öğrenci yalnızca şunları görür: başlık, prompt, kısıtlar ve beklenen karmaşıklık. Kavram
etiketleri, kontrol maddeleri, ipuçları ve çözüm yolu gizlidir.

## 2. Teslim edilecekler (her soru için 3 parça)

| Parça | Yer | Not |
|---|---|---|
| Soru dosyası | `data/questions/<id>.yaml` | Dosya adı kimlikle birebir aynı olmalı |
| Referans çözüm | `private/solutions/<id>.<uzantı>` | Depoya girmez (`.gitignore`) |
| Test tablosu satırları | `tests/unit/question_tables.py` | `MATRIX` ve `METHOD_LEAKS` sözlüklerine birer satır |

Depoya doğrudan yazamıyorsan bu üç parçayı §9'daki biçimde tek bir yanıt olarak ver.

## 3. Dil, motor ve uzantılar

| Dil / motor | `language` | `engine` | Kimlik öneki | Çözüm uzantısı | `expected` |
|---|---|---|---|---|---|
| C | `c` | `none` | `c-` | `.c` | zorunlu |
| C++ | `cpp` | `none` | `cpp-` | `.cpp` | zorunlu |
| Unreal C++ | `cpp` | `unreal` | `unreal-` | `.cpp` | zorunlu |
| C# | `csharp` | `none` | `cs-` | `.cs` | zorunlu |
| Unity C# | `csharp` | `unity` | `unity-` | `.cs` | zorunlu |
| Python | `python` | `none` | `py-` | `.py` | zorunlu |
| HTML | `html` | `none` | `html-` | `.html` | **olmaz** |
| CSS | `css` | `none` | `css-` | `.css` | **olmaz** |

Zorluklar ve kimlikteki karşılıkları:

| YAML'daki `difficulty` | Kimlikte |
|---|---|
| `very_easy` | `veryeasy` |
| `easy` | `easy` |
| `medium` | `medium` |
| `hard` | `hard` |

Zorluk düzeyleri:

- **very_easy:** Tek kavram. Tek fonksiyon ya da kısa program. Tipik hata: başlangıç değeri,
  sınır koşulu, boş girdi.
- **easy:** Bir veri yapısı ya da bir dil özelliği. 2-3 kenar durum.
- **medium:** Performans ya da yaşam döngüsü tuzağı içerir (yineleyici geçersizleşmesi,
  döngüde sorgu, Tick maliyeti …).
- **hard:** Birden çok kavram bir arada. Gerçekçi ölçek (milyonlarca eleman, çok iş parçacığı,
  bellek sahipliği).

## 4. Soru dosyası biçimi

Gerçek bir örnek (`data/questions/c-medium-binary-search.yaml`):

```yaml
id: c-medium-binary-search
version: 1
language: c
engine: none
difficulty: medium
title: "Sıralı dizide arama ve ekleme konumu"
prompt: |
  Artan sırada sıralı, n elemanlı bir int dizisinde bir değeri arayan
  `ptrdiff_t find_position(const int *values, size_t n, int key)` fonksiyonunu yazın. Değer
  dizide varsa ilk geçtiği indeksi döndürsün; yoksa sıralamayı bozmadan ekleneceği indeks i
  için -(i + 1) döndürsün. Dizi iki milyardan fazla eleman içerebilir ve aynı değer birden çok
  kez geçebilir.
constraints:
  - "Çalışma süresi O(log n) olmalı"
  - "Çok büyük dizilerde indeks hesapları taşmamalı"
  - "Boş dizi (n = 0) ve aranan değerin tüm elemanlardan küçük ya da büyük olması doğru ele alınmalı"
expected:
  time: { find_position: "log n" }
  space: "1"
concept_tags: [binary-search, integer-overflow, edge-cases]
checklist_extra:
  - "Orta nokta (alt + üst) / 2 ile mi hesaplanıyor?"
  - "İşaretsiz bir indeks 0'dayken 1 çıkarılıp sarıyor mu?"
  - "Yinelenen değerlerde ilk geçiş mi döndürülüyor?"
reference_solution_path: private/solutions/c-medium-binary-search.c
hint_ladder:
  1: "Alt ve üst sınır iki milyara yakınken toplamları kullandığın türe sığıyor mu?"
  2: "Aralığı daraltırken üst sınırı 'orta - 1' yaptığında, orta 0 ise işaretsiz bir sayıya ne olur?"
  3: "Bu kavramlar 'orta nokta hesabında tamsayı taşması' ve 'işaretsiz sayının alttan sarması' olarak bilinir."
```

HTML ve CSS sorularında `expected` alanı **hiç yazılmaz**.

### Alan alan kurallar

**`id`**
- Biçim: `<önek>-<zorluk>-<konu>`, ör. `py-hard-shortest-path`.
- Yalnız küçük harf, rakam ve tire kullanılır; en az iki parça olmalı.
- Zorluk kısmı kimlikte geçmeli (`-veryeasy-`, `-easy-`, `-medium-`, `-hard-`).
- Bankada benzersiz olmalı; mevcut kimlikler §8'de.

**`version`**
- Yeni soruda her zaman `1`.

**`title`**
- Türkçe, en fazla 120 karakter.
- Bankadaki diğer başlıklardan farklı olmalı (büyük/küçük harf duyarsız).

**`prompt`**
- Türkçe, en az 80 karakter, YAML `|` blok biçiminde.
- Satırları yaklaşık 95 karakterde sarın.
- Kod bloğu (```) içermez. Fonksiyon imzası satır içi `ters tırnak` ile verilebilir.
- **Problemi tanımlar, yöntemi söylemez** (bkz. §5).
- Gerçekçi bir ölçek ve kenar durumlar verir: "liste boş olabilir", "bir milyon eleman",
  "yüzlerce aktör" gibi.

**`constraints`**
- En az 2 madde.
- Ölçülebilir ve denetlenebilir olmalı: "O(n) olmalı", "bellek sızıntısı olmamalı",
  "boş girdi doğru ele alınmalı".
- Yöntemi ele vermemeli: "deque kullanın" değil, "işlem başına sabit süre".
- Prompt'la çelişmemeli.

**`expected`** (yalnızca kod dillerinde)
- `time`: işlem adı → Big-O eşlemesi; en az bir işlem.
- `space`: tek bir Big-O ifadesi.
- Yazım: `"1"`, `"n"`, `"log n"`, `"n log n"`, `"n^2"`, `"n + m"`, `"n*m"`, `"k"`,
  `"n + m log m"`. Amortize sabit için `"1*"` kullanılır.
- `n` dışındaki her değişken (`m`, `k`, `d`, `p` …) prompt ya da kısıtlarda **ayrı bir kelime
  olarak tanımlanmalı**, ör. "m farklı IP vardır", "k dalga başına düşman sayısıdır".

**`concept_tags`**
- En az 2, tekrarsız; küçük harf ve tire.
- **En az biri** o dilin kontrol listesinde bir maddeyle eşleşmeli; listeler §6'da.
- Listede olmayan bir etiket de eklenebilir, ama eşleşen bir tane mutlaka olmalı.

**`checklist_extra`**
- En az 2 madde, soru biçiminde.
- Öğrenci kodunda bu soruya özgü **tipik hatayı** arar.

**`reference_solution_path`**
- Tam olarak `private/solutions/<id><uzantı>` olmalı.

**`hint_ladder`**
- Tam olarak 1, 2 ve 3 anahtarları; her ipucu en az 20 karakter.
  - **1:** Öğrencinin kendi kodunda bir duruma bakmasını sağlayan soru ("Liste boşken ilk
    satırın ne yapıyor?").
  - **2:** Daha yönlendirici bir soru; mekanizmayı düşündürür ama cevabı söylemez.
  - **3:** Kavramı **adlandırır** ve mutlaka "**olarak bilinir**" ifadesini içerir
    ("Bu kavram 'X' olarak bilinir.").
- İpuçları kodu ya da çözümü vermez.

### Yazım kuralları
- YAML'da metinleri çift tırnakla yazın. İçeride çift tırnak gerekiyorsa tek tırnak (`'`)
  kullanın.
- Kullanıcıya dönük her metin Türkçedir. Tanımlayıcılar (fonksiyon adları, API adları)
  İngilizce kalır.

## 5. Yöntem sızıntısı (en önemli kural)

Soru, öğrencinin **neyi** yapacağını söyler, **nasıl** yapacağını söylemez. Çözümün anahtar
yöntemi başlıkta, prompt'ta ya da kısıtlarda geçmemelidir.

| Kötü (yöntemi söylüyor) | İyi (problemi tanımlıyor) |
|---|---|
| "StringBuilder kullanarak raporu üretin" | "Metot n = 1.000.000 için birkaç yüz milisaniyede tamamlanmalı" |
| "deque ile BFS yazın" | "En az duraklı rotayı bulun; yüz bin istasyon olabilir" |
| "OnDisable'da abonelikten çıkın" | "Yok edilen dinleyiciler hata ya da sızıntı üretmemeli" |
| "weak_ptr ile ebeveyne işaret edin" | "Kök yok edildiğinde hiçbir düğüm bellekte kalmamalı" |

Her soru için 2-5 **yöntem işareti** belirleyin. Bunlar çözümde geçen ama soru metninde
geçmemesi gereken terimlerdir: API adları, anahtar sözdizimi, Türkçe yöntem adları. Örnekler:
`["remove_if", "erase_if", "erase-remove"]`, `["<dialog", "showmodal", "aria-labelledby"]`.

- Testler bu terimlerin hiçbirinin başlık, prompt ve kısıtlarda geçmediğini (büyük/küçük harf
  duyarsız) denetler.
- Testler ayrıca referans çözümde **en az birinin** geçtiğini denetler.
- Terimler kısa kelime parçaları olmamalı: `"rem"` Türkçe kelimelerin içinde geçer; bunun yerine
  `"1.125rem"` yazın.

## 6. Kontrol listesi etiketleri (dil başına)

`concept_tags` içinden en az biri buradan seçilmeli.

- **C:** amortized-analysis, arrays, binary-search, dangling-pointer, dynamic-memory, edge-cases,
  hashing, input-validation, integer-overflow, linked-list, loop-invariant, memory-safety,
  ownership, performance, pointer-arithmetic, pointers, realloc, state-machine, stdin, strings,
  undefined-behavior, use-after-free
- **C++:** concurrency, const-correctness, copies, cyclic-reference, data-race, data-structures,
  edge-cases, hash-map, integer-division, iterator-invalidation, lru-cache, move-semantics,
  operator-overloading, ownership, performance, raii, rule-of-five, rule-of-zero,
  signed-unsigned, smart-pointers, strings, trees
- **Unreal:** C++ etiketlerine ek olarak actor-component, delegates, events, gc-roots,
  lifecycle, object-pooling, reserve, tarray, tick, timers, tobjectptr, uproperty
- **C#:** allocation, async-await, concurrency, data-structures, deferred-execution, edge-cases,
  encapsulation, error-handling, floating-point, gc, hot-path, input-validation,
  integer-division, memory-leak, memory-safety, parsing, performance, resource-management, span,
  string-building, zero-allocation
- **Unity:** C# etiketlerine ek olarak caching, coroutine, data, events, files, frame-rate,
  input, instantiate, lifecycle, object-pooling, physics, scriptableobject, serialization,
  subscriptions, triggers, ui
- **Python:** boundary-conditions, data-structures, design, edge-cases, error-handling,
  exceptions, files, floating-point, graphs, hashing, input-validation, mutable-default,
  parsing, performance, resources, strings
- **HTML:** accessibility, dialogs, focus, forms, images, input-validation, links, lists,
  navigation, performance, security, semantics, standards, tables
- **CSS:** accessibility, animation, centering, color, edge-cases, focus, layout,
  maintainability, performance, positioning, responsive, specificity, stacking-context,
  typography, variables

Sorunuzun konusu bu listelerin hiçbirine uymuyorsa yeni bir kontrol maddesi gerekir. Bunu
teslimde ayrıca belirtin (bkz. §9); maddeyi bakımcı ekler.

## 7. Referans çözüm

- Sorunun **tüm** kısıtlarını karşılayan, örnek niteliğinde, derlenebilir bir çözüm yazın.
  Yöntem işaretlerinden en az biri çözümde geçmeli.
- **C/C++:** `-std=c17` / `-std=c++20 -Wall -Wextra` ile **uyarısız** derlenmeli. Yalnızca
  standart kütüphane kullanın; `strdup` gibi POSIX fonksiyonlarından kaçının. C'de `main`
  ekleyin.
- **C#:** Sözdizimi Roslyn'den hatasız geçmeli. Unity çözümlerinde `UnityEngine` kullanılabilir.
- **Unreal:** Gerçek motor başlıkları yoktur, bir stub başlıkla denetlenir. Sözdizimi geçerli
  olmalı. Stub'ın tanımadığı motor türleri (`Super`, `FMath` …) yalnızca uyarı verir, sorun
  değildir. Biçim: `#include "CoreMinimal.h"`, `UCLASS()`, `GENERATED_BODY()`,
  `UPROPERTY(...)`.
- **Python:** Python 3.12, tip ipuçlu, ayrıştırılabilir olmalı.
- **HTML/CSS:** Geçerli ve anlamsal olmalı. HTML'de `lang`, `charset` ve `viewport` olmalı.
- Yorumlar Türkçe olabilir. Çözüm öğrenciye gösterilmez; kısa ve doğru olsun.
- En fazla 256 KB.

## 8. Mevcut sorular (kimlik ve konu tekrarı yapmayın)

- **C:** calculator, max-of-array, palindrome, reverse-string, binary-search, linked-list,
  hash-table, stack
- **C++:** vector-sum, word-reverse, matrix-class, rule-of-zero, erase-while-iterating,
  tree-smartptr, lru-cache, thread-safe-queue
- **Unreal:** health-property, rotating-actor, overlap-pickup, timer-spawner, actor-component,
  cached-actor-lookup, actor-pool, tarray-gc
- **C#:** list-max, temperature-convert, bank-account, fizzbuzz-alloc, async-downloader,
  linq-report, event-bus, span-parser
- **Unity:** rigidbody-move, rotate-object, coroutine-spawner, trigger-events, component-cache,
  object-pool, inventory, save-system
- **Python:** grade-letter, list-average, shopping-cart, word-count, log-parser, two-sum,
  lru-cache, shortest-path
- **HTML:** link-list, recipe-page, contact-form, profile-card, data-table, image-gallery,
  dialog-form, site-navigation
- **CSS:** button-states, readable-typography, card-grid, centered-layout, sticky-header,
  theme-variables, animation-performance, specificity-refactor

Konu önerileri (henüz yok): özyineleme, sıralama algoritmaları, yığın/öncelik kuyruğu,
dosya G/Ç, metin ayrıştırma, bit işlemleri, iki boyutlu ızgara, durum makinesi, Unity
ScriptableObject olay kanalı, Unity UI Toolkit, Unreal arayüz (UINTERFACE), Unreal
Enhanced Input, Python dekoratör/bağlam yöneticisi, Python asyncio, HTML erişilebilir sekmeler,
CSS container queries.

## 9. Teslim biçimi (depoya yazamıyorsan)

Her soru için aşağıdaki bloğu doldur. Birden çok soru tek yanıtta sırayla verilebilir.

````markdown
### <id>

**question.yaml**
```yaml
id: ...
(§4'teki biçimde tam dosya)
```

**Referans çözüm (<id>.<uzantı>)**
```<dil>
(tam çözüm)
```

**Test tablosu**
```python
# MATRIX
"<id>": (Language.<C|CPP|CSHARP|PYTHON|HTML|CSS>, Engine.<NONE|UNITY|UNREAL>, Difficulty.<VERY_EASY|EASY|MEDIUM|HARD>),
# METHOD_LEAKS
"<id>": ["terim1", "terim2", "terim3"],
```

**Yeni kontrol maddesi gerekiyor mu?** Hayır / Evet: (madde metni ve etiketleri)
````

## 10. Doğrulama (depoya yazabiliyorsan)

```bash
uv run codementor questions validate                               # dağılım, etiketler, çözüm dosyaları
uv run pytest tests/unit/test_question_data.py -q                  # alan kuralları, yöntem sızıntısı
uv run pytest tests/compiler/test_reference_solutions.py -m compiler -q   # çözümler derleniyor mu
```

Üçü de yeşil olmadan soru teslim edilmiş sayılmaz.

## 11. Son kontrol listesi

- [ ] Kimlik `<önek>-<zorluk>-<konu>` biçiminde, benzersiz ve dosya adıyla aynı
- [ ] Başlık benzersiz ve en fazla 120 karakter
- [ ] Prompt en az 80 karakter, kod bloğu yok, yöntemi söylemiyor, ölçek ve kenar durumlar var
- [ ] En az 2 kısıt; ölçülebilir ve prompt'la çelişmiyor
- [ ] `expected` kod dillerinde var, HTML/CSS'te yok; `n` dışındaki değişkenler metinde tanımlı
- [ ] En az 2 `concept_tags`, en az biri §6'daki listede
- [ ] En az 2 `checklist_extra`, soru biçiminde
- [ ] 3 ipucu; 1 ve 2 soru biçiminde ve çözümsüz, 3'te "olarak bilinir"
- [ ] `reference_solution_path: private/solutions/<id><uzantı>`
- [ ] Referans çözüm derleniyor ve yöntem işaretlerinden en az birini içeriyor
- [ ] `MATRIX` ve `METHOD_LEAKS` satırları eklendi; terimler soru metninde geçmiyor
- [ ] Türkçe yazım ve teknik iddialar doğru (güncel tarayıcı ve motor davranışına göre)
