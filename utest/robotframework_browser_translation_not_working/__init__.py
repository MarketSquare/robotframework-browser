from pathlib import Path


def get_language_not_working() -> dict:
    curr_dir = Path(__file__).parent.absolute()
    return {"language": "fi", "path": curr_dir / "translate.json"}
