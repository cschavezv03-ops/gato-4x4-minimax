#Se encarga de hablar con el usuario por consola mediante inputs y outputs
from .board import board_to_string

def show_welcome():
    """
    Muestra en consola un encabezado sobre el juego.
    """
    print("================================")
    print("  GATO 4x4 - HUMAN VS HUMAN")
    print("================================")

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