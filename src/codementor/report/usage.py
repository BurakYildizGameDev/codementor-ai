"""Token ve tahmini maliyet etiketi (mimari §13, Faz 33): CLI, masaüstü ve web aynı metni
gösterir."""

from __future__ import annotations

from codementor.models.report import ReportMeta


def usage_label(meta: ReportMeta) -> str | None:
    """`token 1200/340 (tahmini) · ~$0.0123`; LLM token'ı harcanmadıysa (statik, önbellek) None."""
    if not meta.tokens_in and not meta.tokens_out:
        return None
    label = f"token {meta.tokens_in}/{meta.tokens_out}"
    if meta.usage_estimated:
        label += " (tahmini)"
    if meta.cost_est is not None:
        label += f" · ~${meta.cost_est:.4f}"
    return label
