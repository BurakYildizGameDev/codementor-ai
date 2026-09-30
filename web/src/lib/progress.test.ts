import { stage } from "../test-fixtures";
import { initialProgress, progressReducer, totalDuration } from "./progress";

describe("progressReducer", () => {
  it("aşamaları geliş sırasıyla tutar ve durumlarını günceller", () => {
    const state = [
      stage("tier0", "started"),
      stage("tier0", "completed", 4),
      stage("tier1", "skipped"),
      stage("llm_a", "started"),
    ].reduce(progressReducer, initialProgress);
    expect(state.map((s) => [s.stage, s.status])).toEqual([
      ["tier0", "completed"],
      ["tier1", "skipped"],
      ["llm_a", "started"],
    ]);
    expect(totalDuration(state)).toBe(4);
  });

  it("aynı aşamanın başarısız olayı durumu failed yapar", () => {
    const state = [stage("llm_b", "started"), stage("llm_b", "failed", 9)].reduce(
      progressReducer,
      initialProgress,
    );
    expect(state).toEqual([{ stage: "llm_b", status: "failed", duration_ms: 9 }]);
  });
});
