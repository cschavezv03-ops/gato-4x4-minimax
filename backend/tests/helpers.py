"""Utilidades para construir tableros y estados en los tests."""

from app.core.state import Board, GameState


def make_board(rows: list[str]) -> Board:
    """Construye un tablero del núcleo desde filas en texto.

    Ejemplo: make_board(["XX..", "O...", "....", "...."]).
    """
    return tuple(tuple(cell for cell in row) for row in rows)


def make_state(
    rows: list[str], current_player: str, winner: str | None = None
) -> GameState:
    """Construye un GameState desde filas en texto."""
    return GameState(
        board=make_board(rows), current_player=current_player, winner=winner
    )


def board_as_lists(rows: list[str]) -> list[list[str]]:
    """Construye un tablero como listas (formato de la API) desde filas en texto."""
    return [list(row) for row in rows]
