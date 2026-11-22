import base64
import hashlib
import json
import uuid
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

from robot.libraries.BuiltIn import BuiltIn

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
    return sha256_of_bytes(http_fixture_bytes(name))


def http_fixture_bytes(name: str) -> bytes:
    """Return the content of a file in the Test App's ``static/http-fixtures``."""
    return Path(http_fixture_path(name)).read_bytes()


def http_fixture_integrity(name: str) -> str:
    """Return the subresource integrity value (``sha256-<base64>``) of an HTTP fixture."""
    digest = hashlib.sha256(http_fixture_bytes(name)).digest()
    return f"sha256-{base64.b64encode(digest).decode('ascii')}"


def sha256_of_bytes(data: bytes) -> str:
    """Return the SHA-256 hex digest of ``data``."""
    return hashlib.sha256(data).hexdigest()


def http_page_url(page_url: str, send: bool = True, **fields: str) -> str:
    """Return the URL of the HTTP test page with its request builder prefilled.

    ``fields`` are the builder's prefill parameters (``kind``, ``method``, ``url``,
    ``headers``, ``bodyMode``, ``body``, ``fixture``, ``fileField``, ``credentials``,
    ``target``). With ``send`` the page sends the request as soon as it has loaded.
    """
    if send:
        fields["send"] = "1"
    return f"{page_url}?{urlencode(fields)}"


def respond_url(**query: str) -> str:
    """Return the relative URL ``/api/respond/fetch`` with ``query`` URL-encoded.

    ``/api/respond/**`` answers any path below it the same way, so ``fetch`` only names the
    request. ``query`` holds the endpoint's parameters (``status``, ``statusText``,
    ``contentType``, ``header``, ``delay``, ``body``, ``file``).
    """
    return f"/api/respond/fetch?{urlencode(query)}"


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


def http_journal(path: str) -> list[dict]:
    """Return the Test App request journal entries whose path starts with ``path``.

    The Test App is the one at ``${SERVER_PORT}``. Each entry is one request that reached
    ``/api/echo``, ``/api/respond`` or ``/api/basic-auth``.
    """
    port = BuiltIn().get_variable_value("${SERVER_PORT}")
    query = urlencode({"path": path})
    with urlopen(
        f"http://localhost:{port}/api/journal?{query}", timeout=10
    ) as response:
        return json.loads(response.read())
