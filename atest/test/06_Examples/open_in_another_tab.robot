*** Settings ***
Resource          imports.resource

*** Test Cases ***
Open PDF in another tab
    New Page    ${WELCOME_URL}
    Click    text=Open pdf
    Sleep    1s
    ${b}=    get browser catalog

Open html in another tab
    New Page    ${WELCOME_URL}
    Click    text=Open html
    Switch Page  ${1}
    Get Title   ==   Error Page
    Close Page
    Get Tilte   ==   Welcome Page
