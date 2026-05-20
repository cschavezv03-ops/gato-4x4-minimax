import { cn } from "../utils/cn";
import styles from "./TeamCredit.module.css";

const MEMBERS = [
  "Renato Aguilar",
  "Sebastian Chavez",
  "Frank Jumbo",
  "Dax Navarrete",
];

interface TeamCreditProps {
  className?: string;
}

/** Crédito del equipo: "Grupo 5" y los integrantes. */
export function TeamCredit({ className }: TeamCreditProps) {
  return (
    <div className={cn(styles.credit, className)}>
      <span className={styles.group}>Grupo 5</span>
      <span className={styles.members}>{MEMBERS.join(" · ")}</span>
    </div>
  );
}
