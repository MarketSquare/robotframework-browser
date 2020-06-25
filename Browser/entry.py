import os
import sys
from subprocess import Popen, PIPE

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
        print("installing node dependencies...")
        installation_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "wrapper"
        )
        process = Popen(
            "npm install --production",
            shell=True,
            cwd=installation_dir,
            stdout=PIPE,
            stderr=PIPE,
        )
        if process.stdout is None:
            raise RuntimeError("problem installing node dependencies")
        for line in process.stdout:
            print(line.decode("utf-8"))
    else:
        print(f"Invalid command `{cmd}`")
        print(USAGE)
