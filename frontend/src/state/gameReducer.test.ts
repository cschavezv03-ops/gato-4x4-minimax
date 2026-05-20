import { describe, expect, it } from "vitest";

import {
  type AiMetrics,
  type Board,
  type GameSnapshot,
  CELL,
  PLAYER,
} from "../domain/types";
import { STATUS, gameReducer, initialState } from "./gameReducer";

function emptyBoard(): Board {
  return Array.from({ length: 4 }, () =>
    Array.from({ length: 4 }, () => CELL.EMPTY),
  );
}

function emptySnapshot(): GameSnapshot {
  return {
    board: emptyBoard(),
    currentPlayer: PLAYER.X,
    winner: null,
    isDraw: false,
    isTerminal: false,
    legalMoves: [],
    winningLine: null,
  };
}

function terminalSnapshot(): GameSnapshot {
  return {
    ...emptySnapshot(),
    winner: PLAYER.X,
    isTerminal: true,
    winningLine: [
      [0, 0],
      [0, 1],
      [0, 2],
      [0, 3],
    ],
  };
}

const sampleMetrics: AiMetrics = {
  algorithm: "alpha_beta",
  move: [1, 1],
  score: 50,
  nodesEvaluated: 120,
  elapsedMs: 4.2,
  isRandom: false,
};

describe("gameReducer", () => {
  it("fusiona la configuración con UPDATE_CONFIG", () => {
    const next = gameReducer(initialState, {
      type: "UPDATE_CONFIG",
      config: { depth: 5 },
    });
    expect(next.config.depth).toBe(5);
    expect(next.config.mode).toBe(initialState.config.mode);
  });

  it("pasa a estado jugando al iniciar la partida", () => {
    const next = gameReducer(initialState, {
      type: "GAME_STARTED",
      snapshot: emptySnapshot(),
    });
    expect(next.status).toBe(STATUS.PLAYING);
    expect(next.snapshot).not.toBeNull();
  });

  it("coloca una ficha de forma optimista", () => {
    const started = gameReducer(initialState, {
      type: "GAME_STARTED",
      snapshot: emptySnapshot(),
    });
    const next = gameReducer(started, {
      type: "OPTIMISTIC_MOVE",
      position: [2, 3],
      player: PLAYER.X,
    });
    expect(next.snapshot?.board[2]?.[3]).toBe(PLAYER.X);
    expect(next.snapshot?.currentPlayer).toBe(PLAYER.O);
  });

  it("marca la partida como terminada cuando el estado es terminal", () => {
    const next = gameReducer(initialState, {
      type: "STATE_ADVANCED",
      snapshot: terminalSnapshot(),
    });
    expect(next.status).toBe(STATUS.FINISHED);
  });

  it("conserva las métricas previas si STATE_ADVANCED no las trae", () => {
    const withMetrics = gameReducer(
      { ...initialState, snapshot: emptySnapshot() },
      { type: "STATE_ADVANCED", snapshot: emptySnapshot(), aiMetrics: sampleMetrics },
    );
    const afterHumanMove = gameReducer(withMetrics, {
      type: "STATE_ADVANCED",
      snapshot: emptySnapshot(),
    });
    expect(afterHumanMove.aiMetrics).toEqual(sampleMetrics);
  });

  it("registra el mensaje de error", () => {
    const next = gameReducer(initialState, {
      type: "ERROR",
      message: "Falló la conexión",
    });
    expect(next.error).toBe("Falló la conexión");
  });

  it("vuelve al menú conservando la configuración", () => {
    const configured = gameReducer(initialState, {
      type: "UPDATE_CONFIG",
      config: { depth: 6 },
    });
    const next = gameReducer(configured, { type: "RETURN_TO_MENU" });
    expect(next.status).toBe(STATUS.MENU);
    expect(next.config.depth).toBe(6);
    expect(next.snapshot).toBeNull();
  });
});
