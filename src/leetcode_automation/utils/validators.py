
"""Reusable validators for common API data patterns."""
from __future__ import annotations

from datetime import datetime, timezone

# We enforce a strict Zulu/UTC format for simplicity in tests.
ISO_FMT = "%Y-%m-%dT%H:%M:%SZ"


def is_iso_utc(ts: str) -> bool:
    """Return ``True`` if ``ts`` matches ``YYYY-MM-DDTHH:MM:SSZ`` (UTC)."""
    try:
        datetime.strptime(ts, ISO_FMT).replace(tzinfo=timezone.utc)
        return True
    except Exception:
        return False


def not_future(ts: str) -> bool:
    """Return ``True`` if the timestamp is **not** in the future (<= now UTC)."""
    dt = datetime.strptime(ts, ISO_FMT).replace(tzinfo=timezone.utc)
    return dt <= datetime.now(timezone.utc)
