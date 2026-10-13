import type { AnalysisPage } from "../types/analysis_page";
import type { DeletedCount } from "../types/deleted_count";
import type { Problem } from "../types/problem";
import type { ProviderStatus } from "../types/provider_status";
import type { QuestionPublic } from "../types/question_public";
import type { AnalysisReport } from "../types/report";
import type { AnalysisRequest, Engine, Language } from "../types/request";
import type { StageEvent } from "../types/stage_event";
import { getApiKey } from "../lib/apiKey";
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
  const headers = new Headers(init?.headers);
  const apiKey = getApiKey();
  if (apiKey) {
    headers.set("X-API-Key", apiKey);
  }
  let response: Response;
  try {
    response = await fetch(url, { ...init, headers });
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") throw error;
    throw new ApiError(UNREACHABLE);
  }
  if (!response.ok) {
    if (response.status === 401) {
      throw new ApiError("API anahtarı gerekli ya da yanlış. Ayarlardan girin.", 401);
    }
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

/** Kayıtlı analizlerin sayfalı listesi (Faz E). */
export async function listAnalyses(limit?: number, before?: string): Promise<AnalysisPage> {
  const params = new URLSearchParams();
  if (limit !== undefined) params.set("limit", String(limit));
  if (before) params.set("before", before);
  const qs = params.toString();
  const response = await request(`/v1/analyses${qs ? `?${qs}` : ""}`);
  return (await response.json()) as AnalysisPage;
}

/** Kimlikle tek bir kayıtlı analizi getirir (Faz E). */
export async function getAnalysis(analysisId: string): Promise<AnalysisReport> {
  const response = await request(`/v1/analyses/${encodeURIComponent(analysisId)}`);
  return (await response.json()) as AnalysisReport;
}

/** Tek bir kayıtlı analizi siler (Faz E). */
export async function deleteAnalysis(analysisId: string): Promise<void> {
  await request(`/v1/analyses/${encodeURIComponent(analysisId)}`, { method: "DELETE" });
}

/** Tüm kayıtlı analizleri siler (Faz E). */
export async function deleteAllAnalyses(): Promise<DeletedCount> {
  const response = await request("/v1/analyses", { method: "DELETE" });
  return (await response.json()) as DeletedCount;
}

