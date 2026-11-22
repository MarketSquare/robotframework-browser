import shutil
from pathlib import Path

import Browser

NODE_WORKING_DIRECTORY = Path(Browser.__file__).parent / "wrapper"


def remove_from_node_working_directory(name: str) -> None:
    """Remove a file or folder that the Node process created from a relative path.

    The library starts the Node process in its wrapper folder, so a relative path that Node
    resolves itself lands there. Nothing happens when ``name`` does not exist there.
    """
    path = NODE_WORKING_DIRECTORY / name
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()
