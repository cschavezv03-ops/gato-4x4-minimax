import { TeamCredit } from "./TeamCredit";
import styles from "./Footer.module.css";

/** Pie de página con el crédito del equipo (pantalla de partida). */
export function Footer() {
  return (
    <footer className={styles.footer}>
      <TeamCredit />
    </footer>
  );
}
