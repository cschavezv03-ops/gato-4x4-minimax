#Es el archivo que controla toda la partida
from .state import create_initial_state
from .rules import apply_move, is_legal_move, is_terminal, is_draw
from .console_ui import show_welcome, show_board, ask_move, show_invalid_move, show_winner, show_draw, show_goodbye

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