import { STAGE_LABELS, type StageState, totalDuration } from "../lib/progress";

const STATUS_ICON: Record<StageState["status"], string> = {
  started: "…",
  completed: "✓",
  skipped: "–",
  failed: "✗",
};

/** SSE aşama ilerlemesi (mimari §9). */
export function StageProgress({ stages, busy }: { stages: StageState[]; busy: boolean }) {
  if (!stages.length) return null;
  const seconds = (totalDuration(stages) / 1000).toFixed(1);
  return (
    <section className="card progress" aria-label="İlerleme" aria-busy={busy}>
      <ol>
        {stages.map((s) => (
          <li key={s.stage} className={`stage stage-${s.status}`}>
            <span aria-hidden="true">{STATUS_ICON[s.status]}</span> {STAGE_LABELS[s.stage]}
          </li>
        ))}
      </ol>
      {!busy && <p className="muted">Toplam {seconds} sn</p>}
    </section>
  );
}
