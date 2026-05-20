import { type Board as BoardType, type Position } from "../domain/types";
import { Cell } from "./Cell";
import styles from "./Board.module.css";

interface BoardProps {
  board: BoardType;
  winningLine: Position[] | null;
  isInteractive: boolean;
  onSelect: (position: Position) => void;
}

function isWinningCell(
  line: Position[] | null,
  row: number,
  col: number,
): boolean {
  return line?.some(([r, c]) => r === row && c === col) ?? false;
}

/** Tablero NxN (3x3 o 4x4). Solo las casillas vacías son interactivas. */
export function Board({
  board,
  winningLine,
  isInteractive,
  onSelect,
}: BoardProps) {
  const size = board.length;

  return (
    <div
      className={styles.board}
      style={{ gridTemplateColumns: `repeat(${size}, minmax(0, 1fr))` }}
      role="grid"
      aria-label={`Tablero ${size} por ${size}`}
    >
      {board.map((row, rowIndex) =>
        row.map((cell, colIndex) => (
          <Cell
            key={`${rowIndex}-${colIndex}`}
            value={cell}
            position={[rowIndex, colIndex]}
            isInteractive={isInteractive}
            isWinning={isWinningCell(winningLine, rowIndex, colIndex)}
            onSelect={onSelect}
          />
        )),
      )}
    </div>
  );
}
