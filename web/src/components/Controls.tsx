import { ENGINE_LABELS, LANGUAGES, enginesFor } from "../lib/samples";
import type { ProviderStatus } from "../types/provider_status";
import type { QuestionPublic } from "../types/question_public";
import type { Engine, Language, PipelineMode } from "../types/request";

export const MODE_LABELS: Record<PipelineMode, string> = {
  two_pass: "İki geçiş (denetim + mentor)",
  single_pass: "Tek geçiş (hızlı)",
};

interface Props {
  language: Language;
  engine: Engine;
  questionId: string;
  questions: QuestionPublic[];
  providers: ProviderStatus[];
  /** Boş: yapılandırmadaki varsayılan sağlayıcı. */
  provider: string;
  /** Boş: yapılandırmadaki varsayılan mod. */
  mode: PipelineMode | "";
  busy: boolean;
  onLanguage: (language: Language) => void;
  onEngine: (engine: Engine) => void;
  onQuestion: (id: string) => void;
  onProvider: (name: string) => void;
  onMode: (mode: PipelineMode | "") => void;
  onAnalyze: () => void;
}

/** Dil, motor, soru, sağlayıcı ve mod seçimi + analiz düğmesi. */
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
      <label>
        Sağlayıcı
        <select
          value={props.provider}
          onChange={(e) => props.onProvider(e.target.value)}
          disabled={props.busy}
        >
          <option value="">Varsayılan</option>
          {props.providers.map((p) => (
            <option key={p.name} value={p.name} disabled={!p.ready} title={p.detail}>
              {p.ready ? `${p.name} · ${p.model}` : `${p.name} (hazır değil)`}
            </option>
          ))}
        </select>
      </label>
      <label>
        Mod
        <select
          value={props.mode}
          onChange={(e) => props.onMode(e.target.value as PipelineMode | "")}
          disabled={props.busy}
        >
          <option value="">Varsayılan</option>
          {(Object.keys(MODE_LABELS) as PipelineMode[]).map((m) => (
            <option key={m} value={m}>
              {MODE_LABELS[m]}
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
