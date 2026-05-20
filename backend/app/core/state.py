"""Estado inmutable de una partida.

El tablero es una tupla de tuplas para garantizar inmutabilidad. Su tamaño
(3 o 4) se deriva del propio tablero con `board_size`.
"""

from dataclasses import dataclass
from typing import Optional

from .constants import DEFAULT_BOARD_SIZE, EMPTY, PLAYER_1

# Una fila y un tablero como estructuras inmutables.
Row = tuple[str, ...]
Board = tuple[Row, ...]
Move = tuple[int, int]


@dataclass(frozen=True)
class GameState:
    """Estado inmutable del juego en un instante dado.

    Attributes:
        board: Tablero NxN como tupla de tuplas.
        current_player: Jugador al que le toca mover ("X" u "O").
        winner: Símbolo del ganador, o None si la partida sigue o es empate.
    """

    board: Board
    current_player: str
    winner: Optional[str] = None


def board_size(board: Board) -> int:
    """Devuelve el tamaño N de un tablero NxN."""
    return len(board)


def create_initial_state(size: int = DEFAULT_BOARD_SIZE) -> GameState:
    """Crea el estado inicial: tablero NxN vacío, comienza PLAYER_1 (X).

    Args:
        size: Tamaño del tablero (3 o 4).

    Returns:
        GameState con el tablero vacío y sin ganador.
    """
    board: Board = tuple(
        tuple(EMPTY for _ in range(size)) for _ in range(size)
    )
    return GameState(board=board, current_player=PLAYER_1, winner=None)
