/** Une nombres de clase descartando los valores vacíos o falsos. */
export function cn(
  ...values: Array<string | false | null | undefined>
): string {
  return values.filter(Boolean).join(" ");
}
