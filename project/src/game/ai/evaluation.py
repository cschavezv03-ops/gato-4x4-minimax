from game.constants import BOARD_SIZE, EMPTY
from game.rules import is_terminal, is_draw


WIN_SCORE = 100000
LOSE_SCORE = -100000
DRAW_SCORE = 0

# Funciones auxiliares para heurística
def get_lines(board):
    """
    Devuelve todas las lineas posibles de victoria:
    filas, columnas y diagonales.
    param board: Tuple - Tablero actual del juego
    return: list - lista con todas las lineas (tuplas) posibles de victoria 
            (horizontal, vertical, diagonal principal y secundaria)
    """
    lines = []

    for row in range(BOARD_SIZE):
        lines.append(board[row])

    for col in range(BOARD_SIZE):
        column = []
        for row in range(BOARD_SIZE):
            column.append(board[row][col])
        lines.append(tuple(column))

    diagonal_1 = []
    for i in range(BOARD_SIZE):
        diagonal_1.append(board[i][i])
    lines.append(tuple(diagonal_1))

    diagonal_2 = []
    for i in range(BOARD_SIZE):
        diagonal_2.append(board[i][BOARD_SIZE - 1 - i])
    lines.append(tuple(diagonal_2))

    return lines

def get_opponent(state, ai_player):
    """
    Obtiene el jugador contrario a la IA.
    param
    state: GameState - Estado no terminal del juego
    ai_player: str - "X"
    return: str - jugador contrario "O"
    """
    for row in state.board:
        for cell in row:
            if cell != EMPTY and cell != ai_player:
                return cell

    if state.current_player != ai_player:
        return state.current_player

    raise ValueError("No se pudo determinar el oponente")

def evaluate_line(line, ai_player, opponent):
    """
    Evalua una sola fila, columna o diagonal.
    param
    line: tuple - cualquier línea (horizontal, vertical, diagonal principal y secundaria)
    ai_player: str - "X"
    opponent: str - "O"
    return: el valor de qué tan útil es la línea para la IA
    """
    ai_count = line.count(ai_player) # Cuenta el número de veces que aparece "X" en la línea
    opponent_count = line.count(opponent) # Cuenta el número de veces que aparece "O" en la línea

    
    if ai_count > 0 and opponent_count > 0: 
        return 0 # Una línea donde aparezca "X" y "O" al menos una vez, es inútil para ambos

    if ai_count > 0: 
        return 10 ** ai_count # Una línea donde solo aparece "X" es valiosa para la IA

    if opponent_count > 0: 
        return -(10 ** opponent_count) # Una línea donde solo aparece "O" es peligrosa para la IA

    return 0 # Si la línea es del tipo "." "." "." "."

# Heurística

def heuristic(state, ai_player):
    """
    Evalua un estado no terminal.
    param
    state: GameState - Estado no terminal del juego
    ai_player: str - "X"
    return: el valor que tendrá el estado según 
            que tan útiles son las líneas dentro de este
    """
    score = 0
    opponent = get_opponent(state, ai_player)

    for line in get_lines(state.board):
        score += evaluate_line(line, ai_player, opponent)

    return score

# Función de utilidad

def utility(state, ai_player):
    """
    Evalua estados terminales.
    param
    state: GameState - Estado terminal del juego
    ai_player: str - "X"
    return:
    WIN_SCORE: si gana la IA
    LOSE_SCORE: si gana el oponente
    DRAW_SCORE: si hay empate
    """
    if state.winner == ai_player:
        return WIN_SCORE

    if state.winner is not None:
        return LOSE_SCORE

    if is_draw(state):
        return DRAW_SCORE

    raise ValueError("utility solo debe usarse con estados terminales")


def evaluate(state, ai_player):
    """
    Evalua cualquier estado del juego. Si es terminal, utiliza la función utility, si no, utiliza heuristic
    param
    state: GameState - Cualquier estado del juego
    ai_player: str - "X"
    return: valor de utility o heuristic según state y ai_player
    """
    if is_terminal(state):
        return utility(state, ai_player)

    return heuristic(state, ai_player)