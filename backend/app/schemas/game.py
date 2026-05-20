"""Modelos Pydantic que definen el contrato de la API.

Toda petición es autónoma (stateless): lleva el tablero completo. El servidor
valida la forma del tablero (3x3 o 4x4); la legalidad de cada jugada la
verifica el núcleo.
"""

from typing import Annotated, Literal, Optional

from pydantic import AfterValidator, BaseModel, Field

from ..core.constants import (
    DEFAULT_BOARD_SIZE,
    DEFAULT_DEPTH_LIMIT,
    EMPTY,
    PLAYER_1,
    PLAYER_2,
    SUPPORTED_BOARD_SIZES,
)

Player = Literal["X", "O"]
Algorithm = Literal["minimax", "alpha_beta"]
BoardSize = Literal[3, 4]
Position = tuple[int, int]


def _validate_board(board: list[list[str]]) -> list[list[str]]:
    """Verifica que el tablero sea cuadrado de 3x3 o 4x4 y con celdas válidas."""
    valid_cells = {PLAYER_1, PLAYER_2, EMPTY}
    size = len(board)
    if size not in SUPPORTED_BOARD_SIZES:
        raise ValueError("El tablero debe ser de 3x3 o 4x4")
    for row in board:
        if len(row) != size:
            raise ValueError(f"Cada fila debe tener {size} columnas")
        for cell in row:
            if cell not in valid_cells:
                raise ValueError(f"Celda inválida: {cell!r}")
    return board


BoardField = Annotated[list[list[str]], AfterValidator(_validate_board)]
DepthField = Annotated[int, Field(ge=1, le=6)]


# --- Peticiones ---------------------------------------------------------------


class NewGameRequest(BaseModel):
    """Petición para crear una partida nueva."""

    size: BoardSize = DEFAULT_BOARD_SIZE


class MoveRequest(BaseModel):
    """Petición para aplicar una jugada de un jugador."""

    board: BoardField
    current_player: Player
    move: Position


class AiMoveRequest(BaseModel):
    """Petición para que la IA calcule y aplique su jugada."""

    board: BoardField
    current_player: Player
    ai_player: Player
    algorithm: Algorithm = "alpha_beta"
    depth_limit: DepthField = DEFAULT_DEPTH_LIMIT


class CompareRequest(BaseModel):
    """Petición para comparar Minimax y Alpha-Beta sobre el mismo estado."""

    board: BoardField
    current_player: Player
    ai_player: Player
    depth_limit: DepthField = DEFAULT_DEPTH_LIMIT


# --- Respuestas ---------------------------------------------------------------


class GameStateResponse(BaseModel):
    """Estado completo del juego tras una jugada."""

    board: list[list[str]]
    current_player: Player
    winner: Optional[Player]
    is_draw: bool
    is_terminal: bool
    legal_moves: list[Position]
    winning_line: Optional[list[Position]]


class AiMetrics(BaseModel):
    """Métricas de una ejecución de un algoritmo de IA."""

    algorithm: Algorithm
    move: Position
    score: int
    nodes_evaluated: int
    elapsed_ms: float
    is_random: bool = False


class AiMoveResponse(BaseModel):
    """Resultado de la jugada de la IA: métricas y nuevo estado."""

    metrics: AiMetrics
    state: GameStateResponse


class CompareResponse(BaseModel):
    """Comparación entre Minimax y Alpha-Beta para la misma jugada."""

    minimax: AiMetrics
    alpha_beta: AiMetrics
    nodes_saved: int
    state: GameStateResponse
