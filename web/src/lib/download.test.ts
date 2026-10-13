import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { saveBlob } from "./download";

describe("saveBlob", () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
  });

  it("indirme URL'sini 1000ms gecikmeyle iptal eder (Faz E: E9)", () => {
    const createObjectURL = vi.fn().mockReturnValue("blob:http://localhost/test-uuid");
    const revokeObjectURL = vi.fn();
    vi.stubGlobal("URL", {
      ...URL,
      createObjectURL,
      revokeObjectURL,
    });

    const blob = new Blob(["test"], { type: "text/plain" });
    saveBlob(blob, "rapor.md");

    expect(createObjectURL).toHaveBeenCalledWith(blob);
    expect(revokeObjectURL).not.toHaveBeenCalled();

    vi.advanceTimersByTime(999);
    expect(revokeObjectURL).not.toHaveBeenCalled();

    vi.advanceTimersByTime(1);
    expect(revokeObjectURL).toHaveBeenCalledWith("blob:http://localhost/test-uuid");
  });
});
