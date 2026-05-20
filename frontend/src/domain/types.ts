/**
 * Tipos de dominio del juego.
 *
 * Convención: se define un objeto `const` y se extrae el tipo a partir de él.
 * Así hay una única fuente de verdad y valores disponibles en tiempo de ejecución.
 */

export const PLAYER = {
  X: "X",
  O: "O",
} as const;
export type Player = (typeof PLAYER)[keyof typeof PLAYER];

export const CELL = {
  X: "X",
  O: "O",
  EMPTY: ".",
} as const;
export type Cell = (typeof CELL)[keyof typeof CELL];

/** Tablero 4x4: filas de celdas. */
export type Board = Cell[][];

/** Posición en el tablero como par [fila, columna]. */
export type Position = [number, number];

export const GAME_MODE = {
  HUMAN_VS_HUMAN: "hvh",
  HUMAN_VS_AI: "hvai",
} as const;
export type GameMode = (typeof GAME_MODE)[keyof typeof GAME_MODE];

/** Elección de algoritmo del usuario (incluye el modo comparación). */
export const ALGORITHM = {
  MINIMAX: "minimax",
  ALPHA_BETA: "alpha_beta",
  COMPARE: "compare",
} as const;
export type Algorithm = (typeof ALGORITHM)[keyof typeof ALGORITHM];

/** Algoritmo que acepta la API (la comparación usa otro endpoint). */
export type ApiAlgorithm = typeof ALGORITHM.MINIMAX | typeof ALGORITHM.ALPHA_BETA;

export const DEPTH = {
  MIN: 1,
  MAX: 6,
  DEFAULT: 3,
} as const;

/** Tamaños de tablero admitidos. */
export const BOARD_SIZE = {
  SMALL: 3,
  LARGE: 4,
} as const;
export type BoardSize = (typeof BOARD_SIZE)[keyof typeof BOARD_SIZE];

/** Estado del tablero devuelto por la API. */
export interface GameSnapshot {
  board: Board;
  currentPlayer: Player;
  winner: Player | null;
  isDraw: boolean;
  isTerminal: boolean;
  legalMoves: Position[];
  winningLine: Position[] | null;
}

/** Métricas de una ejecución de un algoritmo de IA. */
export interface AiMetrics {
  algorithm: ApiAlgorithm;
  move: Position;
  score: number;
  nodesEvaluated: number;
  elapsedMs: number;
  isRandom: boolean;
}

/** Resultado de una jugada de la IA. */
export interface AiMoveResult {
  metrics: AiMetrics;
  state: GameSnapshot;
}

/** Resultado de comparar Minimax y Alpha-Beta sobre el mismo estado. */
export interface CompareResult {
  minimax: AiMetrics;
  alphaBeta: AiMetrics;
  nodesSaved: number;
  state: GameSnapshot;
}

/** Configuración de una partida elegida en el menú. */
export interface GameConfig {
  mode: GameMode;
  boardSize: BoardSize;
  algorithm: Algorithm;
  depth: number;
  humanStarts: boolean;
}
