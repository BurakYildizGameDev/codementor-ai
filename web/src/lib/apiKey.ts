/** API anahtarı oturum depolaması (Faz E: E4). Yalnızca sessionStorage kullanılır (sekme kapanınca silinir). */

const KEY_NAME = "codementor_api_key";

export function getApiKey(): string | null {
  try {
    return sessionStorage.getItem(KEY_NAME);
  } catch {
    return null;
  }
}

export function setApiKey(value: string): void {
  try {
    sessionStorage.setItem(KEY_NAME, value);
  } catch {
    // sessionStorage engelliyse yut
  }
}

export function clearApiKey(): void {
  try {
    sessionStorage.removeItem(KEY_NAME);
  } catch {
    // yut
  }
}
