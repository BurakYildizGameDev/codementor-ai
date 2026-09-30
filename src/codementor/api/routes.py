"""REST uç noktaları (mimari §9). Rotalar incedir; iş orkestratörde ve katman modüllerindedir."""

from __future__ import annotations

import json
from functools import lru_cache
from importlib.resources import files
from typing import Annotated, Any

from fastapi import APIRouter, Body, Query, Request
from fastapi.responses import JSONResponse, StreamingResponse

from codementor import __version__
from codementor.api.errors import ApiProblemError
from codementor.api.sse import SSE_HEADERS, stream_analysis
from codementor.api.state import ApiState
from codementor.models.api import PROBLEM_JSON, CompilerStatus, Health, Problem, Readiness
from codementor.models.enums import Difficulty, Engine, Language
from codementor.models.provider import ProviderStatus
from codementor.models.questions import QuestionPublic
from codementor.models.report import AnalysisReport
from codementor.models.request import AnalysisRequest
from codementor.models.rules import RuleInfo
from codementor.providers.factory import chain_names
from codementor.providers.health import check_providers
from codementor.questions.bank import QuestionNotFoundError
from codementor.report.sarif import to_sarif
from codementor.rules.catalog import rule_catalog
from codementor.storage.cache import get_analysis
from codementor.validation.toolchain import get_toolchain

SARIF_MEDIA_TYPE = "application/sarif+json"
_EXTENSIONS = {Language.C: "c", Language.CPP: "cpp", Language.CSHARP: "cs"}

router = APIRouter()


@lru_cache(maxsize=1)
def examples() -> dict[str, Any]:
    """OpenAPI örnekleri (§9 istek, §6.5 rapor); paket verisi."""
    base = files("codementor.api") / "examples"
    return {
        "request": json.loads((base / "analyze_request.json").read_text(encoding="utf-8")),
        "report": json.loads((base / "report.json").read_text(encoding="utf-8")),
    }


def _problems(*codes: int) -> dict[int | str, dict[str, Any]]:
    return {code: {"model": Problem, "content": {PROBLEM_JSON: {}}} for code in codes}


def _report_response() -> dict[int | str, dict[str, Any]]:
    return {200: {"content": {"application/json": {"example": examples()["report"]}}}}


AnalyzeBody = Annotated[
    AnalysisRequest,
    Body(
        openapi_examples={"unity": {"summary": "C hesap makinesi", "value": examples()["request"]}}
    ),
]


def _state(request: Request) -> ApiState:
    state: ApiState = request.app.state.codementor
    return state


@router.post(
    "/v1/analyze",
    response_model=AnalysisReport,
    responses={**_report_response(), **_problems(404, 413, 422, 503)},
    tags=["analiz"],
)
async def analyze(request: Request, body: AnalyzeBody) -> AnalysisReport:
    """Senkron analiz. Sağlayıcıların hepsi düşse de rapor döner (`meta.degraded=true`)."""
    return await _state(request).orchestrator().analyze(body)


@router.post(
    "/v1/analyze/stream",
    response_class=StreamingResponse,
    responses={
        200: {
            "content": {
                "text/event-stream": {
                    "example": 'event: stage\ndata: {"stage":"tier0","status":"completed",'
                    '"duration_ms":6}\n\nevent: report\ndata: {...AnalysisReport...}\n\n'
                }
            }
        }
    },
    tags=["analiz"],
)
async def analyze_stream(request: Request, body: AnalyzeBody) -> StreamingResponse:
    """SSE: `stage` olayları (`started`/`completed`/`skipped`), sonda `report` ya da `error`."""
    state = _state(request)
    stream = stream_analysis(state.orchestrator, body, request.url.path)
    return StreamingResponse(stream, media_type="text/event-stream", headers=SSE_HEADERS)


def _stored(request: Request, analysis_id: str) -> AnalysisReport:
    report = get_analysis(_state(request).database(), analysis_id)
    if report is None:
        raise ApiProblemError(404, f"'{analysis_id}' kimlikli analiz bulunamadı.")
    return report


@router.get(
    "/v1/analyses/{analysis_id}",
    response_model=AnalysisReport,
    responses={**_report_response(), **_problems(404)},
    tags=["analiz"],
)
def get_stored(request: Request, analysis_id: str) -> AnalysisReport:
    """Kayıtlı raporu getirir."""
    return _stored(request, analysis_id)


@router.get(
    "/v1/analyses/{analysis_id}/sarif",
    responses={200: {"content": {SARIF_MEDIA_TYPE: {}}}, **_problems(404)},
    tags=["analiz"],
)
def get_sarif(request: Request, analysis_id: str) -> JSONResponse:
    """Kayıtlı raporun SARIF 2.1.0 dışa aktarımı."""
    report = _stored(request, analysis_id)
    artifact = f"{report.analysis_id}.{_EXTENSIONS[report.language]}"
    return JSONResponse(to_sarif(report, artifact), media_type=SARIF_MEDIA_TYPE)


@router.get("/v1/questions", response_model=list[QuestionPublic], tags=["sorular"])
def list_questions(
    request: Request,
    language: Annotated[Language | None, Query()] = None,
    engine: Annotated[Engine | None, Query()] = None,
    difficulty: Annotated[Difficulty | None, Query()] = None,
) -> list[QuestionPublic]:
    """Soru listesi (referans çözüm ve mentorluk verisi olmadan)."""
    return _state(request).questions().filter(language, engine, difficulty)


@router.get(
    "/v1/questions/{question_id}",
    response_model=QuestionPublic,
    responses=_problems(404),
    tags=["sorular"],
)
def get_question(request: Request, question_id: str) -> QuestionPublic:
    """Soru detayı; referans çözüm yolu (§12) ve ipucu merdiveni **dönmez**."""
    try:
        return _state(request).questions().public(question_id)
    except QuestionNotFoundError as exc:
        raise ApiProblemError(404, str(exc).strip("'\"")) from exc


@router.get("/v1/providers", response_model=list[ProviderStatus], tags=["sistem"])
async def list_providers(request: Request) -> list[ProviderStatus]:
    """Etkin sağlayıcılar (varsayılan + fallback) ve erişilebilirlik; anahtar değeri dönmez."""
    providers = _state(request).settings.providers
    return await check_providers(chain_names(providers), providers)


@router.get("/v1/rules", response_model=list[RuleInfo], tags=["sistem"])
def list_rules(
    language: Annotated[Language | None, Query()] = None,
    engine: Annotated[Engine | None, Query()] = None,
) -> list[RuleInfo]:
    """Statik kural kataloğu."""
    return rule_catalog(language, engine)


@router.get("/health", response_model=Health, tags=["sistem"])
def health() -> Health:
    """Canlılık."""
    return Health(version=__version__)


@router.get("/health/ready", response_model=Readiness, tags=["sistem"])
async def ready(request: Request) -> Readiness:
    """Hazırlık: birincil sağlayıcı hazır mı + bulunan derleyiciler (yoksa Tier 1 SKIPPED)."""
    settings = _state(request).settings
    statuses = await check_providers([settings.providers.default], settings.providers)
    toolchain = get_toolchain(settings.validation)
    compilers = [
        CompilerStatus(target=target, tool=tool.name if tool else None)
        for target, tool in (
            ("c", toolchain.c),
            ("cpp", toolchain.cpp),
            ("unreal", toolchain.unreal),
            ("csharp", toolchain.csharp),
        )
    ]
    return Readiness(ready=all(s.ready for s in statuses), providers=statuses, compilers=compilers)
