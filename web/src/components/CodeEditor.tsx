import Editor, { type OnMount } from "@monaco-editor/react";
// Monaco yalnız bu modülle (tembel parça) yüklenir; ilk sayfa paketi küçük kalır (Faz 26)
import "../monaco-setup";
import { useEffect, useRef } from "react";
import type { LineDecoration } from "../lib/markers";

type MonacoEditor = Parameters<OnMount>[0];

interface Props {
  value: string;
  language: string;
  decorations: LineDecoration[];
  /** Seçilen bulgunun satırı; değişince editör o satıra kayar. */
  focusLine: number | null;
  onChange: (value: string) => void;
}

/** Monaco editörü; bulgu satırları önem derecesine göre işaretlenir (mimari §5.7). */
export function CodeEditor({ value, language, decorations, focusLine, onChange }: Props) {
  const editorRef = useRef<MonacoEditor | null>(null);
  const collectionRef = useRef<ReturnType<MonacoEditor["createDecorationsCollection"]> | null>(
    null,
  );

  useEffect(() => {
    collectionRef.current?.set(decorations);
  }, [decorations]);

  useEffect(() => {
    const editor = editorRef.current;
    if (!editor || focusLine === null) return;
    editor.revealLineInCenter(focusLine);
    editor.setSelection({
      startLineNumber: focusLine,
      startColumn: 1,
      endLineNumber: focusLine,
      endColumn: editor.getModel()?.getLineMaxColumn(focusLine) ?? 1,
    });
  }, [focusLine]);

  const onMount: OnMount = (editor) => {
    editorRef.current = editor;
    collectionRef.current = editor.createDecorationsCollection(decorations);
  };

  return (
    <div className="editor" data-testid="editor">
      <Editor
        value={value}
        language={language}
        theme="vs-dark"
        onChange={(v) => onChange(v ?? "")}
        onMount={onMount}
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          scrollBeyondLastLine: false,
          automaticLayout: true,
          glyphMargin: false,
          lineDecorationsWidth: 6,
          wordWrap: "on",
        }}
      />
    </div>
  );
}

export default CodeEditor;
