"""REST uç noktaları (mimari §9). Rotalar incedir; iş orkestratörde ve katman modüllerindedir."""

from __future__ import annotations

import asyncio
import json
import re
from collections.abc import AsyncIterator, Callable
from functools import lru_cache
from importlib.resources import files
from typing import Annotated, Any

from fastapi import APIRouter, Body, Query, Request, status
from fastapi.responses import JSONResponse, PlainTextResponse, Response, StreamingResponse
from starlette.background import BackgroundTask

from codementor import __version__
from codementor.api.disconnect import ClientDisconnectedError, run_until_disconnect
from codementor.api.errors import ApiProblemError
from codementor.api.sse import SSE_HEADERS, stream_analysis
from codementor.api.state import ApiState
from codementor.config import Settings
from codementor.languages import CANONICAL_SUFFIX
from codementor.models.api import PROBLEM_JSON, Health, Problem, Readiness
from codementor.models.enums import Difficulty, Engine, Language
from codementor.models.provider import ProviderStatus
from codementor.models.questions import QuestionPublic
from codementor.models.report import ULID_PATTERN, AnalysisReport
from codementor.models.request import AnalysisRequest
from codementor.models.rules import RuleInfo
from codementor.providers.factory import chain_names
from codementor.providers.health import check_providers
from codementor.questions.bank import QuestionNotFoundError
from codementor.report.markdown import to_markdown
from codementor.report.sarif import to_sarif
from codementor.rules.catalog import rule_catalog
from codementor.storage.cache import delete_analysis, get_analysis
from codementor.validation.toolchain import compiler_statuses, get_toolchain

SARIF_MEDIA_TYPE = "application/sarif+json"
MARKDOWN_MEDIA_TYPE = "text/markdown; charset=utf-8"
# Kaba ön sınır (karakter): asıl bayt/satır sınırı K0'da (`too_large`); bu, devasa girdiyi
# normalizasyona hiç sokmaz (Faz 47)
CODE_CHARS_FACTOR = 4

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
async def analyze(request: Request, body: AnalyzeBody) -> AnalysisReport | Response:
    """Senkron analiz. Sağlayıcıların hepsi düşse de rapor döner (`meta.degraded=true`).
    İstemci yanıtı beklemeden koparsa analiz iptal edilir (Faz 48; yanıt 499, okuyan yok)."""
    state = _state(request)
    _admit(state, body)
    try:
        return await run_until_disconnect(request.receive, state.orchestrator().analyze(body))
    except ClientDisconnectedError:
        return Response(status_code=499)
    finally:
        state.slots.release()


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
        },
        **_problems(413, 422, 503),
    },
    tags=["analiz"],
)
async def analyze_stream(request: Request, body: AnalyzeBody) -> StreamingResponse:
    """SSE: `stage` olayları (`started`/`completed`/`skipped`), sonda `report` ya da `error`."""
    state = _state(request)
    _admit(state, body)
    release = _once(state.slots.release)

    async def guarded() -> AsyncIterator[str]:
        try:
            async for chunk in stream_analysis(state.orchestrator, body, request.url.path):
                yield chunk
        finally:
            release()

    # akış hiç başlamadan kopan bağlantıda da yuva bırakılsın: arka plan görevi yedek
    return StreamingResponse(
        guarded(),
        media_type="text/event-stream",
        headers=SSE_HEADERS,
        background=BackgroundTask(release),
    )


def allowed_providers(settings: Settings) -> list[str]:
    """İstekte seçilebilen sağlayıcılar: `api.allowed_providers`, yoksa varsayılan + fallback."""
    configured = settings.api.allowed_providers
    return configured if configured is not None else chain_names(settings.providers)


def _admit(state: ApiState, body: AnalysisRequest) -> None:
    """Analiz kapısı (Faz 47): izinli sağlayıcı, kaba kod sınırı, eşzamanlılık yuvası.

    Yuva en son alınır; reddedilen istek yuva tutmaz. Alınan yuvayı çağıran bırakır.
    """
    settings = state.settings
    if body.provider is not None and body.provider not in allowed_providers(settings):
        raise ApiProblemError(
            422, f"'{body.provider}' sağlayıcısı bu sunucuda seçilemez (api.allowed_providers)."
        )
    if len(body.code) > settings.limits.max_bytes * CODE_CHARS_FACTOR:
        raise ApiProblemError(413, "Kod çok büyük: sınırın çok üzerinde (limits.max_bytes).")
    if not state.slots.try_acquire():
        raise ApiProblemError(
            503, "Sunucu meşgul: eşzamanlı analiz sınırına ulaşıldı; biraz sonra yeniden dene."
        )


def _once(action: Callable[[], None]) -> Callable[[], None]:
    done = False

    def run() -> None:
        nonlocal done
        if not done:
            done = True
            action()

    return run


def _stored(request: Request, analysis_id: str) -> AnalysisReport:
    # Biçimi bozuk kimlik veritabanına hiç gitmez; varlığı sızdırmamak için yine 404 (Faz 27)
    valid = re.fullmatch(ULID_PATTERN, analysis_id) is not None
    report = get_analysis(_state(request).database(), analysis_id) if valid else None
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
    artifact = f"{report.analysis_id}{CANONICAL_SUFFIX[report.language]}"
    return JSONResponse(to_sarif(report, artifact), media_type=SARIF_MEDIA_TYPE)


@router.get(
    "/v1/analyses/{analysis_id}/markdown",
    responses={200: {"content": {"text/markdown": {}}}, **_problems(404)},
    tags=["analiz"],
)
def get_markdown(request: Request, analysis_id: str) -> PlainTextResponse:
    """Kayıtlı raporun Markdown dışa aktarımı (Faz 26; kod içermez)."""
    report = _stored(request, analysis_id)
    return PlainTextResponse(to_markdown(report), media_type=MARKDOWN_MEDIA_TYPE)


@router.delete(
    "/v1/analyses/{analysis_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={204: {"description": "Analiz silindi."}, **_problems(404)},
    tags=["analiz"],
)
def delete_stored(request: Request, analysis_id: str) -> Response:
    """Kayıtlı analizi siler (Faz 62)."""
    valid = re.fullmatch(ULID_PATTERN, analysis_id) is not None
    if not valid:
        raise ApiProblemError(404, f"'{analysis_id}' kimlikli analiz bulunamadı.")
    deleted = delete_analysis(_state(request).database(), analysis_id)
    if not deleted:
        raise ApiProblemError(404, f"'{analysis_id}' kimlikli analiz bulunamadı.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


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
    """İstekte seçilebilen sağlayıcılar ve erişilebilirlik; anahtar değeri dönmez (Faz 47)."""
    settings = _state(request).settings
    return await check_providers(allowed_providers(settings), settings.providers)


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
    # zig sondası (ilk keşifte ~0,4 sn) olay döngüsünü kilitlemesin
    toolchain = await asyncio.to_thread(get_toolchain, settings.validation)
    compilers = compiler_statuses(toolchain)
    return Readiness(ready=all(s.ready for s in statuses), providers=statuses, compilers=compilers)
