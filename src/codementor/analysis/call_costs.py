"""Bilinen çağrı maliyetleri (mimari §5.3.2, `data/call_costs.yaml`).

Çağrı adı tabloya şu sırayla eşlenir; ilk eşleşen anahtar kullanılır, hiçbiri yoksa
maliyet bilinmez (tahmin yapılmaz):

- Dosyada aynı adla tanımlı bir kullanıcı fonksiyonu varsa niteliksiz çağrı tabloya
  eşlenmez (`int count(int)` → `std::count` değil).
- C: serbest fonksiyon adı (`strlen`).
- C++: nitelikli ad (`std::sort`), `using namespace std` varsa niteliksiz ad da
  (`sort` → `std::sort`); üye çağrısında alıcının bildirilen tipi (`v.push_back` →
  `std::vector::push_back`, `arr.Add` → `TArray::Add`).
- Python (ADR-0015): yerleşik fonksiyon adı (`sorted`); üye çağrısında ek açıklamadan ya da
  değerden çözülen tip (`xs: list` / `xs = []` → `list.insert`); modül çağrısı (`heapq.heappush`).
- C#: alıcının bildirilen tipi (`list.Contains` → `List.Contains`); tipi bilinmeyen,
  büyük harfle başlayan alıcı statik sınıf sayılır (`Array.Sort`, `Mathf.Max`);
  `using System.Linq` varsa LINQ (`Enumerable.*`) yalnızca alıcı bilinen bir koleksiyon
  ya da başka bir çağrının sonucuysa (`xs.Where(...).ToList()`). Argümansız `First`,
  `FirstOrDefault`, `Any` O(1); koleksiyonlarda `Count()` ve listelerde `Last()` de O(1).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import cache
from pathlib import Path

from codementor.analysis._symbols import CallName
from codementor.models.enums import Language
from codementor.models.facts import CallCostTable
from codementor.questions._loader import DataFileError, load_model

_STRING_TYPES = frozenset({"string", "String", "System.String"})
_RECEIVER_PREFIXES = ("this->", "this.", "base.")
CSHARP_COLLECTIONS = frozenset(
    {
        "Array",
        "List",
        "IList",
        "IReadOnlyList",
        "ICollection",
        "IReadOnlyCollection",
        "IEnumerable",
        "HashSet",
        "ISet",
        "SortedSet",
        "Dictionary",
        "IDictionary",
        "SortedDictionary",
        "SortedList",
        "Queue",
        "Stack",
        "LinkedList",
        "ObservableCollection",
    }
)
_INDEXABLE = frozenset({"Array", "List", "IList", "IReadOnlyList"})
_COUNTED = CSHARP_COLLECTIONS - {"IEnumerable"}
_CONSTANT_WITHOUT_ARGS = {
    "Enumerable.First": None,
    "Enumerable.FirstOrDefault": None,
    "Enumerable.Any": None,
    "Enumerable.Count": _COUNTED,
    "Enumerable.Last": _INDEXABLE,
    "Enumerable.LastOrDefault": _INDEXABLE,
}


class CallCostError(DataFileError):
    """`call_costs.yaml` okunamadı veya geçersiz."""


@cache
def load_call_costs(path: Path) -> CallCostTable:
    """Maliyet tablosunu okur ve doğrular (önbellekli)."""
    if not path.is_file():
        raise CallCostError(f"Çağrı maliyeti dosyası bulunamadı: {path}")
    return load_model(path, CallCostTable, CallCostError)


@dataclass(frozen=True)
class CostResolver:
    """Bir dosya için çağrı → (anahtar, maliyet) çözümleyicisi."""

    table: CallCostTable
    language: Language
    types: dict[str, str]
    using_std: bool = False
    using_linq: bool = False
    user_functions: frozenset[str] = field(default_factory=frozenset)

    def _entries(self) -> dict[str, str]:
        return {
            Language.C: self.table.c,
            Language.CPP: self.table.cpp,
            Language.PYTHON: self.table.python,
        }.get(self.language, self.table.csharp)

    def _free(self, call: CallName) -> list[str]:
        if call.method in self.user_functions:
            return []
        if self.language is Language.CPP and self.using_std:
            return [f"std::{call.method}", call.method]
        return [call.method]

    def _csharp_member(self, call: CallName, receiver: str) -> list[str]:
        declared = self.types.get(receiver)
        found: list[str] = []
        if declared is not None:
            found.append(f"{'string' if declared in _STRING_TYPES else declared}.{call.method}")
        elif receiver[:1].isupper():
            found.append(f"{receiver}.{call.method}")  # statik: Array.Sort, GameObject.Find
        collection = declared in CSHARP_COLLECTIONS or call.chained
        if self.using_linq and collection:
            found.append(f"Enumerable.{call.method}")
        return found

    def _candidates(self, call: CallName) -> list[str]:
        receiver = call.receiver
        if receiver is not None:
            for prefix in _RECEIVER_PREFIXES:
                receiver = receiver.removeprefix(prefix)
        if call.qualified is not None:
            return [call.qualified] if self.language is Language.CPP else []
        if receiver is None:
            return self._free(call)
        if self.language is Language.C:
            return []
        if self.language is Language.PYTHON:
            # `xs.insert` → `list.insert` (tip biliniyorsa); `heapq.heappush` modül çağrısı
            declared = self.types.get(receiver.removeprefix("self."))
            return [f"{declared or receiver}.{call.method}"]
        if self.language is Language.CSHARP:
            return self._csharp_member(call, receiver)
        declared = self.types.get(receiver)
        if declared is None:
            return []
        base = declared.removeprefix("std::")
        return [f"std::{base}::{call.method}", f"{base}::{call.method}"]

    def resolve(self, call: CallName) -> tuple[str, str] | None:
        """(tablo anahtarı, maliyet) ya da None."""
        entries = self._entries()
        for candidate in self._candidates(call):
            if candidate not in entries:
                continue
            cost = entries[candidate]
            if candidate in _CONSTANT_WITHOUT_ARGS and call.arg_count == 0:
                allowed = _CONSTANT_WITHOUT_ARGS[candidate]
                receiver = (call.receiver or "").removeprefix("this.")
                if allowed is None or self.types.get(receiver) in allowed:
                    cost = "1"
            return candidate, cost
        return None
