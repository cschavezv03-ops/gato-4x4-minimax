import styles from "./Footer.module.css";

const MEMBERS = [
  "Renato Aguilar",
  "Sebastian Chavez",
  "Frank Jumbo",
  "Dax Navarrete",
];

/** Crédito del equipo, discreto al pie de la aplicación. */
export function Footer() {
  return (
    <footer className={styles.footer}>
      <span className={styles.group}>Grupo 5</span>
      <span className={styles.members}>{MEMBERS.join(" · ")}</span>
    </footer>
  );
}
