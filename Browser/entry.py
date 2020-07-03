import os
import sys
from subprocess import Popen, PIPE, STDOUT

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
    else:
        print(f"Invalid command `{cmd}`")
        print(USAGE)
