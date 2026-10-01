/** CodeMentor REST/SSE API istemcisi (mimari §9). Tipler şemadan üretilmiş dosyalardan gelir. */
import type { Problem } from "../types/problem";
import type { ProviderStatus } from "../types/provider_status";
import type { QuestionPublic } from "../types/question_public";
import type { AnalysisReport } from "../types/report";
import type { AnalysisRequest, Engine, Language } from "../types/request";
import type { StageEvent } from "../types/stage_event";
import { SseParser } from "./sse";

/** Kullanıcıya gösterilecek Türkçe mesajı taşıyan API hatası. */
export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number | null = null,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

const UNREACHABLE = "API'ye ulaşılamadı. `uv run codementor serve` çalışıyor mu?";

function problemMessage(problem: Partial<Problem>): string {
  const parts = [problem.detail ?? problem.title ?? "Bilinmeyen hata"];
  if (problem.errors?.length) parts.push(problem.errors.join("; "));
  return parts.join(" — ");
}

async function request(url: string, init?: RequestInit): Promise<Response> {
  let response: Response;
  try {
    response = await fetch(url, init);
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") throw error;
    throw new ApiError(UNREACHABLE);
  }
  if (!response.ok) {
    const body = (await response.json().catch(() => ({}))) as Partial<Problem>;
    throw new ApiError(problemMessage({ title: `HTTP ${response.status}`, ...body }), response.status);
  }
  return response;
}

/** Soru listesi (referans çözüm içermez). */
export async function fetchQuestions(language: Language, engine: Engine): Promise<QuestionPublic[]> {
  const query = new URLSearchParams({ language, engine });
  const response = await request(`/v1/questions?${query.toString()}`);
  return (await response.json()) as QuestionPublic[];
}

/** Analizi SSE ile çalıştırır: her aşama olayında `onStage`, sonunda rapor. */
export async function analyzeStream(
  body: AnalysisRequest,
  onStage: (event: StageEvent) => void,
  signal?: AbortSignal,
): Promise<AnalysisReport> {
  const response = await request("/v1/analyze/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "text/event-stream" },
    body: JSON.stringify(body),
    signal,
  });
  if (!response.body) throw new ApiError("Sunucu akış döndürmedi.");
  const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
  const parser = new SseParser();
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    for (const event of parser.push(value)) {
      if (event.event === "stage") onStage(JSON.parse(event.data) as StageEvent);
      else if (event.event === "report") return JSON.parse(event.data) as AnalysisReport;
      else if (event.event === "error") {
        const problem = JSON.parse(event.data) as Partial<Problem>;
        throw new ApiError(problemMessage(problem), problem.status ?? null);
      }
    }
  }
  throw new ApiError("Analiz akışı rapor gelmeden kapandı.");
}

/** Yapılandırılmış sağlayıcılar ve hazır olup olmadıkları (Faz 26: web'de seçim). */
export async function fetchProviders(): Promise<ProviderStatus[]> {
  const response = await request("/v1/providers");
  return (await response.json()) as ProviderStatus[];
}

export type ExportFormat = "markdown" | "sarif";

/** Kayıtlı raporun sunucuda üretilen dışa aktarımı (Markdown ya da SARIF). */
export async function fetchExport(analysisId: string, format: ExportFormat): Promise<Blob> {
  const response = await request(`/v1/analyses/${encodeURIComponent(analysisId)}/${format}`);
  return response.blob();
}
