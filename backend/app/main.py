"""Punto de entrada de la API FastAPI.

Arranque local:
    uvicorn app.main:app --reload

Documentación interactiva: http://localhost:8000/api/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router
from .config import settings

app = FastAPI(
    title="Gato 4x4 IA - API",
    description="API REST del juego Gato 4x4 con IA (Minimax y poda Alpha-Beta).",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url=None,
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["sistema"], summary="Información de la API")
def root() -> dict[str, str]:
    """Devuelve información básica y el enlace a la documentación."""
    return {"name": "Gato 4x4 IA - API", "docs": "/api/docs"}
