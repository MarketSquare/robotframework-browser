# Copyright 2020-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import re
from typing import Any

import yaml
from robot.utils import DotDict

_LABEL = re.compile(
    r"""
    ^(?P<role>\S+)
    (?:\s+"(?P<name>(?:[^"\\]|\\.)*)")?
    (?P<properties>(?:\s*\[[^\]]*\])*)
    \s*$
    """,
    re.VERBOSE,
)
_PROPERTY = re.compile(r"\[([^\]]*)\]")
_INTEGER = re.compile(r"^-?\d+$")
_BOX_FIELDS = ("x", "y", "width", "height")


def parse_aria_snapshot(snapshot: str) -> list[DotDict]:
    """Turns Playwright's aria snapshot YAML into a tree of node dictionaries.

    Every node has the keys ``role``, ``name``, ``text``, ``props`` and
    ``children``. Nodes are ``DotDict``s, so their values are reachable both as
    ``node["role"]`` and as ``node.role``.
    """
    if not snapshot:
        return []
    return _to_nodes(yaml.safe_load(snapshot))


def _to_nodes(loaded: Any) -> list[DotDict]:
    if not loaded:
        return []
    return [_to_node(entry) for entry in loaded]


def _to_node(entry: Any) -> DotDict:
    if isinstance(entry, dict):
        [(label, content)] = entry.items()
        return _node(label, content)
    return _node(entry, None)


def _node(label: str, content: Any) -> DotDict:
    node = _parse_label(label)
    if isinstance(content, list):
        node.children = _hoist_properties(node, content)
    elif content is not None:
        node.text = str(content)
    return node


def _hoist_properties(node: DotDict, content: list) -> list[DotDict]:
    """Playwright renders link targets as a ``/url`` child, not as an element."""
    children = []
    for entry in content:
        if isinstance(entry, dict):
            [(label, value)] = entry.items()
            if label.startswith("/"):
                node.props[label[1:]] = value
                continue
        children.append(_to_node(entry))
    return children


def _parse_label(label: str) -> DotDict:
    match = _LABEL.match(label)
    if not match:
        return DotDict(role=label, name=None, text=None, props=DotDict(), children=[])
    name = match["name"]
    return DotDict(
        role=match["role"],
        name=None if name is None else name.replace('\\"', '"'),
        text=None,
        props=_parse_properties(match["properties"]),
        children=[],
    )


def _parse_properties(properties: str) -> DotDict:
    parsed = DotDict()
    for property_ in _PROPERTY.findall(properties):
        name, separator, value = property_.partition("=")
        parsed[name] = _parse_property_value(name, value) if separator else True
    return parsed


def _parse_property_value(name: str, value: str) -> Any:
    if name == "box":
        coordinates = value.split(",")
        if len(coordinates) == len(_BOX_FIELDS):
            return DotDict(zip(_BOX_FIELDS, [int(c) for c in coordinates], strict=True))
    if _INTEGER.match(value):
        return int(value)
    return value
