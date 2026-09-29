# İlerleme Günlüğü

## Durum
| Faz | Durum | Dal | Tarih | Araç (uygulayan / denetleyen) |
|---|---|---|---|---|
| 0 | ✅ | faz/0-iskelet | 2026-09-29 | Claude Code / — |
| 1 | 🔄 | faz/1-modeller | | |
| 2 | ⏳ | | | |

## Faz 0 — Notlar
**Yapılanlar:** pyproject (uv, ruff, mypy strict, pytest işaretleri live/sandbox/slow), config (pydantic-settings; CLI > env > TOML > varsayılan), `codementor --version`, Makefile, CI, ajan dosyaları (Bölüm 4).
**Alınan kararlar (ve neden):**
- TOML dosya yolu `CODEMENTOR_CONFIG_FILE` ile değiştirilebilir (varsayılan `./codementor.toml`); testlerin geçici dosya kullanabilmesi için.
- CLI bayrakları `load_settings(**overrides)` init argümanı olarak verilir → en yüksek öncelik.
- ruff `allowed-confusables = ["ı"]`: Türkçe docstring/yorumlar RUF001-003 uyarısı vermesin.
**Mimariden sapmalar (ADR linki):** yok
**Açık sorular:**
- Windows geliştirme makinesinde `make` yok; komutlar `uv run ...` ile doğrudan çalıştırıldı. (Git Bash için `choco install make` / `winget install GnuWin32.Make` önerilir.)
- CI henüz GitHub'da çalıştırılmadı (uzak repo yok).
**Bu fazda öğrendiğim:**

## Sonraya (kapsam dışı fikirler)
-
