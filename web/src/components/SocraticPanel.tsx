import type { SocraticResult } from "../types/report";

interface Props {
  socratic: SocraticResult | null;
  busy: boolean;
  onNextHint: () => void;
}

const MAX_HINT_LEVEL = 3;

/** Sokratik sorular ve ipucu merdiveni (mimari §5.4.3): "sonraki ipucu" aynı oturumla yeniden
 * gönderir, sunucu seviyeyi bir artırır. */
export function SocraticPanel({ socratic, busy, onNextHint }: Props) {
  if (!socratic) return null;
  const atMax = socratic.hint_level >= MAX_HINT_LEVEL;
  return (
    <section className="card mentor" aria-label="Sokratik sorular">
      <h2>
        Sokratik sorular <span className="badge">Seviye {socratic.hint_level}/3</span>
      </h2>
      <ol>
        {socratic.guiding_questions.map((q, i) => (
          <li key={i}>{q}</li>
        ))}
      </ol>
      {socratic.next_step_hint && <p className="hint">{socratic.next_step_hint}</p>}
      <button type="button" onClick={onNextHint} disabled={busy || atMax}>
        {atMax ? "En yüksek ipucu seviyesi" : "Sonraki ipucu"}
      </button>
    </section>
  );
}
