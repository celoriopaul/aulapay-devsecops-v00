"""
Configuración de logging para AulaPay.

Centralizar el logging permite mantener un formato consistente
entre módulos y facilita una futura integración con plataformas
de observabilidad.
"""

import logging
import sys


LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | "
    "%(name)s | %(message)s"
)


def configure_logging() -> None:
    """
    Configura el logger raíz utilizado por la aplicación.

    La salida se dirige a stdout para que Docker pueda recolectar
    los eventos mediante su sistema estándar de logs.
    """

    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        stream=sys.stdout,
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger reutilizable para un módulo.

    Args:
        name:
            Nombre del módulo que solicita el logger.

    Returns:
        Instancia configurada de logging.Logger.
    """

    return logging.getLogger(name)
