import { describe, expect, it } from "vitest";
import { report } from "../test-fixtures";
import { usageLabel } from "./usage";

describe("usageLabel", () => {
  it("token ve maliyeti CLI ile aynı biçimde yazar", () => {
    const meta = { ...report().meta, tokens_in: 1200, tokens_out: 340, cost_est: 0.01234 };
    expect(usageLabel(meta)).toBe("token 1200/340 · ~$0.0123");
    expect(usageLabel({ ...meta, usage_estimated: true, cost_est: null })).toBe(
      "token 1200/340 (tahmini)",
    );
  });

  it("LLM token'ı harcanmadıysa etiket yok", () => {
    expect(usageLabel({ ...report().meta, tokens_in: 0, tokens_out: 0 })).toBeNull();
  });
});
