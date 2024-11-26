from pathlib import Path


def get_language() -> list:
    curr_dir = Path(__file__).parent.absolute()
    return [
        {"language": "eng", "path": curr_dir / "translate_1.json"},
        {"language": "swe", "path": curr_dir / "translate_2.json"},
    ]
