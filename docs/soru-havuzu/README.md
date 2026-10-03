# Soru Havuzu (aday sorular) — Analiz

Bu dizin, `docs/SORU_YAZIM_REHBERI.md` verilerek Antigravity'ye yazdırılan **1200 aday
soruyu** içerir. Sorular henüz bankada (`data/questions/`) **değildir**; buradan seçilip
düzeltilerek bankaya alınır.

| Dosya | Dil | Soru | Zorluk dağılımı | Motor |
|---|---|---|---|---|
| `c.md` | C | 200 | 50 / 50 / 50 / 50 | none |
| `cpp.md` | C++ | 200 | 50 / 50 / 50 / 50 | none |
| `csharp.md` | C# | 200 | 50 / 50 / 50 / 50 | none |
| `python.md` | Python | 200 | 50 / 50 / 50 / 50 | none |
| `html.md` | HTML | 200 | 50 / 50 / 50 / 50 | — |
| `css.md` | CSS | 200 | 50 / 50 / 50 / 50 | — |

Analiz tarihi: 2026-10-03. Yöntem: her ` ```yaml ` bloğu ayrıştırılıp `Question` modeliyle
doğrulandı, ardından `tests/unit/test_question_data.py`'deki banka kuralları (kimlik, başlık
tekliği, prompt uzunluğu, ipucu merdiveni, çözüm yolu, kontrol listesi eşleşmesi, Big-O
değişkenlerinin tanımı) ve sezgisel yöntem sızıntısı / Sokratik biçim taramaları uygulandı.

## 1. Özet

- **Şema:** 1200 sorunun **tamamı** `Question` şemasından geçiyor; YAML hatası yok.
- **Teklik:** Kimlik ve başlık çakışması yok — ne kendi aralarında ne mevcut 64 soruyla.
- **Kontrol listesi:** Her sorunun en az bir `concept_tags` etiketi ilgili dilin kontrol
  listesiyle eşleşiyor.
- **Bankaya doğrudan alınamaz**, çünkü her soru için istenen üç parçadan ikisi yok:
  referans çözüm (`private/solutions/`) ve `MATRIX` / `METHOD_LEAKS` satırları.
- **Motor sorusu yok:** Unity ve Unreal için tek soru üretilmemiş (1200'ün hepsi
  `engine: none`).

## 2. Kural ihlalleri (otomatik)

| Sorun | C | C++ | C# | Python | HTML | CSS |
|---|---|---|---|---|---|---|
| Başlıkta parantezli yöntem/etiket adı (ör. "(rowspan)", "(C#)") | 0 | 8 | 58 | 13 | 129 | 0 |
| İpucu 1-2 soru biçiminde değil (doğrudan talimat) | 148 | 200 | 200 | 8 | 0 | 0 |
| Big-O değişkeni metinde tanımsız / büyük harf | 0 | 0 | 0 | 11 | — | — |
| Hiç sorun bulunmayan | 200* | 192* | 142* | 176* | 71 | 200 |

\* "Hiç sorun bulunmayan" sütunu ipucu biçimini saymaz; ipucu biçimiyle birlikte C++ ve C#'ta
temiz soru **yoktur**.

### 2.1 İpuçları çözümü söylüyor (en ciddi sorun)

Rehber §4: ipucu 1 ve 2 **soru** olmalı ve çözümü vermemeli. C++ ve C#'ın tamamında, C'nin
easy/medium/hard bölümlerinde ipuçları talimat biçiminde ve yöntemi ele veriyor:

- `cpp-veryeasy-accumulate-elements` — 2: "…long long türünde bir sayaç kullanın."
- `cs-hard-actor-mailbox-queue` — 1: "Mesajları ConcurrentQueue içinde toplayın."

Bu, ürünün temel ilkesine (kodu düzeltmeyen Sokratik mentor) aykırıdır; bu sorular ipuçları
yeniden yazılmadan bankaya girmemeli. Python, HTML, CSS ve C very_easy bu açıdan temiz.

### 2.2 Yöntem sızıntısı

- **HTML:** Belgenin kendi notu, başlıklardaki parantezli etiket adlarının (örn.
  "(picture)", "(aria-live polite)") bilinçli olduğunu söylüyor. Bankada bu kabul edilmez
  (rehber §5): 129 başlıktan parantez kaldırılmalı.
- **C#:** Başlıklarda gereksiz "(C#)" eki ve kısıtlarda API adı (ör. "Interlocked ile …
  verilmelidir", "StringBuilder").
- **Diğer:** Prompt/kısıtlarda "kayan pencereyle", "iki işaretçi", "dinamik programlama",
  "yığın (heap)" gibi yöntem adları geçen sorular var (sezgisel taramada C 41, C# 85, Python 70, CSS 49 soru işaretlendi; bir kısmı yanlış
  pozitif. C++'ta imzalardaki `std::` taramayı anlamsızlaştırdığından sayı verilmedi).

### 2.3 Python'da Big-O değişkenleri

11 soruda `expected` büyük harf değişken kullanıyor (`V + E`, `E log V`, `N log k`,
`m*n*4^L`, `W*L`, `C`). Banka değişkenleri küçük harfe çevirir, metinde ise büyük harfle
geçer → `test_complexity_variables_are_defined` düşer. Örnekler:
`py-medium-clone-graph-nodes`, `py-hard-dijkstra-network-delay`,
`py-hard-word-search-grid-trie`. Çözüm: değişkenleri metinde küçük harfle tanımlamak
("v düğüm ve e kenar").

## 3. Nitel değerlendirme

**Güçlü yanlar**
- Dağılım dengeli (her dilde 4 zorluk × 50).
- C ve CSS en iyi durumda: prompt'lar uzun ve ölçekli (medyan 250-390 karakter), kısıtlar
  ölçülebilir, CSS'te hiçbir otomatik ihlal yok.
- HTML/CSS'te `expected` doğru biçimde yok; kavram etiketleri kontrol listesi
  sözlüğüne iyi oturuyor.

**Zayıf yanlar**
- **Klasik mülakat sorusu ağırlığı:** Aynı konu birçok dilde tekrar ediyor (114 konu birden
  fazla dilde; ör. `set-matrix-zeroes` ×4, `product-except-self` ×4, `trapping-rain-water`
  ×3). Bunlar CodeMentor'un statik kural/kontrol listesi gücünü (bellek sahipliği, yaşam
  döngüsü, sıcak yolda ayırma) az kullanıyor.
- **C# zor sorular ince:** Bazı prompt'lar tek cümle (ör. `cs-hard-actor-mailbox-queue`),
  `expected` anlamsız (`ActorMailbox: "1"`, işlem değil sınıf adı).
- **Kavram etiketi yığılması:** C++'ta `data-structures` 110, C#'ta 121, Python'da
  `design` 104 soruda — kontrol listesi seçimini ayırt edici kılmıyor.
- **Mevcut bankayla konu yakınlığı:** Kimlik çakışması yok ama C'de `check-palindrome-chars`,
  `lru-cache-implementation`; C++/C#'ta `lru-cache-sync` mevcut sorulara çok yakın.

## 4. Bankaya alma önerisi

1. Önce temiz ve yüksek değerli adayları al: **CSS** (200), **C very_easy** (50),
   **Python** (176 temiz), **HTML** (71 temiz + başlığı düzeltilen).
2. C++/C#/C (easy+) için ipuçlarını Sokratik soruya çevirmeden alma.
3. Her alınan soru için: referans çözüm + `MATRIX`/`METHOD_LEAKS` satırı + `questions validate`
   ve `pytest tests/unit/test_question_data.py`.
4. Tekrarlayan klasik konulardan dil başına en fazla biri; Unity/Unreal için ayrı üretim iste.
5. Bankanın yüzlerce soruya büyümesinin masaüstü/web soru seçicisine etkisi (arama,
   sayfalama) toplu alımdan önce değerlendirilmeli.
