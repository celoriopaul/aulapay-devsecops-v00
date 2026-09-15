"""
Servicio de autorización de AulaPay.

Centraliza las decisiones de autorización sobre recursos pertenecientes
a estudiantes. La autenticación determina quién realiza la solicitud;
este servicio determina a qué recursos puede acceder esa identidad.
"""

from app.schemas.student import AuthenticatedStudent


class ResourceAccessDeniedError(Exception):
    """
    Se genera cuando una identidad autenticada intenta acceder a un
    recurso que pertenece a otro estudiante.
    """


class AuthorizationService:
    """
    Proporciona controles reutilizables de autorización a nivel de objeto.
    """

    def ensure_student_resource_access(
        self,
        current_student: AuthenticatedStudent,
        requested_student_code: str,
    ) -> None:
        """
        Comprueba que el estudiante autenticado sea propietario del
        recurso solicitado.

        Raises:
            ResourceAccessDeniedError:
                Cuando el recurso solicitado pertenece a otro estudiante.
        """

        if current_student.student_code != requested_student_code:
            raise ResourceAccessDeniedError(
                "El estudiante autenticado no puede acceder "
                "al recurso solicitado."
            )


authorization_service = AuthorizationService()