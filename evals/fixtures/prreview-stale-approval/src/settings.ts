export function loadSettings(input: {timeoutMs?: number | null}) {
  const timeoutMs = input.timeoutMs || 30_000;
  return {...input, timeoutMs};
}
