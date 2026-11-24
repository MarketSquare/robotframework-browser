from typing import cast

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

from Browser import Browser
from Browser.utils.data_types import HighLightElement


def set_presenter_mode(status: HighLightElement | bool = False):
    """Set presenter mode in Browser library"""
    browser = cast(Browser, BuiltIn().get_library_instance("Browser"))
    logger.info(f"Set presenter_mode to {status}")
    browser.presenter_mode = status
