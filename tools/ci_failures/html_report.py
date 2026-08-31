"""Renders the database as a single self-contained HTML page."""

import html
from datetime import datetime, timezone
from pathlib import Path

from .annotations import known_cause_for, load_known_causes
from .report import (
    FailureGroup,
    FixtureFailure,
    co_failures,
    coverage_by_fixture,
    coverage_by_test,
    failure_groups,
    first_attempt_counts_by_fixture,
    first_attempt_counts_by_test,
    fixture_co_failures,
    fixture_failures,
    latest_run,
    log_messages_by_result,
    neighbouring_fixture_outcomes,
    neighbouring_outcomes,
    occurrences_by_fixture,
    occurrences_by_test,
    pass_durations_by_test,
    platform_breakdown,
    rank_screenshots,
    totals,
    zero_is_inconclusive,
)
from .window import ALL_HISTORY, Window

_FONTS = "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap"

_CSS = r"""
:root {
  color-scheme: light;
  --surface:    #fcfcfb;
  --plane:      #f9f9f7;
  --ink:        #0b0b0b;
  --ink-2:      #52514e;
  --ink-muted:  #898781;
  --rule:       #e1e0d9;
  --baseline:   #c3c2b7;
  --bar:        #2a78d6;
  --bar-soft:   rgba(42, 120, 214, 0.14);
  --critical:   #d03b3b;
  --ring:       rgba(11, 11, 11, 0.10);
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --surface:   #1a1a19;
    --plane:     #0d0d0d;
    --ink:       #ffffff;
    --ink-2:     #c3c2b7;
    --ink-muted: #898781;
    --rule:      #2c2c2a;
    --baseline:  #383835;
    --bar:       #3987e5;
    --bar-soft:  rgba(57, 135, 229, 0.20);
    --critical:  #d03b3b;
    --ring:      rgba(255, 255, 255, 0.10);
  }
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --surface:   #1a1a19;
  --plane:     #0d0d0d;
  --ink:       #ffffff;
  --ink-2:     #c3c2b7;
  --ink-muted: #898781;
  --rule:      #2c2c2a;
  --baseline:  #383835;
  --bar:       #3987e5;
  --bar-soft:  rgba(57, 135, 229, 0.20);
  --critical:  #d03b3b;
  --ring:      rgba(255, 255, 255, 0.10);
}

*, *::before, *::after { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--plane);
  color: var(--ink);
  font-family: "IBM Plex Sans", ui-sans-serif, system-ui, sans-serif;
  font-size: 15px;
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}
.page {
  max-width: 1080px;
  margin: 0 auto;
  padding: 48px 24px 96px;
  display: flex;
  flex-direction: column;
  gap: 40px;
}

header { display: flex; flex-direction: column; gap: 6px; }
h1 {
  margin: 0;
  font-size: 30px;
  font-weight: 600;
  letter-spacing: -0.015em;
  text-wrap: balance;
}
.window {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 13px;
  color: var(--ink-muted);
}
.lede { margin: 0; max-width: 62ch; color: var(--ink-2); }

.tiles {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(148px, 1fr));
  /* Surface, not rule: when the tiles wrap, the cells left over on the last row
     would otherwise show as a block of divider colour. */
  background: var(--surface);
  border: 1px solid var(--rule);
  border-radius: 4px;
  overflow: hidden;
}
.tile {
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  border-right: 1px solid var(--rule);
  border-top: 1px solid var(--rule);
}
.tile:first-child { border-top: none; }
.tile .value {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 26px;
  font-weight: 500;
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.02em;
}
.tile .label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: var(--ink-muted);
}
.tile.is-critical .value { color: var(--critical); }

h2 {
  margin: 0 0 4px;
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--ink-2);
}
.section-note { margin: 0 0 20px; font-size: 13px; color: var(--ink-muted); max-width: 68ch; }

.groups { display: flex; flex-direction: column; gap: 1px; background: var(--rule); border: 1px solid var(--rule); border-radius: 4px; overflow: hidden; }
.group {
  background: var(--surface);
  display: grid;
  grid-template-columns: 132px minmax(0, 1fr);
  gap: 20px;
  padding: 18px 20px;
}
.group:hover { background: color-mix(in srgb, var(--bar) 4%, var(--surface)); }

.magnitude { display: flex; flex-direction: column; gap: 6px; }
.count {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-variant-numeric: tabular-nums;
  font-size: 20px;
  font-weight: 500;
}
.count .of { color: var(--ink-muted); font-size: 13px; }
.track { height: 8px; background: var(--bar-soft); border-radius: 4px; overflow: hidden; }
.fill { height: 100%; background: var(--bar); border-radius: 4px; }
.rate {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-variant-numeric: tabular-nums;
  font-size: 12px;
  color: var(--ink-muted);
}

.identity { display: flex; flex-direction: column; gap: 8px; min-width: 0; }
.testname {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 13.5px;
  font-weight: 500;
  overflow-wrap: anywhere;
}
.suite { color: var(--ink-muted); font-weight: 400; }
.error {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 12.5px;
  color: var(--ink-2);
  background: var(--plane);
  border-left: 2px solid var(--critical);
  padding: 7px 10px;
  border-radius: 0 3px 3px 0;
  overflow-wrap: anywhere;
}
.error.is-empty { border-left-color: var(--baseline); color: var(--ink-muted); font-style: italic; }
.where {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 11.5px;
  color: var(--ink-2);
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.where .k {
  color: var(--ink-muted);
  display: inline-block;
  min-width: 62px;
  padding-right: 10px;
}
.kind {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: 1px solid var(--ring);
  border-radius: 3px;
  padding: 0 5px;
  margin-left: 6px;
  color: var(--ink-muted);
}
.kind[data-kind="library"] { color: var(--bar); border-color: var(--bar); }
.kind[data-kind="project"] { color: var(--ink-2); }

.seen {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 11.5px;
  color: var(--ink-2);
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.seen .k {
  color: var(--ink-muted);
  display: inline-block;
  min-width: 62px;
  padding-right: 10px;
}
.seen .row { display: flex; gap: 10px; }
.seen .cfg { flex: 1; }
.seen .n {
  color: var(--ink-muted);
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

.chips { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.chip {
  font-size: 11.5px;
  padding: 2px 8px;
  border: 1px solid var(--ring);
  border-radius: 3px;
  color: var(--ink-2);
  white-space: nowrap;
}
.chip .k { color: var(--ink-muted); }
.chip.kw { font-family: "IBM Plex Mono", ui-monospace, monospace; }
a.evidence { color: var(--bar); text-decoration: none; font-size: 12px; border-bottom: 1px solid transparent; }
a.evidence:hover, a.evidence:focus-visible { border-bottom-color: var(--bar); }
:focus-visible { outline: 2px solid var(--bar); outline-offset: 2px; }

.thin {
  color: var(--ink-muted);
  font-size: 11px;
  font-style: italic;
  margin-left: 8px;
  border-bottom: 1px dotted var(--baseline);
  cursor: help;
}
.cause {
  font-size: 12.5px;
  color: var(--ink-2);
  background: var(--bar-soft);
  border-left: 2px solid var(--bar);
  padding: 7px 10px;
  border-radius: 0 3px 3px 0;
}
.cause .hd {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: var(--bar);
  font-weight: 600;
}
.cause .ref { color: var(--ink-muted); font-size: 11.5px; }
.oev { margin: 4px 0 2px; }
.oev > summary {
  cursor: pointer;
  font-size: 11.5px;
  color: var(--ink-muted);
  list-style: none;
}
.oev > summary::-webkit-details-marker { display: none; }
.oev > summary::before { content: "\25B8  "; }
.oev[open] > summary::before { content: "\25BE  "; }
.oev > summary:hover { color: var(--bar); }

.log { display: flex; flex-direction: column; gap: 0; margin-top: 2px; }
.logline {
  display: grid;
  grid-template-columns: 52px minmax(0, 1fr);
  gap: 10px;
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 11.5px;
  line-height: 1.5;
  padding: 2px 0;
  color: var(--ink-2);
}
.logline .lv {
  font-size: 10px;
  letter-spacing: 0.04em;
  color: var(--ink-muted);
  text-transform: uppercase;
  padding-top: 1px;
}
.logline .lv[data-level="FAIL"] { color: var(--critical); }
.logline .lv[data-level="WARN"] { color: var(--critical); }
.logline .txt { overflow-wrap: anywhere; white-space: pre-wrap; }
.logline.gap .txt { color: var(--ink-muted); }

.shots {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 11.5px;
  color: var(--ink-2);
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.shots .k {
  color: var(--ink-muted);
  display: inline-block;
  min-width: 62px;
  padding-right: 10px;
}
.shots .none { color: var(--ink-muted); font-style: italic; }
.origin {
  font-size: 11px;
  color: var(--ink-muted);
  padding: 4px 0 2px;
  font-style: italic;
}
details.more > summary {
  cursor: pointer;
  font-size: 11.5px;
  color: var(--ink-muted);
  padding: 3px 0;
  list-style: none;
  width: fit-content;
}
details.more > summary::-webkit-details-marker { display: none; }
details.more > summary::before { content: "\25B8  "; }
details.more[open] > summary::before { content: "\25BE  "; }
details.more > summary:hover { color: var(--ink-2); }

.affected {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 11.5px;
  color: var(--ink-muted);
  overflow-wrap: anywhere;
}
.scope {
  display: inline-block;
  font-size: 10.5px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--critical);
  border: 1px solid var(--critical);
  border-radius: 3px;
  padding: 1px 6px;
  margin-bottom: 6px;
}

.platforms { display: flex; flex-direction: column; gap: 1px; background: var(--rule); border: 1px solid var(--rule); border-radius: 4px; overflow: hidden; }
.prow { background: var(--surface); display: grid; grid-template-columns: 92px minmax(0, 1fr) 132px; gap: 16px; align-items: center; padding: 12px 20px; }
.pname { font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: 13px; }
.pnum { font-family: "IBM Plex Mono", ui-monospace, monospace; font-variant-numeric: tabular-nums; font-size: 12px; color: var(--ink-2); text-align: right; }
.ptrack { height: 10px; background: var(--bar-soft); border-radius: 4px; overflow: hidden; }
.pfill { height: 100%; background: var(--bar); border-radius: 4px; }

.empty { background: var(--surface); border: 1px solid var(--rule); border-radius: 4px; padding: 40px 24px; text-align: center; color: var(--ink-muted); }

footer { border-top: 1px solid var(--rule); padding-top: 16px; font-size: 12px; color: var(--ink-muted); display: flex; flex-direction: column; gap: 4px; }
code { font-family: "IBM Plex Mono", ui-monospace, monospace; }

.seen .n.is-clean { color: var(--baseline); }
.seen .ms { color: var(--ink-muted); font-size: 11px; white-space: nowrap; }
.never { font-size: 12px; color: var(--ink-muted); font-style: italic; }
.first { font-size: 11px; color: var(--ink-muted); font-variant-numeric: tabular-nums; }

.occ { display: flex; flex-direction: column; gap: 6px; border-top: 1px dashed var(--rule); padding-top: 10px; }
.occ .hd { font-size: 11px; letter-spacing: 0.04em; text-transform: uppercase; color: var(--ink-muted); }
.orow { display: flex; flex-wrap: wrap; gap: 6px; align-items: baseline; font-size: 12px; }
.odate, .oleg { font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: 11px; }
.oleg { color: var(--ink-2); }
.otag {
  font-size: 11px; line-height: 1.7; padding: 0 6px; border-radius: 3px;
  border: 1px solid var(--rule); color: var(--ink-muted); white-space: nowrap;
}
.otag.is-rerun { color: var(--bar); border-color: var(--bar); }
.otag.is-bad { color: var(--critical); border-color: var(--critical); }
.oalso { font-size: 11px; color: var(--ink-muted); padding-left: 2px; overflow-wrap: anywhere; }
.omore { font-size: 11px; color: var(--ink-muted); font-style: italic; }

@media (max-width: 640px) {
  .group { grid-template-columns: 1fr; gap: 12px; }
  .page { padding: 32px 16px 64px; }
}
"""


def _e(value: object) -> str:
    return html.escape(str(value)) if value is not None else ""


def _tile(value: object, label: str, critical: bool = False) -> str:
    return (
        f'<div class="tile{" is-critical" if critical else ""}">'
        f'<span class="value">{_e(value)}</span>'
        f'<span class="label">{_e(label)}</span></div>'
    )


SHOWN_LOG_LINES = 3
# Levels that must never sit behind a disclosure: they are the conclusion.
_LOUD_LEVELS = {"FAIL", "WARN", "ERROR"}


def _skipped_before(entries: list[dict], shown: list[dict], index: int) -> bool:
    """Whether lines were passed over between this shown line and the one before."""
    previous = entries.index(shown[index - 1])
    current = entries.index(shown[index])
    return current - previous > 1


def _log_line(entry: dict, skipped: bool = False) -> str:
    level = entry.get("level") or ""
    gap = (
        '<div class="logline gap"><span class="lv"></span><span class="txt">...</span></div>'
        if skipped
        else ""
    )
    return (
        f'{gap}<div class="logline"><span class="lv" data-level="{_e(level)}">{_e(level)}</span>'
        f'<span class="txt">{_e(entry.get("message"))}</span></div>'
    )


def _origin_note(origin: str) -> str:
    return f'<div class="origin">from the {_e(origin)}, not from the test itself</div>'


def _log_html(entries: list[dict]) -> str:
    """The opening lines and every FAIL or WARN, with the rest behind a disclosure.

    Chronological, which is how they were logged, but the line that names the
    failure is usually near the end rather than the start - the opening lines
    tend to be timeout bookkeeping and dumps - so it is never behind a click.
    """
    if not entries:
        return ""
    origins = {e.get("origin") for e in entries if e.get("origin")}
    note = _origin_note(sorted(origins)[0]) if len(origins) == 1 else ""
    visible = {id(e) for e in entries[:SHOWN_LOG_LINES]}
    visible |= {id(e) for e in entries if (e.get("level") or "") in _LOUD_LEVELS}
    shown_entries = [e for e in entries if id(e) in visible]
    rest = [e for e in entries if id(e) not in visible]
    shown = note + "".join(
        _log_line(
            entry, skipped=index > 0 and _skipped_before(entries, shown_entries, index)
        )
        for index, entry in enumerate(shown_entries)
    )
    if not rest:
        return f'<div class="log">{shown}</div>'
    notable = sum(1 for e in rest if (e.get("level") or "") in {"FAIL", "WARN"})
    tail = f", {notable} of them FAIL or WARN" if notable else ""
    return (
        f'<div class="log">{shown}'
        f'<details class="more"><summary>{len(rest)} more line'
        f"{'' if len(rest) == 1 else 's'}{tail}</summary>"
        f"{''.join(_log_line(e) for e in rest)}</details></div>"
    )


def _screenshots_html(screenshots: str | None, status: str | None) -> str:
    """Where the pictures are, or why there are none.

    A screenshot is often the quickest way to see what was on screen when a
    keyword failed. When there is none that is a clue in itself: the library
    takes one automatically, so "could not" usually means there was no page.
    """
    if status == "file" and screenshots:
        paths = [path for path in screenshots.split(",") if path]
        rows = [
            f'<div><span class="k">{_e("screenshot" if index == 0 else "")}</span>{_e(path)}</div>'
            for index, path in enumerate(paths)
        ]
        rows.append(
            '<div><span class="k"></span>'
            '<span class="none">paths are inside the artifact</span></div>'
        )
        return f'<div class="shots">{"".join(rows)}</div>'
    if status == "embedded":
        return (
            '<div class="shots"><div><span class="k">screenshot</span>'
            '<span class="none">embedded in log.html only, not saved as a file</span>'
            "</div></div>"
        )
    if status == "unavailable":
        return (
            '<div class="shots"><div><span class="k">screenshot</span>'
            '<span class="none">none - the library could not take one, so there was '
            "probably no page open</span></div></div>"
        )
    return ""


SHOWN_OCCURRENCES = 5


def _configuration_label(configuration: dict) -> str:
    parts = [configuration.get("platform") or "?"]
    for label, key in (
        ("rf", "rf_version"),
        ("py", "python_version"),
        ("node", "node_version"),
    ):
        value = configuration.get(key)
        if value:
            parts.append(f"{label} {value}")
    return " &middot; ".join(parts)


def _rates_html(
    coverage: list[dict],
    never_ran_on: list[str],
    durations: dict[tuple, dict] | None = None,
    longname: str | None = None,
    overall_rate: float = 0.0,
) -> str:
    """Every matrix leg that ran this, with its denominator.

    One line per combination, not one list per dimension: "rf 7.1.1, 7.4.2"
    beside "py 3.13.15, 3.14.7" reads as four combinations when only two ever
    ran, and when each version pair is a whole matrix leg the two dimensions
    cannot be told apart at all.

    Configurations that never failed are kept, greyed rather than dropped. 3 of
    81 says nothing; 3 of 55 on linux against 0 of 26 on darwin says where to
    look, and the clean 26 is half of that sentence. A configuration missing
    from the list never ran this at all, which is the opposite finding to a
    zero, so it gets its own line.

    Where the passing runs have durations they follow the rate. For a timeout,
    whether they cluster far below the limit or run up against it is the
    difference between a keyword that broke and a budget that was too thin.

    A clean configuration that has not run often enough to mean anything says
    so. `0 of 25` against a one-in-twenty failure is what a configuration
    exactly as broken as the rest would show more than half the time, and the
    move it invites - "it only breaks on linux, look at what linux does" - is
    only sound if the zero is evidence.
    """
    if not coverage and not never_ran_on:
        return ""
    rows = []
    for index, configuration in enumerate(coverage):
        failed = configuration.get("failed") or 0
        ran = configuration.get("ran") or 0
        spread = ""
        if durations is not None and longname is not None:
            measured = durations.get(
                (
                    longname,
                    configuration.get("platform"),
                    configuration.get("python_version"),
                    configuration.get("rf_version"),
                    configuration.get("node_version"),
                )
            )
            if measured:
                spread = (
                    f'<span class="ms">passes {measured["min"]}&ndash;'
                    f"{measured['max']} ms</span>"
                )
        thin = "" if failed else zero_is_inconclusive(ran, overall_rate)
        if thin:
            spread += (
                f'<span class="thin" title="A configuration failing as often as '
                f"the rest would still show nothing here "
                f'{thin["would_look_clean_anyway"]:.0%} of the time.">'
                f"too few to call ({thin['runs_for_a_meaningful_zero']} needed)</span>"
            )
        rows.append(
            f'<div class="row"><span class="k">{"ran on" if not index else ""}</span>'
            f'<span class="cfg">{_e(_configuration_label(configuration))}</span>'
            f'<span class="n{"" if failed else " is-clean"}">{failed} of {ran}</span>'
            f"{spread}</div>"
        )
    if never_ran_on:
        rows.append(
            f'<div class="row"><span class="k"></span>'
            f'<span class="never">never ran on {_e(", ".join(never_ran_on))}</span>'
            "</div>"
        )
    return f'<div class="seen">{"".join(rows)}</div>'.replace(
        "&amp;middot;", "&middot;"
    ).replace("&amp;ndash;", "&ndash;")


def _leg_label(name: str | None) -> str:
    return (name or "?").replace("Test results-", "")


def _cause_html(cause: dict | None) -> str:
    """What is already known, where a group has been worked out before.

    Placed above the evidence rather than below it, because it changes what the
    reader should do with the rest: an explained group does not want
    re-investigating, it wants its fix verified.
    """
    if not cause or not cause.get("cause"):
        return ""
    bits = []
    if cause.get("reference"):
        bits.append(f"see {_e(cause['reference'])}")
    if cause.get("recorded"):
        bits.append(f"recorded {_e(cause['recorded'])}")
    if cause.get("fixed_by"):
        verified = cause.get("fix_verified")
        bits.append(
            f"fixed by {_e(cause['fixed_by'])}, verified {_e(verified)}"
            if verified
            else f"fixed by {_e(cause['fixed_by'])} - not yet verified in CI"
        )
    tail = f'<div class="ref">{" &middot; ".join(bits)}</div>' if bits else ""
    return (
        f'<div class="cause"><div class="hd">known cause</div>'
        f"{_e(cause['cause'])}{tail}</div>"
    )


def _evidence_html(entry: dict, logs: dict | None) -> str:
    """What this one occurrence logged, and which pictures it left behind."""
    if logs is None:
        return ""
    lines = logs.get(entry.get("result_id")) or []
    ranked = rank_screenshots(
        [p for p in (entry.get("screenshots") or "").split(",") if p], lines
    )
    body = _log_html(lines) + _screenshots_html(
        ",".join(ranked), entry.get("screenshot_status")
    )
    if not body:
        return ""
    return (
        f'<details class="oev"><summary>what this one logged</summary>{body}</details>'
    )


def _occurrences_html(
    entries: list[dict], around_for, alongside_for, logs: dict | None = None
) -> str:
    """Each individual failure, and what surrounded it.

    The counts describe a group. These describe one execution: which leg ran it,
    which attempt that was, what the same leg did in the runs either side, and
    what else broke alongside. A rate cannot say whether a failure was a blip on
    a leg that is otherwise healthy or the point where something broke and
    stayed broken, and those want opposite responses.

    Each row carries its own log lines and its own screenshots, because the
    occurrences of one group do not have to agree. Four failures of
    `Screenshot On Failure` on one masked signature were two different image
    comparisons breaking, and rendering the newest occurrence's lines against
    the group said so only for half of them.

    No verdict is drawn from any of it. `before` and `after` are what the same
    leg did, and a re-run that passed is a re-run that passed; a re-run that
    never happened says nothing at all, because nothing here retries
    automatically and whether someone pressed the button follows queue time.
    """
    if not entries:
        return ""
    rows = []
    for entry in entries[:SHOWN_OCCURRENCES]:
        tags = []
        attempt = entry.get("attempt")
        if attempt and attempt > 1:
            tags.append(f'<span class="otag">attempt {attempt}</span>')
        if entry.get("tests_marked"):
            tags.append(f'<span class="otag">marked {entry["tests_marked"]}</span>')
        around = around_for(entry) or {}
        for label, key in (
            ("before", "previous_run_on_this_leg"),
            ("after", "next_run_on_this_leg"),
        ):
            neighbour = around.get(key)
            if not neighbour:
                continue
            outcome = neighbour["outcome"]
            bad = " is-bad" if outcome != "pass" else ""
            tags.append(f'<span class="otag{bad}">{label} {_e(outcome)}</span>')
        retry = around.get("retry")
        if retry:
            passed = retry["passed_on_another_attempt"]
            tags.append(
                '<span class="otag is-rerun">re-run passed</span>'
                if passed
                else '<span class="otag is-bad">re-run failed again</span>'
            )
        if entry.get("artifact_url"):
            tags.append(
                f'<a class="evidence" href="{_e(entry["artifact_url"])}">'
                "artifact &rarr;</a>"
            )
        alongside = alongside_for(entry) or []
        also = ""
        if alongside:
            names = [item["test"] for item in alongside[:3]]
            rest = len(alongside) - len(names)
            tail = f" and {rest} more" if rest > 0 else ""
            also = (
                f'<div class="oalso">also failed here: '
                f"{_e('; '.join(names))}{_e(tail)}</div>"
            )
        evidence = _evidence_html(entry, logs)
        rows.append(
            f'<div class="orow">'
            f'<span class="odate">{_e((entry.get("created_at") or "")[:10])}</span>'
            f'<span class="oleg">{_e(_leg_label(entry.get("artifact_name")))}</span>'
            f"{''.join(tags)}</div>{also}{evidence}"
        )
    hidden = len(entries) - SHOWN_OCCURRENCES
    more = (
        f'<div class="omore">and {hidden} earlier occurrence(s) not shown</div>'
        if hidden > 0
        else ""
    )
    return (
        '<div class="occ"><div class="hd">every occurrence</div>'
        f"{''.join(rows)}{more}</div>"
    ).replace("&amp;rarr;", "&rarr;")


def _first_attempt_html(failures: int, ran: int, total_runs: int) -> str:
    """Only when a re-run actually moved the denominator.

    A leg is re-run because it failed, so re-attempts land where the failures
    are and pull the rate down. Where nothing was re-run the two numbers are the
    same and printing both is noise.
    """
    if ran >= total_runs:
        return ""
    rate = failures / ran if ran else 0
    return (
        f'<span class="first">{failures} / {ran} on first attempts ({rate:.1%})</span>'
    )


def _where_html(
    test_source: str | None,
    test_lineno: int | None,
    *,
    keyword: str | None,
    owner: str | None,
    kind: str | None,
    source: str | None,
    lineno: int | None,
) -> str:
    """Where to start looking: the test, and the keyword that broke."""
    rows = []
    if test_source:
        line = f":{test_lineno}" if test_lineno else ""
        rows.append(
            f'<div><span class="k">test</span>{_e(test_source)}{_e(line)}</div>'
        )
    if keyword:
        badge = (
            f'<span class="kind" data-kind="{_e(kind)}">{_e(owner or kind)}</span>'
            if owner or kind
            else ""
        )
        where = ""
        if source:
            line = f":{lineno}" if lineno else ""
            where = f" &mdash; {_e(source)}{_e(line)}"
        rows.append(
            f'<div><span class="k">keyword</span>{_e(keyword)}{badge}{where}</div>'
        )
    return f'<div class="where">{"".join(rows)}</div>' if rows else ""


def _group_html(
    group: FailureGroup,
    widest: int,
    *,
    cause: str = "",
    rates: str,
    occurrences: str,
    first_attempt: str,
) -> str:
    width = (group.failures / widest * 100) if widest else 0
    suite, _, leaf = group.longname.rpartition(".")
    signature = group.error_signature
    error_class = "error" if signature else "error is-empty"
    return f"""      <article class="group">
        <div class="magnitude">
          <span class="count">{group.failures}<span class="of"> / {
        group.total_runs
    }</span></span>
          <div class="track"><div class="fill" style="width: {width:.1f}%"></div></div>
          <span class="rate">{group.failure_rate:.1%} of runs</span>
          {first_attempt}
        </div>
        <div class="identity">
          <div class="testname"><span class="suite">{_e(suite)}.</span>{_e(leaf)}</div>
          <div class="{error_class}">{
        _e(signature) if signature else "no message recorded"
    }</div>
          {
        _where_html(
            group.test_source,
            group.test_lineno,
            keyword=group.failing_keyword,
            owner=group.keyword_owner,
            kind=group.keyword_kind,
            source=group.keyword_source,
            lineno=group.keyword_lineno,
        )
    }
          {cause}
          {rates}
          {occurrences}
        </div>
      </article>
"""


def _fixture_html(
    fixture: FixtureFailure,
    widest: int,
    *,
    cause: str = "",
    rates: str,
    occurrences: str,
    first_attempt: str,
) -> str:
    width = (fixture.occurrences / widest * 100) if widest else 0
    kind = fixture.failure_scope.replace("_", " ")
    tests = [name for name in (fixture.affected_tests or "").split(",") if name]
    return f"""      <article class="group">
        <div class="magnitude">
          <span class="count">{fixture.occurrences}<span class="of"> / {
        fixture.suite_runs
    }</span></span>
          <div class="track"><div class="fill" style="width: {width:.1f}%"></div></div>
          <span class="rate">{fixture.failure_rate:.1%} of suite runs</span>
          {first_attempt}
        </div>
        <div class="identity">
          <div><span class="scope">{_e(kind)}</span></div>
          <div class="testname">{_e(fixture.scope_owner)}</div>
          <div class="error">{
        _e(fixture.error_signature)
        if fixture.error_signature
        else "no message recorded"
    }</div>
          {
        _where_html(
            fixture.test_source,
            None,
            keyword=fixture.keyword,
            owner=fixture.keyword_owner,
            kind=fixture.keyword_kind,
            source=fixture.keyword_source,
            lineno=fixture.keyword_lineno,
        )
    }
          {cause}
          {rates}
          <div class="affected">marked {fixture.tests_marked} test row(s) failed:
            {_e(", ".join(tests)) or "-"}</div>
          {occurrences}
        </div>
      </article>
"""


def _never_ran_on(coverage: list[dict], known_platforms: set[str]) -> list[str]:
    """Absent and clean are opposite findings and a zero cannot tell them apart."""
    return sorted(known_platforms - {c["platform"] for c in coverage if c["platform"]})


def _fixture_section_html(
    db_path: Path,
    fixture: FixtureFailure,
    widest: int,
    *,
    coverage: dict,
    occurrences: dict,
    neighbours: dict,
    alongside: dict,
    first_runs: dict,
    first_failures: dict,
    known_platforms: set[str],
    logs: dict,
    known: dict,
) -> str:
    identity = (fixture.scope_owner, fixture.failure_scope)
    key = (*identity, fixture.signature_key)
    entries = coverage.get(identity, [])
    return _fixture_html(
        fixture,
        widest,
        cause=_cause_html(
            known_cause_for(known, fixture.scope_owner, fixture.error_signature)
        ),
        rates=_rates_html(
            entries,
            _never_ran_on(entries, known_platforms),
            overall_rate=fixture.failure_rate,
        ),
        occurrences=_occurrences_html(
            occurrences.get(key, []),
            lambda entry: neighbours.get((*identity, entry["leg_id"])),
            lambda entry: alongside.get((*identity, entry["leg_id"])),
            logs,
        ),
        first_attempt=_first_attempt_html(
            first_failures.get(key, 0),
            first_runs.get(identity, 0),
            fixture.suite_runs,
        ),
    )


def render(
    db_path: Path,
    destination: Path,
    limit: int = 100,
    window: Window = ALL_HISTORY,
) -> Path:
    summary = totals(db_path, window=window)
    groups = failure_groups(db_path, limit=limit, window=window)
    platforms = platform_breakdown(db_path, window=window)
    known_platforms = {p["platform"] for p in platforms}
    coverage = coverage_by_test(db_path, window=window)
    durations = pass_durations_by_test(db_path, window=window)
    occurrences = occurrences_by_test(db_path, window=window)
    neighbours = neighbouring_outcomes(db_path, window=window)
    alongside = co_failures(db_path, window=window)
    first_runs, first_failures = first_attempt_counts_by_test(db_path, window=window)
    logs = log_messages_by_result(db_path, window=window)
    known = load_known_causes()
    widest = max((g.failures for g in groups), default=0)
    ingested_span = (
        f"{summary['since'][:10]} to {summary['until'][:10]}"
        if summary["since"]
        else "no runs ingested"
    )
    # A saved page has to say which question it answers: an all-history report
    # and a `--days 3` one are the same document with incomparable numbers, and
    # both are written to the same path.
    scope = (
        f"{window.label}, {summary['runs']} run(s)" if window.bounded else ingested_span
    )
    rate = (summary["failures"] / summary["results"]) if summary["results"] else 0

    if groups:
        body = (
            '<div class="groups">\n'
            + "".join(
                _group_html(
                    g,
                    widest,
                    cause=_cause_html(
                        known_cause_for(known, g.longname, g.error_signature)
                    ),
                    rates=_rates_html(
                        coverage.get(g.longname, []),
                        _never_ran_on(coverage.get(g.longname, []), known_platforms),
                        durations,
                        g.longname,
                        g.failure_rate,
                    ),
                    occurrences=_occurrences_html(
                        occurrences.get((g.longname, g.signature_key), []),
                        lambda entry: neighbours.get(entry["result_id"]),
                        lambda entry: alongside.get(entry["result_id"]),
                        logs,
                    ),
                    first_attempt=_first_attempt_html(
                        first_failures.get((g.longname, g.signature_key), 0),
                        first_runs.get(g.longname, 0),
                        g.total_runs,
                    ),
                )
                for g in groups
            )
            + "</div>"
        )
        note = (
            "One row per test and error. The same test failing on two different errors is "
            "two rows, because they are two problems. The denominator is every time that "
            "test ran, passes included."
        )
    else:
        body = (
            f'<div class="empty">No test failures in {_e(window.label)}. '
            f"{summary['runs']} run(s) and {summary['legs']} matrix leg(s) "
            "examined.</div>"
            if window.bounded
            else '<div class="empty">No failures in the ingested runs.</div>'
        )
        note = "Nothing failed in this window."

    fixtures = fixture_failures(db_path, limit=limit, window=window)
    fixture_coverage = coverage_by_fixture(db_path, window=window)
    fixture_occurrences = occurrences_by_fixture(db_path, window=window)
    fixture_neighbours = neighbouring_fixture_outcomes(db_path, window=window)
    fixture_alongside = fixture_co_failures(db_path, window=window)
    first_fixture_runs, first_fixture_failures = first_attempt_counts_by_fixture(
        db_path, window=window
    )
    widest_fixture = max((f.occurrences for f in fixtures), default=0)
    fixture_section = (
        f"""  <section>
    <h2>Suite setup and teardown failures</h2>
    <p class="section-note">These failed outside any test. Robot Framework marks every test in
    the suite as failed, which is why the same broken teardown would otherwise look like as many
    flaky tests as the suite happens to contain. Counted once here, against the number of times
    the suite ran.</p>
    <div class="groups">
{"".join(_fixture_section_html(db_path, f, widest_fixture, coverage=fixture_coverage, occurrences=fixture_occurrences, neighbours=fixture_neighbours, alongside=fixture_alongside, first_runs=first_fixture_runs, first_failures=first_fixture_failures, known_platforms=known_platforms, logs=logs, known=known) for f in fixtures)}    </div>
  </section>
"""
        if fixtures
        else ""
    )

    busiest = max((p["per_leg"] for p in platforms), default=0)
    platform_rows = "".join(
        f"""      <div class="prow">
        <span class="pname">{_e(p["platform"])}</span>
        <div class="ptrack"><div class="pfill" style="width: {(p["per_leg"] / busiest * 100) if busiest else 0:.1f}%"></div></div>
        <span class="pnum">{p["failures"]} in {p["legs"]} legs</span>
      </div>
"""
        for p in platforms
    )
    platform_section = (
        f"""  <section>
    <h2>Failures per matrix leg, by platform</h2>
    <p class="section-note">Per leg, not in total: the matrix does not run the platforms an
    equal number of times, so raw counts would describe the matrix rather than the platforms.</p>
    <div class="platforms">
{platform_rows}    </div>
  </section>
"""
        if platforms
        else ""
    )

    # Formatted outside the page template: a nested same-quote f-string needs
    # Python 3.12 and this repo supports 3.10, and `ruff format` will happily
    # rewrite it back into one if the expression sits inline.
    result_count = f"{summary['results']:,}"
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    newest = latest_run(db_path, window=window)
    # A first-attempt rate is a floor while any leg is unplaced, and a page that
    # does not say so is a page that reads as if it were not.
    unknown = summary["legs_without_attempt"]
    unknown_note = (
        f'  <p class="section-note">{unknown} leg(s) could not be placed on an '
        "attempt, so the first-attempt rates below are a floor.</p>"
        if unknown
        else ""
    )
    page = f"""<title>Browser CI Failures</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{_FONTS}">
<style>{_CSS}</style>
<div class="page">
  <header>
    <h1>Browser CI Failures</h1>
    <div class="window">{_e(scope)} &middot; main branch, push and scheduled runs</div>
  </header>

  <p class="lede">What actually failed in the acceptance test matrix, grouped by the error
  it failed with. Read from each run's <code>output.xml</code>; follow an artifact link for
  screenshots, traces and the Playwright log.</p>

  <div class="tiles">
    {_tile(summary["runs"], "runs")}
    {_tile(summary["legs"], "matrix legs")}
    {_tile(result_count, "test results")}
    {_tile(summary["failures"], "failures", critical=summary["failures"] > 0)}
    {_tile(f"{rate:.2%}", "failure rate")}
    {_tile(len(groups), "test/error groups")}
    {_tile(len(fixtures), "fixture failures")}
    {
        _tile(
            newest["failures"],
            "failures in the newest run",
            critical=bool(newest.get("failures")),
        )
        if newest
        else ""
    }
  </div>
{unknown_note}

{platform_section}
{fixture_section}
  <section>
    <h2>Test failures, most frequent first</h2>
    <p class="section-note">{_e(note)}</p>
    {body}
  </section>

  <footer>
    <div>Generated {_e(generated)} by <code>inv ci-report --html</code> from {
        _e(summary["tests"]):} distinct tests.</div>
    <div>Proof of concept. No flakiness verdict is implied: whether an error is a flake, a real
    bug or a broken runner is a judgement to make while looking at these numbers.</div>
  </footer>
</div>
"""
    destination.parent.mkdir(parents=True, exist_ok=True)
    # ASCII with the rest as numeric character references. Test names and error
    # messages are arbitrary text, and the page cannot declare its own encoding,
    # so anything above ASCII has to survive as an entity rather than as bytes.
    destination.write_text(page, encoding="ascii", errors="xmlcharrefreplace")
    return destination
