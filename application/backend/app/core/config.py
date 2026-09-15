"""
Configuración central de AulaPay.

Este módulo concentra las variables de configuración utilizadas
por el backend. Los valores sensibles se reciben exclusivamente
mediante variables de entorno.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Representa la configuración global de AulaPay.

    Pydantic valida automáticamente las variables recibidas desde
    el entorno antes de que la aplicación termine de iniciar.
    """

    # --------------------------------------------------------
    # Aplicación
    # --------------------------------------------------------

    app_name: str = "AulaPay API"
    app_env: str = "development"
    app_version: str = "0.1.0"

    # --------------------------------------------------------
    # PostgreSQL
    # --------------------------------------------------------

    db_host: str
    db_port: int = 5432
    db_name: str
    db_user: str
    db_password: str

    # Ignora variables adicionales que puedan existir dentro
    # del contenedor y que no pertenezcan a esta configuración.
    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def database_dsn(self) -> str:
        """
        Construye el DSN utilizado para conectarse a PostgreSQL.

        Returns:
            Cadena de conexión compatible con asyncpg.
        """

        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache
def get_settings() -> Settings:
    """
    Devuelve una única instancia reutilizable de configuración.

    El uso de caché evita reconstruir y validar Settings en cada
    solicitud HTTP.
    """

    return Settings()
