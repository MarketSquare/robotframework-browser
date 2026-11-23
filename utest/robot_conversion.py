import inspect
from typing import get_type_hints

from robot.running.arguments.typeinfo import TypeInfo

from Browser import Browser

# Robot Framework keeps a value of an unknown type, such as Secret before 7.4. On 7.3,
# TypeInfo.convert raises for one unless allow_unknown is given, as Robot Framework does.
_KEEP_UNKNOWN = (
    {"allow_unknown": True}
    if "allow_unknown" in inspect.signature(TypeInfo.convert).parameters
    else {}
)


def convert_like_robot(keyword, argument: str, value):
    """Converts ``value`` the way Robot Framework does for ``argument`` of ``keyword``."""
    hint = get_type_hints(keyword)[argument]
    return TypeInfo.from_type_hint(hint).convert(
        value, custom_converters=Browser.ROBOT_LIBRARY_CONVERTERS, **_KEEP_UNKNOWN
    )
