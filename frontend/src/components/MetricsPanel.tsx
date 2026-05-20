import {
  type AiMetrics,
  type ApiAlgorithm,
  type CompareResult,
} from "../domain/types";
import styles from "./MetricsPanel.module.css";

interface MetricsPanelProps {
  aiMetrics: AiMetrics | null;
  compareResult: CompareResult | null;
}

const ALGORITHM_LABEL: Record<ApiAlgorithm, string> = {
  minimax: "Minimax",
  alpha_beta: "Alpha-Beta",
};

function formatNumber(value: number): string {
  return value.toLocaleString("es");
}

function formatMs(value: number): string {
  return `${value.toFixed(1)} ms`;
}

function formatScore(value: number): string {
  if (value >= 100_000) return "Gana la IA";
  if (value <= -100_000) return "Gana el rival";
  return formatNumber(value);
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className={styles.stat}>
      <span className={styles.statLabel}>{label}</span>
      <span className={styles.statValue}>{value}</span>
    </div>
  );
}

function SingleView({ metrics }: { metrics: AiMetrics }) {
  return (
    <div className={styles.panel}>
      <h2 className={styles.title}>Última jugada de la IA</h2>
      {metrics.isRandom ? (
        <p className={styles.note}>Jugada inicial aleatoria.</p>
      ) : (
        <div className={styles.stats}>
          <Stat label="Algoritmo" value={ALGORITHM_LABEL[metrics.algorithm]} />
          <Stat label="Nodos evaluados" value={formatNumber(metrics.nodesEvaluated)} />
          <Stat label="Puntaje" value={formatScore(metrics.score)} />
          <Stat label="Tiempo" value={formatMs(metrics.elapsedMs)} />
        </div>
      )}
    </div>
  );
}

function CompareView({ result }: { result: CompareResult }) {
  if (result.minimax.isRandom) {
    return (
      <div className={styles.panel}>
        <h2 className={styles.title}>Comparación de algoritmos</h2>
        <p className={styles.note}>Jugada inicial aleatoria.</p>
      </div>
    );
  }

  const percent =
    result.minimax.nodesEvaluated > 0
      ? Math.round((result.nodesSaved / result.minimax.nodesEvaluated) * 100)
      : 0;

  return (
    <div className={styles.panel}>
      <h2 className={styles.title}>Comparación de algoritmos</h2>
      <div className={styles.columns}>
        <div className={styles.column}>
          <span className={styles.columnTitle}>Minimax</span>
          <Stat label="Nodos" value={formatNumber(result.minimax.nodesEvaluated)} />
          <Stat label="Tiempo" value={formatMs(result.minimax.elapsedMs)} />
        </div>
        <div className={styles.column}>
          <span className={styles.columnTitle}>Alpha-Beta</span>
          <Stat label="Nodos" value={formatNumber(result.alphaBeta.nodesEvaluated)} />
          <Stat label="Tiempo" value={formatMs(result.alphaBeta.elapsedMs)} />
        </div>
      </div>
      <p className={styles.highlight}>
        La poda evitó <strong>{formatNumber(result.nodesSaved)}</strong> nodos
        {" "}({percent}%).
      </p>
    </div>
  );
}

/** Métricas de la IA: jugada simple o comparación entre algoritmos. */
export function MetricsPanel({ aiMetrics, compareResult }: MetricsPanelProps) {
  if (compareResult) {
    return <CompareView result={compareResult} />;
  }
  if (aiMetrics) {
    return <SingleView metrics={aiMetrics} />;
  }
  return (
    <div className={styles.panel}>
      <p className={styles.note}>La IA aún no ha jugado.</p>
    </div>
  );
}
