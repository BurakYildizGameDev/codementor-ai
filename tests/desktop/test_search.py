"""Editör araması (Faz 24): Tk'siz eşleşme mantığı."""

from __future__ import annotations

from codementor.desktop.search import Match, find_all, step


def test_find_all_case_insensitive() -> None:
    assert find_all("Node node NODE", "node") == [Match(1, 0, 4), Match(1, 5, 4), Match(1, 10, 4)]
    assert find_all("Node node", "node", case_sensitive=True) == [Match(1, 5, 4)]


def test_find_all_multiline_positions() -> None:
    text = "int a;\n  free(a);\nfree(b);"
    assert find_all(text, "free(") == [Match(2, 2, 5), Match(3, 0, 5)]
    assert Match(2, 2, 5).start == "2.2"
    assert Match(2, 2, 5).end == "2.7"


def test_find_all_does_not_overlap() -> None:
    assert find_all("aaaa", "aa") == [Match(1, 0, 2), Match(1, 2, 2)]


def test_empty_query_no_matches() -> None:
    assert find_all("abc", "") == []
    assert find_all("", "a") == []


def test_step_wraps() -> None:
    assert step(None, 3, forward=True) == 0
    assert step(None, 3, forward=False) == 2
    assert step(2, 3, forward=True) == 0
    assert step(0, 3, forward=False) == 2
    assert step(1, 0, forward=True) is None
