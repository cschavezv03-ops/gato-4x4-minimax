from dataclasses import dataclass
from typing import Optional, Tuple

from .constants import BOARD_SIZE, EMPTY, PLAYER_1

# aqui ando haciendo el tablero como una tupla de tuplas

Board = Tuple[Tuple[str, str, str, str], Tuple[str, str, str, str], 
              Tuple[str, str, str, str], Tuple[str, str, str, str]] 

@dataclass(frozen=True) #esto es para que no se pueda modificar el estado del tablero
class GameState:
    board: Board
    current_player: str
    winner : Optional[str] = None


def create_initial_state():
    """
    Va a crear el estado inicial del juego (todo tablero vacio), el jugador inicial va a ser el jugador 0 (ESTE VA A SER LA IA) (X)
    return: GameState
    """
    board = tuple(
        tuple (EMPTY for _ in range(BOARD_SIZE))  # Crea una fila vacía
        for _ in range(BOARD_SIZE)
    )

    return GameState(
        board=board,
        current_player=PLAYER_1,  # El primer jugador comienza
        winner=None
    )
    
