"""
Repositorio de acceso a datos para pagos.

IMPORTANTE:
Esta versión corresponde al baseline vulnerable del laboratorio
DevSecOps. Contiene deliberadamente una construcción insegura de SQL
para que pueda ser identificada mediante SAST y posteriormente
corregida.

No utilizar este patrón en código de producción.
"""

from asyncpg import Record

from app.core.logging import get_logger
from app.db.connection import database


logger = get_logger(__name__)


class PaymentRepository:
    """
    Gestiona las operaciones de lectura relacionadas con pagos.

    La capa repository centraliza el acceso SQL y evita que las rutas
    HTTP conozcan detalles de persistencia.
    """

    async def get_by_student_code(
        self,
        student_code: str,
    ) -> list[Record]:
        """
        Obtiene los pagos asociados al código de un estudiante.

        VULNERABILIDAD INTENCIONAL:
        student_code se concatena directamente dentro de la consulta.
        Esta implementación será utilizada como evidencia BEFORE del
        análisis SAST y posteriormente será reemplazada por una consulta
        parametrizada.
        """

        query = (
            "SELECT "
            "p.id, "
            "s.student_code AS student_id, "
            "p.external_reference, "
            "p.amount, "
            "p.currency, "
            "p.status, "
            "p.payment_date, "
            "r.storage_path AS receipt_url "
            "FROM payments p "
            "INNER JOIN students s ON s.id = p.student_id "
            "LEFT JOIN payment_receipts r ON r.payment_id = p.id "
            "WHERE s.student_code = '" + student_code + "' "
            "ORDER BY p.payment_date DESC"
        )

        logger.info(
            "Consultando pagos para student_code=%s",
            student_code,
        )

        async with database.pool.acquire() as connection:
            records = await connection.fetch(query)

        return records


payment_repository = PaymentRepository()