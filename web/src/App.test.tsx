import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "./App";
import { QUESTIONS, finding, report, sseResponse, stage } from "./test-fixtures";
import type { AnalysisRequest } from "./types/request";

// Monaco jsdom'da çalışmaz; editör düz textarea ile taklit edilir (işaretler markers.test.ts
// ve e2e testinde sınanır).
vi.mock("@monaco-editor/react", () => ({
  default: ({ value, onChange }: { value: string; onChange: (v: string) => void }) => (
    <textarea aria-label="Kod" value={value} onChange={(e) => onChange(e.target.value)} />
  ),
}));

let analyzeBodies: AnalysisRequest[];
let reports: ReturnType<typeof report>[];

beforeEach(() => {
  analyzeBodies = [];
  reports = [
    report(),
    report({
      socratic: {
        key_flaw_concept: "bellek sahipliği",
        hint_level: 2,
        guiding_questions: ["4. satırdaki tmp ne zaman serbest bırakılıyor?"],
        next_step_hint: "free çağrısının yerini düşün.",
        leak_check: "passed",
      },
    }),
  ];
  vi.spyOn(globalThis, "fetch").mockImplementation(async (input, init) => {
    const url = String(input);
    if (url.startsWith("/v1/questions")) {
      const language = new URL(url, "http://x").searchParams.get("language");
      return new Response(JSON.stringify(QUESTIONS.filter((q) => q.language === language)));
    }
    if (url === "/v1/analyze/stream") {
      analyzeBodies.push(JSON.parse(String(init?.body)) as AnalysisRequest);
      return sseResponse([
        ["stage", stage("tier0", "started")],
        ["stage", stage("tier0", "completed", 3)],
        ["stage", stage("llm_a", "completed", 1200)],
        ["report", reports[analyzeBodies.length - 1] ?? reports[1]],
      ]);
    }
    return new Response("{}", { status: 404 });
  });
});

afterEach(() => vi.restoreAllMocks());

async function analyze(user: ReturnType<typeof userEvent.setup>): Promise<void> {
  await user.click(screen.getByRole("button", { name: "Analiz et" }));
  await screen.findByText("O(n)");
}

it("analiz sonrası karmaşıklık, bulgular, sorular ve aşamalar görünür", async () => {
  const user = userEvent.setup();
  render(<App />);
  await analyze(user);

  const complexity = screen.getByRole("region", { name: "Karmaşıklık" });
  expect(within(complexity).getByText("6. satırdaki döngü n kez döner.")).toBeInTheDocument();
  expect(within(complexity).getByText(/%90/)).toBeInTheDocument();

  const findings = screen.getByRole("region", { name: "Bulgular" });
  expect(within(findings).getByText("Ayrılan bellek kimde kalıyor?")).toBeInTheDocument();
  expect(within(findings).getByText(/Satır 4/)).toBeInTheDocument();

  const mentor = screen.getByRole("region", { name: "Sokratik sorular" });
  expect(within(mentor).getByText("Fonksiyon bittiğinde tmp nereye gidiyor?")).toBeInTheDocument();
  expect(within(mentor).getByText(/Seviye 1/)).toBeInTheDocument();

  expect(screen.getByText("Sözdizimi")).toBeInTheDocument();
  expect(analyzeBodies[0]).toMatchObject({ language: "c", engine: "none" });
  expect(analyzeBodies[0]?.session_id).toMatch(/^web-/);
});

it("sonraki ipucu aynı oturum ve soruyla yeniden gönderir, seviye artar", async () => {
  const user = userEvent.setup();
  render(<App />);
  await user.selectOptions(await screen.findByLabelText("Soru"), "c-easy-sum");
  await analyze(user);

  await user.click(screen.getByRole("button", { name: /Sonraki ipucu/ }));
  await screen.findByText("4. satırdaki tmp ne zaman serbest bırakılıyor?");
  expect(screen.getByText(/Seviye 2/)).toBeInTheDocument();
  expect(screen.getByText("free çağrısının yerini düşün.")).toBeInTheDocument();

  expect(analyzeBodies).toHaveLength(2);
  expect(analyzeBodies[1]?.session_id).toBe(analyzeBodies[0]?.session_id);
  expect(analyzeBodies[1]?.question_id).toBe("c-easy-sum");
  expect(analyzeBodies[1]?.code).toBe(analyzeBodies[0]?.code);
});

it("dil değişince soru listesi ve motor seçenekleri süzülür", async () => {
  const user = userEvent.setup();
  render(<App />);
  expect(await screen.findByRole("option", { name: "Dizi toplamı" })).toBeInTheDocument();

  await user.selectOptions(screen.getByLabelText("Dil"), "csharp");
  await waitFor(() =>
    expect(screen.queryByRole("option", { name: "Dizi toplamı" })).not.toBeInTheDocument(),
  );
  const engines = within(screen.getByLabelText("Motor")).getAllByRole("option");
  expect(engines.map((o) => o.getAttribute("value"))).toEqual(["none", "unity"]);
});

it("bulguya tıklamak ilgili satırı seçer", async () => {
  reports[0] = report({ findings: [finding({ id: "F-9", line_start: 4 })] });
  const user = userEvent.setup();
  render(<App />);
  await analyze(user);
  const item = screen.getByRole("button", { name: /Satır 4/ });
  await user.click(item);
  expect(item).toHaveAttribute("aria-pressed", "true");
});

it("API hatası Türkçe mesajla gösterilir", async () => {
  vi.mocked(fetch).mockImplementation(async (input) => {
    if (String(input).startsWith("/v1/questions")) return new Response("[]");
    throw new TypeError("Failed to fetch");
  });
  const user = userEvent.setup();
  render(<App />);
  await user.click(screen.getByRole("button", { name: "Analiz et" }));
  expect(await screen.findByRole("alert")).toHaveTextContent("API'ye ulaşılamadı");
});
