import { type ButtonHTMLAttributes } from "react";
import { cn } from "../utils/cn";
import styles from "./Button.module.css";

type ButtonVariant = "primary" | "secondary";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
}

/** Botón con estilos de marca. Variante primaria (dorada) o secundaria. */
export function Button({
  variant = "primary",
  className,
  type = "button",
  ...rest
}: ButtonProps) {
  return (
    <button
      type={type}
      className={cn(styles.button, styles[variant], className)}
      {...rest}
    />
  );
}
