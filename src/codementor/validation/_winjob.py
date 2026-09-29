"""Windows Job Object ile süreç ağacı sınırlama (mimari §5.2.3, ADR-0009).

Süreç `CREATE_SUSPENDED` ile başlatılır, işe atanır, sonra devam ettirilir; böylece
derleyicinin başlattığı alt süreçler (`cc1`, `cc1plus`) de iş içinde doğar ve yarış
penceresi kalmaz. İş şunları sınırlar: toplam commit bellek, etkin süreç sayısı;
`KILL_ON_JOB_CLOSE` ile tanıtıcı kapanınca ağacın tamamı ölür.

Yalnızca Windows'ta içe aktarılır; tüm hatalar `OSError` olarak yükselir. Çağıran bu
durumda süreci öldürür ve Tier 1'i atlar (fail-closed, ADR-0010).
"""

from __future__ import annotations

import ctypes
import sys
from ctypes import wintypes

assert sys.platform == "win32"

CREATE_SUSPENDED = 0x00000004
_JOB_OBJECT_EXTENDED_LIMIT_INFORMATION = 9
_LIMIT_ACTIVE_PROCESS = 0x00000008
_LIMIT_JOB_MEMORY = 0x00000200
_LIMIT_DIE_ON_UNHANDLED_EXCEPTION = 0x00000400
_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
_PROCESS_TERMINATE = 0x0001
_PROCESS_SET_QUOTA = 0x0100
_PROCESS_SUSPEND_RESUME = 0x0800


class _BasicLimits(ctypes.Structure):
    _fields_ = (
        ("PerProcessUserTimeLimit", ctypes.c_int64),
        ("PerJobUserTimeLimit", ctypes.c_int64),
        ("LimitFlags", wintypes.DWORD),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", wintypes.DWORD),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", wintypes.DWORD),
        ("SchedulingClass", wintypes.DWORD),
    )


class _IoCounters(ctypes.Structure):
    _fields_ = tuple((name, ctypes.c_uint64) for name in ("r", "w", "o", "rb", "wb", "ob"))


class _ExtendedLimits(ctypes.Structure):
    _fields_ = (
        ("BasicLimitInformation", _BasicLimits),
        ("IoInfo", _IoCounters),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    )


_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
_ntdll = ctypes.WinDLL("ntdll")
_kernel32.CreateJobObjectW.restype = wintypes.HANDLE
_kernel32.CreateJobObjectW.argtypes = (ctypes.c_void_p, wintypes.LPCWSTR)
_kernel32.SetInformationJobObject.argtypes = (
    wintypes.HANDLE,
    ctypes.c_int,
    ctypes.c_void_p,
    wintypes.DWORD,
)
_kernel32.OpenProcess.restype = wintypes.HANDLE
_kernel32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
_kernel32.AssignProcessToJobObject.argtypes = (wintypes.HANDLE, wintypes.HANDLE)
_kernel32.TerminateJobObject.argtypes = (wintypes.HANDLE, wintypes.UINT)
_kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
_ntdll.NtResumeProcess.argtypes = (wintypes.HANDLE,)
_ntdll.NtResumeProcess.restype = ctypes.c_long


def _check(ok: object, what: str) -> None:
    if not ok:
        raise ctypes.WinError(ctypes.get_last_error(), f"{what} başarısız")


class Job:
    """Bellek ve süreç sayısı sınırlı, kapanınca ağacı öldüren bir Job Object."""

    def __init__(self, memory_bytes: int, max_processes: int) -> None:
        handle = _kernel32.CreateJobObjectW(None, None)
        _check(handle, "CreateJobObject")
        self._handle: int | None = handle
        info = _ExtendedLimits()
        info.BasicLimitInformation.LimitFlags = (
            _LIMIT_ACTIVE_PROCESS
            | _LIMIT_JOB_MEMORY
            | _LIMIT_DIE_ON_UNHANDLED_EXCEPTION
            | _LIMIT_KILL_ON_JOB_CLOSE
        )
        info.BasicLimitInformation.ActiveProcessLimit = max_processes
        info.JobMemoryLimit = memory_bytes
        ok = _kernel32.SetInformationJobObject(
            handle, _JOB_OBJECT_EXTENDED_LIMIT_INFORMATION, ctypes.byref(info), ctypes.sizeof(info)
        )
        if not ok:
            self.close()
            _check(ok, "SetInformationJobObject")

    def assign_and_resume(self, pid: int) -> None:
        """Askıdaki süreci işe atar ve devam ettirir."""
        access = _PROCESS_SET_QUOTA | _PROCESS_TERMINATE | _PROCESS_SUSPEND_RESUME
        process = _kernel32.OpenProcess(access, False, pid)
        _check(process, "OpenProcess")
        try:
            _check(_kernel32.AssignProcessToJobObject(self._handle, process), "AssignProcess")
            if _ntdll.NtResumeProcess(process) != 0:
                raise OSError("NtResumeProcess başarısız")
        finally:
            _kernel32.CloseHandle(process)

    def terminate(self) -> None:
        """İşteki tüm süreçleri öldürür."""
        if self._handle is not None:
            _kernel32.TerminateJobObject(self._handle, 1)

    def close(self) -> None:
        """Tanıtıcıyı kapatır (`KILL_ON_JOB_CLOSE`: kalan süreçler de ölür)."""
        if self._handle is not None:
            _kernel32.CloseHandle(self._handle)
            self._handle = None
