# Güncellemeler — Faz Faz (Faz 60-66)

**Tarih:** 2026-10-06 · **Kaynak:** kullanıcının masaüstü uygulamasındaki el testleri (ekran
görüntüleri) + `~/.codementor/codementor.db` geçmiş kayıtları + `desktop.log` + güncel kodla
karşılaştırma. Her bulgunun yanında kanıtı var; tahmin olan yerler "doğrulanmadı" diye yazılı.

## 0. Önce şunu bil: testler eski bir exe ile yapıldı

`dist/CodeMentor.exe` **2026-10-01 23:42**'de derlenmiş. Ondan sonra 34 faz geldi; aradaki
önemli farklar:

| Exe'de olmayan | Geldiği faz | Etkisi testlerde |
|---|---|---|
| Soru bankası 18 → 64 görev | Faz 30 (03.10) | "Ek sorular gözükmüyor" (exe'de 18 görev var: `dist/CodeMentor/_internal/data/questions`) |
| agy'nin stdin/stream-json çağrısı | Faz 28 (03.10) | Antigravity: `-p took "--output-format" as its prompt` hatası |
| Haiku için düşünme kapalı ayarı | Faz 34 (03.10) | Haiku'nun uzun beklemesi (doğrulanmadı, güncel sürümde yeniden denenmeli) |
| Bulgu doğrulama geçişi (`verify`) | Faz 35 (03.10) | Hiçbir koşuda `llm_v` aşaması yok; küçük modellerin uydurma bulguları süzülmedi |
| Rapordaki `usage_estimated`, `cost_est` alanları | Faz 25 (02.10) | Geçmiş açılırken çöküyor (yeni sürümün yazdığı raporları eski exe okuyamıyor) |

Yani 1 ve 2 numaralı sorunlar **güncel kodda zaten çözülmüş**; 6 büyük olasılıkla öyle. Ama
eski exe'nin farkına varılamaması da bir sorun (Faz 60).

## 1. Bulgular (kanıtlı)

| # | Gözlem | Kök neden | Güncel kodda? | Faz |
|---|---|---|---|---|
| 1 | Soru bankasında ek görevler yok | Eski exe (18 görev); güncel kodda 64 | Çözülmüş | 60 |
| 2 | Antigravity çalışmıyor | Eski exe'de argv sırası hatası; Faz 28'de düzeltildi. Kurulu agy artık 1.2.17 (kod 1.2.14'e göre doğrulandı) | Büyük olasılıkla çözülmüş; canlı doğrulanmalı | 63 |
| 3 | Claude iyi çalışıyor | — (26,3 sn, 3 isabetli bulgu, iyi sorular) | — | — |
| 4 | Dolphin 2.9 (7B) yavaş ve zayıf | 45,4 sn (43,7 sn analiz geçişi). Sorular koda değmiyor: "Bu sorunun neden önemli olduğunu açıklayın." Bulgusu kanıtsız diye atıldı | **Var** | 64-65 |
| 5 | Qwen 2.5 Coder 1.5B "çok iyi, 5 sn" | **Hızlı ama çıktı kullanılamaz:** aynı soru 3 kez tekrarlanıyor, "sonraki adım" metni döngüye girmiş (aynı cümle 4 kez), kavram başlığı koda uymuyor ("Karesel maliyet ve tamponu"), Big-O O(n²) dediği kod O(n), 0 bulgu | **Var** (tekrar/döngü denetimi yok) | 64-65 |
| 6 | Haiku çok uzun bekletiyor | Bugün kayıtlı Haiku analizi yok: analiz bitmeden kesilmiş. Eski exe'de Haiku düşünme ayarı yoktu (Faz 34) | Doğrulanmadı; canlı denenmeli | 63 |
| 7 | Geçmişi silme yok | Depolama, API ve masaüstünde silme işlemi hiç yok; kullanıcı kodu `desktop-sources/` altında da duruyor | **Var** (eksik özellik) | 62 |
| 8 | Qwen 2.5 Coder 14B "çok daha iyi" | 60,7 sn, 7 bulgu; **çoğu yanlış:** "n <= 0 ele alınmamış" (yüksek önem) ama 8. satır tam olarak bunu ele alıyor; "`i % 15` kontrolü daha pahalı" gibi 4 anlamsız performans bulgusu. Satırlar gerçek olduğu için kanıt denetiminden geçiyor | **Var** (anlamsal yanlışı yakalayan bir katman yok; doğrulama geçişi aynı küçük modelle) | 64-65 |
| 9 | (fark edilmeyen) Her analiz "Seviye 3/3" | Başarısız Antigravity denemesi (bozulmuş rapor) ipucu seviyesini 2 → 3 yaptı; Claude'un ilk gerçek analizi bile en açık ipucuyla geldi. Model karşılaştırırken her deneme seviye harcıyor | **Var** (hata) | 61 |
| 10 | (fark edilmeyen) Geçmiş açılırken çökme | Kayıtlı raporlar katı şemayla okunuyor (`extra="forbid"`); farklı sürümün yazdığı rapor Tkinter istisnası atıyor | **Var** (sürüm uyumu) | 60 |

**Dürüst değerlendirme:** Claude'la proje beklenen kalitede. Küçük yerel modellerde sorun
"yavaşlık" değil **kalite**: 1,5B hızlı ama tekrar eden, koda değmeyen sorular üretiyor; 14B
çok bulgu veriyor ama bulguların çoğu yanlış ve öğrenciyi yanlış yöne götürür. Mevcut
korumalar (şema, satır kanıtı, sızıntı) biçimi denetliyor, anlamı denetlemiyor. Faz 64-65
bunu ölçüp kapatmak için.

## 2. Fazlar

Sıra önceliğe göredir. Her faz `UYGULAMA_PLANI.md` protokolüyle uygulanır (plan, test,
`make check`, kabul kriterleri, PROGRESS).

### Faz 60 — Güncel exe ve sürüm uyumu (öncelik: yüksek)

**Amaç:** Kullanıcı hangi sürümü çalıştırdığını görsün; sürümler arası geçmiş çökmesin.
Uygulama ayrıntısı: [DEVIR_FAZ60_62.md](DEVIR_FAZ60_62.md) (Faz 60-62 GLM'e devredildi).

- [ ] Güncel `main`'den exe'yi yeniden derle (`uv run python build_exe.py --both`) ya da CI'nın
      `CodeMentor-win64` artefaktını kullan; 64 görev, agy ve geçmiş açma ile doğrula
- [x] Uygulama sürümünü ve derleme tarihini/commit'ini göster (durum çubuğu + Bağlantılar);
      CLI'da `codementor --version` aynı bilgiyi versin
- [x] Kayıtlı rapor okunamazsa çökme yok: geçmişte "bu rapor farklı bir sürümle oluşturuldu"
      mesajı ve kodun yine açılması; okuma, bilinmeyen alanları yok sayan ayrı bir yolla
      (API'nin katı şeması değişmez)
- [x] ~~Exe'de referans çözüm olmaması her analizde uyarı yazmasın~~ → Faz 31'de zaten
      çözülmüş (`load_reference`: dosya yoksa `log.debug`); logdaki uyarı eski exe'dendi
- [x] Testler: eski/yeni şemalı rapor geçmişten açılır; sürüm bilgisi testli

### Faz 61 — İpucu seviyesi adaleti (öncelik: yüksek, hata)

**Amaç:** İpucu merdiveni yalnız öğrencinin gerçek denemeleriyle ilerlesin.

- [x] Sağlayıcı kullanılamadığı için bozulmuş dönen deneme (model yok, CLI hatası, zaman aşımı)
      ipucu seviyesi harcamaz (`release_attempt`)
- [x] Karar + ADR: sözdizimi hatasıyla erken çıkış ipucu seviyesini ilerletmeli mi? (Öneri:
      ilerletmesin; içerik ipucu merdiveni ayrı)
- [x] Aynı kod + aynı görevle yalnız model değiştirilerek yeniden denetleme seviyeyi
      ilerletmesin (ya da masaüstünde "aynı seviyede başka modelle dene" seçeneği)
- [x] Testler: başarısız sağlayıcı, erken çıkış ve model değişimi senaryoları

### Faz 62 — Geçmişi silme (öncelik: orta, kullanıcı isteği)

**Amaç:** Öğrenci geçmişini ve kayıtlı kodunu silebilsin (gizlilik).

- [x] Depolama: tek analiz ve tüm geçmiş silme; ilgili oturum kaydı ve
      `~/.codementor/desktop-sources/*.txt` kod dosyaları da silinir
- [x] Masaüstü: satır başına sil, "Tüm geçmişi temizle" (onaylı); silinen analiz açıksa ekran
      temizlenir
- [x] API: `DELETE /v1/analyses/{id}` ve toplu silme (API anahtarı açıksa korumalı); web
      arayüzünde aynı düğmeler
- [x] Önbellek tutarlılığı: silinen analiz önbellekten dönmez
- [x] Testler: depolama, API, masaüstü görünüm modeli

### Faz 63 — Antigravity ve Haiku canlı doğrulaması (öncelik: orta)

**Amaç:** Güncel sürümde iki sağlayıcının gerçekten çalıştığını ölçerek kanıtlamak.

- [ ] agy 1.2.17 ile tek bir canlı analiz (kullanıcı onayıyla, kota harcar); argv/stream-json
      biçimi değiştiyse uyarla; `ADR-0012` notunu güncelle
- [ ] `claude_cli` + Haiku 4.5: aşama sürelerini ölç (`llm_a`, `llm_v`, `llm_b`); uzun bekleme
      sürerse nedenini bul (CLI açılışı, düşünme, şema onarımı, doğrulama geçişi)
- [ ] Geçiş başına süre sınırı ve arayüzde "model yanıt vermiyor, iptal et / başka modele geç"
- [ ] **Bağlantıyı dene** gerçek, küçük bir gidiş-dönüş yapıp süresini göstersin

### Faz 64 — Yerel model ölçüm tabanı (öncelik: orta; Faz 65'ten önce)

**Amaç:** İyileştirmeden önce ölç. Yerel modeller şimdiye kadar eval'de hiç ölçülmedi.

- [ ] `ollama` ile dev setinin bir alt kümesi (ör. 24 örnek; ardından 96): `qwen2.5-coder:1.5b`,
      `qwen2.5-coder:14b`, `dolphin-2.9.2-qwen2-7b`; two_pass ve single_pass
- [ ] Ek metrikler: soru tekrar oranı, koda değmeyen soru oranı, yanlış bulgu oranı (elle
      etiketli küçük bir alt küme), Big-O'nun statik ipucuyla çelişme oranı, gecikme (model
      yükleme ayrı)
- [ ] README'ye ayrı "yerel modeller" tablosu (Claude satırlarıyla karıştırılmadan)
- Not: token maliyeti yok, süre maliyeti var (14B ile 96 örnek ≈ 1,5-2 saat)

### Faz 65 — Küçük modeller için kalite korumaları (öncelik: orta)

**Amaç:** Zayıf model çıktısı öğrenciye gitmeden yakalansın; yakalanamıyorsa statik analize
dayalı şablon sorulara düşülsün. Kabul: Faz 64 tabanına göre ölçülebilir iyileşme.

- [ ] **Sokratik kalite kapısı (deterministik):** neredeyse aynı soruları ele, metindeki döngü
      tekrarını (aynı cümle/n-gram) yakala, seviye ≥ 2'de soruların koddaki bir ada ya da satıra
      değmesini iste; kapıdan geçemeyen çıktı yerine statik bulgulardan şablon sorular +
      uyarı (`degraded_socratic`)
- [ ] **Karmaşıklık politikası:** LLM statik ipucuyla çelişirse ve model "küçük" profildeyse
      statik ipucu gösterilir, LLM'in gerekçesi "model farklı düşünüyor" olarak işaretlenir
- [ ] **Bulgu sağduyu denetimi:** "X ele alınmamış / kontrol edilmiyor" iddiası, kanıt satırının
      kendisi bir denetimse (`if (n <= 0)`) düşürülür; küçük profilde bulgu sayısı ve önem tavanı
- [ ] **Model profili** (`[providers.ollama] profile = "small" | "standard"`, yapılandırmadan):
      kısa prompt (daha az few-shot, sıkıştırılmış kontrol listesi), varsayılan single_pass,
      sıcaklık 0, en fazla 3 bulgu
- [ ] İsteğe bağlı: doğrulama geçişini daha güçlü bir sağlayıcıya yönlendirme
      (`pipeline.verify_provider`), maliyet notuyla
- [ ] Faz 64 ölçümünü tekrarla; önce/sonra tablosu PROGRESS'e ve README'ye

### Faz 66 — Yerel modelde hız (öncelik: düşük)

**Amaç:** Dolphin 45 sn, 14B 61 sn. Kaliteyi bozmadan bekleme süresini düşürmek ve
görünür kılmak.

- [ ] `keep_alive` ile model bellekte tutulsun; ilk çağrıdaki model yükleme süresi ayrı
      ölçülüp arayüzde "model yükleniyor" olarak gösterilsin
- [ ] `num_ctx` prompt boyuna göre (gereğinden büyük bağlam yavaşlatır); ölçümle
- [ ] Akış (streaming) ile ilerleme: kullanıcı modelin yazdığını görsün
- [ ] Masaüstünde makineye göre model önerisi (VRAM'e sığan en büyük coder modeli)

## 3. Önerilen sıra

1. **Faz 60** (hemen): eski exe her şeyi karıştırıyor; yeni exe ile 1, 2 ve 6 yeniden denenir.
2. **Faz 61**: ipucu merdiveni hatası, karşılaştırmaları ve öğrenci deneyimini bozuyor.
3. **Faz 62**: istenen özellik, küçük ve bağımsız.
4. **Faz 63**: yeni exe ile canlı doğrulama.
5. **Faz 64 → 65**: önce ölç, sonra iyileştir, sonra yeniden ölç.
6. **Faz 66**: kalite oturduktan sonra hız.
