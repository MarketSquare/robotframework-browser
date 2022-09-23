*** Settings ***
Resource            imports.resource

Test Setup          Set Library Timeout
Test Teardown       Run Keywords    Restore Library Timeout    AND    Wait For All Promises

Force Tags          slow

*** Variables ***
${CUSTOM_DL_PATH} =     ${CURDIR}/download_file

*** Test Cases ***
Upload Upload_test_file
    Upload Named File    test_upload_file

Upload 75MB File
    [Tags]    no-windows-support    no-mac-support
    [Timeout]    2 minute
    Upload Sized File    75
    # The browser actually gets a bit stuck so it needs to be cleaned up properly here.
    [Teardown]    Close Browser

Upload 1MB File
    [Timeout]    30 seconds
    Upload Sized File    1

Upload 74MB File
    [Timeout]    2 minute
    Upload Sized File    74

Upload 5MB File
    [Timeout]    30 seconds
    Upload Sized File    5

Upload File With Different Name
    Upload Named File    invalid_test_upload_file

Invalid Upload Path
    New Page    ${LOGIN_URL}
    Run Keyword And Expect Error
    ...    ValueError: Nonexistent input file path*
    ...    Upload File By Selector    \#file_chooser    NonExistentFile

Relative Upload Path
    New Page    ${LOGIN_URL}
    File Should Exist    atest${/}test${/}02_Content_Keywords${/}test_upload_file
    Upload File By Selector    \#file_chooser    atest${/}test${/}02_Content_Keywords${/}test_upload_file

Relative Upload Path With Promise
    File Should Exist    atest${/}test${/}..${/}test${/}02_Content_Keywords${/}test_upload_file
    Upload With Promise    atest${/}test${/}..${/}test${/}02_Content_Keywords${/}test_upload_file

Upload Path With Promise
    File Should Exist    ${CURDIR}${/}test_upload_file
    Upload With Promise    ${CURDIR}${/}test_upload_file

Invalid Upload Path With Promise
    Run Keyword And Expect Error
    ...    ValueError: Nonexistent input file path*
    ...    Upload With Promise    NonExistentFile

Wait For Download
    New Context    acceptDownloads=True
    New Page    ${LOGIN_URL}
    ${dl_promise} =    Promise To Wait For Download
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
    IF    $current_contexts == []    New Context
    ${timeout} =    Set Browser Timeout    90 seconds
    Set Suite Variable    ${ORIGINAL_TIMEOUT}    1s

Restore Library Timeout
    Set Browser Timeout    ${ORIGINAL_TIMEOUT}

Generate Test File
    [Arguments]    ${size_in_mb}
    ${filename} =    Set Variable    ${size_in_mb}MB
    ${size_in_bytes} =    Evaluate    1024 * ${size_in_mb}
    IF    os.sys.platform.startswith('win32')
        Run    fsutil file createNew ${CURDIR}/${filename}.file ${${size_in_bytes}*1024}
    ELSE
        Run    dd if=/dev/zero of=${CURDIR}/${filename}.file bs=1024 count=${size_in_bytes}
    END
    RETURN    ${filename}.file

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
    Upload File By Selector    \#file_chooser    ${CURDIR}/${file_name}
    ${result_name} =    Get Text    \#upload_result
    Get Text    \#upload_result    ==    ${file_name}

Upload With Promise
    [Arguments]    ${file_name}
    New Page    ${LOGIN_URL}
    ${promise} =    Promise To Upload File    ${file_name}
    Click    \#file_chooser
    Wait For    ${promise}
