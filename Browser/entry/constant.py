import platform
from pathlib import Path

INSTALLATION_DIR = Path(__file__).parent.parent / "wrapper"
NODE_MODULES = INSTALLATION_DIR / "node_modules"
IS_WINDOWS = platform.system() == "Windows"
# This is required because weirdly windows doesn't have `npm` in PATH without shell=True.
# But shell=True breaks our linux CI
SHELL = bool(IS_WINDOWS)
ROOT_FOLDER = Path(__file__).resolve().parent.parent
LOG_FILE = "rfbrowser.log"
INSTALL_LOG = ROOT_FOLDER / LOG_FILE
PLAYWRIGHT_BROWSERS_PATH = "PLAYWRIGHT_BROWSERS_PATH"
