# Backend — Tic-Tac-Toe AI

REST API that exposes the Tic-Tac-Toe game logic (3×3 and 4×4 boards) and the AI
(Minimax and Alpha-Beta pruning). It adapts the core from `project/src/game/`
without modifying the original. The board size is derived from the board itself,
so the rules and the AI work the same for both sizes.

## Architecture

```
app/
├── core/        Pure core: state, rules, constants (no UI dependencies)
├── ai/          Algorithms: Minimax, Alpha-Beta, and heuristic evaluation
├── schemas/     Pydantic models (the API contract)
├── services/    Orchestrates core + AI and translates to the API contract
├── api/         REST routes
├── config.py    Configuration read from the environment
└── main.py      FastAPI entry point
```

The API is **stateless**: every request carries the full board. There is no
database and no sessions.

## Requirements

- Python 3.11 or higher

## Installation

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Running

```bash
uvicorn app.main:app --reload
```

- API: http://localhost:8000
- Interactive documentation (Swagger): http://localhost:8000/api/docs

## Tests

```bash
pytest
```

## Environment variables

| Variable       | Default                                                | Description                            |
|----------------|--------------------------------------------------------|----------------------------------------|
| `CORS_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173`          | Comma-separated list of allowed CORS origins. |

## Endpoints

| Method | Route             | Description                                       |
|--------|-------------------|---------------------------------------------------|
| GET    | `/api/health`     | Service status.                                   |
| POST   | `/api/games/new`  | Initial state of a game (`{"size": 3}` or `4`).   |
| POST   | `/api/moves`      | Applies a move (422 if illegal).                  |
| POST   | `/api/ai/move`    | AI move with metrics.                             |
| POST   | `/api/ai/compare` | Compares Minimax vs Alpha-Beta on the state.      |

### AI parameters

- `algorithm`: `minimax` or `alpha_beta`.
- `depth_limit`: search depth (integer from 1 to 6; default 3).

If the board is empty, the AI plays a random position: a full search from the
empty board is intractable (same criterion as the original project).
