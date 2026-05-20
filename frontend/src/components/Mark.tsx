import { type Player, PLAYER } from "../domain/types";
import styles from "./Mark.module.css";

interface MarkProps {
  player: Player;
}

/** Ficha del juego dibujada como SVG: X con dos trazos, O con un anillo. */
export function Mark({ player }: MarkProps) {
  if (player === PLAYER.X) {
    return (
      <svg className={styles.mark} viewBox="0 0 100 100" aria-hidden="true">
        <line x1="26" y1="26" x2="74" y2="74" />
        <line x1="74" y1="26" x2="26" y2="74" />
      </svg>
    );
  }
  return (
    <svg className={styles.mark} viewBox="0 0 100 100" aria-hidden="true">
      <circle cx="50" cy="50" r="26" />
    </svg>
  );
}
