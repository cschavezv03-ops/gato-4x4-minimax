import { Button } from "./Button";
import styles from "./GameControls.module.css";

interface GameControlsProps {
  onNewGame: () => void;
  onMenu: () => void;
}

/** Acciones de partida: empezar de nuevo o volver al menú. */
export function GameControls({ onNewGame, onMenu }: GameControlsProps) {
  return (
    <div className={styles.controls}>
      <Button variant="primary" onClick={onNewGame}>
        Nueva partida
      </Button>
      <Button variant="secondary" onClick={onMenu}>
        Menú
      </Button>
    </div>
  );
}
