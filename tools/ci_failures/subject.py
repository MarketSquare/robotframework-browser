"""What failed, resolved once, so no query has to work it out again.

A Group and a Fixture Failure are each one **Subject** and one Error Signature.
They differ in what their Occurrences are counted in - Results for a test, Legs
for a suite fixture - and in nothing else that matters to a query. Yet the rule
telling them apart was a `WHERE` clause somebody had to remember to type, nine
times, and four of the nine test-side queries typed it while five did not. One
of the five was a denominator, and it put `2 of 30` under a heading that said
`1 / 108`.

So the rule stops being a predicate and becomes the table you read. There is no
unfiltered view here to reach for by accident: a query names `test_failure` or
`fixture_failure`, and the Subject arrives already resolved.

## The two grains

A test's Occurrence is one Result and a suite fixture's is one Leg, so the
fixture side has two grains at once: the rows Robot Framework wrote onto each
marked test, and the Leg they collectively describe. `occurrence_id` carries
both. It is the row's own id on the test side, and on the fixture side the
lowest id of the rows sharing a Leg, computed as a window rather than an
aggregate - so the view keeps row grain, and a query that wants Occurrences
groups by `occurrence_id` while one that wants rows does not.

(Window functions need SQLite 3.25, from 2018. This tool is run by hand by a
maintainer, so the only build that has to be new enough is theirs.)

## Where these live

Temp views on the connection, created after `window.apply`, and that ordering is
load-bearing rather than tidy. A permanent view resolves its body against `main`
and would not see the Window's shadowing views at all, so putting these in
`schema.sql` would quietly hand every windowed report the whole of history -
the exact failure `window.py` exists to prevent, reintroduced by the fix for a
different one. Created here and unqualified, they layer on the shadow when there
is one and fall through to the real table when there is not.
"""

from sqlite3 import Connection

_FIXTURE_SCOPES = "('suite_setup', 'suite_teardown')"

_VIEWS = (
    (
        "test_failure",
        f"""
        SELECT f.*,
               f.longname                           AS subject_owner,
               'test'                               AS subject_scope,
               LOWER(IFNULL(f.error_signature, '')) AS signature_key,
               f.id                                 AS occurrence_id
        FROM test_result f
        WHERE f.status = 'FAIL'
          AND IFNULL(f.failure_scope, 'test') NOT IN {_FIXTURE_SCOPES}
        """,
    ),
    (
        "fixture_failure",
        f"""
        SELECT f.*,
               f.scope_owner                        AS subject_owner,
               f.failure_scope                      AS subject_scope,
               LOWER(IFNULL(f.error_signature, '')) AS signature_key,
               MIN(f.id) OVER (
                   PARTITION BY f.scope_owner, f.failure_scope,
                                LOWER(IFNULL(f.error_signature, '')), f.leg_id
               )                                    AS occurrence_id
        FROM test_result f
        WHERE f.status = 'FAIL'
          AND f.failure_scope IN {_FIXTURE_SCOPES}
        """,
    ),
)


def apply(connection: Connection) -> None:
    """Hangs the Subject views off a connection the Window has already scoped."""
    for name, select in _VIEWS:
        connection.execute(f"CREATE TEMP VIEW {name} AS {select}")
