"""Algoritmo Minimax con poda Alpha-Beta.

Adaptado de project/src/game/ai/alpha_beta.py. Misma lógica, con tipos e
imports relativos consistentes.

La poda descarta ramas que no pueden afectar la decisión final, evaluando
menos nodos que Minimax básico para obtener el mismo resultado.
"""

from typing import Optional

from ..core.rules import apply_move, get_legal_moves, is_terminal
from ..core.state import GameState, Move
from .evaluation import evaluate
from .minimax import NodesCounter, decrease_depth


def maximize_alpha_beta(
    state: GameState,
    ai_player: str,
    depth_limit: Optional[int],
    alpha: float,
    beta: float,
    nodes_counter: Optional[NodesCounter],
) -> int:
    """Turno de la IA con poda: busca el mayor puntaje posible."""
    best_score = float("-inf")

    for move in get_legal_moves(state):
        new_state = apply_move(state, move)
        score = alpha_beta(
            new_state, ai_player, decrease_depth(depth_limit), alpha, beta, nodes_counter
        )
        if score > best_score:
            best_score = score
        if best_score > alpha:
            alpha = best_score
        if beta <= alpha:
            break  # Poda: el jugador MIN nunca permitirá llegar a esta rama.

    return int(best_score)


def minimize_alpha_beta(
    state: GameState,
    ai_player: str,
    depth_limit: Optional[int],
    alpha: float,
    beta: float,
    nodes_counter: Optional[NodesCounter],
) -> int:
    """Turno del humano con poda: busca el menor puntaje posible para la IA."""
    best_score = float("inf")

    for move in get_legal_moves(state):
        new_state = apply_move(state, move)
        score = alpha_beta(
            new_state, ai_player, decrease_depth(depth_limit), alpha, beta, nodes_counter
        )
        if score < best_score:
            best_score = score
        if best_score < beta:
            beta = best_score
        if beta <= alpha:
            break  # Poda: el jugador MAX nunca permitirá llegar a esta rama.

    return int(best_score)


def alpha_beta(
    state: GameState,
    ai_player: str,
    depth_limit: Optional[int] = None,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
    nodes_counter: Optional[NodesCounter] = None,
) -> int:
    """Aplica Minimax con poda Alpha-Beta sobre un estado y devuelve su puntaje."""
    if nodes_counter is not None:
        nodes_counter["count"] += 1

    if is_terminal(state):
        return evaluate(state, ai_player)

    if depth_limit is not None and depth_limit == 0:
        return evaluate(state, ai_player)

    if state.current_player == ai_player:
        return maximize_alpha_beta(
            state, ai_player, depth_limit, alpha, beta, nodes_counter
        )
    return minimize_alpha_beta(state, ai_player, depth_limit, alpha, beta, nodes_counter)


def get_best_move_alpha_beta(
    state: GameState,
    ai_player: str,
    depth_limit: Optional[int] = None,
) -> tuple[Optional[Move], int, int]:
    """Obtiene el mejor movimiento para la IA usando Minimax con poda Alpha-Beta.

    Returns:
        Tupla (mejor movimiento, puntaje, nodos evaluados).
    """
    best_move: Optional[Move] = None
    best_score = float("-inf")
    alpha = float("-inf")
    beta = float("inf")
    nodes_counter: NodesCounter = {"count": 0}

    for move in get_legal_moves(state):
        new_state = apply_move(state, move)
        score = alpha_beta(
            new_state, ai_player, decrease_depth(depth_limit), alpha, beta, nodes_counter
        )
        if score > best_score:
            best_score = score
            best_move = move
        if best_score > alpha:
            alpha = best_score

    return best_move, int(best_score), nodes_counter["count"]
