# ADR-0018: Derleyicisiz kullanıcı için indirilebilir zig ve gömülü Roslyn

**Tarih:** 2026-10-03 · **Durum:** Kabul edildi · **Etkilenen bölümler:** mimari §5.2.2, §5.2.3, §12, §17; ADR-0009

## Bağlam

ADR-0009 ile Tier 1, makinede kurulu gcc/clang/dotnet'e bağlandı. Çoğu öğrencide bu araçlar
yok; Tier 1 o zaman `SKIPPED` kalıyor ve tree-sitter'ın görmediği tip/anlam hataları kaçıyor.
Docker yasak (ADR-0009). Faz 29 ölçümleri (Windows 11, 2026-10-03):

| Konu | Sonuç |
|---|---|
| `ziglang` 0.16.0 (PyPI wheel, zip) | 99 MB indirme, açılmış 382 MB (19.565 dosya) |
| `zig cc -` | Temizlenmiş ortamda çöker (`AppDataDirUnavailable`). Önbellek dizini verilince çalışır ama stdin'i önbellek dizinine `…-stdin.c` olarak **yazar**, tanılarda `<stdin>` yerine bu yolu basar |
| `zig clang <bayraklar> -x c -` | Kod yalnızca stdin'den okunur, diske dosya yazılmaz; tanı biçimi `<stdin>:L:C:`. `run_process` sınırlarıyla (Job Object 1024 MB) C 0,06–0,1 sn, C++ (`<iostream>`) 1,4 sn, Unreal stub 0,24 sn |
| `zig c++ -###` (başlık bayrakları için sonda) | Düz hâliyle 23–38 sn sürer ve 105 MB kütüphane derler; `-c` eklenince 0,19 sn sürer, bayraklar aynı kalır |
| Roslyn, `dotnet publish --self-contained -p:PublishSingleFile=true` | Kırpılmamış 83 MB, `PublishTrimmed=true` ile 14,8 MB; kırpma uyarısı yok, sözdizimi tanıları doğru (0,35–0,66 sn) |

## Karar

1. **C / C++ / Unreal:** zig'in içindeki clang doğrudan çağrılır:
   `zig clang <bayraklar> -x c|c++ -std=… -fsyntax-only … -`. `<bayraklar>` (hedef üçlüsü,
   `-nostdinc`, libc/libc++ `-isystem` yolları, `-D` tanımları) keşifte
   `zig cc|c++ -x … -c -fsyntax-only -### -` çıktısının `-cc1` satırından çıkarılır. Sonda boş
   girdiyle çalışır (kullanıcı kodu gitmez), zig önbelleği geçici bir dizindedir ve silinir.
   Tanılar mevcut clang ayrıştırıcısıyla okunur; include koruması, stub ve sınıflandırma
   değişmez.
2. **Keşif sırası** (`validation.toolchain_priority`): `path_first` (varsayılan) sistemdeki
   gcc/clang → `PATH`'teki zig → indirilen zig; `bundled_first` indirilen zig'i öne alır.
   C#: `dotnet` + `RoslynCheck.dll` → self-contained `RoslynCheck` (`bundled_first`'te ters).
   Zig yalnızca bir hedef boşta kalırsa sondalanır. Araçların kökeni (`system` / `downloaded` /
   `bundled`) `/health/ready`'de ve masaüstünde gösterilir.
3. **İndirme:** yalnızca zig indirilir. Kaynak PyPI `ziglang` wheel'i: her platformda zip olduğu
   için tek bir açıcı yetiyor ve sha256 PyPI'de yayımlanıyor. Adres ve sha256 platform anahtarıyla
   (`windows-x86_64`, `linux-aarch64`, `macos-aarch64` …) `codementor.toml`'daki
   `[validation.zig.sources]` tablosundan gelir (koda gömülmez). Hedef
   `validation.toolchain_dir` (varsayılan `~/.codementor/toolchain/zig`). Kurulum masaüstündeki
   "Derleyiciyi indir" düğmesiyle (ilerleme, iptal) ya da `codementor toolchain install zig` ile
   yapılır. API'de indirme uç noktası yoktur: sunucu kendiliğinden ikili dosya indirmez.
4. **Roslyn exe'ye gömülür:** trimmed self-contained tek dosya (~15 MB) CI exe işinde
   yayımlanır, `build_exe.py` bunu `tools/roslyn-check/sc` olarak pakete koyar ve varsa
   dotnet'e bağlı derlemeye tercih eder. İndirilmez, çünkü depo private ve kendi derlememiz için
   herkese açık bir adres yok. Kaynaktan kuranlar için `make roslyn-check-sc` hedefi var.

## Güvenlik (§12)

- Yalnızca https adreslerine izin verilir. Her istek (yönlendirme adımları dahil) bir httpx
  kancasıyla denetlenir; https olmayan bir adrese istek hiç gitmez. sha256 akış sırasında
  hesaplanır ve açmadan önce diskteki dosyadan yeniden doğrulanır. Toplam boyut
  `max_download_mb` ile sınırlıdır.
- Aynı `toolchain_dir`'e aynı anda tek kurulum yapılabilir. `.install.lock` üzerinde işletim
  sistemi kilidi tutulur (Windows `msvcrt.locking`, POSIX `flock`); süreç ölünce kilit bırakılır.
  Önceki çökmelerin artıkları yalnızca kilit alındıktan sonra temizlenir. `.part` adları
  benzersizdir; uyuşmazlık, kopma ya da iptalde silinir.
- Arşiv (`validation/archive.py`) yalnızca `ziglang/` önekli üyeleriyle, geçici bir staging
  dizinine açılır. Reddedilenler:
  - mutlak yol, sürücü harfi, `..`, `\`, `:` (NTFS akışı) ve NUL içeren adlar;
  - sembolik bağlantılar;
  - noktayla ya da boşlukla biten adlar (Windows bunları sessizce yeniden adlandırır);
  - ayrılmış aygıt adları (`CON`, `NUL.h`, `COM1` …);
  - büyük-küçük harf duyarsız çakışan adlar;
  - çözümlendiğinde staging dışına düşen hedefler.

  Açılmış boyut (bildirilen ve gerçekten yazılan) `max_extract_mb` ile, dosya sayısı
  `max_files` ile sınırlıdır. Bozuk, şifreli ya da desteklenmeyen sıkıştırmalı arşiv Türkçe
  hatayla reddedilir.
- Açılan zig C ve C++ için sondalanır; biri çalışmazsa kurulum geri alınır. Tamamlanma işareti
  (`.codementor-install.json`) staging'e yazılır. Ardından son iptal denetimi yapılır ve staging
  atomik olarak yerine taşınır. İşareti olmayan dizin kurulu sayılmaz (yarım kurulum). Eski
  kurulum, yenisi yerine geçene kadar silinmez; iki taşıma arasında çökülürse bir sonraki kurulum
  onu `.zig-old-*`'tan geri getirir.
- Sonda en az bir `-isystem` yolu bulamazsa zig kullanılmaz. Bu, sürüm değişince her
  `#include <…>`'in sessizce "bulunamadı" uyarısına dönmesini önler. Keşif hiçbir zaman istisna
  fırlatmaz (erişim hatası, TEMP yazılamaması, sonda hatası); sorun loglanır ve araç yok sayılır.
- Çalıştırma mevcut `run_process` sınırlarıyla yapılır (ADR-0010). Kullanıcı kodu diske
  yazılmaz: §5.2.3'ün ilkesi `zig cc` yerine `zig clang` kullanılarak korunur.
- Masaüstünde iptal bir işarettir. Arayüz "İptal ediliyor…" gösterir; sonuç (iptal ya da son
  anda tamamlanma) işçi iş parçacığı bitince gelir. Böylece "silindi" mesajı silme bittikten
  sonra görünür ve son anda tamamlanan kurulumda önbellek yine temizlenir.

## Sonuçlar

**Olumlu**
- Derleyicisi olmayan kullanıcı tek tıkla C/C++/Unreal için Tier 1 alır.
- Exe kullanıcısı C# Tier 1 için dotnet kurmak zorunda kalmaz (exe ~37 MB'tan ~52 MB'a çıkar).
- Clang ayrıştırıcısı ve Unreal stub yolu değişmeden yeniden kullanılır.

**Olumsuz / riskler**
- Disk kullanımı 382 MB, çünkü wheel bütün hedeflerin libc başlıklarını içeriyor. Yalnızca yerel
  hedefin başlıklarını tutacak bir budama "Sonraya" listesinde.
- zig sürümü yükseltilince `-cc1` satırının biçimi değişebilir; sonda başarısız olursa zig
  kullanılmaz ve Tier 1 eskisi gibi `SKIPPED` olur. Fixture testleri ve CI'daki zig testleri
  (`CODEMENTOR_REQUIRE_ZIG=1`) bunu yakalar.
- Linux'ta `RLIMIT_AS` altındaki davranış Windows'ta ölçülemedi; CI'daki zig testleri doğrular.
- Gömülü Roslyn yalnızca win-x64 exe'sinde var; macOS/Linux kaynak kullanıcısı `dotnet` yolunu
  kullanır.
