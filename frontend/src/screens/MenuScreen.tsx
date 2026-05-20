import {
  type BoardSize,
  type GameConfig,
  type GameMode,
  BOARD_SIZE,
  GAME_MODE,
} from "../domain/types";
import { Button } from "../components/Button";
import { ErrorBanner } from "../components/ErrorBanner";
import { Field } from "../components/Field";
import { Segmented } from "../components/Segmented";
import { SettingsPanel } from "../components/SettingsPanel";
import { TeamCredit } from "../components/TeamCredit";
import styles from "./MenuScreen.module.css";

interface MenuScreenProps {
  config: GameConfig;
  error: string | null;
  onConfigChange: (config: Partial<GameConfig>) => void;
  onStart: () => void;
}

const MODE_OPTIONS: Array<{ value: GameMode; label: string }> = [
  { value: GAME_MODE.HUMAN_VS_HUMAN, label: "Humano vs Humano" },
  { value: GAME_MODE.HUMAN_VS_AI, label: "Humano vs IA" },
];

const SIZE_OPTIONS: Array<{ value: BoardSize; label: string }> = [
  { value: BOARD_SIZE.SMALL, label: "3 × 3" },
  { value: BOARD_SIZE.LARGE, label: "4 × 4" },
];

/** Pantalla de inicio: elige el modo, el tamaño y los parámetros de la partida. */
export function MenuScreen({
  config,
  error,
  onConfigChange,
  onStart,
}: MenuScreenProps) {
  const isVsAi = config.mode === GAME_MODE.HUMAN_VS_AI;

  return (
    <section className={styles.menu}>
      <header className={styles.header}>
        <h1 className={styles.title}>Gato</h1>
        <p className={styles.subtitle}>Tres en raya contra una IA</p>
        <TeamCredit className={styles.credit} />
      </header>

      <div className={styles.fields}>
        <Field label="Modo de juego">
          <Segmented
            ariaLabel="Modo de juego"
            options={MODE_OPTIONS}
            value={config.mode}
            onChange={(value) => onConfigChange({ mode: value })}
          />
        </Field>

        <Field label="Tamaño del tablero">
          <Segmented
            ariaLabel="Tamaño del tablero"
            options={SIZE_OPTIONS}
            value={config.boardSize}
            onChange={(value) => onConfigChange({ boardSize: value })}
          />
        </Field>

        {isVsAi && (
          <SettingsPanel
            algorithm={config.algorithm}
            depth={config.depth}
            humanStarts={config.humanStarts}
            onChange={onConfigChange}
          />
        )}
      </div>

      {error && <ErrorBanner message={error} />}

      <Button variant="primary" className={styles.play} onClick={onStart}>
        Jugar
      </Button>
    </section>
  );
}
