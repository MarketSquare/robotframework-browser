import hashlib
from pathlib import Path
from urllib.parse import urlencode

FIXTURES_DIR = (
    Path(__file__).parent.parent.parent
    / "node"
    / "dynamic-test-app"
    / "static"
    / "http-fixtures"
)


def http_fixture_path(name: str) -> str:
    """Return the absolute path of a file in the Test App's ``static/http-fixtures``."""
    path = FIXTURES_DIR / name
    if not path.is_file():
        raise FileNotFoundError(f"No HTTP fixture named {name!r} in {FIXTURES_DIR}")
    return str(path)


def http_fixture_sha256(name: str) -> str:
    """Return the SHA-256 hex digest of a file in the Test App's ``static/http-fixtures``."""
    return hashlib.sha256(Path(http_fixture_path(name)).read_bytes()).hexdigest()


def http_page_url(page_url: str, send: bool = True, **fields: str) -> str:
    """Return the URL of the HTTP test page with its request builder prefilled.

    ``fields`` are the builder's prefill parameters (``kind``, ``method``, ``url``,
    ``headers``, ``bodyMode``, ``body``, ``fixture``, ``fileField``, ``credentials``,
    ``target``). With ``send`` the page sends the request as soon as it has loaded.
    """
    if send:
        fields["send"] = "1"
    return f"{page_url}?{urlencode(fields)}"
