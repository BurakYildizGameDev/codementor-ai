# CodeMentor AI — Zayıf ve geliştirilecek yönler

> **Tarih:** 2026-10-13 · **Sürüm:** 0.1.1 · **Yazan:** Claude Code (proje sahibiyle konuşmadan sonra)
> **Amaç:** Projenin nerede güçlü olduğunu değil, **nerede zayıf olduğunu** dürüstçe ve ayrıntılı
> yazmak; her zayıflık için somut bir iyileştirme yolu, ölçütü ve önceliği vermek.
> **Bu belge ne değildir:** teknik hata listesi değildir (o `docs/BulgularVeDuzeltilecekler.md`'de),
> faz planı değildir (o `docs/UYGULAMA_PLANI.md` ve `docs/DEVIR_FAZ_E_J.md`'de). Burası "ürün olarak
> ve proje olarak eksiklerimiz neler, bir sonraki seviyeye nasıl çıkarız" sorusunun cevabıdır.

---

## İçindekiler

1. [Özet: tek paragrafta durum](#1-özet)
2. [Konumlandırma: kimlerle karşılaştırıyoruz](#2-konumlandırma)
3. [Güçlü yanlar (kısa, bağlam için)](#3-güçlü-yanlar)
4. [Zayıf yönler — ayrıntılı](#4-zayıf-yönler)
   - 4.1 Pedagojik etki kanıtlanmadı
   - 4.2 Gerçek kullanıcı yok
   - 4.3 Eval seti küçük, tek modelli ve kısmen eski
   - 4.4 Kod çalıştırılmıyor: doğruluk değil, kusur aranıyor
   - 4.5 Mentor sorularının kalitesi ölçülmüyor
   - 4.6 LLM bağımlılığı: maliyet, gecikme, erişilebilirlik
   - 4.7 Yerel model yolu zayıf
   - 4.8 Statik kural kapsamı dar ve dengesiz
   - 4.9 Sızıntı koruması sezgisel
   - 4.10 İpucu merdiveni kaba ve soruya bağımlı
   - 4.11 Öğrenci modeli yok
   - 4.12 Öğretmen tarafı yok
   - 4.13 Dağıtım ve kurulum zahmetli
   - 4.14 Platform ve dil kapsamı
   - 4.15 Web arayüzü masaüstünün gerisinde
   - 4.16 Paylaşılan sunucu için hazır değil
   - 4.17 Kod tabanının sürdürülebilirliği
   - 4.18 Belgeler dağınık ve Türkçe-öncelikli
   - 4.19 Geliştirme süreci tek kişi + ajanlara bağımlı
5. [Geliştirme yol haritası (öncelik sırasıyla)](#5-geliştirme-yol-haritası)
6. [Öğrenci pilotu: adım adım deney tasarımı](#6-öğrenci-pilotu)
7. [Ölçüt panosu: neyi, nasıl ölçeceğiz](#7-ölçüt-panosu)
8. [Yapmamamız gerekenler](#8-yapmamamız-gerekenler)
9. [Portföy ve anlatım açısından](#9-portföy-ve-anlatım-açısından)
10. [Ek: zayıflık → iyileştirme özet tablosu](#10-ek-özet-tablo)

---

## 1. Özet

CodeMentor, "kodu düzeltmeyen, sorgulatan" bir mentor fikrini **teknik olarak ciddi** biçimde hayata
geçiriyor: deterministik analiz + LLM, satır kanıtıyla doğrulama, çözüm sızıntısı koruması, ölçülmüş
eval, 3.700+ test, 30 ADR. Bireysel bir proje için mühendislik kalitesi yüksek. **Ama bir eğitim
ürününün asıl kanıtlaması gereken şeyi — öğrencinin gerçekten daha iyi öğrendiğini — henüz
kanıtlamadı**; hiç gerçek kullanıcısı olmadı; eval küçük ve büyük ölçüde tek modelli; kod
çalıştırılmadığı için "çözüm doğru mu" sorusuna cevap veremiyor; dağıtımı zahmetli ve çoğunlukla
bir Claude CLI oturumuna bağımlı. Bir sonraki seviyeye çıkmanın yolu yeni özellik eklemekten çok
**ölçmek ve kullanıcıya açmaktır**: küçük bir öğrenci pilotu, mentor sorusu kalitesinin ölçülmesi,
test çalıştırarak doğruluk değerlendirmesi ve kurulumun basitleştirilmesi.

---

## 2. Konumlandırma

CodeMentor'u **kod yazdıran** araçlarla (GitHub Copilot, Cursor, ChatGPT/Claude sohbeti) karşılaştırmak
yanlış olur: onların amacı kodu yazmak/düzeltmek, CodeMentor'unki bilerek yazmamak. Doğru karşılaştırma
grubu **öğreten** araçlardır:

| Araç türü | Örnekler | Ne yapıyor | CodeMentor'a göre farkı |
|---|---|---|---|
| Eğitim amaçlı AI asistanları | CS50 Duck (Harvard), Khanmigo (Khan Academy), Codecademy/Coursera AI ipuçları | Sohbet tabanlı, cevabı vermemeye çalışan LLM | Gerçek öğrenci kitlesi ve araştırma verisi var; çoğu deterministik analiz yapmaz, "cevap vermeme" kuralını büyük ölçüde prompt'a bırakır |
| Otomatik not verenler | GitHub Classroom autograding, CodeGrade, Gradescope, Judge0 tabanlı sistemler | Kodu derler, testlerle çalıştırır, puan verir | Doğruluğu **kesin** ölçerler (test geçti/kaldı); geri bildirimleri genellikle "test X kaldı" düzeyinde, Sokratik değil |
| Statik analiz / linter | SonarQube, cppcheck, clang-tidy, Pylint, Roslyn analizörleri | Kural tabanlı kusur bulma | Çok daha geniş kural setleri, ama mesajlar profesyonel geliştiriciye göre; öğretici değil, cevabı söyler |
| Çevrimiçi yargıçlar | LeetCode, HackerRank, Codeforces | Test + süre/bellek ölçümü | Karmaşıklığı **ampirik** ölçer; ama neden yavaş/yanlış olduğunu öğretmez |

**CodeMentor'un nişi:** bu dört grubun kesişimi — statik analizin kesinliği + LLM'in açıklama gücü +
eğitim amaçlı "cevap vermeme" + oyun motoru (Unity/Unreal) bağlamı. Bu niş gerçek ve az dolu. Zayıflıklar
çoğunlukla bu nişin **kanıtlanmamış** olmasından ve rakiplerin güçlü olduğu alanlarda (test çalıştırma,
gerçek kullanıcı, geniş kural seti) geride kalınmasından geliyor.

---

## 3. Güçlü yanlar

(Zayıflıkları doğru tartmak için kısa bağlam.)

- **Hibrit mimari:** sözdizimi hatasında LLM hiç çağrılmıyor; LLM bulguları satır kanıtıyla doğrulanıyor;
  olgular prompt'tan çıkarılınca Big-O birebir doğruluk %96 → %85 düşüyor (ablasyon kanıtı).
- **Sızıntı koruması kodda, prompt'ta değil:** çıktı denetleniyor, çözüm sızdıran soru yeniden üretiliyor.
- **Ölçüm disiplini:** 166 elle etiketlenmiş örnek, dev/test ayrımı, sonuç dosyalarından üretilen ve testle
  denetlenen README tabloları. Dev'de precision %27 → %78, recall korunarak.
- **Güvenlik düşüncesi:** kod çalıştırılmıyor; derleyici yalıtımı; include koruması; prompt injection
  fixture'ları; tehdit modeli (`SECURITY.md`); birden fazla bağımsız güvenlik denetimi.
- **Mühendislik:** mypy strict, 3.700+ test, ağsız testler, ADR kültürü, otomatik ve doğrulanmış release.
- **Niş:** Unity/Unreal bağlamı, Türkçe öğrenci kitlesi.

---

## 4. Zayıf yönler

Her başlık aynı yapıda: **Durum** (bugün ne var) · **Neden önemli** · **Kanıt** (nereden biliyoruz) ·
**İyileştirme** (somut adımlar) · **Nasıl ölçülür** · **Öncelik / efor**.

Öncelik: 🔴 yüksek · 🟠 orta · 🟡 düşük. Efor: S (≤1 gün) · M (2-5 gün) · L (1-3 hafta) · XL (>3 hafta).

---

### 4.1 Pedagojik etki kanıtlanmadı 🔴

- **Durum:** Projedeki bütün metrikler **teknik**: bulgu precision/recall, Big-O doğruluğu, sızıntı oranı,
  prompt injection direnci, gecikme. "Öğrenci bu araçla daha iyi öğreniyor mu?" sorusuna dair tek bir
  veri yok.
- **Neden önemli:** Bir eğitim aracının varlık nedeni öğrenmedir. Teknik olarak kusursuz bir mentor,
  öğrenciyi sinirlendiriyorsa, ipucunu anlamsız buluyorsa ya da öğrenci aracı atlatıp ChatGPT'ye
  gidiyorsa başarısızdır. Ayrıca "Sokratik soru" yaklaşımının her öğrenci için iyi olduğu varsayımı
  tartışmalıdır: yeni başlayanlar bazen doğrudan örnekten daha iyi öğrenir (literatürde "worked
  example effect").
- **Kanıt:** `eval/` yalnız teknik metrikler içeriyor; README "Sonuçlar" bölümünde öğrenme ölçütü yok.
- **İyileştirme:**
  1. Küçük bir öğrenci pilotu (bkz. §6) — en değerli tek adım.
  2. Öğrenme ölçütlerini tanımla: hatayı **kendi başına** bulma oranı, kaç ipucu seviyesinde bulduğu,
     düzeltme süresi, aynı hata türünü sonraki görevde tekrar yapma oranı (transfer).
  3. Karşılaştırma koşulu: aynı görevler üç koşulda — (a) CodeMentor, (b) yalnız derleyici/test çıktısı,
     (c) serbest ChatGPT. Küçük örneklemde bile yön gösterir.
  4. Ön test / son test: pilotun başında ve sonunda aynı kavramlarla 3-4 kısa soru.
- **Nasıl ölçülür:** bkz. §7 "Öğrenme" satırları.
- **Öncelik / efor:** 🔴 · M (pilot hazırlığı) + L (yürütme ve analiz).

### 4.2 Gerçek kullanıcı yok 🔴

- **Durum:** Uygulamayı yalnız geliştirici ve kodlama ajanları kullandı. Yaklaşık 60 faz boyunca bulunan
  hataların büyük çoğunluğu iç denetimden geldi; gerçek kullanımdan gelen tek kaynak geliştiricinin kendi
  el testi (Faz 60-63).
- **Neden önemli:** Arayüz akışındaki sürtünmeler (hangi düğmeye basılacağı belirsizliği, uzun bekleme,
  anlaşılmayan soru), sorulardaki dil sorunları, beklenmedik kod biçimleri ancak gerçek kullanıcıyla çıkar.
  Ayrıca public bir repoda "kim kullanıyor?" sorusunun cevabı projenin ciddiyetini belirler.
- **Kanıt:** telemetri yok, kullanıcı geri bildirimi kanalı yok (issue şablonları yeni eklendi).
- **İyileştirme:**
  1. Pilot (§6).
  2. Uygulama içi **isteğe bağlı** geri bildirim: her mentor sorusunun yanında 👍/👎 ve "bu soru
     anlaşılmadı" düğmesi; yalnız yerel veritabanına yazılır, kullanıcı isterse dışa aktarır (gizlilik).
  3. GitHub Discussions'ı açmak; README'ye "deneyenlerden geri bildirim" çağrısı.
  4. Kısa bir tanıtım videosu/GIF (masaüstü akışı) — kullanıcıyı denemeye ikna eden şey.
- **Nasıl ölçülür:** pilot katılımcı sayısı, geri bildirim sayısı, issue sayısı, haftalık aktif kullanım
  (yerel sayaç, gönderilmeyen).
- **Öncelik / efor:** 🔴 · S (geri bildirim düğmesi) + M (tanıtım materyali).

### 4.3 Eval seti küçük, tek modelli ve kısmen eski 🔴

- **Durum:** 166 elle etiketlenmiş örnek (dev 96 / test 70). Ana sonuçlar `claude-opus-5-5` (`claude_cli`)
  için. Claude Haiku 4.5 ve Codex `gpt-6-luna` yalnız dev'in bir kısmında ölçüldü; Ollama, Gemini ve
  Anthropic API hiç ölçülmedi. **Test bölümündeki LLM satırı Faz 12'nin eski prompt'uyla** (precision %27);
  sonraki iyileştirmelerden sonra test yeniden koşulmadı (bilinçli: test bölümü "son bir kez" koşulacak).
- **Neden önemli:** Küçük veride bir örnek ~2-3 puan eder; sonuçların güven aralığı geniş. Tek model
  ağırlıklı ölçüm, "başka modelle de çalışır mı" sorusunu cevapsız bırakır. Eski test satırı README'de
  okuyucuyu yanıltabilir (precision 27 görüp projeyi zayıf sanabilir ya da dev'deki 78'i genellenebilir
  sanabilir).
- **Kanıt:** `README.md` Sonuçlar tablosu ve okuma notları; `eval/results/`.
- **İyileştirme:**
  1. **Test bölümünü güncel prompt'la bir kez koş** ve README'yi güncelle (dev'e dokunmadan; test
     sonuçları "son" kabul edilir). Bu tek başına README'nin en zayıf satırını düzeltir.
  2. Eval'i büyüt: dil başına en az 30 örnek (bugün dengesiz), özellikle CSS, HTML, Python ve Unreal.
     Etiketleme yönergesi zaten var (`docs/EVAL_ORNEK_REHBERI.md`).
  3. Güven aralığı: precision/recall için bootstrap ile %95 güven aralığı hesapla ve tabloya ekle
     (`eval/metrics.py`'ye küçük bir fonksiyon).
  4. İkinci bağımsız etiketleyici: 30 örneği ikinci kişi etiketlesin; etiketleyiciler arası uyum
     (Cohen's kappa) raporlansın. Bu, "etiketler doğru mu" sorusuna cevap verir.
  5. En az bir açık ağırlıklı model ve bir ucuz API modeliyle tam dev koşusu (maliyet/kalite eğrisi).
- **Nasıl ölçülür:** örnek sayısı, dil başına dağılım, güven aralığı genişliği, kappa, model sayısı.
- **Öncelik / efor:** 🔴 (test koşusu: S) · L (eval büyütme, ikinci etiketleyici).

### 4.4 Kod çalıştırılmıyor: doğruluk değil, kusur aranıyor 🔴

- **Durum:** ADR-0005 gereği kullanıcı kodu hiçbir zaman çalıştırılmaz. Tier 1 yalnız sözdizimi/tip
  denetimi (`-fsyntax-only`, Roslyn ayrıştırma). Big-O statik ipucu + LLM gerekçesidir, ölçülmüş süre
  değildir. Mantık hataları (yanlış çıktı) yalnız LLM ve kurallar yakalayabildiği kadar bulunur.
- **Neden önemli:** Öğrencinin en temel sorusu "kodum doğru mu?"dur. Otomatik not verenler ve çevrimiçi
  yargıçlar bunu test çalıştırarak kesin cevaplar. CodeMentor "şu satırda şu risk var" diyebiliyor ama
  "çözümün 7 testten 5'ini geçiyor" diyemiyor. Ayrıca "kodu çalıştırmıyoruz" sınırlaması, bulgu
  doğruluğunu da sınırlar: LLM'in "bu satır taşar" iddiasını gerçek bir girdiyle kanıtlayamıyoruz.
- **Kanıt:** ADR-0005, mimari §5.2, README Sınırlamalar.
- **İyileştirme** (güvenlik kararını bozmadan, aşamalı):
  1. **Görev başına test senaryoları** (soru bankasına `tests:` alanı: girdi → beklenen çıktı). Önce
     yalnız Python ve C için.
  2. **Yalıtılmış yürütme** — Docker kullanılmadan (proje kuralı). Seçenekler: WebAssembly çalışma
     zamanı (C/C++ → wasm, `wasmtime` ile yalnız stdin/stdout; dosya sistemi ve ağ yok), Python için
     Pyodide/wasm. Süre/bellek sınırı wasm içinde kesin uygulanabilir. Yeni bir ADR gerektirir
     (ADR-0005'i daraltan).
  3. Sonucu Sokratik dile çevir: "Boş dizi girdisinde programın ne yazdırdığını tahmin edebilir misin?"
     (hangi testin kaldığını göstermek yerine ipucu).
  4. Ampirik karmaşıklık: aynı çözümü n = 100, 1.000, 10.000 ile çalıştırıp süre eğrisinden Big-O tahmini;
     statik ipucuyla karşılaştırma (README yol haritasında v2.0).
- **Nasıl ölçülür:** test senaryosu olan görev oranı; yanlış çözümlerin yakalanma oranı (eval'e "doğru
  çalışan ama yavaş" ve "yanlış çıktı veren" örnek türleri eklenerek).
- **Öncelik / efor:** 🔴 · XL (yalıtım + soru bankası verisi). İlk adım (soru bankasına test alanı) M.

### 4.5 Mentor sorularının kalitesi ölçülmüyor 🔴

- **Durum:** Sokratik çıktı için ölçülen tek şey **sızıntı** (çözümü ele veriyor mu: %0). Sorunun
  **iyi** olup olmadığı — doğru hataya yönlendiriyor mu, anlaşılır mı, öğrencinin seviyesine uygun mu,
  tekrara düşüyor mu — ölçülmüyor. Faz 63-65 notları küçük modellerde tekrar eden/anlamsız soru
  sorununu zaten gösteriyor.
- **Neden önemli:** Sızıntısız ama işe yaramaz soru ("Kodunu tekrar gözden geçirdin mi?") da başarısızlıktır
  ve şu an metriklerde "başarılı" görünür.
- **Kanıt:** `eval/metrics.py` (sızıntı var, kalite yok); README yol haritası "LLM-as-judge ile Sokratik
  kalite puanı".
- **İyileştirme:**
  1. **Rubrik** tanımla (4-5 boyut, 1-3 puan): (a) doğru hataya işaret ediyor mu, (b) cevabı vermeden
     yönlendiriyor mu, (c) anlaşılır ve tek bir şey mi soruyor, (d) seviyeye uygun mu, (e) koda somut
     bağlanıyor mu.
  2. 50 soru-kod çiftini iki insanla rubrikle puanla (altın standart).
  3. LLM-as-judge: aynı rubrikle bir yargıç modeli; insan puanlarıyla korelasyonu ölç. Yeterliyse eval'e
     otomatik "soru kalitesi" metriği olarak ekle.
  4. Deterministik kapılar (Faz I'da planlı): aynı soruyu tekrar, kodda geçmeyen tanımlayıcıya atıf,
     çok uzun soru → yeniden üretim.
- **Nasıl ölçülür:** rubrik ortalaması (insan ve yargıç), yargıç-insan korelasyonu, deterministik kapıdan
  düşen soru oranı.
- **Öncelik / efor:** 🔴 · M (rubrik + insan puanı) + M (yargıç).

### 4.6 LLM bağımlılığı: maliyet, gecikme, erişilebilirlik 🟠

- **Durum:** Varsayılan sağlayıcı oturum açılmış bir **Claude Code CLI** (`claude_cli`). Tam analiz p50
  ~16-24 sn (iki geçiş + isteğe bağlı doğrulama geçişi). Maliyet sağlayıcıya göre değişiyor; CLI
  oturumunda kullanıcının aboneliğinden düşüyor.
- **Neden önemli:**
  - Öğrencinin çoğunun Claude Code aboneliği yok; API anahtarı almak ve ücret ödemek öğrenci için
    engel. Bu, kitleyi ciddi daraltır.
  - 20 saniye bekleme, "derle-çalıştır-düzelt" döngüsünde uzun. Öğrenci arada sekme değiştirir.
  - Okul/laboratuvar ortamında dış API'ye erişim kısıtlı olabilir.
- **Kanıt:** README Sağlayıcılar tablosu, gecikme satırı; ADR-0012.
- **İyileştirme:**
  1. **Kademeli yanıt:** statik bulgular ve derleme sonucu ~1 sn'de gösterilir (zaten hesaplanıyor),
     LLM bölümü geldikçe akar (web'de SSE var; masaüstünde aşama ilerlemesi var, ama bulguların
     erken gösterimi değil).
  2. **Tek geçiş modunu** küçük/hızlı modeller için varsayılan yapmayı ölç (gecikme ~yarıya iner).
  3. Ücretsiz/ucuz yol: Gemini ücretsiz katmanı (deneysel sağlayıcı zaten var, canlı doğrulanmadı) ya da
     yerel model (§4.7). Kurulum sihirbazında "API anahtarın yoksa şunu seç" rehberi.
  4. **Önbellek** zaten var; aynı kodu tekrar gönderen öğrenci için anında yanıt. Kurumsal kullanımda
     sınıf düzeyinde paylaşılan önbellek (aynı ödevin benzer hataları) düşünülebilir — gizlilik
     değerlendirmesiyle.
  5. Maliyet görünürlüğü zaten eklendi (token ve tahmini maliyet); kurumsal kullanım için aylık bütçe
     sınırı ayarı.
- **Nasıl ölçülür:** ilk anlamlı geri bildirime kadar süre (statik: <2 sn hedef), tam analiz p50/p95,
  analiz başına maliyet, "anahtarsız kurulum" başarı oranı (pilotta).
- **Öncelik / efor:** 🟠 · M.

### 4.7 Yerel model yolu zayıf 🟠

- **Durum:** Ollama sağlayıcısı var ama eval'de hiç ölçülmedi. Faz 63 el testinde küçük modellerde
  tekrar eden, koda değmeyen sorular ve anlamsız bulgular görüldü. Planlanan Faz I (eski 64-66) yapılmadı.
- **Neden önemli:** Çevrimdışı, ücretsiz ve gizlilik dostu kullanım ancak yerel modelle mümkün. Okullar
  için (öğrenci kodunu dışarı göndermemek) bu çok değerli bir satış noktası olabilir.
- **İyileştirme:** Faz I'nın üç parçası (`docs/BulgularVeDuzeltilecekler.md` §10):
  1. Ölçüm tabanı: 2-3 yerel modelle dev alt kümesi; soru tekrar oranı, koda değmeyen soru oranı,
     yanlış bulgu oranı, gecikme.
  2. Kalite korumaları: deterministik Sokratik kapı, küçük model profili (daha kısa prompt, tek geçiş,
     doğrulamayı büyük modele bırakma seçeneği).
  3. Hız: `keep_alive`, `num_ctx` ayarı, makineye göre model önerisi.
- **Nasıl ölçülür:** yerel modelde precision/recall ve soru kalitesi rubriği; "kabul edilebilir kalite"
  eşiğini önceden tanımla (ör. precision ≥ %60, sızıntı %0, rubrik ≥ 2/3).
- **Öncelik / efor:** 🟠 · L.

### 4.8 Statik kural kapsamı dar ve dengesiz 🟠

- **Durum:** 41 kural (Faz H1). Dile göre dağılım (bir kural birden çok dilde sayılır): C 8, C++ 9,
  C# 7, HTML 6, CSS 6, Python 5; motor: Unity 4, Unreal 3. En zayıf alan Python (5 kural); CSS ve C++
  Faz H1'de üçer yeni kural kazandı (CSS-ACC-001, CSS-LAYOUT-001/002, CPP-PERF-002..004) ve C'ye
  C-BUF-002 eklendi. Endüstri araçlarında (cppcheck, clang-tidy, SonarQube) yüzlerce kural var.
  Bilinen kaçırmalar ve yanlış pozitifler `docs/BulgularVeDuzeltilecekler.md` §10 Faz H'de.
- **Neden önemli:** Statik katman precision'ı yüksek (%100) ama recall düşük (%57,5). LLM recall'ı
  taşıyor; LLM olmayan (statik) modda kullanıcı bulguların yarısını kaçırır. Ayrıca statik kurallar
  deterministik ve hızlı — ne kadar çok şey statik yakalanırsa LLM'e o kadar az iş (ve maliyet) kalır.
- **İyileştirme:**
  1. ~~Faz H'deki 7 yeni kural ve bilinen kaçırma düzeltmeleri.~~ → Faz H1 (7 kural), H2 (CPP-OWN-001,
     CS-PERF-001) ve H3 (analiz verisi: `call_costs`, `parse_bigo`, maskeleme, stub, include koruması,
     kolon birimi) tamamlandı; statik dev F1 %71 → %73, precision %100'de kaldı.
  2. **cppcheck / clang-tidy entegrasyonu** (README yol haritası v1.1): bunların çıktısını
     Sokratik dile çeviren bir eşleme katmanı; seçili ve öğretici kontrollerle sınırlı tutmak şart
     (profesyonel uyarı seli öğrenciyi boğar).
  3. Kural önceliklendirmesi: eval'de LLM'in en sık bulduğu ama statik katmanın kaçırdığı hata türlerini
     listele → bunlar için kural yaz (veriye dayalı kural seçimi).
- **Nasıl ölçülür:** statik recall (Faz H4: %57,5), dil başına kural sayısı ve recall, yanlış pozitif oranı.
- **Öncelik / efor:** 🟠 · L.

### 4.9 Sızıntı koruması sezgisel 🟠

- **Durum:** Çözüm sızıntısı n-gram örtüşmesi, kod bloğu/satır tespiti ve yasaklı tanımlayıcı listesiyle
  yakalanıyor. Eval'deki %0, **ölçülen işaretler** için. Referans çözümü olmayan sorularda (serbest mod,
  kullanıcı soruları) yalnız kod örüntüsü kontrolü var.
- **Neden önemli:** Modelin çözümü "kelimelerle" anlatması ("bir hash set kullanırsan her aramayı sabit
  zamanda yaparsın") n-gram ve kod örüntüsünden kaçabilir. Bu, aracın temel vaadini zayıflatır.
- **Kanıt:** README Sınırlamalar; `verify/leak_guard.py`.
- **İyileştirme:**
  1. **Anlamsal sızıntı kontrolü:** bir yargıç model ya da küçük bir sınıflandırıcıyla "bu soru çözümü
     doğrudan söylüyor mu" sorusu (ayrı, ucuz çağrı; yalnız şüpheli durumlarda).
  2. Sızıntı eval'ini zenginleştir: "kelimelerle çözüm söyleyen" düşmanca örnekler (red team seti).
  3. Seviye bazlı politika: 3. seviyede kavram adı serbest ama algoritma adımları değil; bunu açık
     kurala dök ve test et.
- **Nasıl ölçülür:** red team setinde kaçan sızıntı oranı.
- **Öncelik / efor:** 🟠 · M.

### 4.10 İpucu merdiveni kaba ve soruya bağımlı 🟡

- **Durum:** Üç seviye (kavram → satır → yön), deneme sayısıyla artıyor (ADR-0026). Seviye içeriği
  büyük ölçüde LLM'e ve soru bankasındaki `hint_ladder` metnine bağlı. Kullanıcı sorularında (Faz K)
  ipuçları genel şablon.
- **Neden önemli:** Öğrenci ihtiyacı deneme sayısından çok **ne kadar yaklaştığına** bağlıdır. Hatanın
  yarısını düzelten öğrenciyle hiç dokunmayan öğrenci aynı seviyeyi alıyor.
- **İyileştirme:**
  1. **İlerleme farkındalığı:** önceki denemeyle karşılaştır (hangi bulgular kapandı, hangileri yeni);
     kapanan bulgu varsa seviyeyi artırmak yerine "iyi gidiyorsun, şimdi şuna bak" geri bildirimi.
  2. Öğrencinin seviyeyi kendi seçmesi (zaten "Bir ipucu daha" var) ile otomatik seviye arasında açık bir
     model.
  3. Kullanıcı sorularında ipucu üretimini LLM'e bırakma seçeneği (görev metninden ipucu merdiveni
     taslağı önerme; öğretmen onaylar).
- **Nasıl ölçülür:** pilotta "hatayı bulduğu seviye" dağılımı; gereksiz seviye atlama oranı.
- **Öncelik / efor:** 🟡 · M.

### 4.11 Öğrenci modeli yok 🟡

- **Durum:** Uygulama öğrenciyi tanımıyor: hangi kavramlarda sık hata yaptığı, hangi görevleri bitirdiği,
  ilerlemesi kayıtlı değil (geçmiş analiz listesi var, ama özet/çıkarım yok).
- **Neden önemli:** Kişiselleştirme (zayıf olduğu kavrama yönelik görev önerme, aynı hatayı üçüncü kez
  yapınca farklı açıklama) öğrenmeyi en çok artıran şeylerden biri.
- **İyileştirme:**
  1. Yerel "kavram profili": her analizden bulgu kategorisi + çözülme durumu → kategori başına sayaç.
  2. "Sık yaptığın hatalar" ekranı ve buna göre soru bankasından görev önerisi.
  3. Gizlilik: tamamen yerel, dışa aktarılabilir, silinebilir (Faz 62 deseni).
- **Öncelik / efor:** 🟡 · M.

### 4.12 Öğretmen tarafı yok 🟡

- **Durum:** Tek kullanıcılı tasarım. Öğretmenin ödev tanımlaması (Faz K ile kendi soru ekleme geldi, ama
  paylaşma yok), sınıfın genel hata dağılımını görmesi, ipucu merdivenini ayarlaması mümkün değil.
- **Neden önemli:** Eğitim araçları çoğunlukla öğretmen aracılığıyla yayılır. Öğretmenin "bu aracı
  derste kullanayım" demesi için kontrol ve görünürlük ister.
- **İyileştirme** (büyük iş, aşamalı):
  1. Soru paketi dışa/içe aktarma (Faz K'nın YAML biçimi zaten var → "sınıf paketi" zip'i).
  2. Öğrencinin isteğe bağlı olarak analiz özetini (kod olmadan) dışa aktarıp öğretmene vermesi.
  3. İleride: paylaşılan sunucu modu + öğretmen paneli (kimlik doğrulama, çok kiracılılık — §4.16).
- **Öncelik / efor:** 🟡 · L-XL.

### 4.13 Dağıtım ve kurulum zahmetli 🟠

- **Durum:** Windows exe **imzasız** (SmartScreen uyarısı); ~43 MB; açılışta bir LLM sağlayıcısı
  gerekiyor (varsayılan Claude Code CLI oturumu). Web için Python + uv + Node.js gerekiyor. macOS/Linux
  masaüstü paketi yok.
- **Neden önemli:** İlk 5 dakika deneyimi kullanıcıyı ya kazandırır ya kaybettirir. "Bilinmeyen yayıncı"
  uyarısı ve "önce şu CLI'ya oturum aç" adımı, teknik olmayan öğrenciyi kaybettirir.
- **İyileştirme:**
  1. **İlk açılış sihirbazı:** "Hangi model?" → seçeneğe göre adım adım (anahtar al bağlantısı, oturum
     aç düğmesi, bağlantıyı dene); bitince örnek bir görevle ilk analiz.
  2. Kod imzalama (sertifika maliyeti var; açık kaynak projeler için ücretsiz/ucuz seçenekler
     araştırılabilir) + Inno Setup kurulum paketi (Faz J).
  3. Web için tek komutla başlatma: `codementor serve --web` (derlenmiş web dosyalarını FastAPI'den
     sunmak; Node.js gerekmez).
  4. `pipx install codementor` / `uv tool install codementor` yolunu README'de birinci sınıf yapmak
     (wheel artık varsayılan yapılandırmayı içeriyor — Faz C).
- **Nasıl ölçülür:** pilotta "kurulumdan ilk analize süre" ve "yardımsız kurulum başarı oranı".
- **Öncelik / efor:** 🟠 · M (sihirbaz, `serve --web`) + L (imza, kurulum paketi).

### 4.14 Platform ve dil kapsamı 🟡

- **Durum:** Masaüstü "Oturum aç" Windows'ta yeni konsolda, Linux/macOS'ta sistem terminalinde
  açılıyor (Faz F, F12); diğer masaüstü davranışları hâlâ pratikte Windows'ta deneniyor.
  Diller: C, C++, C#, Python, HTML, CSS. JavaScript/TypeScript, Java yok — bunlar öğrencilerin en çok
  kullandığı dillerden. Arayüz ve tüm mesajlar Türkçe.
- **Neden önemli:** Türkçe odak bilinçli bir niş tercihi ve değerli; ama uluslararası görünürlüğü ve
  katkı alma şansını düşürüyor. JS ve Java'nın yokluğu potansiyel kullanıcıların büyük kısmını dışarıda
  bırakıyor.
- **İyileştirme:**
  1. Java ve JavaScript için Tier 0 (tree-sitter zaten destekliyor) + temel kurallar + eval örnekleri.
     Mimari dil eklemeye uygun (ADR-0015 deseni).
  2. Arayüz metinlerini tek bir dosyada topla (i18n altyapısı); İngilizce arayüz seçeneği. Prompt'lar
     ve mentor şablonları için dil parametresi.
- **Öncelik / efor:** 🟡 · L (her dil), L (i18n).

### 4.15 Web arayüzü masaüstünün gerisinde 🟠

- **Durum:** Web'de geçmiş yok, silme yok, API anahtarı gönderilemiyor, CSP yok (Faz E'de planlı).
  Masaüstündeki kullanıcı soruları, token geçmişi, bağlantı yönetimi web'de yok.
- **Neden önemli:** Web, Windows dışı kullanıcılar ve olası paylaşılan sunucu senaryosu için tek yol.
- **İyileştirme:** Faz E (`docs/DEVIR_FAZ_E_J.md` §5) + kullanıcı sorularının web'de listelenmesi
  (yazma ucu güvenlik incelemesinden sonra).
- **Öncelik / efor:** 🟠 · L (Faz E).

### 4.16 Paylaşılan sunucu için hazır değil 🟡

- **Durum:** Varsayılan yerel kullanım. Paylaşılan sunucu için: tek bir API anahtarı (kullanıcı kimliği
  yok), `session_id` sahipsiz (kimliği bilen başkasının ipucu merdivenini ilerletebilir, D16), hız
  sınırı yok (Faz E'de planlı), Tier 0 yalıtımı varsayılan kapalı, çok kiracılılık yok.
- **Neden önemli:** Okul/kurs kullanımı çoğunlukla merkezi bir sunucu ister.
- **İyileştirme:** kimlik doğrulama (OIDC ya da basit kullanıcı/parola), kullanıcı başına oturum ve
  geçmiş, kota, yönetici paneli; güvenlik denetimi. Bu büyük bir mimari adım; ayrı bir ADR serisi.
- **Öncelik / efor:** 🟡 (şimdilik) · XL.

### 4.17 Kod tabanının sürdürülebilirliği 🟠

- **Durum:**
  - 400 satır kuralını aşan dosya yok (boş satırlar sayılmaz): en büyükler `analysis/extractor.py` 396
    ve `config.py` 390. Faz F/G'de bölünenler artık sınırın altında: `desktop/app.py` 350,
    `pipeline/orchestrator.py` 350, `pipeline/passes.py` 323.
  - ~27 bin satır kaynak, ~39 bin satır test; tek geliştirici.
  - Masaüstü (CustomTkinter) testleri gerçek Tk penceresi açıyor: yavaş ve Linux CI'da atlanıyor
    (pencere testleri yalnız Windows'ta koşuyor).
  - Modüller arası bağımlılıklar katman sınırını zorluyordu; `report/usage.py` 62 satır ve yalnız
    `models/` içe aktarıyor — **kapandı** (Faz G).
  - Ertelenen küçük hatalar `PROGRESS.md` "Sonraya" ve "Denetim" notlarında birikiyor
    (46 açık madde / 120 madde; "açık" = üstü çizili olmayan tek düzey madde).
- **Neden önemli:** Büyüyen dosyalar ve biriken "sonraya"lar, yeni özellik eklemeyi yavaşlatır ve
  hata riskini artırır. Pencere testlerinin Linux'ta koşmaması, masaüstü gerilemelerinin CI'da
  yakalanmamasına yol açabilir.
- **İyileştirme:**
  1. Faz F0/G0 bölmeleri.
  2. Masaüstü mantığını görünümden ayırma (controller deseni zaten başladı) → mantık Tk'siz test edilir;
     pencere testleri azaltılır.
  3. Linux CI'da sanal ekranla (Xvfb) pencere testlerini koşmak — ya da Windows CI işinde masaüstü
     testlerinin kesin koştuğunu doğrulamak.
  4. "Sonraya" listesini çeyrekte bir gözden geçirip ya faza almak ya da bilinçli olarak kapatmak.
  5. İçe aktarma katmanlarını denetleyen bir test (ör. `report` → `storage` içe aktarması yasak).
- **Nasıl ölçülür:** 400 satırı aşan dosya sayısı (hedef 0), "Sonraya" madde sayısı, test süresi,
  kapsama (CI'da `--cov` var; hedef belirlenmemiş).
- **Öncelik / efor:** 🟠 · M.

### 4.18 Belgeler dağınık ve Türkçe-öncelikli 🟡

- **Durum:** `docs/` altında mimari (büyük), uygulama planı (büyük), bulgular, güncellemeler, devir
  belgeleri, eval rehberleri, 30 ADR; kökte README (TR), README.en.md (kısa), PROGRESS. Faz D'de iç
  belgeler `docs/gelistirme-gunlugu/`'ye taşındı ama hâlâ çok sayıda giriş noktası var.
- **Neden önemli:** Yeni bir katkıcı ya da işe alım yapan kişi "nereden başlayayım" sorusunda kaybolabilir.
  Uluslararası okuyucu için İngilizce belge çok sınırlı.
- **İyileştirme:**
  1. `docs/README.md`: belgelerin haritası ("şunu öğrenmek istiyorsan şunu oku").
  2. Mimari belgesinin başına 1 sayfalık "mimari özeti" ve bir diyagram.
  3. İngilizce: mimari özeti + ADR başlıklarının İngilizce listesi.
  4. Uygulama planı ve bulgular gibi "yaşayan" belgelerde tamamlanan bölümleri arşive taşıma rutini.
- **Öncelik / efor:** 🟡 · S-M.

### 4.19 Geliştirme süreci tek kişi + ajanlara bağımlı 🟡

- **Durum:** Proje tek geliştirici ve birden fazla kodlama ajanıyla (Claude Code, Codex, Antigravity, GLM,
  Mimo) geliştirildi. Ajan teslimlerinde uydurma sayılar, gevşetilmiş testler ve gerçek hatalar
  görüldü; hepsi denetimle yakalandı. Denetim kalitesi büyük ölçüde tek bir ajana (kod-denetci) ve
  geliştiricinin dikkatine bağlı.
- **Neden önemli:** "Ajanla geliştirme" anlatımı güçlü bir portföy hikâyesi, ama aynı zamanda bir risk:
  denetim atlanırsa sessiz gerilemeler girer (ör. Faz K'daki tkinter içe aktarması Linux CI'ı kırdı).
- **İyileştirme:**
  1. Ajan teslimlerini **otomatik** denetleyen bir betik: `git diff main...<dal> -- tests/` taraması (silinen
     test, eklenen `skip`), mutasyon kontrolü, görünmez karakter taraması, 400 satır, tkinter'sız içe
     aktarma — tek komut. (`docs/DEVIR_FAZ_E_J.md` §13'teki adımların betiğe dökülmesi.)
  2. Branch protection: main'e yalnız CI yeşilken birleştirme (GitHub ayarı).
  3. İnsan gözden geçirmesi için kısa PR şablonu (eklendi) ve "ajan teslimi" etiketi.
- **Öncelik / efor:** 🟡 · S-M.

---

## 5. Geliştirme yol haritası

Önerilen sıra (yukarıdaki maddelere atıfla). Her aşamanın **çıkış ölçütü** var; ölçüt sağlanmadan
sonrakine geçmemek öneriliyor.

### Aşama 0 — Public'e hazırlık (şimdi)
- Y2 (referans çözüm kontrolü), GitHub güvenlik ayarları, branch protection.
- **Çıkış:** repo public, CI yeşil, release çalışıyor.

### Aşama 1 — Ölç ve dürüstleştir (1-2 hafta)
- 4.3-1: test bölümünü güncel prompt'la koş, README'yi güncelle.
- 4.3-3: güven aralıkları.
- 4.5-1/2: Sokratik rubrik + 50 çiftin insan puanlaması.
- 4.2-2: uygulama içi 👍/👎 geri bildirim (yerel).
- **Çıkış:** README'deki her sayı güncel ve güven aralıklı; soru kalitesi için bir taban puan var.

### Aşama 2 — Kullanıcıya aç (2-4 hafta)
- 4.13-1: ilk açılış sihirbazı; 4.13-3: `serve --web`.
- 4.6-1: statik bulguların erken gösterimi.
- §6 öğrenci pilotu.
- **Çıkış:** en az 5 öğrenci pilotu tamamladı; kurulumdan ilk analize medyan süre ölçüldü; en az 20
  geri bildirim toplandı.

### Aşama 3 — Pilotun söylediğini düzelt (2-4 hafta)
- Pilottan çıkan ilk 5 sorun (ne olacağı önceden bilinmiyor; bilinçli olarak boş bırakıldı).
- Faz E/F (web ve masaüstü sağlamlık) — Antigravity devri.
- **Çıkış:** pilot sorunlarının ilk 5'i kapandı.

### Aşama 4 — Derinleş (1-3 ay)
- 4.4: görev başına test senaryoları + wasm tabanlı yalıtılmış yürütme (yeni ADR).
- 4.5-3: LLM-as-judge soru kalitesi metriği.
- 4.7: yerel model yolu (Faz I).
- 4.8: Faz H + cppcheck/clang-tidy eşlemesi.
- **Çıkış:** "kodum doğru mu" sorusuna en az Python ve C görevlerinde test sonucuyla cevap; yerel
  modelde kabul edilebilir kalite eşiği karşılandı ya da karşılanmadığı belgelendi.

### Aşama 5 — Genişle (3+ ay, isteğe bağlı)
- 4.14: Java/JavaScript, i18n.
- 4.11/4.12: öğrenci modeli, öğretmen paketleri.
- 4.16: paylaşılan sunucu.

---

## 6. Öğrenci pilotu

Projeyi bir sonraki seviyeye en çok taşıyacak tek adım. Küçük, etik ve tekrarlanabilir tasarlanmalı.

### 6.1 Amaç ve sorular
1. Öğrenciler hatayı CodeMentor'la **kendi başlarına** bulabiliyor mu? Kaçıncı ipucu seviyesinde?
2. Sorular anlaşılır mı? Hangi sorular "işe yaramadı" olarak işaretleniyor?
3. Öğrenci aracı atlatıp çözümü başka yerden mi alıyor (ChatGPT)?
4. Kurulum ve ilk kullanım nerede takılıyor?
5. (İsteğe bağlı) Aynı hata türünü sonraki görevde tekrar yapma oranı düşüyor mu?

### 6.2 Katılımcılar
- 5-10 öğrenci (C/C++/C#/Python bilen, başlangıç-orta seviye). Üniversite birinci/ikinci sınıf ya da
  kurs öğrencileri ideal.
- **Etik:** gönüllü katılım, kısa bilgilendirme metni, kod ve geri bildirimlerin anonimleştirilmesi,
  istenince silme. Öğrenci kodunu dış sağlayıcıya gönderiyorsak (Claude) bunu açıkça yaz. Kurum içi
  yapılıyorsa ilgili etik kurul/öğretmen onayı.

### 6.3 Görevler
- Soru bankasından 3 görev (kolay → orta → zor), her birinde **bilinen kasıtlı hata** içeren bir
  başlangıç kodu (öğrenci hatayı bulup düzeltmeli). Örn. `c-medium-linked-list` (serbest bırakılmış
  belleğe erişim), bir Python kenar durumu, bir C# Unity GC sorunu.
- Her görev için süre sınırı (ör. 20 dk) ve "bitirdim / vazgeçtim" düğmesi.

### 6.4 Prosedür
1. Kurulum (gözlemle, yardım etmeden; takıldığı yer not edilir).
2. Ön test: 4 kısa kavram sorusu (5 dk).
3. Üç görev; her gönderim uygulama tarafından yerel olarak kaydedilir (zaten kaydediliyor: analiz
   geçmişi, ipucu seviyesi, süre).
4. Her mentor sorusunda 👍/👎 (4.2-2).
5. Son test: ön testteki kavramların benzeri 4 soru.
6. 10 dakikalık kısa görüşme ya da anket: "en çok hangi soru işe yaradı / yaramadı", "ChatGPT'ye
   gitme isteği duydun mu", "tekrar kullanır mısın" (1-5).

### 6.5 Toplanacak veri (öğrenci izniyle, anonim)
- Görev başına: gönderim sayısı, hatayı bulduğu ipucu seviyesi (1/2/3/bulamadı), süre, son kod
  derleniyor mu / hata giderildi mi.
- Soru başına: 👍/👎, "anlaşılmadı" işareti.
- Kurulum: süre, takıldığı adım.
- Anket cevapları.

### 6.6 Analiz
- Hatayı bulma oranı ve seviye dağılımı (betimsel; örneklem küçük, istatistiksel test iddiası yok).
- En çok 👎 alan 10 soru → nitel inceleme → prompt/şablon değişikliği.
- Kurulum takılma noktaları → sihirbaz.
- Ön/son test farkı (yalnız yön göstergesi).
- Sonuçları `docs/PILOT_SONUCLARI.md`'ye ve README'ye kısa bir bölüm olarak yaz — "ölçülmüş iddialar"
  ilkesinin pedagojik karşılığı.

### 6.7 Başarı ölçütleri (önceden belirlenen)
- Öğrencilerin en az yarısı en az 2 görevde hatayı **3. seviyeden önce** buluyor.
- Mentor sorularının en az %70'i 👍.
- Yardımsız kurulum başarısı en az %80.
- "Tekrar kullanır mısın" ortalaması ≥ 3,5/5.
Ölçütlerin tutmaması başarısızlık değildir; neyin değişmesi gerektiğini söyler.

---

## 7. Ölçüt panosu

| Alan | Ölçüt | Bugün | Hedef (Aşama 2-4 sonu) | Nasıl ölçülür |
|---|---|---|---|---|
| Doğruluk | Denetim precision / recall / F1 (dev, Opus) | 78 / 96 / 86 | koru; güven aralığıyla raporla | `eval run --split dev` + bootstrap |
| Doğruluk | Denetim P/R/F1 (test, güncel prompt) | ölçülmedi (eski: 27/92/42) | ölçülmüş ve README'de | `eval run --split test --final` |
| Doğruluk | Statik recall | %55 | %65+ | statik dev eval |
| Doğruluk | Yanlış çözümün yakalanma oranı (test çalıştırarak) | yok | Python/C görevlerinde %90+ | yeni eval türü (4.4) |
| Güvenlik | Sızıntı (ölçülen işaretler) | %0 | %0 | eval |
| Güvenlik | Sızıntı (red team, anlamsal) | ölçülmedi | ≤ %5 | yeni red team seti (4.9) |
| Kalite | Sokratik rubrik ortalaması (insan) | yok | ≥ 2,3 / 3 | §4.5 |
| Kalite | Yargıç-insan korelasyonu | yok | ≥ 0,6 | §4.5 |
| Öğrenme | Hatayı 3. seviyeden önce bulma oranı | yok | ≥ %50 | pilot |
| Öğrenme | Soru 👍 oranı | yok | ≥ %70 | uygulama içi geri bildirim |
| Deneyim | Statik geri bildirim süresi | ~1 sn (hesaplanıyor, gösterilmiyor) | < 2 sn gösterim | ölçüm |
| Deneyim | Tam analiz p50 | ~16-24 sn | < 12 sn (tek geçiş/küçük model seçeneğiyle) | eval gecikme sütunu |
| Deneyim | Yardımsız kurulum başarısı | ölçülmedi | ≥ %80 | pilot |
| Erişim | Anahtar/abonelik gerektirmeyen çalışan yol | yok (yerel model ölçülmedi) | en az bir yol, kalite eşiğiyle | Faz I |
| Kod sağlığı | 400 satırı aşan dosya (boş satır hariç) | 0 (en büyük 396) | 0 | `wc -l` |
| Kod sağlığı | "Sonraya" madde sayısı (açık) | 46 (120 madde) | < 30 | PROGRESS |

---

## 8. Yapmamamız gerekenler

- **Özellik yarışına girmemek.** Copilot/Cursor gibi kod yazan araçlarla aynı özellikleri eklemek
  (otomatik düzeltme, tamamlama) projenin kimliğini yok eder. "Kodu düzeltmez" ilkesi bir sınırlama değil,
  ürünün kendisi.
- **Ölçmeden "daha iyi" demek.** Prompt ya da kural değişikliklerini eval'siz yayınlamamak (bugünkü
  disiplin korunmalı). Pedagojik iddiaları da pilot verisi olmadan yapmamak ("öğrenmeyi %X artırır" gibi).
- **Güvenlik sınırlarını kolaylık için gevşetmek.** Kod çalıştırmaya geçerken Docker yasağı ve
  "kullanıcı kodu güvenilmez" ilkesi korunmalı; wasm gibi gerçek yalıtım olmadan yürütme yok.
- **Uyarı seli.** cppcheck/clang-tidy entegre edilirken her uyarıyı öğrenciye göstermek; öğretici değeri
  olmayan bulgular öğrenciyi boğar ve güveni düşürür.
- **Telemetriyi izinsiz toplamak.** Geri bildirim ve kullanım verisi yalnız yerel ve açık izinle.
- **Her şeyi tek seferde.** §5'teki aşamalar sırayla; pilot öncesinde büyük mimari işlere (paylaşılan
  sunucu, yeni diller) girmemek.

---

## 9. Portföy ve anlatım açısından

Proje portföyde **çok güçlü**; aşağıdakiler onu daha da güçlü kılar:

- **Hikâye:** "LLM'in kodu düzeltmesi öğrenmeyi öldürüyor → hibrit bir mentor tasarladım → ölçtüm →
  öğrencilerle denedim." Son adım (öğrencilerle deneme) eksik; eklendiğinde hikâye tamamlanır.
- **Dürüstlük bir güçtür:** README'deki "Sınırlamalar" ve "Okuma notları" bölümleri (eski test satırı,
  küçük veri uyarısı) okuyucuya güven verir. Bu belgenin özeti de README'ye "bilinen zayıflıklar ve yol
  haritası" olarak bağlanabilir.
- **Ajanla geliştirme deneyimi:** birden fazla kodlama ajanını yönetme, denetleme ve onların hatalarını
  yakalama deneyimi değerli ve güncel bir beceri; bir blog yazısı/LinkedIn yazısı olarak anlatılabilir
  (somut örneklerle: uydurma sayılar, gevşetilen testler, Linux CI'ı kıran içe aktarma ve nasıl yakalandığı).
- **Görsel kanıt:** kısa bir demo videosu (30-60 sn) ve pilot sonrası "öğrenciler ne dedi" alıntıları.
- **İngilizce görünürlük:** README.en.md'yi genişletmek ve mimari özetini İngilizceye çevirmek,
  uluslararası işe alım için önemli.

---

## 10. Ek: özet tablo

| # | Zayıflık | Öncelik | Efor | İlk somut adım |
|---|---|---|---|---|
| 4.1 | Pedagojik etki kanıtlanmadı | 🔴 | M+L | §6 pilot tasarımını kesinleştir |
| 4.2 | Gerçek kullanıcı yok | 🔴 | S+M | uygulama içi 👍/👎 (yerel) |
| 4.3 | Eval küçük, tek modelli, test satırı eski | 🔴 | S→L | test bölümünü güncel prompt'la koş |
| 4.4 | Kod çalıştırılmıyor | 🔴 | XL | soru bankasına `tests:` alanı (Python/C) |
| 4.5 | Soru kalitesi ölçülmüyor | 🔴 | M | rubrik + 50 çiftin insan puanlaması |
| 4.6 | LLM bağımlılığı: maliyet/gecikme/erişim | 🟠 | M | statik bulguları erken göster |
| 4.7 | Yerel model yolu zayıf | 🟠 | L | Faz I ölçüm tabanı |
| 4.8 | Statik kural kapsamı dar | 🟠 | L | Faz H |
| 4.9 | Sızıntı koruması sezgisel | 🟠 | M | red team seti |
| 4.10 | İpucu merdiveni kaba | 🟡 | M | önceki denemeyle karşılaştırma |
| 4.11 | Öğrenci modeli yok | 🟡 | M | yerel kavram profili |
| 4.12 | Öğretmen tarafı yok | 🟡 | L-XL | soru paketi dışa/içe aktarma |
| 4.13 | Dağıtım zahmetli | 🟠 | M+L | ilk açılış sihirbazı, `serve --web` |
| 4.14 | Platform/dil kapsamı | 🟡 | L | Java/JS Tier 0 + temel kurallar |
| 4.15 | Web masaüstünün gerisinde | 🟠 | L | Faz E |
| 4.16 | Paylaşılan sunucuya hazır değil | 🟡 | XL | (pilot sonrası karar) |
| 4.17 | Kod tabanı sürdürülebilirliği | 🟠 | M | Faz F0/G0 bölmeleri |
| 4.18 | Belgeler dağınık | 🟡 | S-M | `docs/README.md` belge haritası |
| 4.19 | Tek kişi + ajan bağımlılığı | 🟡 | S-M | ajan teslimi denetim betiği |
