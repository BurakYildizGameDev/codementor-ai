/// <reference types="vitest/config" />
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// API (codementor serve) varsayılan olarak 127.0.0.1:8000'de; geliştirmede proxy ile aynı köken.
const API = process.env.CODEMENTOR_API ?? "http://127.0.0.1:8000";

export default defineConfig({
  plugins: [react()],
  // Monaco çekirdeği tek başına ~3 MB (gzip ~770 kB); yerel araç olduğu için kabul edilir.
  build: { chunkSizeWarningLimit: 3500 },
  server: {
    host: "127.0.0.1",
    port: 5173,
    proxy: { "/v1": API, "/health": API },
  },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/test-setup.ts"],
    include: ["src/**/*.test.{ts,tsx}"],
  },
});
