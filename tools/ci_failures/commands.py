"""What each `inv ci-*` task does, behind an interface tests can reach.

One function per task, named after it without the `ci_` prefix and always
called as `commands.<name>`: `commands.report` and `commands.ingest` share
their names with modules. Each takes the task's flags by name, as invoke passes them,
writes its lines through `out`, and refuses with a `RefusalError` whose code is
the task's exit code (ADR 0007). The flags themselves are documented once, on
the task.
"""

from collections.abc import Callable
from pathlib import Path

from . import workspace
from .artifacts import clean as clean_artifacts
from .artifacts import fetch, shortlist
from .history import of_run
from .refusal import MisaskedError

Out = Callable[[str], None]


def _whole(flag: str, value) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        raise MisaskedError(f"{flag} wants a whole number, got {value!r}.") from None


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
