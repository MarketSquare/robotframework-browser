import os
import subprocess
import sys
from pathlib import Path
from subprocess import DEVNULL, PIPE, STDOUT, CalledProcessError, Popen

from .utils import logger

USAGE = """USAGE
  rf-browser [command]
AVAILABLE COMMANDS
  init  Install required nodejs dependencies
"""


def run():
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "init":
        rfbrowser_init()
    else:
        print(f"Invalid command `{cmd}`")
        print(USAGE)


def ensure_node_dependencies():
    # Skip the checks when initializing
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        return
    # Checks if node is in PATH, errors if it isn't
    try:
        subprocess.run(["node", "-v"], stdout=DEVNULL, check=True)
    except (CalledProcessError, FileNotFoundError, PermissionError) as exception:
        print(
            "Couldn't execute node. Please ensure you have node.js installed and in PATH."
            "See https://nodejs.org/ for documentation"
        )
        sys.exit(exception)
        return

    rfbrowser_dir = Path(__file__).parent
    installation_dir = rfbrowser_dir / "wrapper"
    # This second application of .parent is necessary to find out that a developer setup has node_modules correctly
    project_folder = rfbrowser_dir.parent
    subfolders = os.listdir(project_folder) + os.listdir(installation_dir)

    if "node_modules" in subfolders:
        return
    logger.error("Run `rfbrowser init` to install node dependencies")
    sys.exit(1)
    return


def rfbrowser_init():
    print("installing node dependencies...")
    installation_dir = Path(__file__).parent / "wrapper"

    if not (installation_dir / "package.json").is_file():
        print(
            "Directory needs to contain package.json "
            + "and have write permissions to succesfully install all dependencies. "
            + "\nPrinting contents:"
        )
        for root, dirs, files in os.walk(installation_dir):
            level = root.replace(installation_dir.__str__(), "").count(os.sep)
            indent = " " * 4 * (level)
            print("{}{}/".format(indent, os.path.basename(root)))
            subindent = " " * 4 * (level + 1)
            for f in files:
                print("{}{}".format(subindent, f))
        raise RuntimeError("Could not find robotframework-browser's package.json")

    print("installing rfbrowser node dependencies at {}".format(installation_dir))
    process = Popen(
        "npm install --production",
        shell=True,
        cwd=installation_dir,
        stdout=PIPE,
        stderr=STDOUT,
    )

    for line in process.stdout:
        print(line.decode("utf-8"))

    if process.returncode is not None:
        raise RuntimeError(
            "Problem installing node dependencies."
            + f"Node process returned with exit status {process.returncode}"
        )

    print("rfbrowser init completed")
