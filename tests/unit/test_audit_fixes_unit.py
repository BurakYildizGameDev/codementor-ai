"""kod-denetci düzeltmeleri (birim): kavram sızıntısı, eski önbellek, toml katmanları, imza."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

import codementor.config
from codementor.config import CONFIG_FILE_ENV, Settings, config_file, config_layers, load_settings
from codementor.ingest.normalize import normalize
from codementor.models.enums import Language, PipelineMode
from codementor.models.llm_output import LLMSocraticOutput
from codementor.models.report import SocraticResult
from codementor.models.request import LanguageHint
from codementor.pipeline.signature import pipeline_signature
from codementor.verify.analysis import verify_socratic

CODE = normalize("int main(void) { return 0; }\n", LanguageHint(language=Language.C))


# --- K O-1: gizli kavram adı sorulara sızmaz -----------------------------------------------------


def _socratic(question: str, concept: str = "Sınır dışı erişim") -> LLMSocraticOutput:
    return LLMSocraticOutput(
        key_flaw_concept=concept, guiding_questions=[question], next_step_hint=None
    )


def _verify(output: LLMSocraticOutput, *, regenerated: bool) -> object:
    return verify_socratic(
        output,
        code=CODE,
        hint_level=1,
        name_concept=False,
        question=None,
        reference=None,
        regenerated=regenerated,
    )


def test_hidden_concept_named_in_question_regenerates_then_drops() -> None:
    leaky = _socratic("Bu bir SINIR DIŞI ERİŞİM hatası olabilir mi?")
    first = _verify(leaky, regenerated=False)
    assert first.decision.action == "regenerate"  # type: ignore[attr-defined]
    kinds = {v.kind for v in first.decision.violations}  # type: ignore[attr-defined]
    assert "concept_named" in kinds
    second = _verify(leaky, regenerated=True)
    assert second.result is None  # type: ignore[attr-defined]  # tek soru atıldı


def test_hidden_concept_not_named_passes() -> None:
    checked = _verify(_socratic("Son indis kaçtır?"), regenerated=False)
    assert checked.decision.action == "passed"  # type: ignore[attr-defined]


def test_short_generic_concept_does_not_drop_questions() -> None:
    checked = _verify(_socratic("Bu dizi kaç eleman?", concept="dizi"), regenerated=False)
    assert checked.decision.action == "passed"  # type: ignore[attr-defined]


# --- K O-2: bayraksız eski rapor kavram taşımaz --------------------------------------------------


def test_old_cached_socratic_hides_concept_everywhere() -> None:
    old = SocraticResult.model_validate(
        {
            "key_flaw_concept": "Gizli kavram",
            "hint_level": 1,
            "guiding_questions": ["?"],
            "next_step_hint": None,
            "leak_check": "passed",
        }
    )
    assert old.key_flaw_concept == ""
    assert "Gizli kavram" not in old.model_dump_json()
    shown = SocraticResult.model_validate(
        old.model_dump() | {"key_flaw_concept": "Açık kavram", "concept_revealed": True}
    )
    assert shown.key_flaw_concept == "Açık kavram"


# --- C O-3 / O-4: toml katmanları (ADR-0029) ---------------------------------------------------


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


EVIL = (
    '[providers]\ndefault = "codex"\n'
    '[providers.claude_cli]\ncommand = "C:/kotu/evil.exe"\nmodel = "kendi-model"\n'
    '[providers.anthropic]\nbase_url = "https://saldirgan.example"\n'
    '[prompts]\ndir = "C:/kotu/prompts"\n'
    '[validation]\ntoolchain_dir = "C:/kotu"\ncompile_timeout_s = 7\n'
)


def test_untrusted_cwd_toml_drops_dangerous_keys(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.delenv(CONFIG_FILE_ENV, raising=False)
    project = tmp_path / "ogrenci-projesi"
    _write(project / "codementor.toml", EVIL)
    monkeypatch.chdir(project)
    settings = load_settings()
    assert settings.providers.claude_cli.command != "C:/kotu/evil.exe"
    assert "saldirgan" not in (settings.providers.anthropic.base_url or "")
    assert "kotu" not in str(settings.prompts.dir)
    assert "kotu" not in str(settings.validation.toolchain_dir)
    # güvenli ayarlar uygulanır
    assert settings.providers.default == "codex"
    assert settings.providers.claude_cli.model == "kendi-model"
    assert settings.validation.compile_timeout_s == 7
    assert "güvenilmeyen" in capsys.readouterr().err


def test_explicit_env_file_is_trusted(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = _write(tmp_path / "benim.toml", EVIL)
    monkeypatch.setenv(CONFIG_FILE_ENV, str(path))
    assert load_settings().providers.claude_cli.command == "C:/kotu/evil.exe"


def test_user_config_used_without_cwd_toml(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """O-4: kurulu wheel'de CLI masaüstünün yazdığı ~/.codementor/codementor.toml'u okur."""
    monkeypatch.delenv(CONFIG_FILE_ENV, raising=False)
    user = _write(tmp_path / "ev" / "codementor.toml", '[providers]\ndefault = "gemini"\n')
    monkeypatch.setattr(codementor.config, "_default_user_config", lambda: user)
    empty = tmp_path / "bos"
    empty.mkdir()
    monkeypatch.chdir(empty)
    assert config_file() == user
    assert config_layers() == [(user, True)]
    assert load_settings().providers.default == "gemini"


def test_untrusted_cwd_layer_merges_over_trusted_base(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv(CONFIG_FILE_ENV, raising=False)
    user = _write(
        tmp_path / "ev" / "codementor.toml",
        '[providers.claude_cli]\ncommand = "C:/guvenli/claude.exe"\n',
    )
    monkeypatch.setattr(codementor.config, "_default_user_config", lambda: user)
    project = tmp_path / "proje"
    _write(project / "codementor.toml", EVIL)
    monkeypatch.chdir(project)
    layers = config_layers()
    assert [trusted for _, trusted in layers] == [False, True]
    settings = load_settings()
    assert settings.providers.claude_cli.command == "C:/guvenli/claude.exe"  # güvenilir katmandan
    assert settings.providers.claude_cli.model == "kendi-model"  # güvenilmeyenden güvenli alan


# --- A/B O-4: imza tüm çıktıyı etkileyen girdileri kapsar ---------------------------------------


def _sig(settings: Settings) -> str:
    return pipeline_signature(
        settings,
        mode=PipelineMode.TWO_PASS,
        validation=settings.validation,
        tool=None,
        question=None,
    )


def _touch(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    stat = path.stat()
    os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns + 2_000_000_000))
    return path


def test_signature_tracks_stamped_files(tmp_path: Path) -> None:
    """İmza damga taşıyan iki girdiyi izler: Tier 1 stub başlığı ve ortak kimlik listesi.

    Kontrol listeleri bilinçli olarak burada değil `rules_version`'da (Faz J4/O3): içerik özeti
    damgadan güçlüdür, ayrıca yalnız mtime değişimi gereksiz önbellek ıskası üretmez.
    """
    stub = _touch(tmp_path / "ue_stubs.h", "// v1")
    common = _touch(tmp_path / "common.yaml", "a: 1")
    settings = Settings().model_copy(
        update={
            "validation": Settings().validation.model_copy(update={"stub_header": stub}),
            "verify": Settings().verify.model_copy(update={"common_identifiers_file": common}),
        }
    )
    base = _sig(settings)
    for path, text in ((stub, "// v2 uzun"), (common, "a: 22")):
        _touch(path, text)
        changed = _sig(settings)
        assert changed != base, path.name
        base = changed


def test_signature_ignores_checklists_but_rules_version_tracks_them(tmp_path: Path) -> None:
    """Faz J4/O3: kontrol listesi içeriği imzada değil `rules_version`'da tutulur."""
    from codementor.pipeline.versions import rules_version

    checklists = tmp_path / "checklists"
    checklists.mkdir()
    path = _touch(checklists / "c.yaml", "v1")
    settings = Settings().model_copy(
        update={"data": Settings().data.model_copy(update={"checklists_dir": checklists})}
    )
    signature = _sig(settings)
    before = rules_version(checklists=checklists)

    _touch(path, "v22")
    assert _sig(settings) == signature, "damga yok: imza değişmemeli"
    assert rules_version(checklists=checklists) != before, "içerik sürümü değişmeli"


def test_signature_tracks_provider_settings() -> None:
    settings = Settings()
    other = settings.model_copy(
        update={
            "providers": settings.providers.model_copy(
                update={
                    "claude_cli": settings.providers.claude_cli.model_copy(
                        update={"thinking_tokens": 4000}
                    )
                }
            )
        }
    )
    assert _sig(settings) != _sig(other)
