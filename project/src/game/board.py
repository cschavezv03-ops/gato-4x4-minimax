# Se encarga de mostrar el tablero en formato legible
from typing import Sequence

def board_to_string(board):
    """
    Convierte el tablero del juego en un texto para consola.

    Ejemplo de salida:

    0 1 2 3
    0 . . . .
    1 . X . .
    2 . . O .
    3 . . . .
    """

    if not board:
        raise ValueError("No existe tablero para mostrar") #Sirve para verificar cualquier error durante las pruebas
    
    size = len(board)

    lines = []

    header = "   " + "   ".join(str(col) for col in range(size)) #Imprime número de las columnas (encabezado)
    lines.append(header) #Guarda el encabezado en lines

    for row_index, row in enumerate(board): 
        row_text = str(row_index) + "   " + "   ".join(row) #Convierte fila en texto
        lines.append(row_text) #Guarda en lines

    return "\n".join(lines) #se unen todas las lineas

#Prueba para ejecutar solo si el archivo lo está ejecutando directamente, no se usa cuando otro archivo lo importa
if __name__ == "__main__":
    test_board = (
        (".", ".", ".", "."),
        (".", "X", ".", "."),
        (".", ".", "O", "."),
        (".", ".", ".", "."),
    )

    print(board_to_string(test_board))