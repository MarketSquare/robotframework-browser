import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).parent.parent
STATIC = ROOT / "node" / "playwright-wrapper" / "static"


def _static_files() -> set[str]:
    """The files in the wrapper's static folder: the committed ones and those
    ``node/build.wrapper.js`` writes there, also before it ran."""
    build = (ROOT / "node" / "build.wrapper.js").read_text(encoding="utf-8")
    built = re.findall(r"outfile: '\./node/playwright-wrapper/static/([^']+)'", build)
    return {path.name for path in STATIC.glob("*.js")} | set(built)


def test_the_wheel_ships_every_static_file_of_the_wrapper() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    shipped = set(pyproject["tool"]["setuptools"]["package-data"]["*"])
    static = _static_files()
    assert "recorder-toolbar.js" in static
    assert static - shipped == set()
