"""`codementor providers check` (mimari §10): Ollama gerçekten sorgulanır (burada respx ile)."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import httpx
import pytest
import respx
from typer.testing import CliRunner, Result

from codementor.cli.main import app
from codementor.config import CONFIG_FILE_ENV

TAGS = "http://ollama.test/api/tags"
SECRET = "sk-test-cli-SECRET-0123456789"


@pytest.fixture
def config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "codementor.toml"
    path.write_text(
        "[providers]\n"
        'default = "ollama"\n'
        'fallback = ["anthropic"]\n'
        "[providers.ollama]\n"
        'base_url = "http://ollama.test"\n'
        'model = "qwen2.5-coder:7b"\n'
        "[providers.anthropic]\n"
        'model = "claude-test"\n',
        encoding="utf-8",
    )
    monkeypatch.setenv(CONFIG_FILE_ENV, str(path))
    monkeypatch.setenv("ANTHROPIC_API_KEY", SECRET)
    return path


@pytest.fixture
def router() -> Iterator[respx.MockRouter]:
    with respx.mock(assert_all_mocked=True, assert_all_called=False) as mock:
        yield mock


def _invoke(*args: str) -> Result:
    return CliRunner().invoke(app, ["providers", "check", *args], env={"COLUMNS": "200"})


@pytest.mark.usefixtures("config")
def test_ollama_ready_when_model_pulled(router: respx.MockRouter) -> None:
    route = router.get(TAGS).mock(
        return_value=httpx.Response(200, json={"models": [{"name": "qwen2.5-coder:7b"}]})
    )
    result = _invoke()
    assert result.exit_code == 0, result.output
    assert route.call_count == 1  # gerçekten sorgulandı
    assert "hazır" in result.output
    assert "num_ctx=16384" in result.output
    assert "ANTHROPIC_API_KEY tanımlı" in result.output
    assert SECRET not in result.output


@pytest.mark.usefixtures("config")
def test_ollama_model_missing(router: respx.MockRouter) -> None:
    router.get(TAGS).mock(return_value=httpx.Response(200, json={"models": [{"name": "x"}]}))
    result = _invoke()
    assert result.exit_code == 1
    assert "ollama pull qwen2.5-coder:7b" in result.output


@pytest.mark.usefixtures("config")
def test_ollama_unreachable(router: respx.MockRouter) -> None:
    router.get(TAGS).mock(side_effect=httpx.ConnectError("reddedildi"))
    result = _invoke()
    assert result.exit_code == 1
    assert "erişilemiyor" in result.output


@pytest.mark.usefixtures("config")
def test_cloud_key_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY")
    result = _invoke("--provider", "anthropic")
    assert result.exit_code == 1
    assert "ANTHROPIC_API_KEY ortam değişkeni tanımlı değil" in result.output


@pytest.mark.usefixtures("config")
def test_cloud_ready_without_network(router: respx.MockRouter) -> None:
    # assert_all_mocked: herhangi bir istek taklit edilmediği için hata verirdi
    result = _invoke("--provider", "anthropic")
    assert not router.calls
    assert result.exit_code == 0, result.output
    assert SECRET not in result.output


@pytest.mark.usefixtures("config")
def test_unknown_provider() -> None:
    result = _invoke("--provider", "gemini")
    assert result.exit_code == 2
    assert "bilinmeyen sağlayıcı" in result.output


def test_broken_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "bozuk.toml"
    path.write_text("[providers\n", encoding="utf-8")
    monkeypatch.setenv(CONFIG_FILE_ENV, str(path))
    assert _invoke().exit_code == 3


def test_origin_hides_credentials() -> None:
    from codementor.cli.providers import _origin

    assert (
        _origin("http://kullanici:parola@ollama.test:11434/yol?x=1") == "http://ollama.test:11434"
    )
    assert _origin(None) == "(adres yok)"


@pytest.mark.usefixtures("config")
def test_health_check_uses_short_timeout(router: respx.MockRouter) -> None:
    from codementor.cli import providers as cli

    seen: list[float] = []
    original = cli.HttpTransport

    def spy(name: str, timeout_s: float, *args: object, **kwargs: object) -> object:
        seen.append(timeout_s)
        return original(name, timeout_s, *args, **kwargs)  # type: ignore[arg-type]

    router.get(TAGS).mock(side_effect=httpx.ConnectError("reddedildi"))
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(cli, "HttpTransport", spy)
        _invoke("--provider", "ollama")
    assert seen == [cli.HEALTH_TIMEOUT_S]
