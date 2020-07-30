import os
from subprocess import Popen, PIPE, STDOUT, DEVNULL, CalledProcessError
import subprocess
import sys
from pathlib import Path

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
    installation_dir = os.path.join(rfbrowser_dir, "wrapper")
    subfolders = os.listdir(rfbrowser_dir.parent) + os.listdir(installation_dir)

    if "node_modules" in subfolders:
        return
    logger.error("Run `rfbrowser init` to install node dependencies")
    sys.exit(1)
    return


def rfbrowser_init():
    print("installing node dependencies...")
    installation_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "wrapper"
    )
    if not os.path.isfile(os.path.join(installation_dir, "package.json")):
        print(
            "Directory needs to contain package.json "
            + "and have write permissions to succesfully install all dependencies. "
            + "\nPrinting contents:"
        )
        for root, dirs, files in os.walk(installation_dir):
            level = root.replace(installation_dir, "").count(os.sep)
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
