"""Constantes del juego Gato.

El juego admite tableros 3x3 y 4x4. El tamaño no es una constante global:
cada función lo deriva del propio tablero. Aquí solo se define el valor por
defecto y el conjunto de tamaños admitidos.
"""

from typing import Final

# Tamaños de tablero admitidos y valor por defecto.
SUPPORTED_BOARD_SIZES: Final[tuple[int, ...]] = (3, 4)
DEFAULT_BOARD_SIZE: Final[int] = 4

EMPTY: Final[str] = "."
PLAYER_1: Final[str] = "X"
PLAYER_2: Final[str] = "O"

PLAYERS: Final[tuple[str, str]] = (PLAYER_1, PLAYER_2)

# Puntajes de la función de utilidad para estados terminales.
WIN_SCORE: Final[int] = 100_000
LOSE_SCORE: Final[int] = -100_000
DRAW_SCORE: Final[int] = 0

# Profundidad máxima por defecto para la búsqueda con límite.
DEFAULT_DEPTH_LIMIT: Final[int] = 3
