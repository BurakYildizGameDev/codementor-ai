import { expect, test, type Page } from "@playwright/test";
import { fileURLToPath } from "node:url";
import { QUESTIONS, finding, report, stage } from "../src/test-fixtures";

// Ekran görüntüleri README için docs/img/ altına yazılır.
const IMG = fileURLToPath(new URL("../../docs/img/", import.meta.url));
// README GIF'inin kareleri (Faz 26): `uv run python tools/make_demo_gif.py` birleştirir
const FRAMES = fileURLToPath(new URL("../test-results/demo-frames/", import.meta.url));

const REPORT = report({
  findings: [
    finding(),
    finding({
      id: "F-002",
      rule_id: null,
      category: "edge_case",
      severity: "medium",
      line_start: 10,
      evidence: "return sum / n;",
      description: "n = 0 olduğunda bu satırda ne olur?",
      source: "llm",
      confidence: 0.7,
    }),
    finding({
      id: "F-003",
      rule_id: null,
      category: "performance",
      severity: "low",
      line_start: 7,
      evidence: "tmp[i] = values[i] * 2;",
      description: "tmp dizisi hesaplamaya bir şey katıyor mu?",
      source: "llm",
      confidence: 0.7,
    }),
  ],
});

function sse(events: [string, unknown][]): string {
  return events.map(([e, d]) => `event: ${e}\ndata: ${JSON.stringify(d)}\n\n`).join("");
}

async function mockApi(page: Page): Promise<void> {
  await page.route("**/v1/providers", (route) =>
    route.fulfill({
      json: [
        { name: "claude_cli", model: "claude-opus-5-5", ready: true, detail: "hazır" },
        { name: "ollama", model: "qwen2.5-coder:14b", ready: false, detail: "sunucu yok" },
      ],
    }),
  );
  await page.route("**/v1/questions?*", (route) =>
    route.fulfill({ json: QUESTIONS.filter((q) => route.request().url().includes(`language=${q.language}`)) }),
  );
  await page.route("**/v1/analyses*", (route) =>
    route.fulfill({ json: { items: [], next_cursor: null } }),
  );
  await page.route("**/v1/analyze/stream", (route) =>
    route.fulfill({
      status: 200,
      headers: { "Content-Type": "text/event-stream" },
      body: sse([
        ["stage", stage("tier0", "completed", 3)],
        ["stage", stage("tier1", "skipped")],
        ["stage", stage("rules", "completed", 8)],
        ["stage", stage("llm_a", "completed", 17800)],
        ["stage", stage("llm_b", "completed", 6400)],
        ["report", REPORT],
      ]),
    }),
  );
}

test("analiz sonrası bulgu satırları editörde önem derecesine göre işaretli", async ({ page }) => {
  await mockApi(page);
  await page.goto("/");
  await expect(page.locator(".monaco-editor")).toBeVisible();
  await page.getByRole("button", { name: "Analiz et" }).click();
  await expect(page.getByRole("region", { name: "Karmaşıklık" })).toContainText("O(n)");

  await expect(page.locator(".view-overlays .cm-line-high")).toHaveCount(1);
  await expect(page.locator(".view-overlays .cm-line-medium")).toHaveCount(1);
  await expect(page.locator(".view-overlays .cm-line-low")).toHaveCount(1);

  await page.getByRole("button", { name: /Satır 10/ }).click();
  await expect(page.getByRole("button", { name: /Satır 10/ })).toHaveAttribute("aria-pressed", "true");
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.screenshot({ path: `${IMG}web-desktop.png`, fullPage: true });
});

test("mobil genişlikte yatay kaydırma yok, paneller alt alta", async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await mockApi(page);
  await page.goto("/");
  await page.getByRole("button", { name: "Analiz et" }).click();
  await expect(page.getByRole("region", { name: "Sokratik sorular" })).toBeVisible();

  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );
  expect(overflow).toBeLessThanOrEqual(0);

  const editor = await page.getByTestId("editor").boundingBox();
  const mentor = await page.getByRole("region", { name: "Sokratik sorular" }).boundingBox();
  expect(mentor!.y).toBeGreaterThan(editor!.y + editor!.height - 1);
  await page.screenshot({ path: `${IMG}web-mobile.png`, fullPage: true });
});

test("README GIF kareleri: aç → analiz et → bulguya git → indir", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await mockApi(page);
  await page.goto("/");
  await expect(page.locator(".monaco-editor")).toBeVisible();
  const frame = async (n: number) => {
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.screenshot({ path: `${FRAMES}${n}.png` });
  };
  await frame(1);
  await page.getByLabel("Sağlayıcı").selectOption("claude_cli");
  await page.getByRole("combobox", { name: /^Mod/ }).selectOption("two_pass");
  await frame(2);
  await page.getByRole("button", { name: "Analiz et" }).click();
  await expect(page.getByRole("region", { name: "Sokratik sorular" })).toBeVisible();
  await frame(3);
  await page.getByRole("button", { name: /Satır 10/ }).click();
  await expect(page.locator(".view-overlays .cm-line-medium")).toHaveCount(1);
  await frame(4);
  // 1440×900'de indirme kartı da görünür: son kare akışın tamamını gösterir
  await expect(page.getByRole("region", { name: "Raporu indir" })).toBeInViewport();
});

test("geçmiş paneli analizleri listeler ve silme isteği atar (Faz E: E3)", async ({ page }) => {
  let deleteCalled = false;
  await page.route("**/v1/providers", (route) => route.fulfill({ json: [] }));
  await page.route("**/v1/questions?*", (route) => route.fulfill({ json: [] }));
  await page.route("**/v1/analyses*", (route) => {
    if (route.request().method() === "GET") {
      return route.fulfill({
        json: {
          items: [
            {
              analysis_id: "01JTEST1234567890ABCDEFGH",
              created_at: new Date().toISOString(),
              language: "c",
              engine: "none",
              question_id: "c-test-q",
              provider: "claude_cli",
              degraded: false,
              early_exit: false,
              tokens_in: 50,
              tokens_out: 100,
            },
          ],
          next_cursor: null,
        },
      });
    }
    return route.continue();
  });
  await page.route("**/v1/analyses/01JTEST1234567890ABCDEFGH", (route) => {
    if (route.request().method() === "DELETE") {
      deleteCalled = true;
      return route.fulfill({ status: 204 });
    }
    return route.continue();
  });

  const consoleErrors: string[] = [];
  page.on("console", (msg) => {
    if (msg.type() === "error") consoleErrors.push(msg.text());
  });

  await page.goto("/");
  const historyPanel = page.getByRole("region", { name: "Analiz geçmişi" });
  await expect(historyPanel).toBeVisible();
  await expect(historyPanel.getByText("c-test-q")).toBeVisible();

  await historyPanel.getByRole("button", { name: "Sil", exact: true }).click();
  await expect(historyPanel.getByText("c-test-q")).not.toBeVisible();
  expect(deleteCalled).toBe(true);
  expect(consoleErrors.filter((e) => e.includes("Content Security Policy"))).toEqual([]);
});
