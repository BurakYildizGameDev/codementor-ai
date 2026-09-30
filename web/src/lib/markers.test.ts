import { finding } from "../test-fixtures";
import type { Diagnostic } from "../types/report";
import { lineDecorations } from "./markers";

describe("lineDecorations", () => {
  it("önem derecesini satır sınıfına eşler", () => {
    const decos = lineDecorations(
      [
        finding({ id: "F-1", severity: "high", line_start: 2 }),
        finding({ id: "F-2", severity: "medium", line_start: 3 }),
        finding({ id: "F-3", severity: "low", line_start: 5 }),
      ],
      [],
      10,
    );
    expect(decos.map((d) => [d.range.startLineNumber, d.options.className])).toEqual([
      [2, "cm-line cm-line-high"],
      [3, "cm-line cm-line-medium"],
      [5, "cm-line cm-line-low"],
    ]);
    expect(decos[0]!.options.isWholeLine).toBe(true);
    expect(decos[0]!.options.hoverMessage.value).toContain("Ayrılan bellek");
  });

  it("line_end varsa aralıktaki her satırı işaretler", () => {
    const decos = lineDecorations([finding({ line_start: 3, line_end: 6 })], [], 10);
    expect(decos.map((d) => d.range.startLineNumber)).toEqual([3, 4, 5, 6]);
  });

  it("aynı satırda birden çok bulgu: en yüksek önem kazanır, mesajlar birleşir", () => {
    const decos = lineDecorations(
      [
        finding({ id: "F-1", severity: "low", line_start: 4, description: "tampon gereksiz" }),
        finding({ id: "F-2", severity: "high", line_start: 4, description: "bellek sızıntısı" }),
      ],
      [],
      10,
    );
    expect(decos).toHaveLength(1);
    expect(decos[0]!.options.className).toBe("cm-line cm-line-high");
    expect(decos[0]!.options.hoverMessage.value).toContain("tampon gereksiz");
    expect(decos[0]!.options.hoverMessage.value).toContain("bellek sızıntısı");
  });

  it("dosya dışına taşan satırlar atlanır ya da kırpılır", () => {
    const decos = lineDecorations(
      [finding({ id: "F-1", line_start: 12 }), finding({ id: "F-2", line_start: 4, line_end: 40 })],
      [],
      10,
    );
    expect(decos.map((d) => d.range.startLineNumber)).toEqual([4, 5, 6, 7, 8, 9, 10]);
  });

  it("derleyici/sözdizimi hataları yüksek önemle işaretlenir, notlar atlanır", () => {
    const diagnostics: Diagnostic[] = [
      { tool: "tree-sitter", severity: "error", line: 7, column: 3, message: "beklenmeyen }" },
      { tool: "gcc", severity: "warning", line: 2, column: null, message: "kullanılmayan değişken" },
      { tool: "gcc", severity: "note", line: 1, column: null, message: "burada tanımlı" },
    ];
    const decos = lineDecorations([], diagnostics, 10);
    expect(decos.map((d) => [d.range.startLineNumber, d.options.className])).toEqual([
      [2, "cm-line cm-line-medium"],
      [7, "cm-line cm-line-high"],
    ]);
  });
});
