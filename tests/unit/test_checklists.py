"""Kontrol listesi yükleme ve seçim testleri (mimari §8.3)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

from codementor.models.enums import Engine, Language
from codementor.models.questions import ChecklistFile
from codementor.questions.checklists import DEFAULT_LIMIT, ChecklistError, Checklists


def _item(item_id: str, *tags: str) -> dict[str, Any]:
    return {"id": item_id, "text": f"{item_id} maddesi?", "tags": list(tags)}


def _file(language: str, engine: str | None, items: list[dict[str, Any]]) -> dict[str, Any]:
    applies: dict[str, Any] = {"language": language}
    if engine is not None:
        applies["engine"] = engine
    return {"version": 1, "applies_to": applies, "items": items}


def _write(directory: Path, name: str, data: dict[str, Any]) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f"{name}.yaml").write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )


@pytest.fixture
def checklists(tmp_path: Path) -> Checklists:
    _write(
        tmp_path,
        "csharp",
        _file(
            "csharp",
            None,
            [
                _item("CS-CL-001", "core"),
                _item("CS-CL-002", "gc", "allocation"),
                _item("CS-CL-003", "parsing"),
                _item("CS-CL-004", "gc", "hot-path", "allocation"),
            ],
        ),
    )
    _write(
        tmp_path,
        "unity",
        _file(
            "csharp",
            "unity",
            [
                _item("UNITY-CL-001", "core"),
                _item("UNITY-SO-001", "scriptableobject", "data"),
                _item("UNITY-CL-002", "coroutine", "lifecycle"),
            ],
        ),
    )
    _write(tmp_path, "c", _file("c", None, [_item("C-CL-001", "core"), _item("C-CL-002", "gc")]))
    return Checklists.load(tmp_path)


def _ids(items: list[Any]) -> list[str]:
    return [i.id for i in items]


def test_core_always_included(checklists: Checklists) -> None:
    items = checklists.select_items(Language.CSHARP, Engine.NONE, [])
    assert _ids(items) == ["CS-CL-001"]


def test_tag_intersection(checklists: Checklists) -> None:
    items = checklists.select_items(Language.CSHARP, Engine.NONE, ["parsing"])
    assert _ids(items) == ["CS-CL-001", "CS-CL-003"]


def test_engine_files_merged(checklists: Checklists) -> None:
    items = checklists.select_items(Language.CSHARP, Engine.UNITY, ["scriptableobject", "gc"])
    ids = _ids(items)
    assert {"UNITY-CL-001", "CS-CL-001", "UNITY-SO-001", "CS-CL-002", "CS-CL-004"} == set(ids)
    assert "UNITY-CL-002" not in ids


def test_priority_order(checklists: Checklists) -> None:
    items = checklists.select_items(
        Language.CSHARP, Engine.UNITY, ["gc", "hot-path", "scriptableobject"]
    )
    # 1) core: önce motora özgü, sonra dile özgü
    # 2) kesişim: kesişen etiket sayısı azalan; eşitlikte motor dosyası önce, sonra dosya sırası
    assert _ids(items) == [
        "UNITY-CL-001",
        "CS-CL-001",
        "CS-CL-004",
        "UNITY-SO-001",
        "CS-CL-002",
    ]


def test_other_language_excluded(checklists: Checklists) -> None:
    items = checklists.select_items(Language.C, Engine.NONE, ["gc", "parsing"])
    assert _ids(items) == ["C-CL-001", "C-CL-002"]


def test_engine_specific_file_not_used_for_other_engines(checklists: Checklists) -> None:
    items = checklists.select_items(Language.CSHARP, Engine.NONE, ["scriptableobject"])
    assert "UNITY-SO-001" not in _ids(items)


def test_limit_12(tmp_path: Path) -> None:
    items = [_item(f"CS-CL-{i:03d}", "gc") for i in range(1, 21)]
    _write(tmp_path, "csharp", _file("csharp", None, [_item("CS-CORE-001", "core"), *items]))
    cl = Checklists.load(tmp_path)
    selected = cl.select_items(Language.CSHARP, Engine.NONE, ["gc"])
    assert DEFAULT_LIMIT == 12
    assert len(selected) == 12
    assert selected[0].id == "CS-CORE-001"
    assert len(cl.select_items(Language.CSHARP, Engine.NONE, ["gc"], limit=3)) == 3
    assert cl.select_items(Language.CSHARP, Engine.NONE, ["gc"], limit=0) == []


def test_negative_limit_rejected(checklists: Checklists) -> None:
    with pytest.raises(ValueError, match="limit"):
        checklists.select_items(Language.C, Engine.NONE, [], limit=-1)


def test_no_duplicates_when_core_item_also_tagged(tmp_path: Path) -> None:
    _write(tmp_path, "c", _file("c", None, [_item("C-CL-001", "core", "gc")]))
    items = Checklists.load(tmp_path).select_items(Language.C, Engine.NONE, ["gc"])
    assert _ids(items) == ["C-CL-001"]


def test_duplicate_item_id_error(tmp_path: Path) -> None:
    _write(tmp_path, "c", _file("c", None, [_item("C-CL-001", "core")]))
    _write(tmp_path, "cpp", _file("cpp", None, [_item("C-CL-001", "core")]))
    with pytest.raises(ChecklistError, match="Yinelenen kontrol maddesi 'C-CL-001'"):
        Checklists.load(tmp_path)


def test_invalid_item_id_format(tmp_path: Path) -> None:
    _write(tmp_path, "c", _file("c", None, [_item("c-cl-1", "core")]))
    with pytest.raises(ChecklistError, match=r"c\.yaml") as exc:
        Checklists.load(tmp_path)
    assert "items.0.id" in str(exc.value)


def test_engine_language_mismatch_in_applies_to() -> None:
    with pytest.raises(ValueError, match="motoru"):
        ChecklistFile.model_validate(_file("c", "unity", [_item("C-CL-001", "core")]))


def test_items_need_tags_and_text() -> None:
    with pytest.raises(ValueError, match="tags"):
        ChecklistFile.model_validate(
            _file("c", None, [{"id": "C-CL-001", "text": "x", "tags": []}])
        )
    with pytest.raises(ValueError, match="text"):
        ChecklistFile.model_validate(
            _file("c", None, [{"id": "C-CL-001", "text": "", "tags": ["core"]}])
        )


def test_missing_dir_error(tmp_path: Path) -> None:
    with pytest.raises(ChecklistError, match="bulunamadı"):
        Checklists.load(tmp_path / "yok")


def test_duplicate_item_id_in_same_file(tmp_path: Path) -> None:
    _write(tmp_path, "c", _file("c", None, [_item("C-CL-001", "core"), _item("C-CL-001", "gc")]))
    with pytest.raises(ChecklistError, match=r"'C-CL-001': c\.yaml içinde birden fazla kez"):
        Checklists.load(tmp_path)


def test_plain_string_tags_rejected(checklists: Checklists) -> None:
    with pytest.raises(TypeError, match="etiket listesi"):
        checklists.select_items(Language.CSHARP, Engine.NONE, "gc")


def test_core_items_fill_limit_before_tagged(tmp_path: Path) -> None:
    core = [_item(f"CS-CORE-{i:03d}", "core") for i in range(1, 4)]
    _write(tmp_path, "csharp", _file("csharp", None, [*core, _item("CS-CL-001", "gc")]))
    selected = Checklists.load(tmp_path).select_items(Language.CSHARP, Engine.NONE, ["gc"], limit=3)
    assert _ids(selected) == ["CS-CORE-001", "CS-CORE-002", "CS-CORE-003"]


def test_duplicate_tags_in_item_rejected() -> None:
    with pytest.raises(ValueError, match="yinelenen öğe"):
        ChecklistFile.model_validate(_file("c", None, [_item("C-CL-001", "gc", "gc")]))
