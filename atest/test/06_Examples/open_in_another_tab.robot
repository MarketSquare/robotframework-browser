*** Settings ***
Resource          imports.resource

*** Test Cases ***
Open PDF in another tab
    [Setup]    New Browser    headless=${FALSE}
    New Page    ${WELCOME_URL}
    Click    text=Open pdf
    Switch Page    ${1}
    Get Url    should end with    Moving%20Robot%20Framework%20browser%20automation%20to%202020%20(or%202021).pdf
    Close Page
    Get Url    should end with    welcome.html
    [Teardown]    Close Browser

Open html in another tab
    New Page    ${WELCOME_URL}
    Click    text=Open html
    Switch Page    ${1}
    Get Title    ==    Error Page
    Close Page
    Get Title    ==    Welcome Page
