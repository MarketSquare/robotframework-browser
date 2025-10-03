*** Settings ***
Library             OperatingSystem
Resource            imports.resource

Test Setup          Open Browser To No Page
Test Teardown       Close Browser

Test Tags           slow

*** Test Cases ***
Open PDF In Another Tab And Download It
    [Tags]    no-docker-pr
    [Setup]    New Browser    headless=${FALSE}    downloadsPath=${EXECDIR}
    New Context    acceptDownloads=${TRUE}
    Set Browser Timeout    30s
    New Page    ${WELCOME_URL}
    Click    text=Open pdf
    Switch Page    NEW
    ${url} =    Get Url    should end with    .pdf
    ${path} =    Download    ${url}
    ${actual_size} =    Get File Size    ${path.saveAs}
    Should Be Equal    ${actual_size}    ${32201}
    Remove File    ${path.saveAs}
    Close Page
    Get Url    should end with    welcome.html
    [Teardown]    Close Browser

Download Without Page Fails
    New Context    acceptDownloads=${TRUE}
    Run Keyword And Expect Error
    ...    Error: Download requires an active page
    ...    Download    ${WELCOME_URL}

Download Without Page URL Fails
    New Context    acceptDownloads=${TRUE}
    New Page
    Run Keyword And Expect Error
    ...    Error: Download requires that the page has been navigated to an url
    ...    Download    ${WELCOME_URL}

Download With No AcceptDownloads Fails
    New Context    acceptDownloads=${FALSE}
    New Page    ${WELCOME_URL}
    Run Keyword And Expect Error
    ...    Error: Context acceptDownloads is false
    ...    Download    ${WELCOME_URL}
    [Teardown]    Close Context

Open Html In Another Tab
    New Page    ${WELCOME_URL}
    Click    text=Open html
    Switch Page    NEW
    Get Title    ==    Error Page
    Close Page
    Get Title    ==    Welcome Page

Download Works Also Headless
    [Tags]    no-iframe
    New Context    acceptDownloads=${TRUE}
    New Page    ${WELCOME_URL}
    ${path} =    Download    ${WELCOME_URL}
    ${actual_size} =    Get File Size    ${path}[saveAs]
    Should Be True    ${actual_size} < ${500}
    Remove File    ${path}[saveAs]
    Should Contain    ${path}[suggestedFilename]    .html

Download Without Wait For Finish
    [Tags]    no-iframe
    New Context    acceptDownloads=${TRUE}
    New Page    ${WELCOME_URL}
    ${download} =    Download    ${WELCOME_URL}    wait_for_finished=False
    ${finished_download} =    Wait For Condition
    ...    download_state
    ...    ${download}
    ...    validate
    ...    value['state'] == 'finished'
    ${actual_size} =    Get File Size    ${finished_download}[saveAs]
    Should Be True    ${actual_size} < ${500}
    Remove File    ${finished_download}[saveAs]
    Should Contain    ${finished_download}[suggestedFilename]    .html
