"""The Report as a page, for someone who will scan it and follow a link.

A Rendering, like `render_json`: it formats what `report.build` produced and
never asks the database anything of its own. What it decides is presentation -
which lines sit behind a disclosure, how many occurrences are shown before the
rest are counted instead - never what the numbers are.

Everything here is ASCII with the rest as numeric character references: test
names and error messages are arbitrary text, and the page cannot declare its own
encoding.
"""

import html
from datetime import datetime, timezone
from pathlib import Path

from .report import (
    FixtureEntry,
    KnownCause,
    LogLine,
    Occurrence,
    Rate,
    RawMessage,
    Report,
    SignatureVariant,
    TestEntry,
    WhereToLook,
    build,
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
.raw { margin: 4px 0 2px; }
.raw > summary, .variants > summary {
  cursor: pointer;
  font-size: 11.5px;
  color: var(--ink-muted);
  list-style: none;
}
.raw > summary::-webkit-details-marker, .variants > summary::-webkit-details-marker { display: none; }
.raw > summary::before, .variants > summary::before { content: "\25B8  "; }
.raw[open] > summary::before, .variants[open] > summary::before { content: "\25BE  "; }
.raw > summary:hover, .variants > summary:hover { color: var(--bar); }
.rawmsg {
  font-family: var(--mono);
  font-size: 11.5px;
  color: var(--ink-2);
  white-space: pre-wrap;
  word-break: break-word;
  border-left: 2px solid var(--rule);
  padding: 4px 0 4px 8px;
  margin: 4px 0;
}
.rawmsg .n { color: var(--ink-muted); font-family: var(--sans); font-size: 11px; }
.variants { margin: 4px 0 2px; }
.variants .v { font-family: var(--mono); font-size: 11.5px; color: var(--ink-2); padding: 2px 0; }
.changed { display: flex; flex-direction: column; gap: 4px; }
.chg { display: flex; gap: 8px; align-items: baseline; font-size: 12.5px; }
.chg .tag {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  font-weight: 600;
  min-width: 52px;
  color: var(--ink-muted);
}
.chg .tag[data-kind="new"], .chg .tag[data-kind="grew"] { color: var(--critical); }
.chg .tag[data-kind="gone"] { color: var(--bar); }
.chg .subj { color: var(--ink-2); }
.chg .was { color: var(--ink-muted); font-size: 11.5px; }
.rules > summary {
  cursor: pointer;
  font-size: 12.5px;
  color: var(--ink-2);
  list-style: none;
}
.rules > summary::-webkit-details-marker { display: none; }
.rules > summary::before { content: "\25B8  "; }
.rules[open] > summary::before { content: "\25BE  "; }
.rules dl { margin: 10px 0 0; }
.rules dt {
  font-family: var(--mono);
  font-size: 11.5px;
  color: var(--ink);
  margin-top: 10px;
}
.rules dd {
  margin: 3px 0 0;
  font-size: 12.5px;
  color: var(--ink-2);
  max-width: 74ch;
}
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


def _skipped_before(
    entries: tuple[LogLine, ...], shown: list[LogLine], index: int
) -> bool:
    """Whether lines were passed over between this shown line and the one before."""
    previous = entries.index(shown[index - 1])
    current = entries.index(shown[index])
    return current - previous > 1


def _log_line(entry: LogLine, skipped: bool = False) -> str:
    level = entry.level or ""
    gap = (
        '<div class="logline gap"><span class="lv"></span><span class="txt">...</span></div>'
        if skipped
        else ""
    )
    return (
        f'{gap}<div class="logline"><span class="lv" data-level="{_e(level)}">{_e(level)}</span>'
        f'<span class="txt">{_e(entry.message)}</span></div>'
    )


def _origin_note(origin: str) -> str:
    return f'<div class="origin">from the {_e(origin)}, not from the test itself</div>'


def _log_html(entries: tuple[LogLine, ...]) -> str:
    """The opening lines and every FAIL or WARN, with the rest behind a disclosure.

    Chronological, which is how they were logged, but the line that names the
    failure is usually near the end rather than the start - the opening lines
    tend to be timeout bookkeeping and dumps - so it is never behind a click.
    """
    if not entries:
        return ""
    origins = {e.origin for e in entries if e.origin}
    note = _origin_note(sorted(origins)[0]) if len(origins) == 1 else ""
    visible = {id(e) for e in entries[:SHOWN_LOG_LINES]}
    visible |= {id(e) for e in entries if (e.level or "") in _LOUD_LEVELS}
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
    notable = sum(1 for e in rest if (e.level or "") in {"FAIL", "WARN"})
    tail = f", {notable} of them FAIL or WARN" if notable else ""
    return (
        f'<div class="log">{shown}'
        f'<details class="more"><summary>{len(rest)} more line'
        f"{'' if len(rest) == 1 else 's'}{tail}</summary>"
        f"{''.join(_log_line(e) for e in rest)}</details></div>"
    )


def _screenshots_html(screenshots: tuple[str, ...], status: str | None) -> str:
    """Where the pictures are, or why there are none.

    A screenshot is often the quickest way to see what was on screen when a
    keyword failed. When there is none that is a clue in itself: the library
    takes one automatically, so "could not" usually means there was no page.
    """
    if status == "file" and screenshots:
        rows = [
            f'<div><span class="k">{_e("screenshot" if index == 0 else "")}</span>{_e(path)}</div>'
            for index, path in enumerate(screenshots)
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
# How many of the Report's co-failures to name before counting the rest. The
# Report already stopped at CO_FAILURE_LIMIT; this is the page being narrower
# still, and it says how many it did not name.
SHOWN_CO_FAILURES = 3


def _configuration_label(rate: Rate) -> str:
    parts = [rate.platform or "?"]
    for label, value in (("rf", rate.rf), ("py", rate.python), ("node", rate.node)):
        if value:
            parts.append(f"{label} {value}")
    return " &middot; ".join(parts)


def _rates_html(rates: tuple[Rate, ...], never_ran_on: tuple[str, ...]) -> str:
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
    so - the Report decided that; this only puts it on the page.
    """
    if not rates and not never_ran_on:
        return ""
    rows = []
    for index, rate in enumerate(rates):
        spread = ""
        if rate.pass_ms:
            spread = (
                f'<span class="ms">passes {rate.pass_ms.min}&ndash;'
                f"{rate.pass_ms.max} ms</span>"
            )
        thin = rate.zero_is_inconclusive
        if thin:
            spread += (
                f'<span class="thin" title="A configuration failing as often as '
                f"the rest would still show nothing here "
                f'{thin.would_look_clean_anyway:.0%} of the time.">'
                f"too few to call ({thin.runs_for_a_meaningful_zero} needed)</span>"
            )
        rows.append(
            f'<div class="row"><span class="k">{"ran on" if not index else ""}</span>'
            f'<span class="cfg">{_e(_configuration_label(rate))}</span>'
            f'<span class="n{"" if rate.failed else " is-clean"}">'
            f"{rate.failed} of {rate.ran}</span>"
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


def _cause_html(cause: KnownCause | None) -> str:
    """What is already known, where a group has been worked out before.

    Placed above the evidence rather than below it, because it changes what the
    reader should do with the rest: an explained group does not want
    re-investigating, it wants its fix verified.
    """
    if not cause or not cause.cause:
        return ""
    bits = []
    if cause.reference:
        bits.append(f"see {_e(cause.reference)}")
    if cause.recorded:
        bits.append(f"recorded {_e(cause.recorded)}")
    if cause.fixed_by:
        bits.append(
            f"fixed by {_e(cause.fixed_by)}, verified {_e(cause.fix_verified)}"
            if cause.fix_verified
            else f"fixed by {_e(cause.fixed_by)} - not yet verified in CI"
        )
    tail = f'<div class="ref">{" &middot; ".join(bits)}</div>' if bits else ""
    return (
        f'<div class="cause"><div class="hd">known cause</div>'
        f"{_e(cause.cause)}{tail}</div>"
    )


def _evidence_html(occurrence: Occurrence) -> str:
    """What this one occurrence logged, and which pictures it left behind."""
    body = _log_html(occurrence.log) + _screenshots_html(
        occurrence.screenshots, occurrence.screenshot_status
    )
    if not body:
        return ""
    return (
        f'<details class="oev"><summary>what this one logged</summary>{body}</details>'
    )


def _occurrences_html(occurrences: tuple[Occurrence, ...]) -> str:
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
    if not occurrences:
        return ""
    rows = []
    for occurrence in occurrences[:SHOWN_OCCURRENCES]:
        tags = []
        if occurrence.attempt and occurrence.attempt > 1:
            tags.append(f'<span class="otag">attempt {occurrence.attempt}</span>')
        if occurrence.tests_marked:
            tags.append(f'<span class="otag">marked {occurrence.tests_marked}</span>')
        for label, neighbour in (
            ("before", occurrence.previous_run_on_this_leg),
            ("after", occurrence.next_run_on_this_leg),
        ):
            if not neighbour:
                continue
            bad = " is-bad" if neighbour.outcome in ("fail", "mixed") else ""
            tags.append(
                f'<span class="otag{bad}">{label} {_e(neighbour.outcome)}</span>'
            )
        if occurrence.retry:
            tags.append(
                '<span class="otag is-rerun">re-run passed</span>'
                if occurrence.retry.passed_on_another_attempt
                else '<span class="otag is-bad">re-run failed again</span>'
            )
        if occurrence.artifact_url:
            tags.append(
                f'<a class="evidence" href="{_e(occurrence.artifact_url)}">'
                "artifact &rarr;</a>"
            )
        also = ""
        if occurrence.also_failed_in_this_leg:
            named = occurrence.also_failed_in_this_leg[:SHOWN_CO_FAILURES]
            names = [
                f"{item.subject} ({item.scope.replace('_', ' ')})"
                if item.scope in ("suite_setup", "suite_teardown")
                else item.subject
                for item in named
            ]
            # Counted against everything the Report found, not only what it
            # listed, or a leg with more than CO_FAILURE_LIMIT co-failures would
            # understate how much went down with it.
            rest = (
                len(occurrence.also_failed_in_this_leg)
                + occurrence.also_failed_in_this_leg_not_listed
                - len(names)
            )
            tail = f" and {rest} more" if rest > 0 else ""
            also = (
                f'<div class="oalso">also failed here: '
                f"{_e('; '.join(names))}{_e(tail)}</div>"
            )
        rows.append(
            f'<div class="orow">'
            f'<span class="odate">{_e((occurrence.at or "")[:10])}</span>'
            f'<span class="oleg">{_e(_leg_label(occurrence.leg))}</span>'
            f"{''.join(tags)}</div>{also}{_evidence_html(occurrence)}"
        )
    hidden = len(occurrences) - SHOWN_OCCURRENCES
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


def _where_html(where: WhereToLook) -> str:
    """Where to start looking: the test, and the keyword that broke."""
    rows = []
    if where.test_file:
        rows.append(f'<div><span class="k">test</span>{_e(where.test_file)}</div>')
    if where.keyword:
        badge = (
            f'<span class="kind" data-kind="{_e(where.keyword_kind)}">'
            f"{_e(where.keyword_owner or where.keyword_kind)}</span>"
            if where.keyword_owner or where.keyword_kind
            else ""
        )
        defined = (
            f" &mdash; {_e(where.keyword_defined)}" if where.keyword_defined else ""
        )
        rows.append(
            f'<div><span class="k">keyword</span>{_e(where.keyword)}{badge}{defined}</div>'
        )
    return f'<div class="where">{"".join(rows)}</div>' if rows else ""


def _messages_html(messages: tuple[RawMessage, ...]) -> str:
    """The unmasked messages behind the signature.

    The mask is what makes grouping possible and also what throws the evidence
    away: three `Compare Images` failures share a byte-identical box and differ
    by three pixels, and the signature renders all of it as `<n>`.
    """
    if not messages:
        return ""
    body = "".join(
        f'<div class="rawmsg">{_e(message.message)}'
        f'<span class="n">  seen {message.occurrences}x</span></div>'
        for message in messages
    )
    total = len(messages)
    return (
        f'<details class="raw"><summary>{total} distinct message'
        f"{'' if total == 1 else 's'} behind this signature</summary>{body}</details>"
    )


# One spelling is not a variant of anything, and saying "spelled 1 ways" beside
# a signature that is already on the page is noise.
VARIANTS_WORTH_SHOWING = 2


def _variants_html(variants: tuple[SignatureVariant, ...]) -> str:
    """The spellings a case-folded Group merged.

    Two libraries implement the same gRPC deadline and whichever timer fires
    first names the error, so the spelling says which side gave up - real
    information, and still no reason to call one problem two.
    """
    if len(variants) < VARIANTS_WORTH_SHOWING:
        return ""
    body = "".join(
        f'<div class="v">{_e(variant.signature)}'
        f'<span class="n">  {variant.occurrences}x</span></div>'
        for variant in variants
    )
    return (
        f'<details class="variants"><summary>spelled {len(variants)} ways'
        f"</summary>{body}</details>"
    )


def _changes_html(changes: dict | None, bounded: bool) -> str:
    """What is new, gone or moved since somebody last took a baseline.

    Absence is three different facts and the page has to say which: no baseline
    was ever taken, the report is windowed and has none it could compare with,
    or a baseline exists and nothing moved.
    """
    if changes is None:
        why = (
            "A windowed report has no baseline it can compare with: one is never "
            "taken from a window, so the only baseline available covers more "
            "data and would report every group as having shrunk."
            if bounded
            else "No baseline has been taken. <code>inv ci-report --mark-seen</code> "
            "records what this report said, so the next one can say what moved."
        )
        return (
            "  <section>\n    <h2>Since the last report</h2>\n"
            f'    <p class="section-note">{why}</p>\n  </section>\n'
        )
    rows = []
    for kind in ("new", "grew", "shrank", "gone"):
        for change in changes.get(kind, []):
            was, now = change.get("was"), change.get("now")
            if was is not None and now is not None:
                counts = f"{was} &rarr; {now}"
            elif now is not None:
                counts = f"{now} failure(s)"
            else:
                counts = f"was {was}"
            rows.append(
                f'      <div class="chg"><span class="tag" data-kind="{kind}">'
                f'{kind}</span><span class="subj">{_e(change.get("subject"))}</span>'
                f'<span class="was">{counts}</span></div>\n'
            )
    taken = changes.get("compared_with")
    note = (
        f"Against the baseline taken {_e(taken[:16])}."
        if taken
        else "Against the last baseline."
    )
    body = (
        f'    <div class="changed">\n{"".join(rows)}    </div>\n'
        if rows
        else '    <p class="section-note">Nothing has moved.</p>\n'
    )
    return (
        "  <section>\n    <h2>Since the last report</h2>\n"
        f'    <p class="section-note">{note}</p>\n{body}  </section>\n'
    ).replace("&amp;rarr;", "&rarr;")


def _about_html(about: dict) -> str:
    """The rules the numbers were built on, so they are read rather than inferred.

    The same text the document carries, rendered rather than restated. The page
    used to make three of these claims in its own prose, which is two authors of
    one rule and nothing keeping them in agreement.
    """
    items = "".join(
        f"      <dt>{_e(name)}</dt>\n      <dd>{_e(rule)}</dd>\n"
        for name, rule in about.items()
    )
    return (
        '  <section>\n    <details class="rules">'
        f"<summary>How these numbers are built &mdash; {len(about)} rules</summary>\n"
        f"    <dl>\n{items}    </dl></details>\n  </section>\n"
    ).replace("&amp;mdash;", "&mdash;")


def _group_html(entry: TestEntry, widest: int) -> str:
    counts = entry.counts
    width = (counts.failures / widest * 100) if widest else 0
    suite, _, leaf = entry.test.rpartition(".")
    error_class = "error" if entry.signature else "error is-empty"
    return f"""      <article class="group">
        <div class="magnitude">
          <span class="count">{counts.failures}<span class="of"> / {
        counts.ran
    }</span></span>
          <div class="track"><div class="fill" style="width: {width:.1f}%"></div></div>
          <span class="rate">{counts.rate:.1%} of runs</span>
          {
        _first_attempt_html(
            counts.first_attempt.failures, counts.first_attempt.ran, counts.ran
        )
    }
        </div>
        <div class="identity">
          <div class="testname"><span class="suite">{_e(suite)}.</span>{_e(leaf)}</div>
          <div class="{error_class}">{
        _e(entry.signature) if entry.signature else "no message recorded"
    }</div>
          {_where_html(entry.where_to_look)}
          {_cause_html(entry.known_cause)}
          {_rates_html(entry.rates, entry.never_ran_on)}
          {_variants_html(entry.signature_variants)}
          {_messages_html(entry.raw_messages)}
          {_occurrences_html(entry.occurrences)}
        </div>
      </article>
"""


def _fixture_html(entry: FixtureEntry, widest: int) -> str:
    counts = entry.counts
    width = (counts.failures / widest * 100) if widest else 0
    kind = entry.scope.replace("_", " ")
    return f"""      <article class="group">
        <div class="magnitude">
          <span class="count">{counts.failures}<span class="of"> / {
        counts.suite_runs
    }</span></span>
          <div class="track"><div class="fill" style="width: {width:.1f}%"></div></div>
          <span class="rate">{counts.rate:.1%} of suite runs</span>
          {
        _first_attempt_html(
            counts.first_attempt.failures,
            counts.first_attempt.ran,
            counts.suite_runs,
        )
    }
        </div>
        <div class="identity">
          <div><span class="scope">{_e(kind)}</span></div>
          <div class="testname">{_e(entry.suite)}</div>
          <div class="error">{
        _e(entry.signature) if entry.signature else "no message recorded"
    }</div>
          {_where_html(entry.where_to_look)}
          {_cause_html(entry.known_cause)}
          {_rates_html(entry.rates, entry.never_ran_on)}
          <div class="affected">marked {
        counts.test_rows_marked_failed
    } test row(s) failed:
            {_e(", ".join(entry.affected_tests)) or "-"}</div>
          {_variants_html(entry.signature_variants)}
          {_messages_html(entry.raw_messages)}
          {_occurrences_html(entry.occurrences)}
        </div>
      </article>
"""


def page(report: Report) -> str:
    """The whole page, from a Report that is already built."""
    summary = report.window
    groups = report.test_failures
    fixtures = report.fixture_failures
    widest = max((g.counts.failures for g in groups), default=0)
    widest_fixture = max((f.counts.failures for f in fixtures), default=0)
    rate = (summary.failures / summary.results) if summary.results else 0
    ingested_span = (
        f"{summary.since[:10]} to {summary.until[:10]}"
        if summary.since
        else "no runs ingested"
    )
    # A saved page has to say which question it answers: an all-history report
    # and a `--days 3` one are the same document with incomparable numbers, and
    # both are written to the same path.
    scope = (
        f"{summary.label}, {summary.runs} run(s)" if summary.bounded else ingested_span
    )

    if groups:
        body = (
            '<div class="groups">\n'
            + "".join(_group_html(g, widest) for g in groups)
            + "</div>"
        )
        note = (
            "One row per test and error. The same test failing on two different errors is "
            "two rows, because they are two problems. The denominator is every time that "
            "test ran, passes included."
        )
    else:
        body = (
            f'<div class="empty">No test failures in {_e(summary.label)}. '
            f"{summary.runs} run(s) and {summary.legs} matrix leg(s) "
            "examined.</div>"
            if summary.bounded
            else '<div class="empty">No failures in the ingested runs.</div>'
        )
        note = "Nothing failed in this window."

    fixture_section = (
        f"""  <section>
    <h2>Suite setup and teardown failures</h2>
    <p class="section-note">These failed outside any test, and are counted once per fixture
    against the number of times the suite ran - never once per test they marked. The rules at the
    foot of this page say why.</p>
    <div class="groups">
{"".join(_fixture_html(f, widest_fixture) for f in fixtures)}    </div>
  </section>
"""
        if fixtures
        else ""
    )

    busiest = max((p.per_leg for p in report.platforms), default=0)
    platform_rows = "".join(
        f"""      <div class="prow">
        <span class="pname">{_e(p.platform)}</span>
        <div class="ptrack"><div class="pfill" style="width: {(p.per_leg / busiest * 100) if busiest else 0:.1f}%"></div></div>
        <span class="pnum">{p.failures} in {p.legs} legs</span>
      </div>
"""
        for p in report.platforms
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
        if report.platforms
        else ""
    )

    # Formatted outside the page template: a nested same-quote f-string needs
    # Python 3.12 and this repo supports 3.10, and `ruff format` will happily
    # rewrite it back into one if the expression sits inline.
    changes_section = _changes_html(report.since_last_report, summary.bounded)
    about_section = _about_html(report.about)
    result_count = f"{summary.results:,}"
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    newest = summary.latest_run
    # A first-attempt rate is a floor while any leg is unplaced, and a page that
    # does not say so is a page that reads as if it were not.
    unknown = summary.legs_with_unknown_attempt
    unknown_note = (
        f'  <p class="section-note">{unknown} leg(s) could not be placed on an '
        "attempt, so the first-attempt rates below are a floor.</p>"
        if unknown
        else ""
    )
    return f"""<title>Browser CI Failures</title>
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
    {_tile(summary.runs, "runs")}
    {_tile(summary.legs, "matrix legs")}
    {_tile(result_count, "test results")}
    {_tile(summary.failures, "failures", critical=summary.failures > 0)}
    {_tile(f"{rate:.2%}", "failure rate")}
    {_tile(len(groups), "test/error groups")}
    {_tile(len(fixtures), "fixture failures")}
    {
        _tile(
            newest.failures,
            "failures in the newest run",
            critical=bool(newest.failures),
        )
        if newest
        else ""
    }
  </div>
{unknown_note}

{changes_section}
{platform_section}
{fixture_section}
  <section>
    <h2>Test failures, most frequent first</h2>
    <p class="section-note">{_e(note)}</p>
    {body}
  </section>

{about_section}
  <footer>
    <div>Generated {_e(generated)} by <code>inv ci-report --html</code> from {
        _e(summary.distinct_tests):} distinct tests.</div>
    <div>Proof of concept. No flakiness verdict is implied: whether an error is a flake, a real
    bug or a broken runner is a judgement to make while looking at these numbers.</div>
  </footer>
</div>
"""


def render(
    db_path: Path,
    destination: Path,
    limit: int = 100,
    window: Window = ALL_HISTORY,
) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    # ASCII with the rest as numeric character references. Test names and error
    # messages are arbitrary text, and the page cannot declare its own encoding,
    # so anything above ASCII has to survive as an entity rather than as bytes.
    destination.write_text(
        page(build(db_path, limit=limit, window=window)),
        encoding="ascii",
        errors="xmlcharrefreplace",
    )
    return destination
