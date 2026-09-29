# ADR-0010: Tier 1 süreç sınırları — `RLIMIT_NPROC` yerine süreç grubu, Windows'ta Job Object

**Tarih:** 2026-09-29 · **Durum:** Kabul edildi · **Etkilenen bölümler:** mimari §5.2.3, §20; ADR-0009

## Bağlam

ADR-0009 ve mimari §5.2.3, Docker olmadan derleyiciyi çalıştırırken POSIX'te
`RLIMIT_AS` / `RLIMIT_CPU` / `RLIMIT_NPROC` kullanılmasını öngörüyordu. Faz 4 uygulamasında
şu sorunlar görüldü:

- **`RLIMIT_NPROC` kullanıcı başınadır, süreç ağacı başına değildir.** Çekirdek, sınırı
  o kullanıcının (gerçek UID) sistemdeki toplam süreç/iş parçacığı sayısıyla karşılaştırır.
  Geliştirme makinesinde veya CI'da kullanıcının zaten yüzlerce süreci varken küçük bir
  değer (ör. 16), gcc sürücüsünün `cc1`/`cc1plus` başlatmasını `EAGAIN` ile bozar;
  büyük bir değer ise hiçbir şeyi sınırlamaz. Ayrıca aynı UID ile çalışan paralel
  isteklerin birbirini etkilemesine yol açar.
- **`RLIMIT_AS` .NET ile uyumsuzdur.** .NET çalışma zamanı GC için çok büyük sanal adres
  alanı ayırır (commit etmez); sanal alan sınırı `dotnet`'i başlangıçta düşürür.
- Kod **çalıştırılmadığı** için (ADR-0005) süreç çoğaltma riski yalnızca derleyicinin kendi
  davranışıyla sınırlıdır: gcc/clang sürücüsü en fazla birkaç alt süreç başlatır.

## Karar

1. **POSIX:** `RLIMIT_NPROC` kullanılmaz. Derleyici yeni bir oturumda/süreç grubunda
   başlatılır (`start_new_session=True`); iş bittiğinde (normal çıkış, zaman aşımı veya
   beklenmedik hata) tüm grup `SIGKILL` ile öldürülür. Uygulanan sınırlar: `RLIMIT_CPU`
   (zaman aşımı + 1 s), `RLIMIT_CORE = 0`, `RLIMIT_FSIZE = 1 MB` ve derleyiciler için
   `RLIMIT_AS = validation.compile_memory_mb`. Sınırlar `preexec_fn` ile değil, derleyiciden
   önce çalışan küçük bir Python başlatıcısında (`python -I -S -c ...` → `os.execv`)
   uygulanır: `preexec_fn` çok iş parçacıklı bir sunucuda fork sonrası kilitlenebilir.
2. **Windows:** Süreç `CREATE_SUSPENDED` ile başlatılır, Job Object'e atanır, sonra devam
   ettirilir (yarış penceresi yok). İş: toplam commit bellek sınırı, **etkin süreç sayısı
   sınırı (8)**, `KILL_ON_JOB_CLOSE`, `DIE_ON_UNHANDLED_EXCEPTION`. İş bittiğinde
   `TerminateJobObject`. **İş kurulamazsa süreç öldürülür ve Tier 1 `SKIPPED` olur**
   (fail-closed; sınırsız çalıştırma yok).
3. **Roslyn (`dotnet`):** `RLIMIT_AS` uygulanmaz; bunun yerine `DOTNET_GCHeapHardLimit`
   bellek sınırının %75'ine ayarlanır. Windows'ta Job Object commit sınırı geçerlidir.
4. Bellek sınırı yapılandırmadan gelir: `validation.compile_memory_mb` (varsayılan 1024).

## Sonuçlar

- (+) Derleyici başlatma, kullanıcının diğer süreçlerinden bağımsız olarak güvenilir çalışır.
- (+) Windows'ta süreç sayısı sınırı gerçek anlamda süreç ağacı başınadır.
- (−) Linux'ta Roslyn (`dotnet`) için `RLIMIT_AS` yoktur; yalnızca yönetilen yığın sınırı
  (`DOTNET_GCHeapHardLimit`), `RLIMIT_CPU` ve zaman aşımı geçerlidir. Roslyn yalnızca
  `ParseText` çalıştırdığı ve girdi 40 KB ile sınırlı olduğu için kabul edilmiştir.
- (−) POSIX'te süreç sayısı için çekirdek düzeyi sınır yoktur; zaman aşımı ve süreç grubu
  öldürme ile sınırlanır. Paylaşılan sunucuda yine `validation.tier1_enabled = false`
  önerilir (§12); ayrı bir kullanıcı/cgroup ile çalıştırma Faz 13 dağıtım notudur.
- Testler: `tests/unit/test_runner.py` (zaman aşımında torun sürecin öldüğü, bellek sınırı,
  Windows'ta süreç sayısı sınırı, POSIX'te rlimit'ler).
