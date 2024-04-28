"""Creates a virtual environment for developing the library.

Also installs the needed dependencies.
"""

import platform
import subprocess
from pathlib import Path
from venv import EnvBuilder

venv_dir = Path(__file__).parent / ".venv"
if not platform.platform().startswith("Windows"):
    venv_python = venv_dir / "bin" / "python"
else:
    venv_python = venv_dir / "Scripts" / "python.exe"
src_dir = Path(__file__).parent / "Browser"

if not venv_dir.exists():
    print(f"Creating virtualenv in {venv_dir}")
    EnvBuilder(with_pip=True).create(venv_dir)

subprocess.run([venv_python, "-m", "pip", "install", "-U", "uv"], check=True)
subprocess.run(
    [
        venv_python,
        "-m",
        "uv",
        "pip",
        "install",
        "-r",
        str(src_dir / "dev-requirements.txt"),
    ],
    check=True,
)

activate_script = (
    "source .venv/bin/activate"
    if not platform.platform().startswith("Windows")
    else ".venv\\Scripts\\activate.bat"
)
print(f"Virtualenv `{venv_dir}` is ready and up-to-date.")
print(f"Run `{activate_script}` to activate the virtualenv.")
