"""
Dependencias reutilizables de la API AulaPay.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import (
    InvalidAuthenticationTokenError,
    authentication_provider,
)
from app.schemas.student import AuthenticatedStudent


bearer_scheme = HTTPBearer(
    auto_error=False,
)


async def get_current_student(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
) -> AuthenticatedStudent:
    """
    Obtiene la identidad correspondiente al token Bearer recibido.

    Esta dependencia comprueba autenticación, pero deliberadamente no
    determina si el estudiante puede acceder al recurso solicitado.
    La autorización a nivel de objeto pertenece a la capa de negocio.
    """

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Se requiere autenticación.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        return authentication_provider.authenticate(
            credentials.credentials,
        )
    except InvalidAuthenticationTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc