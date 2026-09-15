"""
Schemas correspondientes al estado de salud de AulaPay.
"""

from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """
    Contrato de respuesta del endpoint de salud.
    """

    status: Literal["healthy", "degraded"]
    service: str
    version: str
    environment: str
    database: Literal["healthy", "unhealthy"]
