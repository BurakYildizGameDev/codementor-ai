import { expect, test, type Page } from "@playwright/test";
import { fileURLToPath } from "node:url";
import { QUESTIONS, finding, report, stage } from "../src/test-fixtures";

// Ekran görüntüleri README için docs/img/ altına yazılır.
const IMG = fileURLToPath(new URL("../../docs/img/", import.meta.url));

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
  await page.route("**/v1/questions?*", (route) =>
    route.fulfill({ json: QUESTIONS.filter((q) => route.request().url().includes(`language=${q.language}`)) }),
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
