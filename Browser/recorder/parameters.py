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
"""The parameters a recorded Keyword Call could name.

Robot reads ``name=value`` as a named argument only when ``name`` is a
parameter of the called keyword, so a recorded value needs its ``=`` escaped
only then. ``role=button`` stays readable in ``Click``, ``txt\\=hello`` is
escaped in ``Fill Text``. `utest/test_recorder_parameters.py` keeps this table
equal to the real signatures.
"""

from __future__ import annotations

KEYWORD_PARAMETERS: dict[str, frozenset[str]] = {
    "Check Checkbox": frozenset({"selector", "force"}),
    "Click": frozenset({"selector", "button"}),
    "Click With Options": frozenset(
        {
            "selector",
            "button",
            "clickCount",
            "delay",
            "force",
            "noWaitAfter",
            "position_x",
            "position_y",
            "trial",
        }
    ),
    "Close Page": frozenset({"page", "context", "browser", "runBeforeUnload"}),
    "Fill Text": frozenset({"selector", "txt", "force"}),
    "Get Aria Snapshot": frozenset(
        {
            "selector",
            "return_type",
            "assertion_operator",
            "assertion_expected",
            "message",
            "mode",
            "depth",
            "boxes",
        }
    ),
    "Get Checkbox State": frozenset(
        {"selector", "assertion_operator", "assertion_expected", "message"}
    ),
    "Get Element States": frozenset(
        {"selector", "assertion_operator", "message", "return_names"}
    ),
    "Get Property": frozenset(
        {"selector", "property", "assertion_operator", "assertion_expected", "message"}
    ),
    "Get Text": frozenset(
        {"selector", "assertion_operator", "assertion_expected", "message", "text_type"}
    ),
    "Go To": frozenset({"url", "timeout", "wait_until"}),
    "Handle Future Dialogs": frozenset({"action", "prompt_input"}),
    "Press Keys": frozenset({"selector", "press_duration", "key_delay"}),
    "Promise To Upload File": frozenset({"path"}),
    "Promise To Wait For Download": frozenset(
        {"saveAs", "wait_for_finished", "download_timeout"}
    ),
    "Select Options By": frozenset({"selector", "attribute"}),
    "Switch Page": frozenset({"id", "context", "browser"}),
    "Uncheck Checkbox": frozenset({"selector", "force"}),
    "Upload File By Selector": frozenset({"selector", "path"}),
    "Wait For": frozenset(),
}
