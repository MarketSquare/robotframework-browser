import json
import time
import uuid
from pathlib import Path

import Browser


def _lines_logged_after(log_file: Path, offset: int, action: str) -> list[dict]:
    deadline = time.monotonic() + 5
    while True:
        with log_file.open() as log:
            log.seek(offset)
            new = [json.loads(raw) for raw in log if raw.startswith("{")]
        lines = [line for line in new if line.get("action") == action]
        if lines or time.monotonic() > deadline:
            return lines
        time.sleep(0.1)


def test_first_keyword_after_suite_and_test_start_carries_their_context():
    browser = Browser.Browser()
    suite_id = f"s-{uuid.uuid4().hex}"
    browser._start_suite("Lazy Suite", {"id": suite_id, "longname": "Top.Lazy Suite"})
    browser._start_test(
        "First Test", {"id": f"{suite_id}-t1", "longname": "Top.Lazy Suite.First Test"}
    )
    assert browser._playwright is None
    log_file = browser._playwright_log
    offset = log_file.stat().st_size if log_file.exists() else 0

    browser.get_browser_catalog()

    lines = _lines_logged_after(log_file, offset, "getBrowserCatalog")
    browser.playwright.close()
    assert lines
    for line in lines:
        assert line.get("suite_id") == suite_id
        assert line.get("suite_name") == "Top.Lazy Suite"
        assert line.get("test_id") == f"{suite_id}-t1"
        assert line.get("test_name") == "Top.Lazy Suite.First Test"
