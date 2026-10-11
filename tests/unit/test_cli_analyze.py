"""`codementor analyze` (mimari §10): çıkış kodları ve biçimler; ağsız (FakeProvider)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft4Validator
from typer.testing import CliRunner

import codementor.cli.analyze as analyze_module
from codementor.cli.main import app
from codementor.pipeline.orchestrator import Orchestrator
from codementor.providers.base import RetryPolicy
from codementor.providers.fake import FakeProvider, FakeReply
from tests.integration.conftest import BROKEN_C, LINKED_LIST, analysis_reply, socratic_reply

REPO = Path(__file__).resolve().parents[2]
CLEAN_C = "int add(int a, int b) {\n    return a + b;\n}\n"
SARIF_SCHEMA = json.loads(
    (REPO / "tests" / "fixtures" / "sarif-schema-2.1.0.json").read_text(encoding="utf-8")
)


@pytest.fixture
def run(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Any:
    """CLI'yı FakeProvider ile çalıştıran yardımcı; `replies` sağlayıcı senaryosu."""
    config = tmp_path / "codementor.toml"
    config.write_text(
        f"""
[validation]
tier1_enabled = false
[providers]
default = "fake"
fallback = []
[storage]
db_path = "{(tmp_path / "cm.db").as_posix()}"
[data]
questions_dir = "{(REPO / "data" / "questions").as_posix()}"
checklists_dir = "{(REPO / "data" / "checklists").as_posix()}"
call_costs_file = "{(REPO / "data" / "call_costs.yaml").as_posix()}"
mentor_templates_file = "{(REPO / "data" / "mentor_templates.yaml").as_posix()}"
[prompts]
dir = "{(REPO / "prompts" / "v1").as_posix()}"
[verify]
common_identifiers_file = "{(REPO / "data" / "leak_common_identifiers.yaml").as_posix()}"
""",
        encoding="utf-8",
    )
    monkeypatch.setenv("CODEMENTOR_CONFIG_FILE", str(config))
    monkeypatch.delenv("CODEMENTOR_DB_PATH", raising=False)
    calls: list[FakeProvider] = []

    def invoke(
        code: str,
        *args: str,
        replies: list[dict[str, Any]] | None = None,
        filename: str = "kod.c",
        language: str | None = "c",
    ) -> Any:
        provider = FakeProvider(
            script=[FakeReply(data=r) for r in replies or []], retry=RetryPolicy(max_retries=0)
        )
        calls.append(provider)

        class FakeOrchestrator(Orchestrator):
            def __init__(self, settings: Any, db: Any) -> None:
                super().__init__(settings, db, provider_factory=lambda _n: provider)

        monkeypatch.setattr(analyze_module, "Orchestrator", FakeOrchestrator)
        source = tmp_path / filename
        source.write_text(code, encoding="utf-8")
        hint = ["--language", language] if language else []
        return CliRunner().invoke(app, ["analyze", str(source), *hint, *args])

    invoke.calls = calls  # type: ignore[attr-defined]
    return invoke


def test_exit_2_on_compile_failure_without_llm(run: Any) -> None:
    result = run(BROKEN_C)
    assert result.exit_code == 2
    assert run.calls[-1].calls == []


def test_exit_1_on_high_severity_finding(run: Any) -> None:
    result = run(
        LINKED_LIST,
        "--question",
        "c-medium-linked-list",
        "--format",
        "json",
        replies=[analysis_reply(), socratic_reply()],
    )
    assert result.exit_code == 1, result.output
    report = json.loads(result.stdout)
    assert report["meta"]["provider"] == "fake"
    assert any(f["severity"] == "high" for f in report["findings"])


def test_exit_0_clean_code(run: Any) -> None:
    reply = {
        "complexity": {
            "reasoning_steps": ["Tek işlem."],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "optimal_time_target": "O(1)",
            "agreement": "no_hint",
        },
        "additional_findings": [],
    }
    result = run(CLEAN_C, "--format", "md", replies=[reply, socratic_reply("Toplam taşabilir mi?")])
    assert result.exit_code == 0, result.output
    assert "# CodeMentor raporu" in result.stdout


def test_exit_3_on_system_error(run: Any) -> None:
    result = run(CLEAN_C, "--question", "boyle-bir-soru-yok")
    assert result.exit_code == 3
    assert "boyle-bir-soru-yok" in result.output


def test_exit_3_missing_file(run: Any, tmp_path: Path) -> None:
    result = CliRunner().invoke(app, ["analyze", str(tmp_path / "yok.c")])
    assert result.exit_code == 3
    assert "Dosya okunamadı" in result.output


def test_sarif_output_valid(run: Any, tmp_path: Path) -> None:
    out = tmp_path / "out.sarif"
    result = run(BROKEN_C, "--format", "sarif", "--out", str(out))
    assert result.exit_code == 2
    log = json.loads(out.read_text(encoding="utf-8"))
    Draft4Validator(SARIF_SCHEMA).validate(log)
    assert log["runs"][0]["results"][0]["ruleId"] == "CM-COMPILE"


def test_pretty_output_to_file(run: Any, tmp_path: Path) -> None:
    out = tmp_path / "rapor.txt"
    result = run(BROKEN_C, "--out", str(out))
    assert result.exit_code == 2
    text = out.read_text(encoding="utf-8")
    assert "CodeMentor" in text
    assert "Mentor soruları" in text


def test_no_cache_flag_calls_provider_again(run: Any) -> None:
    args = ("--question", "c-medium-linked-list", "--format", "json")
    replies = [analysis_reply(), socratic_reply()]
    run(LINKED_LIST, *args, replies=replies)
    second = run(LINKED_LIST, *args, replies=replies)
    assert json.loads(second.stdout)["meta"]["cache_hit"] is True
    third = run(LINKED_LIST, *args, "--no-cache", replies=replies)
    assert json.loads(third.stdout)["meta"]["cache_hit"] is False
    assert len(run.calls[-1].calls) == 2


@pytest.mark.parametrize(("flag", "expected"), [("--tier1", True), ("--no-tier1", False)])
def test_cli_tier1_flag_controls_local_config(
    run: Any, monkeypatch: pytest.MonkeyPatch, flag: str, expected: bool
) -> None:
    """Faz 47: istek Tier 1'i açamaz, ama yerel CLI kullanıcısı kendi yapılandırmasını açabilir."""
    seen: list[bool] = []
    validation = Orchestrator._validation

    def capture(self: Orchestrator, request: Any) -> Any:
        seen.append(self.settings.validation.tier1_enabled)
        return validation(self, request)

    monkeypatch.setattr(Orchestrator, "_validation", capture)
    run(CLEAN_C, flag, "--format", "json")
    assert seen == [expected]


def test_cli_cp1254_file_fails_with_turkish_message(tmp_path: Path) -> None:
    """Kabul (Faz 50): UTF-8 olmayan dosya sessizce U+FFFD'ye dönüşmez; Türkçe hata, çıkış 3."""
    source = tmp_path / "eski.c"
    source.write_bytes("// açıklama: öğrenci\nint main(void) { return 0; }\n".encode("cp1254"))
    result = CliRunner().invoke(app, ["analyze", str(source), "--language", "c"])
    assert result.exit_code == 3
    assert "UTF-8 değil" in result.output
    assert "\ufffd" not in result.output


def test_language_from_extension_when_flag_missing(run: Any) -> None:
    """İçerikten belirlenemeyen kısa kod `.c` uzantısıyla C sayılır (çıkış 3 değil)."""
    result = run(BROKEN_C, "--format", "json", language=None)
    assert result.exit_code == 2, result.output
    assert json.loads(result.stdout)["language"] == "c"


def test_explicit_language_overrides_extension(run: Any) -> None:
    result = run(BROKEN_C, "--format", "json", filename="kod.py", language="c")
    assert result.exit_code == 2, result.output
    assert json.loads(result.stdout)["language"] == "c"


def test_header_extension_left_to_content_detection(run: Any) -> None:
    """`.h` C/C++ arasında belirsiz: C'ye zorlanmaz, içerik C++ ise cpp."""
    code = "#include <vector>\nint main() {\n    std::vector<int> v\n    return 0;\n}\n"
    result = run(code, "--format", "json", filename="kod.h", language=None)
    assert result.exit_code == 2, result.output
    assert json.loads(result.stdout)["language"] == "cpp"


def test_unknown_extension_ambiguous_code_lists_all_languages(run: Any) -> None:
    result = run(BROKEN_C, filename="kod.txt", language=None)
    assert result.exit_code == 3
    assert "belirlenemedi" in result.output
    assert "python, html, css" in " ".join(result.output.split())
