import { Suspense, lazy, useEffect, useMemo, useReducer, useRef, useState } from "react";
import { analyzeStream, fetchProviders, fetchQuestions } from "./api/client";
import { ComplexityCard } from "./components/ComplexityCard";
import { Controls } from "./components/Controls";
import { FindingList } from "./components/FindingList";
import { ReportDownload } from "./components/ReportDownload";
import { SocraticPanel } from "./components/SocraticPanel";
import { StageProgress } from "./components/StageProgress";
import { lineDecorations } from "./lib/markers";
import { initialProgress, progressReducer } from "./lib/progress";
import { SAMPLES, enginesFor, monacoLanguage } from "./lib/samples";
import { getSessionId } from "./lib/session";
import type { ProviderStatus } from "./types/provider_status";
import type { Difficulty, QuestionPublic } from "./types/question_public";
import type { AnalysisReport } from "./types/report";
import { usageLabel } from "./lib/usage";
import type { Engine, Language, PipelineMode } from "./types/request";
import type { StageEvent } from "./types/stage_event";

// Monaco (~3 MB) ayrı parçada; editör görünene kadar iskelet gösterilir (Faz 26)
const CodeEditor = lazy(() => import("./components/CodeEditor"));

type ProgressAction = { type: "reset" } | { type: "event"; event: StageEvent };

function progress(state: typeof initialProgress, action: ProgressAction) {
  return action.type === "reset" ? initialProgress : progressReducer(state, action.event);
}

export default function App() {
  const [language, setLanguage] = useState<Language>("c");
  const [engine, setEngine] = useState<Engine>("none");
  const [questionId, setQuestionId] = useState("");
  const [questions, setQuestions] = useState<QuestionPublic[]>([]);
  const [difficulty, setDifficulty] = useState<Difficulty | "">("");
  const [providers, setProviders] = useState<ProviderStatus[]>([]);
  const [provider, setProvider] = useState("");
  const [mode, setMode] = useState<PipelineMode | "">("");
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

  useEffect(() => {
    let cancelled = false;
    fetchProviders()
      .then((list) => !cancelled && setProviders(list))
      .catch(() => !cancelled && setProviders([]));
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => () => abortRef.current?.abort(), []);

  const decorations = useMemo(
    () =>
      report
        ? lineDecorations(report.findings, report.compilation.diagnostics, code.split("\n").length)
        : [],
    // işaretler analiz edilen koda aittir; yalnızca yeni raporla güncellenir
    [report],
  );

  function changeDifficulty(next: Difficulty | "") {
    setDifficulty(next);
    const selected = questions.find((q) => q.id === questionId);
    if (next && selected && selected.difficulty !== next) setQuestionId("");
  }

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
          provider: provider || null,
          ...(mode ? { options: { mode } } : {}),
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
        difficulty={difficulty}
        providers={providers}
        provider={provider}
        mode={mode}
        busy={busy}
        onLanguage={changeLanguage}
        onEngine={changeEngine}
        onQuestion={setQuestionId}
        onDifficulty={changeDifficulty}
        onProvider={setProvider}
        onMode={setMode}
        onAnalyze={() => void run()}
      />
      <main className="layout">
        <Suspense
          fallback={
            <div className="editor editor-loading" role="status">
              Editör yükleniyor…
            </div>
          }
        >
          <CodeEditor
            value={code}
            language={monacoLanguage(language)}
            decorations={decorations}
            focusLine={selectedLine}
            onChange={setCode}
          />
        </Suspense>
        <aside className="panel">
          {error && (
            <div className="card error" role="alert">
              {error}
            </div>
          )}
          <StageProgress stages={stages} busy={busy} />
          {report && usageLabel(report.meta) && (
            <p className="usage" aria-label="Kullanım">
              {usageLabel(report.meta)}
            </p>
          )}
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
          {report && <ReportDownload report={report} onError={setError} />}
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
