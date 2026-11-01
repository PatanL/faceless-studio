"""Named advisory locks shared with the shell scripts (`flock ~/studio/locks/<name>.lock`).

Lock dir: $STUDIO_LOCKS, else ~/studio/locks when ~/studio exists (the Spark), else <tmp>/studio-locks (Mac).
Known names: code (shared by make steps, exclusive by the Mac rsync), render, make, ytdlp, research_daily, state.
"""
from __future__ import annotations

import contextlib
import fcntl
import os
import tempfile
import time


class LockTimeout(TimeoutError):
    pass


def lock_dir() -> str:
    d = os.environ.get("STUDIO_LOCKS")
    if not d:
        studio = os.path.expanduser("~/studio")
        d = os.path.join(studio, "locks") if os.path.isdir(studio) else os.path.join(tempfile.gettempdir(), "studio-locks")
    os.makedirs(d, exist_ok=True)
    return d


def lock_path(name: str) -> str:
    return name if os.path.isabs(name) else os.path.join(lock_dir(), f"{name}.lock")


@contextlib.contextmanager
def flock(name: str, shared: bool = False, timeout_s: float = 1800):
    """Hold `<lock_dir>/<name>.lock` (or an absolute path). timeout_s=0 means try once.

    Uses flock(2), so it interoperates with `flock(1)` in the shell scripts. Raises LockTimeout.
    """
    path = lock_path(name)
    fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o644)
    mode = fcntl.LOCK_SH if shared else fcntl.LOCK_EX
    deadline = time.monotonic() + max(0.0, timeout_s)
    try:
        while True:
            try:
                fcntl.flock(fd, mode | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise LockTimeout(f"lock {path} busy after {timeout_s:.0f}s")
                time.sleep(0.2)
        yield path
    finally:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)
