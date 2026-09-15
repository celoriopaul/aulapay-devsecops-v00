"""
Esquemas relacionados con la identidad del estudiante autenticado.

En esta fase del laboratorio se utiliza una identidad simplificada para
reproducir de forma controlada escenarios de autorización.
"""

from pydantic import BaseModel


class AuthenticatedStudent(BaseModel):
    """
    Representa la identidad autenticada utilizada por AulaPay.
    """

    student_code: str
    username: str
    role: str = "student"