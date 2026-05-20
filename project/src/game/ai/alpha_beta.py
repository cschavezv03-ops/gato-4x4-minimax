from game.rules import is_terminal, get_legal_moves, apply_move
from game.ai.evaluation import evaluate
from game.ai.minimax import decrease_depth

# Funciones auxiliares para Alpha-Beta

def maximize_alpha_beta(state, ai_player, depth_limit, alpha, beta, nodes_counter):
    """
    Busca el mejor puntaje posible para la IA usando poda Alpha-Beta.
    param
    state: GameState - Estado actual del juego
    ai_player: str - "X"
    depth_limit: int | None - Profundidad maxima de busqueda
    alpha: float - Mejor valor encontrado hasta ahora para MAX
    beta: float - Mejor valor encontrado hasta ahora para MIN
    nodes_counter: dict | None - Diccionario para contar cuantos nodos fueron evaluados
    return: int - Mayor puntaje encontrado para la IA
    """
    best_score = float("-inf")

    for move in get_legal_moves(state):
        new_state = apply_move(state, move)
        new_depth_limit = decrease_depth(depth_limit)

        score = alpha_beta(
            new_state,
            ai_player,
            new_depth_limit,
            alpha,
            beta,
            nodes_counter
        )

        if score > best_score:
            best_score = score

        if best_score > alpha:
            alpha = best_score

        if beta <= alpha:
            break

    return best_score


def minimize_alpha_beta(state, ai_player, depth_limit, alpha, beta, nodes_counter):
    """
    Busca el peor puntaje posible para la IA usando poda Alpha-Beta.
    param
    state: GameState - Estado actual del juego
    ai_player: str - "X"
    depth_limit: int | None - Profundidad maxima de busqueda
    alpha: float - Mejor valor encontrado hasta ahora para MAX
    beta: float - Mejor valor encontrado hasta ahora para MIN
    nodes_counter: dict | None - Diccionario para contar cuantos nodos fueron evaluados
    return: int - Menor puntaje encontrado para la IA
    """
    best_score = float("inf")

    for move in get_legal_moves(state):
        new_state = apply_move(state, move)
        new_depth_limit = decrease_depth(depth_limit)

        score = alpha_beta(
            new_state,
            ai_player,
            new_depth_limit,
            alpha,
            beta,
            nodes_counter
        )

        if score < best_score:
            best_score = score

        if best_score < beta:
            beta = best_score

        if beta <= alpha:
            break

    return best_score

# Algoritmo Alpha-Beta

def alpha_beta(
    state,
    ai_player,
    depth_limit=None,
    alpha=float("-inf"),
    beta=float("inf"),
    nodes_counter=None
):
    """
    Aplica el algoritmo Minimax con poda Alpha-Beta sobre un estado del juego.
    param
    state: GameState - Estado actual del juego
    ai_player: str - "X"
    depth_limit: int | None - Profundidad maxima de busqueda. Si es None, busca hasta estados terminales
    alpha: float - Mejor valor encontrado hasta ahora para MAX
    beta: float - Mejor valor encontrado hasta ahora para MIN
    nodes_counter: dict | None - Diccionario para contar cuantos nodos fueron evaluados
    return: int - Puntaje del estado segun la mejor jugada posible
    """
    if nodes_counter is not None:
        nodes_counter["count"] += 1

    if is_terminal(state):
        return evaluate(state, ai_player)

    if depth_limit is not None and depth_limit == 0:
        return evaluate(state, ai_player)

    if state.current_player == ai_player:
        return maximize_alpha_beta(
            state,
            ai_player,
            depth_limit,
            alpha,
            beta,
            nodes_counter
        )

    return minimize_alpha_beta(
        state,
        ai_player,
        depth_limit,
        alpha,
        beta,
        nodes_counter
    )


def get_best_move_alpha_beta(state, ai_player, depth_limit=None):
    """
    Obtiene el mejor movimiento para la IA usando Minimax con poda Alpha-Beta.
    param
    state: GameState - Estado actual del juego
    ai_player: str - "X"
    depth_limit: int | None - Profundidad maxima de busqueda. Si es None, busca hasta estados terminales
    return: Tuple[Tuple[int, int], int, int] - Mejor movimiento, puntaje obtenido y nodos evaluados
    """
    best_move = None
    best_score = float("-inf")
    alpha = float("-inf")
    beta = float("inf")
    nodes_counter = {"count": 0}

    for move in get_legal_moves(state):
        new_state = apply_move(state, move)
        new_depth_limit = decrease_depth(depth_limit)

        score = alpha_beta(
            new_state,
            ai_player,
            new_depth_limit,
            alpha,
            beta,
            nodes_counter
        )

        if score > best_score:
            best_score = score
            best_move = move

        if best_score > alpha:
            alpha = best_score

    return best_move, best_score, nodes_counter["count"]