# A Run's Controls come from the database, and GitHub only fetches

`inv ci-artifact --run <id> --test "<name>"` without `--leg` lists the Legs of that Run where the
test ran, each with its outcome and Attempt, the passes marked as **Controls**. That is a
reporting question, so it is answered from the database like every other one. GitHub is reached
only to fetch an artifact once a Leg is chosen.

The GitHub listing of a Run's artifacts was the obvious fallback for a Run not yet ingested, and
it was rejected. It names every Leg, but it cannot say which ones ran the test or passed it, and
with four shards most of them did neither. A list that looks like an answer and is not one sends
the reader on 100 MB downloads to find out. A Run the database does not hold is refused with
`inv ci-ingest` as the way on.

## Consequences

- `ci-artifact` is the one task that reads the database and talks to GitHub. The listing and the
  fetch stay separate paths inside it: the listing never calls `github.py`, and the fetch never
  reads the database.
- A Leg whose `attempt` is still NULL is listed as `attempt ?`, not dropped. A pass with an
  unknown Attempt is still a Control, and the fetch's wrong-Attempt error corrects a guess.
