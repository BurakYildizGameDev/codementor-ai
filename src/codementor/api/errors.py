"""RFC 7807 hata yanıtları (mimari §9): her hata `application/problem+json`.

§9 hata kodları: 413 kod çok büyük · 422 dil belirlenemedi / geçersiz istek · 404 bulunamadı ·
503 sağlayıcı yapılandırması eksik ya da soru bankası okunamıyor (Faz 49). Tüm sağlayıcılar
düşse de bozulmuş rapor döndürülebildiği için 502 yerine 200 + `degraded=true` verilir.
"""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from codementor.log import get_logger
from codementor.models.api import PROBLEM_JSON, Problem
from codementor.pipeline.run_state import BANK_UNREADABLE, PipelineError, PipelineErrorKind
from codementor.questions import QuestionBankError

log = get_logger("codementor.api")

_KIND_STATUS: dict[PipelineErrorKind, tuple[int, str]] = {
    "too_large": (413, "Kod çok büyük"),
    "invalid": (422, "Geçersiz istek"),
    "not_found": (404, "Bulunamadı"),
    "provider": (503, "Sağlayıcı kullanılamıyor"),
    "unavailable": (503, "Hizmet kullanılamıyor"),
}
_TITLES = {
    400: "Hatalı istek",
    404: "Bulunamadı",
    405: "Yönteme izin verilmiyor",
    413: "Kod çok büyük",
    422: "Geçersiz istek",
    429: "Çok fazla istek",
    500: "Sunucu hatası",
    503: "Servis hazır değil",
}


class ApiProblemError(Exception):
    """Rotalardan fırlatılan, doğrudan problem+json'a dönüşen hata."""

    def __init__(
        self,
        status: int,
        detail: str,
        title: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(detail)
        self.status = status
        self.detail = detail
        self.title = title or _TITLES.get(status, "Hata")
        self.headers = headers or {}


def problem_response(problem: Problem, headers: dict[str, str] | None = None) -> JSONResponse:
    """Problem gövdesi, doğru içerik türüyle."""
    return JSONResponse(
        problem.model_dump(exclude_none=True),
        status_code=problem.status,
        media_type=PROBLEM_JSON,
        headers=headers,
    )


def pipeline_problem(exc: PipelineError, instance: str | None) -> Problem:
    """`PipelineError` → Problem (SSE `error` olayı da bunu kullanır)."""
    status, title = _KIND_STATUS[exc.kind]
    return Problem(title=title, status=status, detail=str(exc), instance=instance)


def install_error_handlers(app: FastAPI) -> None:
    """Uygulamaya problem+json işleyicilerini ekler."""

    @app.exception_handler(PipelineError)
    async def _pipeline(request: Request, exc: PipelineError) -> JSONResponse:
        return problem_response(pipeline_problem(exc, request.url.path))

    @app.exception_handler(ApiProblemError)
    async def _api(request: Request, exc: ApiProblemError) -> JSONResponse:
        return problem_response(
            Problem(
                title=exc.title, status=exc.status, detail=exc.detail, instance=request.url.path
            ),
            headers=exc.headers,
        )

    @app.exception_handler(RequestValidationError)
    async def _validation(request: Request, exc: RequestValidationError) -> JSONResponse:
        # girdi değeri (kullanıcı kodu) yanıta yansıtılmaz
        errors = [f"{'.'.join(str(p) for p in err['loc'])}: {err['msg']}" for err in exc.errors()]
        return problem_response(
            Problem(
                title="Geçersiz istek",
                status=422,
                detail="İstek gövdesi şemaya uymuyor.",
                instance=request.url.path,
                errors=errors[:20],
            )
        )

    @app.exception_handler(QuestionBankError)
    async def _bank(request: Request, exc: QuestionBankError) -> JSONResponse:
        # Sunucu verisi bozuk (Faz 49): istemci hatası değil, 500 de değil; düzelince geçer
        log.error(
            "question_bank_unreadable",
            path=request.url.path,
            error=type(exc).__name__,
            detail=str(exc)[:300],
        )
        return problem_response(
            Problem(
                title="Hizmet kullanılamıyor",
                status=503,
                detail=BANK_UNREADABLE,
                instance=request.url.path,
            )
        )

    @app.exception_handler(StarletteHTTPException)
    async def _http(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        status = exc.status_code
        return problem_response(
            Problem(
                title=_TITLES.get(status, "Hata"),
                status=status,
                detail=str(exc.detail),
                instance=request.url.path,
            )
        )

    @app.exception_handler(Exception)
    async def _unexpected(request: Request, exc: Exception) -> JSONResponse:
        log.error("api_unhandled", path=request.url.path, error=type(exc).__name__)
        return problem_response(
            Problem(
                title="Sunucu hatası",
                status=500,
                detail="Beklenmeyen bir hata oluştu.",
                instance=request.url.path,
            )
        )
