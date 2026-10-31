import pytest

from Browser import Browser
from Browser.recorder.action_mapper import ActionMapper
from Browser.recorder.parameters import KEYWORD_PARAMETERS

ACTIONS = [
    {"name": "navigate", "url": "u"},
    {"name": "click", "selector": "s", "button": "left", "clickCount": 1},
    {"name": "click", "selector": "s", "button": "right", "clickCount": 2},
    {"name": "fill", "selector": "s", "text": "t"},
    {"name": "press", "selector": "s", "key": "Enter"},
    {"name": "check", "selector": "s"},
    {"name": "uncheck", "selector": "s"},
    {"name": "select", "selector": "s", "options": ["o"]},
    {"name": "assertText", "selector": "s", "text": "t"},
    {"name": "assertValue", "selector": "s", "value": "v"},
    {"name": "assertChecked", "selector": "s", "checked": True},
    {"name": "assertVisible", "selector": "s"},
    {"name": "assertSnapshot", "selector": "s", "ariaSnapshot": "- a"},
]
SIGNALS = [{"name": "popup"}, {"name": "dialog"}, {"name": "download"}]


def recorded_keywords() -> set[str]:
    mapper = ActionMapper()
    names = {mapper.map(action).keyword for action in ACTIONS}
    for signal in SIGNALS:
        effect = mapper.map_signal(signal, lambda base: base)
        names.update(call.keyword for call in [*effect.before, *effect.after])
    upload = mapper.map_upload("a.txt", lambda base: base)
    names.update(call.keyword for call in [*upload.before, *upload.after])
    names.add(mapper.map_upload_by_selector({"selector": "s"}, ["a.txt"]).keyword)
    names.add(mapper.switch_page("page").keyword)
    names.add(mapper.close_page(None).keyword)
    return names


def test_every_recorded_keyword_has_its_parameters_listed():
    assert recorded_keywords() == set(KEYWORD_PARAMETERS)


@pytest.mark.parametrize("keyword", sorted(KEYWORD_PARAMETERS))
def test_parameters_match_the_keyword_signature(keyword):
    spec = Browser().get_keyword_arguments(keyword.lower().replace(" ", "_"))
    names = [item[0] if isinstance(item, tuple) else item for item in spec]
    # `**kwargs` would make every name a named argument; the table cannot say so.
    assert not any(name.startswith("**") for name in names)
    nameable = {name for name in names if not name.startswith("*")}
    assert KEYWORD_PARAMETERS[keyword] == nameable
