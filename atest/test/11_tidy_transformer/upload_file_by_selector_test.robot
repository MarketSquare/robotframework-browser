*** Settings ***
Resource            imports.resource

Test Setup          Upload File By Selector Setup
Test Teardown       Upload File By Selector Treardown

*** Test Cases ***
Tranform Upload File By Selector Keyword To Varargs
    ${entry_cmd} =    Get Enty Command
    ${process} =    Run Process
    ...    ${entry_cmd} transform --upload-file-by-selector ${CURDIR}/upload_file_by_selector_file.robot
    ...    shell=True
    Log    ${process.stdout}
    Log    ${process.stderr}
    Should Be Equal As Integers    ${process.rc}    0
    ${file} =    Get File    ${CURDIR}/upload_file_by_selector_file.robot
    ${lines} =    Split To Lines    ${file}
    Log    ${lines}
    Should Be Equal    ${lines}[5]    ${SPACE*4}\${not used} =${SPACE*4}New Context${SPACE*4}\# This is not changed
    Should Be Equal    ${lines}[6]    ${SPACE*4}Upload File By Selector${SPACE*4}id=file${SPACE*4}file.txt${SPACE*4}\# This is not changed
    Should Be Equal    ${lines}[7]    ${SPACE*4}Upload File By Selector${SPACE*4}selector=id=file${SPACE*4}file.txt

*** Keywords ***
Upload File By Selector Setup
    ${TRANSFORM_UPLOAD_FILE_BY_SELECTOR_DATA} =    Get File    ${CURDIR}/upload_file_by_selector_file.robot
    Set Test Variable    ${TRANSFORM_UPLOAD_FILE_BY_SELECTOR_DATA}

Upload File By Selector Treardown
    Create File    ${CURDIR}/upload_file_by_selector_file.robot    ${TRANSFORM_UPLOAD_FILE_BY_SELECTOR_DATA}
