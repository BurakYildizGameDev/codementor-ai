import { useEffect, useMemo, useReducer, useRef, useState } from "react";
import { analyzeStream, fetchQuestions } from "./api/client";
import { CodeEditor } from "./components/CodeEditor";
import { ComplexityCard } from "./components/ComplexityCard";
import { Controls } from "./components/Controls";
import { FindingList } from "./components/FindingList";
import { SocraticPanel } from "./components/SocraticPanel";
import { StageProgress } from "./components/StageProgress";
import { lineDecorations } from "./lib/markers";
import { initialProgress, progressReducer } from "./lib/progress";
import { SAMPLES, enginesFor, monacoLanguage } from "./lib/samples";
import { getSessionId } from "./lib/session";
import type { QuestionPublic } from "./types/question_public";
import type { AnalysisReport } from "./types/report";
import type { Engine, Language } from "./types/request";
import type { StageEvent } from "./types/stage_event";

type ProgressAction = { type: "reset" } | { type: "event"; event: StageEvent };

function progress(state: typeof initialProgress, action: ProgressAction) {
  return action.type === "reset" ? initialProgress : progressReducer(state, action.event);
}

export default function App() {
  const [language, setLanguage] = useState<Language>("c");
  const [engine, setEngine] = useState<Engine>("none");
  const [questionId, setQuestionId] = useState("");
  const [questions, setQuestions] = useState<QuestionPublic[]>([]);
  const [code, setCode] = useState(SAMPLES.c);
  const [busy, setBusy] = useState(false);
  const [stages, dispatch] = useReducer(progress, initialProgress);
  const [report, setReport] = useState<AnalysisReport | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedLine, setSelectedLine] = useState<number | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    let cancelled = false;
    fetchQuestions(language, engine)
      .then((list) => !cancelled && setQuestions(list))
      .catch(() => !cancelled && setQuestions([]));
    return () => {
      cancelled = true;
    };
  }, [language, engine]);

  useEffect(() => () => abortRef.current?.abort(), []);

  const decorations = useMemo(
    () =>
      report
        ? lineDecorations(report.findings, report.compilation.diagnostics, code.split("\n").length)
        : [],
    // işaretler analiz edilen koda aittir; yalnızca yeni raporla güncellenir
    [report],
  );

  function changeLanguage(next: Language) {
    if (code === SAMPLES[language]) setCode(SAMPLES[next]);
    setLanguage(next);
    setEngine(enginesFor(next)[0] ?? "none");
    setQuestionId("");
    setReport(null);
  }

  function changeEngine(next: Engine) {
    setEngine(next);
    setQuestionId("");
  }

  async function run() {
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    setBusy(true);
    setError(null);
    setSelectedLine(null);
    dispatch({ type: "reset" });
    try {
      const result = await analyzeStream(
        {
          code,
          language,
          engine,
          question_id: questionId || null,
          session_id: getSessionId(),
        },
        (event) => dispatch({ type: "event", event }),
        controller.signal,
      );
      setReport(result);
    } catch (e) {
      if (e instanceof DOMException && e.name === "AbortError") return;
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      if (abortRef.current === controller) setBusy(false);
    }
  }

  const notes = report ? report.meta.warnings : [];

  return (
    <div className="app">
      <header>
        <h1>CodeMentor AI</h1>
        <p className="muted">Kodu düzeltmez; denetler ve Sokratik sorular sorar.</p>
      </header>
      <Controls
        language={language}
        engine={engine}
        questionId={questionId}
        questions={questions}
        busy={busy}
        onLanguage={changeLanguage}
        onEngine={changeEngine}
        onQuestion={setQuestionId}
        onAnalyze={() => void run()}
      />
      <main className="layout">
        <CodeEditor
          value={code}
          language={monacoLanguage(language)}
          decorations={decorations}
          focusLine={selectedLine}
          onChange={setCode}
        />
        <aside className="panel">
          {error && (
            <div className="card error" role="alert">
              {error}
            </div>
          )}
          <StageProgress stages={stages} busy={busy} />
          {report && (report.meta.degraded || notes.length > 0) && (
            <div className="card notice" role="status">
              {report.meta.degraded && <p>LLM yanıt vermedi; yalnızca statik analiz gösteriliyor.</p>}
              {notes.map((n, i) => (
                <p key={i}>{n}</p>
              ))}
            </div>
          )}
          <SocraticPanel
            socratic={report?.socratic ?? null}
            busy={busy}
            onNextHint={() => void run()}
          />
          <ComplexityCard complexity={report?.complexity ?? null} />
          {report && (
            <FindingList
              findings={report.findings}
              diagnostics={report.compilation.diagnostics}
              selectedLine={selectedLine}
              onSelect={setSelectedLine}
            />
          )}
        </aside>
      </main>
    </div>
  );
}
