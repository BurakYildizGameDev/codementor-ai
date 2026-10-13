import { describe, expect, it } from "vitest";
import { report } from "../test-fixtures";
import { formatCount, usageBreakdown, usageLabel } from "./usage";

describe("usageLabel", () => {
  it("token ve maliyeti CLI ile aynı biçimde yazar", () => {
    const meta = {
      ...report().meta,
      tokens_in: 1200,
      tokens_out: 340,
      cost_est: 0.01234,
    };
    expect(usageLabel(meta)).toBe(
      "1.540 token (giriş 1.200 · çıkış 340) · ~$0.0123",
    );
    expect(usageLabel({ ...meta, usage_estimated: true, cost_est: null })).toBe(
      "1.540 token (giriş 1.200 · çıkış 340) · tahmini",
    );
  });

  it("token harcanmadıysa nedenini yazar (Faz K: hep görünür)", () => {
    const none = {
      ...report().meta,
      tokens_in: 0,
      tokens_out: 0,
      cache_hit: false,
    };
    expect(usageLabel({ ...none, early_exit: false, degraded: false })).toBe(
      "token 0 (model çağrılmadı)",
    );
    expect(usageLabel({ ...none, cache_hit: true })).toBe(
      "token 0 (önbellekten)",
    );
    expect(usageLabel({ ...none, early_exit: true })).toBe(
      "token 0 (derleme hatası; model çağrılmadı)",
    );
    expect(usageLabel({ ...none, early_exit: false, degraded: true })).toBe(
      "token 0 (model yanıt vermedi)",
    );
  });
});

describe("usageBreakdown", () => {
  it("aşamaları sırayla yazar, onarımı belirtir", () => {
    const meta = {
      ...report().meta,
      repair_attempts: 1,
      stage_tokens: {
        llm_b: { input: 900, output: 200 },
        llm_a: { input: 1200, output: 340 },
      },
    };
    expect(usageBreakdown(meta)).toBe(
      "Giriş/çıkış: Analiz 1.200/340 · Mentor soruları 900/200 · 1 onarım",
    );
  });

  it("LLM aşaması yoksa null", () => {
    expect(usageBreakdown({ ...report().meta, stage_tokens: {} })).toBeNull();
  });

  it("binlik ayırıcı", () => {
    expect(formatCount(1234567)).toBe("1.234.567");
    expect(formatCount(999)).toBe("999");
  });
});
