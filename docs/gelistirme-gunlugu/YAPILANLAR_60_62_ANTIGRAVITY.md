# CodeMentor AI — Faz 60, 61 ve 62 Yapılanlar Raporu (Antigravity)

**Tarih:** 07.10.2026  
**Geliştirici Ajan:** Antigravity  
**Kaynak Belge:** [`docs/DEVIR_FAZ60_62.md`](DEVIR_FAZ60_62.md)  
**İzleme:** [`PROGRESS.md`](../../PROGRESS.md) ve [`docs/GUNCELLEMELER.md`](../GUNCELLEMELER.md)

---

## 1. Yönetici Özeti ve Git Dal Ağacı

Bu raporda, `docs/DEVIR_FAZ60_62.md` belgesinde devredilen üç öncelikli fazın (Faz 60, Faz 61 ve Faz 62) Antigravity tarafından uçtan uca uygulanması, test edilmesi ve belgelenmesi detaylandırılmıştır.

Geliştirme süreci, projenin altın kurallarına uygun olarak ardışık git dallarında ve sırayla yürütülmüştür:

| Faz | Dal | Taban Dalı | Commit | Mesaj |
|---|---|---|---|---|
| **Faz 60** | `faz/60-surum-uyumu` | `main` | `2990d0f` | `feat(faz-60): sürüm bilgisi ve sürümler arası geçmiş uyumu` |
| **Faz 61** | `faz/61-ipucu-merdiveni` | `faz/60-surum-uyumu` | `7d65893` | `fix(faz-61): ipucu merdiveni yalnız sayılan denemelerle ilerler` |
| **Faz 62** | `faz/62-gecmis-silme` | `faz/61-ipucu-merdiveni` | `b33b6aa` | `feat(faz-62): geçmişi ve saklanan kodu silme` |

*Not: Hiçbir commit'te AI ya da üçüncü taraf imza etiketi (Co-Authored-By / Generated with) kullanılmamıştır.*

---

## 2. Faz 60 — Sürüm Bilgisi ve Sürümler Arası Geçmiş Uyumu

### 2.1. Çözülen Sorunlar
1. **Sürüm Belirsizliği:** Kullanıcının hangi exe veya kaynak sürümünü çalıştırdığı (versiyon, commit hash, derleme tarihi) arayüzde ve CLI'da net olarak görülemiyordu.
2. **Geçmiş Açılırken Çökme:** Yeni CodeMentor sürümlerinin yazdığı raporlarda bulunan yeni alanlar (`usage_estimated`, `cost_est` vb.), katı şemayla (`extra="forbid"`) çalışan eski/farklı sürümler tarafından okunurken `ValidationError` ve `DetachedInstanceError` fırlatıyor, masaüstü arayüzünün çökmesine yol açıyordu.

### 2.2. Yapılan Geliştirmeler
- **Veri Modeli (`src/codementor/models/build.py`):**
  - `BuildInfo(StrictModel)` tanımlandı (`version`, `commit`, `built_at`, `source: Literal["exe", "kaynak"]`).
- **Sürüm Yardımcısı (`src/codementor/buildinfo.py`):**
  - `build_info()` fonksiyonu yazıldı: Exe modunda `data/build_info.json` dosyasını okur; kaynak modunda paket sürümünü alır. Çalışma anında asla harici `git` süreci çalıştırmaz (güvenli/hızlı). `@functools.lru_cache(maxsize=1)` ile önbelleklenir. Bozuk/eksik JSON durumunda çökmez, loglayıp güvenli fallback döner.
  - `describe(info)` ve `format_cli_version(info)` formatlama işlevleri eklendi.
- **Exe Derleme Betiği (`build_exe.py`):**
  - `build_info_file()` fonksiyonu eklendi: PyInstaller derlemesinden önce `build/build_info.json` üretir (`git rev-parse --short HEAD`, UTC ISO tarihi). PyInstaller komutuna `--add-data "build/build_info.json;data"` parametresi eklendi.
- **CLI (`src/codementor/cli/main.py`):**
  - `codementor --version` çıktısı `codementor 0.1.0 (kaynaktan)` veya `codementor 0.1.0 (<commit>, <tarih>, exe)` biçiminde güncellendi.
- **Masaüstü Arayüzü (`src/codementor/desktop/`):**
  - `widgets/sidebar.py`: Sol kenar çubuğunda durum bilgisinin hemen altında `describe(build_info())` gösterildi.
  - `views/connections_view.py`: Bağlantılar ekranındaki Konumlar kartına sürüm ve kaynak bilgisi eklendi.
- **Depolama ve Geçmiş Kurtarma:**
  - `src/codementor/storage/cache.py`: `get_row(db, analysis_id) -> AnalysisRow | None` fonksiyonu eklendi. Session kapandıktan sonra alanlara erişildiğinde SQLAlchemy `DetachedInstanceError` oluşmaması için `session.expunge(row)` uygulandı.
  - `src/codementor/desktop/app.py`: `open_history()` metodu güncellendi: Rapor şeması çözülemediğinde (`get_analysis` None) ancak veritabanı satırı mevcutsa (`get_row`), saklanan kaynak kod editöre yüklenir, sonuç paneli temizlenir, dil/motor güvenle seçilir ve kullanıcıya toast bildirimi verilir ("Bu rapor farklı bir CodeMentor sürümüyle oluşturulduğu için gösterilemiyor. Kodu editöre açtım; yeniden denetleyebilirsin.").

### 2.3. Test Kapsamı
- `tests/unit/test_buildinfo.py`: Kaynak/exe modu, bozuk JSON/tip hatası fallback'leri, formatlama fonksiyonları.
- `tests/desktop/test_build_exe.py`: Derleme öncesi JSON üretim testleri.
- `tests/unit/test_storage.py`: `get_row` ve `expunge` davranışı testleri.
- `tests/desktop/test_app.py`: Uyumsuz rapor açma, kaynak kodu olmayan uyumsuz rapor, geçersiz dil fallback testleri.

---

## 3. Faz 61 — İpucu Seviyesi Adaleti (Sayılan Denemeler)

### 3.1. Çözülen Sorunlar
1. **Hatalı Analizlerin İpucu Harcaması:** Sağlayıcı çöktüğünde (500), zaman aşımına uğradığında veya şema hatası verdiğinde dönen bozulmuş (`degraded=True`) raporlar ipucu sayacını artırıyordu. Öğrenci ilk geçerli model yanıtında dahi 3. seviye (en açık) ipucuyla karşılaşıyordu.
2. **Sözdizimi Erken Çıkışları:** Kod derlenmediğinde (`early_exit=True`) içerik ve kavram ipucu merdiveninin ilerlemesi haksız seviye tüketimine yol açıyordu.
3. **Model Karşılaştırma / Tekrar Denetleme:** Masaüstünde aynı kod ve aynı görev üzerinde model değiştirilip "Denetle" basıldığında ipucu seviyesi gereksiz yere artıyordu.

### 3.2. Mimari Karar: ADR-0026
`docs/adr/0026-ipucu-merdiveni-sayilan-denemeler.md` oluşturuldu ve üç temel kural belirlendi:
- **K1 (Bozulmuş rapor sayılmaz):** `degraded=True` ise ayrılan sayaç `sessions.release_attempt()` ile iade edilir.
- **K2 (Sözdizimi erken çıkışı sayılmaz):** `early_exit=True` ise ayrılan sayaç `sessions.release_attempt()` ile iade edilir.
- **K3 (Aynı kod merdiveni ilerletmez):** Aynı kod + soru ile "Denetle"ye basıldığında `options.advance_hint = False` atanır. Merdiven yalnızca açıkça "Bir ipucu daha" (`actions.next_hint`) tıklandığında `advance_hint = True` ile ilerletilir.

### 3.3. Yapılan Geliştirmeler
- **İstek Modeli (`src/codementor/models/request.py`):**
  - `AnalysisOptions` modeline `advance_hint: bool | None` alanı eklendi (`extra="forbid"` korunarak).
- **Boru Hattı Orkestratörü (`src/codementor/pipeline/orchestrator.py`):**
  - `_traced()`: `options.advance_hint is False` ise yeni sayaç ayrılmaz (`sessions.next_attempt - 1` ile mevcut sayaç kullanılır, `run.advance = False`). Yalnızca `run.advance` ise iptal/hata durumunda `_release()` çağrılır.
  - `_run_attempt()`: Rapor DB'ye yazıldıktan sonra sayılan bir analiz olup olmadığı denetlenir (`counts = not report.meta.early_exit and not report.meta.degraded`). Sayılan analiz `sessions.record_attempt()`, sayılmayan analiz `sessions.release_attempt()` çağırır.
- **Masaüstü Arayüzü (`src/codementor/desktop/app.py`):**
  - `_last_question_id: str | None` ve `_last_counted: bool | None` durum takibi eklendi.
  - `AnalyzeActions.next_hint`: `self.analyze(advance=True)` eylemine bağlandı.
  - `analyze()`: Kod ve soru değişmediyse ve önceki analiz sayıldıysa `options.advance_hint = False` geçirildi.
  - `start_question()` ve `restart()`: `_last_counted = None` ile sıfırlandı.
- **Şema ve Web UI Senkronizasyonu:**
  - `schemas/request.schema.json` güncellendi (`codementor schema export`).
  - `web/src/types/request.ts` güncellendi (`npm --prefix web run gen:types`).

### 3.4. Test Kapsamı
- `tests/integration/test_pipeline_sessions.py`: K1 sağlayıcı hatası (500), zaman aşımı, şema hatası; K2 Tier 0 sözdizimi erken çıkışı; K3 `advance_hint=False` ve iptal koruması testleri (13 test).
- `tests/api/test_routes.py`: `options.advance_hint` kabulü (200) ve bilinmeyen alan reddi (422) testi.
- `tests/desktop/test_app.py`: `test_advance_hint_desktop_decisions` (5 durum geçişi) ve `test_full_mentoring_flow`.

---

## 4. Faz 62 — Geçmişi ve Saklanan Kodu Silme (Gizlilik)

### 4.1. Çözülen Sorunlar
Öğrencinin analiz geçmişini, veritabanı kayıtlarını ve diskte (`~/.codementor/desktop-sources/`) saklanan kaynak kodlarını silebilmesini sağlayan hiçbir uç nokta veya arayüz düğmesi bulunmuyordu.

### 4.2. Yapılan Geliştirmeler
- **Depolama Katmanı (`src/codementor/storage/`):**
  - `cache.py`:
    - `delete_analysis(db, analysis_id) -> bool`: Veritabanından belirtilen analiz kaydını siler; bulunduysa `True`, yoksa `False` döner.
    - `clear_analyses(db) -> int`: Tüm `analyses` tablosunu siler ve silinen kayıt sayısını döner.
  - `sessions.py`:
    - `clear_sessions(db) -> int`: Tüm `sessions` tablosunu temizler ve sayısını döner.
- **Kullanıcı Kaynak Kodları (`src/codementor/desktop/runtime.py`):**
  - `delete_source(analysis_id, directory=None) -> bool`: `{user_dir}/desktop-sources/{analysis_id}.txt` dosyasını siler. Path traversal saldırılarını önlemek için `analysis_id.isalnum()` kuralı zorunlu tutulur.
  - `clear_sources(directory=None) -> int`: `desktop-sources/` altındaki tüm `.txt` dosyalarını siler ve silinen dosya adedini döner.
- **REST API ve CORS:**
  - `src/codementor/api/routes.py`: `DELETE /v1/analyses/{analysis_id}` rotası eklendi.
    - Başarılı silme: `204 No Content`.
    - Bulunamadı: `404 Not Found` (Problem+JSON).
    - Biçim dışı ULID: `404 Not Found` (Faz 27 uyarınca varlık sızıntısı önlenir).
  - `src/codementor/api/app.py`: CORS `allow_methods` listesine `"DELETE"` eklendi.
- **Masaüstü Arayüzü:**
  - `src/codementor/desktop/views/history_view.py`:
    - Her satıra "Sil" butonu eklendi. Buton tıklaması, satır tıklamasından (`open_row`) izole edildi; satır açılmadan doğrudan silme tetiklenir.
    - Başlık alanına "Tümünü temizle" butonu eklendi (kayıt yoksa devre dışı kalır).
  - `src/codementor/desktop/app.py`:
    - `delete_history(analysis_id)`: DB ve diskten kaydı siler, liste ekranını yeniler; açık analiz bu ise (`_shown_analysis_id` ile eski uyumsuz raporlar dâhil) rapor ve sonuçları sıfırlar, toast verir.
    - `clear_history()`: `self.confirm` enjekte edilebilir onay diyaloğu sunar (`Tüm analiz geçmişi, saklanan kodlar ve ipucu ilerlemen silinecek. Emin misin?`). Onay verilirse analizleri (`clear_analyses`), oturumları (`clear_sessions`) ve saklanan kodları (`clear_sources`) siler; açık ekranı sıfırlar, geçmişi yeniler ve toast verir (`Geçmiş temizlendi (N analiz).`).
- **Dokümantasyon:**
  - `docs/mimari.md` §9 API tablosuna `DELETE /v1/analyses/{id}` eklendi.

### 4.3. Test Kapsamı
- `tests/unit/test_storage.py`: `delete_analysis` (başarılı/bulunamadı), `clear_analyses`, `clear_sessions`.
- `tests/desktop/test_runtime.py`: `delete_source` (başarılı, bulunamadı, traversal koruması), `clear_sources`.
- `tests/api/test_routes.py`: `DELETE /v1/analyses/{id}` (204, 404, geçersiz ULID 404).
- `tests/api/test_errors_and_app.py`: CORS preflight `DELETE` metodu izni.
- `tests/desktop/test_app.py`: `delete_history` ve `clear_history` (onaylı/onaysız, açık analiz ve oturum sıfırlama, uyumsuz eski rapor silme), `HistoryView` buton geri çağrıları. Toplam 3079 test yeşil.

---

## 5. Doğrulama ve Kalite Metrikleri

Tüm aşamalarda projenin 4 temel denetim adımı eksiksiz olarak çalıştırılmış ve yeşil sonuç alınmıştır:

1. **Ruff Linter:**
   ```bash
   uv run ruff check .
   # Çıktı: All checks passed!
   ```
2. **Ruff Biçimlendirme:**
   ```bash
   uv run ruff format --check .
   # Çıktı: 421 files already formatted
   ```
3. **Mypy Tip Denetimi:**
   ```bash
   uv run mypy src/
   # Çıktı: Success: no issues found in 198 source files
   ```
4. **Pytest Test Paketi (Ağsız):**
   ```bash
   uv run pytest -m "not live"
   # Çıktı: 3079 passed, 14 skipped, 6 deselected in 114.90s
   ```
5. **Web UI Tipleri ve Derleme:**
   ```bash
   npm --prefix web run typecheck && npm --prefix web run build
   # Çıktı: ✓ built in 398ms
   ```

---

## 6. Bağımsız Kod Denetimi ve Kapanan Bulgular (`faz-denetim`)

Kullanıcının talebi ve doğrulamasıyla `faz-denetim` becerisi protokolü işletilmiş, şartnameyle karşılaştırmalı kod taraması yapılmıştır:

1. **`clear_sessions` Entegrasyonu:** Masaüstünde tüm geçmiş temizlendiğinde veritabanındaki oturumların da sıfırlanması sağlandı.
2. **`_shown_analysis_id` Takibi:** Ekranda açık olan analiz (özellikle eski uyumsuz şemalı raporlar dâhil) silindiğinde ekranın anında temizlenmesi sağlandı.
3. **`self.confirm` Enjeksiyonu:** Testlerin gerçek onay fonksiyonunu taklit edebilmesi için onay mekanizması enjekte edilebilir hâle getirildi.
4. **Metin ve Bildirim Doğrulaması:** Onay sorusu ve silinen kayıt sayısını belirten toast mesajı (`Geçmiş temizlendi (N analiz).`) şartnameye uyarlandı.

---

## 7. Değiştirilen ve Eklenen Dosyaların Özeti

```
docs/
  ├── adr/0026-ipucu-merdiveni-sayilan-denemeler.md  (YENİ)
  ├── DEVIR_FAZ60_62.md                             (Referans)
  ├── GUNCELLEMELER.md                              (Güncellendi: Faz 60-62 işaretlendi)
  ├── mimari.md                                     (Güncellendi: DELETE /v1/analyses/{id})
  └── YAPILANLAR_60_62_ANTIGRAVITY.md               (YENİ - Bu rapor)
src/codementor/
  ├── api/app.py                                    (CORS DELETE)
  ├── api/routes.py                                 (DELETE /v1/analyses/{id})
  ├── buildinfo.py                                  (YENİ)
  ├── cli/main.py                                   (--version formatı)
  ├── desktop/app.py                                (Sürüm uyumu, advance_hint, silme/temizleme)
  ├── desktop/runtime.py                            (delete_source, clear_sources)
  ├── desktop/views/connections_view.py             (Sürüm gösterimi)
  ├── desktop/views/history_view.py                 (Sil ve Tümünü temizle butonları)
  ├── desktop/widgets/sidebar.py                    (Sürüm gösterimi)
  ├── models/build.py                               (YENİ)
  ├── models/request.py                             (advance_hint seçeneği)
  ├── pipeline/orchestrator.py                      (Sayılan deneme rezervasyonu/iadesi)
  ├── storage/cache.py                              (get_row, delete_analysis, clear_analyses)
  └── storage/sessions.py                           (clear_sessions, kural docstring'leri)
tests/
  ├── api/test_errors_and_app.py                    (CORS DELETE testi)
  ├── api/test_routes.py                            (advance_hint, DELETE testi)
  ├── desktop/test_app.py                           (Sürüm uyumu, advance_hint, silme testleri)
  ├── desktop/test_build_exe.py                     (YENİ)
  ├── desktop/test_runtime.py                       (delete_source, clear_sources testleri)
  ├── integration/test_pipeline_sessions.py         (K1, K2, K3 entegrasyon testleri)
  ├── unit/test_buildinfo.py                        (YENİ)
  └── unit/test_storage.py                          (get_row, delete_analysis, clear_analyses, clear_sessions)
schemas/request.schema.json                         (advance_hint şeması)
web/src/types/request.ts                            (advance_hint TypeScript tipi)
build_exe.py                                        (build_info.json paketi)
PROGRESS.md                                         (Faz 60, 61, 62 durum ve notları)
```
