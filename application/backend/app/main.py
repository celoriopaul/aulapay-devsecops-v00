"""
Punto de entrada de AulaPay API.

Este módulo construye la aplicación FastAPI y administra los
recursos que deben abrirse y cerrarse durante su ciclo de vida.
"""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.db.connection import database


configure_logging()

logger = get_logger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Administra el ciclo de vida de los recursos de AulaPay.

    PostgreSQL se conecta una sola vez durante el arranque y el
    pool se cierra ordenadamente cuando termina la aplicación.
    """

    logger.info(
        "Iniciando %s versión %s",
        settings.app_name,
        settings.app_version,
    )

    await database.connect()

    yield

    await database.disconnect()

    logger.info("AulaPay finalizado correctamente")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "API de servicios de pago de la plataforma AulaPay."
    ),
    lifespan=lifespan,
)


app.include_router(api_router)


@app.get(
    "/",
    tags=["System"],
    summary="Información básica del servicio",
)
async def root() -> dict[str, str]:
    """
    Devuelve información mínima para identificar el servicio.
    """

    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "documentation": "/docs",
    }
