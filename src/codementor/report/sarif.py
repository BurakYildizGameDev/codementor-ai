"""SARIF 2.1.0 çıktısı (mimari §5.7): GitHub Code Scanning ve IDE'ler için.

Her `Finding` → `result` (`rule_id` → `ruleId`; kuralı olmayan LLM bulgusu `CM-LLM-<kategori>`),
derleme tanıları → `CM-COMPILE` sonuçları.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from typing import Any

from codementor.models.enums import Severity
from codementor.models.findings import Diagnostic, Finding
from codementor.models.report import AnalysisReport

SARIF_SCHEMA = (
    "https://docs.oasis-open.org/sarif/sarif/v2.1.0/errata01/os/schemas/sarif-schema-2.1.0.json"
)
TOOL_NAME = "CodeMentor AI"
COMPILE_RULE = "CM-COMPILE"
_LEVELS = {Severity.HIGH: "error", Severity.MEDIUM: "warning", Severity.LOW: "note"}
_DIAGNOSTIC_LEVELS = {"error": "error", "warning": "warning", "note": "note"}


def _tool_version() -> str:
    try:
        return version("codementor")
    except PackageNotFoundError:
        return "0.0.0"


def rule_id(finding: Finding) -> str:
    """SARIF `ruleId`: statik kural kimliği ya da LLM kategorisi."""
    return finding.rule_id or f"CM-LLM-{finding.category.value.upper().replace('_', '-')}"


def _location(uri: str, start: int, end: int | None, snippet: str | None) -> dict[str, Any]:
    region: dict[str, Any] = {"startLine": start}
    if end is not None and end >= start:
        region["endLine"] = end
    if snippet:
        region["snippet"] = {"text": snippet}
    return {"physicalLocation": {"artifactLocation": {"uri": uri}, "region": region}}


def _finding_result(finding: Finding, uri: str) -> dict[str, Any]:
    return {
        "ruleId": rule_id(finding),
        "level": _LEVELS[finding.severity],
        "message": {"text": finding.description},
        "locations": [_location(uri, finding.line_start, finding.line_end, finding.evidence)],
        "properties": {
            "findingId": finding.id,
            "category": finding.category.value,
            "source": finding.source.value,
            "confidence": finding.confidence,
        },
    }


def _diagnostic_result(diagnostic: Diagnostic, uri: str) -> dict[str, Any]:
    location = _location(uri, max(1, diagnostic.line), None, None)
    if diagnostic.column:
        location["physicalLocation"]["region"]["startColumn"] = diagnostic.column
    return {
        "ruleId": COMPILE_RULE,
        "level": _DIAGNOSTIC_LEVELS[diagnostic.severity],
        "message": {"text": diagnostic.message},
        "locations": [location],
        "properties": {"tool": diagnostic.tool},
    }


def _rules(report: AnalysisReport) -> list[dict[str, Any]]:
    rules: dict[str, dict[str, Any]] = {}
    for finding in report.findings:
        rid = rule_id(finding)
        rules.setdefault(
            rid,
            {
                "id": rid,
                "shortDescription": {"text": f"{finding.category.value} ({finding.source.value})"},
                "properties": {"category": finding.category.value},
            },
        )
    if report.compilation.diagnostics:
        rules[COMPILE_RULE] = {
            "id": COMPILE_RULE,
            "shortDescription": {"text": "Derleme / sözdizimi tanısı"},
        }
    return list(rules.values())


def to_sarif(report: AnalysisReport, artifact_uri: str) -> dict[str, Any]:
    """Raporu SARIF 2.1.0 günlüğüne çevirir; `artifact_uri` analiz edilen dosyanın yolu."""
    uri = artifact_uri.replace("\\", "/")
    results = [_diagnostic_result(d, uri) for d in report.compilation.diagnostics]
    results += [_finding_result(f, uri) for f in report.findings]
    return {
        "$schema": SARIF_SCHEMA,
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": TOOL_NAME,
                        "version": _tool_version(),
                        "rules": _rules(report),
                    }
                },
                "artifacts": [{"location": {"uri": uri}}],
                "results": results,
                "invocations": [{"executionSuccessful": True}],
                "properties": {
                    "analysisId": report.analysis_id,
                    "compilationStatus": report.compilation.status.value,
                    "degraded": report.meta.degraded,
                    "promptVersion": report.meta.prompt_version,
                    "rulesVersion": report.meta.rules_version,
                },
            }
        ],
    }
