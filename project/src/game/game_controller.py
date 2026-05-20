#Es el archivo que controla toda la partida
from .state import create_initial_state
from .rules import apply_move, is_legal_move, is_terminal, is_draw, get_legal_moves
from .constants import PLAYER_1, PLAYER_2, DEPTH_LIMIT
from .ai.minimax import get_best_move
from .ai.alpha_beta import get_best_move_alpha_beta
from .console_ui import (
    show_welcome,
    show_ai_welcome,
    show_board,
    ask_move,
    show_invalid_move,
    show_ai_turn,
    show_ai_move,
    show_winner,
    show_draw,
    show_goodbye,
)
from random import choice


def run_human_vs_human():
    """
    Función que llama a las demás funciones para controlar la partida
    y mostrar respectivos outputs.
    """
    #Crear una partida nueva con tablero vacío, empezando con X (próximamente IA)
    state = create_initial_state() #Objeto tipo GameState que representa el estado actual del juego

    show_welcome()

    while not is_terminal(state): #Mientras no se llegue a un estado terminal
        show_board(state)

        move = ask_move(state.current_player)
    
        if not is_legal_move(state, move):
            show_invalid_move()
            continue
        
        #Actualiza la partida y guarda el nuevo estado
        state = apply_move(state, move) #apply_move crea un nuevo objeto tipo GameState con tablero actualizado, turno cambiado y ganador actualizado (en caso de existir)

    show_board(state)

    if state.winner is not None:
        show_winner(state.winner)
    elif is_draw(state):
        show_draw()

    show_goodbye()

def run_ai_vs_human(depth_limit=DEPTH_LIMIT):
    """
    Funcion que controla una partida entre la IA y un jugador humano.
    param
    depth_limit: int | None - Profundidad maxima usada por Minimax. Si es None, busca hasta estados terminales
    return: None
    """
    state = create_initial_state()
    ai_has_played = False
    show_ai_welcome(PLAYER_1, PLAYER_2, depth_limit)

    while not is_terminal(state):
        show_board(state)

        if state.current_player == PLAYER_1:
            show_ai_turn(PLAYER_1)

            if not ai_has_played:
                move = choice(get_legal_moves(state))
                print(f"IA jugo aleatoriamente en {move}")
                state = apply_move(state, move)
                ai_has_played = True
                continue

            move, score, nodes = get_best_move(state, PLAYER_1, depth_limit)

            if move is None:
                break

            show_ai_move(move, score, nodes)
            state = apply_move(state, move)
            continue

        move = ask_move(state.current_player)

        if not is_legal_move(state, move):
            show_invalid_move()
            continue

        state = apply_move(state, move)

    show_board(state)

    if state.winner is not None:
        show_winner(state.winner)
    elif is_draw(state):
        show_draw()

    show_goodbye()

def run_ai_vs_human_alpha_beta(depth_limit=DEPTH_LIMIT):
    """
    Funcion que controla una partida entre la IA y un jugador humano.
    param
    depth_limit: int | None - Profundidad maxima usada por Alpha Beta. Si es None, busca hasta estados terminales
    return: None
    """
    state = create_initial_state()
    ai_has_played = False
    show_ai_welcome(PLAYER_1, PLAYER_2, depth_limit)

    while not is_terminal(state):
        show_board(state)

        if state.current_player == PLAYER_1:
            show_ai_turn(PLAYER_1)

            if not ai_has_played:
                move = choice(get_legal_moves(state))
                print(f"IA jugo aleatoriamente en {move}")
                state = apply_move(state, move)
                ai_has_played = True
                continue

            move, score, nodes = get_best_move_alpha_beta(state, PLAYER_1, depth_limit)

            if move is None:
                break

            show_ai_move(move, score, nodes)
            state = apply_move(state, move)
            continue

        move = ask_move(state.current_player)

        if not is_legal_move(state, move):
            show_invalid_move()
            continue

        state = apply_move(state, move)

    show_board(state)

    if state.winner is not None:
        show_winner(state.winner)
    elif is_draw(state):
        show_draw()

    show_goodbye()

def run_ai_vs_human_comparison(depth_limit=DEPTH_LIMIT):
    """
    Funcion que controla una partida entre la IA y un jugador humano comparando nodos evaluados.
    param
    depth_limit: int | None - Profundidad maxima usada por Minimax y Alpha-Beta
    return: None
    """
    from .console_ui import show_comparison_welcome, show_node_comparison

    state = create_initial_state()
    ai_has_played = False
    show_comparison_welcome(PLAYER_1, PLAYER_2, depth_limit)

    while not is_terminal(state):
        show_board(state)

        if state.current_player == PLAYER_1:
            show_ai_turn(PLAYER_1)

            if not ai_has_played:
                move = choice(get_legal_moves(state))
                print(f"IA jugo aleatoriamente en {move}")
                state = apply_move(state, move)
                ai_has_played = True
                continue

            minimax_move, minimax_score, minimax_nodes = get_best_move(state, PLAYER_1, depth_limit)
            alpha_beta_move, alpha_beta_score, alpha_beta_nodes = get_best_move_alpha_beta(state, PLAYER_1, depth_limit)

            if alpha_beta_move is None:
                break

            show_node_comparison(
                minimax_move,
                minimax_score,
                minimax_nodes,
                alpha_beta_move,
                alpha_beta_score,
                alpha_beta_nodes
            )

            state = apply_move(state, alpha_beta_move)
            continue

        move = ask_move(state.current_player)

        if not is_legal_move(state, move):
            show_invalid_move()
            continue

        state = apply_move(state, move)

    show_board(state)

    if state.winner is not None:
        show_winner(state.winner)
    elif is_draw(state):
        show_draw()

    show_goodbye()

def run_main_menu():
    """
    Muestra un menu principal para escoger el modo de juego.
    return: None
    """
    from .console_ui import show_main_menu, ask_game_mode, show_invalid_option

    while True:
        show_main_menu()
        option = ask_game_mode()

        if option == "1":
            run_human_vs_human()
            return

        if option == "2":
            run_ai_vs_human()
            return

        if option == "3":
            run_ai_vs_human_alpha_beta()
            return

        if option == "4":
            run_ai_vs_human_comparison()
            return

        if option == "5":
            show_goodbye()
            return

        show_invalid_option()
