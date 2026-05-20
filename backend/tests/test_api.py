"""Tests de la API REST (endpoints HTTP)."""

from tests.helpers import board_as_lists

EMPTY_ROWS = ["....", "....", "....", "...."]
ONE_MOVE_TO_WIN = ["XXX.", "OOXO", "OXOX", "XOOX"]
MIDGAME = ["XOXO", "OX.O", "X.OX", ".O.."]


class TestHealth:
    def test_health_returns_ok(self, client):
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_root_returns_info(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "docs" in response.json()


class TestNewGame:
    def test_new_game_returns_empty_board(self, client):
        response = client.post("/api/games/new")
        assert response.status_code == 200
        data = response.json()
        assert data["current_player"] == "X"
        assert data["winner"] is None
        assert len(data["legal_moves"]) == 16

    def test_new_game_3x3(self, client):
        response = client.post("/api/games/new", json={"size": 3})
        assert response.status_code == 200
        data = response.json()
        assert len(data["board"]) == 3
        assert len(data["legal_moves"]) == 9

    def test_new_game_rejects_invalid_size(self, client):
        response = client.post("/api/games/new", json={"size": 5})
        assert response.status_code == 422


class TestApplyMove:
    def test_apply_move_places_symbol(self, client):
        response = client.post(
            "/api/moves",
            json={
                "board": board_as_lists(EMPTY_ROWS),
                "current_player": "X",
                "move": [0, 0],
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["board"][0][0] == "X"
        assert data["current_player"] == "O"

    def test_apply_move_on_occupied_cell_returns_422(self, client):
        response = client.post(
            "/api/moves",
            json={
                "board": board_as_lists(["X...", "....", "....", "...."]),
                "current_player": "O",
                "move": [0, 0],
            },
        )
        assert response.status_code == 422

    def test_apply_move_out_of_bounds_returns_422(self, client):
        response = client.post(
            "/api/moves",
            json={
                "board": board_as_lists(EMPTY_ROWS),
                "current_player": "X",
                "move": [9, 9],
            },
        )
        assert response.status_code == 422

    def test_invalid_board_shape_returns_422(self, client):
        response = client.post(
            "/api/moves",
            json={
                "board": [["."], ["."], ["."]],
                "current_player": "X",
                "move": [0, 0],
            },
        )
        assert response.status_code == 422


class TestAiMove:
    def test_ai_takes_winning_move(self, client):
        response = client.post(
            "/api/ai/move",
            json={
                "board": board_as_lists(ONE_MOVE_TO_WIN),
                "current_player": "X",
                "ai_player": "X",
                "algorithm": "alpha_beta",
                "depth_limit": 3,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["metrics"]["move"] == [0, 3]
        assert data["state"]["winner"] == "X"
        assert data["state"]["is_terminal"] is True

    def test_ai_move_reports_nodes_evaluated(self, client):
        response = client.post(
            "/api/ai/move",
            json={
                "board": board_as_lists(MIDGAME),
                "current_player": "X",
                "ai_player": "X",
                "algorithm": "minimax",
                "depth_limit": 3,
            },
        )
        assert response.status_code == 200
        assert response.json()["metrics"]["nodes_evaluated"] > 0

    def test_ai_wins_on_3x3_board(self, client):
        response = client.post(
            "/api/ai/move",
            json={
                "board": board_as_lists(["XX.", "OO.", "XOO"]),
                "current_player": "X",
                "ai_player": "X",
                "algorithm": "minimax",
                "depth_limit": 3,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["metrics"]["move"] == [0, 2]
        assert data["state"]["winner"] == "X"

    def test_ai_move_when_not_ai_turn_returns_422(self, client):
        response = client.post(
            "/api/ai/move",
            json={
                "board": board_as_lists(EMPTY_ROWS),
                "current_player": "X",
                "ai_player": "O",
                "algorithm": "alpha_beta",
                "depth_limit": 3,
            },
        )
        assert response.status_code == 422


class TestAiCompare:
    def test_compare_returns_both_algorithms(self, client):
        response = client.post(
            "/api/ai/compare",
            json={
                "board": board_as_lists(MIDGAME),
                "current_player": "X",
                "ai_player": "X",
                "depth_limit": 4,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["minimax"]["algorithm"] == "minimax"
        assert data["alpha_beta"]["algorithm"] == "alpha_beta"
        assert data["minimax"]["move"] == data["alpha_beta"]["move"]

    def test_compare_reports_pruning_savings(self, client):
        response = client.post(
            "/api/ai/compare",
            json={
                "board": board_as_lists(MIDGAME),
                "current_player": "X",
                "ai_player": "X",
                "depth_limit": 4,
            },
        )
        data = response.json()
        expected = data["minimax"]["nodes_evaluated"] - data["alpha_beta"]["nodes_evaluated"]
        assert data["nodes_saved"] == expected
        assert data["nodes_saved"] >= 0
