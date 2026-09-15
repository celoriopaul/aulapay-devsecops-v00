# ============================================================
# AulaPay Backend
# Imagen Python para ejecutar FastAPI.
# ============================================================

FROM python:3.13-slim

# Evita la generación de archivos .pyc.
ENV PYTHONDONTWRITEBYTECODE=1

# Fuerza salida inmediata de logs hacia stdout/stderr.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# ------------------------------------------------------------
# Dependencias
#
# Copiamos primero requirements.txt para aprovechar la caché
# por capas de Docker cuando solo cambia el código fuente.
# ------------------------------------------------------------

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    --disable-pip-version-check \
    -r requirements.txt

# ------------------------------------------------------------
# Usuario de ejecución
#
# El backend no necesita ejecutarse como root.
# ------------------------------------------------------------

RUN groupadd \
        --system \
        appgroup \
    && useradd \
        --system \
        --gid appgroup \
        --create-home \
        appuser

# Copia únicamente el código requerido por la aplicación.
COPY app ./app

# El usuario de aplicación será propietario del directorio.
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

# ------------------------------------------------------------
# Proceso principal
#
# Uvicorn inicia la aplicación FastAPI escuchando en todas las
# interfaces del contenedor a través del puerto 8000.
# ------------------------------------------------------------

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]