import sys
from pathlib import Path

from robot.api.exceptions import SkipExecution


def get_electron_binary_path(app_dir: str) -> str:
    """Return the platform-specific Electron binary path for the test suite.

    Raises SkipExecution when app_dir does not exist so the caller suite is
    gracefully skipped (e.g. BrowserBatteries runs that remove node/).

    The Electron binary is resolved from the project root node_modules/,
    which is populated by npm ci at project level before tests run.
    """
    app_path = Path(app_dir)
    if not app_path.exists():
        raise SkipExecution(
            f"Electron test app not present ({app_dir} missing) — skipping suite."
        )

    electron_dist = app_path.parent.parent / "node_modules" / "electron" / "dist"

    if sys.platform == "win32":
        return str(electron_dist / "electron.exe")
    if sys.platform == "darwin":
        return str(electron_dist / "Electron.app" / "Contents" / "MacOS" / "Electron")
    return str(electron_dist / "electron")
