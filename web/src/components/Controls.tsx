import { ENGINE_LABELS, LANGUAGES, enginesFor } from "../lib/samples";
import type { ProviderStatus } from "../types/provider_status";
import type { Difficulty, QuestionPublic } from "../types/question_public";
import type { Engine, Language, PipelineMode } from "../types/request";

export const DIFFICULTY_LABELS: Record<Difficulty, string> = {
  very_easy: "Çok kolay",
  easy: "Kolay",
  medium: "Orta",
  hard: "Zor",
};

export const MODE_LABELS: Record<PipelineMode, string> = {
  two_pass: "İki geçiş (denetim + mentor)",
  single_pass: "Tek geçiş (hızlı)",
};

interface Props {
  language: Language;
  engine: Engine;
  questionId: string;
  questions: QuestionPublic[];
  /** Boş: tüm zorluklar (Faz 30). */
  difficulty: Difficulty | "";
  providers: ProviderStatus[];
  /** Boş: yapılandırmadaki varsayılan sağlayıcı. */
  provider: string;
  /** Boş: yapılandırmadaki varsayılan mod. */
  mode: PipelineMode | "";
  busy: boolean;
  onLanguage: (language: Language) => void;
  onEngine: (engine: Engine) => void;
  onQuestion: (id: string) => void;
  onDifficulty: (difficulty: Difficulty | "") => void;
  onProvider: (name: string) => void;
  onMode: (mode: PipelineMode | "") => void;
  onAnalyze: () => void;
}

/** Dil, motor, zorluk, soru, sağlayıcı ve mod seçimi + analiz düğmesi. */
export function Controls(props: Props) {
  const visible = props.difficulty
    ? props.questions.filter((q) => q.difficulty === props.difficulty)
    : props.questions;
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
      <label>
        Zorluk
        <select
          value={props.difficulty}
          onChange={(e) => props.onDifficulty(e.target.value as Difficulty | "")}
          disabled={props.busy}
        >
          <option value="">Tümü</option>
          {(Object.keys(DIFFICULTY_LABELS) as Difficulty[]).map((d) => (
            <option key={d} value={d}>
              {DIFFICULTY_LABELS[d]}
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
          {visible.map((q) => (
            <option key={q.id} value={q.id}>
              {q.title} ({DIFFICULTY_LABELS[q.difficulty]})
            </option>
          ))}
        </select>
        {visible.length === 0 && (
          <span className="muted filter-empty">Bu filtrelerle eşleşen soru yok.</span>
        )}
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
