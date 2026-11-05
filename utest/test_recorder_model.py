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
"""Tests for the in-memory recorded keyword model."""

from __future__ import annotations

import pytest

from Browser.recorder.model import ArgRef, Call, RecordedKeyword, Value


def fill(text: str) -> Call:
    return Call(
        "Fill Text", [Value.literal("#name", selectable=False), Value.literal(text)]
    )


def test_block_has_tag_and_calls():
    kw = RecordedKeyword("Fill Name")
    kw.add(fill("Alice"))
    assert kw.block() == (
        "Fill Name\n    [Tags]    recorded\n    Fill Text    \\#name    Alice\n"
    )
    assert kw.text().startswith("*** Keywords ***\nFill Name\n")


def test_update_last_replaces_the_primary_call():
    kw = RecordedKeyword("K")
    kw.add(fill("A"))
    assert kw.update_last(fill("Al"))
    assert [c.render() for c in kw.calls()] == ["Fill Text    \\#name    Al"]


def test_undo_removes_the_whole_group():
    kw = RecordedKeyword("K")
    kw.add(Call("Click", [Value.literal("#b", False)]))
    kw.attach(
        [Call("Handle Future Dialogs", [Value.literal("action=accept", False)])], []
    )
    assert len(kw) == 2
    assert kw.undo()
    assert len(kw) == 0
    assert not kw.undo()


def test_make_argument_whole_value_with_default():
    kw = RecordedKeyword("K")
    kw.add(fill("admin@example.com"))
    assert kw.make_argument(0, 1, 0, len("admin@example.com"), "email") == []
    assert kw.lines() == [
        "[Tags]    recorded",
        "[Arguments]    ${email}=admin@example.com",
        "Fill Text    \\#name    ${email}",
    ]


def test_make_argument_partial_value():
    kw = RecordedKeyword("K")
    kw.add(Call("Go To", [Value.literal("https://shop/item/42")]))
    kw.make_argument(0, 0, 18, 20, "item_id")
    assert kw.calls()[0].render() == "Go To    https://shop/item/${item_id}"
    assert kw.arguments[0].default == "42"


def test_partial_argument_keeps_literal_parts_escaped():
    kw = RecordedKeyword("K")
    kw.add(fill("price ${x} is 42"))
    kw.make_argument(0, 1, 14, 16, "amount")
    assert kw.calls()[0].render() == "Fill Text    \\#name    price \\${x} is ${amount}"


def test_fixed_values_cannot_become_arguments():
    kw = RecordedKeyword("K")
    kw.add(fill("x"))
    with pytest.raises(ValueError, match="Fixed options"):
        kw.make_argument(0, 0, 0, 1, "sel")


def test_part_of_a_selector_becomes_an_argument():
    kw = RecordedKeyword("K")
    kw.add(Call("Click", [Value.literal('[data-testid="row-42"]')]))
    kw.make_argument(0, 0, 18, 20, "row")
    assert kw.lines()[1:] == [
        "[Arguments]    ${row}=42",
        'Click    [data-testid="row-${row}"]',
    ]


def test_make_argument_reports_other_occurrences():
    kw = RecordedKeyword("K")
    kw.add(fill("admin@example.com"))
    kw.add(
        Call(
            "Fill Text",
            [Value.literal("#search", False), Value.literal("admin@example.com")],
        )
    )
    assert kw.make_argument(0, 1, 0, 17, "email") == [(1, 1)]
    kw.replace("email", [(1, 1)])
    assert kw.calls()[1].render() == "Fill Text    \\#search    ${email}"


def test_unused_argument_is_removed_on_undo():
    kw = RecordedKeyword("K")
    kw.add(fill("a"))
    kw.add(fill("b"))
    kw.make_argument(1, 1, 0, 1, "second")
    kw.undo()
    assert kw.arguments == []


def test_default_follows_continued_typing():
    kw = RecordedKeyword("K")
    kw.add(fill("adm"))
    kw.make_argument(0, 1, 0, 3, "email")
    kw.update_last(fill("admin@example.com"))
    assert kw.calls()[0].render() == "Fill Text    \\#name    ${email}"
    assert kw.arguments[0].default == "admin@example.com"


def test_partial_default_follows_when_prefix_still_matches():
    kw = RecordedKeyword("K")
    kw.add(fill("id-4"))
    kw.make_argument(0, 1, 3, 4, "n")
    kw.update_last(fill("id-42"))
    assert kw.arguments[0].default == "42"


def test_partial_argument_is_dropped_when_typing_breaks_the_prefix():
    kw = RecordedKeyword("K")
    kw.add(fill("id-4"))
    kw.make_argument(0, 1, 3, 4, "n")
    kw.update_last(fill("xd-42"))
    assert kw.calls()[0].render() == "Fill Text    \\#name    xd-42"
    assert kw.arguments == []


def test_required_arguments_come_before_defaulted_ones():
    kw = RecordedKeyword("K")
    kw.add(fill("a"))
    kw.add(fill("b"))
    kw.make_argument(0, 1, 0, 1, "first")
    kw.make_argument(1, 1, 0, 1, "second", use_default=False)
    assert kw.lines()[1] == "[Arguments]    ${second}    ${first}=a"


def test_argument_name_must_be_unique_in_any_spelling():
    kw = RecordedKeyword("K")
    kw.add(fill("a"))
    kw.add(fill("b"))
    kw.make_argument(0, 1, 0, 1, "email")
    with pytest.raises(ValueError, match="already"):
        kw.make_argument(1, 1, 0, 1, "E_mail")


def test_argument_name_must_not_reuse_an_assigned_variable():
    kw = RecordedKeyword("K")
    kw.add(Call("Click", [Value.literal("#dl", False)]))
    var = kw.unique_variable("download")
    kw.attach(
        [Call("Promise To Wait For Download", [], assign=var)],
        [Call("Wait For", [Value([ArgRef(var)], selectable=False)])],
    )
    kw.add(fill("x"))
    with pytest.raises(ValueError, match="already"):
        kw.make_argument(3, 1, 0, 1, "download")


def test_unique_variable_counts_up():
    kw = RecordedKeyword("K")
    kw.add(Call("Click", [Value.literal("#a", False)]))
    first = kw.unique_variable("download")
    kw.attach([Call("Promise To Wait For Download", [], assign=first)], [])
    assert (first, kw.unique_variable("download")) == ("download", "download_2")


def test_empty_value_renders_as_empty_marker():
    assert Value.literal("").render() == "${EMPTY}"


@pytest.mark.parametrize("start,end", [(0, 0), (2, 1), (-1, 1), (0, 99)])
def test_bad_marks_are_rejected(start, end):
    kw = RecordedKeyword("K")
    kw.add(fill("ab"))
    with pytest.raises(ValueError):
        kw.make_argument(0, 1, start, end, "x")


def test_update_last_with_a_different_keyword_replaces_the_call_without_carrying_arguments():
    kw = RecordedKeyword("K")
    kw.add(fill("A"))
    assert kw.update_last(Call("Click", [Value.literal("#b", False)]))
    assert [c.render() for c in kw.calls()] == ["Click    \\#b"]


def test_update_last_with_a_different_argument_count_replaces_the_call():
    kw = RecordedKeyword("K")
    kw.add(Call("Click", [Value.literal("#b", False)]))
    assert kw.update_last(
        Call("Click", [Value.literal("#b", False), Value.literal("left")])
    )
    assert [c.render() for c in kw.calls()] == ["Click    \\#b    left"]


def test_update_last_and_attach_on_an_empty_keyword_do_nothing():
    kw = RecordedKeyword("K")
    assert kw.update_last(fill("A")) is False
    assert kw.attach([], []) is False
    assert kw.undo() is False


def test_a_value_that_is_already_an_argument_cannot_become_one_again():
    kw = RecordedKeyword("K")
    kw.add(fill("ab"))
    kw.make_argument(0, 1, 0, 2, "first")
    with pytest.raises(ValueError, match="already contains an argument"):
        kw.make_argument(0, 1, 0, 1, "second")


def test_a_selection_of_a_value_that_does_not_exist_is_rejected():
    kw = RecordedKeyword("K")
    kw.add(fill("ab"))
    with pytest.raises(ValueError, match="No such value"):
        kw.make_argument(0, 9, 0, 1, "x")
    with pytest.raises(ValueError, match="No such value"):
        kw.make_argument(5, 1, 0, 1, "x")


def test_value_changed_compares_the_current_text_and_ignores_missing_values():
    kw = RecordedKeyword("K")
    kw.add(fill("ab"))
    assert kw.value_changed(0, 1, "ab") is False
    assert kw.value_changed(0, 1, "a") is True
    assert kw.value_changed(0, 9, "ab") is False
    assert kw.value_changed(5, 1, "ab") is False


def test_replace_skips_occurrences_that_no_longer_contain_the_text_or_are_selectors():
    kw = RecordedKeyword("K")
    kw.add(fill("admin"))
    kw.add(
        Call(
            "Fill Text",
            [Value.literal("#admin", False), Value.literal("something else")],
        )
    )
    kw.make_argument(0, 1, 0, 5, "user")
    kw.replace("user", [(1, 0), (1, 1)])
    assert kw.calls()[1].render() == "Fill Text    \\#admin    something else"


def test_a_refinement_keeps_a_value_whose_argument_is_unknown_to_the_keyword():
    kw = RecordedKeyword("K")
    kw.add(Call("Fill Text", [Value.literal("#n", False), Value([ArgRef("ghost")])]))
    assert kw.update_last(fill("typed"))
    assert kw.calls()[0].args[1].text == "typed"
