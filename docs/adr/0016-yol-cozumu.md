# ADR-0016: Yapılandırma yollarının çözümü ve paket verisi

**Tarih:** 2026-10-01 · **Durum:** Kabul edildi · **Etkilenen bölümler:** mimari §16, §17, §18; ADR-0013

## Bağlam

`data/`, `prompts/`, `data/stubs/ue_stubs.h` ve `tools/roslyn-check/out/RoslynCheck.dll` gibi
yapılandırma yolları göreliydi ve çalışma dizinine göre çözülüyordu. Uygulama proje dışından
çalıştırılınca soru bankası ve şablonlar bulunamıyordu. Masaüstü uygulaması bunu açılışta çalışma
dizinini paket köküne alarak (`os.chdir`) geçiştiriyordu. Wheel'de ise `data/` ve `prompts/`
hiç yoktu, yani `pip install` ile kurulan paket çalışmıyordu.

## Karar

1. **Kaynak kökü** (`codementor.paths.resource_root()`):
   - exe'de (PyInstaller) `sys._MEIPASS`,
   - kurulu wheel'de `importlib.resources.files("codementor") / "_resources"`,
   - kaynaktan ya da düzenlenebilir kurulumda depo kökü.
2. **Wheel paket verisi:** hatch `force-include` ile `data/` → `codementor/_resources/data`,
   `prompts/` → `codementor/_resources/prompts`. Depoda dosyalar yerinde kalır, taşınmaz.
3. **Göreli yol, değerin geldiği yere göre çözülür:**
   - varsayılan değer → kaynak kökü (varsayılanlar mutlak yol olarak üretilir),
   - `codementor.toml` → toml dosyasının dizini (`Path` tipli alanlar introspeksiyonla bulunur),
   - ortam değişkeni ve CLI bayrağı → çalışma dizini (kullanıcının beklediği davranış).
4. Masaüstü `chdir` davranışı kaldırılmadı ama artık hiçbir şey ona bağlı değil.

## Sonuçlar

- `codementor` herhangi bir dizinden çalışır; wheel kendi başına yeterlidir.
- **Davranış değişikliği:** exe'nin yanındaki kullanıcı `codementor.toml`'undaki göreli yollar
  artık exe'nin dizinine göre çözülür (önceden paket köküne göreydi). Bu, kullanıcının kendi
  veri dizinini exe'nin yanına koymasını sağlar.
- Kapsam dışında kalanlar: soru dosyasındaki `reference_solution_path` (`private/solutions/`,
  pakete girmez) ve geliştirici araçlarının varsayılanları (`eval/dataset`, `eval/results`,
  `tests/golden`) çalışma dizinine göre kalır.
- Zip içinden içe aktarma (zipimport) desteklenmez: kaynak kökü gerçek bir dizin olmalıdır.

## Değerlendirilen alternatifler

- **`data/` ve `prompts/`'u `src/codementor/` altına taşımak:** yüzlerce yol referansı, belge
  ve test değişirdi; `force-include` aynı sonucu verir.
- **Tüm göreli yolları çalışma dizinine göre çözmeyi sürdürüp `chdir` yapmak:** kütüphane
  kullanımında ve CLI'da yan etkili, toml'un yerini yok sayar.
