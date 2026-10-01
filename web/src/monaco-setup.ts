// Monaco yerel paketten yüklenir (CDN yok; çevrimdışı çalışır). Yalnızca çekirdek editör ve
// C/C++/C#/Python/HTML/CSS sözdizimi renklendirmesi alınır; dil servisleri paketi şişirir.
import { loader } from "@monaco-editor/react";
import * as monaco from "monaco-editor/editor";
import EditorWorker from "monaco-editor/editor/editor.worker?worker";
import "monaco-editor/languages/definitions/cpp/register";
import "monaco-editor/languages/definitions/csharp/register";
// Faz 16 (ADR-0015): yalnızca Monarch renklendirmesi; HTML/CSS dil servisleri yüklenmez
import "monaco-editor/languages/definitions/css/register";
import "monaco-editor/languages/definitions/html/register";
import "monaco-editor/languages/definitions/python/register";

self.MonacoEnvironment = {
  getWorker: () => new EditorWorker(),
};

loader.config({ monaco });
