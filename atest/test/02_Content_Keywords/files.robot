*** Settings ***
Resource         imports.resource

Test Setup       Set Library Timeout
Test Teardown    Run Keywords    Restore Library Timeout    AND    Wait For All Promises

Test Tags        slow

*** Variables ***
${CUSTOM_DL_PATH} =      ${CURDIR}/download_file
${ORIGINAL_TIMEOUT} =    1s

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

Upload Many Files
    New Context
    New Page    ${LOGIN_URL}
    Get Text    id=upload_result    ==    ${EMPTY}
    Upload File By Selector
    ...    id=multi_file_chooser
    ...    ${CURDIR}/__init__.robot
    ...    ${CURDIR}/assertions.robot
    ...    ${CURDIR}/files.robot
    ...    ${CURDIR}/__init__.robot
    VAR    @{exptected_list} =    __init__.robot    assertions.robot    files.robot    __init__.robot
    Check Upload Result    ${exptected_list}

Upload Files And Directories
    New Context
    New Page    ${LOGIN_URL}
    OperatingSystem.Create Directory    ${CURDIR}/tmp_dir
    OperatingSystem.Create File    ${CURDIR}/tmp_dir/tmp_file1.txt
    OperatingSystem.Create File    ${CURDIR}/tmp_dir/tmp_file2.txt
    OperatingSystem.Create Directory    ${CURDIR}/tmp_dir/not_from_here
    OperatingSystem.Create File    ${CURDIR}/tmp_dir/not_from_here/tmp_file3.txt
    Get Text    id=upload_result    ==    ${EMPTY}
    Upload File By Selector
    ...    id=multi_file_chooser
    ...    ${CURDIR}/__init__.robot
    ...    ${CURDIR}/tmp_dir
    ...    ${CURDIR}/__init__.robot
    VAR    @{exptected_list} =    __init__.robot    tmp_file1.txt    tmp_file2.txt    __init__.robot
    Check Upload Result    ${exptected_list}
    [Teardown]    OperatingSystem.Remove Directory    ${CURDIR}/tmp_dir    recursive=True

Upload File As Buffer
    New Context
    New Page    ${LOGIN_URL}
    ${text} =    Get File    ${CURDIR}/__init__.robot
    VAR    &{buffer} =    name=not_here.txt    mimeType=text/plain    buffer=${text}
    Upload File By Selector    id=file_chooser    ${buffer}
    Get Text    id=upload_result    ==    not_here.txt

Upload Large File As Buffer
    New Context
    New Page    ${LOGIN_URL}
    ${file_name} =    Generate Test Text File    ${10 000 000}
    ${text} =    Get File    ${CURDIR}/${file_name}
    Log    ${text}[:100]    formatter=repr
    VAR    &{buffer} =    name=large_not_here.txt    mimeType=text/plain    buffer=${text}
    Upload File By Selector    id=file_chooser    ${buffer}
    Get Text    id=upload_result    ==    large_not_here.txt
    [Teardown]    Remove File    ${CURDIR}/${file_name}

Upload File With Different Name
    Upload Named File    invalid_test_upload_file

Invalid Upload Path
    New Page    ${LOGIN_URL}
    Run Keyword And Expect Error
    ...    ValueError: Nonexistent input file path*
    ...    Upload File By Selector    \#file_chooser    NonExistentFile

Relative Upload Path
    [Tags]    no-docker-pr
    New Page    ${LOGIN_URL}
    File Should Exist    atest${/}test${/}02_Content_Keywords${/}test_upload_file
    Upload File By Selector    \#file_chooser    atest${/}test${/}02_Content_Keywords${/}test_upload_file

Relative Upload Path With Promise
    [Tags]    no-docker-pr
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

Wait For Download Not Finished
    New Context    acceptDownloads=True
    New Page    ${LOGIN_URL}
    ${dl_promise} =    Promise To Wait For Download    wait_for_finished=False
    Sleep    0.5
    Click    \#file_download
    ${file_object} =    Wait For    ${dl_promise}
    ${state} =    Get Download State    download=${file_object}
    Should Be True    $state['downloadID']
    Should Be Equal    ${state}[downloadID]    ${file_object}[downloadID]
    ${finished_download} =    Wait For Condition
    ...    download_state
    ...    ${file_object}
    ...    validate
    ...    value['state'] == 'finished'
    File Should Exist    ${finished_download}[saveAs]
    Should Be Equal    ${finished_download}[suggestedFilename]    test_download_file.js
    Remove File    ${finished_download}[saveAs]

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

Wait For Download That Starts Slower Than Browser Timeout
    New Context    acceptDownloads=True
    New Page    ${DOWNLOADS_URL}
    Set Browser Timeout    1s
    ${dl_promise} =    Promise To Wait For Download    download_timeout=10s
    Evaluate JavaScript    id=slow_start_download    (link) => link.click()
    ${file_object} =    Wait For    ${dl_promise}
    File Should Exist    ${file_object}[saveAs]
    Remove File    ${file_object}[saveAs]

Wait For Download Fails At Browser Timeout By Default
    New Context    acceptDownloads=True
    New Page
    Set Browser Timeout    1s
    ${dl_promise} =    Promise To Wait For Download
    Run Keyword And Expect Error    *Timeout 1000ms exceeded while waiting for event "download"*
    ...    Wait For    ${dl_promise}

Download Fails Without Crashing When File Is Not Fetched Within Download Timeout
    New Context    acceptDownloads=True
    New Page    ${DOWNLOADS_URL}
    Set Browser Timeout    1s
    Run Keyword And Expect Error    *Timeout 500ms exceeded while waiting for event "download"*
    ...    Download    ${ROOT_URL}api/download/slow?transferMs=2000    download_timeout=500ms
    Get Title    ==    Downloads

Wait For Download Relative To downloadsPath
    New Browser    ${BROWSER}    headless=${HEADLESS}    downloadsPath=${OUTPUT DIR}
    New Context    acceptDownloads=True
    New Page    ${LOGIN_URL}
    ${dl_promise} =    Promise To Wait For Download    saveAs=test_waitfordownload_file_saveAs.js
    Sleep    0.5
    Click    id=file_download
    ${file_object} =    Wait For    ${dl_promise}
    Log To Console    \n${file_object}
    ${download_url} =    Get Property    id=file_download    href
    ${download_file_object} =    Download    ${download_url}    saveAs=test_download_file_saveAs.js
    Log To Console    ${download_file_object}
    Close Browser
    File Should Exist    ${file_object}[saveAs]
    File Should Exist    ${OUTPUT DIR}/test_waitfordownload_file_saveAs.js
    Should Be Equal    ${file_object}[suggestedFilename]    test_download_file.js
    Remove File    ${file_object}[saveAs]
    File Should Exist    ${download_file_object}[saveAs]
    File Should Exist    ${OUTPUT DIR}/test_download_file_saveAs.js
    Remove File    ${download_file_object}[saveAs]

Wait For Download With Remote Browser
    [Setup]    Launch And Connect To Remote Browser
    New Context    acceptDownloads=True
    New Page    ${LOGIN_URL}
    ${dl_promise} =    Promise To Wait For Download    saveAs=persistent_downloads
    Click    \#file_download
    ${file_object} =    Wait For    ${dl_promise}
    File Should Exist    ${file_object}[saveAs]
    Should Be Equal    ${file_object}[suggestedFilename]    test_download_file.js
    Remove File    ${file_object}[saveAs]
    [Teardown]    Close Remote Browser

Wait For Download With Remote Browser Without SaveAs
    [Setup]    Launch And Connect To Remote Browser
    New Context    acceptDownloads=True
    New Page    ${LOGIN_URL}
    ${dl_promise} =    Promise To Wait For Download
    Click    \#file_download
    Run Keyword And Expect Error
    ...    *Path is not available when connecting remotely. Use saveAs() to save a local copy.
    ...    Wait For    ${dl_promise}
    [Teardown]    Close Remote Browser

Get Download State Saves A Download To saveAs When It Has Finished
    New Context    acceptDownloads=True
    New Page    ${LOGIN_URL}
    VAR    ${target} =    ${OUTPUT_DIR}${/}download-later${/}test_download_file.js
    ${dl_promise} =    Promise To Wait For Download    saveAs=${target}    wait_for_finished=False
    Click    id=file_download
    ${download} =    Wait For    ${dl_promise}
    Should Be Equal    ${download}[state]    in_progress
    Should Be Empty    ${download}[saveAs]
    ${finished} =    Wait For Condition
    ...    download_state
    ...    ${download}
    ...    validate
    ...    value['state'] == 'finished'
    Paths Should Be Equal    ${finished}[saveAs]    ${target}
    File Should Not Be Empty    ${target}
    ${again} =    Get Download State    ${download}
    Should Be Equal    ${again}[state]    finished
    Paths Should Be Equal    ${again}[saveAs]    ${target}
    [Teardown]    Remove Directory    ${OUTPUT_DIR}${/}download-later    recursive=True

Download Not Waiting For The End Is Saved To saveAs Later
    New Context    acceptDownloads=True
    New Page    ${DOWNLOADS_URL}
    VAR    ${target} =    ${OUTPUT_DIR}${/}download-keyword-later${/}slow_download.txt
    ${download} =    Download
    ...    ${ROOT_URL}api/download/slow?transferMs=1000
    ...    saveAs=${target}
    ...    wait_for_finished=False
    Should Be Equal    ${download}[state]    in_progress
    Should Be Empty    ${download}[saveAs]
    ${finished} =    Wait For Condition
    ...    download_state
    ...    ${download}
    ...    validate
    ...    value['state'] == 'finished'
    Paths Should Be Equal    ${finished}[saveAs]    ${target}
    ${content} =    Get File    ${target}
    Should Be Equal    ${content}    xxxxxxxxxx
    [Teardown]    Remove Directory    ${OUTPUT_DIR}${/}download-keyword-later    recursive=True

Cancel Download Stops A Running Download
    New Context    acceptDownloads=True
    New Page    ${DOWNLOADS_URL}
    ${dl_promise} =    Promise To Wait For Download    wait_for_finished=False
    Click    id=slow_transfer_download
    ${download} =    Wait For    ${dl_promise}
    Should Be Equal    ${download}[state]    in_progress
    Cancel Download    ${download}
    ${state} =    Get Download State    ${download}
    Should Be Equal    ${state}[state]    canceled
    Should Be Empty    ${state}[saveAs]

Cancel Download Accepts The Download Id
    New Context    acceptDownloads=True
    New Page    ${DOWNLOADS_URL}
    ${dl_promise} =    Promise To Wait For Download    wait_for_finished=False
    Click    id=slow_transfer_download
    ${download} =    Wait For    ${dl_promise}
    Cancel Download    ${download}[downloadID]
    ${state} =    Get Download State    ${download}[downloadID]
    Should Be Equal    ${state}[state]    canceled

Cancel Download After It Has Finished Keeps The File
    New Context    acceptDownloads=True
    New Page    ${LOGIN_URL}
    VAR    ${target} =    ${OUTPUT_DIR}${/}download-cancel-late${/}test_download_file.js
    ${dl_promise} =    Promise To Wait For Download    saveAs=${target}    wait_for_finished=False
    Click    id=file_download
    ${download} =    Wait For    ${dl_promise}
    Wait For Condition    download_state    ${download}    validate    value['state'] == 'finished'
    Cancel Download    ${download}
    ${state} =    Get Download State    ${download}
    Should Be Equal    ${state}[state]    finished
    File Should Not Be Empty    ${target}
    [Teardown]    Remove Directory    ${OUTPUT_DIR}${/}download-cancel-late    recursive=True

Relative saveAs Without downloadsPath Is Not Relative To The Working Directory
    [Tags]    no-docker-pr
    New Context    acceptDownloads=True
    New Page    ${LOGIN_URL}
    # Today the Node process resolves it against its own working directory; issue #5620 changes this.
    ${dl_promise} =    Promise To Wait For Download    saveAs=pinned-relative-download.js
    Click    id=file_download
    ${download} =    Wait For    ${dl_promise}
    Should Be True    os.path.isabs($download['saveAs'])
    Should End With    ${download}[saveAs]    ${/}pinned-relative-download.js
    File Should Exist    ${download}[saveAs]
    File Should Not Exist    ${EXECDIR}${/}pinned-relative-download.js
    Remove File    ${download}[saveAs]

Relative downloadsPath Is Not Relative To The Working Directory
    [Tags]    no-docker-pr
    New Browser    ${BROWSER}    headless=${HEADLESS}    downloadsPath=pinned-relative-downloads
    New Context    acceptDownloads=True
    New Page    ${LOGIN_URL}
    # Today Playwright resolves it against the working directory of the Node process; issue #5620 changes this.
    ${dl_promise} =    Promise To Wait For Download    saveAs=test_download_file.js
    Click    id=file_download
    ${download} =    Wait For    ${dl_promise}
    Should End With    ${download}[saveAs]    pinned-relative-downloads${/}test_download_file.js
    File Should Exist    ${download}[saveAs]
    Directory Should Not Exist    ${EXECDIR}${/}pinned-relative-downloads
    Remove Directory    ${{ os.path.dirname($download['saveAs']) }}    recursive=True
    [Teardown]    Close Browser

*** Keywords ***
Paths Should Be Equal
    [Arguments]    ${actual}    ${expected}
    ${actual} =    Normalize Path    ${actual}
    ${expected} =    Normalize Path    ${expected}
    Should Be Equal    ${actual}    ${expected}

Launch And Connect To Remote Browser
    ${ws} =    Launch Browser Server    headless=${HEADLESS}
    Connect To Browser    wsEndpoint=${ws}
    Set Browser Timeout    90 seconds

Close Remote Browser
    Wait For All Promises
    Restore Library Timeout
    Close Browser

Set Library Timeout
    ${open_browsers} =    Get Browser Ids
    IF    $open_browsers == []
        New Browser    ${BROWSER}    headless=${HEADLESS}
    END
    ${current_contexts} =    Get Context Ids    Active    Active
    IF    $current_contexts == []    New Context
    Set Browser Timeout    90 seconds

Restore Library Timeout
    Set Browser Timeout    ${ORIGINAL_TIMEOUT}

Generate Test File
    [Arguments]    ${size_in_mb}
    VAR    ${filename} =    ${size_in_mb}MB
    ${size_in_bytes} =    Evaluate    1024 * ${size_in_mb}
    IF    os.sys.platform.startswith('win32')
        Run    fsutil file createNew ${CURDIR}/${filename}.file ${${size_in_bytes}*1024}
    ELSE
        Run    dd if=/dev/zero of=${CURDIR}/${filename}.file bs=1024 count=${size_in_bytes}
    END
    RETURN    ${filename}.file

Generate Test Text File
    [Arguments]    ${length_of_text}
    VAR    ${filename} =    ${length_of_text}.txt
    ${length_of_text} =    Convert To Integer    ${length_of_text}
    ${full_path} =    Normalize Path    ${CURDIR}${/}${filename}
    Evaluate
    ...    open(r'${full_path}', 'w').write(''.join(random.choices(string.ascii_letters + string.digits, k=${length_of_text})))
    ...    random,string
    RETURN    ${filename}

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
    Get Text    \#upload_result    ==    ${file_name}

Check Upload Result
    [Documentation]    Sometimes upload of files happen in different order than they are listed in the file chooser.
    [Arguments]    ${expected}
    ${result} =    Get Text    id=upload_result
    ${result_list} =    Split String    ${result}    ,
    Sort List    ${expected}
    Sort List    ${result_list}
    Lists Should Be Equal    ${result_list}    ${expected}

Upload With Promise
    [Arguments]    ${file_name}
    New Page    ${LOGIN_URL}
    ${promise} =    Promise To Upload File    ${file_name}
    Click    \#file_chooser
    Wait For    ${promise}
