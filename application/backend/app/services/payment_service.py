"""
Servicio de negocio para la gestión de pagos.

Esta capa actúa como intermediaria entre las rutas HTTP y el repositorio
de datos. Su objetivo es mantener separadas las responsabilidades de
presentación, lógica de negocio y persistencia.
"""

from app.db.repositories.payments import payment_repository
from app.schemas.payment import PaymentResponse


class PaymentService:
    """
    Proporciona las operaciones de negocio relacionadas con pagos.
    """

    async def get_student_payments(
        self,
        student_code: str,
    ) -> list[PaymentResponse]:
        """
        Obtiene los pagos asociados al código de un estudiante.

        En el baseline vulnerable todavía no se realiza aquí la
        autorización sobre el propietario del recurso. Esa ausencia
        será utilizada posteriormente para demostrar el problema
        de autorización a nivel de objeto (BOLA/IDOR).
        """

        records = await payment_repository.get_by_student_code(
            student_code=student_code,
        )

        return [
            PaymentResponse(
                id=record["id"],
                student_id=record["student_id"],
                external_reference=record["external_reference"],
                amount=record["amount"],
                currency=record["currency"],
                status=record["status"],
                payment_date=record["payment_date"],
                receipt_url=record["receipt_url"],
            )
            for record in records
        ]


payment_service = PaymentService()