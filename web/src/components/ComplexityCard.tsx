import type { ComplexityResult } from "../types/report";

const AGREEMENT: Record<ComplexityResult["agreement"], string> = {
  agrees: "statik ipucuyla uyumlu",
  conflicts: "statik ipucuyla çelişiyor",
  no_hint: "statik ipucu yok",
};

/** Big-O, gerekçe adımları ve güven (mimari §5.7, §6.4). */
export function ComplexityCard({ complexity }: { complexity: ComplexityResult | null }) {
  if (!complexity) return null;
  const confidence = Math.round(complexity.confidence * 100);
  return (
    <section className="card" aria-label="Karmaşıklık">
      <h2>Karmaşıklık</h2>
      <p className="bigo">
        <strong>{complexity.display_time}</strong>
        <span className="muted"> zaman · O({complexity.space_complexity}) bellek</span>
      </p>
      <p className="muted">
        Güven %{confidence} · {AGREEMENT[complexity.agreement]}
        {complexity.static_hint ? ` (O(${complexity.static_hint}))` : ""}
      </p>
      {complexity.reasoning_steps.length > 0 && (
        <details open>
          <summary>Gerekçe adımları</summary>
          <ol>
            {complexity.reasoning_steps.map((step, i) => (
              <li key={i}>{step}</li>
            ))}
          </ol>
        </details>
      )}
    </section>
  );
}
