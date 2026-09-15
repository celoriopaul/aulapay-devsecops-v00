"""
Router principal de la versión 1 de AulaPay.

Centralizar los routers evita registrar cada módulo directamente
desde main.py y facilita incorporar nuevos dominios funcionales.
"""

from fastapi import APIRouter

from app.api.routes import health


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health.router)
