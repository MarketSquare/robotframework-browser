import hashlib
import json
import uuid
from pathlib import Path
from urllib.parse import urlencode

from robot.libraries.BuiltIn import BuiltIn

TEST_APP_LOG_DIR = Path(__file__).parent.parent / "output" / "test-app"
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


def multipart_body(boundary: str, *parts: dict[str, str]) -> str:
    """Return a ``multipart/form-data`` body with ``parts`` in the given order.

    Each part is a dictionary with ``name`` and ``value``; a part with ``filename``
    is sent as a file of type ``text/plain``.
    """
    lines = []
    for part in parts:
        disposition = f'form-data; name="{part["name"]}"'
        lines.append(f"--{boundary}")
        if "filename" in part:
            lines.append(
                f'Content-Disposition: {disposition}; filename="{part["filename"]}"'
            )
            lines.append("Content-Type: text/plain")
        else:
            lines.append(f"Content-Disposition: {disposition}")
        lines.extend(["", part["value"]])
    lines.append(f"--{boundary}--")
    return "\r\n".join(lines) + "\r\n"


def unique_http_path(prefix: str) -> str:
    """Return ``prefix`` with a random suffix, so parallel tests sharing one Test App stay apart."""
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def http_echo_count(path: str) -> int:
    """Return how many ``http_echo`` entries in the Test App Log File have a URL starting with ``path``.

    The Test App is the one at ``${SERVER_PORT}``. Each entry is one request that reached
    an HTTP test page endpoint.
    """
    port = BuiltIn().get_variable_value("${SERVER_PORT}")
    log_file = TEST_APP_LOG_DIR / f"test-app-{port}.log"
    count = 0
    for line in log_file.read_text(encoding="utf-8").splitlines():
        if '"http_echo"' not in line:
            continue
        entry = json.loads(line)
        if entry.get("event") == "http_echo" and entry.get("url", "").startswith(path):
            count += 1
    return count
