import Browser
import inspect
from typing import Any


def is_named_method(keyword_name: str) -> bool:
    keyword_attribute = br.attributes[keyword_name]
    return (
        keyword_attribute.robot_name is not None
        and keyword_attribute.robot_name == keyword_name
    )


def get_method_name_for_keyword(keyword_name: str) -> str:
    if is_named_method(keyword_name):
        for key in br.attributes.keys():
            if key != keyword_name and keyword_name == br.attributes[key].robot_name:
                return key
    return keyword_name


def get_type_string_from_type(argument_type: type) -> str:
    if hasattr(argument_type, "__name__"):
        return argument_type.__name__
    else:
        return str(argument_type.__repr__()).lstrip("typing.")


def get_type_sting_from_argument(argument_string: str, argument_types: dict) -> str:
    agrument_name = argument_string.lstrip("*")
    if agrument_name in argument_types:
        return get_type_string_from_type(argument_types[agrument_name])
    return ""


def get_function_list_from_keywords(keywords):
    functions = list()
    for keyword in keywords:
        method_name = get_method_name_for_keyword(keyword)
        keyword_arguments = br.get_keyword_arguments(keyword)
        keyword_types = br.get_keyword_types(keyword)
        arguments_list = list()
        for argument in keyword_arguments:
            if isinstance(argument, tuple):
                arg_str = argument[0]
                default_value = argument[1]
                arg_type_str = get_type_sting_from_argument(arg_str, keyword_types)
                if arg_type_str:
                    if default_value is None:
                        arg_type_str = f"Optional[{arg_type_str}]"
                    if arg_type_str == "str":
                        default_value = f"'{default_value}'"
                    arg_str = arg_str + f": {arg_type_str}"
                elif isinstance(default_value, str):
                    default_value = f"'{default_value}'"
                arg_str = arg_str + f" = {default_value}"
            else:
                arg_str = argument
                arg_type_str = get_type_sting_from_argument(arg_str, keyword_types)
                if arg_type_str:
                    arg_str = arg_str + f": {arg_type_str}"
            arguments_list.append(arg_str)
        arguments_string = (
            f", {', '.join(arguments_list)}" if len(arguments_list) > 0 else ""
        )
        functions.append(f"    def {method_name}(self{arguments_string}): ...\n")
    functions.sort()
    return functions


br: Any = Browser.Browser()
function_list = get_function_list_from_keywords(br.get_keyword_names())


pyi_boilerplate = f"""from concurrent.futures import Future
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)

from .utils.data_types import *


class Browser:

    def __init__(self, {str(inspect.signature(br.__init__))[1:]}: ...\n
"""

with open("Browser/__init__.pyi", "w") as stub_file:
    stub_file.write(pyi_boilerplate)
    stub_file.writelines(function_list)
