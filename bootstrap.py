"""Creates a virtual environment for developing the library.

Also installs the needed dependencies.
"""

from pathlib import Path
import platform
import subprocess
import sys
from venv import EnvBuilder

venv_dir = Path(".") / ".venv"
src_dir = Path(".") / "Browser"

if not venv_dir.exists():
    print(f"Creating virtualenv in {venv_dir}")
    EnvBuilder(with_pip=True).create(venv_dir)

subprocess.run(
    [
        sys.executable,
        "-m",
        "pip",
        "install",
        "-r",
        str(src_dir / "dev-requirements.txt"),
    ]
)
subprocess.run(
    [sys.executable, "-m", "pip", "install", "-r", str(src_dir / "requirements.txt")]
)

activate_script = (
    "source .venv/bin/activate"
    if sys.platform != "Windows"
    else ".venv\Scripts\activate.bat"
)
print(f"Virtualenv `{venv_dir}` is ready and up-to-date.")
print(f"Run `{activate_script}` to activate the virtualenv.")
