/** Bulgular ve derleyici tanıları → Monaco satır dekorasyonları (önem derecesine göre renk).
 * Monaco'ya bağımlı değildir; nesneler `IModelDeltaDecoration` ile yapısal olarak uyumludur. */
import type { Diagnostic, Finding } from "../types/report";

export type Level = Finding["severity"];

export interface LineDecoration {
  range: { startLineNumber: number; startColumn: number; endLineNumber: number; endColumn: number };
  options: {
    isWholeLine: true;
    className: string;
    linesDecorationsClassName: string;
    hoverMessage: { value: string };
  };
}

const DIAGNOSTIC_LEVEL: Partial<Record<Diagnostic["severity"], Level>> = {
  error: "high",
  warning: "medium",
};

const RANK: Record<Level, number> = { low: 1, medium: 2, high: 3 };

function decoration(line: number, level: Level, messages: string[]): LineDecoration {
  return {
    range: { startLineNumber: line, startColumn: 1, endLineNumber: line, endColumn: 1 },
    options: {
      isWholeLine: true,
      className: `cm-line cm-line-${level}`,
      linesDecorationsClassName: `cm-gutter cm-gutter-${level}`,
      hoverMessage: { value: messages.join("\n\n") },
    },
  };
}

/** Satır başına tek dekorasyon: aynı satırdaki bulgulardan en yüksek önem rengi verir (üst üste
 * binen dekorasyonlarda sonuncusu görünür olurdu), mesajlar birleşir. Dosya dışı satırlar atlanır. */
export function lineDecorations(
  findings: Finding[],
  diagnostics: Diagnostic[],
  lineCount: number,
): LineDecoration[] {
  const lines = new Map<number, { level: Level; messages: string[] }>();
  const mark = (line: number, level: Level, message: string) => {
    const current = lines.get(line);
    if (!current) lines.set(line, { level, messages: [message] });
    else {
      current.messages.push(message);
      if (RANK[level] > RANK[current.level]) current.level = level;
    }
  };
  for (const f of findings) {
    if (f.line_start < 1 || f.line_start > lineCount) continue;
    const end = Math.min(Math.max(f.line_end ?? f.line_start, f.line_start), lineCount);
    for (let line = f.line_start; line <= end; line++) {
      mark(line, f.severity, `**${f.category}** — ${f.description}`);
    }
  }
  for (const d of diagnostics) {
    const level = DIAGNOSTIC_LEVEL[d.severity];
    if (level && d.line >= 1 && d.line <= lineCount) mark(d.line, level, `**${d.tool}** — ${d.message}`);
  }
  return [...lines.entries()]
    .sort(([a], [b]) => a - b)
    .map(([line, { level, messages }]) => decoration(line, level, messages));
}
