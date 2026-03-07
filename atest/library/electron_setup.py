import subprocess
import sys
from pathlib import Path

from robot.api.exceptions import SkipExecution


def install_electron_test_app(app_dir: str) -> str:
    """Install npm dependencies and return the platform-specific Electron binary path.

    Raises SkipExecution when app_dir does not exist so the caller suite is
    gracefully skipped (e.g. BrowserBatteries runs that remove node/).
    Skips the npm ci step when node_modules is already present.
    """
    app_path = Path(app_dir)
    if not app_path.exists():
        raise SkipExecution(
            f"Electron test app not present ({app_dir} missing) — skipping suite."
        )

    node_modules = app_path / "node_modules"
    if not node_modules.exists():
        npm = "npm.cmd" if sys.platform == "win32" else "npm"
        result = subprocess.run(
            [npm, "ci"],
            cwd=str(app_path),
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(f"npm ci failed in {app_dir}:\n{result.stderr}")

    if sys.platform == "win32":
        return str(app_path / "node_modules" / "electron" / "dist" / "electron.exe")
    if sys.platform == "darwin":
        return str(
            app_path
            / "node_modules"
            / "electron"
            / "dist"
            / "Electron.app"
            / "Contents"
            / "MacOS"
            / "Electron"
        )
    return str(app_path / "node_modules" / "electron" / "dist" / "electron")
