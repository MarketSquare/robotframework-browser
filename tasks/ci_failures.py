from invoke import Exit, task


def _refusing(command, **flags):
    """Runs a `tools.ci_failures.commands` function, its refusal as the exit.

    The one place a refusal becomes an exit code; ADR 0007 says what each means.
    """
    from tools.ci_failures.refusal import RefusalError

    try:
        command(**flags)
    except RefusalError as refused:
        raise Exit(str(refused), refused.code) from None


@task
def ci_ingest(c, limit=None, days=None, db=None, dry_run=False):
    """Pulls CI test results into the local database.

    Incremental: legs already ingested are skipped, so running this often only
    costs what is new. Afterwards, the artifacts a triage left behind beside
    this database are removed. See `tools/ci_failures/README.md`.

    Args:
        limit: How many runs to consider, newest first. Defaults to 25. Runs,
            not days - 25 is about a week of this repository and 100 about a
            month, and the rate moves with how busy it is. Above roughly 100 the
            two events stop coming back in the same proportion and 200 is the
            ceiling, so a question deeper than that wants --days.
        days: Consider runs from the last this-many whole local days instead,
            the same span --days means on the report. This is the one that means
            the same thing next month, and the one that can reach past a page of
            listing: both events are walked to the same date rather than to the
            same count. Artifacts live 90 days, so nothing older can be ingested
            however it is asked for.
        db: Database file. Defaults to ci_failures/ci_failures.sqlite3.
        dry_run: Say which legs would be fetched; fetch, write and remove
            nothing, not even a database that is not there yet. A full
            ingest is download-bound and can run for hours; this reads one
            artifact listing per run instead, so it is minutes for a wide
            window and worth doing before a long ingest.
    """
    from tools.ci_failures import commands

    _refusing(commands.ingest, limit=limit, days=days, db=db, dry_run=dry_run)


@task
def ci_artifact(c, run=None, leg=None, attempt=1, test=None, clean=False, db=None):
    """Fetches one Leg's artifact again, for triaging a failure in it.

    Ingest keeps only the parsed rows. This brings back the rest, unpacked
    under `artifacts/` beside the database, and prints the files worth
    opening, by their path inside it. A Leg already fetched is reused. Remove
    them with --clean once the triage is done; an `inv ci-ingest` of the same
    database also removes any left behind.

    Args:
        run: The run id, as an Occurrence in `inv ci-report` gives it.
        leg: The Leg, as an Occurrence names it, or the artifact's own name.
            Left out, with --test: lists the Legs of the Run that ran the test,
            by Install, the passes marked as Controls, from the database and
            with nothing fetched.
        attempt: The Occurrence's attempt. A Leg re-run by hand uploaded once
            per attempt, and only the one that failed holds the failure.
        test: The Test Name, from `Test.` down. Lists the files that bear on
            that test instead of only the Leg's: the Executor that ran it, the
            log of each test app its suite setups started, and every file its
            log links to, MISSING when the artifact lacks it. Works on
            a Leg where the test passed, as a control. Spelt under another
            top suite, as a Leg that ran several suite directories at once
            spells its tests, it is the same test. Any other name the Leg or
            Run did not run is refused with the names it may mean.
        clean: Remove the artifacts fetched beside the database instead of
            fetching one.
        db: Database file. Defaults to ci_failures/ci_failures.sqlite3. The
            artifacts are fetched into, and cleaned from, the directory it is in.
    """
    from tools.ci_failures import commands

    _refusing(
        commands.artifact,
        run=run,
        leg=leg,
        attempt=attempt,
        test=test,
        clean=clean,
        db=db,
    )


@task
def ci_verify_fixes(c, db=None, mark=False):
    """Says whether each Known Cause's fix held.

    For every entry with `fixed_by` set and `fix_verified` empty: the days since
    the first ingested run containing the fix, the runs of the test since, and
    how often its Group came back. A fix is ready to mark Verified after seven
    days with no recurrence. Every entry is also checked for matching no Group
    at all. Read-only unless --mark; see `tools/ci_failures/verify.py`.

    Args:
        db: Database file. Defaults to ci_failures/ci_failures.sqlite3.
        mark: Write today's date into `fix_verified` of the entries that are
            ready, and only those. Never done automatically: Verified is agreed,
            like the Known Cause itself.
    """
    from tools.ci_failures import commands

    _refusing(commands.verify_fixes, db=db, mark=mark)


@task
def ci_backfill_attempts(c, db=None):
    """Resolves the attempt of legs ingested before it was being recorded.

    Downloads nothing - a run says how many attempts it had and the artifact
    listing says when each was created, which is all the resolution needs.

    Run by hand rather than on every ingest, which is where it used to sit. Its
    whole population is databases predating the column, so on any other it was a
    connection opened and a query returning no rows, every time.

    Args:
        db: Database file. Defaults to ci_failures/ci_failures.sqlite3.
    """
    from tools.ci_failures import commands

    _refusing(commands.backfill_attempts, db=db)


@task
def ci_report(
    c,
    db=None,
    html=None,
    json=None,
    limit=100,
    open_it=False,
    mark_seen=False,
    days=None,
    test=None,
):
    """Shows which tests fail and on which error.

    Two renderings of one report: a page to read, and a document for a language
    model to read. There was a third, printed to the terminal, and it was the
    worst of them - it showed 8 of the 24 fields the others show, cut every
    message to 110 characters, and dropped the source locations, the versions,
    the screenshots, the log lines and everything about what surrounded a
    failure. Anyone reading it was reading less than the page for no gain.

    Args:
        db: Database file. Defaults to ci_failures/ci_failures.sqlite3.
        html: Write a self-contained HTML page here. Defaults to
            ci_report.html beside the database.
        json: Write the report as JSON here, for a language model to read.
            Goes with --html: both are renderings of the one Report.
        limit: How many test/error groups to show.
        open_it: Open the HTML page in a browser once written.
        mark_seen: Record what this report said, so the next one can say what
            changed. Never done automatically: a report that moved its own
            baseline would answer differently the second time it was run on
            unchanged data.
        days: Report only on the last this-many whole local days, today
            included: 1 is today, 2 is today and yesterday. The window is a hard
            scope - every count, rate and denominator comes from inside it, and
            a test that did not fail inside it does not appear at all. That is
            what makes it answer "did what I fixed come back", which no
            all-history report can. It cannot reach further back than the
            database does: ask for more days than have been ingested and the
            answer covers what is there, so read `since` against the span the
            label claims. Goes with everything except --mark-seen; see
            `tools/ci_failures/window.py`.
        test: Report on this one test only, by its Test Name, from `Test.`
            down: its Groups, the Fixture Failures of the suites around it,
            and its Known Cause. Printed as JSON unless --json or --html names
            a file. Spelt under another top suite, it is the same test. A test
            with no Groups gets one line saying how often it ran; a name in no
            Result is refused with the names it may mean, and one with no
            Result in the window says when it last ran.
            --limit does not apply; --mark-seen is refused.
    """
    from tools.ci_failures import commands

    _refusing(
        commands.report,
        db=db,
        html=html,
        json=json,
        limit=limit,
        open_it=open_it,
        mark_seen=mark_seen,
        days=days,
        test=test,
    )


@task
def ci_recompute(c, db=None, what="all"):
    """Works the derived columns out again from what is already stored.

    There is no re-parse: nothing is kept but the parsed rows, so changing what
    is read out of output.xml costs the whole window again. That is not true of
    a derived column whose source is itself in the database, and there are six
    of those - none of these needs the network or the artifacts.

    Args:
        db: Database file. Defaults to ci_failures/ci_failures.sqlite3.
        what: `signatures` after changing the masking rules in `parse.py`;
            `locations` after moving a keyword, after changing `locate._ROOTS`,
            or after an ingest that reported a library it could not import -
            that answer is cached for the whole run, so one failed import
            leaves three columns null on every row it wrote; `installs` after
            changing the artifact name patterns in `legs.py`; `platforms` after
            changing `parse.platform_of`. `all` does every one.
    """
    from tools.ci_failures import commands

    _refusing(commands.recompute, db=db, what=what)
