*** Settings ***
Resource          imports.resource

*** Test Cases ***
No Open Browser Throws
    Run KeyWord and Expect Error    *details = "Tried to open URl but had no browser open"*    GoTo    "about:blank"

Open GoTo GoBack GoForward
    [Setup]    Open Browser    ${LOGIN URL}
    Login User
    Get Url    ==    ${WELCOME URL}
    Go To    ${ERROR URL}
    Go Back
    Get Url    ==    ${WELCOME URL}
    Go Back
    Get Url    ==    ${LOGIN URL}
    Go Forward
    Get Url    ==    ${WELCOME URL}
    Go Forward
    Get Url    ==    ${ERROR URL}
    [Teardown]    Close Browser
