import { defineConfig, devices } from "@playwright/test";

// E2E: gerçek tarayıcıda Monaco + düzen. API `page.route` ile taklit edilir (e2e/app.spec.ts);
// gerçek sağlayıcıyla uçtan uca doğrulama `CODEMENTOR_E2E_LIVE=1` ile (e2e/live.spec.ts).
export default defineConfig({
  testDir: "./e2e",
  timeout: 60_000,
  reporter: "list",
  use: { baseURL: "http://127.0.0.1:5173", ...devices["Desktop Chrome"] },
  webServer: {
    command: "npm run dev",
    url: "http://127.0.0.1:5173",
    reuseExistingServer: true,
    timeout: 60_000,
  },
});
