// Monaco yerel paketten yüklenir (CDN yok; çevrimdışı çalışır). Yalnızca çekirdek editör ve
// C/C++/C# sözdizimi renklendirmesi alınır; TS/CSS/HTML dil servisleri paket boyutunu şişirir.
import { loader } from "@monaco-editor/react";
import * as monaco from "monaco-editor/editor";
import EditorWorker from "monaco-editor/editor/editor.worker?worker";
import "monaco-editor/languages/definitions/cpp/register";
import "monaco-editor/languages/definitions/csharp/register";

self.MonacoEnvironment = {
  getWorker: () => new EditorWorker(),
};

loader.config({ monaco });
