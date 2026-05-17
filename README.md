# 4x4 Tic-Tac-Toe with Minimax and Alpha-Beta Pruning

This project is an Artificial Intelligence assignment focused on adversarial search in two-player games.  
The game implemented is a 4x4 version of Tic-Tac-Toe, where a human player can play against another human or against an AI opponent.

The AI uses the Minimax algorithm, Alpha-Beta Pruning, and a heuristic evaluation function when depth-limited search is required.

## Team Members

- Member 1: Renato Aguilar
- Member 2: Sebastian Chavez
- Member 3: Frank Jumbo
- Member 4: Dax Navarrete

## Project Objective

The objective of this project is to build a functional two-player game where the computer can make intelligent decisions using adversarial search techniques.

The project applies the following Artificial Intelligence concepts:

- Game states
- Legal actions
- Terminal states
- Utility function
- MAX and MIN players
- Minimax algorithm
- Alpha-Beta Pruning
- Heuristic evaluation function
- Depth-limited search

## Game Modes

The application includes the following game modes:

1. Human vs Human
2. Human vs AI

## Main Features

- 4x4 game board representation
- Turn-based gameplay
- Legal move validation
- Win, loss, and draw detection
- Human vs Human mode
- Human vs AI mode
- Minimax implementation
- Alpha-Beta Pruning implementation
- Node evaluation counter
- Performance comparison between Minimax and Alpha-Beta Pruning
- Heuristic evaluation for non-terminal states

## Project Structure

```text
gato-4x4-minimax/
│
├── README.md
├── .gitignore
│
├── src/
│   ├── main.py
│   ├── board.py
│   ├── game.py
│   ├── rules.py
│   │
│   └── ai/
│       ├── minimax.py
│       ├── alpha_beta.py
│       └── evaluation.py
│
├── docs/
│   ├── report.md
│   ├── game_tree_example.md
│   └── results.md
│
└── slides/
    └── presentation.pptx
```

## File Description

### `src/main.py`

Main entry point of the program.  
It allows the user to select the game mode and starts the game.

### `src/board.py`

Contains the board representation and functions to display or update the board.

### `src/game.py`

Controls the general flow of the game, including turns, player input, and game execution.

### `src/rules.py`

Contains the game rules, including:

- Legal move generation
- Win detection
- Draw detection
- Terminal state detection

### `src/ai/minimax.py`

Contains the basic Minimax algorithm implementation.

### `src/ai/alpha_beta.py`

Contains the Minimax algorithm optimized with Alpha-Beta Pruning.

### `src/ai/evaluation.py`

Contains the utility function and heuristic evaluation function used by the AI.

## How to Run

Make sure you have Python installed.

Then, run the following command:

```bash
python src/main.py
```

## Algorithms Used

## Minimax

Minimax is an adversarial search algorithm used in two-player games.  
It assumes that both players play optimally.

The AI is represented as the MAX player, trying to maximize its score.  
The human opponent is represented as the MIN player, trying to minimize the AI's score.

## Alpha-Beta Pruning

Alpha-Beta Pruning is an optimization of the Minimax algorithm.  
It reduces the number of nodes evaluated by ignoring branches that cannot affect the final decision.

This allows the AI to make decisions more efficiently.

## Heuristic Evaluation

For larger game trees, the search may be limited by depth.  
When the depth limit is reached, the AI evaluates the board using a heuristic function instead of exploring all possible future states.

The heuristic considers factors such as:

- Possible winning lines for the AI
- Possible winning lines for the opponent
- Blocking opponent threats
- Creating future winning opportunities

## Utility Function

Terminal states are evaluated as follows:

```text
AI wins      -> positive score
Human wins   -> negative score
Draw         -> zero
```

Example:

```text
AI wins      -> +10
Human wins   -> -10
Draw         -> 0
```

## Performance Comparison

The project compares the number of nodes evaluated by:

1. Basic Minimax
2. Minimax with Alpha-Beta Pruning

The results are documented in:

```text
docs/results.md
```

## Deliverables

The project includes:

- Functional game
- Human vs AI mode
- Minimax implementation
- Alpha-Beta Pruning implementation
- Performance comparison
- Short written report
- Partial game tree explanation
- Presentation slides
- Live demo

## Git Branches

The repository uses the following branch structure:

```text
main
develop
feature/human-vs-human
feature/ai-minimax
feature/alpha-beta
feature/heuristic
feature/documentation
```

### Branch Description

| Branch | Purpose |
|---|---|
| `main` | Final stable version |
| `develop` | Integration branch |
| `feature/human-vs-human` | Human vs Human game mode |
| `feature/ai-minimax` | Basic AI with Minimax |
| `feature/alpha-beta` | Alpha-Beta Pruning implementation |
| `feature/heuristic` | Depth-limited heuristic evaluation |
| `feature/documentation` | Report, results, and presentation |

## Development Workflow

1. Create a feature branch from `develop`.
2. Work only on the assigned feature branch.
3. Commit changes with clear messages.
4. Push the branch to GitHub.
5. Open a Pull Request to `develop`.
6. Test the integrated version.
7. Merge `develop` into `main` only when the project is stable.

## Example Commit Messages

```bash
git commit -m "Add board representation"
git commit -m "Implement win detection"
git commit -m "Add human vs human mode"
git commit -m "Implement basic minimax algorithm"
git commit -m "Add alpha-beta pruning"
git commit -m "Add node evaluation counter"
git commit -m "Update project report"
```

## Authors

Developed by students of Artificial Intelligence as a group project.

## License

This project is for academic purposes.
