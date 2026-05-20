/**
 * Hook que orquesta la partida: combina el reducer (estado) con la API
 * (efectos). Los componentes solo llaman a las acciones que expone.
 */

import { useReducer } from "react";

import {
  type GameConfig,
  type GameSnapshot,
  type Player,
  type Position,
  ALGORITHM,
  GAME_MODE,
  PLAYER,
} from "../domain/types";
import * as api from "../services/api";
import { ApiError } from "../services/api";
import { STATUS, gameReducer, initialState } from "../state/gameReducer";

interface ResolvedPlayers {
  humanPlayer: Player;
  aiPlayer: Player;
}

/** Determina qué símbolo controla el humano y cuál la IA según la configuración. */
function resolvePlayers(config: GameConfig): ResolvedPlayers {
  if (config.mode === GAME_MODE.HUMAN_VS_HUMAN || config.humanStarts) {
    return { humanPlayer: PLAYER.X, aiPlayer: PLAYER.O };
  }
  return { humanPlayer: PLAYER.O, aiPlayer: PLAYER.X };
}

function errorMessage(error: unknown): string {
  return error instanceof ApiError
    ? error.message
    : "Ocurrió un error inesperado.";
}

export function useGame() {
  const [state, dispatch] = useReducer(gameReducer, initialState);
  const { humanPlayer, aiPlayer } = resolvePlayers(state.config);

  /** Ejecuta el turno de la IA con el algoritmo configurado. */
  async function runAiTurn(snapshot: GameSnapshot, config: GameConfig) {
    const players = resolvePlayers(config);
    dispatch({ type: "AI_THINKING" });
    try {
      if (config.algorithm === ALGORITHM.COMPARE) {
        const result = await api.requestAiCompare({
          board: snapshot.board,
          currentPlayer: snapshot.currentPlayer,
          aiPlayer: players.aiPlayer,
          depthLimit: config.depth,
        });
        dispatch({
          type: "STATE_ADVANCED",
          snapshot: result.state,
          aiMetrics: result.alphaBeta,
          compareResult: result,
        });
      } else {
        const result = await api.requestAiMove({
          board: snapshot.board,
          currentPlayer: snapshot.currentPlayer,
          aiPlayer: players.aiPlayer,
          algorithm: config.algorithm,
          depthLimit: config.depth,
        });
        dispatch({
          type: "STATE_ADVANCED",
          snapshot: result.state,
          aiMetrics: result.metrics,
        });
      }
    } catch (error) {
      dispatch({ type: "ERROR", message: errorMessage(error), snapshot });
    }
  }

  /** Inicia una partida nueva con la configuración actual. */
  async function startGame() {
    const config = state.config;
    try {
      const snapshot = await api.newGame(config.boardSize);
      dispatch({ type: "GAME_STARTED", snapshot });

      const players = resolvePlayers(config);
      if (
        config.mode === GAME_MODE.HUMAN_VS_AI &&
        snapshot.currentPlayer === players.aiPlayer
      ) {
        await runAiTurn(snapshot, config);
      }
    } catch (error) {
      dispatch({ type: "ERROR", message: errorMessage(error) });
    }
  }

  /** Aplica la jugada del humano y, si corresponde, dispara el turno de la IA. */
  async function playMove(position: Position) {
    const snapshot = state.snapshot;
    if (!snapshot || state.status !== STATUS.PLAYING) return;

    const config = state.config;
    const player = snapshot.currentPlayer;
    dispatch({ type: "OPTIMISTIC_MOVE", position, player });

    try {
      const next = await api.applyMove(snapshot.board, player, position);
      dispatch({ type: "STATE_ADVANCED", snapshot: next });

      const players = resolvePlayers(config);
      if (
        config.mode === GAME_MODE.HUMAN_VS_AI &&
        !next.isTerminal &&
        next.currentPlayer === players.aiPlayer
      ) {
        await runAiTurn(next, config);
      }
    } catch (error) {
      dispatch({ type: "ERROR", message: errorMessage(error), snapshot });
    }
  }

  function updateConfig(config: Partial<GameConfig>) {
    dispatch({ type: "UPDATE_CONFIG", config });
  }

  function returnToMenu() {
    dispatch({ type: "RETURN_TO_MENU" });
  }

  return {
    state,
    humanPlayer,
    aiPlayer,
    startGame,
    playMove,
    updateConfig,
    returnToMenu,
  };
}

/** Tipo de la API que expone el hook `useGame`. */
export type Game = ReturnType<typeof useGame>;
