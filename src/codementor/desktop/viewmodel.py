"""Arayüzden bağımsız sunum mantığı: aşama grupları, satır işaretleri, etiketler ve örnekler.

Web UI'daki `web/src/lib/{progress,markers,samples}.ts` mantığının Python karşılığıdır; widget'lar
yalnızca buradaki sonuçları çizer, böylece davranış Tk olmadan test edilir.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from codementor.models.enums import AuditCategory, Difficulty, Engine, Language, Severity
from codementor.models.findings import Diagnostic, Finding
from codementor.models.pipeline import Stage, StageEvent
from codementor.models.report import AnalysisReport
from codementor.report.usage import usage_label

GroupStatus = Literal["pending", "running", "done", "skipped", "failed"]


@dataclass(frozen=True)
class StageGroup:
    key: str
    label: str
    stages: tuple[Stage, ...]


# 16 iç aşama kullanıcıya 6 anlamlı adım olarak gösterilir.
STAGE_GROUPS: tuple[StageGroup, ...] = (
    StageGroup("prepare", "Hazırlık", ("cache", "ingest")),
    StageGroup("compile", "Derleme denetimi", ("tier0", "tier1")),
    StageGroup("static", "Statik analiz", ("facts", "rules")),
    StageGroup(
        "analysis",
        "Derin analiz",
        ("prompt_a", "llm_a", "verify_a", "prompt_v", "llm_v", "verify_v"),
    ),
    StageGroup("mentor", "Mentor soruları", ("prompt_b", "llm_b", "verify_b")),
    StageGroup("report", "Rapor", ("report",)),
)


@dataclass(frozen=True)
class GroupView:
    key: str
    label: str
    status: GroupStatus
    duration_ms: int


@dataclass
class StageTracker:
    """`StageEvent` akışını 6 adımlık zaman çizelgesine çevirir."""

    _status: dict[str, str] = field(default_factory=dict)
    _duration: dict[str, int] = field(default_factory=dict)
    finished: bool = False

    def reset(self) -> None:
        self._status.clear()
        self._duration.clear()
        self.finished = False

    def apply(self, event: StageEvent) -> None:
        self._status[event.stage] = event.status
        self._duration[event.stage] = self._duration.get(event.stage, 0) + event.duration_ms

    def finish(self) -> None:
        """Analiz bitti: hiç olay gelmeyen aşamalar (erken çıkış, önbellek) atlanmış sayılır."""
        self.finished = True

    def groups(self) -> list[GroupView]:
        return [self._view(g) for g in STAGE_GROUPS]

    def completed_ratio(self) -> float:
        """İlerleme çubuğu için 0..1 (koşan adım yarım sayılır)."""
        weights = {"done": 1.0, "skipped": 1.0, "failed": 1.0, "running": 0.5, "pending": 0.0}
        views = self.groups()
        return sum(weights[v.status] for v in views) / len(views)

    def total_ms(self) -> int:
        return sum(self._duration.values())

    def _view(self, group: StageGroup) -> GroupView:
        states = [self._status.get(s) for s in group.stages]
        duration = sum(self._duration.get(s, 0) for s in group.stages)
        return GroupView(group.key, group.label, self._group_status(states), duration)

    def _group_status(self, states: list[str | None]) -> GroupStatus:
        if "failed" in states:
            return "failed"
        if "started" in states:
            return "running"
        seen = [s for s in states if s is not None]
        if not seen:
            return "skipped" if self.finished else "pending"
        if len(seen) < len(states) and not self.finished:
            return "running"
        return "done" if "completed" in seen else "skipped"


# --- Satır işaretleri ------------------------------------------------------------------------

_RANK: dict[Severity, int] = {Severity.LOW: 1, Severity.MEDIUM: 2, Severity.HIGH: 3}
_DIAGNOSTIC_LEVEL: dict[str, Severity] = {"error": Severity.HIGH, "warning": Severity.MEDIUM}


@dataclass
class LineMark:
    line: int
    level: Severity
    messages: list[str]


def line_marks(
    findings: list[Finding], diagnostics: list[Diagnostic], line_count: int
) -> list[LineMark]:
    """Satır başına tek işaret: en yüksek önem rengi, birleşik mesajlar; dosya dışı satır yok."""
    marks: dict[int, LineMark] = {}

    def mark(line: int, level: Severity, message: str) -> None:
        current = marks.get(line)
        if current is None:
            marks[line] = LineMark(line, level, [message])
            return
        current.messages.append(message)
        if _RANK[level] > _RANK[current.level]:
            current.level = level

    for f in findings:
        if not 1 <= f.line_start <= line_count:
            continue
        end = min(max(f.line_end or f.line_start, f.line_start), line_count)
        for line in range(f.line_start, end + 1):
            mark(line, f.severity, f"{CATEGORY_LABELS[f.category]}: {f.description}")
    for d in diagnostics:
        level = _DIAGNOSTIC_LEVEL.get(d.severity)
        if level is not None and 1 <= d.line <= line_count:
            mark(d.line, level, f"{d.tool}: {d.message}")
    return [marks[line] for line in sorted(marks)]


# --- Etiketler -------------------------------------------------------------------------------

LANGUAGE_LABELS: dict[Language, str] = {
    Language.C: "C",
    Language.CPP: "C++",
    Language.CSHARP: "C#",
    Language.PYTHON: "Python",
    Language.HTML: "HTML",
    Language.CSS: "CSS",
}
ENGINE_LABELS: dict[Engine, str] = {
    Engine.NONE: "Motor yok",
    Engine.UNITY: "Unity",
    Engine.UNREAL: "Unreal",
}
SEVERITY_LABELS: dict[Severity, str] = {
    Severity.HIGH: "Yüksek",
    Severity.MEDIUM: "Orta",
    Severity.LOW: "Düşük",
}
DIFFICULTY_LABELS: dict[Difficulty, str] = {
    Difficulty.VERY_EASY: "Çok kolay",
    Difficulty.EASY: "Kolay",
    Difficulty.MEDIUM: "Orta",
    Difficulty.HARD: "Zor",
}
# data/mentor_templates.yaml ile aynı (test eşitliği denetler)
CATEGORY_LABELS: dict[AuditCategory, str] = {
    AuditCategory.MEMORY_SAFETY: "Bellek güvenliği",
    AuditCategory.RESOURCE_LEAK: "Kaynak sızıntısı",
    AuditCategory.UNDEFINED_BEHAVIOR: "Tanımsız davranış",
    AuditCategory.GARBAGE_COLLECTION: "Çöp toplayıcı baskısı",
    AuditCategory.PERFORMANCE: "Performans",
    AuditCategory.ENGINE_BEST_PRACTICE: "Motor kullanımı",
    AuditCategory.EDGE_CASE: "Uç durum",
    AuditCategory.INPUT_HANDLING: "Girdi denetimi",
    AuditCategory.DESIGN: "Tasarım ve mantık",
    AuditCategory.ACCESSIBILITY: "Erişilebilirlik",
    AuditCategory.MAINTAINABILITY: "Bakım kolaylığı",
}
HINT_LEVEL_LABELS: dict[int, str] = {
    1: "Kavramsal ipucu",
    2: "Yönlendirici ipucu",
    3: "Satıra işaret eden ipucu",
}
COMPILATION_LABELS: dict[str, str] = {
    "passed": "Derleme temiz",
    "warning": "Derleme uyarılı",
    "failed": "Derleme hatalı",
    "skipped": "Derleyici yok",
}
MAX_HINT_LEVEL = 3


def engines_for(language: Language) -> list[Engine]:
    """Motor/dil uyumu (mimari §6.2): Unity yalnızca C#, Unreal yalnızca C++."""
    if language is Language.CPP:
        return [Engine.NONE, Engine.UNREAL]
    if language is Language.CSHARP:
        return [Engine.NONE, Engine.UNITY]
    return [Engine.NONE]


_SUFFIXES: dict[str, Language] = {
    ".c": Language.C,
    ".h": Language.C,
    ".cpp": Language.CPP,
    ".cc": Language.CPP,
    ".cxx": Language.CPP,
    ".hpp": Language.CPP,
    ".hh": Language.CPP,
    ".cs": Language.CSHARP,
    ".py": Language.PYTHON,
    ".pyw": Language.PYTHON,
    ".html": Language.HTML,
    ".htm": Language.HTML,
    ".css": Language.CSS,
}
SOURCE_PATTERNS = " ".join(f"*{s}" for s in _SUFFIXES)


def language_for_path(path: str | Path) -> Language | None:
    """Dosya uzantısından dil; bilinmiyorsa None."""
    return _SUFFIXES.get(Path(path).suffix.lower())


def format_ms(ms: int) -> str:
    """`850 ms`, `4.2 sn`, `1 dk 05 sn`."""
    if ms < 1000:
        return f"{ms} ms"
    seconds = ms / 1000
    if seconds < 60:
        return f"{seconds:.1f} sn"
    minutes, rest = divmod(int(seconds), 60)
    return f"{minutes} dk {rest:02d} sn"


def report_usage(report: AnalysisReport) -> str | None:
    """Rapor başlığındaki token/maliyet (Faz 33); LLM harcanmadıysa None."""
    return usage_label(report.meta)


def report_headline(report: AnalysisReport) -> str:
    """Rapor özeti: `3 bulgu · 1 yüksek · Derleme temiz`."""
    parts = [f"{len(report.findings)} bulgu" if report.findings else "Bulgu yok"]
    high = sum(1 for f in report.findings if f.severity is Severity.HIGH)
    if high:
        parts.append(f"{high} yüksek önem")
    parts.append(COMPILATION_LABELS[report.compilation.status.value])
    if report.meta.cache_hit:
        parts.append("önbellekten")
    return " · ".join(parts)


def report_notices(report: AnalysisReport) -> list[str]:
    """Kullanıcının bilmesi gereken durumlar (bozulma, erken çıkış, uyarılar)."""
    notes: list[str] = []
    if report.meta.degraded:
        notes.append("LLM yanıt vermedi; yalnızca statik analiz gösteriliyor.")
    if report.meta.early_exit:
        notes.append("Kod derlenmediği için önce derleme hatasına odaklanıldı.")
    notes.extend(report.meta.warnings)
    return notes


SAMPLES: dict[Language, str] = {
    Language.C: """#include <stdlib.h>

int average(const int *values, int n) {
    int *tmp = malloc(n * sizeof(int));
    int sum = 0;
    for (int i = 0; i < n; i++) {
        tmp[i] = values[i] * 2;
        sum += tmp[i] / 2;
    }
    return sum / n;
}
""",
    Language.CPP: """#include <vector>

bool hasDuplicate(const std::vector<int>& items) {
    for (size_t i = 0; i < items.size(); ++i) {
        for (size_t j = 0; j < items.size(); ++j) {
            if (i != j && items[i] == items[j]) {
                return true;
            }
        }
    }
    return false;
}
""",
    Language.CSHARP: """using System.Collections.Generic;

public static class Scores
{
    public static int CountAbove(List<int> scores, int limit)
    {
        var result = new List<int>();
        foreach (var s in scores)
        {
            if (s > limit) result.Add(s);
        }
        return result.Count;
    }
}
""",
    Language.PYTHON: """def has_duplicate(items):
    seen = []
    for item in items:
        if item in seen:
            return True
        seen.append(item)
    return False
""",
    Language.HTML: """<!DOCTYPE html>
<html>
<body>
  <img src="profil.png">
  <form>
    <input type="email" name="email">
    <button>Gönder</button>
  </form>
</body>
</html>
""",
    Language.CSS: """.kart {
  width: 400px;
  color: #333 !important;
  padding: 16px;
  padding: 24px;
}

.kart:focus {
  outline: none !important;
}

.baslik {}
""",
}
