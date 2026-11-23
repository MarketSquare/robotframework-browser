# Copyright 2020-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import mimetypes
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from os import PathLike
from pathlib import Path
from typing import Any

from .types import Secret

JSON = "application/json"
TEXT = "text/plain; charset=utf-8"
BINARY = "application/octet-stream"


@dataclass(frozen=True)
class HttpBody:
    content: str | bytes
    content_type: str | None
    kind: str

    @property
    def encoded(self) -> bytes:
        return (
            self.content.encode("utf-8")
            if isinstance(self.content, str)
            else self.content
        )

    def headers(
        self, headers: Mapping[str, str], removed: Iterable[str] = ()
    ) -> dict[str, str]:
        given = {name.lower() for name in [*headers, *removed]}
        if self.content_type is None or "content-type" in given:
            return dict(headers)
        return {**headers, "Content-Type": self.content_type}


def revealed(value: Any) -> Any:
    value = value.value if isinstance(value, Secret) else value
    return bytes(value) if isinstance(value, bytearray) else value


def at_most_one(**given: Any):
    given_names = [name for name, value in given.items() if value is not None]
    if len(given_names) > 1:
        raise ValueError(
            f"Give at most one of {_join_with_and(list(given))}, "
            f"got {_join_with_and(given_names)}."
        )


def json_text(value: Any, name: str, hint: str = "") -> str:
    try:
        return json.dumps(value, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{name} cannot be sent as JSON: {error}.{hint}") from error


def made_up(
    body: Any = None, json_value: Any = None, path: PathLike | None = None
) -> HttpBody:
    at_most_one(body=body, json=json_value, path=path)
    if path is not None:
        return _file(path)
    if json_value is not None:
        return HttpBody(json_text(json_value, "json"), JSON, "json body")
    body = revealed(body)
    if isinstance(body, bytes):
        return HttpBody(body, BINARY, "binary body")
    if isinstance(body, str):
        return HttpBody(body, TEXT, "text body")
    if body is not None:
        return HttpBody(json_text(body, "body"), JSON, "json body")
    return HttpBody(b"", None, "no body")


def replacement(
    body: Any = None,
    json_value: Any = None,
    path: PathLike | None = None,
    name: str = "body",
) -> HttpBody | None:
    at_most_one(**{name: body, "json": json_value, "path": path})
    body = revealed(body)
    if isinstance(body, str | bytes):
        return _as_given(body)
    if body is not None:
        return HttpBody(json_text(body, name), JSON, "json body")
    if json_value is None and path is None:
        return None
    return made_up(json_value=json_value, path=path)


def page_request(body: Any) -> HttpBody | None:
    body = revealed(body)
    if body is None:
        return None
    if isinstance(body, bytes):
        return _as_given(body)
    if isinstance(body, str):
        return HttpBody(body, JSON if _is_json(body) else TEXT, "text body")
    return HttpBody(json_text(body, "body"), JSON, "json body")


def api_request(data: Any) -> HttpBody | None:
    data = revealed(data)
    if data is None:
        return None
    if isinstance(data, str | bytes):
        return _as_given(data)
    text = json_text(
        data,
        "data",
        " Give a string, bytes, or a dictionary, a list, a number or a boolean that "
        "holds only such values and None.",
    )
    return HttpBody(text, JSON, "json body")


def _join_with_and(names: list[str]) -> str:
    return names[0] if len(names) == 1 else f"{', '.join(names[:-1])} and {names[-1]}"


def _as_given(content: str | bytes) -> HttpBody:
    return HttpBody(
        content, None, "text body" if isinstance(content, str) else "binary body"
    )


def _file(path: PathLike) -> HttpBody:
    file = Path(path)
    if not file.is_file():
        raise ValueError(f"path {file} is not a file.")
    content_type = mimetypes.guess_type(file.name)[0] or BINARY
    if content_type.startswith("text/"):
        content_type = f"{content_type}; charset=utf-8"
    return HttpBody(file.read_bytes(), content_type, f"file {file}")


def _is_json(text: str) -> bool:
    try:
        json.loads(text)
    except json.JSONDecodeError:
        return False
    return True
