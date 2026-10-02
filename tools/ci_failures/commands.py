"""What each `inv ci-*` task does, behind an interface tests can reach.

One function per task, named after it without the `ci_` prefix and always
called as `commands.<name>`: `commands.report` and `commands.ingest` share
their names with modules. Each takes the task's flags by name, as invoke passes them,
writes its lines through `out`, and refuses with a `RefusalError` whose code is
the task's exit code (ADR 0007). The flags themselves are documented once, on
the task.
"""

import webbrowser
from collections.abc import Callable
from datetime import date, datetime, timezone
from pathlib import Path

from . import ingest as ingesting
from . import render_html, render_json, workspace
from .annotations import mark_verified, write_snapshot
from .artifacts import clean as clean_artifacts
from .artifacts import fetch, shortlist
from .history import in_archive, never_failed, of_run
from .refusal import MisaskedError
from .report import build, of_test, snapshot_entries
from .verify import Git, History, Status, Verification, check
from .window import ALL_HISTORY, Window, of_days

_CHECKOUT = Path(__file__).resolve().parents[2]

Out = Callable[[str], None]


def _whole(flag: str, value) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        raise MisaskedError(f"{flag} wants a whole number, got {value!r}.") from None


def _window_of_days(days) -> Window:
    """`--days N` as a Window, or a refusal saying which part of N was wrong.

    `int()` knows about "seven" and `of_days` knows about 0, so they are asked
    separately: one `except ValueError` around both told `--days 0` it was not a
    whole number.
    """
    whole_days = _whole("--days", days)
    try:
        return of_days(whole_days)
    except ValueError as refused:
        raise MisaskedError(str(refused)) from None


def _open_in_browser(page: Path) -> None:
    webbrowser.open(page.resolve().as_uri())


def artifact(
    *,
    run=None,
    leg=None,
    attempt=1,
    test=None,
    clean=False,
    db: str | Path | None = None,
    out: Out = print,
) -> None:
    """What `inv ci-artifact` does; flags as its task documents them."""
    db_path = workspace.database(db)
    artifacts = workspace.artifacts(db_path)
    if clean:
        if clean_artifacts(artifacts):
            out(f"Removed {artifacts}")
        return
    if run is not None and leg is None and test is not None:
        for line in of_run(db_path, _whole("--run", run), test).lines():
            out(line)
        return
    if run is None or leg is None:
        raise MisaskedError("Pass --run and --leg, --run and --test, or --clean.")
    directory = fetch(
        _whole("--run", run), leg, artifacts, attempt=_whole("--attempt", attempt)
    )
    if not (directory / "output.xml").is_file():
        out(f"directory:  {directory}")
        out("output.xml: (none in this artifact)")
        return
    for line in shortlist(directory, test).lines():
        out(line)


def report(
    *,
    db: str | Path | None = None,
    html=None,
    json=None,
    limit=100,
    open_it=False,
    mark_seen=False,
    days=None,
    test=None,
    out: Out = print,
    open_page: Callable[[Path], None] = _open_in_browser,
) -> None:
    """What `inv ci-report` does; flags as its task documents them.

    `open_page` is what `--open-it` hands the written page to.
    """
    if test and mark_seen:
        raise MisaskedError(
            "A baseline of one test would record every other group as gone; "
            "take it without --test."
        )
    window = _window_of_days(days) if days is not None else ALL_HISTORY
    db_path = workspace.database(db)

    # Built once. Both Renderings and the baseline are of the same Report.
    built = build(
        db_path, limit=None if test else _whole("--limit", limit), window=window
    )

    if test:
        test = in_archive(db_path, test)
        built = of_test(built, test)
        if not built.test_failures and not built.fixture_failures:
            out(never_failed(db_path, test, window).line())
            return
        if not json and not html:
            out(render_json.text(built).removesuffix("\n"))
            return

    if mark_seen:
        seen = snapshot_entries(built)
        out(f"Baseline recorded at {write_snapshot(db_path, seen)}")

    written = []
    if json:
        written.append(render_json.write(built, Path(json)))
    # The page unless only the document was asked for.
    if html or not json:
        page_at = render_html.write(
            built, Path(html) if html else workspace.page(db_path)
        )
        written.append(page_at)
        if open_it:
            open_page(page_at)
    for destination in written:
        out(f"Wrote {destination}")


def _verification_lines(entry: Verification) -> list[str]:
    indent = f"{'':<12}"
    lines = [
        f"{entry.status:<12} {entry.subject}",
        f"{indent} {entry.signature}",
        f"{indent} {entry.line()}",
    ]
    lines += [f"{indent} did you mean: {name}" for name in entry.suggestions]
    lines += [
        f"{indent} recurred in run {run}: {url}" for run, url in entry.recurred_in
    ]
    lines += [
        f"{indent} note: {other.occurrences}x on another error, "
        f"not a recurrence: {other.signature}"
        for other in entry.other_failures
    ]
    if entry.unknown_commits:
        lines.append(
            f"{indent} note: {entry.unknown_commits} run(s) on commits this "
            f"clone lacks were not counted; {entry.fetch}"
        )
    return [*lines, ""]


def verify_fixes(
    *,
    db: str | Path | None = None,
    mark=False,
    out: Out = print,
    history: History | None = None,
    today: date | None = None,
    known_causes: Path | None = None,
) -> None:
    """What `inv ci-verify-fixes` does; flags as its task documents them.

    `history` defaults to the checkout's git, `today` to the UTC date - UTC like
    the `created_at` of the Runs the days are counted from - and `known_causes`
    to the checkout's file, which `--mark` writes.
    """
    db_path = workspace.database(db)
    today = today or datetime.now(timezone.utc).date()
    checked = check(
        db_path, known_causes, history=history or Git(_CHECKOUT), today=today
    )
    if not checked:
        out("No fixed Known Cause is waiting to be verified, and none is an orphan.")
    for entry in checked:
        for line in _verification_lines(entry):
            out(line)

    ready = [entry for entry in checked if entry.status == Status.READY]
    if not mark:
        if ready:
            out(f"{len(ready)} ready. Mark them with --mark.")
        return
    if not ready:
        out("Nothing is ready to mark.")
        return
    marked = mark_verified(
        {entry.key for entry in ready}, today.isoformat(), known_causes
    )
    out(f"Marked {marked} fix(es) Verified on {today.isoformat()}.")
    for entry in ready:
        if entry.issue:
            out(f"issue #{entry.issue} can be closed")


def ingest(
    *,
    limit=None,
    days=None,
    db: str | Path | None = None,
    dry_run=False,
    out: Out = print,
) -> None:
    """What `inv ci-ingest` does; flags as its task documents them."""
    if limit is not None and days is not None:
        raise MisaskedError(
            "--limit and --days ask the same question two ways; pass one."
        )
    since = _window_of_days(days).cutoff if days is not None else None
    totals = ingesting.ingest(
        workspace.database(db),
        limit=25 if limit is None else _whole("--limit", limit),
        since=since,
        dry_run=bool(dry_run),
        out=out,
    )
    if dry_run:
        out(f"\nWould fetch {totals.legs} leg(s) across {totals.runs} run(s).")
        return
    out(f"\n{totals.line()}")


def backfill_attempts(*, db: str | Path | None = None, out: Out = print) -> None:
    """What `inv ci-backfill-attempts` does; flags as its task documents them."""
    ingesting.backfill_attempts(workspace.database(db), out=out)


_RECOMPUTED: dict[str, Callable[..., int]] = {
    "signatures": ingesting.recompute_signatures,
    "locations": ingesting.recompute_keyword_locations,
    "installs": ingesting.recompute_installs,
    "platforms": ingesting.recompute_platforms,
}


def recompute(*, db: str | Path | None = None, what="all", out: Out = print) -> None:
    """What `inv ci-recompute` does; flags as its task documents them."""
    known = {"all", *_RECOMPUTED}
    if what not in known:
        raise MisaskedError(f"--what wants one of {sorted(known)}, got {what!r}.")
    db_path = workspace.database(db)
    for name, recomputed in _RECOMPUTED.items():
        if what in ("all", name):
            recomputed(db_path, out=out)
