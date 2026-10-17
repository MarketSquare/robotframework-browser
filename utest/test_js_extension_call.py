import inspect
import json
import math
from contextlib import contextmanager
from datetime import timedelta
from types import SimpleNamespace

import pytest

from Browser import Browser
from Browser.base import LibraryComponent
from Browser.utils.data_types import Scope


class RecordingPlaywright:
    def __init__(self):
        self.requests = []
        self.responses = []

    @contextmanager
    def grpc_channel(self):
        yield self

    def CallExtensionKeyword(self, request):  # noqa: N802 - the name of the gRPC method
        self.requests.append(request)
        return self.responses

    def SetTimeout(self, request):  # noqa: N802 - the name of the gRPC method
        return SimpleNamespace(log="")

    def payload(self) -> dict:
        return json.loads(self.requests[-1].arguments)


@pytest.fixture
def playwright() -> RecordingPlaywright:
    return RecordingPlaywright()


@pytest.fixture
def library(tmpdir, monkeypatch, playwright: RecordingPlaywright) -> Browser:
    monkeypatch.setattr(Browser, "_output_dir", tmpdir)
    library = Browser(timeout=timedelta(seconds=7))
    library._playwright = playwright
    return library


def extension_response(log: str, body_part: str = "") -> SimpleNamespace:
    return SimpleNamespace(log=log, bodyPart=body_part, json="")


def generated_keyword(library: Browser, name: str, arguments: str):
    component = LibraryComponent(library)
    library._jskeyword_call(component, name, arguments, "")
    return getattr(component, name)


def test_generated_keyword_passes_the_library_timeout_as_default_timeout(
    library: Browser, playwright: RecordingPlaywright
):
    keyword = generated_keyword(library, "openOwnContext", "url, defaultTimeout")

    keyword("https://a.b")

    assert list(inspect.signature(keyword).parameters) == ["url"]
    assert playwright.payload() == {
        "arguments": [["url", "https://a.b"], ["defaultTimeout", 7000]]
    }


def test_generated_keyword_reads_the_library_timeout_at_each_call(
    library: Browser, playwright: RecordingPlaywright
):
    keyword = generated_keyword(library, "openOwnContext", "defaultTimeout")

    library.set_browser_timeout(timedelta(seconds=3), Scope.Global)
    keyword()

    assert playwright.payload() == {"arguments": [["defaultTimeout", 3000]]}


def test_other_generated_keywords_send_only_their_arguments(
    library: Browser, playwright: RecordingPlaywright
):
    generated_keyword(library, "clickTwice", "selector, page")("#button")

    assert playwright.payload() == {
        "arguments": [["selector", "#button"], ["page", "RESERVED"]]
    }


def test_call_js_keyword_sends_the_arguments_as_given(
    library: Browser, playwright: RecordingPlaywright
):
    library.call_js_keyword("openOwnContext", url="https://a.b", defaultTimeout=5000)

    assert playwright.payload() == {
        "arguments": [["url", "https://a.b"], ["defaultTimeout", 5000]]
    }


def test_generated_keyword_joins_the_body_parts_of_a_chunked_result(
    library: Browser, playwright: RecordingPlaywright
):
    playwright.responses = [
        extension_response("ok chunk 0", '{"name": "J'),
        extension_response("ok", 'örn", "size": 2}'),
    ]

    result = generated_keyword(library, "describe", "")()

    assert result == {"name": "Jörn", "size": 2}


def test_generated_keyword_returns_none_when_the_function_returns_nothing(
    library: Browser, playwright: RecordingPlaywright
):
    playwright.responses = [extension_response("ok")]

    assert generated_keyword(library, "closeAll", "")() is None


def test_generated_keyword_sends_its_varargs_as_one_args_list(
    library: Browser, playwright: RecordingPlaywright
):
    keyword = generated_keyword(library, "typeAll", "selector, args, logger")

    keyword("#field", "first", "second")

    assert playwright.payload() == {
        "arguments": [
            ["selector", "#field"],
            ["args", ["first", "second"]],
            ["logger", "RESERVED"],
        ]
    }


def test_generated_keyword_takes_its_defaults_from_the_javascript_signature(
    library: Browser,
):
    keyword = generated_keyword(
        library,
        "measure",
        'label = "width", count = 3, ratio = NaN, upper = Infinity, '
        "lower = -Infinity, strict = false, limit = null, unit = undefined",
    )

    defaults = {
        name: parameter.default
        for name, parameter in inspect.signature(keyword).parameters.items()
    }

    assert math.isnan(defaults.pop("ratio"))
    assert defaults == {
        "label": "width",
        "count": 3,
        "upper": math.inf,
        "lower": -math.inf,
        "strict": False,
        "limit": None,
        "unit": None,
    }


def test_generated_keyword_sends_a_test_scoped_timeout(
    library: Browser, playwright: RecordingPlaywright
):
    keyword = generated_keyword(library, "openOwnContext", "defaultTimeout")

    library.set_browser_timeout(timedelta(milliseconds=1500), Scope.Test)
    keyword()

    assert playwright.payload() == {"arguments": [["defaultTimeout", 1500]]}
