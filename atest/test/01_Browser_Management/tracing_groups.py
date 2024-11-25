import json
from pathlib import Path
from typing import Union

def get_trace_lines(path: Path) -> list[dict]:
    with path.open(encoding='utf-8') as file:
        return [ json.loads(line) for line in file.readlines() if '"type":"before"' in line ]

def get_file_line(file: Union[Path, None], line: int, column: int) -> str:
    if file is None:
        return
    with file.open(encoding='utf-8') as file:
        return file.readlines()[line-1]