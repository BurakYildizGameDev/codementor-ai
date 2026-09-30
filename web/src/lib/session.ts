/** İpucu merdiveni için kalıcı oturum kimliği (mimari §5.4.3): aynı `session_id` + `question_id`
 * ile her yeni gönderim ipucu seviyesini bir artırır. localStorage yoksa bellek içi yedek. */

const KEY = "codementor.session_id";
let fallback: string | null = null;

type SessionStorage = Pick<Storage, "getItem" | "setItem">;

function defaultStorage(): SessionStorage | undefined {
  try {
    return globalThis.localStorage;
  } catch {
    return undefined;
  }
}

export function getSessionId(storage: SessionStorage | undefined = defaultStorage()): string {
  try {
    const stored = storage?.getItem(KEY);
    if (stored) return stored;
  } catch {
    // gizli pencere / engellenmiş depolama: bellek içi yedeğe düş
  }
  fallback ??= `web-${crypto.randomUUID()}`;
  try {
    storage?.setItem(KEY, fallback);
  } catch {
    // kalıcı değil; bu sekme boyunca aynı kimlik kullanılır
  }
  return fallback;
}
