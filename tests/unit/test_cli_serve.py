"""`codementor serve` CLI komutu testleri (Faz E: E11)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
import uvicorn
from typer.testing import CliRunner

from codementor.cli.main import app


def test_serve_rejects_external_host_without_key_or_insecure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    run_mock = MagicMock()
    monkeypatch.setattr(uvicorn, "run", run_mock)
    monkeypatch.delenv("CODEMENTOR_TEST_API_KEY", raising=False)

    runner = CliRunner()
    result = runner.invoke(app, ["serve", "--host", "0.0.0.0"])
    assert result.exit_code == 3
    assert "Dışa açık adrese anahtarsız bağlanılamaz" in result.output
    run_mock.assert_not_called()


def test_serve_allows_external_host_with_insecure(monkeypatch: pytest.MonkeyPatch) -> None:
    run_mock = MagicMock()
    monkeypatch.setattr(uvicorn, "run", run_mock)
    monkeypatch.delenv("CODEMENTOR_TEST_API_KEY", raising=False)

    runner = CliRunner()
    result = runner.invoke(app, ["serve", "--host", "0.0.0.0", "--insecure"])
    assert result.exit_code == 0
    assert "--insecure etkin" in result.output
    run_mock.assert_called_once()


def test_serve_allows_loopback_normal(monkeypatch: pytest.MonkeyPatch) -> None:
    run_mock = MagicMock()
    monkeypatch.setattr(uvicorn, "run", run_mock)

    runner = CliRunner()
    result = runner.invoke(app, ["serve", "--host", "127.0.0.1"])
    assert result.exit_code == 0
    run_mock.assert_called_once()
