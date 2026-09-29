# ADR-0009: Docker zorunluluğunun kaldırılması — Tier 1 yerel derleyiciyle, opsiyonel

**Tarih:** 2026-09-29 · **Durum:** Kabul edildi · **Etkilenen bölümler:** mimari §3, §5.2.2–5.2.4, §9, §12, §15–19, §23; uygulama planı §3.1, Faz 4, Faz 13

## Bağlam

Mimari, Tier 1 derleyici doğrulamasını (gcc/clang `-fsyntax-only`, Roslyn) bir Docker
sandbox'ında çalıştırmayı öngörüyordu (§5.2.3). Pratikte:

- Geliştirme makinesi Windows; Docker kurulu değil. Docker Desktop + WSL2 kurulumu ağır,
  lisans ve kaynak maliyeti var, CI'da ayrı job gerektiriyor.
- Docker'a bağlı her şey (sandbox imajı, `docker.sock` bağlama) projeyi denemek isteyen
  herkese yüksek bir giriş eşiği koyuyor; asıl değer (Tier 0 + statik kurallar + LLM)
  Docker gerektirmiyor.
- Tier 1 zaten "opsiyonel, yoksa `SKIPPED`" olarak tasarlanmıştı; yani sistem Docker'sız
  çalışabiliyordu, ama Faz 4 tamamen Docker üzerine kuruluydu ve Docker'sız test edilemezdi.
- Derleyiciler yalnızca sözdizimi/tip denetimi yapıyor; kullanıcı kodu **çalıştırılmıyor**
  (ADR-0005). Sandbox'ın koruduğu asıl riskler derleyici üzerinden dosya okuma
  (`#include "/etc/shadow"`) ve kaynak tüketimi; bunlar süreç düzeyinde azaltılabilir.

## Karar

1. **Docker hiçbir yerde zorunlu değildir.** Sandbox imajı, `docker run` ve `docker.sock`
   bağlama mimariden çıkarılır.
2. **Tier 1, makinede kurulu derleyicileri doğrudan alt süreç olarak çalıştırır** ve
   tamamen opsiyoneldir:
   - C/C++: `PATH`'te bulunan `gcc`/`g++` veya `clang`/`clang++` (`-fsyntax-only`).
   - C#/Unity: `dotnet` varsa, repodaki `tools/roslyn-check` (yalnızca `CSharpSyntaxTree.ParseText`;
     dosya sistemine erişmez).
   - Unreal: `clang++ -include data/stubs/ue_stubs.h` (ADR-0007 geçerli: stub hataları `WARNING`).
   - İlgili araç yoksa → Tier 1 `SKIPPED` + uyarı; istisna yok, sistem Tier 0 ile devam eder.
3. **Yerel yürütme güvenlik önlemleri** (§5.2.3'ün yerini alır):
   - Kod **yalnızca stdin** ile verilir (`-x c -`); kullanıcı kodu diske yazılmaz.
   - **Include koruması** (derleyici çağrılmadan önce, maskelenmiş kod üzerinde):
     mutlak yol, `..`, sürücü harfi, ters eğik çizgi içeren; makro ile hesaplanan
     (`#include MACRO`) `#include`/`#import`, ayrıca `#embed` ve `__has_include` →
     Tier 1 çalıştırılmaz (`SKIPPED` + uyarı).
   - Çalışma dizini boş bir geçici dizin; ek `-I` yolu yok; ortam değişkenleri temizlenir
     (yalnızca `PATH`, `TEMP`/`TMP` ve derleyicinin gerektirdikleri).
   - Duvar saati zaman aşımı (`validation.compile_timeout_s`) → süreç ağacı öldürülür, `SKIPPED`.
   - Çıktı boyutu sınırı (ör. 64 KB); fazlası kesilir.
   - POSIX'te `RLIMIT_AS`/`RLIMIT_CPU`/`RLIMIT_NPROC` ile bellek/CPU/süreç sınırı;
     Windows'ta Job Object bellek sınırı (mümkün değilse yalnızca zaman aşımı — belgelenmiş risk).
   - Yerel bulunamayan başlık (`"WaveSpawner.h": file not found`) `FAILED` sayılmaz, `WARNING`'dir.
4. `validation.tier1_enabled` varsayılan `true` kalır; API sunucusu `127.0.0.1` dışına
   açılıyorsa belgede Tier 1'i kapatmak önerilir (§12).
5. Docker yalnızca **dağıtım için opsiyonel** bir paketleme yolu olarak kalabilir (Faz 13);
   uygulamanın hiçbir özelliği ona bağlı değildir.
6. `sandbox` pytest işareti `compiler` olarak yeniden adlandırılır: "gerçek derleyici
   gerektiren testler"; araç yoksa bu testler otomatik atlanır.

## Sonuçlar

**Olumlu**
- Kurulum eşiği düşer: Python + uv yeterli; derleyici varsa Tier 1 kendiliğinden devreye girer.
- Faz 4 Docker'sız, bu makinede (C# için `dotnet` ile) test edilebilir.
- CI basitleşir: ayrı sandbox job'u gerekmez; derleyicili testler GitHub runner'ında
  (gcc/clang kurulu) doğrudan çalışır.

**Olumsuz / riskler**
- Konteyner yalıtımı yok: derleyicinin kendisindeki bir açık host üzerinde çalışır.
  Azaltım: kod çalıştırılmıyor, include koruması, ortam/dizin yalıtımı, kaynak sınırları.
  Paylaşılan/çok kullanıcılı sunucuda Tier 1'in kapatılması önerilir.
- Windows'ta bellek sınırı zayıf; ağır şablon açılımı yalnızca zaman aşımıyla durdurulur.
- Sonuçlar makinedeki derleyici sürümüne bağlı olabilir (tanı metinleri farklılaşır);
  `diagnostics.py` gcc ve clang biçimlerini ayrıştırır, testler mesaj metnine değil
  satır/önem düzeyine bakar.

**Değişmeyenler:** Tier 0 her zaman çalışır (ADR-0001); kod çalıştırma yok (ADR-0005);
Unreal stub + uyarıya düşürme (ADR-0007); erken çıkış politikası tablosunun mantığı (§5.2.4).
