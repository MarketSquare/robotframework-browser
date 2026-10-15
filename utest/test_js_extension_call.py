import inspect
import json
from contextlib import contextmanager
from datetime import timedelta
from types import SimpleNamespace

from Browser import Browser
from Browser.base import LibraryComponent
from Browser.utils.data_types import Scope


class RecordingPlaywright:
    def __init__(self):
        self.requests = []

    @contextmanager
    def grpc_channel(self):
        yield self

    def CallExtensionKeyword(self, request):  # noqa: N802 - the name of the gRPC method
        self.requests.append(request)
        return []

    def SetTimeout(self, request):  # noqa: N802 - the name of the gRPC method
        return SimpleNamespace(log="")

    def payload(self) -> dict:
        return json.loads(self.requests[-1].arguments)


def library_with_recorded_calls(
    tmpdir, monkeypatch
) -> tuple[Browser, RecordingPlaywright]:
    monkeypatch.setattr(Browser, "_output_dir", tmpdir)
    library = Browser(timeout=timedelta(seconds=7))
    library._playwright = RecordingPlaywright()
    return library, library._playwright


def generated_keyword(library: Browser, name: str, arguments: str):
    component = LibraryComponent(library)
    library._jskeyword_call(component, name, arguments, "")
    return getattr(component, name)


def test_generated_keyword_passes_the_library_timeout_as_default_timeout(
    tmpdir, monkeypatch
):
    library, playwright = library_with_recorded_calls(tmpdir, monkeypatch)
    keyword = generated_keyword(library, "openOwnContext", "url, defaultTimeout")

    keyword("https://a.b")

    assert list(inspect.signature(keyword).parameters) == ["url"]
    assert playwright.payload() == {
        "arguments": [["url", "https://a.b"], ["defaultTimeout", 7000]]
    }


def test_generated_keyword_reads_the_library_timeout_at_each_call(tmpdir, monkeypatch):
    library, playwright = library_with_recorded_calls(tmpdir, monkeypatch)
    keyword = generated_keyword(library, "openOwnContext", "defaultTimeout")

    library.set_browser_timeout(timedelta(seconds=3), Scope.Global)
    keyword()

    assert playwright.payload() == {"arguments": [["defaultTimeout", 3000]]}


def test_other_generated_keywords_send_only_their_arguments(tmpdir, monkeypatch):
    library, playwright = library_with_recorded_calls(tmpdir, monkeypatch)

    generated_keyword(library, "clickTwice", "selector, page")("#button")

    assert playwright.payload() == {
        "arguments": [["selector", "#button"], ["page", "RESERVED"]]
    }


def test_call_js_keyword_sends_the_arguments_as_given(tmpdir, monkeypatch):
    library, playwright = library_with_recorded_calls(tmpdir, monkeypatch)

    library.call_js_keyword("openOwnContext", url="https://a.b", defaultTimeout=5000)

    assert playwright.payload() == {
        "arguments": [["url", "https://a.b"], ["defaultTimeout", 5000]]
    }
