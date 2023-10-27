from typing import Callable, Dict, List, Optional

from assertionengine.formatter import FormatRules
from assertionengine.formatter import Formatter as ASFormatter

from ..base import LibraryComponent
from ..utils import Scope, logger
from ..utils import keyword as keyword_deco

FormatterTypes = Dict[str, List[str]]


class Formatter(ASFormatter, LibraryComponent):
    @keyword_deco(tags=("Config",))
    def set_assertion_formatter(
        self,
        keyword: Optional[str] = None,
        scope: Scope = Scope.Global,
        *formatters: str,
    ) -> list:
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
        kw = self.normalize_keyword(keyword)
        if kw not in self.library.keywords:
            raise ValueError(f"{keyword} is not library keyword")
        formatter_methods = self.formatters_to_method(list(formatters))
        stack = self.assertion_formatter_stack.get()
        stack = stack if stack else {}
        old_scope = stack.get(kw, [])
        old_scope = self._convert_scope_to_strings(old_scope)
        stack[kw] = formatter_methods
        self.assertion_formatter_stack.set(stack, scope)
        return old_scope

    def _clear_all_formatters(self):
        for kw in self.library.keywords:
            if hasattr(kw, "assertion_formatter_used") and kw.assertion_formatter_used:
                name = self.method_to_kw_str(kw)
                logger.debug(f"Clear keyword: {name}")
                self.set_assertion_formatter(name)
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

    def get_formatter(self, keyword: Callable) -> list:
        stack = self.assertion_formatter_stack.get()
        stack = stack if stack else {}
        kw = self.normalize_keyword(keyword.__name__)
        return stack.get(kw, [])

    def set_formatter(self, keyword, formatter):
        pass

    @keyword_deco(tags=("Config",))
    def set_assertion_formatters(self, formatters: FormatterTypes):
        """DEPRECATED!!* `Use Set Assertion Formatter` instead

        Set keywords formatters for assertions.

        ``formatters`` is dictionary, where key is the keyword name
        where formatters are applied. Dictionary value is a list of
        formatter which are applied. Using keywords always replaces
        existing formatters for keywords.

        Supported formatter are: `normalize space`, `strip` and
        `apply to expected`.

        Example:
        | `Set Assertion Formatters`    {"Keyword Name": ["strip", "normalize spaces"]}
        """
        if not formatters:
            self.set_assertion_formatter()
        else:
            for kw, kw_format in formatters.items():
                self.set_assertion_formatter(kw, Scope.Global, *kw_format)
