import { useState } from "react";
import { type ExportFormat, fetchExport } from "../api/client";
import { saveBlob } from "../lib/download";
import type { AnalysisReport } from "../types/report";

interface Props {
  report: AnalysisReport;
  onError: (message: string) => void;
}

const SERVER_FORMATS: {
  format: ExportFormat;
  label: string;
  ext: string;
  type: string;
}[] = [
  { format: "markdown", label: "Markdown", ext: "md", type: "text/markdown" },
  {
    format: "sarif",
    label: "SARIF",
    ext: "sarif",
    type: "application/sarif+json",
  },
];

/** Raporu JSON (tarayıcıdaki kopya) ya da sunucudan Markdown/SARIF olarak indirir. */
export function ReportDownload({ report, onError }: Props) {
  const [pending, setPending] = useState<ExportFormat | null>(null);
  const base = `codementor-${report.analysis_id}`;

  function saveJson() {
    const text = JSON.stringify(report, null, 2);
    saveBlob(new Blob([text], { type: "application/json" }), `${base}.json`);
  }

  async function saveFromServer(format: ExportFormat, ext: string, type: string) {
    setPending(format);
    try {
      const blob = await fetchExport(report.analysis_id, format);
      saveBlob(new Blob([blob], { type }), `${base}.${ext}`);
    } catch (e) {
      onError(e instanceof Error ? e.message : String(e));
    } finally {
      setPending(null);
    }
  }

  return (
    <section className="card download" aria-label="Raporu indir">
      <h2>Raporu indir</h2>
      <div className="row">
        <button type="button" onClick={saveJson}>
          JSON
        </button>
        {SERVER_FORMATS.map(({ format, label, ext, type }) => (
          <button
            key={format}
            type="button"
            disabled={pending !== null}
            onClick={() => void saveFromServer(format, ext, type)}
          >
            {pending === format ? `${label}…` : label}
          </button>
        ))}
      </div>
    </section>
  );
}
