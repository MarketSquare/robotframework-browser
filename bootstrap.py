"""Creates a virtual environment for developing the library.

Also installs the dependencies locked in uv.lock.
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

if not VENV_DIR.exists():
    print(f"Creating virtualenv in {VENV_DIR}")
    EnvBuilder(with_pip=True).create(VENV_DIR)

uv_installed = (
    subprocess.run(
        [VENV_PYTHON, "-m", "uv", "--version"], check=False, capture_output=True
    ).returncode
    == 0
)
if not uv_installed:
    subprocess.run([VENV_PYTHON, "-m", "pip", "install", "uv"], check=True)
subprocess.run(
    [VENV_PYTHON, "-m", "uv", "sync", "--locked", "--all-groups"],
    cwd=ROOT_DIR,
    check=True,
)

activate_script = (
    "source .venv/bin/activate"
    if not platform.platform().startswith("Windows")
    else ".venv\\Scripts\\activate.bat"
)
print(f"Virtualenv `{VENV_DIR}` is ready and up-to-date.")
print(f"Run `{activate_script}` to activate the virtualenv.")
