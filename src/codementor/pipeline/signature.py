"""Önbellek anahtarının `pipeline` alanı (mimari §11, Faz B / O3).

Raporu değiştiren her ayar imzaya girer: pipeline modu ve onarım/doğrulama ayarları, kural ve
prompt ayarları, doğrulayıcı eşikleri, Tier 1'in etkin olup olmadığı ve seçilecek derleyici,
soru içeriği. Derleyici sürümü süreç açmadan çalıştırılabilir dosyanın boyutu ve değişiklik
zamanıyla temsil edilir (sürüm yükseltmesi dosyayı değiştirir).

Kontrol listelerinin **içeriği** ve raporu belirleyen kod burada değil `rules_version`'dadır
(`pipeline/versions.py`); aynı bilgiyi burada damgayla tekrarlamak mtime değişiminde gereksiz
önbellek ıskası üretirdi (Faz J4/O3).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from codementor.config import Settings, ValidationSettings
from codementor.models.enums import PipelineMode
from codementor.models.questions import Question
from codementor.models.request import NormalizedCode
from codementor.models.validation import CompilerTool, Toolchain
from codementor.paths import resource_root
from codementor.validation.toolchain import get_toolchain

_DIGEST_CHARS = 16


def _file_stamp(path: str | Path) -> list[int] | None:
    """Dosyanın boyutu ve değişiklik zamanı; yoksa ya da okunamıyorsa None."""
    try:
        info = Path(path).stat()
    except (OSError, ValueError):
        return None
    return [info.st_size, info.st_mtime_ns]


def _reference_stamp(question: Question | None) -> list[int] | None:
    if question is None or not question.reference_solution_path:
        return None
    return _file_stamp(resource_root() / question.reference_solution_path)


def tier1_tool(
    code: NormalizedCode, validation: ValidationSettings, toolchain: Toolchain | None
) -> CompilerTool | None:
    """Tier 1'in bu kod için seçeceği araç (`run_tier1` ile aynı seçim); kapalıysa None."""
    if not validation.tier1_enabled:
        return None
    chain = toolchain if toolchain is not None else get_toolchain(validation)
    return chain.for_code(code.language, code.engine)


def _tool_identity(tool: CompilerTool | None) -> dict[str, Any] | None:
    if tool is None:
        return None
    return {
        "name": tool.name,
        "kind": tool.kind,
        "origin": tool.origin,
        "command": tool.command,
        "files": [_file_stamp(part) for part in tool.command if Path(part).is_absolute()],
    }


def pipeline_signature(
    settings: Settings,
    *,
    mode: PipelineMode,
    validation: ValidationSettings,
    tool: CompilerTool | None,
    question: Question | None,
) -> str:
    """Çıktıyı etkileyen ayarların kararlı özeti; `mod[+verify]:<sha256 öneki>`.

    `validation` isteğe göre düzeltilmiş ayardır (`options.tier1=False` Tier 1'i kapatır).
    """
    pipeline, prompts, verify, rules = (
        settings.pipeline,
        settings.prompts,
        settings.verify,
        settings.rules,
    )
    fields: dict[str, Any] = {
        "max_repair_attempts": pipeline.max_repair_attempts,
        "rules": {"disabled": sorted(set(rules.disabled)), "max_findings": rules.max_findings},
        "prompts": prompts.model_dump(mode="json", exclude={"dir"}),
        "verify": {
            **verify.model_dump(mode="json"),
            "common_identifiers_stamp": _file_stamp(verify.common_identifiers_file),
        },
        "tier1": {
            "enabled": validation.tier1_enabled,
            "compile_timeout_s": validation.compile_timeout_s,
            "compile_memory_mb": validation.compile_memory_mb,
            "stub_header_stamp": _file_stamp(validation.stub_header),
            "tool": _tool_identity(tool),
        },
        # bütçe/kırpmayı ve yanıtı etkileyen sağlayıcı ayarları, sızıntı kontrolünü etkileyen
        # referans çözüm. Kontrol listelerinin *içeriği* `rules_version`'da (Faz J4/O3); burada
        # damga tutmak yalnız mtime değişiminde gereksiz önbellek ıskası üretirdi.
        "providers": settings.providers.model_dump(mode="json"),
        "reference": _reference_stamp(question),
        "question": (
            hashlib.sha256(question.model_dump_json().encode("utf-8")).hexdigest()
            if question is not None
            else None
        ),
    }
    blob = json.dumps(fields, sort_keys=True, ensure_ascii=True, default=str)
    digest = hashlib.sha256(blob.encode("utf-8")).hexdigest()[:_DIGEST_CHARS]
    verify_flag = "+verify" if pipeline.verify_findings else ""
    return f"{mode.value}{verify_flag}:{digest}"
