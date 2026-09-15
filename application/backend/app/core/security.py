"""
Componentes de autenticación para el laboratorio AulaPay.

Esta implementación utiliza tokens Bearer de demostración para disponer
de identidades reproducibles durante las pruebas de seguridad.

No representa un proveedor de identidad productivo ni sustituye OAuth2,
OIDC o un servicio corporativo de identidad.
"""

from app.schemas.student import AuthenticatedStudent


class InvalidAuthenticationTokenError(Exception):
    """
    Se genera cuando el token recibido no corresponde a una identidad
    válida del laboratorio.
    """


class LabAuthenticationProvider:
    """
    Proveedor de autenticación simplificado para el entorno de laboratorio.
    """

    _identities = {
        "student-1024-token": AuthenticatedStudent(
            student_code="1024",
            username="andrea.mendoza",
        ),
        "student-2048-token": AuthenticatedStudent(
            student_code="2048",
            username="carlos.paredes",
        ),
    }

    def authenticate(
        self,
        token: str,
    ) -> AuthenticatedStudent:
        """
        Resuelve un token de laboratorio a una identidad autenticada.
        """

        identity = self._identities.get(token)

        if identity is None:
            raise InvalidAuthenticationTokenError(
                "Token de autenticación inválido."
            )

        return identity


authentication_provider = LabAuthenticationProvider()