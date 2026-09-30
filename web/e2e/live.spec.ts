import { expect, test } from "@playwright/test";
import { fileURLToPath } from "node:url";

// Gerçek uçtan uca doğrulama: `uv run codementor serve` açık ve varsayılan sağlayıcı
// (claude_cli) oturumlu olmalı. Ağ ve kota kullandığı için yalnızca açıkça istenince koşar:
//   CODEMENTOR_E2E_LIVE=1 npx playwright test live
const IMG = fileURLToPath(new URL("../../docs/img/", import.meta.url));

test.skip(!process.env.CODEMENTOR_E2E_LIVE, "CODEMENTOR_E2E_LIVE=1 ile çalışır");
test.setTimeout(240_000);

test("gerçek API ile analiz: rapor gelir, bulgu satırları işaretlenir", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");
  await expect(page.locator(".monaco-editor")).toBeVisible();
  await page.getByRole("button", { name: "Analiz et" }).click();

  const mentor = page.getByRole("region", { name: "Sokratik sorular" });
  await expect(mentor).toBeVisible({ timeout: 200_000 });
  await expect(page.getByRole("region", { name: "Karmaşıklık" })).toContainText("O(");
  await expect(page.locator(".view-overlays .cm-line")).not.toHaveCount(0);
  await expect(page.getByText("yalnızca statik analiz")).toHaveCount(0); // LLM gerçekten yanıt verdi
  await page.screenshot({ path: `${IMG}web-live.png`, fullPage: true });
});
