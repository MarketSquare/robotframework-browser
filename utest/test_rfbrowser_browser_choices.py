import shutil
import subprocess
from pathlib import Path

import pytest
from click.testing import CliRunner

from Browser.entry.__main__ import cli

REPO_ROOT = Path(__file__).parent.parent
NOT_INSTALLABLE_BY_PLAYWRIGHT = ["chromium-tip-of-tree-headless-shell", "bidi-chromium"]


def offered_browsers(command: str) -> list[str]:
    browser = next(p for p in cli.commands[command].params if p.name == "browser")
    return list(browser.type.choices)


@pytest.mark.parametrize("command", ["init", "install"])
def test_playwright_can_install_every_offered_browser(command):
    npx = shutil.which("npx")
    assert npx, "npx not found in PATH"
    result = subprocess.run(
        [npx, "playwright", "install", "--dry-run", *offered_browsers(command)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("browser", NOT_INSTALLABLE_BY_PLAYWRIGHT)
@pytest.mark.parametrize("command", ["init", "install"])
def test_browser_playwright_cannot_install_is_rejected(command, browser):
    result = CliRunner().invoke(cli, [command, browser])
    assert result.exit_code == 2
    assert "Invalid value" in result.output
    assert browser in result.output


@pytest.mark.parametrize("command", ["init", "install"])
def test_webkit_for_wsl_is_offered(command):
    assert "webkit-wsl" in offered_browsers(command)


class RecordingBrowser:
    def __init__(self):
        self.npx_calls = []

    def execute_npx_playwright(self, command, *args):
        self.npx_calls.append((command, *args))


def test_install_accepts_browser_name_in_any_case(monkeypatch, tmp_path):
    monkeypatch.setenv("PLAYWRIGHT_BROWSERS_PATH", str(tmp_path))
    browser = RecordingBrowser()
    monkeypatch.setattr("Browser.entry.__main__.get_browser_lib", lambda: browser)
    result = CliRunner().invoke(cli, ["install", "WebKit"])
    assert result.exit_code == 0, result.output
    assert browser.npx_calls == [("install", "webkit")]
