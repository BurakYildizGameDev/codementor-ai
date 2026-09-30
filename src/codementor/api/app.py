"""FastAPI uygulama fabrikası (mimari §9): CORS yalnızca yapılandırılan web UI kökenlerine."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from codementor import __version__
from codementor.api.errors import install_error_handlers
from codementor.api.routes import router
from codementor.api.state import ApiState
from codementor.config import Settings, get_settings
from codementor.pipeline.orchestrator import ProviderFactory
from codementor.storage.db import Database


def create_app(
    settings: Settings | None = None,
    *,
    db: Database | None = None,
    provider_factory: ProviderFactory | None = None,
) -> FastAPI:
    """Uygulamayı kurar; testler `db` ve `provider_factory` (FakeProvider) verebilir."""
    settings = settings or get_settings()
    state = ApiState(settings, db, provider_factory)

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
        yield
        state.close()

    app = FastAPI(
        title="CodeMentor AI",
        version=__version__,
        description="Kodu düzeltmeyen, denetleyip Sokratik sorular üreten kod mentoru.",
        docs_url="/docs",
        lifespan=lifespan,
    )
    app.state.codementor = state
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.api.cors_origins,
        allow_methods=["GET", "POST"],
        allow_headers=["content-type"],
    )
    install_error_handlers(app)
    app.include_router(router)
    return app
