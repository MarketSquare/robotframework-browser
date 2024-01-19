from datetime import timedelta
from unittest.mock import MagicMock, PropertyMock

from approvaltests.approvals import verify  # type: ignore

from Browser.base.librarycomponent import LibraryComponent


def test_presenter_mode_default():
    lib = MagicMock()
    type(lib).presenter_mode = {}
    ctx = LibraryComponent(lib)
    verify(ctx.get_presenter_mode)


def test_presenter_mode_duration_as_string():
    lib = MagicMock()
    p = PropertyMock(return_value={"color": "white", "duration": "4s"})
    type(lib).presenter_mode = p
    ctx = LibraryComponent(lib)
    verify(ctx.get_presenter_mode)


def test_presenter_mode_duration_as_timedelta():
    lib = MagicMock()
    duration = timedelta(seconds=5)
    p = PropertyMock(return_value={"color": "black", "duration": duration})
    type(lib).presenter_mode = p
    ctx = LibraryComponent(lib)
    verify(ctx.get_presenter_mode)
