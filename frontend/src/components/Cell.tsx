import { type Cell as CellValue, type Position, CELL } from "../domain/types";
import { cn } from "../utils/cn";
import { Mark } from "./Mark";
import styles from "./Cell.module.css";

interface CellProps {
  value: CellValue;
  position: Position;
  isInteractive: boolean;
  isWinning: boolean;
  onSelect: (position: Position) => void;
}

/** Una casilla del tablero. Es un botón accesible por teclado. */
export function Cell({
  value,
  position,
  isInteractive,
  isWinning,
  onSelect,
}: CellProps) {
  const [row, col] = position;
  const isEmpty = value === CELL.EMPTY;
  const label = isEmpty
    ? `Fila ${row + 1}, columna ${col + 1}, vacía`
    : `Fila ${row + 1}, columna ${col + 1}, ${value}`;

  return (
    <button
      type="button"
      className={cn(
        styles.cell,
        value === CELL.X && styles.x,
        value === CELL.O && styles.o,
        isWinning && styles.winning,
      )}
      disabled={!isInteractive || !isEmpty}
      onClick={() => onSelect(position)}
      aria-label={label}
    >
      {value !== CELL.EMPTY && <Mark player={value} />}
    </button>
  );
}
