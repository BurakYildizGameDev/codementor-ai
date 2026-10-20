import type { QuestionPublic } from "../types/question_public";

/** Seçili sorunun tanımı, kısıtları ve örnek giriş/çıkışları (Faz J: `sample_io`). */
export function QuestionDetails({ question }: { question: QuestionPublic | undefined }) {
  if (!question) return null;
  const samples = question.sample_io ?? [];
  return (
    <section className="card" aria-label="Soru">
      <h2>{question.title}</h2>
      <p className="question-prompt">{question.prompt}</p>
      <ul>
        {question.constraints.map((c, i) => (
          <li key={i}>{c}</li>
        ))}
      </ul>
      {samples.length > 0 && (
        <details open>
          <summary>Örnekler ({samples.length})</summary>
          {samples.map((s, i) => (
            <div key={i} className="sample-io">
              <span className="muted">Girdi</span>
              <pre>{s.input}</pre>
              <span className="muted">Beklenen çıktı</span>
              <pre>{s.output}</pre>
              {s.explanation && <p className="muted">{s.explanation}</p>}
            </div>
          ))}
        </details>
      )}
    </section>
  );
}
