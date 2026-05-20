import { cn } from "../utils/cn";
import styles from "./Segmented.module.css";

interface SegmentedOption<T extends string | number> {
  value: T;
  label: string;
}

interface SegmentedProps<T extends string | number> {
  options: SegmentedOption<T>[];
  value: T;
  ariaLabel: string;
  onChange: (value: T) => void;
}

/** Control segmentado: elige una opción entre varias mutuamente excluyentes. */
export function Segmented<T extends string | number>({
  options,
  value,
  ariaLabel,
  onChange,
}: SegmentedProps<T>) {
  return (
    <div className={styles.group} role="group" aria-label={ariaLabel}>
      {options.map((option) => (
        <button
          key={option.value}
          type="button"
          className={cn(styles.option, option.value === value && styles.active)}
          aria-pressed={option.value === value}
          onClick={() => onChange(option.value)}
        >
          {option.label}
        </button>
      ))}
    </div>
  );
}
