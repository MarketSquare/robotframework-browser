*** Settings ***
Resource        imports.resource

Suite Setup     New Page    ${LOGIN_URL}

*** Test Cases ***
Equal
    Get Title    ==    Login Page
    Get Title    equal    Login Page
    Get Title    should be    Login Page

Formatter Scopes
    ${old_scope} =    Set Assertion Formatter    Get Text    Global    normalize spaces
    Should Be Empty    ${old_scope}
    ${current_scope} =    Get Current Scope From Lib    Get Text
    ${expected_scope} =    Create List    _normalize_spaces
    Should Be Equal    ${current_scope}    ${expected_scope}

    ${old_scope} =    Set Assertion Formatter    Get Text    Global    strip
    ${scope} =    Create List    normalize spaces
    Should Be Equal    ${old_scope}    ${scope}
    ${current_scope} =    Get Current Scope From Lib    Get Text
    ${expected_scope} =    Create List    _strip
    Should Be Equal    ${current_scope}    ${expected_scope}

    ${old_scope} =    Set Assertion Formatter    Get Text    Test    normalize spaces
    ${scope} =    Create List    strip
    Should Be Equal    ${old_scope}    ${scope}
    ${current_scope} =    Get Current Scope From Lib    Get Text
    ${expected_scope} =    Create List    _normalize_spaces
    Should Be Equal    ${current_scope}    ${expected_scope}

    ${old_scope} =    Set Assertion Formatter    Get Text    Suite    apply to expected    case insensitive
    ${scope} =    Create List    normalize spaces
    Should Be Equal    ${old_scope}    ${scope}
    ${current_scope} =    Get Current Scope From Lib    Get Text
    ${expected_scope} =    Create List    _apply_to_expected    _case_insensitive
    Should Be Equal    ${current_scope}    ${expected_scope}

    Set Assertion Formatter    Get Text    Suite
    ${current_scope} =    Get Current Scope From Lib    Get Text
    Should Be Empty    ${current_scope}
    [Teardown]    Formatter TearDown

Equal With Formatter Global:
    [Setup]    Go To    ${SPACES_URL}
    Set Assertion Formatter    Get Text    Global    normalize spaces
    Set Assertion Formatter    Get Text    Global    strip
    Get Text    id=two    ==    two spaces
    [Teardown]    Formatter TearDown

Cat Not Set Formatter For Not Library Keyword
    TRY
        Set Assertion Formatter    Not Browser Library Keyword    Suite    strip
    EXCEPT    ValueError: Not Browser Library Keyword is not library keyword    AS    ${error}
        Log    ${error}
    END
    TRY
        Set Assertion Formatter    Log    Suite    strip
    EXCEPT    ValueError: Log is not library keyword    AS    ${error}
        Log    ${error}
    END

Equal With Deprecated Formatter:
    [Setup]    Go To    ${SPACES_URL}
    Set Assertion Formatters    {"Get Text": ["strip"]}
    Get Text    id=two    ==    two spaces
    [Teardown]    Formatter TearDown

Get Attribute Names Does Not Support Formatter:
    [Documentation]
    ...    LOG 2:*    WARN    Formatter is not supported by Get Attribute Names keyword.
    [Setup]    Go To    ${SPACES_URL}
    Set Assertion Formatter    Get Attribute Names    Test    strip
    Get Attribute Names    id=two    ==    id
    [Teardown]    Formatter TearDown

Get Attribute Names Does Not Support Formatter2:
    [Documentation]
    ...    LOG 1:*    DEBUG    GLOB:    Assertion polling statistics:*
    [Setup]    Go To    ${SPACES_URL}
    Get Attribute Names    id=two    ==    id
    [Teardown]    Formatter TearDown

Get Element Count Does Not Support Formatter:
    [Documentation]
    ...    LOG 2:*    WARN    Formatter is not supported by Get Element Count keyword.
    [Setup]    Go To    ${SPACES_URL}
    Set Assertion Formatter    Get Element Count    Test    strip
    Get Element Count    id=two    ==    1
    [Teardown]    Formatter TearDown

InEqual
    Get Title    !=    Cool Page
    Get Title    inequal    Cool Page
    Get Title    should not be    Cool Page

Greater Than
    Get Style    //*[@id="progress"]    width    >    100
    Get Style    id=progress    width    greater than    100

Greater Or Equal
    Get Style    css=#progress    width    >=    400

Less
    Get Style    //*[@id="progress"]    width    <    401
    Get Style    //*[@id="progress"]    width    less than    401

Pseudo Elements And Keyword Banner Activated Scope Suite
    Show Keyword Banner    show=True    scope=Suite
    Get Title
    Get Style    body    bottom    ==    5px    pseudo_element=::before
    Get Style    body    background-color    ==    rgba(0, 0, 139, 0.565)    pseudo_element=::before
    Get Style    body    font-size    ==    13px    pseudo_element=::before
    Get Style    body    color    ==    rgb(255, 255, 255)    pseudo_element=::before

Pseudo Elements And Keyword Banner Styled Scope Test
    Show Keyword Banner
    ...    show=True
    ...    style=top: 5px; bottom: auto; left: 5px; background-color: #00909077; font-size: 9px; color: black;
    ...    scope=Test
    Get Title
    Get Style    body    top    ==    5px    pseudo_element=::before
    Get Style    body    background-color    ==    rgba(0, 144, 144, 0.467)    pseudo_element=::before
    Get Style    body    font-size    ==    9px    pseudo_element=::before
    Get Style    body    color    ==    rgb(0, 0, 0)    pseudo_element=::before
    Get Style    body    ALL    pseudo_element=::before
    Get Style    body    ${None}    pseudo_element=::before

Pseudo Elements And Keyword Banner Off Scope Test
    Show Keyword Banner    show=False    scope=Test
    Get Title
    Get Style    body    top    ==    auto    pseudo_element=::before
    Get Style    body    background-color    ==    rgba(0, 0, 0, 0)    pseudo_element=::before
    Get Style    body    font-size    ==    16px    pseudo_element=::before
    Get Style    body    color    ==    rgb(0, 0, 0)    pseudo_element=::before
    Get Style    body    content    ==    none    pseudo_element=::before

Pseudo Elements And Keyword Banner Scope Test
    Get Title
    Get Style    body    bottom    ==    5px    pseudo_element=::before
    Get Style    body    background-color    ==    rgba(0, 0, 139, 0.565)    pseudo_element=::before
    Get Style    body    font-size    ==    13px    pseudo_element=::before
    Get Style    body    color    ==    rgb(255, 255, 255)    pseudo_element=::before
    Show Keyword Banner    show=False    scope=Suite

Contains
    Get Title    *=    Page
    Get Title    contains    Page

Matches
    Get Title    matches    \\w+\\s\\w+

Starts With
    Get Title    ^=    Log
    Get Title    should start with    Log

Ends With
    Get Title    $=    ge
    Get Title    should end with    ge

Validate
    Get Title    validate    value == "Login Page"
    Get Title    validate    3 < 4

Evaluate
    Get Title    then    value if value == value else value
    Get Title    evaluate    value if value == value else value

*** Keywords ***
Formatter TearDown
    Set Assertion Formatter
    Go To    ${LOGIN_URL}
