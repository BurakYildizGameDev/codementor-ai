import { ENGINE_LABELS, LANGUAGES, enginesFor } from "../lib/samples";
import type { QuestionPublic } from "../types/question_public";
import type { Engine, Language } from "../types/request";

interface Props {
  language: Language;
  engine: Engine;
  questionId: string;
  questions: QuestionPublic[];
  busy: boolean;
  onLanguage: (language: Language) => void;
  onEngine: (engine: Engine) => void;
  onQuestion: (id: string) => void;
  onAnalyze: () => void;
}

/** Dil, motor ve soru seçimi + analiz düğmesi. */
export function Controls(props: Props) {
  return (
    <div className="controls">
      <label>
        Dil
        <select
          value={props.language}
          onChange={(e) => props.onLanguage(e.target.value as Language)}
          disabled={props.busy}
        >
          {LANGUAGES.map((l) => (
            <option key={l.value} value={l.value}>
              {l.label}
            </option>
          ))}
        </select>
      </label>
      <label>
        Motor
        <select
          value={props.engine}
          onChange={(e) => props.onEngine(e.target.value as Engine)}
          disabled={props.busy}
        >
          {enginesFor(props.language).map((e) => (
            <option key={e} value={e}>
              {ENGINE_LABELS[e]}
            </option>
          ))}
        </select>
      </label>
      <label className="grow">
        Soru
        <select
          value={props.questionId}
          onChange={(e) => props.onQuestion(e.target.value)}
          disabled={props.busy}
        >
          <option value="">Serbest mod (soru yok)</option>
          {props.questions.map((q) => (
            <option key={q.id} value={q.id}>
              {q.title}
            </option>
          ))}
        </select>
      </label>
      <button type="button" className="primary" onClick={props.onAnalyze} disabled={props.busy}>
        {props.busy ? "Analiz ediliyor…" : "Analiz et"}
      </button>
    </div>
  );
}
