import Browser
import inspect
from typing import Any

br: Any = Browser.Browser()
keywords = br.get_keyword_names()
function_list = list()
for keyword in keywords:
    keyword_name = keyword
    if " " in keyword:
        for key in br.attributes.keys():
            if keyword == br.attributes[key].robot_name and " " not in key:
                keyword_name = key
                break
    args = br.get_keyword_arguments(keyword)
    types = br.get_keyword_types(keyword)
    args_str = ""
    for arg in args:
        if isinstance(arg, tuple):
            arg_name = arg[0]
            if arg_name[0] == "*":
                tpe = types[arg_name[1:]]
            else:
                tpe = types[arg_name]
            if hasattr(tpe, "__name__"):
                arg_type = tpe.__name__
            else:
                arg_type = str(tpe.__repr__()).lstrip("typing.")
            if arg[1] is None:
                arg_type_str = f"Optional[{arg_type}]"
            else:
                arg_type_str = arg_type
            if arg_type == "str":
                arg_str = f"{arg_name}: {arg_type_str} = '{arg[1]}'"
            else:
                arg_str = f"{arg_name}: {arg_type_str} = {arg[1]}"
        else:
            if arg[0] == "*":
                arg_name = arg[1:]
            else:
                arg_name = arg
            if arg_name in types:
                tpe = types[arg_name]
                if hasattr(tpe, "__name__"):
                    arg_type = tpe.__name__
                else:
                    arg_type = str(tpe.__repr__()).lstrip("typing.")
                arg_str = f"{arg}: {arg_type}"
            else:
                arg_str = f"{arg}"

        args_str = f"{args_str}, {arg_str}"
    function_list.append(f"    def {keyword_name}(self{args_str}): ...\n")

function_list.sort()

pyi_boilerplate = f"""from concurrent.futures import Future
from typing import Union, Any, Dict, List, Optional

from .assertion_engine import AssertionOperator
from .keywords.input import SelectAttribute, MouseButton, KeyboardModifier
from .keywords.playwright_state import SupportedBrowsers, ViewportDimensions, ColorScheme
from .keywords.waiter import ElementState
from .keywords.evaluation import RequestMethod


class Browser:

    def __init__(self, {str(inspect.signature(br.__init__))[1:]}: ...\n
"""

with open("Browser/__init__.pyi", "w") as stub_file:
    stub_file.write(pyi_boilerplate)
    stub_file.writelines(function_list)
