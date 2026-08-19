import pytest
from click.testing import CliRunner

from Browser.entry import __main__ as entry
from Browser.entry.constant import PLAYWRIGHT_BROWSERS_PATH


class FakeBrowserLib:
    def __init__(self, error: Exception | None = None):
        self.calls: list[tuple] = []
        self._error = error

    def execute_npx_playwright(self, *args):
        self.calls.append(args)
        if self._error:
            raise self._error


@pytest.fixture(autouse=True)
def isolated_browsers_path(monkeypatch: pytest.MonkeyPatch):
    # ensure_playwright_browsers_path writes PLAYWRIGHT_BROWSERS_PATH into
    # os.environ and never removes it. Without this stub the variable escapes into
    # the rest of the pytest session and points every browser-backed test at a
    # directory that does not exist.
    monkeypatch.setattr(entry, "ensure_playwright_browsers_path", lambda: None)
    monkeypatch.delenv(PLAYWRIGHT_BROWSERS_PATH, raising=False)


@pytest.fixture
def browser_lib(monkeypatch: pytest.MonkeyPatch) -> FakeBrowserLib:
    lib = FakeBrowserLib()
    monkeypatch.setattr(entry, "get_browser_lib", lambda: lib)
    return lib


def test_runs_npx_playwright_uninstall(browser_lib: FakeBrowserLib):
    result = CliRunner().invoke(entry.uninstall)

    assert result.exit_code == 0, result.output
    assert browser_lib.calls == [("uninstall",)]


def test_all_flag_is_forwarded_to_npx(browser_lib: FakeBrowserLib):
    result = CliRunner().invoke(entry.uninstall, ["--all"])

    assert result.exit_code == 0, result.output
    assert browser_lib.calls == [("uninstall", "--all")]


def test_browsers_path_is_resolved_before_the_library_is_built(
    monkeypatch: pytest.MonkeyPatch,
):
    # Resolving it later would leave npx looking in Playwright's own default
    # location instead of this installation's, and it would remove nothing.
    order: list[str] = []
    lib = FakeBrowserLib()
    monkeypatch.setattr(
        entry, "ensure_playwright_browsers_path", lambda: order.append("ensure")
    )
    monkeypatch.setattr(
        entry, "get_browser_lib", lambda: (order.append("get_lib"), lib)[1]
    )

    result = CliRunner().invoke(entry.uninstall)

    assert result.exit_code == 0, result.output
    assert order == ["ensure", "get_lib"]


def test_a_failing_npx_uninstall_still_exits_zero():
    # contextlib.suppress(Exception) in the command, pinned so that a change to it
    # is deliberate. It is why the exit code alone is not evidence of success.
    lib = FakeBrowserLib(error=RuntimeError("npx exploded"))

    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setattr(entry, "get_browser_lib", lambda: lib)
        result = CliRunner().invoke(entry.uninstall)

    assert result.exit_code == 0, result.output
    assert lib.calls == [("uninstall",)]
