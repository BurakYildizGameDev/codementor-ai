# ADR-0013: Birincil istemci olarak masaüstü uygulaması (CustomTkinter + PyInstaller .exe)

**Tarih:** 2026-10-01 · **Durum:** Kabul edildi · **Etkilenen bölümler:** mimari §3.1, §16, §18, §19

## Bağlam

Mimari §3.1'de istemciler CLI, Web UI (React) ve REST istemcisiydi. Web UI'yi kullanmak için
iki süreç (`codementor serve` + `npm run dev`), Node.js ve bir tarayıcı gerekiyor. Kullanıcı
uygulamayı Windows'ta çift tıkla açılan tek bir **.exe** olarak istedi; örnek olarak aynı
geliştiricinin "AI-Driven Synthetic Data Studio" uygulamasını gösterdi (CustomTkinter arayüzü,
PyInstaller ile onefile/onedir paketleme). Hedef: o örnekten daha şık, CodeMentor'un tek işine
(kodu yaz/aç → denetle → Sokratik soru → ipucunu kademeli aç) odaklı bir arayüz.

Seçenekler:

1. **CustomTkinter + PyInstaller.** Saf Python, ek çalışma zamanı yok, örnek uygulamayla aynı
   aile. Monaco yok; editör `tk.Text` üzerine kurulur.
2. **pywebview + mevcut React arayüzü.** Monaco korunur, ama WebView2'ye bağımlı, arayüz yine
   web; kullanıcı "web arayüzü yerine" dedi.
3. **Electron/Tauri.** Node/Rust araç zinciri, büyük paket; projenin Python odaklı yapısına uymuyor.

## Karar

1. `src/codementor/desktop/` paketi (CustomTkinter). Çekirdeği **doğrudan** çağırır, sunucu
   açmaz: `api.state.ApiState` orkestratörü, veritabanını ve soru bankasını sağlar. Böylece
   analiz, önbellek, ipucu merdiveni (session_id) ve geçmiş API ile birebir aynı koddan geçer.
2. Thread modeli: Tk widget'larına yalnızca ana thread dokunur. Uzun işler (`analyze`,
   sağlayıcı ve derleyici denetimi) `desktop.bridge.Bridge` ile kendi thread'lerinde,
   kendi event loop'larıyla (`asyncio.run`) koşar; `StageEvent`'ler ve sonuç bir kuyruğa yazılır,
   ana pencere `after(60 ms)` ile okur. Görev başına "kuşak" sayacı: yeniden başlatılan ya da
   iptal edilen görevin geç gelen mesajları atılır.
3. Sunum mantığı (`viewmodel.py`: 13 aşama → 6 adımlık zaman çizelgesi, satır işaretleri,
   etiketler; `highlight.py`: sözdizimi renkleri) Tk'den bağımsızdır ve ayrıca test edilir.
4. Paketleme: `build_exe.py` → `dist/CodeMentor.exe` (onefile, açılış görselli) ve
   `dist/CodeMentor/` + `CodeMentor-<sürüm>-win64.zip` (onedir). Pakette `data/`, `prompts/`,
   varsayılan `codementor.toml` ve görseller bulunur. Göreli yollar için uygulama açılışta
   çalışma dizinini paket köküne (`sys._MEIPASS`) alır; exe'nin yanına konan `codementor.toml`
   paketteki varsayılanı geçersiz kılar. Pencereli exe'de stdout/stderr yoksa log
   `~/.codementor/desktop.log`'a yazılır.
5. Kullanıcı verisi `~/.codementor` altında: veritabanı (değişmedi), `desktop.json`
   (sağlayıcı, son dil/motor, ipucu oturumu, son dosyalar; `models.desktop.DesktopPrefs`) ve
   geçmişten yeniden açılabilsin diye analiz edilen kod (`desktop-sources/<analysis_id>.txt`;
   rapor kodu içermediği için). Kod yerel diskte kalır, hiçbir yere gönderilmez.
6. `web/` silinmez; ikincil istemci olarak kalır (CI işi sürer). Yeni özellikler önce
   masaüstüne gelir.
7. Docker yok (ADR-0009). API anahtarları yine yalnızca ortam değişkeninden okunur;
   masaüstü anahtar saklamaz.

## Sonuçlar

- Kurulum: Python/Node gerekmeden tek dosya. LLM sağlayıcısı yine gerekir (varsayılan
  `claude_cli`: `claude` PATH'te ve oturum açılmış olmalı). Derleyici yoksa Tier 1 atlanır.
- Boyut: onefile ~37 MB (örnek uygulama ~196 MB; bilimsel kütüphane yok).
- Monaco'nun zengin editörü yerine `tk.Text` + regex renklendirme: çoklu imleç, otomatik
  tamamlama yok. Mentorluk aracı için yeterli; tree-sitter analiz içindir, renklendirme için değil.
- Bağımlılıklar: `customtkinter`, `pillow` (çalışma), `pyinstaller` (geliştirme). customtkinter
  tip bilgisi yayımlamadığı için mypy'de `ignore_missing_imports` istisnası var.
- GUI testleri gerçek Tk penceresiyle koşar; ekran yoksa (Linux CI) atlanır, mantık testleri
  her yerde koşar.
