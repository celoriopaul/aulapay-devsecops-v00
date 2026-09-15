"""
Endpoints utilizados para comprobar el estado de AulaPay.
"""

from fastapi import APIRouter, Response, status

from app.core.config import get_settings
from app.db.connection import database
from app.schemas.health import HealthResponse


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "",
    response_model=HealthResponse,
    summary="Comprobar estado de AulaPay",
)
async def healthcheck(response: Response) -> HealthResponse:
    """
    Comprueba la disponibilidad de la API y PostgreSQL.

    Un estado degradado devuelve HTTP 503 para permitir que
    Docker, Kubernetes o un balanceador detecten que la instancia
    no está preparada para recibir tráfico.
    """

    settings = get_settings()
    database_healthy = await database.healthcheck()

    if not database_healthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        return HealthResponse(
            status="degraded",
            service=settings.app_name,
            version=settings.app_version,
            environment=settings.app_env,
            database="unhealthy",
        )

    return HealthResponse(
        status="healthy",
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
        database="healthy",
    )
