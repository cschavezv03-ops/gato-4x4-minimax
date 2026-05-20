/**
 * Máquina de estados de la partida.
 *
 * El reducer es una función pura: dada una acción, produce el nuevo estado.
 * Los efectos (llamadas a la API) viven en el hook `useGame`.
 */

import {
  type AiMetrics,
  type CompareResult,
  type GameConfig,
  type GameSnapshot,
  type Player,
  type Position,
  ALGORITHM,
  BOARD_SIZE,
  CELL,
  DEPTH,
  GAME_MODE,
  PLAYER,
} from "../domain/types";

export const STATUS = {
  /** En el menú, configurando la partida. */
  MENU: "menu",
  /** Partida en curso, esperando una jugada. */
  PLAYING: "playing",
  /** La IA está calculando su jugada. */
  THINKING: "thinking",
  /** La partida terminó (victoria o empate). */
  FINISHED: "finished",
} as const;
export type Status = (typeof STATUS)[keyof typeof STATUS];

export interface GameState {
  status: Status;
  config: GameConfig;
  snapshot: GameSnapshot | null;
  aiMetrics: AiMetrics | null;
  compareResult: CompareResult | null;
  error: string | null;
}

export const initialConfig: GameConfig = {
  mode: GAME_MODE.HUMAN_VS_AI,
  boardSize: BOARD_SIZE.LARGE,
  algorithm: ALGORITHM.ALPHA_BETA,
  depth: DEPTH.DEFAULT,
  humanStarts: true,
};

export const initialState: GameState = {
  status: STATUS.MENU,
  config: initialConfig,
  snapshot: null,
  aiMetrics: null,
  compareResult: null,
  error: null,
};

export type GameAction =
  | { type: "UPDATE_CONFIG"; config: Partial<GameConfig> }
  | { type: "GAME_STARTED"; snapshot: GameSnapshot }
  | { type: "OPTIMISTIC_MOVE"; position: Position; player: Player }
  | { type: "AI_THINKING" }
  | {
      type: "STATE_ADVANCED";
      snapshot: GameSnapshot;
      aiMetrics?: AiMetrics;
      compareResult?: CompareResult;
    }
  | { type: "ERROR"; message: string; snapshot?: GameSnapshot }
  | { type: "RETURN_TO_MENU" };

function resolveStatus(snapshot: GameSnapshot): Status {
  return snapshot.isTerminal ? STATUS.FINISHED : STATUS.PLAYING;
}

/**
 * Coloca una ficha de forma optimista para que la interfaz responda al
 * instante. El estado autoritativo del servidor lo reemplaza enseguida.
 */
function placeOptimistic(
  snapshot: GameSnapshot,
  position: Position,
  player: Player,
): GameSnapshot {
  const [targetRow, targetCol] = position;
  const board = snapshot.board.map((row, rowIndex) =>
    row.map((cell, colIndex) =>
      rowIndex === targetRow && colIndex === targetCol ? player : cell,
    ),
  );

  const legalMoves: Position[] = [];
  board.forEach((row, rowIndex) => {
    row.forEach((cell, colIndex) => {
      if (cell === CELL.EMPTY) legalMoves.push([rowIndex, colIndex]);
    });
  });

  return {
    board,
    currentPlayer: player === PLAYER.X ? PLAYER.O : PLAYER.X,
    winner: null,
    isDraw: false,
    isTerminal: false,
    legalMoves,
    winningLine: null,
  };
}

export function gameReducer(state: GameState, action: GameAction): GameState {
  switch (action.type) {
    case "UPDATE_CONFIG":
      return { ...state, config: { ...state.config, ...action.config } };

    case "GAME_STARTED":
      return {
        ...state,
        status: resolveStatus(action.snapshot),
        snapshot: action.snapshot,
        aiMetrics: null,
        compareResult: null,
        error: null,
      };

    case "OPTIMISTIC_MOVE":
      if (!state.snapshot) return state;
      return {
        ...state,
        snapshot: placeOptimistic(state.snapshot, action.position, action.player),
      };

    case "AI_THINKING":
      return { ...state, status: STATUS.THINKING, error: null };

    case "STATE_ADVANCED":
      return {
        ...state,
        status: resolveStatus(action.snapshot),
        snapshot: action.snapshot,
        aiMetrics: action.aiMetrics ?? state.aiMetrics,
        compareResult: action.compareResult ?? state.compareResult,
        error: null,
      };

    case "ERROR": {
      const snapshot = action.snapshot ?? state.snapshot;
      return {
        ...state,
        status: snapshot ? resolveStatus(snapshot) : STATUS.MENU,
        snapshot,
        error: action.message,
      };
    }

    case "RETURN_TO_MENU":
      return { ...initialState, config: state.config };

    default:
      return state;
  }
}
