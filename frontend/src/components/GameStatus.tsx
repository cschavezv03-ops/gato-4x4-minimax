import {
  type GameMode,
  type GameSnapshot,
  type Player,
  GAME_MODE,
} from "../domain/types";
import { type Status, STATUS } from "../state/gameReducer";
import { cn } from "../utils/cn";
import { Mark } from "./Mark";
import styles from "./GameStatus.module.css";

interface GameStatusProps {
  status: Status;
  snapshot: GameSnapshot;
  mode: GameMode;
  humanPlayer: Player;
}

type Tone = "neutral" | "win" | "lose";

interface StatusView {
  text: string;
  player: Player | null;
  tone: Tone;
}

function describe({
  status,
  snapshot,
  mode,
  humanPlayer,
}: GameStatusProps): StatusView {
  if (status === STATUS.THINKING) {
    return { text: "La IA está pensando", player: null, tone: "neutral" };
  }

  if (status === STATUS.FINISHED) {
    if (snapshot.winner === null) {
      return { text: "Empate", player: null, tone: "neutral" };
    }
    if (mode === GAME_MODE.HUMAN_VS_HUMAN) {
      return { text: `Ganó ${snapshot.winner}`, player: snapshot.winner, tone: "win" };
    }
    return snapshot.winner === humanPlayer
      ? { text: "¡Ganaste!", player: snapshot.winner, tone: "win" }
      : { text: "Ganó la IA", player: snapshot.winner, tone: "lose" };
  }

  if (mode === GAME_MODE.HUMAN_VS_HUMAN) {
    return {
      text: `Turno de ${snapshot.currentPlayer}`,
      player: snapshot.currentPlayer,
      tone: "neutral",
    };
  }
  return snapshot.currentPlayer === humanPlayer
    ? { text: "Tu turno", player: snapshot.currentPlayer, tone: "neutral" }
    : { text: "Turno de la IA", player: snapshot.currentPlayer, tone: "neutral" };
}

/** Mensaje breve del estado de la partida: turno, victoria o empate. */
export function GameStatus(props: GameStatusProps) {
  const view = describe(props);
  const isThinking = props.status === STATUS.THINKING;

  return (
    <div
      className={cn(styles.status, styles[view.tone])}
      role="status"
      aria-live="polite"
    >
      {view.player && (
        <span className={styles.badge}>
          <Mark player={view.player} />
        </span>
      )}
      <span className={styles.text}>{view.text}</span>
      {isThinking && (
        <span className={styles.dots} aria-hidden="true">
          <span />
          <span />
          <span />
        </span>
      )}
    </div>
  );
}
