import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner

from Browser.entry import __main__ as entry
from Browser.entry.constant import PLAYWRIGHT_BROWSERS_PATH, get_playwright_browser_path


@pytest.fixture(autouse=True)
def quiet_info(monkeypatch: pytest.MonkeyPatch):
    # clean-node shells out to pip freeze and npm -v before deleting anything.
    monkeypatch.setattr(entry, "_python_info", lambda: None)
    monkeypatch.setattr(entry, "_node_info", lambda: None)
    monkeypatch.setattr(entry, "log_install_dir", lambda *args: None)


@pytest.fixture
def node_modules(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    node_modules = tmp_path / "wrapper" / "node_modules"
    browsers = node_modules / "playwright-core" / ".local-browsers" / "chromium-1234"
    browsers.mkdir(parents=True)
    (browsers / "1").write_text("browser binary")
    (node_modules / "some-dependency").mkdir()
    (node_modules / "some-dependency" / "index.js").write_text("dependency")
    monkeypatch.setattr(entry, "NODE_MODULES", node_modules)
    monkeypatch.setattr("Browser.entry.constant.NODE_MODULES", node_modules)
    return node_modules


def test_deletes_the_node_dependencies(node_modules: Path):
    result = CliRunner().invoke(entry.clean_node)

    assert result.exit_code == 0, result.output
    assert not node_modules.exists()


def test_deletes_the_browser_binaries_in_the_default_location(
    node_modules: Path, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.delenv(PLAYWRIGHT_BROWSERS_PATH, raising=False)
    binaries = get_playwright_browser_path()
    assert binaries.is_dir()

    result = CliRunner().invoke(entry.clean_node)

    assert result.exit_code == 0, result.output
    assert not binaries.exists()


def test_keeps_browsers_installed_outside_the_default_location(
    node_modules: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    elsewhere = tmp_path / "shared-browsers"
    elsewhere.mkdir()
    (elsewhere / "chromium-1234").write_text("browser binary")
    monkeypatch.setenv(PLAYWRIGHT_BROWSERS_PATH, str(elsewhere))

    result = CliRunner().invoke(entry.clean_node)

    assert result.exit_code == 0, result.output
    assert not node_modules.exists()
    assert (elsewhere / "chromium-1234").exists()


def test_exits_zero_when_there_is_nothing_installed(
    node_modules: Path, caplog: pytest.LogCaptureFixture
):
    shutil.rmtree(node_modules)

    result = CliRunner().invoke(entry.clean_node)

    assert result.exit_code == 0, result.output
    assert "nothing to delete" in caplog.text


def test_real_default_browser_location_is_inside_the_deleted_directory():
    from Browser.entry.constant import NODE_MODULES  # noqa: PLC0415

    assert get_playwright_browser_path().is_relative_to(NODE_MODULES)
