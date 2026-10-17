import json
from pathlib import Path


def get_trace_lines(path: Path) -> list[dict]:
    """Returns the ``before`` entries of a Playwright trace file."""
    with path.open(encoding="utf-8") as file:
        return [
            json.loads(line) for line in file.readlines() if '"type":"before"' in line
        ]


def get_trace_group_titles(path: Path) -> list[str]:
    """Returns the titles of the trace groups in a Playwright trace file, in order."""
    return [
        line["title"]
        for line in get_trace_lines(path)
        if line.get("method") == "tracingGroup"
    ]


def get_file_line(file: Path | None, line: int, column: int) -> str | None:
    """Returns line ``line`` of ``file``, or ``None`` without a file."""
    if file is None:
        return None
    with file.open(encoding="utf-8") as source:
        return source.readlines()[line - 1]
