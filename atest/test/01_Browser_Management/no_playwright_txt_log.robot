*** Settings ***
Resource        imports.resource

Test Tags       no-coverage-support    no-windows-support

*** Test Cases ***
This should not be logged to file playwright-log.txt
    [Documentation]    This is prerequisite for test cases in this suite.
    Log    This should not be logged to file
    FOR    ${i}    IN RANGE    5
        Log    This should not be logged to file ${i}
    END
    IF    ${True}    Log    This should not be logged to file

Read playwright_log.txt and verify that the above keyword or test are not present
    ${log_file} =    Find Playwright Log File
    ${log} =    Get File    ${log_file}
    Log    ${log}
    Should Not Contain    ${log}    This should not be logged to file playwright-log.txt
    Should Not Contain    ${log}    Dummy Keyword For Log File Checking
    Should Not Contain    ${log}    This should not be logged to file
    Should Not Be Empty    ${log}

*** Keywords ***
Dummy Keyword For Log File Checking
    Log    This should not be logged to file

Find Playwright Log File
    ${files} =    List Files In Directory    ${OUTPUT_DIR}
    IF    'playwright-log.txt' in ${files}
        RETURN    ${OUTPUT_DIR}/playwright-log.txt
    ELSE
        ${files} =    List Files In Directory    ${OUTPUT_DIR}/..
        IF    'playwright-log.txt' in ${files}
            RETURN    ${OUTPUT_DIR}/../playwright-log.txt
        ELSE
            ${files} =    List Files In Directory    ${OUTPUT_DIR}/../..
            IF    'playwright-log.txt' in ${files}
                RETURN    ${OUTPUT_DIR}/../../playwright-log.txt
            END
        END
    END
    Fail    Playwright log file not found in ${OUTPUT_DIR} or its parent directories
