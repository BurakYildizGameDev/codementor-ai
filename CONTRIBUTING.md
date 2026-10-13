# Katkı rehberi

Katkılar memnuniyetle karşılanır. Proje Türkçe öğrenciler için yazıldı: kullanıcıya dönük
mesajlar Türkçedir; tanımlayıcılar İngilizce, yorumlar Türkçe ya da İngilizce olabilir.
*English contributions are welcome too; user-facing strings stay Turkish.*

## Kurulum

```bash
git clone https://github.com/BurakYildizGameDev/codementor-ai.git
cd codementor-ai
uv sync                 # Python 3.12 + bağımlılıklar
cd web && npm ci        # web arayüzü (isteğe bağlı)
```

## Denetimler

Bir PR açmadan önce hepsi yeşil olmalı (CI de aynısını koşar):

```bash
uv run ruff check . && uv run ruff format --check .
uv run mypy src/                  # strict
uv run pytest -m "not live"       # ağa çıkmaz
make web-test                     # web değiştiyse
```

`make check` ilk üçünü birlikte koşar. Derleyici testleri: `uv run pytest -m compiler`
(gcc/clang/dotnet yoksa atlanır).

## Kurallar

- **Mimari:** `docs/mimari.md`. Ondan sapan bir değişiklik bir ADR ile gelir (`docs/adr/`).
- **Her yeni davranış testle gelir.** LLM çağıran kod testlerde `FakeProvider` kullanır; gerçek
  API testleri `@pytest.mark.live` ile işaretlenir ve CI'da koşmaz.
- **Kullanıcı kodu güvenilmeyen veridir** (mimari §12): çalıştırılmaz, prompt'a veri olarak girer.
- **Model adları, anahtarlar, URL'ler koda gömülmez;** `codementor.toml`'dan gelir.
- Pydantic modelleri `src/codementor/models/` altındadır; tüm fonksiyonlarda tip ipucu vardır.
- 400 satırı geçen dosya bölünmelidir.
- JSON şemaları modellerden üretilir (`make schema`); web tipleri şemadan (`make web-types`),
  elle yazılmaz.
- Statik kural eklerken pozitif/negatif fixture ve 40 KB kötü niyetli girdiyle süre testi ekleyin.
- Soru bankasına soru eklerken `docs/SORU_YAZIM_REHBERI.md`'ye uyun ve
  `uv run codementor questions validate` çalıştırın.

## Commit ve PR

- Conventional commits: `feat(...)`, `fix(...)`, `docs(...)`, `test(...)`, `refactor(...)`.
- PR açıklamasında: ne değişti, neden, nasıl test edildi; eval'i etkiliyorsa ölçüm sonucu.
- Güvenlik açıklarını issue olarak değil, [SECURITY.md](SECURITY.md)'deki yolla bildirin.
