"""
Router principal de la version 1 de AulaPay.

Centralizar los routers evita registrar cada modulo directamente
desde main.py y facilita incorporar nuevos dominios funcionales.
"""

from fastapi import APIRouter

from app.api.routes import health, payments


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health.router)
api_router.include_router(payments.router)