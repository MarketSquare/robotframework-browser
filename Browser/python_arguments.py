# Copyright 2017- Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import inspect
from collections.abc import Callable, Mapping
from functools import wraps
from typing import NamedTuple

from robot.running.arguments.typeconverters import TypeConverter
from robotlibcore import DynamicCore  # type: ignore

from .utils.data_types import RobotTypeConverter


def _detached(value):
    """Return a value the converter may rewrite without touching the caller's own object."""
    if isinstance(value, Mapping):
        return _rebuild(value, {key: _detached(item) for key, item in value.items()})
    if isinstance(value, (list, tuple, set, frozenset)):
        return _rebuild(value, [_detached(item) for item in value])
    return value


def _rebuild(original, items):
    """Put copied items back into a container of the caller's own type."""
    try:
        return type(original)(items)
    except TypeError:
        return items if isinstance(original, Mapping) else original


class _ArgumentConverter(NamedTuple):
    """A parameter that needs converting, and everything needed to convert it."""

    name: str
    converter: TypeConverter
    kind: inspect._ParameterKind

    def convert(self, value):
        """Convert one bound argument, or its elements when it is *args / **kwargs."""
        if value is None:
            return None
        # For *args and **kwargs the type hint is the item type, so convert each element
        # rather than the tuple or dict holding them.
        if self.kind is inspect.Parameter.VAR_POSITIONAL:
            return tuple(self._convert_one(item) for item in value)
        if self.kind is inspect.Parameter.VAR_KEYWORD:
            return {key: self._convert_one(item) for key, item in value.items()}
        return self._convert_one(value)

    def _convert_one(self, value):
        # A Python caller who means "nothing" passes the None object. Never convert it: on a
        # `str` hint Robot Framework turns None into the string "None".
        if value is None:
            return None
        return self.converter.convert(name=self.name, value=_detached(value))


def converting_proxy(bound_method: Callable, types: dict) -> Callable:
    """Return a proxy that converts plain Python values to the declared keyword types.

    Keywords with nothing convertible are returned unchanged, so an attribute lookup on
    them costs exactly what it costs today.
    """
    if not types:
        return bound_method
    signature = inspect.signature(bound_method)
    plan = [
        _ArgumentConverter(name, converter, signature.parameters[name].kind)
        for name, hint in types.items()
        if name in signature.parameters
        and (converter := RobotTypeConverter.converter_for(hint))
    ]
    if not plan:
        return bound_method

    # @wraps is required, not cosmetic: `rfbrowser translate` reads __name__ and __doc__ off
    # these entries and checksums the doc. Dropping it silently changes every translation
    # checksum in the project.
    @wraps(bound_method)
    def wrapper(*args, **kwargs):
        try:
            bound = signature.bind(*args, **kwargs)
        except TypeError:
            return bound_method(*args, **kwargs)
        for argument in plan:
            if argument.name in bound.arguments:
                bound.arguments[argument.name] = argument.convert(
                    bound.arguments[argument.name]
                )
        return bound_method(*bound.args, **bound.kwargs)

    return wrapper


def add_argument_conversion(library: DynamicCore) -> None:
    """Give the Python path argument conversion, leaving the Robot Framework path alone.

    Robot Framework reaches keywords through the keyword table (``library.keywords``);
    Python reaches them through the attribute table (``library.attributes``). The two are
    separate dicts holding the same bound methods, so rebuilding only the attribute table
    leaves the Robot Framework execution path byte-for-byte unchanged. That is why
    conversion appears on a keyword the module defining it knows nothing about.

    Types are resolved through the keyword table and cached by the bound method itself:
    ``keywords_spec`` is keyed by Robot name only, while ``attributes`` is keyed by both the
    method name and the Robot name. Looking types up by ``__name__`` raises for every
    ``@keyword(name=...)`` keyword, and wrapping per attribute entry would build two
    wrappers for the keywords that carry an alias.

    Must be called after ``DynamicCore.__init__``, which is what fills both tables.
    """
    types_by_method = {
        keyword: library.get_keyword_types(keyword_name)
        for keyword_name, keyword in library.keywords.items()
    }
    wrapped: dict = {}
    for name, keyword in list(library.attributes.items()):
        if keyword not in wrapped:
            wrapped[keyword] = converting_proxy(
                keyword, types_by_method.get(keyword, {})
            )
        library.attributes[name] = wrapped[keyword]
