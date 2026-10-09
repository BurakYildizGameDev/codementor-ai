# ADR-0027: toml'daki göreli yol bulunamazsa kaynak köküne düşülür

**Tarih:** 2026-10-09 · **Durum:** Kabul edildi · **Değiştirdiği:** ADR-0016 karar 3 · **Etkilenen bölümler:** mimari §17

## Bağlam

Masaüstündeki "Seçimleri codementor.toml'a yaz" düğmesi (Faz 24), exe'nin yanında toml yoksa
paketteki varsayılan `codementor.toml`'u oraya olduğu gibi kopyalar. Kopyalamak gerekir: exe
yanındaki toml varken paketteki varsayılan hiç okunmaz, ayarlar (sağlayıcı komutları, Tier 1
ayarları) kaybolmasın.

ADR-0016'ya göre toml'daki göreli yollar toml'un dizinine göre çözülür. Kopyalanan dosyadaki
`questions_dir = "data/questions"`, `call_costs_file = "data/call_costs.yaml"`,
`stub_header = "data/stubs/ue_stubs.h"` artık `<exe dizini>/data/...` olur; orada veri yoktur.
Sonuç: exe'de soru bankası boş görünür ve her analiz `CallCostError` ile düşer (kullanıcı bunu
"sağlayıcıya bağlanılamıyor" diye görür). Hata 2026-10-09'da `desktop.log`'da görüldü.

## Karar

`codementor.toml`'daki göreli yol önce toml'un dizinine göre çözülür. O yol yoksa ve aynı göreli
yol kaynak kökünde (`paths.resource_root()`) varsa kaynak kökü kullanılır. İkisinde de yoksa
toml dizini kalır (ör. henüz oluşturulmamış veritabanı dosyası). Mutlak yollar değişmez.
Uygulama: `codementor.paths.resolve_config_relative`, `_RelativeTomlSource`.

**Yazılabilir yollar hariç (denetim O3):** uygulamanın yazdığı `storage.db_path` ve
`validation.toolchain_dir` her zaman toml dizinine çözülür (`config.WRITABLE_PATHS`). Aksi halde
paketteki aynı adlı bir dizine (ör. `tools/`) düşüp exe'nin her kapanışta silinen geçici
dizinine indirme yapılabilirdi.

## Sonuçlar

- Daha önce kopyalanıp bozulmuş toml'lar da kendiliğinden düzelir; kullanıcının dosya silmesi
  gerekmez.
- Kullanıcı exe'nin yanına kendi `data/questions` dizinini koyarsa o yine önceliklidir
  (ADR-0016'nın sağladığı olanak korunur).
- Kaynaktan çalışırken toml depo kökündedir, kaynak kökü de odur; davranış değişmez.
- Yazım hatalı bir yol, kaynak kökünde aynı adla bir dosya varsa sessizce oraya çözülebilir;
  göreli yollar `data/...` biçiminde olduğundan kabul edilebilir.

## Değerlendirilen alternatifler

- **Kopyalarken yol alanlarını silmek ya da mutlak yapmak:** onefile exe'de kaynak kökü her
  açılışta değişen geçici dizindir, mutlak yol tutulamaz; alanları silmek ise zaten kopyalanmış
  bozuk dosyaları düzeltmez.
- **Exe yanındaki toml'u paketteki varsayılanın üstüne katman olarak okumak:** daha büyük bir
  yapılandırma değişikliği; bu hata için gereksiz.
