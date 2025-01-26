from typing import Callable, Optional, Union

from assertionengine.formatter import FormatRules
from assertionengine.formatter import Formatter as ASFormatter
from robot.utils import DotDict

from Browser.utils.data_types import ensure_formatter_type

from ..base import LibraryComponent
from ..utils import (
    FormatingRules,
    FormatterKeywords,
    FormatterTypes,
    LambdaFunction,
    Scope,
    logger,
)
from ..utils import keyword as keyword_deco


class Formatter(ASFormatter, LibraryComponent):
    def set_assertion_formatter(
        self,
        keyword: Optional[FormatterKeywords] = None,
        *formatters: Union[FormatingRules, LambdaFunction],
        scope: Scope = Scope.Global,
    ) -> dict[str, list[str]]:
        """Set keyword assertion formatter with defined scope.

        Returns the old formatter from the scope.

        Calling keyword without ``formatters`` arguments will clear all formatters from the keyword.
        If ``keyword``  is None, then keyword will clear all formatters from all keywords.

        | =Arguments= | =Description= |
        | ``keyword`` | The name of a keyword where assertion formatter is applied. |
        | ``scope`` | Defines the lifetime of the formatter, possible values are Global, Suite and Test. |
        | ``formatters`` | List of formatter which will be applied to the assertion when keyword is called. |

        Example:
        | # Set strip assertion formatter for Get Text keyword for duration of the suite
        | `Set Assertion Formatter | `Get Text` | Suite | strip |
        | # Set strip and case insensitive assertion formatter for Get Text keyword for duration of the suite
        | `Set Assertion Formatter | `Get Text` | Suite | strip | case insensitive |
        | `Set Assertion Formatter | `Get Text` | Suite | # Removes Get Text formatters from suite level.
        """
        if keyword is None:
            return self._clear_all_formatters()
        kw = keyword.name
        if kw not in [k.name for k in FormatterKeywords]:
            raise ValueError(f"{keyword} is not keyword that supports formatters.")
        stack = self.assertion_formatter_stack.get()
        old_scope_functions = stack.get(kw, [])
        old_scope = self._convert_scope_to_strings(old_scope_functions)
        stack[kw] = list(self.get_formatter_functions(formatters))
        self.assertion_formatter_stack.set(stack, scope)
        return {keyword.name: old_scope}

    def get_formatter_functions(self, formatters):
        for formatter in formatters:
            if callable(formatter):
                yield formatter
            elif isinstance(formatter, FormatingRules):
                yield FormatRules[formatter.name]
            elif isinstance(formatter, str) and formatter.lower() in FormatRules:
                yield FormatRules[formatter.lower()]
            else:
                raise ValueError(
                    f"{formatter} is not valid formatter. Choose from {FormatRules.keys()} or define a lambda function."
                )

    def _clear_all_formatters(self):
        for formatter_kw in FormatterKeywords:
            logger.debug(f"Clear keyword formatter: {formatter_kw.name}")
            self.set_assertion_formatter(formatter_kw)
        return []

    def method_to_kw_str(self, keyword: Callable) -> str:
        name = keyword.__name__
        return name.replace("_", " ").title()

    def _convert_scope_to_strings(self, scopes: list) -> list:
        scopes_str = []
        for rule_name, rule_method in FormatRules.items():
            for scope in scopes:
                if scope == rule_method:
                    scopes_str.append(rule_name)
        return scopes_str

    def get_formatter(self, keyword: str) -> list:
        stack = self.assertion_formatter_stack.get()
        return stack.get(keyword, [])

    def set_formatter(self, keyword, formatter):
        pass

    @keyword_deco(tags=("Config",))
    def set_assertion_formatters(
        self, formatters: FormatterTypes, scope: Scope = Scope.Suite
    ) -> dict[str, list[str]]:
        """Set keywords formatters for assertions.

        | =Arguments= | =Description= |
        | ``formatters`` | Dictionary of keywords and formatters, where key is the keyword name where formatters are applied. Dictionary value is a list of formatter which are applied. Formatters for a defined keyword are always overwritten. An empty list will clear all formatters for the keyword. If ``formatters`` is empty dictionary, then all formatters are cleared from all keywords. |
        | ``scope`` | Defines the lifetime of the formatter, possible values are Global, Suite and Test. |

        See type documentation of `FormatterTypes` for more information.

        It is possible to define own formatters as lambda functions.

        Example:
        | `Set Assertion Formatters`    {"Get Text": ["strip", "normalize spaces"]}  # This will convert all kind of spaces to single space and removes spaces from start and end of the string.
        | `Set Assertion Formatters`    {"Get Title": ["apply to expected","lambda x: x.replace(' ', '')"]}  # This will remove all spaces from the string.
        """
        if not formatters:
            return DotDict(self.set_assertion_formatter())
        formatters = ensure_formatter_type(formatters)
        old_formatters = DotDict()
        for kw, kw_format in formatters.items():
            old_formatters.update(
                self.set_assertion_formatter(kw, *kw_format, scope=scope)
            )
        return old_formatters
