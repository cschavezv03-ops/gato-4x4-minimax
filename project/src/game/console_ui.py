#Se encarga de hablar con el usuario por consola mediante inputs y outputs
from .board import board_to_string

def show_welcome():
    """
    Muestra en consola un encabezado sobre el juego.
    """
    print("================================")
    print("  GATO 4x4 - HUMAN VS HUMAN")
    print("================================")

def show_ai_welcome(ai_player, human_player, depth_limit):
    """
    Muestra en consola un encabezado para el modo humano contra IA.
    param
    ai_player: str - Jugador que representa a la IA
    human_player: str - Jugador que representa al humano
    depth_limit: int | None - Profundidad maxima usada por Minimax
    return: None
    """
    print("================================")
    print("  GATO 4x4 - IA VS HUMANO")
    print("================================")
    print(f"IA: {ai_player}")
    print(f"Humano: {human_player}")

    if depth_limit is None:
        print("Minimax: busqueda completa")
    else:
        print(f"Minimax: profundidad {depth_limit}")

def show_board(state):
    """
    Muestra el tablero 4x4 en donde se va a jugar.
    """
    print()
    print()
    print("Tablero:")
    print(board_to_string(state.board))
    print()

def ask_move(current_player):
    """
    Pregunta la posición (row, col) en donde se pondrá X o O.

    Param:
    current_player (String): Jugador al que le toca

    Returns:
    int, int: valores de row y col
    """
    print(f"Turno del jugador {current_player}")

    try:
        row = int(input("Fila: "))
        col = int(input("Columna: "))
        return row, col
    except ValueError: #Si no son valores enteros
        return -1, -1
    
def show_invalid_move():
    """
    Impresión cuando se presenta un movimiento inválido, fuera del tablero 4x4.
    """
    print("Movimiento inválido, intentalo nuevamente")

def show_ai_turn(ai_player):
    """
    Muestra en consola que la IA esta calculando su movimiento.
    param
    ai_player: str - Jugador que representa a la IA
    return: None
    """
    print(f"Turno de la IA ({ai_player})...")

def show_ai_move(move, score, nodes):
    """
    Muestra en consola el movimiento elegido por la IA.
    param
    move: Tuple[int, int] - Movimiento elegido por la IA
    score: int - Puntaje obtenido por Minimax
    nodes: int - Cantidad de nodos evaluados
    return: None
    """
    row, col = move

    print(f"IA jugo en fila {row}, columna {col}")
    print(f"Puntaje: {score}")
    print(f"Nodos evaluados: {nodes}")

def show_winner(winner):
    """
    Impresión del jugador ganador.

    Param:
    winner: jugador ganador
    """
    print(f"Ganó el jugador {winner}")

def show_draw():
    """
    Impresión en caso de empate.
    """
    print("El juego terminó en empate")

def show_goodbye():
    """
    Impresión indicando fin de la partida actual.
    """
    print("Fin de la partida")
