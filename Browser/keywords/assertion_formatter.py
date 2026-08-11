from collections.abc import Callable

from assertionengine.assertion_formatter import FormatRules
from assertionengine.assertion_formatter import Formatter as ASFormatter
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
        keyword: FormatterKeywords | None = None,
        *formatters: FormatingRules | LambdaFunction,
        scope: Scope = Scope.Global,
    ) -> dict[str, list[str]]:
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
        | ``formatters`` | Dictionary of keywords and formatters, where the key is the name of the keyword where the formatters are applied. The dictionary value is a list of formatters which are applied. Formatters for a defined keyword are always overwritten. An empty list will clear all formatters for the keyword. If ``formatters`` is an empty dictionary, then all formatters are cleared from all keywords, in the Global scope, regardless of the ``scope`` argument. |
        | ``scope`` | Defines the lifetime of the formatter, possible values are Global, Suite and Test. |

        Returns the formatters which were in use before this keyword was called.
        Formatters defined as lambda functions are not included in the returned value.

        See type documentation of `FormatterKeywords` and `FormatingRules` for more information.

        It is possible to define own formatters as lambda functions.

        Example:
        | `Set Assertion Formatters`    {"Get Text": ["strip", "normalize spaces"]}  # This will convert all kinds of spaces to a single space and remove spaces from the start and end of the string.
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
