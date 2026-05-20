"""Algoritmo Minimax básico.

Adaptado de project/src/game/ai/minimax.py. Misma lógica, con tipos e imports
relativos consistentes.

La IA es el jugador MAX (maximiza su puntaje); el humano es MIN (lo minimiza).
"""

from typing import Optional

from ..core.rules import apply_move, get_legal_moves, is_terminal
from ..core.state import GameState, Move
from .evaluation import evaluate

NodesCounter = dict[str, int]


def decrease_depth(depth_limit: Optional[int]) -> Optional[int]:
    """Reduce la profundidad restante si existe un límite."""
    if depth_limit is None:
        return None
    return depth_limit - 1


def maximize(
    state: GameState,
    ai_player: str,
    depth_limit: Optional[int],
    nodes_counter: Optional[NodesCounter],
) -> int:
    """Turno de la IA: busca el mayor puntaje posible."""
    best_score = float("-inf")

    for move in get_legal_moves(state):
        new_state = apply_move(state, move)
        score = minimax(new_state, ai_player, decrease_depth(depth_limit), nodes_counter)
        if score > best_score:
            best_score = score

    return int(best_score)


def minimize(
    state: GameState,
    ai_player: str,
    depth_limit: Optional[int],
    nodes_counter: Optional[NodesCounter],
) -> int:
    """Turno del humano: busca el menor puntaje posible para la IA."""
    best_score = float("inf")

    for move in get_legal_moves(state):
        new_state = apply_move(state, move)
        score = minimax(new_state, ai_player, decrease_depth(depth_limit), nodes_counter)
        if score < best_score:
            best_score = score

    return int(best_score)


def minimax(
    state: GameState,
    ai_player: str,
    depth_limit: Optional[int] = None,
    nodes_counter: Optional[NodesCounter] = None,
) -> int:
    """Aplica Minimax sobre un estado y devuelve su puntaje.

    Args:
        state: Estado a evaluar.
        ai_player: Símbolo de la IA ("X" u "O").
        depth_limit: Profundidad máxima; None busca hasta estados terminales.
        nodes_counter: Diccionario opcional para contar nodos evaluados.
    """
    if nodes_counter is not None:
        nodes_counter["count"] += 1

    if is_terminal(state):
        return evaluate(state, ai_player)

    if depth_limit is not None and depth_limit == 0:
        return evaluate(state, ai_player)

    if state.current_player == ai_player:
        return maximize(state, ai_player, depth_limit, nodes_counter)
    return minimize(state, ai_player, depth_limit, nodes_counter)


def get_best_move(
    state: GameState,
    ai_player: str,
    depth_limit: Optional[int] = None,
) -> tuple[Optional[Move], int, int]:
    """Obtiene el mejor movimiento para la IA usando Minimax.

    Returns:
        Tupla (mejor movimiento, puntaje, nodos evaluados).
    """
    best_move: Optional[Move] = None
    best_score = float("-inf")
    nodes_counter: NodesCounter = {"count": 0}

    for move in get_legal_moves(state):
        new_state = apply_move(state, move)
        score = minimax(new_state, ai_player, decrease_depth(depth_limit), nodes_counter)
        if score > best_score:
            best_score = score
            best_move = move

    return best_move, int(best_score), nodes_counter["count"]
