*** Settings ***
Resource            imports.resource

Test Setup          Set Library Timeout
Test Teardown       Run Keywords    Restore Library Timeout    AND    Wait For All Promises

*** Variables ***
${CUSTOM_DL_PATH}=      ${CURDIR}/download_file

*** Test Cases ***
Upload File
    New Page    ${LOGIN_URL}
    Promise To Upload File    ${CURDIR}/test_upload_file
    Click    \#file_chooser
    Get Text    \#upload_result    ==    test_upload_file

Upload File with different name
    New Page    ${LOGIN_URL}
    Promise to Upload File    ${CURDIR}/invalid_test_upload_file
    Click    \#file_chooser
    Get Text    \#upload_result    ==    wrong_upload_filename

Invalid Upload Path
    [Tags]    No-Windows-Support
    ${promise}=    Promise to Upload File    NonExistentFile
    Run Keyword And Expect Error    STARTS: FileNotFoundError: [Errno 2] No such file or directory:    Wait For
    ...    ${promise}
    Wait For All Promises

Wait For Download
    New Context    acceptDownloads=True
    New Page    ${LOGIN_URL}
    ${dl_promise}=    Promise To Wait for Download
    Sleep    0.5
    Click    \#file_download
    ${file_object}=    Wait For    ${dl_promise}
    File Should Exist    ${file_object}[saveAs]
    Should Be Equal    ${file_object}[suggestedFilename]    test_download_file.js
    Remove File    ${file_object}[saveAs]

Wait For Download With Custom Path
    [Tags]    No-Windows-Support
    New Context    acceptDownloads=True
    New Page    ${LOGIN_URL}
    ${dl_promise}=    Promise To Wait For Download    saveAs=${CUSTOM_DL_PATH}
    Sleep    0.5
    Click    \#file_download
    ${file_object}=    Wait For    ${dl_promise}
    File Should Exist    ${file_object.saveAs}
    Should Be Equal    ${file_object.suggestedFilename}    test_download_file.js
    File Should Exist    ${CUSTOM_DL_PATH}
    Remove File    ${CUSTOM_DL_PATH}
    Remove File    ${file_object.saveAs}

*** Keywords ***
Set Library Timeout
    ${open_browsers}=    Get Browser Ids
    IF    $open_browsers == []
        New Browser    ${BROWSER}    headless=${HEADLESS}
    END
    ${current_contexts}=    Get Context Ids    Active    Active
    IF    $current_contexts == []
        New Context
    END
    ${timeout}=    Set Browser Timeout    2 seconds
    Set Suite Variable    ${ORIGINAL_TIMEOUT}    1s

Restore Library Timeout
    Set Browser Timeout    ${ORIGINAL_TIMEOUT}
