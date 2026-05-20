# Imagen del backend: API FastAPI del juego Gato.
FROM python:3.12-slim

WORKDIR /srv

# Evita archivos .pyc y fuerza salida sin búfer en logs.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instala las dependencias primero (capa cacheable).
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación.
COPY app ./app

# Ejecuta como usuario sin privilegios.
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
