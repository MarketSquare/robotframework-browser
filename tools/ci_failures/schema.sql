-- CI test results, as read out of output.xml.
--
-- Every result is stored, passing ones too, because a failure count without a
-- run count is not a rate. Passing rows carry no message: nothing to say.
--
-- Grouping is (test, error signature). A test failing twice on one error and
-- four times on another is two rows, not one - the errors are what distinguish
-- one problem from another.

CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS run (
    id          INTEGER PRIMARY KEY,   -- the GitHub run id
    event       TEXT,                  -- push | schedule
    head_sha    TEXT,
    head_branch TEXT,
    created_at  TEXT,
    conclusion  TEXT,
    url         TEXT
);

-- One matrix leg: one atest execution, one artifact.
CREATE TABLE IF NOT EXISTS leg (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id        INTEGER NOT NULL REFERENCES run(id),
    artifact_id   INTEGER NOT NULL UNIQUE,
    artifact_name TEXT    NOT NULL,
    -- Where to get the screenshots, traces and playwright-log.txt when one
    -- failure turns out to be worth a closer look. Not derivable from
    -- output.xml: the upload happens after output.xml is written.
    artifact_url  TEXT,
    -- Everything below is read out of output.xml itself.
    python_version TEXT,
    rf_version     TEXT,
    platform       TEXT,
    node_version   TEXT,   -- null until the metadata change reaches CI
    generated_at   TEXT,
    ingested_at    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS test_result (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    leg_id          INTEGER NOT NULL REFERENCES leg(id),
    longname        TEXT    NOT NULL,
    name            TEXT    NOT NULL,
    suite_longname  TEXT    NOT NULL,
    status          TEXT    NOT NULL,   -- PASS | FAIL | SKIP
    elapsed_ms      INTEGER,
    -- Failures only. A passing test has nothing to say and storing it would
    -- bloat the database for nothing.
    message         TEXT,
    error_signature TEXT,               -- message with the varying parts masked
    failing_keyword TEXT                -- innermost keyword that failed
);

-- What the keywords on the failing branch logged on their way down. Robot
-- Framework keeps these as MESSAGE items under each keyword, and they routinely
-- say more than the failure message does: the exception is the summary, these
-- are the evidence. Failures only.
CREATE TABLE IF NOT EXISTS log_message (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    test_result_id INTEGER NOT NULL REFERENCES test_result(id),
    seq            INTEGER NOT NULL,   -- order the messages were logged in
    level          TEXT,               -- TRACE | DEBUG | INFO | WARN | FAIL
    keyword        TEXT,               -- which keyword logged it
    -- Null when the line came from the test's own keywords. Otherwise it names
    -- the setup or teardown that failed, which may belong to an enclosing suite
    -- and may have run after the test itself had already finished.
    origin         TEXT,
    message        TEXT
);

CREATE INDEX IF NOT EXISTS idx_logmsg_result ON log_message(test_result_id);

CREATE INDEX IF NOT EXISTS idx_leg_run       ON leg(run_id);
CREATE INDEX IF NOT EXISTS idx_result_leg    ON test_result(leg_id);
CREATE INDEX IF NOT EXISTS idx_result_name   ON test_result(longname);
CREATE INDEX IF NOT EXISTS idx_result_status ON test_result(status);
CREATE INDEX IF NOT EXISTS idx_result_group  ON test_result(longname, error_signature);
