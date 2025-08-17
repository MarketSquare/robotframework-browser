"""Creates a virtual environment for developing the library.

Also installs the needed dependencies.
"""

import platform
import subprocess
from pathlib import Path
from venv import EnvBuilder

ROOT_DIR = Path(__file__).parent
VENV_DIR = ROOT_DIR / ".venv"
if not platform.platform().startswith("Windows"):
    VENV_PYTHON = VENV_DIR / "bin" / "python"
else:
    VENV_PYTHON = VENV_DIR / "Scripts" / "python.exe"
SRC_DIR = ROOT_DIR / "Browser"

if not VENV_DIR.exists():
    print(f"Creating virtualenv in {VENV_DIR}")
    EnvBuilder(with_pip=True).create(VENV_DIR)

subprocess.run([VENV_PYTHON, "-m", "pip", "install", "-U", "uv"], check=True)
subprocess.run(
    [
        VENV_PYTHON,
        "-m",
        "uv",
        "pip",
        "install",
        "-r",
        str(SRC_DIR / "dev-requirements.txt"),
    ],
    check=True,
)
subprocess.run(
    [
        VENV_PYTHON,
        "-m",
        "uv",
        "pip",
        "install",
        "-r",
        str(ROOT_DIR / "pyproject.toml"),
    ],
    check=True,
)

activate_script = (
    "source .venv/bin/activate"
    if not platform.platform().startswith("Windows")
    else ".venv\\Scripts\\activate.bat"
)
print(f"Virtualenv `{VENV_DIR}` is ready and up-to-date.")
print(f"Run `{activate_script}` to activate the virtualenv.")
