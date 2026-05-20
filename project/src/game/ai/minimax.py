from game.rules import is_terminal, get_legal_moves, apply_move
from game.ai.evaluation import evaluate


# Funciones auxiliares para minimax

def maximize(state, ai_player, depth_limit, nodes_counter):
    """
    Busca el mejor puntaje posible para la IA.
    param
    state: GameState - Estado actual del juego
    ai_player: str - "X"
    depth_limit: int | None - Profundidad maxima de busqueda
    nodes_counter: dict | None - Diccionario para contar cuantos nodos fueron evaluados
    return: int - Mayor puntaje encontrado para la IA
    """
    best_score = float("-inf") # Peor valor posible

    for move in get_legal_moves(state): # Prueba cada jugada
        new_state = apply_move(state, move)
        new_depth_limit = decrease_depth(depth_limit)

        score = minimax(new_state, ai_player, new_depth_limit, nodes_counter) # Resultado futuro de la jugada que se prueba

        if score > best_score:
            best_score = score # Va guardando el mejor resultado

    return best_score

def minimize(state, ai_player, depth_limit, nodes_counter):
    """
    Busca el peor puntaje posible para la IA, asumiendo que el oponente juega bien.
    param
    state: GameState - Estado actual del juego
    ai_player: str - "X"
    depth_limit: int | None - Profundidad máxima de busqueda
    nodes_counter: dict | None - Diccionario para contar cuantos nodos fueron evaluados
    return: int - Menor puntaje encontrado para la IA
    """
    best_score = float("inf") # Mayor valor posible

    for move in get_legal_moves(state): # Prueba cada jugada
        new_state = apply_move(state, move)
        new_depth_limit = decrease_depth(depth_limit)

        score = minimax(new_state, ai_player, new_depth_limit, nodes_counter) # Resultado futuro de la jugada que se prueba

        if score < best_score:
            best_score = score # Va guardando el peor resultado

    return best_score

# Manejo de límite de profundidad

def decrease_depth(depth_limit):
    """
    Reduce la profundidad disponible si existe un límite.
    param
    depth_limit: int | None - Profundidad máxima restante
    return: int | None - Nueva profundidad máxima restante
    """
    if depth_limit is None:
        return None # En caso de que no se halla definido un límite de profundidad

    return depth_limit - 1

# Algoritmo de Minimax

def minimax(state, ai_player, depth_limit=None, nodes_counter=None):
    """
    Aplica el algoritmo Minimax sobre un estado del juego.
    param
    state: GameState - Estado actual del juego
    ai_player: str - "X"
    depth_limit: int | None - Profundidad maxima de busqueda. Si es None, busca hasta estados terminales
    nodes_counter: dict | None - Diccionario para contar cuantos nodos fueron evaluados
    return: int - Puntaje del estado segun la mejor jugada posible
    """
    if nodes_counter is not None:
        nodes_counter["count"] += 1 # Cuenta nodos evaluados, útil para posterior comparación con Poda Alpha-Beta

    if is_terminal(state):
        return evaluate(state, ai_player) # Si el juego termina, tiene que evaluar. No hay más escenarios por simular

    if depth_limit is not None and depth_limit == 0: # Evalúa con heurística si es que se definió un límite de profundidad y se alcanzó el máximo de profundidad
        return evaluate(state, ai_player)

    if state.current_player == ai_player:
        return maximize(state, ai_player, depth_limit, nodes_counter) # Turno de la IA: debe maximizar

    return minimize(state, ai_player, depth_limit, nodes_counter) # Turno del humano: debe minimizar


def get_best_move(state, ai_player, depth_limit=None):
    """
    Obtiene el mejor movimiento para la IA usando Minimax.
    param
    state: GameState - Estado actual del juego
    ai_player: str - "X"
    depth_limit: int | None - Profundidad maxima de busqueda. Si es None, busca hasta estados terminales
    return: Tuple[Tuple[int, int], int, int] - Mejor movimiento, puntaje obtenido y nodos evaluados
    """
    best_move = None
    best_score = float("-inf")
    nodes_counter = {"count": 0}

    for move in get_legal_moves(state): # Prueba todos los movimientos posibles desde el estado actual 
        new_state = apply_move(state, move)
        new_depth_limit = decrease_depth(depth_limit)

        score = minimax(new_state, ai_player, new_depth_limit, nodes_counter) # Simula turnos futuros

        if score > best_score:
            best_score = score
            best_move = move

    return best_move, best_score, nodes_counter["count"]