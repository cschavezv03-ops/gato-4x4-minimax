import { GAME_MODE } from "../domain/types";
import { type Game } from "../hooks/useGame";
import { STATUS } from "../state/gameReducer";
import { Board } from "../components/Board";
import { ErrorBanner } from "../components/ErrorBanner";
import { GameControls } from "../components/GameControls";
import { GameStatus } from "../components/GameStatus";
import { MetricsPanel } from "../components/MetricsPanel";
import styles from "./GameScreen.module.css";

interface GameScreenProps {
  game: Game;
}

/** Pantalla de partida: tablero, estado, métricas y controles. */
export function GameScreen({ game }: GameScreenProps) {
  const { state, humanPlayer, playMove, startGame, returnToMenu } = game;
  const { snapshot, status, config } = state;

  if (!snapshot) return null;

  const isVsAi = config.mode === GAME_MODE.HUMAN_VS_AI;
  const isHumanTurn =
    config.mode === GAME_MODE.HUMAN_VS_HUMAN ||
    snapshot.currentPlayer === humanPlayer;
  const isInteractive = status === STATUS.PLAYING && isHumanTurn;

  return (
    <section className={styles.game}>
      <GameStatus
        status={status}
        snapshot={snapshot}
        mode={config.mode}
        humanPlayer={humanPlayer}
      />

      <Board
        board={snapshot.board}
        winningLine={snapshot.winningLine}
        isInteractive={isInteractive}
        onSelect={playMove}
      />

      {isVsAi && (
        <MetricsPanel
          aiMetrics={state.aiMetrics}
          compareResult={state.compareResult}
        />
      )}

      {state.error && <ErrorBanner message={state.error} />}

      <GameControls onNewGame={startGame} onMenu={returnToMenu} />
    </section>
  );
}
