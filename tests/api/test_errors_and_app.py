"""RFC 7807 hata eşlemesi, CORS, OpenAPI örnekleri, `serve` varsayılanları."""

from __future__ import annotations

from typing import Any

import httpx
import pytest
from typer.testing import CliRunner

import codementor.cli.serve as serve_module
from codementor.api.app import create_app
from codementor.cli.main import app as cli_app
from codementor.cli.serve import is_loopback
from codementor.config import Settings
from codementor.providers.base import ProviderConfigError
from codementor.storage.db import Database
from tests.api.conftest import ClientFactory
from tests.integration.conftest import FakeFactory

pytestmark = pytest.mark.anyio
PROBLEM = "application/problem+json"


async def test_code_too_large_413(client_for: ClientFactory, fake: FakeFactory) -> None:
    body = {"code": "int x;\n" * 10_000, "language": "c"}
    response = await client_for(fake()).post("/v1/analyze", json=body)
    assert response.status_code == 413
    assert response.headers["content-type"] == PROBLEM
    problem = response.json()
    assert problem["status"] == 413
    assert problem["title"] == "Kod çok büyük"
    assert problem["instance"] == "/v1/analyze"


async def test_invalid_body_422_without_echoing_input(client_for: ClientFactory) -> None:
    secret = "gizli_kullanici_kodu_42"
    response = await client_for().post(
        "/v1/analyze", json={"code": secret, "language": "cobol", "extra": 1}
    )
    assert response.status_code == 422
    assert response.headers["content-type"] == PROBLEM
    problem = response.json()
    assert any(e.startswith("body.language") for e in problem["errors"])
    assert secret not in response.text


async def test_undetectable_language_422(client_for: ClientFactory, fake: FakeFactory) -> None:
    response = await client_for(fake()).post("/v1/analyze", json={"code": "merhaba dünya"})
    assert response.status_code == 422
    assert response.headers["content-type"] == PROBLEM


async def test_unknown_question_in_analyze_404(
    client_for: ClientFactory, fake: FakeFactory
) -> None:
    response = await client_for(fake()).post(
        "/v1/analyze", json={"code": "int x;", "language": "c", "question_id": "yok"}
    )
    assert response.status_code == 404
    assert response.headers["content-type"] == PROBLEM


async def test_provider_config_missing_503(settings: Settings, db: Database) -> None:
    def broken(_name: str) -> Any:
        raise ProviderConfigError("openai", "model tanımlı değil")

    app = create_app(settings, db=db, provider_factory=broken)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://127.0.0.1"
    ) as c:
        response = await c.post("/v1/analyze", json={"code": "int x;", "language": "c"})
    assert response.status_code == 503
    assert response.headers["content-type"] == PROBLEM
    assert "model tanımlı değil" in response.json()["detail"]


async def test_unknown_route_and_method_are_problems(client_for: ClientFactory) -> None:
    client = client_for()
    missing = await client.get("/v1/yok")
    assert missing.status_code == 404
    assert missing.headers["content-type"] == PROBLEM
    wrong = await client.get("/v1/analyze")
    assert wrong.status_code == 405
    assert wrong.headers["content-type"] == PROBLEM


async def test_cors_only_configured_origin(client_for: ClientFactory) -> None:
    client = client_for()
    allowed = await client.options(
        "/v1/analyze",
        headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "POST"},
    )
    assert allowed.headers.get("access-control-allow-origin") == "http://localhost:5173"
    denied = await client.options(
        "/v1/analyze",
        headers={"Origin": "http://evil.example", "Access-Control-Request-Method": "POST"},
    )
    assert "access-control-allow-origin" not in denied.headers


async def test_cors_allows_delete_method(client_for: ClientFactory) -> None:
    """Faz 62: CORS preflight DELETE metoduna izin verir."""
    client = client_for()
    response = await client.options(
        "/v1/analyses/01J9ZK4M8Q3W6Y2T5R7N1B0C9D",
        headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "DELETE"},
    )
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"
    allowed_methods = response.headers.get("access-control-allow-methods", "")
    assert "DELETE" in allowed_methods


async def test_openapi_has_examples(client_for: ClientFactory) -> None:
    client = client_for()
    spec = (await client.get("/openapi.json")).json()
    analyze = spec["paths"]["/v1/analyze"]["post"]
    request_examples = analyze["requestBody"]["content"]["application/json"]["examples"]
    assert next(iter(request_examples.values()))["value"]["question_id"] == "c-veryeasy-calculator"
    report_example = analyze["responses"]["200"]["content"]["application/json"]["example"]
    assert report_example["schema_version"] == "1.0"
    assert PROBLEM in analyze["responses"]["413"]["content"]
    stream = spec["paths"]["/v1/analyze/stream"]["post"]["responses"]["200"]["content"]
    assert "event: report" in stream["text/event-stream"]["example"]
    docs = await client.get("/docs")
    assert docs.status_code == 200


def test_default_bind_is_loopback(settings: Settings) -> None:
    assert Settings.model_fields["api"].default_factory().host == "127.0.0.1"  # type: ignore[misc]
    assert settings.api.host == "127.0.0.1"


@pytest.mark.parametrize(
    ("host", "loopback"),
    [
        ("127.0.0.1", True),
        ("::1", True),
        ("localhost", True),
        ("0.0.0.0", False),
        ("192.168.1.5", False),
    ],
)
def test_is_loopback(host: str, loopback: bool) -> None:
    assert is_loopback(host) is loopback


def test_serve_uses_config_and_warns_when_exposed(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[dict[str, Any]] = []
    monkeypatch.setattr(serve_module.uvicorn, "run", lambda app, **kw: calls.append(kw))
    result = CliRunner().invoke(cli_app, ["serve"])
    assert result.exit_code == 0
    assert calls[-1]["host"] == "127.0.0.1"
    assert calls[-1]["port"] == 8000
    assert "Uyarı" not in result.output
    exposed = CliRunner().invoke(
        cli_app, ["serve", "--host", "0.0.0.0", "--port", "9000", "--insecure"]
    )
    assert calls[-1] == {"host": "0.0.0.0", "port": 9000, "log_level": "warning"}
    assert "Uyarı" in exposed.output
