*** Settings ***
Resource          imports.resource
Library           OperatingSystem

*** Test Cases ***
Open PDF in another tab and download it
    [Setup]    New Browser    headless=${FALSE}    downloadsPath=${EXECDIR}
    New Context    acceptDownloads=${TRUE}
    New Page    ${WELCOME_URL}
    Click    text=Open pdf
    Switch Page    NEW
    ${url}=    Get Url    should end with    .pdf
    ${path}=    Download    ${url}
    ${actual_size}=    get file size    ${path}
    Should be equal    ${actual_size}    ${32201}
    remove file    ${path}
    Close Page
    Get Url    should end with    welcome.html
    [Teardown]    Close Browser

Download without page fails
    New Context    acceptDownloads=${TRUE}
    Run keyword and expect error    Download requires an active page    Download    ${WELCOME_URL}

Download with no acceptDownloads fails
    New Context    acceptDownloads=${FALSE}
    New Page    ${WELCOME_URL}
    Run keyword and expect error    Context acceptDownloads is false    Download    ${WELCOME_URL}

Open html in another tab
    New Page    ${WELCOME_URL}
    Click    text=Open html
    Switch Page    NEW
    Get Title    ==    Error Page
    Close Page
    Get Title    ==    Welcome Page

Download works also headless
    New Context    acceptDownloads=${TRUE}
    New Page    ${WELCOME_URL}
    ${path}=    Download    ${WELCOME_URL}
    ${actual_size}=    get file size    ${path}
    Should be equal    ${actual_size}    ${449}
    remove file    ${path}
