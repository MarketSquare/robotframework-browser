"""Renders the database as a single self-contained HTML page."""

import html
from datetime import datetime, timezone
from pathlib import Path

from .report import (
    FailureGroup,
    failure_groups,
    log_messages,
    platform_breakdown,
    totals,
)

_FONTS = "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap"

_CSS = """
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
  gap: 1px;
  background: var(--rule);
  border: 1px solid var(--rule);
  border-radius: 4px;
  overflow: hidden;
}
.tile { background: var(--surface); padding: 16px 18px; display: flex; flex-direction: column; gap: 2px; }
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
details.more > summary {
  cursor: pointer;
  font-size: 11.5px;
  color: var(--ink-muted);
  padding: 3px 0;
  list-style: none;
  width: fit-content;
}
details.more > summary::-webkit-details-marker { display: none; }
details.more > summary::before { content: "▸  "; }
details.more[open] > summary::before { content: "▾  "; }
details.more > summary:hover { color: var(--ink-2); }

.platforms { display: flex; flex-direction: column; gap: 1px; background: var(--rule); border: 1px solid var(--rule); border-radius: 4px; overflow: hidden; }
.prow { background: var(--surface); display: grid; grid-template-columns: 92px minmax(0, 1fr) 132px; gap: 16px; align-items: center; padding: 12px 20px; }
.pname { font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: 13px; }
.pnum { font-family: "IBM Plex Mono", ui-monospace, monospace; font-variant-numeric: tabular-nums; font-size: 12px; color: var(--ink-2); text-align: right; }
.ptrack { height: 10px; background: var(--bar-soft); border-radius: 4px; overflow: hidden; }
.pfill { height: 100%; background: var(--bar); border-radius: 4px; }

.empty { background: var(--surface); border: 1px solid var(--rule); border-radius: 4px; padding: 40px 24px; text-align: center; color: var(--ink-muted); }

footer { border-top: 1px solid var(--rule); padding-top: 16px; font-size: 12px; color: var(--ink-muted); display: flex; flex-direction: column; gap: 4px; }
code { font-family: "IBM Plex Mono", ui-monospace, monospace; }

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


def _log_line(entry: dict) -> str:
    level = entry.get("level") or ""
    return (
        f'<div class="logline"><span class="lv" data-level="{_e(level)}">{_e(level)}</span>'
        f'<span class="txt">{_e(entry.get("message"))}</span></div>'
    )


def _log_html(entries: list[dict]) -> str:
    """The first few lines, and the rest behind a disclosure.

    Chronological, which is how they were logged. Worth knowing when reading
    them: the line that names the failure is usually near the end, not the
    start - the opening lines tend to be timeout bookkeeping and dumps.
    """
    if not entries:
        return ""
    shown = "".join(_log_line(e) for e in entries[:SHOWN_LOG_LINES])
    rest = entries[SHOWN_LOG_LINES:]
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


def _group_html(group: FailureGroup, widest: int, entries: list[dict]) -> str:
    width = (group.failures / widest * 100) if widest else 0
    suite, _, leaf = group.longname.rpartition(".")
    chips = (
        [
            f'<span class="chip kw"><span class="k">keyword</span> {_e(group.failing_keyword)}</span>'
        ]
        if group.failing_keyword
        else []
    )
    if group.platforms:
        chips.append(
            f'<span class="chip"><span class="k">on</span> {_e(group.platforms.replace(",", ", "))}</span>'
        )
    chips.append(
        f'<span class="chip"><span class="k">last</span> {_e(group.last_seen[:10])}</span>'
    )
    if group.latest_artifact_url:
        chips.append(
            f'<a class="evidence" href="{_e(group.latest_artifact_url)}">artifact &rarr;</a>'
        )
    signature = group.error_signature
    error_class = "error" if signature else "error is-empty"
    return f"""      <article class="group">
        <div class="magnitude">
          <span class="count">{group.failures}<span class="of"> / {group.total_runs}</span></span>
          <div class="track"><div class="fill" style="width: {width:.1f}%"></div></div>
          <span class="rate">{group.failure_rate:.1%} of runs</span>
        </div>
        <div class="identity">
          <div class="testname"><span class="suite">{_e(suite)}.</span>{_e(leaf)}</div>
          <div class="{error_class}">{_e(signature) if signature else "no message recorded"}</div>
          {_log_html(entries)}
          <div class="chips">{"".join(chips)}</div>
        </div>
      </article>
"""


def render(db_path: Path, destination: Path, limit: int = 100) -> Path:
    summary = totals(db_path)
    groups = failure_groups(db_path, limit=limit)
    widest = max((g.failures for g in groups), default=0)
    window = (
        f"{summary['since'][:10]} to {summary['until'][:10]}"
        if summary["since"]
        else "no runs ingested"
    )
    rate = (summary["failures"] / summary["results"]) if summary["results"] else 0

    if groups:
        body = (
            '<div class="groups">\n'
            + "".join(
                _group_html(g, widest, log_messages(db_path, g.latest_result_id))
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
        body = '<div class="empty">No failures in the ingested runs.</div>'
        note = "Nothing failed in this window."

    platforms = platform_breakdown(db_path)
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
    page = f"""<title>Browser CI Failures</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{_FONTS}">
<style>{_CSS}</style>
<div class="page">
  <header>
    <h1>Browser CI Failures</h1>
    <div class="window">{_e(window)} &middot; main branch, push and scheduled runs</div>
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
  </div>

{platform_section}
  <section>
    <h2>Failures, most frequent first</h2>
    <p class="section-note">{_e(note)}</p>
    {body}
  </section>

  <footer>
    <div>Generated {_e(generated)} by <code>inv ci-report --html</code> from {_e(summary["tests"]):} distinct tests.</div>
    <div>Proof of concept. No flakiness verdict is implied: whether an error is a flake, a real
    bug or a broken runner is a judgement to make while looking at these numbers.</div>
  </footer>
</div>
"""
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(page, encoding="utf-8")
    return destination
