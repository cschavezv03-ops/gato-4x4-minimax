"""Tests de la IA: evaluación, Minimax y poda Alpha-Beta."""

from app.ai.alpha_beta import get_best_move_alpha_beta
from app.ai.evaluation import evaluate, heuristic, utility
from app.ai.minimax import get_best_move
from app.core.constants import DRAW_SCORE, LOSE_SCORE, WIN_SCORE
from app.core.rules import apply_move
from app.core.state import create_initial_state
from tests.helpers import make_state

# Tablero al que le falta una sola jugada: X gana colocando en (0, 3).
ONE_MOVE_TO_WIN = ["XXX.", "OOXO", "OXOX", "XOOX"]

# X (IA) debe bloquear: si no juega (0, 3), O completa la fila superior.
MUST_BLOCK = ["OOO.", "XX.O", "XOXO", "OXOX"]


class TestUtility:
    def test_ai_victory_scores_positive(self):
        state = make_state(ONE_MOVE_TO_WIN, "O", winner="X")
        assert utility(state, "X") == WIN_SCORE

    def test_opponent_victory_scores_negative(self):
        state = make_state(["OOOO", "X.X.", "XXXO", "...."], "X", winner="O")
        assert utility(state, "X") == LOSE_SCORE

    def test_draw_scores_zero(self):
        state = make_state(["XOXO", "OXOX", "XOXO", "OXOX"], "X")
        assert utility(state, "X") == DRAW_SCORE


class TestHeuristic:
    def test_heuristic_returns_int_on_non_terminal_state(self):
        state = make_state(["XX.O", "....", "....", "...."], "O")
        assert isinstance(heuristic(state, "X"), int)

    def test_evaluate_uses_utility_on_terminal_state(self):
        state = make_state(ONE_MOVE_TO_WIN, "O", winner="X")
        assert evaluate(state, "X") == WIN_SCORE


class TestBestMove:
    def test_minimax_takes_immediate_win(self):
        state = make_state(ONE_MOVE_TO_WIN, "X")
        move, score, _ = get_best_move(state, "X", None)
        assert move == (0, 3)
        assert score == WIN_SCORE

    def test_alpha_beta_takes_immediate_win(self):
        state = make_state(ONE_MOVE_TO_WIN, "X")
        move, score, _ = get_best_move_alpha_beta(state, "X", None)
        assert move == (0, 3)
        assert score == WIN_SCORE

    def test_minimax_blocks_opponent_win(self):
        state = make_state(MUST_BLOCK, "X")
        move, _, _ = get_best_move(state, "X", None)
        assert move == (0, 3)

    def test_alpha_beta_blocks_opponent_win(self):
        state = make_state(MUST_BLOCK, "X")
        move, _, _ = get_best_move_alpha_beta(state, "X", None)
        assert move == (0, 3)


class TestAlgorithmEquivalence:
    """Minimax y Alpha-Beta deben decidir igual; Alpha-Beta evalúa menos nodos."""

    def _midgame_state(self):
        state = create_initial_state()
        for move in [(0, 0), (1, 1), (0, 1), (1, 0), (2, 2), (3, 3), (2, 0), (0, 2)]:
            state = apply_move(state, move)
        return state

    def test_both_algorithms_choose_the_same_move(self):
        state = self._midgame_state()
        minimax_move, minimax_score, _ = get_best_move(state, "X", 4)
        alpha_beta_move, alpha_beta_score, _ = get_best_move_alpha_beta(state, "X", 4)
        assert minimax_move == alpha_beta_move
        assert minimax_score == alpha_beta_score

    def test_alpha_beta_evaluates_no_more_nodes_than_minimax(self):
        state = self._midgame_state()
        _, _, minimax_nodes = get_best_move(state, "X", 4)
        _, _, alpha_beta_nodes = get_best_move_alpha_beta(state, "X", 4)
        assert 0 < alpha_beta_nodes <= minimax_nodes
