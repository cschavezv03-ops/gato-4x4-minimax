import { type ReactNode } from "react";
import styles from "./Field.module.css";

interface FieldProps {
  label: string;
  hint?: string;
  children: ReactNode;
}

/** Agrupa una etiqueta con su control y una ayuda opcional. */
export function Field({ label, hint, children }: FieldProps) {
  return (
    <div className={styles.field}>
      <span className={styles.label}>{label}</span>
      {children}
      {hint && <span className={styles.hint}>{hint}</span>}
    </div>
  );
}
