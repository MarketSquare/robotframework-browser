from unittest.mock import patch

import pytest
from click.testing import CliRunner

from Browser.entry.__main__ import cli


@pytest.mark.parametrize(
    ("args", "command"),
    [
        (["init"], "npx --quiet playwright install"),
        (["init", "--verbose"], "npx playwright install"),
        (["init", "--verbose", "firefox"], "npx playwright install firefox "),
    ],
)
def test_init_browser_install_command(monkeypatch, args, command):
    monkeypatch.setenv("PLAYWRIGHT_BROWSERS_PATH", "0")
    with (
        patch("Browser.entry.rfbrowser_init._check_files_and_access"),
        patch("Browser.entry.rfbrowser_init._check_npm"),
        patch("Browser.entry.rfbrowser_init._process_poller"),
        patch("Browser.entry.rfbrowser_init.has_pty", False),
        patch("Browser.entry.rfbrowser_init.subprocess.Popen") as popen,
    ):
        result = CliRunner().invoke(cli, args)
    assert result.exit_code == 0, result.output
    assert popen.call_args_list[-1].args[0] == command
