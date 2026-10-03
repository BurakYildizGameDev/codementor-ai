"""Zig bayrak sondası (Faz 29, ADR-0018): `zig c++ -###` çıktısından `zig clang` bayrakları."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path

import pytest

from codementor.validation import zig as zig_module
from codementor.validation.runner import ProcessLimits, ProcessResult
from codementor.validation.zig import parse_cc1_flags, probe_flags

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "zig"


def _pairs(flags: list[str], option: str) -> list[str]:
    return [flags[i + 1] for i, flag in enumerate(flags[:-1]) if flag == option]


def test_parse_cc1_flags_windows() -> None:
    flags = parse_cc1_flags((FIXTURES / "cc1_windows_cpp.txt").read_text(encoding="utf-8"))
    assert flags is not None
    assert flags[:2] == ["--target=x86_64-unknown-windows-gnu", "-nostdinc"]
    includes = _pairs(flags, "-isystem")
    assert includes[0] == r"C:\Users\ogrenci\.codementor\toolchain\zig\lib\libcxx\include"
    assert any(p.endswith(r"libc\include\any-windows-any") for p in includes)
    assert "_LIBCPP_ABI_VERSION=1" in _pairs(flags, "-D")
    # derleme dışı cc1 ayrıntıları (çıktı dosyası, stdin kopyası, hata ayıklama) taşınmaz
    assert not any("stdin." in f or f.startswith("-fdebug") for f in flags)


def test_parse_cc1_flags_linux() -> None:
    flags = parse_cc1_flags((FIXTURES / "cc1_linux_cpp.txt").read_text(encoding="utf-8"))
    assert flags is not None
    assert flags[0] == "--target=x86_64-unknown-linux5.10.0-gnu2.31.0"
    includes = _pairs(flags, "-isystem")
    assert includes[0] == "/home/ogrenci/.codementor/toolchain/zig/lib/libcxx/include"
    assert all(Path(p).is_absolute() or p.startswith("/") for p in includes)


def test_parse_cc1_rejects_relative_include_path() -> None:
    text = '"zig" "-cc1" "-triple" "x86_64-unknown-linux-gnu" "-isystem" "lib/include"\n'
    assert parse_cc1_flags(text) is None


@pytest.mark.parametrize(
    "text",
    [
        "",
        "clang version 21\nzig: error: bir şey oldu\n",
        '"zig" "-cc1" "-isystem" "/z/lib/include"\n',  # hedef üçlüsü yok
        '"zig" "-cc1" "-triple" "x86_64-unknown-linux-gnu" "-isystem\n',  # bozuk tırnak
        # yalnız -D: sürüm değişip başlık seçeneklerinin adı değişirse zig kullanılmamalı
        '"zig" "-cc1" "-triple" "x86_64-unknown-linux-gnu" "-D" "X=1" "-foo" "/z/lib"\n',
    ],
)
def test_parse_cc1_missing_line_returns_none(text: str) -> None:
    assert parse_cc1_flags(text) is None


class _Runner:
    def __init__(self, result: ProcessResult) -> None:
        self.result = result
        self.calls: list[tuple[list[str], str, dict[str, str]]] = []

    def __call__(
        self,
        argv: Sequence[str],
        stdin: str,
        limits: ProcessLimits,
        *,
        extra_env: Mapping[str, str] | None = None,
        cancel: object = None,
    ) -> ProcessResult:
        self.calls.append((list(argv), stdin, dict(extra_env or {})))
        return self.result


def test_probe_uses_empty_input_and_private_cache() -> None:
    text = (FIXTURES / "cc1_windows_cpp.txt").read_text(encoding="utf-8")
    runner = _Runner(ProcessResult(1, "", text))  # zig -### çıkış kodu 1 olsa da çıktı geçerli
    flags = probe_flags("/z/zig", "c++", timeout_s=5, runner=runner)
    assert flags is not None
    argv, stdin, env = runner.calls[0]
    assert argv[:2] == ["/z/zig", "c++"]
    assert {"-###", "-c", "-"} <= set(argv)  # -c: libc++/mingw kütüphaneleri derlenmez
    assert stdin == ""  # sondaya kullanıcı kodu gitmez
    assert env["ZIG_GLOBAL_CACHE_DIR"] == env["ZIG_LOCAL_CACHE_DIR"]
    assert not Path(env["ZIG_GLOBAL_CACHE_DIR"]).exists()  # geçici önbellek silindi


@pytest.mark.parametrize(
    "result",
    [
        ProcessResult(None, "", "", error="başlatılamadı"),
        ProcessResult(None, "", "", timed_out=True),
        ProcessResult(1, "", "zig: error: unable to resolve zig cache directory\n"),
    ],
)
def test_probe_failure_returns_none(result: ProcessResult) -> None:
    assert probe_flags("/z/zig", "c", timeout_s=5, runner=_Runner(result)) is None


def test_probe_never_raises_when_temp_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    def broken(*_args: object, **_kwargs: object) -> object:
        raise PermissionError("TEMP yazılamıyor")

    monkeypatch.setattr(zig_module.tempfile, "TemporaryDirectory", broken)
    runner = _Runner(ProcessResult(0, "", ""))
    assert probe_flags("/z/zig", "c", timeout_s=5, runner=runner) is None
    assert runner.calls == []
