import re
import zipfile
from pathlib import Path

from robot.libraries.BuiltIn import BuiltIn


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


def mark(word: str) -> None:
    """Runs an action on the active page whose trace entry mentions ``word``."""
    BuiltIn().get_library_instance("Browser").evaluate_javascript(None, f"() => '{word}'")


def trace_should_be(trace: str, *path_parts: str) -> None:
    """Verify that ``trace`` is the file the joined ``path_parts`` point to."""
    expected = Path(*path_parts).resolve()
    assert Path(trace) == expected, f"Trace {trace} is not {expected}"


def trace_should_be_in_directory(trace: str, *path_parts: str) -> None:
    """Verify that ``trace`` is a file directly in the directory of the joined ``path_parts``."""
    expected = Path(*path_parts).resolve()
    assert Path(trace).parent == expected, f"Trace {trace} is not in {expected}"
