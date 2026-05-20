"""Rutas REST de la API del juego.

Las rutas son finas: validan la entrada (vía Pydantic), delegan en el servicio
y traducen los errores de reglas a respuestas HTTP 422.
"""

from fastapi import APIRouter, HTTPException, status

from ..core.constants import DEFAULT_BOARD_SIZE
from ..schemas.game import (
    AiMoveRequest,
    AiMoveResponse,
    CompareRequest,
    CompareResponse,
    GameStateResponse,
    MoveRequest,
    NewGameRequest,
)
from ..services import game_service
from ..services.game_service import IllegalMoveError

router = APIRouter(prefix="/api")


@router.get("/health", tags=["sistema"], summary="Estado del servicio")
def health() -> dict[str, str]:
    """Comprobación de vida del servicio."""
    return {"status": "ok"}


@router.post(
    "/games/new",
    response_model=GameStateResponse,
    tags=["juego"],
    summary="Crear partida nueva",
)
def create_new_game(request: NewGameRequest | None = None) -> GameStateResponse:
    """Devuelve el estado inicial: tablero vacío (3x3 o 4x4) y turno de 'X'."""
    size = request.size if request else DEFAULT_BOARD_SIZE
    return game_service.new_game(size)


@router.post(
    "/moves",
    response_model=GameStateResponse,
    tags=["juego"],
    summary="Aplicar una jugada",
)
def apply_move(request: MoveRequest) -> GameStateResponse:
    """Aplica la jugada de un jugador y devuelve el nuevo estado."""
    try:
        return game_service.apply_player_move(
            request.board, request.current_player, request.move
        )
    except IllegalMoveError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)
        ) from exc


@router.post(
    "/ai/move",
    response_model=AiMoveResponse,
    tags=["ia"],
    summary="Jugada de la IA",
)
def ai_move(request: AiMoveRequest) -> AiMoveResponse:
    """Calcula y aplica la jugada de la IA con el algoritmo y profundidad dados."""
    try:
        return game_service.compute_ai_move(
            request.board,
            request.current_player,
            request.ai_player,
            request.algorithm,
            request.depth_limit,
        )
    except IllegalMoveError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)
        ) from exc


@router.post(
    "/ai/compare",
    response_model=CompareResponse,
    tags=["ia"],
    summary="Comparar Minimax vs Alpha-Beta",
)
def ai_compare(request: CompareRequest) -> CompareResponse:
    """Ejecuta ambos algoritmos sobre el mismo estado y compara los nodos evaluados."""
    try:
        return game_service.compare_algorithms(
            request.board,
            request.current_player,
            request.ai_player,
            request.depth_limit,
        )
    except IllegalMoveError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)
        ) from exc
