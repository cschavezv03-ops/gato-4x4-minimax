import { Minus, Plus } from "lucide-react";

import {
  type Algorithm,
  type GameConfig,
  ALGORITHM,
  DEPTH,
} from "../domain/types";
import { Field } from "./Field";
import { Segmented } from "./Segmented";
import styles from "./SettingsPanel.module.css";

interface SettingsPanelProps {
  algorithm: Algorithm;
  depth: number;
  humanStarts: boolean;
  onChange: (config: Partial<GameConfig>) => void;
}

type Starter = "human" | "ai";

const ALGORITHM_OPTIONS: Array<{ value: Algorithm; label: string }> = [
  { value: ALGORITHM.MINIMAX, label: "Minimax" },
  { value: ALGORITHM.ALPHA_BETA, label: "Alpha-Beta" },
  { value: ALGORITHM.COMPARE, label: "Comparar" },
];

const STARTER_OPTIONS: Array<{ value: Starter; label: string }> = [
  { value: "human", label: "Tú" },
  { value: "ai", label: "IA" },
];

/** Parámetros configurables de la partida contra la IA. */
export function SettingsPanel({
  algorithm,
  depth,
  humanStarts,
  onChange,
}: SettingsPanelProps) {
  function changeDepth(delta: number) {
    const next = depth + delta;
    if (next >= DEPTH.MIN && next <= DEPTH.MAX) {
      onChange({ depth: next });
    }
  }

  return (
    <div className={styles.panel}>
      <Field label="Algoritmo">
        <Segmented
          ariaLabel="Algoritmo de la IA"
          options={ALGORITHM_OPTIONS}
          value={algorithm}
          onChange={(value) => onChange({ algorithm: value })}
        />
      </Field>

      <Field label="Profundidad de búsqueda" hint="Más profundidad, IA más fuerte.">
        <div className={styles.stepper}>
          <button
            type="button"
            className={styles.stepButton}
            onClick={() => changeDepth(-1)}
            disabled={depth <= DEPTH.MIN}
            aria-label="Disminuir profundidad"
          >
            <Minus size={18} aria-hidden="true" />
          </button>
          <span className={styles.depthValue} aria-live="polite">
            {depth}
          </span>
          <button
            type="button"
            className={styles.stepButton}
            onClick={() => changeDepth(1)}
            disabled={depth >= DEPTH.MAX}
            aria-label="Aumentar profundidad"
          >
            <Plus size={18} aria-hidden="true" />
          </button>
        </div>
      </Field>

      <Field label="Quién empieza">
        <Segmented
          ariaLabel="Quién hace la primera jugada"
          options={STARTER_OPTIONS}
          value={humanStarts ? "human" : "ai"}
          onChange={(value) => onChange({ humanStarts: value === "human" })}
        />
      </Field>
    </div>
  );
}
