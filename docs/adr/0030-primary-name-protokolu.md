# ADR-0030: `LLMProvider.primary_name` protokol üyesi

**Tarih:** 2026-10-16 · **Durum:** Kabul edildi · **Etkilenen bölümler:** mimari §5.5.1, §5.5.2, §20

## Bağlam

Önbellek kaydı yalnızca **zincirin başındaki** sağlayıcı yanıt verdiğinde geçerlidir: geri dönüşe
düşen bir yanıt (ör. claude_cli çöktü, gemini yanıtladı) önbelleğe yazılırsa sonraki koşu, birincil
sağlayıcı düzeldiğinde eski (farklı model) sonucu servis ederdi. `orchestrator` bunu bilmek için
sağlayıcının **somut** tipine bakıyordu:

```python
primary = getattr(provider, "chain", [provider])[0].name
```

Bu, protokolün bilmediği bir alanı (`chain` yalnız `FallbackProvider`'da var) yoklamak demekti:
sağlayıcı arayüzünü uygulayan yeni bir adaptör eklendiğinde (ya da `chain` alanının adı değiştiğinde)
`orchestrator` sessizce yanlış ada düşebilir, tip denetimi (mypy strict) bunu yakalayamaz. Eksik olan,
zincirin ilk halkası bilgisini sağlayıcı arayüzünün sözleşmesine yazmaktı.

## Karar

1. `LLMProvider` protokolüne **`primary_name: str`** salt-okunur özelliği eklendi: zincirin başında
   gerçekten çağrılan sağlayıcının adı. Tek sağlayıcıda `name` ile aynıdır.
2. Tek halkalı sağlayıcılar için `providers/base.py::NamedProvider` tabanı eklendi
   (`primary_name` → `name`). `fake`, `ollama`, `openai_compat` (gemini), `anthropic`, `claude_cli`,
   `agy`, `codex_cli` ve eval'in `StaticOnlyProvider`'ı bu tabandan türer.
3. `FallbackProvider` (tek halkalı bir sağlayıcıyı sarmalarken de) ilk halkanın `primary_name`'ini
   döndürür; boş zincir `ProviderConfigError` ile reddedildiği için tanımsız durum yok.
4. `orchestrator` artık `getattr(..., "chain", ...)` yoklaması yapmaz; yalnız `provider.primary_name`
   okur. Önbellek ölçütü değişmedi (yalnız birincil sağlayıcı yanıtı önbelleğe girer).

## Sonuçlar

- (+) Sağlayıcı tipine özel yoklama kalktı; yeni bir adaptör `NamedProvider`'dan türeyerek doğru
  davranışı bedava alır. Protokol üyesi olduğu için mypy strict eksik uygulamayı yakalar.
- (+) Test: `tests/providers/test_contract.py` her adaptörde `primary_name == name` eşitliğini,
  `tests/providers/test_factory.py` zincirde ilk halkayı, `tests/integration/test_pipeline_partial.py`
  önbellek/geri dönüş davranışını doğrular.
- (−) Protokol genişledi: protokolü dışarıdan uygulayan üçüncü taraf bir sağlayıcı (yok; §5.5.2
  sağlayıcıları depo içindedir) `primary_name` vermek zorunda.
- Not: `primary_name` yalnız önbellek ölçütü ve tanı içindir; rapora ya da `ProviderResult`'a
  yazılmaz (ADR-0004: tek rapor şeması).
