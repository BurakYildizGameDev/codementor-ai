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

interface ItemProps {
  finding: Finding;
  selectedLine: number | null;
  onSelect: (line: number) => void;
}

function FindingItem({ finding: f, selectedLine, onSelect }: ItemProps) {
  return (
    <li>
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
  );
}

/** Bulgu listesi; tıklanınca editör ilgili satıra gider. Faz 36: önce hatalar, öneriler katlı
 * `<details>` içinde (eski raporlarda `kind` yoksa bulgu hatadır). */
export function FindingList({ findings, diagnostics, selectedLine, onSelect }: Props) {
  const errors = diagnostics.filter((d) => d.severity !== "note");
  const issues = findings.filter((f) => f.kind !== "suggestion");
  const suggestions = findings.filter((f) => f.kind === "suggestion");
  const total = issues.length + errors.length;
  return (
    <section className="card" aria-label="Bulgular">
      <h2>Hatalar ({total})</h2>
      {total === 0 && <p className="muted">{suggestions.length ? "Hata yok." : "Bulgu yok."}</p>}
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
        {issues.map((f) => (
          <FindingItem key={f.id} finding={f} selectedLine={selectedLine} onSelect={onSelect} />
        ))}
      </ul>
      {suggestions.length > 0 && (
        <details className="suggestions">
          <summary>Öneriler ({suggestions.length})</summary>
          <ul className="findings">
            {suggestions.map((f) => (
              <FindingItem key={f.id} finding={f} selectedLine={selectedLine} onSelect={onSelect} />
            ))}
          </ul>
        </details>
      )}
    </section>
  );
}
