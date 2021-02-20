*** Settings ***
Resource          imports.resource
Suite Setup        New Page    ${LOGIN_URL}

*** Test Cases ***
Equal
    Get Title    ==    Login Page
    Get Title    equal    Login Page
    Get Title    should be    Login Page

InEqual
    Get Title    !=    Cool Page
    Get Title    inequal    Cool Page
    Get Title    should not be    Cool Page

Greater Than
    Get Style    //*[@id="progress"]    width    >    100
    Get Style    //*[@id="progress"]    width    greater than    100

Greater or Equal
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
