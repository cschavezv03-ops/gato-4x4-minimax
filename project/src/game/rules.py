from .state import GameState
from .constants import BOARD_SIZE, EMPTY, PLAYER_1, PLAYER_2


def switch_player(player):

    """
    Cambia el jugador actual al siguiente jugador.
    param
    player: str - El jugador actual (PLAYER_1 o PLAYER_2)
    return: str - El siguiente jugador
    """

    if player == PLAYER_1:
        return PLAYER_2
    
    if player == PLAYER_2:
        return PLAYER_1
    
    raise ValueError("Jugador no encontrado")

def is_terminal(state):

    """
    Verifica si el estado del juego es terminal (es decir, si hay un ganador o si el tablero está lleno).
    param
    state: GameState - El estado actual del juego
    return: bool - True si el estado es terminal, False de lo contrario
    """
    
    if state.winner is not None:
        return True
    
    board_is_full = all(cell != EMPTY 
                        for row in state.board 
                        for cell in row
                    )
    
    return board_is_full


def get_legal_moves(state):

    """
    Obtiene una lista de movimientos legales para el estado actual del juego.
    param
    state: GameState - El estado actual del juego
    return: List[Tuple[int, int]] - Una lista de tuplas que representan las posiciones legales para colocar una ficha
    """

    legal_moves = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if state.board[row][col] == EMPTY:
                legal_moves.append((row, col))
    
    return legal_moves

def is_legal_move(state, move):
    """
    Verifica si un movimiento es legal en el estado actual del juego.
    param
    state: GameState - El estado actual del juego
    move: Tuple[int, int] - La posición del movimiento a verificar
    return: bool - True si el movimiento es legal, False de lo contrario
    """

    row, col = move

    if is_terminal(state):
        return False
    
    if row < 0 or row >= BOARD_SIZE:
        return False
    
    if col < 0 or col >= BOARD_SIZE:
        return False
    
    return state.board[row][col] == EMPTY

def check_winner(board):
    lines = []

    for row in range(BOARD_SIZE):
        line = []

        for col in range(BOARD_SIZE):
            line.append(board[row][col])

        lines.append(line)

    for col in range(BOARD_SIZE):
        line = []

        for row in range(BOARD_SIZE):
            line.append(board[row][col])

        lines.append(line)
    
    diagonal = []

    for i in range(BOARD_SIZE):
        diagonal.append(board[i][BOARD_SIZE - 1 - i])

    lines.append(diagonal)

    for line in lines:
        first_cell = line[0]

        if first_cell == EMPTY:
            continue

        if all(cell == first_cell for cell in line):
            return first_cell
        
    return None




def apply_move(state, move):

    if not is_legal_move(state, move):
        raise ValueError("Movimiento ilegal")
    
    row, col = move

    new_board_as_list = [list(row) for row in state.board]
    new_board_as_list[row][col] = state.current_player

    new_board = tuple(tuple(row) 
                      for row in new_board_as_list
                      )
    
    winner = check_winner(new_board)

    return GameState(
        board=new_board,
        current_player=switch_player(state.current_player),
        winner=winner
    )

def is_draw(state):
    if state.winner is not None:
        return False
    
    return len(get_legal_moves(state)) == 0


