import { getSessionId } from "./session";

describe("getSessionId", () => {
  it("ilk çağrıda üretir, sonra aynı kimliği döndürür", () => {
    const store = new Map<string, string>();
    const storage = {
      getItem: (k: string) => store.get(k) ?? null,
      setItem: (k: string, v: string) => void store.set(k, v),
    };
    const first = getSessionId(storage);
    expect(first).toMatch(/^web-[0-9a-f-]{36}$/);
    expect(getSessionId(storage)).toBe(first);
  });

  it("depolama erişimi hata verse de bir kimlik döndürür (gizli pencere)", () => {
    const broken = {
      getItem: (): string | null => {
        throw new Error("SecurityError");
      },
      setItem: (): void => {
        throw new Error("SecurityError");
      },
    };
    const id = getSessionId(broken);
    expect(id).toMatch(/^web-/);
    expect(getSessionId(broken)).toBe(id); // bellek içi yedek
  });
});
