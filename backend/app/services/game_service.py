"""Servicio de juego: orquesta núcleo e IA y traduce al contrato de la API.

Es la única capa que conoce a la vez el núcleo (`core`), la IA (`ai`) y los
modelos de la API (`schemas`). El núcleo y la IA se mantienen puros.
"""

import time
from random import choice

from ..ai.alpha_beta import get_best_move_alpha_beta
from ..ai.minimax import get_best_move
from ..core.constants import DEFAULT_BOARD_SIZE
from ..core.rules import (
    apply_move,
    check_winner,
    get_legal_moves,
    is_draw,
    is_terminal,
    winning_line,
)
from ..core.state import Board, GameState, Move, board_size, create_initial_state
from ..schemas.game import (
    AiMetrics,
    AiMoveResponse,
    Algorithm,
    CompareResponse,
    GameStateResponse,
)


class IllegalMoveError(Exception):
    """Se lanza cuando una jugada o una petición no es válida según las reglas."""


# --- Conversiones entre el contrato de la API y el núcleo ---------------------


def _to_board(rows: list[list[str]]) -> Board:
    """Convierte el tablero de la API (listas) al tablero del núcleo (tuplas)."""
    return tuple(tuple(row) for row in rows)


def _rebuild_state(rows: list[list[str]], current_player: str) -> GameState:
    """Reconstruye un GameState desde una petición, calculando el ganador."""
    board = _to_board(rows)
    return GameState(
        board=board, current_player=current_player, winner=check_winner(board)
    )


def _build_state_response(state: GameState) -> GameStateResponse:
    """Traduce un GameState del núcleo al modelo de respuesta de la API."""
    return GameStateResponse(
        board=[list(row) for row in state.board],
        current_player=state.current_player,
        winner=state.winner,
        is_draw=is_draw(state),
        is_terminal=is_terminal(state),
        legal_moves=get_legal_moves(state),
        winning_line=winning_line(state.board),
    )


# --- Operaciones del juego ----------------------------------------------------


def new_game(size: int = DEFAULT_BOARD_SIZE) -> GameStateResponse:
    """Devuelve el estado inicial de una partida nueva de tamaño `size`."""
    return _build_state_response(create_initial_state(size))


def apply_player_move(
    rows: list[list[str]], current_player: str, move: Move
) -> GameStateResponse:
    """Aplica la jugada de un jugador y devuelve el nuevo estado.

    Raises:
        IllegalMoveError: si la jugada no es legal.
    """
    state = _rebuild_state(rows, current_player)
    try:
        new_state = apply_move(state, tuple(move))
    except ValueError as exc:
        raise IllegalMoveError(str(exc)) from exc
    return _build_state_response(new_state)


def _run_algorithm(
    state: GameState, ai_player: str, algorithm: Algorithm, depth_limit: int
) -> AiMetrics:
    """Ejecuta un algoritmo de IA sobre el estado y mide su rendimiento.

    Si el tablero está vacío devuelve una jugada aleatoria: la búsqueda completa
    desde el tablero vacío es intratable (igual criterio que el proyecto original).
    """
    legal_moves = get_legal_moves(state)
    total_cells = board_size(state.board) ** 2

    if len(legal_moves) == total_cells:
        return AiMetrics(
            algorithm=algorithm,
            move=choice(legal_moves),
            score=0,
            nodes_evaluated=0,
            elapsed_ms=0.0,
            is_random=True,
        )

    start = time.perf_counter()
    if algorithm == "minimax":
        move, score, nodes = get_best_move(state, ai_player, depth_limit)
    else:
        move, score, nodes = get_best_move_alpha_beta(state, ai_player, depth_limit)
    elapsed_ms = round((time.perf_counter() - start) * 1000, 3)

    if move is None:  # Defensivo: no debería ocurrir con un estado no terminal.
        raise IllegalMoveError("La IA no encontró ningún movimiento")

    return AiMetrics(
        algorithm=algorithm,
        move=move,
        score=score,
        nodes_evaluated=nodes,
        elapsed_ms=elapsed_ms,
    )


def _validate_ai_turn(state: GameState, ai_player: str) -> None:
    """Verifica que sea el turno de la IA y que la partida siga en curso."""
    if is_terminal(state):
        raise IllegalMoveError("La partida ya terminó")
    if state.current_player != ai_player:
        raise IllegalMoveError("No es el turno de la IA")


def compute_ai_move(
    rows: list[list[str]],
    current_player: str,
    ai_player: str,
    algorithm: Algorithm,
    depth_limit: int,
) -> AiMoveResponse:
    """Calcula y aplica la jugada de la IA.

    Raises:
        IllegalMoveError: si no es el turno de la IA o la partida ya terminó.
    """
    state = _rebuild_state(rows, current_player)
    _validate_ai_turn(state, ai_player)

    metrics = _run_algorithm(state, ai_player, algorithm, depth_limit)
    new_state = apply_move(state, metrics.move)
    return AiMoveResponse(metrics=metrics, state=_build_state_response(new_state))


def compare_algorithms(
    rows: list[list[str]],
    current_player: str,
    ai_player: str,
    depth_limit: int,
) -> CompareResponse:
    """Ejecuta Minimax y Alpha-Beta sobre el mismo estado y compara sus métricas.

    Ambos algoritmos eligen el mismo movimiento óptimo; se aplica para avanzar
    la partida. La diferencia está en la cantidad de nodos evaluados.

    Raises:
        IllegalMoveError: si no es el turno de la IA o la partida ya terminó.
    """
    state = _rebuild_state(rows, current_player)
    _validate_ai_turn(state, ai_player)

    minimax_metrics = _run_algorithm(state, ai_player, "minimax", depth_limit)
    alpha_beta_metrics = _run_algorithm(state, ai_player, "alpha_beta", depth_limit)

    new_state = apply_move(state, alpha_beta_metrics.move)
    nodes_saved = minimax_metrics.nodes_evaluated - alpha_beta_metrics.nodes_evaluated

    return CompareResponse(
        minimax=minimax_metrics,
        alpha_beta=alpha_beta_metrics,
        nodes_saved=nodes_saved,
        state=_build_state_response(new_state),
    )
