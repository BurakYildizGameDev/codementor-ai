"""`test_bigo.py` için ortak düzenek: sabitler, yardımcılar, fixture'lar."""

from __future__ import annotations

from hypothesis import strategies as st

from codementor.models.bigo import (
    parse_bigo,
)

# ---------------------------------------------------------------- sıralama

CHAIN = ["1", "log n", "n", "n log n", "n^2", "n^3", "2^n", "n!"]


# ---------------------------------------------------------------- hypothesis

_PIECES = [
    "1",
    "7",
    "n",
    "N",
    "n^2",
    "n²",
    "n^3",
    "n^1.5",
    "sqrt(n)",
    "log n",
    "log(n)",
    "lg n",
    "log^2 n",
    "log log n",
    "2^n",
    "3^n",
    "n!",
]


@st.composite
def univariate_texts(draw: st.DrawFn) -> str:
    """Tek değişkenli (n) rastgele Big-O metni: çarpımların toplamı."""
    terms = draw(
        st.lists(
            st.lists(st.sampled_from(_PIECES), min_size=1, max_size=3),
            min_size=1,
            max_size=3,
        )
    )
    sep = draw(st.sampled_from(["*", " ", " * ", "·"]))
    return " + ".join(sep.join(f"({p})" for p in term) for term in terms)


univariates = univariate_texts().map(parse_bigo)
