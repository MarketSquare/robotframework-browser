from datetime import timedelta
from os import PathLike

from assertionengine import AssertionOperator
from robot.api.deco import keyword

from Browser import Browser, KeyboardModifier, MouseButton
from Browser.base.librarycomponent import LibraryComponent
from Browser.utils.data_types import ClientCertificate, Proxy, RecordVideo
from Browser.utils.types import Secret


class KeywordArgumentSpy(LibraryComponent):
    def __init__(self, library: Browser):
        super().__init__(library)
        library.spy_calls = []

    def _record(self, name, *args, **kwargs):
        self.library.spy_calls.append((name, args, kwargs))

    @keyword
    def spy_enum(self, button: MouseButton = MouseButton.left):
        self._record("spy_enum", button)

    @keyword
    def spy_text(self, text: str):
        self._record("spy_text", text)

    @keyword
    def spy_optional_text(self, text: str | None = None):
        self._record("spy_optional_text", text)

    @keyword
    def spy_operator(self, operator: AssertionOperator | None = None):
        self._record("spy_operator", operator)

    @keyword
    def spy_secret(self, secret: str | Secret):
        self._record("spy_secret", secret)

    @keyword
    def spy_proxy(self, proxy: Proxy | None = None):
        self._record("spy_proxy", proxy)

    @keyword
    def spy_record_video(self, recordVideo: RecordVideo | None = None):
        self._record("spy_record_video", recordVideo)

    @keyword
    def spy_certificates(self, certificates: list[ClientCertificate] | None = None):
        self._record("spy_certificates", certificates)

    @keyword
    def spy_delay(self, delay: timedelta | None = None):
        self._record("spy_delay", delay)

    # Shaped like `click_with_options`: a defaulted positional before the varargs and a
    # keyword-only argument after them, which is what drives the bound.args/bound.kwargs split.
    @keyword
    def spy_modifiers(
        self,
        selector: str,
        button: MouseButton = MouseButton.left,
        *modifiers: KeyboardModifier,
        delay: timedelta | None = None,
    ):
        self._record("spy_modifiers", selector, button, *modifiers, delay=delay)

    # Shaped like `upload_file_by_selector`: required positionals and nothing after the
    # varargs, the only other varargs shape in the library that carries a type hint.
    @keyword
    def spy_paths(self, selector: str, path: PathLike, *extra_paths: PathLike):
        self._record("spy_paths", selector, path, *extra_paths)

    @keyword
    def spy_counts(self, **counts: int):
        self._record("spy_counts", **counts)

    @keyword
    def spy_untyped(self, value):
        self._record("spy_untyped", value)

    @keyword(types={"button": MouseButton})
    def spy_declared_type(self, button="left"):
        self._record("spy_declared_type", button)

    @keyword(name="Spy Renamed")
    def spy_renamed(self, button: MouseButton = MouseButton.left):
        self._record("spy_renamed", button)
