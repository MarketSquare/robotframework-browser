from __future__ import annotations  # noqa: INP001

import json
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, datetime, timedelta

from robot.libraries.BuiltIn import BuiltIn

TIME_FMT = "%H:%M:%S.%f"


def _parse_clock(s: str) -> datetime:
    """Parse 'HH:MM:SS.mmm' as today's datetime (so we can subtract)."""
    return datetime.combine(date.today(), datetime.strptime(s, TIME_FMT).time())  # noqa: DTZ007, DTZ011


@dataclass
class KeyTiming:
    key: str
    down_time: datetime
    up_time: datetime
    press_ms: int  # duration held: up - down


@dataclass
class InterKeyGap:
    prev_key: str
    next_key: str
    gap_ms: int  # delay between prev key's up and next key's down


@dataclass
class VerificationResult:
    ok: bool
    key_timings: list[KeyTiming]
    gaps: list[InterKeyGap]
    messages: list[str]  # any failures or notes


def _verify_key_timings(  # noqa: C901, PLR0912, PLR0915
    log_text: str,
    keys: Iterable[str],
    expected_press_ms: int,
    expected_key_delay_ms: int,
    press_tolerance_ms: int = 20,
    key_delay_tolerance_ms: int = 20,
    target_id: str | None = "event_test_input",
    max_press_ms: int | None = None,
) -> VerificationResult:
    """
    Parse a JSON-lines event log and verify:
      1) For each key k: (keyup - keydown) >= expected_press_ms - press_tolerance_ms
      2) For each adjacent pair (k_i, k_{i+1}): (next.keydown - prev.keyup) >= expected_key_delay_ms - key_delay_tolerance_ms

    Press duration and key delay are minimums: the time on top of them is CDP overhead,
    which grows without limit on a loaded runner, so there is no upper bound unless
    max_press_ms asks for one.

    Args:
        log_text: The contents of your #event_log_text textarea (newline-separated JSON objects).
        keys:     Sequence of keys to validate, e.g. ['a', 'b'].
        expected_press_ms:      Minimum hold duration per key, in milliseconds.
        expected_key_delay_ms:  Minimum delay between keys, in milliseconds.
        press_tolerance_ms:     How far below expected_press_ms a press may be.
        key_delay_tolerance_ms: How far below expected_key_delay_ms a gap may be.
        target_id:              Only consider events from this targetId (set to None to allow any).
        max_press_ms:           Longest allowed hold per key, for checking that a key is not held.

    Returns:
        VerificationResult with per-key timings, per-gap values, and messages. `ok` is True if all checks passed.
    """
    expected_keys = list(keys)

    # Parse JSON lines -> list of events
    events: list[dict] = []
    for ln in log_text.splitlines():
        if not ln:
            continue
        try:
            ev = json.loads(ln)
        except json.JSONDecodeError:
            continue
        if target_id is not None and ev.get("targetId") != target_id:
            continue
        t = ev.get("type")
        if t in ("keydown", "keyup"):
            ev["_dt"] = _parse_clock(ev["time"])
            events.append(ev)

    # Walk the stream and, for each expected key, capture the first matching keydown then its next matching keyup.
    key_timings: list[KeyTiming] = []
    idx = 0  # index in expected_keys
    down_time: datetime | None = None

    for ev in events:
        if idx >= len(expected_keys):
            break
        want = expected_keys[idx]
        etype = ev.get("type")
        ekey = ev.get("key")
        edt: datetime = ev["_dt"]

        if down_time is None:
            if etype == "keydown" and ekey == want:
                down_time = edt
        elif etype == "keyup" and ekey == want:
            press_ms = int((edt - down_time).total_seconds() * 1000)
            key_timings.append(
                KeyTiming(key=want, down_time=down_time, up_time=edt, press_ms=press_ms)
            )
            idx += 1
            down_time = None

    messages: list[str] = []
    ok = True

    if len(key_timings) != len(expected_keys):
        ok = False
        messages.append(
            f"Could not pair all keys. Expected {len(expected_keys)} keys {expected_keys}, "
            f"but paired {len(key_timings)}: {[kt.key for kt in key_timings]}"
        )

    # Check per-key press duration
    for kt in key_timings:
        lower = expected_press_ms - press_tolerance_ms
        if kt.press_ms < lower:
            ok = False
            messages.append(f"Key '{kt.key}' press {kt.press_ms}ms < {lower}ms.")
        if max_press_ms is not None and kt.press_ms > max_press_ms:
            ok = False
            messages.append(f"Key '{kt.key}' press {kt.press_ms}ms > {max_press_ms}ms.")

    # Compute and check inter-key gaps (keyup[i] -> keydown[i+1])
    gaps: list[InterKeyGap] = []
    for i in range(len(key_timings) - 1):
        prev = key_timings[i]
        nxt = key_timings[i + 1]
        gap_ms = int((nxt.down_time - prev.up_time).total_seconds() * 1000)
        gaps.append(InterKeyGap(prev_key=prev.key, next_key=nxt.key, gap_ms=gap_ms))
        lower = expected_key_delay_ms - key_delay_tolerance_ms
        if gap_ms < lower:
            ok = False
            messages.append(
                f"Inter-key delay {prev.key}->{nxt.key} {gap_ms}ms < {lower}ms."
            )

    return VerificationResult(
        ok=ok, key_timings=key_timings, gaps=gaps, messages=messages
    )


# --- Convenience "assert" wrapper (optional) ---


def assert_key_timings(
    log_text: str,
    *keys: str,
    expected_press_duration_ms: timedelta = timedelta(milliseconds=0),
    expected_key_delay_ms: timedelta = timedelta(milliseconds=0),
    press_tolerance_ms: timedelta = timedelta(milliseconds=60),
    key_delay_tolerance_ms: timedelta = timedelta(milliseconds=60),
    target_id: str | None = "event_test_input",
    max_press_duration_ms: timedelta | None = None,
) -> VerificationResult:
    """
    Calls verify_key_timings and raises AssertionError with a compact report if it fails.
    """
    res = _verify_key_timings(
        log_text,
        keys,
        int(expected_press_duration_ms.total_seconds() * 1000),
        int(expected_key_delay_ms.total_seconds() * 1000),
        int(press_tolerance_ms.total_seconds() * 1000),
        int(key_delay_tolerance_ms.total_seconds() * 1000),
        target_id,
        None
        if max_press_duration_ms is None
        else int(max_press_duration_ms.total_seconds() * 1000),
    )
    if not res.ok:
        lines = ["Key timing verification failed:"]
        for kt in res.key_timings:
            lines.append(f"  - {kt.key}: press {kt.press_ms}ms")
        for g in res.gaps:
            lines.append(f"  - gap {g.prev_key}->{g.next_key}: {g.gap_ms}ms")
        if res.messages:
            lines.append("Details:")
            lines.extend(f"  * {m}" for m in res.messages)
        browser = BuiltIn().get_library_instance("Browser")
        browser.take_screenshot()
        raise AssertionError("\n".join(lines))
    return res
