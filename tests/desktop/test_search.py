"""Editör araması (Faz 24): Tk'siz eşleşme mantığı."""

from __future__ import annotations

from codementor.desktop.search import Match, find_all, replace_all, step


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


# --- Faz 33: tam sözcük ve değiştir -------------------------------------------------------


def test_whole_word_skips_identifier_parts() -> None:
    text = "count counter recount count_ count"
    assert find_all(text, "count", whole_word=True) == [Match(1, 0, 5), Match(1, 29, 5)]
    assert len(find_all(text, "count")) == 5


def test_whole_word_with_turkish_letters_and_punctuation() -> None:
    assert find_all("ağaç ağaçlar (ağaç)", "ağaç", whole_word=True) == [
        Match(1, 0, 4),
        Match(1, 14, 4),
    ]


def test_replace_all_respects_options() -> None:
    text = "Node node\nnodes node"
    assert replace_all(text, "node", "Item") == ("Item Item\nItems Item", 4)
    assert replace_all(text, "node", "Item", case_sensitive=True) == ("Node Item\nItems Item", 3)
    assert replace_all(text, "node", "Item", whole_word=True) == ("Item Item\nnodes Item", 3)
    assert replace_all(text, "", "x") == (text, 0)


def test_replace_all_replacement_may_contain_query() -> None:
    """Değiştirilen metin sorguyu içeriyorsa sonsuz döngü ya da çift değiştirme olmaz."""
    assert replace_all("a a", "a", "aa") == ("aa aa", 2)
