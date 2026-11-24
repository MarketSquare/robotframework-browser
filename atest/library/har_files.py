import json
from pathlib import Path
from urllib.parse import urlparse


def _har_log(har: Path) -> dict:
    return json.loads(Path(har).read_text(encoding="utf-8"))["log"]


def get_har_request_paths(har: Path) -> list[str]:
    """Returns the URL paths of the requests recorded in ``har``, in recording order."""
    return [
        urlparse(entry["request"]["url"]).path for entry in _har_log(har)["entries"]
    ]


def har_should_not_have_pages(har: Path) -> None:
    """Verify that ``har`` records no pages, as a minimal HAR does."""
    pages = _har_log(har).get("pages", [])
    assert pages == [], f"HAR {har} records pages: {pages}"
