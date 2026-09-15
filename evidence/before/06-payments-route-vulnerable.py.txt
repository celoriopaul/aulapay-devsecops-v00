"""
Endpoints HTTP relacionados con pagos de estudiantes.

Esta versión forma parte del baseline vulnerable del laboratorio
DevSecOps. La autenticación del usuario se valida correctamente,
pero todavía no se aplica autorización a nivel de objeto.

Esto permite reproducir deliberadamente un escenario BOLA/IDOR
que será detectado, documentado y corregido posteriormente.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_current_student
from app.schemas.payment import PaymentResponse
from app.schemas.student import AuthenticatedStudent
from app.services.payment_service import payment_service


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.get(
    "/{student_code}",
    response_model=list[PaymentResponse],
    status_code=status.HTTP_200_OK,
    summary="Consultar pagos de un estudiante",
)
async def get_student_payments(
    student_code: str,
    current_student: Annotated[
        AuthenticatedStudent,
        Depends(get_current_student),
    ],
) -> list[PaymentResponse]:
    """
    Obtiene los pagos asociados al código solicitado.

    BASELINE VULNERABLE:

    El endpoint verifica que exista un usuario autenticado, pero no
    comprueba que student_code corresponda al estudiante autenticado.

    Ejemplo vulnerable:

        Usuario autenticado: 1024
        Recurso solicitado:   2048
        Resultado actual:     HTTP 200

    Esta ausencia de autorización a nivel de objeto será corregida
    posteriormente durante la fase de remediación DevSecOps.
    """

    # La variable se conserva explícitamente porque demuestra que existe
    # una identidad autenticada aunque todavía no se utilice para autorizar
    # el acceso al recurso solicitado.
    _ = current_student

    return await payment_service.get_student_payments(
        student_code=student_code,
    )