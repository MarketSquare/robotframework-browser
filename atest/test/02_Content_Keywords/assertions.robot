*** Settings ***
Resource        imports.resource

Suite Setup     New Page    ${LOGIN_URL}

*** Test Cases ***
Equal
    Get Title    ==    Login Page
    Get Title    equal    Login Page
    Get Title    should be    Login Page

Formatter Scopes
    ${old_scope} =    Set Assertion Formatters    {'Get Text' : ['normalize spaces']}    Global
    Should Be Equal    ${old_scope}    ${{{'Get Text': []}}}
    ${current_scope} =    Get Current Scope From Lib    Get Text
    ${expected_scope} =    Create List    _normalize_spaces
    Should Be Equal    ${current_scope}    ${expected_scope}

    ${old_scope} =    Set Assertion Formatters    {'Get Text' : ['strip']}    Global
    ${scope} =    Create List    normalize spaces
    Should Be Equal    ${old_scope}[Get Text]    ${scope}
    ${current_scope} =    Get Current Scope From Lib    Get Text
    ${expected_scope} =    Create List    _strip
    Should Be Equal    ${current_scope}    ${expected_scope}

    ${old_scope} =    Set Assertion Formatters    {'Get Text' : ['normalize spaces']}    Test
    ${scope} =    Create List    strip
    Should Be Equal    ${old_scope}[Get Text]    ${scope}
    ${current_scope} =    Get Current Scope From Lib    Get Text
    ${expected_scope} =    Create List    _normalize_spaces
    Should Be Equal    ${current_scope}    ${expected_scope}

    ${old_scope} =    Set Assertion Formatters    {'Get Text' : ['apply to expected', 'case insensitive']}    Suite
    ${scope} =    Create List    normalize spaces
    Should Be Equal    ${old_scope}[Get Text]    ${scope}
    ${current_scope} =    Get Current Scope From Lib    Get Text
    ${expected_scope} =    Create List    _apply_to_expected    _case_insensitive
    Should Be Equal    ${current_scope}    ${expected_scope}

    Set Assertion Formatters    {'Get Text' : []}    Suite
    ${current_scope} =    Get Current Scope From Lib    Get Text
    Should Be Empty    ${current_scope}
    [Teardown]    Formatter TearDown

Equal With Formatter Global:
    [Setup]    Go To    ${SPACES_URL}
    ${old} =    Set Assertion Formatters    {'Get Text': ['normalize spaces']}    Global
    Should Be Equal    ${old}    ${{{'Get Text': []}}}
    ${old} =    Set Assertion Formatters    {'Get Text': ['strip']}    Global
    Should Be Equal    ${old}    ${{{'Get Text': ['normalize spaces']}}}
    ${current_scope} =    Get Current Scope From Lib    Get Text
    Get Text    id=two    ==    two spaces
    [Teardown]    Formatter TearDown

Cat Not Set Formatter For Not Library Keyword
    TRY
        Set Assertion Formatters    {'Not Browser Library Keyword': ['strip']}    Suite
    EXCEPT    ValueError: Argument 'formatters' got value '{'Not Browser Library Keyword': ['strip']}' that cannot be converted to Dict[FormatterKeywords, list[FormatingRules | LambdaFunction]]: Key 'Not Browser Library Keyword' cannot be converted to FormatterKeywords: FormatterKeywords does not have member 'Not Browser Library Keyword'. Available: 'Get Attribute', 'Get Browser Catalog', 'Get Page Source', 'Get Property', 'Get Select Options', 'Get Style', 'Get Text', 'Get Title', 'Get Url', 'LocalStorage Get Item' and 'SessionStorage Get Item'    AS    ${error}
        Log    ${error}
    END
    TRY
        Set Assertion Formatters    {'Log': ['strip']}    Suite
    EXCEPT    ValueError: Argument 'formatters' got value '{'Log': ['strip']}' that cannot be converted to Dict[FormatterKeywords, list[FormatingRules | LambdaFunction]]: Key 'Log' cannot be converted to FormatterKeywords: FormatterKeywords does not have member 'Log'. Available: 'Get Attribute', 'Get Browser Catalog', 'Get Page Source', 'Get Property', 'Get Select Options', 'Get Style', 'Get Text', 'Get Title', 'Get Url', 'LocalStorage Get Item' and 'SessionStorage Get Item'    AS    ${error}
        Log    ${error}
    END

Get Attribute Names Does Not Support Formatter:
    TRY
        Set Assertion Formatters    {'Get Attribute Names':['strip']}    Test
    EXCEPT    ValueError: Argument 'formatters' got value '{'Get Attribute Names':['strip']}' that cannot be converted to Dict[FormatterKeywords, list[FormatingRules | LambdaFunction]]: Key 'Get Attribute Names' cannot be converted to FormatterKeywords: FormatterKeywords does not have member 'Get Attribute Names'. Available: 'Get Attribute', 'Get Browser Catalog', 'Get Page Source', 'Get Property', 'Get Select Options', 'Get Style', 'Get Text', 'Get Title', 'Get Url', 'LocalStorage Get Item' and 'SessionStorage Get Item'    AS    ${error}
        Log    ${error}
    END

Equal With Formatter:
    [Setup]    Go To    ${SPACES_URL}
    Set Assertion Formatters    {"Get Text": ["strip"], "Get Title": ["lambda x: x.replace(' ', '')"]}
    Get Text    id=two    ==    two spaces
    Get Title    ==    Pagewithspaces
    [Teardown]    Formatter TearDown

Equal With Lambda Formatter:
    [Setup]    Go To    ${SPACES_URL}
    Set Assertion Formatters
    ...    {"Get Text": ["apply to expected", "strip", "lambda x: x.replace('two', 'three')", "lambda x: x.upper()", "lambda x: x.replace(' ', '')"]}
    Get Text    id=two    ==    Thr E e Sp A CES
    [Teardown]    Formatter TearDown

Get Attribute Names Does Not Support Formatter2:
    [Documentation]
    ...    LOG 1:*    DEBUG    GLOB:    Assertion polling statistics:*
    [Setup]    Go To    ${SPACES_URL}
    Get Attribute Names    id=two    ==    id
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
    Set Assertion Formatters    {}
    Go To    ${LOGIN_URL}
