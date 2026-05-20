/**
 * Cliente HTTP de la API del juego.
 *
 * Capa anticorrupción: la API usa snake_case y este módulo traduce las
 * respuestas a los tipos de dominio en camelCase. El resto de la aplicación
 * nunca ve el formato crudo del servidor.
 */

import {
  type AiMetrics,
  type AiMoveResult,
  type ApiAlgorithm,
  type Board,
  type CompareResult,
  type GameSnapshot,
  type Player,
  type Position,
} from "../domain/types";

const API_BASE_URL: string =
  import.meta.env.VITE_API_URL ?? "http://localhost:8000";

/** Error de comunicación o de validación devuelto por la API. */
export class ApiError extends Error {}

// --- Formato crudo de la API (snake_case) ------------------------------------

interface RawSnapshot {
  board: Cell2D;
  current_player: string;
  winner: string | null;
  is_draw: boolean;
  is_terminal: boolean;
  legal_moves: Position[];
  winning_line: Position[] | null;
}

interface RawMetrics {
  algorithm: string;
  move: Position;
  score: number;
  nodes_evaluated: number;
  elapsed_ms: number;
  is_random: boolean;
}

type Cell2D = string[][];

// --- Traducción crudo -> dominio ---------------------------------------------

function toSnapshot(raw: RawSnapshot): GameSnapshot {
  return {
    board: raw.board as Board,
    currentPlayer: raw.current_player as Player,
    winner: raw.winner as Player | null,
    isDraw: raw.is_draw,
    isTerminal: raw.is_terminal,
    legalMoves: raw.legal_moves,
    winningLine: raw.winning_line,
  };
}

function toMetrics(raw: RawMetrics): AiMetrics {
  return {
    algorithm: raw.algorithm as ApiAlgorithm,
    move: raw.move,
    score: raw.score,
    nodesEvaluated: raw.nodes_evaluated,
    elapsedMs: raw.elapsed_ms,
    isRandom: raw.is_random,
  };
}

// --- Petición genérica -------------------------------------------------------

async function post<T>(path: string, body?: unknown): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: body === undefined ? undefined : JSON.stringify(body),
    });
  } catch {
    throw new ApiError("No se pudo conectar con el servidor.");
  }

  if (!response.ok) {
    throw new ApiError(await extractDetail(response));
  }
  return (await response.json()) as T;
}

async function extractDetail(response: Response): Promise<string> {
  try {
    const data: unknown = await response.json();
    if (
      data &&
      typeof data === "object" &&
      "detail" in data &&
      typeof data.detail === "string"
    ) {
      return data.detail;
    }
  } catch {
    /* respuesta sin cuerpo JSON */
  }
  return "El servidor rechazó la petición.";
}

// --- Operaciones públicas ----------------------------------------------------

/** Crea una partida nueva con el tablero vacío del tamaño indicado (3 o 4). */
export async function newGame(size: number): Promise<GameSnapshot> {
  return toSnapshot(await post<RawSnapshot>("/api/games/new", { size }));
}

/** Aplica la jugada de un jugador y devuelve el nuevo estado. */
export async function applyMove(
  board: Board,
  currentPlayer: Player,
  move: Position,
): Promise<GameSnapshot> {
  const raw = await post<RawSnapshot>("/api/moves", {
    board,
    current_player: currentPlayer,
    move,
  });
  return toSnapshot(raw);
}

export interface AiMoveParams {
  board: Board;
  currentPlayer: Player;
  aiPlayer: Player;
  algorithm: ApiAlgorithm;
  depthLimit: number;
}

/** Pide a la IA que calcule y aplique su jugada. */
export async function requestAiMove(params: AiMoveParams): Promise<AiMoveResult> {
  const raw = await post<{ metrics: RawMetrics; state: RawSnapshot }>(
    "/api/ai/move",
    {
      board: params.board,
      current_player: params.currentPlayer,
      ai_player: params.aiPlayer,
      algorithm: params.algorithm,
      depth_limit: params.depthLimit,
    },
  );
  return { metrics: toMetrics(raw.metrics), state: toSnapshot(raw.state) };
}

export interface CompareParams {
  board: Board;
  currentPlayer: Player;
  aiPlayer: Player;
  depthLimit: number;
}

/** Ejecuta Minimax y Alpha-Beta sobre el mismo estado y compara sus métricas. */
export async function requestAiCompare(
  params: CompareParams,
): Promise<CompareResult> {
  const raw = await post<{
    minimax: RawMetrics;
    alpha_beta: RawMetrics;
    nodes_saved: number;
    state: RawSnapshot;
  }>("/api/ai/compare", {
    board: params.board,
    current_player: params.currentPlayer,
    ai_player: params.aiPlayer,
    depth_limit: params.depthLimit,
  });
  return {
    minimax: toMetrics(raw.minimax),
    alphaBeta: toMetrics(raw.alpha_beta),
    nodesSaved: raw.nodes_saved,
    state: toSnapshot(raw.state),
  };
}
