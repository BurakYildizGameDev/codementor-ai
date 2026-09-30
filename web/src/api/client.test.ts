import { report, sseResponse, stage, QUESTIONS } from "../test-fixtures";
import { ApiError, analyzeStream, fetchQuestions } from "./client";

const REQUEST = { code: "int main(){}", language: "c" as const };

afterEach(() => vi.restoreAllMocks());

describe("analyzeStream", () => {
  it("aşama olaylarını sırayla bildirir ve raporu döndürür", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      sseResponse([
        ["stage", stage("tier0", "started")],
        ["stage", stage("tier0", "completed", 3)],
        ["report", report()],
      ]),
    );
    const seen: string[] = [];
    const result = await analyzeStream(REQUEST, (e) => seen.push(`${e.stage}:${e.status}`));
    expect(seen).toEqual(["tier0:started", "tier0:completed"]);
    expect(result.analysis_id).toBe("01TEST");
    const [url, init] = fetchMock.mock.calls[0]!;
    expect(url).toBe("/v1/analyze/stream");
    expect(init?.method).toBe("POST");
    expect(JSON.parse(String(init?.body))).toEqual(REQUEST);
  });

  it("error olayı Türkçe ayrıntıyla ApiError fırlatır", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      sseResponse([["error", { title: "Sağlayıcı yok", status: 503, detail: "Hiçbir sağlayıcı yanıt vermedi." }]]),
    );
    await expect(analyzeStream(REQUEST, () => {})).rejects.toThrow("Hiçbir sağlayıcı yanıt vermedi.");
  });

  it("HTTP 422 problem gövdesindeki doğrulama hatalarını gösterir", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(
        JSON.stringify({ title: "Geçersiz istek", status: 422, errors: ["code: boş olamaz"] }),
        { status: 422, headers: { "Content-Type": "application/problem+json" } },
      ),
    );
    const error = await analyzeStream(REQUEST, () => {}).catch((e: unknown) => e);
    expect(error).toBeInstanceOf(ApiError);
    expect((error as ApiError).message).toContain("code: boş olamaz");
    expect((error as ApiError).status).toBe(422);
  });

  it("rapor gelmeden akış biterse hata verir", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(sseResponse([["stage", stage("tier0", "started")]]));
    await expect(analyzeStream(REQUEST, () => {})).rejects.toThrow("rapor");
  });

  it("ağ hatası kullanıcıya anlaşılır mesaj olur", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new TypeError("Failed to fetch"));
    await expect(analyzeStream(REQUEST, () => {})).rejects.toThrow("API'ye ulaşılamadı");
  });
});

describe("fetchQuestions", () => {
  it("dil ve motora göre sorgu parametresi gönderir", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(new Response(JSON.stringify(QUESTIONS), { status: 200 }));
    const questions = await fetchQuestions("c", "none");
    expect(questions).toHaveLength(1);
    expect(fetchMock.mock.calls[0]![0]).toBe("/v1/questions?language=c&engine=none");
  });
});
