*** Settings ***
Resource        imports.resource

Suite Setup     Aria Snapshot Setup

*** Variables ***
${MouseTable} =         css=table >> nth=1
${LEFT_FRAME_URL} =     ${ROOT_URL}frames/left.html

*** Test Cases ***
Aria Snapshot YAML
    ${snapshot} =    Get Aria Snapshot    h1
    Should Be Equal    ${snapshot}    - heading "Login Page" [level=1]
    ${snapshot} =    Get Aria Snapshot    id=username_field    yaml    ==    - textbox "User Name:"
    ${snapshot} =    Get Aria Snapshot    id=username_field    yaml    contains    User Name

Aria Snapshot Dict
    VAR    @{expected} =    heading "Login Page" [level=1]
    ${snapshot} =    Get Aria Snapshot    h1    dict
    Should Be Equal    ${snapshot}    ${expected}    # Use type=list when RF 7.4 is minimum requirement
    VAR    @{expected} =    textbox "User Name:"
    ${snapshot} =    Get Aria Snapshot    id=username_field    dict    ==    ${expected}

Aria Snapshot Strict Mode
    ${strict} =    Set Strict Mode    True
    TRY
        Get Aria Snapshot    //input
    EXCEPT    *strict mode violation*    type=glob
        Log    Caught expected PlaywrightError in strict mode.
    END
    Set Strict Mode    False
    ${snapshot} =    Get Aria Snapshot    //input    yaml    ==    - textbox "User Name:"
    [Teardown]    Set Strict Mode    ${strict}

Aria Snapshot Non-existing Element
    TRY
        Get Aria Snapshot    id=non_existing_element
    EXCEPT    *locator.ariaSnapshot: Timeout*    type=glob
        Log    Caught expected PlaywrightError for non-existing element.
    END

Aria Snapshot Depth
    ${full} =    Get Aria Snapshot    ${MouseTable}
    ${depth_1} =    Get Aria Snapshot    ${MouseTable}    depth=1
    ${depth_2} =    Get Aria Snapshot    ${MouseTable}    depth=2
    Should Be Equal    ${depth_1}    - table:\n${SPACE*2}- rowgroup
    Should Contain    ${depth_2}    - row "Mouse Delay:"
    Should Not Contain    ${depth_2}    - cell "Mouse Delay:"
    Should Contain    ${full}    - cell "Mouse Delay:"

Aria Snapshot Depth With Assertion
    Get Aria Snapshot    ${MouseTable}    yaml    contains    - row "Mouse Delay:"    depth=2

Aria Snapshot Invalid Depth
    FOR    ${depth}    IN    ${0}    ${-1}
        TRY
            Get Aria Snapshot    ${MouseTable}    depth=${depth}
        EXCEPT    ValueError: depth must be a positive integer, but got: ${depth}
            Log    Failed as expected with depth ${depth}.
        ELSE
            Fail    Get Aria Snapshot did not reject depth ${depth}.
        END
    END

Aria Snapshot Boxes
    ${expected} =    Aria Box Annotation Of    h1
    ${snapshot} =    Get Aria Snapshot    h1    boxes=True
    Should Be Equal    ${snapshot}    - heading "Login Page" [level=1] ${expected}
    ${without_boxes} =    Get Aria Snapshot    h1
    Should Not Contain    ${without_boxes}    [box=

Aria Snapshot AI Mode
    ${snapshot} =    Get Aria Snapshot    h1    mode=ai
    Should Match Regexp    ${snapshot}    ^- heading "Login Page" \\[level=1\\] \\[ref=\\w+\\]$
    ${default_mode} =    Get Aria Snapshot    h1
    Should Not Contain    ${default_mode}    [ref=

Aria Snapshot AI Mode Includes Iframes
    Ensure Location    ${FRAMES_URL}
    ${default_mode} =    Get Aria Snapshot    css=body
    Should Not Contain    ${default_mode}    This is LEFT side.
    ${snapshot} =    Get Aria Snapshot    css=body    mode=ai
    Should Contain    ${snapshot}    This is LEFT side.
    Should Contain    ${snapshot}    This is RIGHT side.
    [Teardown]    Ensure Location    ${LOGIN_URL}

Aria Snapshot AI Mode Non-existing Element
    TRY
        Get Aria Snapshot    id=non_existing_element    mode=ai
    EXCEPT    *does not match any element*    type=glob
        Log    Caught expected PlaywrightError without waiting for a timeout.
    ELSE
        Fail    Get Aria Snapshot returned a snapshot for a non-existing element in ai mode.
    END

Aria Snapshot Options With Dict Return Type
    ${expected_box} =    Aria Box Annotation Of    h1
    VAR    @{expected} =    heading "Login Page" [level=1] ${expected_box}
    ${snapshot} =    Get Aria Snapshot    h1    dict    boxes=True
    Should Be Equal    ${snapshot}    ${expected}

Aria Snapshot Parsed
    ${nodes} =    Get Aria Snapshot    h1    parsed
    Length Should Be    ${nodes}    1
    Should Be Equal    ${nodes}[0][role]    heading
    Should Be Equal    ${nodes}[0][name]    Login Page
    Should Be Equal    ${nodes}[0][props][level]    ${1}
    Should Be Equal    ${nodes}[0][text]    ${None}
    Should Be Empty    ${nodes}[0][children]

Aria Snapshot Parsed Complete Structure
    [Documentation]    Covers every node key in both of its shapes: named and unnamed nodes,
    ...    nodes with and without text, a hoisted ``/url`` property next to nodes without
    ...    properties, and two levels of nesting with three siblings. The page renders as:
    ...    - paragraph: "This is LEFT side. Links:"
    ...    - list:
    ...    ${SPACE*2}- listitem:
    ...    ${SPACE*4}- text: Open
    ...    ${SPACE*4}- link "foo":
    ...    ${SPACE*6}- /url: foo.html
    ...    ${SPACE*4}- text: on the right-hand side frame
    ...    - paragraph: "Form:"
    ...    - textbox
    ...    - button "Search"
    Ensure Location    ${LEFT_FRAME_URL}
    ${nodes} =    Get Aria Snapshot    css=body    parsed
    VAR    ${literal} =
    ...    [
    ...    {'role': 'paragraph', 'name': None, 'text': 'This is LEFT side. Links:', 'props': {}, 'children': []},
    ...    {'role': 'list', 'name': None, 'text': None, 'props': {}, 'children': [
    ...    {'role': 'listitem', 'name': None, 'text': None, 'props': {}, 'children': [
    ...    {'role': 'text', 'name': None, 'text': 'Open', 'props': {}, 'children': []},
    ...    {'role': 'link', 'name': 'foo', 'text': None, 'props': {'url': 'foo.html'}, 'children': []},
    ...    {'role': 'text', 'name': None, 'text': 'on the right-hand side frame', 'props': {}, 'children': []},]},]},
    ...    {'role': 'paragraph', 'name': None, 'text': 'Form:', 'props': {}, 'children': []},
    ...    {'role': 'textbox', 'name': None, 'text': None, 'props': {}, 'children': []},
    ...    {'role': 'button', 'name': 'Search', 'text': None, 'props': {}, 'children': []},
    ...    ]
    ...    separator=${SPACE}
    ${expected} =    Evaluate    ${literal}
    Should Be Equal    ${nodes}    ${expected}
    [Teardown]    Ensure Location    ${LOGIN_URL}

Aria Snapshot Parsed With Boxes Matches Get BoundingBox
    ${box} =    Get BoundingBox    h1    ALL
    ${nodes} =    Get Aria Snapshot    h1    parsed    boxes=True
    ${rounded} =    Evaluate    {key: int(value + 0.5) for key, value in $box.items()}
    Should Be Equal    ${nodes}[0][props][box]    ${rounded}

Aria Snapshot Parsed With AI Mode Has Refs
    ${nodes} =    Get Aria Snapshot    h1    parsed    mode=ai
    Should Match Regexp    ${nodes}[0][props][ref]    ^\\w+$

Aria Snapshot Parsed Reads Link Url As Property
    ${nodes} =    Get Aria Snapshot    css=a >> nth=0    parsed
    Should Be Equal    ${nodes}[0][role]    link
    Should Be Equal    ${nodes}[0][props][url]    index.js
    Should Be Empty    ${nodes}[0][children]

Aria Snapshot Parsed Reads Valueless Annotation As True
    ${nodes} =    Get Aria Snapshot    css=select    parsed
    Should Be Equal    ${nodes}[0][children][0][props][selected]    ${True}

*** Keywords ***
Aria Snapshot Setup
    Ensure Open Page    ${LOGIN_URL}

Aria Box Annotation Of
    [Arguments]    ${selector}
    ${box} =    Get BoundingBox    ${selector}    ALL
    ${annotation} =    Evaluate
    ...    "[box=%d,%d,%d,%d]" % (int($box["x"] + 0.5), int($box["y"] + 0.5), int($box["width"] + 0.5), int($box["height"] + 0.5))
    RETURN    ${annotation}
