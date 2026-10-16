<div align="center">

# CodeMentor AI

**A code mentoring engine that never fixes your code: it audits it and asks Socratic questions.**

Static analysis + local compiler + LLM: it finds the bug, withholds the answer, and asks the
questions that lead students to find the problem themselves.

[Türkçe](README.md) · **English**

</div>

> The product, its messages and most documentation are in Turkish (it was built for Turkish
> students). This page is a short English overview.

## Why?

Ask an LLM "what is wrong with my code?" and it usually returns the corrected code. The student
submits it without ever seeing the bug. CodeMentor reverses that flow:

- **Questions instead of solutions.** LLM output never reaches the student directly. Findings
  are verified against the actual source lines, and Socratic questions pass a **leak guard**;
  a question that reveals the solution is regenerated or dropped. Leakage is measured (0%).
- **Deterministic foundation.** Syntax errors, known memory / GC / game-engine pitfalls and a
  Big-O hint are found statically before any LLM call. On a syntax error **the LLM is never
  called**; if the LLM is unavailable the report still comes back from static analysis.
- **Graduated hints.** Each "one more hint" in a session raises the level (1 → 3): concept,
  then line, then direction. The answer is never given.
- **Measured claims.** Every prompt and rule change is evaluated against a hand-labelled set
  (166 samples, dev 96 / test 70); the result tables are generated from result files.

## Highlights

| | |
|---|---|
| **Languages** | C, C++, C#, Python, HTML, CSS + Unity and Unreal engine context |
| **Static rules** | 41 deterministic rules ([catalog, Turkish](docs/rules-catalog.md)) |
| **Pre-validation** | tree-sitter (always) + gcc / clang / Roslyn when installed (or one-click zig) |
| **LLM providers** | Claude Code CLI (default), Codex CLI, Anthropic API, Ollama, Gemini |
| **Interfaces** | Windows desktop app (.exe), web UI (React), CLI, REST API + SSE |
| **Outputs** | JSON · Markdown · SARIF 2.1.0 · Rich terminal panel |
| **Quality** | 3,300+ tests, `mypy --strict`, ruff, Windows + Ubuntu CI, 29 ADRs |

## How it works

1. **K0 Ingest:** normalisation, language/engine detection, size limits.
2. **K1 Pre-validation:** tree-sitter (Tier 0) and the local compiler in syntax-only mode
   (Tier 1). User code is **never executed**; compilers get it via stdin, in an empty temp dir,
   with a sanitised environment and OS resource limits.
3. **K2 Static analysis:** facts (loops, calls, allocations), Big-O hint, 41 rules.
4. **K3–K4 LLM:** pass A (analysis + extra findings) and pass B (mentoring questions), with
   schema repair and an optional finding-verification pass.
5. **K5 Verification:** JSON schema, line evidence, Big-O agreement with the static hint, leak
   guard. A failure in a later pass never discards findings that were already verified.
6. **K6 Report:** one schema rendered as JSON, Markdown, SARIF, web and desktop views.

Details (Turkish): [docs/mimari.md](docs/mimari.md) · decisions: [docs/adr/](docs/adr/).

## Results (summary)

| Metric | Claude Opus (`claude_cli`) | Static only (no LLM) |
|---|---|---|
| Audit P / R / F1, dev 96 | **78 / 96 / 86** | 100 / 55 / 71 |
| Early exit P / R | 100% / 100% | 100% / 100% |
| Solution leakage | 0% | — |
| Prompt-injection resistance | 100% | — |

Static rules are precise but find few issues; the LLM lifts recall from 55% to 92–96%. The
test split was intentionally not re-run after dev tuning (its table is an older measurement).
Small data: one test sample is worth ~2–3 points. Full tables: [README.md](README.md#sonuçlar).

## Quick start

**Desktop (Windows):** download `CodeMentor-<version>-win64.zip` from
[Releases](https://github.com/BurakYildizGameDev/codementor-ai/releases/latest), unzip and run
`CodeMentor.exe` (unsigned: SmartScreen → "More info" → "Run anyway"). Each release ships a
`SHA256SUMS` file. You need one LLM provider; the default is a logged-in
[Claude Code](https://claude.com/claude-code) CLI.

**Web UI + API** (Python 3.12 + [uv](https://docs.astral.sh/uv/), Node.js 20+):

```bash
git clone https://github.com/BurakYildizGameDev/codementor-ai.git
cd codementor-ai
uv sync
uv run codementor serve                # API: http://127.0.0.1:8000/docs
cd web && npm install && npm run dev   # UI:  http://127.0.0.1:5173
```

**CLI:**

```bash
uv run codementor analyze code.c                     # Rich panel
uv run codementor analyze code.cs --engine unity --format sarif --out report.sarif
uv run codementor questions list                     # 64-task question bank
uv run codementor questions add my-task.yaml         # add your own task
```

`analyze` exit codes: 0 done, no high-severity finding · 1 high-severity finding · 2 compilation
failed (early exit) · 3 system error.
API keys are read from environment variables (a `.env` file is intentionally **not** loaded;
see `.env.example`).

## Security

User code is untrusted data: it is never executed, include directives that point outside the
snippet are rejected before the compiler sees them, the code is wrapped as data in the prompt
and delimiter look-alikes are neutralised. The API binds to `127.0.0.1` by default. See
[SECURITY.md](SECURITY.md) for how to report a vulnerability.

## Limitations

Unreal is compiled against a stub header only; C#/Unity Tier 1 is Roslyn syntax parsing. Big-O
is a static hint plus LLM reasoning, not measured runtime. The evaluation is small and mostly
covers two models. The leak guard is heuristic.

## Development

```bash
uv sync
make check          # ruff + mypy --strict + pytest (tests never touch the network)
```

See [CONTRIBUTING.md](CONTRIBUTING.md). License: [MIT](LICENSE).
