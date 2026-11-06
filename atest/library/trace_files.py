import re
import zipfile
from pathlib import Path


def get_trace_marks(trace_zip: Path) -> list[str]:
    """Returns the sorted ``MARK_*`` words that the actions in a trace zip mention."""
    with zipfile.ZipFile(trace_zip) as archive:
        text = "".join(
            archive.read(name).decode("utf-8", errors="replace")
            for name in archive.namelist()
            if name.endswith(".trace")
        )
    return sorted(set(re.findall(r"MARK_\w+", text)))


def find_traces_with_mark(directory: Path, mark: str) -> list[str]:
    """Returns the trace zips directly under ``directory`` whose actions mention ``mark``."""
    return [
        str(trace_zip)
        for trace_zip in sorted(Path(directory).glob("*.zip"))
        if mark in get_trace_marks(trace_zip)
    ]
