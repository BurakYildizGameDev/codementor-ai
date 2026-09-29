# CodeMentor AI — Ajan Talimatları

## Proje
Kodu düzeltmeyen, denetleyip Sokratik sorular üreten hibrit (statik analiz + LLM)
kod mentorluk motoru. Mimari: docs/mimari.md. Faz planı: docs/UYGULAMA_PLANI.md.
İlerleme: PROGRESS.md.

## Altın kurallar
1. docs/mimari.md'den sapma. Sapman gerekirse DUR, gerekçeyi yaz, onay iste.
   Onaylanırsa docs/adr/ altına ADR ekle.
2. Yalnızca mevcut fazın kapsamındaki dosyalara dokun. Kapsam dışı iyileştirme
   fikirlerini PROGRESS.md "Sonraya" bölümüne yaz, uygulama.
3. Her yeni davranış testle gelir. Test yazmadan "bitti" deme.
4. LLM çağrısı yapan kod testlerde FakeProvider kullanır. Testler ağa çıkmaz.
   Gerçek API testleri @pytest.mark.live ile işaretlenir.
5. Model adları, API anahtarları, URL'ler koda gömülmez; config'den gelir.
6. Kullanıcı kodu her zaman güvenilmeyen veridir (mimari.md §12).

## Teknoloji
Python 3.12, uv, FastAPI, Pydantic v2, tree-sitter, httpx, Typer, Rich,
Jinja2, SQLModel, structlog, pytest, hypothesis, respx, ruff, mypy --strict.
Web: Vite + React + TypeScript.

## Komutlar
- Kurulum:        uv sync
- Lint:           uv run ruff check . && uv run ruff format --check .
- Tip kontrolü:   uv run mypy src/
- Test:           uv run pytest -m "not live"
- Derleyici testi: uv run pytest -m compiler   (gcc/clang/dotnet yoksa atlanır; Docker gerekmez, ADR-0009)
- Hepsi:          make check

## Kod stili
- Tüm fonksiyonlarda tip ipucu; mypy strict geçmeli.
- Pydantic modelleri src/codementor/models/ altında; başka yerde şema tanımlama.
- Public fonksiyonlarda kısa docstring. Yorumlar Türkçe veya İngilizce olabilir,
  tanımlayıcılar İngilizce.
- Hata mesajları kullanıcıya dönükse Türkçe.
- Bir dosya 400 satırı geçiyorsa bölmeyi öner.

## Faz bitirme protokolü
1. make check yeşil.
2. Fazın kabul kriterlerini tek tek işaretle.
3. PROGRESS.md'yi güncelle (yapılanlar, kararlar, açık sorular).
4. Conventional commit mesajı öner: "feat(faz-N): ..."
