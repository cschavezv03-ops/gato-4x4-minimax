import { TriangleAlert } from "lucide-react";
import styles from "./ErrorBanner.module.css";

interface ErrorBannerProps {
  message: string;
}

/** Aviso de error accesible (lo anuncian los lectores de pantalla). */
export function ErrorBanner({ message }: ErrorBannerProps) {
  return (
    <div className={styles.banner} role="alert">
      <TriangleAlert className={styles.icon} size={18} aria-hidden="true" />
      <span>{message}</span>
    </div>
  );
}
