*** Settings ***
Resource          imports.resource

*** Variables ***
${WELCOME URL}    ${ROOT URL}/welcome.html
${ERROR URL}      ${ROOT URL}/error.html

*** Test Cases ***
No Open Browser Throws
    Run KeyWord and Expect Error    *details = "Tried to do playwirght action 'goto', but no open browser."*    GoTo    "about:blank"

Open GoTo GoBack GoForward
    [Setup]    Open Browser    ${LOGIN URL}
    Go To    ${WELCOME URL}
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
