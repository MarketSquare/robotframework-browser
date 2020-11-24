from __future__ import annotations
from approvaltests import verify_all  # type: ignore

from Browser.utils.misc import type_converter


def test_type_converter():
    results = [
        type_converter(None),
        type_converter(""),
        type_converter(1),
        type_converter(True),
    ]
    verify_all("Type converter", results)
