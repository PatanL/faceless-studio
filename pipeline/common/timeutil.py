"""Time helpers. Files store UTC ISO-8601 with a trailing Z; schedules are America/Chicago.

The Spark's /etc/timezone says UTC while `date` prints CST, so nothing here trusts the process time zone:
local times always go through TZ explicitly.
"""
from __future__ import annotations

import datetime as _dt
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Chicago")
UTC = _dt.timezone.utc


def now_utc() -> _dt.datetime:
    return _dt.datetime.now(UTC)


def iso(dt: _dt.datetime | None = None) -> str:
    """UTC ISO-8601 with seconds and a Z suffix. Naive datetimes are taken as UTC."""
    dt = dt or now_utc()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse(s: str) -> _dt.datetime:
    """Parse an ISO string (Z or offset). Naive strings are taken as UTC. Returns an aware UTC datetime."""
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = _dt.datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def to_local(dt: _dt.datetime | None = None, tz: ZoneInfo = TZ) -> _dt.datetime:
    return (dt or now_utc()).astimezone(tz)


def local_date(dt: _dt.datetime | None = None, tz: ZoneInfo = TZ) -> str:
    """YYYY-MM-DD of `dt` (default now) in America/Chicago."""
    return to_local(dt, tz).date().isoformat()


def at_local(date: str, hhmm: str, tz: ZoneInfo = TZ) -> _dt.datetime:
    """UTC datetime of local wall time `hhmm` on local `date` (DST-aware)."""
    d = _dt.date.fromisoformat(date)
    h, m = (int(x) for x in hhmm.split(":"))
    return _dt.datetime(d.year, d.month, d.day, h, m, tzinfo=tz).astimezone(UTC)


def iso_week(dt: _dt.datetime | None = None, tz: ZoneInfo = TZ) -> str:
    """ISO week of the local date, e.g. 2026-W45."""
    y, w, _ = to_local(dt, tz).isocalendar()
    return f"{y}-W{w:02d}"
