---
name: parse-rf-results
description: 'Parse Robot Framework test results from output.xml. Use when: analyzing test execution results, extracting pass/fail statistics, filtering failures, summarizing test runs'
argument-hint: 'Path to output.xml, or describe what to extract (e.g. failed tests, keyword timings, suite stats)'
---

# Parse Robot Framework Results

Uses [scripts/parse_results.py](./scripts/parse_results.py) to parse `output.xml` via `robot.api.ExecutionResult`.

**The output.xml file is always at `atest/output/output.xml`. Do not guess another path unless the user explicitly provides one.**

## Running the script

```bash
.venv/bin/python .github/skills/parse-rf-results/scripts/parse_results.py atest/output/output.xml
```

On Windows:

```bash
.venv\Scripts\python .github/skills/parse-rf-results/scripts/parse_results.py atest/output/output.xml
```

The script prints three sections automatically: pass rate summary, individual failures with error messages, and failures grouped by identical error message.

## Optional flags

### `--keyword-logs`

Include all keyword log messages for each failing test. Each log entry shows the timestamp, log level, and message text. HTML tags are stripped from messages.

```bash
.venv/bin/python .github/skills/parse-rf-results/scripts/parse_results.py atest/output/output.xml --keyword-logs
```

Example output for a failing test:

```
FAIL  Suite.Test Name
      keyword: Some Keyword (SomeLibrary)
      AssertionError: expected True but got False
      --- keyword logs ---
      20260306 14:32:01.123  INFO      Clicks the element 'id=submit'.
      20260306 14:32:01.456  DEBUG     Clicked element: 'id=submit' successfully.
```
