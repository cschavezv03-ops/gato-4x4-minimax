"""Configuración de la aplicación leída del entorno."""

import os

# Orígenes permitidos por CORS. Se sobreescribe con la variable de entorno
# CORS_ORIGINS (lista separada por comas) para el despliegue.
_DEFAULT_ORIGINS = "http://localhost:5173,http://127.0.0.1:5173"


class Settings:
    """Ajustes de la API."""

    cors_origins: list[str] = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", _DEFAULT_ORIGINS).split(",")
        if origin.strip()
    ]


settings = Settings()
