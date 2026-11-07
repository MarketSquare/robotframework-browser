import pytest
from click.testing import CliRunner

from Browser.entry.__main__ import cli

REMOVED_BY_PLAYWRIGHT = "chromium-tip-of-tree-headless-shell"


@pytest.mark.parametrize("command", ["init", "install"])
def test_browser_removed_by_playwright_is_rejected(command):
    result = CliRunner().invoke(cli, [command, REMOVED_BY_PLAYWRIGHT])
    assert result.exit_code == 2
    assert "Invalid value" in result.output
    assert REMOVED_BY_PLAYWRIGHT in result.output
