# Kural Kataloğu

> Bu dosya otomatik üretilir: `make rules-doc`
> (`uv run codementor rules doc --out docs/rules-catalog.md`). Elle düzenlemeyin.

Statik kurallar (mimari §5.3.3, §8.2). "LLM" tespitli maddeler burada değil,
`data/checklists/` altındaki kontrol listelerindedir. Bir kural `codementor.toml`
içinde `[rules] disabled = ["KURAL-ID"]` ile kapatılabilir.

Toplam: 10 kural.

| ID | Başlık | Dil | Motor | Kategori | Önem |
|---|---|---|---|---|---|
| C-BUF-001 | Sınır denetimsiz tampon fonksiyonu | c | — | memory_safety | high |
| C-MEM-001 | Serbest bırakılmayan bellek | c | — | resource_leak | high |
| CPP-OWN-001 | Çıplak new/delete | cpp | — | memory_safety | medium |
| CS-ALLOC-001 | Döngüde string birleştirme | csharp | — | garbage_collection | medium |
| CS-PERF-001 | Döngüde doğrusal arama | csharp | — | performance | medium |
| UE-GC-001 | UPROPERTY'siz UObject alanı | cpp | unreal | garbage_collection | high |
| UE-PERF-001 | Tick içinde ağır iş | cpp | unreal | performance | medium |
| UNITY-EVT-001 | Kaldırılmayan olay aboneliği | csharp | unity | resource_leak | medium |
| UNITY-GC-001 | Sıcak yolda heap tahsisi | csharp | unity | garbage_collection | high |
| UNITY-PERF-001 | Sıcak yolda bileşen/sahne araması | csharp | unity | performance | high |

## Açıklamalar

### C-BUF-001 — Sınır denetimsiz tampon fonksiyonu

`gets`, `strcpy`, `strcat` ve `sprintf` hedef tamponun boyutunu bilmez; girdi tampondan uzunsa bellek taşar. Hedefin kaç bayt aldığını nereden biliyorsun?

### C-MEM-001 — Serbest bırakılmayan bellek

Bu fonksiyonda `malloc`/`calloc` ile ayrılan bellek ne `free` ediliyor ne de fonksiyondan dışarı veriliyor. Fonksiyon bittiğinde bu bellek kimde kalıyor?

### CPP-OWN-001 — Çıplak new/delete

Nesnenin ömrü elle yönetiliyor. Arada bir istisna ya da erken `return` olursa `delete` çalışır mı? Sahipliği kim taşıyor?

### CS-ALLOC-001 — Döngüde string birleştirme

`string` değiştirilemez: her `+=` yeni bir metin ayırıp eskisini kopyalar. Döngü n kez dönerse toplam kaç karakter kopyalanır?

### CS-PERF-001 — Döngüde doğrusal arama

`List.Contains`/`IndexOf`/`Remove` elemanı bulmak için listeyi baştan sona tarar ve bu bir döngünün içinde. Toplam maliyet ne olur? Hangi veri yapısı bu aramayı daha hızlı yapar?

### UE-GC-001 — UPROPERTY'siz UObject alanı

Çöp toplayıcı yalnızca `UPROPERTY` ile işaretli alanları görür. Bu alanın gösterdiği nesne başka hiçbir yerden tutulmuyorsa GC onu toplar; alan ne gösterir?

### UE-PERF-001 — Tick içinde ağır iş

`Tick` her karede çalışır. Bu iş gerçekten her karede mi gerekli, yoksa bir olaya, zamanlayıcıya ya da önbelleğe taşınabilir mi?

### UNITY-EVT-001 — Kaldırılmayan olay aboneliği

Bu abonelik `OnDisable`/`OnDestroy` içinde kaldırılmıyor. Nesne yok edildikten sonra olay tetiklenirse ne olur?

### UNITY-GC-001 — Sıcak yolda heap tahsisi

Bu satır her karede yeni bir nesne ayırıyor; çöp toplayıcı bunları bir noktada toplarken oyun takılabilir. Bu nesne bir kez oluşturulup yeniden kullanılabilir mi?

### UNITY-PERF-001 — Sıcak yolda bileşen/sahne araması

Bu arama her karede yeniden yapılıyor ama sonucu kareden kareye değişiyor mu? Sonucu bir kez bulup saklamak mümkün mü?
