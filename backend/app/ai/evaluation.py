"""Función de utilidad (estados terminales) y heurística (estados no terminales).

El tamaño del tablero se deriva del propio tablero: la evaluación funciona
igual para 3x3 y para 4x4.
"""

from ..core.constants import DRAW_SCORE, EMPTY, LOSE_SCORE, WIN_SCORE
from ..core.rules import is_draw, is_terminal
from ..core.state import Board, GameState, board_size

Line = tuple[str, ...]


def get_lines(board: Board) -> list[Line]:
    """Devuelve todas las líneas posibles de victoria: filas, columnas y diagonales."""
    size = board_size(board)
    lines: list[Line] = []

    for row in range(size):
        lines.append(board[row])

    for col in range(size):
        lines.append(tuple(board[row][col] for row in range(size)))

    lines.append(tuple(board[i][i] for i in range(size)))
    lines.append(tuple(board[i][size - 1 - i] for i in range(size)))

    return lines


def get_opponent(state: GameState, ai_player: str) -> str:
    """Determina el símbolo del jugador contrario a la IA."""
    for row in state.board:
        for cell in row:
            if cell != EMPTY and cell != ai_player:
                return cell

    if state.current_player != ai_player:
        return state.current_player

    raise ValueError("No se pudo determinar el oponente")


def evaluate_line(line: Line, ai_player: str, opponent: str) -> int:
    """Evalúa una sola línea según su utilidad para la IA.

    Una línea mixta (X y O) no sirve a nadie. Una línea con solo fichas de la IA
    es valiosa; con solo fichas del oponente, es peligrosa. El valor crece
    exponencialmente con la cantidad de fichas.
    """
    ai_count = line.count(ai_player)
    opponent_count = line.count(opponent)

    if ai_count > 0 and opponent_count > 0:
        return 0
    if ai_count > 0:
        return 10**ai_count
    if opponent_count > 0:
        return -(10**opponent_count)
    return 0


def heuristic(state: GameState, ai_player: str) -> int:
    """Evalúa un estado no terminal sumando la utilidad de todas sus líneas."""
    opponent = get_opponent(state, ai_player)
    return sum(
        evaluate_line(line, ai_player, opponent) for line in get_lines(state.board)
    )


def utility(state: GameState, ai_player: str) -> int:
    """Evalúa un estado terminal: victoria, derrota o empate.

    Raises:
        ValueError: si el estado no es terminal.
    """
    if state.winner == ai_player:
        return WIN_SCORE
    if state.winner is not None:
        return LOSE_SCORE
    if is_draw(state):
        return DRAW_SCORE
    raise ValueError("utility solo debe usarse con estados terminales")


def evaluate(state: GameState, ai_player: str) -> int:
    """Evalúa cualquier estado: utility si es terminal, heuristic si no lo es."""
    if is_terminal(state):
        return utility(state, ai_player)
    return heuristic(state, ai_player)
