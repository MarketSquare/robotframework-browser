"""Verify that ``rfbrowser clean-node`` actually removed the node dependencies.

CI runs ``rfbrowser clean-node`` as the last step before uninstalling the library,
so nothing after it observes anything except its exit code -- and the command
returns 0 whether it deleted the dependencies or merely found nothing to delete.
This asserts the result instead.

Run it *after* ``rfbrowser clean-node`` and *before* ``pip uninstall``: it locates
the installed package, and once pip has removed it there is nothing left to check.

Deliberately a script file rather than an inline ``python -c``. It reads the same
in bash and PowerShell, and because ``sys.path[0]`` is this file's directory rather
than the working directory, a ``Browser/`` source tree in the checkout cannot
shadow the installed package and send the check at the wrong directory.
"""

import importlib.util
import sys
from pathlib import Path

MAX_LISTED_LEFTOVERS = 10


def installed_node_modules() -> Path:
    """The node_modules directory belonging to the *installed* Browser package.

    Mirrors ``NODE_MODULES`` in ``Browser/entry/constant.py``, which is what
    ``clean-node`` deletes. Resolved without importing Browser, so this still works
    if the node side is already gone.
    """
    spec = importlib.util.find_spec("Browser")
    if spec is None or spec.origin is None:
        sys.exit(
            "Browser is not installed, so there is nothing to verify. "
            "Run this after 'rfbrowser clean-node' but before 'pip uninstall'."
        )
    return Path(spec.origin).parent / "wrapper" / "node_modules"


def main() -> int:
    node_modules = installed_node_modules()
    print(f"Checking {node_modules}")
    if node_modules.exists():
        leftovers = sorted(path.name for path in node_modules.iterdir())
        shown = ", ".join(leftovers[:MAX_LISTED_LEFTOVERS])
        sys.exit(
            f"rfbrowser clean-node exited 0 but {node_modules} is still present "
            f"with {len(leftovers)} entries: {shown}"
        )
    print("OK: rfbrowser clean-node removed the node dependencies.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
