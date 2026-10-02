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
from pathlib import Path

from . import render_html, render_json, workspace
from .annotations import write_snapshot
from .artifacts import clean as clean_artifacts
from .artifacts import fetch, shortlist
from .history import in_archive, never_failed, of_run
from .refusal import MisaskedError
from .report import build, of_test, snapshot_entries
from .window import ALL_HISTORY, Window, of_days

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
