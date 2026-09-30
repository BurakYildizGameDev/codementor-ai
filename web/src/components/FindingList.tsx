import type { Diagnostic, Finding } from "../types/report";

const SEVERITY_LABEL: Record<Finding["severity"], string> = {
  high: "Yüksek",
  medium: "Orta",
  low: "Düşük",
};

interface Props {
  findings: Finding[];
  diagnostics: Diagnostic[];
  selectedLine: number | null;
  onSelect: (line: number) => void;
}

/** Bulgu listesi; tıklanınca editör ilgili satıra gider. */
export function FindingList({ findings, diagnostics, selectedLine, onSelect }: Props) {
  const errors = diagnostics.filter((d) => d.severity !== "note");
  return (
    <section className="card" aria-label="Bulgular">
      <h2>Bulgular ({findings.length + errors.length})</h2>
      {findings.length + errors.length === 0 && <p className="muted">Bulgu yok.</p>}
      <ul className="findings">
        {errors.map((d, i) => (
          <li key={`d-${i}`}>
            <button
              type="button"
              className="finding sev-high"
              aria-pressed={selectedLine === d.line}
              onClick={() => onSelect(d.line)}
            >
              <span className="finding-head">
                Satır {d.line} · {d.tool} · {d.severity === "error" ? "hata" : "uyarı"}
              </span>
              <span>{d.message}</span>
            </button>
          </li>
        ))}
        {findings.map((f) => (
          <li key={f.id}>
            <button
              type="button"
              className={`finding sev-${f.severity}`}
              aria-pressed={selectedLine === f.line_start}
              onClick={() => onSelect(f.line_start)}
            >
              <span className="finding-head">
                Satır {f.line_start}
                {f.line_end && f.line_end !== f.line_start ? `–${f.line_end}` : ""} ·{" "}
                {SEVERITY_LABEL[f.severity]} · {f.category}
                {f.rule_id ? ` · ${f.rule_id}` : ""}
              </span>
              <span>{f.description}</span>
              <code>{f.evidence}</code>
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}
