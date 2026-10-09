# A task exits 1, 2 or 3, and each says whose move it is

Every `ci_*` task refuses with one of three exit codes, and nothing else. 1 is **Unanswerable**:
the question was well asked, and the archive cannot answer it - no database, a Test Name it never
recorded, a Leg the Run did not have. 2 is **Misasked**: the flags contradict themselves or
are not values, and no archive could answer them. 3 is **Unreachable**: GitHub could not be
reached, whichever task was talking to it. The triage skill branches on 3 and asks the maintainer
whether to retry, because they are sometimes on a limited connection; 1 and 2 it can act on
by itself. So the codes are a contract with a reader that is not a person, and renumbering or
merging them breaks it silently.

A refusal is raised as one of three error types, each carrying its code, and the commands are
tested through them. `tasks.py` converts them to an exit in one place. An error a lower
module raises belongs to whichever of the three it means, not to where it is caught:
`WindowedBaselineError` is Misasked even though `report.py` raises it, and a missing Leg is
Unanswerable even though GitHub is what lacks it.

## Considered Options

- One code for every refusal, with the message telling them apart. Rejected: the skill would
  have to parse prose to know whether to ask the maintainer.
- A code per error type. Rejected: the reader's next move is one of three, so the codes are too.
