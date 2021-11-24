*** Settings ***
Resource            imports.resource

Test Setup          Set Library Timeout
Test Teardown       Run Keywords    Restore Library Timeout    AND    Wait For All Promises

*** Variables ***
${CUSTOM_DL_PATH} =     ${CURDIR}/download_file

*** Test Cases ***
Upload upload_test_file
    Upload Named File    test_upload_file

Upload 75MB file
    [Tags]    no-windows-support
    [Timeout]    1 minute
    Run Keyword And Expect Error    Error: fileChooser.setFiles: fileChooser.setFiles: Target closed
    ...    Upload Sized File    75
    # The browser actually gets a bit stuck so it needs to be cleaned up properly here.
    Close Browser

Upload 1MB file
    Upload Sized File    1

Upload 74MB file
    [Timeout]    1 minute
    Upload Sized File    74

Upload File By Selector
    New Page    ${LOGIN_URL}
    Get Text    \#upload_result    ==    ${EMPTY}
    Generate Test File    5
    Upload File By Selector    \#file_chooser    ${CURDIR}/5MB.file
    Remove File    ${CURDIR}/5MB.file

Upload File with different name
    New Page    ${LOGIN_URL}
    Promise to Upload File    ${CURDIR}/invalid_test_upload_file
    Click    \#file_chooser
    Get Text    \#upload_result    ==    invalid_test_upload_file

Invalid Upload Path
    ${promise} =    Promise to Upload File    NonExistentFile
    IF    os.sys.platform.startswith('win32')
        Run Keyword And Expect Error
        ...    STARTS: FileNotFoundError: [WinError 2] The system cannot find the file specified: 'NonExistentFile'
        ...    Wait For    ${promise}
    ELSE
        Run Keyword And Expect Error    STARTS: FileNotFoundError: [Errno 2] No such file or directory:    Wait For
        ...    ${promise}
    END
    Wait For All Promises

Wait For Download
    New Context    acceptDownloads=True
    New Page    ${LOGIN_URL}
    ${dl_promise} =    Promise To Wait for Download
    Sleep    0.5
    Click    \#file_download
    ${file_object} =    Wait For    ${dl_promise}
    File Should Exist    ${file_object}[saveAs]
    Should Be Equal    ${file_object}[suggestedFilename]    test_download_file.js
    Remove File    ${file_object}[saveAs]

Wait For Download With Custom Path
    New Context    acceptDownloads=True
    New Page    ${LOGIN_URL}
    ${dl_promise} =    Promise To Wait For Download    saveAs=${CUSTOM_DL_PATH}
    Sleep    0.5
    Click    \#file_download
    ${file_object} =    Wait For    ${dl_promise}
    File Should Exist    ${file_object.saveAs}
    Should Be Equal    ${file_object.suggestedFilename}    test_download_file.js
    File Should Exist    ${CUSTOM_DL_PATH}
    Remove File    ${CUSTOM_DL_PATH}
    Remove File    ${file_object.saveAs}

*** Keywords ***
Set Library Timeout
    ${open_browsers} =    Get Browser Ids
    IF    $open_browsers == []
        New Browser    ${BROWSER}    headless=${HEADLESS}
    END
    ${current_contexts} =    Get Context Ids    Active    Active
    IF    $current_contexts == []
        New Context
    END
    IF    os.sys.platform.startswith('win32')
        ${timeout} =    Set Browser Timeout    60 seconds
    ELSE
        ${timeout} =    Set Browser Timeout    30 seconds
    END
    Set Suite Variable    ${ORIGINAL_TIMEOUT}    1s

Restore Library Timeout
    Set Browser Timeout    ${ORIGINAL_TIMEOUT}

Generate Test File
    [Arguments]    ${size_in_mb}
    ${filename} =    Set Variable    ${size_in_mb}MB
    ${size_in_bytes} =    Evaluate    1024 * ${size_in_mb}
    Run    dd if=/dev/zero of=${CURDIR}/${filename}.file bs=1024 count=${size_in_bytes}

    [Return]    ${filename}.file

Upload Sized File
    [Arguments]    ${size_in_mb}

    ${file_name} =    Generate Test File    ${size_in_mb}
    Upload Named File    ${file_name}

    [Teardown]    Remove File    ${CURDIR}/${file_name}

Upload Named File
    [Arguments]    ${file_name}
    New Context
    New Page    ${LOGIN_URL}
    Get Text    \#upload_result    ==    ${EMPTY}
    ${promise} =    Promise to Upload File    ${CURDIR}/${file_name}
    Click    \#file_chooser
    Wait For    ${promise}
    ${result_name} =    Get Text    \#upload_result
    Get Text    \#upload_result    ==    ${file_name}
