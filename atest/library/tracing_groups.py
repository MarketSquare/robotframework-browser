import json
from fnmatch import fnmatchcase
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


def get_trace_group_parent_title(path: Path, title_pattern: str) -> str | None:
    """Returns the title of the group that holds the first group matching the glob
    ``title_pattern``, ``None`` at top level."""
    groups = [
        line for line in get_trace_lines(path) if line.get("method") == "tracingGroup"
    ]
    titles = {group["callId"]: group["title"] for group in groups}
    group = next(
        group for group in groups if fnmatchcase(group["title"], title_pattern)
    )
    return titles.get(group.get("parentId"))
