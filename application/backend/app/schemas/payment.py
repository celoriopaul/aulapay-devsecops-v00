"""
Esquemas de transferencia de datos para el módulo de pagos.

Los modelos definidos en este archivo representan la información que
la API AulaPay expone a sus consumidores. La capa de schemas evita
devolver directamente estructuras internas de la base de datos.
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PaymentResponse(BaseModel):
    """
    Representa un pago asociado a un estudiante.

    El campo receipt_url contiene la referencia lógica al comprobante
    generado para el pago. En esta fase del laboratorio no se almacena
    el archivo PDF directamente en PostgreSQL.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: str
    external_reference: str
    amount: Decimal
    currency: str
    status: str
    payment_date: datetime
    receipt_url: str | None = None