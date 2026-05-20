# Imagen del backend: API FastAPI del juego Gato 4x4.
FROM python:3.12-slim

WORKDIR /srv

# Evita archivos .pyc y fuerza salida sin búfer en logs.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instala el proyecto y sus dependencias.
COPY pyproject.toml README.md ./
COPY app ./app
RUN pip install --no-cache-dir .

# Ejecuta como usuario sin privilegios.
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
