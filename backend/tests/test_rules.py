"""Tests del núcleo del juego: estado y reglas."""

import pytest

from app.core.constants import DEFAULT_BOARD_SIZE, EMPTY, PLAYER_1, PLAYER_2
from app.core.rules import (
    apply_move,
    check_winner,
    get_legal_moves,
    is_draw,
    is_legal_move,
    is_terminal,
    switch_player,
    winning_line,
)
from app.core.state import create_initial_state
from tests.helpers import make_board, make_state


class TestInitialState:
    def test_initial_board_is_empty(self):
        state = create_initial_state()
        assert all(cell == EMPTY for row in state.board for cell in row)

    def test_initial_player_is_x(self):
        assert create_initial_state().current_player == PLAYER_1

    def test_initial_state_has_no_winner(self):
        assert create_initial_state().winner is None

    def test_initial_state_has_all_cells_legal(self):
        moves = get_legal_moves(create_initial_state())
        assert len(moves) == DEFAULT_BOARD_SIZE * DEFAULT_BOARD_SIZE


class TestSwitchPlayer:
    def test_switch_from_x_returns_o(self):
        assert switch_player(PLAYER_1) == PLAYER_2

    def test_switch_from_o_returns_x(self):
        assert switch_player(PLAYER_2) == PLAYER_1

    def test_switch_unknown_player_raises(self):
        with pytest.raises(ValueError, match="Jugador no encontrado"):
            switch_player("Z")


class TestLegalMoves:
    def test_occupied_cell_is_illegal(self):
        state = make_state(["X...", "....", "....", "...."], PLAYER_2)
        assert is_legal_move(state, (0, 0)) is False

    def test_empty_cell_is_legal(self):
        state = make_state(["X...", "....", "....", "...."], PLAYER_2)
        assert is_legal_move(state, (1, 1)) is True

    @pytest.mark.parametrize("move", [(-1, 0), (0, -1), (4, 0), (0, 4)])
    def test_out_of_bounds_is_illegal(self, move):
        assert is_legal_move(create_initial_state(), move) is False

    def test_move_on_terminal_state_is_illegal(self):
        state = make_state(["XXXX", "....", "....", "...."], PLAYER_2, winner=PLAYER_1)
        assert is_legal_move(state, (1, 1)) is False


class TestApplyMove:
    def test_apply_move_places_symbol(self):
        new_state = apply_move(create_initial_state(), (1, 2))
        assert new_state.board[1][2] == PLAYER_1

    def test_apply_move_switches_player(self):
        new_state = apply_move(create_initial_state(), (0, 0))
        assert new_state.current_player == PLAYER_2

    def test_apply_move_does_not_mutate_original(self):
        state = create_initial_state()
        apply_move(state, (0, 0))
        assert state.board[0][0] == EMPTY

    def test_apply_illegal_move_raises(self):
        state = make_state(["X...", "....", "....", "...."], PLAYER_2)
        with pytest.raises(ValueError, match="Movimiento ilegal"):
            apply_move(state, (0, 0))


class TestCheckWinner:
    def test_detects_row_winner(self):
        assert check_winner(make_board(["XXXX", "....", "....", "...."])) == PLAYER_1

    def test_detects_column_winner(self):
        assert check_winner(make_board(["O...", "O...", "O...", "O..."])) == PLAYER_2

    def test_detects_main_diagonal_winner(self):
        assert check_winner(make_board(["X...", ".X..", "..X.", "...X"])) == PLAYER_1

    def test_detects_anti_diagonal_winner(self):
        assert check_winner(make_board(["...O", "..O.", ".O..", "O..."])) == PLAYER_2

    def test_no_winner_on_mixed_line(self):
        assert check_winner(make_board(["XXXO", "....", "....", "...."])) is None

    def test_no_winner_on_empty_board(self):
        assert check_winner(create_initial_state().board) is None


class TestWinningLine:
    def test_returns_coordinates_of_winning_row(self):
        line = winning_line(make_board(["....", "XXXX", "....", "...."]))
        assert line == [(1, 0), (1, 1), (1, 2), (1, 3)]

    def test_returns_none_when_no_winner(self):
        assert winning_line(create_initial_state().board) is None


class TestTerminalAndDraw:
    def test_state_with_winner_is_terminal(self):
        state = make_state(["XXXX", "....", "....", "...."], PLAYER_2, winner=PLAYER_1)
        assert is_terminal(state) is True

    def test_full_board_is_terminal(self):
        state = make_state(["XOXO", "OXOX", "XOXO", "OXOX"], PLAYER_1)
        assert is_terminal(state) is True

    def test_full_board_without_winner_is_draw(self):
        state = make_state(["XOXO", "OXOX", "XOXO", "OXOX"], PLAYER_1)
        assert is_draw(state) is True

    def test_state_with_winner_is_not_draw(self):
        state = make_state(["XXXX", "....", "....", "...."], PLAYER_2, winner=PLAYER_1)
        assert is_draw(state) is False

    def test_ongoing_game_is_not_terminal(self):
        assert is_terminal(create_initial_state()) is False


class TestBoardSizes:
    """El juego admite tableros 3x3 y 4x4 con las mismas reglas."""

    def test_create_3x3_initial_state(self):
        state = create_initial_state(3)
        assert len(state.board) == 3
        assert len(get_legal_moves(state)) == 9

    def test_create_4x4_initial_state(self):
        state = create_initial_state(4)
        assert len(state.board) == 4
        assert len(get_legal_moves(state)) == 16

    def test_3x3_detects_row_winner(self):
        assert check_winner(make_board(["XXX", "O.O", "O.."])) == PLAYER_1

    def test_3x3_detects_diagonal_winner(self):
        assert check_winner(make_board(["O.X", ".O.", "X.O"])) == PLAYER_2

    def test_3x3_winning_line(self):
        line = winning_line(make_board(["O..", "XXX", "O.."]))
        assert line == [(1, 0), (1, 1), (1, 2)]

    def test_3x3_move_out_of_bounds_is_illegal(self):
        state = create_initial_state(3)
        assert is_legal_move(state, (2, 2)) is True
        assert is_legal_move(state, (3, 0)) is False
