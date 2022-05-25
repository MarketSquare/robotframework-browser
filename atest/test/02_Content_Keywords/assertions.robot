*** Settings ***
Resource        imports.resource

Suite Setup     New Page    ${LOGIN_URL}

*** Test Cases ***
Equal
    Get Title    ==    Login Page
    Get Title    equal    Login Page
    Get Title    should be    Login Page

Equal With Formatter:
    [Setup]    Go To    ${SPACES_URL}
    Set Assertion Formatters    {"Get Text": ["strip"]}
    Get Text    id=two    ==    two spaces
    [Teardown]    Formatter TearDown

Get Attribute Names Does Not Support Formatter:
    [Documentation]
    ...    LOG 2:2    WARN    Formatter is not supported by Get Attribute Names keyword.
    [Setup]    Go To    ${SPACES_URL}
    Set Assertion Formatters    {"Get Attribute Names": ["strip"]}
    Get Attribute Names    id=two    ==    id
    [Teardown]    Formatter TearDown

Get Attribute Names Does Not Support Formatter:
    [Documentation]
    ...    LOG 1:2    DEBUG    GLOB:    Assertion polling statistics:*
    [Setup]    Go To    ${SPACES_URL}
    Get Attribute Names    id=two    ==    id
    [Teardown]    Formatter TearDown

Get Element Count Does Not Support Formatter:
    [Documentation]
    ...    LOG 2:2    WARN    Formatter is not supported by Get Element Count keyword.
    [Setup]    Go To    ${SPACES_URL}
    Set Assertion Formatters    {"Get Element Count": ["strip"]}
    Get Element Count    id=two    ==    1
    [Teardown]    Formatter TearDown

InEqual
    Get Title    !=    Cool Page
    Get Title    inequal    Cool Page
    Get Title    should not be    Cool Page

Greater Than
    Get Style    //*[@id="progress"]    width    >    100
    Get Style    //*[@id="progress"]    width    greater than    100

Greater Or Equal
    Get Style    //*[@id="progress"]    width    >=    400

Less
    Get Style    //*[@id="progress"]    width    <    401
    Get Style    //*[@id="progress"]    width    less than    401

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
