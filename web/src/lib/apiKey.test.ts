import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { clearApiKey, getApiKey, setApiKey } from "./apiKey";

describe("apiKey", () => {
  beforeEach(() => {
    sessionStorage.clear();
    localStorage.clear();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("anahtar yokken getApiKey null döner", () => {
    expect(getApiKey()).toBeNull();
  });

  it("setApiKey anahtarı sessionStorage'a yazar ve localStorage'a dokunmaz", () => {
    const setItemSpy = vi.spyOn(Storage.prototype, "setItem");

    setApiKey("test-key-123");

    expect(getApiKey()).toBe("test-key-123");
    expect(sessionStorage.getItem("codementor_api_key")).toBe("test-key-123");
    expect(localStorage.getItem("codementor_api_key")).toBeNull();
    expect(setItemSpy).toHaveBeenCalled();
    expect(setItemSpy.mock.instances[0]).toBe(sessionStorage);
    expect(setItemSpy.mock.instances[0]).not.toBe(localStorage);
  });

  it("clearApiKey anahtarı siler", () => {
    setApiKey("test-key-123");
    expect(getApiKey()).toBe("test-key-123");
    clearApiKey();
    expect(getApiKey()).toBeNull();
  });
});
