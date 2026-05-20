"""Reglas del juego: turnos, movimientos legales, estados terminales y ganador.

El tamaño del tablero (3 o 4) se deriva del propio tablero, por lo que las
reglas funcionan igual para 3x3 y para 4x4. Gana quien complete una línea
entera (fila, columna o diagonal).
"""

from typing import Optional

from .constants import EMPTY, PLAYER_1, PLAYER_2
from .state import Board, GameState, Move, board_size


def switch_player(player: str) -> str:
    """Devuelve el jugador contrario."""
    if player == PLAYER_1:
        return PLAYER_2
    if player == PLAYER_2:
        return PLAYER_1
    raise ValueError(f"Jugador no encontrado: {player!r}")


def is_terminal(state: GameState) -> bool:
    """Indica si el estado es terminal: hay ganador o el tablero está lleno."""
    if state.winner is not None:
        return True
    return all(cell != EMPTY for row in state.board for cell in row)


def get_legal_moves(state: GameState) -> list[Move]:
    """Devuelve las posiciones vacías donde se puede colocar una ficha."""
    size = board_size(state.board)
    return [
        (row, col)
        for row in range(size)
        for col in range(size)
        if state.board[row][col] == EMPTY
    ]


def is_legal_move(state: GameState, move: Move) -> bool:
    """Indica si un movimiento es legal en el estado actual."""
    row, col = move
    size = board_size(state.board)

    if is_terminal(state):
        return False
    if not 0 <= row < size:
        return False
    if not 0 <= col < size:
        return False
    return state.board[row][col] == EMPTY


def _all_lines_coords(size: int) -> list[list[Move]]:
    """Coordenadas de todas las líneas ganadoras: filas, columnas y diagonales."""
    lines: list[list[Move]] = []
    for row in range(size):
        lines.append([(row, col) for col in range(size)])
    for col in range(size):
        lines.append([(row, col) for row in range(size)])
    lines.append([(i, i) for i in range(size)])
    lines.append([(i, size - 1 - i) for i in range(size)])
    return lines


def check_winner(board: Board) -> Optional[str]:
    """Devuelve el símbolo del ganador, o None si no hay ganador."""
    for coords in _all_lines_coords(board_size(board)):
        first = board[coords[0][0]][coords[0][1]]
        if first == EMPTY:
            continue
        if all(board[r][c] == first for r, c in coords):
            return first
    return None


def winning_line(board: Board) -> Optional[list[Move]]:
    """Devuelve las coordenadas de la línea ganadora, o None si no hay.

    Permite a la interfaz resaltar la línea con la que se ganó.
    """
    for coords in _all_lines_coords(board_size(board)):
        first = board[coords[0][0]][coords[0][1]]
        if first == EMPTY:
            continue
        if all(board[r][c] == first for r, c in coords):
            return coords
    return None


def apply_move(state: GameState, move: Move) -> GameState:
    """Aplica un movimiento y devuelve el nuevo estado resultante.

    Raises:
        ValueError: si el movimiento es ilegal.
    """
    if not is_legal_move(state, move):
        raise ValueError(f"Movimiento ilegal: {move}")

    row, col = move
    new_board_rows = [list(board_row) for board_row in state.board]
    new_board_rows[row][col] = state.current_player
    new_board: Board = tuple(tuple(board_row) for board_row in new_board_rows)

    return GameState(
        board=new_board,
        current_player=switch_player(state.current_player),
        winner=check_winner(new_board),
    )


def is_draw(state: GameState) -> bool:
    """Indica si el estado es un empate: sin ganador y sin movimientos legales."""
    if state.winner is not None:
        return False
    return len(get_legal_moves(state)) == 0
