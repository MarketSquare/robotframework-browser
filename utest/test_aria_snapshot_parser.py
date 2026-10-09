import pytest

from Browser.utils.aria_snapshot import parse_aria_snapshot


def test_empty_snapshot():
    assert parse_aria_snapshot("") == []


def test_blank_snapshot():
    assert parse_aria_snapshot("\n") == []


def test_unknown_label_syntax_survives_as_role():
    [node] = parse_aria_snapshot("- some future syntax")
    assert node.role == "some future syntax"
    assert node.props == {}
    assert node.children == []


def test_role_only():
    [node] = parse_aria_snapshot("- button")
    assert node.role == "button"
    assert node.name is None
    assert node.text is None
    assert node.props == {}
    assert node.children == []


def test_role_and_name():
    [node] = parse_aria_snapshot('- textbox "User Name:"')
    assert node.role == "textbox"
    assert node.name == "User Name:"


def test_name_with_apostrophe():
    [node] = parse_aria_snapshot('- button "Doesn\'t do anything"')
    assert node.name == "Doesn't do anything"


def test_name_with_escaped_quotes():
    [node] = parse_aria_snapshot('- heading "He said \\"hi\\""')
    assert node.name == 'He said "hi"'


def test_numeric_property_is_int():
    [node] = parse_aria_snapshot('- heading "Login Page" [level=1]')
    assert node.props.level == 1


def test_property_without_value_is_true():
    [node] = parse_aria_snapshot('- option "Dog" [selected]')
    assert node.props.selected is True


def test_string_properties():
    [node] = parse_aria_snapshot("- link [ref=e74] [cursor=pointer] [checked=mixed]")
    assert node.props.ref == "e74"
    assert node.props.cursor == "pointer"
    assert node.props.checked == "mixed"


def test_box_property_matches_get_boundingbox_keys():
    [node] = parse_aria_snapshot("- heading [box=8,21,1264,37]")
    assert node.props.box == {"x": 8, "y": 21, "width": 1264, "height": 37}


def test_all_properties_of_one_node():
    [node] = parse_aria_snapshot(
        '- heading "Login Page" [level=1] [ref=e3] [box=8,21,1264,37]'
    )
    assert node.role == "heading"
    assert node.name == "Login Page"
    assert node.props == {
        "level": 1,
        "ref": "e3",
        "box": {"x": 8, "y": 21, "width": 1264, "height": 37},
    }


def test_scalar_content_becomes_text():
    [node] = parse_aria_snapshot("- generic [ref=e29]: Online")
    assert node.text == "Online"
    assert node.children == []


def test_text_role_carries_its_content():
    [node] = parse_aria_snapshot('- text: "Choose a pet:"')
    assert node.role == "text"
    assert node.name is None
    assert node.text == "Choose a pet:"


def test_named_node_can_have_text():
    [node] = parse_aria_snapshot('- paragraph "Intro": Please input your user name.')
    assert node.name == "Intro"
    assert node.text == "Please input your user name."


def test_children_are_nested():
    snapshot = "\n".join(
        [
            "- table:",
            "  - rowgroup:",
            "    - row:",
            '      - cell "User Name:"',
        ]
    )
    [table] = parse_aria_snapshot(snapshot)
    assert table.role == "table"
    [rowgroup] = table.children
    [row] = rowgroup.children
    [cell] = row.children
    assert cell.role == "cell"
    assert cell.name == "User Name:"
    assert cell.children == []


def test_node_without_children_after_colon():
    [node] = parse_aria_snapshot("- listitem:")
    assert node.role == "listitem"
    assert node.text is None
    assert node.children == []


def test_url_of_link_becomes_property_of_the_link():
    snapshot = '- link "Download file":\n  - /url: index.js'
    [link] = parse_aria_snapshot(snapshot)
    assert link.props.url == "index.js"
    assert link.children == []


def test_siblings_with_identical_labels_are_kept():
    label = '- button "Doesn\'t do anything"'
    nodes = parse_aria_snapshot("\n".join([label, label, label]))
    assert [node.name for node in nodes] == ["Doesn't do anything"] * 3


def test_top_level_can_hold_several_nodes():
    nodes = parse_aria_snapshot("- iframe\n- iframe")
    assert [node.role for node in nodes] == ["iframe", "iframe"]


def test_dot_access_works_on_nested_nodes():
    snapshot = '- generic [ref=e1]:\n  - textbox "username" [ref=e10]'
    [generic] = parse_aria_snapshot(snapshot)
    assert generic.children[0].props.ref == "e10"


@pytest.fixture
def login_form():
    return "\n".join(
        [
            "- generic [ref=e1] [box=506,0,253,279]:",
            '  - heading "Login" [level=2] [ref=e3] [box=506,0,253,32]',
            "  - generic [ref=e4] [box=516,56,233,66]:",
            '    - textbox "username" [ref=e10] [box=553,76,186,18]',
            "    - generic [box=553,56,186,46]: username",
            '  - button "login" [ref=e19] [cursor=pointer] [box=516,207,233,36]',
            "  - generic [ref=e21] [box=603,243,60,36]:",
            "    - checkbox [box=633,260,0,0]",
        ]
    )


def test_login_form_structure(login_form):
    [root] = parse_aria_snapshot(login_form)
    assert root.role == "generic"
    assert [child.role for child in root.children] == [
        "heading",
        "generic",
        "button",
        "generic",
    ]


def test_login_form_leaf_details(login_form):
    [root] = parse_aria_snapshot(login_form)
    username_group = root.children[1]
    textbox, label = username_group.children
    assert textbox.role == "textbox"
    assert textbox.name == "username"
    assert textbox.props.box == {"x": 553, "y": 76, "width": 186, "height": 18}
    assert label.text == "username"
    assert root.children[3].children[0].role == "checkbox"
