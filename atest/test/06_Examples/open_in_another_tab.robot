*** Settings ***
Resource          imports.resource
Library           OperatingSystem

*** Test Cases ***
Open PDF in another tab and download it
    [Setup]    New Browser    headless=${FALSE}  downloadsPath=${EXECDIR}
    New Context   acceptDownloads=${TRUE}
    New Page    ${WELCOME_URL}
    Click    text=Open pdf
    Switch Page    ${1}
    ${url}=    Get Url    should end with    .pdf
    ${p}=      Promise to   Wait for download
    Download   ${url}
    ${path}=   Wait for  ${p}
    ${actual_size}=   get file size   ${path}
    Should be equal  ${actual_size}   ${32201}
    remove file  ${path}
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
