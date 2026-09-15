"""
Administración de conexiones PostgreSQL.

Este módulo encapsula el pool de conexiones para evitar que las
rutas HTTP tengan que administrar conexiones directamente.
"""

import asyncpg

from app.core.config import get_settings
from app.core.logging import get_logger


logger = get_logger(__name__)


class Database:
    """
    Administra el ciclo de vida del pool PostgreSQL.

    Una única instancia puede ser compartida por los diferentes
    repositories de la aplicación.
    """

    def __init__(self) -> None:
        """Inicializa el administrador sin abrir conexiones."""

        self._pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        """
        Inicializa el pool de conexiones PostgreSQL.

        Raises:
            Exception:
                Si PostgreSQL no está disponible o las
                credenciales son inválidas.
        """

        settings = get_settings()

        logger.info("Inicializando pool de conexiones PostgreSQL")

        self._pool = await asyncpg.create_pool(
            dsn=settings.database_dsn,
            min_size=1,
            max_size=10,
            command_timeout=30,
        )

        logger.info("Pool PostgreSQL inicializado correctamente")

    async def disconnect(self) -> None:
        """
        Cierra de forma controlada todas las conexiones.
        """

        if self._pool is not None:
            logger.info("Cerrando pool PostgreSQL")

            await self._pool.close()
            self._pool = None

            logger.info("Pool PostgreSQL cerrado")

    async def healthcheck(self) -> bool:
        """
        Comprueba que PostgreSQL responde correctamente.

        Returns:
            True cuando la consulta de validación se ejecuta.
            False cuando la base de datos no está disponible.
        """

        if self._pool is None:
            return False

        try:
            async with self._pool.acquire() as connection:
                result = await connection.fetchval("SELECT 1;")

            return result == 1

        except Exception:
            logger.exception(
                "Falló la comprobación de salud de PostgreSQL"
            )
            return False

    @property
    def pool(self) -> asyncpg.Pool:
        """
        Expone el pool para los repositories.

        Raises:
            RuntimeError:
                Si algún componente intenta utilizar PostgreSQL
                antes de que la aplicación inicialice el pool.
        """

        if self._pool is None:
            raise RuntimeError(
                "El pool PostgreSQL no ha sido inicializado."
            )

        return self._pool


# Instancia compartida por toda la aplicación.
database = Database()
